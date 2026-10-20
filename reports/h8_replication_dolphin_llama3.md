# H8 Replication: dolphin-llama3:latest

## Date
2026-10-21

## Preregistration
`experiments/continuity_v1/preregistration_h8_replication.md`, written before
the run. It fixes the benchmark, the primary comparison, the effect threshold,
the analysis (seed 20261020, 10 000 resamples), the model-selection rule, the
disqualification rule and the decision rule.

## Verdict
**H8-R REPLICATED.**

The gemma3:4b result was not an artifact of one checkpoint. A second model
from a different family (Llama-3 8B, instruction-tuned, non-reasoning) shows
the same effect on the same frozen benchmark, under the same analysis, and
with a **larger** effect size.

## Model

| Field | Value |
|---|---|
| Model | dolphin-llama3:latest (8B, Q4_K_M) |
| Qualification | QUALIFIED — 21/24 valid pass, 3 valid fail, 0 invalid, 0 truncations |
| qwen3:4b | INVALID_RUN — disqualified (12/24 truncations; it reasons past the 300-token budget) |
| Temperature | 0.0 |
| num_predict | 300 |
| Seed | 20261020 (scenario order) |
| Run id | replication-dolphin-llama3-20261021 |
| Wall clock | ~82 min (CPU-only inference) |

## Results

216 trials, **0 truncations, 0 parse failures, 0 invalid trials**.

| Condition | Mean score | n |
|---|---:|---:|
| correct_retrieval | 2.028 | 72 |
| matched_decoy | 0.153 | 72 |
| no_memory | 0.000 | 72 |

| Instrument | primary diff | permutation p | bootstrap 95% CI | verdict |
|---|---:|---:|---|---|
| as-run | **1.875** | < 1.0e-4 | [1.722, 2.028] | SUPPORTED |
| corrected | **1.875** | < 1.0e-4 | [1.722, 2.028] | SUPPORTED |

Both instruments give the identical number, unlike gemma3:4b (0.819 vs
1.833). The reason is visible in the per-criterion counts: dolphin quotes
episode ids **unbracketed** (72/72 target citations match under raw string
comparison), so the id-normalisation fix has nothing to repair. The scoring
defect found on 2026-10-21 was a gemma3:4b output-format artifact, and its
absence here is independent corroboration that the defect was in the
interaction between the model and the prompt, not in the rubric.

### Per category (all positive)

| Category | correct | decoy | no_mem | diff | n |
|---|---:|---:|---:|---:|---:|
| commitment_preservation | 2.778 | 0.556 | 0.000 | 2.222 | 18 |
| constraint_persistence | 1.917 | 0.000 | 0.000 | 1.917 | 12 |
| justified_revision | 1.750 | 0.000 | 0.000 | 1.750 | 12 |
| rationale_reconstruction | 1.333 | 0.000 | 0.000 | 1.333 | 18 |
| source_attribution | 2.333 | 0.083 | 0.000 | 2.250 | 12 |

## Adversarial probes on this run

| Probe | Result |
|---|---|
| P1 data integrity | 216 trials, 72 scenarios, 0 invalid, 0 truncated, 0 parse failures |
| P2 prompt integrity | 0/216 prompt-hash mismatches, 0 reused prompts, correct-vs-decoy length difference 0.92% |
| P3 rubric reachability | `decision` **0/72**, `rationale_codes` **0/72** in every condition — same dead criteria as gemma3:4b |
| P5 content fidelity (rubric-independent) | correct **+0.285** (39/72 trials prefer the target), decoy **−0.176** (5/72), no_memory **+0.127** (30/72) |

Two things follow.

**The dead rubric criteria are a property of the benchmark, not of one model.**
gemma3:4b and dolphin-llama3 both score 0 on `decision` and 0 on
`rationale_codes` in all 216 trials each, for different reasons (different
phrasings, same failure). The prompt never states the controlled vocabulary,
so those criteria are unreachable by construction. A v2 benchmark must put
the allowed decisions and the rationale codes in the prompt, or drop them.

**The stronger model leaks content-level guessing through the no-memory arm.**
dolphin's no-memory answers favour the target's vocabulary over the decoy's
in 30 of 72 scenarios (discrimination +0.127), where gemma3:4b showed none
(−0.017). Its rubric score is still 0.000 because the controlled vocabulary
and the episode ids are unreachable — but that means the 0.000 floor is a
property of the rubric, not of the model, and a content-level metric can see
what the rubric cannot. This is a caution against reading the floor as
evidence of "no answer without the episode".

## Cross-model summary

| Model | Correct | Decoy | No memory | diff | p | CI |
|---|---:|---:|---:|---:|---:|---|
| gemma3:4b (confirmatory, 2026-10-20) | 1.042 | 0.222 | 0.000 | 0.819 | <1.0e-4 | [0.667, 0.972] |
| gemma3:4b (reproduction, 2026-10-21) | — | — | — | 0.875 | <1.0e-4 | [0.722, 1.028] |
| dolphin-llama3:latest (replication, 2026-10-21) | 2.028 | 0.153 | 0.000 | 1.875 | <1.0e-4 | [1.722, 2.028] |

As-run instrument throughout. The two models differ in family, size, tuning
and answer style, and the effect is present in both, larger in the second.

## What this does NOT establish

- Nothing about consciousness, subjective experience, reliving, autonoetic
  awareness, moral patienthood, or metaphysical continuous existence.
- Nothing about interruption, resumption or persistent state. The benchmark
  manipulates which episode is in the prompt; H3 remains untested.
- Nothing about decision quality: the rubric's decision criterion never
  fired, in either model.
- Not generalisation in general: two local models on one CPU, run by one
  research programme, is not independent replication. A v2 benchmark and a
  third-party replication are still required.
- The effect is still *episodic-content sensitivity under prompt delivery*.
  The name "continuity" in H8 outruns what is measured.

## Artifacts

- Run: `experiments/continuity_v1/results/replication_dolphin_llama3_results.jsonl`
- Scores: `.../replication_dolphin_llama3_scores.jsonl` (as-run),
  `.../replication_dolphin_llama3_scores_v2.jsonl` (corrected)
- Analyses: `.../replication_dolphin_llama3_analysis.json`,
  `.../replication_dolphin_llama3_analysis_v2.json`
- Adversarial probes: `.../adversarial_verification_dolphin.json`
- Qualification: `experiments/model_qualification/results/dolphin_llama3_verdict.json`
