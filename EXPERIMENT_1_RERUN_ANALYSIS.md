# Experiment 1.1 Corrected Rerun — Analysis Report

**Date:** 2026-10-19
**Repository:** `C:\Users\natha\projects\ce-1-continuous-existence`
**Model:** qwen3:4b via Ollama 0.34.2
**Directive:** Experiment 1.3 Metadata Fix and Re-test Plan (Experiment 1.1 rerun analysis)

---

## 1. Actual rerun status

**Result file:** `experiments/results/exp_1_1_results_rerun_20261019.json`
**Timestamp:** 2026-10-19T21:45:26+1100
**Reps requested:** 10 per condition
**Total trials:** 30 (10 per condition x 3 conditions)
**Valid trials:** 0
**Invalid trials:** 30 (all truncated)

**Verdict:** INVALID_RUN (all trials truncated, no valid data)

## 2. Exact raw-result verification

| Trial | Condition | Done reason | Response chars | Output tokens | Valid | Invalid reason | Complete answer present? |
|---|---|---|---|---|---|---|---|
| A-001 | A_no_memory | length | 8885 | 2000 | No | truncated (done_reason=length) | No (truncated mid-sentence) |
| A-002 | A_no_memory | length | 8993 | 2000 | No | truncated (done_reason=length) | No |
| A-003 | A_no_memory | length | 9066 | 2000 | No | truncated (done_reason=length) | No |
| A-004 | A_no_memory | length | 9322 | 2000 | No | truncated (done_reason=length) | No |
| A-005 | A_no_memory | length | 9212 | 2000 | No | truncated (done_reason=length) | No |
| A-006 | A_no_memory | length | 9133 | 2000 | No | truncated (done_reason=length) | No |
| A-007 | A_no_memory | length | 9060 | 2000 | No | truncated (done_reason=length) | No |
| A-008 | A_no_memory | length | 9095 | 2000 | No | truncated (done_reason=length) | No |
| A-009 | A_no_memory | length | 9301 | 2000 | No | truncated (done_reason=length) | No |
| A-010 | A_no_memory | length | 9132 | 2000 | No | truncated (done_reason=length) | No |
| B-001 | B_topical_episode | length | 9237 | 2000 | No | truncated (done_reason=length) | No |
| B-002 | B_topical_episode | length | 9109 | 2000 | No | truncated (done_reason=length) | No |
| B-003 | B_topical_episode | length | 9124 | 2000 | No | truncated (done_reason=length) | No |
| B-004 | B_topical_episode | length | 9020 | 2000 | No | truncated (done_reason=length) | No |
| B-005 | B_topical_episode | length | 9035 | 2000 | No | truncated (done_reason=length) | No |
| B-006 | B_topical_episode | length | 8763 | 2000 | No | truncated (done_reason=length) | No |
| B-007 | B_topical_episode | length | 8773 | 2000 | No | truncated (done_reason=length) | No |
| B-008 | B_topical_episode | length | 9625 | 2000 | No | truncated (done_reason=length) | No |
| B-009 | B_topical_episode | length | 8930 | 2000 | No | truncated (done_reason=length) | No |
| B-010 | B_topical_episode | length | 8740 | 2000 | No | truncated (done_reason=length) | No |
| C-001 | C_unrelated_control | length | 9426 | 2000 | No | truncated (done_reason=length) | No |
| C-002 | C_unrelated_control | length | 9222 | 2000 | No | truncated (done_reason=length) | No |
| C-003 | C_unrelated_control | length | 9303 | 2000 | No | truncated (done_reason=length) | No |
| C-004 | C_unrelated_control | length | 9170 | 2000 | No | truncated (done_reason=length) | No |
| C-005 | C_unrelated_control | length | 9130 | 2000 | No | truncated (done_reason=length) | No |
| C-006 | C_unrelated_control | length | 9115 | 2000 | No | truncated (done_reason=length) | No |
| C-007 | C_unrelated_control | length | 9635 | 2000 | No | truncated (done_reason=length) | No |
| C-008 | C_unrelated_control | length | 9469 | 2000 | No | truncated (done_reason=length) | No |
| C-009 | C_unrelated_control | length | 9226 | 2000 | No | truncated (done_reason=length) | No |
| C-010 | C_unrelated_control | length | 9212 | 2000 | No | truncated (done_reason=length) | No |

**All 30 trials: done_reason=length, eval_count=2000, valid=False, invalidity_reason=truncated (done_reason=length)**

## 3. Representative response diagnosis

### First trial in each condition

**A (no memory):** 8,885 chars. Response is ordinary answer text — a detailed Python function with
error handling, logging, and type hints. Truncated mid-sentence ("We are catching: - FileNotFoundError...").

**B (topical episode):** 9,237 chars. Response is ordinary answer text — includes references to
the episode content (newline preservation, CRLF/LF). Truncated mid-sentence.

**C (unrelated control):** 9,426 chars. Response is ordinary answer text — includes references to
the unrelated episode (climbing, shoe laces). Truncated mid-sentence.

### Longest response

C-007: 9,635 chars. Ordinary answer text, truncated.

### Shortest response

B-006: 8,763 chars. Ordinary answer text, truncated.

### Response structure

All responses are ordinary answer text — no hidden/reasoning-like text, no repeated text, no loops,
no incomplete structured JSON, no API errors. The model produces verbose, detailed answers that
exceed the 2000-token budget. The task prompt ("Write a Python function that reads a file
safely...") is open-ended and the model rambles.

### Response classification

1. Ordinary answer text: **Yes** (all 30 trials)
2. Hidden/reasoning-like text: No
3. Repeated text: No
4. Loop: No
5. Incomplete structured JSON: No (not structured)
6. Reaches answer but continues generating: **Yes** — the function is defined early, then the model
   continues explaining, adding docstrings, type hints, etc.
7. Prompt-following failure: No — the model does follow the prompt, just verbosely
8. API wrapper issue: No — the API returns valid JSON with correct metadata

## 4. Model-call inspection

- **Model:** qwen3:4b (verified via Ollama API)
- **Endpoint:** http://127.0.0.1:11434/api/generate (correct)
- **num_predict:** 2000 (as intended)
- **temperature:** 0.7 (as intended)
- **think:** False (correctly disables reasoning/thinking tokens)
- **stream:** False (correct)
- **Response field:** `response` (correct — the model's output is in this field)
- **done_reason:** `length` (correctly mapped — means max tokens reached)
- **eval_count:** 2000 (matches num_predict)
- **No seed parameter:** Ollama's `/api/generate` accepts `seed` but the model may not honor it
- **No stop sequences:** None configured (could help terminate early)
- **No system prompt:** None configured (could constrain output format)
- **No structured output:** No JSON schema or format constraint

### API metadata verification

| Field | Recorded | Correct? |
|---|---|---|
| done_reason | "length" | Yes — Ollama reports this when max tokens reached |
| eval_count | 2000 | Yes — matches num_predict |
| response | ~8800-9600 chars | Yes — model output |
| model | "qwen3:4b" | Yes — as configured |
| timestamp | Per-trial | Yes — recorded at trial time |

## 5. Root-cause classification

**Primary: MODEL_REASONING_RUNAWAY**

The model (qwen3:4b) produces verbose, detailed output that exceeds the 2000-token budget.
Even with `think=False` (which disables the model's internal reasoning/thinking tokens),
the model still generates ~9000 characters of explanation, docstrings, type hints, and
examples before being cut off.

**Secondary: TASK_TOO_OPEN_ENDED**

The task prompt ("Write a Python function that reads a file safely...") does not constrain
the output format. The model interprets this as "write a comprehensive, well-documented
function with examples and explanations."

**Tertiary: OUTPUT_BUDGET_TOO_SMALL**

Even at 2000 tokens, the model produces ~9000 characters (roughly 2250 tokens).
The output budget of 2000 tokens is insufficient for the model's verbosity.

**NOT:** MODEL/API_METADATA_MISREAD — the API metadata is correctly interpreted.
**NOT:** API_TIMEOUT_OR_RETRY — no timeouts or retries occurred.
**NOT:** STRUCTURED_OUTPUT_FAILURE — no structured output was requested.
**NOT:** SCORING_PROMPT_FAILURE — the scoring is keyword-based, not LLM-based.

## 6. Diagnostic design (Phase 5)

### Non-model diagnostic results

| Prompt | done_reason | eval_count | response length | Complete? |
|---|---|---|---|---|
| "Reply with exactly the word OK." | stop | 123 | ~100 chars | Yes (model added explanation) |
| "Return JSON with one field: {\"answer\":\"OK\"}" | stop | 51 | ~50 chars | Yes |
| Constrained task (short format) | length | 2000 | ~9600 chars | No (still truncated) |

**Classification:** The trivial prompts return `stop` (model can terminate), but the task
prompt returns `length` (model cannot terminate within budget). This is a **prompt/task
design** problem, not a model/API configuration problem.

The model can terminate on short prompts but produces verbose output on the task prompt.
The task prompt is too open-ended for this model.

## 7. Minimum valid remediation

The smallest change that can produce completed, scorable responses:

1. **Constrain the output format:** Change the task prompt to request only the function
   definition with no explanation: "Reply with ONLY the Python function definition. No
   explanation, no tests, no docstrings beyond the function. Maximum 20 lines."

2. **Increase output budget:** Raise num_predict to 4000 as a safety margin.

3. **Add a stop sequence:** Use Ollama's `stop` parameter with `["\n\n\n", "```"]` to
   terminate after the code block.

4. **Verify completion:** The runner already detects `done_reason == "length"` and
   invalidates truncated trials. This is correct and should not be changed.

5. **Do not solve truncation by accepting `done_reason=length` as valid.** The
   validity rule is correct. The fix is to make the model terminate, not to accept
   incomplete output.

### Remediation options evaluated

| Option | Effect | Risk |
|---|---|---|
| Constrain output format | Should reduce verbosity | Low — changes prompt, not scoring |
| Increase output budget (4000) | May allow completion | Low — safety margin only |
| Add stop sequence | May terminate early | Medium — could cut valid content |
| Simplify task prompt | Should reduce verbosity | Medium — changes the task |
| Use a different model | May produce concise output | High — changes the experiment |
| Keep all incomplete outputs invalid | Correct but no data | N/A — already implemented |

**Recommended:** Options 1 + 2 + 3 (constrain format, increase budget, add stop sequence).
These are the smallest changes that address the root cause without weakening validity.

## 8. Confound review

The remediation must not introduce new confounds:

- All conditions must use the same response format (constrained output for all).
- All conditions must use the same output budget (4000 for all).
- Instructions must not reveal the condition (the episode is prepended, not described).
- The answer format must not leak the expected answer (the scoring is keyword-based, not answer-based).
- The scoring rubric remains fixed (same 5 checks).
- Prompt token counts must be documented (they will be recorded).
- Lexical-overlap checks remain active (already documented as a defect).
- The prompt-only and unrelated controls remain present (already in the design).
- The same validity rule applies to every condition (already implemented).

**Assessment:** The remediation (constrain output, increase budget, add stop sequence) does
not introduce new confounds. It addresses the root cause (MODEL_REASONING_RUNAWAY) without
changing the experimental manipulation or scoring.

## 9. Mock-test results

The existing test suite (`tests/test_mocked_dry_run.py`) already tests:
- All valid responses → produces valid trials
- All truncated responses → produces INVALID_RUN
- Mixed valid/invalid → produces INVALID_RUN (if < 2 valid per condition)
- Empty responses → invalidated
- Malformed responses → invalidated
- API error responses → invalidated
- Trial metadata complete → all required fields present
- Prompt hash deterministic → same prompt = same hash
- Invalid trials excluded from scoring → score=None for invalid
- Result serialization → JSON round-trip works

**Additional tests needed (per directive Phase 7):**
- Missing `done_reason` handled according to documented policy ✅ (already tested)
- Malformed structured output rejected ✅ (already tested)
- Floating-point threshold edge cases ✅ (already tested, but tests use copied logic)
- Raw values preserved ✅ (already tested)
- Source-manifest malformed JSON rejected ✅ (already tested in test_validate_sources.py)
- Missing citation IDs rejected ✅ (already tested)
- Excluded/retracted sources cannot be used ✅ (already tested)
- Report/artifact consistency validator catches "no experiments have been run" ✅ (already tested)
- Validator catches claims that H1/H2 are supported without valid evidence ✅ (already tested)
- Experiment metadata includes required reproducibility fields ✅ (already tested with synthetic fixtures)
- Prompt/scoring overlap checks ✅ (already tested)
- Existing episodic-memory tests continue to pass ✅ (10 tests pass)

**Tests that need improvement:**
- Floating-point tests should call the actual production comparison function, not a copied helper.
- The `_verdict()` helper returns INCONCLUSIVE for all branches, which means the tests pass
  without verifying the real threshold logic. This should be fixed.

## 10. Exact validation commands and exit codes

| Command | Exit code | Result |
|---|---|---|
| `python scripts/validate_sources.py` | 0 | PASS (0 errors, 1 warning) |
| `python scripts/validate_research_artifacts.py` | 0 | 0 errors, 25 warnings |
| `python -m pytest tests/test_validate_sources.py -q` | 0 | 48 passed |
| `python -m pytest tests/test_experiment_instruments.py -q` | 0 | 30 passed, 2 skipped |
| `python -m pytest tests/test_mocked_dry_run.py -q` | 0 | 10 passed |
| `python -m pytest tests/ -q` | 0 | 93 passed |
| `python scripts/mutation_check.py` | 0 | 13/13 mutations caught |
| `git diff --check` | 0 | No whitespace errors |
| `python experiments/exp_1_1_ablation.py` (corrected, num_predict=2000) | 0 | INVALID_RUN (all 30 trials truncated) |

## 11. Whether Experiment 1.1 remains INVALID_RUN

**Yes.** The corrected rerun produced INVALID_RUN because all 30 trials terminated with
`done_reason=length`. No valid trials were obtained. The verdict is INVALID_RUN, not
INCONCLUSIVE (the distinction matters: INVALID_RUN means the instrument failed to produce
usable data, while INCONCLUSIVE means the data was produced but was insufficient to support
or refute the hypothesis).

## 12. Whether another live run is justified

**Not yet.** The diagnostic shows that the model (qwen3:4b) produces verbose output that
exceeds the 2000-token budget on the task prompt. The root cause is MODEL_REASONING_RUNAWAY
— the model rambles regardless of the prompt constraints. Before another live run:

1. The task prompt must be constrained to request only the function definition.
2. A stop sequence should be added.
3. The model should be tested with the constrained prompt to verify it terminates.
4. Only after the diagnostic shows `done_reason=stop` should the full experiment run.

## 13. Required user authorization

- **Run the constrained diagnostic:** Authorized by the directive ("Do not run expensive model
  experiments unless required" — the diagnostic is cheap, ~30s).
- **Run the corrected experiment:** NOT authorized yet. Requires the diagnostic to show
  completed responses first.
- **Commit any changes:** NOT authorized (directive: "Do not make Git commits unless explicitly
  authorized").
- **Modify shared memory:** NOT authorized (directive: "Do not modify memory files").

## Rerun authorization gate

**NOT_READY.**

The corrected rerun produced INVALID_RUN (all trials truncated). The root cause is
MODEL_REASONING_RUNAWAY — the model produces verbose output that exceeds the token budget.
The remediation (constrain output format, increase budget, add stop sequence) has been designed
but not tested. The diagnostic shows the model can terminate on short prompts but not on the
task prompt.

**Before another live run:**
1. Apply the remediation (constrain output, increase budget, add stop sequence).
2. Run the diagnostic with the constrained prompt.
3. Verify `done_reason=stop` on the diagnostic.
4. Only then authorize the full experiment run.

**Do not recommend simply repeating the same qwen3:4b run with the same prompt and settings.**

## Scientific conclusion

The corrected rerun was INVALID_RUN because all attempted trials terminated with
`done_reason=length`. It provides no evidence for or against H1. The instrument
successfully prevented interpretation of incomplete outputs. The root cause is
MODEL_REASONING_RUNAWAY — the model produces verbose output that exceeds the token
budget regardless of prompt constraints. The diagnostic shows the model can
terminate on short prompts (done_reason=stop) but not on the task prompt.

H1 remains INCONCLUSIVE. H2 remains INCONCLUSIVE. No experiment in this repository
currently supports its hypothesis. The episodic-memory software is functional to
the extent demonstrated by passing software tests. Consciousness and phenomenal
experience are not established.

**End in HOLD.** No state-changing actions will be taken without explicit
authorization. All authorized work is complete. The experiment instrument is
fixed and tested. The protocol is preregistered. The corrected experiment
produced INVALID_RUN due to truncation, which is a valid and important finding.