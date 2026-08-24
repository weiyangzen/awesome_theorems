#!/usr/bin/env python3
"""Independently validate the landmark quality overlay and aggregate ledger."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[4]
CURATION_REL = Path("Docs/catalog/v5/curation/theorem_quality_v5_5")
BASE_REL = CURATION_REL / "landmark-ledger-0-1199.json"
REVIEW_REL = CURATION_REL / "reviews/wiki-reference-review-000-066.json"
OVERLAY_REL = CURATION_REL / "landmark-overlay-000-066.json"
AGGREGATE_REL = CURATION_REL / "landmark-ledger-0-1199-overlay-000-066.json"
MANIFEST_REL = Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json")
CATALOG_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
BUILDER_REL = Path("Docs/catalog/v5/tools/build_theorem_quality_landmark_overlay_v5_5.py")
REVIEW_CHECKER_REL = Path("Docs/catalog/v5/tools/check_theorem_quality_wiki_review_000_066_v5_5.py")

BASE_SHA256 = "51c5607cd4289f8340745879b8b134673bbd44e873cebc82e2da59f0ba6c1471"
REVIEW_SHA256 = "ab7fcefbc7618dfb42770307475342974340c845310d03e4988328620b35559d"
OVERLAY_SHA256 = "8fb15a29a527c355e723a4a5abddd05e8034030e5dc1c1128625e10675744a68"
AGGREGATE_SHA256 = "09965eecb4f5a5bb0ec36df03fa83e140e0d616a6b10d2d792cf78e545885634"
MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
REVIEW_AUTHORITY_SHA256 = "64de172f15ec4518f3409dc6d4cc699abfa009004c3ca4a856f899a628b1352b"
OVERLAY_AUTHORITY_SHA256 = "088c0452af2feb214f94ed04b9132b25b34a3e369a4bc6cd13bd4dec8c215094"
AGGREGATE_AUTHORITY_SHA256 = "106442d748dc77b4346fc179db3c7a64065d6f3baf97e8b81fc1c37de09a221e"


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


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


def values_for_key(value: Any, key: str) -> Iterable[Any]:
    if isinstance(value, dict):
        for child_key, child in value.items():
            if child_key == key:
                yield child
            yield from values_for_key(child, key)
    elif isinstance(value, list):
        for child in value:
            yield from values_for_key(child, key)


def normalize_decision(value: str) -> str:
    if value in {"eligible", "eligible_existing_quality_credit"}:
        return "eligible_existing_quality_credit"
    require(value in {"pending", "reject"}, f"unknown review decision: {value!r}")
    return value


def check(
    root: Path = ROOT,
    overlay_path: Path | None = None,
    aggregate_path: Path | None = None,
) -> dict[str, Any]:
    overlay_path = overlay_path or root / OVERLAY_REL
    aggregate_path = aggregate_path or root / AGGREGATE_REL
    fixed = {
        root / BASE_REL: BASE_SHA256,
        root / REVIEW_REL: REVIEW_SHA256,
        root / MANIFEST_REL: MANIFEST_SHA256,
        root / CATALOG_REL: CATALOG_SHA256,
        overlay_path: OVERLAY_SHA256,
        aggregate_path: AGGREGATE_SHA256,
    }
    for path, expected in fixed.items():
        require(file_sha256(path) == expected, f"file hash mismatch: {path}")

    for path in (overlay_path, aggregate_path):
        encoded = path.read_bytes()
        require(encoded.endswith(b"\n"), f"missing final newline: {path.name}")
        require(
            b"/tmp/" not in encoded and b"/home/" not in encoded,
            f"ephemeral/workstation path in {path.name}",
        )

    base = json.loads((root / BASE_REL).read_text(encoding="utf-8"))
    review = json.loads((root / REVIEW_REL).read_text(encoding="utf-8"))
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
    require(review["authority_sha256"] == REVIEW_AUTHORITY_SHA256, "review authority mismatch")
    require(
        overlay.get("authority_sha256") == OVERLAY_AUTHORITY_SHA256
        and overlay["authority_sha256"] == hash_without(overlay, "authority_sha256"),
        "overlay authority mismatch",
    )
    require(
        aggregate.get("authority_sha256") == AGGREGATE_AUTHORITY_SHA256
        and aggregate["authority_sha256"] == hash_without(aggregate, "authority_sha256"),
        "aggregate authority mismatch",
    )
    require(
        overlay.get("schema_version") == "awesome-theorems/landmark-existing-quality-overlay/5.5",
        "overlay schema mismatch",
    )
    require(
        aggregate.get("schema_version") == "awesome-theorems/landmark-overlay-aggregate-ledger/5.5",
        "aggregate schema mismatch",
    )
    require(overlay.get("artifact_path") == OVERLAY_REL.as_posix(), "overlay path mismatch")
    require(aggregate.get("artifact_path") == AGGREGATE_REL.as_posix(), "aggregate path mismatch")

    base_records = base["records"]
    review_records = review["records"]
    overlay_records = overlay["records"]
    aggregate_records = aggregate["records"]
    require(len(base_records) == len(aggregate_records) == 1200, "aggregate cardinality mismatch")
    require(len(review_records) == len(overlay_records) == 51, "overlay cardinality mismatch")
    require([row["source_index"] for row in base_records] == list(range(1200)), "base index mismatch")
    require([row["source_index"] for row in aggregate_records] == list(range(1200)), "aggregate index mismatch")
    require(
        [row["source_index"] for row in overlay_records]
        == review["scope"]["source_indices"],
        "overlay/review coverage mismatch",
    )
    require(
        overlay["records_canonical_sha256"] == sha256(canonical(overlay_records)),
        "overlay record-set hash mismatch",
    )
    require(
        aggregate["records_canonical_sha256"] == sha256(canonical(aggregate_records)),
        "aggregate record-set hash mismatch",
    )

    review_by_index = {row["index"]: row for row in review_records}
    overlay_by_index = {row["source_index"]: row for row in overlay_records}
    quality_delta = 0
    for row in overlay_records:
        index = row["source_index"]
        source = base_records[index]
        evidence = review_by_index[index]
        require(source["review_disposition"] == "pending", f"overlay source not pending: {index}")
        require(source["grants_existing_quality_credit"] is False, f"base credit at {index}")
        require(row["source_record_id"] == source["source_record_id"], f"source ID mismatch at {index}")
        require(row["external_id"] == source["external_id"], f"external ID mismatch at {index}")
        require(row["title"] == source["title"] == evidence["title"], f"title mismatch at {index}")
        disposition = normalize_decision(evidence["decision"])
        quality = disposition == "eligible_existing_quality_credit"
        require(row["base_review_disposition"] == "pending", f"base decision mismatch at {index}")
        require(row["overlay_review_disposition"] == disposition, f"overlay decision mismatch at {index}")
        require(row["base_existing_quality_credit"] is False, f"base row credit mismatch at {index}")
        require(row["grants_existing_quality_credit"] is quality, f"overlay credit mismatch at {index}")
        require(row["existing_quality_credit_delta"] == int(quality), f"delta mismatch at {index}")
        require(row["grants_new_release_theorem_credit"] is False, f"new credit at {index}")
        require(row["formal_proof_claimed"] is False, f"proof claim at {index}")
        require(row["review_record_canonical_sha256"] == sha256(canonical(evidence)), f"review binding mismatch at {index}")
        require(row["row_sha256"] == hash_without(row, "row_sha256"), f"overlay row hash mismatch at {index}")
        boundary = row["review_evidence_boundary"]
        require(boundary["automatic_reference_credit"] is False, f"automatic credit at {index}")
        require(boundary["external_fulltext_checked"] is False, f"fulltext claim at {index}")
        require(boundary["external_proof_checked"] is False, f"proof evidence claim at {index}")
        statement_verified = (
            evidence.get("evidence") is not None
            or evidence.get("statement_evidence") is not None
        )
        require(
            boundary["exact_wikipedia_statement_verified"] is statement_verified,
            f"statement evidence boundary mismatch at {index}",
        )
        require(
            boundary["manual_reference_match_verified"] is quality,
            f"reference evidence boundary mismatch at {index}",
        )
        quality_delta += int(quality)

    base_decisions = Counter()
    current_decisions = Counter()
    base_quality = 0
    current_quality = 0
    for source, row in zip(base_records, aggregate_records, strict=True):
        index = source["source_index"]
        applied = overlay_by_index.get(index)
        expected_disposition = (
            applied["overlay_review_disposition"]
            if applied
            else source["review_disposition"]
        )
        expected_quality = (
            applied["grants_existing_quality_credit"]
            if applied
            else source["grants_existing_quality_credit"]
        )
        require(row["source_record_id"] == source["source_record_id"], f"aggregate source mismatch at {index}")
        require(row["source_row_sha256"] == source["source_row_sha256"], f"aggregate source hash mismatch at {index}")
        require(row["external_id"] == source["external_id"] and row["title"] == source["title"], f"aggregate identity mismatch at {index}")
        require(row["base_record_canonical_sha256"] == sha256(canonical(source)), f"base record binding mismatch at {index}")
        require(row["base_review_disposition"] == source["review_disposition"], f"aggregate base decision mismatch at {index}")
        require(row["current_review_disposition"] == expected_disposition, f"aggregate decision mismatch at {index}")
        require(row["base_existing_quality_credit"] is source["grants_existing_quality_credit"], f"aggregate base credit mismatch at {index}")
        require(row["current_existing_quality_credit"] is expected_quality, f"aggregate current credit mismatch at {index}")
        require(row["overlay_applied"] is (applied is not None), f"overlay marker mismatch at {index}")
        require(row["overlay_row_sha256"] == (applied["row_sha256"] if applied else None), f"overlay row binding mismatch at {index}")
        require(row["grants_new_release_theorem_credit"] is False, f"aggregate new credit at {index}")
        require(row["row_sha256"] == hash_without(row, "row_sha256"), f"aggregate row hash mismatch at {index}")
        base_decisions[source["review_disposition"]] += 1
        current_decisions[expected_disposition] += 1
        base_quality += int(source["grants_existing_quality_credit"])
        current_quality += int(expected_quality)

    expected_overlay_counts = {
        "reviewed_rows": 51,
        "overlay_decision_counts": {
            "eligible_existing_quality_credit": 30,
            "pending": 15,
            "reject": 6,
        },
        "existing_quality_credit_delta": 30,
        "new_release_theorem_credit_delta": 0,
        "strict_conjecture_credit_delta": 0,
    }
    expected_aggregate_counts = {
        "candidate_identities": 1200,
        "base_decision_counts": dict(sorted(base_decisions.items())),
        "current_decision_counts": dict(sorted(current_decisions.items())),
        "base_existing_quality_credits": 439,
        "current_existing_quality_credits": 469,
        "existing_quality_credit_delta": 30,
        "overlay_rows": 51,
        "new_release_theorem_credits": 0,
        "strict_conjecture_credits": 0,
    }
    require(quality_delta == 30, "quality delta is not exactly 30")
    require(base_quality == 439 and current_quality == 469, "quality totals mismatch")
    require(overlay["counts"] == expected_overlay_counts, "overlay summary mismatch")
    require(aggregate["counts"] == expected_aggregate_counts, "aggregate summary mismatch")
    require(
        current_decisions
        == Counter(eligible_existing_quality_credit=469, pending=678, reject=53),
        "aggregate decision totals mismatch",
    )
    for document in (overlay, aggregate):
        for field in ("grants_new_catalog_entry", "grants_new_release_theorem_credit"):
            require(
                all(value in {False, 0} for value in values_for_key(document, field)),
                f"new theorem credit leakage: {field}",
            )

    manifest = json.loads((root / MANIFEST_REL).read_text(encoding="utf-8"))
    require(manifest["counts"]["cumulative_theorems"] == 2500, "release theorem count changed")
    require(
        manifest["counts"]["effective_strict_conjecture_credits"] == 1000,
        "release conjecture count changed",
    )
    return {
        "rows": 1200,
        "overlay_rows": 51,
        "base_existing_quality": 439,
        "current_existing_quality": 469,
        "existing_quality_delta": 30,
        "current_pending": 678,
        "current_reject": 53,
        "new_release_theorems": 0,
        "overlay_authority_sha256": overlay["authority_sha256"],
        "aggregate_authority_sha256": aggregate["authority_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=ROOT)
    parser.add_argument("--overlay", type=Path)
    parser.add_argument("--aggregate", type=Path)
    args = parser.parse_args()
    root = args.workspace.resolve()
    try:
        review_check = subprocess.run(
            [sys.executable, str(root / REVIEW_CHECKER_REL)],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        require(review_check.returncode == 0, f"review validator failed: {review_check.stderr}")
        result = check(
            root,
            args.overlay.resolve() if args.overlay else None,
            args.aggregate.resolve() if args.aggregate else None,
        )
        rebuild = subprocess.run(
            [sys.executable, str(root / BUILDER_REL), "--check"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        require(rebuild.returncode == 0, f"overlay reproducibility failed: {rebuild.stderr}")
    except (CheckError, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"FAIL theorem quality landmark overlay: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"overall_pass": True, **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
