# Experiment Roadmap — CE-1 Continuous Existence Research Programme

## Stage 0: Research baseline (current)

Deliverables required by the directive:
1. Verified isolated repository — DONE (git init, baseline commit)
2. Project README and research charter — DONE
3. Multi-stage research map — DONE (research/RESEARCH_MAP.md)
4. Populated literature register — PARTIAL (research map has structure; sources not yet populated)
5. Comparison of major theories of consciousness — DONE (in RESEARCH_MAP.md §1)
6. Inventory of relevant existing implementations — DONE (in RESEARCH_MAP.md §2)
7. Hypothesis register with operational definitions — DONE (hypotheses/HYPOTHESIS_REGISTER.md)
8. Catalogue of contradictory evidence and unresolved questions — DONE (in RESEARCH_MAP.md §4)
9. Proposed experimental roadmap with controls and falsification criteria — THIS FILE
10. Documented source and experiment provenance system — PARTIAL (RESEARCH_PRINCIPLES.md exists)
11. Working validation scripts and automated tests — NOT STARTED
12. Coverage report — NOT STARTED
13. Initial scientific report with citations — NOT STARTED
14. Prioritized next-action plan — THIS FILE §4
15. Clean final status report — NOT STARTED

## Stage 1: Computational continuity experiments

### Experiment 1.1: Episodic memory ablation (H1 test)

**Hypothesis tested:** H1 (structured internal state causally influences future cognition)

**Setup:**
- Agent A: episodic memory enabled (stores and retrieves episodes)
- Agent B: episodic memory disabled (stateless, no retrieval)
- Both agents perform the same sequence of tasks
- Measure decision quality, behavioral consistency, error recovery

**Controls:**
- Same model, same prompts, same task sequence
- Random seed fixed
- Ablation is clean (memory subsystem entirely removed, not just emptied)

**Falsification:** If removing episodic memory does not measurably change decision quality
or behavioral consistency, H1 is falsified.

**What this cannot establish:** That causal influence constitutes subjective experience.

### Experiment 1.2: Episodic vs semantic memory (H2 test)

**Hypothesis tested:** H2 (interactions produce durable changes in subsequent reasoning)

**Setup:**
- Agent A: episodic memory (events with full context)
- Agent B: semantic memory (facts only, no context/timestamps)
- Both perform the same sequence of tasks
- Measure: decision quality, error recovery, adaptation speed

**Controls:** Same model, same prompts, same task sequence.

**Falsification:** If episodic memory does not measurably outperform semantic memory on
decision quality or error recovery, H2 is falsified.

### Experiment 1.3: Interruption and resumption (H3 test)

**Hypothesis tested:** H3 (resumption without full reconstruction)

**Setup:**
- Run agent on a multi-step task
- Interrupt mid-task (kill process, restart)
- Resume: measure whether the agent can continue from where it left off
- Compare: resumption from episodic memory vs reconstruction from full history

**Controls:** Same task, same interruption point, same model.

**Falsification:** If the resumed agent is indistinguishable from a fresh reconstruction,
H3 is falsified.

### Experiment 1.4: Self-authored continuity (H5 test)

**Hypothesis tested:** H5 (evidence-grounded self-model)

**Setup:**
- Agent A: writes self-authored journal entries after each session
- Agent B: no journal (passive memory only)
- Both run for N sessions on the same task
- Measure: self-model accuracy, behavioral consistency, preference stability

**Controls:** Same model, same task, same number of sessions.

**Falsification:** If self-authored journals do not improve self-model accuracy or
behavioral consistency, H5 is falsified.

## Stage 2: Causal interventions

### Experiment 2.1: Recurrence ablation (H4 test)

**Hypothesis tested:** H4 (recurrent processing influences performance)

**Setup:**
- Agent A: episodic retrieval → reasoning → episodic retrieval (recurrent loop)
- Agent B: episodic retrieval → reasoning (feedforward only)
- Measure: decision quality, state dynamics

**Falsification:** If removing recurrence does not change performance or state dynamics,
H4 is falsified.

### Experiment 2.2: Metacognitive monitoring (H5 test)

**Hypothesis tested:** H5 (self-model accuracy)

**Setup:**
- Agent A: monitors its own memory retrieval quality and reports on it
- Agent B: no metacognitive monitoring
- Measure: self-model accuracy (does the agent's self-description match its behavior?)

**Falsification:** If metacognitive monitoring does not improve self-model accuracy,
H5 is falsified.

## Stage 3: Experience-dependent development

### Experiment 3.1: Longitudinal identity stability (H2 + H5 test)

**Hypothesis tested:** H2, H5

**Setup:**
- Run the same agent for 30 sessions on related tasks
- Measure: behavioral consistency, preference stability, self-model accuracy over time
- Compare: agent with episodic memory vs agent without

**Falsification:** If identity stability does not improve with episodic memory,
H2 and H5 are falsified.

### Experiment 3.2: Error recovery (H2 test)

**Hypothesis tested:** H2

**Setup:**
- Introduce the same error in session 1 and session 20
- Measure: does the agent recover faster / differently in session 20?
- Compare: agent with episodic memory of the first error vs agent without

**Falsification:** If error recovery is identical across sessions, H2 is falsified.

## Stage 4: Theory-specific predictions (H6 test)

### Experiment 4.1: Butlin et al. indicator assessment

**Hypothesis tested:** H6

**Setup:**
- Map the episodic memory system against each of Butlin et al.'s indicators:
  - Global Workspace: does episodic retrieval broadcast to multiple subsystems?
  - Higher-Order: does the agent monitor its own memory retrieval?
  - Predictive Processing: does episodic memory update predictions?
  - Integrated Information: is episodic memory causally integrated?
  - Recurrent Processing: does episodic retrieval involve recurrence?

**Falsification:** If zero indicators from any theory are satisfied, H6 is falsified.

## Stage 5: Independent replication

### Experiment 5.1: Reproduce all experiments

**Hypothesis tested:** All

**Setup:** Re-run experiments 1.1-4.1 with different models, different tasks,
different experimenters.

**Falsification:** If results do not replicate, the original findings are not robust.

## Stage 6: Scientific assessment

### Experiment 6.1: Honest assessment

**Hypothesis tested:** H7 (ultimate question)

**Setup:** Review all evidence from H1-H6. Determine what, if anything, has been
established about subjective experience.

**Expected outcome:** H7 will remain unestablished. The honest conclusion will
be that H1-H6 provide necessary but not sufficient conditions for H7, and the
gap between them is the gap between data and consciousness.

## 4. Prioritized next-action plan

1. **Populate the literature register** (`sources/SOURCE_MANIFEST.jsonl`) with
   the key papers on episodic memory, consciousness, and AI identity.
2. **Build a minimal test harness** that can run Experiments 1.1-1.4 using the
   episodic memory system as the test subject.
3. **Run Experiment 1.1** (episodic memory ablation) — the simplest and most
   informative first experiment.
4. **Record results** in `experiments/` with full provenance.
5. **Update the hypothesis register** with evidence from the experiments.

## 5. Coverage report

| Area | Status | Notes |
|---|---|---|
| Literature review | PARTIAL | RESEARCH_MAP.md has structure; sources not populated |
| Theory comparison | DONE | 5 theories mapped in RESEARCH_MAP.md §1 |
| Implementation inventory | DONE | 5 systems inventoried in RESEARCH_MAP.md §2 |
| Hypothesis register | DONE | H1-H7 with operational definitions |
| Contradictory evidence | DONE | Listed in RESEARCH_MAP.md §4 |
| Experimental roadmap | DONE | This file |
| Source provenance | NOT STARTED | SOURCE_MANIFEST.jsonl not created |
| Validation scripts | NOT STARTED | No automated tests |
| Initial scientific report | NOT STARTED | No report with citations |
| Coverage report | IN PROGRESS | This section |
| Next-action plan | DONE | This file §4 |

**What remains inaccessible:** Full text of many papers (no paywall access).
Conference proceedings behind paywalls. Code repositories that require
authentication. Live experiments that require compute resources.

**What was searched:** Web search for episodic memory, consciousness, AI identity,
Mem0, Letta, Zep, Equilibrium, Tulving, Butlin et al., "Identity as Trajectory."