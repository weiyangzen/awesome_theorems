#!/usr/bin/env python3
"""Build the fixed-source theorem-statement/reference review for indices 0..66."""

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
BUILDERS = [
    REPO / "Docs/catalog/v5/tools/build_theorem_quality_wiki_subreview_000_016_v5_5.py",
    REPO / "Docs/catalog/v5/tools/build_theorem_quality_wiki_subreview_017_065_v5_5.py",
]
SUBREVIEWS = [
    AUDIT / "reviews/wiki-reference-subreview-000-016.json",
    AUDIT / "reviews/wiki-reference-subreview-017-065.json",
]
OUTPUT = AUDIT / "reviews/wiki-reference-review-000-066.json"

EXPECTED_SHA256 = {
    REVIEW: "9bbaf8db012b5f7283bac1f2362717a27e50ef8178e379992e24a2693dd59052",
    WIKIPEDIA: "73341aebcc1d9d1c577881d2c6d59734ce102d7cc07b1f8ec6d21c9875076d33",
    REFERENCES: "f86b87afcffbf120d2f3cf0ff8860e7c925e8f9fa514db3714936e3cfa100435",
}
REFERENCE_AUTHORITY_SHA256 = "d428f5659c242fa66c3e78f5497013ea1b6eaf13a4558c4f15e6c0af005acc42"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def assert_fixed_inputs() -> None:
    for path, expected in EXPECTED_SHA256.items():
        actual = sha256(path.read_bytes())
        if actual != expected:
            raise AssertionError(f"fixed input hash mismatch {path}: {actual}")


def rebuild_subreviews() -> None:
    for builder in BUILDERS:
        subprocess.run(
            [sys.executable, str(builder)],
            check=True,
            stdout=subprocess.DEVNULL,
        )


def build() -> dict:
    assert_fixed_inputs()
    rebuild_subreviews()

    parent_rows = [
        json.loads(line)
        for line in REVIEW.read_text(encoding="utf-8").splitlines()
    ]
    expected_indices = [
        row["index"]
        for row in parent_rows
        if 0 <= row["index"] <= 66 and row["decision"] == "pending"
    ]
    records = []
    for path in SUBREVIEWS:
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            raise AssertionError(f"subreview must be a list: {path}")
        records.extend(rows)
    if [row["index"] for row in records] != expected_indices:
        raise AssertionError("subreview indices do not equal the parent pending slice")

    for row in records:
        if row["grants_new_catalog_entry"] or row["formal_proof_claimed"]:
            raise AssertionError(f"forbidden grant/proof claim at {row['index']}")
        eligible = row["decision"] == "eligible"
        if row["grants_existing_quality_credit"] is not eligible:
            raise AssertionError(f"quality-credit mismatch at {row['index']}")
        if eligible:
            if not row.get("evidence") or not row.get("reference_evidence"):
                raise AssertionError(f"eligible row lacks dual evidence at {row['index']}")
            reference = row["reference_evidence"]
            if reference["automatic_credit"] or not reference["human_match_performed"]:
                raise AssertionError(f"automatic/unmatched reference at {row['index']}")
            if reference["external_proof_checked"] or reference["external_fulltext_checked"]:
                raise AssertionError(f"unsupported external-content claim at {row['index']}")
        elif row.get("reference_evidence") is not None:
            raise AssertionError(f"noneligible row has promoted reference at {row['index']}")

    counts = {
        "rows": len(records),
        "eligible_existing_quality_credit": sum(
            row["decision"] == "eligible" for row in records
        ),
        "pending": sum(row["decision"] == "pending" for row in records),
        "reject": sum(row["decision"] == "reject" for row in records),
        "new_catalog_entries": 0,
        "formal_proofs_claimed": 0,
    }
    expected_counts = {
        "rows": 51,
        "eligible_existing_quality_credit": 30,
        "pending": 15,
        "reject": 6,
        "new_catalog_entries": 0,
        "formal_proofs_claimed": 0,
    }
    if counts != expected_counts:
        raise AssertionError(counts)

    with gzip.open(WIKIPEDIA, "rt", encoding="utf-8") as handle:
        wikipedia = json.load(handle)
    reference_asset = json.loads(REFERENCES.read_text(encoding="utf-8"))
    if reference_asset["authority_sha256"] != REFERENCE_AUTHORITY_SHA256:
        raise AssertionError("reference authority mismatch")

    payload = {
        "schema_version": "awesome-theorems/wikipedia-reference-existing-quality-review/1.0",
        "scope": {
            "parent_pending_slice": [0, 66],
            "source_indices": expected_indices,
            "credit_scope": "existing_catalog_quality_only",
            "release_modified": False,
        },
        "inputs": {
            path.relative_to(REPO).as_posix(): digest
            for path, digest in EXPECTED_SHA256.items()
        },
        "reference_authority_sha256": REFERENCE_AUTHORITY_SHA256,
        "reference_policy": reference_asset["policy"],
        "rights": wikipedia["rights"],
        "builders": {
            path.relative_to(REPO).as_posix(): sha256(path.read_bytes())
            for path in BUILDERS
        },
        "subreviews": {
            path.relative_to(REPO).as_posix(): sha256(path.read_bytes())
            for path in SUBREVIEWS
        },
        "counts": counts,
        "records": records,
    }
    payload["authority_sha256"] = canonical_sha256(payload)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    if b"/tmp/" in encoded or b"/home/" in encoded:
        raise AssertionError("ephemeral or workstation-local provenance in review")
    return payload


def main() -> None:
    payload = build()
    serialized = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(serialized, encoding="utf-8")
    rebuilt = build()
    rebuilt_bytes = (
        json.dumps(rebuilt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if OUTPUT.read_bytes() != rebuilt_bytes:
        raise AssertionError("deterministic rebuild mismatch")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": sha256(OUTPUT.read_bytes()),
                **payload["counts"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
