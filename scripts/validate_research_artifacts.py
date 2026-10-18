"""Research-artifact validator for CE-1.

Master directive section 7 forbids empty files created "merely to satisfy a
checklist" and requires every artifact to contain substantive content or
document why it is incomplete. Master directive section 13 requires scripts
that "fail visibly when required information is missing."

This script enforces that across the repository's research documents. It is
deliberately opinionated and reports findings rather than silently passing.

Two classes of check:

  A. STRUCTURAL  - required artifacts exist and are non-trivial.
  B. CONSISTENCY - claims in the prose agree with the data files. This is the
                   check that caught the falsified exp_1_1 result.

Usage:
    python scripts/validate_research_artifacts.py
    python scripts/validate_research_artifacts.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Artifacts the directive requires. Each maps to whether it must exist at
# Stage 0 or is deferred to a later stage.
REQUIRED_AT_STAGE_0 = {
    "README.md": "project charter",
    "MISSION.md": "research charter",
    "RESEARCH_PRINCIPLES.md": "evidence grading policy",
    "research/RESEARCH_MAP.md": "research map",
    "research/RESEARCH_AUDIT.md": "evidence audit",
    "hypotheses/HYPOTHESIS_REGISTER.md": "H1-H7 register",
    "experiments/EXPERIMENT_ROADMAP.md": "experimental roadmap",
    "sources/SOURCE_MANIFEST.jsonl": "source manifest",
    "sources/SEARCH_LOG.jsonl": "search log",
    "sources/ACCESS_LIMITATIONS.md": "access limitations",
}

DEFERRED = {
    "research/LITERATURE_REVIEW.md": "Stage 0 stretch goal",
    "research/LITERATURE_REGISTER.csv": "Stage 0 stretch goal",
    "research/THEORY_COMPARISON.md": "Stage 0 stretch goal",
    "research/IMPLEMENTATION_CATALOG.md": "Stage 0 stretch goal",
    "research/EVIDENCE_LEDGER.md": "Stage 0 stretch goal",
    "research/OPEN_QUESTIONS.md": "Stage 0 stretch goal",
    "research/CONTRADICTORY_EVIDENCE.md": "Stage 0 stretch goal",
    "research/RESEARCH_GAPS.md": "Stage 0 stretch goal",
    "hypotheses/OPERATIONAL_DEFINITIONS.md": "Stage 1",
    "hypotheses/FALSIFICATION_CRITERIA.md": "Stage 1",
    "hypotheses/COMPETING_EXPLANATIONS.md": "Stage 1",
    "experiments/PROTOCOL_TEMPLATE.md": "Stage 1",
    "experiments/PREREGISTRATION_TEMPLATE.md": "Stage 1",
    "experiments/CONTROL_DESIGNS.md": "Stage 1",
    "experiments/METRICS.md": "Stage 1",
    "experiments/RESULTS_TEMPLATE.md": "Stage 1",
    "experiments/REPLICATION_PROTOCOL.md": "Stage 5",
    "architecture/ARCHITECTURE_OPTIONS.md": "Stage 1",
    "architecture/PERSISTENT_STATE_DESIGN.md": "exists (Stage 1)",
    "architecture/CONTINUAL_LEARNING_REVIEW.md": "Stage 1",
    "architecture/COGNITIVE_PROCESSING_DESIGN.md": "Stage 1",
    "architecture/SELF_MODEL_DESIGN.md": "Stage 1",
    "architecture/SAFETY_AND_FAILURE_MODES.md": "Stage 0",
    "reports/INITIAL_RESEARCH_REPORT.md": "initial report",
    "reports/EXECUTIVE_SUMMARY.md": "executive summary",
    "reports/NEXT_STEPS.md": "next-action plan",
    "CONTRIBUTING.md": "contribution guide",
    "scripts/make_research_manifest.py": "provenance system",
}

# A document shorter than this is treated as a stub unless it explains itself.
STUB_BYTES = 400

# A markdown document claiming substantive content should exceed this.
THIN_BYTES = 1200


def human(n: int) -> str:
    return f"{n/1024:.1f} KB"


def check_structure() -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict = {"required": {}, "deferred": {}, "dirs": {}}

    for rel, purpose in REQUIRED_AT_STAGE_0.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"REQUIRED ARTIFACT MISSING: {rel} ({purpose})")
            continue
        size = p.stat().st_size
        stats["required"][rel] = size
        if size < STUB_BYTES:
            errors.append(f"REQUIRED ARTIFACT IS A STUB: {rel} ({size} B < {STUB_BYTES} B)")
        elif rel.endswith(".md") and size < THIN_BYTES:
            warnings.append(f"artifact looks thin: {rel} ({human(size)})")

    for rel, stage in DEFERRED.items():
        p = ROOT / rel
        exists = p.exists()
        stats["deferred"][rel] = {"exists": exists, "stage": stage}
        if not exists:
            warnings.append(f"not yet present (declared: {stage}): {rel}")

    # Empty directories the directive explicitly calls out.
    for d in ("datasets", "prototypes", "tests", "scripts", "sources"):
        p = ROOT / d
        if p.exists() and p.is_dir():
            files = [f for f in p.rglob("*") if f.is_file() and "__pycache__" not in str(f)]
            stats["dirs"][d] = len(files)
            if not files:
                errors.append(f"EMPTY DIRECTORY: {d}/ (directive sec. 7 forbids checklist-only dirs)")
    return errors, warnings, stats


def check_consistency() -> tuple[list[str], list[str]]:
    """Cross-check prose claims against result data.

    This is the check that matters most: it is what catches a report claiming
    an experiment supports a hypothesis when the data says otherwise, or when
    the data has been withdrawn.
    """
    errors: list[str] = []
    warnings: list[str] = []

    audit = ROOT / "research" / "RESEARCH_AUDIT.md"
    results_dir = ROOT / "experiments" / "results"

    # 1. If the audit declares a result VOID, the void marker must exist.
    if audit.exists():
        text = audit.read_text(encoding="utf-8", errors="replace")
        if "VOID" in text.upper() and results_dir.exists():
            void_files = list(results_dir.glob("*.VOID.md"))
            if not void_files:
                warnings.append(
                    "audit discusses a VOID result but no *.VOID.md marker exists "
                    "in experiments/results/"
                )

    # 2. Any result JSON must not assert a hypothesis the audit has withdrawn.
    withdrawn = set()
    if audit.exists():
        for m in re.finditer(r"\bexp_1_(\d)\b", audit.read_text(encoding="utf-8", errors="replace")):
            withdrawn.add(f"exp_1_{m.group(1)}")

    for jf in sorted(results_dir.glob("exp_*.json")) if results_dir.exists() else []:
        stem_key = jf.stem.split("_results")[0]
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"malformed result JSON: {jf.name}: {exc}")
            continue

        comp = data.get("comparison", {})
        # 3. A verdict flag that disagrees with its own displayed difference is
        #    the float-threshold bug found in exp_1_2.
        for flag, delta_key in (
            ("any_context_helps", None),
            ("episodic_structure_matters", None),
            ("h1_supported", "mean_difference"),
        ):
            if flag in comp and isinstance(comp[flag], bool):
                # find a matching numeric delta
                deltas = [
                    v
                    for k, v in comp.items()
                    if isinstance(v, (int, float)) and k != flag
                ]
                if deltas and all(d == 0 for d in deltas) and comp[flag] is True:
                    errors.append(
                        f"{jf.name}: verdict '{flag}' is True but every reported "
                        f"difference is 0.0 -- verdict and data disagree"
                    )

        # 4. Empty model outputs make every score zero by construction.
        for cond_name, cond in (data.get("conditions") or {}).items():
            outs = cond.get("outputs")
            if isinstance(outs, list) and outs and all(not o for o in outs):
                errors.append(
                    f"{jf.name}: condition '{cond_name}' has ALL EMPTY model "
                    f"outputs ({len(outs)}/{len(outs)}); all scores are 0 by "
                    f"construction and the result is VOID"
                )

        # 5. A committed result that the audit has declared non-reproducible
        #    must carry a warning in its own filename or a sidecar.
        if stem_key in withdrawn and audit.exists():
            atext = audit.read_text(encoding="utf-8", errors="replace")
            if ("INCONCLUSIVE" in atext or "not reproduce" in atext.lower()):
                sidecars = list(results_dir.glob(f"{stem_key}*.VOID.md"))
                if not sidecars and "VOID" not in jf.name:
                    warnings.append(
                        f"{jf.name}: audit treats {stem_key} as inconclusive but "
                        f"no VOID sidecar marks this file -- it can still be cited "
                        f"by mistake"
                    )
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate CE-1 research artifacts.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    s_err, s_warn, stats = check_structure()
    c_err, c_warn = check_consistency()
    errors, warnings = s_err + c_err, s_warn + c_warn

    if args.json:
        print(
            json.dumps(
                {
                    "ok": not errors,
                    "stats": stats,
                    "errors": errors,
                    "warnings": warnings,
                },
                indent=2,
            )
        )
        return 1 if errors else 0

    print("CE-1 research artifact validation")
    print("=" * 60)
    print("\nSTRUCTURE")
    for rel, size in sorted(stats["required"].items()):
        print(f"  ok   {rel:45s} {human(size)}")
    print(f"\n  dirs: {stats['dirs']}")

    print("\nCONSISTENCY")
    print(f"  {len(c_err)} error(s), {len(c_warn)} warning(s)")

    print("\nFINDINGS")
    for e in errors:
        print(f"  ERROR   {e}")
    for w in warnings:
        print(f"  warning {w}")

    print("\n" + "=" * 60)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())