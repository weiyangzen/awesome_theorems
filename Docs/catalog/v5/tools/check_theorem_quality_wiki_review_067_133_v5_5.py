#!/usr/bin/env python3
"""Independently validate the fixed-source theorem review for indices 67..133."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys


REPO = Path(__file__).resolve().parents[4]
AUDIT = REPO / "Docs/catalog/v5/curation/theorem_quality_v5_5"
LEDGER = AUDIT / "landmark-ledger-0-1199.json"
WIKIPEDIA = REPO / "Docs/catalog/v5/sources/wikipedia-en-1000-plus-revisions-20260810.json.gz"
REFERENCES = REPO / "Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json"
OPENALEX = REPO / "Docs/catalog/v5/sources/openalex-thousand-plus-doi-metadata-20260810.json.gz"
BUILDER = REPO / "Docs/catalog/v5/tools/build_theorem_quality_wiki_review_067_133_v5_5.py"
DEFAULT_ARTIFACT = AUDIT / "reviews/wiki-reference-review-067-133.json"

EXPECTED_FILE_SHA256 = {
    LEDGER: "51c5607cd4289f8340745879b8b134673bbd44e873cebc82e2da59f0ba6c1471",
    WIKIPEDIA: "73341aebcc1d9d1c577881d2c6d59734ce102d7cc07b1f8ec6d21c9875076d33",
    REFERENCES: "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435",
    OPENALEX: "e3d490619eac4e16bdf24478c74de2024d32d3ec0d603f3ac4a102ad4c206486",
    BUILDER: "2b5cf737a739e4201c29aef95af5b9e3d313bc1361ffd8ac43836426d1dc2db3",
}
RELEASE_SENTINELS = {
    REPO / "Docs/catalog/v5/Current_Release.json":
        "261f27d39f379a879ea0fcacbab9e3c43dc5be8d83ea56473b2e8b4e6c384795",
    REPO / "Docs/catalog/v5/releases/5.4/Release_Manifest.json":
        "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9",
    REPO / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json":
        "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
    REPO / "Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json":
        "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3",
}
LEDGER_AUTHORITY_SHA256 = "2cc91efdcbd604f46fd7a4f59ca9f19b25a74fdabd5e829fc7a6c50e5c7bf844"
REFERENCE_AUTHORITY_SHA256 = "d428f5659c242fa66c3e78f5497013ea1b6eaf13a4558c4f15e6c0af005acc42"
OPENALEX_AUTHORITY_SHA256 = "4a6abb7d9f22dbca688eed164116b429beacb15a643465bf424f41d0e0e3f565"
ARTIFACT_SHA256 = "a6274527790ff89f530325f35470cebda742ae0c4dc740ee48d70e4b9e60daa0"
ARTIFACT_AUTHORITY_SHA256 = "c6717771eda15518389f5917fefa34f2a7fcfa1ca9843dfa96d70c3cfb60e764"

EXPECTED_PENDING = [
    69, 70, 71, 72, 73, 74, 75, 76, 79, 80, 82, 84, 85, 87, 88, 89,
    90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 104, 105, 106,
    107, 108, 109, 110, 112, 115, 117, 118, 119, 120, 121, 122, 123,
    124, 125, 126, 127, 128, 129, 132, 133,
]
EXPECTED_DECISION_SETS = {
    "eligible": [
        69, 75, 76, 79, 80, 82, 84, 85, 88, 89, 91, 93, 96, 97, 98,
        99, 106, 107, 109, 117, 118, 125, 126, 127, 128, 132, 133,
    ],
    "pending": [
        70, 71, 72, 73, 74, 87, 90, 92, 94, 95, 100, 101, 104, 110,
        112, 115, 119, 120, 121,
    ],
    "reject": [105, 108, 122, 123, 124, 129],
}
EXPECTED_COUNTS = {
    "rows": 52,
    "eligible_existing_quality_credit": 27,
    "pending": 19,
    "reject": 6,
    "new_catalog_entries": 0,
    "new_release_theorem_credits": 0,
    "strict_conjecture_credits": 0,
    "formal_proofs_claimed": 0,
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8"))


def canonical_row_sha256(row: dict) -> str:
    return canonical_sha256({key: value for key, value in row.items() if key != "row_sha256"})


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def validate_statement(evidence: dict, page: dict, index: int) -> None:
    assert evidence["asset"] == rel(WIKIPEDIA), index
    assert evidence["asset_sha256"] == EXPECTED_FILE_SHA256[WIKIPEDIA], index
    field = evidence["source_field"]
    assert field in {"extract", "wikitext"}, index
    text = page[field]
    assert evidence["source_field_sha256"] == page[f"{field}_sha256"], index
    cs, ce = evidence["char_start"], evidence["char_end_exclusive"]
    bs, be = evidence["utf8_byte_start"], evidence["utf8_byte_end_exclusive"]
    passage = evidence["passage"]
    assert 0 <= cs < ce <= len(text), index
    assert text[cs:ce] == passage, index
    assert len(text[:cs].encode("utf-8")) == bs, index
    assert len(text[:ce].encode("utf-8")) == be, index
    assert text.encode("utf-8")[bs:be].decode("utf-8") == passage, index
    assert sha256(passage.encode("utf-8")) == evidence["passage_sha256"], index
    assert evidence["page_id"] == page["page_id"], index
    assert evidence["page"] == page["resolved_title"], index
    assert evidence["revision_id"] == page["revision_id"], index
    assert evidence["revision_timestamp"] == page["revision_timestamp"], index
    assert evidence["mediawiki_revision_sha1"] == page["mediawiki_revision_sha1"], index
    assert evidence["attribution_url"] == page["attribution_url"], index
    assert evidence["completeness"].strip(), index
    if evidence["selection"] == "full_revision_pinned_extract":
        assert field == "extract" and cs == 0 and ce == len(text), index
    else:
        assert evidence["selection"] == "reviewed_contiguous_theorem_passage", index


def validate_reference(
    evidence: dict, page: dict, parent: dict, reference_parent: dict,
    openalex_by_doi: dict[str, dict], rights: dict, index: int,
) -> None:
    assert evidence["asset"] == rel(REFERENCES), index
    assert evidence["asset_sha256"] == EXPECTED_FILE_SHA256[REFERENCES], index
    assert evidence["authority_sha256"] == REFERENCE_AUTHORITY_SHA256, index
    assert evidence["automatic_credit"] is False, index
    assert evidence["human_match_performed"] is True, index
    assert evidence["bibliographic_identity_human_verified"] is True, index
    assert evidence["human_match_rationale"].strip(), index
    assert evidence["external_fulltext_checked"] is False, index
    assert evidence["external_proof_checked"] is False, index
    assert evidence["rights_for_reproduced_material_verified"] is True, index
    assert evidence["reproduced_material_rights"] == rights, index
    record = evidence["record"]
    assert record == {
        "external_id": reference_parent["external_id"],
        "source_record_id": reference_parent["source_record_id"],
        "title": reference_parent["title"],
        "row_sha256": reference_parent["row_sha256"],
    }, index
    assert record["source_record_id"] == parent["source_record_id"], index

    recorded = evidence["candidate"]
    matches = [
        candidate for candidate in reference_parent["reference_candidates"]
        if candidate["kind"] == recorded["kind"]
        and candidate["normalized_identifier"] == recorded["normalized_identifier"]
    ]
    assert len(matches) == 1, index
    candidate = matches[0]
    assert canonical_row_sha256(candidate) == candidate["row_sha256"], index
    assert recorded["row_sha256"] == candidate["row_sha256"], index
    assert recorded["raw_identifier"] == candidate["raw_identifier"], index
    assert recorded["page_id"] == candidate["page_id"] == page["page_id"], index
    assert recorded["page"] == candidate["resolved_title"] == page["resolved_title"], index
    assert recorded["revision_id"] == candidate["revision_id"] == page["revision_id"], index
    assert recorded["revision_timestamp"] == candidate["revision_timestamp"], index
    assert recorded["mediawiki_revision_sha1"] == candidate["mediawiki_revision_sha1"], index
    assert recorded["wikitext_sha256"] == candidate["wikitext_sha256"] == page["wikitext_sha256"], index
    assert recorded["source_locator"] == candidate["source_locator"], index
    text = page["wikitext"]
    cs, ce = recorded["context_char_start"], recorded["context_char_end_exclusive"]
    bs, be = recorded["context_utf8_byte_start"], recorded["context_utf8_byte_end_exclusive"]
    assert text[cs:ce] == recorded["context_text"] == candidate["context_text"], index
    assert len(text[:cs].encode("utf-8")) == bs, index
    assert len(text[:ce].encode("utf-8")) == be, index
    assert sha256(recorded["context_text"].encode("utf-8")) == recorded["context_sha256"] == candidate["context_sha256"], index
    ids, ide = recorded["identifier_char_start"], recorded["identifier_char_end_exclusive"]
    ibs, ibe = recorded["identifier_utf8_byte_start"], recorded["identifier_utf8_byte_end_exclusive"]
    identifier_text = text[ids:ide]
    assert identifier_text == recorded["identifier_text"], index
    assert len(text[:ids].encode("utf-8")) == ibs, index
    assert len(text[:ide].encode("utf-8")) == ibe, index
    assert candidate["raw_identifier"] in identifier_text, index
    assert sha256(identifier_text.encode("utf-8")) == recorded["identifier_text_sha256"], index

    metadata = evidence["openalex_metadata"]
    if candidate["kind"] == "doi":
        oa = openalex_by_doi[candidate["normalized_identifier"]]
        assert canonical_row_sha256(oa) == oa["row_sha256"], index
        assert metadata["asset"] == rel(OPENALEX), index
        assert metadata["asset_sha256"] == EXPECTED_FILE_SHA256[OPENALEX], index
        assert metadata["authority_sha256"] == OPENALEX_AUTHORITY_SHA256, index
        assert metadata["join_key"] == candidate["normalized_identifier"], index
        assert metadata["record"] == oa, index
        assert metadata["bibliographic_metadata_only"] is True, index
        assert metadata["quality_credit_granted"] is False, index
        assert metadata["supports_exact_theorem_statement_verified"] is False, index
    else:
        assert metadata is None, index


def validate(artifact: Path) -> dict:
    for path, expected in {**EXPECTED_FILE_SHA256, **RELEASE_SENTINELS}.items():
        assert sha256(path.read_bytes()) == expected, path
    protected_before = {path: sha256(path.read_bytes()) for path in RELEASE_SENTINELS}
    raw = artifact.read_bytes()
    if artifact.resolve() == DEFAULT_ARTIFACT.resolve():
        assert sha256(raw) == ARTIFACT_SHA256
    assert raw.endswith(b"\n")
    assert b"/tmp/" not in raw and b"/home/" not in raw
    payload = json.loads(raw)
    authority = payload["authority_sha256"]
    body = dict(payload)
    del body["authority_sha256"]
    assert authority == canonical_sha256(body)
    if artifact.resolve() == DEFAULT_ARTIFACT.resolve():
        assert authority == ARTIFACT_AUTHORITY_SHA256
    assert payload["schema_version"] == "awesome-theorems/wikipedia-reference-range-review/1.0"
    assert payload["artifact_path"] == rel(DEFAULT_ARTIFACT)
    assert payload["scope"] == {
        "source_index_range": [67, 133],
        "reviewed_parent_pending_indices": EXPECTED_PENDING,
        "credit_scope": "existing_catalog_quality_only",
        "base_ledger_is_frozen": True,
        "existing_parent_overlay_only": True,
        "not_a_release_append": True,
        "release_modified": False,
        "new_catalog_entries_granted": False,
        "new_release_theorem_credits_granted": False,
        "strict_conjecture_credits_granted": False,
    }
    assert payload["decision_sets"] == EXPECTED_DECISION_SETS
    assert payload["counts"] == EXPECTED_COUNTS
    assert payload["release_boundary"] == {
        "release": "5.4",
        "protected_file_sha256": {rel(path): digest for path, digest in RELEASE_SENTINELS.items()},
        "theorem_status_records": 2500,
        "effective_strict_conjecture_credits": 1000,
        "open_problem_records": 599,
        "review_changes_inventory_counts": False,
    }

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert ledger["authority_sha256"] == LEDGER_AUTHORITY_SHA256
    parent_by_index = {row["source_index"]: row for row in ledger["records"]}
    assert [
        row["source_index"] for row in ledger["records"]
        if 67 <= row["source_index"] <= 133 and row["review_disposition"] == "pending"
    ] == EXPECTED_PENDING
    with gzip.open(WIKIPEDIA, "rt", encoding="utf-8") as stream:
        wikipedia = json.load(stream)
    pages = {row["page_id"]: row for row in wikipedia["pages"]}
    resolution_by_source = {row["source_record_id"]: row for row in wikipedia["identity_resolution"]}
    references = json.loads(REFERENCES.read_text(encoding="utf-8"))
    assert references["authority_sha256"] == REFERENCE_AUTHORITY_SHA256
    assert references["policy"] == payload["reference_policy"]
    assert references["policy"]["page_or_identifier_presence_grants_credit"] is False
    reference_by_source = {row["source_record_id"]: row for row in references["records"]}
    with gzip.open(OPENALEX, "rt", encoding="utf-8") as stream:
        openalex = json.load(stream)
    assert openalex["authority_sha256"] == OPENALEX_AUTHORITY_SHA256
    assert openalex["policy"] == payload["openalex_policy"]
    assert openalex["policy"]["openalex_metadata_grants_theorem_support_credit"] is False
    openalex_by_doi = {row["normalized_doi"]: row for row in openalex["records"]}

    records = payload["records"]
    assert [row["source_index"] for row in records] == EXPECTED_PENDING
    assert canonical_sha256(records) == payload["records_canonical_sha256"]
    expected_by_index = {
        index: decision
        for decision, indices in EXPECTED_DECISION_SETS.items()
        for index in indices
    }
    for row in records:
        index = row["source_index"]
        assert canonical_row_sha256(row) == row["row_sha256"], index
        parent = parent_by_index[index]
        assert row["source_record_id"] == parent["source_record_id"], index
        assert row["external_id"] == parent["external_id"], index
        assert row["title"] == parent["title"], index
        assert row["msc2020"] == parent["msc2020"], index
        assert row["original_review_disposition"] == "pending", index
        assert row["decision"] == expected_by_index[index], index
        assert row["grants_existing_quality_credit"] is (row["decision"] == "eligible"), index
        for forbidden in (
            "grants_new_catalog_entry", "grants_new_release_theorem_credit",
            "grants_strict_conjecture_credit", "formal_proof_claimed",
            "external_proof_checked",
        ):
            assert row[forbidden] is False, (index, forbidden)
        resolution = resolution_by_source[parent["source_record_id"]]
        assert canonical_row_sha256(resolution) == resolution["row_sha256"], index
        assert resolution["source_row_sha256"] == parent["source_row_sha256"], index
        expected_bindings = [{
            "page": pages[page_id]["resolved_title"],
            "page_id": page_id,
            "revision_id": pages[page_id]["revision_id"],
            "revision_timestamp": pages[page_id]["revision_timestamp"],
            "mediawiki_revision_sha1": pages[page_id]["mediawiki_revision_sha1"],
            "wikitext_sha256": pages[page_id]["wikitext_sha256"],
            "extract_sha256": pages[page_id]["extract_sha256"],
            "attribution_url": pages[page_id]["attribution_url"],
        } for page_id in resolution["resolved_page_ids"]]
        assert row["wikipedia_revision_bindings"] == expected_bindings, index

        reference_parent = reference_by_source[parent["source_record_id"]]
        assert canonical_row_sha256(reference_parent) == reference_parent["row_sha256"], index
        assert row["existing_parent_boundary"] == {
            "base_ledger_path": rel(LEDGER),
            "base_ledger_sha256": EXPECTED_FILE_SHA256[LEDGER],
            "base_ledger_authority_sha256": LEDGER_AUTHORITY_SHA256,
            "base_record_canonical_sha256": canonical_sha256(parent),
            "base_source_row_sha256": parent["source_row_sha256"],
            "base_source_review_record_canonical_sha256": parent["source_review_record_canonical_sha256"],
            "base_reference_row_sha256": reference_parent["row_sha256"],
            "base_existing_quality_credit": False,
            "base_new_release_theorem_credit": False,
            "overlay_only": True,
            "creates_identity": False,
            "creates_family": False,
            "reopens_parent_dedupe": False,
            "semantic_key": parent["source_review_record"]["dedupe"]["semantic_key"],
        }, index
        assert row["reference_parent_boundary"] == {
            "asset": rel(REFERENCES),
            "asset_sha256": EXPECTED_FILE_SHA256[REFERENCES],
            "authority_sha256": REFERENCE_AUTHORITY_SHA256,
            "row_sha256": reference_parent["row_sha256"],
            "candidate_count": len(reference_parent["reference_candidates"]),
            "automatic_credit": False,
        }, index

        if row["decision"] == "eligible":
            assert row["blockers"] == [], index
            assert len(resolution["resolved_page_ids"]) == 1, index
            page = pages[resolution["resolved_page_ids"][0]]
            validate_statement(row["statement_evidence"], page, index)
            validate_reference(
                row["reference_evidence"], page, parent, reference_parent,
                openalex_by_doi, wikipedia["rights"], index,
            )
        else:
            assert row["statement_evidence"] is None, index
            assert row["reference_evidence"] is None, index
            assert row["blockers"] == [row["reason_code"]], index
            assert row["rationale"].strip(), index

    manifest = json.loads((REPO / "Docs/catalog/v5/releases/5.4/Release_Manifest.json").read_text(encoding="utf-8"))
    assert manifest["counts"]["cumulative_theorems"] == 2500
    assert manifest["counts"]["effective_strict_conjecture_credits"] == 1000
    strict = json.loads((REPO / "Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json").read_text(encoding="utf-8"))
    assert strict["counts"]["effective_strict_credits"] == 1000

    deterministic = False
    if artifact.resolve() == DEFAULT_ARTIFACT.resolve():
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--check"], cwd=REPO,
            text=True, capture_output=True, check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        deterministic = True
    protected_after = {path: sha256(path.read_bytes()) for path in RELEASE_SENTINELS}
    assert protected_after == protected_before
    return {
        "overall_pass": True,
        "artifact": str(artifact),
        "artifact_sha256": sha256(raw),
        "authority_sha256": authority,
        "deterministic_rebuild": deterministic,
        **EXPECTED_COUNTS,
        "release_theorems": 2500,
        "release_strict_conjectures": 1000,
        "release_open_problems": 599,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args()
    print(json.dumps(validate(args.artifact), sort_keys=True))


if __name__ == "__main__":
    main()
