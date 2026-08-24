#!/usr/bin/env python3
"""Independent checker for the 1,000-row important mathlib inventory."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


SOURCE_REL = Path("Docs/catalog/v5/sources/mathlib-theorems-8a178386.json")
CURATION_RELS = (
    Path("Docs/catalog/v5/curation/Mathlib_Theorem_Curation_v5_3.json"),
    Path("Docs/catalog/v5/curation/Mathlib_Theorem_Curation_v5_4.json"),
)
CATALOG_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
LEDGER_REL = Path("Docs/catalog/v5/curation/theorem_quality_v5_5/mathlib-important-inventory-1000.json")
EXPECTED_SHA256 = {
    SOURCE_REL: "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a",
    CURATION_RELS[0]: "379e165ae52ffd911e383fdb351fc602d36ec585e40bade54612c1512a7a1905",
    CURATION_RELS[1]: "0057a36999422726d6d490dbf59eca69824bc29a02f5117f9a02ebdd601dd386",
    CATALOG_REL: "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
    LEDGER_REL: "a3db9bcd31feb8f2ea4ac07c0b60076446af25b3e4045c2938851440fb974f92",
}
AUTHORITY = "0b4d7c43f91e3c57104665c579fabf7b8a27282b10d95670dea9ccb3bbaf11d2"
COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


class CheckError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return sha(canonical({key: item for key, item in value.items() if key not in ignored}))


def set_digest(values: Iterable[str]) -> str:
    return sha(canonical(sorted(values)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def reject_constant(token: str) -> None:
    raise CheckError(f"non-finite JSON token: {token}")


def closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(root: Path, relative: Path) -> dict[str, Any]:
    path = (root / relative).resolve(strict=True)
    require(path.is_relative_to(root), f"path escapes root: {relative}")
    require(file_sha(path) == EXPECTED_SHA256[relative], f"file digest drifted: {relative}")
    document = json.loads(path.read_bytes(), object_pairs_hook=closed_object, parse_constant=reject_constant)
    require(isinstance(document, dict), f"root is not object: {relative}")
    return document


def verify(repo_root: Path) -> None:
    root = repo_root.resolve(strict=True)
    source = load(root, SOURCE_REL)
    curations = [load(root, relative) for relative in CURATION_RELS]
    catalog = load(root, CATALOG_REL)
    ledger = load(root, LEDGER_REL)
    require(ledger.get("authority_sha256") == AUTHORITY, "ledger authority constant drifted")
    require(ledger.get("authority_sha256") == hash_without(ledger, "authority_sha256"), "ledger authority replay mismatch")
    require(ledger.get("schema_version") == "awesome-theorems/mathlib-important-inventory/5.5", "ledger schema drifted")
    require(ledger.get("review_as_of") == "2026-08-10", "review date drifted")
    require(ledger.get("scope", {}).get("not_a_release_append") is True, "ledger release boundary drifted")
    require(ledger.get("scope", {}).get("not_a_universal_importance_ranking") is True, "ranking boundary drifted")
    require(type(ledger.get("scope", {}).get("new_theorem_identity_credit")) is int and ledger["scope"]["new_theorem_identity_credit"] == 0, "scope new credit drifted")

    source_rows = source.get("records")
    require(isinstance(source_rows, list) and len(source_rows) == 1_500, "source denominator drifted")
    source_by_id = {row.get("source_record_id"): row for row in source_rows if isinstance(row, dict)}
    require(len(source_by_id) == 1_500 and None not in source_by_id, "source ids are not unique")
    catalog_rows = catalog.get("records")
    require(isinstance(catalog_rows, list) and len(catalog_rows) == 4_100, "catalog denominator drifted")
    catalog_by_id = {row.get("stage_claim_id"): row for row in catalog_rows if isinstance(row, dict)}
    require(len(catalog_by_id) == 4_100 and None not in catalog_by_id, "catalog ids are not unique")

    accepted_by_stage: dict[str, tuple[str, dict[str, Any]]] = {}
    for relative, curation in zip(CURATION_RELS, curations, strict=True):
        require(curation.get("authority_sha256") == hash_without(curation, "authority_sha256"), f"curation authority drifted: {relative}")
        accepted = [row for row in curation.get("candidate_dispositions", []) if isinstance(row, dict) and row.get("disposition") == "accepted_new_kernel_checked_theorem"]
        require(len(accepted) == 500, f"accepted denominator drifted: {relative}")
        for row in accepted:
            require(row.get("row_sha256") == hash_without(row, "row_sha256"), "curation row digest mismatch")
            stage_id = row.get("target_s5_id")
            require(isinstance(stage_id, str) and stage_id not in accepted_by_stage, "accepted stage id duplicate")
            accepted_by_stage[stage_id] = (relative.as_posix(), row)
    require(len(accepted_by_stage) == 1_000, "accepted theorem union drifted")

    rows = ledger.get("records")
    require(isinstance(rows, list) and len(rows) == 1_000, "ledger record denominator drifted")
    require([row.get("stage_claim_id") for row in rows] == sorted(accepted_by_stage), "ledger ids/order do not equal accepted set")
    tiers: Counter[str] = Counter()
    origins: Counter[str] = Counter()
    source_ids: list[str] = []
    semantic_keys: list[str] = []
    row_hashes: list[str] = []
    for row in rows:
        require(isinstance(row, dict), "ledger row is not object")
        stage_id = row["stage_claim_id"]
        curation_path, curation_row = accepted_by_stage[stage_id]
        source_id = curation_row["source_record_id"]
        source_row = source_by_id[source_id]
        claim = catalog_by_id[stage_id]
        require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"row digest mismatch: {stage_id}")
        require(row.get("curation_path") == curation_path and row.get("curation_row_sha256") == curation_row["row_sha256"], f"curation binding mismatch: {stage_id}")
        require(row.get("source_record_id") == source_id and row.get("source_record_sha256") == sha(canonical(source_row)), f"source binding mismatch: {stage_id}")
        require(row.get("variant_id") == claim.get("variant_id") and row.get("family_id") == claim.get("family_id"), f"identity binding mismatch: {stage_id}")
        require(row.get("semantic_key") == claim.get("semantic_key") == curation_row.get("semantic_key"), f"semantic binding mismatch: {stage_id}")
        require(claim.get("claim_kind") == "theorem" and claim.get("material_status") == "proved", f"catalog status mismatch: {stage_id}")
        require(source_row.get("formal_proof_state") == "kernel_checked_sorry_free" and source_row.get("proof_evidence", {}).get("uses_sorry") is False, f"formal proof gate failed: {stage_id}")
        require(source_row.get("material_status", {}).get("as_of_commit") == COMMIT, f"commit binding mismatch: {stage_id}")
        signals = source_row.get("importance_signals")
        require(row.get("importance_evidence", {}).get("signals") == signals, f"importance evidence mismatch: {stage_id}")
        kinds = sorted({signal.get("kind") for signal in signals if isinstance(signal, dict)})
        require(row.get("importance_evidence", {}).get("signal_kinds") == kinds, f"importance kinds mismatch: {stage_id}")
        expected_tier = "human_curated_mathlib_1000_named_theorem" if "mathlib_1000_theorems" in kinds else "human_documented_mathlib_module_main_result"
        require("mathlib_1000_theorems" in kinds or "mathlib_module_main_result" in kinds, f"human editorial signal absent: {stage_id}")
        require(row.get("quality_tier") == expected_tier, f"quality tier mismatch: {stage_id}")
        require(row.get("grants_existing_important_theorem_credit") is True, f"important credit absent: {stage_id}")
        require(row.get("grants_new_theorem_identity_credit") is False and row.get("grants_new_proof_credit") is False, f"new credit escalation: {stage_id}")
        require(row.get("rights") == source_row.get("rights"), f"rights binding mismatch: {stage_id}")
        tiers[expected_tier] += 1
        origins[row["origin_release"]] += 1
        source_ids.append(source_id)
        semantic_keys.append(row["semantic_key"])
        row_hashes.append(row["row_sha256"])
    require(len(set(source_ids)) == len(set(semantic_keys)) == 1_000, "source or semantic identity duplication")
    counts = ledger.get("counts")
    require(type(counts.get("existing_important_theorem_credits")) is int and counts["existing_important_theorem_credits"] == 1_000, "important count drifted")
    require(type(counts.get("new_theorem_identity_credits")) is int and counts["new_theorem_identity_credits"] == 0, "new theorem count drifted")
    require(type(counts.get("new_proof_credits")) is int and counts["new_proof_credits"] == 0, "new proof count drifted")
    require(counts.get("by_quality_tier") == dict(sorted(tiers.items())), "tier counts drifted")
    require(counts.get("by_origin_release") == dict(sorted(origins.items())) == {"5.3": 500, "5.4": 500}, "origin counts drifted")
    require(
        ledger.get("set_digests")
        == {
            "row_sha256_set_sha256": set_digest(row_hashes),
            "semantic_keys_sha256": set_digest(semantic_keys),
            "source_record_ids_sha256": set_digest(source_ids),
            "stage_claim_ids_sha256": set_digest(accepted_by_stage),
        },
        "set digests drifted",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    args = parser.parse_args()
    try:
        verify(args.repo_root)
    except (CheckError, OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"FAIL mathlib important inventory: {error}")
        return 1
    print(f"PASS mathlib important inventory important=1000 named=180 module_main=820 new=0 authority={AUTHORITY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
