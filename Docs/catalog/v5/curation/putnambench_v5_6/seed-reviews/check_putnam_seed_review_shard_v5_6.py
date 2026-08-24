#!/usr/bin/env python3
"""Independently verify a sealed PutnamGAP seed-identity review shard."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[6]
PB_ROOT = REPO / "Docs/catalog/v5/curation/putnambench_v5_6"
PB_INVENTORY = PB_ROOT / "PutnamBench_Source_Inventory_v5_6.json"
PB_PROBLEMS = PB_ROOT / "PutnamBench_Source_Problems_v5_6.jsonl"
PB_HEADERS = PB_ROOT / "PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
PARENT = REPO / "Docs/catalog/v5/releases/5.5/Claim_Catalog.json"
CURRENT = REPO / "Docs/catalog/v5/Current_Release.json"

PUTNAM_COMMIT = "aee05407afc7e621e8d9c7f909f4f25ccb8131c0"
PUTNAM_TREE = "0f55aee4f4b911e767785a7c5977fbe36f58dbbe"
PB_INVENTORY_SHA = "f8407e1aefe39daea09bfa4f940533130139e2e6c65a2eff3e0688d68013ff95"
PB_PROBLEMS_SHA = "85727d9216226b14be5bc52a2a7cf8aad11d3834ca10192acb4df1331631889d"
PB_HEADERS_SHA = "6431c652a888bf2dce1f9eb91692cc79f8bf986e613bc5658a43f5f770e7b563"
RELEASE_ROOT = "fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0"


def canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha(path: Path) -> str:
    return digest(path.read_bytes())


def authority(value: dict, field: str) -> str:
    work = copy.deepcopy(value)
    work.pop(field, None)
    return digest(canonical(work))


def semantic_key(statement: str) -> str:
    text = unicodedata.normalize("NFKC", statement).casefold()
    text = re.sub(r"\s+", " ", text).strip()
    return "putnam-seed-semantic-v1/" + digest(text.encode("utf-8"))


def read_jsonl(path: Path, findings: list[str]) -> list[tuple[bytes, dict]]:
    result: list[tuple[bytes, dict]] = []
    for number, raw in enumerate(path.read_bytes().splitlines(), 1):
        try:
            row = json.loads(raw)
        except Exception as exc:  # pragma: no cover - diagnostic path
            findings.append(f"{path}: line {number}: invalid JSON: {exc}")
            continue
        if not raw or raw.strip() != raw:
            findings.append(f"{path}: line {number}: surrounding whitespace")
        if raw != canonical(row):
            findings.append(f"{path}: line {number}: not canonical JSON")
        result.append((raw, row))
    return result


def expected_keys(first_year: int, last_year: int) -> list[str]:
    return [
        f"putnam_{year}_{section}{number}"
        for year in range(first_year, last_year + 1)
        for section in ("a", "b")
        for number in range(1, 7)
    ]


def source_index(key: str) -> str:
    match = re.fullmatch(r"putnam_(\d{4})_([ab])([1-6])", key)
    assert match
    return f"{match.group(1)}-{match.group(2).upper()}-{match.group(3)}"


def file_binding(path: Path, rows: int | None = None) -> dict:
    value = {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": sha(path),
        "size_bytes": path.stat().st_size,
    }
    if rows is not None:
        value["rows"] = rows
    return value


def check_binding(actual: object, expected: dict, label: str,
                  findings: list[str]) -> None:
    if actual != expected:
        findings.append(f"{label}: file binding mismatch")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--first-year", type=int, required=True)
    parser.add_argument("--last-year", type=int, required=True)
    parser.add_argument(
        "--raw-root", type=Path,
        default=Path("/tmp/putnamgap-audit.uYDPao/dataset"))
    parser.add_argument("--receipt-json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    findings: list[str] = []

    for path, expected in (
        (PB_INVENTORY, PB_INVENTORY_SHA),
        (PB_PROBLEMS, PB_PROBLEMS_SHA),
        (PB_HEADERS, PB_HEADERS_SHA),
    ):
        if not path.is_file() or sha(path) != expected:
            findings.append(f"pinned input mismatch: {path}")

    current = json.loads(CURRENT.read_text())
    if current.get("release") != "5.5" or \
            current.get("release_root_sha256") != RELEASE_ROOT:
        findings.append("Current_Release is not the sealed 5.5 parent")

    problem_rows = read_jsonl(PB_PROBLEMS, findings)
    header_rows = read_jsonl(PB_HEADERS, findings)
    pb_problem = {
        row["problem_key"]: (number, row)
        for number, (_, row) in enumerate(problem_rows, 1)
    }
    pb_headers: dict[str, list[tuple[int, dict]]] = {}
    for number, (_, row) in enumerate(header_rows, 1):
        pb_headers.setdefault(row["problem_key"], []).append((number, row))

    review_rows = read_jsonl(args.review, findings)
    rows = [row for _, row in review_rows]
    keys = expected_keys(args.first_year, args.last_year)
    if len(rows) != len(keys):
        findings.append(f"review row count {len(rows)} != {len(keys)}")
    if [row.get("problem_key") for row in rows] != keys:
        findings.append("review coordinate order/coverage mismatch")
    if len({row.get("problem_key") for row in rows}) != len(rows):
        findings.append("duplicate review problem keys")

    semantic_keys: list[str] = []
    for position, row in enumerate(rows):
        key = row.get("problem_key", f"line-{position + 1}")
        index = source_index(key) if key in keys else "invalid"
        if row.get("schema_version") != \
                "awesome-theorems/putnam-seed-claim-review/5.6":
            findings.append(f"{key}: schema version")
        if row.get("row_sha256") != authority(row, "row_sha256"):
            findings.append(f"{key}: row seal")
        if row.get("source_index") != index:
            findings.append(f"{key}: source index")
        if index != "invalid" and row.get("coordinate") != {
            "year": int(index[:4]), "section": index[5],
            "problem_number": int(index[-1]),
        }:
            findings.append(f"{key}: coordinate")
        expected_candidate = f"putnamgap/{PUTNAM_COMMIT}/{index}"
        if row.get("source_candidate_id") != expected_candidate:
            findings.append(f"{key}: source candidate id")

        if index != "invalid":
            raw_path = args.raw_root / f"{index}.json"
            if not raw_path.is_file():
                findings.append(f"{key}: missing raw source {raw_path}")
                raw = None
                raw_bytes = b""
            else:
                raw_bytes = raw_path.read_bytes()
                raw = json.loads(raw_bytes)
                if raw.get("index") != index:
                    findings.append(f"{key}: raw source index")
            if raw is not None:
                expected_source = {
                    "source_kind": "putnamgap",
                    "repository": "https://github.com/YurenHao0426/PutnamGAP",
                    "commit": PUTNAM_COMMIT,
                    "tree": PUTNAM_TREE,
                    "archive_member_path": f"dataset/{index}.json",
                    "file_sha256": digest(raw_bytes),
                    "git_blob_sha1": hashlib.sha1(
                        b"blob " + str(len(raw_bytes)).encode() + b"\0" +
                        raw_bytes).hexdigest(),
                    "byte_length": len(raw_bytes),
                    "row_canonical_sha256": digest(canonical(raw)),
                    "question_json_pointer": "/question",
                    "question_value_sha256_utf8": digest(
                        raw["question"].encode("utf-8")),
                    "solution_json_pointer": "/solution",
                    "solution_value_sha256_utf8": digest(
                        raw["solution"].encode("utf-8")),
                    "evidence_only": True,
                }
                if row.get("source_binding") != expected_source:
                    findings.append(f"{key}: raw source binding")
                if row.get("source_problem_type") != raw.get("problem_type"):
                    findings.append(f"{key}: source problem type")

        problem = pb_problem.get(key)
        if problem is None:
            expected_problem_binding = None
        else:
            number, problem_row = problem
            expected_problem_binding = {
                "path": PB_PROBLEMS.relative_to(REPO).as_posix(),
                "file_sha256": PB_PROBLEMS_SHA,
                "line_number": number,
                "row_sha256": problem_row["row_sha256"],
            }
        expected_formal = []
        for number, header in pb_headers.get(key, []):
            expected_formal.append({
                "variant_id": header["variant_id"],
                "language": header["language"],
                "header_sha256": header["declaration_header"]["sha256"],
                "asset_path": PB_HEADERS.relative_to(REPO).as_posix(),
                "asset_file_sha256": PB_HEADERS_SHA,
                "asset_line_number": number,
                "asset_row_sha256": header["row_sha256"],
                "rights_id": header["rights"]["rights_id"],
                "license_expression": header["rights"]["license_expression"],
                "external_source_path": header["external_source_binding"][
                    "upstream_relative_path"],
                "external_file_sha256": header["external_source_binding"][
                    "file_sha256"],
                "source_proof_state": "placeholder_with_proof_hole",
            })
        order = {"lean4": 0, "isabelle": 1, "coq": 2}
        expected_formal.sort(key=lambda item: order[item["language"]])
        expected_pb = {
            "present": problem is not None,
            "source_problem_row_binding": expected_problem_binding,
            "formal_headers": expected_formal,
        }
        if row.get("putnambench_binding") != expected_pb:
            findings.append(f"{key}: PutnamBench binding")

        languages = [item["language"] for item in expected_formal]
        expected_variants = {
            "formal_variant_count": len(expected_formal),
            "formal_languages": languages,
            "one_seed_identity_credit_max": True,
            "formal_variants_grant_no_duplicate_credit": True,
        }
        if row.get("variant_handling") != expected_variants:
            findings.append(f"{key}: variant handling")
        expected_licenses = sorted({
            item["license_expression"] for item in expected_formal})
        rights = row.get("rights", {})
        if rights.get("formal_header_licenses") != expected_licenses or \
                rights.get("question_and_solution_usage") != \
                "evidence_only_no_redistribution" or \
                rights.get("independent_statement_origin") != \
                "reviewer_authored" or \
                rights.get("question_solution_license") != \
                "NOASSERTION_MAA_COPYRIGHT":
            findings.append(f"{key}: rights boundary")

        claim = row.get("claim_review", {})
        disposition = claim.get("claim_disposition")
        statement = claim.get("independent_english_statement")
        children = claim.get("children", [])
        if disposition == "split":
            if statement is not None or len(children) < 2 or \
                    claim.get("semantic_key") is not None:
                findings.append(f"{key}: malformed split")
            for child in children:
                child_statement = child.get("independent_english_statement")
                if not isinstance(child_statement, str) or \
                        not child_statement.strip():
                    findings.append(f"{key}: empty split child statement")
                    continue
                expected_semantic = semantic_key(child_statement)
                if child.get("semantic_key") != expected_semantic:
                    findings.append(f"{key}: split child semantic key")
                semantic_keys.append(expected_semantic)
        elif disposition in {"theorem", "alias"}:
            if not isinstance(statement, str) or not statement.strip() or \
                    children:
                findings.append(f"{key}: malformed single claim")
            else:
                expected_semantic = semantic_key(statement)
                if claim.get("semantic_key") != expected_semantic:
                    findings.append(f"{key}: semantic key")
                semantic_keys.append(expected_semantic)
        elif disposition in {"not_truth_apt", "reject"}:
            if statement is not None or children or \
                    claim.get("semantic_key") is not None:
                findings.append(f"{key}: malformed rejection")
        else:
            findings.append(f"{key}: unknown claim disposition {disposition}")
        if claim.get("statement_representation") != \
                "independently_written_review_statement":
            findings.append(f"{key}: statement representation")
        if claim.get("review_as_of") != "2026-08-10" or \
                claim.get("multipart_handling", {}).get(
                    "all_parts_accounted_for") is not True:
            findings.append(f"{key}: review/multipart metadata")
        validity = claim.get("source_claim_validity")
        if validity != "valid_as_scoped" and (
            not row.get("anomaly_codes") or
            not claim.get("source_defect_detail")
        ):
            findings.append(f"{key}: repair lacks anomaly/defect detail")
        proof = row.get("proof_status", {})
        if not proof.get("proof_method_summary", "").strip():
            findings.append(f"{key}: empty proof-method summary")
        if proof.get("human_status") != "solved_competition_problem" or \
                proof.get("status_as_of") != "2026-08-10" or \
                proof.get("solution_evidence") != \
                "pinned_solution_locator_and_hash" or \
                proof.get("solution_text_redistributed") is not False or \
                proof.get("formal_statement_available") is not \
                bool(expected_formal) or proof.get("formal_proof_state") != (
                    "placeholder_only_not_proof" if expected_formal
                    else "no_pb_formal_variant"):
            findings.append(f"{key}: proof-status boundary")
        if not isinstance(row.get("existing_5_5_exact_match_candidates"), list):
            findings.append(f"{key}: existing-match candidates not a list")

        for flag in ("candidate_only",):
            if row.get(flag) is not True:
                findings.append(f"{key}: {flag} must be true")
        for flag in (
            "verbatim_source_text_included", "grants_theorem_credit",
            "grants_catalog_entry", "release_mutation_authorized_or_performed",
        ):
            if row.get(flag) is not False:
                findings.append(f"{key}: {flag} must be false")

    if len(semantic_keys) != len(set(semantic_keys)):
        findings.append("duplicate semantic keys within shard")

    try:
        summary_raw = args.summary.read_bytes()
        summary = json.loads(summary_raw)
        if summary_raw != canonical(summary) + b"\n":
            findings.append("summary is not one canonical JSON line")
        if summary.get("authority_sha256") != authority(
                summary, "authority_sha256"):
            findings.append("summary authority seal")
    except Exception as exc:
        findings.append(f"summary parse failed: {exc}")
        summary = {}

    expected_range = {
        "first_year": args.first_year,
        "last_year": args.last_year,
        "rows": len(keys),
    }
    if summary.get("review_range") != expected_range:
        findings.append("summary review range")
    if summary.get("expected_problem_keys") != keys:
        findings.append("summary expected keys")
    expected_inputs = {
        "putnamgap": {
            "repository": "https://github.com/YurenHao0426/PutnamGAP",
            "commit": PUTNAM_COMMIT,
            "tree": PUTNAM_TREE,
            "question_and_solution_usage":
                "evidence_only_no_redistribution",
        },
        "putnambench_inventory": file_binding(PB_INVENTORY, 1),
        "putnambench_source_problems":
            file_binding(PB_PROBLEMS, len(problem_rows)),
        "putnambench_formal_headers":
            file_binding(PB_HEADERS, len(header_rows)),
        "parent_5_5_catalog": file_binding(PARENT, 1),
    }
    if summary.get("inputs") != expected_inputs:
        findings.append("summary inputs mismatch")
    check_binding(summary.get("output"), file_binding(args.review, len(rows)),
                  "summary output", findings)
    counts = summary.get("counts", {})
    expected_counts = {
        "rows": len(rows),
        "claim_dispositions": dict(sorted(Counter(
            row["claim_review"]["claim_disposition"]
            for row in rows).items())),
        "source_claim_validity": dict(sorted(Counter(
            row["claim_review"]["source_claim_validity"]
            for row in rows).items())),
        "answer_visibility": dict(sorted(Counter(
            row["claim_review"]["answer_visibility"]
            for row in rows).items())),
        "source_problem_types": dict(sorted(Counter(
            row["source_problem_type"] for row in rows).items())),
        "putnambench_present": sum(
            row["putnambench_binding"]["present"] for row in rows),
        "putnambench_absent": sum(
            not row["putnambench_binding"]["present"] for row in rows),
        "formal_variant_headers": sum(
            row["variant_handling"]["formal_variant_count"] for row in rows),
        "rows_with_anomalies": sum(bool(row["anomaly_codes"]) for row in rows),
        "rows_with_explicit_source_repair": sum(
            row["claim_review"]["source_claim_validity"] != "valid_as_scoped"
            for row in rows),
        "split_parent_rows": sum(
            row["claim_review"]["claim_disposition"] == "split"
            for row in rows),
        "split_child_claims": sum(
            len(row["claim_review"]["children"]) for row in rows),
        "alias_rows": sum(
            row["claim_review"]["claim_disposition"] == "alias"
            for row in rows),
        "rejected_rows": sum(
            row["claim_review"]["claim_disposition"] in
            {"reject", "not_truth_apt"} for row in rows),
        "rows_with_existing_5_5_candidates": sum(
            bool(row["existing_5_5_exact_match_candidates"])
            for row in rows),
    }
    if counts != expected_counts:
        findings.append("summary counts mismatch")
    boundary = summary.get("publication_boundary", {})
    if boundary.get("candidate_only") is not True or any(
        boundary.get(field) not in (0, False)
        for field in (
            "theorem_identity_credits_granted", "release_entries_granted",
            "release_mutation_authorized_or_performed",
            "question_or_solution_text_redistributed",
        )
    ):
        findings.append("summary publication boundary")
    coverage = summary.get("coverage", {})
    expected_coverage_keys = {
        "exact_year_coordinate_grid",
        "all_problem_keys_unique",
        "all_parts_and_answer_visibility_reviewed",
        "independently_written_statements_and_proof_summaries",
        "question_and_solution_value_hashes_bound",
        "putnambench_formal_headers_bound_where_available",
        "formal_variants_do_not_grant_duplicate_credit",
        "semantic_keys_unique_within_shard",
        "source_defects_explicitly_repaired_or_rejected",
    }
    if set(coverage) != expected_coverage_keys or \
            any(value is not True for value in coverage.values()):
        findings.append("summary coverage assertions")

    try:
        receipt_raw = args.receipt.read_bytes()
        receipt = json.loads(receipt_raw)
        if receipt_raw != canonical(receipt) + b"\n":
            findings.append("receipt is not one canonical JSON line")
        if receipt.get("authority_sha256") != authority(
                receipt, "authority_sha256"):
            findings.append("receipt authority seal")
    except Exception as exc:
        findings.append(f"receipt parse failed: {exc}")
        receipt = {}
    if receipt.get("review_range") != expected_range:
        findings.append("receipt review range")
    check_binding(receipt.get("review_output"),
                  file_binding(args.review, len(rows)),
                  "receipt output", findings)
    check_binding(receipt.get("review_summary"),
                  file_binding(args.summary, 1),
                  "receipt summary", findings)
    checker_binding = file_binding(Path(__file__))
    check_binding(receipt.get("independent_checker"), checker_binding,
                  "receipt checker", findings)
    if receipt.get("source_authorities") != expected_inputs:
        findings.append("receipt source authorities")
    expected_checks = {
        **coverage,
        "canonical_json_and_row_seals": True,
        "summary_self_seal": True,
        "exact_output_hash_and_row_count": True,
        "independent_checker_required": True,
    }
    if receipt.get("checks") != expected_checks:
        findings.append("receipt checks")
    if receipt.get("publication_boundary") != boundary:
        findings.append("receipt publication boundary")

    result = {
        "schema_version": "awesome-theorems/putnam-seed-claim-review-check/5.6",
        "review_range": expected_range,
        "review_sha256": sha(args.review) if args.review.is_file() else None,
        "summary_sha256": sha(args.summary) if args.summary.is_file() else None,
        "receipt_sha256": sha(args.receipt) if args.receipt.is_file() else None,
        "checker_sha256": sha(Path(__file__)),
        "findings": findings,
    }
    if args.receipt_json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")))
    else:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True,
                         indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
