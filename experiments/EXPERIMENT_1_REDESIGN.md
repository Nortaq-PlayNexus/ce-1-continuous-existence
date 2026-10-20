# Experiment 1 Redesign — Protocol Document

**Status:** Protocol document, not a claim that the experiment has already succeeded.

**Date:** 2026-10-18

## 1. Research question

Does structured episodic memory (content + context + decisions + lessons + valence)
causally influence an agent's output quality beyond what can be explained by
prompt length, instruction content, or in-context learning?

## 2. Hypothesis definitions

### H1: Causal state influence
The system maintains a structured internal state (episodic memory) that
causally influences future cognition. Removing or corrupting this state
changes behavior in measurable ways.

### H2: Durable change
Interactions produce durable changes in subsequent reasoning, expectations,
associations, and decisions. The change persists across sessions.

## 3. Primary and secondary outcomes

- **Primary:** Decision quality score (0-5) on a file-I/O safety task
- **Secondary:** Behavioral consistency (variance across repetitions)
- **Secondary:** Error recovery (does the agent avoid previously-encountered errors?)

## 4. Conditions

1. **A (store empty / baseline):** Task prompt only. No prior context.
2. **B (retrieved memory):** Task prompt + episodic memory context.
3. **C (prompt-only control):** Task prompt + unrelated episode of comparable length.
4. **D (semantic-only control):** Task prompt + facts only (no structure, no context).
5. **E (length-matched control):** Task prompt + unrelated text of identical length to B.

## 5. How prompts are held constant

- All conditions use the same task prompt (TASK_PROMPT).
- The only difference is the presence/type of memory context prepended.
- Prompt length is measured and reported for each condition.
- If lengths differ by more than 10%, the condition is flagged.

## 6. How memory content is injected

- Condition B: full episodic context (content + context + decisions + lessons + valence)
- Condition C: unrelated episode (comparable length, zero keyword overlap with scoring rubric)
- Condition D: semantic facts only (no structure, no context, no valence)
- Condition E: lorem ipsum or unrelated text of identical length to B

## 7. How prompt length and token count are measured and balanced

- Character count and estimated token count (via Ollama's eval_count) recorded per trial.
- If any condition's mean prompt length differs by more than 10% from the longest,
  a warning is logged.
- Token count is recorded in the result file for each trial.

## 8. How lexical overlap between episode text and scoring criteria is prohibited or quantified

- The scoring rubric keywords MUST NOT appear in the episode text.
- A pre-run check verifies that no scoring keyword appears in any episode text.
- If overlap is detected, the experiment aborts with an error.
- The unrelated control (C) must have zero keyword overlap with the scoring rubric.

## 9. How keyword-copying is prevented

- Scoring keywords are defined AFTER the episode text is written, not before.
- The episode text is checked against the scoring keywords; if any match, the
  experiment aborts.
- An independent judge (LLM-as-judge) scores a subset of responses to cross-validate
  the keyword-based scores.

## 10. The scoring rubric

5 quality checks (0/1 each, total 0-5):
1. mentions_error_handling: any of ["try", "except", "error", "handle"]
2. mentions_logging: any of ["log", "logging", "audit"]
3. mentions_atomic_write: any of ["atomic", "temp", "rename", "replace"]
4. mentions_specific_error_types: any of ["FileNotFoundError", "OSError", "IOError", "PermissionError"]
5. mentions_newline_preservation: any of ["newline", "line ending", "CRLF", "LF", "\n", "\r\n"]

**Critical:** The scoring keywords must NOT appear in the episode text. The episode
describes a real experience; the scoring checks whether the agent *learned* from it,
not whether it *copied* words from it.

## 11. Whether an independent judge is used

Yes. An LLM-as-judge (same model, separate prompt) scores a subset of responses
(20%) to cross-validate the keyword-based scores. The judge is given the episode
and the response, and asked to rate whether the response shows evidence of learning
from the episode (0-5 scale).

## 12. Judge blinding, if feasible

The judge receives the response and the episode, but not the condition label.
This is partial blinding — the judge can infer the condition from the response content.

## 13. How judge reliability is measured

- Inter-rater reliability between keyword scores and judge scores (Cohen's kappa).
- If kappa < 0.6, the scoring method is unreliable and must be revised.

## 14. Required response completion criteria

- Response must be non-empty.
- `done_reason` must be "stop" (not "length").
- Response must contain at least one complete function definition.
- If any criterion is not met, the trial is INVALID and excluded from analysis.

## 15. Invalid-trial handling

- Invalid trials are recorded with `valid: false` and `invalidity_reason`.
- A condition with fewer than `min_valid` (2) valid trials → verdict is INVALID_RUN.
- Invalid trials are NOT scored and do NOT count toward the mean.
- The experiment summary reports valid/invalid counts per condition.

## 16. Required sample size and rationale

- Minimum 10 valid repetitions per condition.
- Rationale: with variance ~0.5 on a 0-5 scale, 10 reps per condition gives
  approximately 80% power to detect a 1-point effect at p=0.05 (two-sided).
- If any condition has fewer than 10 valid trials, the experiment is INVALID_RUN.

## 17. Randomization procedure

- Seeds are generated once at the start of the experiment using `random.Random(20261018)`.
- Seeds are assigned to conditions in round-robin order.
- The same seed is used for both the generation and the judge (seed + 1 for judge).

## 18. Seed policy

- Seeds are recorded in the result file.
- The same seeds produce the same prompts (but not necessarily the same outputs,
  since Ollama does not guarantee deterministic generation even with seeds).
- "Exact reproducibility" is not claimed. "Approximate reproducibility" is claimed.

## 19. Model and generation settings

- Model: qwen3:4b (local, via Ollama)
- Temperature: 0.7
- num_predict: 2000 (increased from 1000 to reduce truncation)
- think: False (to get response, not thinking tokens)
- Ollama version: 0.34.2 (recorded)

## 20. Statistical analysis plan

- Primary: Mann-Whitney U (two-sided, normal approximation with tie correction)
- Secondary: Bootstrap 95% CI (2000 iterations)
- Secondary: Mean and variance per condition
- Secondary: Cohen's kappa between keyword scores and judge scores

## 21. Threshold and tolerance, declared before data collection

- THRESHOLD = 1.0 (minimum mean difference to support H1/H2)
- TOLERANCE = 1e-9
- Comparison: `round(mean_diff, 3) - THRESHOLD > -TOLERANCE`
- Both sides rounded to 3 decimal places before comparison.
- Threshold declared here, before any data collection. Not adjustable post-hoc.

## 22. Multiple-comparison policy

- 5 quality checks per condition. No correction applied (exploratory).
- If the experiment is upgraded to confirmatory, apply Bonferroni correction
  (alpha = 0.05/5 = 0.01).

## 23. Stopping rule

- Stop after 10 valid repetitions per condition.
- If a condition has fewer than 10 valid trials after 15 attempts, stop and
  report INVALID_RUN.

## 24. Exclusion rule

- A trial is excluded if: truncated, empty, unparseable, or fails completion criteria.
- Excluded trials are recorded with `valid: false` and `invalidity_reason`.
- Exclusion criteria are fixed before data collection. No post-hoc changes.

## 25. What outcome would count as support, null evidence, or inconclusive

- **Support:** B (episodic) mean > C (unrelated control) mean by >= 1.0 point,
  with p < 0.05, no truncation, and kappa >= 0.6 between keyword and judge scores.
- **Null evidence:** No measurable difference between B and C (difference < 0.5).
- **Inconclusive:** Difference between B and C is 0.5-1.0, or kappa < 0.6, or
  any truncation occurred, or sample size < 10.

## 26. What the experiment cannot establish

- Textual retrieval is not equivalent to phenomenal memory.
- A performance difference alone would not prove conscious experience.
- Prompt-content and in-context-learning explanations must be addressed.
- The experiment tests a narrow operational effect, not consciousness itself.
- Even if H1 is supported, it does not imply H7 (subjective experience).
- Even if H1 is supported, it does not imply identity or continuity.

## Evidence grade

D (speculation) until executed. Will be upgraded based on results.

## Preregistration status

This document constitutes a pre-registration of the experiment design. The
threshold (1.0), tolerance (1e-9), sample size (10), and scoring rubric are
declared here before any data collection. Any deviation from this protocol
must be documented as a protocol violation.