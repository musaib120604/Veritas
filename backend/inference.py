"""
Veritas inference module.

Scores a statement for linguistic deception markers and returns a
confidence score (0-100) plus the phrases that triggered each flag.

This ships with a rule-based scorer so the API is usable out of the box.
Swap `score_statement()` internals for a call to your fine-tuned LLM
once it's trained (see model/train.py) — the input/output contract
below is what backend/app.py expects, so nothing else needs to change.
"""

import re

# --- marker categories -----------------------------------------------
# Each marker adds weight toward the deception score when matched.
# Tune these lists / weights as the real dataset comes in.

HEDGES = [
    "basically", "honestly", "to be honest", "i guess", "kind of",
    "sort of", "i think", "i believe", "as far as i know",
    "give or take", "more or less", "i don't really remember",
    "i don't recall", "not sure", "probably",
]

DISTANCING = [
    "that person", "the individual", "not gonna lie", "no comment",
    "why would i", "i would never", "i swear", "trust me",
]

MEMORY_GAPS = [
    "don't remember", "can't recall", "blacked out", "don't know why",
    "i don't know", "no idea",
]

TENSE_SHIFT_HINTS = [
    r"\bwas\b.{0,40}\bis\b", r"\bis\b.{0,40}\bwas\b",
]

WEIGHTS = {
    "hedge": 9,
    "distancing": 12,
    "memory_gap": 14,
    "tense_shift": 10,
}


def _find_matches(text_lower, phrases):
    hits = []
    for phrase in phrases:
        for m in re.finditer(re.escape(phrase), text_lower):
            hits.append((m.start(), m.end(), phrase))
    return hits


def score_statement(statement: str) -> dict:
    """
    Returns:
        {
            "score": int 0-100,
            "flags": [{"phrase": str, "type": str, "start": int, "end": int}],
            "verdict": "low" | "moderate" | "high"
        }
    """
    text_lower = statement.lower()
    flags = []
    raw_score = 0

    for phrase, start, end, kind, weight in [
        (p, s, e, "hedge", WEIGHTS["hedge"])
        for (s, e, p) in _find_matches(text_lower, HEDGES)
    ] + [
        (p, s, e, "distancing", WEIGHTS["distancing"])
        for (s, e, p) in _find_matches(text_lower, DISTANCING)
    ] + [
        (p, s, e, "memory_gap", WEIGHTS["memory_gap"])
        for (s, e, p) in _find_matches(text_lower, MEMORY_GAPS)
    ]:
        flags.append({"phrase": phrase, "type": kind, "start": start, "end": end})
        raw_score += weight

    for pattern in TENSE_SHIFT_HINTS:
        if re.search(pattern, text_lower):
            raw_score += WEIGHTS["tense_shift"]
            flags.append({"phrase": "tense inconsistency", "type": "tense_shift",
                           "start": 0, "end": 0})

    # dedupe overlapping flags, cap score at 100
    score = min(100, raw_score)

    if score < 30:
        verdict = "low"
    elif score < 65:
        verdict = "moderate"
    else:
        verdict = "high"

    return {
        "score": score,
        "flags": flags,
        "verdict": verdict,
    }
