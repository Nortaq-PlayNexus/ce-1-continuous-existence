"""Source manifest schema + validator for CE-1.

Implements the provenance contract from MISSION.md section 8 and
RESEARCH_PRINCIPLES.md section 2: every source must carry a stable ID,
title, authors, publication date, DOI or canonical URL, source type,
publication status, access date, relevant research questions, evidence
grade, factual summary, limitations, and verification status.

Design rules:
  * Deterministic. Same input -> same verdict, every run.
  * Fails VISIBLY. A missing required field is an error, never a default.
  * No third-party dependencies. stdlib only.
  * Never invents data. An unverified source is recorded as such.

Usage:
    python scripts/validate_sources.py
    python scripts/validate_sources.py --json
    python scripts/validate_sources.py sources/SOURCE_MANIFEST.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"

# --- Controlled vocabularies -------------------------------------------------
# These are deliberately closed sets. An unknown value is an error, because a
# free-text field cannot be validated and a silently-accepted typo becomes an
# ungradeable source.

SOURCE_TYPES = frozenset(
    {
        "journal_article",
        "preprint",
        "conference_paper",
        "book",
        "book_chapter",
        "repository",
        "dataset",
        "technical_report",
        "thesis",
        "encyclopedia",
        "web_page",
        "research_sprint",  # agent-generated sprint write-ups: NOT peer reviewed
    }
)

PUBLICATION_STATUS = frozenset(
    {
        "peer_reviewed",
        "preprint_not_peer_reviewed",
        "published_not_peer_reviewed",
        "thesis_under_review",
        "unrefereed",
        "withdrawn",
    }
)

EVIDENCE_GRADES = frozenset({"A", "B", "C", "D"})

# What we actually did to verify the source. This is the field that stops a
# plausible-looking citation from passing as a checked one.
VERIFICATION_STATUS = frozenset(
    {
        "abstract_read",  # read the abstract only
        "full_text_read",  # read the full paper
        "code_inspected",  # read the implementation
        "metadata_only",  # confirmed it exists via index/DOI, nothing read
        "unverified",  # asserted by another document, not independently checked
    }
)

# Grades B and A require actual reading. A metadata-only or unverified source
# CANNOT be graded better than C. This is the single most important rule in
# this file: it is what stops "62 papers!" style source inflation.
MAX_GRADE_BY_VERIFICATION = {
    "full_text_read": "A",
    "code_inspected": "A",
    "abstract_read": "B",
    "metadata_only": "C",
    "unverified": "D",
}

REQUIRED_FIELDS = (
    "source_id",
    "title",
    "authors",
    "published",
    "year",
    "source_type",
    "publication_status",
    "accessed",
    "research_questions",
    "evidence_grade",
    "summary",
    "limitations",
    "verification_status",
)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
ARXIV_DOI_RE = re.compile(r"^10\.48550/arXiv\.\d{4}\.\d{4,5}$")

GRADE_ORDER = {"A": 4, "B": 3, "C": 2, "D": 1}


class Finding:
    """One validation problem, tied to a line number and a source ID."""

    __slots__ = ("level", "source_id", "line", "message")

    def __init__(self, level: str, source_id: str, line: int, message: str) -> None:
        self.level = level  # "error" | "warning"
        self.source_id = source_id
        self.line = line
        self.message = message

    def __str__(self) -> str:
        return f"[{self.level.upper()}] line {self.line} ({self.source_id}): {self.message}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "source_id": self.source_id,
            "line": self.line,
            "message": self.message,
        }


def validate_record(rec: dict[str, Any], line: int) -> list[Finding]:
    """Validate one source record. Returns findings; empty means valid."""
    out: list[Finding] = []
    sid = rec.get("source_id", f"<no source_id on line {line}>")

    def err(msg: str) -> None:
        out.append(Finding("error", sid, line, msg))

    def warn(msg: str) -> None:
        out.append(Finding("warning", sid, line, msg))

    # 1. Required fields present and non-empty.
    for field in REQUIRED_FIELDS:
        if field not in rec:
            err(f"missing required field '{field}'")
        elif rec[field] in (None, "", [], {}):
            err(f"required field '{field}' is empty")

    # 2. Controlled vocabularies.
    st = rec.get("source_type")
    if st and st not in SOURCE_TYPES:
        err(f"source_type '{st}' not in {sorted(SOURCE_TYPES)}")

    ps = rec.get("publication_status")
    if ps and ps not in PUBLICATION_STATUS:
        err(f"publication_status '{ps}' not in {sorted(PUBLICATION_STATUS)}")

    vs = rec.get("verification_status")
    if vs and vs not in VERIFICATION_STATUS:
        err(f"verification_status '{vs}' not in {sorted(VERIFICATION_STATUS)}")

    # 3. Evidence grade must be uppercase A-D and must respect the
    #    verification ceiling. This is the anti-inflation rule.
    grade = rec.get("evidence_grade")
    if grade:
        if grade not in EVIDENCE_GRADES:
            err(f"evidence_grade '{grade}' must be one of A/B/C/D")
        elif vs in MAX_GRADE_BY_VERIFICATION:
            ceiling = MAX_GRADE_BY_VERIFICATION[vs]
            if GRADE_ORDER[grade] > GRADE_ORDER[ceiling]:
                err(
                    f"evidence_grade {grade} exceeds ceiling {ceiling} for "
                    f"verification_status '{vs}' -- a source that was not read "
                    f"cannot be graded as strong evidence"
                )

    # 4. Identifier: DOI preferred, canonical URL acceptable, but one required.
    doi = rec.get("doi")
    url = rec.get("url")
    if doi:
        if not (DOI_RE.match(doi) or ARXIV_DOI_RE.match(doi)):
            err(f"doi '{doi}' is not a syntactically valid DOI")
    elif not url:
        err("neither 'doi' nor 'url' present -- a source must be traceable")

    if url and not str(url).startswith(("http://", "https://", "arxiv.org", "github.com")):
        warn(f"url '{url}' is not an http(s) URL")

    # 5. Dates.
    pub = rec.get("published")
    if pub and not DATE_RE.match(str(pub)):
        err(f"published '{pub}' must be ISO YYYY-MM-DD")

    acc = rec.get("accessed")
    if acc and not DATE_RE.match(str(acc)):
        err(f"accessed '{acc}' must be ISO YYYY-MM-DD")

    year = rec.get("year")
    if year is not None:
        if not isinstance(year, int):
            err(f"year '{year}' must be an integer, not {type(year).__name__}")
        elif not 1900 <= year <= 2100:
            err(f"year {year} out of plausible range")

    # 6. Authors must be a non-empty list of strings.
    authors = rec.get("authors")
    if authors is not None:
        if not isinstance(authors, list) or not authors:
            err("authors must be a non-empty list")
        elif not all(isinstance(a, str) and a.strip() for a in authors):
            err("authors must be a list of non-empty strings")

    # 7. Limitations must be explicit, even if "none known".
    lim = rec.get("limitations")
    if isinstance(lim, list) and not lim:
        warn("limitations is an empty list -- record 'none known' if truly none")

    # 8. Anti-anthropomorphism. CE-1 must never itself assert that a system has
    #    subjective experience (RESEARCH_PRINCIPLES.md section 9). Reporting
    #    what a theory *claims* is legitimate and necessary, so a record that
    #    does so must mark it: "claims_attribution": "source_claim".
    summary = str(rec.get("summary", "")).lower()
    banned = (
        "proves consciousness",
        "proves that the ai is conscious",
        "demonstrates subjective experience",
        "is conscious",
    )
    if summary:
        attribution = str(rec.get("claims_attribution", "")).strip().lower()
        attributed = attribution in {"source_claim", "source"}
        for phrase in banned:
            if phrase not in summary:
                continue
            if attributed:
                warn(
                    f"summary reports the source's own claim ('{phrase}') -- "
                    f"acceptable because claims_attribution='source_claim'; "
                    f"CE-1 must not adopt it"
                )
            else:
                err(
                    f"summary contains a consciousness-establishing claim "
                    f"('{phrase}') with no attribution. CE-1 must never assert "
                    f"this. If the phrase is the SOURCE's claim, set "
                    f"\"claims_attribution\": \"source_claim\"."
                )

    return out


def validate_manifest(path: Path) -> tuple[list[Finding], dict[str, Any]]:
    """Validate a JSONL manifest. Returns (findings, stats)."""
    findings: list[Finding] = []
    seen_ids: dict[str, int] = {}
    seen_dois: dict[str, int] = {}
    seen_urls: dict[str, int] = {}
    records: list[dict[str, Any]] = []

    if not path.exists():
        return (
            [Finding("error", "<manifest>", 0, f"manifest not found: {path}")],
            {"records": 0},
        )

    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()

    for lineno, line in enumerate(raw.decode("utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            findings.append(
                Finding("error", "<malformed>", lineno, f"invalid JSON: {exc}")
            )
            continue
        if not isinstance(rec, dict):
            findings.append(
                Finding("error", "<malformed>", lineno, "record is not a JSON object")
            )
            continue

        findings.extend(validate_record(rec, lineno))
        records.append(rec)

        # Duplicate detection (directive section 8: "duplicate source detection").
        sid = rec.get("source_id")
        if isinstance(sid, str):
            if sid in seen_ids:
                findings.append(
                    Finding(
                        "error",
                        sid,
                        lineno,
                        f"duplicate source_id, first seen on line {seen_ids[sid]}",
                    )
                )
            else:
                seen_ids[sid] = lineno

        doi = rec.get("doi")
        if isinstance(doi, str) and doi:
            key = doi.lower()
            if key in seen_dois:
                findings.append(
                    Finding(
                        "error",
                        sid,
                        lineno,
                        f"duplicate DOI {doi}, first seen on line {seen_dois[key]}",
                    )
                )
            else:
                seen_dois[key] = lineno

        url = rec.get("url")
        if isinstance(url, str) and not doi:
            key = url.rstrip("/").lower()
            if key in seen_urls:
                findings.append(
                    Finding(
                        "error",
                        sid,
                        lineno,
                        f"duplicate URL {url}, first seen on line {seen_urls[key]}",
                    )
                )
            else:
                seen_urls[key] = lineno

    grades: dict[str, int] = {}
    vstatus: dict[str, int] = {}
    for rec in records:
        g = rec.get("evidence_grade")
        if isinstance(g, str):
            grades[g] = grades.get(g, 0) + 1
        v = rec.get("verification_status")
        if isinstance(v, str):
            vstatus[v] = vstatus.get(v, 0) + 1

    stats = {
        "manifest": str(path),
        "sha256": digest,
        "schema_version": SCHEMA_VERSION,
        "records": len(records),
        "by_evidence_grade": dict(sorted(grades.items())),
        "by_verification_status": dict(sorted(vstatus.items())),
        "unique_dois": len(seen_dois),
        "unique_urls_without_doi": len(seen_urls),
    }
    return findings, stats


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate the CE-1 source manifest.")
    ap.add_argument(
        "manifest",
        nargs="?",
        default=str(Path(__file__).resolve().parent.parent / "sources" / "SOURCE_MANIFEST.jsonl"),
        help="path to SOURCE_MANIFEST.jsonl",
    )
    ap.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = ap.parse_args(argv)

    findings, stats = validate_manifest(Path(args.manifest))
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]

    if args.json:
        print(
            json.dumps(
                {
                    "ok": not errors,
                    "stats": stats,
                    "errors": [f.as_dict() for f in errors],
                    "warnings": [f.as_dict() for f in warnings],
                },
                indent=2,
            )
        )
        return 1 if errors else 0

    print(f"CE-1 source manifest validation  (schema {SCHEMA_VERSION})")
    print(f"  manifest : {stats['manifest']}")
    print(f"  sha256   : {stats.get('sha256', 'n/a')}")
    print(f"  records  : {stats['records']}")
    if "by_evidence_grade" in stats:
        print(f"  grades   : {stats['by_evidence_grade']}")
        print(f"  verified : {stats['by_verification_status']}")
    print()

    for f in errors:
        print(f"  {f}")
    for f in warnings:
        print(f"  {f}")

    print()
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())