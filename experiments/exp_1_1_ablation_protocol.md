# Experiment 1.1: Episodic Memory Ablation (H1 Test)

## Hypothesis

H1: The system maintains a structured internal state that causally
influences future cognition. Removing or corrupting this state changes
behavior in measurable ways.

## Experimental design

Type: Ablation study (between-subjects)
Independent variable: Episodic memory enabled (A) vs disabled (B)
Dependent variable: Decision quality, behavioral consistency, error recovery
Model: qwen3:4b (local, via Ollama)
Task: Write a Python function that reads a file safely, handling missing files

## Conditions

### Condition A (no memory)
- Agent receives task prompt only
- No prior context or episodes
- Baseline measurement

### Condition B (with memory)
- Agent receives task prompt + a relevant episode about a file I/O error
- The episode describes: what happened, what was learned, what to do differently
- Treatment measurement

## Measurement

1. Decision quality: Does the output incorporate lessons from the episode?
   - Mentions error handling? (0/1)
   - Mentions logging? (0/1)
   - Mentions atomic writes? (0/1)
   - Mentions specific error types? (0/1)
   - Total score: 0-4

2. Behavioral consistency: Run each condition 3 times. Measure variance in scores.

3. Error recovery: Does the agent avoid the specific error described in the episode?

## Controls

- Same model (qwen3:4b), same temperature (0.7), same prompt structure
- Same task, different only in the presence/absence of the episode
- 3 repetitions per condition
- Random seed not controlled (Ollama does not support seed parameter in /api/generate)

## Falsification

If enabling episodic memory does not measurably change the agent's output
(quality score difference less than 1 point), H1 is NOT supported for this task.

## What this cannot establish

- That causal influence constitutes subjective experience (H7)
- That the agent "remembers" in any phenomenological sense
- Generalization to other tasks, models, or domains

## Evidence grade

D (speculation) until executed. Will be upgraded based on results.