# Preregistration: H3 — Resumption After Interruption Without Full Reconstruction

## Date
2026-10-28 (written before any H3 run)

## Hypothesis
**H3.** After an interruption, a system that resumes from a persistent episodic
store produces measurably different (and better) continuation behaviour than a
system that resumes from an empty store, and the difference cannot be
attributed to prompt content, because the prompt text is controlled.

## What is fixed in advance

- The benchmark: `benchmarks/h3_interruption/` — 84 scenarios, 3 conditions,
  252 trials. Frozen. No scenario, episode, or prompt may change.
- Primary comparison: mean(score_store_populated − score_store_empty), paired
  by scenario.
- Minimum meaningful effect: +0.50 on the 0-6 scale.
- Analysis: paired permutation test (seed 20261020, 10 000 resamples) and
  scenario-level bootstrap CI (seed 20261020, 10 000 resamples), validity
  gate at >5% invalid → INVALID_RUN, ≥90% of scenarios required as paired
  observations.
- Model parameters: temperature 0.0, num_predict 300, seed 20261020 for the
  scenario order.
- Model selection: gemma3:4b (qualified 23/24, 95.8%).

## Conditions

- **store_populated:** after interruption, the model receives the stored
  episode from step 1 (retrieved from a persistent store). The prompt has
  the same structure as store_empty.
- **store_empty:** after interruption, the model receives nothing (the store
  is empty). Same prompt structure as store_populated.
- **reconstruct:** after interruption, the model receives the full transcript
  of step 1 (no store, just raw text).

The primary comparison is store_populated vs store_empty. If they differ, the
store provides continuity. The difference cannot be attributed to prompt
length or to the presence of the words, because the prompt text is controlled.

reconstruct is a secondary comparison: does retrieval match reconstruction?

## Falsification
If store_populated does not produce a measurable improvement over store_empty,
H3 is falsified. If store_populated ≈ reconstruct, retrieval is as good as
reconstruction (a positive finding about the store's efficiency).

## Decision rule
H3 is SUPPORTED if the primary difference ≥ 0.50 AND the permutation p ≤ 0.05
AND the bootstrap CI lower bound > 0 AND the run is not INVALID_RUN.
Otherwise it is NOT SUPPORTED or INVALID_RUN. A null result is reported as
a null result.

## What a positive result would NOT establish
- Consciousness, subjective experience, reliving, moral patienthood
- That the store provides *genuine* persistence (it is still prompt delivery)
- Generalisation beyond gemma3:4b

## Stopping rule
One run. No re-runs to "fix" a disappointing result.
