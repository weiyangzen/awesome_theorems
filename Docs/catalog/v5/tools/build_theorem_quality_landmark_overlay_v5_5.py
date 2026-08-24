#!/usr/bin/env python3
"""Build the non-release landmark quality overlay and its 1,200-row aggregate."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[4]
CURATION_REL = Path("Docs/catalog/v5/curation/theorem_quality_v5_5")
BASE_REL = CURATION_REL / "landmark-ledger-0-1199.json"
REVIEW_REL = CURATION_REL / "reviews/wiki-reference-review-000-066.json"
OVERLAY_REL = CURATION_REL / "landmark-overlay-000-066.json"
AGGREGATE_REL = CURATION_REL / "landmark-ledger-0-1199-overlay-000-066.json"
MANIFEST_REL = Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json")

BASE_SHA256 = "51c5607cd4289f8340745879b8b134673bbd44e873cebc82e2da59f0ba6c1471"
REVIEW_SHA256 = "ab7fcefbc7618dfb42770307475342974340c845310d03e4988328620b35559d"
REVIEW_AUTHORITY_SHA256 = "64de172f15ec4518f3409dc6d4cc699abfa009004c3ca4a856f899a628b1352b"
MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], field: str) -> str:
    return sha256(canonical({key: item for key, item in value.items() if key != field}))


def normalize_decision(value: str) -> str:
    if value in {"eligible", "eligible_existing_quality_credit"}:
        return "eligible_existing_quality_credit"
    if value in {"pending", "reject"}:
        return value
    raise AssertionError(f"unknown decision {value!r}")


def load_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    expected = {
        BASE_REL: BASE_SHA256,
        REVIEW_REL: REVIEW_SHA256,
        MANIFEST_REL: MANIFEST_SHA256,
    }
    for relative, digest in expected.items():
        if file_sha256(ROOT / relative) != digest:
            raise AssertionError(f"fixed input hash mismatch: {relative}")
    base = json.loads((ROOT / BASE_REL).read_text(encoding="utf-8"))
    review = json.loads((ROOT / REVIEW_REL).read_text(encoding="utf-8"))
    if review["authority_sha256"] != REVIEW_AUTHORITY_SHA256:
        raise AssertionError("review authority mismatch")
    if base["counts"]["existing_quality_credits"] != 439:
        raise AssertionError("unexpected base quality count")
    if review["counts"] != {
        "eligible_existing_quality_credit": 30,
        "formal_proofs_claimed": 0,
        "new_catalog_entries": 0,
        "pending": 15,
        "reject": 6,
        "rows": 51,
    }:
        raise AssertionError("unexpected review counts")
    return base, review


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    base, review = load_inputs()
    base_records = base["records"]
    if len(base_records) != 1200 or [row["source_index"] for row in base_records] != list(range(1200)):
        raise AssertionError("base ledger coverage mismatch")

    review_by_index = {row["index"]: row for row in review["records"]}
    if len(review_by_index) != 51:
        raise AssertionError("overlay review index collision")
    overlay_records: list[dict[str, Any]] = []
    for index in review["scope"]["source_indices"]:
        source = base_records[index]
        evidence = review_by_index[index]
        if source["review_disposition"] != "pending" or source["grants_existing_quality_credit"]:
            raise AssertionError(f"overlay source was not pending at {index}")
        if source["title"] != evidence["title"]:
            raise AssertionError(f"overlay title mismatch at {index}")
        if evidence["decision"] == "eligible" and (
            source["external_id"]
            != evidence["reference_evidence"]["record"]["external_id"]
        ):
            raise AssertionError(f"overlay external identity mismatch at {index}")
        disposition = normalize_decision(evidence["decision"])
        grants_quality = disposition == "eligible_existing_quality_credit"
        row: dict[str, Any] = {
            "source_index": index,
            "source_record_id": source["source_record_id"],
            "external_id": source["external_id"],
            "title": source["title"],
            "base_review_disposition": "pending",
            "overlay_review_disposition": disposition,
            "base_existing_quality_credit": False,
            "grants_existing_quality_credit": grants_quality,
            "existing_quality_credit_delta": 1 if grants_quality else 0,
            "grants_new_release_theorem_credit": False,
            "formal_proof_claimed": False,
            "review_record_canonical_sha256": sha256(canonical(evidence)),
            "review_evidence_boundary": {
                "exact_wikipedia_statement_verified": (
                    evidence.get("evidence") is not None
                    or evidence.get("statement_evidence") is not None
                ),
                "manual_reference_match_verified": evidence.get("reference_evidence") is not None,
                "automatic_reference_credit": False,
                "external_fulltext_checked": False,
                "external_proof_checked": False,
            },
        }
        row["row_sha256"] = sha256(canonical(row))
        overlay_records.append(row)

    overlay_decisions = Counter(row["overlay_review_disposition"] for row in overlay_records)
    overlay: dict[str, Any] = {
        "schema_version": "awesome-theorems/landmark-existing-quality-overlay/5.5",
        "artifact_path": OVERLAY_REL.as_posix(),
        "review_as_of": "2026-08-10",
        "scope": {
            "base_ledger_is_frozen": True,
            "not_a_release_append": True,
            "new_release_theorem_credit_granted": 0,
            "strict_conjecture_credit_granted": 0,
            "quality_credit_only": True,
            "source_index_range": [0, 66],
        },
        "inputs": {
            "base_ledger_path": BASE_REL.as_posix(),
            "base_ledger_sha256": BASE_SHA256,
            "review_path": REVIEW_REL.as_posix(),
            "review_sha256": REVIEW_SHA256,
            "review_authority_sha256": REVIEW_AUTHORITY_SHA256,
            "release_manifest_path": MANIFEST_REL.as_posix(),
            "release_manifest_sha256": MANIFEST_SHA256,
        },
        "counts": {
            "reviewed_rows": len(overlay_records),
            "overlay_decision_counts": dict(sorted(overlay_decisions.items())),
            "existing_quality_credit_delta": sum(
                row["existing_quality_credit_delta"] for row in overlay_records
            ),
            "new_release_theorem_credit_delta": 0,
            "strict_conjecture_credit_delta": 0,
        },
        "records": overlay_records,
    }
    if overlay["counts"]["existing_quality_credit_delta"] != 30:
        raise AssertionError("overlay must add exactly 30 existing-quality credits")
    overlay["records_canonical_sha256"] = sha256(canonical(overlay_records))
    overlay["authority_sha256"] = sha256(canonical(overlay))
    overlay_file_sha256 = sha256(canonical(overlay) + b"\n")

    aggregate_records: list[dict[str, Any]] = []
    overlay_by_index = {row["source_index"]: row for row in overlay_records}
    for source in base_records:
        index = source["source_index"]
        applied = overlay_by_index.get(index)
        base_disposition = source["review_disposition"]
        base_quality = source["grants_existing_quality_credit"] is True
        current_disposition = (
            applied["overlay_review_disposition"] if applied else base_disposition
        )
        current_quality = (
            applied["grants_existing_quality_credit"] if applied else base_quality
        )
        row = {
            "source_index": index,
            "source_record_id": source["source_record_id"],
            "source_row_sha256": source["source_row_sha256"],
            "external_id": source["external_id"],
            "title": source["title"],
            "msc2020": source["msc2020"],
            "base_record_canonical_sha256": sha256(canonical(source)),
            "base_review_disposition": base_disposition,
            "current_review_disposition": current_disposition,
            "base_existing_quality_credit": base_quality,
            "current_existing_quality_credit": current_quality,
            "overlay_applied": applied is not None,
            "overlay_row_sha256": applied["row_sha256"] if applied else None,
            "grants_new_release_theorem_credit": False,
        }
        row["row_sha256"] = sha256(canonical(row))
        aggregate_records.append(row)

    base_decisions = Counter(row["base_review_disposition"] for row in aggregate_records)
    current_decisions = Counter(row["current_review_disposition"] for row in aggregate_records)
    aggregate: dict[str, Any] = {
        "schema_version": "awesome-theorems/landmark-overlay-aggregate-ledger/5.5",
        "artifact_path": AGGREGATE_REL.as_posix(),
        "review_as_of": "2026-08-10",
        "scope": {
            "base_ledger_is_frozen": True,
            "overlay_precedence_only_for_listed_indices": True,
            "not_a_release_append": True,
            "new_release_theorem_credit_granted": 0,
            "strict_conjecture_credit_granted": 0,
        },
        "inputs": {
            "base_ledger_path": BASE_REL.as_posix(),
            "base_ledger_sha256": BASE_SHA256,
            "overlay_path": OVERLAY_REL.as_posix(),
            "overlay_sha256": overlay_file_sha256,
            "overlay_authority_sha256": overlay["authority_sha256"],
        },
        "counts": {
            "candidate_identities": 1200,
            "base_decision_counts": dict(sorted(base_decisions.items())),
            "current_decision_counts": dict(sorted(current_decisions.items())),
            "base_existing_quality_credits": sum(
                row["base_existing_quality_credit"] for row in aggregate_records
            ),
            "current_existing_quality_credits": sum(
                row["current_existing_quality_credit"] for row in aggregate_records
            ),
            "existing_quality_credit_delta": sum(
                row["current_existing_quality_credit"]
                - row["base_existing_quality_credit"]
                for row in aggregate_records
            ),
            "overlay_rows": len(overlay_records),
            "new_release_theorem_credits": 0,
            "strict_conjecture_credits": 0,
        },
        "records": aggregate_records,
    }
    expected_counts = {
        "candidate_identities": 1200,
        "base_decision_counts": {
            "eligible_existing_quality_credit": 439,
            "pending": 714,
            "reject": 47,
        },
        "current_decision_counts": {
            "eligible_existing_quality_credit": 469,
            "pending": 678,
            "reject": 53,
        },
        "base_existing_quality_credits": 439,
        "current_existing_quality_credits": 469,
        "existing_quality_credit_delta": 30,
        "overlay_rows": 51,
        "new_release_theorem_credits": 0,
        "strict_conjecture_credits": 0,
    }
    if aggregate["counts"] != expected_counts:
        raise AssertionError(f"aggregate count mismatch: {aggregate['counts']}")
    aggregate["records_canonical_sha256"] = sha256(canonical(aggregate_records))
    aggregate["authority_sha256"] = sha256(canonical(aggregate))

    for document in (overlay, aggregate):
        encoded = canonical(document)
        if b"/tmp/" in encoded or b"/home/" in encoded:
            raise AssertionError("ephemeral or workstation-local path in generated artifact")
    return overlay, aggregate


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    overlay, aggregate = build()
    outputs = [
        (ROOT / OVERLAY_REL, canonical(overlay) + b"\n"),
        (ROOT / AGGREGATE_REL, canonical(aggregate) + b"\n"),
    ]
    if args.write:
        for path, payload in outputs:
            path.write_bytes(payload)
        mode = "WROTE"
    else:
        for path, payload in outputs:
            if not path.exists() or path.read_bytes() != payload:
                raise SystemExit(f"overlay artifact is absent or stale: {path}; run --write")
        mode = "PASS"
    print(
        f"{mode} landmark overlay rows=51 delta=30 current=469 "
        f"new=0 overlay_authority={overlay['authority_sha256']} "
        f"aggregate_authority={aggregate['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
