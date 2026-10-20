# Claim Audit — Post-Publication

## Date
2026-10-20

## Scope
Repository-wide search across all tracked and untracked files for:
- "H1 supported"
- "H2 supported"
- "conscious"
- "subjective experience"
- "Identity as Trajectory"

## Classification key

| Classification | Definition |
|---|---|
| **Valid historical/audit reference** | Occurrence is in an audit report, correction log, or historical result file that accurately documents what was claimed and why it was retracted. |
| **Valid limitation/disclaimer** | Occurrence is in a disclaimer, limitation statement, or boundary condition that correctly states what is NOT established. |
| **Potentially misleading active claim** | Occurrence appears in a document that could be read as currently asserting the claim without adequate qualification. |

## "H1 supported" occurrences

| File | Line(s) | Context | Classification |
|---|---|---|---|
| reports/exp_1_1_results.md | 8, 58 | RETRACTED banner + corrected "H1 supported: INCONCLUSIVE" | Valid historical/audit reference |
| research/RESEARCH_AUDIT.md | 30, 341 | Audit context, correctly labeled as retracted | Valid historical/audit reference |
| FINAL_AUDIT_REPORT.md | 19, 47, 52, 58, 63, 69, 71, 92, 138, 239-242, 394 | Audit report documenting correction | Valid historical/audit reference |
| experiments/results/exp_1_1_results.json | 239 | `"h1_supported": true` in void run (labeled VOID) | Valid historical/audit reference |
| hypotheses/HYPOTHESIS_REGISTER.md | 30 | "H1 supported: INCONCLUSIVE" (corrected) | Valid historical/audit reference |

**Verdict:** No potentially misleading active claims. All occurrences are in audit/correction context or historical files with retraction labels.

## "H2 supported" occurrences

| File | Line(s) | Context | Classification |
|---|---|---|---|
| reports/exp_1_2_results.md | 30 | "H2 supported: INCONCLUSIVE" (corrected) | Valid historical/audit reference |
| FINAL_AUDIT_REPORT.md | 241 | Audit report documenting correction | Valid historical/audit reference |
| experiments/results/exp_1_2_results.json | 241 | `"episodic_structure_matters": false` (corrected) | Valid historical/audit reference |

**Verdict:** No potentially misleading active claims. H2 is consistently labeled INCONCLUSIVE.

## "conscious" occurrences

All occurrences of "conscious" are in one of these categories:

1. **Research literature references** (RESEARCH_MAP.md, INITIAL_RESEARCH_REPORT.md): Discussion of consciousness theories (GWT, IIT, etc.) as background literature. These are academic references, not claims about CE-1.
2. **Limitation/disclaimer statements**: "This does not establish consciousness," "No AI system has been confirmed conscious," "A performance difference alone would not prove conscious experience."
3. **Hypothesis definitions** (HYPOTHESIS_REGISTER.md): H7 "Subjective experience" is explicitly defined as "Out of reach" with no supporting evidence.
4. **Audit reports**: References to consciousness in the context of what is NOT claimed.

**Verdict:** No potentially misleading active claims. All occurrences are either academic references or explicit limitations.

## "subjective experience" occurrences

| File | Context | Classification |
|---|---|---|
| RESEARCH_PRINCIPLES.md | "The gap between storage and experience is the gap between data and consciousness" | Valid limitation/disclaimer |
| reports/* | "H7 (subjective experience) is supported" — in context of "What this cannot establish" | Valid limitation/disclaimer |
| hypotheses/HYPOTHESIS_REGISTER.md | H7 definition, labeled "Out of reach" | Valid limitation/disclaimer |
| experiments/exp_1_3_state_ablation.py | "subjective experience (RESEARCH_PRINCIPLES.md section 9)" in code comment | Valid limitation/disclaimer |
| src/ce1/* (if present) | Validation code checking for "demonstrates subjective experience" string | Valid limitation/disclaimer |

**Verdict:** No potentially misleading active claims. Subjective experience is consistently framed as not established.

## "Identity as Trajectory" occurrences

| File | Context | Classification |
|---|---|---|
| sources/SOURCE_MANIFEST.jsonl | Retracted citation entry (correctly marked as retracted) | Valid historical/audit reference |
| research/RESEARCH_AUDIT.md | Audit finding documenting retraction | Valid historical/audit reference |
| FINAL_AUDIT_REPORT.md | Audit report documenting retraction | Valid historical/audit reference |
| tests/test_validate_sources.py | Test verifying retracted citation is flagged | Valid historical/audit reference |
| research/RESEARCH_MAP.md | Removed from gap table (citation retracted) | Valid historical/audit reference |
| experiments/EXPERIMENT_ROADMAP.md | Removed from searched list | Valid historical/audit reference |

**Verdict:** No potentially misleading active claims. All references are in audit/correction context documenting the retraction.

## Summary

| Phrase | Total occurrences | Misleading active claims | Action required |
|---|---|---|---|
| "H1 supported" | ~15 | 0 | None |
| "H2 supported" | ~5 | 0 | None |
| "conscious" | ~40 | 0 | None |
| "subjective experience" | ~20 | 0 | None |
| "Identity as Trajectory" | ~15 | 0 | None |

## Conclusion

**No potentially misleading active claims found.** All occurrences of the target phrases are either:
1. Valid historical/audit references documenting corrections and retractions.
2. Valid limitation/disclaimer statements correctly stating what is NOT established.

No document modifications are required. Historical evidence and audit history are preserved.

## Recommendation

The repository's claim hygiene is satisfactory for the current stage. Future documents (especially the H8 preregistration and continuity_v1 benchmark) should continue the pattern of explicit limitation statements and avoid any language that could be read as claiming consciousness, subjective experience, or continuous existence.
