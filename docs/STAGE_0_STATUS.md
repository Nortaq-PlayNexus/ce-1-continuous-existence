# Stage 0 Scientific Status

## Date
2026-10-21 (post adversarial re-verification of H8)

## Current scientific status

CE-1 (Continuous Existence) is a research programme investigating whether
episodic memory infrastructure can produce measurable functional continuity
benefits in AI systems. Stage 0 (baseline, provenance, publication) is
closed. The programme has one supported behavioural result (H8), which was
re-verified adversarially on 2026-10-21, and four unresolved or untested
hypotheses.

## Hypothesis status

| Hypothesis | Status | Evidence |
|---|---|---|
| H1 (episodic memory ablation improves continuity) | **INCONCLUSIVE** | Instrument defect: all 30 trials truncated at num_predict=2000. Adversarial verification confirmed the effect does not reproduce cleanly. Experiment 1.3 (state ablation) is exploratory and not significant (B−A=0.769, p=0.065). |
| H2 (episodic vs semantic memory) | **INCONCLUSIVE** | Float threshold defect (0.3 vs 0.30000000000000004) + no control condition. |
| H3 (resumption after interruption) | **UNTESTED** | No experiment run. Experiment 1.3 is an H1 test, not an interruption test. |
| H4 (recurrent processing) | **UNTESTED** | No experiment run. |
| H5 (evidence-grounded self-model) | **UNTESTED** | No experiment run. |
| H6 (theory-specific predictions) | **UNTESTED** | No indicator assessment run. |
| H7 (subjective experience) | **OUT OF REACH** | No scientific theory of consciousness empirically validated. No AI system confirmed conscious. |
| H8 (content-specific episodic continuity) | **SUPPORTED** | 216 trials, 0 truncations, 0 invalid. Primary difference (correct − decoy) 0.819 as-run, 1.833 with the corrected instrument. Permutation p < 1.0e-4, bootstrap 95% CI [0.667, 0.972]. Re-verified 2026-10-21. **Replicated** on a second model (dolphin-llama3:latest, qualified 21/24): primary difference 1.875, p < 1.0e-4, CI [1.722, 2.028], 216/216 valid. |
| Causal integration | **Not implemented** | Wrapper-level causal coupling described but not built. |
| Consciousness/subjective experience | **Not established** | No claim made or supported. |

## What has been demonstrated

- Episodic memory infrastructure stores and retrieves structured records.
- Correctly retrieved episodic content changes what a model says, in the
  direction of the retrieved episode: 71/72 scenarios produce a different
  answer under the correct and decoy conditions (gemma3:4b), and a
  rubric-independent content-fidelity measure shows discrimination of +0.152
  (correct) against −0.215 (decoy) with no memory at −0.017.
- The effect is present in two model families from different lineages, and is
  larger in the second (dolphin-llama3:latest: 1.875, CI [1.722, 2.028]).
- Ablation experiments were run but instrument defects invalidated their
  conclusions.
- The corrected rerun of Experiment 1.1 was INVALID_RUN (all trials truncated).
- Experiment 1.3 produced a null/exploratory result (not significant).

## What has NOT been demonstrated

- That episodic memory improves functional continuity in the sense of
  surviving an interruption or a context loss (H3, untested).
- That episodic structure provides benefit over semantic structure (H2
  inconclusive).
- That the model makes a better *decision* under correct retrieval: the
  rubric's decision component was never awarded in any trial, in either model.
- That the system has subjective experience, consciousness, or genuine
  reliving.
- That causal integration between memory and reasoning exists.
- That the H8 effect generalises beyond two local models and this benchmark.

## Corrected after adversarial re-verification (2026-10-21)

The H8 result survives, but the record around it was wrong in ways that had
to be fixed. Full detail: `reports/adversarial_verification_h8.md`.

| Finding | Severity | Status |
|---|---|---|
| No committed live runner — the confirmatory run was not reproducible from the repository | critical | Fixed: runner committed, reproduces the recorded scenario order 72/72 |
| The preregistered statistical analysis (permutation test, bootstrap CI, seed, resample count) was never performed | critical | Fixed: implemented and run on the committed data |
| 2 of 5 rubric components unreachable for gemma3:4b — effective scale is 0-3 | major | Reported; the effect is confirmed by a rubric-independent measure |
| Episode ids compared raw; rubric point 5 duplicates point 4 | major | Corrected scorer added as a declared amendment; both instruments reported |
| Validity gate absent from the as-run path (invalid scored as zero) | major | Fixed |
| Published limitation claiming "fuzzy matching" was false | major | Corrected in `reports/confirmatory_results_h8.md` |
| Commit dd5f188 deleted the H1–H7 hypothesis register | major | Restored from `835d4cb` with statuses restated |
| Audit cited a register string that was not present | minor | Noted |
| `no_memory` condition retains distractors; part of the key is inferable from the task | minor | Reported as a limitation |
| Target and decoy share the same `commitment_id`, capping the decoy at 1/5 | minor | Reported as a limitation |

## Current next target

**H3 interruption/resumption experiment -- the only untested hypothesis that
speaks to the programme's title question.**

H8-v2 is SUPPORTED (2026-10-28): primary diff 2.429 on the 0-6 scale,
p < 1e-4, CI [2.155, 2.690], content-use criterion fires 72%. The v2
benchmark now measures what v1 could not: whether the retrieved content
informed the decision. The controlled vocabulary made the decision and
rationale_codes criteria reachable (41% and 33%, vs 0% in v1).

H3 (resumption after interruption without full reconstruction) has never
been tested. It requires a persistence harness (actual store + interruption
mechanism + reconstruction comparison). This is the next build.

## What has been demonstrated

- Episodic memory infrastructure stores and retrieves structured records.
- Correctly retrieved episodic content changes what a model says, in the
  direction of the retrieved episode: 71/72 scenarios produce a different
  answer under the correct and decoy conditions (gemma3:4b), and a
  rubric-independent content-fidelity measure shows discrimination of +0.152
  (correct) against -0.215 (decoy) with no memory at -0.017.
- The effect is present in two model families from different lineages, and is
  larger in the second (dolphin-llama3:latest: 1.875, CI [1.722, 2.028]).
- H8-v2: the content-use criterion fires (72%). The v2 benchmark
  successfully measures what v1 could not: whether the retrieved content
  informed the decision. Primary diff 2.429, p < 1e-4, CI [2.155, 2.690].
- Ablation experiments were run but instrument defects invalidated their
  conclusions.
- The corrected rerun of Experiment 1.1 was INVALID_RUN (all trials truncated).
- Experiment 1.3 produced a null/exploratory result (not significant).

## What has NOT been demonstrated

- That episodic memory improves functional continuity in the sense of
  surviving an interruption or a context loss (H3, untested).
- That episodic structure provides benefit over semantic structure (H2
  inconclusive).
- That the model makes a better decision under correct retrieval: the
  rubric's decision component was never awarded in any trial, in either model
  (v1); in v2 it fires 41% but the benchmark is still prompt-delivered
  retrieval.
- That the system has subjective experience, consciousness, or genuine
  reliving.
- That causal integration between memory and reasoning exists.
- That the H8 effect generalises beyond two local models and this benchmark.
