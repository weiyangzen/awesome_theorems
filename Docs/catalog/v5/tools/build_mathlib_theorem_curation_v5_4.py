#!/usr/bin/env python3
"""Build the sealed residual mathlib theorem curation ledger for release 5.4.

The only candidate pool is the exact 731-row ``eligible_not_selected`` set
sealed by the 5.3 curation authority.  The builder joins those rows to the
fixed mathlib source asset, replays three independent mechanical identity
gates against both the residual pool and the complete 5.3 catalog, then takes
exactly 500 rows by bytewise module-root round-robin.  Literal Lean ``lemma``
rows never enter this pool and never receive quota credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unicodedata
from typing import Any, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[4]
V5_ROOT = REPO_ROOT / "Docs/catalog/v5"
SOURCE_PATH = V5_ROOT / "sources/mathlib-theorems-8a178386.json"
PARENT_LEDGER_PATH = V5_ROOT / "curation/Mathlib_Theorem_Curation_v5_3.json"
PARENT_CATALOG_PATH = V5_ROOT / "releases/5.3/Claim_Catalog.json"
PARENT_MANIFEST_PATH = V5_ROOT / "releases/5.3/Release_Manifest.json"
OUTPUT_PATH = V5_ROOT / "curation/Mathlib_Theorem_Curation_v5_4.json"

SCHEMA_VERSION = "awesome-theorems/mathlib-theorem-curation/5.4"
SOURCE_ID = "SRC-MATH-V5-MATHLIB-8A178386"
SOURCE_SHA256 = "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
SOURCE_SIZE_BYTES = 6_316_287
SOURCE_RECORDS = 1_500
PARENT_LEDGER_SHA256 = "379e165ae52ffd911e383fdb351fc602d36ec585e40bade54612c1512a7a1905"
PARENT_LEDGER_AUTHORITY = "9661eebbd25bbb8aee3a0c7ae1c9cbe671ec77324f889d25e967811ffd9f7d5d"
PARENT_CATALOG_SHA256 = "957da23fbd1e50244912fb6dbb76fbf663e7970ace3f6da8b19407929211a8bb"
PARENT_MANIFEST_SHA256 = "8384deebd8ff33cf06c592ed443fd3ed78a4a294c4cea106362705e95954419a"
PARENT_RELEASE_ROOT = "9ec5a097c0286b6751b02e89d18c400aab655021ba1ad4843eadba5a69fc41fa"
PARENT_VARIANT_HIGH_WATERMARK = 7_084
SELECTED_ROWS = 500
FIRST_VARIANT_ORDINAL = 7_085
LAST_VARIANT_ORDINAL = 7_584
RESIDUAL_ROWS = 731

EXPECTED_ROOT_COUNTS = {
    "Algebra": 13,
    "Analysis": 103,
    "FieldTheory": 64,
    "LinearAlgebra": 17,
    "MeasureTheory": 77,
    "NumberTheory": 67,
    "RingTheory": 103,
    "Topology": 56,
}
EXPECTED_REMAINING_ROOT_COUNTS = {"Analysis": 155, "RingTheory": 76}


class CurationError(RuntimeError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CurationError(f"not canonical-JSON serializable: {error}") from error


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return sha256_bytes(
        canonical_json_bytes({key: item for key, item in value.items() if key not in omitted})
    )


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(values)))


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CurationError(f"cannot load {path}: {error}") from error
    if not isinstance(value, dict):
        raise CurationError(f"{path} must contain one object")
    return value


def verify_authority(document: Mapping[str, Any], label: str) -> None:
    observed = document.get("authority_sha256")
    expected = hash_without(document, "authority_sha256")
    if observed != expected:
        raise CurationError(f"{label} has stale authority_sha256")


def normalized_formal_type(value: str) -> str:
    return " ".join(value.split())


def normalized_formal_type_sha256(value: str) -> str:
    return sha256_bytes(normalized_formal_type(value).encode("utf-8"))


def normalized_declaration(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().strip()


def normalized_declaration_sha256(value: str) -> str:
    return sha256_bytes(normalized_declaration(value).encode("utf-8"))


def module_root(source: Mapping[str, Any]) -> str:
    module = source.get("source", {}).get("module")
    if not isinstance(module, str):
        raise CurationError("source row lacks source.module")
    parts = module.split(".")
    if len(parts) < 2 or parts[0] != "Mathlib" or not parts[1]:
        raise CurationError(f"invalid mathlib module path: {module!r}")
    return parts[1]


def source_indexes(source_document: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows = source_document.get("records")
    if not isinstance(rows, list) or len(rows) != SOURCE_RECORDS or not all(
        isinstance(row, dict) for row in rows
    ):
        raise CurationError("fixed mathlib asset must contain exactly 1,500 object rows")
    by_id: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        source_id = row.get("source_record_id")
        if not isinstance(source_id, str) or source_id in by_id:
            raise CurationError(f"source row {index} has duplicate/invalid source_record_id")
        if row.get("selection_rank") != index + 1:
            raise CurationError("source asset selection ranks are not exactly 1..1500")
        by_id[source_id] = row
    return rows, by_id


def parent_identity_sets(records: Sequence[Mapping[str, Any]]) -> tuple[set[str], set[str], set[str]]:
    exact: set[str] = set()
    normalized: set[str] = set()
    names: set[str] = set()
    for row in records:
        formal = row.get("formal_statement")
        formal = formal if isinstance(formal, dict) else {}
        digest = formal.get("formal_type_sha256") or row.get("formal_type_sha256")
        text = formal.get("formal_type") or row.get("formal_type")
        name = formal.get("declaration") or row.get("qualified_name")
        if isinstance(digest, str):
            exact.add(digest)
        if isinstance(text, str):
            normalized.add(normalized_formal_type_sha256(text))
        if isinstance(name, str):
            names.add(normalized_declaration_sha256(name))
    return exact, normalized, names


def validate_source_row(row: Mapping[str, Any], source_id: str) -> None:
    required = {
        "declaration_kind": "theorem",
        "source_syntax_kind": "theorem",
        "formal_proof_state": "kernel_checked_sorry_free",
        "raw_category": "theorem",
        "raw_status": "lean_checked_thmInfo_sorry_free",
    }
    for field, expected in required.items():
        if row.get(field) != expected:
            raise CurationError(f"{source_id} fails literal-theorem gate {field}")
    proof = row.get("proof_evidence")
    material = row.get("material_status")
    rights = row.get("rights")
    if not isinstance(proof, dict) or proof.get("uses_sorry") is not False or proof.get(
        "verification"
    ) != "lean_checked_environment_thmInfo_and_collectAxioms_without_sorryAx":
        raise CurationError(f"{source_id} fails proof-evidence gate")
    if not isinstance(material, dict) or material.get("status") != "proved_formal" or material.get(
        "as_of_commit"
    ) != "8a178386ffc0f5fef0b77738bb5449d50efeea95":
        raise CurationError(f"{source_id} fails material-status gate")
    if not isinstance(rights, dict) or rights.get("source_license") != "Apache-2.0":
        raise CurationError(f"{source_id} fails rights gate")


def residual_pool(
    parent_ledger: Mapping[str, Any], source_by_id: Mapping[str, dict[str, Any]]
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows = parent_ledger.get("candidate_dispositions")
    if not isinstance(rows, list) or len(rows) != SOURCE_RECORDS:
        raise CurationError("5.3 curation row denominator changed")
    residual: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for index, parent_row in enumerate(rows):
        if not isinstance(parent_row, dict):
            raise CurationError(f"5.3 curation row {index} is not an object")
        if parent_row.get("row_sha256") != hash_without(parent_row, "row_sha256"):
            raise CurationError(f"5.3 curation row {index} has a stale row hash")
        if parent_row.get("disposition") != "eligible_not_selected":
            continue
        source_id = parent_row.get("source_record_id")
        source = source_by_id.get(source_id)
        if source is None:
            raise CurationError(f"residual row {source_id!r} has no source asset row")
        if parent_row.get("source_index") != int(source["selection_rank"]) - 1:
            raise CurationError(f"residual row {source_id} source index drifted")
        if parent_row.get("source_record_sha256") != sha256_bytes(canonical_json_bytes(source)):
            raise CurationError(f"residual row {source_id} source hash drifted")
        validate_source_row(source, str(source_id))
        residual.append((parent_row, source))
    if len(residual) != RESIDUAL_ROWS:
        raise CurationError(f"5.3 residual pool has {len(residual)} rows, expected 731")
    return residual


def enforce_three_gate_uniqueness(
    residual: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
    parent_records: Sequence[Mapping[str, Any]],
) -> None:
    exact_parent, normalized_parent, names_parent = parent_identity_sets(parent_records)
    gates: dict[str, list[str]] = {"exact": [], "normalized_type": [], "normalized_name": []}
    for _parent, source in residual:
        source_id = str(source["source_record_id"])
        exact = str(source["formal_type_sha256"])
        normalized = normalized_formal_type_sha256(str(source["formal_type"]))
        name = normalized_declaration_sha256(str(source["declaration"]))
        if exact in exact_parent:
            raise CurationError(f"residual source {source_id} duplicates parent exact formal type")
        if normalized in normalized_parent:
            raise CurationError(f"residual source {source_id} duplicates parent normalized formal type")
        if name in names_parent:
            raise CurationError(f"residual source {source_id} duplicates parent declaration name")
        gates["exact"].append(exact)
        gates["normalized_type"].append(normalized)
        gates["normalized_name"].append(name)
    for label, values in gates.items():
        if len(values) != len(set(values)):
            raise CurationError(f"residual pool is not unique under {label} gate")


def round_robin_select(
    residual: Sequence[tuple[dict[str, Any], dict[str, Any]]]
) -> tuple[list[tuple[dict[str, Any], dict[str, Any]]], list[tuple[dict[str, Any], dict[str, Any]]]]:
    buckets: dict[str, deque[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(deque)
    ordered: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    for pair in residual:
        ordered[module_root(pair[1])].append(pair)
    for root, pairs in ordered.items():
        pairs.sort(key=lambda pair: (int(pair[1]["selection_rank"]), str(pair[1]["source_record_id"])))
        buckets[root] = deque(pairs)
    roots = sorted(buckets)
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    while len(selected) < SELECTED_ROWS:
        progressed = False
        for root in roots:
            if buckets[root]:
                selected.append(buckets[root].popleft())
                progressed = True
                if len(selected) == SELECTED_ROWS:
                    break
        if not progressed:
            raise CurationError("round-robin pool exhausted before 500 selections")
    remaining = [pair for root in roots for pair in buckets[root]]
    selected_counts = Counter(module_root(source) for _parent, source in selected)
    remaining_counts = Counter(module_root(source) for _parent, source in remaining)
    if dict(sorted(selected_counts.items())) != EXPECTED_ROOT_COUNTS:
        raise CurationError(f"selected root distribution drifted: {dict(selected_counts)}")
    if dict(sorted(remaining_counts.items())) != EXPECTED_REMAINING_ROOT_COUNTS:
        raise CurationError(f"remaining root distribution drifted: {dict(remaining_counts)}")
    return selected, remaining


def build_document() -> dict[str, Any]:
    if sha256_file(SOURCE_PATH) != SOURCE_SHA256 or SOURCE_PATH.stat().st_size != SOURCE_SIZE_BYTES:
        raise CurationError("fixed mathlib source asset bytes drifted")
    if sha256_file(PARENT_LEDGER_PATH) != PARENT_LEDGER_SHA256:
        raise CurationError("5.3 curation bytes drifted")
    if sha256_file(PARENT_CATALOG_PATH) != PARENT_CATALOG_SHA256:
        raise CurationError("5.3 catalog bytes drifted")
    if sha256_file(PARENT_MANIFEST_PATH) != PARENT_MANIFEST_SHA256:
        raise CurationError("5.3 manifest bytes drifted")

    source_document = load_json(SOURCE_PATH)
    _source_rows, source_by_id = source_indexes(source_document)
    parent_ledger = load_json(PARENT_LEDGER_PATH)
    parent_catalog = load_json(PARENT_CATALOG_PATH)
    parent_manifest = load_json(PARENT_MANIFEST_PATH)
    verify_authority(parent_ledger, str(PARENT_LEDGER_PATH))
    verify_authority(parent_catalog, str(PARENT_CATALOG_PATH))
    verify_authority(parent_manifest, str(PARENT_MANIFEST_PATH))
    if parent_ledger.get("authority_sha256") != PARENT_LEDGER_AUTHORITY:
        raise CurationError("5.3 curation authority binding drifted")
    if parent_manifest.get("release_root_sha256") != PARENT_RELEASE_ROOT:
        raise CurationError("5.3 release-root binding drifted")
    parent_records = parent_catalog.get("records")
    if not isinstance(parent_records, list) or len(parent_records) != 3_600:
        raise CurationError("5.3 catalog must contain exactly 3,600 records")

    residual = residual_pool(parent_ledger, source_by_id)
    enforce_three_gate_uniqueness(residual, parent_records)
    selected, remaining = round_robin_select(residual)
    selected_rank = {
        str(source["source_record_id"]): rank
        for rank, (_parent, source) in enumerate(selected, start=1)
    }
    selected_ids = set(selected_rank)

    rows: list[dict[str, Any]] = []
    for parent_row, source in sorted(
        residual, key=lambda pair: (int(pair[1]["selection_rank"]), str(pair[1]["source_record_id"]))
    ):
        source_id = str(source["source_record_id"])
        rank = selected_rank.get(source_id)
        accepted = source_id in selected_ids
        ordinal = PARENT_VARIANT_HIGH_WATERMARK + rank if rank is not None else None
        semantic_key = "mathlib-theorem-semantic/" + str(source["formal_type_sha256"])
        row: dict[str, Any] = {
            "candidate_key": f"mathlib-v5.4:{source_id}",
            "source_index": int(source["selection_rank"]) - 1,
            "source_record_id": source_id,
            "source_record_sha256": sha256_bytes(canonical_json_bytes(source)),
            "parent_curation_row_sha256": parent_row["row_sha256"],
            "declaration": source["declaration"],
            "declaration_kind": source["declaration_kind"],
            "source_syntax_kind": source["source_syntax_kind"],
            "selection_rank": source["selection_rank"],
            "selection_cohort": source["selection_cohort"],
            "module_root": module_root(source),
            "formal_proof_state": source["formal_proof_state"],
            "formal_type_sha256": source["formal_type_sha256"],
            "normalized_formal_type_sha256": normalized_formal_type_sha256(str(source["formal_type"])),
            "normalized_declaration_name_sha256": normalized_declaration_sha256(str(source["declaration"])),
            "proof_evidence_payload_sha256": sha256_bytes(canonical_json_bytes(source["proof_evidence"])),
            "importance_payload_sha256": sha256_bytes(canonical_json_bytes(source["importance_signals"])),
            "rights_payload_sha256": sha256_bytes(canonical_json_bytes(source["rights"])),
            "semantic_key": semantic_key,
            "disposition": (
                "accepted_new_kernel_checked_theorem"
                if accepted
                else "eligible_not_selected_after_5_4"
            ),
            "reason_code": (
                "selected_remaining_module_root_round_robin"
                if accepted
                else "viable_theorem_outside_exact_5_4_selection"
            ),
            "accepted_rank": rank,
            "target_variant_id": f"ATV-{ordinal:08d}" if ordinal is not None else None,
            "target_s5_id": f"S5-CLM-{ordinal:08d}" if ordinal is not None else None,
            "grants_catalog_entry": accepted,
            "grants_theorem_credit": accepted,
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        rows.append(row)

    accepted_rows = sorted(
        (row for row in rows if row["grants_theorem_credit"]),
        key=lambda row: int(row["accepted_rank"]),
    )
    if [row["target_variant_id"] for row in accepted_rows] != [
        f"ATV-{ordinal:08d}" for ordinal in range(FIRST_VARIANT_ORDINAL, LAST_VARIANT_ORDINAL + 1)
    ]:
        raise CurationError("accepted target ATV suffix is not exactly 7085..7584")

    counts = {
        "parent_source_rows": SOURCE_RECORDS,
        "parent_literal_lemma_noncredit_rows": 265,
        "parent_literal_theorem_rows": 1_235,
        "parent_5_3_accepted_rows": 500,
        "parent_source_duplicate_noncredit_rows": 4,
        "residual_unique_literal_theorem_rows": len(rows),
        "accepted": len(accepted_rows),
        "eligible_not_selected_after_5_4": len(remaining),
        "selected_by_module_root": dict(
            sorted(Counter(row["module_root"] for row in accepted_rows).items())
        ),
        "remaining_by_module_root": dict(
            sorted(
                Counter(module_root(source) for _parent, source in remaining).items()
            )
        ),
    }
    document: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "release": "5.4",
        "parent_release": "5.3",
        "source_id": SOURCE_ID,
        "source_asset_sha256": SOURCE_SHA256,
        "source_asset_size_bytes": SOURCE_SIZE_BYTES,
        "parent_curation": {
            "path": "Docs/catalog/v5/curation/Mathlib_Theorem_Curation_v5_3.json",
            "file_sha256": PARENT_LEDGER_SHA256,
            "authority_sha256": PARENT_LEDGER_AUTHORITY,
            "required_source_disposition": "eligible_not_selected",
        },
        "parent_release_binding": {
            "release_root_sha256": PARENT_RELEASE_ROOT,
            "manifest_file_sha256": PARENT_MANIFEST_SHA256,
            "catalog_file_sha256": PARENT_CATALOG_SHA256,
            "variant_high_watermark": PARENT_VARIANT_HIGH_WATERMARK,
        },
        "selection_policy": {
            "candidate_denominator": "exact 731-row eligible_not_selected set sealed by the 5.3 curation ledger",
            "identity_gates": [
                "exact formal_type_sha256",
                "Unicode-whitespace normalized formal type",
                "Unicode NFKC-casefolded full declaration name",
            ],
            "parent_scope": "entire 3,600-record release 5.3 Claim_Catalog",
            "module_root": "first component after Mathlib in source.module",
            "root_order": "ascending UTF-8/Unicode codepoint order, identical to Python sorted strings for these ASCII roots",
            "bucket_order": "ascending selection_rank then source_record_id",
            "sweep": "take at most one row per nonempty root per sweep until exactly 500",
            "exact_selected_rows": SELECTED_ROWS,
            "literal_lemma_grants_quota": False,
            "expected_selected_by_module_root": EXPECTED_ROOT_COUNTS,
        },
        "counts": counts,
        "set_digests": {
            "residual_source_record_id_set_sha256": set_digest(row["source_record_id"] for row in rows),
            "residual_exact_formal_type_set_sha256": set_digest(row["formal_type_sha256"] for row in rows),
            "residual_normalized_formal_type_set_sha256": set_digest(row["normalized_formal_type_sha256"] for row in rows),
            "residual_normalized_declaration_set_sha256": set_digest(row["normalized_declaration_name_sha256"] for row in rows),
            "selected_source_record_id_set_sha256": set_digest(row["source_record_id"] for row in accepted_rows),
            "selected_declaration_set_sha256": set_digest(row["declaration"] for row in accepted_rows),
            "selected_formal_type_sha256_set_sha256": set_digest(row["formal_type_sha256"] for row in accepted_rows),
            "selected_semantic_key_set_sha256": set_digest(row["semantic_key"] for row in accepted_rows),
            "selected_variant_id_set_sha256": set_digest(row["target_variant_id"] for row in accepted_rows),
            "selected_s5_id_set_sha256": set_digest(row["target_s5_id"] for row in accepted_rows),
            "candidate_row_sha256_set_sha256": set_digest(row["row_sha256"] for row in rows),
        },
        "candidate_dispositions": rows,
    }
    document["authority_sha256"] = hash_without(document, "authority_sha256")
    return document


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        document = build_document()
        payload = encoded_document(document)
        if args.check:
            if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_bytes() != payload:
                raise CurationError(f"{OUTPUT_PATH} is missing or stale")
            print(
                "PASS mathlib curation 5.4: residual=731 accepted=500 "
                f"remaining=231 authority={document['authority_sha256']}"
            )
            return 0
        atomic_write(OUTPUT_PATH, payload)
        print(
            f"WROTE {OUTPUT_PATH}: accepted=500 authority={document['authority_sha256']}"
        )
        return 0
    except CurationError as error:
        print(f"ERROR: {error}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
