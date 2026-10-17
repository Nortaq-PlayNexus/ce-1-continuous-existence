# Hypothesis Register — CE-1 Continuous Existence Research Programme

## H1: Structured internal state causally influences future cognition

**Operational definition:** The system maintains a persistent internal state (memory,
associations, expectations) that is read by and causally influences subsequent
reasoning, decision-making, and output generation. Removing or corrupting this
state changes behavior in measurable ways.

**Motivation:** If a system's behavior is identical with and without persistent
state, then the state is epiphenomenal, not causal. Causal influence is a
necessary precondition for any claim of genuine cognitive continuity.

**Supporting evidence:** None yet (Stage 0). Theoretical basis: global workspace
theory, predictive processing.

**Contrary evidence:** Stateless LLMs produce coherent outputs without any
persistent state. Behavioral consistency can be achieved through prompt
engineering alone.

**Measurements:** Ablation study — remove persistent state, measure decision
quality change. Effect size, confidence interval, p-value.

**Falsification condition:** If removing persistent state does not measurably
change decision quality or behavioral consistency, H1 is falsified.

**What this cannot establish:** That the causal influence constitutes subjective
experience. H1 is about mechanism, not phenomenology.

**Current confidence:** Unknown (no experiments run).

---

## H2: Interactions produce durable changes in subsequent reasoning

**Operational definition:** After an interaction (conversation, task, error),
the system's subsequent reasoning, expectations, associations, and decisions
are measurably different from what they would have been without that interaction.
The change persists across sessions.

**Motivation:** If interactions do not change the system, then it is a stateless
function of its inputs. Durable change is the defining property of learning.

**Supporting evidence:** None yet. Theoretical basis: connectionist learning,
episodic memory theory (Tulving).

**Contrary evidence:** LLMs can appear to "learn" within a context window but
forget everything between sessions. Fine-tuning is the only durable change,
and it is not interaction-driven in the relevant sense.

**Measurements:** Before/after decision patterns with episodic memory enabled vs
disabled. Effect size, confidence interval, p-value.

**Falsification condition:** If enabling episodic memory does not measurably
change subsequent decision patterns, H2 is falsified.

**What this cannot establish:** That durable changes constitute subjective
experience. H2 is about learning, not phenomenology.

**Current confidence:** Unknown (no experiments run).

---

## H3: Resumption after interruption without full reconstruction

**Operational definition:** The system can resume after an interruption (power
loss, process restart, session boundary) without reconstructing its entire
state through ordinary conversational memory retrieval. The resumed state
is measurably different from a fresh reconstruction.

**Motivation:** If the system must re-read its entire history to "remember,"
then it is using retrieval, not persistence. True persistence survives
interruption without full reconstruction.

**Supporting evidence:** None yet. Theoretical basis: OS virtual memory
(MemGPT/Letta), persistent process state.

**Contrary evidence:** Current LLM systems have no persistent process state.
Every session is a fresh process. "Resumption" is always reconstruction.

**Measurements:** Interrupt, resume, measure state continuity vs
retrieval-based reconstruction. Difference in decision quality, response
latency, and self-model accuracy.

**Falsification condition:** If the resumed system is indistinguishable from a
fresh reconstruction, H3 is falsified.

**What this cannot establish:** That resumption constitutes subjective
continuity. H3 is about state, not experience.

**Current confidence:** Unknown (no experiments run).

---

## H4: Recurrent processing influences performance and state dynamics

**Operational definition:** Recurrent information processing and communication
between cognitive subsystems (memory, reasoning, self-model, planning) measurably
influence performance and internal-state dynamics. Removing recurrence changes
behavior.

**Motivation:** Global Workspace Theory and Recurrent Processing Theory both
predict that recurrence is necessary for conscious processing. If recurrence
does not affect behavior, it is not doing the work the theories predict.

**Supporting evidence:** None yet. Theoretical basis: Global Workspace Theory,
Recurrent Processing Theory.

**Contrary evidence:** Feedforward systems can produce sophisticated behavior.
Recurrence may be an implementation detail, not a consciousness-relevant feature.

**Measurements:** Ablate recurrent connections, measure performance and
state-dynamics changes. Effect size, confidence interval, p-value.

**Falsification condition:** If removing recurrence does not measurably change
performance or state dynamics, H4 is falsified.

**What this cannot establish:** That recurrence constitutes subjective
experience. H4 is about architecture, not phenomenology.

**Current confidence:** Unknown (no experiments run).

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

**Current confidence:** Unknown (no experiments run).

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

**Current confidence:** Unknown (no experiments run).

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

**Current confidence:** Unknown (and possibly unknowable with current methods).

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