"""Tests for the CE-1 provenance machinery.

Directive section 8 requires: "add tests for manifest generation, duplicate
source detection, missing fields, malformed records, and inconsistent
completion states."

These tests are adversarial on purpose. A validator that has never been shown
to fail is not a validator. Each test below constructs a record that SHOULD be
rejected and asserts that it IS.

Run:  python -m pytest tests/ -v
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate_sources as vs  # noqa: E402


def good_record(**overrides) -> dict:
    """A minimal record that must validate cleanly."""
    rec = {
        "source_id": "test2024ok",
        "title": "A Perfectly Ordinary Paper About Nothing In Particular",
        "authors": ["A. Author"],
        "published": "2024-01-15",
        "year": 2024,
        "doi": "10.1234/ordinary",
        "url": "https://example.org/paper",
        "source_type": "journal_article",
        "publication_status": "peer_reviewed",
        "accessed": "2026-10-18",
        "research_questions": ["H1"],
        "evidence_grade": "B",
        "summary": "Reports a modest, well-controlled result about widget calibration.",
        "limitations": ["Single lab.", "Small sample."],
        "verification_status": "full_text_read",
    }
    rec.update(overrides)
    return rec


def errors_for(rec: dict) -> list[str]:
    findings = vs.validate_record(rec, 1)
    return [f.message for f in findings if f.level == "error"]


def warnings_for(rec: dict) -> list[str]:
    findings = vs.validate_record(rec, 1)
    return [f.message for f in findings if f.level == "warning"]


# --- The control: a good record must actually pass --------------------------


def test_good_record_has_no_errors():
    assert errors_for(good_record()) == []


# --- Anti-inflation rule: unread sources cannot be graded A/B ---------------


def test_unverified_source_cannot_be_graded_b():
    """The single most important rule: you cannot claim strong evidence for a
    source you never read."""
    rec = good_record(verification_status="unverified", evidence_grade="B")
    errs = errors_for(rec)
    assert any("exceeds ceiling" in e for e in errs), errs


def test_unverified_source_cannot_be_graded_a():
    rec = good_record(verification_status="unverified", evidence_grade="A")
    assert any("exceeds ceiling" in e for e in errors_for(rec))


def test_metadata_only_cannot_be_graded_a_but_can_be_c():
    rec = good_record(verification_status="metadata_only", evidence_grade="A")
    assert any("exceeds ceiling" in e for e in errors_for(rec))
    rec_c = good_record(verification_status="metadata_only", evidence_grade="C")
    assert errors_for(rec_c) == []


def test_abstract_read_cannot_be_graded_a():
    rec = good_record(verification_status="abstract_read", evidence_grade="A")
    assert any("exceeds ceiling" in e for e in errors_for(rec))


def test_full_text_read_may_be_graded_a():
    rec = good_record(verification_status="full_text_read", evidence_grade="A")
    assert errors_for(rec) == []


# --- Missing required fields -------------------------------------------------


@pytest.mark.parametrize("field", vs.REQUIRED_FIELDS)
def test_each_required_field_is_enforced(field):
    rec = good_record()
    del rec[field]
    errs = errors_for(rec)
    assert any(field in e for e in errs), f"{field} not enforced: {errs}"


def test_empty_required_field_is_an_error_not_a_default():
    """A blank limitations list must not silently become 'no limitations'."""
    rec = good_record(limitations=[])
    assert any("limitations" in e for e in errors_for(rec))


def test_none_required_field_is_an_error():
    rec = good_record(title=None)
    assert any("title" in e for e in errors_for(rec))


# --- Identifier traceability -------------------------------------------------


def test_source_without_doi_or_url_is_rejected():
    rec = good_record()
    del rec["doi"]
    del rec["url"]
    assert any("neither 'doi' nor 'url'" in e for e in errors_for(rec))


def test_malformed_doi_is_rejected():
    rec = good_record(doi="not-a-doi")
    assert any("not a syntactically valid DOI" in e for e in errors_for(rec))


def test_arxiv_doi_is_accepted():
    rec = good_record(doi="10.48550/arXiv.2308.08708")
    assert errors_for(rec) == []


# --- Controlled vocabularies ------------------------------------------------


def test_bad_source_type_rejected():
    rec = good_record(source_type="blog_post")
    assert any("source_type" in e for e in errors_for(rec))


def test_bad_evidence_grade_rejected():
    rec = good_record(evidence_grade="A+")
    assert any("must be one of A/B/C/D" in e for e in errors_for(rec))


def test_lowercase_evidence_grade_rejected():
    rec = good_record(evidence_grade="a", verification_status="full_text_read")
    assert any("must be one of A/B/C/D" in e for e in errors_for(rec))


def test_bad_verification_status_rejected():
    rec = good_record(verification_status="i_read_it_sometime")
    assert any("verification_status" in e for e in errors_for(rec))


def test_research_sprint_is_a_recognised_source_type():
    """The retracted 'Identity as Trajectory' citation was a sprint write-up.
    The schema must be able to say so explicitly rather than hide it."""
    rec = good_record(source_type="research_sprint")
    assert errors_for(rec) == []


# --- Dates and types ---------------------------------------------------------


def test_bad_date_format_rejected():
    rec = good_record(published="15/01/2024")
    assert any("ISO YYYY-MM-DD" in e for e in errors_for(rec))


def test_non_integer_year_rejected():
    rec = good_record(year="2024")
    assert any("must be an integer" in e for e in errors_for(rec))


def test_implausible_year_rejected():
    rec = good_record(year=1600)
    assert any("out of plausible range" in e for e in errors_for(rec))


def test_authors_must_be_list():
    rec = good_record(authors="A. Author")
    assert any("authors must be a non-empty list" in e for e in errors_for(rec))


def test_authors_must_not_contain_blanks():
    rec = good_record(authors=["A. Author", "  "])
    assert any("non-empty strings" in e for e in errors_for(rec))


# --- Anti-anthropomorphism ---------------------------------------------------


def test_consciousness_claim_without_attribution_is_rejected():
    rec = good_record(summary="The framework shows the network is conscious.")
    errs = errors_for(rec)
    assert any("CE-1 must never assert this" in e for e in errs), errs


def test_attributed_source_claim_downgrades_to_warning():
    """Reporting what IIT claims is legitimate. It must warn, not error, and
    must not be silently dropped."""
    rec = good_record(
        summary="The authors propose applying the postulates to determine "
        "whether a system is conscious.",
        claims_attribution="source_claim",
    )
    assert errors_for(rec) == []
    assert any("source's own claim" in w for w in warnings_for(rec))


def test_proves_consciousness_is_always_rejected():
    rec = good_record(summary="This proves consciousness in artificial minds.")
    assert any("CE-1 must never assert this" in e for e in errors_for(rec))


# --- Duplicate detection (directive section 8) -----------------------------


def test_duplicate_source_id_detected(tmp_path: Path):
    p = tmp_path / "m.jsonl"
    rec = good_record()
    p.write_text(json.dumps(rec) + "\n" + json.dumps(rec) + "\n", encoding="utf-8")
    findings, stats = vs.validate_manifest(p)
    dups = [f for f in findings if "duplicate source_id" in f.message]
    assert dups, "duplicate source_id was NOT detected"
    assert stats["records"] == 2


def test_duplicate_doi_detected_even_with_different_ids(tmp_path: Path):
    p = tmp_path / "m.jsonl"
    a = good_record(source_id="one")
    b = good_record(source_id="two")
    p.write_text(json.dumps(a) + "\n" + json.dumps(b) + "\n", encoding="utf-8")
    findings, _ = vs.validate_manifest(p)
    assert any("duplicate DOI" in f.message for f in findings)


def test_blank_lines_are_skipped_not_flagged(tmp_path: Path):
    p = tmp_path / "m.jsonl"
    p.write_text(json.dumps(good_record()) + "\n\n\n", encoding="utf-8")
    findings, stats = vs.validate_manifest(p)
    assert stats["records"] == 1
    assert [f for f in findings if f.level == "error"] == []


# --- Malformed records -------------------------------------------------------


def test_malformed_json_line_is_flagged_not_skipped(tmp_path: Path):
    p = tmp_path / "m.jsonl"
    p.write_text(json.dumps(good_record()) + "\n{not json\n", encoding="utf-8")
    findings, stats = vs.validate_manifest(p)
    assert stats["records"] == 1
    assert any("invalid JSON" in f.message for f in findings)


def test_non_object_line_is_flagged(tmp_path: Path):
    p = tmp_path / "m.jsonl"
    p.write_text('["not", "an", "object"]\n', encoding="utf-8")
    findings, _ = vs.validate_manifest(p)
    assert any("not a JSON object" in f.message for f in findings)


def test_missing_manifest_fails_visibly(tmp_path: Path):
    """Must fail loudly, not return an empty success."""
    findings, stats = vs.validate_manifest(tmp_path / "nope.jsonl")
    assert stats["records"] == 0
    assert any("manifest not found" in f.message for f in findings)


def test_cli_exit_code_is_nonzero_on_error(tmp_path: Path):
    p = tmp_path / "m.jsonl"
    p.write_text(json.dumps(good_record(verification_status="unverified", evidence_grade="A")) + "\n", encoding="utf-8")
    assert vs.main([str(p), "--json"]) == 1


def test_cli_exit_code_zero_on_clean(tmp_path: Path):
    p = tmp_path / "m.jsonl"
    p.write_text(json.dumps(good_record()) + "\n", encoding="utf-8")
    assert vs.main([str(p), "--json"]) == 0


# --- Determinism -------------------------------------------------------------


def test_validation_is_deterministic(tmp_path: Path):
    """Same input must give byte-identical output every run."""
    p = tmp_path / "m.jsonl"
    recs = [good_record(), good_record(source_id="b", doi="10.1234/other", verification_status="abstract_read", evidence_grade="C")]
    p.write_text("\n".join(json.dumps(r) for r in recs) + "\n", encoding="utf-8")
    first = [f.as_dict() for f in vs.validate_manifest(p)[0]]
    second = [f.as_dict() for f in vs.validate_manifest(p)[0]]
    assert first == second


def test_stats_report_content_hash(tmp_path: Path):
    p = tmp_path / "m.jsonl"
    p.write_text(json.dumps(good_record()) + "\n", encoding="utf-8")
    _, stats = vs.validate_manifest(p)
    assert len(stats["sha256"]) == 64


# --- The real manifest must pass --------------------------------------------


def test_repository_manifest_validates():
    """The shipped manifest must satisfy the schema it documents."""
    manifest = Path(__file__).resolve().parent.parent / "sources" / "SOURCE_MANIFEST.jsonl"
    findings, stats = vs.validate_manifest(manifest)
    errors = [f for f in findings if f.level == "error"]
    assert not errors, "\n".join(str(f) for f in errors)
    assert stats["records"] > 0