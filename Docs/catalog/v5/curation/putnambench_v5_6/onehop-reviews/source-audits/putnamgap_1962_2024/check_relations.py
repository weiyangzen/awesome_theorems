#!/usr/bin/env python3
"""Independent, read-only verifier for the PutnamGAP one-hop ledger.

This checker does not import the generator.  It reconstructs the source
universe, Git blob identities, decoded-solution spans, credit accounting, and
receipt hashes directly from files on disk.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "putnamgap_1962_2024_onehop_relations.json"
RECEIPT = ROOT / "receipt.json"
TREE = Path(os.environ.get("PUTNAMGAP_TREE_SNAPSHOT", "/tmp/putnamgap-tree.json"))
DATASET = Path(os.environ.get("PUTNAMGAP_DATASET_ROOT", "/tmp/putnamgap-audit.uYDPao/dataset"))
EXPECTED_COMMIT = "aee05407afc7e621e8d9c7f909f4f25ccb8131c0"
EXPECTED_TOP_KEYS = ["source", "rights", "counts", "edges"]
REQUIRED_EDGE_KEYS = {
    "edge_id",
    "problem_id",
    "target_identity_key",
    "target_display_name",
    "target_kind",
    "relation_type",
    "review_status",
    "review_method",
    "independently_written_target_summary",
    "evidence_summary",
    "source_locator",
    "verbatim_source_text_stored",
    "rights_boundary",
    "disposition",
    "reason",
    "credit_eligible",
    "discovery_only",
}
REQUIRED_LOCATOR_KEYS = {
    "source_id",
    "path",
    "url",
    "commit",
    "git_blob_sha",
    "file_sha256",
    "line_start",
    "line_end",
    "char_start",
    "char_end",
    "span_sha256",
}


def sha256(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def solution_field_line(raw_text: str) -> int:
    for number, line in enumerate(raw_text.splitlines(), 1):
        if re.match(r'^\s*"solution"\s*:', line):
            return number
    fail("source JSON has no top-level solution field line")


def recursive_keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from recursive_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from recursive_keys(nested)


def main() -> int:
    require(ARTIFACT.is_file(), f"artifact missing: {ARTIFACT}")
    require(RECEIPT.is_file(), f"receipt missing: {RECEIPT}")
    require(TREE.is_file(), f"tree snapshot missing: {TREE}")
    require(DATASET.is_dir(), f"dataset directory missing: {DATASET}")

    artifact_bytes = ARTIFACT.read_bytes()
    artifact = json.loads(artifact_bytes)
    receipt = json.loads(RECEIPT.read_bytes())
    tree = json.loads(TREE.read_bytes())

    require(list(artifact) == EXPECTED_TOP_KEYS, f"unexpected top-level keys/order: {list(artifact)}")
    require(tree.get("sha") == EXPECTED_COMMIT, "tree snapshot commit mismatch")
    require(tree.get("truncated") is False, "tree snapshot is truncated")
    require(artifact["source"].get("commit") == EXPECTED_COMMIT, "artifact source commit mismatch")
    require(receipt.get("source_commit") == EXPECTED_COMMIT, "receipt source commit mismatch")

    artifact_digest = sha256(artifact_bytes)
    require(receipt.get("artifact") == ARTIFACT.name, "receipt artifact path mismatch")
    require(receipt.get("artifact_sha256") == artifact_digest, "receipt artifact SHA-256 mismatch")
    checker_path = Path(__file__).resolve()
    require(receipt.get("checker") == checker_path.name, "receipt checker path mismatch")
    require(receipt.get("checker_sha256") == sha256(checker_path.read_bytes()), "receipt checker SHA-256 mismatch")
    require(receipt.get("source_tree_sha256") == sha256(TREE.read_bytes()), "receipt source-tree SHA-256 mismatch")

    tree_blobs = {
        entry["path"]: entry["sha"]
        for entry in tree.get("tree", [])
        if entry.get("type") == "blob"
    }

    # Reconstruct the complete 1962–2024 canonical grid independently.
    universe = {}
    for path in sorted(DATASET.glob("*.json")):
        match = re.fullmatch(r"(\d{4})-([AB])-([1-6])\.json", path.name)
        if not match or not (1962 <= int(match.group(1)) <= 2024):
            continue
        raw = path.read_bytes()
        raw_text = raw.decode("utf-8")
        decoded = json.loads(raw_text)
        problem_id = decoded.get("index")
        require(problem_id == path.stem, f"problem index/path mismatch: {path}")
        upstream_path = f"dataset/{path.name}"
        require(upstream_path in tree_blobs, f"tree lacks {upstream_path}")
        computed_blob = git_blob_sha1(raw)
        require(tree_blobs[upstream_path] == computed_blob, f"tree Git blob mismatch: {upstream_path}")
        universe[problem_id] = {
            "path": path,
            "upstream_path": upstream_path,
            "raw": raw,
            "raw_text": raw_text,
            "solution": decoded["solution"],
            "file_sha256": sha256(raw),
            "git_blob_sha": computed_blob,
            "solution_line": solution_field_line(raw_text),
        }

    require(len(universe) == 756, f"source universe is {len(universe)}, expected 756")
    expected_ids = {
        f"{year}-{side}-{number}"
        for year in range(1962, 2025)
        for side in ("A", "B")
        for number in range(1, 7)
    }
    require(set(universe) == expected_ids, "source universe is not the exact 63×12 grid")
    require(artifact["source"].get("problem_count") == 756, "artifact source problem_count mismatch")
    require(
        artifact["source"].get("decoded_solution_character_count")
        == sum(len(item["solution"]) for item in universe.values()),
        "decoded solution character total mismatch",
    )

    edges = artifact["edges"]
    require(isinstance(edges, list), "edges is not a list")
    require(len(edges) == 910, f"edge/discovery record count is {len(edges)}, expected 910")
    require(len({edge.get("edge_id") for edge in edges}) == len(edges), "edge_id values are not unique")

    banned_payload_keys = {"quote", "quotes", "snippet", "snippets", "trigger", "trigger_text", "source_text", "verbatim_text"}
    present_banned = banned_payload_keys.intersection(recursive_keys(edges))
    require(not present_banned, f"verbatim-bearing keys found: {sorted(present_banned)}")

    for position, edge in enumerate(edges):
        prefix = f"record[{position}]/{edge.get('edge_id', '?')}"
        missing = REQUIRED_EDGE_KEYS.difference(edge)
        require(not missing, f"{prefix}: missing edge keys {sorted(missing)}")
        require(edge["problem_id"] in universe, f"{prefix}: unknown problem_id")
        require(edge["verbatim_source_text_stored"] is False, f"{prefix}: verbatim flag is not false")
        require(isinstance(edge["independently_written_target_summary"], str) and edge["independently_written_target_summary"].strip(), f"{prefix}: empty target summary")
        require(isinstance(edge["evidence_summary"], str) and edge["evidence_summary"].strip(), f"{prefix}: empty evidence summary")
        require(isinstance(edge["rights_boundary"], str) and edge["rights_boundary"].strip(), f"{prefix}: empty rights boundary")
        require(edge["reason"] == edge.get("disposition_reason"), f"{prefix}: reason aliases disagree")

        locator = edge["source_locator"]
        missing_locator = REQUIRED_LOCATOR_KEYS.difference(locator)
        require(not missing_locator, f"{prefix}: missing locator keys {sorted(missing_locator)}")
        source = universe[edge["problem_id"]]
        expected_path = source["upstream_path"]
        require(locator["source_id"] == f"PutnamGAP:{edge['problem_id']}", f"{prefix}: source_id mismatch")
        require(locator["path"] == expected_path, f"{prefix}: source path mismatch")
        require(locator["commit"] == EXPECTED_COMMIT, f"{prefix}: commit mismatch")
        expected_url = f"https://raw.githubusercontent.com/YurenHao0426/PutnamGAP/{EXPECTED_COMMIT}/{expected_path}"
        require(locator["url"] == expected_url, f"{prefix}: pinned URL mismatch")
        require(locator["git_blob_sha"] == source["git_blob_sha"], f"{prefix}: Git blob SHA mismatch")
        require(locator["file_sha256"] == source["file_sha256"], f"{prefix}: file SHA-256 mismatch")
        require(locator["line_start"] == source["solution_line"], f"{prefix}: line_start mismatch")
        require(locator["line_end"] == source["solution_line"], f"{prefix}: line_end mismatch")
        start = locator["char_start"]
        end = locator["char_end"]
        require(type(start) is int and type(end) is int, f"{prefix}: offsets are not integers")
        require(0 <= start < end <= len(source["solution"]), f"{prefix}: decoded-solution offset bounds invalid")
        require(locator["span_sha256"] == sha256(source["solution"][start:end]), f"{prefix}: span SHA-256 mismatch")

        disposition = edge["disposition"]
        method = edge["review_method"]
        status = edge["review_status"]
        require(disposition in {"accepted", "candidate", "pending", "rejected"}, f"{prefix}: invalid disposition")
        if disposition == "accepted":
            require(method.startswith("manual_"), f"{prefix}: nonmanual record received accepted credit")
            require(status == "accepted_human_reviewed", f"{prefix}: accepted status mismatch")
            require(edge["credit_eligible"] is True, f"{prefix}: accepted record lacks credit")
            require(edge["discovery_only"] is False, f"{prefix}: accepted record marked discovery-only")
        elif disposition == "candidate":
            require(not method.startswith("manual_"), f"{prefix}: manual record incorrectly left as discovery candidate")
            require(status == "candidate_pending_human_review", f"{prefix}: candidate status mismatch")
            require(edge["credit_eligible"] is False, f"{prefix}: candidate received credit")
            require(edge["discovery_only"] is True, f"{prefix}: candidate is not marked discovery-only")
        elif disposition == "pending":
            require(method.startswith("manual_"), f"{prefix}: pending record was not manually classified")
            require(status.startswith("pending_"), f"{prefix}: pending status mismatch")
            require(edge["credit_eligible"] is False and edge["discovery_only"] is False, f"{prefix}: pending credit flags invalid")
        else:
            require(method.startswith("manual_"), f"{prefix}: rejected record was not manually classified")
            require(status == "rejected_nonclaim", f"{prefix}: rejected status mismatch")
            require(edge["target_kind"] == "topic_relation", f"{prefix}: rejection is not the audited topic-only record")
            require(edge["credit_eligible"] is False and edge["discovery_only"] is False, f"{prefix}: rejected credit flags invalid")

    dispositions = Counter(edge["disposition"] for edge in edges)
    review_statuses = Counter(edge["review_status"] for edge in edges)
    relation_types = Counter(edge["relation_type"] for edge in edges)
    target_kinds = Counter(edge["target_kind"] for edge in edges)
    accepted = [edge for edge in edges if edge["disposition"] == "accepted"]
    candidates = [edge for edge in edges if edge["disposition"] == "candidate"]
    pending = [edge for edge in edges if edge["disposition"] == "pending"]
    rejected = [edge for edge in edges if edge["disposition"] == "rejected"]
    accepted_conjectures = [edge for edge in accepted if edge["relation_type"] == "explicit_conjecture"]
    accepted_nonconjectures = [edge for edge in accepted if edge["relation_type"] != "explicit_conjecture"]
    open_conjectures = [edge for edge in accepted_conjectures if edge.get("conjecture_status") == "open_in_source"]
    resolved_conjectures = [edge for edge in accepted_conjectures if edge.get("conjecture_status") == "resolved_in_source"]
    covered = {edge["problem_id"] for edge in edges}
    accepted_covered = {edge["problem_id"] for edge in accepted}
    candidate_covered = {edge["problem_id"] for edge in candidates}
    tail_base = [edge for edge in edges if "1995_2024_key_proposition_base" in edge.get("coverage_roles", [])]
    tail_base_all = {edge["problem_id"] for edge in tail_base}
    tail_base_accepted = {edge["problem_id"] for edge in tail_base if edge["disposition"] == "accepted"}
    tail_base_candidates = {edge["problem_id"] for edge in tail_base if edge["disposition"] == "candidate"}
    conjecture_statuses = Counter(edge["conjecture_status"] for edge in edges if "conjecture_status" in edge)

    expected_counts = {
        "problems_in_source_universe": 756,
        "problems_with_any_edge": len(covered),
        "problems_without_any_edge": 756 - len(covered),
        "tail_1995_2024_problems": 360,
        "tail_1995_2024_with_discovery_key_proposition_record": len(tail_base_all),
        "tail_1995_2024_missing_discovery_key_proposition_record": 360 - len(tail_base_all),
        "edges_total": len(edges),
        "accepted_edges_total": len(accepted),
        "accepted_nonconjecture_proposition_edges": len(accepted_nonconjectures),
        "accepted_explicit_conjecture_edges": len(accepted_conjectures),
        "accepted_open_conjecture_edges": len(open_conjectures),
        "accepted_resolved_conjecture_edges": len(resolved_conjectures),
        "candidate_discovery_records": len(candidates),
        "pending_records": len(pending),
        "rejected_records": len(rejected),
        "problems_with_accepted_edge": len(accepted_covered),
        "problems_with_candidate_discovery": len(candidate_covered),
        "tail_1995_2024_accepted_key_proposition_base": len(tail_base_accepted),
        "tail_1995_2024_candidate_key_proposition_base": len(tail_base_candidates),
        "edges_by_relation_type": dict(sorted(relation_types.items())),
        "edges_by_review_status": dict(sorted(review_statuses.items())),
        "edges_by_target_kind": dict(sorted(target_kinds.items())),
        "explicit_conjectures_by_status": dict(sorted(conjecture_statuses.items())),
    }
    require(artifact["counts"] == expected_counts, "artifact counts do not equal independent reconstruction")
    require(receipt.get("counts") == expected_counts, "receipt counts do not equal independent reconstruction")
    require(dispositions == Counter({"candidate": 860, "accepted": 47, "pending": 2, "rejected": 1}), f"unexpected disposition totals: {dispositions}")

    invariants = receipt.get("invariants", {})
    require(all(value is True for value in invariants.values()), "receipt contains a false invariant")
    require(len(tail_base_all) == 360, "tail discovery base does not cover 360 problems")
    require(len(tail_base_accepted) == 0, "automatic tail base incorrectly received accepted credit")
    require(len(tail_base_candidates) == 360, "tail base candidates do not cover all 360 problems")

    print(
        "PASS putnamgap_onehop_relations "
        f"artifact_sha256={artifact_digest} "
        f"records={len(edges)} accepted={len(accepted)} "
        f"accepted_nonconjecture={len(accepted_nonconjectures)} "
        f"accepted_conjecture={len(accepted_conjectures)} "
        f"open={len(open_conjectures)} resolved={len(resolved_conjectures)} "
        f"candidate={len(candidates)} pending={len(pending)} rejected={len(rejected)} "
        f"source_universe={len(universe)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL putnamgap_onehop_relations: {exc}", file=sys.stderr)
        raise SystemExit(1)
