# VOID — DO NOT CITE AS DATA

This file was produced by `experiments/exp_1_3_state_ablation.py` using
`qwen3:4b`. **All 27 runs in it are truncated** (`done_reason=length`): the
model rambled past the `num_predict` budget on every single call. Scoring
truncated text is not a measurement.

Consequences:

- The `p = 0.0173` in this file is **not a finding**. It is a truncation artifact.
- `qwen3:4b` does not terminate on this task at any budget tested (up to 1000
  tokens, ~4400 chars) even with an explicit output-format constraint.
- Retained unmodified for provenance.

**Valid replacement: `exp_1_3_results_gemma.json`** — same experiment on
`gemma3:4b`, which terminates cleanly. 13 reps, seeded, 0/26 truncated.
B - A = +0.769, Mann-Whitney p = 0.0650, not significant. H1 INCONCLUSIVE.
See `research/RESEARCH_AUDIT.md` section 14.
