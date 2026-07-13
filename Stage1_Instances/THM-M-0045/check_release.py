#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0045-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0045"
ITEM = "S56-M-0045-RELEASE"
THEOREM = "THM-M-0045"
BASE_REVISION = "0d2c3bdcd192266bc255ac3d5186da604517145a"
BASE_TREE = "eafbcb48efd51d9cda34f0fc1afe780434abad64"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1085 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1085
    assert item["phase"] == "release" and item["layer"] == 6
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0045-VALIDATION"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0045-VALIDATION"
    )
    assert predecessor["state"] == "[_]"
    local_release = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open" and task_dag["accepted_states"] == []

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-0045-RELEASE-local-20260713T015328Z"
    assert decision["intent"] == receipt["intent"] == "release"
    assert decision["item_id"] == receipt["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["support_state"] == receipt["support_state"] == (
        "provisional_worker_selftest"
    )
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == predecessor["id"]
    assert dependency["worker_projection"] == predecessor["state"] == "[_]"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"] == (
        "provisional_worker_selftest"
    )
    assert dependency["master_accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False

    for name, expected in decision["reconciled_inputs"].items():
        assert sha256(HERE / name) == expected, name
    for name, expected in receipt["inputs"].items():
        assert sha256(HERE / name) == expected, name

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == ["M0045-T-PACKAGE"]
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    machine_ids = registry["frozen_denominators"]["required_machine"]
    assert len(machine_ids) == 31
    assert proof["closed_obligation_ids"] == machine_ids
    assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is proof["result"]["theorem_complete"] is False
    assert "M0045-S-FOUNDATION" in proof["remaining_root_cut_set"]
    assert any("M0045-S-FOUNDATION" in failure for failure in proof["known_failures"])
    assert validation["base_revision"] != BASE_REVISION
    assert validation["result"]["provisional_exact_root_kernel_closed"] is True
    assert validation["result"]["accepted_root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0045-PROOF.master_acceptance"
    assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector"]["accepted_before"] == ["H1", "M3", "R4"]
    assert decision["root_vector"]["accepted_after"] == ["H1", "M3", "R4"]
    assert decision["root_vector"]["best_provisional_kernel_evidence"].startswith(
        "exact_root_local_kernel_replay_pass; M0-L classification disputed"
    )
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
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert receipt["first_failed_gate"] == decision["first_failed_gate"]
    assert receipt["first_failed_release_gate"] == decision["first_failed_release_gate"]
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]
    assert receipt["result"] == {
        "exit_code": 0,
        "verdict": "blocked",
        "lifecycle": "planned",
        "accepted_root_vector": ["H1", "M3", "R4"],
        "provisional_exact_root_kernel_replay": "pass",
        "observed_axioms": EXPECTED_AXIOMS,
        "audit_complete": False,
        "theorem_complete": False,
        "release_accepted": False,
    }
    recipe = receipt["recipe"]
    assert recipe["recipe_id"] == "S56-M-0045-RELEASE-negative-reconciliation-v1"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert recipe["env_allowlist"] == {} and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0 and recipe["timeout_seconds"] == 180
    assert recipe["covered_obligation_ids"] == machine_ids
    assert recipe["covered_declarations"] == [
        "Stage1Instances.THM_M_0045.Proof.schurEquationPackage",
        "Stage1Instances.THM_M_0045.Proof.schurTriangularization",
    ]
    assert recipe["expected_outputs"]

    evidence = decision["evidence_reconciliation"]
    assert evidence["structured_state_freshness"].startswith("failed:")
    assert evidence["receipt_snapshot_freshness"].startswith("failed:")
    for key in (
        "audit_inventory_reconciliation",
        "human_source_acceptance",
        "readability_acceptance",
        "complete_provenance_and_trust_closure",
        "hermetic_release_reproduction",
        "supply_chain_closure",
        "independent_release_verification",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert evidence[key].startswith("missing"), key
    assert evidence["per_obligation_reconciliation"].startswith("conflict:")

    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0045-VALIDATION",
        "contradictory 31-ID proof partition",
        "M0045-S-FOUNDATION",
        "AUDIT-Z",
        "H0 primary-source",
        "R0 node-by-node",
        "executable/bootstrap TCB closure",
        "immutable clean release snapshot",
        "empty-cache network-denied cold build",
        "SBOM and license",
        "two signed attestations",
        "minimal release verifier",
        "mutation, differential, and metamorphic",
        "deterministic content-addressed evidence bundle",
    ):
        assert fragment in cut, f"release cut set omits {fragment!r}"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean",
        "ObligationTree.lean",
        "SchurPort.lean",
        "Proof.lean",
        "Validation.lean",
    ):
        source = without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    mathlib = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    lean_root = ROOT / "Formalizations" / "Lean"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=lean_root).strip())
    assert LEAN_COMMIT in run([str(lean), "--version"])
    assert sha256(lean) == LEAN_SHA256
    assert receipt["environment"]["lean_executable_sha256"] == LEAN_SHA256
    proof_output = run(["bash", str(HERE / "check_proof.sh")])
    assert proof_output.count("Declarations are sorry-free!") == 2
    for axiom in EXPECTED_AXIOMS:
        assert proof_output.count(axiom) == 2, axiom
    assert "sorryAx" not in proof_output

    required_packet_keys = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert required_packet_keys <= set(packet)
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["covered_obligation_ids"] == machine_ids
    assert packet["canonical_target"]["elaborated_expression_sha256"] == (
        "275e1e43027f442607fc48e78ce4e189de66b328d39c61044e87a4c8f85c001b"
    )
    assert packet["receipt_ids"]["release"] == receipt["receipt_id"]
    assert any(
        command.get("argv")
        and command["argv"][-1].endswith("check_release.py")
        and command.get("exit_code") == 0
        for command in packet["commands"]
    )
    actual_changed = {
        line[3:]
        for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS S56-M-0045-RELEASE reconciliation")
    print("PASS narrow Lean replay: exact local Schur root elaborates")
    print("PASS observed axioms: propext, Classical.choice, Quot.sound")
    print("verdict=blocked lifecycle=planned root_vector=H1/M3/R4")
    print("AUDIT-Z=false THEOREM-Z=false theorem_complete=false accepted_receipts=0")
    print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
    print("first_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD")


if __name__ == "__main__":
    main()
