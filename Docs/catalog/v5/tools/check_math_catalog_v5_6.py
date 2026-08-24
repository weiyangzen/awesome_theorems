#!/usr/bin/env python3
"""Independent acceptance checker for the append-only Stage5 5.6 release.

This module intentionally does not import the 5.6 generator.  It authenticates
the complete 5.5 parent, replays the sealed mathlib selection/allocation join,
reconstructs every origin-5.6 claim from the pinned source, checks all parent
prefixes and identity namespaces, and recomputes the manifest and release root.

Ordinary operation is read-only.  ``--write-receipt`` is the only write mode
and has one fixed target: ``receipts/V5_6_Independent_Acceptance_Receipt.json``.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata
from typing import Any, Iterable, Mapping, Sequence


V5_REL = Path("Docs/catalog/v5")
PARENT_REL = V5_REL / "releases/5.5"
RELEASE_REL = V5_REL / "releases/5.6"
CURRENT_REL = V5_REL / "Current_Release.json"
RECEIPT_REL = V5_REL / "receipts/V5_6_Independent_Acceptance_Receipt.json"
CONTRACT_REL = V5_REL / "Stage5_Math_Expansion_Contract_v5_6.json"
SCHEMA_REL = V5_REL / "Math_Claim_Record_Schema_v5_6.json"
SOURCE_REGISTRY_REL = V5_REL / "Math_Source_Registry_v5_6.json"
PARENT_RECEIPT_REL = V5_REL / "V5_5_Parent_Receipt_v5_6.json"
RESERVE_REL = V5_REL / "curation/mathlib_reserve_v5_6"
FULL_SOURCE_REL = RESERVE_REL / "mathlib-verified-theorems-8a178386-full.json"
QUALIFIED_REL = RESERVE_REL / "Mathlib_Qualified_Theorem_Candidates_v5_6.jsonl"
QUALIFIED_INVENTORY_REL = RESERVE_REL / "Mathlib_Qualified_Batch_Inventory_v5_6.json"
ACCEPTED_REL = RESERVE_REL / "Mathlib_Generator_Accepted_Set_v5_6.jsonl"
GENERATOR_RECEIPT_REL = RESERVE_REL / "Mathlib_Generator_Acceptance_Receipt_v5_6.json"
SELECTION_REL = RESERVE_REL / "Mathlib_Release_Selection_v5_6.json"
SELECTION_RECEIPT_REL = RESERVE_REL / "Mathlib_Release_Selection_Acceptance_Receipt_v5_6.json"
ALLOCATION_REL = RESERVE_REL / "Mathlib_Release_Allocation_v5_6.json"
CHECKER_REL = V5_REL / "tools/check_math_catalog_v5_6.py"

RELEASE = "5.6"
PARENT_RELEASE = "5.5"
SOURCE_ID = "SRC-MATH-V5-MATHLIB-8A178386-FULL"
MATHLIB_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"

PARENT_ROOT = "fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0"
PARENT_MANIFEST_SHA = "773253c2afad3a91c1b14cc9b5f60b51ec9b7e258d1619f0168dd23c9c4b0a43"
PARENT_MANIFEST_AUTHORITY = "751c3f9f03d1c2ce3cb31f83834a223c11d269ddc257412ff7172da8138fc724"
PARENT_CATALOG_SHA = "9d6dc79b1cbdee401f2f022ee027557a04331fa9605dc7f443fdc09a62b029b4"
PARENT_REGISTRY_AUTHORITY = "c19b24eee38ecba5634b1420da3f737694bce4a0732f3b5ca7a5cc9f9f40d203"
PARENT_CURRENT_SHA = "d7237b2877787fb18068b0d8b9504e90cc81ad0d58806b413b10dfb12d9cacce"

FULL_SOURCE_SHA = "7075e0bb151182ae4ba01cd34945657969be4bc60f7ee4ae6a62fc518f5386c3"
FULL_SOURCE_SIZE = 10_473_933
FULL_SOURCE_CONTENT_DIGEST = "cd54f6600e733f780153ba8d5f0d08994cb13cdd0ece1d63697f33e4eddf2ece"
QUALIFIED_SHA = "b03a2a3df17165b7f1e4bff7e2de80a8ecea6060a115b0fed66975827fb0f039"
QUALIFIED_INVENTORY_SHA = "669ad0d5b3f7d4b26000ffc36c153f5d415fdce4f7824f85177d999a80d34ab9"
QUALIFIED_INVENTORY_AUTHORITY = "879111d857fc5ce18a4baaf1cc1e98a3aee524f9c7dd5a7736dbd2ca61d370e1"
ACCEPTED_SHA = "7943e8f473aaac523d617a8debd1dda5d589187bf62844933af684172570ab86"
GENERATOR_RECEIPT_SHA = "cc3236b5b91976d9ec876548ee7de6289313c7737d1ffeee019ba1f16916a7a4"
GENERATOR_RECEIPT_AUTHORITY = "c528aba0e081b912c4102e1fea1c54e5adda49662c0bde9a94c994bddb27ebe5"
SELECTION_SHA = "f9c320c702b477308e6b0c392ff8aa7fcc4440e676e058e0b55ac1134cc6e91e"
SELECTION_AUTHORITY = "7ab83a5d3e2aebe1954c6c49cc5d3904c577ff9f6690f8ce2ddf944e76ed7b59"
SELECTION_RECEIPT_SHA = "b226b700df245ef962ca1c6ad97bac11b427e47ac731c4ecceb94492e930d9bf"
SELECTION_RECEIPT_AUTHORITY = "cbdadef86f9ba1263ef7c46952142dfde652fe9a28aa66cc0a846f024c3ea578"
ALLOCATION_SHA = "eebebdd7961806c4f9f4dd87e171fd522d0bc0ccd4d59bddd2bcc55f9076f02e"
ALLOCATION_AUTHORITY = "7fb9d5fe669e2c4ae476573642dc5ab6111932a72e2d5ade7acc37ee1868a0a9"
SCHEMA_SHA = "6e5915d331a908e4e8224f3e4bd739459ec8b105575cf48050730d700259c790"
SCHEMA_AUTHORITY = "619e9f261164bd2728e018298e1006f3ad626fc2e00825b6154d2dd25ef7e1fb"
SOURCE_REGISTRY_SHA = "591555abc29510f0ffd9330acd7531fc79d136251c0e19496372c185a2991442"
SOURCE_REGISTRY_AUTHORITY = "d82830e054cf47e147c5a19909ddc0ecb47d048b3af1aa585b302b9513917034"
PARENT_RECEIPT_SHA = "1c87cc939a11f7886b101d0d76565a2c696a511fc075876025d883ce0a0508c4"
PARENT_RECEIPT_AUTHORITY = "6c495d3f05a9fac4fafaa918a6695c436126997fbee05ece4d1c8f219c1bc6fb"
CONTRACT_SHA = "bcc6311eb345db799b9448ef5af6d6ac205bde94d970644707fbd9ba79d280d9"
CONTRACT_AUTHORITY = "bb24bf4cae40ec966d0426f1d28c77a19974ea68b8e232083ee6c49a54dc09de"

PARENT_CATALOG_ROWS = 4_525
PARENT_THEOREM_ROWS = 2_500
PARENT_OPEN_ROWS = 2_025
PARENT_COVERAGE_ROWS = 6_323
PARENT_ATV_HIGH = 8_009
PARENT_ATF_HIGH = 7_779
NEW_ROWS = 1_000
QUALIFIED_ROWS = 1_561
READY_ROWS = 1_092
QUARANTINE_ROWS = 469
TERMINAL_ROWS = 92
INDIVIDUAL_ROWS = 511
BALANCED_ROWS = 489
LAST_ATV = 9_009
LAST_ATF = 8_779

RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
    "Strict_Conjecture_Ledger.json",
)
MANIFEST_NAME = "Release_Manifest.json"
ALL_RELEASE_FILES = frozenset((*RELEASE_FILES, MANIFEST_NAME))

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
ATF_RE = re.compile(r"^ATF-([0-9]{8})$")
ATO_RE = re.compile(r"^ATO-([0-9]{8})$")
ATS_RE = re.compile(r"^ATS-([0-9]{8})$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")

EXPECTED_COUNTS = {
    "non_manifest_artifacts": 8,
    "catalog_records": 5_525,
    "origin_theorems": 1_000,
    "origin_open_claims": 0,
    "origin_strict_conjectures": 0,
    "cumulative_theorems": 3_500,
    "cumulative_open_claims": 2_025,
    "effective_strict_conjecture_credits": 1_425,
    "net_strict_increase_after_5_0": 1_024,
    "terminal_ready_unselected": 92,
    "preserved_quarantine": 469,
    "canonical_variants": 9_009,
    "variants": 9_009,
}


class CheckError(RuntimeError):
    """An authenticated or semantic release invariant failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def reject_constant(token: str) -> None:
    raise CheckError(f"non-finite JSON token is forbidden: {token}")


def closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CheckError(f"value is not canonical JSON: {error}") from error


def encoded(value: Any) -> bytes:
    return canonical(value) + b"\n"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_sha(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in omitted}))


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop("authority_sha256", None)
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def seal_field(value: Mapping[str, Any], field: str, *also_omit: str) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop(field, None)
    result[field] = hash_without(result, field, *also_omit)
    return result


def row_hash(value: Mapping[str, Any]) -> str:
    return hash_without(value, "row_sha256")


def set_digest(values: Iterable[str]) -> str:
    return digest(canonical(sorted(values)))


def normalize_type(value: str) -> str:
    return " ".join(value.split())


def normalize_name(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().strip()


def normalized_type_sha(value: str) -> str:
    return digest(normalize_type(value).encode("utf-8"))


def normalized_name_sha(value: str) -> str:
    return digest(normalize_name(value).encode("utf-8"))


def repo_root(value: Path) -> Path:
    absolute = value.absolute()
    require(not absolute.is_symlink() and absolute == absolute.resolve(),
            f"symlinked/aliased repository root is forbidden: {value}")
    try:
        root = value.resolve(strict=True)
    except OSError as error:
        raise CheckError(f"repository root does not exist: {value}") from error
    require(root.is_dir(), f"repository root is not a directory: {root}")
    return root


def safe_path(root: Path, relative: Path | str, *, file: bool = True) -> Path:
    raw = Path(relative)
    require(not raw.is_absolute() and raw.parts and ".." not in raw.parts, f"unsafe path: {relative}")
    cursor = root
    for component in raw.parts:
        cursor = cursor / component
        require(not cursor.is_symlink(), f"symlinked authoritative path is forbidden: {relative}")
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise CheckError(f"path escapes repository root: {relative}") from error
    require(candidate.is_file() if file else candidate.is_dir(),
            f"required {'file' if file else 'directory'} is missing: {relative}")
    return candidate


def relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError as error:
        raise CheckError(f"path is outside repository root: {path}") from error


def parse_document_bytes(raw: bytes, label: str, *, canonical_file: bool = True) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=closed_object, parse_constant=reject_constant
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"invalid JSON in {label}: {error}") from error
    require(isinstance(value, dict), f"{label} must contain one object")
    if canonical_file:
        require(raw == encoded(value), f"{label} is not canonical JSON plus one LF")
    return value


def load_json(root: Path, relative_path: Path | str, *, canonical_file: bool = True) -> dict[str, Any]:
    path = safe_path(root, relative_path)
    return parse_document_bytes(path.read_bytes(), str(relative_path), canonical_file=canonical_file)


def load_jsonl(
    root: Path, relative_path: Path, *, expected_sha: str, expected_rows: int
) -> list[dict[str, Any]]:
    path = safe_path(root, relative_path)
    payload = path.read_bytes()
    require(digest(payload) == expected_sha, f"{relative_path.name} SHA-256 drifted")
    rows: list[dict[str, Any]] = []
    for number, raw in enumerate(payload.splitlines(), 1):
        require(bool(raw), f"{relative_path.name} line {number} is blank")
        row = parse_document_bytes(raw, f"{relative_path}:{number}", canonical_file=False)
        require(raw == canonical(row), f"{relative_path.name} line {number} is not canonical JSON")
        require(row.get("row_sha256") == row_hash(row),
                f"{relative_path.name} line {number} row seal is stale")
        rows.append(row)
    require(len(rows) == expected_rows, f"{relative_path.name} row count drifted")
    return rows


def verify_seal(document: Mapping[str, Any], label: str) -> None:
    authority = document.get("authority_sha256")
    require(isinstance(authority, str) and SHA_RE.fullmatch(authority) is not None,
            f"{label} authority is malformed")
    require(authority == hash_without(document, "authority_sha256"), f"{label} authority is stale")


def require_pinned_file(root: Path, rel: Path, expected_sha: str, *, size: int | None = None) -> Path:
    path = safe_path(root, rel)
    require(file_sha(path) == expected_sha, f"{rel} file SHA-256 drifted")
    if size is not None:
        require(path.stat().st_size == size, f"{rel} byte size drifted")
    return path


def primary_rows(name: str, document: Mapping[str, Any]) -> int:
    key = {
        "Claim_Catalog.json": "records",
        "Claim_ID_Registry.json": "variants",
        "Stage5_Claim_ID_Registry.json": "mappings",
        "Migration_v4_to_v5.json": "migrations",
        "Theorem_List.json": "records",
        "Open_Claim_List.json": "records",
        "Coverage_Ledger.json": "candidate_dispositions",
        "Strict_Conjecture_Ledger.json": "strict_credits",
    }[name]
    rows = document.get(key)
    require(isinstance(rows, list), f"{name}.{key} is not an array")
    count = len(rows)
    # Preserve the established manifest row-count meaning from release 5.5:
    # every primary ledger row is counted, not only its largest array.
    if name == "Coverage_Ledger.json":
        extra = document.get("msc_coverage")
        require(isinstance(extra, list), "Coverage_Ledger.json.msc_coverage is not an array")
        count += len(extra)
    elif name == "Strict_Conjecture_Ledger.json":
        extra = document.get("credit_corrections")
        require(isinstance(extra, list),
                "Strict_Conjecture_Ledger.json.credit_corrections is not an array")
        count += len(extra)
    return count


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    rows = [
        {"path": row["path"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}
        for row in inventory
    ]
    return digest(canonical(sorted(rows, key=lambda row: row["path"])))


def validate_manifest_inventory_shape(manifest: Mapping[str, Any]) -> None:
    rows = manifest.get("artifacts")
    require(isinstance(rows, list) and len(rows) == len(RELEASE_FILES),
            "manifest artifact denominator drifted")
    require(all(isinstance(row, dict) and set(row) == {"path", "sha256", "size_bytes", "row_count"}
                for row in rows), "manifest artifact row closure drifted")
    require([row["path"] for row in rows] == sorted(RELEASE_FILES),
            "manifest artifact set/order drifted")


def validate_manifest_bindings(
    manifest: Mapping[str, Any], documents: Mapping[str, Mapping[str, Any]],
    payloads: Mapping[str, bytes] | None = None,
) -> None:
    validate_manifest_inventory_shape(manifest)
    observed: list[dict[str, Any]] = []
    for binding in manifest["artifacts"]:
        name = binding["path"]
        require(name in documents, f"manifest names missing document: {name}")
        payload = payloads[name] if payloads is not None else encoded(documents[name])
        wanted = {
            "path": name,
            "sha256": digest(payload),
            "size_bytes": len(payload),
            "row_count": primary_rows(name, documents[name]),
        }
        require(binding == wanted, f"manifest binding drifted: {name}")
        observed.append(wanted)
    require(release_root(observed) == manifest.get("release_root_sha256"),
            "release root does not recompute")


def validate_parent_prefix(
    child: Sequence[Mapping[str, Any]], parent: Sequence[Mapping[str, Any]], label: str
) -> None:
    require(len(child) >= len(parent) and list(child[:len(parent)]) == list(parent),
            f"{label} parent prefix changed")


def authenticated_parent_pointer() -> dict[str, Any]:
    return {
        "authority_sha256": "518e6d9179f37cf0d895e022f521e16e2ad8430cdaae022fc6945381cd91f41e",
        "manifest_path": "releases/5.5/Release_Manifest.json",
        "manifest_sha256": PARENT_MANIFEST_SHA,
        "release": PARENT_RELEASE,
        "release_root_sha256": PARENT_ROOT,
        "schema_version": "awesome-theorems/stage5-current-release/5.5",
    }


def check_parent(root: Path) -> dict[str, dict[str, Any]]:
    directory = safe_path(root, PARENT_REL, file=False)
    entries = list(directory.iterdir())
    require(all(path.is_file() and not path.is_symlink() for path in entries),
            "5.5 parent contains a non-regular/symlink entry")
    require({path.name for path in entries} == ALL_RELEASE_FILES,
            "5.5 parent release has missing/extra files")
    require_pinned_file(root, PARENT_REL / MANIFEST_NAME, PARENT_MANIFEST_SHA)
    require_pinned_file(root, PARENT_REL / "Claim_Catalog.json", PARENT_CATALOG_SHA)
    documents = {name: load_json(root, PARENT_REL / name) for name in ALL_RELEASE_FILES}
    for name, document in documents.items():
        verify_seal(document, f"5.5 {name}")
    manifest = documents[MANIFEST_NAME]
    require(manifest.get("authority_sha256") == PARENT_MANIFEST_AUTHORITY,
            "5.5 manifest authority drifted")
    require(manifest.get("release_root_sha256") == PARENT_ROOT,
            "5.5 release root drifted")
    payloads = {name: safe_path(root, PARENT_REL / name).read_bytes() for name in RELEASE_FILES}
    validate_manifest_bindings(manifest, documents, payloads)
    require(manifest.get("counts") == {
        "catalog_records": 4_525,
        "cumulative_open_claims": 2_025,
        "cumulative_theorems": 2_500,
        "effective_strict_conjecture_credits": 1_425,
        "net_strict_increase_after_5_0": 1_024,
        "non_manifest_artifacts": 8,
        "origin_open_claims": 425,
        "origin_strict_conjectures": 425,
        "origin_theorems": 0,
    }, "5.5 parent manifest counts drifted")
    registry = documents["Claim_ID_Registry.json"]
    require(registry.get("authority_sha256") == PARENT_REGISTRY_AUTHORITY,
            "5.5 registry authority drifted")
    require(registry.get("namespace_high_watermarks") == {
        "ATF": PARENT_ATF_HIGH, "ATO": PARENT_ATV_HIGH,
        "ATS": PARENT_ATV_HIGH, "ATV": PARENT_ATV_HIGH,
    }, "5.5 namespace high-watermarks drifted")
    require(len(documents["Claim_Catalog.json"].get("records", [])) == PARENT_CATALOG_ROWS,
            "5.5 catalog denominator drifted")
    require(len(documents["Theorem_List.json"].get("records", [])) == PARENT_THEOREM_ROWS,
            "5.5 theorem denominator drifted")
    require(len(documents["Open_Claim_List.json"].get("records", [])) == PARENT_OPEN_ROWS,
            "5.5 open denominator drifted")
    require(len(documents["Coverage_Ledger.json"].get("candidate_dispositions", []))
            == PARENT_COVERAGE_ROWS, "5.5 coverage denominator drifted")
    return documents


def validate_full_source(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    require(document.get("content_digest_before_self_field") == FULL_SOURCE_CONTENT_DIGEST,
            "full source content digest drifted")
    snapshot = document.get("source_snapshot")
    require(isinstance(snapshot, dict) and snapshot.get("commit") == MATHLIB_COMMIT,
            "full source mathlib commit drifted")
    rows = document.get("records")
    require(isinstance(rows, list) and len(rows) == 2_566
            and all(isinstance(row, dict) for row in rows), "full source denominator drifted")
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    for index, row in enumerate(rows):
        source_id = row.get("source_record_id")
        declaration = row.get("declaration")
        formal_type = row.get("formal_type")
        syntax = row.get("source_syntax_kind")
        require(isinstance(source_id, str) and source_id not in seen_ids,
                f"full source ID invalid at index {index}")
        require(isinstance(declaration, str) and bool(declaration),
                f"full source declaration missing at index {index}")
        normalized_name = normalize_name(declaration)
        require(normalized_name not in seen_names,
                f"full source declaration name duplicated: {declaration}")
        expected_id = "ML4-" + digest(
            f"{MATHLIB_COMMIT}\0{declaration}".encode("utf-8"))[:20].upper()
        require(source_id == expected_id and row.get("selection_rank") == index + 1,
                f"full source ID/rank formula drifted at index {index}")
        require(isinstance(formal_type, str)
                and row.get("formal_type_sha256") == digest(formal_type.encode("utf-8")),
                f"full source formal type binding drifted at index {index}")
        require(syntax in {"theorem", "lemma"}
                and row.get("declaration_kind") == syntax
                and row.get("raw_category") == syntax,
                f"full source syntax boundary drifted at index {index}")
        proof = row.get("proof_evidence")
        require(row.get("formal_proof_state") == "kernel_checked_sorry_free"
                and row.get("raw_status") == "lean_checked_thmInfo_sorry_free"
                and isinstance(proof, dict)
                and proof.get("uses_sorry") is False
                and proof.get("verification")
                == "lean_checked_environment_thmInfo_and_collectAxioms_without_sorryAx"
                and isinstance(proof.get("batch_axiom_dependency_union"), list)
                and "sorryAx" not in proof["batch_axiom_dependency_union"],
                f"full source proof gate failed at index {index}")
        material = row.get("material_status")
        require(isinstance(material, dict) and material.get("status") == "proved_formal"
                and material.get("basis")
                == "Loaded from the pinned compiled mathlib environment as Lean.ConstantInfo.thmInfo."
                and material.get("as_of_commit") == MATHLIB_COMMIT,
                f"full source ConstantInfo.thmInfo material gate failed at index {index}")
        seen_ids.add(source_id)
        seen_names.add(normalized_name)
    return list(rows)


def validate_selection(
    selection: Mapping[str, Any], qualified: Sequence[Mapping[str, Any]],
    accepted: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    verify_seal(selection, "mathlib release selection")
    require(selection.get("authority_sha256") == SELECTION_AUTHORITY,
            "mathlib release selection authority drifted")
    require(selection.get("schema_version") == "awesome-theorems/mathlib-release-selection/5.6"
            and selection.get("release") == RELEASE
            and selection.get("parent_release_root_sha256") == PARENT_ROOT,
            "mathlib release selection header drifted")
    require(selection.get("release_credit_granted_here") is False
            and selection.get("ids_allocated_here") is False
            and selection.get("candidate_denominator_closed") is True,
            "selection crossed its non-credit boundary")
    expected_counts = {
        "qualified_denominator": 1_561,
        "ready_denominator": 1_092,
        "selected": 1_000,
        "selected_individual_declaration_docstring": 511,
        "selected_module_main_result_description": 489,
        "selected_source_syntax_theorem": 629,
        "selected_source_syntax_lemma": 371,
        "terminal_ready_unselected": 92,
        "terminal_ready_unselected_analysis": 15,
        "terminal_ready_unselected_ring_theory": 77,
        "preserved_quarantine": 469,
    }
    require(selection.get("counts") == expected_counts, "selection counts drifted")
    dispositions = selection.get("candidate_dispositions")
    require(isinstance(dispositions, list) and len(dispositions) == QUALIFIED_ROWS,
            "selection disposition denominator drifted")
    require(len(qualified) == QUALIFIED_ROWS and len(accepted) == READY_ROWS,
            "qualified/ready denominator drifted")
    source_by_id = {row["source_record_id"]: row for row in source_rows}
    require(len(source_by_id) == len(source_rows), "full source IDs are not unique")
    accepted_by_key = {row["candidate_key"]: row for row in accepted}
    require(len(accepted_by_key) == READY_ROWS, "ready candidate keys are not unique")
    selected: list[dict[str, Any]] = []
    candidate_keys: set[str] = set()
    source_ids: set[str] = set()
    for index, (row, qualified_row) in enumerate(zip(dispositions, qualified, strict=True), 1):
        require(isinstance(row, dict) and row.get("row_sha256") == row_hash(row),
                f"selection row {index} seal is stale")
        key = row.get("candidate_key")
        require(isinstance(key, str) and key not in candidate_keys,
                f"selection candidate key duplicated at row {index}")
        require(row.get("qualified_candidate_index") == index
                and row.get("qualified_candidate_row_sha256") == qualified_row.get("row_sha256")
                and key == qualified_row.get("candidate_key"),
                f"selection-to-qualified binding drifted at row {index}")
        binding = qualified_row.get("source_binding")
        require(isinstance(binding, dict), f"qualified source binding missing at row {index}")
        source_id = binding.get("source_record_id")
        require(isinstance(source_id, str) and source_id not in source_ids,
                f"qualified source ID duplicated at row {index}")
        source = source_by_id.get(source_id)
        require(source is not None
                and binding.get("source_index_zero_based") == row.get("source_index")
                and source_rows[row["source_index"]] == source
                and binding.get("source_record_sha256") == digest(canonical(source))
                and row.get("source_record_sha256") == binding.get("source_record_sha256")
                and row.get("formal_type_sha256") == source.get("formal_type_sha256")
                and row.get("declaration") == source.get("declaration")
                and row.get("source_syntax_kind") == source.get("source_syntax_kind"),
                f"selection source binding drifted at row {index}")
        require(row.get("grants_catalog_entry") is False
                and row.get("grants_theorem_credit") is False
                and row.get("target_variant_id") is None
                and row.get("target_s5_id") is None,
                f"selection row {index} grants premature credit/identity")
        ready = accepted_by_key.get(key)
        if row.get("selected_for_joint_release_transaction") is True:
            require(ready is not None
                    and row.get("ready_candidate_row_sha256") == ready.get("row_sha256")
                    and row.get("disposition") == "selected_for_joint_5_6_release_transaction",
                    f"selected row {index} ready/rank binding drifted")
            selected.append(dict(row))
        candidate_keys.add(key)
        source_ids.add(source_id)
    selected.sort(key=lambda row: row["accepted_rank"])
    require(len(selected) == NEW_ROWS
            and [row["accepted_rank"] for row in selected] == list(range(1, NEW_ROWS + 1)),
            "selected acceptance ranks are not dense")
    require(Counter(row["source_syntax_kind"] for row in selected)
            == Counter({"theorem": 629, "lemma": 371}),
            "theorem/lemma source-syntax partition drifted")
    require(Counter(row["selection_phase"] for row in selected)
            == Counter({"individual_declaration_docstring_priority": 511,
                        "module_root_round_robin": 489}),
            "selection phase partition drifted")
    counts = Counter(row.get("disposition") for row in dispositions)
    require(counts == Counter({
        "selected_for_joint_5_6_release_transaction": 1_000,
        "terminal_ready_unselected_in_5_6": 92,
        "preserved_semantic_variant_review_quarantine": 469,
    }), "selection terminal disposition counts drifted")
    wanted_digests = {
        "all_disposition_row_sha256_set_sha256": set_digest(row["row_sha256"] for row in dispositions),
        "selected_candidate_key_set_sha256": set_digest(row["candidate_key"] for row in selected),
        "selected_formal_type_sha256_set_sha256": set_digest(row["formal_type_sha256"] for row in selected),
        "selected_source_record_id_set_sha256": set_digest(row["source_record_id"] for row in selected),
        "selected_acceptance_rank_set_sha256": set_digest(str(row["accepted_rank"]) for row in selected),
        "terminal_ready_candidate_key_set_sha256": set_digest(
            row["candidate_key"] for row in dispositions
            if row["disposition"] == "terminal_ready_unselected_in_5_6"),
        "quarantine_candidate_key_set_sha256": set_digest(
            row["candidate_key"] for row in dispositions
            if row["disposition"] == "preserved_semantic_variant_review_quarantine"),
    }
    require(selection.get("set_digests") == wanted_digests, "selection set digests drifted")
    return selected


def expected_allocation(selection: Mapping[str, Any]) -> dict[str, Any]:
    selected = sorted(
        (row for row in selection["candidate_dispositions"]
         if row.get("selected_for_joint_release_transaction") is True),
        key=lambda row: row["accepted_rank"],
    )
    accepted_rows: list[dict[str, Any]] = []
    for source in selected:
        rank = source["accepted_rank"]
        row = {
            "candidate_key": source["candidate_key"],
            "selection_row_sha256": source["row_sha256"],
            "qualified_candidate_row_sha256": source["qualified_candidate_row_sha256"],
            "ready_candidate_row_sha256": source["ready_candidate_row_sha256"],
            "source_index": source["source_index"],
            "source_record_id": source["source_record_id"],
            "source_record_sha256": source["source_record_sha256"],
            "declaration": source["declaration"],
            "source_syntax_kind": source["source_syntax_kind"],
            "formal_type_sha256": source["formal_type_sha256"],
            "semantic_key": source["semantic_key"],
            "selection_phase": source["selection_phase"],
            "reason_code": source["reason_code"],
            "accepted_rank": rank,
            "transition_from_disposition": source["disposition"],
            "disposition": "accepted_new_kernel_checked_formal_theorem",
            "target_family_id": f"ATF-{PARENT_ATF_HIGH + rank:08d}",
            "target_occurrence_id": f"ATO-{PARENT_ATV_HIGH + rank:08d}",
            "target_sense_id": f"ATS-{PARENT_ATV_HIGH + rank:08d}",
            "target_variant_id": f"ATV-{PARENT_ATV_HIGH + rank:08d}",
            "target_s5_id": f"S5-CLM-{PARENT_ATV_HIGH + rank:08d}",
            "grants_catalog_entry": True,
            "grants_theorem_credit": True,
            "credit_effective_boundary": "authenticated_published_stage5_release_5_6_only",
            "row_sha256": None,
        }
        row["row_sha256"] = row_hash(row)
        accepted_rows.append(row)
    value = {
        "schema_version": "awesome-theorems/mathlib-release-allocation/5.6",
        "artifact": ALLOCATION_REL.name,
        "release": RELEASE,
        "parent_release_root_sha256": PARENT_ROOT,
        "selection_binding": {
            "path": SELECTION_REL.as_posix(),
            "file_sha256": SELECTION_SHA,
            "authority_sha256": SELECTION_AUTHORITY,
            "selected_rows": NEW_ROWS,
        },
        "allocation_policy": {
            "append_only": True,
            "one_formal_identity_per_credit": True,
            "parent_prefix_rewrite_forbidden": True,
            "putnam_seed_variant_relation_credit": 0,
            "credit_effective_boundary": "authenticated_published_stage5_release_5_6_only",
        },
        "counts": {
            "accepted_rows": NEW_ROWS, "theorem_credits": NEW_ROWS,
            "catalog_entries": NEW_ROWS, "putnam_credits": 0,
        },
        "ranges": {
            "ATF": [7_780, 8_779], "ATO": [8_010, 9_009],
            "ATS": [8_010, 9_009], "ATV": [8_010, 9_009],
            "S5_CLM": [8_010, 9_009],
        },
        "set_digests": {
            "accepted_row_sha256_set_sha256": set_digest(row["row_sha256"] for row in accepted_rows),
            "candidate_key_set_sha256": set_digest(row["candidate_key"] for row in accepted_rows),
            "formal_type_sha256_set_sha256": set_digest(row["formal_type_sha256"] for row in accepted_rows),
            "variant_id_set_sha256": set_digest(row["target_variant_id"] for row in accepted_rows),
            "stage_claim_id_set_sha256": set_digest(row["target_s5_id"] for row in accepted_rows),
        },
        "accepted_rows": accepted_rows,
    }
    return seal(value)


def validate_allocation(allocation: Mapping[str, Any], selection: Mapping[str, Any]) -> list[dict[str, Any]]:
    verify_seal(allocation, "mathlib release allocation")
    require(allocation.get("authority_sha256") == ALLOCATION_AUTHORITY,
            "mathlib release allocation authority drifted")
    wanted = expected_allocation(selection)
    require(allocation == wanted, "release allocation differs from independent replay")
    rows = allocation["accepted_rows"]
    require(len({row["candidate_key"] for row in rows}) == NEW_ROWS
            and len({row["formal_type_sha256"] for row in rows}) == NEW_ROWS,
            "release allocation duplicates a theorem credit identity")
    return list(rows)


def artifact_binding(root: Path, rel: Path, document: Mapping[str, Any]) -> dict[str, Any]:
    path = safe_path(root, rel)
    return {
        "path": rel.as_posix(),
        "file_sha256": file_sha(path),
        "size_bytes": path.stat().st_size,
        "authority_sha256": document["authority_sha256"],
        "schema_version": document.get("schema_version"),
    }


def validate_candidate_receipts(
    inventory: Mapping[str, Any], generator_receipt: Mapping[str, Any],
    selection_receipt: Mapping[str, Any], selection: Mapping[str, Any],
) -> set[str]:
    verify_seal(inventory, "qualified batch inventory")
    require(inventory.get("authority_sha256") == QUALIFIED_INVENTORY_AUTHORITY,
            "qualified inventory authority drifted")
    counts = inventory.get("counts", {})
    require(counts.get("full_mathlib_verified_rows") == 2_566
            and counts.get("full_mathlib_canonical_formal_identities") == 2_561
            and counts.get("unadmitted_canonical_theorem_candidates") == 1_561
            and counts.get("generator_admission_qualified") == 1_092
            and counts.get("semantic_variant_review_quarantine") == 469
            and counts.get("exact_identity_duplicate_losers_noncredit") == 5
            and counts.get("theorem_credits_granted_here") == 0,
            "qualified inventory counts/credit boundary drifted")
    losers = inventory.get("exact_identity_duplicate_losers")
    require(isinstance(losers, list) and len(losers) == 5,
            "exact-identity duplicate loser denominator drifted")
    loser_ids: set[str] = set()
    for index, row in enumerate(losers):
        require(isinstance(row, dict)
                and row.get("candidate_only") is True
                and row.get("grants_catalog_entry") is False
                and row.get("grants_theorem_credit") is False,
                f"duplicate loser {index} crossed the non-credit boundary")
        source_id = row.get("source_record_id")
        require(isinstance(source_id, str) and source_id not in loser_ids,
                f"duplicate loser {index} source ID invalid")
        loser_ids.add(source_id)
    require(loser_ids == {
        "ML4-E57250D080C0DC008AB4", "ML4-FF1EC4354BB7B9D2ACFA",
        "ML4-5DDE00D07425BDCCD751", "ML4-58EEAAF294BB4BE8F298",
        "ML4-4F4AEBB481A1F0C355CE",
    } and [row.get("selection_rank") for row in losers] == [38, 378, 618, 619, 2517]
            and all(row.get("method") == "exact_formal_type_sha256" for row in losers),
            "exact duplicate loser identity set drifted")

    verify_seal(generator_receipt, "generator acceptance receipt")
    require(generator_receipt.get("authority_sha256") == GENERATOR_RECEIPT_AUTHORITY,
            "generator acceptance receipt authority drifted")
    generator_counts = generator_receipt.get("counts", {})
    require(generator_receipt.get("candidate_only") is True
            and generator_receipt.get("release_mutation_authorized_or_performed") is False
            and generator_counts.get("machine_qualified_accepted_set") == READY_ROWS
            and generator_counts.get("unadmitted_canonical_candidates") == QUALIFIED_ROWS
            and generator_counts.get("precanonical_rejected_exact_duplicates") == 5
            and generator_counts.get("theorem_credits_granted_by_receipt") == 0
            and generator_counts.get("catalog_entries_granted_by_receipt") == 0,
            "generator acceptance receipt crossed its candidate-only boundary")
    require(generator_receipt.get("output", {}).get("sha256") == ACCEPTED_SHA
            and generator_receipt.get("output", {}).get("rows") == READY_ROWS
            and generator_receipt.get("qualified_candidate_ledger_sha256") == QUALIFIED_SHA,
            "generator acceptance receipt output binding drifted")

    verify_seal(selection_receipt, "selection acceptance receipt")
    require(selection_receipt.get("authority_sha256") == SELECTION_RECEIPT_AUTHORITY,
            "selection acceptance receipt authority drifted")
    credit = selection_receipt.get("credit_boundary", {})
    require(selection_receipt.get("selection_file_sha256") == SELECTION_SHA
            and selection_receipt.get("selection_authority_sha256") == SELECTION_AUTHORITY
            and selection_receipt.get("qualification_receipt_file_sha256") == GENERATOR_RECEIPT_SHA
            and selection_receipt.get("qualification_receipt_authority_sha256")
            == GENERATOR_RECEIPT_AUTHORITY
            and selection_receipt.get("counts") == selection.get("counts")
            and credit.get("catalog_entries_granted") == 0
            and credit.get("theorem_credits_granted") == 0
            and credit.get("ids_allocated") == 0
            and credit.get("release_credit_granted") is False,
            "selection acceptance receipt binding/credit boundary drifted")
    return loser_ids


def validate_schema(schema: Mapping[str, Any]) -> None:
    verify_seal(schema, "5.6 claim record schema")
    require(schema.get("authority_sha256") == SCHEMA_AUTHORITY,
            "5.6 claim schema pinned authority drifted")
    require(schema.get("$id")
            == "https://example.invalid/awesome-theorems/stage5/math-claim-record-5.6.schema.json",
            "5.6 claim schema ID drifted")
    required = schema.get("required")
    properties = schema.get("properties")
    require(isinstance(required, list) and isinstance(properties, dict)
            and set(required) == set(properties) and schema.get("additionalProperties") is False,
            "5.6 claim schema is not top-level closed")
    require(properties.get("schema_version", {}).get("const")
            == "awesome-theorems/stage5-math-claim-record/5.6"
            and properties.get("release_id", {}).get("const") == RELEASE
            and properties.get("origin_release", {}).get("const") == RELEASE
            and properties.get("source_id", {}).get("const") == SOURCE_ID,
            "5.6 claim schema header constants drifted")
    defs = schema.get("$defs")
    require(isinstance(defs, dict), "5.6 claim schema definitions missing")
    allocation = defs.get("allocation", {}).get("properties", {})
    curator = defs.get("curator_disposition", {}).get("properties", {})
    formal = defs.get("formal_statement", {}).get("properties", {})
    proof = defs.get("proof_evidence", {}).get("properties", {})
    require(allocation.get("parent_registry_authority_sha256", {}).get("const")
            == PARENT_REGISTRY_AUTHORITY
            and allocation.get("parent_release_root_sha256", {}).get("const") == PARENT_ROOT,
            "claim schema allocation constants drifted")
    require(curator.get("curation_ledger_path", {}).get("const") == ALLOCATION_REL.as_posix()
            and curator.get("accepted_rank", {}).get("maximum") == NEW_ROWS
            and curator.get("disposition", {}).get("const")
            == "accepted_new_kernel_checked_formal_theorem",
            "claim schema curator boundary drifted")
    require(formal.get("declaration_kind", {}).get("enum") == ["theorem", "lemma"]
            and formal.get("source_syntax_kind", {}).get("enum") == ["theorem", "lemma"],
            "claim schema rejects theorem/lemma source syntax")
    require(proof.get("formal_proof_state", {}).get("const") == "kernel_checked_sorry_free"
            and proof.get("uses_sorry", {}).get("const") is False,
            "claim schema proof boundary drifted")


def expected_parent_receipt(
    root: Path, parent: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    artifacts = []
    for name in sorted(ALL_RELEASE_FILES):
        path = safe_path(root, PARENT_REL / name)
        artifacts.append({
            "path": (PARENT_REL / name).as_posix(),
            "file_sha256": file_sha(path),
            "size_bytes": path.stat().st_size,
            "authority_sha256": parent[name]["authority_sha256"],
        })
    return seal({
        "schema_version": "awesome-theorems/stage5-parent-receipt/5.6",
        "artifact": PARENT_RECEIPT_REL.name,
        "parent_release": PARENT_RELEASE,
        "parent_release_root_sha256": PARENT_ROOT,
        "parent_manifest_file_sha256": PARENT_MANIFEST_SHA,
        "parent_manifest_authority_sha256": PARENT_MANIFEST_AUTHORITY,
        "parent_registry_authority_sha256": PARENT_REGISTRY_AUTHORITY,
        "parent_counts": copy.deepcopy(parent[MANIFEST_NAME]["counts"]),
        "parent_namespace_high_watermarks": copy.deepcopy(
            parent["Claim_ID_Registry.json"]["namespace_high_watermarks"]),
        "artifacts": artifacts,
        "verification": (
            "All nine 5.5 release files, top-level seals, manifest inventory bindings, "
            "and release root were replayed before 5.6 construction."
        ),
    })


def validate_parent_receipt(
    root: Path, receipt: Mapping[str, Any], parent: Mapping[str, Mapping[str, Any]],
) -> None:
    verify_seal(receipt, "5.6 parent receipt")
    require(receipt.get("authority_sha256") == PARENT_RECEIPT_AUTHORITY,
            "5.6 parent receipt pinned authority drifted")
    require(receipt == expected_parent_receipt(root, parent),
            "5.6 parent receipt differs from independent parent inventory")


def validate_source_registry(
    registry: Mapping[str, Any], selection: Mapping[str, Any],
    allocation: Mapping[str, Any], generator_receipt: Mapping[str, Any], root: Path,
) -> None:
    verify_seal(registry, "5.6 source registry")
    require(registry.get("authority_sha256") == SOURCE_REGISTRY_AUTHORITY,
            "5.6 source registry pinned authority drifted")
    require(registry.get("schema_version") == "awesome-theorems/stage5-math-source-registry/5.6"
            and registry.get("additional_sources_allowed") is False,
            "5.6 source registry header drifted")
    require(registry.get("counts") == {
        "sources": 1, "asset_records": 2_566, "qualified_candidates": 1_561,
        "ready_candidates": 1_092, "selected_release_rows": 1_000,
        "terminal_ready_unselected": 92, "quarantine_preserved": 469,
    }, "5.6 source registry counts drifted")
    sources = registry.get("sources")
    require(isinstance(sources, list) and len(sources) == 1, "source registry is not closed")
    source = sources[0]
    require(source.get("source_id") == SOURCE_ID
            and source.get("snapshot", {}).get("commit") == MATHLIB_COMMIT
            and source.get("asset") == {
                "path": FULL_SOURCE_REL.as_posix(), "file_sha256": FULL_SOURCE_SHA,
                "size_bytes": FULL_SOURCE_SIZE,
                "content_digest_before_self_field": FULL_SOURCE_CONTENT_DIGEST,
                "records": 2_566,
            }, "source registry asset binding drifted")
    require(source.get("selection_binding") == {
        "path": SELECTION_REL.as_posix(), "file_sha256": SELECTION_SHA,
        "authority_sha256": selection["authority_sha256"], "selected": 1_000,
        "terminal_ready_unselected": 92, "quarantine": 469,
    }, "source registry selection binding drifted")
    require(source.get("release_allocation_binding") == {
        "path": ALLOCATION_REL.as_posix(),
        "file_sha256": file_sha(safe_path(root, ALLOCATION_REL)),
        "authority_sha256": allocation["authority_sha256"], "accepted": 1_000,
    }, "source registry allocation binding drifted")
    require(source.get("generator_acceptance_binding") == {
        "path": GENERATOR_RECEIPT_REL.as_posix(), "file_sha256": GENERATOR_RECEIPT_SHA,
        "authority_sha256": generator_receipt["authority_sha256"], "ready": 1_092,
    }, "source registry generator receipt binding drifted")


def validate_contract(
    root: Path, contract: Mapping[str, Any], authorities: Mapping[str, Mapping[str, Any]],
) -> None:
    verify_seal(contract, "5.6 expansion contract")
    require(contract.get("authority_sha256") == CONTRACT_AUTHORITY,
            "5.6 expansion contract pinned authority drifted")
    require(contract.get("schema_version") == "awesome-theorems/stage5-math-expansion-contract/5.6"
            and contract.get("release") == RELEASE
            and contract.get("contract_status")
            == "normative_closed_exact_1000_mathlib_formal_theorem_append",
            "5.6 contract header drifted")
    require(contract.get("parent") == {
        "release": "5.5", "release_root_sha256": PARENT_ROOT,
        "manifest_file_sha256": PARENT_MANIFEST_SHA, "catalog_records": 4_525,
        "theorem_records": 2_500, "open_claim_records": 2_025,
        "effective_strict_conjecture_credits": 1_425,
        "variant_high_watermark": 8_009, "family_high_watermark": 7_779,
    }, "5.6 contract parent boundary drifted")
    require(contract.get("quantity_gates") == {
        "origin_theorems_exact": 1_000, "cumulative_theorems_exact": 3_500,
        "catalog_records_exact": 5_525, "open_claims_conserved": 2_025,
        "strict_conjectures_conserved": 1_425,
        "dynamic_theorem_expansion_bound": [500, 1_000],
    }, "5.6 contract quantity gates drifted")
    require(contract.get("identity_allocation") == {
        "append_only": True, "parent_prefix_rewrite_forbidden": True,
        "ATF": [7_780, 8_779], "ATO": [8_010, 9_009],
        "ATS": [8_010, 9_009], "ATV": [8_010, 9_009],
        "S5_CLM": [8_010, 9_009], "one_formal_identity_per_credit": True,
    }, "5.6 contract identity allocation drifted")
    selection_gates = contract.get("selection_gates", {})
    require(selection_gates.get("selected") == 1_000
            and selection_gates.get("qualified_denominator") == 1_561
            and selection_gates.get("ready_denominator") == 1_092
            and selection_gates.get("terminal_ready_unselected") == 92
            and selection_gates.get("quarantine_preserved") == 469
            and selection_gates.get("formal_variants_or_relation_edges_grant_theorem_credit") is False
            and selection_gates.get("putnam_problem_seeds_grant_theorem_credit") is False,
            "5.6 contract selection/Putnam credit boundary drifted")
    quality = contract.get("quality_gates", {})
    require(quality.get("kernel_checked_sorry_free_exact") == 1_000
            and quality.get("source_syntax_theorem") == 629
            and quality.get("source_syntax_lemma") == 371
            and quality.get("human_semantic_uniqueness_claimed") is False
            and quality.get("independent_universal_importance_ranking_claimed") is False,
            "5.6 contract quality boundary drifted")
    layout = contract.get("release_layout", {})
    require(layout.get("non_manifest_artifacts") == list(RELEASE_FILES)
            and layout.get("manifest_name") == MANIFEST_NAME
            and layout.get("manifest_excluded_from_release_root") is True,
            "5.6 contract release layout drifted")
    publication = contract.get("publication", {})
    require(publication.get("compare_and_swap_parent_pointer_file_sha256") == PARENT_CURRENT_SHA
            and publication.get("independent_acceptance_receipt_path") == RECEIPT_REL.as_posix()
            and publication.get("independent_checker_required") is True
            and publication.get("write_does_not_publish") is True,
            "5.6 contract publication boundary drifted")
    expected_bindings = {
        "record_schema": artifact_binding(root, SCHEMA_REL, authorities["schema"]),
        "source_registry": artifact_binding(root, SOURCE_REGISTRY_REL, authorities["source_registry"]),
        "parent_receipt": artifact_binding(root, PARENT_RECEIPT_REL, authorities["parent_receipt"]),
        "release_selection": artifact_binding(root, SELECTION_REL, authorities["selection"]),
        "release_allocation": artifact_binding(root, ALLOCATION_REL, authorities["allocation"]),
        "generator_acceptance_receipt": artifact_binding(
            root, GENERATOR_RECEIPT_REL, authorities["generator_receipt"]),
    }
    require(contract.get("versioned_authorities") == expected_bindings,
            "5.6 contract versioned authority bindings drifted")


def load_authorities(
    root: Path, parent: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    require_pinned_file(root, FULL_SOURCE_REL, FULL_SOURCE_SHA, size=FULL_SOURCE_SIZE)
    full_source = load_json(root, FULL_SOURCE_REL, canonical_file=False)
    source_rows = validate_full_source(full_source)
    qualified = load_jsonl(root, QUALIFIED_REL, expected_sha=QUALIFIED_SHA,
                           expected_rows=QUALIFIED_ROWS)
    accepted = load_jsonl(root, ACCEPTED_REL, expected_sha=ACCEPTED_SHA,
                          expected_rows=READY_ROWS)
    require_pinned_file(root, QUALIFIED_INVENTORY_REL, QUALIFIED_INVENTORY_SHA)
    inventory = load_json(root, QUALIFIED_INVENTORY_REL, canonical_file=False)
    require_pinned_file(root, GENERATOR_RECEIPT_REL, GENERATOR_RECEIPT_SHA)
    generator_receipt = load_json(root, GENERATOR_RECEIPT_REL, canonical_file=False)
    require_pinned_file(root, SELECTION_REL, SELECTION_SHA)
    selection = load_json(root, SELECTION_REL)
    require_pinned_file(root, SELECTION_RECEIPT_REL, SELECTION_RECEIPT_SHA)
    selection_receipt = load_json(root, SELECTION_RECEIPT_REL, canonical_file=False)
    selected = validate_selection(selection, qualified, accepted, source_rows)
    loser_ids = validate_candidate_receipts(
        inventory, generator_receipt, selection_receipt, selection)
    require_pinned_file(root, ALLOCATION_REL, ALLOCATION_SHA)
    allocation = load_json(root, ALLOCATION_REL)
    allocation_rows = validate_allocation(allocation, selection)

    require_pinned_file(root, SCHEMA_REL, SCHEMA_SHA)
    require_pinned_file(root, SOURCE_REGISTRY_REL, SOURCE_REGISTRY_SHA)
    require_pinned_file(root, PARENT_RECEIPT_REL, PARENT_RECEIPT_SHA)
    require_pinned_file(root, CONTRACT_REL, CONTRACT_SHA)
    schema = load_json(root, SCHEMA_REL)
    source_registry = load_json(root, SOURCE_REGISTRY_REL)
    parent_receipt = load_json(root, PARENT_RECEIPT_REL)
    contract = load_json(root, CONTRACT_REL)
    for label, document in (
        ("schema", schema), ("source registry", source_registry),
        ("parent receipt", parent_receipt), ("contract", contract),
    ):
        verify_seal(document, label)
    require(schema.get("authority_sha256") == SCHEMA_AUTHORITY,
            "5.6 schema pinned authority drifted")
    require(source_registry.get("authority_sha256") == SOURCE_REGISTRY_AUTHORITY,
            "5.6 source registry pinned authority drifted")
    require(parent_receipt.get("authority_sha256") == PARENT_RECEIPT_AUTHORITY,
            "5.6 parent receipt pinned authority drifted")
    require(contract.get("authority_sha256") == CONTRACT_AUTHORITY,
            "5.6 contract pinned authority drifted")
    validate_schema(schema)
    validate_parent_receipt(root, parent_receipt, parent)
    validate_source_registry(source_registry, selection, allocation, generator_receipt, root)
    result: dict[str, Any] = {
        "full_source": full_source, "source_rows": source_rows,
        "qualified": qualified, "accepted": accepted, "inventory": inventory,
        "generator_receipt": generator_receipt, "selection": selection,
        "selection_receipt": selection_receipt, "selected": selected,
        "allocation": allocation, "allocation_rows": allocation_rows,
        "schema": schema, "source_registry": source_registry,
        "parent_receipt": parent_receipt, "contract": contract,
        "loser_ids": loser_ids,
    }
    validate_contract(root, contract, result)
    return result


def module_root(source: Mapping[str, Any]) -> str:
    pieces = str(source["source"]["module"]).split(".")
    require(len(pieces) >= 2 and pieces[0] == "Mathlib" and bool(pieces[1]),
            f"invalid Mathlib module: {source['source']['module']!r}")
    return pieces[1]


def has_importance_signal(source: Mapping[str, Any], kind: str) -> bool:
    signals = source.get("importance_signals")
    return isinstance(signals, list) and any(
        isinstance(signal, dict) and signal.get("kind") == kind for signal in signals
    )


def expected_claim(
    ledger: Mapping[str, Any], source: Mapping[str, Any],
    allocation_authority: str, allocation_file_sha: str,
) -> dict[str, Any]:
    rank = int(ledger["accepted_rank"])
    atv_ordinal = PARENT_ATV_HIGH + rank
    atf_ordinal = PARENT_ATF_HIGH + rank
    source_record_id = str(source["source_record_id"])
    source_record_sha = digest(canonical(source))
    semantic_key = str(ledger["semantic_key"])
    formal_type = str(source["formal_type"])
    formal_type_sha = str(source["formal_type_sha256"])
    source_data = source["source"]
    root = module_root(source)

    source_locator = {
        "source_id": SOURCE_ID,
        "artifact_path": FULL_SOURCE_REL.as_posix(),
        "artifact_sha256": FULL_SOURCE_SHA,
        "artifact_size_bytes": FULL_SOURCE_SIZE,
        "record_index": ledger["source_index"],
        "source_record_id": source_record_id,
        "source_record_sha256": source_record_sha,
        "mathlib_commit": MATHLIB_COMMIT,
        "module": source_data["module"],
        "source_path": source_data["path"],
        "source_sha256": source_data["source_sha256"],
        "url": source_data["url"],
        "source_range": copy.deepcopy(source_data["range"]),
        "selection_range": copy.deepcopy(source_data["selection_range"]),
    }
    formal_statement = {
        "language": "Lean4",
        "completeness": "exact_runtime_formal_type_and_source_locator",
        "declaration": source["declaration"],
        "declaration_kind": source["declaration_kind"],
        "source_syntax_kind": source["source_syntax_kind"],
        "module": source_data["module"],
        "formal_type": formal_type,
        "formal_type_sha256": formal_type_sha,
        "formal_docstring": source["formal_docstring"],
        "formal_docstring_origin": source["formal_docstring_origin"],
        "formal_docstring_sha256": source["formal_docstring_sha256"],
    }
    mathematical_statement = seal_field({
        "completeness": "exact_formal",
        "language": "Lean4",
        "natural_language": source["exact_curated_summary"],
        "formal_type": formal_type,
        "formal_type_sha256": formal_type_sha,
    }, "statement_sha256")
    theorem_selection = {
        "source_record_id": source_record_id,
        "selection_cohort": source["selection_cohort"],
        "selection_rank": source["selection_rank"],
        "display_label": source["display_label"],
        "exact_curated_summary": source["exact_curated_summary"],
        "importance_signals": copy.deepcopy(source["importance_signals"]),
        "selection_phase": ledger["selection_phase"],
        "phase_rank": rank if ledger["selection_phase"]
        == "individual_declaration_docstring_priority" else rank - INDIVIDUAL_ROWS,
        "module_root": root,
    }
    curator_disposition = {
        "curation_ledger_path": ALLOCATION_REL.as_posix(),
        "curation_ledger_file_sha256": allocation_file_sha,
        "curation_ledger_authority_sha256": allocation_authority,
        "source_index": ledger["source_index"],
        "source_record_id": source_record_id,
        "curation_row_sha256": ledger["row_sha256"],
        "disposition": ledger["disposition"],
        "reason_code": ledger["reason_code"],
        "accepted_rank": rank,
        "target_variant_id": ledger["target_variant_id"],
        "target_s5_id": ledger["target_s5_id"],
        "grants_catalog_entry": ledger["grants_catalog_entry"],
        "grants_theorem_credit": ledger["grants_theorem_credit"],
        "semantic_key": semantic_key,
    }
    status_detail = {
        "source_material_status": source["material_status"]["status"],
        "status_as_of_commit": source["material_status"]["as_of_commit"],
        "basis": source["material_status"]["basis"],
        "source_refs": [SOURCE_ID],
        "evidence_level": "kernel_checked_sorry_free_at_pinned_commit",
        "later_commit_status_not_inferred": True,
    }
    classification = {
        "msc2020_code": source["msc2020"]["code"],
        "basis": source["msc2020"]["basis"],
        "status": "source_curated_exact" if source["msc2020"]["basis"]
        == "1000_plus_curated" else "machine_root_crosswalk",
        "module_root": root,
    }
    provenance = {
        "formal_source_ref": SOURCE_ID,
        "source_refs": [SOURCE_ID],
        "extraction_mode": "pinned_mathlib_runtime_extraction",
        "extractor_path": "Docs/tools/extract_mathlib_theorems_v5.py",
        "extractor_version": "1.1.0",
        "extractor_file_sha256": "0e26af2b6740abf4626f3cf43d84fb8f7e1f1a6104096e71f1f9b1f2c33189af",
        "source_asset_sha256": FULL_SOURCE_SHA,
        "source_record_id": source_record_id,
        "source_record_sha256": source_record_sha,
        "mathlib_commit": MATHLIB_COMMIT,
        "exact_source_replay_required": True,
    }
    thousand_signal = has_importance_signal(source, "mathlib_1000_theorems")
    rights = seal_field({
        "formal_code_terms": "Apache-2.0",
        "docstring_terms": "Apache-2.0",
        "optional_metadata_terms": "Unlicense" if thousand_signal else "not_applicable",
        "status": "cleared_with_attribution",
        "redistribution_mode": "apache_2_0_with_attribution",
        "attribution": ["The mathlib Community"],
        "source_refs": [SOURCE_ID],
        "mathlib_license_sha256": "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1",
        "catalog_relicenses_source": False,
    }, "rights_payload_sha256")
    source_proof = source["proof_evidence"]
    proof_evidence = seal_field({
        "formal_proof_state": source["formal_proof_state"],
        "verification": source_proof["verification"],
        "uses_sorry": source_proof["uses_sorry"],
        "compiled_module": source_proof["compiled_module"],
        "ilean_path": source_proof["ilean_path"],
        "ilean_sha256": source_proof["ilean_sha256"],
        "olean_path": source_proof["olean_path"],
        "olean_sha256": source_proof["olean_sha256"],
        "batch_axiom_dependency_union": copy.deepcopy(
            source_proof["batch_axiom_dependency_union"]),
        "axiom_evidence_scope": "batch_union_not_per_declaration_exact_dependencies",
        "mathlib_commit": MATHLIB_COMMIT,
    }, "proof_payload_sha256")
    importance = {
        "tier": "source_signaled_mathlib_theorem",
        "basis": "mathlib_1000_formalized_signal" if thousand_signal
        else "mathlib_module_main_result_signal",
        "rationale": "Selected from the pinned formalized mathlib 1000-theorems signal."
        if thousand_signal else "Selected from a pinned mathlib module Main-result signal.",
        "evidence_level": "source_documentation_signal",
        "independent_universal_ranking_claimed": False,
    }
    dedupe = {
        "normalized_declaration_key": normalize_name(str(source["declaration"])),
        "formal_type_sha256": formal_type_sha,
        "source_record_sha256": source_record_sha,
        "semantic_key": semantic_key,
        "candidate_atv_ids": [],
        "parent_catalog_file_sha256": PARENT_CATALOG_SHA,
        "verdict": "unique_formal_identity_after_parent_and_batch_exact_gates",
        "validation_status": "exact_identity_and_alias_signal_screened_not_exhaustive_human_semantic_dedup",
        "duplicate_grants_quota": False,
        "no_evidence_or_status_inheritance": True,
    }
    allocation_request = {
        "origin_release": RELEASE,
        "source_id": SOURCE_ID,
        "source_record_id": source_record_id,
        "source_record_sha256": source_record_sha,
        "semantic_key": semantic_key,
        "statement_sha256": mathematical_statement["statement_sha256"],
        "family_action": "new_family",
    }
    allocation = {
        "parent_registry_authority_sha256": PARENT_REGISTRY_AUTHORITY,
        "parent_release_root_sha256": PARENT_ROOT,
        "allocation_request_sha256": digest(canonical(allocation_request)),
        "transaction_id": f"S5-ALLOC-{atv_ordinal:08d}",
        "family_action": "new_family",
        "append_only": True,
    }
    aliases = list(dict.fromkeys(
        value for value in (str(source["declaration"]), str(source["exact_curated_summary"]))
        if value != str(source["display_label"])
    ))
    row: dict[str, Any] = {
        "schema_version": "awesome-theorems/stage5-math-claim-record/5.6",
        "release_id": RELEASE,
        "origin_stage": "Stage5",
        "origin_release": RELEASE,
        "curation_key": f"mathlib/{source_record_id}",
        "allocation": allocation,
        "occurrence_id": f"ATO-{atv_ordinal:08d}",
        "family_id": f"ATF-{atf_ordinal:08d}",
        "sense_id": f"ATS-{atv_ordinal:08d}",
        "variant_id": f"ATV-{atv_ordinal:08d}",
        "stage_claim_id": f"S5-CLM-{atv_ordinal:08d}",
        "display_name": source["display_label"],
        "aliases": aliases,
        "owner_domain": "mathematics",
        "membership_domains": ["mathematics"],
        "record_role": "claim",
        "claim_kind": "theorem",
        "current_claim_kind": "theorem",
        "historical_kind": "theorem",
        "atomicity": "atomic",
        "truth_apt": True,
        "category": "theorem",
        "material_status": "proved",
        "source_id": SOURCE_ID,
        "source_locator": source_locator,
        "formal_statement": formal_statement,
        "theorem_selection": theorem_selection,
        "curator_disposition": curator_disposition,
        "mathematical_statement": mathematical_statement,
        "status_detail": status_detail,
        "classification": classification,
        "provenance": provenance,
        "rights": rights,
        "dedupe": dedupe,
        "proof_evidence": proof_evidence,
        "importance": importance,
        "lifecycle": "active",
        "lineage": [],
        "semantic_key": semantic_key,
    }
    row["content_payload_sha256"] = digest(canonical({
        "formal_statement": formal_statement,
        "mathematical_statement": mathematical_statement,
    }))
    row["source_payload_sha256"] = digest(canonical({
        "source_locator": source_locator,
        "theorem_selection": theorem_selection,
        "provenance": provenance,
    }))
    row["proof_payload_sha256"] = proof_evidence["proof_payload_sha256"]
    row["semantic_payload_sha256"] = digest(canonical({
        "record_role": row["record_role"], "atomicity": row["atomicity"],
        "truth_apt": row["truth_apt"], "category": row["category"],
        "current_claim_kind": row["current_claim_kind"],
        "semantic_key": semantic_key,
        "statement_sha256": mathematical_statement["statement_sha256"],
    }))
    return row


def validate_dense_origin_ids(new_rows: Sequence[Mapping[str, Any]]) -> None:
    require(len(new_rows) == NEW_ROWS, "origin theorem credit denominator drifted")
    expected_atv = [f"ATV-{ordinal:08d}" for ordinal in range(8_010, 9_010)]
    expected_atf = [f"ATF-{ordinal:08d}" for ordinal in range(7_780, 8_780)]
    expected_ato = [f"ATO-{ordinal:08d}" for ordinal in range(8_010, 9_010)]
    expected_ats = [f"ATS-{ordinal:08d}" for ordinal in range(8_010, 9_010)]
    expected_s5 = [f"S5-CLM-{ordinal:08d}" for ordinal in range(8_010, 9_010)]
    require([row.get("variant_id") for row in new_rows] == expected_atv,
            "origin ATV IDs contain a duplicate/gap/reorder/out-of-range value")
    require([row.get("family_id") for row in new_rows] == expected_atf,
            "origin ATF IDs contain a duplicate/gap/reorder/out-of-range value")
    require([row.get("occurrence_id") for row in new_rows] == expected_ato,
            "origin ATO IDs contain a duplicate/gap/reorder/out-of-range value")
    require([row.get("sense_id") for row in new_rows] == expected_ats,
            "origin ATS IDs contain a duplicate/gap/reorder/out-of-range value")
    require([row.get("stage_claim_id") for row in new_rows] == expected_s5,
            "origin S5 IDs contain a duplicate/gap/reorder/out-of-range value")


def validate_origin_rows(
    rows: Sequence[Mapping[str, Any]], allocation_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]], schema: Mapping[str, Any],
    allocation_authority: str, allocation_file_sha: str,
) -> None:
    require(len(rows) == len(allocation_rows) == NEW_ROWS,
            "origin/allocation theorem denominator drifted")
    required = schema.get("required")
    properties = schema.get("properties")
    require(isinstance(required, list) and isinstance(properties, dict), "claim schema malformed")
    for index, (observed, ledger) in enumerate(zip(rows, allocation_rows, strict=True)):
        validate_origin_row(
            observed, ledger, source_rows, schema, allocation_authority,
            allocation_file_sha, index=index,
        )


def validate_origin_row(
    observed: Mapping[str, Any], ledger: Mapping[str, Any],
    source_rows: Sequence[Mapping[str, Any]], schema: Mapping[str, Any],
    allocation_authority: str, allocation_file_sha: str, *, index: int = 0,
) -> None:
    required = schema.get("required")
    properties = schema.get("properties")
    require(isinstance(required, list) and isinstance(properties, dict), "claim schema malformed")
    source_index = ledger.get("source_index")
    require(isinstance(source_index, int) and 0 <= source_index < len(source_rows),
            f"origin row {index} source index invalid")
    source = source_rows[source_index]
    require(source.get("source_record_id") == ledger.get("source_record_id"),
            f"origin row {index} allocation/source ID mismatch")
    expected = expected_claim(ledger, source, allocation_authority, allocation_file_sha)
    require(set(observed) == set(required) == set(properties),
            f"origin row {index} top-level schema is not closed")
    require(observed == expected,
            f"origin row {index} differs from independent source/allocation replay")


def exact_identity(row: Mapping[str, Any]) -> tuple[str | None, str | None, str | None]:
    formal = row.get("formal_statement")
    formal = formal if isinstance(formal, dict) else {}
    exact = (formal.get("formal_type_sha256") or formal.get("declaration_type_sha256")
             or row.get("formal_type_sha256"))
    text = formal.get("formal_type") or formal.get("declaration_type") or row.get("formal_type")
    name = (formal.get("declaration") or formal.get("qualified_declaration")
            or formal.get("declaration_name") or row.get("qualified_name"))
    return (
        exact if isinstance(exact, str) and SHA_RE.fullmatch(exact) else None,
        normalized_type_sha(text) if isinstance(text, str) and text else None,
        normalized_name_sha(name) if isinstance(name, str) and name else None,
    )


def identity_components(row: Mapping[str, Any]) -> tuple[set[str], set[str], set[str]]:
    formal = row.get("formal_statement")
    formal = formal if isinstance(formal, dict) else {}
    mathematical = row.get("mathematical_statement")
    mathematical = mathematical if isinstance(mathematical, dict) else {}
    exact: set[str] = set()
    normalized: set[str] = set()
    names: set[str] = set()
    for value in (
        row.get("formal_type_sha256"), formal.get("formal_type_sha256"),
        formal.get("declaration_type_sha256"), mathematical.get("formal_type_sha256"),
    ):
        if isinstance(value, str) and SHA_RE.fullmatch(value):
            exact.add(value)
    for value in (
        row.get("formal_type"), formal.get("formal_type"), formal.get("declaration_type"),
        mathematical.get("formal_type"),
    ):
        if isinstance(value, str) and value:
            exact.add(digest(value.encode("utf-8")))
            normalized.add(normalized_type_sha(value))
    for value in (
        row.get("formal_declaration"), row.get("qualified_name"),
        formal.get("declaration"), formal.get("declaration_name"),
        formal.get("qualified_declaration"),
    ):
        if isinstance(value, str) and value:
            names.add(normalized_name_sha(value))
    return exact, normalized, names


def validate_three_identity_gates(
    parent_records: Sequence[Mapping[str, Any]], new_rows: Sequence[Mapping[str, Any]],
) -> None:
    parent_exact: set[str] = set()
    parent_normalized: set[str] = set()
    parent_names: set[str] = set()
    for row in parent_records:
        exact, normalized, names = identity_components(row)
        parent_exact.update(exact)
        parent_normalized.update(normalized)
        parent_names.update(names)
    batch_exact: set[str] = set()
    batch_normalized: set[str] = set()
    batch_names: set[str] = set()
    for index, row in enumerate(new_rows):
        exact, normalized, names = identity_components(row)
        require(exact and normalized and names,
                f"origin row {index} lacks all three formal identity keys")
        require(exact.isdisjoint(parent_exact),
                f"origin row {index} exact formal type conflicts with parent")
        require(normalized.isdisjoint(parent_normalized),
                f"origin row {index} whitespace-normalized formal type conflicts with parent")
        require(names.isdisjoint(parent_names),
                f"origin row {index} NFKC-casefold declaration conflicts with parent")
        require(exact.isdisjoint(batch_exact),
                f"origin row {index} duplicates a batch exact formal type")
        require(normalized.isdisjoint(batch_normalized),
                f"origin row {index} duplicates a batch normalized formal type")
        require(names.isdisjoint(batch_names),
                f"origin row {index} duplicates a batch normalized declaration")
        batch_exact.update(exact)
        batch_normalized.update(normalized)
        batch_names.update(names)


def validate_no_duplicate_losers(
    new_rows: Sequence[Mapping[str, Any]], loser_ids: set[str]
) -> None:
    observed: set[str] = set()
    for row in new_rows:
        locator = row.get("source_locator")
        require(isinstance(locator, dict), "origin row source locator missing")
        source_id = locator.get("source_record_id")
        if isinstance(source_id, str):
            observed.add(source_id)
    require(observed.isdisjoint(loser_ids), "an exact-identity duplicate loser entered release 5.6")


def expected_authoritative_inputs(
    root: Path, parent: Mapping[str, Mapping[str, Any]], authorities: Mapping[str, Any],
) -> dict[str, Any]:
    def sized(rel: Path) -> int:
        return safe_path(root, rel).stat().st_size

    return {
        "contract": artifact_binding(root, CONTRACT_REL, authorities["contract"]),
        "record_schema": artifact_binding(root, SCHEMA_REL, authorities["schema"]),
        "source_registry": artifact_binding(root, SOURCE_REGISTRY_REL, authorities["source_registry"]),
        "parent_receipt": artifact_binding(root, PARENT_RECEIPT_REL, authorities["parent_receipt"]),
        "release_selection": artifact_binding(root, SELECTION_REL, authorities["selection"]),
        "release_allocation": artifact_binding(root, ALLOCATION_REL, authorities["allocation"]),
        "generator_acceptance_receipt": artifact_binding(
            root, GENERATOR_RECEIPT_REL, authorities["generator_receipt"]),
        "accepted_set": {
            "path": ACCEPTED_REL.as_posix(), "file_sha256": ACCEPTED_SHA,
            "size_bytes": sized(ACCEPTED_REL), "rows": READY_ROWS,
        },
        "qualified_inventory": {
            "path": QUALIFIED_INVENTORY_REL.as_posix(),
            "file_sha256": QUALIFIED_INVENTORY_SHA,
            "size_bytes": sized(QUALIFIED_INVENTORY_REL),
            "authority_sha256": QUALIFIED_INVENTORY_AUTHORITY,
        },
        "qualified_ledger": {
            "path": QUALIFIED_REL.as_posix(), "file_sha256": QUALIFIED_SHA,
            "size_bytes": sized(QUALIFIED_REL), "rows": QUALIFIED_ROWS,
        },
        "full_mathlib_source": {
            "path": FULL_SOURCE_REL.as_posix(), "file_sha256": FULL_SOURCE_SHA,
            "size_bytes": FULL_SOURCE_SIZE, "records": 2_566,
            "content_digest_before_self_field": FULL_SOURCE_CONTENT_DIGEST,
            "mathlib_commit": MATHLIB_COMMIT,
        },
        "parent_release": {
            "release": PARENT_RELEASE, "release_root_sha256": PARENT_ROOT,
            "manifest_file_sha256": PARENT_MANIFEST_SHA,
            "manifest_authority_sha256": parent[MANIFEST_NAME]["authority_sha256"],
            "registry_authority_sha256": PARENT_REGISTRY_AUTHORITY,
        },
    }


def expected_registry_suffixes(
    new_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in new_rows:
        request = row["allocation"]["allocation_request_sha256"]
        families.append({
            "family_id": row["family_id"], "curation_key": row["curation_key"],
            "display_titles": list(dict.fromkeys([row["display_name"], *row["aliases"]])),
            "member_occurrence_ids": [row["occurrence_id"]],
            "historical_member_occurrence_ids": [row["occurrence_id"]],
            "idempotency_request_sha256": request,
            "identity_state": "stage5_mathlib_formal_identity_family",
            "lifecycle": "current", "semantic_equivalence_asserted": False,
        })
        senses.append({
            "sense_id": row["sense_id"], "family_id": row["family_id"],
            "bootstrap_occurrence_id": row["occurrence_id"], "curation_key": row["curation_key"],
            "idempotency_request_sha256": request,
            "identity_state": "stage5_mathlib_formal_identity_sense_without_exhaustive_human_semantic_claim",
            "lifecycle": "current",
        })
        variants.append({
            "variant_id": row["variant_id"], "sense_id": row["sense_id"],
            "bootstrap_occurrence_id": row["occurrence_id"], "curation_key": row["curation_key"],
            "idempotency_request_sha256": request,
            "semantic_payload_sha256": row["semantic_payload_sha256"],
            "identity_state": "stage5_mathlib_exact_formal_type_variant",
            "lifecycle": "current",
        })
    return families, senses, variants


def expected_coverage_additions(
    selection: Mapping[str, Any], allocation: Mapping[str, Any],
) -> list[dict[str, Any]]:
    allocated = {row["candidate_key"]: row for row in allocation["accepted_rows"]}
    result: list[dict[str, Any]] = []
    for source in selection["candidate_dispositions"]:
        accepted = allocated.get(source["candidate_key"])
        effective = accepted if accepted is not None else source
        result.append({
            "candidate_key": source["candidate_key"], "source_id": SOURCE_ID,
            "source_index": source["source_index"], "source_record_id": source["source_record_id"],
            "source_record_sha256": source["source_record_sha256"],
            "declaration": source["declaration"],
            "source_syntax_kind": source["source_syntax_kind"],
            "formal_type_sha256": source["formal_type_sha256"],
            "semantic_key": source["semantic_key"], "generator_lane": source["generator_lane"],
            "disposition": effective["disposition"], "reason_code": source["reason_code"],
            "accepted_rank": source["accepted_rank"],
            "target_variant_id": effective["target_variant_id"],
            "target_s5_id": effective["target_s5_id"],
            "grants_catalog_entry": effective["grants_catalog_entry"],
            "grants_theorem_credit": effective["grants_theorem_credit"],
            "origin_release": RELEASE, "curation_row_sha256": effective["row_sha256"],
            "qualified_candidate_row_sha256": source["qualified_candidate_row_sha256"],
            "ready_candidate_row_sha256": source["ready_candidate_row_sha256"],
            "supersedes_candidate_key": None,
            "transition_from_disposition": accepted["transition_from_disposition"]
            if accepted is not None else "qualified_candidate_only",
        })
    return result


def expected_msc_coverage(
    parent_rows: Sequence[Mapping[str, Any]], new_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_code: dict[str, list[Mapping[str, Any]]] = {}
    for claim in new_rows:
        by_code.setdefault(str(claim["classification"]["msc2020_code"]), []).append(claim)
    result: list[dict[str, Any]] = []
    for original in parent_rows:
        row = copy.deepcopy(dict(original))
        additions = by_code.pop(str(row["msc_top_class"]), [])
        identifiers = [claim["stage_claim_id"] for claim in additions]
        row["current_theorem_s5_ids"] = [*row["current_theorem_s5_ids"], *identifiers]
        row["origin_theorem_s5_ids"] = identifiers
        row["origin_open_s5_ids"] = []
        if additions:
            row["source_ids"] = sorted(set(row["source_ids"]) | {SOURCE_ID})
        exact = sum(claim["classification"]["basis"] == "1000_plus_curated"
                    for claim in additions)
        row["classification_basis_counts"]["source_annotation"] += exact
        row["classification_basis_counts"]["machine_crosswalk"] += len(additions) - exact
        row["counts"]["current_theorems"] = len(row["current_theorem_s5_ids"])
        row["counts"]["current_open"] = len(row["current_open_s5_ids"])
        row["counts"]["origin_theorems"] = len(identifiers)
        row["counts"]["origin_open"] = 0
        row["counts"]["open_reserve"] = len(row["open_reserve_candidate_keys"])
        classified = (row["counts"]["current_theorems"] + row["counts"]["current_open"]
                      + row["counts"]["open_reserve"])
        row["scarcity"] = "zero" if classified == 0 else (
            "thin" if classified < 10 else "adequate_in_source_inventory")
        row["scarcity_reason"] = (
            "No current or open-reserve member has this primary source annotation."
            if classified == 0 else
            "Fewer than ten current-plus-reserve members have this primary class."
            if classified < 10 else
            "At least ten current-plus-reserve members have this primary class."
        )
        result.append(row)
    require(not by_code, f"origin rows contain unknown MSC classes: {sorted(by_code)}")
    return result


def validate_parent_prefixes(
    documents: Mapping[str, Mapping[str, Any]], parent: Mapping[str, Mapping[str, Any]],
) -> None:
    validate_parent_prefix(documents["Claim_Catalog.json"]["records"],
                           parent["Claim_Catalog.json"]["records"], "catalog")
    validate_parent_prefix(documents["Theorem_List.json"]["records"],
                           parent["Theorem_List.json"]["records"], "theorem projection")
    require(documents["Theorem_List.json"]["stage_claim_ids"][:PARENT_THEOREM_ROWS]
            == parent["Theorem_List.json"]["stage_claim_ids"],
            "theorem projection ID parent prefix changed")
    require(documents["Open_Claim_List.json"]["records"]
            == parent["Open_Claim_List.json"]["records"]
            and documents["Open_Claim_List.json"]["stage_claim_ids"]
            == parent["Open_Claim_List.json"]["stage_claim_ids"],
            "open-claim projection changed")
    for key in ("families", "senses", "variants"):
        validate_parent_prefix(documents["Claim_ID_Registry.json"][key],
                               parent["Claim_ID_Registry.json"][key], f"registry {key}")
    for key in ("legacy_aliases", "redirects", "splits", "family_membership_extensions"):
        require(documents["Claim_ID_Registry.json"][key]
                == parent["Claim_ID_Registry.json"][key], f"registry static array changed: {key}")
    validate_parent_prefix(documents["Stage5_Claim_ID_Registry.json"]["mappings"],
                           parent["Stage5_Claim_ID_Registry.json"]["mappings"],
                           "Stage5 mappings")
    validate_parent_prefix(documents["Migration_v4_to_v5.json"]["migrations"],
                           parent["Migration_v4_to_v5.json"]["migrations"], "migrations")
    validate_parent_prefix(documents["Coverage_Ledger.json"]["candidate_dispositions"],
                           parent["Coverage_Ledger.json"]["candidate_dispositions"],
                           "coverage dispositions")
    require(documents["Strict_Conjecture_Ledger.json"]["strict_credits"]
            == parent["Strict_Conjecture_Ledger.json"]["strict_credits"]
            and documents["Strict_Conjecture_Ledger.json"]["credit_corrections"]
            == parent["Strict_Conjecture_Ledger.json"]["credit_corrections"],
            "strict conjecture credits/corrections changed")


def validate_release_documents(
    root: Path, documents: Mapping[str, Mapping[str, Any]],
    parent: Mapping[str, Mapping[str, Any]], authorities: Mapping[str, Any],
    expected_inputs: Mapping[str, Any],
) -> list[dict[str, Any]]:
    require(set(documents) == ALL_RELEASE_FILES, "release document set drifted")
    expected_schemas = {
        "Claim_Catalog.json": "awesome-theorems/stage5-claim-catalog/5.6",
        "Claim_ID_Registry.json": "awesome-theorems/claim-id-registry/5.6",
        "Stage5_Claim_ID_Registry.json": "awesome-theorems/stage5-claim-id-registry/5.6",
        "Migration_v4_to_v5.json": "awesome-theorems/migration-v4-to-v5/5.6",
        "Theorem_List.json": "awesome-theorems/stage5-query-projection/5.6",
        "Open_Claim_List.json": "awesome-theorems/stage5-query-projection/5.6",
        "Coverage_Ledger.json": "awesome-theorems/stage5-coverage-ledger/5.6",
        "Strict_Conjecture_Ledger.json": "awesome-theorems/stage5-strict-conjecture-ledger/5.6",
        MANIFEST_NAME: "awesome-theorems/stage5-release-manifest/5.6",
    }
    for name, document in documents.items():
        verify_seal(document, name)
        require(document.get("schema_version") == expected_schemas[name]
                and document.get("release") == RELEASE, f"{name} release/schema marker drifted")
        if name not in {"Strict_Conjecture_Ledger.json", MANIFEST_NAME}:
            require(document.get("authoritative_inputs") == expected_inputs,
                    f"{name} authoritative inputs drifted")
    require(documents[MANIFEST_NAME].get("authoritative_inputs") == expected_inputs,
            "manifest authoritative inputs drifted")
    validate_parent_prefixes(documents, parent)

    catalog = documents["Claim_Catalog.json"]
    theorem = documents["Theorem_List.json"]
    new_rows = catalog["records"][PARENT_CATALOG_ROWS:]
    require(len(catalog["records"]) == 5_525 and len(new_rows) == NEW_ROWS,
            "catalog/origin theorem denominator drifted")
    require(theorem["records"][PARENT_THEOREM_ROWS:] == new_rows
            and theorem["stage_claim_ids"][PARENT_THEOREM_ROWS:]
            == [row["stage_claim_id"] for row in new_rows],
            "theorem projection suffix differs from catalog theorem suffix")
    validate_dense_origin_ids(new_rows)
    allocation_file_sha = file_sha(safe_path(root, ALLOCATION_REL))
    validate_origin_rows(new_rows, authorities["allocation_rows"], authorities["source_rows"],
                         authorities["schema"], authorities["allocation"]["authority_sha256"],
                         allocation_file_sha)
    validate_three_identity_gates(parent["Claim_Catalog.json"]["records"], new_rows)
    validate_no_duplicate_losers(new_rows, authorities["loser_ids"])
    require(Counter(row["formal_statement"]["source_syntax_kind"] for row in new_rows)
            == Counter({"theorem": 629, "lemma": 371})
            and all(row["claim_kind"] == row["current_claim_kind"] == "theorem"
                    for row in new_rows),
            "lemma/theorem source syntax was rejected or double-counted")

    expected_quality = {
        "inherited_5_5": copy.deepcopy(parent[MANIFEST_NAME]["quality_qualification"]),
        "origin_5_6": {
            "accepted_kernel_checked_sorry_free_formal_identities": 1_000,
            "selected_individual_declaration_docstring": 511,
            "selected_module_main_result_description": 489,
            "source_syntax_theorem": 629,
            "source_syntax_lemma": 371,
            "selection_authority_sha256": SELECTION_AUTHORITY,
            "allocation_authority_sha256": ALLOCATION_AUTHORITY,
            "unsupported_formal_truth_credit": 0,
            "human_semantic_uniqueness_claimed": False,
            "independent_universal_importance_ranking_claimed": False,
        },
    }
    require(catalog.get("artifact") == "Claim_Catalog.json"
            and catalog.get("catalog_scope") == parent["Claim_Catalog.json"]["catalog_scope"]
            and catalog.get("counts") == {
                "records": 5_525, "origin_theorems": 1_000, "origin_open_claims": 0,
                "origin_strict_conjectures": 0, "cumulative_theorems": 3_500,
                "cumulative_open_claims": 2_025, "effective_strict_conjectures": 1_425,
            }
            and catalog.get("quality_qualification") == expected_quality
            and catalog.get("origin_5_6_closed_schema") == {
                "closed": True, "origin_records": 1_000,
                "schema_path": SCHEMA_REL.as_posix(),
                "schema_authority_sha256": authorities["schema"]["authority_sha256"],
                "record_keys": sorted(authorities["schema"]["required"]),
                "parent_records_rewritten": False,
            }, "catalog header/count/quality/schema boundary drifted")
    for projection_name, count in (("Theorem_List.json", 3_500),
                                   ("Open_Claim_List.json", 2_025)):
        projection = documents[projection_name]
        require(projection.get("artifact") == projection_name
                and projection.get("query")
                == "pure predicate over Claim_Catalog.json; records copied byte-semantically"
                and projection.get("counts") == {"records": count},
                f"{projection_name} header/count drifted")

    registry = documents["Claim_ID_Registry.json"]
    require(registry.get("namespace_high_watermarks") == {
        "ATF": LAST_ATF, "ATO": LAST_ATV, "ATS": LAST_ATV, "ATV": LAST_ATV,
    }, "5.6 namespace high-watermarks drifted")
    families, senses, variants = expected_registry_suffixes(new_rows)
    require(registry["families"][len(parent["Claim_ID_Registry.json"]["families"]):] == families
            and registry["senses"][len(parent["Claim_ID_Registry.json"]["senses"]):] == senses
            and registry["variants"][len(parent["Claim_ID_Registry.json"]["variants"]):] == variants,
            "5.6 identity registry suffix differs from origin claims")
    expected_policy = copy.deepcopy(parent["Claim_ID_Registry.json"]["allocation_policy"])
    expected_policy.update({
        "release_5_6_first_new_atv_ordinal": 8_010,
        "release_5_6_new_family_first_atf_ordinal": 7_780,
        "release_5_6_credit_unit":
        "canonical_formal_proposition_identity_not_asserted_human_semantic_landmark",
    })
    require(registry.get("artifact") == "Claim_ID_Registry.json"
            and registry.get("parent_registry_authority_sha256") == PARENT_REGISTRY_AUTHORITY
            and registry.get("baseline_registry_authority_sha256")
            == parent["Claim_ID_Registry.json"]["baseline_registry_authority_sha256"]
            and registry.get("allocation_policy") == expected_policy
            and registry.get("counts") == {
                "families": 8_779, "senses": 9_009, "variants": 9_009,
                "stage4_variants": parent["Claim_ID_Registry.json"]["counts"]["stage4_variants"],
                "stage5_additions": 5_525,
                "legacy_aliases": len(parent["Claim_ID_Registry.json"]["legacy_aliases"]),
                "redirects": len(parent["Claim_ID_Registry.json"]["redirects"]),
                "splits": len(parent["Claim_ID_Registry.json"]["splits"]),
            }, "identity registry header/count/policy drifted")
    expected_mappings = [{
        "ordinal": PARENT_ATV_HIGH + rank, "variant_id": row["variant_id"],
        "predecessor_stage_claim_id": None, "stage_claim_id": row["stage_claim_id"],
        "lifecycle": "current",
    } for rank, row in enumerate(new_rows, 1)]
    stage_suffix = documents["Stage5_Claim_ID_Registry.json"]["mappings"][PARENT_ATV_HIGH:]
    require(stage_suffix == expected_mappings, "Stage5 mapping suffix drifted")
    stage = documents["Stage5_Claim_ID_Registry.json"]
    require(stage.get("artifact") == "Stage5_Claim_ID_Registry.json"
            and stage.get("numbering_policy")
            == parent["Stage5_Claim_ID_Registry.json"]["numbering_policy"]
            and stage.get("counts") == {"mappings": 9_009},
            "Stage5 registry header/count drifted")
    expected_migrations = [{
        "ordinal": PARENT_ATV_HIGH + rank, "variant_id": row["variant_id"],
        "v4_variant_id": None, "s4_claim_id": None, "stage_claim_id": row["stage_claim_id"],
        "migration_action": "new_stage5_allocation", "predecessor_record_sha256": None,
        "current_resolution": {
            "kind": "current", "terminal_atv_ids": [row["variant_id"]],
            "terminal_s5_ids": [row["stage_claim_id"]], "default_child": None,
            "evidence_inherited": False,
        },
    } for rank, row in enumerate(new_rows, 1)]
    migration_suffix = documents["Migration_v4_to_v5.json"]["migrations"][PARENT_ATV_HIGH:]
    require(migration_suffix == expected_migrations, "migration suffix drifted")
    migration = documents["Migration_v4_to_v5.json"]
    require(migration.get("artifact") == "Migration_v4_to_v5.json"
            and migration.get("v4_import_receipt")
            == parent["Migration_v4_to_v5.json"]["v4_import_receipt"]
            and migration.get("counts") == {
                "historical_bindings": parent["Migration_v4_to_v5.json"]["counts"]["historical_bindings"],
                "new_allocations": 5_525, "migrations": 9_009,
            }, "migration header/count drifted")

    coverage = documents["Coverage_Ledger.json"]
    coverage_suffix = coverage["candidate_dispositions"][PARENT_COVERAGE_ROWS:]
    require(coverage_suffix == expected_coverage_additions(
        authorities["selection"], authorities["allocation"]),
        "coverage suffix differs from selection/allocation join")
    require(coverage["msc_coverage"] == expected_msc_coverage(
        parent["Coverage_Ledger.json"]["msc_coverage"], new_rows),
        "MSC coverage differs from independent replay")
    disposition_counts = Counter(row["disposition"] for row in coverage_suffix)
    require(disposition_counts == Counter({
        "accepted_new_kernel_checked_formal_theorem": 1_000,
        "terminal_ready_unselected_in_5_6": 92,
        "preserved_semantic_variant_review_quarantine": 469,
    }), "coverage disposition counts drifted")
    require(sum(row.get("grants_theorem_credit") is True for row in coverage_suffix) == NEW_ROWS,
            "coverage theorem credit count drifted")
    require(coverage.get("effective_state_policy") == {
        "identity_fields": ["source_id", "source_record_id"],
        "historical_parent_rows_are_immutable": True,
        "origin_5_6_candidate_denominator_closed": True,
        "release_selection_dispositions_terminal": [
            "accepted_new_kernel_checked_formal_theorem",
            "terminal_ready_unselected_in_5_6",
            "preserved_semantic_variant_review_quarantine",
        ],
    } and coverage.get("counts") == {
        "candidate_dispositions": 7_884, "msc_coverage": 63,
        "origin_5_6_candidates": 1_561, "origin_5_6_accepted_new_theorems": 1_000,
        "origin_5_6_terminal_ready_unselected": 92,
        "origin_5_6_quarantine_preserved": 469,
    }, "coverage header/count/policy drifted")

    strict = documents["Strict_Conjecture_Ledger.json"]
    parent_strict = parent["Strict_Conjecture_Ledger.json"]
    require(strict.get("counts") == parent_strict.get("counts")
            and strict.get("set_digests") == parent_strict.get("set_digests")
            and strict.get("origin_5_6_change") == {
                "strict_credits_added": 0, "strict_credits_removed": 0,
                "credit_corrections_added": 0,
            }, "strict conjecture conservation boundary drifted")
    require(strict.get("parent_release_root_sha256") == PARENT_ROOT
            and strict.get("parent_strict_ledger_file_sha256")
            == file_sha(safe_path(root, PARENT_REL / "Strict_Conjecture_Ledger.json"))
            and strict.get("parent_strict_ledger_authority_sha256")
            == parent_strict["authority_sha256"],
            "strict ledger parent binding drifted")
    return list(new_rows)


def expected_quality_qualification(
    parent: Mapping[str, Mapping[str, Any]], authorities: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "inherited_5_5": copy.deepcopy(parent[MANIFEST_NAME]["quality_qualification"]),
        "origin_5_6": {
            "accepted_kernel_checked_sorry_free_formal_identities": 1_000,
            "selected_individual_declaration_docstring": 511,
            "selected_module_main_result_description": 489,
            "source_syntax_theorem": 629,
            "source_syntax_lemma": 371,
            "selection_authority_sha256": authorities["selection"]["authority_sha256"],
            "allocation_authority_sha256": authorities["allocation"]["authority_sha256"],
            "unsupported_formal_truth_credit": 0,
            "human_semantic_uniqueness_claimed": False,
            "independent_universal_importance_ranking_claimed": False,
        },
    }


def validate_manifest_semantics(
    manifest: Mapping[str, Any], documents: Mapping[str, Mapping[str, Any]],
    parent: Mapping[str, Mapping[str, Any]], authorities: Mapping[str, Any],
    expected_inputs: Mapping[str, Any],
) -> None:
    verify_seal(manifest, MANIFEST_NAME)
    require(manifest.get("schema_version") == "awesome-theorems/stage5-release-manifest/5.6"
            and manifest.get("release") == RELEASE
            and manifest.get("parent_release") == PARENT_RELEASE
            and manifest.get("parent_release_root_sha256") == PARENT_ROOT,
            "manifest release/parent header drifted")
    require(manifest.get("authoritative_inputs") == expected_inputs,
            "manifest authoritative inputs drifted")
    require(manifest.get("counts") == EXPECTED_COUNTS, "manifest counts drifted")
    expected_quality = expected_quality_qualification(parent, authorities)
    require(manifest.get("quality_qualification") == expected_quality
            and documents["Claim_Catalog.json"].get("quality_qualification") == expected_quality,
            "manifest/catalog nested quality qualification drifted")
    require(manifest.get("accepted_set_digests") == authorities["selection"]["set_digests"],
            "manifest selection set digest binding drifted")
    require(manifest.get("release_allocation_digests")
            == authorities["allocation"]["set_digests"],
            "manifest allocation set digest binding drifted")
    strict = documents["Strict_Conjecture_Ledger.json"]
    strict_binding = manifest.get("strict_credit_binding", {})
    require(strict_binding.get("effective_credits") == 1_425
            and strict_binding.get("new_credits") == 0
            and strict_binding.get("strict_ledger_authority_sha256") == strict["authority_sha256"]
            and strict_binding.get("strict_credit_set_sha256")
            == strict["set_digests"].get(
                "effective_strict_credit_set_sha256", strict["set_digests"]),
            "manifest strict-credit binding drifted")
    require(manifest.get("publication") == {
        "current_release_not_mutated_by_build": True,
        "cas_parent_pointer_file_sha256": PARENT_CURRENT_SHA,
        "independent_acceptance_receipt_required": RECEIPT_REL.as_posix(),
    }, "manifest publication boundary drifted")


def check_release(
    root: Path, parent: Mapping[str, Mapping[str, Any]], authorities: Mapping[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    directory = safe_path(root, RELEASE_REL, file=False)
    entries = list(directory.iterdir())
    require(all(path.is_file() and not path.is_symlink() for path in entries),
            "5.6 release contains a non-regular/symlink entry")
    require({path.name for path in entries} == ALL_RELEASE_FILES,
            "5.6 release has missing/extra files")
    raw = {name: safe_path(root, RELEASE_REL / name).read_bytes() for name in ALL_RELEASE_FILES}
    documents = {
        name: parse_document_bytes(raw[name], (RELEASE_REL / name).as_posix())
        for name in ALL_RELEASE_FILES
    }
    inputs = expected_authoritative_inputs(root, parent, authorities)
    new_rows = validate_release_documents(root, documents, parent, authorities, inputs)
    manifest = documents[MANIFEST_NAME]
    validate_manifest_semantics(manifest, documents, parent, authorities, inputs)
    validate_manifest_bindings(
        manifest, documents, {name: raw[name] for name in RELEASE_FILES})
    expected_row_counts = {
        "Claim_Catalog.json": 5_525, "Claim_ID_Registry.json": 9_009,
        "Coverage_Ledger.json": 7_947, "Migration_v4_to_v5.json": 9_009,
        "Open_Claim_List.json": 2_025, "Stage5_Claim_ID_Registry.json": 9_009,
        "Strict_Conjecture_Ledger.json": 1_426, "Theorem_List.json": 3_500,
    }
    require({row["path"]: row["row_count"] for row in manifest["artifacts"]}
            == expected_row_counts, "manifest row-count semantics drifted")
    return documents, manifest, new_rows, inputs


def expected_target_pointer(manifest_file_sha: str, release_root_sha: str) -> dict[str, Any]:
    return seal({
        "schema_version": "awesome-theorems/stage5-current-release/5.6",
        "release": RELEASE,
        "manifest_path": "releases/5.6/Release_Manifest.json",
        "manifest_sha256": manifest_file_sha,
        "release_root_sha256": release_root_sha,
    })


def validate_current_pointer(
    current: Mapping[str, Any], manifest: Mapping[str, Any], manifest_file_sha: str,
    boundary: str,
) -> str:
    verify_seal(current, "Current_Release.json")
    require(boundary in {"auto", "prepublish", "published"},
            "invalid publication boundary")
    parent = authenticated_parent_pointer()
    target = expected_target_pointer(manifest_file_sha, str(manifest["release_root_sha256"]))
    if boundary == "prepublish":
        require(current == parent,
                "prepublish gate requires exact authenticated 5.5 Current_Release")
        return "prepublish"
    if boundary == "published":
        require(current == target,
                "published gate requires exact accepted 5.6 Current_Release")
        return "published"
    if current == parent:
        return "prepublish"
    if current == target:
        return "published"
    raise CheckError(
        "auto publication boundary found neither exact 5.5 parent nor exact 5.6 target pointer"
    )


def acceptance_receipt(root: Path, result: Mapping[str, Any]) -> dict[str, Any]:
    require(result.get("transaction_authenticated") is True,
            "independent receipt requires a complete authenticated release transaction")
    manifest = result["manifest"]
    authorities = result["authorities"]
    return seal({
        "schema_version": "awesome-theorems/stage5-independent-release-acceptance/5.6",
        "release": RELEASE,
        "release_root_sha256": manifest["release_root_sha256"],
        "manifest_file_sha256": result["manifest_file_sha256"],
        "manifest_authority_sha256": manifest["authority_sha256"],
        "checker_file_sha256": file_sha(safe_path(root, CHECKER_REL)),
        "generator_acceptance_authority_sha256":
        authorities["generator_receipt"]["authority_sha256"],
        "selection_authority_sha256": authorities["selection"]["authority_sha256"],
        "counts": copy.deepcopy(manifest["counts"]),
        "quality_boundary": copy.deepcopy(manifest["quality_qualification"]),
        "findings": [],
    })


def verify(repo: Path, *, boundary: str = "auto") -> dict[str, Any]:
    root = repo_root(repo)
    current_path = safe_path(root, CURRENT_REL)
    current_before = current_path.read_bytes()
    parent = check_parent(root)
    authorities = load_authorities(root, parent)
    documents, manifest, new_rows, inputs = check_release(root, parent, authorities)
    manifest_path = safe_path(root, RELEASE_REL / MANIFEST_NAME)
    manifest_file_sha = file_sha(manifest_path)
    current = parse_document_bytes(current_before, CURRENT_REL.as_posix())
    require(current_path.read_bytes() == current_before,
            "Current_Release changed during independent acceptance")
    observed_boundary = validate_current_pointer(current, manifest, manifest_file_sha, boundary)

    # Re-read every authenticated byte to close a publication/race window.
    by_name = {row["path"]: row for row in manifest["artifacts"]}
    for name in RELEASE_FILES:
        path = safe_path(root, RELEASE_REL / name)
        require(file_sha(path) == by_name[name]["sha256"],
                f"release changed during acceptance: {name}")
    require(file_sha(manifest_path) == digest(encoded(manifest)),
            "manifest changed during acceptance")
    require(current_path.read_bytes() == current_before,
            "Current_Release changed before acceptance completed")
    result: dict[str, Any] = {
        "root": root, "boundary": observed_boundary, "parent": parent,
        "authorities": authorities, "documents": documents, "manifest": manifest,
        "manifest_file_sha256": manifest_file_sha, "new_rows": new_rows,
        "authoritative_inputs": inputs, "transaction_authenticated": True,
    }
    result["receipt"] = acceptance_receipt(root, result)
    return result


def atomic_write_receipt(root: Path, receipt: Mapping[str, Any]) -> Path:
    target = root / RECEIPT_REL
    require(target.resolve().parent == (root / RECEIPT_REL.parent).resolve(),
            "receipt target escaped its fixed directory")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = encoded(receipt)
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=target.parent, prefix=target.name + ".", suffix=".tmp", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        os.replace(temporary, target)
        directory_fd = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    require(target.read_bytes() == payload, "written receipt failed byte replay")
    return target


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    boundary = parser.add_mutually_exclusive_group()
    boundary.add_argument("--auto", "--auto-boundary", dest="boundary",
                          action="store_const", const="auto",
                          help="accept exact prepublish 5.5 or published 5.6 pointer (default)")
    boundary.add_argument("--prepublish", dest="boundary", action="store_const",
                          const="prepublish", help="require exact authenticated 5.5 pointer")
    boundary.add_argument("--published", dest="boundary", action="store_const",
                          const="published", help="require exact accepted 5.6 pointer")
    parser.set_defaults(boundary="auto")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--receipt-json", action="store_true",
                        help="print only the canonical independent receipt")
    output.add_argument("--write-receipt", action="store_true",
                        help=f"atomically write only {RECEIPT_REL.as_posix()}")
    parser.add_argument("--quiet", action="store_true", help="suppress the human PASS line")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = verify(args.repo_root, boundary=args.boundary)
        if args.write_receipt:
            atomic_write_receipt(result["root"], result["receipt"])
    except (CheckError, OSError, KeyError, TypeError, ValueError, IndexError) as error:
        print(f"FAIL independent math catalog 5.6: {error}", file=sys.stderr)
        return 1
    if args.receipt_json:
        sys.stdout.buffer.write(encoded(result["receipt"]))
    elif not args.quiet:
        manifest = result["manifest"]
        print(
            "PASS independent math catalog 5.6 "
            f"mode={result['boundary']} root={manifest['release_root_sha256']} "
            f"catalog={manifest['counts']['catalog_records']} "
            f"theorem={manifest['counts']['cumulative_theorems']} "
            f"open={manifest['counts']['cumulative_open_claims']} "
            f"strict={manifest['counts']['effective_strict_conjecture_credits']} "
            f"origin_theorem={manifest['counts']['origin_theorems']} "
            f"receipt_written={args.write_receipt}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
