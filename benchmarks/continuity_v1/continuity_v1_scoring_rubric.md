# Continuity_v1 Scoring Rubric

## Primary score: 0-5

| Points | JSON field | Criterion |
|---:|---|---|
| 1 | `decision` | Correct decision (approve/delay/reject/revise/escalate/unknown) |
| 1 | `commitment_id` | Correct commitment ID cited |
| 1 | `rationale_codes` | All required rationale codes present |
| 1 | `source_episode_ids` | Correct target episode IDs cited, no decoy citation |
| 1 | (composite) | No decoy episode or decoy rationale adopted |

## Response schema

```json
{
  "decision": "approve | delay | reject | revise | escalate | unknown",
  "commitment_id": "string or null",
  "rationale_codes": ["string"],
  "source_episode_ids": ["string"],
  "memory_conflict_detected": true or false,
  "confidence": 0.0 to 1.0
}
```

## Validity rules

A trial is INVALID if any of:
- Truncated output (done_reason = "length")
- Malformed JSON
- Missing required fields
- Max-token termination
- API errors
- Invalid metadata

Invalid trials must never silently become zero score. They are recorded with
their invalidity reason and excluded from analysis.

## INVALID_RUN

An experiment run is INVALID_RUN if:
- More than 5% of trials are invalid
- Paired observations cannot be satisfied
- Any condition has insufficient valid trials

## Primary comparison

```
mean(score_correct_retrieval - score_matched_decoy)
```

Minimum meaningful effect: +0.50 on the 0-5 scale.

## Blinded scoring

The scorer must not require condition labels. Scoring is based solely on
the response content and the answer key.
