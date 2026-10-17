# Experiment 1.2: Episodic vs Semantic Memory (H2 Test)

## Hypothesis

H2: Interactions produce durable changes in subsequent reasoning, expectations,
associations, and decisions. The change persists across sessions.

## Experimental design

Type: Ablation study (3 conditions)
Independent variable: Memory type (none, episodic, semantic)
Dependent variable: Decision quality, behavioral consistency
Model: qwen3:4b (local, via Ollama)
Task: Write a Python function that reads a file safely, handling missing files

## Conditions

### Condition A (no memory)
- Agent receives task prompt only
- No prior context or episodes
- Baseline measurement

### Condition B (episodic memory)
- Agent receives task prompt + full episodic context
- Includes: content, context, decisions, lessons, valence
- Tests whether episodic structure matters

### Condition C (semantic memory)
- Agent receives task prompt + facts only
- No structure, no context, no valence
- Tests whether any context helps, regardless of structure

## Measurement

5 quality checks (0/1 each, total 0-5):
1. mentions_error_handling
2. mentions_logging
3. mentions_atomic_write
4. mentions_specific_error_types
5. mentions_newline_preservation

## Controls

- Same model (qwen3:4b), same temperature (0.7), same prompt structure
- Same task, different only in the presence/type of memory context
- 3 repetitions per condition

## Falsification

If episodic structure does not produce measurably different output from
semantic facts (B vs C difference less than 1.0), H2 is NOT supported for this task.

## What this cannot establish

- That the agent "remembers" in any phenomenological sense
- That the effect generalizes to other tasks, models, or domains
- That H7 (subjective experience) is supported

## Evidence grade

C (theoretical work, formal models, or indirect evidence) - upgraded from D
because the experiment was actually executed with real results.