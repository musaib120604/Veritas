# Methodology

## Marker categories

Veritas scores statements against four categories of linguistic deception markers, drawn from deception-detection literature (statement analysis, criteria-based content analysis):

| Category | Signal | Weight |
|---|---|---|
| Hedging | qualifiers that soften a claim ("basically", "I think", "give or take") | 9 |
| Distancing | phrases that create emotional/psychological distance from the claim | 12 |
| Memory gaps | selective or convenient memory loss around key details | 14 |
| Tense shift | inconsistent verb tense within a single account | 10 |

Matched phrases are summed into a raw score, capped at 100.

- **0–29** → low likelihood of deception
- **30–64** → moderate — some markers present, worth a follow-up question
- **65–100** → high — multiple strong markers present

## Current implementation

`backend/inference.py` ships with a rule-based scorer (keyword + regex matching) so the API works without a trained model. This is intentionally simple and will produce false positives/negatives — it exists to define the input/output contract and give something demoable.

## Path to the LLM version

1. Collect labeled data (`model/prepare_dataset.py` expects `statement,label,source` CSV).
2. Convert to instruction-tuning format (JSONL).
3. Fine-tune (`model/train.py`) — hosted fine-tuning API recommended over local, since Termux has no GPU.
4. Replace the body of `score_statement()` in `backend/inference.py` with a call to the fine-tuned model, keeping the same return shape (`score`, `flags`, `verdict`) so the frontend doesn't need to change.

## Known limitations

- Rule-based scorer is keyword-driven and easy to fool with rephrasing.
- No ground-truth dataset is bundled — scores from the current version should not be treated as meaningful signal, only as a working demo of the pipeline.
- Text-only deception detection has real accuracy limits even with a trained model; treat output as a probabilistic signal, not a verdict.
