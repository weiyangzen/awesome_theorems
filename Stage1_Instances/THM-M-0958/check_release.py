#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0958-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0958"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0958-RELEASE"
THEOREM = "THM-M-0958"
BASE_REVISION = "564d3694f4758ec663d807fe837874fa3945a640"
BASE_TREE = "b9cfbcd25fa4ce19f9b8f70dc8514810a885ab58"
EXPRESSION_SHA256 = "bc0d841038cdbcd4960581583c4ddfb7004d7ad38cf6432ab4803e9908f8f59c"
DENOMINATOR_SHA256 = "a66280599ad67d6daac4bea5c3e08484e1b6c1aa0d75223a5d3aaf428c383e5b"
VALIDATION_RECEIPT_ID = "S56-M-0958-VALIDATION-local-20260715T083500Z"
VALIDATION_RECEIPT_SHA256 = "673be25379c811a0cb422a6cb25de2ff90c1d7581a26bddd209b546da123c673"
VALIDATION_BASE = "51c2828e82ffb19860830f78b771f80e13ad7dff"
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "c2b14d4510fb999cedd50bab8cd040c79cd0ed0218a640166e497c291099bc9f",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "4b64c5534f72d038546fa674df02b4f8ee9e058e8e6a7f5ff381e6003bd3f4e5",
    "Docs/Blueprint_Guidelines.md":
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
RECONCILED_INPUTS = {
    "README.md": "9c0572b1ab01694c35e85170464a74203ba95ae2ae8c2b601a0504920c9978bd",
    "source-statement-crosswalk.md":
        "6b3e0528d77f8a83f35969e0a756c27792389f0ff60eb7913d00aea3b5727136",
    "Statement.lean": "765d13f4b2fc0bc8bdf0a1211039b62ed6269148819857795aac0c7a42dc40e6",
    "ObligationTree.lean": "c52b448dfaa236834207a048c5d26208e6b4db8b39830eaf620b398497a64394",
    "Proof.lean": "60def65f51836f174a4d0c10fb782b6c10158184183d6bbc05eb7a1b578fd3be",
    "Validation.lean": "7b44aeb83a7896b71ac9a7f7d6da4e5d15fd61a8cc0d8af381ee34e157faf214",
    "instance.json": "28dd5b490a3e83306ea10985feeba58904b5d1193fa605eb53f27990413b8990",
    "task-dag.json": "31e963bdb84f105e66071ea2c8af769f205d00ecb945d0fbcc2b671ef77f2faa",
    "statement.json": "2e48944da988922ac8b4c9a0b56f13795c6dad8536464d29f64e449ed6920500",
    "anchor-audit.json": "eba38a4e3bb2530ffb45bc9560be6b667823a4b3ff9e19fdedc802fc6190224d",
    "obligation-registry.json":
        "53433fb10301f4166c0500b9872f04f0f31839117f4c54457d448458712287d2",
    "typed-graphs.json": "c6f40a4fa5d20d0b0ca88d17222d71e87ad292d29a8218ecdac17f0ddaa4f62a",
    "proof-receipt.json": "4ba570039727a924a5d650bf1948f50b7b145e0e292f78d1162c7f85c052e4e5",
    "proof-blocker.json": "7cc75b4698b15ba892f3742ed4205866d93b63e758636762ac9198645bf21e83",
    "validation-spec.json": "9fcb742f3b5fd5dc1e2efd18a4eb9543bb9e6af2eb2685fc7ba403a463243462",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-phase.md": "dde3e2dcb289e553d70ed0738459a3cf79f5a3bf5f46f77ed1907e54dad79b9d",
    "check_validation.py": "1fb469e25162cbb4285008036a9d94e6ca3bd7bd2bbfe060b709b70914c9ac54",
}
SUMMARY_LINES = [
    "release-decision: ok (blocked at validation dependency acceptance)",
    "structured authority: ok (H1/M3/R4; M0958-T-WITNESS remains open)",
    "validation replay boundary: fail closed (historical base assertion is stale)",
    "AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]",
    "release assurance: open (clean cold/offline, supply chain, independent verification, deterministic bundle, and master acceptance)",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 60) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if not __debug__:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert run(["git", "rev-parse", "HEAD"]) == BASE_REVISION
    assert run(["git", "rev-parse", "HEAD^{tree}"]) == BASE_TREE
    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1492 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1492,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0958-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0958-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0958.ElkinConstructionTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == RECONCILED_INPUTS["Statement.lean"]
    assert statement["theorem_complete"] is False
    vector = {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == vector
    assert instance["accepted_receipt_ids"] == instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert local_dag["accepted_states"] == [] and local_dag["theorem_complete"] is False

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 64
    assert registry["root_obligation_id"] == "M0958-ROOT"
    observed = registry["status_observed_after_freeze"]
    assert observed["accepted_closed_obligations"] == []
    assert observed["accepted_root_machine_debt"] == "M3"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["minimal_open_machine_proof_cut_sets"] == [["M0958-T-WITNESS"]]
    assert closure["remaining_root_cut_set"] == [
        "M0958-T-WITNESS",
        "M0958-X-SOURCE-ELKIN",
        "M0958-S-FOUNDATION",
        "M0958-X-PROVENANCE",
        "M0958-X-EVIDENCE",
        "M0958-X-TRUST",
        "M0958-X-READABLE",
        "M0958-X-WORKFLOW",
    ]

    assert proof["accepted"] is False and proof["verdict"] == "no_state_change"
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == ["M0958-T-WITNESS"]
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["root_vector"] == vector
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["verdict"] == "blocked" and decision["proposed_state"] == "[_]"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    dependency = decision["dependency"]
    assert dependency["item_id"] == "S56-M-0958-VALIDATION"
    assert dependency["scheduler_projection"] == predecessor["state"] == "[_]"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_base_revision"] == VALIDATION_BASE
    assert dependency["receipt_accepted"] is dependency["receipt_release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_recipe_currently_replayable"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision["root_vector"]["before"] == decision["root_vector"]["after"] == vector
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == (
        "M0958-T-WITNESS.kernel_closure"
    )
    assert decision["first_failed_release_protocol_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["next_failed_release_protocol_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    for key in (
        "validation_dependency_master_accepted",
        "exact_root_kernel_closed",
        "audit_inventory_accepted_and_reconciled",
        "human_source_h0_accepted",
        "readability_r0_accepted",
        "accepted_foundation_profile",
        "complete_transitive_tcb_and_provenance",
        "immutable_clean_release_input",
        "cold_empty_cache_network_denied_build",
        "offline_archive_replay",
        "complete_sbom_and_license_closure",
        "deterministic_content_addressed_release_bundle",
        "two_signed_independent_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_adversarial_ci",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == vector
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-0958-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_theorem_gate"] == "M0958-T-WITNESS.kernel_closure"
    assert receipt["first_failed_release_gate"] == "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["status_boundary"] == decision["status_boundary"]
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
            "covered_decisions",
        )
    }
    assert receipt["inputs"]["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["release_decision_sha256"] == sha256(
        HERE / "release-decision.json"
    )
    assert receipt["inputs"]["release_validation_sha256"] == sha256(
        HERE / "release-validation.md"
    )
    assert receipt["inputs"]["check_release_sha256"] == sha256(HERE / "check_release.py")

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES

    status = run([
        "git", "status", "--short", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    ])
    actual_changed = {line[3:] for line in status.splitlines()}
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink() and lake_link.resolve(strict=True).is_dir()
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (
        HERE / "release-decision.json",
        HERE / "release-receipt.json",
        HERE / "release-validation.md",
    ):
        public = path.read_text(encoding="utf-8")
        assert "/home/" not in public and ".cron/" not in public
        assert "theorem_complete=true" not in public

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
