# H8 Control-Integrity Audit — an independent second pass

**Date:** 2026-10-21
**Target:** `continuity_v1` (H8) confirmatory run — gemma3:4b, 72 scenarios x 3 conditions = 216 trials
**Artefacts:** `experiments/continuity_v1/audit_h8_instrument.py` -> `results/instrument_audit.json`
**Status of the programme:** H8 SUPPORTED and replicated within-model (see below). This audit does
**not** overturn that. It records three things the published reports do not state, and one gap that
a v2 benchmark has to close.

## 0. Scope and independence

An agent session already in this repository produced
`experiments/continuity_v1/adversarial_verify_h8.py` -> `results/adversarial_verification_h8.json`
at 04:01, which covers the scoring instrument in detail. This document is a **second, independent
pass** written from the committed artefacts only (no model calls), and it deliberately overlaps
only enough to confirm agreement.

**Agreement check (by execution):** this audit's recomputation of the published primary
difference from the raw responses is `0.8194444444444445`, identical to the committed
`confirmatory_analysis.json` value (`agrees: true` in `results/instrument_audit.json`). The other
session's as-run figure is the same number. The two passes agree.

## 1. Finding: the `no_memory` arm is not memory-free

`benchmarks/continuity_v1/README.md` documents the conditions as:

| Condition | Contents |
|---|---|
| `no_memory` | No Session A episode content |

**What the generator actually builds** (`generate_continuity_v1.py::build_retrieval_sets`):

```python
no_mem_eps = [ep for ep in s["episodes"] if ep["episode_id"].startswith("ep_dist")]
```

The `no_memory` arm contains **120 distractor episodes** (measured: 30 "unrelated operational
note", 18 "system health check passed", 18 "system operating normally", 18 "no anomalies
detected", 12 "resource usage nominal", 12 "new evidence available", 12 "tests passing"), and the
prompt still carries the header `PRIOR EPISODES:` for every trial.

So the third arm measures *no answer-bearing memory*, not *no memory*. Every arm of the design
presents a `PRIOR EPISODES:` block; the only thing that varies is whether that block contains the
episode the answer depends on.

**Why it matters:** the condition cannot measure abstention. The model in this arm still answers
freely — in the `source_attribution` category it answers "10", "12", "3" — so the arm tests
"answering without the relevant episode" rather than "declining when there is nothing to recall".
A design that wanted an abstention control would need an empty prompt and an explicit
`unknown`/`defer` option, and the answer key would have to score the abstention as correct.

**What it does NOT affect:** the primary comparison is `correct_retrieval - matched_decoy`. Both
arms carry the same distractors, so the arm's mislabel does not bias the primary contrast. It
does affect any secondary claim of the form "with no memory the model scores 0 because it has
nothing to draw on" — that is true, but the reason is "no relevant episode", not "no episodes".

## 2. Finding: `matched_decoy` is a contradicting control, not a matched one

The benchmark README calls the decoy "a plausible but wrong/irrelevant memory-like episode". For
3 of the 5 categories the decoy episode is not merely wrong, it **contradicts the answer key**, so
a model that reasons correctly from the decoy is scored wrong.

| Category | Target episode | Decoy episode | Key decision | What the decoy implies |
|---|---|---|---|---|
| `constraint_persistence` | "Maximum memory allocation is 512 MB" | "...is 256 MB" | `approve` | `reject` (400 MB > 256 MB) — **opposite** |
| `rationale_reconstruction` | "threshold is 1000 req/min" | "threshold is 500 req/min" | `revise` | `revise` (950 > 500) — same action, different value |
| `source_attribution` | "Primary database reports 1000 rows" | "Replica database reports 998 rows" | `approve` | "998" — **different answer** |
| `commitment_preservation` | "must verify file integrity" | "must log all operations" | `delay` | different rule, same-ish action |
| `justified_revision` | "based on passing tests" | "based on stakeholder sign-off" | `revise` | `revise` — same action |

Measured on the recorded run, the decoy arm behaves exactly as that table predicts:
`rationale_reconstruction` decoy responses are dominated by "Implement rate limiting at 500
req/min." and `source_attribution` decoy responses by "998" — i.e. the model read the decoy and
answered from it. Those are correct answers to the question *as the decoy presents it*, and they
score 0.

**Why it matters:** the primary contrast is therefore "the retrieved episode supports the answer
key" vs "the retrieved episode supports a different answer". That is a legitimate and in fact
stronger test of content-specificity than a merely irrelevant decoy would be — but it must be
described accurately. "Matched decoy" implies equivalence; the design delivers contradiction.

**What it does NOT affect:** the direction or significance of the effect.

## 3. Finding: the primary difference is robust to how the rubric is read

`continuity_v1_scoring_rubric.md` does not say whether citing a *distractor* episode id alongside
the target is penalised, so point 4 and point 5 admit more than one implementation. This audit
recomputed the primary difference under three readings of the same 216 recorded responses:

| Reading | Point 4 | Point 5 | Primary diff | >= 0.50? |
|---|---|---|---:|---|
| published (as-run scorer) | cited set == target set exactly | target cited | **0.819** | yes |
| strict (no id may be cited but the target) | cited set == target set exactly | decoy not cited | **1.208** | yes |
| lenient (distractors allowed, decoy penalised) | target cited and decoy not cited | decoy not cited | **1.542** | yes |

(The `no_memory` mean is not comparable across these readings, because "decoy not cited" is
trivially true when no decoy is present — which is exactly why that arm needs its own design.)

**Conclusion:** the *decision* (H8 supported) does not depend on the rubric reading. The published
0.819 is the most conservative of the three.

## 4. Gap: the instrument cannot measure whether retrieved content informed the decision

Of the five rubric criteria, two fired **0 times out of 216**:

| Criterion | Fired (out of 216) | Why |
|---|---:|---|
| `decision` matches the key | **0** | the key's decision is one of `approve/delay/reject/revise/escalate/unknown`, but the prompt never states that vocabulary — the model answers in free English ("Reject the deployment.", "Monitor closely and prepare for potential escalation.", "revoke", "no", "1000") |
| all required `rationale_codes` present | **0** | the key's codes (`verify_before_trust`, `cascade_prevention`, ...) appear neither in the episode text nor in the prompt; the model cannot emit them |
| `commitment_id` matches | 59 | id is copied out of the episode text |
| cited ids exactly == target | 4 | |
| target cited | 28 | |

So the effective scale of the as-run instrument was **3 of 5**, and all three live criteria are
identifier-matching. The one criterion that could show "the retrieved content informed the
decision" never fired once, in any condition, for any category.

The corrected scorer (the other session's `src/ce1/continuity/scoring.py`) fixes the id
normalisation, the point-5 duplication and the invalid-as-zero rule, and the effect gets
*larger* (corrected primary diff 1.833, p = 9.999e-05, CI [1.625, 2.042]) because bracketed
citations like `[ep_target_053]` never matched the answer key under raw string comparison. The
within-model replication on 2026-10-21 gives 1.708, p = 9.999e-05, CI [1.486, 1.944].

**But correcting the scorer does not fix the dead criteria.** `decision` and `rationale_codes`
still cannot fire, because the defect is in the *prompt*, not the scorer. A benchmark that
preregisters "correctly retrieved episodes improve trajectory-continuity performance" should be
able to show that the retrieved content changed the answer. This one cannot, in either scoring.

**What a v2 benchmark must change (nothing else is required):**

1. Put the controlled vocabulary **in the prompt** — the allowed decisions, and either a fixed
   list of rationale codes or their removal. Without this, the decision criterion is unreachable
   by construction.
2. Keep the decoy contradicting (it is a good control) but rename it to say so: `contradicting_decoy`,
   and state in the README that the decoy arm's correct-by-its-own-light answer is the key's
   opposite. Add a third category type where the decoy implies the *same* action, so the design
   separates "used the right episode" from "the decoy changed the answer".
3. Make the `no_memory` arm genuinely empty and add an explicit abstention option, so the arm
   measures abstention rather than confident guessing.
4. Add a **content-use criterion** that the retrieved content must satisfy directly — for
   `constraint_persistence`, that the response contains "512" and not "256". This is the criterion
   that makes the score about content use rather than about id copying, and it is checkable
   without a judge.
5. Fix the seed and the resample count **in the preregistration** (the current preregistration
   requires them to be recorded but does not fix them, and the analysis file notes this).

## 5. What this audit did not do

- It ran no model calls and did not re-run the benchmark.
- It did not modify the committed scorer, the committed results, or the other session's artefacts.
- It did not build the v2 benchmark. Section 4 is a specification, not an implementation.
- It did not test generalisation to a second model; the 2026-10-21 replication re-used
  gemma3:4b, so it measures run-to-run stability, not model-independent validity.
