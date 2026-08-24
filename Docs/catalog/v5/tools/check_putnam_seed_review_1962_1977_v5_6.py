#!/usr/bin/env python3
"""Independently verify the 192-row Putnam seed-review progress aggregate."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
from typing import Any, Mapping


REPO = Path(__file__).resolve().parents[4]
ROOT = REPO / "Docs/catalog/v5/curation/putnambench_v5_6/seed-reviews"
AGGREGATE = ROOT / "1962-1977.jsonl"
SUMMARY = ROOT / "1962-1977-summary.json"
RECEIPT = ROOT / "1962-1977-receipt.json"
SHARDS = {
    "1962-1969": ROOT / "1962-1969.jsonl",
    "1970-1977": ROOT / "1970-1977.jsonl",
}
EXPECTED_SHARD_SHA256 = {
    "1962-1969": "900326f07319d8dd7087dcd7a2ca805e84157999cc39d21063a910e036fe3b50",
    "1970-1977": "eb200050b8f4400de03842d755bc9da35b7c6bb5364711579d4316ba79cf1362",
}
LOCATORS = REPO / "Docs/catalog/v5/curation/putnambench_v5_6/PutnamGAP_Source_Locator_Manifest_v5_6.jsonl"
PB_PROBLEMS = REPO / "Docs/catalog/v5/curation/putnambench_v5_6/PutnamBench_Source_Problems_v5_6.jsonl"
PB_HEADERS = REPO / "Docs/catalog/v5/curation/putnambench_v5_6/PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
PB_PROBLEMS_SHA256 = "85727d9216226b14be5bc52a2a7cf8aad11d3834ca10192acb4df1331631889d"
PB_HEADERS_SHA256 = "6431c652a888bf2dce1f9eb91692cc79f8bf986e613bc5658a43f5f770e7b563"
PUTNAM_COMMIT = "aee05407afc7e621e8d9c7f909f4f25ccb8131c0"
PUTNAM_TREE = "0f55aee4f4b911e767785a7c5977fbe36f58dbbe"
ROW_SCHEMA = "awesome-theorems/putnam-seed-claim-review/5.6"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

TOP_KEYS = {
    "anomaly_codes", "candidate_only", "claim_review", "coordinate",
    "existing_5_5_exact_match_candidates", "grants_catalog_entry",
    "grants_theorem_credit", "problem_key", "proof_status",
    "putnambench_binding", "release_mutation_authorized_or_performed",
    "rights", "row_sha256", "schema_version", "source_binding",
    "source_candidate_id", "source_index", "source_problem_type",
    "variant_handling", "verbatim_source_text_included",
}
CLAIM_KEYS = {
    "alias_target_problem_key", "answer_visibility", "children",
    "claim_disposition", "claim_shape", "independent_english_statement",
    "multipart_handling", "review_as_of", "review_rationale", "semantic_key",
    "source_claim_validity", "source_defect_detail",
    "statement_representation", "truth_apt",
}
CHILD_KEYS = {
    "answer_visibility", "child_id", "distinction_basis",
    "independent_english_statement", "part_label", "semantic_key",
}
MULTIPART_KEYS = {
    "all_parts_accounted_for", "detail", "handling",
    "source_has_multiple_parts",
}
SOURCE_KEYS = {
    "archive_member_path", "byte_length", "commit", "evidence_only",
    "file_sha256", "git_blob_sha1", "question_json_pointer",
    "question_value_sha256_utf8", "repository", "row_canonical_sha256",
    "solution_json_pointer", "solution_value_sha256_utf8", "source_kind",
    "tree",
}
FORMAL_HEADER_KEYS = {
    "asset_file_sha256", "asset_line_number", "asset_path",
    "asset_row_sha256", "external_file_sha256", "external_source_path",
    "header_sha256", "language", "license_expression", "rights_id",
    "source_proof_state", "variant_id",
}


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


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_rows(path: Path, label: str) -> tuple[bytes, list[dict[str, Any]]]:
    payload = path.read_bytes()
    rows: list[dict[str, Any]] = []
    for number, raw in enumerate(payload.splitlines(), 1):
        require(bool(raw), f"{label} line {number} empty")
        value = json.loads(raw)
        require(isinstance(value, dict), f"{label} line {number} not object")
        require(raw == canonical(value), f"{label} line {number} noncanonical")
        rows.append(value)
    return payload, rows


def read_document(path: Path, label: str) -> tuple[bytes, dict[str, Any]]:
    payload = path.read_bytes()
    value = json.loads(payload)
    require(isinstance(value, dict) and payload == canonical(value) + b"\n", f"{label} noncanonical")
    return payload, value


def verify_object_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label} not object")
    require(set(value) == keys, f"{label} key drift: {sorted(set(value) ^ keys)}")
    return value


def verify_hash(value: Any, label: str) -> str:
    require(isinstance(value, str) and SHA_RE.fullmatch(value) is not None, f"{label} not SHA-256")
    return value


def verify_self_seal(value: Mapping[str, Any], field: str, label: str) -> None:
    payload = dict(value)
    observed = payload.pop(field, None)
    require(observed == digest(canonical(payload)), f"{label} self-seal drifted")


def semantic_key(statement: str) -> str:
    normalized = unicodedata.normalize("NFKC", statement).casefold()
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return "putnam-seed-semantic-v1/" + digest(normalized.encode("utf-8"))


def expected_grid() -> list[str]:
    return [
        f"putnam_{year}_{section}{number}"
        for year in range(1962, 1978)
        for section in ("a", "b")
        for number in range(1, 7)
    ]


def index_for(key: str) -> str:
    match = re.fullmatch(r"putnam_(\d{4})_([ab])([1-6])", key)
    require(match is not None, f"bad problem key {key}")
    return f"{match.group(1)}-{match.group(2).upper()}-{match.group(3)}"


def load_authorities() -> tuple[dict[str, dict[str, Any]], dict[str, tuple[int, dict[str, Any]]], dict[str, list[tuple[int, dict[str, Any]]]]]:
    _, locator_rows = read_rows(LOCATORS, "PutnamGAP locator manifest")
    locators = {str(row["source_candidate_id"]): row for row in locator_rows}
    require(len(locators) == len(locator_rows), "duplicate PutnamGAP locator candidate")

    problem_payload, problem_rows = read_rows(PB_PROBLEMS, "PutnamBench source problems")
    require(digest(problem_payload) == PB_PROBLEMS_SHA256 and len(problem_rows) == 675, "PutnamBench problem authority drifted")
    problems = {str(row["problem_key"]): (number, row) for number, row in enumerate(problem_rows, 1)}
    require(len(problems) == 675, "duplicate PutnamBench problem key")

    header_payload, header_rows = read_rows(PB_HEADERS, "PutnamBench formal header asset")
    require(digest(header_payload) == PB_HEADERS_SHA256 and len(header_rows) == 1_724, "PutnamBench header authority drifted")
    headers: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for number, row in enumerate(header_rows, 1):
        headers.setdefault(str(row["problem_key"]), []).append((number, row))
    return locators, problems, headers


def expected_formal_binding(number: int, source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "asset_file_sha256": PB_HEADERS_SHA256,
        "asset_line_number": number,
        "asset_path": "Docs/catalog/v5/curation/putnambench_v5_6/PutnamBench_Formal_Declaration_Asset_v5_6.jsonl",
        "asset_row_sha256": source["row_sha256"],
        "external_file_sha256": source["external_source_binding"]["file_sha256"],
        "external_source_path": source["external_source_binding"]["upstream_relative_path"],
        "header_sha256": source["declaration_header"]["sha256"],
        "language": source["language"],
        "license_expression": source["rights"]["license_expression"],
        "rights_id": source["rights"]["rights_id"],
        "source_proof_state": "placeholder_with_proof_hole",
        "variant_id": source["variant_id"],
    }


def verify_row(
    row: dict[str, Any],
    position: int,
    locators: Mapping[str, Mapping[str, Any]],
    problems: Mapping[str, tuple[int, Mapping[str, Any]]],
    headers: Mapping[str, list[tuple[int, Mapping[str, Any]]]],
) -> list[str]:
    label = f"aggregate row {position}"
    verify_object_keys(row, TOP_KEYS, label)
    require(row["schema_version"] == ROW_SCHEMA, f"{label} schema drifted")
    seal_payload = dict(row)
    observed_seal = seal_payload.pop("row_sha256")
    require(observed_seal == digest(canonical(seal_payload)), f"{label} row seal drifted")
    key = str(row["problem_key"])
    native = index_for(key)
    year, section, number = native.split("-")
    require(row["coordinate"] == {"year": int(year), "section": section, "problem_number": int(number)}, f"{label} coordinate drifted")
    require(row["source_index"] == native, f"{label} source index drifted")
    expected_candidate = f"putnamgap/{PUTNAM_COMMIT}/{native}"
    require(row["source_candidate_id"] == expected_candidate, f"{label} candidate ID drifted")
    require(row["source_problem_type"] in {"proof", "calculation"}, f"{label} source problem type invalid")

    require(row["candidate_only"] is True, f"{label} crossed candidate-only boundary")
    require(row["verbatim_source_text_included"] is False, f"{label} claims verbatim source text")
    require(row["grants_catalog_entry"] is False and row["grants_theorem_credit"] is False, f"{label} grants catalog/theorem credit")
    require(row["release_mutation_authorized_or_performed"] is False, f"{label} mutates release")
    require(row["existing_5_5_exact_match_candidates"] == [], f"{label} carries unverified parent match")

    source = verify_object_keys(row["source_binding"], SOURCE_KEYS, f"{label}.source_binding")
    locator = locators.get(expected_candidate)
    require(locator is not None, f"{label} missing PutnamGAP locator")
    file_binding = locator["source_file_binding"]
    record = locator["record_locator"]
    require(locator["target_problem_key"] == key and locator["native_index"] == native, f"{label} locator coordinate drifted")
    require(source["source_kind"] == "putnamgap" and source["commit"] == PUTNAM_COMMIT and source["tree"] == PUTNAM_TREE, f"{label} PutnamGAP revision drifted")
    require(source["archive_member_path"] == f"dataset/{native}.json", f"{label} source member path drifted")
    require(source["file_sha256"] == file_binding["file_sha256"], f"{label} source file hash drifted")
    require(source["git_blob_sha1"] == file_binding["git_blob_sha1"], f"{label} git blob drifted")
    require(source["byte_length"] == file_binding["byte_length"], f"{label} byte length drifted")
    require(source["row_canonical_sha256"] == record["record_canonical_sha256"], f"{label} canonical source row drifted")
    require(source["question_json_pointer"] == record["statement_pointer"] == "/question", f"{label} question pointer drifted")
    require(source["solution_json_pointer"] == record["solution_pointer"] == "/solution", f"{label} solution pointer drifted")
    require(source["question_value_sha256_utf8"] == record["statement_value_sha256"], f"{label} question value hash drifted")
    require(source["solution_value_sha256_utf8"] == record["solution_value_sha256"], f"{label} solution value hash drifted")
    require(source["evidence_only"] is True, f"{label} source not evidence-only")

    claim = verify_object_keys(row["claim_review"], CLAIM_KEYS, f"{label}.claim_review")
    require(claim["truth_apt"] is True and claim["alias_target_problem_key"] is None, f"{label} claim truth/alias boundary drifted")
    require(claim["review_as_of"] == "2026-08-10", f"{label} review date drifted")
    require(claim["statement_representation"] == "independently_written_review_statement", f"{label} statement origin drifted")
    require(isinstance(claim["review_rationale"], str) and claim["review_rationale"].strip(), f"{label} rationale empty")
    require(claim["source_claim_validity"] in {"valid_as_scoped", "requires_explicit_convention", "ocr_repair_explicit", "false_as_printed_repaired_explicitly"}, f"{label} validity invalid")
    if claim["source_defect_detail"] is not None:
        require(isinstance(claim["source_defect_detail"], str) and claim["source_defect_detail"].strip(), f"{label} defect detail malformed")
    if claim["source_claim_validity"] != "valid_as_scoped":
        require(isinstance(claim["source_defect_detail"], str) and claim["source_defect_detail"].strip(), f"{label} repair lacks defect detail")
    multipart = verify_object_keys(claim["multipart_handling"], MULTIPART_KEYS, f"{label}.multipart")
    require(multipart["all_parts_accounted_for"] is True and isinstance(multipart["detail"], str) and multipart["detail"].strip(), f"{label} multipart review incomplete")
    require(isinstance(claim["children"], list), f"{label} children malformed")
    semantics: list[str] = []
    if claim["claim_disposition"] == "theorem":
        require(claim["claim_shape"] in {"single", "source_named_compound"}, f"{label} theorem shape invalid")
        require(claim["children"] == [], f"{label} theorem has children")
        statement = claim["independent_english_statement"]
        require(isinstance(statement, str) and statement.strip(), f"{label} theorem statement empty")
        require(claim["semantic_key"] == semantic_key(statement), f"{label} theorem semantic key drifted")
        require(claim["answer_visibility"] in {"proof_claim_no_separate_answer", "explicit_answer_in_statement", "classification_complete"}, f"{label} answer visibility invalid")
        semantics.append(str(claim["semantic_key"]))
    else:
        require(claim["claim_disposition"] == "split" and claim["claim_shape"] == "split", f"{label} disposition invalid")
        require(claim["independent_english_statement"] is None and claim["semantic_key"] is None, f"{label} split parent owns semantic identity")
        require(claim["answer_visibility"] == "not_applicable_split_parent", f"{label} split parent answer visibility invalid")
        require(multipart["source_has_multiple_parts"] is True and multipart["handling"] == "split_into_exhaustive_children", f"{label} split handling invalid")
        require(len(claim["children"]) >= 2, f"{label} split has too few children")
        child_ids: set[str] = set()
        labels: set[str] = set()
        for child_position, child_value in enumerate(claim["children"], 1):
            child = verify_object_keys(child_value, CHILD_KEYS, f"{label}.child[{child_position}]")
            child_id = str(child["child_id"])
            part_label = str(child["part_label"])
            statement = child["independent_english_statement"]
            require(child_id.startswith(expected_candidate + "/") and child_id != expected_candidate + "/" and child_id not in child_ids, f"{label} child ID invalid/duplicate")
            require(part_label and part_label not in labels, f"{label} child part label invalid/duplicate")
            require(isinstance(statement, str) and statement.strip(), f"{label} child statement empty")
            require(child["semantic_key"] == semantic_key(statement), f"{label} child semantic key drifted")
            require(child["answer_visibility"] in {"proof_claim_no_separate_answer", "explicit_answer_in_statement", "classification_complete"}, f"{label} child answer visibility invalid")
            require(isinstance(child["distinction_basis"], str) and child["distinction_basis"].strip(), f"{label} child distinction basis empty")
            child_ids.add(child_id)
            labels.add(part_label)
            semantics.append(str(child["semantic_key"]))

    proof = row["proof_status"]
    require(set(proof) == {"formal_proof_state", "formal_statement_available", "human_status", "proof_method_summary", "solution_evidence", "solution_text_redistributed", "status_as_of"}, f"{label} proof status keys drifted")
    require(proof["human_status"] == "solved_competition_problem" and proof["status_as_of"] == "2026-08-10", f"{label} human proof status drifted")
    require(proof["solution_evidence"] == "pinned_solution_locator_and_hash" and proof["solution_text_redistributed"] is False, f"{label} solution evidence boundary drifted")
    require(isinstance(proof["proof_method_summary"], str) and proof["proof_method_summary"].strip(), f"{label} proof summary empty")

    pb = row["putnambench_binding"]
    require(set(pb) == {"formal_headers", "present", "source_problem_row_binding"}, f"{label} PB binding keys drifted")
    problem_entry = problems.get(key)
    if problem_entry is None:
        require(pb == {"formal_headers": [], "present": False, "source_problem_row_binding": None}, f"{label} absent PB shape invalid")
    else:
        problem_line, problem = problem_entry
        expected_problem_binding = {
            "file_sha256": PB_PROBLEMS_SHA256,
            "line_number": problem_line,
            "path": "Docs/catalog/v5/curation/putnambench_v5_6/PutnamBench_Source_Problems_v5_6.jsonl",
            "row_sha256": problem["row_sha256"],
        }
        require(pb["present"] is True and pb["source_problem_row_binding"] == expected_problem_binding, f"{label} PB problem binding drifted")
        require(set(problem["anomaly_codes"]) <= set(row["anomaly_codes"]), f"{label} drops frozen PB anomaly")

    expected_headers = [expected_formal_binding(n, value) for n, value in headers.get(key, [])]
    expected_headers.sort(key=lambda value: {"lean4": 0, "isabelle": 1, "coq": 2}[value["language"]])
    for header_position, header in enumerate(pb["formal_headers"], 1):
        verify_object_keys(header, FORMAL_HEADER_KEYS, f"{label}.formal_header[{header_position}]")
    require(pb["formal_headers"] == expected_headers, f"{label} formal header list drifted")
    languages = [str(header["language"]) for header in expected_headers]
    variants = row["variant_handling"]
    require(set(variants) == {"formal_languages", "formal_variant_count", "formal_variants_grant_no_duplicate_credit", "one_seed_identity_credit_max"}, f"{label} variant handling keys drifted")
    require(variants["formal_languages"] == languages and variants["formal_variant_count"] == len(languages), f"{label} formal variant projection drifted")
    require(variants["formal_variants_grant_no_duplicate_credit"] is True and variants["one_seed_identity_credit_max"] is True, f"{label} duplicate-credit boundary drifted")
    require(proof["formal_statement_available"] is bool(expected_headers), f"{label} formal-statement availability drifted")
    require(proof["formal_proof_state"] == ("placeholder_only_not_proof" if expected_headers else "no_pb_formal_variant"), f"{label} formal proof-state drifted")

    rights = row["rights"]
    require(set(rights) == {"formal_header_licenses", "independent_statement_origin", "question_and_solution_usage", "question_solution_license"}, f"{label} rights keys drifted")
    require(rights["independent_statement_origin"] == "reviewer_authored" and rights["question_and_solution_usage"] == "evidence_only_no_redistribution" and rights["question_solution_license"] == "NOASSERTION_MAA_COPYRIGHT", f"{label} rights boundary drifted")
    require(rights["formal_header_licenses"] == sorted({str(header["license_expression"]) for header in expected_headers}), f"{label} formal license projection drifted")

    forbidden_keys = {"question", "solution", "declaration_header", "formal_declaration_text"}
    require(not (forbidden_keys & set(row)), f"{label} embeds forbidden source field")
    return semantics


def verify_summary_receipt(
    aggregate_payload: bytes,
    rows: list[dict[str, Any]],
    semantic_keys: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    summary_payload, summary = read_document(SUMMARY, "aggregate summary")
    _, receipt = read_document(RECEIPT, "aggregate receipt")
    verify_self_seal(summary, "authority_sha256", "aggregate summary")
    verify_self_seal(receipt, "authority_sha256", "aggregate receipt")
    require(summary["schema_version"] == "awesome-theorems/putnam-seed-claim-review-summary/5.6", "summary schema drifted")
    require(receipt["schema_version"] == "awesome-theorems/putnam-seed-claim-review-receipt/5.6", "receipt schema drifted")
    require(summary["review_range"] == {"first_year": 1962, "last_year": 1977, "rows": 192}, "summary review range drifted")
    require(summary["full_grid_progress"] == {"reviewed_seed_rows": 192, "full_1962_2025_seed_rows": 768, "remaining_unreviewed_seed_rows": 576, "complete_768_crosswalk_authorized": False}, "summary progress boundary drifted")
    require(summary["output"] == {"path": "Docs/catalog/v5/curation/putnambench_v5_6/seed-reviews/1962-1977.jsonl", "rows": 192, "sha256": digest(aggregate_payload), "size_bytes": len(aggregate_payload)}, "summary output binding drifted")
    publication = summary["publication_boundary"]
    require(publication == {
        "benchmark_seed_catalog_disposition": "reviewed_noncatalog_benchmark_seed",
        "candidate_only": True,
        "conjecture_credits_granted": 0,
        "formal_variants_and_relation_edges_grant_duplicate_credit": False,
        "question_or_solution_text_redistributed": False,
        "release_entries_granted": 0,
        "release_mutation_authorized_or_performed": False,
        "theorem_identity_credits_granted": 0,
    }, "summary publication boundary drifted")
    dispositions = Counter(str(row["claim_review"]["claim_disposition"]) for row in rows)
    validity = Counter(str(row["claim_review"]["source_claim_validity"]) for row in rows)
    visibility = Counter(str(row["claim_review"]["answer_visibility"]) for row in rows)
    require(summary["counts"]["rows"] == 192 and summary["counts"]["reviewed_semantic_claims"] == len(semantic_keys), "summary row/claim counts drifted")
    require(summary["counts"]["claim_dispositions"] == dict(sorted(dispositions.items())), "summary disposition counts drifted")
    require(summary["counts"]["source_claim_validity"] == dict(sorted(validity.items())), "summary validity counts drifted")
    require(summary["counts"]["answer_visibility"] == dict(sorted(visibility.items())), "summary answer counts drifted")
    require(receipt["review_output"] == summary["output"] and receipt["publication_boundary"] == publication, "receipt output/publication binding drifted")
    require(receipt["review_summary"]["sha256"] == digest(summary_payload) and receipt["review_summary"]["authority_sha256"] == summary["authority_sha256"], "receipt summary binding drifted")
    require(all(value is True for value in receipt["checks"].values()), "receipt contains a failed check")
    return summary, receipt


def main() -> int:
    try:
        shard_payloads: list[bytes] = []
        for stem, path in SHARDS.items():
            payload, shard_rows = read_rows(path, f"seed shard {stem}")
            require(len(shard_rows) == 96, f"seed shard {stem} row count drifted")
            require(digest(payload) == EXPECTED_SHARD_SHA256[stem], f"seed shard {stem} final hash drifted")
            shard_payloads.append(payload)
        aggregate_payload, rows = read_rows(AGGREGATE, "seed aggregate")
        require(aggregate_payload == b"".join(shard_payloads), "aggregate is not exact shard concatenation")
        require(len(rows) == 192 and [str(row["problem_key"]) for row in rows] == expected_grid(), "aggregate grid/order drifted")
        locators, problems, headers = load_authorities()
        semantic_keys: list[str] = []
        for position, row in enumerate(rows, 1):
            semantic_keys.extend(verify_row(row, position, locators, problems, headers))
        require(len(semantic_keys) == len(set(semantic_keys)), "semantic keys collide across aggregate")
        require(len({str(row["source_candidate_id"]) for row in rows}) == 192, "source candidate IDs duplicate")
        summary, receipt = verify_summary_receipt(aggregate_payload, rows, semantic_keys)
    except (CheckError, OSError, ValueError, TypeError, KeyError, IndexError, json.JSONDecodeError) as error:
        print(f"FAIL independent Putnam seed review 1962-1977: {error}", file=sys.stderr)
        return 1
    print(
        "PASS independent Putnam seed review 1962-1977 "
        f"rows=192 claims={len(semantic_keys)} theorem_rows={summary['counts']['claim_dispositions']['theorem']} "
        f"split_rows={summary['counts']['claim_dispositions']['split']} "
        f"remaining_full_grid=576 output={summary['output']['sha256']} receipt={receipt['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
