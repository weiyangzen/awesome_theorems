#!/usr/bin/env python3
"""Independently validate the chained 67..133 landmark quality overlay."""

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
PRIOR_REL = CURATION_REL / "landmark-ledger-0-1199-overlay-000-066.json"
REVIEW_REL = CURATION_REL / "reviews/wiki-reference-review-067-133.json"
OVERLAY_REL = CURATION_REL / "landmark-overlay-067-133.json"
AGGREGATE_REL = CURATION_REL / "landmark-ledger-0-1199-overlay-000-133.json"
MANIFEST_REL = Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json")
CATALOG_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
STRICT_REL = Path("Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json")
BUILDER_REL = Path("Docs/catalog/v5/tools/build_theorem_quality_landmark_overlay_067_133_v5_5.py")
REVIEW_CHECKER_REL = Path("Docs/catalog/v5/tools/check_theorem_quality_wiki_review_067_133_v5_5.py")

FIXED_SHA256 = {
    BASE_REL: "51c5607cd4289f8340745879b8b134673bbd44e873cebc82e2da59f0ba6c1471",
    PRIOR_REL: "09965eecb4f5a5bb0ec36df03fa83e140e0d616a6b10d2d792cf78e545885634",
    REVIEW_REL: "a6274527790ff89f530325f35470cebda742ae0c4dc740ee48d70e4b9e60daa0",
    OVERLAY_REL: "02f81e252ff5d605b0e4ae1003623b647d5407cb31eade4f7e06db85f18ae800",
    AGGREGATE_REL: "8a077a4bd31e5e0559276d7b51daf88321e70ae5f2fbe80f8bad5cfdc68db6c3",
    MANIFEST_REL: "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9",
    CATALOG_REL: "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
    STRICT_REL: "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3",
    BUILDER_REL: "cf298b916641c874126e5b06b0e959d89fe67b7672a2b75c2077528af6fb5b35",
}
PRIOR_AUTHORITY_SHA256 = "106442d748dc77b4346fc179db3c7a64065d6f3baf97e8b81fc1c37de09a221e"
REVIEW_AUTHORITY_SHA256 = "c6717771eda15518389f5917fefa34f2a7fcfa1ca9843dfa96d70c3cfb60e764"
OVERLAY_AUTHORITY_SHA256 = "119967d07c9e0b5a581aca8e8851e12a60363098b356bd2ff5137e0c709ffc23"
AGGREGATE_AUTHORITY_SHA256 = "1929b9fdb879b23985b05ebe41235c19e8caf381ab5d81be220fcf61cfa7cdab"


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
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
        root / relative: digest
        for relative, digest in FIXED_SHA256.items()
        if relative not in {OVERLAY_REL, AGGREGATE_REL}
    }
    if overlay_path.resolve() == (root / OVERLAY_REL).resolve():
        fixed[overlay_path] = FIXED_SHA256[OVERLAY_REL]
    if aggregate_path.resolve() == (root / AGGREGATE_REL).resolve():
        fixed[aggregate_path] = FIXED_SHA256[AGGREGATE_REL]
    for path, expected in fixed.items():
        require(file_sha256(path) == expected, f"file hash mismatch: {path}")
    for path in (overlay_path, aggregate_path):
        raw = path.read_bytes()
        require(raw.endswith(b"\n"), f"missing final newline: {path.name}")
        require(b"/tmp/" not in raw and b"/home/" not in raw, f"local path in {path.name}")

    base = json.loads((root / BASE_REL).read_text(encoding="utf-8"))
    prior = json.loads((root / PRIOR_REL).read_text(encoding="utf-8"))
    review = json.loads((root / REVIEW_REL).read_text(encoding="utf-8"))
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
    require(prior["authority_sha256"] == PRIOR_AUTHORITY_SHA256, "prior authority mismatch")
    require(review["authority_sha256"] == REVIEW_AUTHORITY_SHA256, "review authority mismatch")
    require(
        overlay["authority_sha256"] == hash_without(overlay, "authority_sha256"),
        "overlay authority self-hash mismatch",
    )
    require(
        aggregate["authority_sha256"] == hash_without(aggregate, "authority_sha256"),
        "aggregate authority self-hash mismatch",
    )
    if overlay_path.resolve() == (root / OVERLAY_REL).resolve():
        require(overlay["authority_sha256"] == OVERLAY_AUTHORITY_SHA256, "overlay authority mismatch")
    if aggregate_path.resolve() == (root / AGGREGATE_REL).resolve():
        require(aggregate["authority_sha256"] == AGGREGATE_AUTHORITY_SHA256, "aggregate authority mismatch")
    require(
        overlay["schema_version"] == "awesome-theorems/landmark-existing-quality-overlay-chain-layer/5.5",
        "overlay schema mismatch",
    )
    require(
        aggregate["schema_version"] == "awesome-theorems/landmark-overlay-chain-aggregate-ledger/5.5",
        "aggregate schema mismatch",
    )
    require(overlay["artifact_path"] == OVERLAY_REL.as_posix(), "overlay path mismatch")
    require(aggregate["artifact_path"] == AGGREGATE_REL.as_posix(), "aggregate path mismatch")
    require(
        overlay["scope"] == {
            "prior_aggregate_is_frozen": True,
            "base_ledger_is_frozen": True,
            "not_a_release_append": True,
            "new_release_theorem_credit_granted": 0,
            "strict_conjecture_credit_granted": 0,
            "quality_credit_only": True,
            "source_index_range": [67, 133],
        },
        "overlay scope mismatch",
    )
    require(
        aggregate["scope"] == {
            "base_ledger_is_frozen": True,
            "prior_aggregate_is_frozen": True,
            "overlay_precedence_only_for_listed_indices": True,
            "not_a_release_append": True,
            "new_release_theorem_credit_granted": 0,
            "strict_conjecture_credit_granted": 0,
            "overlay_chain_ranges": [[0, 66], [67, 133]],
        },
        "aggregate scope mismatch",
    )

    base_records = base["records"]
    prior_records = prior["records"]
    review_records = review["records"]
    overlay_records = overlay["records"]
    aggregate_records = aggregate["records"]
    require(len(base_records) == len(prior_records) == len(aggregate_records) == 1200, "aggregate cardinality mismatch")
    require(len(review_records) == len(overlay_records) == 52, "overlay cardinality mismatch")
    require([row["source_index"] for row in prior_records] == list(range(1200)), "prior indices mismatch")
    require([row["source_index"] for row in aggregate_records] == list(range(1200)), "aggregate indices mismatch")
    require(
        [row["source_index"] for row in overlay_records]
        == review["scope"]["reviewed_parent_pending_indices"],
        "overlay/review coverage mismatch",
    )
    require(overlay["records_canonical_sha256"] == sha256(canonical(overlay_records)), "overlay records hash mismatch")
    require(aggregate["records_canonical_sha256"] == sha256(canonical(aggregate_records)), "aggregate records hash mismatch")

    review_by_index = {row["source_index"]: row for row in review_records}
    overlay_by_index = {row["source_index"]: row for row in overlay_records}
    layer_delta = 0
    for row in overlay_records:
        index = row["source_index"]
        source = prior_records[index]
        evidence = review_by_index[index]
        require(source["current_review_disposition"] == "pending", f"prior source not pending: {index}")
        require(source["current_existing_quality_credit"] is False, f"prior credit at {index}")
        require(row["source_record_id"] == source["source_record_id"] == evidence["source_record_id"], f"source mismatch at {index}")
        require(row["external_id"] == source["external_id"] == evidence["external_id"], f"external ID mismatch at {index}")
        require(row["title"] == source["title"] == evidence["title"], f"title mismatch at {index}")
        require(row["prior_aggregate_row_sha256"] == source["row_sha256"], f"prior row hash mismatch at {index}")
        disposition = normalize_decision(evidence["decision"])
        quality = disposition == "eligible_existing_quality_credit"
        require(row["prior_review_disposition"] == "pending", f"prior decision mismatch at {index}")
        require(row["overlay_review_disposition"] == disposition, f"overlay decision mismatch at {index}")
        require(row["prior_existing_quality_credit"] is False, f"prior quality mismatch at {index}")
        require(row["grants_existing_quality_credit"] is quality, f"quality mismatch at {index}")
        require(row["existing_quality_credit_delta"] == int(quality), f"delta mismatch at {index}")
        require(row["grants_new_release_theorem_credit"] is False, f"new theorem credit at {index}")
        require(row["grants_strict_conjecture_credit"] is False, f"strict conjecture credit at {index}")
        require(row["formal_proof_claimed"] is False, f"proof claim at {index}")
        require(row["review_record_canonical_sha256"] == sha256(canonical(evidence)), f"review binding mismatch at {index}")
        require(row["row_sha256"] == hash_without(row, "row_sha256"), f"overlay row hash mismatch at {index}")
        boundary = row["review_evidence_boundary"]
        require(boundary["exact_wikipedia_statement_verified"] is quality, f"statement boundary mismatch at {index}")
        require(boundary["manual_reference_match_verified"] is quality, f"reference boundary mismatch at {index}")
        require(boundary["automatic_reference_credit"] is False, f"automatic credit at {index}")
        require(boundary["external_fulltext_checked"] is False, f"fulltext claim at {index}")
        require(boundary["external_proof_checked"] is False, f"proof check at {index}")
        layer_delta += int(quality)

    base_decisions = Counter()
    prior_decisions = Counter()
    current_decisions = Counter()
    base_quality = prior_quality = current_quality = cumulative_overlay_rows = 0
    for source, row in zip(prior_records, aggregate_records, strict=True):
        index = source["source_index"]
        applied = overlay_by_index.get(index)
        expected = dict(source)
        if applied is not None:
            expected["current_review_disposition"] = applied["overlay_review_disposition"]
            expected["current_existing_quality_credit"] = applied["grants_existing_quality_credit"]
            expected["overlay_applied"] = True
            expected["overlay_row_sha256"] = applied["row_sha256"]
        expected.pop("row_sha256")
        expected["row_sha256"] = sha256(canonical(expected))
        require(row == expected, f"aggregate row mismatch at {index}")
        require(row["grants_new_release_theorem_credit"] is False, f"aggregate new credit at {index}")
        base_decisions[row["base_review_disposition"]] += 1
        prior_decisions[source["current_review_disposition"]] += 1
        current_decisions[row["current_review_disposition"]] += 1
        base_quality += int(row["base_existing_quality_credit"])
        prior_quality += int(source["current_existing_quality_credit"])
        current_quality += int(row["current_existing_quality_credit"])
        cumulative_overlay_rows += int(row["overlay_applied"])

    expected_overlay_counts = {
        "reviewed_rows": 52,
        "overlay_decision_counts": {
            "eligible_existing_quality_credit": 27,
            "pending": 19,
            "reject": 6,
        },
        "existing_quality_credit_delta": 27,
        "new_release_theorem_credit_delta": 0,
        "strict_conjecture_credit_delta": 0,
    }
    expected_aggregate_counts = {
        "candidate_identities": 1200,
        "base_decision_counts": dict(sorted(base_decisions.items())),
        "prior_current_decision_counts": dict(sorted(prior_decisions.items())),
        "current_decision_counts": dict(sorted(current_decisions.items())),
        "base_existing_quality_credits": base_quality,
        "prior_current_existing_quality_credits": prior_quality,
        "current_existing_quality_credits": current_quality,
        "layer_existing_quality_credit_delta": layer_delta,
        "cumulative_existing_quality_credit_delta": current_quality - base_quality,
        "prior_overlay_rows": prior["counts"]["overlay_rows"],
        "layer_overlay_rows": len(overlay_records),
        "cumulative_overlay_rows": cumulative_overlay_rows,
        "new_release_theorem_credits": 0,
        "strict_conjecture_credits": 0,
    }
    require(overlay["counts"] == expected_overlay_counts, "overlay counts mismatch")
    require(aggregate["counts"] == expected_aggregate_counts, "aggregate counts mismatch")
    require(layer_delta == 27, "layer quality delta mismatch")
    require(base_quality == 439 and prior_quality == 469 and current_quality == 496, "quality totals mismatch")
    require(
        current_decisions == Counter(eligible_existing_quality_credit=496, pending=645, reject=59),
        "current decision totals mismatch",
    )
    require(cumulative_overlay_rows == 103, "cumulative overlay row total mismatch")
    for document in (overlay, aggregate):
        for field in ("grants_new_catalog_entry", "grants_new_release_theorem_credit", "grants_strict_conjecture_credit"):
            require(
                all(value in {False, 0} for value in values_for_key(document, field)),
                f"inventory-credit leakage: {field}",
            )

    manifest = json.loads((root / MANIFEST_REL).read_text(encoding="utf-8"))
    strict = json.loads((root / STRICT_REL).read_text(encoding="utf-8"))
    require(manifest["counts"]["cumulative_theorems"] == 2500, "release theorem count changed")
    require(manifest["counts"]["effective_strict_conjecture_credits"] == 1000, "release strict count changed")
    require(strict["counts"]["effective_strict_credits"] == 1000, "strict ledger count changed")
    return {
        "rows": 1200,
        "layer_overlay_rows": 52,
        "cumulative_overlay_rows": 103,
        "base_existing_quality": 439,
        "prior_existing_quality": 469,
        "current_existing_quality": 496,
        "layer_existing_quality_delta": 27,
        "cumulative_existing_quality_delta": 57,
        "current_pending": 645,
        "current_reject": 59,
        "new_release_theorems": 0,
        "strict_conjecture_credits": 0,
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
            [sys.executable, str(root / REVIEW_CHECKER_REL)], cwd=root,
            text=True, capture_output=True, check=False,
        )
        require(review_check.returncode == 0, f"review validator failed: {review_check.stderr}")
        result = check(
            root,
            args.overlay.resolve() if args.overlay else None,
            args.aggregate.resolve() if args.aggregate else None,
        )
        rebuild = subprocess.run(
            [sys.executable, str(root / BUILDER_REL), "--check"], cwd=root,
            text=True, capture_output=True, check=False,
        )
        require(rebuild.returncode == 0, f"overlay reproducibility failed: {rebuild.stderr}")
    except (CheckError, AssertionError, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"FAIL theorem quality landmark overlay 067-133: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"overall_pass": True, **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
