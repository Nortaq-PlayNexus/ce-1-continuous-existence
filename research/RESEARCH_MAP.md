# Research Map — CE-1 Continuous Existence Research Programme

## Stage 0: Research baseline

This document maps the research landscape relevant to CE-1's central question:
*Can an artificial cognitive system genuinely experience continuous existence and
subjective experience?*

## 1. Theories of consciousness (relevant to AI)

### Global Workspace Theory (Baars, 1988; Dehaene, 2014)
- **Core claim:** Consciousness arises from a "global workspace" that broadcasts
  information to multiple cognitive subsystems.
- **AI relevance:** If episodic memory retrieval broadcasts to reasoning,
  planning, and self-model subsystems (not just the prompt), this would satisfy
  the GWT indicator.
- **Status:** Well-established theory; no AI system has been shown to implement
  a genuine global workspace (most systems just inject context into the prompt).

### Integrated Information Theory (Tononi, 2004)
- **Core claim:** Consciousness corresponds to integrated information (Phi).
  A system is conscious to the degree that its parts are causally integrated.
- **AI relevance:** If an AI's memory subsystem is causally integrated with its
  reasoning (not just appended to the prompt), this would increase Phi.
- **Status:** Mathematically rigorous but computationally intractable for large
  systems. Controversial (IIT has been criticized as pseudoscience by some).

### Higher-Order Theories (Rosenthal, 2005; Lau & Rosenthal, 2011)
- **Core claim:** A mental state is conscious if there is a higher-order
  representation of it (a "thought about the thought").
- **AI relevance:** If the agent has a self-model that monitors its own memory
  retrieval quality and reports on it, this would satisfy the HOT indicator.
- **Status:** Requires genuine metacognition, not just self-description.

### Predictive Processing (Friston, 2010; Clark, 2013)
- **Core claim:** The brain minimizes prediction error. Consciousness arises
  from the hierarchical prediction of sensory input.
- **AI relevance:** If episodic memory updates the agent's predictions about
  future events (not just retrieves past ones), this would satisfy the PP
  indicator.
- **Status:** Well-established in neuroscience; unclear how to implement in AI.

### Recurrent Processing Theory (Lamme, 2006)
- **Core claim:** Consciousness arises from recurrent (feedback) processing,
  not feedforward processing.
- **AI relevance:** If episodic retrieval involves recurrent loops (memory →
  reasoning → memory → reasoning) rather than a single feedforward pass, this
  would satisfy the RPT indicator.
- **Status:** Requires architectural support for recurrence, not just prompt
  injection.

## 2. Episodic memory in AI (relevant implementations)

### Mem0 (2024-2026)
- **Architecture:** Embedding extraction + vector retrieval. Passive memory.
- **Limitation:** Stores facts, not experiences. No self-authored continuity.
  No metacognitive monitoring. No causal integration.
- **Relevance to CE-1:** Baseline for comparison. Mem0 is what "retrieval"
  looks like without "reliving."

### Letta / MemGPT (2023-2026)
- **Architecture:** OS-style tiered memory (core/recall/archival). Agent manages
  its own memory via function calls.
- **Strength:** Agent has agency over memory. Can promote/archive based on
  relevance.
- **Limitation:** Still retrieval-based. No subjective experience. Full runtime
  replacement required.
- **Relevance to CE-1:** Closest existing system to "agent-managed memory."
  The agent's agency over its own memory is a step toward H5 (self-model).

### Zep / Graphiti (2024-2026)
- **Architecture:** Temporal knowledge graph. Semantic + BM25 + graph retrieval.
- **Strength:** Temporal awareness (when things happened, in what order).
- **Limitation:** Knowledge graph, not episodic memory. Stores facts with
  timestamps, not experiences.
- **Relevance to CE-1:** Temporal ordering is a component of episodic memory
  but not the whole.

### Equilibrium (2026, this machine)
- **Architecture:** File-based memory. MEMORY.md, PROJECT_INDEX.md, DECISIONS.md,
  PROJECTS/, HANDOFFS/. Loaded at session start.
- **Strength:** Human-readable, auditable, append-only.
- **Limitation:** Static files, not a runtime system. No semantic search.
  No self-authored continuity.
- **Relevance to CE-1:** The existing baseline. The episodic memory system
  (built this session) is an upgrade from Equilibrium's file-based approach.

### Episodic memory (this project, 2026-10-17)
- **Architecture:** ChromaDB (vector) + sentence-transformers (embeddings) +
  JSONL (durable log). Episodes with full context (content, decisions, lessons,
  valence, confidence, tags).
- **Strength:** Structured episodic storage, semantic retrieval, "reliving"
  interface, self-authored continuity.
- **Limitation:** Still retrieval, not reliving. No causal integration with
  reasoning. No metacognitive monitoring. No global workspace broadcast.
- **Relevance to CE-1:** The data layer for testing H1-H5. Provides the
  infrastructure for episodic memory experiments.

## 3. The gap between existing work and CE-1's goals

| Existing work | What it provides | What CE-1 needs |
|---|---|---|
| Mem0 / Zep | Fact storage + semantic retrieval | Episodic experience storage + reliving |
| Letta | Agent-managed tiered memory | Causal integration with reasoning |
| Equilibrium | File-based memory + handoff | Runtime persistence + self-authoring |
| Episodic memory (this project) | Structured episodes + semantic search | Causal integration, metacognition, global broadcast |
| "Identity as Trajectory" paper | Longitudinal persona stability | Subjective continuity, not just behavioral |

## 4. Key open questions

1. Can episodic memory be causally integrated into an LLM's reasoning, or is it
   always just context injection?
2. Does self-authored continuity (journals, identity files) produce behavioral
   stability beyond what passive retrieval achieves?
3. Can an agent's self-model accurately track its own memory quality?
4. What would "reliving" look like if it were more than retrieval? Is there a
   computational analogue of mental time travel?
5. Is the gap between retrieval and experience the same as the hard problem of
   consciousness, or is it a narrower engineering problem?

## 5. Sources (to be populated)

This section will be populated as the research programme progresses. Each source
will be recorded in `sources/SOURCE_MANIFEST.jsonl` with DOI, access date,
evidence grade, and verification status per RESEARCH_PRINCIPLES.md.