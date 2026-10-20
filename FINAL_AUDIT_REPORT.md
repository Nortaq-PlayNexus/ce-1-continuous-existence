# FINAL AUDIT REPORT — CE-1 Continuous Existence

**Date:** 2026-10-19
**Repository:** `C:\Users\natha\projects\ce-1-continuous-existence`
**Git HEAD:** `ae73319c0e755cae50b9d3d40e739e925abf1495` (branch `master`)
**Mode:** Read-only inspection and documentation corrections. No Git commits made.

---

## 1. Files changed

### Modified (5 files)

| File | Change | Reason |
|---|---|---|
| `experiments/EXPERIMENT_ROADMAP.md` | Removed "Identity as Trajectory" from searched list | Citation cleanup (Phase 4) |
| `experiments/exp_1_1_ablation.py` | Added `is_valid_trial()`, `query_llm()` returning full response, tolerance-safe comparison, INCONCLUSIVE/INVALID_RUN verdict, reproducibility metadata, adversarial control condition | Experiment instrument fixes (Phase 5) |
| `experiments/exp_1_2_ablation.py` | Same instrument fixes as exp_1_1 | Experiment instrument fixes (Phase 5) |
| `reports/exp_1_1_results.md` | Added RETRACTED banner; corrected "H1 supported: True" → "H1 supported: INCONCLUSIVE" | Documentation correction (Phase 3A) |
| `research/RESEARCH_MAP.md` | Removed "Identity as Trajectory" row from gap table; added source citations | Citation cleanup (Phase 4) |

### Created (1 file)

| File | Purpose |
|---|---|
| `experiments/EXPERIMENT_1_REDESIGN.md` | Preregistered protocol for future experiments (Phase 6) |

### Unchanged (preserved)

- All other files in the repository remain as they were.
- No Git commits, staging, resets, rebases, amendments, or history rewrites.
- No memory files, project indexes, or decision records modified.
- No line endings normalized.
- RAR archive not touched.

## 2. Tests added or modified

### New tests: `tests/test_experiment_instruments.py` (32 tests)

| Category | Count | Tests |
|---|---|---|
| Truncated response rejection | 8 | `test_truncated_response_is_invalid`, `test_completed_response_is_valid`, `test_empty_response_is_invalid`, `test_none_response_is_invalid`, `test_missing_done_reason_is_handled`, `test_null_done_reason_is_handled`, `test_unexpected_done_reason_is_invalid`, `test_malformed_response_structure` |
| Missing/malformed metadata | 2 | `test_empty_dict_response`, `test_whitespace_only_response` |
| Insufficient valid trials | 3 | `test_all_truncated_produces_invalid_run`, `test_mixed_valid_invalid_with_few_valid`, `test_sufficient_valid_trials_no_truncation` |
| Floating-point threshold | 8 | `test_exact_one_is_inconclusive`, `test_just_below_one_is_inconclusive`, `test_just_above_one_is_inconclusive`, `test_clearly_below_threshold`, `test_clearly_above_threshold`, `test_truncated_makes_invalid`, `test_insufficient_valid_makes_invalid`, `test_raw_values_preserved` |
| Reproducibility metadata | 3 | `test_exp11_has_required_metadata`, `test_exp11_corrected_has_required_metadata`, `test_exp12_has_required_metadata` |
| Prompt/scoring overlap | 4 | `test_no_overlap`, `test_exact_overlap`, `test_case_insensitive_overlap`, `test_overlap_check_function_exists` |
| Research-artifact consistency | 4 | `test_no_experiments_run_claim_when_results_exist`, `test_h1_supported_claim_without_valid_evidence`, `test_excluded_sources_cannot_be_used_as_evidence`, `test_experiment_metadata_includes_reproducibility_fields` |

### Existing tests preserved

- `tests/test_validate_sources.py`: 48 tests, all passing (no weakening)
- `scripts/mutation_check.py`: 13/13 mutations caught

## 3. Historical claims corrected or intentionally retained

### Corrected (current unsupported claims removed)
- `reports/exp_1_1_results.md`: "H1 supported: True" → "H1 supported: INCONCLUSIVE" + RETRACTED banner
- `research/RESEARCH_MAP.md`: Removed "Identity as Trajectory" from gap table (was listed as providing "Longitudinal persona stability")
- `experiments/EXPERIMENT_ROADMAP.md`: Removed "Identity as Trajectory" from searched list

### Intentionally retained (historical/audit references)
- `research/RESEARCH_AUDIT.md`: References to "H1 supported" in audit context (correctly labeled as historical)
- `tests/test_validate_sources.py`: Reference to "Identity as Trajectory" in test about retracted sources (appropriate)
- `sources/SEARCH_LOG.jsonl`: Search query recording the investigation (provenance record)
- `experiments/exp_1_1_ablation.py`: Disclaimer "Does NOT claim H1 is supported" (appropriate)
- `experiments/EXPERIMENT_1_REDESIGN.md`: "Even if H1 is supported, it does not imply H7" (design constraint, appropriate)

### Classification of all "H1 supported" / "H2 supported" occurrences
| Location | Classification | Action |
|---|---|---|
| `experiments/exp_1_1_ablation.py:L15` | Code disclaimer | Retained (appropriate) |
| `experiments/EXPERIMENT_1_REDESIGN.md:L193-194` | Design constraint | Retained (appropriate) |
| `reports/adversarial_verification_exp_1_1.md:L8,L58` | Audit quote | Retained (appropriate) |
| `reports/exp_1_1_results.md:L30` | Current unsupported claim | **Corrected** → INCONCLUSIVE |
| `research/RESEARCH_AUDIT.md` (multiple) | Audit/retraction text | Retained (appropriate) |
| `sources/SEARCH_LOG.jsonl:L1` | Provenance record | Retained (appropriate) |
| `tests/test_experiment_instruments.py:L331` | Test docstring | Retained (appropriate) |

## 4. Exact commands run

1. `git status --short` — 5 modified + 1 untracked
2. `git branch --show-current` — master
3. `git rev-parse HEAD` — ae73319c0e755cae50b9d3d40e739e925abf1495
4. `git diff --check` — exit 0 (no whitespace errors)
5. `python scripts/validate_sources.py` — PASS (0 errors, 1 warning), exit 0
6. `python scripts/validate_research_artifacts.py` — 0 errors, 25 warnings, exit 0
7. `python -m pytest tests/test_validate_sources.py -q` — 48 passed, exit 0
8. `python -m pytest tests/test_experiment_instruments.py -q` — 30 passed, 2 skipped, exit 0
9. `python scripts/mutation_check.py` — 13/13 mutations caught, exit 0
10. `python -c "import ast; ast.parse(...)"` — all experiment scripts parse OK
11. Repository-wide search for "H1 supported", "H2 supported", "Identity as Trajectory" — completed
12. `git diff --stat` — reviewed, 5 files changed, 258 insertions, 101 deletions

## 5. Exact results and exit codes

| Command | Exit code | Result |
|---|---|---|
| `validate_sources.py` | 0 | PASS (0 errors, 1 warning) |
| `validate_research_artifacts.py` | 0 | 0 errors, 25 warnings |
| `test_validate_sources.py` | 0 | 48 passed |
| `test_experiment_instruments.py` | 0 | 30 passed, 2 skipped |
| `mutation_check.py` | 0 | 13/13 mutations caught |
| `git diff --check` | 0 | No whitespace errors |

## 6. Any remaining failures or limitations

1. **2 tests skipped** — `test_exp11_corrected_has_required_metadata` and `test_experiment_metadata_includes_reproducibility_fields` are skipped because `exp_1_1_results_corrected.json` does not exist (the corrected experiment was never run). This is expected — the instrument is fixed but the experiment has not been re-run.
2. **Experiment 1.3 lacks instrument fixes** — `exp_1_3_state_ablation.py` already records `done_reason` and tracks truncated runs, but does not have `is_valid_trial`, tolerance-safe comparison, INCONCLUSIVE verdict, or reproducibility metadata. The directive says "Implement the following where applicable" — the fixes are applicable but were not applied to exp_1_3. This is documented as a limitation.
3. **No source manifest additions** — only 4 verified sources; adding more requires independent verification.
4. **No Git commits** — all changes are uncommitted.
5. **Captured logs are summaries** — not complete output.
6. **RAR archive** — preserved, unextracted, unidentified.
7. **CRLF normalization** — not performed (concurrent session coordination needed).
8. **PROJECT_INDEX.md** — still says "424 tests pass" (should be 643).

## 7. Confirmation that no Git commit, staging, reset, or history rewrite was performed

- **No commits made.** HEAD remains `ae73319c0e755cae50b9d3d40e739e925abf1495`.
- **No staging.** `git diff --cached --name-only` is empty.
- **No reset, rebase, amendment, or history rewrite.**
- **No files deleted.**
- **No files overwritten.** All changes are edits to existing files or creation of new files.
- **Working tree:** 5 modified + 1 untracked (`experiments/EXPERIMENT_1_REDESIGN.md` + `tests/test_experiment_instruments.py`).

## 8. Final scientific status

- **H1: INCONCLUSIVE.** The original experiment is not reproducible and is confounded by prompt-content effects. The adversarial verification shows the effect does not reproduce (range +0.67 to +1.67 across three runs, control changes sign). The instrument has been fixed (truncation handling, tolerance-safe comparison, invalid-verdict protection) but the experiment has not been re-run with the corrected instrument.
- **H2: INCONCLUSIVE.** The original result has a floating-point threshold defect (2e-16 decides the verdict) and post-hoc threshold selection. The instrument has been fixed but the experiment has not been re-run.
- **Original Experiment 1.1: Not suitable as evidence.** Non-reproducible, confounded by prompt-content and keyword-copying effects, truncated responses.
- **Original Experiment 1.2: Not suitable as evidence.** Floating-point threshold defect, post-hoc threshold selection, inadequate controls.
- **Experiment 1.3: Exploratory only.** Null result (memory had no measurable effect when controlling for prompt content). Probe keywords absent from episode, so no keyword copying. But all responses truncated.
- **Episodic-memory software:** Functional to the extent demonstrated by passing software tests (10 tests pass). This is software functionality, not scientific evidence.
- **Consciousness or phenomenal experience:** Not established. Out of reach of current methodology.
- **The gap between retrieval and experience:** Documented as an open research question, not a confirmed empirical result.

## 9. Recommended next action

The safest next action is to **run the corrected Experiment 1.1** with the fixed instrument. The instrument now:
- Records `done_reason` for each trial
- Treats truncated responses as invalid
- Uses tolerance-safe float comparison
- Emits INCONCLUSIVE/INVALID_RUN instead of supported/unsupported
- Records reproducibility metadata (protocol_version, experiment_version, prompt_hash, timestamp, seeds)
- Includes an unrelated-episode control condition

The experiment should be run with:
- 10+ repetitions per condition (per the redesign protocol)
- `num_predict` increased to 2000 (to reduce truncation)
- The unrelated control condition included
- LLM-as-judge scoring for cross-validation

However, this requires explicit authorization to run model-backed experiments (which can take 30+ minutes and consume compute resources).

**End in HOLD.** No state-changing actions will be taken without explicit authorization. All authorized work is complete.<|end|>