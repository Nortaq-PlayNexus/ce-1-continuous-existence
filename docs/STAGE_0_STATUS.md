# Stage 0 Scientific Status

## Date
2026-10-20 (post-publication review)

## Current scientific status

CE-1 (Continuous Existence) is a research programme investigating whether
episodic memory infrastructure can produce measurable functional continuity
benefits in AI systems. The programme has completed its Stage 0 baseline
and is preparing for Stage 1 (execution validity) and Stage 2 (functional
episodic continuity, H8).

## Hypothesis status

| Hypothesis | Status | Evidence |
|---|---|---|
| H1 (episodic memory ablation improves continuity) | **INCONCLUSIVE** | Instrument defect: all 30 trials truncated at num_predict=2000. Adversarial verification confirmed the effect does not reproduce cleanly. |
| H2 (episodic vs semantic memory) | **INCONCLUSIVE** | Float threshold defect (0.3 vs 0.30000000000000004) + no control condition. |
| Experiment 1.3 (state ablation) | **Exploratory/null** | gemma3:4b, 13 reps, B-A=0.769, p=0.065 (not significant). Truncation limitation present. Not a preregistered confirmatory test. |
| H7 (subjective experience) | **Out of reach** | No scientific theory of consciousness empirically validated. No AI system confirmed conscious. |
| Causal integration | **Not implemented** | Wrapper-level causal coupling described but not built. |
| Consciousness/subjective experience | **Not established** | No claim made or supported. |

## What has been demonstrated

- Episodic memory infrastructure stores and retrieves structured records.
- Ablation experiments were run but instrument defects invalidated their conclusions.
- The corrected rerun of Experiment 1.1 was INVALID_RUN (all trials truncated).
- Experiment 1.3 produced a null/exploratory result (not significant).

## What has NOT been demonstrated

- That episodic memory improves functional continuity (H1 inconclusive).
- That episodic structure provides benefit over semantic structure (H2 inconclusive).
- That the system has subjective experience, consciousness, or genuine reliving.
- That causal integration between memory and reasoning exists.
- That any model can reliably produce non-truncated structured output (qualification pending).

## Current next target

**Functional, content-specific episodic continuity (H8).**

Establish whether correctly retrieved episodic records cause a measurable
improvement in cross-session continuity behaviour beyond matched generic or
misleading prompt context.

This requires:
1. Fixing remaining experimental infrastructure (Exp 1.3 validity hardening).
2. Building and passing a model qualification gate (gemma3:4b candidate).
3. Building and auditing the continuity_v1 benchmark (72 scenarios).
4. Running a 12-scenario pilot.
5. Running the 72-scenario confirmatory experiment (only if pilot passes).

## Historical results

All historical experiment results remain preserved as evidence. They are
explicitly labeled as inconclusive or exploratory. No historical result
has been deleted or overwritten.

## Publication status

- CE-1 Zenodo deposition: 23471293 (published, DOI: 10.5281/zenodo.23471293, CC BY-NC 4.0)
- S2-F-23 Zenodo deposition: 23489026 (published, DOI: 10.5281/zenodo.23489026, CC BY 4.0)
- These are distinct records with distinct archives, metadata, and identifiers.
