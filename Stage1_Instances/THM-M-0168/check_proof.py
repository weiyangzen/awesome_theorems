#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and worker-packet checks for THM-M-0168."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0168-PROOF"
THEOREM = "THM-M-0168"
BASE_REVISION = "dc0f0264c1db312ac95025747d3212b689facb5e"
BASE_TREE = "633bea3a2e72674768ee426a035a1850b9940ae7"
EXPRESSION_SHA256 = "b5cef8a8bb3b5505be6670f226315884282c53bb0040c30345f4fb0dc33254f5"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CLOSED_CHILD = "M0168-T-INTEGRATE"
REMAINING_CUT = [
    "M0168-C-GRAPH",
    "M0168-N-PDE-MINIMAL",
    "M0168-L-STABILITY",
    "M0168-C-CUTOFF",
    "M0168-L-CURVATURE",
    "M0168-L-DERIVATIVE-RIGIDITY",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 665
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0168-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0168-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for path in (HERE / "Statement.lean", HERE / "ObligationTree.lean", proof_path):
        assert prohibited.search(without_comments(path.read_text(encoding="utf-8"))) is None, path
    for marker in (
        "import Statement",
        "theorem constantPartials_to_affine",
        "theorem constantPartialsToAffine_proof : ConstantPartialsToAffine",
        "theorem canonicalTarget_iff_obligationTarget",
        "theorem canonical_bernstein_of_derivativeRigidity",
        "(rigidity : DerivativeRigidity)",
        "#print axioms canonical_bernstein_of_derivativeRigidity",
    ):
        assert marker in proof, marker

    canonical = statement["canonical_formal_target"]
    assert canonical["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget"
    )
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_before_proof_execution"] is True
    assert registry["canonical_root_expression_sha256"] == EXPRESSION_SHA256
    obligations = {row["obligation_id"]: row for row in registry["obligations"]}
    assert set(obligations) == set(graphs["coverage_denominators"]["canonical_obligations"])
    assert obligations[CLOSED_CHILD]["statement_fingerprint"] == (
        "planned:M0168-T-INTEGRATE-v1"
    )
    assert obligations[CLOSED_CHILD]["formal_target"] == (
        "Stage1Instances.THM_M_0168_Obligations.ConstantPartialsToAffine"
    )
    assert obligations["M0168-ROOT"]["machine_debt"] == "M2"
    assert graphs["closure_metrics_observed"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["terminal_declaration"] == (
        "Stage1Instances.THM_M_0168_Obligations.constantPartials_to_affine"
    )
    assert receipt["provisionally_closed_obligation_ids"] == [CLOSED_CHILD]
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == REMAINING_CUT
    for filename, expected in receipt["inputs"].items():
        path = ROOT / filename if filename.startswith("Formalizations/") else HERE / filename
        assert sha256(path) == expected, f"stale receipt input: {filename}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "M0168-T-INTEGRATE" in validation
    assert "root remains open at `M2`" in validation
    assert "theorem_complete=false" in validation
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0168 partial proof phase: exact affine-integration child checked")
    print("canonical composition remains conditional; root remains open M2")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
