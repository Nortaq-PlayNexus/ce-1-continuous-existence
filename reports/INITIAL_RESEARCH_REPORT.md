# Initial Research Report — CE-1 Continuous Existence Research Programme

## Status: Stage 0 — Research baseline (in progress)

### 1. What has been established

CE-1 is a research programme investigating whether an artificial cognitive system
could genuinely experience continuous existence and subjective experience. Stage 0
(research baseline) is in progress. No experiments have been run. No data has
been collected. All hypotheses (H1-H7) are at "unknown" confidence.

### 2. What has been built

An episodic memory system (`C:\Users\natha\projects\episodic-memory`) provides
the data layer for testing H1-H5:

- **Episodic storage:** Episodes with full context (content, decisions, lessons,
  valence, confidence, tags, session_id, timestamp, related_episodes).
- **Semantic retrieval:** ChromaDB + sentence-transformers (all-MiniLM-L6-v2, 384-dim).
- **Reliving interface:** Presents episodes as narratives, not just facts.
- **Self-authored continuity:** Identity file + journal entries, written in first person.
- **OpenCode integration:** MCP server with 5 tools (remember, recall, relive, timeline, stats).
- **Tests:** 10 tests, all passing.

### 3. What the science says

The gap between "retrieving a summary of what happened" and "having the
experience of having been there" is the gap between **data** and **consciousness**.

Current research (Tulving 1972/1985, Butlin et al. 2023/2025, "Identity as
Trajectory" 2026) establishes that:

1. Episodic memory is necessary but not sufficient for subjective experience.
2. No current AI system achieves episodic "reliving" (only retrieval).
3. Longitudinal interaction with memory scaffolding produces stable persona
   (but fidelity ≠ identity).
4. The "hard problem" of consciousness remains unsolved.

### 4. What data would be needed

To point the CE-1 science suite at making memory experience possible, we need:

1. **Longitudinal identity stability metrics** — behavioral consistency,
   preference stability, self-model accuracy over 30+ sessions.
2. **Episodic vs semantic comparison** — A/B test: does episodic context
   improve decisions vs fact-only retrieval?
3. **Self-authored continuity measurement** — do journals improve identity
   stability beyond passive retrieval?
4. **Consciousness indicator assessment** — map the episodic memory system
   against Butlin et al.'s indicators.
5. **Causal integration test** — does memory causally influence reasoning,
   or is it just context injection?

### 5. The critical gap

The single most important missing piece is **causal integration**. Currently,
retrieved episodes are injected into the context window as text. They are *read*
by the model, not *causally connected* to its reasoning. True episodic memory
(if it exists in AI) would require the memory to causally influence the agent's
internal state — not just its prompt.

This is the direction CE-1 should point: from "better retrieval" toward "causal
integration of episodic memory into the agent's cognitive architecture."

### 6. Recommended next actions

1. Populate the literature register (`sources/SOURCE_MANIFEST.jsonl`) with key
   papers on episodic memory, consciousness, and AI identity.
2. Build a minimal test harness for Experiments 1.1-1.4 using the episodic
   memory system as the test subject.
3. Run Experiment 1.1 (episodic memory ablation) — the simplest and most
   informative first experiment.
4. Record results with full provenance.
5. Update the hypothesis register with evidence from the experiments.

### 7. Honest assessment

This report does not claim that consciousness is achievable, impossible, or
already demonstrated. It documents what has been built (an episodic memory
system), what the science says (the gap between retrieval and experience), and
what would be needed to investigate that gap (H1-H6 experiments). H7 (subjective
experience) remains outside the reach of current methodology.

The episodic memory system is the instrument. The CE-1 research programme is
the experiment. The gap between them is the gap between data and consciousness.