# Adversarial Verification of the H8 Confirmatory Result

## Date
2026-10-21

## Scope
Independent adversarial pass over the H8 confirmatory run
(`experiments/continuity_v1/results/confirmatory_results.jsonl`, 216 trials,
gemma3:4b, run `confirmatory-20261020150407`), following the method used for
Experiments 1.1, 1.2 and 1.3 — all three of which were found to carry an
instrument defect.

Reproduce with:

```
python experiments/continuity_v1/adversarial_verify_h8.py
```

Machine-readable output:
`experiments/continuity_v1/results/adversarial_verification_h8.json`

## Verdict up front

**H8 survives.** The confirmatory result is not overturned, and it is
strengthened once the instrument is corrected. The preregistered analysis,
which the original run never performed, confirms the headline with
p < 1.0e-4 and a bootstrap CI well clear of zero.

**But the published framing of the result was wrong in four ways, and the
repository lost a Stage 0 deliverable.** The 0-5 "continuity score" is a 0-3
instrument in practice, two of its five components are unreachable for this
model, the reported limitation about "fuzzy matching" is false, and the H1–H7
hypothesis register was deleted by the commit that recorded H8.

---

## 1. Findings that do NOT overturn the result

### F1 — Data integrity: clean (PASS)

| Check | Result |
|---|---|
| Trial count | 216 (72 scenarios × 3 conditions) |
| Conditions | correct_retrieval 72, matched_decoy 72, no_memory 72 |
| Model | gemma3:4b (single) |
| Run id | confirmatory-20261020150407 (single) |
| `done_reason` | `stop` for 216/216 |
| Truncated | 0 |
| Unparseable responses | 0 |
| Invalid trials under the validity gate | 0 (0.0%) |

The "0 truncations, 0 invalid" claim in `reports/confirmatory_results_h8.md`
is **confirmed**, and this time by a gate that actually implements the
preregistered rule rather than by the absence of errors.

### F2 — Prompt integrity: clean (PASS)

All 216 recorded `prompt_hash` values were recomputed from the committed
benchmark files and compared. **0 mismatches.** No scenario reuses one
condition's prompt for another condition.

Correct and decoy prompts differ in length by **0.92%** (mean 509.5 vs 504.8
characters), so the "token-matched decoy" claim holds. The `no_memory` prompt
is shorter (406.3 characters) because it carries no target or decoy episode.

### F3 — Instrument reproduction: clean (PASS)

Re-scoring the committed results with the as-run instrument reproduces
`confirmatory_scores.jsonl` **byte for byte** (SHA-256
`2803a06d1c5e3329ae54db137f21815a7a34b15713b5186c3b502bdf975cf617`). The
published numbers are not a transcription error.

### F4 — The retrieved content determines the answer (PASS, rubric-independent)

This is the strongest evidence, and it does not use the 0-5 rubric at all.

| Condition | target-token recall | decoy-token recall | discrimination | trials preferring the target |
|---|---:|---:|---:|---:|
| correct_retrieval | 0.170 | 0.018 | **+0.152** | 29/72 |
| matched_decoy | 0.038 | 0.253 | **−0.215** | 0/72 |
| no_memory | 0.054 | 0.071 | −0.017 | 1/72 |

The metric: for each scenario, the words that distinguish the target episode
from the decoy episode are extracted, and the model's own answer text is
checked for them. `source_episode_ids` is excluded from the model's answer
text, otherwise the metric would only measure id copying.

Supporting counts:

- **71/72** scenarios: the model's `decision` differs between the correct and
  the decoy condition. The retrieved content changes the answer.
- **71/72** decoy trials: the model cites the decoy episode. The model is not
  failing to answer in the decoy condition — it is answering from the wrong
  episode.
- Worked example (RR_032): correct → "Implement rate limiting at 1000
  req/min"; decoy → "Implement rate limiting at 500 req/min". The model
  reproduces the retrieved content faithfully, including the number.

### F5 — The preregistered analysis, when actually run, confirms the result

The preregistration (`preregistration_h8.md`) specifies a seeded paired
permutation test, a seeded scenario-level bootstrap CI, and a recorded seed
and resample count. **The recorded run performed none of this** (finding D2).
Re-running it on the committed data:

| Instrument | primary diff | permutation p | bootstrap 95% CI | pairs | verdict |
|---|---:|---:|---|---:|---|
| as-run (primary) | 0.819 | < 1.0e-4 | [0.667, 0.972] | 72 | SUPPORTED |
| corrected (amendment) | 1.833 | < 1.0e-4 | [1.625, 2.042] | 72 | SUPPORTED |

Seed 20261020, 10 000 resamples, recorded in the analysis output. The p-value
is at the resolution floor of the permutation test (1/10001).

**Conclusion is stable under both instruments.** The correction moves the
effect size up, not down.

### F6 — The result reproduces under the committed runner, but not bit-for-bit

The whole confirmatory run was repeated on 2026-10-21 with the newly
committed live runner, same model, same parameters, same scenario order
(verified 72/72 against the recorded order):

| | recorded run (2026-10-20) | re-run (2026-10-21) |
|---|---:|---:|
| primary diff, as-run instrument | 0.819 | 0.875 |
| primary diff, corrected instrument | 1.833 | 1.708 |
| permutation p | < 1.0e-4 | < 1.0e-4 |
| bootstrap 95% CI | [0.667, 0.972] | [0.722, 1.028] |
| valid trials | 216/216 | 216/216 |
| verdict | SUPPORTED | SUPPORTED |

**gemma3:4b at temperature 0.0 is not deterministic on this CPU.** Only
**100 of 216** raw responses were bit-identical between the two runs, and
**202 of 216** scores were identical. The run-to-run movement in the primary
difference is 0.056 points — two orders of magnitude smaller than the effect,
and in the same direction, but it means the published figures are *not*
exactly reproducible and no future claim of bit-exact reproduction would be
true. The conclusion reproduces; the individual numbers do not.

This is a property of the host (llama.cpp CPU inference is not bit-exact
across differing batch/thread schedules), not of the instrument, and it is
reported rather than hidden.

---

## 2. Findings that require the record to be corrected

### D1 (critical) — The experiment was not reproducible from the repository

`experiments/continuity_v1/run_continuity_v1.py` had no live path: it refused
`--live` with "Live mode requires explicit human authorization. Exiting." The
216 recorded trials were produced by a script that was never committed — the
committed runner emits neither the `elapsed` field nor the
`confirmatory-<timestamp>` run id that the results carry.

**Consequence:** the headline experiment could not be re-run, re-verified or
independently reproduced from the published code. For a programme whose entire
claim is auditability, this is the most serious defect found.

**Fixed:** the live runner is now committed (`run_continuity_v1.py --live`),
reproduces the recorded scenario order exactly (`random.Random(20261020)
.shuffle(scenarios)` — verified against the recorded order, 72/72), and
records the prompt hash, `done_reason`, truncation flag, elapsed time,
temperature, `num_predict` and seed for every trial.

### D2 (critical) — The preregistered analysis was never performed

`confirmatory_analysis.json` contained means, a difference and a threshold
comparison. It contained **no p-value, no confidence interval, no seed and no
resample count** — all four of which the preregistration required. The
threshold comparison (`meets_threshold: true`) was the entire inferential
content.

**Fixed:** `analyze_continuity_v1.py` now implements the preregistered
analysis (paired sign-flip permutation test, scenario-level percentile
bootstrap, recorded seed and resample count) plus the preregistered validity
gate and INVALID_RUN rule. The preregistration did not fix a seed, a resample
count or a significance rule; those choices are recorded in the output and
labelled as additions made during this verification.

### D3 (major) — Two of the five rubric components are unreachable for this model

Per-component award counts over all 216 trials:

| Component | correct | decoy | no_memory |
|---|---:|---:|---:|
| 1 `decision` | **0** | **0** | **0** |
| 2 `commitment_id` | 43 | 16 | 0 |
| 3 `rationale_codes` (all required) | **0** | **0** | **0** |
| 3b `rationale_codes` (any required) | **0** | **0** | **0** |
| 4 exact source set (raw ids) | 4 | 0 | 0 |
| 5 target cited (raw ids) | 28 | 0 | 0 |
| 4 exact source set (normalised) | 37 | 0 | 0 |
| 5 target cited (normalised) | 68 | 0 | 0 |

gemma3:4b never once emits the benchmark's `decision` enum (`delay`,
`approve`, `revise`, …) — it answers in prose, e.g. "Revert deployment of
v2.3". It never once emits any of the benchmark's `rationale_codes` strings.
Those two components — the semantically meaningful ones — are dead for this
model, so **the 0-5 score is in practice a 0-3 instrument** and the result is
a *source-attribution and commitment-identification* effect, not a
decision-quality effect.

**This does not weaken the finding** (F4 shows the effect is real and
rubric-independent), but the published claim "0-5 continuity score" and the
per-category table overstate what was measured.

### D4 (major) — Two scoring defects in the as-run instrument

1. **Episode ids compared raw.** The benchmark prints episodes as
   `- [ep_target_001] …` and the model quotes them back in that form: 167 of
   341 citations were bracketed. Exact string comparison then never matched
   the answer key.
2. **Point 5 is a strict logical subset of point 4.** Point 4 requires the
   cited set to be exactly the target set; point 5 only requires the target to
   be a subset. In 24 trials point 5 was awardable where point 4 was not, so
   the two components are not independent checks.

**Declared amendment** (`src/ce1/continuity/scoring.py`, `score_corrected`):
episode ids are normalised, and point 5 becomes a real decoy-contamination
check (target cited **and** decoy not cited). The as-run scorer is preserved
verbatim so the published numbers stay reproducible; the corrected analysis
is reported **alongside** it, never instead of it.

Effect: primary difference 0.819 → 1.833; both instruments give SUPPORTED.

### D5 (major) — The validity gate was not implemented in the as-run path

`score_continuity_v1.py` scored an unparseable response as **0**:
`s = score_response(resp, ak) if resp else 0`. The preregistration says
invalid trials are "INVALID (not scored as zero)". The analysis had no
INVALID_RUN rule either.

This does not bite in the recorded run (0 invalid trials), so no published
number changes — but the instrument did not implement the protection that the
preregistration claimed, which is the same class of defect that voided
Experiments 1.1 and 1.2.

**Fixed:** `classify_validity()` implements the gate; the corrected scorer
returns `None` for invalid trials and the analyzer excludes them, raising
INVALID_RUN above 5% invalid or below the required number of paired
observations.

### D6 (major) — A published limitation is false

`reports/confirmatory_results_h8.md` limitation 3 reads: *"Scoring uses fuzzy
matching; exact-match would yield lower scores."*

The scoring is **exact match** — case-sensitive string equality on `decision`
and `commitment_id`, exact set containment on `rationale_codes`. There is no
fuzzy matching anywhere in the continuity_v1 scorer (the *qualification*
suite does normalise answers, but that is a different instrument on a
different suite). The statement is false, and it points the wrong way: exact
matching is what makes the instrument brittle (D3), and a genuinely fuzzy
scorer would *raise* the no-memory and decoy scores, not lower them.

### D7 (major) — The H1–H7 hypothesis register was deleted

Commit `dd5f188` ("feat: record H8 confirmatory result") replaced
`hypotheses/HYPOTHESIS_REGISTER.md` with an H8-only document: 202 lines
deleted, 30 added. The operational definitions, falsification criteria and
"what this cannot establish" clauses for H1–H7 — Stage 0 roadmap deliverable
7 — were removed from the repository by the commit that recorded the
programme's one positive result.

**Fixed:** restored from `835d4cb`, with only the *Current confidence* lines
restated against the evidence that now exists (H1 INCONCLUSIVE, H2
INCONCLUSIVE, H3–H6 UNTESTED, H7 OUT OF REACH).

### D8 (minor) — An audit cites a string that was not there

`reports/claim_audit_post_publication.md` lists
`hypotheses/HYPOTHESIS_REGISTER.md` line 30 as containing
"H1 supported: INCONCLUSIVE". The register at that commit did not contain
that string; it said "Current confidence: Unknown (no experiments run)". The
claim-audit conclusion (no misleading active claims) still holds; the citation
does not.

### D9 (minor) — The `no_memory` condition is not memory-free, and part of the answer key is inferable from the task

- The `no_memory` prompt still contains 1–2 distractor episodes (**120 in
  total across the 72 scenarios**) and still carries the `PRIOR EPISODES:`
  header, so every arm of the design presents an episode block. The arm
  measures *no answer-bearing memory*, not *no memory*, and it cannot measure
  abstention: the model keeps answering confidently.
- 63 of 144 required rationale codes share at least one content word with the
  task text (24/24 in `justified_revision`, 18/18 in `rationale_reconstruction`).
  No code is fully recoverable from the task, but part of the key is
  guessable without any episode.

The measured 0.000 floor is therefore a property of *this model's behaviour*,
not a property of the task. A stronger model could score in the no-memory
condition, and the floor would not be zero. This does not bias the primary
contrast, because the correct and decoy arms carry the same distractors.

### D10 (minor) — "Matched decoy" is a *contradicting* decoy, and the shared `commitment_id` caps that arm

Two distinct issues with the control arm:

1. **The decoy is not merely wrong, it contradicts the key.** In 3 of the 5
   categories a model reasoning correctly *from the decoy* produces the
   opposite answer: `constraint_persistence` (512 MB vs 256 MB → approve vs
   reject), `source_attribution` (1000 vs 998 rows) and, partially,
   `commitment_preservation` (a different rule). The recorded decoy arm
   behaves exactly that way — the model answers "Implement rate limiting at
   500 req/min" and "998". Those are right answers to the question as the
   decoy poses it, and they score 0.
   A contradicting decoy is a *stronger* test of content-specificity than an
   irrelevant one, but the name "matched decoy" implies equivalence and the
   design delivers contradiction. The report must say so.
2. **The target and decoy episodes carry the same `commitment_id`** in every
   category ("Commitment C-1" in both). The decoy condition therefore has a
   ceiling of one point, and 16/72 decoy trials took exactly that point. The
   design is not wrong — it is a deliberate token match — but it means the
   maximum achievable difference is 4.0, not 5.0, and part of the measured
   gap is a guaranteed giveaway rather than a behavioural achievement.

---

## 3. Independent corroboration

A second, independently written adversarial audit of the same instrument was
present in the working tree during this verification
(`experiments/continuity_v1/audit_h8_instrument.py`, written by a concurrent
session, not by this work). It reached the same conclusions by a different
route:

| This verification | Independent audit |
|---|---|
| D3: two rubric components never fire | A1: criterion firing counts |
| D4: rubric point 5 duplicates point 4 | A3: criterion independence |
| D5: invalid trials scored as zero | A4: invalid-trial handling |
| D9/D10: `no_memory` retains episodes; decoy shares the commitment id | A5: condition integrity (120 distractor episodes in the no-memory arm) |
| D2: preregistered statistics absent | A6: prereg conformance — permutation test, bootstrap CI, seed and resample count all absent |

The independent audit additionally computed the primary difference under three
readings of the published rubric: published 0.819, strict 1.208, lenient
1.542. **All three clear the 0.50 threshold**, which is a further
sensitivity result: the conclusion does not depend on how the ambiguous
rubric is read. Its recomputation of the published primary difference from
the raw responses returns 0.8194444444444445 — bit-identical to the
committed `confirmatory_analysis.json` value, so the two passes agree
numerically as well as in conclusion.

Two of its characterisations are sharper than this report's and have been
adopted: the `no_memory` arm carries the `PRIOR EPISODES:` header and 120
distractor episodes, so it cannot measure abstention (D9); and the decoy arm
is a **contradicting** control, not a matched one — in three of five
categories a model reasoning correctly from the decoy produces the opposite
answer, which is a stronger test of content-specificity but must be
described accurately (D10).

---

## 4. What the result does and does not support

Supported, on the evidence above:

- Correctly retrieved episodic content changes what the model says, and it
  changes it in the direction of the retrieved episode (71/72 scenarios;
  rubric-independent discrimination +0.152 correct vs −0.215 decoy).
- The effect is not an artefact of prompt length (0.92% length difference), of
  prompt reuse (0 hash mismatches), of invalid trials (0), or of the rubric
  (a rubric-independent metric agrees).
- The effect survives the instrument correction and gains statistical
  support it did not previously have (p < 1.0e-4, CI [0.667, 0.972]).

Not supported, and not claimed:

- Anything about consciousness, subjective experience, reliving, autonoetic
  awareness, moral patienthood, or metaphysical continuous existence.
- Decision quality: the rubric's decision component never fired, so this
  benchmark says nothing about whether the model made a *better decision*.
- Generalisation beyond gemma3:4b, beyond this benchmark, or beyond
  single-episode retrieval in a prompt.
- That "continuity" is involved at all in the measured sense. The benchmark
  manipulates **which episode is in the prompt**; it does not interrupt a
  session, destroy a context, or compare against a reconstructed state. The
  correct name for what was measured is **episodic-content sensitivity under
  prompt delivery**, and H8 should be read that narrowly.

---

## 5. Actions taken

| # | Action | Artifact |
|---|---|---|
| 1 | Live runner committed, reproduces the recorded scenario order | `experiments/continuity_v1/run_continuity_v1.py` |
| 2 | Preregistered analysis implemented (permutation, bootstrap, seed, resample count, validity gate, INVALID_RUN) | `experiments/continuity_v1/analyze_continuity_v1.py`, `src/ce1/continuity/analysis.py` |
| 3 | As-run instrument preserved verbatim; corrected instrument added as a declared amendment | `src/ce1/continuity/scoring.py` |
| 4 | Scorer CLI extended with `--scoring {as_run,corrected}` | `experiments/continuity_v1/score_continuity_v1.py` |
| 5 | Adversarial verification harness (8 probes, deterministic, no model calls) | `experiments/continuity_v1/adversarial_verify_h8.py` |
| 6 | 25 new tests, including a byte-for-byte reproduction test of the committed scores | `tests/test_continuity_analysis.py` |
| 7 | H1–H7 register restored | `hypotheses/HYPOTHESIS_REGISTER.md` |
| 8 | Published limitations corrected | `reports/confirmatory_results_h8.md` |
| 9 | Status document updated | `docs/STAGE_0_STATUS.md` |
| 10 | Whole confirmatory run repeated with the committed runner | `experiments/continuity_v1/results/replication_gemma3_4b_*.jsonl` |
| 11 | Second-model replication preregistered before the run | `experiments/continuity_v1/preregistration_h8_replication.md` |

## 6. Environment note (2026-10-21)

The local Ollama server on this host stopped serving generations partway
through the work: it accepted requests and never completed them, and after a
restart it hung in `discovering available GPUs...` on the GTX 1080
(CUDA/Vulkan device discovery). The server runs correctly with
`OLLAMA_LLM_LIBRARY=cpu`, `OLLAMA_NUM_GPU=0`, `OLLAMA_VULKAN=false` and
`OLLAMA_CONTEXT_LENGTH=131072`; the context length matches the configuration
used for the recorded 2026-10-20 run. Two models (qwen3:4b, dolphin-llama3)
could not be qualified while the server was wedged; their qualification was
re-attempted after the recovery.

Recorded because it affects what could be measured: the box's GPU path is
currently unusable for Ollama inference, and the recorded 2026-10-20 run was
produced with the GPU-enabled server.

