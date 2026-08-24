#!/usr/bin/env python3
"""Independent acceptance checker for immutable Stage5 release 5.4.

This checker intentionally imports neither the 5.4 curation builder nor any
catalog generator.  It replays the source selection, identity gates, record
construction, payload hashes, append-only projections, manifest/root formula,
and Current_Release compare-and-swap directly from the pinned inputs.
"""

from __future__ import annotations

import copy
import argparse
from collections import Counter, defaultdict, deque
import hashlib
import json
from pathlib import Path
import re
import sys
import subprocess
from typing import Any, Iterable, Mapping, Sequence
import unicodedata


REPO_ROOT = Path(__file__).resolve().parents[4]
V5_ROOT = REPO_ROOT / "Docs/catalog/v5"
PARENT_DIR = V5_ROOT / "releases/5.3"
RELEASE_DIR = V5_ROOT / "releases/5.4"
READABLE_DIR = V5_ROOT / "readable/5.4"
SOURCE_PATH = V5_ROOT / "sources/mathlib-theorems-8a178386.json"
PARENT_CURATION_PATH = V5_ROOT / "curation/Mathlib_Theorem_Curation_v5_3.json"
CURATION_PATH = V5_ROOT / "curation/Mathlib_Theorem_Curation_v5_4.json"
CONTRACT_PATH = V5_ROOT / "Stage5_Math_Expansion_Contract_v5_4.json"
SCHEMA_PATH = V5_ROOT / "Math_Claim_Record_Schema_v5_4.json"
SOURCE_REGISTRY_PATH = V5_ROOT / "Math_Source_Registry_v5_4.json"
PARENT_RECEIPT_PATH = V5_ROOT / "V5_3_Parent_Receipt_v5_4.json"
CURRENT_PATH = V5_ROOT / "Current_Release.json"

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

SOURCE_ID = "SRC-MATH-V5-MATHLIB-8A178386"
SOURCE_SHA256 = "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
SOURCE_SIZE_BYTES = 6_316_287
SOURCE_CONTENT_DIGEST = "dd49c8322d8eded995c84a235fd458fc093a187230323f87bea78049ae90e53b"
MATHLIB_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
PARENT_ROOT = "9ec5a097c0286b6751b02e89d18c400aab655021ba1ad4843eadba5a69fc41fa"
PARENT_MANIFEST_SHA256 = "8384deebd8ff33cf06c592ed443fd3ed78a4a294c4cea106362705e95954419a"
PARENT_CATALOG_SHA256 = "957da23fbd1e50244912fb6dbb76fbf663e7970ace3f6da8b19407929211a8bb"
PARENT_CURATION_SHA256 = "379e165ae52ffd911e383fdb351fc602d36ec585e40bade54612c1512a7a1905"
PARENT_CURATION_AUTHORITY = "9661eebbd25bbb8aee3a0c7ae1c9cbe671ec77324f889d25e967811ffd9f7d5d"
PARENT_ATV_HIGH = 7_084
PARENT_ATF_HIGH = 6_854
LAST_ATV = 7_584
LAST_ATF = 7_354
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

ATO_RE = re.compile(r"^ATO-([0-9]{8})$")
ATF_RE = re.compile(r"^ATF-([0-9]{8})$")
ATS_RE = re.compile(r"^ATS-([0-9]{8})$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


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
        raise CheckError(f"not canonical-JSON serializable: {error}") from error


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


def load_json(path: Path, *, canonical: bool = False) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"cannot load {path}: {error}") from error
    require(isinstance(value, dict), f"{path} must contain one JSON object")
    if canonical:
        require(raw == encoded_document(value), f"{path} is not canonical JSON plus one newline")
    return value


def verify_seal(document: Mapping[str, Any], label: str) -> None:
    observed = document.get("authority_sha256")
    require(
        isinstance(observed, str)
        and re.fullmatch(r"[a-f0-9]{64}", observed) is not None
        and observed == hash_without(document, "authority_sha256"),
        f"{label} has a stale/invalid authority_sha256",
    )


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def artifact_binding(path: Path, document: Mapping[str, Any]) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": relative(path),
        "file_sha256": sha256_bytes(raw),
        "size_bytes": len(raw),
        "authority_sha256": document["authority_sha256"],
    }


def primary_row_count(document: Mapping[str, Any]) -> int:
    candidates = document.get("candidate_dispositions")
    coverage = document.get("msc_coverage")
    if isinstance(candidates, list) and isinstance(coverage, list):
        return len(candidates) + len(coverage)
    strict = document.get("strict_credits")
    corrections = document.get("credit_corrections")
    if isinstance(strict, list) and isinstance(corrections, list):
        return len(strict) + len(corrections)
    for key in ("records", "variants", "mappings", "migrations", "rows"):
        rows = document.get(key)
        if isinstance(rows, list):
            return len(rows)
    return 0


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    normalized = [
        {"path": row["path"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}
        for row in sorted(inventory, key=lambda row: str(row["path"]))
    ]
    return sha256_bytes(canonical_json_bytes(normalized))


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
    require(isinstance(module, str), "source row lacks source.module")
    pieces = module.split(".")
    require(
        len(pieces) >= 2 and pieces[0] == "Mathlib" and bool(pieces[1]),
        f"invalid mathlib module path: {module!r}",
    )
    return pieces[1]


def _json_type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, False)


def validate_closed_schema(row: Mapping[str, Any], schema: Mapping[str, Any], label: str) -> None:
    require(schema.get("type") == "object", "5.4 record schema type drifted")
    require(schema.get("additionalProperties") is False, "5.4 schema is not closed")
    required = schema.get("required")
    properties = schema.get("properties")
    require(isinstance(required, list) and isinstance(properties, dict), "malformed 5.4 schema")
    require(
        len(required) == len(set(required)) and set(required) == set(properties),
        "5.4 schema required/property closure drifted",
    )
    require(set(row) == set(required), f"{label} top-level field closure differs from schema")
    for field, specification in properties.items():
        require(isinstance(specification, dict), f"malformed schema property {field}")
        value = row[field]
        if "const" in specification:
            require(value == specification["const"], f"{label}.{field} violates const")
        expected_type = specification.get("type")
        if isinstance(expected_type, str):
            require(_json_type_matches(value, expected_type), f"{label}.{field} violates type")
        minimum = specification.get("minLength")
        if isinstance(minimum, int):
            require(isinstance(value, str) and len(value) >= minimum, f"{label}.{field} is empty")
        pattern = specification.get("pattern")
        if isinstance(pattern, str):
            require(isinstance(value, str) and re.fullmatch(pattern, value) is not None, f"{label}.{field} violates pattern")


def validate_schema_instance(
    value: Any,
    schema: Mapping[str, Any],
    root: Mapping[str, Any],
    location: str = "$",
) -> None:
    reference = schema.get("$ref")
    if reference is not None:
        require(isinstance(reference, str) and reference.startswith("#/"), f"unsupported schema ref at {location}")
        target: Any = root
        for component in reference[2:].split("/"):
            target = target[component.replace("~1", "/").replace("~0", "~")]
        validate_schema_instance(value, target, root, location)
        return
    for subschema in schema.get("allOf", []):
        validate_schema_instance(value, subschema, root, location)
    one_of = schema.get("oneOf")
    if isinstance(one_of, list):
        matches = 0
        for subschema in one_of:
            try:
                validate_schema_instance(value, subschema, root, location)
            except CheckError:
                continue
            matches += 1
        require(matches == 1, f"schema oneOf mismatch at {location}")
    negated = schema.get("not")
    if isinstance(negated, dict):
        try:
            validate_schema_instance(value, negated, root, location)
        except CheckError:
            pass
        else:
            raise CheckError(f"schema not mismatch at {location}")
    conditional = schema.get("if")
    if isinstance(conditional, dict):
        try:
            validate_schema_instance(value, conditional, root, location)
        except CheckError:
            matches_condition = False
        else:
            matches_condition = True
        branch = schema.get("then" if matches_condition else "else")
        if isinstance(branch, dict):
            validate_schema_instance(value, branch, root, location)
    if "const" in schema:
        require(value == schema["const"], f"schema const mismatch at {location}")
    if "enum" in schema:
        require(value in schema["enum"], f"schema enum mismatch at {location}")
    expected_type = schema.get("type")
    if expected_type is not None:
        accepted = [expected_type] if isinstance(expected_type, str) else expected_type
        require(any(_json_type_matches(value, item) for item in accepted), f"schema type mismatch at {location}")
    if isinstance(value, dict):
        missing = [item for item in schema.get("required", []) if item not in value]
        require(not missing, f"schema missing fields at {location}: {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            require(not extras, f"schema extra fields at {location}: {extras}")
        for key, item in value.items():
            child = properties.get(key)
            if isinstance(child, dict):
                validate_schema_instance(item, child, root, f"{location}.{key}")
    if isinstance(value, list):
        minimum = schema.get("minItems")
        maximum = schema.get("maxItems")
        if minimum is not None:
            require(len(value) >= int(minimum), f"schema minItems mismatch at {location}")
        if maximum is not None:
            require(len(value) <= int(maximum), f"schema maxItems mismatch at {location}")
        if schema.get("uniqueItems"):
            require(len({canonical_json_bytes(item) for item in value}) == len(value), f"schema uniqueItems mismatch at {location}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_schema_instance(item, item_schema, root, f"{location}[{index}]")
        contains = schema.get("contains")
        if isinstance(contains, dict):
            matches = 0
            for index, item in enumerate(value):
                try:
                    validate_schema_instance(item, contains, root, f"{location}[{index}]")
                except CheckError:
                    continue
                matches += 1
            require(matches >= int(schema.get("minContains", 1)), f"schema contains mismatch at {location}")
            if schema.get("maxContains") is not None:
                require(matches <= int(schema["maxContains"]), f"schema maxContains mismatch at {location}")
    if isinstance(value, str):
        require(len(value) >= int(schema.get("minLength", 0)), f"schema minLength mismatch at {location}")
        if schema.get("pattern") is not None:
            require(re.search(str(schema["pattern"]), value) is not None, f"schema pattern mismatch at {location}")
        if schema.get("format") == "date":
            require(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is not None, f"schema date mismatch at {location}")
        if schema.get("format") == "date-time":
            require(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})", value) is not None, f"schema date-time mismatch at {location}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema:
            require(value >= schema["minimum"], f"schema minimum mismatch at {location}")
        if "maximum" in schema:
            require(value <= schema["maximum"], f"schema maximum mismatch at {location}")


def check_parent_release() -> None:
    require(sha256_file(PARENT_DIR / MANIFEST_NAME) == PARENT_MANIFEST_SHA256, "5.3 manifest bytes drifted")
    manifest = load_json(PARENT_DIR / MANIFEST_NAME)
    verify_seal(manifest, "5.3 manifest")
    require(manifest.get("release_root_sha256") == PARENT_ROOT, "5.3 parent root drifted")
    inventory = manifest.get("artifacts")
    require(isinstance(inventory, list), "5.3 manifest inventory malformed")
    require({row.get("path") for row in inventory} == set(RELEASE_FILES), "5.3 artifact set drifted")
    for binding in inventory:
        name = binding["path"]
        path = PARENT_DIR / name
        document = load_json(path)
        verify_seal(document, f"5.3 {name}")
        require(binding.get("sha256") == sha256_file(path), f"5.3 {name} hash binding drifted")
        require(binding.get("size_bytes") == path.stat().st_size, f"5.3 {name} size binding drifted")
        require(binding.get("row_count") == primary_row_count(document), f"5.3 {name} row_count semantics drifted")
    require(release_root(inventory) == PARENT_ROOT, "5.3 release root does not recompute")


def check_release_package() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    observed = {path.name for path in RELEASE_DIR.iterdir() if path.is_file()}
    require(observed == ALL_RELEASE_FILES, f"5.4 release file set drifted: {sorted(observed)}")
    documents: dict[str, dict[str, Any]] = {}
    for name in ALL_RELEASE_FILES:
        document = load_json(RELEASE_DIR / name, canonical=True)
        verify_seal(document, f"5.4 {name}")
        documents[name] = document
    manifest = documents[MANIFEST_NAME]
    validate_release_inventory(manifest, documents, RELEASE_DIR)
    return manifest, documents


def validate_release_inventory(
    manifest: Mapping[str, Any],
    documents: Mapping[str, Mapping[str, Any]],
    release_dir: Path,
) -> str:
    inventory = manifest.get("artifacts")
    require(isinstance(inventory, list), "5.4 manifest inventory malformed")
    expected_inventory = []
    for name in sorted(RELEASE_FILES):
        path = release_dir / name
        expected_inventory.append(
            {
                "path": name,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
                "row_count": primary_row_count(documents[name]),
            }
        )
    require(inventory == expected_inventory, "5.4 manifest artifact inventory drifted")
    root = release_root(expected_inventory)
    require(manifest.get("release_root_sha256") == root, "5.4 release root does not recompute")
    require(manifest.get("parent_release_root_sha256") == PARENT_ROOT, "5.4 manifest parent root drifted")
    require(
        next(row for row in inventory if row["path"] == "Coverage_Ledger.json")["row_count"] == 5_961,
        "coverage row_count must include 5,898 dispositions plus 63 MSC rows",
    )
    require(
        next(row for row in inventory if row["path"] == "Strict_Conjecture_Ledger.json")["row_count"] == 1_001,
        "strict row_count must include 1,000 credits plus one correction",
    )
    return root


def validate_source_registry(source_registry: Mapping[str, Any]) -> None:
    require(source_registry.get("schema_version") == "awesome-theorems/stage5-math-source-registry/5.4", "5.4 source registry schema drifted")
    sources = source_registry.get("sources")
    require(isinstance(sources, list) and len(sources) == 1 and sources[0].get("source_id") == SOURCE_ID, "5.4 source registry source binding malformed")
    asset = sources[0].get("asset", {})
    require(
        asset.get("path") == relative(SOURCE_PATH)
        and asset.get("sha256") == SOURCE_SHA256
        and asset.get("size_bytes") == SOURCE_SIZE_BYTES
        and asset.get("record_count") == 1_500
        and asset.get("content_digest_before_self_field") == SOURCE_CONTENT_DIGEST,
        "5.4 source registry asset binding drifted",
    )
    parent_path = V5_ROOT / "Math_Source_Registry_v5_3.json"
    parent = load_json(parent_path)
    verify_seal(parent, "5.3 source registry")
    require(sources == parent.get("sources"), "5.4 source rows are not exact 5.3 byte-semantic rows")
    require(
        source_registry.get("source_record_contract") == parent.get("source_record_contract"),
        "5.4 source-record contract differs from its inherited 5.3 row contract",
    )
    parent_binding = source_registry.get("parent_registry", {})
    require(
        parent_binding.get("path") == relative(parent_path)
        and parent_binding.get("file_sha256") == sha256_file(parent_path)
        and parent_binding.get("authority_sha256") == parent.get("authority_sha256")
        and parent_binding.get("source_rows_rewritten") is False,
        "5.4 source registry parent/source-row binding drifted",
    )
    extensions = source_registry.get("source_policy_extensions")
    require(isinstance(extensions, list) and len(extensions) == 1, "5.4 source policy extension cardinality drifted")
    extension = extensions[0]
    require(
        extension.get("extension_id") == "SRC-POLICY-MATHLIB-RESIDUAL-5.4"
        and extension.get("source_id") == SOURCE_ID
        and extension.get("applies_to_release") == "5.4"
        and extension.get("parent_source_registry_path") == relative(parent_path)
        and extension.get("parent_source_row_sha256") == sha256_bytes(canonical_json_bytes(parent["sources"][0]))
        and extension.get("source_row_reused_without_rewrite") is True
        and extension.get("inherits_parent_proof_rights_locator_and_dedupe_policy") is True,
        "5.4 source policy extension binding drifted",
    )
    require(extension.get("asset_identity_reused") == {
        "path": relative(SOURCE_PATH), "sha256": SOURCE_SHA256,
        "size_bytes": SOURCE_SIZE_BYTES, "record_count": 1_500,
        "mathlib_commit": MATHLIB_COMMIT,
    }, "5.4 source policy extension asset identity drifted")
    residual = extension.get("residual_selection", {})
    require(
        residual.get("residual_unique_literal_theorems") == 731
        and residual.get("accepted_in_5_4") == 500
        and residual.get("remaining_after_5_4") == 231
        and residual.get("literal_lemma_grants_quota") is False,
        "5.4 source policy extension residual facts drifted",
    )
    require(source_registry.get("counts") == {
        "inherited_source_rows": 1,
        "new_source_rows": 0,
        "source_policy_extensions": 1,
        "asset_rows": 1_500,
        "parent_literal_lemma_noncredit_rows": 265,
        "residual_literal_theorem_rows": 731,
        "exact_release_acceptance_rows": 500,
    }, "5.4 source registry counts drifted")
    require(source_registry.get("source_readiness") == {
        "mathlib_ready_for_residual_literal_theorem_only_5_4_intake": True,
        "release_completion_not_asserted_by_registry": True,
        "literal_lemma_grants_quota": False,
        "source_row_semantics_remain_the_5_3_authority": True,
    }, "5.4 source registry readiness boundary drifted")


def source_indexes() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    require(sha256_file(SOURCE_PATH) == SOURCE_SHA256, "fixed mathlib asset hash drifted")
    require(SOURCE_PATH.stat().st_size == SOURCE_SIZE_BYTES, "fixed mathlib asset size drifted")
    source = load_json(SOURCE_PATH)
    require(source.get("content_digest_before_self_field") == SOURCE_CONTENT_DIGEST, "source content digest field drifted")
    rows = source.get("records")
    require(isinstance(rows, list) and len(rows) == 1_500, "mathlib asset must have 1,500 rows")
    by_id: dict[str, dict[str, Any]] = {}
    theorem_count = 0
    lemma_count = 0
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"source row {index} is not an object")
        source_id = row.get("source_record_id")
        require(isinstance(source_id, str) and source_id not in by_id, f"source row {index} ID invalid/duplicate")
        require(row.get("selection_rank") == index + 1, "source selection ranks are not 1..1500")
        require(row.get("formal_type_sha256") == sha256_bytes(str(row.get("formal_type")).encode("utf-8")), f"source {source_id} formal hash drifted")
        require(row.get("formal_docstring_sha256") == sha256_bytes(str(row.get("formal_docstring")).encode("utf-8")), f"source {source_id} docstring hash drifted")
        require(row.get("declaration_kind") == row.get("source_syntax_kind") == row.get("raw_category"), f"source {source_id} literal kind fields disagree")
        if row["declaration_kind"] == "theorem":
            theorem_count += 1
        elif row["declaration_kind"] == "lemma":
            lemma_count += 1
        else:
            raise CheckError(f"source {source_id} unsupported literal declaration kind")
        proof = row.get("proof_evidence")
        require(isinstance(proof, dict), f"source {source_id} lacks proof evidence")
        require(
            row.get("formal_proof_state") == "kernel_checked_sorry_free"
            and proof.get("uses_sorry") is False
            and proof.get("verification") == "lean_checked_environment_thmInfo_and_collectAxioms_without_sorryAx"
            and proof.get("compiled_module") == row.get("source", {}).get("module"),
            f"source {source_id} fails proof gate",
        )
        by_id[source_id] = row
    require((theorem_count, lemma_count) == (1_235, 265), "source theorem/lemma partition drifted")
    return rows, by_id


def parent_identity_sets(records: Sequence[Mapping[str, Any]]) -> tuple[set[str], set[str], set[str]]:
    exact: set[str] = set()
    normalized_types: set[str] = set()
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
            normalized_types.add(normalized_formal_type_sha256(text))
        if isinstance(name, str):
            names.add(normalized_declaration_sha256(name))
    return exact, normalized_types, names


def enforce_three_identity_gates(
    residual: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
    parent_records: Sequence[Mapping[str, Any]],
) -> None:
    exact_parent, type_parent, name_parent = parent_identity_sets(parent_records)
    exact_values: list[str] = []
    type_values: list[str] = []
    name_values: list[str] = []
    for _ledger_row, source in residual:
        exact = str(source["formal_type_sha256"])
        normalized_type = normalized_formal_type_sha256(str(source["formal_type"]))
        name = normalized_declaration_sha256(str(source["declaration"]))
        source_id = source.get("source_record_id")
        require(exact not in exact_parent, f"residual {source_id} exact-duplicates parent catalog")
        require(normalized_type not in type_parent, f"residual {source_id} normalized-type-duplicates parent catalog")
        require(name not in name_parent, f"residual {source_id} name-duplicates parent catalog")
        exact_values.append(exact)
        type_values.append(normalized_type)
        name_values.append(name)
    require(len(set(exact_values)) == len(exact_values), "residual exact formal types are not unique")
    require(len(set(type_values)) == len(type_values), "residual normalized formal types are not unique")
    require(len(set(name_values)) == len(name_values), "residual normalized declaration names are not unique")


def validate_literal_theorem_credits(rows: Sequence[Mapping[str, Any]]) -> None:
    for row in rows:
        require(
            row.get("grants_catalog_entry") is True
            and row.get("grants_theorem_credit") is True
            and row.get("declaration_kind") == "theorem"
            and row.get("source_syntax_kind") == "theorem",
            "a nonliteral theorem/lemma received release quota",
        )


def replay_residual_selection(
    parent_catalog: Mapping[str, Any], source_by_id: Mapping[str, dict[str, Any]]
) -> tuple[list[tuple[dict[str, Any], dict[str, Any]]], list[tuple[dict[str, Any], dict[str, Any]]]]:
    require(sha256_file(PARENT_CURATION_PATH) == PARENT_CURATION_SHA256, "5.3 curation bytes drifted")
    parent_curation = load_json(PARENT_CURATION_PATH)
    verify_seal(parent_curation, "5.3 curation")
    require(parent_curation.get("authority_sha256") == PARENT_CURATION_AUTHORITY, "5.3 curation authority drifted")
    rows = parent_curation.get("candidate_dispositions")
    require(isinstance(rows, list) and len(rows) == 1_500, "5.3 curation denominator drifted")
    residual: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for index, ledger_row in enumerate(rows):
        require(isinstance(ledger_row, dict), f"5.3 curation row {index} is not an object")
        require(ledger_row.get("row_sha256") == hash_without(ledger_row, "row_sha256"), f"5.3 curation row {index} hash stale")
        if ledger_row.get("disposition") != "eligible_not_selected":
            continue
        source_id = ledger_row.get("source_record_id")
        source = source_by_id.get(source_id)
        require(source is not None, f"residual source {source_id!r} missing")
        require(source.get("declaration_kind") == source.get("source_syntax_kind") == "theorem", f"residual {source_id} is not a literal theorem")
        require(ledger_row.get("source_index") == int(source["selection_rank"]) - 1, f"residual {source_id} source index drifted")
        require(ledger_row.get("source_record_sha256") == sha256_bytes(canonical_json_bytes(source)), f"residual {source_id} source hash drifted")
        residual.append((ledger_row, source))
    require(len(residual) == 731, "5.3 exact residual pool is not 731 rows")

    enforce_three_identity_gates(residual, parent_catalog["records"])

    ordered: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    for pair in residual:
        ordered[module_root(pair[1])].append(pair)
    buckets: dict[str, deque[tuple[dict[str, Any], dict[str, Any]]]] = {}
    for root, pairs in ordered.items():
        pairs.sort(key=lambda pair: (int(pair[1]["selection_rank"]), str(pair[1]["source_record_id"])))
        buckets[root] = deque(pairs)
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    roots = sorted(buckets, key=lambda value: value.encode("utf-8"))
    while len(selected) < 500:
        advanced = False
        for root in roots:
            if buckets[root]:
                selected.append(buckets[root].popleft())
                advanced = True
                if len(selected) == 500:
                    break
        require(advanced, "round-robin pool exhausted before 500")
    remaining = [pair for root in roots for pair in buckets[root]]
    require(Counter(module_root(source) for _row, source in selected) == Counter(EXPECTED_ROOT_COUNTS), "selected root distribution drifted")
    require(Counter(module_root(source) for _row, source in remaining) == Counter(EXPECTED_REMAINING_ROOT_COUNTS), "remaining root distribution drifted")
    return selected, remaining


def expected_curation_rows(
    residual: Sequence[tuple[dict[str, Any], dict[str, Any]]],
    selected: Sequence[tuple[dict[str, Any], dict[str, Any]]],
) -> list[dict[str, Any]]:
    selected_rank = {
        str(source["source_record_id"]): rank
        for rank, (_parent, source) in enumerate(selected, start=1)
    }
    rows: list[dict[str, Any]] = []
    for parent_row, source in sorted(
        residual,
        key=lambda pair: (int(pair[1]["selection_rank"]), str(pair[1]["source_record_id"])),
    ):
        source_id = str(source["source_record_id"])
        rank = selected_rank.get(source_id)
        accepted = rank is not None
        ordinal = PARENT_ATV_HIGH + rank if rank is not None else None
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
            "semantic_key": "mathlib-theorem-semantic/" + str(source["formal_type_sha256"]),
            "disposition": "accepted_new_kernel_checked_theorem" if accepted else "eligible_not_selected_after_5_4",
            "reason_code": "selected_remaining_module_root_round_robin" if accepted else "viable_theorem_outside_exact_5_4_selection",
            "accepted_rank": rank,
            "target_variant_id": f"ATV-{ordinal:08d}" if ordinal is not None else None,
            "target_s5_id": f"S5-CLM-{ordinal:08d}" if ordinal is not None else None,
            "grants_catalog_entry": accepted,
            "grants_theorem_credit": accepted,
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        rows.append(row)
    return rows


def check_curation(
    parent_catalog: Mapping[str, Any], source_by_id: Mapping[str, dict[str, Any]]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    selected, remaining = replay_residual_selection(parent_catalog, source_by_id)
    residual = [*selected, *remaining]
    expected_rows = expected_curation_rows(residual, selected)
    curation = load_json(CURATION_PATH, canonical=True)
    verify_seal(curation, "5.4 curation")
    require(curation.get("schema_version") == "awesome-theorems/mathlib-theorem-curation/5.4", "5.4 curation schema drifted")
    require(curation.get("candidate_dispositions") == expected_rows, "5.4 curation is not the independently replayed 731-row ledger")
    accepted = sorted((row for row in expected_rows if row["grants_theorem_credit"]), key=lambda row: int(row["accepted_rank"]))
    require(len(accepted) == 500 and len(remaining) == 231, "5.4 curation counts drifted")
    validate_literal_theorem_credits(accepted)
    expected_digests = {
        "residual_source_record_id_set_sha256": set_digest(row["source_record_id"] for row in expected_rows),
        "residual_exact_formal_type_set_sha256": set_digest(row["formal_type_sha256"] for row in expected_rows),
        "residual_normalized_formal_type_set_sha256": set_digest(row["normalized_formal_type_sha256"] for row in expected_rows),
        "residual_normalized_declaration_set_sha256": set_digest(row["normalized_declaration_name_sha256"] for row in expected_rows),
        "selected_source_record_id_set_sha256": set_digest(row["source_record_id"] for row in accepted),
        "selected_declaration_set_sha256": set_digest(row["declaration"] for row in accepted),
        "selected_formal_type_sha256_set_sha256": set_digest(row["formal_type_sha256"] for row in accepted),
        "selected_semantic_key_set_sha256": set_digest(row["semantic_key"] for row in accepted),
        "selected_variant_id_set_sha256": set_digest(row["target_variant_id"] for row in accepted),
        "selected_s5_id_set_sha256": set_digest(row["target_s5_id"] for row in accepted),
        "candidate_row_sha256_set_sha256": set_digest(row["row_sha256"] for row in expected_rows),
    }
    require(curation.get("set_digests") == expected_digests, "5.4 curation set digests drifted")
    counts = curation.get("counts", {})
    require(
        counts.get("residual_unique_literal_theorem_rows") == 731
        and counts.get("accepted") == 500
        and counts.get("eligible_not_selected_after_5_4") == 231
        and counts.get("selected_by_module_root") == EXPECTED_ROOT_COUNTS
        and counts.get("remaining_by_module_root") == EXPECTED_REMAINING_ROOT_COUNTS,
        "5.4 curation declared counts drifted",
    )
    return curation, accepted


def seal_field(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result[field] = sha256_bytes(canonical_json_bytes(result))
    return result


def expected_claim_row(
    ledger_row: Mapping[str, Any],
    source: Mapping[str, Any],
    parent_registry_authority: str,
    curation: Mapping[str, Any],
) -> dict[str, Any]:
    rank = int(ledger_row["accepted_rank"])
    atv_ordinal = PARENT_ATV_HIGH + rank
    atf_ordinal = PARENT_ATF_HIGH + rank
    source_id = str(source["source_record_id"])
    source_hash = sha256_bytes(canonical_json_bytes(source))
    source_data = source["source"]
    formal_type = str(source["formal_type"])
    semantic_key = "mathlib-theorem-semantic/" + str(source["formal_type_sha256"])
    root = module_root(source)
    source_locator = {
        "source_id": SOURCE_ID,
        "artifact_path": relative(SOURCE_PATH),
        "artifact_sha256": SOURCE_SHA256,
        "artifact_size_bytes": SOURCE_SIZE_BYTES,
        "record_index": ledger_row["source_index"],
        "source_record_id": source_id,
        "source_record_sha256": source_hash,
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
        "formal_type_sha256": source["formal_type_sha256"],
        "formal_docstring": source["formal_docstring"],
        "formal_docstring_origin": source["formal_docstring_origin"],
        "formal_docstring_sha256": source["formal_docstring_sha256"],
    }
    mathematical_statement = seal_field(
        {
            "completeness": "exact_formal",
            "language": "Lean4",
            "natural_language": source["exact_curated_summary"],
            "formal_type": formal_type,
            "formal_type_sha256": source["formal_type_sha256"],
        },
        "statement_sha256",
    )
    theorem_selection = {
        "source_record_id": source_id,
        "selection_cohort": source["selection_cohort"],
        "selection_rank": source["selection_rank"],
        "display_label": source["display_label"],
        "exact_curated_summary": source["exact_curated_summary"],
        "importance_signals": copy.deepcopy(source["importance_signals"]),
        "selection_phase": "selected_remaining_module_root_round_robin",
        "phase_rank": rank,
        "module_root": root,
    }
    curator_disposition = {
        "curation_ledger_path": relative(CURATION_PATH),
        "curation_ledger_file_sha256": sha256_file(CURATION_PATH),
        "curation_ledger_authority_sha256": curation["authority_sha256"],
        "source_index": ledger_row["source_index"],
        "source_record_id": source_id,
        "curation_row_sha256": ledger_row["row_sha256"],
        "disposition": ledger_row["disposition"],
        "reason_code": ledger_row["reason_code"],
        "accepted_rank": rank,
        "target_variant_id": ledger_row["target_variant_id"],
        "target_s5_id": ledger_row["target_s5_id"],
        "grants_catalog_entry": ledger_row["grants_catalog_entry"],
        "grants_theorem_credit": ledger_row["grants_theorem_credit"],
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
        "status": "source_curated_exact" if source["msc2020"]["basis"] == "1000_plus_curated" else "machine_root_crosswalk",
        "module_root": root,
    }
    provenance = {
        "formal_source_ref": SOURCE_ID,
        "source_refs": [SOURCE_ID],
        "extraction_mode": "pinned_mathlib_runtime_extraction",
        "extractor_path": "Docs/tools/extract_mathlib_theorems_v5.py",
        "extractor_version": "1.1.0",
        "extractor_file_sha256": "0e26af2b6740abf4626f3cf43d84fb8f7e1f1a6104096e71f1f9b1f2c33189af",
        "source_asset_sha256": SOURCE_SHA256,
        "source_record_id": source_id,
        "source_record_sha256": source_hash,
        "mathlib_commit": MATHLIB_COMMIT,
        "exact_source_replay_required": True,
    }
    has_docs_signal = any(
        isinstance(signal, dict) and signal.get("kind") == "mathlib_1000_theorems"
        for signal in source["importance_signals"]
    )
    rights = seal_field(
        {
            "formal_code_terms": "Apache-2.0",
            "docstring_terms": "Apache-2.0",
            "optional_metadata_terms": "Unlicense" if has_docs_signal else "not_applicable",
            "status": "cleared_with_attribution",
            "redistribution_mode": "apache_2_0_with_attribution",
            "attribution": ["The mathlib Community"],
            "source_refs": [SOURCE_ID],
            "mathlib_license_sha256": "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1",
            "catalog_relicenses_source": False,
        },
        "rights_payload_sha256",
    )
    source_proof = source["proof_evidence"]
    proof_evidence = seal_field(
        {
            "formal_proof_state": source["formal_proof_state"],
            "verification": source_proof["verification"],
            "uses_sorry": source_proof["uses_sorry"],
            "compiled_module": source_proof["compiled_module"],
            "ilean_path": source_proof["ilean_path"],
            "ilean_sha256": source_proof["ilean_sha256"],
            "olean_path": source_proof["olean_path"],
            "olean_sha256": source_proof["olean_sha256"],
            "batch_axiom_dependency_union": copy.deepcopy(source_proof["batch_axiom_dependency_union"]),
            "axiom_evidence_scope": "batch_union_not_per_declaration_exact_dependencies",
            "mathlib_commit": MATHLIB_COMMIT,
        },
        "proof_payload_sha256",
    )
    importance = {
        "tier": "source_signaled_mathlib_theorem",
        "basis": "mathlib_1000_formalized_signal" if has_docs_signal else "mathlib_module_main_result_signal",
        "rationale": "Selected from the pinned formalized mathlib 1000-theorems signal." if has_docs_signal else "Selected from a pinned mathlib module Main-result signal.",
        "evidence_level": "source_documentation_signal",
        "independent_universal_ranking_claimed": False,
    }
    dedupe = {
        "normalized_declaration_key": normalized_declaration(str(source["declaration"])),
        "formal_type_sha256": source["formal_type_sha256"],
        "source_record_sha256": source_hash,
        "semantic_key": semantic_key,
        "candidate_atv_ids": [],
        "parent_catalog_file_sha256": PARENT_CATALOG_SHA256,
        "verdict": "unique_after_source_and_parent_curation",
        "validation_status": "machine_replayed_and_manifest_bound_curation",
        "duplicate_grants_quota": False,
        "no_evidence_or_status_inheritance": True,
    }
    allocation_request = {
        "origin_release": "5.4",
        "source_id": SOURCE_ID,
        "source_record_id": source_id,
        "source_record_sha256": source_hash,
        "semantic_key": semantic_key,
        "statement_sha256": mathematical_statement["statement_sha256"],
        "family_action": "new_family",
    }
    allocation = {
        "parent_registry_authority_sha256": parent_registry_authority,
        "parent_release_root_sha256": PARENT_ROOT,
        "allocation_request_sha256": sha256_bytes(canonical_json_bytes(allocation_request)),
        "transaction_id": f"S5-ALLOC-{atv_ordinal:08d}",
        "family_action": "new_family",
        "append_only": True,
    }
    aliases = list(
        dict.fromkeys(
            value
            for value in (str(source["declaration"]), str(source["exact_curated_summary"]))
            if value != str(source["display_label"])
        )
    )
    row: dict[str, Any] = {
        "schema_version": "awesome-theorems/stage5-math-claim-record/5.4",
        "release_id": "5.4",
        "origin_stage": "Stage5",
        "origin_release": "5.4",
        "curation_key": f"mathlib/{source_id}",
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
    row["content_payload_sha256"] = sha256_bytes(canonical_json_bytes({"formal_statement": formal_statement, "mathematical_statement": mathematical_statement}))
    row["source_payload_sha256"] = sha256_bytes(canonical_json_bytes({"source_locator": source_locator, "theorem_selection": theorem_selection, "provenance": provenance}))
    row["proof_payload_sha256"] = proof_evidence["proof_payload_sha256"]
    row["semantic_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "record_role": "claim",
                "atomicity": "atomic",
                "truth_apt": True,
                "category": "theorem",
                "current_claim_kind": "theorem",
                "semantic_key": semantic_key,
                "statement_sha256": mathematical_statement["statement_sha256"],
            }
        )
    )
    return row


def validate_record_payload_hashes(row: Mapping[str, Any]) -> None:
    statement = row.get("mathematical_statement")
    rights = row.get("rights")
    proof = row.get("proof_evidence")
    require(isinstance(statement, dict) and isinstance(rights, dict) and isinstance(proof, dict), "claim payload objects malformed")
    require(statement.get("statement_sha256") == hash_without(statement, "statement_sha256"), "statement payload hash is stale")
    require(rights.get("rights_payload_sha256") == hash_without(rights, "rights_payload_sha256"), "rights payload hash is stale")
    require(proof.get("proof_payload_sha256") == hash_without(proof, "proof_payload_sha256"), "proof evidence payload hash is stale")
    require(row.get("content_payload_sha256") == sha256_bytes(canonical_json_bytes({
        "formal_statement": row.get("formal_statement"), "mathematical_statement": statement,
    })), "content payload hash is stale")
    require(row.get("source_payload_sha256") == sha256_bytes(canonical_json_bytes({
        "source_locator": row.get("source_locator"), "theorem_selection": row.get("theorem_selection"), "provenance": row.get("provenance"),
    })), "source payload hash is stale")
    require(row.get("proof_payload_sha256") == proof.get("proof_payload_sha256"), "top-level proof payload hash is stale")
    require(row.get("semantic_payload_sha256") == sha256_bytes(canonical_json_bytes({
        "record_role": row.get("record_role"), "atomicity": row.get("atomicity"),
        "truth_apt": row.get("truth_apt"), "category": row.get("category"),
        "current_claim_kind": row.get("current_claim_kind"), "semantic_key": row.get("semantic_key"),
        "statement_sha256": statement.get("statement_sha256"),
    })), "semantic payload hash is stale")


def check_authorities(manifest: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    paths = {
        "record_schema": SCHEMA_PATH,
        "source_registry": SOURCE_REGISTRY_PATH,
        "parent_receipt": PARENT_RECEIPT_PATH,
        "curation_ledger": CURATION_PATH,
    }
    documents: dict[str, dict[str, Any]] = {}
    for key, path in paths.items():
        document = load_json(path, canonical=True)
        verify_seal(document, str(path))
        documents[key] = document
    contract = load_json(CONTRACT_PATH, canonical=True)
    verify_seal(contract, str(CONTRACT_PATH))
    require(contract.get("release") == "5.4", "5.4 contract release drifted")
    bindings = contract.get("versioned_authorities")
    require(isinstance(bindings, dict), "5.4 contract authority bindings malformed")
    for key, path in paths.items():
        require(bindings.get(key) == artifact_binding(path, documents[key]), f"contract binding {key} differs from actual authority bytes")
    schema = documents["record_schema"]
    require(schema.get("$id") == "urn:awesome-theorems:schema:stage5-math-claim-record:5.4", "5.4 schema ID drifted")
    require(isinstance(schema.get("$defs"), dict) and len(schema["$defs"]) >= 25, "5.4 deep schema definitions missing")
    for name in (
        "allocation", "source_locator", "formal_statement", "theorem_selection",
        "curator_disposition", "mathematical_statement", "status_detail",
        "classification", "provenance", "rights", "dedupe", "proof_evidence", "importance",
    ):
        definition = schema["$defs"].get(name)
        require(isinstance(definition, dict) and definition.get("additionalProperties") is False, f"5.4 schema nested {name} is not closed")
    source_registry = documents["source_registry"]
    validate_source_registry(source_registry)
    receipt = documents["parent_receipt"]
    parent_binding = receipt.get("parent_release", {})
    require(
        parent_binding.get("release") == "5.3"
        and parent_binding.get("release_root_sha256") == PARENT_ROOT
        and parent_binding.get("manifest_file_sha256") == PARENT_MANIFEST_SHA256,
        "5.4 parent receipt boundary drifted",
    )
    inventory = receipt.get("artifact_inventory")
    require(isinstance(inventory, list) and {row.get("path") for row in inventory} == ALL_RELEASE_FILES, "parent receipt artifact set drifted")
    for binding in inventory:
        path = PARENT_DIR / binding["path"]
        document = load_json(path)
        require(
            binding.get("file_sha256") == sha256_file(path)
            and binding.get("size_bytes") == path.stat().st_size
            and binding.get("row_count") == primary_row_count(document)
            and binding.get("authority_sha256") == document.get("authority_sha256"),
            f"parent receipt binding drifted for {path.name}",
        )
    expected_inputs = {
        "contract": artifact_binding(CONTRACT_PATH, contract),
        "record_schema": artifact_binding(SCHEMA_PATH, schema),
        "source_registry": artifact_binding(SOURCE_REGISTRY_PATH, source_registry),
        "parent_receipt": artifact_binding(PARENT_RECEIPT_PATH, receipt),
        "curation_ledger": artifact_binding(CURATION_PATH, documents["curation_ledger"]),
        "mathlib_asset": {
            "path": relative(SOURCE_PATH),
            "file_sha256": SOURCE_SHA256,
            "size_bytes": SOURCE_SIZE_BYTES,
            "content_digest_before_self_field": SOURCE_CONTENT_DIGEST,
            "mathlib_commit": MATHLIB_COMMIT,
        },
        "parent_release": {
            "release": "5.3",
            "release_root_sha256": PARENT_ROOT,
            "manifest_file_sha256": PARENT_MANIFEST_SHA256,
            "manifest_authority_sha256": load_json(PARENT_DIR / MANIFEST_NAME)["authority_sha256"],
            "registry_authority_sha256": load_json(PARENT_DIR / "Claim_ID_Registry.json")["authority_sha256"],
        },
    }
    require(manifest.get("authoritative_inputs") == expected_inputs, "manifest authoritative inputs drifted")
    return schema, expected_inputs


def theorem_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "theorem"
        and row.get("current_claim_kind") == "theorem"
        and row.get("material_status") == "proved"
        and (
            row.get("origin_release") != "5.4"
            or (
                row.get("formal_statement", {}).get("declaration_kind") == "theorem"
                and row.get("formal_statement", {}).get("source_syntax_kind") == "theorem"
                and row.get("proof_evidence", {}).get("formal_proof_state") == "kernel_checked_sorry_free"
                and row.get("proof_evidence", {}).get("uses_sorry") is False
            )
        )
    )


def open_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("current_claim_kind") in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status") in {"open", "partial", "independent", "disputed"}
    )


def validate_parent_prefix(
    child: Sequence[Mapping[str, Any]],
    parent: Sequence[Mapping[str, Any]],
    label: str,
) -> None:
    require(len(child) >= len(parent) and list(child[: len(parent)]) == list(parent), f"{label} parent canonical prefix changed")


def expected_registry_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        families.append({
            "family_id": row["family_id"], "curation_key": row["curation_key"],
            "display_titles": list(dict.fromkeys([row["display_name"], *row["aliases"]])),
            "member_occurrence_ids": [row["occurrence_id"]], "historical_member_occurrence_ids": [row["occurrence_id"]],
            "idempotency_request_sha256": request, "identity_state": "stage5_mathlib_exact_formal_type_family",
            "lifecycle": "current", "semantic_equivalence_asserted": True,
        })
        senses.append({
            "sense_id": row["sense_id"], "family_id": row["family_id"], "bootstrap_occurrence_id": row["occurrence_id"],
            "curation_key": row["curation_key"], "idempotency_request_sha256": request,
            "identity_state": "stage5_mathlib_exact_formal_type_sense", "lifecycle": "current",
        })
        variants.append({
            "variant_id": row["variant_id"], "sense_id": row["sense_id"], "bootstrap_occurrence_id": row["occurrence_id"],
            "curation_key": row["curation_key"], "idempotency_request_sha256": request,
            "semantic_payload_sha256": row["semantic_payload_sha256"],
            "identity_state": "stage5_mathlib_exact_formal_type_variant", "lifecycle": "current",
        })
    return families, senses, variants


def check_artifacts(
    documents: Mapping[str, Mapping[str, Any]],
    schema: Mapping[str, Any],
    inputs: Mapping[str, Any],
    curation: Mapping[str, Any],
    accepted: Sequence[Mapping[str, Any]],
    source_by_id: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    parent = {name: load_json(PARENT_DIR / name) for name in ALL_RELEASE_FILES}
    for name in RELEASE_FILES:
        child = documents[name]
        if name != "Strict_Conjecture_Ledger.json":
            require(child.get("authoritative_inputs") == inputs, f"{name} authoritative inputs drifted")
    expected_new = [
        expected_claim_row(row, source_by_id[row["source_record_id"]], parent["Claim_ID_Registry.json"]["authority_sha256"], curation)
        for row in accepted
    ]
    for index, row in enumerate(expected_new, start=1):
        validate_closed_schema(row, schema, f"new claim {index}")
        validate_schema_instance(row, schema, schema, f"new claim {index}")
        validate_record_payload_hashes(row)
    catalog = documents["Claim_Catalog.json"]
    validate_parent_prefix(catalog["records"], parent["Claim_Catalog.json"]["records"], "catalog records")
    require(catalog["records"][3_600:] == expected_new, "catalog suffix differs from independently reconstructed 500 claims")
    records = catalog["records"]
    require(len(records) == 4_100, "catalog count is not 4,100")
    require(len({row["variant_id"] for row in records}) == 4_100, "catalog variant IDs are not unique")
    require(len({row["stage_claim_id"] for row in records}) == 4_100, "catalog Stage5 IDs are not unique")
    require(catalog.get("counts") == {
        "records": 4_100, "origin_theorems": 500, "origin_open_claims": 0,
        "cumulative_theorems": 2_500, "cumulative_open_claims": 1_600,
    }, "catalog declared counts drifted")
    require(sum(theorem_predicate(row) for row in records) == 2_500, "theorem count does not recompute")
    require(sum(open_predicate(row) for row in records) == 1_600, "open count does not recompute")
    require([row["occurrence_id"] for row in expected_new] == [f"ATO-{n:08d}" for n in range(7_085, 7_585)], "ATO range drifted")
    require([row["sense_id"] for row in expected_new] == [f"ATS-{n:08d}" for n in range(7_085, 7_585)], "ATS range drifted")
    require([row["variant_id"] for row in expected_new] == [f"ATV-{n:08d}" for n in range(7_085, 7_585)], "ATV range drifted")
    require([row["stage_claim_id"] for row in expected_new] == [f"S5-CLM-{n:08d}" for n in range(7_085, 7_585)], "S5 range drifted")
    require([row["family_id"] for row in expected_new] == [f"ATF-{n:08d}" for n in range(6_855, 7_355)], "ATF range drifted")

    theorem_rows = [row for row in records if theorem_predicate(row)]
    open_rows = [row for row in records if open_predicate(row)]
    theorem = documents["Theorem_List.json"]
    open_list = documents["Open_Claim_List.json"]
    require(theorem["records"] == theorem_rows and theorem["stage_claim_ids"] == [row["stage_claim_id"] for row in theorem_rows] and theorem["counts"] == {"records": 2_500}, "theorem projection drifted")
    require(open_list["records"] == open_rows and open_list["stage_claim_ids"] == [row["stage_claim_id"] for row in open_rows] and open_list["counts"] == {"records": 1_600}, "open projection drifted")
    validate_parent_prefix(theorem["records"], parent["Theorem_List.json"]["records"], "theorem projection")
    require(open_list["records"] == parent["Open_Claim_List.json"]["records"], "open projection changed from parent")

    registry = documents["Claim_ID_Registry.json"]
    families, senses, variants = expected_registry_rows(expected_new)
    for key, expected_suffix in (("families", families), ("senses", senses), ("variants", variants)):
        parent_rows = parent["Claim_ID_Registry.json"][key]
        validate_parent_prefix(registry[key], parent_rows, f"registry {key}")
        require(registry[key][len(parent_rows):] == expected_suffix, f"registry {key} suffix drifted")
    require(registry["namespace_high_watermarks"] == {"ATF": LAST_ATF, "ATO": LAST_ATV, "ATS": LAST_ATV, "ATV": LAST_ATV}, "registry watermarks drifted")
    for key in ("legacy_aliases", "redirects", "splits", "family_membership_extensions"):
        require(registry[key] == parent["Claim_ID_Registry.json"][key], f"registry {key} changed")

    stage = documents["Stage5_Claim_ID_Registry.json"]
    parent_mappings = parent["Stage5_Claim_ID_Registry.json"]["mappings"]
    expected_mappings = [{
        "ordinal": n, "variant_id": row["variant_id"], "predecessor_stage_claim_id": None,
        "stage_claim_id": row["stage_claim_id"], "lifecycle": "current",
    } for n, row in zip(range(7_085, 7_585), expected_new)]
    validate_parent_prefix(stage["mappings"], parent_mappings, "Stage5 mappings")
    require(stage["mappings"][len(parent_mappings):] == expected_mappings, "Stage5 mapping append drifted")
    migration = documents["Migration_v4_to_v5.json"]
    parent_migrations = parent["Migration_v4_to_v5.json"]["migrations"]
    expected_migrations = [{
        "ordinal": n, "variant_id": row["variant_id"], "v4_variant_id": None, "s4_claim_id": None,
        "stage_claim_id": row["stage_claim_id"], "migration_action": "new_stage5_allocation", "predecessor_record_sha256": None,
        "current_resolution": {"kind": "current", "terminal_atv_ids": [row["variant_id"]], "terminal_s5_ids": [row["stage_claim_id"]], "default_child": None, "evidence_inherited": False},
    } for n, row in zip(range(7_085, 7_585), expected_new)]
    validate_parent_prefix(migration["migrations"], parent_migrations, "migrations")
    require(migration["migrations"][len(parent_migrations):] == expected_migrations, "migration append drifted")

    strict = documents["Strict_Conjecture_Ledger.json"]
    parent_strict = parent["Strict_Conjecture_Ledger.json"]
    for key in ("strict_credits", "credit_corrections", "counts", "set_digests"):
        require(strict[key] == parent_strict[key], f"strict {key} changed")
    require(len(strict["strict_credits"]) == 1_000 and len(strict["credit_corrections"]) == 1, "strict counts drifted")
    return expected_new


def check_coverage(
    coverage: Mapping[str, Any],
    curation: Mapping[str, Any],
    new_rows: Sequence[Mapping[str, Any]],
) -> None:
    parent = load_json(PARENT_DIR / "Coverage_Ledger.json")
    parent_candidates = parent["candidate_dispositions"]
    child_candidates = coverage.get("candidate_dispositions")
    require(isinstance(child_candidates, list), "coverage candidates malformed")
    validate_parent_prefix(child_candidates, parent_candidates, "coverage candidates")
    parent_residual = {
        row["source_record_id"]: row
        for row in parent_candidates
        if row.get("source_id") == SOURCE_ID and row.get("disposition") == "eligible_not_selected"
    }
    require(len(parent_residual) == 731, "parent coverage residual set is not 731")
    expected_additions: list[dict[str, Any]] = []
    for row in curation["candidate_dispositions"]:
        predecessor = parent_residual.get(row["source_record_id"])
        require(predecessor is not None, f"coverage transition lacks predecessor for {row['source_record_id']}")
        expected_additions.append({
            "candidate_key": row["candidate_key"], "source_id": SOURCE_ID,
            "source_index": row["source_index"], "source_record_id": row["source_record_id"],
            "source_record_sha256": row["source_record_sha256"], "declaration": row["declaration"],
            "declaration_kind": row["declaration_kind"], "source_syntax_kind": row["source_syntax_kind"],
            "formal_type_sha256": row["formal_type_sha256"], "semantic_key": row["semantic_key"],
            "disposition": row["disposition"], "reason_code": row["reason_code"],
            "accepted_rank": row["accepted_rank"], "target_variant_id": row["target_variant_id"],
            "target_s5_id": row["target_s5_id"], "canonical_source_record_id": None,
            "duplicate_of_semantic_key": None, "duplicate_of_variant_id": None,
            "grants_catalog_entry": row["grants_catalog_entry"], "grants_theorem_credit": row["grants_theorem_credit"],
            "origin_release": "5.4", "curation_row_sha256": row["row_sha256"],
            "parent_curation_row_sha256": row["parent_curation_row_sha256"],
            "supersedes_candidate_key": predecessor["candidate_key"],
            "transition_from_disposition": predecessor["disposition"],
        })
    require(child_candidates[len(parent_candidates):] == expected_additions, "coverage 5.4 transition rows drifted")
    keys = [row.get("candidate_key") for row in child_candidates]
    require(all(isinstance(key, str) and key for key in keys) and len(keys) == len(set(keys)), "coverage candidate_key values are not globally unique")
    superseded = [row["supersedes_candidate_key"] for row in expected_additions]
    require(len(superseded) == len(set(superseded)) == 731, "coverage supersession is not one-to-one")
    policy = coverage.get("effective_state_policy")
    require(policy == {
        "identity_fields": ["source_id", "source_record_id"],
        "supersession_field": "supersedes_candidate_key",
        "effective_rule": "A candidate row is effective exactly when no later appended row names its candidate_key in supersedes_candidate_key.",
        "historical_parent_rows_are_immutable": True,
        "release_5_4_rows_supersede_exact_5_3_residual_rows": True,
    }, "coverage effective-state policy drifted")
    referenced = set(superseded)
    effective = [row for row in child_candidates if row["candidate_key"] not in referenced]
    effective_by_identity: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for row in effective:
        source_record_id = row.get("source_record_id")
        if isinstance(source_record_id, str):
            effective_by_identity[(str(row.get("source_id")), source_record_id)].append(row)
    require(all(len(rows) == 1 for rows in effective_by_identity.values()), "coverage effective states are ambiguous")

    additions_by_code: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in new_rows:
        additions_by_code[str(row["classification"]["msc2020_code"])].append(row)
    expected_msc: list[dict[str, Any]] = []
    for parent_row in parent["msc_coverage"]:
        row = copy.deepcopy(parent_row)
        additions = additions_by_code.pop(str(row["msc_top_class"]), [])
        new_ids = sorted(item["stage_claim_id"] for item in additions)
        row["current_theorem_s5_ids"] = sorted([*row["current_theorem_s5_ids"], *new_ids])
        row["origin_theorem_s5_ids"] = new_ids
        row["origin_open_s5_ids"] = []
        if additions:
            row["source_ids"] = sorted(set(row["source_ids"]) | {SOURCE_ID})
        exact = sum(item["classification"]["basis"] == "1000_plus_curated" for item in additions)
        row["classification_basis_counts"]["source_annotation"] += exact
        row["classification_basis_counts"]["machine_crosswalk"] += len(additions) - exact
        row["counts"]["current_theorems"] = len(row["current_theorem_s5_ids"])
        row["counts"]["current_open"] = len(row["current_open_s5_ids"])
        row["counts"]["origin_theorems"] = len(new_ids)
        row["counts"]["origin_open"] = 0
        row["counts"]["open_reserve"] = len(row["open_reserve_candidate_keys"])
        classified = row["counts"]["current_theorems"] + row["counts"]["current_open"] + row["counts"]["open_reserve"]
        if classified == 0:
            row["scarcity"] = "zero"
            row["scarcity_reason"] = "No current or open-reserve member has this primary source annotation."
        elif classified < 10:
            row["scarcity"] = "thin"
            row["scarcity_reason"] = "Fewer than ten current-plus-reserve members have this primary class."
        else:
            row["scarcity"] = "adequate_in_source_inventory"
            row["scarcity_reason"] = "At least ten current-plus-reserve members have this primary class."
        expected_msc.append(row)
    require(not additions_by_code, f"coverage lacks MSC rows for {sorted(additions_by_code)}")
    require(coverage.get("msc_coverage") == expected_msc, "coverage MSC projection drifted")
    require(coverage.get("counts") == {
        "candidate_dispositions": 5_898,
        "msc_coverage": 63,
        "origin_5_4_candidates": 731,
        "origin_5_4_accepted_new_theorems": 500,
        "origin_5_4_literal_lemma_noncredit": 0,
        "origin_5_4_eligible_not_selected": 231,
    }, "coverage declared counts drifted")


def check_manifest_semantics(
    manifest: Mapping[str, Any],
    documents: Mapping[str, Mapping[str, Any]],
    curation: Mapping[str, Any],
) -> None:
    require(manifest.get("counts") == {
        "non_manifest_artifacts": 8, "catalog_records": 4_100,
        "origin_theorems": 500, "origin_open_claims": 0,
        "cumulative_theorems": 2_500, "cumulative_open_claims": 1_600,
        "effective_strict_conjecture_credits": 1_000,
    }, "manifest counts drifted")
    digests = curation["set_digests"]
    require(manifest.get("accepted_set_digests") == {
        "source_record_id_set_sha256": digests["selected_source_record_id_set_sha256"],
        "declaration_set_sha256": digests["selected_declaration_set_sha256"],
        "formal_type_sha256_set_sha256": digests["selected_formal_type_sha256_set_sha256"],
        "semantic_key_set_sha256": digests["selected_semantic_key_set_sha256"],
        "variant_id_set_sha256": digests["selected_variant_id_set_sha256"],
        "s5_id_set_sha256": digests["selected_s5_id_set_sha256"],
    }, "manifest accepted-set digests drifted")
    strict = documents["Strict_Conjecture_Ledger.json"]
    require(manifest.get("strict_credit_binding") == {
        "path": "Strict_Conjecture_Ledger.json",
        "file_sha256": sha256_file(RELEASE_DIR / "Strict_Conjecture_Ledger.json"),
        "authority_sha256": strict["authority_sha256"],
        "effective_s5_id_set_sha256": strict["set_digests"]["effective_s5_id_set_sha256"],
        "effective_variant_id_set_sha256": strict["set_digests"]["effective_variant_id_set_sha256"],
    }, "manifest strict-credit binding drifted")


def validate_current_pointer(
    current: Mapping[str, Any], manifest: Mapping[str, Any], *, prepublish: bool
) -> None:
    verify_seal(current, "Current_Release.json")
    parent = authenticated_parent_pointer()
    target = expected_target_pointer(manifest)
    if prepublish:
        require(
            current == parent or current == target,
            "transition-gate Current_Release is neither the authenticated 5.3 parent nor exact 5.4 target",
        )
        return
    require(current == target, "Current_Release is not the exact accepted 5.4 CAS pointer")


def authenticated_parent_pointer() -> dict[str, Any]:
    return {
        "authority_sha256": "c0b48bd538a3109e7695a96fb3ffc16b5a3047ab41e13b5e8d3ccfae2ec785bf",
        "manifest_path": "releases/5.3/Release_Manifest.json",
        "manifest_sha256": PARENT_MANIFEST_SHA256,
        "release": "5.3",
        "release_root_sha256": PARENT_ROOT,
        "schema_version": "awesome-theorems/stage5-current-release/5.3",
    }


def expected_target_pointer(manifest: Mapping[str, Any]) -> dict[str, Any]:
    expected: dict[str, Any] = {
        "schema_version": "awesome-theorems/stage5-current-release/5.4",
        "release": "5.4",
        "manifest_path": "releases/5.4/Release_Manifest.json",
        "manifest_sha256": sha256_file(RELEASE_DIR / MANIFEST_NAME),
        "release_root_sha256": manifest["release_root_sha256"],
    }
    expected["authority_sha256"] = hash_without(expected, "authority_sha256")
    return expected


def check_current(manifest: Mapping[str, Any], *, prepublish: bool) -> None:
    current = load_json(CURRENT_PATH, canonical=True)
    validate_current_pointer(current, manifest, prepublish=prepublish)


def validate_readable_structure(
    readable_dir: Path, documents: Mapping[str, Mapping[str, Any]]
) -> None:
    expected_names = {"Theorem_List.md", "Open_Claim_List.md", "Strict_Conjecture_List.md"}
    require(readable_dir.is_dir(), "readable/5.4 directory is missing")
    observed = {path.name for path in readable_dir.iterdir() if path.is_file()}
    require(observed == expected_names, f"readable/5.4 file set drifted: {sorted(observed)}")
    expected_ids = {
        "Theorem_List.md": documents["Theorem_List.json"]["stage_claim_ids"],
        "Open_Claim_List.md": documents["Open_Claim_List.json"]["stage_claim_ids"],
        "Strict_Conjecture_List.md": [
            row["stage_claim_id"]
            for row in documents["Strict_Conjecture_Ledger.json"]["strict_credits"]
        ],
    }
    root = str(documents[MANIFEST_NAME]["release_root_sha256"])
    for name in sorted(expected_names):
        raw = (readable_dir / name).read_bytes()
        require(raw and raw.endswith(b"\n"), f"readable {name} is empty/noncanonical")
        try:
            text_value = raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise CheckError(f"readable {name} is not UTF-8: {error}") from error
        require(f"sha256:{root}" in text_value, f"readable {name} release-root header drifted")
        observed_ids = re.findall(r"^## (S5-CLM-[0-9]{8})(?:\s|$)", text_value, re.MULTILINE)
        require(observed_ids == expected_ids[name], f"readable {name} member ID/order projection drifted")


def check_readable(documents: Mapping[str, Mapping[str, Any]]) -> None:
    validate_readable_structure(READABLE_DIR, documents)
    command = [
        sys.executable,
        str(REPO_ROOT / "Docs/tools/render_math_catalog_v5.py"),
        "--release",
        "5.4",
        "--check",
    ]
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    require(result.returncode == 0, f"detailed readable projections drifted: {result.stdout.strip()}")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prepublish",
        action="store_true",
        help="transition gate: accept only authenticated parent 5.3 or the exact idempotent 5.4 target pointer",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        check_parent_release()
        manifest, documents = check_release_package()
        schema, inputs = check_authorities(manifest)
        _source_rows, source_by_id = source_indexes()
        parent_catalog = load_json(PARENT_DIR / "Claim_Catalog.json")
        require(sha256_file(PARENT_DIR / "Claim_Catalog.json") == PARENT_CATALOG_SHA256, "5.3 catalog bytes drifted")
        curation, accepted = check_curation(parent_catalog, source_by_id)
        new_rows = check_artifacts(documents, schema, inputs, curation, accepted, source_by_id)
        check_coverage(documents["Coverage_Ledger.json"], curation, new_rows)
        check_manifest_semantics(manifest, documents, curation)
        check_readable(documents)
        check_current(manifest, prepublish=args.prepublish)
        print(
            "PASS independent math catalog 5.4 "
            f"mode={'prepublish' if args.prepublish else 'published'} "
            f"root={manifest['release_root_sha256']} catalog=4100 theorem=2500 "
            "open=1600 strict=1000 selected=500 remaining=231"
        )
        return 0
    except (CheckError, OSError, KeyError, TypeError, ValueError, IndexError) as error:
        print(f"FAIL independent math catalog 5.4: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
