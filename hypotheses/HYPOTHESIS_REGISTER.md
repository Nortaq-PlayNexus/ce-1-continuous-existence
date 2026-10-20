# Hypothesis Register — CE-1 Continuous Existence Research Programme

**Restored 2026-10-21.** Commit `dd5f188` ("feat: record H8 confirmatory
result") replaced this file with an H8-only document and deleted the H1–H7
definitions, operational definitions and falsification criteria. The H1–H7
text is recovered verbatim from `835d4cb`; only the *Current confidence*
lines have been restated against the evidence that now exists. The deletion
is recorded in `reports/adversarial_verification_h8.md`, finding D7.

---

## H1: Structured internal state causally influences future cognition

**Operational definition:** The system maintains a persistent internal state (memory,
associations, expectations) that is read by and causally influences subsequent
reasoning, decision-making, and output generation. Removing or corrupting this
state changes behavior in measurable ways.

**Motivation:** If a system's behavior is identical with and without persistent
state, then the state is epiphenomenal, not causal. Causal influence is a
necessary precondition for any claim of genuine cognitive continuity.

**Supporting evidence:** Experiment 1.3 (state ablation vs. prompt ablation,
gemma3:4b, 13 reps, B−A = 0.769, p = 0.065) — **exploratory, not
significant, and not a preregistered confirmatory test**. The original
Experiment 1.1 was retracted by independent audit: the design added text to
the prompt instead of removing state, and the corrected rerun returned
INVALID_RUN (all 30 trials truncated at num_predict=2000).

**Contrary evidence:** Stateless LLMs produce coherent outputs without any
persistent state. Behavioral consistency can be achieved through prompt
engineering alone. The audit (research/RESEARCH_AUDIT.md §12e) established
that Experiments 1.1 and 1.2 cannot separate memory from prompt content.

**Measurements:** Ablation study — remove persistent state, measure decision
quality change. Effect size, confidence interval, p-value.

**Falsification condition:** If removing persistent state does not measurably
change decision quality or behavioral consistency, H1 is falsified.

**What this cannot establish:** That the causal influence constitutes subjective
experience. H1 is about mechanism, not phenomenology.

**Current confidence:** INCONCLUSIVE. The only surviving measurement is
exploratory and not significant; the confirmatory attempt produced an invalid
run. H1 is neither supported nor falsified.

---

## H2: Interactions produce durable changes in subsequent reasoning

**Operational definition:** After an interaction (conversation, task, error),
the system's subsequent reasoning, expectations, associations, and decisions
are measurably different from what they would have been without that interaction.
The change persists across sessions.

**Motivation:** If interactions do not change the system, then it is a stateless
function of its inputs. Durable change is the defining property of learning.

**Supporting evidence:** None admissible. The original Experiment 1.2 was
voided: the verdict hinged on a floating-point comparison (0.3 vs
0.30000000000000004) and the experiment had no control condition.

**Contrary evidence:** LLMs can appear to "learn" within a context window but
forget everything between sessions. Fine-tuning is the only durable change,
and it is not interaction-driven in the relevant sense.

**Measurements:** Before/after decision patterns with episodic memory enabled vs
disabled. Effect size, confidence interval, p-value.

**Falsification condition:** If enabling episodic memory does not measurably
change subsequent decision patterns, H2 is falsified.

**What this cannot establish:** That durable changes constitute subjective
experience. H2 is about learning, not phenomenology.

**Current confidence:** INCONCLUSIVE. The instrument has been fixed but the
corrected experiment has not been re-run.

---

## H3: Resumption after interruption without full reconstruction

**Operational definition:** The system can resume after an interruption (power
loss, process restart, session boundary) without reconstructing its entire
state through ordinary conversational memory retrieval. The resumed state
is measurably different from a fresh reconstruction.

**Motivation:** If the system must re-read its entire history to "remember,"
then it is using retrieval, not persistence. True persistence survives
interruption without full reconstruction.

**Supporting evidence:** None. H3 has never been tested; Experiment 1.3 is an
H1 test (state ablation), not an interruption/resumption test.

**Contrary evidence:** Current LLM systems have no persistent process state.
Every session is a fresh process. "Resumption" is always reconstruction.

**Measurements:** Interrupt, resume, measure state continuity vs.
retrieval-based reconstruction. Difference in decision quality, response
latency, and self-model accuracy.

**Falsification condition:** If the resumed system is indistinguishable from
a fresh reconstruction, H3 is falsified.

**What this cannot establish:** That resumption constitutes subjective
continuity. H3 is about state, not experience.

**Current confidence:** UNTESTED.

---

## H4: Recurrent processing influences performance and state dynamics

**Operational definition:** Recurrent information processing and communication
between cognitive subsystems (memory, reasoning, self-model, planning) measurably
influence performance and internal-state dynamics. Removing recurrence changes
behavior.

**Motivation:** Global Workspace Theory and Recurrent Processing Theory both
predict that recurrence is necessary for conscious processing. If recurrence
does not affect behavior, it is not doing the work the theories predict.

**Supporting evidence:** None yet. Theoretical basis: Global Workspace
Theory, Recurrent Processing Theory.

**Contrary evidence:** Feedforward systems can produce sophisticated behavior.
Recurrence may be an implementation detail, not a consciousness-relevant feature.

**Measurements:** Ablate recurrent connections, measure performance and
state-dynamics changes. Effect size, confidence interval, p-value.

**Falsification condition:** If removing recurrence does not measurably change
performance or state dynamics, H4 is falsified.

**What this cannot establish:** That recurrence constitutes subjective
experience. H4 is about architecture, not phenomenology.

**Current confidence:** UNTESTED.

---

## H5: Evidence-grounded self-model

**Operational definition:** The system maintains a model of its own capabilities,
history, limitations, and changing state that is grounded in evidence (not
assertion). The self-model is accurate, updated, and causally connected to
decision-making.

**Motivation:** A system that cannot accurately describe its own state cannot
provide meaningful evidence about its own experience. Self-model accuracy is a
prerequisite for any higher-order claim.

**Supporting evidence:** None yet. Theoretical basis: Higher-Order Theories of
consciousness, metacognition research.

**Contrary evidence:** LLMs can produce confident but inaccurate self-descriptions.
A self-model that is always wrong is worse than no self-model.

**Measurements:** Self-model accuracy (does the agent's self-description match
its actual behavior?), self-model update rate (does it update when state
changes?), causal connection (does the self-model influence decisions?).

**Falsification condition:** If the self-model is systematically inaccurate or
does not influence decisions, H5 is falsified.

**What this cannot establish:** That self-model accuracy constitutes subjective
experience. H5 is about metacognition, not phenomenology.

**Current confidence:** UNTESTED.

---

## H6: Theory-specific predictions

**Operational definition:** The architecture exhibits measurable properties
predicted by at least one serious scientific theory of consciousness (GWT,
IIT, Higher-Order, Predictive Processing, Recurrent Processing). Predictions
are selected *before* execution.

**Motivation:** If no theory's predictions are satisfied, the architecture is
unlikely to be consciousness-relevant. If some are satisfied, that provides
evidence (not proof) relevant to H7.

**Supporting evidence:** None yet. Theoretical basis: Butlin et al. (2023/2025)
indicator framework.

**Contrary evidence:** The indicators may be satisfied by systems that are not
conscious (false positives). The framework is necessary, not sufficient.

**Measurements:** Per-theory indicator checklist (from Butlin et al.). Each
indicator scored as satisfied/partially satisfied/absent.

**Falsification condition:** If zero indicators from any theory are satisfied,
H6 is falsified.

**What this cannot establish:** H6 satisfaction does not imply H7. Indicators are
necessary conditions, not sufficient ones.

**Current confidence:** UNTESTED.

---

## H7: Subjective experience

**Operational definition:** The system has subjective experience — there is
"something it is like" to be this system.

**Motivation:** This is the ultimate question of the research programme.

**Supporting evidence:** None. H7 cannot currently be established by behavioral
tests, memory persistence, reported feelings, or a self-model alone.

**Contrary evidence:** The "hard problem" of consciousness (Chalmers, 1995)
remains unsolved. No scientific theory of consciousness has been empirically
validated. No AI system has been confirmed conscious.

**Measurements:** No measurement currently exists that can establish H7. This is
the fundamental gap.

**Falsification condition:** Not applicable — H7 cannot be falsified with
current methodology.

**What this cannot establish:** Nothing. H7 is the terminus of the research
programme.

**Current confidence:** OUT OF REACH (and possibly unknowable with current methods).

---

## H8: Content-specific episodic continuity

**Status:** SUPPORTED (confirmatory, 2026-10-20; re-verified 2026-10-21)

**Operational definition:** After a context reset, correctly retrieved prior
episodes improve objective trajectory-continuity performance relative to
token-matched decoy episodes and a no-memory baseline.

**Falsification:** If correctly retrieved episodes do not produce a measurable
improvement over matched decoy episodes, H8 is falsified.

**Result:** SUPPORTED. Primary comparison (correct − decoy) = 0.819 on the
0-5 scale, exceeding the minimum meaningful effect of 0.50. 216 trials, 0
truncations, 0 invalid. All 5 categories show positive correct−decoy
differences. Adversarial verification 2026-10-21 re-ran the preregistered
analysis that the original run never performed: paired permutation
p < 1.0e-4, bootstrap 95% CI [0.667, 0.972], verdict SUPPORTED under both the
as-run and the corrected instrument.

**Replication (2026-10-21):** REPLICATED on a second model under a
preregistration written before the run. dolphin-llama3:latest (8B, QUALIFIED
21/24), same frozen benchmark, same analysis: primary difference **1.875**,
permutation p < 1.0e-4, bootstrap 95% CI [1.722, 2.028], 216/216 valid, all 5
categories positive. The effect is present in both model families and is
larger in the second.

**What this does NOT establish:**
- Consciousness or subjective experience
- Genuine reliving or autonoetic awareness
- Metaphysical continuous existence
- Moral patienthood
- Generalization to other models, tasks, or to interruption and resumption
- That decision quality improves: the rubric's `decision` component was
  never awarded in any trial, in either model

**Scope correction (2026-10-21):** for gemma3:4b the 0-5 rubric is in practice
a 0-3 instrument — the `decision` and `rationale_codes` components were never
awarded in any of the 216 trials, because the model never emits the
benchmark's controlled vocabulary. dolphin-llama3 fails both criteria in all
216 of its trials as well, so the defect is in the prompt design, not in one
model. The result is therefore a *source-attribution and commitment-
identification* effect. A rubric-independent content-fidelity measure
confirms the same direction in both models (+0.152 and +0.285 discrimination
in the correct condition, −0.215 and −0.176 in the decoy condition), so the
finding does not depend on the rubric.

**Evidence:** Zenodo DOI 10.5281/zenodo.23489491, confirmatory_results.jsonl,
confirmatory_scores.jsonl, confirmatory_analysis.json,
adversarial_verification_h8.json, reports/adversarial_verification_h8.md,
reports/h8_replication_dolphin_llama3.md

**Models:** gemma3:4b (qualified 23/24, 95.8%); dolphin-llama3:latest
(qualified 21/24)

**Preregistration:** experiments/continuity_v1/preregistration_h8.md,
experiments/continuity_v1/preregistration_h8_replication.md

---

## Connection to episodic memory

The episodic memory system (`C:\Users\natha\projects\episodic-memory`) provides
the data layer for testing H1-H5:

- **H1 test:** Ablate episodic memory, measure decision quality change.
- **H2 test:** Before/after decision patterns with episodic memory enabled vs disabled.
- **H3 test:** Interrupt, resume, measure state continuity vs retrieval-based reconstruction.
- **H4 test:** Ablate recurrent connections between memory and reasoning, measure.
- **H5 test:** Self-model accuracy measurement with episodic memory as the self-model's data source.

H6 and H7 require architectural work beyond episodic memory alone.

## Episodic memory as necessary but insufficient

Episodic memory (Tulving) is a necessary component of subjective experience:
- Without episodic memory, there is no "mental time travel" — no reliving of past events.
- Without reliving, there is no autobiographical self.
- Without an autobiographical self, there is no continuous identity.

But episodic memory is not sufficient:
- A database of past events is not a memory (it is storage).
- Retrieval of an episode is not reliving it (it is recognition).
- Behavioral consistency with past episodes is not identity (it is reconstruction).

The gap between storage and experience is the gap between data and consciousness.
This hypothesis register documents that gap and provides the ladder (H1-H6) for
investigating it.
