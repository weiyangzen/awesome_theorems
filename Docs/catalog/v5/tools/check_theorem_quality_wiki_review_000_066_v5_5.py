#!/usr/bin/env python3
"""Independent validator for wiki-review-000-066.json.

This file intentionally does not import either builder.  It replays every
Wikipedia and reference slice directly from the fixed assets, recomputes row
hashes, and only then invokes the builder to check byte determinism.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
AUDIT = REPO / "Docs/catalog/v5/curation/theorem_quality_v5_5"
REVIEW = AUDIT / "reviews/review-000-199.jsonl"
WIKIPEDIA = REPO / "Docs/catalog/v5/sources/wikipedia-en-1000-plus-revisions-20260810.json.gz"
REFERENCES = REPO / "Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json"
OUTPUT = AUDIT / "reviews/wiki-reference-review-000-066.json"
BUILDER = REPO / "Docs/catalog/v5/tools/build_theorem_quality_wiki_review_000_066_v5_5.py"
SUBBUILDERS = [
    REPO / "Docs/catalog/v5/tools/build_theorem_quality_wiki_subreview_000_016_v5_5.py",
    REPO / "Docs/catalog/v5/tools/build_theorem_quality_wiki_subreview_017_065_v5_5.py",
]
SUBREVIEWS = [
    AUDIT / "reviews/wiki-reference-subreview-000-016.json",
    AUDIT / "reviews/wiki-reference-subreview-017-065.json",
]
EXPECTED_INPUT_SHA256 = {
    REVIEW: "9bbaf8db012b5f7283bac1f2362717a27e50ef8178e379992e24a2693dd59052",
    WIKIPEDIA: "73341aebcc1d9d1c577881d2c6d59734ce102d7cc07b1f8ec6d21c9875076d33",
    REFERENCES: "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435",
}
REFERENCE_AUTHORITY_SHA256 = "d428f5659c242fa66c3e78f5497013ea1b6eaf13a4558c4f15e6c0af005acc42"
EXPECTED_INDICES = [
    3, 4, 5, 7, 9, 10, 11, 12, 13, 15, 16,
    17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 33, 35, 36, 37, 38,
    39, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
    59, 60, 61, 63, 64, 65,
]
EXPECTED_COUNTS = {
    "rows": 51,
    "eligible_existing_quality_credit": 30,
    "pending": 15,
    "reject": 6,
    "new_catalog_entries": 0,
    "formal_proofs_claimed": 0,
}
RELEASE_SENTINELS = [
    REPO / "Docs/catalog/v5/Current_Release.json",
    REPO / "Docs/catalog/v5/releases/5.4/Release_Manifest.json",
    REPO / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json",
    REPO / "Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def canonical_row_sha256(row: dict) -> str:
    return canonical_sha256(
        {key: value for key, value in row.items() if key != "row_sha256"}
    )


def utf8_slice(text: str, start: int, end: int) -> str:
    return text.encode("utf-8")[start:end].decode("utf-8")


def validate_passage(binding: dict, pages: dict[int, dict], index: int) -> None:
    page = pages[binding["page_id"]]
    assert binding["page"] == page["resolved_title"], index
    assert binding["revision_id"] == page["revision_id"], index
    field = binding["source_field"]
    text = page[field]
    assert binding["source_field_sha256"] == page[f"{field}_sha256"], index
    passage = binding["passage"]
    assert (
        text[binding["char_start"] : binding["char_end_exclusive"]] == passage
    ), index
    assert (
        utf8_slice(
            text,
            binding["utf8_byte_start"],
            binding["utf8_byte_end_exclusive"],
        )
        == passage
    ), index
    assert sha256(passage.encode("utf-8")) == binding["passage_sha256"], index
    assert len(text[: binding["char_start"]].encode("utf-8")) == binding[
        "utf8_byte_start"
    ], index
    assert len(text[: binding["char_end_exclusive"]].encode("utf-8")) == binding[
        "utf8_byte_end_exclusive"
    ], index


def validate_reference(
    reference: dict,
    statement: dict,
    index: int,
    expected_external_id: str,
    pages: dict[int, dict],
    reference_rows: dict[str, dict],
    rights: dict,
) -> None:
    assert reference["asset_sha256"] == EXPECTED_INPUT_SHA256[REFERENCES], index
    assert reference["authority_sha256"] == REFERENCE_AUTHORITY_SHA256, index
    assert reference["automatic_credit"] is False, index
    assert reference["human_match_performed"] is True, index
    assert reference["bibliographic_identity_human_verified"] is True, index
    assert reference["rights_for_reproduced_material_verified"] is True, index
    assert reference["reproduced_material_rights"] == rights, index
    assert reference["external_fulltext_checked"] is False, index
    assert reference["external_proof_checked"] is False, index
    assert reference["human_match_rationale"].strip(), index

    recorded_parent = reference["record"]
    assert recorded_parent["external_id"] == expected_external_id, index
    parent = reference_rows[expected_external_id]
    assert canonical_row_sha256(parent) == parent["row_sha256"], index
    assert recorded_parent == {
        "external_id": parent["external_id"],
        "source_record_id": parent["source_record_id"],
        "title": parent["title"],
        "row_sha256": parent["row_sha256"],
    }, index

    recorded_candidate = reference["candidate"]
    matches = [
        candidate
        for candidate in parent["reference_candidates"]
        if candidate["row_sha256"] == recorded_candidate["row_sha256"]
    ]
    assert len(matches) == 1, index
    candidate = matches[0]
    assert canonical_row_sha256(candidate) == candidate["row_sha256"], index
    assert candidate["automatic_credit"] is False, index
    for output_key, source_key in {
        "kind": "kind",
        "normalized_identifier": "normalized_identifier",
        "raw_identifier": "raw_identifier",
        "row_sha256": "row_sha256",
        "page": "resolved_title",
        "page_id": "page_id",
        "revision_id": "revision_id",
        "revision_timestamp": "revision_timestamp",
        "mediawiki_revision_sha1": "mediawiki_revision_sha1",
        "wikitext_sha256": "wikitext_sha256",
        "source_locator": "source_locator",
        "context_text": "context_text",
        "context_char_start": "context_char_start",
        "context_char_end_exclusive": "context_char_end_exclusive",
        "context_sha256": "context_sha256",
        "identifier_char_start": "identifier_char_start",
        "identifier_char_end_exclusive": "identifier_char_end_exclusive",
    }.items():
        assert recorded_candidate[output_key] == candidate[source_key], (
            index,
            output_key,
        )

    page = pages[candidate["page_id"]]
    assert candidate["revision_id"] == page["revision_id"], index
    assert candidate["wikitext_sha256"] == page["wikitext_sha256"], index
    assert statement["page_id"] == page["page_id"], index
    assert statement["revision_id"] == page["revision_id"], index
    text = page["wikitext"]
    context = recorded_candidate["context_text"]
    char_start = recorded_candidate["context_char_start"]
    char_end = recorded_candidate["context_char_end_exclusive"]
    byte_start = recorded_candidate["context_utf8_byte_start"]
    byte_end = recorded_candidate["context_utf8_byte_end_exclusive"]
    assert text[char_start:char_end] == context, index
    assert utf8_slice(text, byte_start, byte_end) == context, index
    assert len(text[:char_start].encode("utf-8")) == byte_start, index
    assert len(text[:char_end].encode("utf-8")) == byte_end, index
    assert sha256(context.encode("utf-8")) == recorded_candidate[
        "context_sha256"
    ], index

    identifier_start = recorded_candidate["identifier_char_start"]
    identifier_end = recorded_candidate["identifier_char_end_exclusive"]
    identifier_text = recorded_candidate["identifier_text"]
    identifier_byte_start = recorded_candidate["identifier_utf8_byte_start"]
    identifier_byte_end = recorded_candidate["identifier_utf8_byte_end_exclusive"]
    assert text[identifier_start:identifier_end] == identifier_text, index
    assert (
        utf8_slice(text, identifier_byte_start, identifier_byte_end)
        == identifier_text
    ), index
    assert len(text[:identifier_start].encode("utf-8")) == identifier_byte_start
    assert len(text[:identifier_end].encode("utf-8")) == identifier_byte_end
    assert candidate["raw_identifier"] in identifier_text, index
    assert sha256(identifier_text.encode("utf-8")) == recorded_candidate[
        "identifier_text_sha256"
    ], index


def validate_reference_parent(
    binding: dict, expected_external_id: str, reference_rows: dict[str, dict], index: int
) -> None:
    parent = reference_rows[expected_external_id]
    assert canonical_row_sha256(parent) == parent["row_sha256"], index
    assert binding["asset_sha256"] == EXPECTED_INPUT_SHA256[REFERENCES], index
    assert binding["authority_sha256"] == REFERENCE_AUTHORITY_SHA256, index
    assert binding["external_id"] == expected_external_id, index
    assert binding["source_record_id"] == parent["source_record_id"], index
    assert binding["title"] == parent["title"], index
    assert binding["row_sha256"] == parent["row_sha256"], index
    assert binding["candidate_count"] == len(parent["reference_candidates"]), index
    assert binding["automatic_credit"] is False, index


def main() -> None:
    for path, expected in EXPECTED_INPUT_SHA256.items():
        assert sha256(path.read_bytes()) == expected, path
    protected_before = {
        path: sha256(path.read_bytes()) for path in [REVIEW, *RELEASE_SENTINELS]
    }

    payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    authority = payload["authority_sha256"]
    authority_body = dict(payload)
    del authority_body["authority_sha256"]
    assert canonical_sha256(authority_body) == authority
    assert payload["schema_version"] == (
        "awesome-theorems/wikipedia-reference-existing-quality-review/1.0"
    )
    assert payload["scope"]["source_indices"] == EXPECTED_INDICES
    assert payload["scope"]["credit_scope"] == "existing_catalog_quality_only"
    assert payload["scope"]["release_modified"] is False
    assert payload["counts"] == EXPECTED_COUNTS
    assert payload["reference_authority_sha256"] == REFERENCE_AUTHORITY_SHA256

    parent_rows = [
        json.loads(line)
        for line in REVIEW.read_text(encoding="utf-8").splitlines()
    ]
    parent_by_index = {row["index"]: row for row in parent_rows}
    assert [
        row["index"]
        for row in parent_rows
        if 0 <= row["index"] <= 66 and row["decision"] == "pending"
    ] == EXPECTED_INDICES

    with gzip.open(WIKIPEDIA, "rt", encoding="utf-8") as handle:
        wikipedia = json.load(handle)
    pages = {page["page_id"]: page for page in wikipedia["pages"]}
    reference_asset = json.loads(REFERENCES.read_text(encoding="utf-8"))
    assert reference_asset["authority_sha256"] == REFERENCE_AUTHORITY_SHA256
    assert reference_asset["policy"] == payload["reference_policy"]
    assert reference_asset["policy"]["page_or_identifier_presence_grants_credit"] is False
    assert wikipedia["rights"] == payload["rights"]
    reference_rows = {
        row["external_id"]: row for row in reference_asset["records"]
    }

    records = payload["records"]
    assert [row["index"] for row in records] == EXPECTED_INDICES
    decision_counts = {decision: 0 for decision in ("eligible", "pending", "reject")}
    for row in records:
        index = row["index"]
        decision_counts[row["decision"]] += 1
        expected_external_id = parent_by_index[index]["identity"]["synthetic_source_id"]
        assert row["original_decision"] == "pending", index
        assert row["grants_new_catalog_entry"] is False, index
        assert row["formal_proof_claimed"] is False, index
        eligible = row["decision"] == "eligible"
        assert row["grants_existing_quality_credit"] is eligible, index
        if eligible:
            assert row.get("statement_evidence") is None, index
            validate_passage(row["evidence"], pages, index)
            validate_reference(
                row["reference_evidence"],
                row["evidence"],
                index,
                expected_external_id,
                pages,
                reference_rows,
                wikipedia["rights"],
            )
        else:
            assert row["evidence"] is None, index
            assert row["reference_evidence"] is None, index
            if row.get("statement_evidence") is not None:
                validate_passage(row["statement_evidence"], pages, index)
            if row.get("reference_parent") is not None:
                validate_reference_parent(
                    row["reference_parent"], expected_external_id, reference_rows, index
                )
            inspected = row.get("inspected_source")
            if inspected and inspected.get("page_id") is not None:
                page = pages[inspected["page_id"]]
                assert inspected["revision_id"] == page["revision_id"], index
                if inspected.get("source_field"):
                    field = inspected["source_field"]
                    assert inspected["source_field_sha256"] == page[
                        f"{field}_sha256"
                    ], index

    assert decision_counts == {"eligible": 30, "pending": 15, "reject": 6}
    for path, digest in payload["builders"].items():
        assert sha256((REPO / path).read_bytes()) == digest
    for path, digest in payload["subreviews"].items():
        assert sha256((REPO / path).read_bytes()) == digest

    before = OUTPUT.read_bytes()
    subprocess.run(
        [sys.executable, str(BUILDER)],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    after = OUTPUT.read_bytes()
    assert after == before, "combined builder is not byte-deterministic"
    protected_after = {
        path: sha256(path.read_bytes()) for path in [REVIEW, *RELEASE_SENTINELS]
    }
    assert protected_after == protected_before, "builder modified review or release authority"
    print(
        json.dumps(
            {
                "validated": str(OUTPUT),
                "sha256": sha256(after),
                "authority_sha256": authority,
                **EXPECTED_COUNTS,
                "deterministic_rebuild": True,
                "release_and_parent_review_unchanged": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
