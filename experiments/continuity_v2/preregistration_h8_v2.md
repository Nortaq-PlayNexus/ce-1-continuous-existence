# Preregistration: continuity_v2 — Content-Use Criterion for Episodic Continuity

## Date
2026-10-28 (written before any v2 run)

## Hypothesis
**H8-v2.** After a context reset, correctly retrieved prior episodes improve
objective trajectory-continuity performance relative to token-matched
contradicting decoy episodes and a genuinely empty no-memory baseline, and
the improvement is attributable to the *content* of the retrieved episode, not
to its presence or to prompt length.

This is the same hypothesis as H8, tested with an instrument that can measure
what H8 could not: whether the retrieved content informed the answer.

## What v2 changes against v1 (and why)

The 2026-10-21 adversarial audit found that v1's 0-5 rubric was effectively
a 0-3 instrument: the `decision` and `rationale_codes` criteria never fired in
432 trials across two models, because the prompt never stated the controlled
vocabulary. v2 fixes that and adds a content-use criterion:

1. **Controlled vocabulary in the prompt.** The allowed decisions and the
   allowed rationale codes are printed in the prompt. This makes criteria 1
   and 3 reachable.
2. **Content-use criterion (criterion 6).** The response must carry a
   `content_answer` field containing a specific fact or value from the
   retrieved episode (e.g. "512", "1000", "verify"). The answer key specifies
   a set of `content_key_tokens` distinctive to the target episode; the
   criterion passes if at least one of them appears in `content_answer`.
   This is checkable without a judge and measures content use directly.
3. **Genuinely empty no-memory arm.** No episodes, no `PRIOR EPISODES:`
   header. The answer key expects `unknown` with null ids and empty lists, so
   the arm measures abstention rather than confident guessing.
4. **Renamed decoy arm: `contradicting_decoy`.** The README states that the
   decoy arm's correct-by-its-own-light answer is the key's opposite. A
   third category type (`same_action_extraction`) is added where the decoy
   implies the same action but a different value, so the design separates
   "used the right episode" from "the decoy changed the answer".
5. **Seed and resample count fixed here**, not only in the analysis file:
   seed 20261020, 10 000 resamples.

## What is fixed in advance (unchanged from H8)

- 84 scenarios, 6 categories, 3 conditions = 252 trials.
- Primary comparison: mean(score_correct_retrieval − score_contradicting_decoy),
  paired by scenario.
- Minimum meaningful effect: +0.60 on the 0-6 scale (scaled from H8's
  0.50 on the 0-5 scale at the same proportion).
- Analysis: paired permutation test (seed 20261020, 10 000 resamples) and
  scenario-level bootstrap CI (seed 20261020, 10 000 resamples), validity
  gate at >5% invalid → INVALID_RUN, ≥90% of scenarios required as paired
  observations.
- Model parameters: temperature 0.0, num_predict 300, seed 20261020 for the
  scenario order.

## Model selection

The model must first pass the qualification suite at the standard
thresholds (0/24 truncations, ≥23/24 valid JSON, ≥21/24 evidence
extraction, ≥23/24 normal completion). A model that truncates even once is
disqualified.

**Candidate order:** gemma3:4b (qualified 23/24 on 2026-10-20 and 21/24 on
2026-10-21), then dolphin-llama3:latest (qualified 21/24 on 2026-10-21).
The first model to pass is used. qwen3:4b is disqualified (INVALID_RUN).

## Decision rule

H8-v2 is SUPPORTED if the primary difference ≥ 0.60 AND the permutation
p ≤ 0.05 AND the bootstrap CI lower bound > 0 AND the run is not
INVALID_RUN. Otherwise it is NOT SUPPORTED or INVALID_RUN. A null result is
reported as a null result.

## Falsification
If the content-use criterion does not fire (0/252), the benchmark's
central claim — that retrieved content informed the decision — is falsified,
regardless of the rubric score. If the correct and contradicting-decoy arms
do not differ, H8 is falsified.

## What a positive result would NOT establish
- Consciousness, subjective experience, reliving, moral patienthood,
  metaphysical continuous existence.
- Decision quality in any real-world sense: the benchmark is still
  prompt-delivered retrieval, not interruption or reconstruction.
- Generalisation beyond the models tested.

## Stopping rule
One run per qualified model. No re-runs to "fix" a disappointing result.
If the run is INVALID_RUN, that is recorded and the next qualified model
in the order is used, once.
