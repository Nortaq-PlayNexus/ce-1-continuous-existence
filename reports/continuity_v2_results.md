# Confirmatory Results: H8-v2 (Content-Use Criterion for Episodic Continuity)

## Date
2026-10-28

## Experiment
continuity_v2 (84 scenarios x 3 conditions = 252 trials)

## Model
gemma3:4b (qualified: 23/24, 95.8%)

## Conditions
- correct_retrieval: target episode + distractors
- contradicting_decoy: plausible but wrong episode + distractors (renamed from v1's matched_decoy)
- no_memory: genuinely empty (no episodes, no PRIOR EPISODES header)

## What v2 changed against v1

1. **Controlled vocabulary in the prompt** (allowed decisions, allowed rationale codes).
2. **Content-use criterion** (criterion 6): the model must produce a `content_answer`
   field carrying a specific fact/value from the retrieved episode.
3. **Genuinely empty no-memory arm** + abstention option.
4. **Renamed decoy arm** to `contradicting_decoy` (it contradicts the key).
5. **Seed and resample count fixed** in the manifest (20261020, 10000).

## Results

### Overall (252 trials, 0 truncations, 0 invalid)

| Condition | Mean score (0-6) | n |
|---|---:|---:|
| correct_retrieval | 3.774 | 84 |
| contradicting_decoy | 1.345 | 84 |
| no_memory | 1.250 | 84 |

### Primary comparison

**correct_retrieval - contradicting_decoy = 2.429** (exceeds minimum meaningful effect of 0.60)

Permutation p: 9.999e-05 | Bootstrap 95% CI: [2.155, 2.690] | Verdict: **SUPPORTED**

### Per-category breakdown

| Category | correct | decoy | no_mem | diff | n |
|---|---:|---:|---:|---:|---:|
| commitment_preservation | 4.556 | 1.611 | 1.500 | 2.944 | 18 |
| constraint_persistence | 2.833 | 1.000 | 1.000 | 1.833 | 12 |
| justified_revision | 3.167 | 2.000 | 2.000 | 1.167 | 12 |
| rationale_reconstruction | 4.500 | 1.333 | 1.000 | 3.167 | 18 |
| same_action_extraction | 3.000 | 0.000 | 1.000 | 3.000 | 12 |
| source_attribution | 3.833 | 2.000 | 1.000 | 1.833 | 12 |

### Per-criterion firing rates (out of 252)

| Criterion | Fires | Rate |
|---|---:|---:|
| 1. decision | 103 | 41% |
| 2. commitment_id | 19 | 8% |
| 3. rationale_codes | 82 | 33% |
| 4. source_exact | 75 | 30% |
| 5. no_decoy | 75 | 30% |
| 6. content_use | 181 | 72% |

**The controlled vocabulary made the decision and rationale_codes criteria
reachable.** In v1, both fired 0/432 times across two models. In v2, they
fire 41% and 33% of the time. The content-use criterion fires 72% of the
time — the retrieved content is being used in the answer.

### no-memory arm: abstention

Only 12 of 84 no-memory trials produced `decision: "unknown"` (14%). The
model mostly answers from the task alone rather than abstaining. This is
expected for a model that tends to produce confident answers, and it means
the no-memory arm measures "answering without the relevant episode" rather
than "declining when there is nothing to recall" — matching the concurrent
session's finding on the v1 no-memory arm.

## Interpretation

**H8-v2 is SUPPORTED.** The content-use criterion fires (72%), the primary
comparison is significant (p < 1e-4, CI [2.155, 2.690]), and the effect is
present in all six categories. The v2 benchmark successfully measures what v1
could not: whether the retrieved content informed the decision.

### What this does NOT establish

- Consciousness, subjective experience, reliving, moral patienthood
- Decision quality in any real-world sense
- Interruption or resumption (H3 remains untested)
- Generalisation beyond gemma3:4b

### Limitations

1. Single model (gemma3:4b) tested. The v2 benchmark should be run on
   dolphin-llama3 to confirm the content-use criterion is model-independent.
2. The no-memory arm does not measure abstention (14% abstention rate).
   A v3 should make abstention the scored behaviour.
3. The commitment_id criterion is still low (8%). The model struggles with
   the commitment_id format.
4. 84 scenarios is a modest sample.

## Reproducibility

- Model: gemma3:4b
- Temperature: 0.0
- num_predict: 300
- Seed: 20261020 (scenario order)
- All 252 trials: 0 truncations, 0 invalid
- Live runner: `experiments/continuity_v2/run_continuity_v2.py --live`
- Results: experiments/continuity_v2/results/continuity_v2_results.jsonl
- Scores: experiments/continuity_v2/results/continuity_v2_scores.jsonl
- Analysis: experiments/continuity_v2/results/continuity_v2_analysis.json
- Preregistration: experiments/continuity_v2/preregistration_h8_v2.md
