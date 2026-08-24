#!/usr/bin/env python3
"""Build the fail-closed PutnamBench 5.6 intake qualification.

This program does not discover or invent mathematical relations.  It joins a
frozen PutnamBench source universe to separately reviewed seed, formal-variant,
and one-hop-relation ledgers.  Qualification is possible only when all 768
full-grid benchmark seeds, the exact 675-key PutnamBench subset, 1,724
formalization files, and the complete frozen relation-candidate universe all
have final dispositions.  Benchmark seeds, formal variants, and edges receive
zero catalog credit.

``--write`` writes only qualification receipts; it never creates release 5.6
or changes ``Current_Release.json``.  ``--check`` reconstructs the receipts and
requires byte-identical existing files.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
import hashlib
import json
import math
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[4]
V5_ROOT = REPO_ROOT / "Docs/catalog/v5"
CURATION_ROOT = V5_ROOT / "curation/putnambench_v5_6"
PARENT_ROOT = V5_ROOT / "releases/5.5"

SOURCE_INVENTORY = CURATION_ROOT / "PutnamBench_Source_Inventory_v5_6.json"
SOURCE_PROBLEMS = CURATION_ROOT / "PutnamBench_Source_Problems_v5_6.jsonl"
FORMAL_VARIANTS = CURATION_ROOT / "PutnamBench_Formal_Variants_v5_6.jsonl"
FORMAL_DECLARATION_ASSET = CURATION_ROOT / "PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
FULL_SOURCE_INVENTORY = CURATION_ROOT / "Full_Putnam_Source_Inventory_v5_6.json"
FULL_SOURCE_CANDIDATES = CURATION_ROOT / "Full_Putnam_Source_Candidates_v5_6.jsonl"
FULL_SOURCE_PROBLEMS = CURATION_ROOT / "Full_Putnam_Seed_Problems_v5_6.jsonl"
SEED_CROSSWALK = CURATION_ROOT / "seed-crosswalk.jsonl"
FORMAL_CROSSWALK = CURATION_ROOT / "formal-variant-crosswalk.jsonl"
RELATION_UNIVERSE = CURATION_ROOT / "relation-source-universe.json"
RELATION_CANDIDATES = CURATION_ROOT / "relation-candidate-ledger.jsonl"
CLOSURE_NODES = CURATION_ROOT / "closure-node-ledger.jsonl"
RELATION_EDGES = CURATION_ROOT / "relation-edge-ledger.jsonl"

QUALIFICATION = CURATION_ROOT / "PutnamBench_Intake_Qualification_v5_6.json"
COVERAGE_RECEIPT = CURATION_ROOT / "coverage-receipt.json"
RELATION_RECEIPT = CURATION_ROOT / "relation-closure-receipt.json"

PARENT_RELEASE_ROOT_SHA256 = "fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0"
PARENT_MANIFEST_SHA256 = "773253c2afad3a91c1b14cc9b5f60b51ec9b7e258d1619f0168dd23c9c4b0a43"
PARENT_CATALOG_SHA256 = "9d6dc79b1cbdee401f2f022ee027557a04331fa9605dc7f443fdc09a62b029b4"
PARENT_THEOREM_SHA256 = "f57b885995f4edf8204e96b57b7489c3dfa9d6ac96785031d0498b9ed80f46ab"
PARENT_STRICT_SHA256 = "01d80455b51d03861fffdf23bc3a300a0d8a176304c61667f3e6a68ba365d34a"

EXPECTED_SOURCE_COUNTS = {
    "all_problem_key_union": 675,
    "informal_problem_key_union": 673,
    "formal_variants": 1_724,
    "formal_problem_key_union": 674,
}
EXPECTED_LANGUAGE_COUNTS = {"lean4": 672, "isabelle": 640, "coq": 412}

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
PROBLEM_RE = re.compile(r"^putnam_[0-9]{4}_[ab][1-6]$")
S5_RE = re.compile(r"^S5-CLM-[0-9]{8}$")
ATV_RE = re.compile(r"^ATV-[0-9]{8}$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

SEED_DISPOSITIONS = {"reviewed_noncatalog_benchmark_seed"}
FORMAL_DISPOSITIONS = {
    "same_exact_claim_variant",
    "stronger_variant",
    "weaker_variant",
    "different_claim_variant",
    "wrong_problem_duplicate",
    "malformed_or_nonclaim_variant",
}
RELATION_TYPES = {
    "direct_prerequisite",
    "standard_solution_uses",
    "generalization",
    "specialization",
    "equivalence",
    "dual",
    "analogy",
    "corollary",
    "strengthening",
    "weakening",
    "direct_open_generalization",
    "partial_progress",
}
REJECTED_RELATION_DISPOSITIONS = {
    "rejected_topic_only",
    "rejected_tag_only",
    "rejected_import_only",
    "rejected_cooccurrence_only",
    "rejected_name_only",
    "rejected_nonclaim_method",
    "rejected_nonclaim_endpoint",
    "rejected_relation_not_established",
    "rejected_duplicate_candidate",
    "rejected_outside_one_hop",
}
CLAIM_KINDS = {"theorem", "conjecture", "hypothesis", "open_problem"}
OPEN_KINDS = CLAIM_KINDS - {"theorem"}

SEED_ROW_KEYS = frozenset(
    {
        "schema_version", "problem_key", "source_problem_row_sha256",
        "disposition", "alias_of_problem_key", "targets",
        "formal_variant_ids", "statement_review", "review", "row_sha256",
    }
)
TARGET_KEYS = frozenset(
    {
        "semantic_key", "identity_action", "stage_claim_id", "variant_id",
        "parent_catalog_record_sha256", "allocation_request_sha256",
        "claim_kind", "material_status", "statement", "proof_evidence",
        "rights",
    }
)
STATEMENT_KEYS = frozenset(
    {
        "language", "representation", "text", "statement_sha256",
        "source_bindings", "independently_written",
    }
)
SEED_REVIEW_KEYS = frozenset(
    {
        "reviewer_id", "reviewed_as_of", "manual_statement_review",
        "manual_benchmark_proposition_review", "notes",
    }
)
STATEMENT_REVIEW_KEYS = frozenset(
    {
        "exact_scope_reviewed", "quantifiers_and_assumptions_reviewed",
        "factored_answer_visibility_reviewed", "formal_variant_inventory_bound",
        "formal_variant_semantic_review_deferred_to_formal_crosswalk",
        "parent_semantic_dedupe_reviewed", "benchmark_proposition_complete",
    }
)
FORMAL_ROW_KEYS = frozenset(
    {
        "schema_version", "variant_id", "source_variant_row_sha256",
        "source_problem_key", "semantic_problem_key", "disposition",
        "target_semantic_keys", "statement_equivalence", "review", "row_sha256",
    }
)
FORMAL_EQUIVALENCE_KEYS = frozenset(
    {
        "reviewed", "exact_statement_scope", "assumptions_preserved",
        "conclusion_preserved", "notes",
    }
)
RELATION_SOURCE_KEYS = frozenset(
    {
        "source_id", "role", "path", "file_sha256", "size_bytes",
        "source_revision", "rights", "scope", "row_sha256",
    }
)
RELATION_OBLIGATION_KEYS = frozenset(
    {
        "obligation_id", "problem_key", "source_id", "discovery_method",
        "source_scope", "candidate_keys", "zero_candidate_finding", "row_sha256",
    }
)
RELATION_CANDIDATE_KEYS = frozenset(
    {
        "schema_version", "candidate_key", "obligation_id", "problem_key",
        "proposed_relation_type", "target_candidate", "disposition",
        "reason_code", "target_node_id", "edge_id", "review", "row_sha256",
    }
)
NODE_KEYS = frozenset(
    {
        "schema_version", "node_id", "distance", "seed_problem_keys",
        "semantic_key", "claim_kind", "material_status", "catalog_action",
        "stage_claim_id", "variant_id", "parent_catalog_record_sha256",
        "allocation_request_sha256", "statement", "status_evidence",
        "proof_evidence", "rights", "source_bindings", "incoming_edge_ids",
        "row_sha256",
    }
)
EDGE_KEYS = frozenset(
    {
        "schema_version", "edge_id", "candidate_key", "seed_problem_key",
        "from_node_id", "to_node_id", "relation_type", "evidence",
        "directness", "review", "row_sha256",
    }
)
FULL_SOURCE_ROW_KEYS = frozenset(
    {
        "schema_version", "problem_key", "coordinate", "source_branch",
        "source_candidate_ids", "source_statement_sha256",
        "source_solution_sha256", "putnambench_problem_row_sha256",
        "formal_variant_ids", "rights_id", "anomaly_codes", "row_sha256",
    }
)
FULL_SOURCE_CANDIDATE_KEYS = frozenset(
    {
        "schema_version", "source_candidate_id", "source_branch",
        "source_binding", "source_statement_sha256", "source_solution_sha256",
        "source_problem_key", "source_year", "disposition", "target_problem_key",
        "rights_id", "row_sha256",
    }
)
DIRECTNESS_KEYS = frozenset(
    {
        "proposition_level", "direct_relation_verified", "topic_only",
        "tag_only", "import_only", "cooccurrence_only", "name_only",
        "nonclaim_endpoint",
    }
)
SOURCE_EVIDENCE_KEYS = frozenset(
    {
        "source_id", "path", "file_sha256", "locator", "evidence_sha256",
        "rights_id",
    }
)
TARGET_RIGHTS_KEYS = frozenset(
    {
        "catalog_relicenses_source", "statement_origin",
        "source_wording_redistributed", "cleared_for_catalog_statement",
        "attribution",
    }
)
PROOF_KEYS = frozenset(
    {
        "kind", "proof_state", "uses_placeholder", "reviewed",
        "applies_to_statement_sha256", "proof_method_summary",
        "proof_method_summary_sha256", "independently_written_summary",
        "source_binding", "rights",
    }
)
RELATION_REVIEW_KEYS = frozenset(
    {
        "reviewer_id", "reviewed_as_of", "manual_statement_review",
        "manual_relation_review", "notes",
    }
)
FORMAL_REVIEW_KEYS = frozenset(
    {
        "reviewer_id", "reviewed_as_of", "manual_statement_review",
        "manual_formal_variant_semantic_review",
        "manual_filename_declaration_anomaly_review", "notes",
    }
)
STATUS_EVIDENCE_KEYS = frozenset(
    {"status", "as_of", "independently_reviewed", "source_bindings", "notes"}
)
TARGET_CANDIDATE_KEYS = frozenset(
    {"kind", "label", "statement_sha256", "source_binding"}
)
RELATION_EVIDENCE_KEYS = frozenset(
    {
        "source_id", "path", "file_sha256", "locator",
        "relation_evidence_sha256", "rights_id", "relation_assertion",
        "relation_assertion_origin", "source_wording_redistributed",
        "proof_step_binding",
    }
)


class IntakeError(RuntimeError):
    """An intake authority, review ledger, or closure invariant failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IntakeError(message)


def closed(value: Any, keys: Iterable[str], label: str) -> Mapping[str, Any]:
    require(isinstance(value, dict), f"{label} is not an object")
    expected = set(keys)
    require(set(value) == expected, f"{label} keys differ: expected={sorted(expected)} got={sorted(value)}")
    return value


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise IntakeError(f"value is not canonical JSON: {error}") from error


def encoded(value: Any) -> bytes:
    return canonical(value) + b"\n"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def reject_constant(token: str) -> None:
    raise IntakeError(f"non-finite JSON constant is forbidden: {token}")


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(raw: bytes, label: str) -> Any:
    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=reject_pairs,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise IntakeError(f"{label} is not strict UTF-8 JSON: {error}") from error
    return value


def safe_file(path: Path, label: str) -> Path:
    resolved_root = REPO_ROOT.resolve()
    resolved = path.resolve(strict=True)
    require(resolved.is_relative_to(resolved_root), f"{label} escapes repository")
    require(path.is_file() and not path.is_symlink(), f"{label} is not a regular file")
    return path


def load_json(path: Path, label: str) -> dict[str, Any]:
    safe_file(path, label)
    value = parse_json(path.read_bytes(), label)
    require(isinstance(value, dict), f"{label} root is not an object")
    return value


def load_jsonl(path: Path, label: str) -> list[dict[str, Any]]:
    safe_file(path, label)
    rows: list[dict[str, Any]] = []
    for number, raw in enumerate(path.read_bytes().splitlines(), start=1):
        require(raw.strip() == raw and raw, f"{label}:{number} blank/whitespace line")
        value = parse_json(raw, f"{label}:{number}")
        require(isinstance(value, dict), f"{label}:{number} is not an object")
        require(canonical(value) == raw, f"{label}:{number} is not canonical JSON")
        rows.append(value)
    return rows


def row_hash(row: Mapping[str, Any], field: str = "row_sha256") -> str:
    return digest(canonical({key: value for key, value in row.items() if key != field}))


def verify_row(row: Mapping[str, Any], keys: Iterable[str], label: str) -> None:
    closed(row, keys, label)
    require(row.get("row_sha256") == row_hash(row), f"{label} row hash drifted")


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop("authority_sha256", None)
    result["authority_sha256"] = digest(canonical(result))
    return result


def verify_seal(value: Mapping[str, Any], label: str) -> None:
    authority = value.get("authority_sha256")
    require(isinstance(authority, str) and SHA_RE.fullmatch(authority) is not None, f"{label} authority missing")
    body = {key: item for key, item in value.items() if key != "authority_sha256"}
    require(authority == digest(canonical(body)), f"{label} authority drifted")


def set_digest(values: Iterable[str]) -> str:
    ordered = sorted(values)
    require(len(ordered) == len(set(ordered)), "set digest input contains duplicates")
    return digest(canonical(ordered))


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def binding(path: Path, *, rows: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": relative(path),
        "file_sha256": sha_file(path),
        "size_bytes": path.stat().st_size,
    }
    if rows is not None:
        result["row_count"] = len(rows)
        result["row_set_sha256"] = set_digest(str(row["row_sha256"]) for row in rows)
    return result


def text(value: Any, label: str, pattern: re.Pattern[str] | None = None) -> str:
    require(isinstance(value, str) and value.strip() == value and value, f"{label} is not a nonempty canonical string")
    if pattern is not None:
        require(pattern.fullmatch(value) is not None, f"{label} syntax invalid")
    return value


def integer(value: Any, label: str, minimum: int = 0) -> int:
    require(isinstance(value, int) and not isinstance(value, bool) and value >= minimum, f"{label} is not an integer >= {minimum}")
    return value


def verify_parent() -> tuple[dict[str, Any], dict[str, Mapping[str, Any]]]:
    manifest_path = PARENT_ROOT / "Release_Manifest.json"
    catalog_path = PARENT_ROOT / "Claim_Catalog.json"
    theorem_path = PARENT_ROOT / "Theorem_List.json"
    strict_path = PARENT_ROOT / "Strict_Conjecture_Ledger.json"
    require(sha_file(manifest_path) == PARENT_MANIFEST_SHA256, "5.5 manifest bytes drifted")
    require(sha_file(catalog_path) == PARENT_CATALOG_SHA256, "5.5 catalog bytes drifted")
    require(sha_file(theorem_path) == PARENT_THEOREM_SHA256, "5.5 theorem projection bytes drifted")
    require(sha_file(strict_path) == PARENT_STRICT_SHA256, "5.5 strict ledger bytes drifted")
    manifest = load_json(manifest_path, "5.5 manifest")
    verify_seal(manifest, "5.5 manifest")
    require(manifest.get("release") == "5.5" and manifest.get("release_root_sha256") == PARENT_RELEASE_ROOT_SHA256, "wrong 5.5 parent root")
    counts = manifest.get("counts")
    require(
        isinstance(counts, dict)
        and counts.get("catalog_records") == 4_525
        and counts.get("cumulative_theorems") == 2_500
        and counts.get("cumulative_open_claims") == 2_025
        and counts.get("effective_strict_conjecture_credits") == 1_425,
        "5.5 parent counts drifted",
    )
    catalog = load_json(catalog_path, "5.5 catalog")
    verify_seal(catalog, "5.5 catalog")
    records = catalog.get("records")
    require(isinstance(records, list) and len(records) == 4_525, "5.5 catalog denominator drifted")
    by_stage: dict[str, Mapping[str, Any]] = {}
    for index, row in enumerate(records):
        require(isinstance(row, dict), f"5.5 catalog[{index}] malformed")
        sid = text(row.get("stage_claim_id"), f"5.5 catalog[{index}].stage_claim_id", S5_RE)
        require(sid not in by_stage, f"duplicate 5.5 stage ID: {sid}")
        by_stage[sid] = row
    return manifest, by_stage


def source_universe() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    inventory = load_json(SOURCE_INVENTORY, "PutnamBench source inventory")
    verify_seal(inventory, "PutnamBench source inventory")
    snapshot = inventory.get("source_snapshot")
    require(
        isinstance(snapshot, dict)
        and snapshot.get("archive_embedded_in_repository") is False
        and snapshot.get("catalog_distributes_full_source_archive") is False
        and snapshot.get("operator_supplied_external_archive_required_for_full_replay") is True
        and snapshot.get("upstream_commit") == "dfb0a47a1c1ec3a10f2a9acfdf41a2043920f33c"
        and snapshot.get("upstream_git_tree_sha1") == "609c8623a81281f5442c0c4dc7e82dc015e97ed9"
        and snapshot.get("archive_sha256") == "843911c7eb432c0ce96ac1e6494f9675336a9be935884cd5b6de4575db042c30"
        and snapshot.get("archive_byte_length") == 988_321,
        "PutnamBench source snapshot pin drifted",
    )
    text(snapshot.get("external_archive_url"), "PutnamBench external archive URL")
    problems = load_jsonl(SOURCE_PROBLEMS, "PutnamBench source problems")
    variants = load_jsonl(FORMAL_VARIANTS, "PutnamBench formal variants")
    counts = inventory.get("counts")
    require(isinstance(counts, dict), "source inventory counts malformed")
    for key, wanted in EXPECTED_SOURCE_COUNTS.items():
        require(counts.get(key) == wanted, f"source inventory {key} drifted")
    by_language = counts.get("formal_variants_by_language")
    require(by_language == EXPECTED_LANGUAGE_COUNTS, "source inventory language counts drifted")
    require(len(problems) == 675 and len(variants) == 1_724, "source JSONL denominator drifted")
    problem_by_key: dict[str, dict[str, Any]] = {}
    variant_by_id: dict[str, dict[str, Any]] = {}
    variant_ids_by_problem: dict[str, list[str]] = defaultdict(list)
    for index, row in enumerate(problems):
        require(row.get("row_sha256") == row_hash(row), f"source problem[{index}] hash drifted")
        key = text(row.get("problem_key"), f"source problem[{index}].problem_key", PROBLEM_RE)
        require(key not in problem_by_key, f"duplicate source problem: {key}")
        problem_by_key[key] = row
    for index, row in enumerate(variants):
        require(row.get("row_sha256") == row_hash(row), f"formal variant[{index}] hash drifted")
        variant_id = text(row.get("variant_id"), f"formal variant[{index}].variant_id")
        key = text(row.get("problem_key"), f"formal variant[{index}].problem_key", PROBLEM_RE)
        require(variant_id not in variant_by_id and key in problem_by_key, f"formal variant[{index}] identity invalid")
        language = row.get("language")
        require(language in EXPECTED_LANGUAGE_COUNTS, f"formal variant[{index}] language invalid")
        variant_by_id[variant_id] = row
        variant_ids_by_problem[key].append(variant_id)
    require(Counter(row["language"] for row in variants) == Counter(EXPECTED_LANGUAGE_COUNTS), "formal language denominator differs")
    for key, row in problem_by_key.items():
        declared = row.get("formal_variant_ids")
        require(isinstance(declared, list) and len(declared) == len(set(declared)), f"source problem {key} variant IDs malformed")
        require(set(declared) == set(variant_ids_by_problem.get(key, [])), f"source problem {key} variant projection drifted")
    outputs = inventory.get("outputs")
    require(isinstance(outputs, dict), "source inventory output bindings malformed")
    for name, path, rows in (
        ("problems", SOURCE_PROBLEMS, problems),
        ("formal_variants", FORMAL_VARIANTS, variants),
    ):
        item = outputs.get(name)
        require(
            isinstance(item, dict)
            and item.get("path") == relative(path)
            and item.get("sha256") == sha_file(path)
            and item.get("row_count") == len(rows),
            f"source inventory {name} output binding drifted",
        )
    formal_assets = load_jsonl(FORMAL_DECLARATION_ASSET, "PutnamBench formal declaration asset")
    formal_output = outputs.get("formal_declaration_asset")
    require(
        len(formal_assets) == 1_724
        and isinstance(formal_output, dict)
        and formal_output.get("path") == relative(FORMAL_DECLARATION_ASSET)
        and formal_output.get("sha256") == sha_file(FORMAL_DECLARATION_ASSET)
        and formal_output.get("row_count") == len(formal_assets),
        "source inventory formal declaration asset binding drifted",
    )
    require(
        inventory.get("coverage", {}).get("exact_informal_statement_or_solution_text_reproduced_in_derived_rows") is False
        and inventory.get("coverage", {}).get("full_informal_source_replay_available_without_external_archive") is False
        and inventory.get("coverage", {}).get("formal_asset_excludes_docstrings_supporting_definitions_and_full_source_files") is True,
        "PutnamBench source rights/replay boundary drifted",
    )
    return inventory, problems, variants, problem_by_key, variant_by_id


def coordinate_for(problem_key: str) -> dict[str, Any]:
    match = PROBLEM_RE.fullmatch(problem_key)
    require(match is not None, f"invalid Putnam coordinate key: {problem_key}")
    parts = problem_key.split("_")
    return {
        "competition": "William Lowell Putnam Mathematical Competition",
        "year": int(parts[1]),
        "section": parts[2][0].upper(),
        "problem_number": int(parts[2][1:]),
    }


def full_grid_keys() -> set[str]:
    return {
        f"putnam_{year}_{section}{number}"
        for year in range(1962, 2026)
        for section in ("a", "b")
        for number in range(1, 7)
    }


def full_source_universe(
    pb_inventory: Mapping[str, Any],
    pb_problem_by_key: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    inventory = load_json(FULL_SOURCE_INVENTORY, "full Putnam source inventory")
    verify_seal(inventory, "full Putnam source inventory")
    expected_keys = {
        "schema_version", "putnambench_source_inventory_authority_sha256",
        "source_snapshots", "coordinate_policy", "rights", "outputs", "counts",
        "set_digests", "authority_sha256",
    }
    closed(inventory, expected_keys, "full Putnam source inventory")
    require(inventory.get("schema_version") == "awesome-theorems/full-putnam-source-inventory/5.6", "full Putnam source schema drifted")
    require(inventory.get("putnambench_source_inventory_authority_sha256") == pb_inventory.get("authority_sha256"), "full source PB authority drifted")
    snapshots = inventory.get("source_snapshots")
    require(isinstance(snapshots, dict) and set(snapshots) == {"putnamgap", "kedlaya_2025"}, "full Putnam source snapshots malformed")
    putnamgap = snapshots["putnamgap"]
    kedlaya = snapshots["kedlaya_2025"]
    require(
        isinstance(putnamgap, dict)
        and putnamgap.get("repository") == "https://github.com/YurenHao0426/PutnamGAP"
        and putnamgap.get("commit") == "aee05407afc7e621e8d9c7f909f4f25ccb8131c0"
        and putnamgap.get("git_tree_sha1") == "0f55aee4f4b911e767785a7c5977fbe36f58dbbe"
        and putnamgap.get("source_row_count") == 1_051
        and putnamgap.get("archive_embedded_in_repository") is False
        and putnamgap.get("raw_problem_or_solution_text_redistributed") is False,
        "PutnamGAP source pin drifted",
    )
    require(
        isinstance(kedlaya, dict)
        and kedlaya.get("source_row_count") == 12
        and kedlaya.get("year") == 2025
        and kedlaya.get("archive_embedded_in_repository") is False
        and kedlaya.get("raw_problem_or_solution_text_redistributed") is False
        and isinstance(kedlaya.get("immutable_revision"), str)
        and bool(kedlaya["immutable_revision"]),
        "Kedlaya 2025 source pin drifted",
    )
    for source_name, snapshot in snapshots.items():
        text(snapshot.get("external_archive_sha256"), f"full source {source_name}.external_archive_sha256", SHA_RE)
        integer(snapshot.get("external_archive_byte_length"), f"full source {source_name}.external_archive_byte_length", 1)
        text(snapshot.get("external_archive_locator"), f"full source {source_name}.external_archive_locator")
        manifest_path_text = text(snapshot.get("prose_free_manifest_repository_path"), f"full source {source_name}.prose_free_manifest_repository_path")
        manifest_path = safe_file(REPO_ROOT / manifest_path_text, f"full source {source_name} prose-free manifest")
        require(
            snapshot.get("prose_free_manifest_sha256") == sha_file(manifest_path)
            and snapshot.get("prose_free_manifest_byte_length") == manifest_path.stat().st_size,
            f"full source {source_name} prose-free manifest bytes drifted",
        )
    rights = inventory.get("rights")
    release_policy = rights.get("catalog_release_policy") if isinstance(rights, dict) else None
    require(
        isinstance(release_policy, dict)
        and release_policy.get("catalog_relicenses_source") is False
        and release_policy.get("exact_original_problem_text_redistributed") is False
        and release_policy.get("exact_canonical_solution_text_redistributed") is False
        and release_policy.get("independently_written_statement_required") is True
        and release_policy.get("independently_written_proof_and_relation_summary_required") is True,
        "full Putnam source rights boundary malformed",
    )
    policy = inventory.get("coordinate_policy")
    require(
        isinstance(policy, dict)
        and policy.get("first_year") == 1962
        and policy.get("last_year") == 2025
        and policy.get("sections") == ["A", "B"]
        and policy.get("problems_per_section") == [1, 2, 3, 4, 5, 6]
        and policy.get("coordinate_existence_alone_grants_claim_credit") is False,
        "full Putnam coordinate policy drifted",
    )
    candidates = load_jsonl(FULL_SOURCE_CANDIDATES, "full Putnam source candidates")
    require(len(candidates) == 1_063, "full Putnam source-candidate denominator must be 1,051 + 12")
    candidate_by_id: dict[str, dict[str, Any]] = {}
    candidates_by_target: dict[str, list[str]] = defaultdict(list)
    candidate_branches: Counter[str] = Counter()
    for index, row in enumerate(candidates):
        verify_row(row, FULL_SOURCE_CANDIDATE_KEYS, f"full source candidate[{index}]")
        require(row.get("schema_version") == "awesome-theorems/full-putnam-source-candidate/5.6", f"full source candidate[{index}] schema drifted")
        candidate_id = text(row.get("source_candidate_id"), f"full source candidate[{index}].source_candidate_id")
        require(candidate_id not in candidate_by_id, f"duplicate full source candidate {candidate_id}")
        branch = row.get("source_branch")
        require(branch in {"putnamgap", "kedlaya_2025"}, f"full source candidate {candidate_id} branch invalid")
        verify_source_evidence(row.get("source_binding"), f"full source candidate {candidate_id}.source_binding")
        text(row.get("source_statement_sha256"), f"full source candidate {candidate_id}.source_statement_sha256", SHA_RE)
        text(row.get("source_solution_sha256"), f"full source candidate {candidate_id}.source_solution_sha256", SHA_RE)
        text(row.get("source_problem_key"), f"full source candidate {candidate_id}.source_problem_key")
        source_year = integer(row.get("source_year"), f"full source candidate {candidate_id}.source_year", 1938)
        require(source_year <= 2025, f"full source candidate {candidate_id} year invalid")
        disposition = row.get("disposition")
        require(disposition in {
            "mapped_in_scope_coordinate", "alternate_or_duplicate_source_variant",
            "out_of_scope_pre_1962", "rejected_malformed_source_row",
        }, f"full source candidate {candidate_id} disposition invalid")
        target = row.get("target_problem_key")
        if disposition in {"mapped_in_scope_coordinate", "alternate_or_duplicate_source_variant"}:
            target_key = text(target, f"full source candidate {candidate_id}.target_problem_key", PROBLEM_RE)
            require(target_key in full_grid_keys(), f"full source candidate {candidate_id} maps outside grid")
            require(int(target_key.split("_")[1]) == source_year, f"full source candidate {candidate_id} crosses years")
            candidates_by_target[target_key].append(candidate_id)
        else:
            require(target is None, f"out-of-scope/malformed source candidate {candidate_id} has target")
            if disposition == "out_of_scope_pre_1962":
                require(source_year < 1962, f"source candidate {candidate_id} pre-1962 disposition false")
        text(row.get("rights_id"), f"full source candidate {candidate_id}.rights_id")
        candidate_by_id[candidate_id] = row
        candidate_branches[str(branch)] += 1
    require(candidate_branches == Counter({"putnamgap": 1_051, "kedlaya_2025": 12}), "full source candidate branch counts drifted")
    rows = load_jsonl(FULL_SOURCE_PROBLEMS, "full Putnam source problems")
    require(len(rows) == 768, "full Putnam source must contain exactly 768 rows")
    by_key: dict[str, dict[str, Any]] = {}
    branches: Counter[str] = Counter()
    for index, row in enumerate(rows):
        verify_row(row, FULL_SOURCE_ROW_KEYS, f"full Putnam source[{index}]")
        require(row.get("schema_version") == "awesome-theorems/full-putnam-source-problem/5.6", f"full Putnam source[{index}] schema drifted")
        key = text(row.get("problem_key"), f"full Putnam source[{index}].problem_key", PROBLEM_RE)
        require(key not in by_key, f"duplicate full Putnam key {key}")
        require(row.get("coordinate") == coordinate_for(key), f"full Putnam source {key} coordinate drifted")
        branch = row.get("source_branch")
        wanted_branch = "putnamgap" if int(key.split("_")[1]) <= 2024 else "kedlaya_2025"
        require(branch == wanted_branch, f"full Putnam source {key} branch invalid")
        candidate_ids = row.get("source_candidate_ids")
        require(
            isinstance(candidate_ids, list)
            and candidate_ids == sorted(set(candidate_ids))
            and candidate_ids
            and set(candidate_ids) == set(candidates_by_target.get(key, [])),
            f"full Putnam source {key} candidate projection drifted",
        )
        require(all(candidate_by_id[item]["source_branch"] == branch for item in candidate_ids), f"full Putnam source {key} mixes source branches")
        variants = row.get("formal_variant_ids")
        require(isinstance(variants, list) and len(variants) == len(set(variants)), f"full Putnam source {key} variants malformed")
        pb = pb_problem_by_key.get(key)
        if pb is not None:
            require(
                row.get("putnambench_problem_row_sha256") == pb.get("row_sha256")
                and variants == pb.get("formal_variant_ids"),
                f"full Putnam source {key} PB binding drifted",
            )
        else:
            require(row.get("putnambench_problem_row_sha256") is None and not variants, f"full Putnam source {key} PB complement binding drifted")
        text(row.get("source_statement_sha256"), f"full Putnam source {key}.source_statement_sha256", SHA_RE)
        text(row.get("source_solution_sha256"), f"full Putnam source {key}.source_solution_sha256", SHA_RE)
        text(row.get("rights_id"), f"full Putnam source {key}.rights_id")
        require(isinstance(row.get("anomaly_codes"), list), f"full Putnam source {key}.anomaly_codes malformed")
        branches[branch] += 1
        by_key[key] = row
    grid = full_grid_keys()
    require(set(by_key) == grid, "full Putnam source key set differs from the 1962--2025 768 grid")
    require(branches == Counter({"putnamgap": 756, "kedlaya_2025": 12}), "full Putnam source branch counts drifted")
    counts = inventory.get("counts")
    require(
        isinstance(counts, dict)
        and counts.get("full_grid_problem_keys") == 768
        and counts.get("putnambench_subset_problem_keys") == 675
        and counts.get("outside_putnambench_problem_keys") == 93
        and counts.get("putnamgap_source_candidates") == 1_051
        and counts.get("kedlaya_2025_source_candidates") == 12
        and counts.get("putnamgap_grid_problem_keys") == 756
        and counts.get("kedlaya_2025_grid_problem_keys") == 12,
        "full Putnam source counts drifted",
    )
    outputs = inventory.get("outputs")
    require(isinstance(outputs, dict), "full Putnam source outputs malformed")
    candidate_output = outputs.get("full_source_candidates")
    output = outputs.get("full_source_problems")
    require(
        isinstance(candidate_output, dict)
        and candidate_output.get("path") == relative(FULL_SOURCE_CANDIDATES)
        and candidate_output.get("sha256") == sha_file(FULL_SOURCE_CANDIDATES)
        and candidate_output.get("row_count") == 1_063,
        "full Putnam source-candidate output binding drifted",
    )
    require(
        isinstance(output, dict)
        and output.get("path") == relative(FULL_SOURCE_PROBLEMS)
        and output.get("sha256") == sha_file(FULL_SOURCE_PROBLEMS)
        and output.get("row_count") == 768,
        "full Putnam source output binding drifted",
    )
    digests = inventory.get("set_digests")
    require(
        isinstance(digests, dict)
        and digests.get("full_grid_problem_key_set_sha256") == set_digest(grid)
        and digests.get("putnambench_problem_key_set_sha256") == set_digest(pb_problem_by_key)
        and digests.get("supplemental_problem_key_set_sha256") == set_digest(grid - set(pb_problem_by_key))
        and digests.get("source_candidate_id_set_sha256") == set_digest(candidate_by_id)
        and digests.get("problem_row_set_sha256") == set_digest(str(row["row_sha256"]) for row in rows),
        "full Putnam source set digests drifted",
    )
    return inventory, candidates, rows, by_key


def verify_source_evidence(value: Any, label: str) -> dict[str, Any]:
    source = dict(closed(value, SOURCE_EVIDENCE_KEYS, label))
    text(source.get("source_id"), f"{label}.source_id")
    path_text = text(source.get("path"), f"{label}.path")
    require(not path_text.startswith("/") and ".." not in Path(path_text).parts, f"{label}.path is not repository-relative")
    path = safe_file(REPO_ROOT / path_text, f"{label}.path")
    expected_file = text(source.get("file_sha256"), f"{label}.file_sha256", SHA_RE)
    require(sha_file(path) == expected_file, f"{label} file bytes drifted")
    locator = source.get("locator")
    require(isinstance(locator, dict) and locator, f"{label}.locator malformed")
    text(source.get("evidence_sha256"), f"{label}.evidence_sha256", SHA_RE)
    text(source.get("rights_id"), f"{label}.rights_id")
    return source


def verify_rights(value: Any, label: str) -> dict[str, Any]:
    rights = dict(closed(value, TARGET_RIGHTS_KEYS, label))
    require(rights.get("catalog_relicenses_source") is False, f"{label} improperly relicenses source")
    require(rights.get("statement_origin") == "independently_written_reviewed_summary", f"{label} statement origin is not cleared")
    require(rights.get("source_wording_redistributed") is False, f"{label} redistributes source wording")
    require(rights.get("cleared_for_catalog_statement") is True, f"{label} catalog statement not cleared")
    attribution = rights.get("attribution")
    require(
        isinstance(attribution, list)
        and attribution
        and all(isinstance(item, str) and item.strip() == item and item for item in attribution),
        f"{label}.attribution malformed",
    )
    return rights


def verify_statement(value: Any, label: str) -> dict[str, Any]:
    statement = dict(closed(value, STATEMENT_KEYS, label))
    language = text(statement.get("language"), f"{label}.language")
    representation = text(statement.get("representation"), f"{label}.representation")
    body = text(statement.get("text"), f"{label}.text")
    wanted = digest(canonical({"language": language, "representation": representation, "text": body}))
    require(statement.get("statement_sha256") == wanted, f"{label}.statement_sha256 drifted")
    require(statement.get("independently_written") is True, f"{label} must be independently written")
    sources = statement.get("source_bindings")
    require(isinstance(sources, list) and sources, f"{label}.source_bindings empty")
    for index, source in enumerate(sources):
        verify_source_evidence(source, f"{label}.source_bindings[{index}]")
    return statement


def verify_proofs(value: Any, statement_sha: str, label: str) -> list[dict[str, Any]]:
    require(isinstance(value, list) and value, f"{label} is empty")
    proofs: list[dict[str, Any]] = []
    qualifying = 0
    for index, item in enumerate(value):
        proof = dict(closed(item, PROOF_KEYS, f"{label}[{index}]"))
        kind = proof.get("kind")
        require(kind in {"human_published_solution", "kernel_checked_formal_proof"}, f"{label}[{index}].kind invalid")
        require(proof.get("proof_state") == "proved", f"{label}[{index}] does not prove the claim")
        require(proof.get("uses_placeholder") is False, f"{label}[{index}] uses a proof placeholder")
        require(proof.get("reviewed") is True, f"{label}[{index}] is not reviewed")
        require(proof.get("applies_to_statement_sha256") == statement_sha, f"{label}[{index}] statement applicability drifted")
        summary = text(proof.get("proof_method_summary"), f"{label}[{index}].proof_method_summary")
        require(
            proof.get("proof_method_summary_sha256") == digest(summary.encode("utf-8"))
            and proof.get("independently_written_summary") is True,
            f"{label}[{index}] proof-method summary binding drifted",
        )
        verify_source_evidence(proof.get("source_binding"), f"{label}[{index}].source_binding")
        rights = proof.get("rights")
        require(
            isinstance(rights, dict)
            and rights.get("catalog_relicenses_source") is False
            and rights.get("proof_text_redistributed") is False
            and isinstance(rights.get("attribution"), list)
            and rights["attribution"],
            f"{label}[{index}].rights malformed",
        )
        qualifying += 1
        proofs.append(proof)
    require(qualifying > 0, f"{label} has no qualifying proof")
    return proofs


def expected_allocation_request(problem_key: str, target: Mapping[str, Any]) -> str:
    return digest(
        canonical(
            {
                "release": "5.6",
                "parent_release_root_sha256": PARENT_RELEASE_ROOT_SHA256,
                "problem_key": problem_key,
                "semantic_key": target["semantic_key"],
                "statement_sha256": target["statement"]["statement_sha256"],
                "claim_kind": target["claim_kind"],
                "material_status": target["material_status"],
            }
        )
    )


def verify_target(
    target: Any,
    problem_key: str,
    index: int,
    parent_by_stage: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    label = f"seed {problem_key}.targets[{index}]"
    result = dict(closed(target, TARGET_KEYS, label))
    semantic = text(result.get("semantic_key"), f"{label}.semantic_key")
    require(result.get("claim_kind") == "theorem" and result.get("material_status") == "proved", f"{label} is not a proved theorem")
    statement = verify_statement(result.get("statement"), f"{label}.statement")
    verify_proofs(result.get("proof_evidence"), statement["statement_sha256"], f"{label}.proof_evidence")
    verify_rights(result.get("rights"), f"{label}.rights")
    require(
        result.get("identity_action") == "noncatalog_benchmark_seed",
        f"{label} must remain a noncatalog benchmark seed",
    )
    require(
        result.get("stage_claim_id") is None
        and result.get("variant_id") is None
        and result.get("parent_catalog_record_sha256") is None
        and result.get("allocation_request_sha256") is None,
        f"{label} allocates or joins a catalog identity",
    )
    require(semantic == result["semantic_key"], f"{label} semantic key drifted")
    return result


def verify_review(value: Any, label: str, *, relation: bool = False) -> dict[str, Any]:
    keys = RELATION_REVIEW_KEYS if relation else SEED_REVIEW_KEYS
    review = dict(closed(value, keys, label))
    text(review.get("reviewer_id"), f"{label}.reviewer_id")
    text(review.get("reviewed_as_of"), f"{label}.reviewed_as_of", DATE_RE)
    if relation:
        require(review.get("manual_statement_review") is True and review.get("manual_relation_review") is True, f"{label} gates not passed")
    else:
        require(
            review.get("manual_statement_review") is True
            and review.get("manual_benchmark_proposition_review") is True,
            f"{label} gates not passed",
        )
    require(isinstance(review.get("notes"), str), f"{label}.notes malformed")
    return review


def verify_seed_crosswalk(
    problem_by_key: Mapping[str, Mapping[str, Any]],
    parent_by_stage: Mapping[str, Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, str]]:
    rows = load_jsonl(SEED_CROSSWALK, "PutnamBench seed crosswalk")
    require(len(rows) == 768, "seed crosswalk must contain exactly 768 full-grid rows")
    by_key: dict[str, dict[str, Any]] = {}
    direct_targets: dict[str, list[dict[str, Any]]] = {}
    aliases: dict[str, str] = {}
    seen_semantics: dict[str, str] = {}
    for index, row in enumerate(rows):
        verify_row(row, SEED_ROW_KEYS, f"seed crosswalk[{index}]")
        require(row.get("schema_version") == "awesome-theorems/putnambench-seed-crosswalk-row/5.6", f"seed crosswalk[{index}] schema drifted")
        key = text(row.get("problem_key"), f"seed crosswalk[{index}].problem_key", PROBLEM_RE)
        source = problem_by_key.get(key)
        require(source is not None and key not in by_key, f"seed crosswalk[{index}] unknown/duplicate key")
        require(row.get("source_problem_row_sha256") == source.get("row_sha256"), f"seed crosswalk {key} source row binding drifted")
        variants = row.get("formal_variant_ids")
        require(variants == source.get("formal_variant_ids"), f"seed crosswalk {key} formal variants drifted")
        disposition = row.get("disposition")
        require(disposition in SEED_DISPOSITIONS, f"seed crosswalk {key} has nonfinal/nonpublishable disposition")
        statement_review = dict(closed(row.get("statement_review"), STATEMENT_REVIEW_KEYS, f"seed {key}.statement_review"))
        require(all(value is True for value in statement_review.values()), f"seed {key} statement review gates not all true")
        verify_review(row.get("review"), f"seed {key}.review")
        target_values = row.get("targets")
        require(isinstance(target_values, list), f"seed {key}.targets malformed")
        require(row.get("alias_of_problem_key") is None, f"seed {key} aliases another coordinate")
        require(target_values, f"seed {key} has no reviewed benchmark proposition")
        normalized = [
            verify_target(value, key, rank, parent_by_stage)
            for rank, value in enumerate(target_values)
        ]
        for target in normalized:
            semantic = target["semantic_key"]
            require(semantic not in seen_semantics, f"seed {key} duplicates benchmark semantic target of {seen_semantics.get(semantic)}")
            seen_semantics[semantic] = key
        direct_targets[key] = normalized
        by_key[key] = row
    require(set(by_key) == set(problem_by_key), "seed crosswalk key set differs from frozen source universe")

    resolved = direct_targets
    require(len(resolved) == 768 and all(targets for targets in resolved.values()), "benchmark seed proposition projection drifted")
    return rows, resolved, aliases


def verify_formal_crosswalk(
    variant_by_id: Mapping[str, Mapping[str, Any]],
    problem_by_key: Mapping[str, Mapping[str, Any]],
    resolved_targets: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    rows = load_jsonl(FORMAL_CROSSWALK, "PutnamBench formal-variant crosswalk")
    require(len(rows) == 1_724, "formal-variant crosswalk must contain exactly 1,724 rows")
    by_id: dict[str, dict[str, Any]] = {}
    semantic_keys = {
        target["semantic_key"]
        for targets in resolved_targets.values()
        for target in targets
    }
    for index, row in enumerate(rows):
        verify_row(row, FORMAL_ROW_KEYS, f"formal crosswalk[{index}]")
        require(row.get("schema_version") == "awesome-theorems/putnambench-formal-crosswalk-row/5.6", f"formal crosswalk[{index}] schema drifted")
        variant_id = text(row.get("variant_id"), f"formal crosswalk[{index}].variant_id")
        source = variant_by_id.get(variant_id)
        require(source is not None and variant_id not in by_id, f"formal crosswalk[{index}] unknown/duplicate variant")
        require(row.get("source_variant_row_sha256") == source.get("row_sha256"), f"formal crosswalk {variant_id} source binding drifted")
        source_problem = text(row.get("source_problem_key"), f"formal crosswalk {variant_id}.source_problem_key", PROBLEM_RE)
        semantic_problem = text(row.get("semantic_problem_key"), f"formal crosswalk {variant_id}.semantic_problem_key", PROBLEM_RE)
        require(source_problem == source.get("problem_key") and semantic_problem in problem_by_key, f"formal crosswalk {variant_id} problem mapping invalid")
        disposition = row.get("disposition")
        require(disposition in FORMAL_DISPOSITIONS, f"formal crosswalk {variant_id} disposition invalid")
        targets = row.get("target_semantic_keys")
        require(isinstance(targets, list) and len(targets) == len(set(targets)), f"formal crosswalk {variant_id} target set malformed")
        if disposition == "malformed_or_nonclaim_variant":
            require(not targets, f"malformed formal variant {variant_id} targets a theorem")
        else:
            require(targets and all(item in semantic_keys for item in targets), f"formal crosswalk {variant_id} targets unknown semantics")
            wanted = {target["semantic_key"] for target in resolved_targets[semantic_problem]}
            require(set(targets) <= wanted, f"formal crosswalk {variant_id} target is not a target of semantic problem {semantic_problem}")
        equivalence = dict(closed(row.get("statement_equivalence"), FORMAL_EQUIVALENCE_KEYS, f"formal crosswalk {variant_id}.statement_equivalence"))
        require(equivalence.get("reviewed") is True and isinstance(equivalence.get("notes"), str), f"formal crosswalk {variant_id} was not reviewed")
        if disposition == "same_exact_claim_variant":
            require(
                equivalence.get("exact_statement_scope") is True
                and equivalence.get("assumptions_preserved") is True
                and equivalence.get("conclusion_preserved") is True,
                f"formal crosswalk {variant_id} exact-equivalence gates failed",
            )
        review = dict(closed(row.get("review"), FORMAL_REVIEW_KEYS, f"formal crosswalk {variant_id}.review"))
        text(review.get("reviewer_id"), f"formal crosswalk {variant_id}.review.reviewer_id")
        text(review.get("reviewed_as_of"), f"formal crosswalk {variant_id}.review.reviewed_as_of", DATE_RE)
        require(
            review.get("manual_statement_review") is True
            and review.get("manual_formal_variant_semantic_review") is True
            and review.get("manual_filename_declaration_anomaly_review") is True,
            f"formal crosswalk {variant_id} review gates not passed",
        )
        require(isinstance(review.get("notes"), str), f"formal crosswalk {variant_id}.review.notes malformed")
        by_id[variant_id] = row
    require(set(by_id) == set(variant_by_id), "formal-variant crosswalk set differs from frozen 1,724-row universe")
    return rows


def verify_relation_universe(
    problem_keys: set[str],
    pb_source_inventory_authority: str,
    full_source_inventory_authority: str,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, dict[str, Any]], set[str]]:
    document = load_json(RELATION_UNIVERSE, "PutnamBench relation-source universe")
    verify_seal(document, "PutnamBench relation-source universe")
    expected_keys = {
        "schema_version", "parent_release", "putnambench_source_inventory_authority_sha256",
        "full_putnam_source_inventory_authority_sha256",
        "completeness_boundary", "sources", "obligations", "counts", "set_digests",
        "authority_sha256",
    }
    closed(document, expected_keys, "relation-source universe")
    require(document.get("schema_version") == "awesome-theorems/putnambench-relation-source-universe/5.6", "relation-source universe schema drifted")
    parent = document.get("parent_release")
    require(
        isinstance(parent, dict)
        and parent.get("release") == "5.5"
        and parent.get("release_root_sha256") == PARENT_RELEASE_ROOT_SHA256,
        "relation-source universe parent drifted",
    )
    require(document.get("putnambench_source_inventory_authority_sha256") == pb_source_inventory_authority, "relation-source universe PB source authority drifted")
    require(document.get("full_putnam_source_inventory_authority_sha256") == full_source_inventory_authority, "relation-source universe full source authority drifted")
    boundary = document.get("completeness_boundary")
    require(
        isinstance(boundary, dict)
        and boundary.get("claim") == "complete_relative_to_frozen_sources_and_candidate_occurrences"
        and boundary.get("global_literature_completeness_claimed") is False
        and boundary.get("one_hop_only") is True
        and boundary.get("topic_or_import_edges_forbidden") is True,
        "relation-source completeness boundary malformed",
    )
    sources = document.get("sources")
    obligations = document.get("obligations")
    require(isinstance(sources, list) and sources, "relation-source universe has no sources")
    require(isinstance(obligations, list) and obligations, "relation-source universe has no obligations")
    source_by_id: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(sources):
        verify_row(row, RELATION_SOURCE_KEYS, f"relation source[{index}]")
        source_id = text(row.get("source_id"), f"relation source[{index}].source_id")
        require(source_id not in source_by_id, f"duplicate relation source {source_id}")
        path_text = text(row.get("path"), f"relation source {source_id}.path")
        require(not path_text.startswith("/") and ".." not in Path(path_text).parts, f"relation source {source_id} path unsafe")
        path = safe_file(REPO_ROOT / path_text, f"relation source {source_id}.path")
        require(row.get("file_sha256") == sha_file(path) and row.get("size_bytes") == path.stat().st_size, f"relation source {source_id} bytes drifted")
        require(isinstance(row.get("rights"), dict) and row["rights"].get("catalog_relicenses_source") is False, f"relation source {source_id} rights malformed")
        require(isinstance(row.get("scope"), dict) and row["scope"], f"relation source {source_id} scope malformed")
        source_by_id[source_id] = row
    obligation_by_id: dict[str, dict[str, Any]] = {}
    candidate_keys: set[str] = set()
    covered_problem_keys: set[str] = set()
    for index, row in enumerate(obligations):
        verify_row(row, RELATION_OBLIGATION_KEYS, f"relation obligation[{index}]")
        obligation_id = text(row.get("obligation_id"), f"relation obligation[{index}].obligation_id")
        problem_key = text(row.get("problem_key"), f"relation obligation {obligation_id}.problem_key", PROBLEM_RE)
        source_id = text(row.get("source_id"), f"relation obligation {obligation_id}.source_id")
        require(obligation_id not in obligation_by_id and problem_key in problem_keys and source_id in source_by_id, f"relation obligation {obligation_id} identity invalid")
        require(row.get("discovery_method") in {
            "full_official_solution_review", "exact_relation_section_scan",
            "formal_declaration_reference_scan", "bibliography_relation_scan",
        }, f"relation obligation {obligation_id} discovery method invalid")
        require(isinstance(row.get("source_scope"), dict) and row["source_scope"], f"relation obligation {obligation_id} scope malformed")
        keys = row.get("candidate_keys")
        require(isinstance(keys, list) and len(keys) == len(set(keys)), f"relation obligation {obligation_id} candidate keys malformed")
        require(not (candidate_keys & set(keys)), f"relation candidate key appears in multiple obligations: {obligation_id}")
        candidate_keys.update(keys)
        zero = row.get("zero_candidate_finding")
        if keys:
            require(zero is None, f"nonempty relation obligation {obligation_id} has zero finding")
        else:
            require(
                isinstance(zero, dict)
                and zero.get("full_scope_reviewed") is True
                and isinstance(zero.get("reviewer_id"), str)
                and bool(zero["reviewer_id"]),
                f"zero-candidate relation obligation {obligation_id} lacks reviewed finding",
            )
        covered_problem_keys.add(problem_key)
        obligation_by_id[obligation_id] = row
    require(covered_problem_keys == problem_keys, "relation-source obligations do not cover every Putnam seed key")
    require(set(source_by_id) == {row["source_id"] for row in obligations}, "relation-source universe contains an unused source")
    counts = document.get("counts")
    require(
        isinstance(counts, dict)
        and counts.get("sources") == len(sources)
        and counts.get("obligations") == len(obligations)
        and counts.get("covered_problem_keys") == 768
        and counts.get("candidate_occurrences") == len(candidate_keys),
        "relation-source universe counts drifted",
    )
    digests = document.get("set_digests")
    require(
        isinstance(digests, dict)
        and digests.get("source_id_set_sha256") == set_digest(source_by_id)
        and digests.get("obligation_id_set_sha256") == set_digest(obligation_by_id)
        and digests.get("candidate_key_set_sha256") == set_digest(candidate_keys),
        "relation-source universe set digests drifted",
    )
    return document, source_by_id, obligation_by_id, candidate_keys


def expected_node_id(semantic_key: str) -> str:
    return "PBN-" + digest(semantic_key.encode("utf-8"))[:32].upper()


def expected_node_allocation(node: Mapping[str, Any]) -> str:
    return digest(
        canonical(
            {
                "release": "5.6",
                "parent_release_root_sha256": PARENT_RELEASE_ROOT_SHA256,
                "node_id": node["node_id"],
                "semantic_key": node["semantic_key"],
                "statement_sha256": node["statement"]["statement_sha256"],
                "claim_kind": node["claim_kind"],
                "material_status": node["material_status"],
                "distance": node["distance"],
            }
        )
    )


def verify_status_evidence(value: Any, claim_kind: str, material_status: str, label: str) -> dict[str, Any]:
    status = dict(closed(value, STATUS_EVIDENCE_KEYS, label))
    require(status.get("status") == material_status, f"{label}.status drifted")
    text(status.get("as_of"), f"{label}.as_of", DATE_RE)
    require(status.get("independently_reviewed") is True, f"{label} is not independently reviewed")
    sources = status.get("source_bindings")
    require(isinstance(sources, list) and sources, f"{label}.source_bindings empty")
    for index, source in enumerate(sources):
        verify_source_evidence(source, f"{label}.source_bindings[{index}]")
    require(isinstance(status.get("notes"), str), f"{label}.notes malformed")
    if claim_kind == "theorem":
        require(material_status == "proved", f"{label} theorem is not proved")
    else:
        require(material_status in {"open", "partial", "independent", "disputed"}, f"{label} open-claim status invalid")
    return status


def verify_closure_nodes(
    resolved_targets: Mapping[str, Sequence[Mapping[str, Any]]],
    parent_by_stage: Mapping[str, Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, set[str]], dict[str, Mapping[str, Any]]]:
    rows = load_jsonl(CLOSURE_NODES, "Putnam one-hop closure nodes")
    require(rows, "closure-node ledger is empty")
    target_by_semantic: dict[str, Mapping[str, Any]] = {}
    seed_keys_by_semantic: dict[str, set[str]] = defaultdict(set)
    for problem_key, targets in resolved_targets.items():
        for target in targets:
            semantic = str(target["semantic_key"])
            prior = target_by_semantic.get(semantic)
            if prior is not None:
                require(prior == target, f"seed semantic {semantic} has inconsistent target payloads")
            target_by_semantic[semantic] = target
            seed_keys_by_semantic[semantic].add(problem_key)
    by_id: dict[str, dict[str, Any]] = {}
    semantics: set[str] = set()
    distance_zero_semantics: set[str] = set()
    for index, row in enumerate(rows):
        verify_row(row, NODE_KEYS, f"closure node[{index}]")
        require(row.get("schema_version") == "awesome-theorems/putnam-onehop-closure-node/5.6", f"closure node[{index}] schema drifted")
        semantic = text(row.get("semantic_key"), f"closure node[{index}].semantic_key")
        node_id = text(row.get("node_id"), f"closure node[{index}].node_id")
        require(node_id == expected_node_id(semantic), f"closure node {node_id} ID drifted")
        require(node_id not in by_id and semantic not in semantics, f"duplicate closure node/semantic: {node_id}")
        distance = integer(row.get("distance"), f"closure node {node_id}.distance")
        require(distance in {0, 1}, f"closure node {node_id} is outside one hop")
        seeds = row.get("seed_problem_keys")
        require(
            isinstance(seeds, list)
            and seeds == sorted(set(seeds))
            and seeds
            and all(PROBLEM_RE.fullmatch(item) for item in seeds),
            f"closure node {node_id}.seed_problem_keys malformed",
        )
        kind = row.get("claim_kind")
        material = row.get("material_status")
        require(kind in CLAIM_KINDS, f"closure node {node_id}.claim_kind invalid")
        if kind == "theorem":
            require(material == "proved", f"closure theorem {node_id} is not proved")
        else:
            require(material in {"open", "partial", "independent", "disputed"}, f"closure open node {node_id} status invalid")
        statement = verify_statement(row.get("statement"), f"closure node {node_id}.statement")
        verify_status_evidence(row.get("status_evidence"), str(kind), str(material), f"closure node {node_id}.status_evidence")
        proofs = row.get("proof_evidence")
        if kind == "theorem":
            verify_proofs(proofs, statement["statement_sha256"], f"closure node {node_id}.proof_evidence")
        else:
            require(proofs == [], f"closure open node {node_id} carries theorem proof evidence")
        verify_rights(row.get("rights"), f"closure node {node_id}.rights")
        source_bindings = row.get("source_bindings")
        require(isinstance(source_bindings, list) and source_bindings, f"closure node {node_id}.source_bindings empty")
        for source_index, source in enumerate(source_bindings):
            verify_source_evidence(source, f"closure node {node_id}.source_bindings[{source_index}]")
        incoming = row.get("incoming_edge_ids")
        require(isinstance(incoming, list) and incoming == sorted(set(incoming)), f"closure node {node_id}.incoming_edge_ids malformed")
        action = row.get("catalog_action")
        require(
            action in {"noncatalog_benchmark_seed", "existing_parent", "allocate_5_6"},
            f"closure node {node_id}.catalog_action invalid",
        )
        if action == "noncatalog_benchmark_seed":
            require(distance == 0, f"distance-one closure node {node_id} cannot use benchmark-seed action")
            require(
                row.get("stage_claim_id") is None
                and row.get("variant_id") is None
                and row.get("parent_catalog_record_sha256") is None
                and row.get("allocation_request_sha256") is None,
                f"benchmark seed node {node_id} allocates or joins a catalog identity",
            )
        elif action == "existing_parent":
            sid = text(row.get("stage_claim_id"), f"closure node {node_id}.stage_claim_id", S5_RE)
            atv = text(row.get("variant_id"), f"closure node {node_id}.variant_id", ATV_RE)
            parent = parent_by_stage.get(sid)
            require(parent is not None and parent.get("variant_id") == atv, f"closure node {node_id} parent identity invalid")
            require(row.get("parent_catalog_record_sha256") == digest(canonical(parent)), f"closure node {node_id} parent row binding drifted")
            require(row.get("allocation_request_sha256") is None, f"closure node {node_id} existing identity has allocation request")
        else:
            require(distance == 1, f"benchmark seed node {node_id} cannot allocate a catalog identity")
            require(row.get("stage_claim_id") is None and row.get("variant_id") is None and row.get("parent_catalog_record_sha256") is None, f"closure node {node_id} preallocates/binds IDs")
            require(row.get("allocation_request_sha256") == expected_node_allocation(row), f"closure node {node_id} allocation request drifted")
        if distance == 0:
            target = target_by_semantic.get(semantic)
            require(target is not None, f"distance-zero node {node_id} is not a seed target")
            require(set(seeds) == seed_keys_by_semantic[semantic], f"distance-zero node {node_id} seed membership drifted")
            require(row.get("catalog_action") == target.get("identity_action"), f"distance-zero node {node_id} identity action drifted")
            for field in (
                "claim_kind", "material_status", "stage_claim_id", "variant_id",
                "parent_catalog_record_sha256", "allocation_request_sha256",
                "statement", "proof_evidence", "rights",
            ):
                require(row.get(field) == target.get(field), f"distance-zero node {node_id}.{field} differs from seed target")
            distance_zero_semantics.add(semantic)
        by_id[node_id] = row
        semantics.add(semantic)
    require(distance_zero_semantics == set(target_by_semantic), "closure distance-zero nodes do not exactly cover reviewed benchmark-seed propositions")
    return rows, by_id, seed_keys_by_semantic, target_by_semantic


def verify_relation_candidates(
    wanted_candidate_keys: set[str],
    obligation_by_id: Mapping[str, Mapping[str, Any]],
    node_by_id: Mapping[str, Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows = load_jsonl(RELATION_CANDIDATES, "Putnam relation-candidate ledger")
    require(len(rows) == len(wanted_candidate_keys), "relation-candidate ledger denominator differs from frozen universe")
    by_key: dict[str, dict[str, Any]] = {}
    edge_ids: set[str] = set()
    for index, row in enumerate(rows):
        verify_row(row, RELATION_CANDIDATE_KEYS, f"relation candidate[{index}]")
        require(row.get("schema_version") == "awesome-theorems/putnam-onehop-relation-candidate/5.6", f"relation candidate[{index}] schema drifted")
        key = text(row.get("candidate_key"), f"relation candidate[{index}].candidate_key")
        obligation_id = text(row.get("obligation_id"), f"relation candidate {key}.obligation_id")
        obligation = obligation_by_id.get(obligation_id)
        require(obligation is not None and key in obligation["candidate_keys"] and key not in by_key, f"relation candidate {key} obligation/identity invalid")
        require(row.get("problem_key") == obligation.get("problem_key"), f"relation candidate {key} seed key drifted")
        target = dict(closed(row.get("target_candidate"), TARGET_CANDIDATE_KEYS, f"relation candidate {key}.target_candidate"))
        text(target.get("label"), f"relation candidate {key}.target_candidate.label")
        require(target.get("kind") in {"claim", "topic", "method", "definition", "person", "historical_event"}, f"relation candidate {key} target kind invalid")
        if target.get("statement_sha256") is not None:
            text(target["statement_sha256"], f"relation candidate {key}.target_candidate.statement_sha256", SHA_RE)
        verify_source_evidence(target.get("source_binding"), f"relation candidate {key}.target_candidate.source_binding")
        disposition = row.get("disposition")
        proposed = row.get("proposed_relation_type")
        require(proposed is None or proposed in RELATION_TYPES, f"relation candidate {key} proposed type invalid")
        if disposition == "accepted_edge":
            require(proposed in RELATION_TYPES and target.get("kind") == "claim" and target.get("statement_sha256") is not None, f"accepted relation candidate {key} is not a proposition-level relation")
            node_id = text(row.get("target_node_id"), f"relation candidate {key}.target_node_id")
            edge_id = text(row.get("edge_id"), f"relation candidate {key}.edge_id")
            node = node_by_id.get(node_id)
            require(node is not None and node["statement"]["statement_sha256"] == target["statement_sha256"], f"accepted relation candidate {key} target-node binding drifted")
            require(edge_id not in edge_ids, f"duplicate accepted edge ID {edge_id}")
            edge_ids.add(edge_id)
            require(row.get("reason_code") == "reviewed_direct_proposition_relation", f"accepted relation candidate {key} reason invalid")
        else:
            require(disposition in REJECTED_RELATION_DISPOSITIONS, f"relation candidate {key} is pending/unknown")
            require(row.get("target_node_id") is None and row.get("edge_id") is None, f"rejected relation candidate {key} targets accepted graph")
            text(row.get("reason_code"), f"relation candidate {key}.reason_code")
        verify_review(row.get("review"), f"relation candidate {key}.review", relation=True)
        by_key[key] = row
    require(set(by_key) == wanted_candidate_keys, "relation-candidate ledger set differs from frozen universe")
    return rows, by_key


def verify_relation_evidence(
    value: Any,
    relation_type: str,
    relation_sources: Mapping[str, Mapping[str, Any]],
    label: str,
) -> dict[str, Any]:
    evidence = dict(closed(value, RELATION_EVIDENCE_KEYS, label))
    source_id = text(evidence.get("source_id"), f"{label}.source_id")
    source = relation_sources.get(source_id)
    require(source is not None, f"{label} uses an unpinned relation source")
    require(evidence.get("path") == source.get("path") and evidence.get("file_sha256") == source.get("file_sha256"), f"{label} source binding drifted")
    require(isinstance(evidence.get("locator"), dict) and evidence["locator"], f"{label}.locator malformed")
    text(evidence.get("relation_evidence_sha256"), f"{label}.relation_evidence_sha256", SHA_RE)
    text(evidence.get("rights_id"), f"{label}.rights_id")
    text(evidence.get("relation_assertion"), f"{label}.relation_assertion")
    require(
        evidence.get("relation_assertion_origin") == "independently_written_reviewed_summary"
        and evidence.get("source_wording_redistributed") is False,
        f"{label} violates relation-summary rights boundary",
    )
    proof_step = evidence.get("proof_step_binding")
    if relation_type in {"direct_prerequisite", "standard_solution_uses"}:
        require(isinstance(proof_step, dict) and proof_step, f"{label} lacks exact proof-step/declaration-use binding")
        require(
            proof_step.get("use_verified") is True
            and proof_step.get("import_or_topic_only") is False
            and isinstance(proof_step.get("locator"), dict)
            and proof_step["locator"],
            f"{label} proof-step binding malformed",
        )
    else:
        require(proof_step is None or isinstance(proof_step, dict), f"{label}.proof_step_binding malformed")
    return evidence


def verify_relation_edges(
    candidates_by_key: Mapping[str, Mapping[str, Any]],
    node_by_id: Mapping[str, Mapping[str, Any]],
    relation_sources: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows = load_jsonl(RELATION_EDGES, "Putnam relation-edge ledger")
    accepted = {
        key: row for key, row in candidates_by_key.items()
        if row.get("disposition") == "accepted_edge"
    }
    require(len(rows) == len(accepted), "relation-edge ledger count differs from accepted candidates")
    by_id: dict[str, dict[str, Any]] = {}
    by_candidate: dict[str, dict[str, Any]] = {}
    triples: set[tuple[str, str, str]] = set()
    incoming_by_node: dict[str, set[str]] = defaultdict(set)
    incoming_seed_keys_by_node: dict[str, set[str]] = defaultdict(set)
    covered_seed_keys: set[str] = set()
    for index, row in enumerate(rows):
        verify_row(row, EDGE_KEYS, f"relation edge[{index}]")
        require(row.get("schema_version") == "awesome-theorems/putnam-onehop-relation-edge/5.6", f"relation edge[{index}] schema drifted")
        edge_id = text(row.get("edge_id"), f"relation edge[{index}].edge_id")
        candidate_key = text(row.get("candidate_key"), f"relation edge {edge_id}.candidate_key")
        candidate = accepted.get(candidate_key)
        require(candidate is not None and edge_id == candidate.get("edge_id"), f"relation edge {edge_id} candidate binding invalid")
        require(edge_id not in by_id and candidate_key not in by_candidate, f"duplicate relation edge/candidate: {edge_id}")
        seed_key = text(row.get("seed_problem_key"), f"relation edge {edge_id}.seed_problem_key", PROBLEM_RE)
        require(seed_key == candidate.get("problem_key"), f"relation edge {edge_id} seed binding drifted")
        from_id = text(row.get("from_node_id"), f"relation edge {edge_id}.from_node_id")
        to_id = text(row.get("to_node_id"), f"relation edge {edge_id}.to_node_id")
        source_node = node_by_id.get(from_id)
        target_node = node_by_id.get(to_id)
        require(source_node is not None and target_node is not None and from_id != to_id, f"relation edge {edge_id} endpoint invalid")
        require(source_node.get("distance") == 0 and seed_key in source_node.get("seed_problem_keys", []), f"relation edge {edge_id} does not originate at its benchmark seed proposition")
        require(target_node.get("distance") in {0, 1}, f"relation edge {edge_id} target lies outside one hop")
        require(to_id == candidate.get("target_node_id"), f"relation edge {edge_id} target/candidate drifted")
        relation_type = row.get("relation_type")
        require(relation_type in RELATION_TYPES and relation_type == candidate.get("proposed_relation_type"), f"relation edge {edge_id} type drifted")
        directness = dict(closed(row.get("directness"), DIRECTNESS_KEYS, f"relation edge {edge_id}.directness"))
        require(
            directness.get("proposition_level") is True
            and directness.get("direct_relation_verified") is True
            and all(directness.get(flag) is False for flag in (
                "topic_only", "tag_only", "import_only", "cooccurrence_only",
                "name_only", "nonclaim_endpoint",
            )),
            f"relation edge {edge_id} admits a topic/import/nonclaim pseudo-edge",
        )
        verify_relation_evidence(row.get("evidence"), str(relation_type), relation_sources, f"relation edge {edge_id}.evidence")
        verify_review(row.get("review"), f"relation edge {edge_id}.review", relation=True)
        triple = (from_id, to_id, str(relation_type))
        require(triple not in triples, f"duplicate proposition relation edge: {triple}")
        triples.add(triple)
        incoming_by_node[to_id].add(edge_id)
        incoming_seed_keys_by_node[to_id].add(seed_key)
        covered_seed_keys.add(seed_key)
        by_id[edge_id] = row
        by_candidate[candidate_key] = row
    require(set(by_candidate) == set(accepted), "accepted relation candidates and edge ledger differ")
    require(
        covered_seed_keys == full_grid_keys(),
        f"accepted proposition-level relation edges miss full-grid seeds: {sorted(full_grid_keys() - covered_seed_keys)}",
    )
    for node_id, node in node_by_id.items():
        expected = sorted(incoming_by_node.get(node_id, set()))
        if node.get("distance") == 1:
            require(expected, f"distance-one closure node {node_id} is orphaned")
            require(
                node.get("seed_problem_keys") == sorted(incoming_seed_keys_by_node.get(node_id, set())),
                f"distance-one closure node {node_id} seed projection drifted",
            )
        require(node.get("incoming_edge_ids") == expected, f"closure node {node_id} incoming-edge projection drifted")
    return rows


def document_binding(path: Path, document: Mapping[str, Any]) -> dict[str, Any]:
    payload = encoded(document)
    return {
        "path": relative(path),
        "file_sha256": digest(payload),
        "size_bytes": len(payload),
        "authority_sha256": document["authority_sha256"],
    }


def build_receipts(
    parent_manifest: Mapping[str, Any],
    pb_inventory: Mapping[str, Any],
    pb_problems: Sequence[Mapping[str, Any]],
    pb_variants: Sequence[Mapping[str, Any]],
    full_inventory: Mapping[str, Any],
    full_candidates: Sequence[Mapping[str, Any]],
    full_problems: Sequence[Mapping[str, Any]],
    seed_rows: Sequence[Mapping[str, Any]],
    resolved_targets: Mapping[str, Sequence[Mapping[str, Any]]],
    formal_rows: Sequence[Mapping[str, Any]],
    relation_universe: Mapping[str, Any],
    candidate_rows: Sequence[Mapping[str, Any]],
    node_rows: Sequence[Mapping[str, Any]],
    edge_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    pb_keys = {str(row["problem_key"]) for row in pb_problems}
    full_keys = {str(row["problem_key"]) for row in full_problems}
    supplemental_keys = full_keys - pb_keys
    seed_by_key = {str(row["problem_key"]): row for row in seed_rows}
    seed_counts = Counter(str(row["disposition"]) for row in seed_rows)
    pb_seed_counts = Counter(str(seed_by_key[key]["disposition"]) for key in pb_keys)
    require(
        seed_counts == Counter({"reviewed_noncatalog_benchmark_seed": 768})
        and pb_seed_counts == Counter({"reviewed_noncatalog_benchmark_seed": 675}),
        "benchmark seed disposition equations do not close at 768/675",
    )
    formal_counts = Counter(str(row["disposition"]) for row in formal_rows)
    formal_language_counts = Counter(str(row["language"]) for row in pb_variants)
    distinct_seed_semantics = {
        str(target["semantic_key"])
        for targets in resolved_targets.values()
        for target in targets
    }
    require(len(distinct_seed_semantics) >= 768, "reviewed benchmark proposition denominator is below the 768 seed rows")
    nodes_by_distance = Counter(int(row["distance"]) for row in node_rows)
    nodes_by_kind = Counter(str(row["claim_kind"]) for row in node_rows)
    catalog_nodes_by_kind = Counter(
        str(row["claim_kind"])
        for row in node_rows
        if row.get("catalog_action") != "noncatalog_benchmark_seed"
    )
    benchmark_seed_nodes = [row for row in node_rows if row.get("catalog_action") == "noncatalog_benchmark_seed"]
    new_nodes = [row for row in node_rows if row.get("catalog_action") == "allocate_5_6"]
    existing_nodes = [row for row in node_rows if row.get("catalog_action") == "existing_parent"]
    require(
        len(benchmark_seed_nodes) == len(distinct_seed_semantics)
        and len(benchmark_seed_nodes) >= 768
        and all(row.get("distance") == 0 for row in benchmark_seed_nodes),
        "reviewed benchmark propositions are not exactly the zero-credit distance-zero node set",
    )
    new_theorems = [row for row in new_nodes if row.get("claim_kind") == "theorem"]
    new_seed_theorems = [row for row in new_theorems if row.get("distance") == 0]
    new_closure_theorems = [row for row in new_theorems if row.get("distance") == 1]
    require(
        len(new_seed_theorems) + len(new_closure_theorems) == len(new_theorems),
        "new Putnam theorem nodes are not partitioned by distance",
    )
    require(not new_seed_theorems, "benchmark seed propositions received theorem catalog credit")
    new_open = [row for row in new_nodes if row.get("claim_kind") in OPEN_KINDS]
    new_strict = [row for row in new_nodes if row.get("claim_kind") == "conjecture"]
    relation_candidate_counts = Counter(str(row["disposition"]) for row in candidate_rows)
    edge_type_counts = Counter(str(row["relation_type"]) for row in edge_rows)
    require(
        set(edge_type_counts) == RELATION_TYPES
        and all(edge_type_counts[relation_type] > 0 for relation_type in RELATION_TYPES),
        "accepted one-hop edges do not cover every required relation type",
    )

    coverage_counts = {
        "full_grid_problem_keys": 768,
        "putnambench_subset_problem_keys": 675,
        "supplemental_problem_keys": 93,
        "putnambench_formal_variants": 1_724,
        "formal_variants_by_language": dict(sorted(formal_language_counts.items())),
        "seed_dispositions": dict(sorted(seed_counts.items())),
        "putnambench_subset_seed_dispositions": dict(sorted(pb_seed_counts.items())),
        "formal_variant_dispositions": dict(sorted(formal_counts.items())),
        "distinct_reviewed_benchmark_seed_propositions": len(distinct_seed_semantics),
        "benchmark_seed_theorem_catalog_credits": 0,
        "uncovered_full_grid_seed_keys": 0,
        "uncovered_putnambench_seed_keys": 0,
        "uncovered_formal_variants": 0,
        "pending_or_unreviewed_seed_rows": 0,
        "pending_or_unreviewed_formal_rows": 0,
    }
    coverage = seal(
        {
            "schema_version": "awesome-theorems/putnambench-intake-coverage-receipt/5.6",
            "release": "5.6",
            "parent_release": {
                "release": "5.5",
                "release_root_sha256": PARENT_RELEASE_ROOT_SHA256,
                "manifest_authority_sha256": parent_manifest["authority_sha256"],
            },
            "source_authorities": {
                "putnambench": pb_inventory["authority_sha256"],
                "full_putnam_grid": full_inventory["authority_sha256"],
            },
            "inputs": {
                "putnambench_source_inventory": binding(SOURCE_INVENTORY),
                "putnambench_source_problems": binding(SOURCE_PROBLEMS, rows=pb_problems),
                "putnambench_formal_variants": binding(FORMAL_VARIANTS, rows=pb_variants),
                "putnambench_formal_declaration_asset": binding(FORMAL_DECLARATION_ASSET),
                "full_putnam_source_inventory": binding(FULL_SOURCE_INVENTORY),
                "full_putnam_source_candidates": binding(FULL_SOURCE_CANDIDATES, rows=full_candidates),
                "full_putnam_source_problems": binding(FULL_SOURCE_PROBLEMS, rows=full_problems),
                "seed_crosswalk": binding(SEED_CROSSWALK, rows=seed_rows),
                "formal_variant_crosswalk": binding(FORMAL_CROSSWALK, rows=formal_rows),
            },
            "counts": coverage_counts,
            "set_digests": {
                "full_grid_problem_key_set_sha256": set_digest(full_keys),
                "putnambench_problem_key_set_sha256": set_digest(pb_keys),
                "supplemental_problem_key_set_sha256": set_digest(supplemental_keys),
                "putnambench_formal_variant_id_set_sha256": set_digest(str(row["variant_id"]) for row in pb_variants),
                "resolved_seed_semantic_key_set_sha256": set_digest(distinct_seed_semantics),
            },
            "findings": [],
        }
    )

    relation = seal(
        {
            "schema_version": "awesome-theorems/putnam-onehop-closure-receipt/5.6",
            "release": "5.6",
            "parent_release_root_sha256": PARENT_RELEASE_ROOT_SHA256,
            "source_universe_authority_sha256": relation_universe["authority_sha256"],
            "inputs": {
                "relation_source_universe": binding(RELATION_UNIVERSE),
                "relation_candidates": binding(RELATION_CANDIDATES, rows=candidate_rows),
                "closure_nodes": binding(CLOSURE_NODES, rows=node_rows),
                "relation_edges": binding(RELATION_EDGES, rows=edge_rows),
            },
            "completeness_boundary": copy.deepcopy(relation_universe["completeness_boundary"]),
            "counts": {
                "covered_seed_problem_keys": 768,
                "candidate_occurrences": len(candidate_rows),
                "candidate_dispositions": dict(sorted(relation_candidate_counts.items())),
                "accepted_relation_edges": len(edge_rows),
                "accepted_edge_seed_coverage": len({str(row["seed_problem_key"]) for row in edge_rows}),
                "missing_accepted_edge_seed_keys": 0,
                "accepted_edges_by_type": dict(sorted(edge_type_counts.items())),
                "closure_nodes": len(node_rows),
                "distance_zero_nodes": nodes_by_distance[0],
                "distance_one_nodes": nodes_by_distance[1],
                "nodes_by_claim_kind": dict(sorted(nodes_by_kind.items())),
                "catalog_identity_nodes_by_claim_kind": dict(sorted(catalog_nodes_by_kind.items())),
                "reviewed_noncatalog_benchmark_seed_nodes": len(benchmark_seed_nodes),
                "benchmark_seed_catalog_credits": 0,
                "existing_parent_identity_nodes": len(existing_nodes),
                "new_closure_theorem_identity_nodes": len(new_theorems),
                "new_closure_open_identity_nodes": len(new_open),
                "new_closure_strict_conjecture_identity_nodes": len(new_strict),
                "unreviewed_relation_candidates": 0,
                "orphan_distance_one_nodes": 0,
                "topic_or_import_only_accepted_edges": 0,
                "outside_one_hop_nodes": 0,
            },
            "set_digests": {
                "candidate_key_set_sha256": set_digest(str(row["candidate_key"]) for row in candidate_rows),
                "closure_node_id_set_sha256": set_digest(str(row["node_id"]) for row in node_rows),
                "relation_edge_id_set_sha256": set_digest(str(row["edge_id"]) for row in edge_rows),
            },
            "findings": [],
        }
    )

    qualification = seal(
        {
            "schema_version": "awesome-theorems/putnambench-intake-qualification/5.6",
            "release": "5.6",
            "parent_release": {
                "release": "5.5",
                "release_root_sha256": PARENT_RELEASE_ROOT_SHA256,
                "manifest_file_sha256": PARENT_MANIFEST_SHA256,
                "catalog_file_sha256": PARENT_CATALOG_SHA256,
                "theorem_file_sha256": PARENT_THEOREM_SHA256,
                "strict_ledger_file_sha256": PARENT_STRICT_SHA256,
            },
            "coverage_receipt": document_binding(COVERAGE_RECEIPT, coverage),
            "relation_closure_receipt": document_binding(RELATION_RECEIPT, relation),
            "qualified_new_identity_counts": {
                "theorems": len(new_theorems),
                "reviewed_noncatalog_benchmark_seed_propositions": len(benchmark_seed_nodes),
                "new_putnam_seed_theorems": 0,
                "new_putnam_closure_theorems": len(new_closure_theorems),
                "new_mathlib_verified_reserve_theorems": None,
                "strict_conjectures": len(new_strict),
                "other_open_claims": len(new_open) - len(new_strict),
                "all_new_claim_identities": len(new_nodes),
                "existing_parent_identity_joins": len(existing_nodes),
            },
            "expected_release_counts": {
                "numeric_release_total_ready": False,
                "unresolved_operand": "new_mathlib_verified_reserve_theorems",
                "catalog_records_without_mathlib_reserve": 4_525 + len(new_nodes),
                "theorems_without_mathlib_reserve": 2_500 + len(new_theorems),
                "catalog_records_formula": "4525 + all_new_claim_identities + new_mathlib_verified_reserve_theorems",
                "theorems_formula": "2500 + new_putnam_closure_theorems + new_mathlib_verified_reserve_theorems",
                "open_claims": 2_025 + len(new_open),
                "strict_conjecture_credits": 1_425 + len(new_strict),
            },
            "release_gates": {
                "parent_5_5_prefix_required": True,
                "full_grid_768_covered": True,
                "putnambench_subset_675_covered": True,
                "putnambench_formal_variants_1724_covered": True,
                "benchmark_seed_catalog_credit_zero": True,
                "relation_candidate_universe_fully_dispositioned": True,
                "topic_tag_import_only_edges_forbidden": True,
                "theorem_and_open_claim_ledgers_separate": True,
                "proof_or_status_evidence_not_inherited_across_edges": True,
                "mathlib_reserve_independent_qualification_required": True,
                "mathlib_reserve_global_dedupe_against_parent_seed_and_closure_required": True,
                "independent_release_checker_required": True,
                "current_compare_and_swap_5_5_to_5_6_required": True,
            },
            "findings": [],
        }
    )
    return coverage, relation, qualification


def build_all() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    parent_manifest, parent_by_stage = verify_parent()
    pb_inventory, pb_problems, pb_variants, pb_problem_by_key, variant_by_id = source_universe()
    full_inventory, full_candidates, full_problems, full_problem_by_key = full_source_universe(pb_inventory, pb_problem_by_key)
    seed_rows, resolved_targets, _aliases = verify_seed_crosswalk(full_problem_by_key, parent_by_stage)
    formal_rows = verify_formal_crosswalk(variant_by_id, full_problem_by_key, resolved_targets)
    relation_universe, relation_sources, obligations, wanted_candidates = verify_relation_universe(
        set(full_problem_by_key), pb_inventory["authority_sha256"], full_inventory["authority_sha256"]
    )
    node_rows, node_by_id, _seed_membership, _target_by_semantic = verify_closure_nodes(
        resolved_targets, parent_by_stage
    )
    candidate_rows, candidates_by_key = verify_relation_candidates(
        wanted_candidates, obligations, node_by_id
    )
    edge_rows = verify_relation_edges(candidates_by_key, node_by_id, relation_sources)
    return build_receipts(
        parent_manifest, pb_inventory, pb_problems, pb_variants,
        full_inventory, full_candidates, full_problems, seed_rows, resolved_targets, formal_rows,
        relation_universe, candidate_rows, node_rows, edge_rows,
    )


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def emit(outputs: Mapping[Path, Mapping[str, Any]], *, check: bool) -> None:
    for path, document in outputs.items():
        payload = encoded(document)
        if check:
            require(path.is_file(), f"qualified output missing: {relative(path)}")
            require(path.read_bytes() == payload, f"qualified output byte drift: {relative(path)}")
        else:
            atomic_write(path, payload)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        coverage, relation, qualification = build_all()
        emit(
            {
                COVERAGE_RECEIPT: coverage,
                RELATION_RECEIPT: relation,
                QUALIFICATION: qualification,
            },
            check=args.check,
        )
    except (IntakeError, OSError, KeyError, TypeError, ValueError, IndexError) as error:
        print(f"FAIL Putnam 5.6 intake qualification: {error}", file=os.sys.stderr)
        return 1
    counts = qualification["expected_release_counts"]
    print(
        "PASS Putnam 5.6 intake qualification "
        f"mode={'check' if args.check else 'write'} "
        f"full=768 pb=675 variants=1724 theorem={counts['theorems']} "
        f"open={counts['open_claims']} strict={counts['strict_conjecture_credits']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
