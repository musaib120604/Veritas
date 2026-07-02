"""
Fine-tuning entry point for Veritas.

This is a stub — wire it up to whichever fine-tuning route you pick:

  A) Hosted fine-tuning API (e.g. OpenAI/Anthropic-style job submission)
     - upload data/train.jsonl (see prepare_dataset.py)
     - submit a fine-tune job, poll for completion
     - point backend/inference.py at the resulting model id

  B) Local fine-tuning (LoRA/QLoRA on an open-weight base model)
     - requires a GPU; not practical from Termux directly
     - train elsewhere (Colab/cloud), pull weights back down

Usage:
    python train.py --data data/train.jsonl --epochs 3
"""

import argparse
import json


def load_jsonl(path: str) -> list:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="path to train.jsonl")
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()

    records = load_jsonl(args.data)
    print(f"Loaded {len(records)} training examples.")
    print("TODO: submit fine-tune job or launch local training loop here.")
    print(f"Requested epochs: {args.epochs}")


if __name__ == "__main__":
    main()
