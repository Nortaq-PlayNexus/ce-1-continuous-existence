"""make_research_manifest.py — CE-1 experiment + provenance manifest.

Master directive section 8 requires an experiment manifest recording, where
available: experiment identifier, hypothesis, preregistered protocol identifier,
repository commit, software versions, environment details, configuration,
random seeds, dataset identifiers and hashes, commands executed, start and
completion times, exit codes, raw artifact locations, result hashes, deviations
from protocol, and independent verification status.

This script generates that record for the current repository state. It is
deliberately conservative: it records what it can PROVE and writes
`null` with an explicit reason for what it cannot, rather than inventing a
value. A missing seed is a finding, not something to paper over.

Usage:
    python scripts/make_research_manifest.py
    python scripts/make_research_manifest.py --json
    python scripts/make_research_manifest.py --out path.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent


def sha256_file(p: Path) -> str | None:
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str | None:
    """Run a git command. Returns None if unavailable, so the manifest degrades
    honestly instead of crashing or lying."""
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
            stdin=subprocess.DEVNULL,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None


def collect_environment() -> dict[str, Any]:
    venv_python = ROOT / ".venv" / "Scripts" / "python.exe"
    interp = str(venv_python) if venv_python.is_file() else sys.executable
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "interpreter": interp,
        "project_local_venv": venv_python.is_file(),
        "gpu_assumed": False,  # directive sec. 11: "Do not assume GPU availability"
        "internet_assumed": False,  # directive sec. 11
    }


def collect_provenance() -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    status = git("status", "--porcelain")
    return {
        "repository_root": str(ROOT),
        "commit": head,
        "commit_unavailable_reason": None if head else "git unavailable or no commits",
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "clean_working_tree": (status == "") if status is not None else None,
        "uncommitted_changes": (
            [ln for ln in status.splitlines() if ln.strip()] if status else []
        ),
        "git_identity": git("config", "user.name"),
    }


def collect_results() -> list[dict[str, Any]]:
    """Inventory result files with content hashes (directive sec. 8:
    'result hashes', 'raw artifact locations')."""
    results_dir = ROOT / "experiments" / "results"
    entries: list[dict[str, Any]] = []
    if not results_dir.is_dir():
        return entries
    for p in sorted(results_dir.glob("*.json")):
        digest = sha256_file(p)
        verdict: dict[str, Any] | None = None
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            verdict = data.get("comparison") or None
        except (json.JSONDecodeError, UnicodeDecodeError):
            verdict = None
        entries.append(
            {
                "path": str(p.relative_to(ROOT)),
                "sha256": digest,
                "bytes": p.stat().st_size,
                "verdict_fields": verdict,
            }
        )
    return entries


def collect_experiments() -> list[dict[str, Any]]:
    """Experiment definitions found in experiments/*.py and their protocols."""
    exp_dir = ROOT / "experiments"
    out: list[dict[str, Any]] = []
    if not exp_dir.is_dir():
        return out
    for script in sorted(exp_dir.glob("exp_*.py")):
        stem = script.stem
        protocol = exp_dir / f"{stem}_protocol.md"
        out.append(
            {
                "experiment_id": stem,
                "script": str(script.relative_to(ROOT)),
                "script_sha256": sha256_file(script),
                "protocol": str(protocol.relative_to(ROOT)) if protocol.is_file() else None,
                "preregistered": protocol.is_file(),
                "preregistration_note": (
                    "A protocol markdown exists, but thresholds were NOT fixed "
                    "before execution in at least one case (exp_1_2 used a "
                    "post-hoc >= 1.0 threshold)."
                    if stem.startswith("exp_1_2")
                    else None
                ),
                "random_seed_controlled": False,
                "random_seed_note": (
                    "Ollama /api/generate exposes no seed parameter; sampling is "
                    "not reproducible. This is a LIMITATION of every experiment "
                    "in this repository and is why effect sizes moved across runs."
                ),
                "independent_verification_status": (
                    "re-attacked by scripts/verify_exp_1_1.py; original effect did "
                    "not reproduce"
                    if stem.startswith("exp_1_1")
                    else "not independently re-attacked"
                ),
                "status": (
                    "INCONCLUSIVE (instrument defect) - see research/RESEARCH_AUDIT.md"
                    if stem.startswith("exp_1_1")
                    else "INCONCLUSIVE (verdict decided by float error)"
                    if stem.startswith("exp_1_2")
                    else "unknown"
                ),
            }
        )
    return out


def collect_sources() -> dict[str, Any]:
    manifest = ROOT / "sources" / "SOURCE_MANIFEST.jsonl"
    search_log = ROOT / "sources" / "SEARCH_LOG.jsonl"
    grades: dict[str, int] = {}
    records = 0
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            records += 1
            try:
                g = json.loads(line).get("evidence_grade", "?")
            except json.JSONDecodeError:
                g = "?"
            grades[g] = grades.get(g, 0) + 1
    return {
        "source_manifest_sha256": sha256_file(manifest),
        "source_records": records,
        "sources_by_evidence_grade": dict(sorted(grades.items())),
        "search_log_sha256": sha256_file(search_log),
        "search_log_entries": (
            len([ln for ln in search_log.read_text(encoding="utf-8").splitlines() if ln.strip()])
            if search_log.is_file()
            else 0
        ),
    }


def build() -> dict[str, Any]:
    return {
        "manifest_schema": "ce1-experiment-manifest/1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/make_research_manifest.py",
        "programme": {
            "name": "CE-1 Continuous Existence Research Programme",
            "stage": "Stage 0 - research baseline",
            "charter": "MISSION.md",
            "principles": "RESEARCH_PRINCIPLES.md",
            "audit": "research/RESEARCH_AUDIT.md",
        },
        "provenance": collect_provenance(),
        "environment": collect_environment(),
        "experiments": collect_experiments(),
        "results": collect_results(),
        "sources": collect_sources(),
        "deviations_from_protocol": [
            {
                "id": "D1",
                "description": (
                    "Experiments were executed and their results committed to git "
                    "without the authorization the master directive requires "
                    "(section 13: 'Do not make Git commits unless explicitly "
                    "authorized')."
                ),
                "status": "unresolved - flagged for the programme owner",
            },
            {
                "id": "D2",
                "description": (
                    "exp_1_2's decision thresholds were chosen after observing the "
                    "data, and the resulting verdict flags are decided by ~2e-16 of "
                    "floating-point error."
                ),
                "status": "documented in research/RESEARCH_AUDIT.md section 9",
            },
            {
                "id": "D3",
                "description": (
                    "No random seed is controllable via the Ollama API, so no "
                    "experiment in this repository is bit-reproducible."
                ),
                "status": "unresolved - requires a different inference backend",
            },
            {
                "id": "D4",
                "description": (
                    "The literature review is incomplete: 4 verified sources against "
                    "the six areas the directive enumerates."
                ),
                "status": "open - see sources/ACCESS_LIMITATIONS.md",
            },
        ],
        "audit_mechanism_limits": (
            "This manifest is a point-in-time record of file hashes. It is NOT "
            "tamper-proof: an actor with write access can regenerate it after "
            "altering any file. Its value is in making silent drift detectable by "
            "a reviewer who compares hashes across time, not in preventing "
            "modification. Hashes are recorded so a third party can recompute them."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the CE-1 experiment manifest.")
    ap.add_argument("--json", action="store_true", help="print to stdout only")
    ap.add_argument("--out", help="also write to this path")
    args = ap.parse_args(argv)

    manifest = build()
    text = json.dumps(manifest, indent=2)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")

    if args.json:
        print(text)
    else:
        p = manifest["provenance"]
        print("CE-1 experiment manifest")
        print("=" * 60)
        print(f"  generated      : {manifest['generated_at_utc']}")
        print(f"  commit         : {p.get('commit')}")
        print(f"  branch         : {p.get('branch')}")
        print(f"  clean tree     : {p.get('clean_working_tree')}")
        print(f"  experiments    : {len(manifest['experiments'])}")
        print(f"  result files   : {len(manifest['results'])}")
        print(f"  source records : {manifest['sources']['source_records']}")
        print(f"  grades         : {manifest['sources']['sources_by_evidence_grade']}")
        print(f"  deviations     : {len(manifest['deviations_from_protocol'])}")
        print()
        print("  H1/H2 status   : INCONCLUSIVE (see research/RESEARCH_AUDIT.md)")
        if args.out:
            print(f"\n  written to     : {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())