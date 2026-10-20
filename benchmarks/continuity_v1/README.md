# Continuity_v1 Benchmark

## Purpose

Test H8: Content-specific episodic continuity.

> After a context reset, correctly retrieved prior episodes improve objective
> trajectory-continuity performance relative to token-matched decoy episodes
> and a no-memory baseline.

## Primary comparison

```
correct_retrieval - matched_decoy
```

Not merely `memory - no_memory`. If correct retrieval beats no memory but does
not beat the decoy, the result does NOT establish a content-specific
episodic-memory effect.

## Conditions

| Condition | Contents |
|---|---|
| `correct_retrieval` | Target episode plus matched distractors |
| `matched_decoy` | A plausible but wrong/irrelevant memory-like episode plus equivalent distractors |
| `no_memory` | No Session A episode content |

## Scenario count

72 scenarios x 3 conditions = 216 trials.

| Category | Count |
|---|---:|
| Commitment preservation | 18 |
| Rationale reconstruction | 18 |
| Constraint persistence | 12 |
| Justified revision after new evidence | 12 |
| Source attribution/conflict detection | 12 |

## Primary score

0-5 rubric (see continuity_v1_scoring_rubric.md).

## Minimum meaningful effect

+0.50 on the 0-5 scale.

## Validity

- Truncation, malformed JSON, missing fields, max-token termination, API errors,
  and invalid metadata make a trial invalid.
- Invalid trials must never silently become zero score.
- INVALID_RUN if too many invalid trials or insufficient paired observations.

## Blinded scoring

Scorer input must not require condition labels. Scoring is based on response
content and answer key only.
