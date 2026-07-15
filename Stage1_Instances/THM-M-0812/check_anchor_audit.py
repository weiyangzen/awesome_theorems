#!/usr/bin/env python3
"""Validate the bounded immutable THM-M-0812 formal-anchor inventory."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0812-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0812"
BASE_REVISION = "647eb08e6581ada8fde2fbcd0c9e58e142d3dc72"
BASE_TREE = "1a7772398b00170f5a21c9b4dc1bf30de0cebb0c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
INVENTORY_VERSION = "THM-M-0812-anchor-inventory/1"
CUTOFF = "2026-07-15T16:17:50+08:00"
EXPRESSION_SHA256 = "b20dc7426179377f6838e3ca384aaa80431d00713953494a5ea789d84ec1d7b4"
STATEMENT_BUNDLE_SHA256 = "8b8107e613a53247d69c71d1a838fd4719b3c0330e4a707b54060bd9247dc0f1"
STATEMENT_SHA256 = "526bad3f7d42bccb3e9bd263a10c1fc7ebb10e5136eb0ef9cd13131941ea3242"
STATEMENT_JSON_SHA256 = "f32673aef16457b8cf147354dd3404c6515bb2bfb909fc76bf5e68ef9fdf0741"
PROTOCOL_SHA256 = "72220b7aebd96d8234308670fca23a1b4e2a1a2ff1dd84fcb53a2e33707e54eb"
ANCHOR_SHA256 = "22042be0542074aa9621c07e495b5bec4b7291212172c12095b04b4a2f652715"
ANCHOR_OUTPUT_SHA256 = "27903d9622abe8400b46d330d3235fa67356981d7030c737c5c2b40df356d997"
STATEMENT_OUTPUT_SHA256 = "e9c73fc4c1021c91d3f56631341936c638f1d65b5302435fe9e78881860c450e"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
PR_REVISION = "6cfc4b1f77aef6f7f70f8f733cefa8eafc5a3497"
INVENTORY_MEMBERS = {
    "M0812-C01-REPO-LOCAL-EXACT-STATEMENT",
    "M0812-C02-REPO-LOCAL-NONCANDIDATES",
    "M0812-C03-MATHLIB-EXACT-TOPIC",
    "M0812-C04-MATHLIB-SUBSTRATE",
    "M0812-C05-MANIFEST-PINNED-EXTERNALS",
    "M0812-C06-FORMAL-CONJECTURES-SUPPORT",
    "M0812-C07-ATLAS-KONIG",
    "M0812-C08-MATHLIB-PR33032",
    "M0812-C09-PUBLIC-SEARCH-BOUNDARY",
    "M0812-C10-HUMAN-SOURCE-BOUNDARY",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "76b93660b56c11b647dfa9fe0707623df47096e0c86ef58ff01bc0fc97dc4d33",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "2ba8febb2a3eaf726e2f2bbcadc4f565b89b8182331fabc6a8b1bde8946fe539",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    f"Stage1_Instances/{THEOREM_ID}/Statement.lean": STATEMENT_SHA256,
    f"Stage1_Instances/{THEOREM_ID}/statement.json": STATEMENT_JSON_SHA256,
}
MATHLIB_FILES = {
    "Mathlib/Combinatorics/SimpleGraph/Bipartite.lean": (
        "7263d4c6eed57420f67b01639947965ec952d74c",
        "5402f4cd073b757a9d1bd127cbbca9f9a2b0750c8c9edb7e2361df32312acf3f",
    ),
    "Mathlib/Combinatorics/SimpleGraph/Matching.lean": (
        "1c4940a10d3d4c6fc6462bd43ffa2e70ced8dacf",
        "7e8b873ee73808358dd1d1a36e0c72cd4b27f95b7ba29f23286d3f076f8abc4b",
    ),
    "Mathlib/Combinatorics/SimpleGraph/VertexCover.lean": (
        "be8d9555b09f9be0f9e49bebb1d15118f9d05f37",
        "9d2aa284bbb0dc4729150041af31856e9fa2636c8a4da5de49b098f2fdb95b3a",
    ),
    "Mathlib/Combinatorics/SimpleGraph/Hall.lean": (
        "6bd653c1e0cec51aadbd460e67919d9499226f97",
        "e7ffa1e4de6af950973d02725efd8d2bbbb015e2f05b4b45a52148244a2a5f5e",
    ),
    "Mathlib/Combinatorics/Hall/Basic.lean": (
        "5cda9c0e906803f10f1f50b916d564ebb443ac95",
        "dab48f10ac7d10b7190b88f8b7e2447b55be1af098358a9f5318d66c675b2382",
    ),
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def candidate(audit: dict, candidate_id: str) -> dict:
    return next(row for row in audit["candidates"] if row["candidate_id"] == candidate_id)


def without_comments_and_strings(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', source)


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        raise SystemExit(f"missing final newline: {path}")
    if b"\r" in data or b"\x00" in data:
        raise SystemExit(f"invalid byte in {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        raise SystemExit(f"trailing whitespace in {path}")


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"})
    return subprocess.run(
        ["lake", "env", "lean", os.path.relpath(path, LEAN_ROOT)],
        cwd=LEAN_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def serialized_target(result: subprocess.CompletedProcess[str], declaration: str) -> str:
    marker = f"def {declaration}"
    index = result.stdout.rfind(marker)
    if index < 0:
        raise SystemExit(f"missing serialized target: {declaration}")
    tail = result.stdout[index:]
    if " : Prop :=\n" not in tail:
        raise SystemExit(f"malformed serialized target: {declaration}")
    expression = tail.split(" : Prop :=\n", 1)[1].strip()
    if "?m." in expression:
        raise SystemExit(f"unresolved metavariable in target: {declaration}")
    return expression


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path, default=ROOT / ".stage1-worker-selftest.json")
    args = parser.parse_args()

    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(args.worker_packet)

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1371
    assert audit["base_revision"] == protocol["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == protocol["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1371
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0812-STATEMENT")
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]" and predecessor["state"] == "[_]"
    assert item["depends_on"] == ["S56-M-0812-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Audit mathlib and external Lean 4 candidates at immutable revisions."

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == audit["canonical_target"]
    assert formal["elaborated_expression_sha256"] == audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_bundle_sha256"] == audit["canonical_statement_bundle_sha256"] == STATEMENT_BUNDLE_SHA256
    assert formal["statement_file_sha256"] == audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "statement.json") == STATEMENT_JSON_SHA256

    assert protocol["inventory_version"] == audit["inventory_version"] == INVENTORY_VERSION
    assert protocol["frozen_at"] == protocol["cutoff"] == audit["cutoff"] == CUTOFF
    assert protocol["saturation_claim"] is False
    assert set(protocol["inventory_members"]) == INVENTORY_MEMBERS
    assert {row["candidate_id"] for row in audit["candidates"]} == INVENTORY_MEMBERS
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256
    assert receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256

    environment = audit["immutable_environment"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256
    assert sha256(LEAN_ROOT / "lean-toolchain") == environment["lean_toolchain_file_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == environment["lake_manifest_sha256"]
    for path, (blob, digest) in MATHLIB_FILES.items():
        assert output("git", "rev-parse", f"HEAD:{path}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / path) == digest

    local = candidate(audit, "M0812-C01-REPO-LOCAL-EXACT-STATEMENT")
    assert local["candidate_classification"] == "M3_exact_statement_only"
    assert local["evidence_level"] == "E3" and local["terminal_proof_body"] is None
    assert candidate(audit, "M0812-C02-REPO-LOCAL-NONCANDIDATES")["searched_tracked_lean_file_count"] == 2827
    exact_mathlib = candidate(audit, "M0812-C03-MATHLIB-EXACT-TOPIC")
    assert exact_mathlib["searched_library_lean_file_count"] == 7871
    assert exact_mathlib["candidate_classification"] == "no_exact_candidate"
    substrate = candidate(audit, "M0812-C04-MATHLIB-SUBSTRATE")
    assert substrate["candidate_classification"] == "M3_support_only"
    assert substrate["machine_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert candidate(audit, "M0812-C05-MANIFEST-PINNED-EXTERNALS")["searched_lean_file_count"] == 9676

    formal_conjectures = candidate(audit, "M0812-C06-FORMAL-CONJECTURES-SUPPORT")
    assert formal_conjectures["revision"] == "b2e608fc52d765510915a244bb69b1a2741acc3c"
    assert formal_conjectures["file_sha256"] == "c7d3ecd6e13b82ea8daa6c1fc0156c5371e8e5e774dc496bb81d2c184a39ac24"
    assert formal_conjectures["candidate_classification"] == "M3_external_support_only"
    atlas = candidate(audit, "M0812-C07-ATLAS-KONIG")
    assert atlas["revision"] == ATLAS_REVISION
    assert atlas["file_sha256"] == "15aac02e02d67d36d1ff8ec0cda4a73c8bb6270ae88deb2f8519bdb0c99855d1"
    assert atlas["transitive_placeholder"]["token"] == "sorry"
    assert "sorryAx" in atlas["machine_axioms"]
    assert atlas["candidate_classification"] == "M5_placeholder_and_statement_bridge_blocked"
    pull_request = candidate(audit, "M0812-C08-MATHLIB-PR33032")
    assert pull_request["revision"] == PR_REVISION
    assert pull_request["tree"] == "a94eee877a43b09cc0748e862fffe774de606ff1"
    assert pull_request["state_at_cutoff"] == "closed and unmerged"
    assert pull_request["current_pin_replay"]["exit"] == 1
    assert pull_request["candidate_classification"] == "M5_unintegrated_toolchain_and_statement_bridge_blocked"
    assert {entry["blob"] for entry in pull_request["files"]} == {
        "8e50f47f635b2c143c585820dafba49fb82ed497",
        "4bdc03b6c00cd2e0c3857c11fd4de72372892b06",
        "a59c3026476e2c3edb37db2750ea4f3a6fd9ab61",
        "31c555ba2999061756069512fc638719c11d078b",
    }

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("10/10")
    assert result["exact_statement_candidate_located"] is True
    assert result["exact_proof_candidate_located"] is False
    assert result["credible_near_exact_lean4_candidate_located"] is True
    assert result["candidate_kernel_checked_under_repository_pin"] is False
    assert result["independent_exact_external_lean4_terminal_body_found"] is False
    assert result["eligible_external_integration_debt"] is False
    assert result["root_machine_debt_before"] == result["strongest_exact_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E3 exact-statement evidence only; external candidates receive no root proof tier"
    assert result["discovery_protocol_evidence_complete"] is False
    assert "per-query" in result["discovery_protocol_evidence_blocker"]
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is result["theorem_complete"] is False
    expected_vector = {"H": "H1", "M": "M3", "R": "R2"}
    assert audit["root_vector_before"] == audit["root_vector_after"] == expected_vector
    assert audit["accepted_receipt_ids"] == []

    assert receipt["phase"] == "anchor_audit" and receipt["assigned_layer"] == 2
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["known_failures"] == packet["known_failures"] == audit["known_failures"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == expected_vector
    assert receipt["anchor_source_sha256"] == ANCHOR_SHA256
    assert receipt["lean_output_sha256"] == ANCHOR_OUTPUT_SHA256
    assert receipt["statement_lean_output_sha256"] == STATEMENT_OUTPUT_SHA256
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["base_revision"] == BASE_REVISION
    for path, digest in SOURCE_INPUTS.items():
        assert receipt["source_inputs"][path] == f"sha256:{digest}"
        assert sha256(ROOT / path) == digest

    actual_changed = {
        line[3:]
        for line in output("git", "status", "--short", "--untracked-files=all").splitlines()
    }
    assert actual_changed - {"Formalizations/Lean/.lake"} == CHANGED_PATHS

    anchor_path = HERE / "AnchorAudit.lean"
    anchor = anchor_path.read_text(encoding="utf-8")
    assert sha256(anchor_path) == ANCHOR_SHA256
    for marker in (
        "def IsEdgeMatching",
        "def IsBipartiteVertexCover",
        "def HasMatchingNumber",
        "def HasVertexCoverNumber",
        "def ExactTarget",
        "#check SimpleGraph.vertexCoverNum",
        "#check SimpleGraph.exists_isMatching_of_forall_ncard_le",
        "#check_failure (SimpleGraph.vertexCoverNum_exists",
        "#print sorries SimpleGraph.vertexCoverNum_exists",
        "#print Stage1Instances.THM_M_0812.ExactTarget",
    ):
        assert marker in anchor, marker
    stripped = without_comments_and_strings(anchor)
    stripped = re.sub(r"^#print sorries .*?$", "", stripped, flags=re.MULTILINE)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe|native_decide|implemented_by|extern)\b"
    )
    assert forbidden.search(stripped) is None

    statement_result = run_lean(HERE / "Statement.lean")
    anchor_result = run_lean(anchor_path)
    for name, lean_result in (("statement", statement_result), ("anchor", anchor_result)):
        if lean_result.returncode:
            sys.stdout.write(lean_result.stdout)
            raise SystemExit(f"{name} Lean replay failed")
    statement_expression = serialized_target(
        statement_result, "Stage1Instances.THM_M_0812.KonigMatchingCoverTarget"
    )
    anchor_expression = serialized_target(
        anchor_result, "Stage1Instances.THM_M_0812.ExactTarget"
    )
    assert statement_expression == anchor_expression
    assert hashlib.sha256(statement_expression.encode()).hexdigest() == EXPRESSION_SHA256
    assert hashlib.sha256(statement_result.stdout.encode()).hexdigest() == STATEMENT_OUTPUT_SHA256
    assert hashlib.sha256(anchor_result.stdout.encode()).hexdigest() == ANCHOR_OUTPUT_SHA256
    assert anchor_result.stdout.count("Type mismatch") == 2
    assert anchor_result.stdout.count("Declarations are sorry-free!") == 4
    assert anchor_result.stdout.count(
        "depends on axioms: [propext, Classical.choice, Quot.sound]"
    ) == 4
    assert "sorryAx" not in anchor_result.stdout

    for relative in CHANGED_PATHS:
        check_text_file(ROOT / relative)
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    print(
        "check_anchor_audit: ok "
        "(THM-M-0812; 10/10 bounded groups classified; exact root remains H1/M3/R2; "
        "ATLAS and closed PR candidates receive no proof credit)"
    )


if __name__ == "__main__":
    main()
