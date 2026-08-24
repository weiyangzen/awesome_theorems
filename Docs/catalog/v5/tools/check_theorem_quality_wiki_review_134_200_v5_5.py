#!/usr/bin/env python3
"""Independent validator for the 134..200 Wikipedia/reference range review.

This checker intentionally does not import the builder.  It replays parent
identity, pinned passages, reference contexts, OpenAlex DOI joins, row hashes,
decision sets, inventory sentinels, and the zero-new-credit boundary directly
from repository-owned inputs.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
AUDIT = REPO / "Docs/catalog/v5/curation/theorem_quality_v5_5"
LEDGER = AUDIT / "landmark-ledger-0-1199.json"
WIKIPEDIA = REPO / "Docs/catalog/v5/sources/wikipedia-en-1000-plus-revisions-20260810.json.gz"
REFERENCES = REPO / "Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json"
OPENALEX = REPO / "Docs/catalog/v5/sources/openalex-thousand-plus-doi-metadata-20260810.json.gz"
DEFAULT_ARTIFACT = AUDIT / "range_reviews/wiki-reference-review-134-200.json"
BUILDER = REPO / "Docs/catalog/v5/tools/build_theorem_quality_wiki_review_134_200_v5_5.py"

FIXED_INPUT_SHA256 = {
    LEDGER: "51c5607cd4289f8340745879b8b134673bbd44e873cebc82e2da59f0ba6c1471",
    WIKIPEDIA: "73341aebcc1d9d1c577881d2c6d59734ce102d7cc07b1f8ec6d21c9875076d33",
    REFERENCES: "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435",
    OPENALEX: "e3d490619eac4e16bdf24478c74de2024d32d3ec0d603f3ac4a102ad4c206486",
}
LEDGER_AUTHORITY_SHA256 = "2cc91efdcbd604f46fd7a4f59ca9f19b25a74fdabd5e829fc7a6c50e5c7bf844"
REFERENCE_AUTHORITY_SHA256 = "d428f5659c242fa66c3e78f5497013ea1b6eaf13a4558c4f15e6c0af005acc42"
OPENALEX_AUTHORITY_SHA256 = "4a6abb7d9f22dbca688eed164116b429beacb15a643465bf424f41d0e0e3f565"

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

EXPECTED_PENDING = [
    135, 136, 137, 138, 139, 140, 141, 142, 143, 145, 146, 147, 148,
    149, 150, 151, 152, 153, 155, 156, 157, 158, 159, 160, 161, 165,
    167, 168, 169, 171, 172, 173, 174, 176, 177, 179, 180, 182, 183,
    184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196,
    197, 199,
]
EXPECTED_DECISION_SETS = {
    "eligible": [136, 137, 138, 141, 142, 147, 148, 149, 150, 153, 156, 158,
                 160, 161, 165, 167, 168, 169, 173, 174, 179, 180, 182, 183,
                 184, 185, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196,
                 197, 199],
    "pending": [135, 139, 140, 143, 146, 152, 155, 172, 176, 177, 186],
    "reject": [145, 151, 157, 159, 171],
}
EXPECTED_COUNTS = {
    "rows": 54,
    "eligible_existing_quality_credit": 38,
    "pending": 11,
    "reject": 5,
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


def utf8_slice(text: str, start: int, end: int) -> str:
    return text.encode("utf-8")[start:end].decode("utf-8")


def validate_statement(binding: dict, page: dict, index: int) -> None:
    assert binding["asset"] == rel(WIKIPEDIA), index
    assert binding["asset_sha256"] == FIXED_INPUT_SHA256[WIKIPEDIA], index
    assert binding["source_field"] == "wikitext", index
    assert binding["source_field_sha256"] == page["wikitext_sha256"], index
    for key in ("page_id", "revision_id", "revision_timestamp", "mediawiki_revision_sha1", "attribution_url"):
        expected_key = "page_id" if key == "page_id" else key
        assert binding[key] == page[expected_key], (index, key)
    assert binding["page"] == page["resolved_title"], index
    text = page["wikitext"]
    cs, ce = binding["char_start"], binding["char_end_exclusive"]
    bs, be = binding["utf8_byte_start"], binding["utf8_byte_end_exclusive"]
    passage = binding["passage"]
    assert text[cs:ce] == passage, index
    assert utf8_slice(text, bs, be) == passage, index
    assert len(text[:cs].encode("utf-8")) == bs, index
    assert len(text[:ce].encode("utf-8")) == be, index
    assert sha256(passage.encode("utf-8")) == binding["passage_sha256"], index
    assert binding["completeness"].strip(), index
    assert len(passage.strip()) >= 100, index


def validate_reference(
    binding: dict,
    page: dict,
    parent: dict,
    reference_parent: dict,
    openalex_by_doi: dict[str, dict],
    rights: dict,
    index: int,
) -> None:
    assert binding["asset"] == rel(REFERENCES), index
    assert binding["asset_sha256"] == FIXED_INPUT_SHA256[REFERENCES], index
    assert binding["authority_sha256"] == REFERENCE_AUTHORITY_SHA256, index
    assert binding["automatic_credit"] is False, index
    assert binding["human_match_performed"] is True, index
    assert binding["bibliographic_identity_human_verified"] is True, index
    assert binding["rights_for_reproduced_material_verified"] is True, index
    assert binding["external_fulltext_checked"] is False, index
    assert binding["external_proof_checked"] is False, index
    assert binding["reproduced_material_rights"] == rights, index
    assert binding["human_match_rationale"].strip(), index
    assert binding["record"] == {
        "external_id": reference_parent["external_id"],
        "source_record_id": reference_parent["source_record_id"],
        "title": reference_parent["title"],
        "row_sha256": reference_parent["row_sha256"],
    }, index
    assert reference_parent["source_record_id"] == parent["source_record_id"], index

    recorded = binding["candidate"]
    matches = [candidate for candidate in reference_parent["reference_candidates"]
               if candidate["row_sha256"] == recorded["row_sha256"]]
    assert len(matches) == 1, index
    candidate = matches[0]
    assert canonical_row_sha256(candidate) == candidate["row_sha256"], index
    assert candidate["automatic_credit"] is False, index
    source_map = {
        "kind": "kind", "normalized_identifier": "normalized_identifier",
        "raw_identifier": "raw_identifier", "row_sha256": "row_sha256",
        "page": "resolved_title", "page_id": "page_id", "revision_id": "revision_id",
        "revision_timestamp": "revision_timestamp",
        "mediawiki_revision_sha1": "mediawiki_revision_sha1",
        "wikitext_sha256": "wikitext_sha256", "source_locator": "source_locator",
        "context_text": "context_text", "context_char_start": "context_char_start",
        "context_char_end_exclusive": "context_char_end_exclusive",
        "context_sha256": "context_sha256",
        "identifier_char_start": "identifier_char_start",
        "identifier_char_end_exclusive": "identifier_char_end_exclusive",
    }
    for output_key, source_key in source_map.items():
        assert recorded[output_key] == candidate[source_key], (index, output_key)
    assert candidate["page_id"] == page["page_id"], index
    assert candidate["revision_id"] == page["revision_id"], index
    text = page["wikitext"]
    cs, ce = recorded["context_char_start"], recorded["context_char_end_exclusive"]
    cbs, cbe = recorded["context_utf8_byte_start"], recorded["context_utf8_byte_end_exclusive"]
    context = recorded["context_text"]
    assert text[cs:ce] == context, index
    assert utf8_slice(text, cbs, cbe) == context, index
    assert len(text[:cs].encode("utf-8")) == cbs, index
    assert len(text[:ce].encode("utf-8")) == cbe, index
    assert sha256(context.encode("utf-8")) == recorded["context_sha256"], index
    ids, ide = recorded["identifier_char_start"], recorded["identifier_char_end_exclusive"]
    ibs, ibe = recorded["identifier_utf8_byte_start"], recorded["identifier_utf8_byte_end_exclusive"]
    identifier_text = recorded["identifier_text"]
    assert text[ids:ide] == identifier_text, index
    assert utf8_slice(text, ibs, ibe) == identifier_text, index
    assert len(text[:ids].encode("utf-8")) == ibs, index
    assert len(text[:ide].encode("utf-8")) == ibe, index
    assert candidate["raw_identifier"] in identifier_text, index
    assert sha256(identifier_text.encode("utf-8")) == recorded["identifier_text_sha256"], index

    oa_binding = binding["openalex_metadata"]
    if candidate["kind"] == "doi":
        assert oa_binding is not None, index
        assert oa_binding["asset"] == rel(OPENALEX), index
        assert oa_binding["asset_sha256"] == FIXED_INPUT_SHA256[OPENALEX], index
        assert oa_binding["authority_sha256"] == OPENALEX_AUTHORITY_SHA256, index
        assert oa_binding["join_key"] == candidate["normalized_identifier"], index
        expected_oa = openalex_by_doi[candidate["normalized_identifier"]]
        assert canonical_row_sha256(expected_oa) == expected_oa["row_sha256"], index
        assert oa_binding["record"] == expected_oa, index
        assert oa_binding["bibliographic_metadata_only"] is True, index
        assert oa_binding["quality_credit_granted"] is False, index
        assert oa_binding["supports_exact_theorem_statement_verified"] is False, index
        assert expected_oa["evidence_boundary"]["quality_credit_granted"] is False, index
    else:
        assert candidate["kind"] == "isbn", index
        assert oa_binding is None, index


def validate(artifact: Path) -> dict:
    for path, expected in {**FIXED_INPUT_SHA256, **RELEASE_SENTINELS}.items():
        assert sha256(path.read_bytes()) == expected, path
    protected_before = {path: sha256(path.read_bytes()) for path in RELEASE_SENTINELS}

    raw = artifact.read_bytes()
    assert b"/tmp/" not in raw and b"/home/" not in raw
    payload = json.loads(raw)
    authority = payload["authority_sha256"]
    body = dict(payload)
    del body["authority_sha256"]
    assert canonical_sha256(body) == authority
    assert payload["schema_version"] == "awesome-theorems/wikipedia-reference-range-review/1.0"
    assert payload["scope"] == {
        "source_index_range": [134, 200],
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
    assert payload["release_boundary"]["theorem_status_records"] == 2500
    assert payload["release_boundary"]["effective_strict_conjecture_credits"] == 1000
    assert payload["release_boundary"]["open_problem_records"] == 599
    assert payload["release_boundary"]["review_changes_inventory_counts"] is False
    assert payload["release_boundary"]["protected_file_sha256"] == {
        rel(path): digest for path, digest in RELEASE_SENTINELS.items()
    }

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert ledger["authority_sha256"] == LEDGER_AUTHORITY_SHA256
    parent_by_index = {row["source_index"]: row for row in ledger["records"]}
    assert [row["source_index"] for row in ledger["records"]
            if 134 <= row["source_index"] <= 200 and row["review_disposition"] == "pending"] == EXPECTED_PENDING
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
    decision_by_index = {
        index: decision for decision, indices in EXPECTED_DECISION_SETS.items() for index in indices
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
        assert row["decision"] == decision_by_index[index], index
        assert row["grants_existing_quality_credit"] is (row["decision"] == "eligible"), index
        for forbidden in (
            "grants_new_catalog_entry", "grants_new_release_theorem_credit",
            "grants_strict_conjecture_credit", "formal_proof_claimed", "external_proof_checked",
        ):
            assert row[forbidden] is False, (index, forbidden)

        boundary = row["existing_parent_boundary"]
        assert boundary == {
            "base_ledger_path": rel(LEDGER),
            "base_ledger_sha256": FIXED_INPUT_SHA256[LEDGER],
            "base_ledger_authority_sha256": LEDGER_AUTHORITY_SHA256,
            "base_record_canonical_sha256": canonical_sha256(parent),
            "base_source_row_sha256": parent["source_row_sha256"],
            "base_source_review_record_canonical_sha256": parent["source_review_record_canonical_sha256"],
            "base_reference_row_sha256": parent["reference_candidate_entry"]["asset_row_sha256"],
            "base_existing_quality_credit": False,
            "base_new_release_theorem_credit": False,
            "overlay_only": True,
            "creates_identity": False,
            "creates_family": False,
            "reopens_parent_dedupe": False,
            "semantic_key": parent["source_review_record"]["dedupe"]["semantic_key"],
        }, index

        resolution = resolution_by_source[parent["source_record_id"]]
        assert canonical_row_sha256(resolution) == resolution["row_sha256"], index
        assert resolution["source_row_sha256"] == parent["source_row_sha256"], index
        expected_page_bindings = []
        for page_id in resolution["resolved_page_ids"]:
            page = pages[page_id]
            expected_page_bindings.append({
                "page": page["resolved_title"], "page_id": page_id,
                "revision_id": page["revision_id"],
                "revision_timestamp": page["revision_timestamp"],
                "mediawiki_revision_sha1": page["mediawiki_revision_sha1"],
                "wikitext_sha256": page["wikitext_sha256"],
                "attribution_url": page["attribution_url"],
            })
        assert row["wikipedia_revision_bindings"] == expected_page_bindings, index
        assert len(expected_page_bindings) == 1, index
        page = pages[expected_page_bindings[0]["page_id"]]

        reference_parent = reference_by_source[parent["source_record_id"]]
        assert canonical_row_sha256(reference_parent) == reference_parent["row_sha256"], index
        assert row["reference_parent_boundary"] == {
            "asset": rel(REFERENCES),
            "asset_sha256": FIXED_INPUT_SHA256[REFERENCES],
            "authority_sha256": REFERENCE_AUTHORITY_SHA256,
            "row_sha256": reference_parent["row_sha256"],
            "candidate_count": len(reference_parent["reference_candidates"]),
            "automatic_credit": False,
        }, index

        if row["decision"] == "eligible":
            assert row["blockers"] == [], index
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
