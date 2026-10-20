# Preregistration: H8 Replication with a Second Model

## Date
2026-10-21 (written before the replication run, after the adversarial
verification of the gemma3:4b confirmatory run)

## Purpose
The gemma3:4b confirmatory run was adversarially re-verified on 2026-10-21.
The conclusion held, but one of its own stated limitations was not addressed:
the effect was measured on a single model. This preregistration fixes the
protocol for a replication on a second, independently qualified model, so that
the replication is a test rather than a demonstration.

## Hypothesis
**H8-R.** The same content-specific episodic continuity effect measured for
gemma3:4b holds for a second qualified model: correctly retrieved prior
episodes improve objective trajectory-continuity performance relative to
token-matched decoy episodes and a no-memory baseline.

## What is fixed in advance

Fixed by the existing preregistration and carried over unchanged:

- The benchmark: `benchmarks/continuity_v1/` — 72 scenarios, 3 conditions,
  216 trials. **Frozen.** No scenario, episode, decoy, answer key or prompt
  may change.
- The primary comparison: mean(score_correct_retrieval − score_matched_decoy),
  paired by scenario.
- The minimum meaningful effect: +0.50 on the 0-5 score.
- The analysis: paired permutation test (seed 20261020, 10 000 resamples) and
  scenario-level bootstrap CI (seed 20261020, 10 000 resamples), validity gate
  at >5% invalid → INVALID_RUN, ≥65 paired observations required.
- Model parameters: temperature 0.0, num_predict 300, seed 20261020 for the
  scenario order.

Fixed by this document:

- **Model selection rule.** The second model must first pass the model
  qualification suite (`experiments/model_qualification/qualification_protocol.md`)
  at the same thresholds gemma3:4b passed: 0/24 truncations, ≥23/24 valid
  JSON, ≥21/24 evidence extraction, ≥23/24 normal completion. A model that
  truncates even once is disqualified and the replication is NOT run with it.
- **Order of models.** qwen3:4b first (the protocol's own second choice),
  then dolphin-llama3:latest. The first model to pass qualification is used.
- **Decision rule.** H8-R is REPLICATED if the primary difference ≥ 0.50 AND
  the permutation p ≤ 0.05 AND the bootstrap CI lower bound > 0 AND the run is
  not INVALID_RUN. Otherwise H8-R is NOT REPLICATED, including the case of a
  null result. A null result is reported as a null result.
- **Report both instruments.** The as-run scorer and the corrected scorer, as
  for the original run.

## Falsification
If the second qualified model does not show the effect under the same
protocol, the gemma3:4b result is model-specific and H8 must be downgraded
from a general claim to a single-model observation.

## What a replication cannot establish
Replicating on a second model strengthens the claim that the effect is a
property of the model class rather than of one checkpoint. It does not
establish consciousness, subjective experience, reliving, moral patienthood,
or that the effect is a property of "continuous existence" in any sense
beyond prompt-delivered episodic content. Two local models on one CPU is
also not a substitute for independent replication by another laboratory.

## Stopping rule
One replication attempt per qualified model. No re-runs to "fix" a
disappointing result. If the run is INVALID_RUN (for example, the model
truncates), that is recorded as INVALID_RUN and the model is disqualified;
the next qualified model in the order is used, once.
