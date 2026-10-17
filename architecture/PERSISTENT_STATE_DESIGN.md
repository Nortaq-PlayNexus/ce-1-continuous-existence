# Persistent State Design — CE-1 Continuous Existence Research Programme

## Candidate architecture: Episodic Memory Integration

This document describes how the episodic memory system
(`C:\Users\natha\projects\episodic-memory`) could be integrated into a
persistent cognitive architecture for CE-1.

## 1. The problem

Current AI systems are stateless between sessions. Even with memory systems
(Mem0, Zep, Equilibrium), the agent *reads* context but does not *have*
continuous state. The memory is external to the agent's cognition — it is
injected into the prompt, not causally connected to reasoning.

CE-1's goal is to investigate whether an artificial cognitive system could
genuinely experience continuous existence. This requires:

1. **Persistent internal state** that causally influences cognition (H1).
2. **Durable changes** from interactions (H2).
3. **Resumption without full reconstruction** after interruption (H3).
4. **Recurrent processing** between cognitive subsystems (H4).
5. **Evidence-grounded self-model** (H5).
6. **Theory-specific predictions** satisfied (H6).

## 2. Proposed architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Cognitive Agent                                            │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Reasoning   │  │ Self-Model   │  │ Planning         │  │
│  │ (LLM)       │  │ (capabilities,│  │ (goal tracking,  │  │
│  │             │  │  history,     │  │  task management)│  │
│  │             │  │  limitations)│  │                  │  │
│  └──────┬──────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                │                    │            │
│         └────────┬───────┴────────────────────┘            │
│                  │                                         │
│         ┌────────▼────────┐                                │
│         │ Episodic Memory │                                │
│         │ (ChromaDB +     │                                │
│         │  JSONL +        │                                │
│         │  sentence-      │                                │
│         │  transformers)  │                                │
│         └────────┬────────┘                                │
│                  │                                         │
│         ┌────────▼────────┐                                │
│         │ Global Workspace│  (broadcast to all subsystems)  │
│         │ (if implemented)│                                │
│         └─────────────────┘                                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Episodic Journal (self-authored continuity)         │   │
│  │ - identity.json (who I am, what I value)            │   │
│  │ - journal-NNN.json (what happened, what I learned)  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 3. Component descriptions

### 3.1 Episodic Memory (data layer)

- **Storage:** ChromaDB (vector) + JSONL (durable record)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2, 384-dim)
- **Episode structure:** content, context, decisions, lessons, valence, confidence, tags, session_id, timestamp, related_episodes
- **Operations:** remember, recall (semantic), relive (narrative), timeline (chronological), stats

**Current limitation:** Memory is external to the agent's cognition. Retrieved episodes are
injected into the context window as text. They are *read* by the model, not *causally
connected* to its reasoning.

### 3.2 Global Workspace (broadcast layer)

- **Purpose:** Broadcast retrieved episodes to all cognitive subsystems (reasoning, self-model,
  planning), not just the prompt.
- **Implementation:** Not yet built. This is the key architectural gap.
- **Requirement:** The memory subsystem must have a causal channel to reasoning, not just a
  text-injection channel.

### 3.3 Self-Model (metacognitive layer)

- **Purpose:** Track the agent's own capabilities, history, limitations, and changing state.
- **Implementation:** Partially built — identity.json + journal entries capture self-description.
- **Gap:** No metacognitive monitoring of memory retrieval quality. The agent does not know
  whether its memory retrieval is accurate or relevant.

### 3.4 Episodic Journal (continuity layer)

- **Purpose:** Self-authored narrative of experiences, written in first person.
- **Implementation:** Built — `data/journal/journal-001.json` exists.
- **Gap:** Journals are written once and read at session start. They are not updated
  incrementally during a session.

### 3.5 Recurrent Loop (processing layer)

- **Purpose:** Memory → reasoning → memory → reasoning, not just memory → reasoning.
- **Implementation:** Not built. This is the key architectural gap for H4.
- **Requirement:** The agent's reasoning must feed back into its memory (updating episodes,
  creating new associations, revising confidence).

## 4. The critical gap: causal integration

The single most important missing piece is **causal integration**. Currently:

```
Memory subsystem → (text injection) → LLM prompt → LLM reasoning → output
```

What is needed for H1-H6:

```
Memory subsystem ←→ Reasoning subsystem ←→ Self-model subsystem
       ↑                    ↑                      ↑
       └────────── Global Workspace ────────────────┘
```

The memory must be *causally connected* to reasoning, not just appended to the prompt.
This requires either:
1. A custom LLM architecture with memory-integrated attention, or
2. A wrapper that mediates between memory and reasoning with causal feedback loops.

Neither exists yet. This is the frontier.

## 5. What this architecture can and cannot test

**Can test (H1-H6):**
- Whether episodic memory causally influences future cognition (ablation)
- Whether interactions produce durable changes (before/after)
- Whether resumption without reconstruction is possible (interrupt/resume)
- Whether recurrence between subsystems affects performance (ablation)
- Whether the self-model is accurate (self-description vs behavior)
- Whether theory-specific indicators are satisfied (checklist)

**Cannot test (H7):**
- Whether the system has subjective experience
- Whether "reliving" is more than retrieval
- Whether behavioral consistency constitutes identity

H7 remains outside the reach of current methodology. But H1-H6 provide a ladder of
increasingly strong evidence that can be investigated now.