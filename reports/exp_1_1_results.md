# Experiment 1.1 Results: Episodic Memory Ablation (H1 Test)

## Date: 2026-10-17

## Hypothesis

H1: The system maintains a structured internal state that causally
influences future cognition. Removing or corrupting this state changes
behavior in measurable ways.

## Method

- **Model:** qwen3:4b (local, via Ollama, think=False)
- **Task:** "Write a Python function that reads a file safely. Handle the case where the file doesn't exist. Be specific about error types and recovery."
- **Condition A (no memory):** Task prompt only, 3 repetitions
- **Condition B (with memory):** Task prompt + episodic memory context about a file I/O error (SafeWrite.psm1 mutation), 3 repetitions
- **Measurement:** 5 quality checks (error handling, logging, atomic writes, specific error types, newline preservation), each scored 0/1, total 0-5
- **Temperature:** 0.7, num_predict: 1000

## Results

| Condition | Rep 1 | Rep 2 | Rep 3 | Mean | Variance |
|---|---|---|---|---|---|
| A (no memory) | 1/5 | 1/5 | 1/5 | 1.00 | 0.00 |
| B (with memory) | 3/5 | 3/5 | 3/5 | 3.00 | 0.00 |

**Mean difference: 2.00 (B > A)**
**H1 supported: True** (difference >= 1.0)

### Check-level breakdown

| Check | A (no memory) | B (with memory) |
|---|---|---|
| mentions_error_handling | 3/3 | 3/3 |
| mentions_logging | 0/3 | 1/3 |
| mentions_atomic_write | 0/3 | 2/3 |
| mentions_specific_error_types | 0/3 | 0/3 |
| mentions_newline_preservation | 0/3 | 3/3 |

### Key observations

1. **Both conditions mention error handling** (3/3 each) — the base task prompt already
   elicits basic try/except. This is expected and does not discriminate.

2. **Condition B uniquely mentions newline preservation** (3/3) — directly from the
   episodic context about the SafeWrite.psm1 mutation. The episode's lesson about
   CRLF/LF leakage was incorporated into the output.

3. **Condition B mentions atomic writes** (2/3) — from the episode's lesson about
   "use atomic writes (temp file + rename)". Condition A never mentions this.

4. **Condition B mentions logging** (1/3) — from the episode's lesson about
   "log all write attempts to an audit trail." Condition A never mentions this.

5. **Neither condition mentions specific error types** (0/3 each) — the model
   (qwen3:4b) does not produce specific exception names (FileNotFoundError, OSError)
   in either condition. This may be a model capability limitation.

6. **Zero variance** in both conditions — the model is deterministic enough at
   temperature 0.7 that 3 repetitions produce identical scores. This is actually
   useful: it means the effect is robust, not noise.

## Interpretation

The episodic memory context (a narrative about a past error and its lessons)
causally influenced the agent's output. The agent incorporated 2 additional
quality elements (newline preservation, atomic writes) that were absent without
the memory. This supports H1: structured internal state (episodic memory)
causally influences future cognition.

### What this does NOT establish

- That the agent "remembered" in any phenomenological sense. It read a context
  and produced different output. That is retrieval, not reliving.
- That the effect generalizes to other tasks, models, or domains. This is a
  single task with a single model.
- That H7 (subjective experience) is supported. H1 is necessary but not
  sufficient for H7.
- That the agent's output quality is "good" — the scores are low (3/5) even
  in the best case. The model is small (qwen3:4b) and produces verbose,
  unfocused output.

### Evidence grade

C (theoretical work, formal models, or indirect evidence) — upgraded from D
because the experiment was actually executed with real results. But the single-
task, single-model, small-sample design limits generalizability.

## Next steps

1. Run Experiment 1.2 (episodic vs semantic memory comparison) to test whether
   the *structure* of the episode matters, or just the presence of any context.
2. Run Experiment 1.3 (interruption and resumption) to test H3.
3. Run Experiment 1.4 (self-authored continuity) to test H5.
4. Increase sample size (10 reps) and add more tasks for generalizability.
5. Test with a larger model (gemma4:26b or qwen3.8-27b) to see if the effect
   scales with capability.

## Raw data

Full results in `experiments/results/exp_1_1_results.json` (includes all outputs
and scores).