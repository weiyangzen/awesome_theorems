#!/usr/bin/env python3
"""Build the 1,000-row source-qualified important mathlib inventory ledger."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[4]
SOURCE_REL = Path("Docs/catalog/v5/sources/mathlib-theorems-8a178386.json")
CURATION_RELS = (
    Path("Docs/catalog/v5/curation/Mathlib_Theorem_Curation_v5_3.json"),
    Path("Docs/catalog/v5/curation/Mathlib_Theorem_Curation_v5_4.json"),
)
CATALOG_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
OUTPUT_REL = Path("Docs/catalog/v5/curation/theorem_quality_v5_5/mathlib-important-inventory-1000.json")
EXPECTED_FILE_SHA256 = {
    SOURCE_REL: "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a",
    CURATION_RELS[0]: "379e165ae52ffd911e383fdb351fc602d36ec585e40bade54612c1512a7a1905",
    CURATION_RELS[1]: "0057a36999422726d6d490dbf59eca69824bc29a02f5117f9a02ebdd601dd386",
    CATALOG_REL: "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
}
MATHLIB_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
ALLOWED_SIGNALS = {"mathlib_1000_theorems", "mathlib_module_main_result"}


class BuildError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def encoded(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


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
        raise BuildError(message)


def load(relative: Path) -> dict[str, Any]:
    path = ROOT / relative
    require(file_sha(path) == EXPECTED_FILE_SHA256[relative], f"input digest drifted: {relative}")
    document = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(document, dict), f"input root is not an object: {relative}")
    return document


def build() -> dict[str, Any]:
    source_document = load(SOURCE_REL)
    curation_documents = [load(relative) for relative in CURATION_RELS]
    catalog_document = load(CATALOG_REL)

    source_records = source_document.get("records")
    require(isinstance(source_records, list) and len(source_records) == 1_500, "mathlib source denominator drifted")
    source_by_id: dict[str, dict[str, Any]] = {}
    for source_record in source_records:
        require(isinstance(source_record, dict), "mathlib source row is not an object")
        source_id = source_record.get("source_record_id")
        require(isinstance(source_id, str) and source_id not in source_by_id, "duplicate mathlib source id")
        source_by_id[source_id] = source_record

    catalog_records = catalog_document.get("records")
    require(isinstance(catalog_records, list) and len(catalog_records) == 4_100, "catalog denominator drifted")
    catalog_by_id = {record["stage_claim_id"]: record for record in catalog_records if isinstance(record, dict)}
    require(len(catalog_by_id) == 4_100, "catalog stage id duplication")

    selected_rows: list[tuple[str, dict[str, Any]]] = []
    for relative, curation in zip(CURATION_RELS, curation_documents, strict=True):
        require(curation.get("authority_sha256") == hash_without(curation, "authority_sha256"), f"curation seal drifted: {relative}")
        rows = curation.get("candidate_dispositions")
        require(isinstance(rows, list), f"curation rows missing: {relative}")
        accepted = [row for row in rows if row.get("disposition") == "accepted_new_kernel_checked_theorem"]
        require(len(accepted) == 500, f"accepted denominator drifted: {relative}")
        selected_rows.extend((relative.as_posix(), row) for row in accepted)
    require(len(selected_rows) == 1_000, "selected theorem denominator drifted")

    output_rows: list[dict[str, Any]] = []
    seen_source_ids: set[str] = set()
    seen_stage_ids: set[str] = set()
    seen_semantic_keys: set[str] = set()
    for curation_path, curation_row in selected_rows:
        require(curation_row.get("row_sha256") == hash_without(curation_row, "row_sha256"), "curation row digest mismatch")
        require(curation_row.get("grants_catalog_entry") is True and curation_row.get("grants_theorem_credit") is True, "selected curation row lacks theorem credit")
        require(curation_row.get("declaration_kind") == "theorem", "selected row is not a literal theorem")
        require(curation_row.get("formal_proof_state") == "kernel_checked_sorry_free", "selected row is not kernel checked")
        source_id = curation_row.get("source_record_id")
        stage_id = curation_row.get("target_s5_id")
        semantic_key = curation_row.get("semantic_key")
        require(isinstance(source_id, str) and source_id not in seen_source_ids, "selected source id duplicate")
        require(isinstance(stage_id, str) and stage_id not in seen_stage_ids, "selected stage id duplicate")
        require(isinstance(semantic_key, str) and semantic_key not in seen_semantic_keys, "selected semantic key duplicate")
        seen_source_ids.add(source_id)
        seen_stage_ids.add(stage_id)
        seen_semantic_keys.add(semantic_key)

        source_record = source_by_id.get(source_id)
        require(source_record is not None, f"missing source record: {source_id}")
        require(curation_row.get("source_record_sha256") == sha(canonical(source_record)), f"source row binding mismatch: {source_id}")
        require(curation_row.get("importance_payload_sha256") == sha(canonical(source_record.get("importance_signals"))), f"importance binding mismatch: {source_id}")
        require(curation_row.get("proof_evidence_payload_sha256") == sha(canonical(source_record.get("proof_evidence"))), f"proof binding mismatch: {source_id}")
        require(curation_row.get("rights_payload_sha256") == sha(canonical(source_record.get("rights"))), f"rights binding mismatch: {source_id}")
        require(source_record.get("declaration_kind") == "theorem", f"source declaration is not a theorem: {source_id}")
        require(source_record.get("formal_proof_state") == "kernel_checked_sorry_free", f"source proof state drifted: {source_id}")
        require(source_record.get("proof_evidence", {}).get("uses_sorry") is False, f"source uses sorry: {source_id}")
        require(source_record.get("material_status", {}).get("as_of_commit") == MATHLIB_COMMIT, f"source commit drifted: {source_id}")
        signals = source_record.get("importance_signals")
        require(isinstance(signals, list) and signals, f"importance signals missing: {source_id}")
        signal_kinds = sorted({signal.get("kind") for signal in signals if isinstance(signal, dict)})
        require(set(signal_kinds) <= ALLOWED_SIGNALS and set(signal_kinds), f"importance signal kind drifted: {source_id}")
        if "mathlib_1000_theorems" in signal_kinds:
            quality_tier = "human_curated_mathlib_1000_named_theorem"
        else:
            require("mathlib_module_main_result" in signal_kinds, f"module-main signal missing: {source_id}")
            quality_tier = "human_documented_mathlib_module_main_result"

        claim = catalog_by_id.get(stage_id)
        require(claim is not None, f"selected theorem absent from catalog: {stage_id}")
        require(claim.get("variant_id") == curation_row.get("target_variant_id"), f"variant binding mismatch: {stage_id}")
        require(claim.get("claim_kind") == "theorem" and claim.get("material_status") == "proved", f"catalog theorem status mismatch: {stage_id}")
        require(claim.get("semantic_key") == semantic_key, f"catalog semantic key mismatch: {stage_id}")
        require(claim.get("provenance", {}).get("source_record_id") == source_id, f"catalog source id mismatch: {stage_id}")
        require(claim.get("dedupe", {}).get("formal_type_sha256") == source_record.get("formal_type_sha256"), f"formal type binding mismatch: {stage_id}")
        require(claim.get("proof_evidence", {}).get("uses_sorry") is False, f"catalog proof uses sorry: {stage_id}")
        require(claim.get("theorem_selection", {}).get("importance_signals") == signals, f"catalog importance evidence mismatch: {stage_id}")

        row: dict[str, Any] = {
            "stage_claim_id": stage_id,
            "variant_id": claim["variant_id"],
            "family_id": claim["family_id"],
            "origin_release": claim["origin_release"],
            "display_name": claim["display_name"],
            "semantic_key": semantic_key,
            "source_record_id": source_id,
            "source_record_sha256": curation_row["source_record_sha256"],
            "curation_path": curation_path,
            "curation_row_sha256": curation_row["row_sha256"],
            "quality_tier": quality_tier,
            "importance_evidence": {
                "signal_kinds": signal_kinds,
                "signals": signals,
                "human_editorial_basis": "mathlib maintainers' 1000-theorem mapping or module Main statements documentation",
                "independent_universal_ranking_claimed": False,
                "operational_importance_credit": True,
            },
            "formal_evidence": {
                "declaration": source_record["declaration"],
                "formal_type_sha256": source_record["formal_type_sha256"],
                "formal_proof_state": "kernel_checked_sorry_free",
                "mathlib_commit": MATHLIB_COMMIT,
                "uses_sorry": False,
            },
            "rights": source_record["rights"],
            "grants_existing_important_theorem_credit": True,
            "grants_new_theorem_identity_credit": False,
            "grants_new_proof_credit": False,
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        output_rows.append(row)

    output_rows.sort(key=lambda row: row["stage_claim_id"])
    tiers = Counter(row["quality_tier"] for row in output_rows)
    origins = Counter(row["origin_release"] for row in output_rows)
    result: dict[str, Any] = {
        "schema_version": "awesome-theorems/mathlib-important-inventory/5.5",
        "review_as_of": "2026-08-10",
        "scope": {
            "kind": "quality qualification of 1,000 existing human-maintained mathlib theorem records",
            "importance_definition": "a human-curated mathlib 1000-theorem mapping or explicit module Main statements result",
            "not_a_universal_importance_ranking": True,
            "not_a_release_append": True,
            "new_theorem_identity_credit": 0,
        },
        "inputs": {
            relative.as_posix(): {"sha256": expected}
            for relative, expected in sorted(EXPECTED_FILE_SHA256.items(), key=lambda item: item[0].as_posix())
        },
        "counts": {
            "existing_important_theorem_credits": len(output_rows),
            "new_theorem_identity_credits": 0,
            "new_proof_credits": 0,
            "by_quality_tier": dict(sorted(tiers.items())),
            "by_origin_release": dict(sorted(origins.items())),
        },
        "set_digests": {
            "stage_claim_ids_sha256": set_digest(row["stage_claim_id"] for row in output_rows),
            "source_record_ids_sha256": set_digest(row["source_record_id"] for row in output_rows),
            "semantic_keys_sha256": set_digest(row["semantic_key"] for row in output_rows),
            "row_sha256_set_sha256": set_digest(row["row_sha256"] for row in output_rows),
        },
        "records": output_rows,
    }
    require(len(output_rows) == 1_000, "output denominator drifted")
    require(origins == Counter({"5.3": 500, "5.4": 500}), "origin partition drifted")
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise BuildError("choose exactly one of --write or --check")
    document = build()
    output = ROOT / OUTPUT_REL
    payload = encoded(document)
    if args.write:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(payload)
        print(
            f"wrote {OUTPUT_REL} important={document['counts']['existing_important_theorem_credits']} "
            f"new={document['counts']['new_theorem_identity_credits']} authority={document['authority_sha256']}"
        )
        return 0
    require(output.is_file(), f"missing output: {OUTPUT_REL}")
    require(output.read_bytes() == payload, "output is not a deterministic rebuild")
    print(
        f"PASS mathlib important inventory important={document['counts']['existing_important_theorem_credits']} "
        f"new={document['counts']['new_theorem_identity_credits']} authority={document['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
