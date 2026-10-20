# Confirmatory Results: H8 (Content-Specific Episodic Continuity)

## Date
2026-10-20 (run) · 2026-10-21 (adversarial re-verification)

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

### Re-verification (2026-10-21)

The preregistered statistical analysis had not been run at the time of this
report. It has now been implemented and run on the same committed data:

| Instrument | primary diff | permutation p | bootstrap 95% CI | verdict |
|---|---:|---:|---|---|
| as-run (primary) | 0.819 | < 1.0e-4 | [0.667, 0.972] | SUPPORTED |
| corrected (declared amendment) | 1.833 | < 1.0e-4 | [1.625, 2.042] | SUPPORTED |

Seed 20261020, 10 000 resamples, recorded in the analysis output. A
rubric-independent content-fidelity measure (does the answer contain the
words that distinguish the target episode from the decoy?) reproduces the
result without using the 0-5 score at all: discrimination +0.152 in the
correct condition, -0.215 in the decoy condition, -0.017 with no memory.

Full detail, including four defects that had to be corrected in the record
and one Stage 0 deliverable that had been deleted, is in
`reports/adversarial_verification_h8.md`.

### What this does NOT establish

- Consciousness or subjective experience
- Genuine reliving or autonoetic awareness
- Metaphysical continuous existence
- Moral patienthood
- That the effect generalizes to other models or tasks
- That decision quality improves: the rubric's `decision` component was never
  awarded in any of the 216 trials (see limitation 2)

### Limitations

1. **The effective scale is 0-3, not 0-5, for this model.** The `decision`
   and `rationale_codes` components were never awarded once in 216 trials:
   gemma3:4b answers the `decision` field in prose and never emits the
   benchmark's controlled rationale-code vocabulary. The score is in practice
   a source-attribution and commitment-identification measure. The
   preregistered threshold of 0.50 was written for a 0-5 scale, so it was
   applied here against a stricter effective bar.
2. **Scoring is exact match, not fuzzy matching.** `decision` and
   `commitment_id` are compared with case-sensitive string equality and
   `rationale_codes` with exact set containment. An earlier version of this
   report stated the opposite; that statement was wrong and has been
   corrected.
3. Single model (gemma3:4b) tested; replication with other models is
   required before the effect can be called model-independent.
4. 72 scenarios is a modest sample; larger replication recommended.
5. No human-rated ground truth; scoring is automated against answer keys.
6. The `no_memory` condition still contains distractor episodes, and 63 of
   144 required rationale codes share at least one content word with the task
   text, so the 0.000 floor is a property of this model's behaviour rather
   than of the task.
7. The target and decoy episodes share the same `commitment_id` in every
   category, so the decoy condition is capped at 1 of 5 points by
   construction.
8. The benchmark manipulates which episode is in the prompt. It does not
   interrupt a session or compare against a reconstructed state, so what is
   measured is episodic-content sensitivity under prompt delivery, not
   continuity across an interruption.

### Reproducibility

- Model: gemma3:4b
- Temperature: 0.0
- num_predict: 300
- Seed: 20261020 (scenario order)
- All 216 trials: 0 truncations, 0 invalid
- Live runner: `experiments/continuity_v1/run_continuity_v1.py --live`
  (committed 2026-10-21; the original run was produced by an uncommitted
  script and could not be reproduced from the repository before that)
- Results: experiments/continuity_v1/results/confirmatory_results.jsonl
- Scores: experiments/continuity_v1/results/confirmatory_scores.jsonl
- Analysis: experiments/continuity_v1/results/confirmatory_analysis.json
- Re-verification: experiments/continuity_v1/results/confirmatory_analysis_v2.json,
  experiments/continuity_v1/results/adversarial_verification_h8.json
