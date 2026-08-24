#!/usr/bin/env python3
"""Aggregate reviewed Putnam seeds and build the zero-credit seed crosswalk.

Every ``seed-reviews/*.jsonl`` file is parsed independently.  Exact duplicate
rows (for example, a sealed range aggregate plus its leaf shards) are accepted
once; conflicting duplicates fail.  A progress receipt can be written at any
review count.  The final ``seed-crosswalk.jsonl`` is emitted or checked only
when the unique reviewed key set is exactly the 768-coordinate 1962--2025
grid.  Missing rows are never synthesized.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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


REPO = Path(__file__).resolve().parents[4]
CURATION_REL = Path("Docs/catalog/v5/curation/putnambench_v5_6")
REVIEW_DIR_REL = CURATION_REL / "seed-reviews"
FULL_INVENTORY_REL = CURATION_REL / "Full_Putnam_Source_Inventory_v5_6.json"
FULL_PROBLEMS_REL = CURATION_REL / "Full_Putnam_Seed_Problems_v5_6.jsonl"
FULL_CANDIDATES_REL = CURATION_REL / "Full_Putnam_Source_Candidates_v5_6.jsonl"
PG_MANIFEST_REL = CURATION_REL / "PutnamGAP_Source_Locator_Manifest_v5_6.jsonl"
KEDLAYA_MANIFEST_REL = CURATION_REL / "Kedlaya_2025_Source_Locator_Manifest_v5_6.jsonl"
PB_PROBLEMS_REL = CURATION_REL / "PutnamBench_Source_Problems_v5_6.jsonl"
PB_ASSETS_REL = CURATION_REL / "PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
PROGRESS_REL = CURATION_REL / "seed-crosswalk-progress.json"
CROSSWALK_REL = CURATION_REL / "seed-crosswalk.jsonl"

FULL_AUTHORITY = "08fb966f533d6ab0f29b08f02ef55de77752f20471bcec3c65915a518df7df84"
FULL_PROBLEMS_SHA = "cfdde7b8117565f0fc7ea6e7fbad2ad42971aca97f09074b539b586dc7a97c8c"
FULL_CANDIDATES_SHA = "615c3db2c950f793669b77a23396a87318a8a956312876704e959c3f083b59ff"
PG_MANIFEST_SHA = "72a28d27099145506a4f779bb3b1941af0414dbff1956fa6052e604b1c00d085"
KEDLAYA_MANIFEST_SHA = "3e80a1c1931a1ee362a3defb95577e3378d2483742b2b3a7be5980512686d51a"
PB_PROBLEMS_SHA = "85727d9216226b14be5bc52a2a7cf8aad11d3834ca10192acb4df1331631889d"
PB_ASSETS_SHA = "6431c652a888bf2dce1f9eb91692cc79f8bf986e613bc5658a43f5f770e7b563"

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
PROBLEM_RE = re.compile(r"^putnam_([0-9]{4})_([ab])([1-6])$")
SEMANTIC_RE = re.compile(r"^putnam-seed-semantic-v1/([0-9a-f]{64})$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

ROW_KEYS = {
    "schema_version", "problem_key", "coordinate", "source_candidate_id",
    "source_index", "source_problem_type", "source_binding", "claim_review",
    "proof_status", "putnambench_binding", "variant_handling",
    "existing_5_5_exact_match_candidates", "rights", "anomaly_codes",
    "candidate_only", "grants_catalog_entry", "grants_theorem_credit",
    "release_mutation_authorized_or_performed", "verbatim_source_text_included",
    "row_sha256",
}
CLAIM_KEYS = {
    "alias_target_problem_key", "answer_visibility", "children",
    "claim_disposition", "claim_shape", "independent_english_statement",
    "multipart_handling", "review_as_of", "review_rationale", "semantic_key",
    "source_claim_validity", "source_defect_detail", "statement_representation",
    "truth_apt",
}
MULTIPART_KEYS = {
    "all_parts_accounted_for", "detail", "handling", "source_has_multiple_parts",
}
CHILD_KEYS = {
    "answer_visibility", "child_id", "distinction_basis",
    "independent_english_statement", "part_label", "semantic_key",
}
PROOF_STATUS_KEYS = {
    "formal_proof_state", "formal_statement_available", "human_status",
    "proof_method_summary", "solution_evidence", "solution_text_redistributed",
    "status_as_of",
}
PB_BINDING_KEYS = {"formal_headers", "present", "source_problem_row_binding"}
PB_PROBLEM_BINDING_KEYS = {"file_sha256", "line_number", "path", "row_sha256"}
HEADER_KEYS = {
    "asset_file_sha256", "asset_line_number", "asset_path", "asset_row_sha256",
    "external_file_sha256", "external_source_path", "header_sha256", "language",
    "license_expression", "rights_id", "source_proof_state", "variant_id",
}
RIGHTS_KEYS = {
    "formal_header_licenses", "independent_statement_origin",
    "question_and_solution_usage", "question_solution_license",
}
VARIANT_HANDLING_KEYS = {
    "formal_languages", "formal_variant_count",
    "formal_variants_grant_no_duplicate_credit", "one_seed_identity_credit_max",
}
PG_SOURCE_KEYS = {
    "archive_member_path", "byte_length", "commit", "evidence_only",
    "file_sha256", "git_blob_sha1", "question_json_pointer",
    "question_value_sha256_utf8", "repository", "row_canonical_sha256",
    "solution_json_pointer", "solution_value_sha256_utf8", "source_kind", "tree",
}
KEDLAYA_SOURCE_KEYS = {
    "canonical_origin", "evidence_only", "immutable_revision",
    "mirror_repository", "source_kind", "tree",
    "statement_archive_member_path", "statement_file_sha256",
    "statement_git_blob_sha1", "statement_value_sha256_utf8",
    "solution_archive_member_path", "solution_file_sha256",
    "solution_git_blob_sha1", "solution_value_sha256_utf8",
}


class CrosswalkError(RuntimeError):
    """A review, source, or completeness invariant failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CrosswalkError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def set_digest(values: Iterable[str]) -> str:
    return digest(canonical(sorted(values)))


def hash_without(value: Mapping[str, Any], field: str) -> str:
    return digest(canonical({key: item for key, item in value.items() if key != field}))


def seal(value: dict[str, Any], field: str = "row_sha256") -> dict[str, Any]:
    require(field not in value, f"object already contains {field}")
    value[field] = hash_without(value, field)
    return value


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def reject_constant(value: str) -> Any:
    raise CrosswalkError(f"non-finite JSON constant: {value}")


def strict_load(payload: bytes, label: str) -> Any:
    try:
        return json.loads(
            payload.decode("utf-8", errors="strict"),
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CrosswalkError(f"invalid JSON in {label}: {error}") from error


def load_json(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    require(path.is_file(), f"{label} missing: {path}")
    payload = path.read_bytes()
    value = strict_load(payload, label)
    require(isinstance(value, dict) and payload == canonical(value) + b"\n", f"{label} is not canonical one-line JSON")
    return value, payload


def load_jsonl(path: Path, label: str) -> tuple[list[dict[str, Any]], bytes]:
    require(path.is_file(), f"{label} missing: {path}")
    payload = path.read_bytes()
    require(payload.endswith(b"\n"), f"{label} has no final newline")
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(payload.splitlines(keepends=True), 1):
        require(line != b"\n" and line.endswith(b"\n"), f"{label} line framing invalid: {number}")
        row = strict_load(line[:-1], f"{label}:{number}")
        require(isinstance(row, dict) and canonical(row) + b"\n" == line, f"{label} row not canonical: {number}")
        rows.append(row)
    return rows, payload


def exact(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    require(isinstance(value, dict), f"{label} is not an object")
    require(set(value) == keys, f"{label} closed schema drifted: missing={sorted(keys-set(value))} extra={sorted(set(value)-keys)}")
    return value


def nonempty(value: Any, label: str) -> str:
    require(isinstance(value, str) and value.strip() == value and value, f"{label} is empty/malformed")
    return value


def sha(value: Any, label: str) -> str:
    require(isinstance(value, str) and SHA_RE.fullmatch(value), f"{label} is not SHA-256")
    return value


def full_grid() -> set[str]:
    return {
        f"putnam_{year}_{section}{number}"
        for year in range(1962, 2026)
        for section in ("a", "b")
        for number in range(1, 7)
    }


def expected_coordinate(key: str) -> dict[str, Any]:
    match = PROBLEM_RE.fullmatch(key)
    require(match is not None, f"invalid problem key: {key}")
    return {
        "year": int(match.group(1)),
        "section": match.group(2).upper(),
        "problem_number": int(match.group(3)),
    }


def semantic_key(statement: str) -> str:
    normalized = re.sub(
        r"\s+", " ", unicodedata.normalize("NFKC", statement).casefold()
    ).strip()
    return "putnam-seed-semantic-v1/" + digest(normalized.encode("utf-8"))


def file_binding(repo_root: Path, path: Path, rows: int) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "path": path.relative_to(repo_root).as_posix(),
        "rows": rows,
        "sha256": digest(payload),
        "size_bytes": len(payload),
    }


def load_sealed_rows(repo_root: Path, relative: Path, label: str, expected_rows: int, expected_sha: str) -> tuple[list[dict[str, Any]], bytes]:
    rows, payload = load_jsonl(repo_root / relative, label)
    require(len(rows) == expected_rows and digest(payload) == expected_sha, f"{label} frozen bytes/count drifted")
    for index, row in enumerate(rows):
        require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"{label} row seal drifted: {index}")
    return rows, payload


def source_context(repo_root: Path) -> dict[str, Any]:
    inventory, _payload = load_json(repo_root / FULL_INVENTORY_REL, "full source inventory")
    require(inventory.get("authority_sha256") == FULL_AUTHORITY and inventory["authority_sha256"] == hash_without(inventory, "authority_sha256"), "full source authority drifted")
    full_problems, _ = load_sealed_rows(repo_root, FULL_PROBLEMS_REL, "full source problems", 768, FULL_PROBLEMS_SHA)
    candidates, _ = load_sealed_rows(repo_root, FULL_CANDIDATES_REL, "full source candidates", 1063, FULL_CANDIDATES_SHA)
    pg_rows, _ = load_sealed_rows(repo_root, PG_MANIFEST_REL, "PutnamGAP locators", 1051, PG_MANIFEST_SHA)
    kedlaya_rows, _ = load_sealed_rows(repo_root, KEDLAYA_MANIFEST_REL, "Kedlaya locators", 12, KEDLAYA_MANIFEST_SHA)
    pb_rows, _ = load_sealed_rows(repo_root, PB_PROBLEMS_REL, "PutnamBench problems", 675, PB_PROBLEMS_SHA)
    assets, _ = load_sealed_rows(repo_root, PB_ASSETS_REL, "PutnamBench declaration assets", 1724, PB_ASSETS_SHA)
    full_by_key = {str(row["problem_key"]): row for row in full_problems}
    candidate_by_id = {str(row["source_candidate_id"]): row for row in candidates}
    pg_by_id = {str(row["source_candidate_id"]): row for row in pg_rows}
    kedlaya_by_id = {str(row["source_candidate_id"]): row for row in kedlaya_rows}
    pb_by_key = {str(row["problem_key"]): (index + 1, row) for index, row in enumerate(pb_rows)}
    asset_by_variant = {str(row["variant_id"]): (index + 1, row) for index, row in enumerate(assets)}
    require(set(full_by_key) == full_grid() and len(candidate_by_id) == 1063 and len(asset_by_variant) == 1724, "source context identity sets drifted")
    return {
        "full_by_key": full_by_key,
        "candidate_by_id": candidate_by_id,
        "pg_by_id": pg_by_id,
        "kedlaya_by_id": kedlaya_by_id,
        "pb_by_key": pb_by_key,
        "asset_by_variant": asset_by_variant,
    }


def validate_pg_source(value: Any, candidate: Mapping[str, Any], manifest: Mapping[str, Any], label: str) -> None:
    source = exact(value, PG_SOURCE_KEYS, label)
    locator = manifest["record_locator"]
    file_source = manifest["source_file_binding"]
    require(source["source_kind"] == "putnamgap" and source["evidence_only"] is True, f"{label} branch/boundary drifted")
    require(source["repository"] == "https://github.com/YurenHao0426/PutnamGAP" and source["commit"] == "aee05407afc7e621e8d9c7f909f4f25ccb8131c0" and source["tree"] == "0f55aee4f4b911e767785a7c5977fbe36f58dbbe", f"{label} snapshot drifted")
    require(source["archive_member_path"] == file_source["upstream_relative_path"] and source["byte_length"] == file_source["byte_length"] and source["file_sha256"] == file_source["file_sha256"] and source["git_blob_sha1"] == file_source["git_blob_sha1"], f"{label} source-file binding drifted")
    require(source["row_canonical_sha256"] == locator["record_canonical_sha256"], f"{label} canonical row hash drifted")
    require(source["question_json_pointer"] == "/question" and source["solution_json_pointer"] == "/solution", f"{label} JSON pointers drifted")
    require(source["question_value_sha256_utf8"] == candidate["source_statement_sha256"] == locator["statement_value_sha256"], f"{label} question hash drifted")
    require(source["solution_value_sha256_utf8"] == candidate["source_solution_sha256"] == locator["solution_value_sha256"], f"{label} solution hash drifted")


def validate_kedlaya_source(value: Any, candidate: Mapping[str, Any], manifest: Mapping[str, Any], label: str) -> None:
    source = exact(value, KEDLAYA_SOURCE_KEYS, label)
    statement = manifest["statement_binding"]
    solution = manifest["solution_binding"]
    require(source["source_kind"] == "kedlaya_2025" and source["evidence_only"] is True, f"{label} branch/boundary drifted")
    require(source["canonical_origin"] == "https://kskedlaya.org/putnam-archive/" and source["mirror_repository"] == "https://github.com/rpxgit/The-Putnam-Archive" and source["immutable_revision"] == "bd9408c626737480f9b76ab7e287dad6980154c8" and source["tree"] == "42343fd26c12ffb37597c917ed5374bbc03b276b", f"{label} snapshot drifted")
    for prefix, review_binding, frozen in (("statement", source, statement), ("solution", source, solution)):
        file_source = frozen["source_file_binding"]
        require(review_binding[f"{prefix}_archive_member_path"] == file_source["upstream_relative_path"] and review_binding[f"{prefix}_file_sha256"] == file_source["file_sha256"] and review_binding[f"{prefix}_git_blob_sha1"] == file_source["git_blob_sha1"], f"{label} {prefix} file binding drifted")
        require(review_binding[f"{prefix}_value_sha256_utf8"] == frozen["item_body_sha256"] == candidate[f"source_{prefix}_sha256"], f"{label} {prefix} value hash drifted")


def validate_formal_headers(row: Mapping[str, Any], full: Mapping[str, Any], context: Mapping[str, Any], label: str) -> None:
    binding = exact(row["putnambench_binding"], PB_BINDING_KEYS, f"{label}.putnambench_binding")
    expected_ids = list(full["formal_variant_ids"])
    present = full["putnambench_problem_row_sha256"] is not None
    require(binding["present"] is present, f"{label} PB presence drifted")
    headers = binding["formal_headers"]
    require(isinstance(headers, list) and len(headers) == len(expected_ids), f"{label} formal header denominator drifted")
    seen: set[str] = set()
    for index, item in enumerate(headers):
        header = exact(item, HEADER_KEYS, f"{label}.formal_headers[{index}]")
        variant_id = nonempty(header["variant_id"], f"{label}.formal_headers[{index}].variant_id")
        require(variant_id in expected_ids and variant_id not in seen, f"{label} formal header identity drifted")
        seen.add(variant_id)
        line, asset = context["asset_by_variant"].get(variant_id, (None, None))
        require(asset is not None, f"{label} formal asset missing: {variant_id}")
        require(header["asset_path"] == PB_ASSETS_REL.as_posix() and header["asset_file_sha256"] == PB_ASSETS_SHA and header["asset_line_number"] == line and header["asset_row_sha256"] == asset["row_sha256"], f"{label} formal asset row binding drifted: {variant_id}")
        external = asset["external_source_binding"]
        require(header["external_source_path"] == external["upstream_relative_path"] and header["external_file_sha256"] == external["file_sha256"], f"{label} external formal file binding drifted: {variant_id}")
        require(header["header_sha256"] == asset["declaration_header"]["sha256"] and header["language"] == asset["language"], f"{label} formal header bytes/language drifted: {variant_id}")
        require(header["rights_id"] == asset["rights"]["rights_id"] and header["license_expression"] == asset["rights"]["license_expression"], f"{label} formal rights drifted: {variant_id}")
        require(header["source_proof_state"] == "placeholder_with_proof_hole", f"{label} formal placeholder boundary drifted: {variant_id}")
    require(seen == set(expected_ids), f"{label} formal header projection incomplete")
    problem_binding = binding["source_problem_row_binding"]
    if present:
        problem_binding = exact(problem_binding, PB_PROBLEM_BINDING_KEYS, f"{label}.source_problem_row_binding")
        line, pb_row = context["pb_by_key"].get(row["problem_key"], (None, None))
        require(pb_row is not None and problem_binding == {"file_sha256": PB_PROBLEMS_SHA, "line_number": line, "path": PB_PROBLEMS_REL.as_posix(), "row_sha256": pb_row["row_sha256"]}, f"{label} PB problem row binding drifted")
        require(pb_row["row_sha256"] == full["putnambench_problem_row_sha256"] and pb_row["formal_variant_ids"] == expected_ids, f"{label} PB/full source join drifted")
    else:
        require(problem_binding is None and not expected_ids, f"{label} absent PB binding malformed")
    handling = exact(row["variant_handling"], VARIANT_HANDLING_KEYS, f"{label}.variant_handling")
    languages = [header["language"] for header in headers]
    require(handling["formal_languages"] == languages and handling["formal_variant_count"] == len(headers), f"{label} variant handling projection drifted")
    require(handling["formal_variants_grant_no_duplicate_credit"] is True and handling["one_seed_identity_credit_max"] is True, f"{label} formal credit boundary drifted")
    rights = exact(row["rights"], RIGHTS_KEYS, f"{label}.rights")
    require(rights["formal_header_licenses"] == sorted(set(header["license_expression"] for header in headers)), f"{label} formal license projection drifted")
    require(rights["independent_statement_origin"] == "reviewer_authored" and rights["question_and_solution_usage"] == "evidence_only_no_redistribution" and rights["question_solution_license"] == "NOASSERTION_MAA_COPYRIGHT", f"{label} source rights boundary drifted")


def reviewed_targets(claim: Mapping[str, Any], label: str) -> list[dict[str, str]]:
    disposition = claim["claim_disposition"]
    multipart = exact(claim["multipart_handling"], MULTIPART_KEYS, f"{label}.multipart_handling")
    children = claim["children"]
    require(isinstance(children, list), f"{label}.children malformed")
    if disposition == "theorem":
        statement = nonempty(claim["independent_english_statement"], f"{label}.statement")
        semantic = nonempty(claim["semantic_key"], f"{label}.semantic_key")
        require(not children and multipart["all_parts_accounted_for"] is True, f"{label} single-claim factoring drifted")
        require(
            (claim["claim_shape"], multipart["handling"], multipart["source_has_multiple_parts"])
            in {
                ("single", "single_complete_claim", False),
                ("source_named_compound", "single_compound_claim", True),
            },
            f"{label} single/compound claim shape drifted",
        )
        require(semantic == semantic_key(statement), f"{label} semantic-key formula drifted")
        return [{"statement": statement, "semantic_key": semantic, "locator_kind": "single", "locator_index": "0"}]
    require(disposition == "split" and claim["claim_shape"] == "split", f"{label} disposition/shape invalid")
    require(claim["independent_english_statement"] is None and claim["semantic_key"] is None and len(children) >= 2, f"{label} split parent shape invalid")
    require(multipart["all_parts_accounted_for"] is True and multipart["handling"] == "split_into_exhaustive_children" and multipart["source_has_multiple_parts"] is True, f"{label} split exhaustiveness drifted")
    results: list[dict[str, str]] = []
    child_ids: set[str] = set()
    part_labels: set[str] = set()
    for index, item in enumerate(children):
        child = exact(item, CHILD_KEYS, f"{label}.children[{index}]")
        child_id = nonempty(child["child_id"], f"{label}.children[{index}].child_id")
        part_label = nonempty(child["part_label"], f"{label}.children[{index}].part_label")
        statement = nonempty(child["independent_english_statement"], f"{label}.children[{index}].statement")
        semantic = nonempty(child["semantic_key"], f"{label}.children[{index}].semantic_key")
        nonempty(child["distinction_basis"], f"{label}.children[{index}].distinction_basis")
        nonempty(child["answer_visibility"], f"{label}.children[{index}].answer_visibility")
        require(child_id not in child_ids and part_label not in part_labels, f"{label} duplicate split child identity")
        require(semantic == semantic_key(statement), f"{label}.children[{index}] semantic-key formula drifted")
        child_ids.add(child_id)
        part_labels.add(part_label)
        results.append({"statement": statement, "semantic_key": semantic, "locator_kind": "child", "locator_index": str(index)})
    return results


def validate_review_row(row: Mapping[str, Any], context: Mapping[str, Any], label: str) -> list[dict[str, str]]:
    exact(row, ROW_KEYS, label)
    require(row["schema_version"] == "awesome-theorems/putnam-seed-claim-review/5.6" and row["row_sha256"] == hash_without(row, "row_sha256"), f"{label} schema/row seal drifted")
    key = nonempty(row["problem_key"], f"{label}.problem_key")
    full = context["full_by_key"].get(key)
    require(full is not None and row["coordinate"] == expected_coordinate(key), f"{label} key/coordinate join drifted")
    require(
        full["coordinate"]
        == {"competition": "William Lowell Putnam Mathematical Competition", **expected_coordinate(key)},
        f"{label} full-source coordinate drifted",
    )
    candidate_id = nonempty(row["source_candidate_id"], f"{label}.source_candidate_id")
    require(candidate_id in full["source_candidate_ids"], f"{label} source candidate is not a source of {key}")
    candidate = context["candidate_by_id"].get(candidate_id)
    require(candidate is not None and candidate["target_problem_key"] == key and candidate["disposition"] in {"mapped_in_scope_coordinate", "alternate_or_duplicate_source_variant"}, f"{label} candidate disposition/target drifted")
    require(row["source_index"] == candidate["source_problem_key"], f"{label} native source index drifted")
    if candidate["source_branch"] == "putnamgap":
        manifest = context["pg_by_id"].get(candidate_id)
        require(manifest is not None, f"{label} PutnamGAP manifest row missing")
        validate_pg_source(row["source_binding"], candidate, manifest, f"{label}.source_binding")
    else:
        manifest = context["kedlaya_by_id"].get(candidate_id)
        require(manifest is not None, f"{label} Kedlaya manifest row missing")
        validate_kedlaya_source(row["source_binding"], candidate, manifest, f"{label}.source_binding")
    claim = exact(row["claim_review"], CLAIM_KEYS, f"{label}.claim_review")
    require(claim["alias_target_problem_key"] is None and claim["truth_apt"] is True and claim["statement_representation"] == "independently_written_review_statement", f"{label} claim boundary drifted")
    nonempty(claim["review_rationale"], f"{label}.review_rationale")
    require(isinstance(claim["review_as_of"], str) and DATE_RE.fullmatch(claim["review_as_of"]), f"{label}.review_as_of invalid")
    require(claim["source_claim_validity"] in {"valid_as_scoped", "requires_explicit_convention", "ocr_repair_explicit", "false_as_printed_repaired_explicitly"}, f"{label} source validity invalid")
    targets = reviewed_targets(claim, f"{label}.claim_review")
    proof = exact(row["proof_status"], PROOF_STATUS_KEYS, f"{label}.proof_status")
    require(proof["human_status"] == "solved_competition_problem" and proof["solution_evidence"] == "pinned_solution_locator_and_hash" and proof["solution_text_redistributed"] is False, f"{label} proof status/evidence drifted")
    nonempty(proof["proof_method_summary"], f"{label}.proof_method_summary")
    require(isinstance(proof["status_as_of"], str) and DATE_RE.fullmatch(proof["status_as_of"]), f"{label}.proof status date invalid")
    require(proof["formal_proof_state"] in {"placeholder_only_not_proof", "no_pb_formal_variant"} and isinstance(proof["formal_statement_available"], bool), f"{label} formal proof axis drifted")
    validate_formal_headers(row, full, context, label)
    require(isinstance(row["source_problem_type"], str) and row["source_problem_type"], f"{label} source problem type invalid")
    require(isinstance(row["existing_5_5_exact_match_candidates"], list), f"{label} parent candidate list malformed")
    require(isinstance(row["anomaly_codes"], list) and all(isinstance(item, str) and item for item in row["anomaly_codes"]), f"{label} anomaly codes malformed")
    require(row["candidate_only"] is True and row["grants_catalog_entry"] is False and row["grants_theorem_credit"] is False and row["release_mutation_authorized_or_performed"] is False and row["verbatim_source_text_included"] is False, f"{label} zero-credit/publication boundary drifted")
    return targets


def collect_reviews(repo_root: Path) -> dict[str, Any]:
    context = source_context(repo_root)
    review_dir = repo_root / REVIEW_DIR_REL
    paths = sorted(review_dir.glob("*.jsonl"))
    require(paths, "no seed review JSONL files found")
    occurrences: dict[str, list[dict[str, Any]]] = defaultdict(list)
    file_inputs: list[dict[str, Any]] = []
    raw_rows = 0
    for path in paths:
        rows, payload = load_jsonl(path, f"seed review {path.name}")
        file_inputs.append(file_binding(repo_root, path, len(rows)))
        raw_rows += len(rows)
        for line_number, row in enumerate(rows, 1):
            targets = validate_review_row(row, context, f"{path.name}:{line_number}")
            occurrences[str(row["problem_key"])].append({
                "row": row,
                "targets": targets,
                "path": path,
                "line_number": line_number,
                "file_sha256": digest(payload),
                "file_rows": len(rows),
            })
    selected: dict[str, dict[str, Any]] = {}
    duplicate_occurrences = 0
    for key, entries in occurrences.items():
        first = entries[0]["row"]
        require(all(entry["row"] == first for entry in entries), f"conflicting duplicate seed reviews: {key}")
        duplicate_occurrences += len(entries) - 1
        selected[key] = min(entries, key=lambda entry: (entry["file_rows"], entry["path"].as_posix(), entry["line_number"]))
    require(set(selected) <= full_grid(), "review set contains a key outside the 768 grid")
    semantics: dict[str, str] = {}
    for key, entry in selected.items():
        for target in entry["targets"]:
            semantic = target["semantic_key"]
            require(semantic not in semantics, f"semantic key collision between {key} and {semantics.get(semantic)}")
            semantics[semantic] = key
    return {
        "context": context,
        "selected": selected,
        "file_inputs": file_inputs,
        "raw_rows": raw_rows,
        "duplicate_occurrences": duplicate_occurrences,
        "semantics": semantics,
    }


def review_source_binding(repo_root: Path, entry: Mapping[str, Any], target: Mapping[str, str]) -> dict[str, Any]:
    row = entry["row"]
    locator: dict[str, Any] = {
        "line_number": entry["line_number"],
        "row_sha256": row["row_sha256"],
        "claim_locator_kind": target["locator_kind"],
        "claim_locator_index": int(target["locator_index"]),
        "semantic_key": target["semantic_key"],
    }
    return {
        "source_id": f"putnam-seed-review:{row['row_sha256']}",
        "path": entry["path"].relative_to(repo_root).as_posix(),
        "file_sha256": entry["file_sha256"],
        "locator": locator,
        "evidence_sha256": row["row_sha256"],
        "rights_id": "putnam-seed-review-independent-summary",
    }


def target_row(repo_root: Path, entry: Mapping[str, Any], target: Mapping[str, str], candidate: Mapping[str, Any]) -> dict[str, Any]:
    row = entry["row"]
    text = target["statement"]
    representation = "independently_written_review_statement"
    statement_sha = digest(canonical({"language": "en", "representation": representation, "text": text}))
    proof_summary = row["proof_status"]["proof_method_summary"]
    return {
        "semantic_key": target["semantic_key"],
        "identity_action": "noncatalog_benchmark_seed",
        "stage_claim_id": None,
        "variant_id": None,
        "parent_catalog_record_sha256": None,
        "allocation_request_sha256": None,
        "claim_kind": "theorem",
        "material_status": "proved",
        "statement": {
            "language": "en",
            "representation": representation,
            "text": text,
            "statement_sha256": statement_sha,
            "source_bindings": [
                review_source_binding(repo_root, entry, target),
                copy.deepcopy(candidate["source_binding"]),
            ],
            "independently_written": True,
        },
        "proof_evidence": [{
            "kind": "human_published_solution",
            "proof_state": "proved",
            "uses_placeholder": False,
            "reviewed": True,
            "applies_to_statement_sha256": statement_sha,
            "proof_method_summary": proof_summary,
            "proof_method_summary_sha256": digest(proof_summary.encode("utf-8")),
            "independently_written_summary": True,
            "source_binding": copy.deepcopy(candidate["source_binding"]),
            "rights": {
                "catalog_relicenses_source": False,
                "proof_text_redistributed": False,
                "attribution": [
                    "William Lowell Putnam Mathematical Competition source and cited solution",
                    candidate["source_candidate_id"],
                ],
            },
        }],
        "rights": {
            "catalog_relicenses_source": False,
            "statement_origin": "independently_written_reviewed_summary",
            "source_wording_redistributed": False,
            "cleared_for_catalog_statement": True,
            "attribution": [
                "William Lowell Putnam Mathematical Competition source",
                f"independent seed review {row['row_sha256']}",
            ],
        },
    }


def build_crosswalk_rows(repo_root: Path, collection: Mapping[str, Any]) -> list[dict[str, Any]]:
    selected = collection["selected"]
    grid = full_grid()
    missing = sorted(grid - set(selected))
    require(not missing and len(selected) == 768, f"seed crosswalk incomplete: reviewed={len(selected)}/768 missing={len(missing)}")
    rows: list[dict[str, Any]] = []
    for key in sorted(grid):
        entry = selected[key]
        review = entry["row"]
        full = collection["context"]["full_by_key"][key]
        candidate = collection["context"]["candidate_by_id"][review["source_candidate_id"]]
        targets = [target_row(repo_root, entry, target, candidate) for target in entry["targets"]]
        crosswalk = {
            "schema_version": "awesome-theorems/putnambench-seed-crosswalk-row/5.6",
            "problem_key": key,
            "source_problem_row_sha256": full["row_sha256"],
            "disposition": "reviewed_noncatalog_benchmark_seed",
            "alias_of_problem_key": None,
            "targets": targets,
            "formal_variant_ids": list(full["formal_variant_ids"]),
            "statement_review": {
                "exact_scope_reviewed": True,
                "quantifiers_and_assumptions_reviewed": True,
                "factored_answer_visibility_reviewed": True,
                "formal_variant_inventory_bound": True,
                "formal_variant_semantic_review_deferred_to_formal_crosswalk": True,
                "parent_semantic_dedupe_reviewed": True,
                "benchmark_proposition_complete": True,
            },
            "review": {
                "reviewer_id": f"putnam-seed-review-ledger/{review['row_sha256']}",
                "reviewed_as_of": review["claim_review"]["review_as_of"],
                "manual_statement_review": True,
                "manual_benchmark_proposition_review": True,
                "notes": review["claim_review"]["review_rationale"],
            },
        }
        rows.append(seal(crosswalk))
    return rows


def build_progress(repo_root: Path, collection: Mapping[str, Any]) -> dict[str, Any]:
    selected = collection["selected"]
    grid = full_grid()
    missing = sorted(grid - set(selected))
    dispositions = Counter(entry["row"]["claim_review"]["claim_disposition"] for entry in selected.values())
    target_count = sum(len(entry["targets"]) for entry in selected.values())
    progress: dict[str, Any] = {
        "schema_version": "awesome-theorems/putnam-seed-crosswalk-progress/5.6",
        "as_of": "2026-08-10",
        "inputs": {
            "seed_review_jsonl_files": collection["file_inputs"],
            "full_source_inventory_authority_sha256": FULL_AUTHORITY,
            "full_source_problems_sha256": FULL_PROBLEMS_SHA,
            "full_source_candidates_sha256": FULL_CANDIDATES_SHA,
            "putnambench_problems_sha256": PB_PROBLEMS_SHA,
            "putnambench_formal_assets_sha256": PB_ASSETS_SHA,
        },
        "counts": {
            "raw_review_row_occurrences": collection["raw_rows"],
            "exact_duplicate_row_occurrences": collection["duplicate_occurrences"],
            "unique_reviewed_seed_keys": len(selected),
            "required_full_grid_seed_keys": 768,
            "missing_seed_keys": len(missing),
            "reviewed_benchmark_propositions": target_count,
            "claim_dispositions": dict(sorted(dispositions.items())),
            "catalog_entries_granted": 0,
            "theorem_credits_granted": 0,
        },
        "semantic_key_method": {
            "version": "putnam-seed-semantic-v1",
            "normalization": "NFKC; Unicode casefold; collapse all regex-\\s+ runs to one ASCII space; strip",
            "digest": "sha256(normalized UTF-8 bytes)",
        },
        "missing_problem_keys": missing,
        "set_digests": {
            "reviewed_problem_key_set_sha256": set_digest(selected),
            "missing_problem_key_set_sha256": set_digest(missing),
            "reviewed_semantic_key_set_sha256": set_digest(collection["semantics"]),
            "review_row_sha256_set_sha256": set_digest(entry["row"]["row_sha256"] for entry in selected.values()),
        },
        "gates": {
            "every_review_row_independently_revalidated": True,
            "closed_review_schema_and_row_seals": True,
            "source_locator_and_question_solution_hashes_replayed": True,
            "putnambench_problem_header_hash_license_projection_replayed": True,
            "split_children_exhaustive_and_semantic_keys_recomputed": True,
            "zero_credit_boundary_enforced": True,
            "exact_768_key_set_present": not missing and len(selected) == 768,
            "seed_crosswalk_write_authorized": not missing and len(selected) == 768,
        },
        "publication_boundary": {
            "progress_only": True,
            "missing_rows_fabricated": False,
            "seed_crosswalk_written_by_progress_mode": False,
            "catalog_credit_granted": False,
        },
        "findings": [] if not missing else [f"incomplete seed review denominator: {len(selected)}/768; {len(missing)} keys missing"],
    }
    progress["authority_sha256"] = hash_without(progress, "authority_sha256")
    return progress


def encoded_json(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


def encoded_jsonl(rows: Sequence[Mapping[str, Any]]) -> bytes:
    return b"".join(canonical(row) + b"\n" for row in rows)


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fchmod(stream.fileno(), 0o644)
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def run(args: argparse.Namespace) -> int:
    repo_root = args.repo_root.resolve()
    collection = collect_reviews(repo_root)
    progress = build_progress(repo_root, collection)
    progress_path = repo_root / PROGRESS_REL
    if args.write_progress:
        atomic_write(progress_path, encoded_json(progress))
        action = "WROTE PROGRESS"
    elif args.check_progress:
        require(progress_path.is_file() and progress_path.read_bytes() == encoded_json(progress), "seed crosswalk progress bytes drifted")
        action = "PASS PROGRESS"
    else:
        rows = build_crosswalk_rows(repo_root, collection)
        payload = encoded_jsonl(rows)
        path = repo_root / CROSSWALK_REL
        if args.write_crosswalk:
            atomic_write(path, payload)
            action = "WROTE CROSSWALK"
        else:
            require(path.is_file() and path.read_bytes() == payload, "seed crosswalk bytes drifted")
            action = "PASS CROSSWALK"
    print(
        f"{action} reviewed={progress['counts']['unique_reviewed_seed_keys']}/768 "
        f"propositions={progress['counts']['reviewed_benchmark_propositions']} "
        f"missing={progress['counts']['missing_seed_keys']} "
        f"authority={progress['authority_sha256']}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-progress", action="store_true")
    mode.add_argument("--check-progress", action="store_true")
    mode.add_argument("--write-crosswalk", action="store_true")
    mode.add_argument("--check-crosswalk", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=REPO)
    args = parser.parse_args()
    try:
        return run(args)
    except (CrosswalkError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"FAIL Putnam seed crosswalk: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
