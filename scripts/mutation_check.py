"""Mutation harness: do the tests actually CATCH defects in the validator?

Per research-protocol: a test that has never been shown to fail is not a
test. Each mutation below is a deliberate defect injected into
validate_sources.py. Every one MUST be caught by the suite.

    python scripts/mutation_check.py
"""
import pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "scripts" / "validate_sources.py"

# (label, original_snippet, mutated_snippet)
MUTATIONS = [
    (
        "disable the evidence-grade ceiling (anti-inflation rule)",
        'if GRADE_ORDER[grade] > GRADE_ORDER[ceiling]:',
        'if False:',
    ),
    (
        "drop the ceiling lookup so nothing can exceed grade D",
        'MAX_GRADE_BY_VERIFICATION = {',
        'MAX_GRADE_BY_VERIFICATION_DISABLED = {',
    ),
    (
        "stop detecting duplicate DOIs",
        'if key in seen_dois:',
        'if False:',
    ),
    (
        "stop detecting duplicate source_id",
        'if sid in seen_ids:',
        'if False:',
    ),
    (
        "allow malformed JSON silently",
        "except json.JSONDecodeError as exc:",
        "except ValueError as exc:  # noqa\n            pass\n        except Exception as exc:",
    ),
    (
        "treat a missing manifest as valid",
        'if not path.exists():',
        'if False:',
    ),
    (
        "accept any evidence grade string",
        'if grade not in EVIDENCE_GRADES:',
        'if False:',
    ),
    (
        "accept any DOI format",
        'if not (DOI_RE.match(doi) or ARXIV_DOI_RE.match(doi)):',
        'if False:',
    ),
    (
        "stop enforcing required fields",
        'for field in REQUIRED_FIELDS:',
        'for field in ():',
    ),
    (
        "disable the anti-anthropomorphism guard",
        'if phrase not in summary:',
        'if False:',
    ),
    (
        "accept bad date formats",
        'if pub and not DATE_RE.match(str(pub)):',
        'if False:',
    ),
    (
        "accept non-integer years",
        'if not isinstance(year, int):',
        'if False:',
    ),
    (
        "accept empty author lists",
        'if not isinstance(authors, list) or not authors:',
        'if False:',
    ),
]


def run_tests() -> tuple[int, str]:
    # stdin MUST be closed. If this subprocess inherits the parent's stdin and
    # that is not a TTY (e.g. stdin redirected from /dev/null or a pipe held
    # open by a parent script), the child interpreter can fall through into the
    # interactive REPL, print an unbounded stream of _pyrepl tracebacks, and
    # hang forever. Observed on 2026-10-18: 847 MB of output before the kill.
    proc = subprocess.run(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "pytest", "tests", "-q", "--no-header", "-x"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        timeout=300,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    original = TARGET.read_text(encoding="utf-8")
    baseline_rc, _ = run_tests()
    if baseline_rc != 0:
        print("FATAL: baseline test suite does not pass; cannot mutation-test.")
        return 2
    print(f"baseline: PASS ({TARGET.relative_to(ROOT)})\n")

    caught, survived = 0, []
    for label, old, new in MUTATIONS:
        if old not in original:
            print(f"  SKIP    {label}\n          (anchor not found: {old!r})")
            survived.append(label + " [ANCHOR MISSING]")
            continue
        mutated = original.replace(old, new, 1)
        TARGET.write_text(mutated, encoding="utf-8")
        try:
            rc, out = run_tests()
        finally:
            TARGET.write_text(original, encoding="utf-8")
        if rc != 0:
            caught += 1
            print(f"  CAUGHT  {label}")
        else:
            survived.append(label)
            print(f"  SURVIVED {label}   <-- the suite does NOT catch this")

    total = len(MUTATIONS)
    print(f"\n{caught}/{total} mutations caught")
    if survived:
        print("survivors (real test gaps):")
        for s in survived:
            print(f"  - {s}")
        return 1
    print("all mutations caught -- the tests have real detection power")
    return 0


if __name__ == "__main__":
    sys.exit(main())
