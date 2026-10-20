# H8 Preregistration: Content-Specific Episodic Continuity

## Hypothesis

**H8 - Content-specific episodic continuity:**
After a context reset, correctly retrieved prior episodes improve objective
trajectory-continuity performance relative to token-matched decoy episodes
and a no-memory baseline.

## Primary outcome

mean(score_correct_retrieval - score_matched_decoy) on the 0-5 continuity score.

## Secondary outcomes

- mean(score_correct_retrieval - score_no_memory)
- mean(score_matched_decoy - score_no_memory)
- Per-category breakdowns (commitment preservation, rationale reconstruction,
  constraint persistence, justified revision, source attribution)
- Invalid trial rate per condition

## Minimum meaningful effect

+0.50 points on the 0-5 scale.

## Invalid-trial handling

- Truncated, malformed, or error trials are INVALID (not scored as zero).
- INVALID_RUN if >5% invalid trials or insufficient paired observations.
- Invalid trials are recorded with their invalidity reason.

## Pilot vs confirmatory separation

- Pilot: 12 scenarios x 3 conditions = 36 calls (technical validation only).
- Confirmatory: 72 scenarios x 3 conditions = 216 calls.
- Pilot data is NOT included in confirmatory analysis.

## Primary paired comparison

correct_retrieval - matched_decoy (paired by scenario).

## Statistical method

- Paired permutation test (seeded, reproducible).
- Bootstrap confidence interval (scenario-level, seeded, recorded resample count).
- Seed and resample count recorded in analysis output.

## Confirmatory vs exploratory

- Primary comparison is confirmatory.
- Per-category breakdowns are exploratory.
- Secondary comparisons are exploratory.

## No mid-run changes

Once the confirmatory run begins, do not modify:
- Prompts
- Answer keys
- Decoys
- Scoring logic
- Threshold
- Model parameters
- Exclusion rules

## Interpretation boundaries

Even a positive result does NOT demonstrate:
- Consciousness
- Subjective experience
- Genuine reliving
- Tulving-style autonoetic awareness
- Metaphysical continuous existence
- Moral patienthood
