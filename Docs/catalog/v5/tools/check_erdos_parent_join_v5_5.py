#!/usr/bin/env python3
"""Independent validator for the pinned Erdős ↔ parent 5.4 join audit."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import tarfile
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
ERDOS_COMMIT = "af90db960021ff3247f0374e015dae97b5125ff6"
ERDOS_TREE = "931fc5b8a230485d49f095b59bbd30e6a0466455"
ERDOS_COMMIT_TIMESTAMP = "2026-08-09T21:27:45+00:00"
ERDOS_ARCHIVE_SHA256 = "a9125786b0ccf2da2c5411b0eb9c80f6b2cd2717d140606e136314e76bc0be58"
ERDOS_PROBLEMS_SHA256 = "14007c54a9ad0a9560966bd782f3303db898c6387df02754219dc585ef8b989d"
ERDOS_LICENSE_SHA256 = "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
ERDOS_SNAPSHOT_SHA256 = "5425b13a9d77ac3136cdea0f52d754f5f11ae8bff74943577f1b45c3bb665956"
ERDOS_SNAPSHOT_AUTHORITY = "8aeeda4f44f36240fc2ca752df5baae2ac30c31747b7c22d568edcae75e02601"
PARENT_CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
PARENT_LEDGER_SHA256 = "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3"
PARENT_MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
SCHEMA_VERSION = "awesome-theorems/erdos-parent-exact-join-audit/5.5"
DEFAULT_ARCHIVE = REPO_ROOT / "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz"
DEFAULT_SNAPSHOT = REPO_ROOT / "Docs/catalog/v5/sources/erdosproblems-status-af90db96.json"
DEFAULT_RELEASE_ROOT = REPO_ROOT / "Docs/catalog/v5/releases/5.4"
DEFAULT_ARTIFACT_ROOT = REPO_ROOT / "Docs/catalog/v5/curation/erdos_parent_join_v5_5"
RESOLVED_STATES = {"proved", "disproved", "solved"}
FINITE_STATES = {"falsifiable", "verifiable", "decidable", "not provable", "not disprovable", "independent"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    data = path.read_bytes()
    if data and not data.endswith(b"\n"):
        raise AssertionError(f"JSONL lacks final newline: {path}")
    rows = []
    for line_number, raw in enumerate(data.splitlines(), 1):
        value = json.loads(raw)
        assert raw == canonical(value), f"noncanonical JSON at {path}:{line_number}"
        rows.append(value)
    return rows


def load_json(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"JSON lacks final newline: {path}"
    value = json.loads(data)
    assert data[:-1] == canonical(value), f"noncanonical JSON: {path}"
    return value


def complete(record: dict[str, Any]) -> bool:
    statement = record.get("mathematical_statement") or {}
    return bool(
        record.get("truth_apt") is True
        and isinstance(statement.get("natural_language"), str)
        and statement["natural_language"].strip()
        and isinstance(statement.get("formal_type"), str)
        and statement["formal_type"].strip()
        and statement.get("completeness") not in {None, "incomplete"}
    )


def hash_without(value: dict[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return sha256(canonical({key: item for key, item in value.items() if key not in ignored}))


def normalized_status(value: Any) -> dict[str, Any]:
    assert isinstance(value, dict)
    state = value.get("state")
    assert isinstance(state, str) and state.strip()
    result: dict[str, Any] = {"state": state.strip()}
    last_update = value.get("last_update")
    if last_update is not None:
        text = last_update.isoformat() if hasattr(last_update, "isoformat") else str(last_update)
        assert re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text)
        result["last_update"] = text
    return result


def independently_rebuild_snapshot(archive_path: Path) -> dict[str, Any]:
    assert file_sha(archive_path) == ERDOS_ARCHIVE_SHA256
    with tarfile.open(archive_path, "r:gz") as stream:
        members = stream.getmembers()
        assert [member.name for member in members] == ["LICENSE", "data", "data/problems.yaml"]
        extracted: dict[str, bytes] = {}
        for member in members:
            if member.isdir():
                continue
            assert member.isfile() and not member.name.startswith("/") and ".." not in Path(member.name).parts
            handle = stream.extractfile(member)
            assert handle is not None
            extracted[member.name] = handle.read()
    assert sha256(extracted["data/problems.yaml"]) == ERDOS_PROBLEMS_SHA256
    assert sha256(extracted["LICENSE"]) == ERDOS_LICENSE_SHA256
    raw = yaml.safe_load(extracted["data/problems.yaml"].decode("utf-8"))
    assert isinstance(raw, list)
    records = []
    seen: set[int] = set()
    for source_index, item in enumerate(raw):
        assert isinstance(item, dict)
        number = int(item["number"])
        assert number > 0 and number not in seen
        seen.add(number)
        tags = item.get("tags", [])
        oeis = item.get("oeis", [])
        assert isinstance(tags, list) and all(isinstance(value, str) and value for value in tags)
        assert isinstance(oeis, list) and all(isinstance(value, str) and value for value in oeis)
        record = {
            "formal_status": normalized_status(item.get("formal_status")),
            "formalized": normalized_status(item.get("formalized")),
            "informal_status": normalized_status(item.get("informal_status")),
            "oeis_a_numbers": sorted({value for value in oeis if re.fullmatch(r"A[0-9]{6}", value)}),
            "oeis_raw": oeis,
            "prize": item.get("prize"),
            "problem_number": number,
            "source_index": source_index,
            "status": normalized_status(item.get("status")),
            "tags": tags,
            "upstream_page": f"https://www.erdosproblems.com/{number}",
        }
        record["row_sha256"] = hash_without(record, "row_sha256")
        records.append(record)
    records.sort(key=lambda row: row["problem_number"])
    assert len(records) == 1217
    document = {
        "counts": {
            "by_status": dict(sorted(collections.Counter(row["status"]["state"] for row in records).items())),
            "records": len(records),
            "records_with_oeis_a_number": sum(bool(row["oeis_a_numbers"]) for row in records),
            "records_with_oeis_metadata": sum(bool(row["oeis_raw"]) for row in records),
            "records_with_prize": sum(row["prize"] not in (None, "", "no") for row in records),
        },
        "evidence_boundary": {
            "problem_existence_grants_catalog_credit": False,
            "role": "current_status_importance_and_classification_metadata_join",
            "status_disclaimer": (
                "The upstream website states that open status reflects its owner's current belief and may miss "
                "literature; qualifying release rows still require independent status and statement review."
            ),
            "status_metadata_alone_grants_theorem_or_conjecture_credit": False,
        },
        "records": records,
        "schema_version": "awesome-theorems/erdosproblems-status-snapshot/1.0",
        "set_digests": {
            "problem_number_set_sha256": sha256(canonical(sorted(seen))),
            "row_sha256_set_sha256": sha256(canonical(sorted(row["row_sha256"] for row in records))),
        },
        "source": {
            "archive_path": "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz",
            "archive_sha256": ERDOS_ARCHIVE_SHA256,
            "commit": ERDOS_COMMIT,
            "commit_timestamp": ERDOS_COMMIT_TIMESTAMP,
            "license": "Apache-2.0",
            "license_path": "LICENSE",
            "license_sha256": ERDOS_LICENSE_SHA256,
            "problems_path": "data/problems.yaml",
            "problems_sha256": ERDOS_PROBLEMS_SHA256,
            "repository": "https://github.com/teorth/erdosproblems",
            "tree": ERDOS_TREE,
        },
    }
    document["authority_sha256"] = hash_without(document, "authority_sha256")
    return document


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--release-root", type=Path, default=DEFAULT_RELEASE_ROOT)
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    archive_path = args.archive.resolve()
    snapshot_path = args.snapshot.resolve()
    release_root = args.release_root.resolve()
    artifact_root = args.artifact_root.resolve()
    expected_snapshot = independently_rebuild_snapshot(archive_path)
    assert file_sha(snapshot_path) == ERDOS_SNAPSHOT_SHA256
    snapshot = load_json(snapshot_path)
    assert snapshot == expected_snapshot
    assert snapshot["authority_sha256"] == ERDOS_SNAPSHOT_AUTHORITY
    catalog_path = release_root / "Claim_Catalog.json"
    ledger_path = release_root / "Strict_Conjecture_Ledger.json"
    manifest_path = release_root / "Release_Manifest.json"
    assert file_sha(catalog_path) == PARENT_CATALOG_SHA256
    assert file_sha(ledger_path) == PARENT_LEDGER_SHA256
    assert file_sha(manifest_path) == PARENT_MANIFEST_SHA256

    source_list = snapshot["records"]
    source = {row["problem_number"]: row for row in source_list}
    assert len(source) == len(source_list) == 1217
    catalog = json.loads(catalog_path.read_bytes())
    ledger = json.loads(ledger_path.read_bytes())
    assert catalog["release"] == ledger["release"] == "5.4"

    effective_credit = {
        row["stage_claim_id"]: row
        for row in ledger["strict_credits"]
        if row.get("grants_strict_conjecture_credit") is True
    }
    for row in ledger.get("credit_corrections", []):
        if row.get("grants_strict_conjecture_credit") is False:
            effective_credit.pop(row["stage_claim_id"], None)

    expected_parent: list[tuple[int, int, dict[str, Any]]] = []
    for index, record in enumerate(catalog["records"]):
        module_match = re.fullmatch(r"FormalConjectures\.ErdosProblems\.(\d+)", record.get("module", ""))
        if not module_match:
            continue
        qname_match = re.match(r"^Erdos(\d+)\.", record["qualified_name"])
        assert qname_match and qname_match.group(1) == module_match.group(1)
        number = int(module_match.group(1))
        assert number in source
        expected_parent.append((index, number, record))
    assert len(expected_parent) == 1495
    assert len({number for _, number, _ in expected_parent}) == 571
    assert all(complete(record) for _, _, record in expected_parent)
    assert all(record["atomicity"] == "atomic" for _, _, record in expected_parent)
    assert all(record["dedupe"]["verdict"] == "unique_exact_source_declaration" for _, _, record in expected_parent)

    source_rows = load_jsonl(artifact_root / "source-problems.jsonl")
    join_rows = load_jsonl(artifact_root / "parent-erdos-join.jsonl")
    groups = load_jsonl(artifact_root / "problem-groups.jsonl")
    current_open = load_jsonl(artifact_root / "current-open-identities.jsonl")
    existing_credits = load_jsonl(artifact_root / "existing-strict-credits.jsonl")
    polarity_backlog = load_jsonl(artifact_root / "polarity-review-backlog.jsonl")
    new_credit_candidates = load_jsonl(artifact_root / "new-credit-review-candidates.jsonl")
    conflicts = load_jsonl(artifact_root / "status-conflicts.jsonl")
    resolved_theorems = load_jsonl(artifact_root / "resolved-theorem-rows.jsonl")
    resolved_file_capacity = load_jsonl(artifact_root / "resolved-theorem-file-capacity.jsonl")
    resolved_max2 = load_jsonl(artifact_root / "resolved-theorem-max2-selected.jsonl")
    solved_upstream_open_drift = load_jsonl(
        artifact_root / "research-solved-upstream-open-drift.jsonl"
    )
    summary = load_json(artifact_root / "summary.json")
    receipt = load_json(artifact_root / "receipt.json")

    assert len(source_rows) == 1217
    for index, (raw, row) in enumerate(zip(source_list, source_rows, strict=True)):
        number = raw["problem_number"]
        assert row["source_index"] == index
        assert row["problem_number"] == number
        assert row["problem_number_text"] == str(number)
        assert row["prize"] == raw.get("prize")
        assert row["tags"] == raw.get("tags", [])
        assert row["derived_status"] == raw.get("status", {})
        assert row["informal_status"] == raw.get("informal_status", {})
        assert row["last_update"] == raw.get("status", {}).get("last_update")
        assert row["source_record_sha256"] == raw["row_sha256"]
        assert row["source_snapshot_authority_sha256"] == ERDOS_SNAPSHOT_AUTHORITY
        assert row["is_current_exact_open"] is (raw["informal_status"]["state"] == "open")

    assert len(join_rows) == len(expected_parent)
    identity_keys: set[str] = set()
    expected_current_ids: list[str] = []
    expected_credit_ids: list[str] = []
    expected_polarity_ids: list[str] = []
    expected_candidate_ids: list[str] = []
    expected_conflict_ids: list[str] = []
    for row, (catalog_index, number, parent) in zip(join_rows, expected_parent, strict=True):
        source_row = source[number]
        sid = parent["stage_claim_id"]
        assert row["schema_version"] == SCHEMA_VERSION
        assert row["exact_join"]["key"] == str(number)
        assert row["exact_join"]["source_problem_number"] == number
        assert row["exact_join"]["module_problem_number"] == number
        assert row["exact_join"]["qualified_name_problem_number"] == number
        assert row["parent"]["catalog_index"] == catalog_index
        assert row["parent"]["stage_claim_id"] == sid
        assert row["parent"]["qualified_name"] == parent["qualified_name"]
        assert row["parent"]["module"] == parent["module"]
        assert row["parent"]["locator"] == parent["locator"]
        assert row["parent"]["mathematical_statement"] == parent["mathematical_statement"]
        assert row["parent"]["truth_apt"] == parent["truth_apt"]
        assert row["statement_gate"]["complete_truth_apt"] is True
        assert row["source_problem"]["problem_number"] == number
        assert row["source_problem"]["informal_status"] == source_row["informal_status"]
        assert row["source_problem"]["derived_status"] == source_row["status"]
        assert row["source_problem"]["prize"] == source_row.get("prize")
        assert row["source_problem"]["tags"] == source_row.get("tags", [])
        assert row["source_problem"]["source_record_sha256"] == source_row["row_sha256"]
        assert row["source_problem"]["source_snapshot_authority_sha256"] == ERDOS_SNAPSHOT_AUTHORITY
        assert row["credit"]["existing_strict_credit"] is (sid in effective_credit)
        assert row["credit"]["problem_presence_grants_credit"] is False
        assert row["credit"]["grants_new_credit_from_this_audit"] is False
        identity_key = row["identity"]["semantic_identity_key"]
        assert identity_key.endswith(parent["dedupe"]["identity_payload_sha256"])
        assert row["identity"]["exact_identity_duplicate_group_size"] == 1
        assert row["identity"]["exact_identity_duplicate_stage_claim_ids"] == [sid]
        assert identity_key not in identity_keys
        identity_keys.add(identity_key)

        source_open = source_row["informal_status"]["state"] == "open"
        selected_current = source_open and parent["material_status"] == "open" and complete(parent)
        if selected_current:
            expected_current_ids.append(sid)
        if sid in effective_credit:
            expected_credit_ids.append(sid)
        if selected_current and sid not in effective_credit and parent["current_claim_kind"] == "open_problem":
            expected_polarity_ids.append(sid)
            assert row["credit"]["assessment"] == "question_has_no_asserted_conjectural_direction"
        if row["credit"]["new_credit_review_candidate"]:
            expected_candidate_ids.append(sid)
            assert parent["current_claim_kind"] == "conjecture"
            assert selected_current and sid not in effective_credit
        if source_row["informal_status"]["state"] in RESOLVED_STATES and parent["material_status"] == "open":
            expected_conflict_ids.append(sid)
            assert row["status_relation"] == "parent_open_conflicts_with_current_problem_resolution"
        if source_open and parent["current_claim_kind"] == "theorem":
            assert row["credit"]["assessment"] == "theorem_subclaim_not_conjecture_credit"

    def ids(rows: list[dict[str, Any]]) -> list[str]:
        return [row["parent"]["stage_claim_id"] for row in rows]

    assert ids(current_open) == expected_current_ids
    assert ids(existing_credits) == expected_credit_ids
    assert ids(polarity_backlog) == expected_polarity_ids
    assert ids(new_credit_candidates) == expected_candidate_ids == []
    assert ids(conflicts) == expected_conflict_ids
    assert len(current_open) == 369
    assert len(existing_credits) == 123
    assert len(polarity_backlog) == 263
    assert len(conflicts) == 26
    assert len(groups) == 571
    assert [row["problem_number"] for row in groups] == sorted({number for _, number, _ in expected_parent})
    assert len({row["identity"]["semantic_identity_key"] for row in current_open}) == 369
    assert collections.Counter(row["parent"]["current_claim_kind"] for row in current_open) == {
        "conjecture": 106,
        "open_problem": 263,
    }
    assert collections.Counter(row["identity"]["role_within_problem"] for row in current_open) == {
        "base": 169,
        "variant": 126,
        "part": 66,
        "other_subclaim": 8,
    }
    assert sum(
        row["credit"]["existing_strict_credit"]
        and row["source_problem"]["informal_status"]["state"] in RESOLVED_STATES
        for row in join_rows
    ) == 8
    assert sum(
        row["credit"]["existing_strict_credit"]
        and row["source_problem"]["informal_status"]["state"] in FINITE_STATES
        for row in join_rows
    ) == 9

    research_solved_expected = [
        row
        for row in join_rows
        if row["parent"]["current_claim_kind"] == "theorem"
        and row["parent"]["raw_status"] == "research solved"
    ]
    resolved_expected = [
        row
        for row in research_solved_expected
        if row["source_problem"]["informal_status"]["state"] in RESOLVED_STATES
    ]
    open_drift_expected = [
        row
        for row in research_solved_expected
        if row["source_problem"]["informal_status"]["state"] == "open"
    ]
    assert len(research_solved_expected) == 1002
    assert ids(resolved_theorems) == ids(resolved_expected)
    assert len(resolved_theorems) == 546
    assert len({row["source_problem"]["problem_number"] for row in resolved_theorems}) == 249
    assert len({row["parent"]["locator"]["member_path"] for row in resolved_theorems}) == 249
    assert len(resolved_file_capacity) == 249
    assert len(resolved_max2) == 379
    selected_by_file: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in resolved_max2:
        selection = row["theorem_selection"]
        member = row["parent"]["locator"]["member_path"]
        selected_by_file[member].append(row)
        assert selection["eligible_after_upstream_resolved_filter"] is True
        assert selection["max_per_formal_conjectures_file"] == 2
        assert selection["rank_within_file"] in {1, 2}
        assert selection["frontier_credit_allowed_from_problem_status_alone"] is False
        binding = selection["source_problem_binding"]
        number = row["source_problem"]["problem_number"]
        assert binding["problem_page_url"] == f"https://www.erdosproblems.com/{number}"
        assert binding["current_status_locator"]["informal_status"] == source[number]["informal_status"]
        assert binding["current_status_locator"]["derived_status"] == source[number]["status"]
        assert binding["current_status_locator"]["pinned_source_record_sha256"] == source[number]["row_sha256"]
        assert binding["current_status_locator"]["pinned_archive_sha256"] == ERDOS_ARCHIVE_SHA256
        assert binding["current_status_locator"]["pinned_snapshot_authority_sha256"] == ERDOS_SNAPSHOT_AUTHORITY
        assert binding["bibliography_locator"]["container_anchor"].endswith(f"#bib-container{number}")
        assert binding["remarks_locator"]["history_url"].endswith(f"/history/{number}")
        assert binding["remarks_locator"]["latex_url"].endswith(f"/latex/{number}")
    assert all(len(rows) <= 2 for rows in selected_by_file.values())
    expected_selected_ids: list[str] = []
    expected_by_file: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in resolved_expected:
        expected_by_file[row["parent"]["locator"]["member_path"]].append(row)
    for member in sorted(expected_by_file):
        rows = sorted(expected_by_file[member], key=lambda item: item["parent"]["catalog_index"])
        expected_selected_ids.extend(ids(rows[:2]))
    assert ids(resolved_max2) == expected_selected_ids
    assert len(solved_upstream_open_drift) == len(open_drift_expected) == 414
    assert ids(solved_upstream_open_drift) == ids(open_drift_expected)
    assert len({row["source_problem"]["problem_number"] for row in solved_upstream_open_drift}) == 185
    assert len({row["parent"]["locator"]["member_path"] for row in solved_upstream_open_drift}) == 185
    for row in solved_upstream_open_drift:
        drift = row["theorem_status_drift"]
        assert drift["classification"] == "parent_research_solved_but_upstream_problem_current_open"
        assert drift["frontier_credit_allowed"] is False
        assert drift["source_problem_binding"]["current_status_locator"]["informal_status"]["state"] == "open"

    assert summary["source_counts"]["problems"] == 1217
    assert summary["source_counts"]["current_exact_open"] == 608
    assert summary["source_counts"]["current_unresolved_broad"] == 661
    assert summary["join_counts"]["parent_erdos_records"] == 1495
    assert summary["join_counts"]["represented_source_problem_numbers"] == 571
    assert summary["join_counts"]["complete_truth_apt_parent_rows"] == 1495
    assert summary["current_open_identity_inventory"]["complete_truth_apt_distinct_identities"] == 369
    assert summary["current_open_identity_inventory"]["existing_strict_credit"] == 106
    assert summary["current_open_identity_inventory"]["uncredited"] == 263
    assert summary["credit_accounting"]["existing_erdos_strict_credits"] == 123
    assert summary["credit_accounting"]["mechanically_addable_new_credit"] == 0
    assert summary["credit_accounting"]["new_credit_review_candidates_with_asserted_conjecture_kind"] == 0
    assert summary["credit_accounting"]["grants_new_credit_from_audit"] == 0
    theorem_summary = summary["research_solved_theorem_inventory"]
    assert theorem_summary["research_solved_rows_before_upstream_filter"] == 1002
    assert theorem_summary["resolved_filtered_rows"] == 546
    assert theorem_summary["resolved_filtered_distinct_problem_numbers"] == 249
    assert theorem_summary["resolved_filtered_distinct_formal_files"] == 249
    assert theorem_summary["resolved_filtered_by_derived_status_including_lean"] == {
        "disproved": 31,
        "disproved (Lean)": 135,
        "proved": 91,
        "proved (Lean)": 203,
        "solved": 28,
        "solved (Lean)": 58,
    }
    assert theorem_summary["resolved_filtered_by_informal_status"] == {
        "disproved": 166,
        "proved": 294,
        "solved": 86,
    }
    assert theorem_summary["max2_per_file_available_count"] == 379
    assert theorem_summary["upstream_open_drift_rows"] == 414
    assert theorem_summary["upstream_open_drift_distinct_problem_numbers"] == 185
    assert theorem_summary["upstream_open_drift_distinct_formal_files"] == 185
    assert theorem_summary["upstream_open_drift_frontier_credit_allowed"] is False
    assert summary["release_mutation"] is False

    receipt_without_authority = dict(receipt)
    authority = receipt_without_authority.pop("authority_sha256")
    assert authority == sha256(canonical(receipt_without_authority))
    assert receipt["release_mutation"] is False
    assert receipt["source_snapshot"]["commit"] == ERDOS_COMMIT
    assert receipt["source_snapshot"]["tree"] == ERDOS_TREE
    assert receipt["source_snapshot"]["archive_sha256"] == ERDOS_ARCHIVE_SHA256
    assert receipt["source_snapshot"]["status_snapshot_file_sha256"] == ERDOS_SNAPSHOT_SHA256
    assert receipt["source_snapshot"]["status_snapshot_authority_sha256"] == ERDOS_SNAPSHOT_AUTHORITY
    assert receipt["source_snapshot"]["archive_path"] == "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz"
    assert receipt["source_snapshot"]["status_snapshot_path"] == "Docs/catalog/v5/sources/erdosproblems-status-af90db96.json"
    assert receipt["output_root"] == "Docs/catalog/v5/curation/erdos_parent_join_v5_5"
    assert receipt["build_command"] == "python3 Docs/catalog/v5/tools/build_erdos_parent_join_v5_5.py"
    assert receipt["validation_command"] == "python3 Docs/catalog/v5/tools/check_erdos_parent_join_v5_5.py"
    assert receipt["mutation_test_command"] == "python3 Docs/catalog/v5/tools/test_erdos_parent_join_v5_5.py"
    assert receipt["summary_sha256"] == file_sha(artifact_root / "summary.json")
    data_prefix = "Docs/catalog/v5/curation/erdos_parent_join_v5_5/"
    for artifact in receipt["artifact_inventory"]:
        relative = artifact["path"]
        assert not Path(relative).is_absolute() and ".." not in Path(relative).parts
        if relative.startswith(data_prefix):
            path = artifact_root / Path(relative).name
        else:
            path = repo_root / relative
        assert path.exists()
        data = path.read_bytes()
        assert artifact["file_sha256"] == sha256(data)
        assert artifact["size_bytes"] == len(data)
        assert artifact["line_count"] == len(data.splitlines())

    result = {
        "current_open_complete_distinct_identities": len(current_open),
        "existing_strict_credit_among_current_open": sum(
            row["credit"]["existing_strict_credit"] for row in current_open
        ),
        "mechanically_addable_new_credit": len(new_credit_candidates),
        "parent_erdos_rows": len(join_rows),
        "polarity_review_backlog": len(polarity_backlog),
        "resolved_research_solved_theorem_rows": len(resolved_theorems),
        "resolved_theorem_max2_per_file": len(resolved_max2),
        "receipt_authority_sha256": authority,
        "represented_problem_numbers": len(groups),
        "source_problems": len(source_rows),
        "status_conflicts": len(conflicts),
        "upstream_open_research_solved_drift_rows": len(solved_upstream_open_drift),
        "validation": "passed",
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
