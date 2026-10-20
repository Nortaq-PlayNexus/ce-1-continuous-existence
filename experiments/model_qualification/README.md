# Model Qualification Suite

## Purpose

Determine whether a model can reliably complete short, structured-output tasks
before running any scientific experiment. This is a **qualification gate**, not
an experiment. It tests:

- JSON completion
- Output schema adherence
- Normal termination (no truncation)
- Basic use of explicitly supplied evidence
- Non-invention of source IDs

It must **not** be presented as evidence about memory, continuity, consciousness,
or selfhood.

## Pass criteria (all must be met across 24 fixed trials)

| Requirement | Pass threshold |
|---|---:|
| Truncation rate | 0/24 |
| Valid JSON/schema | at least 23/24 |
| Correct supplied-evidence extraction | at least 21/24 (87.5%) |
| Unsupported source-ID invention | no more than 1/24 |
| Completion mode | at least 23/24 normal-stop outcomes |
| Automated scoring compatibility | at least 23/24 parseable without manual intervention |

## Response format

Compact JSON with exactly three fields:

```json
{"answer": "<value>", "evidence_id": "<E-id>", "confidence": <0.0-1.0>}
```

## Usage

```bash
# Dry run (no model calls)
python run_qualification.py --suite qualification_suite.jsonl --output results.jsonl

# Score results
python score_qualification.py --results results.jsonl --suite qualification_suite.jsonl --output scores.json

# Analyze verdict
python analyze_qualification.py --scores scores.json --output verdict.json
```

## Important

- Do not run live model calls without explicit authorization.
- The suite has exactly 24 fixed items. Do not modify them after freezing.
- All randomization uses recorded fixed seeds.
- No network or Ollama calls occur during tests.
- Raw answer keys never enter a model prompt.
