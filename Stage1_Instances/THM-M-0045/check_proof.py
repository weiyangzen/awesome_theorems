#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0045-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0045-PROOF"
THEOREM = "THM-M-0045"
BASE_REVISION = "9a1ce196889e32911beeeffa685084b48a969866"
BASE_TREE = "00d5c1749015f44fb0c5694181253c3a08db5d47"
EXPRESSION_SHA256 = "275e1e43027f442607fc48e78ce4e189de66b328d39c61044e87a4c8f85c001b"
DENOMINATOR_SHA256 = "47fc5062b82b1a06eb2ca0ce6379dc5ea7f6ec15481a1144fe24f11724baad1a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
HISTORICAL_REVISION = "0a539f0ce764fd16726509b62ed7b870461070eb"
HISTORICAL_PATH = "Mathlib/LinearAlgebra/Matrix/SchurTriangulation.lean"
HISTORICAL_SHA256 = "8fc4d47249d8bcc75c02fedc6d9b0008f7c0127c501f608d4226a7f5872f4bc3"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/SchurPort.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    port_path = HERE / "SchurPort.lean"
    proof = proof_path.read_text(encoding="utf-8")
    port = port_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1085
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0045-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    assert prohibited.search(without_comments(port)) is None
    for marker in (
        "private noncomputable def SchurTriangulationAux.of",
        "let W : Submodule",
        "let g : Module.End",
        "int.collectedOrthonormalBasis",
        "termination_by Module.finrank",
        "noncomputable def schurTriangulationUnitary",
        "lemma schur_triangulation",
    ):
        assert marker in port, marker
    for marker in (
        "import ObligationTree",
        "import SchurPort",
        "theorem schurEquationPackage : ObligationTree.SchurEquationPackage",
        "A.schurTriangulationUnitary.property",
        "A.schurTriangulation.property",
        "A.schur_triangulation",
        "theorem schurTriangularization : SchurTriangularizationTarget",
        "ObligationTree.root_of_equationPackage schurEquationPackage",
        "#print sorries schurTriangularization",
        "#print axioms schurTriangularization",
    ):
        assert marker in proof, marker

    machine_ids = registry["frozen_denominators"]["required_machine"]
    assert len(machine_ids) == 31 and machine_ids[0] == "M0045-ROOT"
    assert machine_ids[-1] == "M0045-T-PACKAGE"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0045-ROOT"
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M0045-T-PACKAGE"]
    assert graphs["composition_certificates"][0]["checked_declaration"].endswith(
        "root_of_equationPackage"
    )

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["closed_obligation_ids"] == machine_ids
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["proof_source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["port_source_sha256"] == sha256(port_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    historical = subprocess.check_output(
        ["git", "show", f"{HISTORICAL_REVISION}:{HISTORICAL_PATH}"], cwd=mathlib
    )
    assert hashlib.sha256(historical).hexdigest() == HISTORICAL_SHA256

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-L" in validation and "M0045-S-FOUNDATION" in validation
    for path in (proof_path, port_path, HERE / "check_proof.py", HERE / "check_proof.sh"):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0045 proof phase: current-pin local port closes the exact frozen root")


if __name__ == "__main__":
    main()
