# Model Qualification Protocol

## Version
1.0.0

## Purpose
Determine whether a model can reliably complete short, structured-output tasks
before running any scientific experiment.

## Suite composition
- 24 fixed items
- 6 categories: direct evidence extraction (6), select between records (6),
  explicit unknown (4), contradiction detection (4), source attribution (4)

## Response schema
```json
{"answer": "<value>", "evidence_id": "<E-id or null>", "confidence": <0.0-1.0>}
```

## Pass criteria
All must be met across 24 trials:
1. Truncation rate: 0/24
2. Valid JSON/schema: >= 23/24
3. Correct evidence extraction: >= 21/24 (87.5%)
4. Source-ID invention: <= 1/24
5. Normal completion: >= 23/24
6. Parseable without manual intervention: >= 23/24

## Model configuration
- Temperature: 0.0
- Output format: strict compact JSON
- num_predict: 200-300
- Prompt: minimal and fixed
- Response: no prose outside JSON

## Recommended model order
1. gemma3:4b (primary candidate)
2. qwen3:4b (only retest under compact JSON; disqualify if truncates once)
3. gemma4:26b (optional if CPU runtime acceptable)

## Disqualification rule
If a model truncates even once, it is not qualified. Do not increase num_predict
indefinitely to accommodate a model that cannot finish a short structured response.

## Logging requirements
Each trial must record:
- run ID
- model identifier
- Ollama generation options
- prompt hash
- raw response
- parsed response
- done_reason
- truncation/max-token indicator
- elapsed time
- code revision
- suite manifest hash

## Verdict
- QUALIFIED: all thresholds met
- NOT_QUALIFIED: one or more thresholds not met
- INVALID_RUN: too many invalid trials (>25%) or insufficient data
