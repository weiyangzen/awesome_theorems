#!/usr/bin/env python3
"""Independently check the zero-credit Putnam 1983--1987 seed-review shard."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
from typing import Any


REPO = Path(__file__).resolve().parents[4]
ROOT = REPO / "Docs/catalog/v5/curation/putnambench_v5_6"
REVIEW = ROOT / "seed-reviews/1983-1987.jsonl"
SUMMARY = ROOT / "seed-reviews/1983-1987-summary.json"
RECEIPT = ROOT / "seed-reviews/1983-1987-receipt.json"
FULL_INVENTORY = ROOT / "Full_Putnam_Source_Inventory_v5_6.json"
FULL_CANDIDATES = ROOT / "Full_Putnam_Source_Candidates_v5_6.jsonl"
FULL_SEEDS = ROOT / "Full_Putnam_Seed_Problems_v5_6.jsonl"
LOCATORS = ROOT / "PutnamGAP_Source_Locator_Manifest_v5_6.jsonl"
PB_INVENTORY = ROOT / "PutnamBench_Source_Inventory_v5_6.json"
PB_PROBLEMS = ROOT / "PutnamBench_Source_Problems_v5_6.jsonl"
PB_HEADERS = ROOT / "PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
PARENT = REPO / "Docs/catalog/v5/releases/5.5/Claim_Catalog.json"


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


def sha(path: Path) -> str:
    return digest(path.read_bytes())


def set_digest(values: list[str]) -> str:
    return digest(canonical(sorted(values)))


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def file_binding(path: Path, rows: int) -> dict[str, Any]:
    return {
        "path": relative(path),
        "rows": rows,
        "sha256": sha(path),
        "size_bytes": path.stat().st_size,
    }


def semantic_key(statement: str) -> str:
    normalized = unicodedata.normalize("NFKC", statement).casefold()
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return "putnam-seed-semantic-v1/" + digest(normalized.encode("utf-8"))


def expected_keys() -> list[str]:
    return [
        f"putnam_{year}_{section}{number}"
        for year in range(1983, 1988)
        for section in ("a", "b")
        for number in range(1, 7)
    ]


def index_for(key: str) -> str:
    match = re.fullmatch(r"putnam_(\d{4})_([ab])([1-6])", key)
    require(match is not None, f"malformed key {key}")
    return f"{match.group(1)}-{match.group(2).upper()}-{match.group(3)}"


def read_rows(path: Path, *, verify_row_seals: bool = True) -> tuple[bytes, list[dict[str, Any]]]:
    payload = path.read_bytes()
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(payload.splitlines(), 1):
        require(bool(raw), f"{relative(path)}:{line_number}: empty line")
        row = json.loads(raw)
        require(isinstance(row, dict), f"{relative(path)}:{line_number}: non-object")
        require(raw == canonical(row), f"{relative(path)}:{line_number}: noncanonical JSON")
        if verify_row_seals:
            seal_payload = dict(row)
            observed = seal_payload.pop("row_sha256", None)
            require(
                observed == digest(canonical(seal_payload)),
                f"{relative(path)}:{line_number}: row seal drift",
            )
        rows.append(row)
    return payload, rows


def read_document(path: Path) -> tuple[bytes, dict[str, Any]]:
    payload = path.read_bytes()
    require(payload.endswith(b"\n") and payload.count(b"\n") == 1,
            f"{relative(path)} is not one JSON line")
    value = json.loads(payload)
    require(isinstance(value, dict), f"{relative(path)} is not an object")
    require(payload == canonical(value) + b"\n", f"{relative(path)} is noncanonical")
    seal_payload = dict(value)
    observed = seal_payload.pop("authority_sha256", None)
    require(observed == digest(canonical(seal_payload)),
            f"{relative(path)} authority seal drift")
    return payload, value


def expected_header(number: int, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "variant_id": row["variant_id"],
        "language": row["language"],
        "header_sha256": row["declaration_header"]["sha256"],
        "asset_path": relative(PB_HEADERS),
        "asset_file_sha256": sha(PB_HEADERS),
        "asset_line_number": number,
        "asset_row_sha256": row["row_sha256"],
        "rights_id": row["rights"]["rights_id"],
        "license_expression": row["rights"]["license_expression"],
        "external_source_path": row["external_source_binding"]["upstream_relative_path"],
        "external_file_sha256": row["external_source_binding"]["file_sha256"],
        "source_proof_state": "placeholder_with_proof_hole",
    }


def check(source_root: Path | None) -> dict[str, Any]:
    review_payload, rows = read_rows(REVIEW)
    summary_payload, summary = read_document(SUMMARY)
    receipt_payload, receipt = read_document(RECEIPT)
    _, locator_rows = read_rows(LOCATORS)
    _, candidate_rows = read_rows(FULL_CANDIDATES)
    _, seed_rows = read_rows(FULL_SEEDS)
    _, pb_rows = read_rows(PB_PROBLEMS)
    _, header_rows = read_rows(PB_HEADERS)

    require(len(rows) == 60, "review row count is not 60")
    keys = [str(row.get("problem_key")) for row in rows]
    require(keys == expected_keys(), "review order/grid is not exact 1983--1987 A1--B6")
    require(len(set(keys)) == 60, "duplicate problem key")
    require(summary["expected_problem_keys"] == expected_keys(), "summary key grid drift")

    locators = {row["target_problem_key"]: (i, row)
                for i, row in enumerate(locator_rows, 1)
                if row.get("target_problem_key") in set(keys)}
    candidates = {row["target_problem_key"]: (i, row)
                  for i, row in enumerate(candidate_rows, 1)
                  if row.get("target_problem_key") in set(keys)}
    seeds = {row["problem_key"]: (i, row)
             for i, row in enumerate(seed_rows, 1)
             if row.get("problem_key") in set(keys)}
    pb_problems = {row["problem_key"]: (i, row)
                   for i, row in enumerate(pb_rows, 1)}
    headers: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for number, header in enumerate(header_rows, 1):
        headers[header["problem_key"]].append((number, header))
    require(set(locators) == set(keys), "locator coverage is not 60/60")
    require(set(candidates) == set(keys), "full-source candidate coverage is not 60/60")
    require(set(seeds) == set(keys), "full-seed coverage is not 60/60")

    semantic_keys: list[str] = []
    source_ids: list[str] = []
    replay_file_hashes: list[str] = []
    replay_question_hashes: list[str] = []
    replay_solution_hashes: list[str] = []
    for row in rows:
        key = row["problem_key"]
        index = index_for(key)
        loc_number, locator = locators[key]
        cand_number, candidate = candidates[key]
        seed_number, seed = seeds[key]
        source_ids.append(row["source_candidate_id"])
        require(row["schema_version"] == "awesome-theorems/putnam-seed-claim-review/5.6",
                f"{key}: schema drift")
        require(row["source_candidate_id"] == locator["source_candidate_id"],
                f"{key}: source candidate ID drift")
        require(row["source_index"] == index == locator["native_index"],
                f"{key}: source index drift")
        require(candidate["source_candidate_id"] == row["source_candidate_id"],
                f"{key}: full candidate join drift")
        require(seed["source_candidate_ids"] == [row["source_candidate_id"]],
                f"{key}: full seed join drift")
        require(locator["source_row_index"] == loc_number - 1,
                f"{key}: locator ordinal drift")
        require(candidate["source_binding"]["locator"]["manifest_row_index"] == loc_number - 1,
                f"{key}: candidate locator ordinal drift")
        require(candidate["source_binding"]["locator"]["manifest_row_sha256"] == locator["row_sha256"],
                f"{key}: candidate locator seal drift")
        require(seed["source_statement_sha256"] == candidate["source_statement_sha256"] ==
                locator["record_locator"]["statement_value_sha256"],
                f"{key}: question-value hash join drift")
        require(seed["source_solution_sha256"] == candidate["source_solution_sha256"] ==
                locator["record_locator"]["solution_value_sha256"],
                f"{key}: solution-value hash join drift")
        binding = row["source_binding"]
        expected_binding = {
            "source_kind": "putnamgap",
            "repository": "https://github.com/YurenHao0426/PutnamGAP",
            "commit": "aee05407afc7e621e8d9c7f909f4f25ccb8131c0",
            "tree": "0f55aee4f4b911e767785a7c5977fbe36f58dbbe",
            "archive_member_path": locator["source_file_binding"]["upstream_relative_path"],
            "file_sha256": locator["source_file_binding"]["file_sha256"],
            "git_blob_sha1": locator["source_file_binding"]["git_blob_sha1"],
            "byte_length": locator["source_file_binding"]["byte_length"],
            "row_canonical_sha256": locator["record_locator"]["record_canonical_sha256"],
            "question_json_pointer": locator["record_locator"]["statement_pointer"],
            "question_value_sha256_utf8": locator["record_locator"]["statement_value_sha256"],
            "solution_json_pointer": locator["record_locator"]["solution_pointer"],
            "solution_value_sha256_utf8": locator["record_locator"]["solution_value_sha256"],
            "evidence_only": True,
        }
        require(binding == expected_binding, f"{key}: frozen source binding drift")

        coord = row["coordinate"]
        require(coord == {
            "year": seed["coordinate"]["year"],
            "section": seed["coordinate"]["section"],
            "problem_number": seed["coordinate"]["problem_number"],
        }, f"{key}: coordinate drift")

        claim = row["claim_review"]
        require(claim["truth_apt"] is True, f"{key}: not truth-apt")
        require(claim["statement_representation"] == "independently_written_review_statement",
                f"{key}: statement-origin drift")
        require(claim["multipart_handling"]["all_parts_accounted_for"] is True,
                f"{key}: multipart review incomplete")
        children = claim["children"]
        if claim["claim_disposition"] == "split":
            require(key in {"putnam_1984_a6", "putnam_1987_a3"},
                    f"{key}: unexpected split")
            require(claim["independent_english_statement"] is None and
                    claim["semantic_key"] is None and len(children) == 2,
                    f"{key}: malformed split")
            require(claim["answer_visibility"] == "not_applicable_split_parent",
                    f"{key}: split answer visibility drift")
            for child in children:
                statement = child["independent_english_statement"]
                require(child["semantic_key"] == semantic_key(statement),
                        f"{key}/{child['part_label']}: semantic seal drift")
                semantic_keys.append(child["semantic_key"])
        else:
            require(claim["claim_disposition"] == "theorem" and not children,
                    f"{key}: disposition/children drift")
            statement = claim["independent_english_statement"]
            require(isinstance(statement, str) and bool(statement.strip()),
                    f"{key}: missing independent statement")
            require(claim["semantic_key"] == semantic_key(statement),
                    f"{key}: semantic seal drift")
            semantic_keys.append(claim["semantic_key"])
        require(bool(row["proof_status"]["proof_method_summary"].strip()),
                f"{key}: missing proof-method summary")
        require(row["proof_status"]["solution_text_redistributed"] is False,
                f"{key}: solution redistribution boundary drift")

        pb = pb_problems.get(key)
        actual_pb = row["putnambench_binding"]
        require(actual_pb["present"] is (pb is not None), f"{key}: PB presence drift")
        expected_headers = [expected_header(number, header)
                            for number, header in headers.get(key, [])]
        order = {"lean4": 0, "isabelle": 1, "coq": 2}
        expected_headers.sort(key=lambda item: order[item["language"]])
        require(actual_pb["formal_headers"] == expected_headers,
                f"{key}: PB formal-header binding drift")
        require([item["variant_id"] for item in expected_headers] == seed["formal_variant_ids"],
                f"{key}: full-seed/PB formal-variant join drift")
        if pb is None:
            require(actual_pb["source_problem_row_binding"] is None,
                    f"{key}: unexpected PB problem row")
        else:
            pb_number, pb_row = pb
            require(actual_pb["source_problem_row_binding"] == {
                "path": relative(PB_PROBLEMS),
                "file_sha256": sha(PB_PROBLEMS),
                "line_number": pb_number,
                "row_sha256": pb_row["row_sha256"],
            }, f"{key}: PB problem row binding drift")
            require(pb_row["row_sha256"] == seed["putnambench_problem_row_sha256"],
                    f"{key}: PB/full-seed row join drift")
        require(row["variant_handling"]["formal_variant_count"] == len(expected_headers),
                f"{key}: formal variant count drift")
        require(row["variant_handling"]["formal_languages"] ==
                [item["language"] for item in expected_headers],
                f"{key}: formal language list drift")
        require(row["variant_handling"]["formal_variants_grant_no_duplicate_credit"] is True,
                f"{key}: formal duplicate-credit boundary drift")

        require(row["candidate_only"] is True, f"{key}: not candidate-only")
        require(row["grants_theorem_credit"] is False, f"{key}: theorem credit granted")
        require(row["grants_catalog_entry"] is False, f"{key}: catalog entry granted")
        require(row["release_mutation_authorized_or_performed"] is False,
                f"{key}: release mutation granted")
        require(row["verbatim_source_text_included"] is False,
                f"{key}: verbatim source flag drift")
        require(row["existing_5_5_exact_match_candidates"] == [],
                f"{key}: unresolved exact-match candidate")
        require(row["rights"]["question_and_solution_usage"] ==
                "evidence_only_no_redistribution", f"{key}: rights-use drift")

        if source_root is not None:
            raw_path = source_root / locator["source_file_binding"]["upstream_relative_path"]
            require(raw_path.is_file(), f"{key}: missing external replay file {raw_path}")
            raw = raw_path.read_bytes()
            source = json.loads(raw)
            require(digest(raw) == binding["file_sha256"], f"{key}: external file hash drift")
            require(len(raw) == binding["byte_length"], f"{key}: external byte length drift")
            require(digest(canonical(source)) == binding["row_canonical_sha256"],
                    f"{key}: external canonical-row hash drift")
            require(digest(source["question"].encode("utf-8")) ==
                    binding["question_value_sha256_utf8"], f"{key}: question replay drift")
            require(digest(source["solution"].encode("utf-8")) ==
                    binding["solution_value_sha256_utf8"], f"{key}: solution replay drift")
            git_blob = hashlib.sha1(
                b"blob " + str(len(raw)).encode() + b"\0" + raw
            ).hexdigest()
            require(git_blob == binding["git_blob_sha1"], f"{key}: Git blob replay drift")
            replay_file_hashes.append(digest(raw))
            replay_question_hashes.append(binding["question_value_sha256_utf8"])
            replay_solution_hashes.append(binding["solution_value_sha256_utf8"])

    require(len(source_ids) == len(set(source_ids)) == 60, "source candidate IDs collide")
    require(len(semantic_keys) == len(set(semantic_keys)) == 62,
            "semantic keys are not 62 unique claims")

    # Regression guards for the material repairs and multipart decisions.
    by_key = {row["problem_key"]: row for row in rows}
    a6_statement = by_key["putnam_1983_a6"]["claim_review"]["independent_english_statement"]
    require("2/9" in a6_statement and "1/3" not in a6_statement,
            "1983-A6 regressed from the pinned 2/9 value")
    require(by_key["putnam_1987_b5"]["claim_review"]["source_claim_validity"] ==
            "false_as_printed_repaired_explicitly", "1987-B5 dimension repair lost")
    require("R^(2n)" in by_key["putnam_1987_b5"]["claim_review"]["independent_english_statement"],
            "1987-B5 repaired target dimension lost")
    for key in ("putnam_1985_b6", "putnam_1986_b6", "putnam_1987_b6"):
        require(set(by_key[key]["anomaly_codes"]) >= {
            "source_question_contains_end_itemize",
            "source_question_contains_end_document",
        }, f"{key}: trailing-source defect codes lost")

    dispositions = Counter(row["claim_review"]["claim_disposition"] for row in rows)
    validity = Counter(row["claim_review"]["source_claim_validity"] for row in rows)
    visibility = Counter(row["claim_review"]["answer_visibility"] for row in rows)
    anomalies = [code for row in rows for code in row["anomaly_codes"]]
    languages = Counter(language for row in rows
                        for language in row["variant_handling"]["formal_languages"])
    parent = json.loads(PARENT.read_bytes())
    parent_putnam_namespace_rows = [
        record for record in parent["records"]
        if "putnam" in canonical({
            name: record.get(name)
            for name in ("display_name", "curation_key", "formal_declaration")
        }).decode("utf-8").casefold()
    ]
    require(not parent_putnam_namespace_rows,
            "5.5 parent unexpectedly contains a Putnam namespace/source row")
    expected_counts = {
        "rows": 60,
        "reviewed_semantic_claims": 62,
        "claim_dispositions": dict(sorted(dispositions.items())),
        "split_children": sum(len(row["claim_review"]["children"]) for row in rows),
        "source_claim_validity": dict(sorted(validity.items())),
        "answer_visibility": dict(sorted(visibility.items())),
        "rows_with_explicit_source_defect_detail": sum(
            bool(row["claim_review"]["source_defect_detail"]) for row in rows
        ),
        "anomaly_occurrences": len(anomalies),
        "distinct_anomaly_codes": len(set(anomalies)),
        "putnambench_present": sum(row["putnambench_binding"]["present"] for row in rows),
        "putnambench_absent": sum(not row["putnambench_binding"]["present"] for row in rows),
        "formal_variant_headers": sum(row["variant_handling"]["formal_variant_count"] for row in rows),
        "formal_variant_languages": dict(sorted(languages.items())),
        "parent_5_5_putnam_namespace_rows": len(parent_putnam_namespace_rows),
        "rows_with_existing_5_5_candidates": 0,
    }
    require(summary["counts"] == expected_counts, "summary counts drift")
    expected_sets = {
        "problem_keys_sha256": set_digest(keys),
        "source_candidate_ids_sha256": set_digest(source_ids),
        "semantic_keys_sha256": set_digest(semantic_keys),
        "row_seals_sha256": set_digest([row["row_sha256"] for row in rows]),
    }
    require(summary["set_digests"] == expected_sets, "summary set digests drift")
    require(receipt["set_digests"] == expected_sets, "receipt set digests drift")
    require(summary["output"] == file_binding(REVIEW, 60), "summary output binding drift")
    require(receipt["review_output"] == file_binding(REVIEW, 60), "receipt output binding drift")
    require(receipt["review_summary"] == file_binding(SUMMARY, 1) | {
        "authority_sha256": summary["authority_sha256"]
    }, "receipt summary binding drift")
    require(receipt["publication_boundary"] == summary["publication_boundary"],
            "publication boundary differs between summary and receipt")
    boundary = summary["publication_boundary"]
    require(boundary["candidate_only"] is True and
            boundary["theorem_identity_credits_granted"] == 0 and
            boundary["conjecture_credits_granted"] == 0 and
            boundary["release_entries_granted"] == 0 and
            boundary["release_mutation_authorized_or_performed"] is False,
            "summary grants forbidden publication credit")

    input_paths = {
        "full_putnam_inventory": (FULL_INVENTORY, 1),
        "putnamgap_locator_manifest": (LOCATORS, len(locator_rows)),
        "full_putnam_source_candidates": (FULL_CANDIDATES, len(candidate_rows)),
        "full_putnam_seed_problems": (FULL_SEEDS, len(seed_rows)),
        "putnambench_inventory": (PB_INVENTORY, 1),
        "putnambench_source_problems": (PB_PROBLEMS, len(pb_rows)),
        "putnambench_formal_headers": (PB_HEADERS, len(header_rows)),
        "parent_5_5_catalog": (PARENT, 1),
    }
    for name, (path, count) in input_paths.items():
        require(summary["inputs"][name] == file_binding(path, count),
                f"summary input binding drift: {name}")
        require(receipt["source_authorities"][name] == summary["inputs"][name],
                f"receipt source binding drift: {name}")
    require(receipt["checks"]["noncatalog_seed_credit_boundary_enforced"] is True,
            "receipt zero-credit check missing")

    if source_root is not None:
        replay = summary["inputs"]["putnamgap"]["external_replay"]
        require(replay["files_replayed"] == 60, "summary external replay count drift")
        require(replay["file_sha256_set_digest"] == set_digest(replay_file_hashes),
                "external file set digest drift")
        require(replay["question_value_sha256_set_digest"] == set_digest(replay_question_hashes),
                "external question set digest drift")
        require(replay["solution_value_sha256_set_digest"] == set_digest(replay_solution_hashes),
                "external solution set digest drift")

    return {
        "rows": len(rows),
        "semantic_claims": len(semantic_keys),
        "putnambench_present": expected_counts["putnambench_present"],
        "formal_headers": expected_counts["formal_variant_headers"],
        "external_source_files_replayed": len(replay_file_hashes),
        "output_sha256": digest(review_payload),
        "summary_sha256": digest(summary_payload),
        "receipt_sha256": digest(receipt_payload),
        "summary_authority_sha256": summary["authority_sha256"],
        "receipt_authority_sha256": receipt["authority_sha256"],
        "theorem_credits": boundary["theorem_identity_credits_granted"],
        "conjecture_credits": boundary["conjecture_credits_granted"],
        "release_entries": boundary["release_entries_granted"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root", type=Path,
        help="optional clean PutnamGAP root for all 60 question/solution hash replays",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = check(args.source_root)
    except (CheckError, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        print(f"FAIL Putnam seed review 1983-1987: {error}", file=sys.stderr)
        return 1
    print("PASS Putnam seed review 1983-1987 " + json.dumps(
        result, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
