"""
Prepares a labeled dataset for fine-tuning a deception-detection model.

Expected input: a CSV with columns:
    statement   - raw text of the claim/statement
    label       - 1 (deceptive) or 0 (truthful)
    source      - dataset origin, e.g. "trial_transcripts", "custom"

Expected output: a JSONL file in instruction-tuning format:
    {"prompt": "...", "completion": "..."}

Usage:
    python prepare_dataset.py --input raw/statements.csv --output data/train.jsonl
"""

import argparse
import csv
import json


PROMPT_TEMPLATE = (
    "Analyze the following statement for signs of deception. "
    "Return a score from 0-100 and list the phrases that support your score.\n\n"
    "Statement: \"{statement}\""
)


def build_completion(label: int) -> str:
    if label == 1:
        return "Score: 70+\nVerdict: likely deceptive"
    return "Score: <30\nVerdict: likely truthful"


def convert(input_path: str, output_path: str) -> None:
    count = 0
    with open(input_path, newline="", encoding="utf-8") as f_in, \
         open(output_path, "w", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)
        for row in reader:
            statement = row.get("statement", "").strip()
            label_raw = row.get("label", "").strip()
            if not statement or label_raw not in ("0", "1"):
                continue

            record = {
                "prompt": PROMPT_TEMPLATE.format(statement=statement),
                "completion": build_completion(int(label_raw)),
            }
            f_out.write(json.dumps(record) + "\n")
            count += 1

    print(f"Wrote {count} examples to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="path to raw CSV")
    parser.add_argument("--output", required=True, help="path to output JSONL")
    args = parser.parse_args()
    convert(args.input, args.output)
