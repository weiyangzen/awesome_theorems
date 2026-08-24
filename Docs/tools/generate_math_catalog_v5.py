#!/usr/bin/env python3
"""Build deterministic Stage5 mathematics catalog releases.

The generator consumes the pinned ``formal-conjectures`` source snapshot,
preserves the complete Stage4 identity universe in the registries/migration,
and publishes additions-only Stage5 claim catalogs.  It deliberately records
source assertions rather than claiming that upstream ``sorry``-backed Lean
declarations were replayed or kernel checked here.

Only Python's standard library and the sibling, standard-library-only Stage5
source extractor are used.  The Stage4 generator is never imported.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_ROOT = Path(__file__).resolve().parent
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

import extract_formal_conjectures_v5 as source_extractor  # noqa: E402


PINNED_COMMIT = "2270d31e8dd611521f979de6d86da364930b7669"
SOURCE_ID = "SRC-MATH-V5-FORMAL-CONJECTURES-2270D31E"
SOURCE_ARCHIVE = (
    REPO_ROOT
    / "Docs/catalog/v5/sources/"
    "formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"
)
SOURCE_ARCHIVE_SHA256 = (
    "51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8"
)
SOURCE_ARCHIVE_SIZE = 1_614_060
EXPECTED_CANDIDATES = 2_778
EXPECTED_EXTRACTION_JSONL_SHA256 = (
    "7ec09ebc21475a41b62127fb05eb48aff90577c65b1f6b85c5ebfb11680ce2f7"
)

V4_CATALOG = REPO_ROOT / "Docs/catalog/v4/Claim_Catalog_v4.json"
V4_REGISTRY = REPO_ROOT / "Docs/catalog/v4/Claim_ID_Registry_v4.json"
V4_STAGE_REGISTRY = REPO_ROOT / "Docs/catalog/v4/Stage4_Claim_ID_Registry_v4.json"
V4_IMPORT_RECEIPT = REPO_ROOT / "Docs/catalog/v5/V4_Import_Receipt_v5.json"
CONTRACT_PATH = REPO_ROOT / "Docs/catalog/v5/Stage5_Math_Expansion_Contract_v5.json"
SCHEMA_PATH = REPO_ROOT / "Docs/catalog/v5/Math_Claim_Record_Schema_v5.json"
SOURCE_REGISTRY_PATH = REPO_ROOT / "Docs/catalog/v5/Math_Source_Registry_v5.json"

V4_FILE_LOCKS = {
    V4_CATALOG: "ec438ac0ba5c509a44c4e383d8af3423a4db3640afcd6a9881471425dc97efec",
    V4_REGISTRY: "d2ae172201591090dc6ec518749a984421aca13ea3d09c10a34a731ce4d9c615",
    V4_STAGE_REGISTRY: "aed281a3ddec28d92a927929f049ef8a9c5a4ef793df20413dff2bc8a579d0fd",
    V4_IMPORT_RECEIPT: "c1ded7be1f939b4746fe367f035f4df358fd9cc6fb993f7794f3bfe67219ca08",
}
V4_REGISTRY_AUTHORITY = (
    "86f0ab2de682035d27cd42f833515641516941a1a813c188fbd14da8ab4cec91"
)
V4_IMPORT_RECEIPT_AUTHORITY = (
    "beb8f16f2cccc41aae16277d2701fac1d187bbee0d3efd8dd04d477482929801"
)

RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
)
MANIFEST_NAME = "Release_Manifest.json"
CURRENT_NAME = "Current_Release.json"
REVIEW_DATE = "2026-08-10"
PARENT_ATV_HIGH_WATERMARK = 3_484
PARENT_ATF_HIGH_WATERMARK = 3_254
S5_0_THEOREMS = 1_000
S5_0_OPEN = 1_000
S5_1_THEOREMS = 500


class GenerationError(RuntimeError):
    """Raised when an authority or generated invariant fails closed."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def document_sha256(document: Mapping[str, Any], field: str = "authority_sha256") -> str:
    return sha256_bytes(
        canonical_json_bytes({key: value for key, value in document.items() if key != field})
    )


def seal(document: dict[str, Any]) -> dict[str, Any]:
    document = dict(document)
    document.pop("authority_sha256", None)
    document["authority_sha256"] = document_sha256(document)
    return document


def encoded_document(document: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(document) + b"\n"


def load_json_bytes(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GenerationError(f"cannot load JSON authority {path}: {error}") from error
    if not isinstance(value, dict):
        raise GenerationError(f"JSON authority must be an object: {path}")
    return value, raw


def verify_optional_seal(document: Mapping[str, Any], label: str) -> None:
    observed = document.get("authority_sha256")
    # During integration a zero digest is an explicit unsealed marker.  It is
    # still content-hash bound in every generated artifact; release checking
    # independently rejects an unsealed authority.
    if observed in (None, "0" * 64):
        return
    if observed != document_sha256(document):
        raise GenerationError(f"stale authority_sha256 in {label}")


def canonical_key(record: Mapping[str, Any]) -> str:
    return (
        f"formal-conjectures:{record['source_file']}#"
        f"{record['qualified_name']}"
    )


def source_collection(record: Mapping[str, Any]) -> str:
    parts = str(record["source_file"]).split("/")
    return parts[1] if len(parts) > 2 else "root"


def is_pointer(record: Mapping[str, Any]) -> bool:
    return "type_of%" in str(record["declaration_statement"])


def is_answer_placeholder(record: Mapping[str, Any]) -> bool:
    compact = "".join(str(record["declaration_statement"]).split())
    return "answer(sorry)" in compact


def contextual_statement_sha256(record: Mapping[str, Any]) -> str:
    return sha256_bytes(
        canonical_json_bytes(
            {
                "module": record["module"],
                "namespace": record["namespace"],
                "source_statement_sha256": record["statement_sha256"],
            }
        )
    )


def round_robin(records: Iterable[dict[str, Any]], count: int) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        buckets[(record["ams"][0], source_collection(record))].append(record)
    for values in buckets.values():
        values.sort(
            key=lambda row: (
                contextual_statement_sha256(row),
                row["qualified_name"],
                canonical_key(row),
            )
        )
    keys = sorted(buckets)
    offsets = {key: 0 for key in keys}
    selected: list[dict[str, Any]] = []
    while len(selected) < count:
        advanced = False
        for key in keys:
            offset = offsets[key]
            values = buckets[key]
            if offset >= len(values):
                continue
            selected.append(values[offset])
            offsets[key] += 1
            advanced = True
            if len(selected) == count:
                break
        if not advanced:
            break
    if len(selected) != count:
        raise GenerationError(
            f"round-robin pool has only {len(selected)} rows; required {count}"
        )
    return selected


def validate_source_argument(source_path: Path, canonical_snapshot: Any) -> None:
    observed = source_extractor.load_snapshot(source_path, expected_commit=PINNED_COMMIT)
    expected_files = {
        item.relative_path: sha256_bytes(item.data)
        for item in canonical_snapshot.source_files
    }
    observed_files = {
        item.relative_path: sha256_bytes(item.data) for item in observed.source_files
    }
    if observed_files != expected_files:
        raise GenerationError(
            "source tree/snapshot differs from the vendored canonical snapshot"
        )
    if observed.license_bytes != canonical_snapshot.license_bytes:
        raise GenerationError("source LICENSE differs from the canonical snapshot")
    if observed.readme_bytes != canonical_snapshot.readme_bytes:
        raise GenerationError("source README differs from the canonical snapshot")


def extract_candidates(source_argument: Path | None) -> tuple[list[dict[str, Any]], str]:
    if not SOURCE_ARCHIVE.is_file():
        raise GenerationError(f"missing vendored source snapshot: {SOURCE_ARCHIVE}")
    if SOURCE_ARCHIVE.stat().st_size != SOURCE_ARCHIVE_SIZE:
        raise GenerationError("vendored source snapshot size drifted")
    if sha256_file(SOURCE_ARCHIVE) != SOURCE_ARCHIVE_SHA256:
        raise GenerationError("vendored source snapshot SHA-256 drifted")
    canonical_snapshot = source_extractor.load_snapshot(
        SOURCE_ARCHIVE, expected_commit=PINNED_COMMIT
    )
    if source_argument is not None and source_argument.resolve() != SOURCE_ARCHIVE.resolve():
        validate_source_argument(source_argument, canonical_snapshot)
    records = source_extractor.extract_snapshot(canonical_snapshot)
    receipt = sha256_bytes(source_extractor.canonical_jsonl(records).encode("utf-8"))
    if len(records) != EXPECTED_CANDIDATES:
        raise GenerationError(
            f"extractor returned {len(records)} candidates, expected {EXPECTED_CANDIDATES}"
        )
    if receipt != EXPECTED_EXTRACTION_JSONL_SHA256:
        raise GenerationError(
            "formal-conjectures extraction receipt drifted; refusing silent parse change"
        )
    return records, receipt


def deduplicate(
    records: Sequence[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, tuple[dict[str, Any], str]], dict[str, list[str]]]:
    priority = {"research solved": 0, "textbook": 1, "research open": 2}
    eligible = [record for record in records if not is_pointer(record)]
    eligible.sort(key=lambda row: (priority[row["category"]], canonical_key(row)))
    winners: dict[str, dict[str, Any]] = {}
    duplicates: dict[str, tuple[dict[str, Any], str]] = {}
    aliases: dict[str, list[str]] = defaultdict(list)
    for record in eligible:
        digest = contextual_statement_sha256(record)
        previous = winners.get(digest)
        if previous is None:
            winners[digest] = record
            continue
        duplicates[canonical_key(record)] = (previous, "contextual_exact_statement")
        aliases[canonical_key(previous)].append(str(record["qualified_name"]))
    result = sorted(winners.values(), key=canonical_key)
    return result, duplicates, {key: sorted(set(value)) for key, value in aliases.items()}


def select_releases(
    unique: Sequence[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    literal_theorems = [
        row
        for row in unique
        if row["declaration_kind"] == "theorem"
        and not (
            row["category"] in {"research solved", "textbook"}
            and is_answer_placeholder(row)
        )
    ]
    solved = [row for row in literal_theorems if row["category"] == "research solved"]
    textbook = [row for row in literal_theorems if row["category"] == "textbook"]
    open_rows = [row for row in literal_theorems if row["category"] == "research open"]
    direct_open = [row for row in open_rows if not is_answer_placeholder(row)]
    problem_open = [row for row in open_rows if is_answer_placeholder(row)]

    selected_solved_50 = round_robin(solved, S5_0_THEOREMS)
    selected_solved_keys = {canonical_key(row) for row in selected_solved_50}
    remaining_solved = [
        row for row in solved if canonical_key(row) not in selected_solved_keys
    ]
    if len(direct_open) > S5_0_OPEN:
        selected_direct = round_robin(direct_open, S5_0_OPEN)
    else:
        selected_direct = sorted(direct_open, key=canonical_key)
    selected_problem = round_robin(problem_open, S5_0_OPEN - len(selected_direct))
    selected_50 = sorted(
        selected_solved_50 + selected_direct + selected_problem, key=canonical_key
    )

    solved_51_count = min(len(remaining_solved), S5_1_THEOREMS)
    selected_solved_51 = round_robin(remaining_solved, solved_51_count)
    textbook_needed = S5_1_THEOREMS - solved_51_count
    selected_textbook_51 = round_robin(textbook, textbook_needed)
    selected_51 = sorted(selected_solved_51 + selected_textbook_51, key=canonical_key)

    if len(selected_50) != 2_000 or len(selected_51) != 500:
        raise GenerationError("release selection cardinality drifted")
    if len({canonical_key(row) for row in selected_50 + selected_51}) != 2_500:
        raise GenerationError("release selections overlap or duplicate a canonical key")
    counts = {
        "credit_ready_solved_theorems": len(solved),
        "credit_ready_textbook_theorems": len(textbook),
        "credit_ready_open_theorems": len(open_rows),
        "s5_0_direct_conjectures": len(selected_direct),
        "s5_0_open_problems": len(selected_problem),
        "s5_1_research_solved": len(selected_solved_51),
        "s5_1_textbook": len(selected_textbook_51),
    }
    return selected_50, selected_51, counts


def verify_stage4() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    for path, expected in V4_FILE_LOCKS.items():
        if not path.is_file() or sha256_file(path) != expected:
            raise GenerationError(f"Stage4/import authority drifted: {path}")
    catalog, _ = load_json_bytes(V4_CATALOG)
    registry, _ = load_json_bytes(V4_REGISTRY)
    stage_registry, _ = load_json_bytes(V4_STAGE_REGISTRY)
    receipt, _ = load_json_bytes(V4_IMPORT_RECEIPT)
    if registry.get("authority_sha256") != V4_REGISTRY_AUTHORITY:
        raise GenerationError("Stage4 registry authority seal differs from frozen value")
    if document_sha256(registry) != V4_REGISTRY_AUTHORITY:
        raise GenerationError("Stage4 registry authority seal is stale")
    if receipt.get("authority_sha256") != V4_IMPORT_RECEIPT_AUTHORITY:
        raise GenerationError("V4 import receipt authority differs from frozen value")
    if document_sha256(receipt) != V4_IMPORT_RECEIPT_AUTHORITY:
        raise GenerationError("V4 import receipt authority seal is stale")
    expected_ids = {f"ATV-{ordinal:08d}" for ordinal in range(1, 3485)}
    catalog_ids = {row.get("variant_id") for row in catalog.get("records", [])}
    registry_ids = {row.get("variant_id") for row in registry.get("variants", [])}
    mapping_ids = {row.get("variant_id") for row in stage_registry.get("mappings", [])}
    if catalog_ids != expected_ids or registry_ids != expected_ids or mapping_ids != expected_ids:
        raise GenerationError("Stage4 ATV universe is not the exact continuous 1..3484 set")
    for row in stage_registry["mappings"]:
        ordinal = int(row["variant_id"].split("-")[-1])
        if row.get("stage_claim_id", row.get("stage_id")) != f"S4-CLM-{ordinal:08d}":
            raise GenerationError("Stage4 ATV/S4 ordinal mapping drifted")
    return catalog, registry, stage_registry, receipt


def authority_inventory(paths: Iterable[Path]) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for path in paths:
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(REPO_ROOT.resolve()).as_posix()
        except ValueError as error:
            raise GenerationError(f"authority path is outside the repository: {path}") from error
        if not resolved.is_file():
            raise GenerationError(f"missing authoritative input: {relative}")
        inventory.append(
            {
                "path": relative,
                "sha256": sha256_file(resolved),
                "size_bytes": resolved.stat().st_size,
            }
        )
    return sorted(inventory, key=lambda row: row["path"])


def input_authorities() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract, contract_raw = load_json_bytes(CONTRACT_PATH)
    schema, schema_raw = load_json_bytes(SCHEMA_PATH)
    sources, sources_raw = load_json_bytes(SOURCE_REGISTRY_PATH)
    verify_optional_seal(contract, str(CONTRACT_PATH))
    verify_optional_seal(sources, str(SOURCE_REGISTRY_PATH))
    inputs = {
        "contract_sha256": sha256_bytes(contract_raw),
        "contract_authority_sha256": contract.get("authority_sha256"),
        "record_schema_sha256": sha256_bytes(schema_raw),
        "source_registry_sha256": sha256_bytes(sources_raw),
        "source_registry_authority_sha256": sources.get("authority_sha256"),
        "v4_import_receipt_sha256": V4_FILE_LOCKS[V4_IMPORT_RECEIPT],
        "v4_import_receipt_authority_sha256": V4_IMPORT_RECEIPT_AUTHORITY,
    }
    return contract, schema, sources, inputs


def allocation_metadata(
    selected_50: Sequence[dict[str, Any]], selected_51: Sequence[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(selected_50 + selected_51):
        atv_ordinal = PARENT_ATV_HIGH_WATERMARK + index + 1
        family_ordinal = PARENT_ATF_HIGH_WATERMARK + index + 1
        origin = "5.0" if index < len(selected_50) else "5.1"
        output[canonical_key(record)] = {
            "origin_release": origin,
            "ordinal": atv_ordinal,
            "family_ordinal": family_ordinal,
            "variant_id": f"ATV-{atv_ordinal:08d}",
            "occurrence_id": f"ATO-{atv_ordinal:08d}",
            "sense_id": f"ATS-{atv_ordinal:08d}",
            "family_id": f"ATF-{family_ordinal:08d}",
            "stage_claim_id": f"S5-CLM-{atv_ordinal:08d}",
        }
    return output


def validate_row_shape(row: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    required = set(schema.get("required", []))
    properties = set(schema.get("properties", {}))
    missing = sorted(required - set(row))
    extras = sorted(set(row) - properties)
    if missing or extras:
        raise GenerationError(
            f"generated record/schema top-level drift: missing={missing}, extras={extras}"
        )
    definitions = schema.get("$defs", {})
    for field, definition_name in (
        ("allocation", "allocation"),
        ("locator", "source_locator"),
        ("formal_statement", "formal_statement"),
        ("statement", "statement"),
        ("mathematical_statement", "mathematical_statement"),
        ("status_detail", "status_detail"),
        ("conditionality", "conditionality"),
        ("provenance", "provenance"),
        ("rights", "rights"),
        ("dedupe", "dedupe"),
        ("frontier", "frontier"),
        ("importance", "importance"),
    ):
        definition = definitions.get(definition_name, {})
        missing_nested = set(definition.get("required", [])) - set(row[field])
        extras_nested = set(row[field]) - set(definition.get("properties", {}))
        if missing_nested or extras_nested:
            raise GenerationError(
                f"generated {field} schema drift: missing={sorted(missing_nested)}, "
                f"extras={sorted(extras_nested)}"
            )


def source_locator(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_id": SOURCE_ID,
        "revision": PINNED_COMMIT,
        "member_path": source["source_file"],
        "file_sha256": source["source_file_sha256"],
        "byte_start": source["source_block_byte_start"],
        "byte_end_exclusive": source["source_block_byte_end_exclusive"],
        "line_start": source["source_line_start"],
        "line_end": source["source_line_end"],
        "raw_block_sha256": source["source_block_sha256"],
    }


def build_claim_row(
    source: dict[str, Any],
    identity: Mapping[str, Any],
    parent_registry_authority: str,
    aliases: Sequence[str],
    extraction_receipt: str,
    schema: Mapping[str, Any],
) -> dict[str, Any]:
    source_key = canonical_key(source)
    placeholder = is_answer_placeholder(source)
    raw_category = str(source["category"])
    theorem = raw_category in {"research solved", "textbook"}
    claim_kind = "theorem" if theorem else ("open_problem" if placeholder else "conjecture")
    category = "theorem" if theorem else "open_claim"
    status = "proved" if theorem else "open"
    formal_type = str(source["statement"])
    declaration = str(source["declaration_statement"])
    docstring = str(source.get("docstring_raw", source["docstring"]))
    declaration_sha = sha256_bytes(declaration.encode("utf-8"))
    formal_type_sha = sha256_bytes(formal_type.encode("utf-8"))
    docstring_sha = sha256_bytes(docstring.encode("utf-8"))
    normalized_sha = contextual_statement_sha256(source)
    flat_statement = {
        "completeness": "source_docstring_plus_exact_formal",
        "component_extraction_status": "not_separately_parsed",
        "language": "en",
        "natural_language": str(source["docstring"]).strip(),
        "hypotheses": [],
        "conclusion": None,
        "scope": None,
        "formal_type": formal_type,
    }
    flat_statement_sha = sha256_bytes(canonical_json_bytes(flat_statement))
    nested_statement_body = dict(flat_statement)
    nested_statement_sha = sha256_bytes(canonical_json_bytes(nested_statement_body))
    mathematical_statement = {
        **nested_statement_body,
        "statement_sha256": nested_statement_sha,
    }
    semantic_payload = {
        "record_role": "claim",
        "atomicity": "atomic",
        "truth_apt": True,
        "normalized_formal_statement_sha256": normalized_sha,
        "mathematical_statement_sha256": nested_statement_sha,
    }
    semantic_sha = sha256_bytes(canonical_json_bytes(semantic_payload))
    curation_key = "formal-conjectures/" + sha256_bytes(
        source_key.encode("utf-8")
    )[:40]
    allocation_request = {
        "origin_release": identity["origin_release"],
        "source_id": SOURCE_ID,
        "qualified_name": source["qualified_name"],
        "formal_type_sha256": formal_type_sha,
        "statement_sha256": flat_statement_sha,
        "dedupe.verdict": "unique_exact_source_declaration",
        "allocation.family_action": "new_family",
    }
    locator = source_locator(source)
    formal_statement = {
        "language": "Lean4",
        "locator": locator,
        "module": source["module"],
        "namespace": source["namespace"],
        "declaration_name": source["local_name"],
        "qualified_declaration": source["qualified_name"],
        "declaration_kind": source["declaration_kind"],
        "declaration_text": declaration,
        "declaration_sha256": declaration_sha,
        "declaration_type": formal_type,
        "declaration_type_sha256": formal_type_sha,
        "docstring": docstring,
        "docstring_sha256": docstring_sha,
        "elaboration_status": "source_repository_statement",
        "axioms": [] if source.get("hasSorryFreeProof") else ["sorryAx"],
        "sorry_free": bool(source.get("hasSorryFreeProof")),
    }
    identity_payload = {
        "formal_type_sha256": formal_type_sha,
        "normalized_statement_sha256": normalized_sha,
    }
    ordinal = int(identity["ordinal"])
    row = {
        "schema_version": "awesome-theorems/stage5-math-claim-record/5.0",
        "release_id": identity["origin_release"],
        "origin_stage": "Stage5",
        "origin_release": identity["origin_release"],
        "curation_key": curation_key,
        "allocation": {
            "parent_registry_authority_sha256": parent_registry_authority,
            "allocation_request_sha256": sha256_bytes(
                canonical_json_bytes(allocation_request)
            ),
            "transaction_id": f"S5-ALLOC-{ordinal:08d}",
            "family_action": "new_family",
            "append_only": True,
        },
        "occurrence_id": identity["occurrence_id"],
        "family_id": identity["family_id"],
        "sense_id": identity["sense_id"],
        "variant_id": identity["variant_id"],
        "stage_claim_id": identity["stage_claim_id"],
        "display_name": source["qualified_name"],
        "aliases": list(aliases),
        "owner_domain": "mathematics",
        "membership_domains": ["mathematics"],
        "record_role": "claim",
        "claim_kind": claim_kind,
        "current_claim_kind": claim_kind,
        "historical_kind": claim_kind,
        "atomicity": "atomic",
        "truth_apt": True,
        "source_id": SOURCE_ID,
        "qualified_name": source["qualified_name"],
        "module": source["module"],
        "namespace": source["namespace"],
        "declaration_kind": source["declaration_kind"],
        "formal_shape": "answer_placeholder" if placeholder else "direct_prop",
        "formal_proof_state": "source_asserted_not_replayed",
        "locator": locator,
        "formal_declaration": declaration,
        "formal_declaration_sha256": declaration_sha,
        "formal_type": formal_type,
        "formal_type_sha256": formal_type_sha,
        "formal_docstring": docstring,
        "formal_docstring_sha256": docstring_sha,
        "formal_statement": formal_statement,
        "raw_category": raw_category,
        "category": category,
        "raw_status": raw_category,
        "ams": list(source["ams"]),
        "primary_ams_class": source["ams"][0],
        "classification_status": "source_curated_machine_extracted",
        "statement": flat_statement,
        "statement_sha256": flat_statement_sha,
        "mathematical_statement": mathematical_statement,
        "material_status": status,
        "status_detail": {
            "status_as_of": REVIEW_DATE,
            "basis": (
                f"Pinned Formal Conjectures category {raw_category!r} is preserved "
                "as a source assertion; no independent truth or proof replay is claimed."
            ),
            "source_refs": [SOURCE_ID],
            "evidence_level": "source_asserted_as_of",
            "resolution_criterion": (
                None if theorem else "Resolve the exact Lean proposition by proof or counterexample."
            ),
            "known_special_cases": [],
        },
        "conditionality": {
            "mode": "none",
            "assumption_variant_ids": [],
            "implication_proof_status": "not_applicable",
            "antecedent_status": "not_applicable",
            "consequent_standalone_status": "not_applicable",
            "no_status_inheritance": True,
        },
        "provenance": {
            "formal_source_ref": SOURCE_ID,
            "source_refs": [SOURCE_ID],
            "extraction_mode": "source_curated_machine_extracted",
            "extractor_version": source["schema_version"],
            "extraction_receipt_sha256": extraction_receipt,
            "source_assertion_not_independent_truth_review": True,
        },
        "rights": {
            "formal_code_terms": "Apache-2.0",
            "docstring_terms": "source-specific terms preserved; not independently cleared",
            "status": "source_terms_preserved_not_independently_cleared",
            "redistribution_mode": "source_terms_preserved_in_repository_inventory",
            "attribution": ["The Formal Conjectures Authors", source_key],
            "source_refs": [SOURCE_ID],
            "not_independently_cleared": True,
        },
        "dedupe": {
            "identity_payload_sha256": sha256_bytes(
                canonical_json_bytes(identity_payload)
            ),
            "formal_type_sha256": formal_type_sha,
            "source_statement_sha256": source["statement_sha256"],
            "normalized_statement_sha256": normalized_sha,
            "qualified_name_key": " ".join(str(source["qualified_name"]).split()).casefold(),
            "candidate_atv_ids": [],
            "verdict": "unique_exact_source_declaration",
            "validation_status": "machine_validated_exact",
            "duplicate_grants_quota": False,
            "no_evidence_or_status_inheritance": True,
        },
        "frontier": {
            "class": "source_asserted_solved" if theorem else "source_asserted_open_frontier",
            "as_of": REVIEW_DATE,
            "basis": f"Formal Conjectures source category {raw_category!r} at the pinned commit.",
            "source_refs": [SOURCE_ID],
            "evidence_level": "source_category_signal",
        },
        "importance": {
            "tier": "unranked_research_level",
            "basis": "source_category_signal_only",
            "rationale": "No independent per-record importance ranking was performed.",
            "evidence_level": "unranked",
        },
        "lifecycle": "active",
        "lineage": [],
        "semantic_payload_sha256": semantic_sha,
    }
    validate_row_shape(row, schema)
    return row


def new_registry_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        families.append(
            {
                "family_id": row["family_id"],
                "curation_key": row["curation_key"],
                "display_titles": [row["display_name"]] + list(row["aliases"]),
                "member_occurrence_ids": [row["occurrence_id"]],
                "historical_member_occurrence_ids": [row["occurrence_id"]],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_source_derived_exact_family",
                "lifecycle": "current",
                "semantic_equivalence_asserted": True,
            }
        )
        senses.append(
            {
                "sense_id": row["sense_id"],
                "family_id": row["family_id"],
                "bootstrap_occurrence_id": row["occurrence_id"],
                "curation_key": row["curation_key"],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_source_derived_exact_sense",
                "lifecycle": "current",
            }
        )
        variants.append(
            {
                "variant_id": row["variant_id"],
                "sense_id": row["sense_id"],
                "bootstrap_occurrence_id": row["occurrence_id"],
                "curation_key": row["curation_key"],
                "idempotency_request_sha256": request,
                "semantic_payload_sha256": row["semantic_payload_sha256"],
                "identity_state": "stage5_source_derived_exact_variant",
                "lifecycle": "current",
            }
        )
    return families, senses, variants


def build_registry(
    release: str,
    baseline: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    parent_authority: str,
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    new_families, new_senses, new_variants = new_registry_rows(rows)
    document = {
        "schema_version": "awesome-theorems/claim-id-registry/5.0",
        "artifact": "Claim_ID_Registry.json",
        "release": release,
        "parent_registry_authority_sha256": parent_authority,
        "baseline_registry_authority_sha256": V4_REGISTRY_AUTHORITY,
        "authoritative_inputs": dict(inputs),
        "allocation_policy": {
            "append_only": True,
            "first_new_atv_ordinal": 3485,
            "new_family_first_atf_ordinal": 3255,
            "status_metadata_does_not_renumber": True,
        },
        "namespace_high_watermarks": {
            "ATF": PARENT_ATF_HIGH_WATERMARK + len(rows),
            "ATO": PARENT_ATV_HIGH_WATERMARK + len(rows),
            "ATS": PARENT_ATV_HIGH_WATERMARK + len(rows),
            "ATV": PARENT_ATV_HIGH_WATERMARK + len(rows),
        },
        "families": list(baseline["families"]) + new_families,
        "senses": list(baseline["senses"]) + new_senses,
        "variants": list(baseline["variants"]) + new_variants,
        "legacy_aliases": list(baseline.get("legacy_aliases", [])),
        "redirects": list(baseline.get("redirects", [])),
        "splits": list(baseline.get("splits", [])),
        "family_membership_extensions": list(
            baseline.get("family_membership_extensions", [])
        ),
        "counts": {
            "families": len(baseline["families"]) + len(new_families),
            "senses": len(baseline["senses"]) + len(new_senses),
            "variants": len(baseline["variants"]) + len(new_variants),
            "stage4_variants": len(baseline["variants"]),
            "stage5_additions": len(new_variants),
            "legacy_aliases": len(baseline.get("legacy_aliases", [])),
            "redirects": len(baseline.get("redirects", [])),
            "splits": len(baseline.get("splits", [])),
        },
    }
    return seal(document)


def build_stage_mapping(
    release: str,
    baseline_mapping: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    by_variant = {row["variant_id"]: row for row in baseline_mapping["mappings"]}
    mappings: list[dict[str, Any]] = []
    for ordinal in range(1, PARENT_ATV_HIGH_WATERMARK + 1):
        variant = f"ATV-{ordinal:08d}"
        old = by_variant[variant]
        mappings.append(
            {
                "ordinal": ordinal,
                "variant_id": variant,
                "predecessor_stage_claim_id": old.get("stage_claim_id", old.get("stage_id")),
                "stage_claim_id": f"S5-CLM-{ordinal:08d}",
                "lifecycle": "current",
            }
        )
    for row in rows:
        ordinal = int(str(row["variant_id"]).split("-")[-1])
        mappings.append(
            {
                "ordinal": ordinal,
                "variant_id": row["variant_id"],
                "predecessor_stage_claim_id": None,
                "stage_claim_id": row["stage_claim_id"],
                "lifecycle": "current",
            }
        )
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-id-registry/5.0",
            "artifact": "Stage5_Claim_ID_Registry.json",
            "release": release,
            "authoritative_inputs": dict(inputs),
            "numbering_policy": "S5 ordinal equals canonical ATV ordinal",
            "counts": {"mappings": len(mappings)},
            "mappings": mappings,
        }
    )


def terminal_resolution(
    variant_id: str,
    registry: Mapping[str, Any],
) -> dict[str, Any]:
    redirects = {
        row["source_variant_id"]: row["target_variant_id"]
        for row in registry.get("redirects", [])
    }
    splits = {
        row["source_variant_id"]: list(row["child_variant_ids"])
        for row in registry.get("splits", [])
    }
    if variant_id in splits:
        terminals = splits[variant_id]
        kind = "split"
    elif variant_id in redirects:
        terminals = [redirects[variant_id]]
        kind = "redirect"
    else:
        terminals = [variant_id]
        kind = "current"
    return {
        "kind": kind,
        "terminal_atv_ids": terminals,
        "terminal_s5_ids": [
            f"S5-CLM-{int(value.split('-')[-1]):08d}" for value in terminals
        ],
        "default_child": None,
        "evidence_inherited": False,
    }


def build_migration(
    release: str,
    v4_catalog: Mapping[str, Any],
    v4_registry: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    v4_by_id = {row["variant_id"]: row for row in v4_catalog["records"]}
    migrations: list[dict[str, Any]] = []
    for ordinal in range(1, PARENT_ATV_HIGH_WATERMARK + 1):
        variant = f"ATV-{ordinal:08d}"
        migrations.append(
            {
                "ordinal": ordinal,
                "variant_id": variant,
                "v4_variant_id": variant,
                "s4_claim_id": f"S4-CLM-{ordinal:08d}",
                "stage_claim_id": f"S5-CLM-{ordinal:08d}",
                "migration_action": "historical_binding_preserved",
                "predecessor_record_sha256": sha256_bytes(
                    canonical_json_bytes(v4_by_id[variant])
                ),
                "current_resolution": terminal_resolution(variant, v4_registry),
            }
        )
    for row in rows:
        ordinal = int(str(row["variant_id"]).split("-")[-1])
        migrations.append(
            {
                "ordinal": ordinal,
                "variant_id": row["variant_id"],
                "v4_variant_id": None,
                "s4_claim_id": None,
                "stage_claim_id": row["stage_claim_id"],
                "migration_action": "new_stage5_allocation",
                "predecessor_record_sha256": None,
                "current_resolution": {
                    "kind": "current",
                    "terminal_atv_ids": [row["variant_id"]],
                    "terminal_s5_ids": [row["stage_claim_id"]],
                    "default_child": None,
                    "evidence_inherited": False,
                },
            }
        )
    return seal(
        {
            "schema_version": "awesome-theorems/migration-v4-to-v5/5.0",
            "artifact": "Migration_v4_to_v5.json",
            "release": release,
            "authoritative_inputs": authority_inventory(
                (
                    V4_CATALOG,
                    V4_REGISTRY,
                    V4_STAGE_REGISTRY,
                    V4_IMPORT_RECEIPT,
                    CONTRACT_PATH,
                    SCHEMA_PATH,
                    SOURCE_REGISTRY_PATH,
                )
            ),
            "v4_import_receipt": {
                "path": "Docs/catalog/v5/V4_Import_Receipt_v5.json",
                "sha256": V4_FILE_LOCKS[V4_IMPORT_RECEIPT],
                "authority_sha256": V4_IMPORT_RECEIPT_AUTHORITY,
            },
            "counts": {
                "historical_bindings": PARENT_ATV_HIGH_WATERMARK,
                "new_allocations": len(rows),
                "migrations": len(migrations),
            },
            "migrations": migrations,
        }
    )


def theorem_predicate(row: Mapping[str, Any]) -> bool:
    return (
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "theorem"
        and row.get("declaration_kind") == "theorem"
        and row.get("current_claim_kind") == "theorem"
        and row.get("material_status") == "proved"
    )


def open_predicate(row: Mapping[str, Any]) -> bool:
    return (
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("declaration_kind") == "theorem"
        and row.get("current_claim_kind") in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status") in {"open", "partial", "independent", "disputed"}
    )


def build_projection(
    release: str,
    name: str,
    rows: Sequence[dict[str, Any]],
    predicate: Any,
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    selected = [row for row in rows if predicate(row)]
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-query-projection/5.0",
            "artifact": name,
            "release": release,
            "authoritative_inputs": dict(inputs),
            "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
            "stage_claim_ids": [row["stage_claim_id"] for row in selected],
            "counts": {"records": len(selected)},
            "records": selected,
        }
    )


def candidate_disposition(
    record: Mapping[str, Any],
    release: str,
    duplicate_map: Mapping[str, tuple[dict[str, Any], str]],
    identities: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    key = canonical_key(record)
    identity = identities.get(key)
    identity_visible = (
        identity
        if identity is not None
        and (identity["origin_release"] == "5.0" or release == "5.1")
        else None
    )
    duplicate = duplicate_map.get(key)
    target_variant: str | None = None
    target_stage: str | None = None
    duplicate_of_variant: str | None = None
    reason_code: str
    accepted = identity is not None and identity["origin_release"] == release
    if accepted:
        disposition = "accepted_new_claim"
        grants = True
        target_variant = str(identity["variant_id"])
        target_stage = str(identity["stage_claim_id"])
        reason_code = "deterministic_round_robin_quota_selection"
    elif identity_visible is not None and identity_visible["origin_release"] != release:
        disposition = "already_allocated_noncredit"
        grants = False
        target_variant = str(identity_visible["variant_id"])
        target_stage = str(identity_visible["stage_claim_id"])
        reason_code = "allocated_in_parent_release"
    elif is_pointer(record):
        disposition = "pointer_noncredit"
        grants = False
        reason_code = "type_of_pointer_no_identity_credit"
    elif duplicate is not None:
        grants = False
        winner_key = canonical_key(duplicate[0])
        winner_identity = identities.get(winner_key)
        winner_visible = (
            winner_identity
            if winner_identity is not None
            and (winner_identity["origin_release"] == "5.0" or release == "5.1")
            else None
        )
        if winner_visible is not None:
            disposition = "duplicate_noncredit"
            duplicate_of_variant = str(winner_visible["variant_id"])
            reason_code = duplicate[1]
        else:
            disposition = "excluded_by_source_policy"
            reason_code = "duplicate_winner_not_allocated_in_release"
    elif record["declaration_kind"] != "theorem":
        disposition = "excluded_by_source_policy"
        grants = False
        reason_code = "literal_theorem_only_quota"
    elif record["category"] in {"research solved", "textbook"} and is_answer_placeholder(record):
        disposition = "status_blocked"
        grants = False
        reason_code = "solved_answer_placeholder_quarantined"
    elif record["category"] == "research open" and identity_visible is None:
        disposition = "open_reserve_noncredit"
        grants = False
        reason_code = "deterministic_open_reserve_not_allocated"
    else:
        disposition = "excluded_by_source_policy"
        grants = False
        if identity_visible is not None:
            target_variant = str(identity_visible["variant_id"])
            target_stage = str(identity_visible["stage_claim_id"])
            reason_code = "allocated_in_parent_release"
        else:
            reason_code = "deterministic_theorem_reserve_not_allocated"
    locator_sha = sha256_bytes(canonical_json_bytes(source_locator(record)))
    return {
        "candidate_key": key,
        "source_id": SOURCE_ID,
        "qualified_name": record["qualified_name"],
        "source_statement_sha256": record["statement_sha256"],
        "normalized_statement_sha256": contextual_statement_sha256(record),
        "disposition": disposition,
        "reason_code": reason_code,
        "target_variant_id": target_variant,
        "target_s5_id": target_stage,
        "duplicate_of_variant_id": duplicate_of_variant,
        "grants_quota": grants,
        "origin_release": (
            str(identity_visible["origin_release"])
            if identity_visible is not None
            else release
        ),
        "evidence_locator_sha256": locator_sha,
    }


def build_coverage(
    release: str,
    all_candidates: Sequence[dict[str, Any]],
    duplicate_map: Mapping[str, tuple[dict[str, Any], str]],
    identities: Mapping[str, Mapping[str, Any]],
    rows: Sequence[Mapping[str, Any]],
    contract: Mapping[str, Any],
    selection_counts: Mapping[str, int],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    dispositions = [
        candidate_disposition(record, release, duplicate_map, identities)
        for record in sorted(all_candidates, key=canonical_key)
    ]
    top_classes = list(contract.get("msc_coverage_policy", {}).get("top_level_classes", []))
    if len(top_classes) != 63 or len(set(top_classes)) != 63:
        raise GenerationError("contract does not freeze the exact 63 MSC2020 top classes")
    origin_rows = [row for row in rows if row["origin_release"] == release]
    candidate_by_key = {canonical_key(record): record for record in all_candidates}
    reserve_keys = sorted(
        item["candidate_key"]
        for item in dispositions
        if item["disposition"] == "open_reserve_noncredit"
    )
    msc_rows: list[dict[str, Any]] = []
    for code in top_classes:
        current_theorem = sorted(
            row["stage_claim_id"]
            for row in rows
            if theorem_predicate(row) and row["primary_ams_class"] == code
        )
        current_open = sorted(
            row["stage_claim_id"]
            for row in rows
            if open_predicate(row) and row["primary_ams_class"] == code
        )
        origin_theorem = sorted(
            row["stage_claim_id"]
            for row in origin_rows
            if theorem_predicate(row) and row["primary_ams_class"] == code
        )
        origin_open = sorted(
            row["stage_claim_id"]
            for row in origin_rows
            if open_predicate(row) and row["primary_ams_class"] == code
        )
        class_reserve = sorted(
            key for key in reserve_keys if candidate_by_key[key]["ams"][0] == code
        )
        classified_count = len(current_theorem) + len(current_open) + len(class_reserve)
        if classified_count == 0:
            scarcity = "zero"
            scarcity_reason = "No current or open-reserve member has this primary source annotation."
        elif classified_count < 10:
            scarcity = "thin"
            scarcity_reason = "Fewer than ten current-plus-reserve members have this primary class."
        else:
            scarcity = "adequate_in_source_inventory"
            scarcity_reason = "At least ten current-plus-reserve members have this primary class."
        msc_rows.append(
            {
                "msc_top_class": code,
                "current_theorem_s5_ids": current_theorem,
                "current_open_s5_ids": current_open,
                "origin_theorem_s5_ids": origin_theorem,
                "origin_open_s5_ids": origin_open,
                "open_reserve_candidate_keys": class_reserve,
                "source_ids": [SOURCE_ID] if classified_count else [],
                "classification_basis_counts": {
                    "source_annotation": classified_count,
                    "machine_crosswalk": 0,
                    "independent_review": 0,
                },
                "scarcity": scarcity,
                "scarcity_reason": scarcity_reason,
                "counts": {
                    "current_theorems": len(current_theorem),
                    "current_open": len(current_open),
                    "origin_theorems": len(origin_theorem),
                    "origin_open": len(origin_open),
                    "open_reserve": len(class_reserve),
                },
            }
        )
    disposition_counts = Counter(item["disposition"] for item in dispositions)
    document = {
        "schema_version": "awesome-theorems/stage5-coverage-ledger/5.0",
        "release": release,
        "candidate_dispositions": dispositions,
        "msc_coverage": msc_rows,
        "counts": {
            "candidate_dispositions": len(dispositions),
            "msc_coverage": len(msc_rows),
            "accepted_new_claims": disposition_counts["accepted_new_claim"],
            "open_reserve_noncredit": disposition_counts["open_reserve_noncredit"],
        },
    }
    return seal(document)


def build_catalog(
    release: str,
    rows: Sequence[dict[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    origin = [row for row in rows if row["origin_release"] == release]
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-catalog/5.0",
            "artifact": "Claim_Catalog.json",
            "release": release,
            "catalog_scope": "cumulative Stage5 additions only",
            "authoritative_inputs": dict(inputs),
            "counts": {
                "records": len(rows),
                "origin_theorems": sum(theorem_predicate(row) for row in origin),
                "origin_open_claims": sum(open_predicate(row) for row in origin),
                "cumulative_theorems": sum(theorem_predicate(row) for row in rows),
                "cumulative_open_claims": sum(open_predicate(row) for row in rows),
            },
            "records": list(rows),
        }
    )


def primary_row_count(document: Mapping[str, Any]) -> int:
    candidates = document.get("candidate_dispositions")
    coverage = document.get("msc_coverage")
    if isinstance(candidates, list) and isinstance(coverage, list):
        return len(candidates) + len(coverage)
    for key in ("records", "variants", "mappings", "migrations", "entries", "rows"):
        value = document.get(key)
        if isinstance(value, list):
            return len(value)
    return 0


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    payload = [
        {
            "path": row["path"],
            "sha256": row["sha256"],
            "size_bytes": row["size_bytes"],
        }
        for row in sorted(inventory, key=lambda item: str(item["path"]))
    ]
    return sha256_bytes(canonical_json_bytes(payload))


def package_release(
    release: str,
    artifacts: Mapping[str, Mapping[str, Any]],
    parent_release: str | None,
    parent_root: str | None,
) -> tuple[dict[str, bytes], str]:
    encoded = {name: encoded_document(artifacts[name]) for name in RELEASE_FILES}
    inventory = [
        {
            "path": name,
            "sha256": sha256_bytes(encoded[name]),
            "size_bytes": len(encoded[name]),
            "row_count": primary_row_count(artifacts[name]),
        }
        for name in sorted(RELEASE_FILES)
    ]
    root = release_root(inventory)
    catalog_counts = artifacts["Claim_Catalog.json"]["counts"]
    manifest = seal(
        {
            "schema_version": "awesome-theorems/stage5-release-manifest/5.0",
            "release": release,
            "parent_release": parent_release,
            "parent_release_root_sha256": parent_root,
            "release_root_sha256": root,
            "artifacts": inventory,
            "counts": {
                "non_manifest_artifacts": len(inventory),
                "catalog_records": catalog_counts["records"],
                "origin_theorems": catalog_counts["origin_theorems"],
                "origin_open_claims": catalog_counts["origin_open_claims"],
            },
        }
    )
    encoded[MANIFEST_NAME] = encoded_document(manifest)
    return encoded, root


def build_all(source_argument: Path | None) -> tuple[dict[str, dict[str, bytes]], dict[str, str], dict[str, int]]:
    contract, schema, _sources, inputs = input_authorities()
    v4_catalog, v4_registry, v4_stage_registry, _receipt = verify_stage4()
    candidates, extraction_receipt = extract_candidates(source_argument)
    unique, duplicate_map, aliases = deduplicate(candidates)
    selected_50, selected_51, selection_counts = select_releases(unique)
    identities = allocation_metadata(selected_50, selected_51)
    inputs = {
        **inputs,
        "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
        "source_commit": PINNED_COMMIT,
        "extractor_records_jsonl_sha256": extraction_receipt,
        "v4_registry_authority_sha256": V4_REGISTRY_AUTHORITY,
    }

    rows_50 = [
        build_claim_row(
            source,
            identities[canonical_key(source)],
            V4_REGISTRY_AUTHORITY,
            aliases.get(canonical_key(source), []),
            extraction_receipt,
            schema,
        )
        for source in selected_50
    ]
    registry_50 = build_registry("5.0", v4_registry, rows_50, V4_REGISTRY_AUTHORITY, inputs)
    rows_51_new = [
        build_claim_row(
            source,
            identities[canonical_key(source)],
            registry_50["authority_sha256"],
            aliases.get(canonical_key(source), []),
            extraction_receipt,
            schema,
        )
        for source in selected_51
    ]
    rows_50.sort(key=lambda row: row["variant_id"])
    rows_51_new.sort(key=lambda row: row["variant_id"])
    rows_51 = rows_50 + rows_51_new
    registry_51 = build_registry(
        "5.1", v4_registry, rows_51, registry_50["authority_sha256"], inputs
    )

    def artifacts_for(release: str, rows: list[dict[str, Any]], registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {
            "Claim_Catalog.json": build_catalog(release, rows, inputs),
            "Claim_ID_Registry.json": registry,
            "Stage5_Claim_ID_Registry.json": build_stage_mapping(
                release, v4_stage_registry, rows, inputs
            ),
            "Migration_v4_to_v5.json": build_migration(
                release, v4_catalog, v4_registry, rows, inputs
            ),
            "Theorem_List.json": build_projection(
                release, "Theorem_List.json", rows, theorem_predicate, inputs
            ),
            "Open_Claim_List.json": build_projection(
                release, "Open_Claim_List.json", rows, open_predicate, inputs
            ),
            "Coverage_Ledger.json": build_coverage(
                release,
                candidates,
                duplicate_map,
                identities,
                rows,
                contract,
                selection_counts,
                inputs,
            ),
        }

    artifacts_50 = artifacts_for("5.0", rows_50, registry_50)
    package_50, root_50 = package_release("5.0", artifacts_50, None, None)
    artifacts_51 = artifacts_for("5.1", rows_51, registry_51)
    package_51, root_51 = package_release("5.1", artifacts_51, "5.0", root_50)
    return {"5.0": package_50, "5.1": package_51}, {"5.0": root_50, "5.1": root_51}, selection_counts


def compare_release(path: Path, expected: Mapping[str, bytes]) -> None:
    expected_names = set(expected)
    if not path.is_dir():
        raise GenerationError(f"release directory is missing: {path}")
    actual_names = {item.name for item in path.iterdir() if item.is_file()}
    non_files = [item.name for item in path.iterdir() if not item.is_file()]
    if actual_names != expected_names or non_files:
        raise GenerationError(
            f"release artifact set differs at {path}: files={sorted(actual_names)}, "
            f"non_files={sorted(non_files)}"
        )
    for name in sorted(expected):
        if (path / name).read_bytes() != expected[name]:
            raise GenerationError(f"immutable release byte drift: {path / name}")


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def publish_release(output_root: Path, release: str, package: Mapping[str, bytes]) -> None:
    releases = output_root / "releases"
    target = releases / release
    output_root.mkdir(parents=True, exist_ok=True)
    releases.mkdir(parents=True, exist_ok=True)
    if target.exists():
        compare_release(target, package)
        return
    temporary = Path(tempfile.mkdtemp(prefix=f".{release}.tmp-", dir=releases))
    try:
        # Manifest is written last inside the private directory.
        for name in list(sorted(RELEASE_FILES)) + [MANIFEST_NAME]:
            path = temporary / name
            with path.open("xb") as stream:
                stream.write(package[name])
                stream.flush()
                os.fsync(stream.fileno())
        fsync_directory(temporary)
        try:
            os.rename(temporary, target)
        except FileExistsError:
            compare_release(target, package)
            shutil.rmtree(temporary)
        fsync_directory(releases)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


def update_current(output_root: Path, release: str, package: Mapping[str, bytes], root: str) -> None:
    manifest_sha = sha256_bytes(package[MANIFEST_NAME])
    pointer = seal(
        {
            "schema_version": "awesome-theorems/stage5-current-release/5.0",
            "release": release,
            "release_root_sha256": root,
            "manifest_sha256": manifest_sha,
            "manifest_path": f"releases/{release}/{MANIFEST_NAME}",
        }
    )
    payload = encoded_document(pointer)
    descriptor, raw_path = tempfile.mkstemp(prefix=".Current_Release.tmp-", dir=output_root)
    temporary = Path(raw_path)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output_root / CURRENT_NAME)
        fsync_directory(output_root)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--source-root",
        type=Path,
        help="pinned formal-conjectures checkout root (validated against the canonical snapshot)",
    )
    source_group.add_argument(
        "--source-snapshot",
        type=Path,
        help="pinned formal-conjectures tar snapshot (default: vendored canonical snapshot)",
    )
    parser.add_argument("--release", choices=("5.0", "5.1"))
    parser.add_argument(
        "--output-root",
        type=Path,
        default=REPO_ROOT / "Docs/catalog/v5",
        help="Stage5 catalog output root",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare existing release bytes; with no --release checks both releases",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="fully build and validate in memory without writing",
    )
    args = parser.parse_args(argv)
    if args.check and args.dry_run:
        parser.error("--check and --dry-run are mutually exclusive")
    if not args.check and not args.dry_run and args.release is None:
        parser.error("--release is required when publishing")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    source_argument = args.source_root or args.source_snapshot
    output_root = args.output_root.resolve()
    try:
        packages, roots, selection_counts = build_all(source_argument)
        if args.check:
            releases = (args.release,) if args.release else ("5.0", "5.1")
            for release in releases:
                compare_release(output_root / "releases" / release, packages[release])
            joined = ",".join(releases)
            print(
                f"PASS generate_math_catalog_v5 --check releases={joined} "
                f"roots={','.join(roots[value] for value in releases)}"
            )
            return 0
        if args.dry_run:
            releases = (args.release,) if args.release else ("5.0", "5.1")
            print(
                "PASS generate_math_catalog_v5 --dry-run "
                f"releases={','.join(releases)} "
                f"selection={json.dumps(selection_counts, sort_keys=True, separators=(',', ':'))}"
            )
            return 0
        assert args.release is not None
        if args.release == "5.1":
            compare_release(output_root / "releases" / "5.0", packages["5.0"])
        publish_release(output_root, args.release, packages[args.release])
        update_current(output_root, args.release, packages[args.release], roots[args.release])
        print(
            f"PASS generate_math_catalog_v5 release={args.release} "
            f"root={roots[args.release]}"
        )
        return 0
    except (GenerationError, OSError, ValueError, TypeError, KeyError) as error:
        print(f"FAIL generate_math_catalog_v5: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
