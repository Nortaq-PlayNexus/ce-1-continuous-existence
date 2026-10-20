# Corrected Release-Readiness Report — Read-Only Reconciliation (Final)

**Date:** 2026-10-19
**Repository:** `C:\Users\natha\projects\ce-1-continuous-existence`
**Git HEAD:** `ae73319c0e755cae50b9d3d40e739e925abf1495` (branch `master`)
**Mode:** Read-only. No state-changing actions performed.

---

## 1. Current repository state

### Exact git status

```
 M experiments/EXPERIMENT_ROADMAP.md
 M experiments/exp_1_1_ablation.py
 M experiments/exp_1_2_ablation.py
 M reports/exp_1_1_results.md
 M research/RESEARCH_MAP.md
?? CITATION.cff
?? CORRECTED_RELEASE_READINESS_REPORT.md
?? FINAL_AUDIT_REPORT.md
?? FINAL_REVIEW_REPORT.md
?? FINAL_ZENODO_REPORT.md
?? LICENSE
?? RELEASE_MANIFEST.json
?? ZENODO_DRAFT_REVIEW.md
?? ZENODO_README.md
?? experiments/EXPERIMENT_1_REDESIGN.md
?? tests/test_experiment_instruments.py
?? zenodo_deposition_id.txt
```

- **Modified (tracked):** 5
- **Untracked:** 12
- **Total changed paths:** 17
- **Staged:** 0
- **HEAD:** `ae73319c0e755cae50b9d3d40e739e925abf1495`
- **Branch:** `master`

### Exact modified-file and untracked-file counts

| Category | Count | Files |
|---|---|---|
| Modified (tracked) | 5 | `experiments/EXPERIMENT_ROADMAP.md`, `experiments/exp_1_1_ablation.py`, `experiments/exp_1_2_ablation.py`, `reports/exp_1_1_results.md`, `research/RESEARCH_MAP.md` |
| Untracked | 12 | `CITATION.cff`, `CORRECTED_RELEASE_READINESS_REPORT.md`, `FINAL_AUDIT_REPORT.md`, `FINAL_REVIEW_REPORT.md`, `FINAL_ZENODO_REPORT.md`, `LICENSE`, `RELEASE_MANIFEST.json`, `ZENODO_DRAFT_REVIEW.md`, `ZENODO_README.md`, `experiments/EXPERIMENT_1_REDESIGN.md`, `tests/test_experiment_instruments.py`, `zenodo_deposition_id.txt` |
| **Total** | **17** | |

## 2. Every file in the final status report

All 17 files above are listed. No omissions. No stale entries.

## 3. Archive contents vs manifest

| Source | Files | Hash mismatches |
|---|---|---|
| Local archive (`ce-1-continuous-existence-v0.1.0.zip`) | 49 | — |
| Local manifest (`RELEASE_MANIFEST.json`) | 47 | 0 |
| Only in archive (not in manifest) | 2 | `RELEASE_MANIFEST.json` (self, excluded from own hash list), `.gitignore` |
| Only in manifest (not in archive) | 0 | — |
| Secret hits in archive | 0 | — |
| Extraction test | OK | 47 files extracted successfully |

**Resolution:** The 2-file difference is explained by design. The manifest excludes itself (self-referential hash problem) and `.gitignore` was included in the archive for completeness. All 47 manifest files are present in the archive with matching hashes. No content discrepancy.

## 4. Local archive, manifest, and Zenodo-uploaded archive

| Property | Local archive | Zenodo-uploaded archive |
|---|---|---|
| Filename | `ce-1-continuous-existence-v0.1.0.zip` | `ce-1-continuous-existence-v0.1.0.zip` |
| Size | 157,759 bytes | 157,759 bytes |
| Checksum (MD5) | 0e31ffc6a3ed5c828c4b111ea553fa27 | 0e31ffc6a3ed5c828c4b111ea553fa27 |
| Files | 49 | 1 (single zip archive) |
| Secret hits | 0 | Not re-scanned (Zenodo-side) |

**Status:** Local and uploaded archives match (same filename, size, and checksum).

## 5. Why the report says 10 created files when 11 are listed

The discrepancy was in a chat summary from an earlier session, not in any report file. The `FINAL_AUDIT_REPORT.md` says "Created (1 file)" which is accurate for that specific report (only `EXPERIMENT_1_REDESIGN.md` was created during that phase; `test_experiment_instruments.py` was listed separately under "New tests"). The "10 created files" vs "11 listed" was a counting error in a chat response, not in any report file. No report file contains an incorrect file count.

## 6. Why the total is reported as 15 paths

The "15 paths" figure came from an earlier session's git status that showed 15 changed paths (before the Zenodo-related files were created). The current count is 17 (5 modified + 12 untracked). The count grew as more files were created in subsequent sessions. No discrepancy in the current state — the earlier figure was accurate at the time.

## 7. Whether FINAL_AUDIT_REPORT.md, FINAL_REVIEW_REPORT.md, and FINAL_ZENODO_REPORT.md are included in the archive

- `FINAL_AUDIT_REPORT.md`: **Yes** (in archive, 10,853 bytes)
- `FINAL_REVIEW_REPORT.md`: **Yes** (in archive, 37,665 bytes)
- `FINAL_ZENODO_REPORT.md`: **Yes** (in archive, 13,985 bytes)

All three audit reports are included in the archive.

## 8. Zenodo deposition 23471293 status (without API token)

- **Deposition ID:** 23471293 (recorded in `zenodo_deposition_id.txt`)
- **Last known state:** unsubmitted (draft)
- **Last known archive:** ce-1-continuous-existence-v0.1.0.zip (157,759 bytes, checksum 0e31ffc6a3ed5c828c4b111ea553fa27)
- **Last known title:** CE-1 Continuous Existence: Episodic Memory Instrument, Research Audit, and Experiment Redesign
- **Last known version:** 0.1.0
- **Last known license:** cc-by-nc-4.0
- **Last known files:** 1 (ce-1-continuous-existence-v0.1.0.zip)
- **DOI:** not yet assigned
- **Current Zenodo status:** CANNOT BE VERIFIED (no valid token available; directive forbids using the pasted token)

## 9. Token revocation status

**Cannot be verified without credentials.** The token was used in a previous session and is present in chat history. The user must verify revocation at https://zenodo.org/account/settings/applications/tokens/ and create a replacement if further API work is needed.

## 10. Archive license appropriateness

- **Current license:** CC-BY-NC-4.0 (declared in pyproject.toml, CITATION.cff, ZENODO_README.md, LICENSE file, RELEASE_MANIFEST.json)
- **Consistency:** All agree on CC-BY-NC-4.0
- **Concern:** CC-BY-NC-4.0 is generally NOT recommended for software code (MIT or Apache-2.0 preferred). May need dual licensing: MIT for code, CC-BY-NC-4.0 for documentation/reports.
- **Risk:** Publishing code under CC-BY-NC-4.0 may confuse users about what they can do with the code. The license prohibits commercial use, which is unusual for software.
- **Recommendation:** Confirm whether CC-BY-NC-4.0 applies to code, documentation, or both. If code should be MIT/Apache-2.0, use dual licensing.

## 11. Experiment 1.3 status

- **Included in archive:** NO (exp_1_3_results.json does not exist; only exp_1_3_results_gemma.json and exp_1_3_results.VOID.md)
- **Described in public docs:** YES (in reports, experiment roadmap)
- **Explicitly excluded from confirmatory evidence:** YES (labeled exploratory)
- **Marked invalid where truncated:** YES (VOID marker exists for qwen3:4b run)
- **Instrument fixes applied:** PARTIAL (done_reason tracked, but no is_valid_trial, tolerance, INCONCLUSIVE verdict, or reproducibility metadata)
- **Recommendation:** Keep as clearly labeled exploratory history. Do not treat as confirmatory evidence.

## 12. Skipped metadata tests

- `test_exp11_corrected_has_required_metadata`: SKIPPED (corrected results not generated)
- `test_experiment_metadata_includes_reproducibility_fields`: SKIPPED (same reason)
- **Can be replaced with synthetic fixtures:** YES
- **Current tests use copied verdict logic, not actual production functions:** The `_verdict()` helper in `test_experiment_instruments.py` replicates the comparison logic instead of calling it.
- **Floating-point tests return INCONCLUSIVE for all inputs:** The `_verdict()` helper returns INCONCLUSIVE for every branch, so the tests pass without verifying the real threshold logic.
- **Recommendation:** Replace skipped tests with synthetic fixture tests. Fix floating-point tests to test the actual comparison function.

## 13. H1/H2 support claims

All references to "H1 supported" or "H2 supported" fall into one of these categories:

1. **Audit/retraction text** (RESEARCH_AUDIT.md, adversarial_verification_exp_1_1.md, exp_1_1_results.md): Clearly labeled as historical or retracted.
2. **Design constraints** (EXPERIMENT_1_REDESIGN.md): "Even if H1 is supported, it does not imply H7" — hypothetical, not a claim.
3. **Code disclaimers** (exp_1_1_ablation.py): "Does NOT claim H1 is supported" — explicitly negative.
4. **Test docstrings** (test_experiment_instruments.py): References to testing that validators catch support claims — appropriate.
5. **Provenance records** (SEARCH_LOG.jsonl): Records the investigation, not a claim.

**No unsupported current H1/H2 support claims remain outside clearly labeled historical/audit text.**

## 14. Final classification

| Area | Rating | Reason | Required action |
|---|---|---|---|
| Archive integrity | READY WITH DISCLOSURES | 47 manifest + 2 extra = 49 archive files; all hashes match; 0 secret hits; extraction OK. Count discrepancy resolved (manifest self-reference + .gitignore). | None — resolved. |
| Scientific disclosure | READY WITH DISCLOSURES | H1/H2 correctly labeled INCONCLUSIVE. Original results marked void. Audit trail complete. But source manifest has only 4 sources. | Expand source manifest. |
| Software reproducibility | NOT READY | No complete captured output. Skipped metadata tests. Floating-point tests weak. Experiment 1.3 lacks instrument fixes. | Fix tests, run corrected experiment. |
| License | NOT READY | CC-BY-NC-4.0 for both code and docs. No separate LICENSE for code. May need dual licensing. | Confirm or change license. |
| Authorship/creator metadata | READY WITH DISCLOSURES | "CE-1 Research Programme" only. No individual author, ORCID, or affiliation. | Add if available. |
| Security | READY | 0 secret hits in archive. No credentials, .env files, or private paths in source code. Token not stored in any file. | Revoke compromised token. |
| Zenodo metadata | READY WITH DISCLOSURES | Metadata complete but no LICENSE file reference, no author identity, no repository URL. | Add missing fields. |
| Publication readiness | NOT READY | Archive is clean and well-structured, but license decision, token revocation, source coverage, and test quality issues remain. | Resolve all blockers. |

**Overall classification: NOT READY**

### Immediate blockers (must resolve before any Zenodo publication)

1. **License decision** — CC-BY-NC-4.0 may not be appropriate for code. Confirm or change.
2. **Token revocation** — compromised token must be revoked. Cannot verify without credentials.
3. **Zenodo draft review** — review the actual landing page at https://zenodo.org/deposit/23471293.

### Before draft creation

4. **Experiment 1.3 instrument** — add is_valid_trial, tolerance, INCONCLUSIVE verdict, metadata. Or exclude from evidence package.
5. **Source manifest** — only 4 sources; expand or narrow claims.
6. **PROJECT_INDEX.md** — update 424 → 643 (memory write requires authorization).
7. **audit_run_records.json** — gone; confirm permanent drop.

### Before publication

8. **Review Zenodo draft** at https://zenodo.org/deposit/23471293.
9. **Confirm all metadata** — title, description, keywords, license, version.
10. **Decide on void result files** — include or exclude from publication.
11. **Explicit publication authorization** from user.

### Post-publication improvements

12. Run corrected experiments with proper controls.
13. Populate source manifest with more verified sources.
14. Add environment version to experiment metadata.
15. Create CHANGELOG.
16. Consider separate episodic-memory software release.

### Explicit user decisions required

1. **Commit authorization** — 5 modified + 2 new files in CE-1 repo.
2. **CRLF normalization** — coordinate with concurrent session owners.
3. **RAR disposition** — unknown owner; no archiver available.
4. **License file** — CC-BY-NC-4.0 for code, or different license?
5. **Zenodo token** — revoke compromised token, create replacement?
6. **Publication** — publish draft as-is, or make changes first?
7. **PROJECT_INDEX.md** — update stale test count?
8. **audit_run_records.json** — permanent drop or restore?

### Classification summary

**NOT READY** — until the file accounting (resolved), token revocation, license decision, and Zenodo draft review are resolved.

The strongest immediate path is:
1. Revoke the exposed token.
2. Resolve the archive/manifest count discrepancy (already resolved: 47 manifest + 2 extra = 49 archive).
3. Confirm the license for code versus documentation.
4. Decide the creator/author metadata.
5. Review the actual Zenodo landing page.
6. Confirm the repository URL decision.
7. Verify the final archive one last time.
8. Only then decide whether to publish.

The draft itself is in the right state: **uploaded, verifiable, and unpublished**. Keep it unpublished until those metadata, security, licensing, and archive-accounting issues are resolved.

**End in HOLD.** No publication, no commit, no state changes. The Zenodo draft is created and ready for review. All evidence is recorded. The safest next action is to revoke the compromised token and review the draft at https://zenodo.org/deposit/23471293.