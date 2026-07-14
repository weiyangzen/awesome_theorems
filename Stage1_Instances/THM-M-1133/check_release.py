#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1133-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1133"
ITEM = "S56-M-1133-RELEASE"
THEOREM = "THM-M-1133"
BASE_REVISION = "8fcf03cf3d09c62d0b851f5168feacf59b7421b0"
BASE_TREE = "35333f075c58f129cc3658dd5e4fa5d52d7c0927"
EXPRESSION_SHA256 = "cb70ff9396c3c5fad0ea98bf234dc38f20738f5ff2accc32b4712675e90e5c3b"
DENOMINATOR_SHA256 = "8ae5b9f05fb5913dcb53d061df667c4fcbc5343c208bd22cba9c7f78ef506fd6"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "63e7f31ae3f3b1a8d0a06836f6afe31960fa1cb0c461922eaf69c08cedcd7bee",
    "ObligationTree.lean": "1ec64c882d599a5ee2c40c441e1cc7dd5c6635c21f6debd25cdcc49e4a54b6d2",
    "Proof.lean": "5f6ca5374c7f3666475f9d0b27a298b3138ed0daa3d5b5fb0c8ad9e38ebea4fe",
    "Validation.lean": "3bce01da9978f573666f584a0c9cb0817e0521588381490f70708b80a16e2ee2",
    "statement.json": "caf73f64adbe2900f0f030bda0361b37056b8c1b6b678107ae005ff71e29e379",
    "anchor-audit.json": "4898f449ad4acfafdf94fc14fb9affb56f20f64acdad0818cae9ad39b97b2c09",
    "obligation-registry.json": "a80612db8440ab7249994fd5e732beda9a54177cba06673e896268b4c58b3801",
    "typed-graphs.json": "867ec2cd3456c748416716d2a70dc028d8127b94cb0034b17a042f267262ac10",
    "proof-receipt.json": "ec8b25511ffafc8be6cfb92119cf7c05839a26e3248dff3405ffcf6c25e4e92f",
    "validation-receipt.json": "191e7d2f4d20e9396d5f2bd21113e71eae17c5a05beed54c5f661c9b7fd673db",
    "validation-spec.json": "b5c600c67e7c4af2f6621f2f13a3e28da84c70e623de68b1d0762860d5e5c071",
    "source_statement_crosswalk.md": "2dbdb59a9d5806911e3f7604c71565fcc996aa4a244622470361fb63162d9940",
    "check_proof.sh": "0d6ffc7e114f7d79cd151c3605bb7493d7732bf8f8f803fe466bdf30090af4c1",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release.md",
}

if not __debug__:
    raise RuntimeError("release reconciliation requires Python assertions")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
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
    return result.stdout


def git(*args: str) -> str:
    return run(["git", *args]).rstrip()


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, declaration
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def main() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 338
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1133-VALIDATION"
    )
    assert release_item["phase"] == "release" and release_item["layer"] == 6
    assert release_item["state"] == "[ ]" and release_item["attempts"] == 0
    assert release_item["depends_on"] == ["S56-M-1133-VALIDATION"]
    assert release_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"input drifted: {name}"

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    assert decision["accepted"] is decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert decision["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert decision["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert set(decision["changed_paths"]) == CHANGED_PATHS

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-1133-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == decision["node_receipt_id"]
    assert receipt["depends_on"] == ["S56-M-1133-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["accepted_receipt_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["commands_and_results"][-2]["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert receipt["commands_and_results"][-2]["exit_code"] == 0
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["dependency_receipt"]["receipt_sha256"] == sha256(
        HERE / "validation-receipt.json"
    )
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "covered_obligation_ids",
        "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1133-ROOT"
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["audit_complete"] is False
    assert graphs["closure_boundary"]["theorem_complete"] is False
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M1133-T-LIMIT"]

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert set(proof["result"]["axioms"]) == EXPECTED_AXIOMS
    assert proof["accepted_closed_obligation_ids"] == []

    assert validation["verdict"] == "blocked"
    assert validation["result"]["provisional_root_kernel_closed"] is True
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert set(validation["result"]["observed_axioms"]) == EXPECTED_AXIOMS

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H2", "M": "M3", "R": "R3"
    }
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["next_failed_theorem_gate"]["gate_id"] == (
        "S56-M-1133-AUTHORITATIVE-STATE-FRESHNESS"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["accepted_remaining_root_cut_set"] == ["M1133-T-LIMIT"]
    assert receipt["result"] == {
        "exit_code": 0,
        "verdict": "blocked",
        "lifecycle_before": "planned",
        "lifecycle_after": "planned",
        "root_vector_before": {"H": "H2", "M": "M3", "R": "R3"},
        "root_vector_after": {"H": "H2", "M": "M3", "R": "R3"},
        "audit_complete": False,
        "theorem_complete": False,
        "accepted_receipt_ids": [],
        "current_root_kernel_observation": (
            "warm network-isolated exact-root replay passed with no placeholders and "
            "only propext, Classical.choice, and Quot.sound"
        ),
        "validation_dependency_gate": "fail_closed",
        "authoritative_state_freshness_gate": "fail_closed",
        "hermetic_release_gate": "fail_closed",
        "independent_verification_gate": "fail_closed",
    }

    reconciliation = decision["evidence_reconciliation"]
    for gate in (
        "validation_dependency_master_accepted",
        "validation_release_grade",
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_root_closed",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_policy",
        "complete_transitive_provenance_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[gate] is False, gate
    assert reconciliation["accepted_closed_obligation_ids"] == []

    cut_set = "\n".join(result["remaining_release_cut_set"])
    for fragment in (
        "S56-M-1133-VALIDATION",
        "M1133-S-FOUNDATION",
        "M1133-X-PROVENANCE",
        "M1133-X-SOURCE",
        "n = 0 metadata",
        "R0 node-anchored",
        "AUDIT-Z",
        "empty-cache network-denied cold build",
        "two signed attestations",
        "minimal verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_set, fragment

    proof_output = run([
        "/usr/bin/bwrap",
        "--ro-bind", "/", "/",
        "--tmpfs", "/tmp",
        "--dev", "/dev",
        "--proc", "/proc",
        "--unshare-net",
        "--die-with-parent",
        "--chdir", str(ROOT),
        "/usr/bin/bash", f"Stage1_Instances/{THEOREM}/check_proof.sh",
    ])
    for declaration in (
        "Stage1Instances.THM_M_1133.caloric_isSubcaloric",
        "Stage1Instances.THM_M_1133.root_of_subsolutionMaximumPrinciple",
        "Stage1Instances.THM_M_1133.second_deriv_nonpos_of_localMax",
        "Stage1Instances.THM_M_1133.iteratedFDeriv_diag_nonpos_of_localMax",
        "Stage1Instances.THM_M_1133.spatialLaplacian_nonpos_of_localMax",
        "Stage1Instances.THM_M_1133.deriv_nonneg_of_isLocalMaxOn_Iic",
        "Stage1Instances.THM_M_1133.strictSubsolutionMaximumPrinciple",
        "Stage1Instances.THM_M_1133.perturb_isStrictSubcaloric",
        "Stage1Instances.THM_M_1133.weakSubsolutionMaximumPrinciple",
        "Stage1Instances.THM_M_1133.heatEquationWeakMaximumPrinciple",
    ):
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    assert "PASS THM-M-1133 proof phase" in proof_output
    assert "declaration uses 'sorry'" not in proof_output

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == decision["known_failures"]

    for path in (
        HERE / "check_release.py",
        HERE / "release-decision.json",
        HERE / "release-receipt.json",
        HERE / "release-spec.json",
        HERE / "release.md",
    ):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS release inputs: manifest, DAG, receipts, graph, and hashes agree")
    print("PASS current Lean observation: exact root is sorry-free with expected axioms")
    print("PASS fail-closed state: lifecycle planned; accepted root H2/M3/R3; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED audit, immutable input, cold/offline, trust, and independent release gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
