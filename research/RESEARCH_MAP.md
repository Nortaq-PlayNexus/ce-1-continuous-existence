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

### Integrated Information Theory (Tononi, 2004; IIT 4.0: Albantakis et al. 2023)
- **Core claim:** Consciousness corresponds to integrated information (Phi).
  A system is conscious to the degree that its parts are causally integrated.
- **AI relevance:** If an AI's memory subsystem is causally integrated with its
  reasoning (not just appended to the prompt), this would increase Phi.
- **Status:** Mathematically rigorous but computationally intractable for large
  systems.
- ⚠️ **CORRECTED 2026-10-18 — two errors in the inherited version of this entry.**
  (1) The original entry described IIT only as "controversial (IIT has been
  criticized as pseudoscience by some)". That is weaker than the evidence. In
  the preregistered adversarial collaboration of Cogitate et al. 2025
  (Nature 642:133-142, DOI 10.1038/s41586-025-08888-1, n=256), IIT's
  posterior-cortex synchrony prediction **was not met**, with a Bayes factor of
  1.15-4.9 favouring the null. IIT's central empirical prediction currently
  has a preregistered negative result against it.
  (2) IIT is **not** simply a peer of the other theories on this list. The
  principal AI-consciousness indicator framework (Butlin et al. 2023,
  arXiv:2308.08708) **explicitly excludes IIT** on the grounds that IIT is not
  compatible with computational functionalism, which that framework adopts as a
  working hypothesis. These are incompatible theoretical commitments, not
  adjacent options.
- **Source:** `butlin2023cai`, `cogitate2025`, `albantakis2023iit40`.

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

### Letta / MemGPT (Packer et al. 2023)
- **Architecture:** OS-style tiered memory (core/recall/archival). Agent manages
  its own memory via function calls.
- **Source:** Packer et al. 2023, "MemGPT: Towards LLMs as Operating Systems",
  arXiv:2310.08560, DOI 10.48550/arXiv.2310.08560 — `packer2023memgpt`.
- **Strength:** Agent has agency over memory. Can promote/archive based on
  relevance.
- **Limitation:** Still retrieval-based. No subjective experience. Full runtime
  replacement required.
- **Relevance to CE-1:** Closest existing system to "agent-managed memory."
  The agent's agency over its own memory is a step toward H5 (self-model).
- ⚠️ **Note for the causal-integration agenda:** MemGPT's own framing is
  *paging* — "an illusion of an extended virtual memory" — which is precisely
  the retrieval mechanism that CE-1's own audit (RESEARCH_AUDIT.md §3, §12)
  showed is confounded with prompt content when used to test H1. A system built
  on this pattern cannot by itself demonstrate persistent cognitive state.

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

## 5. Sources

Provenance lives in `sources/SOURCE_MANIFEST.jsonl`, validated by
`scripts/validate_sources.py`. **4 sources are currently verified** — this is
far short of the coverage the directive requires (see
`sources/ACCESS_LIMITATIONS.md` for exactly what has and has not been searched).

Verified so far: `butlin2023cai`, `cogitate2025`, `albantakis2023iit40`,
`packer2023memgpt`.

⚠️ **Still uncited in this document**, and therefore not yet checkable:
Mem0, Zep/Graphiti, the Apart Research "Identity as Trajectory" citation
(retracted — see the audit), and the primary literature for RPT, AST, HOT,
predictive processing, and biological naturalism. Any claim in this file that
rests on those remains **grade D** until sourced.