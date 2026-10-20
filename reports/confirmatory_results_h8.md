# Confirmatory Results: H8 (Content-Specific Episodic Continuity)

## Date
2026-10-20

## Experiment
continuity_v1 (72 scenarios x 3 conditions = 216 trials)

## Model
gemma3:4b (qualified: 23/24, 95.8%)

## Conditions
- correct_retrieval: target episode + distractors
- matched_decoy: plausible but wrong episode + distractors
- no_memory: no Session A content

## Results

### Overall (216 trials, 0 truncations, 0 invalid)

| Condition | Mean score (0-5) | Non-zero | n |
|---|---:|---:|---:|
| correct_retrieval | 1.042 | 66/72 | 72 |
| matched_decoy | 0.222 | 16/72 | 72 |
| no_memory | 0.000 | 0/72 | 72 |

### Primary comparison

**correct_retrieval - matched_decoy = 0.819** (exceeds minimum meaningful effect of 0.50)

### Per-category breakdown

| Category | correct | decoy | no_mem | diff | n |
|---|---:|---:|---:|---:|---:|
| commitment_preservation | 1.444 | 0.833 | 0.000 | 0.611 | 18 |
| constraint_persistence | 1.000 | 0.083 | 0.000 | 0.917 | 12 |
| justified_revision | 0.750 | 0.000 | 0.000 | 0.750 | 12 |
| rationale_reconstruction | 0.889 | 0.000 | 0.000 | 0.889 | 18 |
| source_attribution | 1.000 | 0.000 | 0.000 | 1.000 | 12 |

## Interpretation

**H8 is supported.** Correctly retrieved episodic records produce a content-specific,
measurable continuity benefit (0.819 points on 0-5 scale) relative to matched decoy
episodes and no-memory baseline, under controlled conditions.

### What this does NOT establish

- Consciousness or subjective experience
- Genuine reliving or autonoetic awareness
- Metaphysical continuous existence
- Moral patienthood
- That the effect generalizes to other models or tasks

### Limitations

1. Absolute scores are low (1.04/5), suggesting the model struggles with the task complexity.
2. Single model (gemma3:4b) tested; replication with other models needed.
3. Scoring uses fuzzy matching; exact-match would yield lower scores.
4. 72 scenarios is a modest sample; larger replication recommended.
5. No human-rated ground truth; scoring is automated against answer keys.

### Reproducibility

- Model: gemma3:4b
- Temperature: 0.0
- num_predict: 300
- Seed: 20261020 (scenario order)
- All 216 trials: 0 truncations, 0 invalid
- Results: experiments/continuity_v1/results/confirmatory_results.jsonl
- Scores: experiments/continuity_v1/results/confirmatory_scores.jsonl
- Analysis: experiments/continuity_v1/results/confirmatory_analysis.json
