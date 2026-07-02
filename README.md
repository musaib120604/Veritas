# Veritas

An LLM fine-tuned to detect linguistic markers of deception in written statements.

Veritas doesn't analyze voice, face, or biometric signals — it works purely from text (transcripts, chat logs, written statements) and scores each claim against known deception patterns: hedging language, distancing pronouns, tense inconsistency, and detail imbalance. Output is a confidence score with the contributing phrases highlighted, not a binary verdict.

**[Live demo →](https://musaib120604.github.io/Veritas/)** _(https://veritasllm.vercel.app/)_

---

## How it works

1. **Statement intake** — raw text is split into individual claims so each is scored independently.
2. **Linguistic scan** — each claim is checked against known deception markers.
3. **Confidence score** — flagged claims are weighted into a single 0–100 score, with reasoning kept visible.

## Tech stack

| Layer | Tool |
|---|---|
| Model | Fine-tuned LLM |
| Backend | Python / Flask |
| Interface | HTML / CSS / JS |
| Hosting | GitHub Pages |

## Project structure

```
veritas/
├── index.html          # landing page
├── README.md
├── model/               # fine-tuning scripts, dataset prep
├── backend/             # Flask API serving inference
└── docs/                # writeup, methodology
```

## Setup (Termux)

```bash
pkg install git python -y
git clone https://github.com/musaib120604/Veritas.git
cd Veritas
pip install -r backend/requirements.txt
```

## Roadmap

- [ ] Dataset collection + labeling
- [ ] Fine-tune base model on deception-marker corpus
- [ ] Flask inference API
- [ ] Landing page → live demo
- [ ] Evaluation against known deception-detection benchmarks

## Disclaimer

Veritas is a research/portfolio project, not a validated forensic or legal tool. Deception-detection from text alone has known limitations and should not be used to make decisions about real people.

## License

MIT
