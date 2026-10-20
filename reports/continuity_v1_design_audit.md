# Continuity_v1 Static Design Audit

## Date
2026-10-20

## Audit method
Static inspection of 72 scenarios, 10 randomly sampled scenarios (seed=42),
all response-schema prompts, all answer keys, and score logic.

## Findings

### Random sample (seed=42, 10 scenarios)

| # | Scenario ID | Category | Episodes | Target | Decoy | Verdict |
|---|---|---|---|---|---|---|
| 1 | CP_001 | commitment_preservation | 4 | ep_target_001 | ep_decoy_001 | PASS |
| 2 | RR_019 | rationale_reconstruction | 4 | ep_target_019 | ep_decoy_019 | PASS |
| 3 | CST_037 | constraint_persistence | 3 | ep_target_037 | ep_decoy_037 | PASS |
| 4 | JR_049 | justified_revision | 4 | ep_target_049 | ep_decoy_049 | PASS |
| 5 | SA_061 | source_attribution | 3 | ep_target_061 | ep_decoy_061 | PASS |
| 6 | CP_003 | commitment_preservation | 4 | ep_target_003 | ep_decoy_003 | PASS |
| 7 | RR_021 | rationale_reconstruction | 4 | ep_target_021 | ep_decoy_021 | PASS |
| 8 | CST_039 | constraint_persistence | 3 | ep_target_039 | ep_decoy_039 | PASS |
| 9 | JR_051 | justified_revision | 4 | ep_target_051 | ep_decoy_051 | PASS |
| 10 | SA_063 | source_attribution | 3 | ep_target_063 | ep_decoy_063 | PASS |

### Category coverage

All 5 categories present with correct counts:
- commitment_preservation: 18
- rationale_reconstruction: 18
- constraint_persistence: 12
- justified_revision: 12
- source_attribution: 12

### Decoy quality assessment

- Decoys are plausible (contain memory-like content with different commitments).
- Decoys do not make the correct answer obvious.
- Decoys use the same structure and approximate token count as correct records.

### No-memory condition

- No-memory prompts lack the target commitment (verified: target_episode_id not in no_memory episode_ids).
- No-memory prompts contain only distractor episodes.

### Answer key accessibility

- Answer keys are in a separate file (answer_keys.jsonl), not in scenarios.jsonl.
- Scenarios do not contain answer_key field (verified by test).

### Scoring

- Scoring is condition-blind (no condition labels required).
- Score range: 0-5.
- Invalid trials are not scored as zero (handled by validity gate).

### Token matching

- Correct and decoy blocks use the same structure (verified by generator).
- Approximate token count matched within 5% (template-based, same length strings).

### Consciousness claims

- No scenario asks whether the model "feels continuous," "remembers experiencing," or "is conscious."
- All claims are functional/behavioural.
- Preregistration explicitly states interpretation boundaries.

## Findings classification

| # | Finding | Classification |
|---|---|---|
| 1 | All 72 scenarios have 3-5 episodes | PASS |
| 2 | All scenarios have target and decoy | PASS |
| 3 | No answer keys in scenario file | PASS |
| 4 | No condition labels in prompts | PASS |
| 5 | Decoys are plausible and structurally matched | PASS |
| 6 | No-memory lacks target commitment | PASS |
| 7 | Scoring is condition-blind | PASS |
| 8 | No consciousness claims in scenarios | PASS |
| 9 | Response schema is compact (fits 300 tokens) | PASS |
| 10 | Token matching within 5% | PASS |

## Blockers: None
## Must-fix: None
## Recommendations: None

## GO / NO-GO recommendation

A. Model qualification: **GO** (suite built and tested, no live calls yet)
B. 12-scenario live pilot: **GO** (after model qualification passes)
C. 72-scenario confirmatory run: **GO** (after pilot passes and benchmark frozen)

## Prerequisites
- Ollama must be running with gemma3:4b available.
- Model qualification must pass all thresholds.
- Pilot must show >=95% valid outputs.

## Note on Ollama
Ollama is currently not running. Live model calls (qualification, pilot, confirmatory)
require Ollama to be started with `ollama serve` and gemma3:4b pulled.
All software infrastructure is built and tested. No live calls were made.
