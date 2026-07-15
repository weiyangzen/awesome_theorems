#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0005-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0005"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0005-RELEASE"
THEOREM = "THM-M-0005"
BASE_REVISION = "229ca98e7478d389ccf8de8173c94e0e7c8fe670"
BASE_TREE = "d3cc9562940b923aebbe7e01ce66232079760b3b"
VALIDATION_SHA256 = "b687de90a101947fd0b2bcaf92c20a646ab835b6bfc806d9b3ac8bbe755831dd"
EXPRESSION_SHA256 = "f6396a70702a8bb45dbbb267ebd3ba10aae4f4db28cf25355f8fcd7bb607ddd4"
DENOMINATOR_SHA256 = "563eac891739af1e2468c4fd23e7465013f9e5791e069a03e22ccdf67119a762"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
OPEN_ROOT_CUT = [
    "M0005-CHAIN-FREE",
    "M0005-EZ-MAP",
    "M0005-EZ-EQUIV",
    "M0005-EZ-NAT",
    "M0005-ALG-MAPS",
    "M0005-ALG-ZERO",
    "M0005-ALG-EXACT",
    "M0005-ALG-NAT",
    "M0005-DIRECT-SUM",
    "M0005-COMPONENTS",
    "M0005-TOP-NAT",
]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release.md",
]
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, validation receipt, registry, and graph agree",
    "PASS narrow Lean replay: the exact Kunneth statement elaborates at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H1/M3/R3 unchanged; zero frozen obligations close",
    "BLOCKED AUDIT-Z and THEOREM-Z: source, readability, trust, hermetic, and independent gates remain open",
    "verdict=blocked lifecycle=planned audit_complete=false theorem_complete=false accepted_receipts=0",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL THM-M-0005 release: {message}")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 240,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    return result


def git(*args: str) -> str:
    result = run(["git", *args], timeout=60)
    if result.returncode:
        fail(f"git command failed: {args!r}\n{result.stdout}")
    return result.stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize:
        fail("Python assertions must be enabled")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-direct-sum-receipt-20260715-head-5bb51543-slot21.json")
    intake = load(HERE / "intake.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 100
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    items = {row["id"]: row for row in execution["items"]}
    release_item = items[ITEM]
    validation_item = items["S56-M-0005-VALIDATION"]
    assert release_item["phase"] == "release" and release_item["layer"] == 6
    assert release_item["state"] == "[ ]" and release_item["attempts"] == 0
    assert release_item["depends_on"] == [validation_item["id"]]
    assert release_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert intake["lifecycle_mode"] == "planned"
    assert intake["root_vector"] == {
        "human": "H1", "machine": "M3", "readability": "R3"
    }
    assert intake["theorem_complete"] is False
    formal = intake["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "AwesomeTheorems.Stage1.THM_M_0005.KunnethFormula"
    )
    assert formal["elaborated_expression_hash"] == f"sha256:{EXPRESSION_SHA256}"

    assert registry["root_obligation_id"] == "M0005-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_SHA256
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == validation_item["id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_SHA256
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["scheduler_projection"] == "[_]"
    assert validation["verdict"] == "blocked"
    assert validation["accepted_receipt_ids"] == []
    validation_result = validation["result"]
    assert validation_result["supported_obligation_ids"] == []
    assert validation_result["accepted_closed_obligation_ids"] == []
    assert validation_result["root_kernel_closed"] is False
    assert validation_result["root_machine_debt"] == "M3"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    structural = run(
        ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"]
    )
    assert structural.returncode == 0, structural.stdout
    assert "PASS THM-M-0005 obligation tree: 18 obligations, 51 typed edges" in structural.stdout
    assert f"registry denominator sha256: {DENOMINATOR_SHA256}" in structural.stdout
    assert "root remains open at M3; no obligation receives closure credit" in structural.stdout

    assert proof["accepted"] is False
    assert proof["supported_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["decision_id"] == "S56-M-0005-RELEASE-blocked-20260715T142714+0800-slot5"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["phase"] == "release" and decision["depends_on"] == [
        "S56-M-0005-VALIDATION"
    ]
    assert decision["proposed_state"] == "[_]"
    assert decision["intent"] == "release" and decision["verdict"] == "blocked"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["release_grade"] is decision["release_accepted"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    assert decision["accepted_closed_obligation_ids"] == []
    root = decision["root_vector"]
    assert root["accepted_before"] == root["accepted_after"] == ROOT_VECTOR
    terminal = decision["terminal_decisions"]
    assert terminal == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }
    assert decision["first_failed_gate"] == {
        "gate_id": "S56-10.2-DEPENDENCY-ACCEPTANCE",
        "node_gate": "dependency.S56-M-0005-VALIDATION.master_acceptance",
        "reason": (
            "The direct validation prerequisite is only provisional [_]; its receipt is "
            "accepted=false, release_grade=false, verdict=blocked, and is not master accepted."
        ),
    }
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["first_failed_reproduction_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["authoritative_remaining_root_cut_set"] == OPEN_ROOT_CUT

    evidence = decision["evidence_reconciliation"]
    assert evidence["exact_statement_current_kernel_replay"] is True
    assert evidence["premise_free_exact_root_kernel_closure"] is False
    assert evidence["validated_frozen_obligation_count"] == 0
    assert evidence["validation_receipt_current_snapshot_recipe_replay"] is False
    for key in (
        "dependency_master_acceptance",
        "audit_inventory_reconciliation",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_profile",
        "complete_provenance_trust_tcb_and_sbom",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "independent_signed_runner_attestations",
        "independent_minimal_verifier",
        "protected_ci_mutation_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert evidence[key] is False, key

    cut_text = "\n".join(decision["remaining_release_cut_set"])
    for fragment in (
        "S56-M-0005-VALIDATION",
        "Eilenberg-Zilber",
        "algebraic Kunneth",
        "H0 primary-source",
        "R0 node-specific",
        "foundation profile",
        "empty-cache network-denied cold build",
        "SBOM and license",
        "Two signed attestations",
        "minimal verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_text, fragment

    recipe = spec["recipe"]
    assert spec["schema_version"] == "stage1-release-spec/1.0"
    assert spec["spec_id"] == "S56-M-0005-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["intent"] == "release"
    assert recipe == receipt["recipe"]
    assert recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == registry["frozen_denominators"]["inventory"]
    assert recipe["covered_declarations"] == [
        "AwesomeTheorems.Stage1.THM_M_0005.KunnethFormula"
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["verdict"] == "blocked"
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is receipt["release_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["dependency"] == dependency
    assert receipt["result"] == {
        "exit_code": 0,
        "statement_kernel_replay": "pass",
        "accepted_closed_obligation_ids": [],
        "root_kernel_closed": False,
        "root_machine_debt": "M3",
        "audit_complete": False,
        "theorem_complete": False,
        "verdict": "blocked",
        "lifecycle_after": "planned",
        "accepted_state_changed": False,
        "first_failed_gate": "S56-10.2-DEPENDENCY-ACCEPTANCE",
        "remaining_root_cut_set": OPEN_ROOT_CUT,
        "complete_trust_provenance_gate": "fail_closed",
        "hermetic_cold_offline_gate": "fail_closed",
        "independent_verification_gate": "fail_closed",
    }
    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(expected_stdout.encode()).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }
    assert receipt["recipe"]["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": (
            "sha256:" + receipt["output_evidence"]["stdout_semantic_sha256"]
        ),
    }]
    assert receipt["changed_paths"] == CHANGED_PATHS
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["status_boundary"] == decision["status_boundary"]
    assert receipt["first_failed_gate"] == decision["first_failed_gate"]
    assert receipt["first_failed_release_gate"] == decision["first_failed_release_gate"]
    assert receipt["first_failed_reproduction_gate"] == decision["first_failed_reproduction_gate"]

    public_release = (HERE / "release.md").read_text(encoding="utf-8")
    for required in (
        "The release verdict is `blocked`.",
        "`[H1, M3, R3]`",
        "`audit_complete=false`",
        "`theorem_complete=false`",
        "The first gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.",
        "No premise-free `NaturalKunnethSequence` is recorded or validated",
        "It is not an accepted receipt",
    ):
        assert required in public_release, required
    for prohibited_public_claim in (
        "The release verdict is `accepted`",
        "`audit_complete=true`",
        "`theorem_complete=true`",
        "the theorem is complete",
        "THEOREM-Z is accepted",
    ):
        assert prohibited_public_claim not in public_release, prohibited_public_claim

    statement = run(
        [
            "lake", "env", "lean", "--trust=0",
            f"../../Stage1_Instances/{THEOREM}/KunnethStatement.lean",
        ],
        cwd=LEAN_ROOT,
    )
    assert statement.returncode == 0, statement.stdout
    assert "error:" not in statement.stdout
    assert statement.stdout.count("unused variable") == 4

    stale_validation = run(
        [
            "python3", "-I", "-B",
            f"Stage1_Instances/{THEOREM}/check_validation.py", "--probe",
        ]
    )
    assert stale_validation.returncode == 1
    assert "AssertionError" in stale_validation.stdout
    assert 'assert git("rev-parse", "HEAD") == BASE_REVISION' in stale_validation.stdout
    assert "line 284, in main" in stale_validation.stdout
    assert validation["base_revision"] != BASE_REVISION
    current_authority = {
        relative: sha256(ROOT / relative)
        for relative in validation["authority_hashes"]
    }
    assert current_authority != validation["authority_hashes"]
    assert receipt["current_authority_sha256"] == current_authority
    environment = receipt["environment"]
    lean_toolchain = LEAN_ROOT / "lean-toolchain"
    lake_manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in lake_manifest["packages"] if row["name"] == "mathlib")
    assert sha256(lean_toolchain) == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == environment["mathlib_revision"]
    assert environment["mathlib_revision"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    mathlib_head = run(["git", "rev-parse", "HEAD", "HEAD^{tree}"], cwd=mathlib)
    assert mathlib_head.returncode == 0
    assert mathlib_head.stdout.splitlines() == [
        environment["mathlib_revision"], environment["mathlib_tree"]
    ]
    mathlib_status = run(
        ["git", "status", "--porcelain=v1", "--untracked-files=no"], cwd=mathlib
    )
    assert mathlib_status.returncode == 0 and mathlib_status.stdout == ""
    lean_path = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT)
    assert lean_path.returncode == 0
    lean_executable = Path(lean_path.stdout.strip())
    lake_executable = lean_executable.with_name("lake")
    assert sha256(lean_executable) == environment["lean_executable_sha256"]
    assert sha256(lake_executable) == environment["lake_executable_sha256"]

    hashable_untracked_paths = [
        ".stage1-worker-selftest.json",
        "Formalizations/Lean/.lake",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-spec.json",
        f"Stage1_Instances/{THEOREM}/release.md",
    ]
    expected_untracked_bindings = []
    for relative in hashable_untracked_paths:
        path = ROOT / relative
        if path.is_symlink():
            expected_untracked_bindings.append({
                "path": relative,
                "kind": "symlink_target_utf8",
                "sha256": hashlib.sha256(os.readlink(path).encode()).hexdigest(),
            })
        else:
            expected_untracked_bindings.append({
                "path": relative,
                "kind": "regular_file",
                "sha256": sha256(path),
            })
    assert hashable_untracked_paths == sorted(hashable_untracked_paths)
    assert receipt["untracked_input_bindings"] == expected_untracked_bindings
    assert receipt["self_referential_hash_exclusions"] == [{
        "path": f"Stage1_Instances/{THEOREM}/release-receipt.json",
        "reason": (
            "A receipt cannot embed its own final content hash. The integration lane must "
            "content-address the completed receipt and bind that digest in accepted state."
        ),
    }]

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]

    status = git("status", "--short", "--untracked-files=all")
    actual = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
