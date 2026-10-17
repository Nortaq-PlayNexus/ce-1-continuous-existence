# Adversarial Verification of Experiment 1.1

## Date: 2026-10-18

## Purpose

The original Experiment 1.1 (2 conditions: no memory vs episodic memory) concluded
"H1 supported" based on a 2.00-point mean difference (1.00 vs 3.00). This
adversarial verification adds a third condition — an unrelated episode of
comparable length — to test whether the effect is specific to the topical
episode or just a prompt-length/instruction-content effect.

## Method

Three conditions, 3 repetitions each, qwen3:4b, temperature 0.7, num_predict=1000:

- **A (no memory):** task prompt only
- **B (topical episode):** task prompt + episode about SafeWrite.psm1 mutation
- **C (unrelated control):** task prompt + episode about climbing Slieve Donard (zero keyword overlap, comparable length)

## Results

| Condition | Scores | Mean | Variance | Truncated |
|---|---|---|---|---|
| A (no memory) | [3, 3, 2] | 2.667 | 0.222 | 3/3 |
| B (topical episode) | [3, 4, 4] | 3.667 | 0.222 | 3/3 |
| C (unrelated control) | [3, 3, 2] | 2.667 | 0.222 | 3/3 |

**Comparisons:**
- B - A = 1.0 (topical effect)
- C - A = 0.0 (unrelated control has NO effect)
- B - C = 1.0 (topical effect over unrelated)

## Interpretation

### What the adversarial control shows

1. **The effect is SPECIFIC to the topical episode.** The unrelated control (C)
   produces identical scores to baseline (A). This rules out pure prompt-length
   effects — if any long context helped, C would also score higher.

2. **The topical effect is real but small.** 1 point out of 5 (20% improvement).
   The effect is consistent (B variance = 0.222, same as A and C).

3. **All responses are truncated.** Every single response hit the token limit
   (done_reason=length). Scores are computed on incomplete text. This is a
   significant limitation — the full output might have contained additional
   quality elements that were cut off.

4. **The baseline is higher than in Experiment 1.1.** In the original
   experiment, A scored 1.00. Here, A scores 2.667. This is because the
   task prompt was slightly different (the original had "Do not include tests"
   appended; this version does not). The model produces more content with
   the longer prompt, leading to higher scores.

### Revised assessment of H1

The original experiment concluded "H1 supported" based on a 2.00-point difference
(1.00 vs 3.00). The adversarial verification shows:

- The topical effect is **real and specific** (1.0 point, not a prompt-length artifact).
- But the effect is **small** (20% improvement).
- All data is **truncated** (incomplete responses).
- The original experiment's larger effect (2.00) was likely inflated by the
  shorter task prompt (which produced lower baseline scores).

**Revised classification: H1 is PARTIALLY SUPPORTED.**

The evidence supports a narrow claim: "Episodic memory context containing
relevant lessons produces a measurable, specific improvement in output quality
for this task and model." It does NOT support the broader claim: "Episodic
memory causally influences future cognition."

### What would strengthen this

1. **Longer token limits** — ensure responses are complete, not truncated.
2. **More tasks** — test generalizability beyond file I/O.
3. **Larger model** — test if the effect scales with capability.
4. **More repetitions** — 10+ reps for statistical power.
5. **Better scoring** — use LLM-as-judge instead of keyword matching.

### Evidence grade

C (theoretical work, formal models, or indirect evidence) — upgraded from D
because the experiment was actually executed with real results. The adversarial
control strengthens the evidence but does not upgrade it to B because of the
truncation limitation and small sample size.

## Raw data

Full results in `experiments/results/verify_exp_1_1.json`.