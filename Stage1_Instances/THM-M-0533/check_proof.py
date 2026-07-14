#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and claim checks for THM-M-0533 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0533-PROOF"
THEOREM = "THM-M-0533"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
STATEMENT_SHA256 = "cbe35890b43f302b71cf1230a87c21b2ac4eedf196210389598453c61ff18bce"
OBLIGATION_TREE_SHA256 = "ded027e2345e1b81568067254d083de705bf062e0f9079fe6d2a427c2c21f3b1"
REGISTRY_SHA256 = "cd0411fccc46ee639e87328a41ce396b92f62467fdffd68d9a39761387c9b630"
GRAPHS_SHA256 = "6ac4e3d41e8e184c6a88f7ffdcde043a79c43e6766a664caf12453aab66a9a24"
PROOF_SHA256 = "4b577167c4778809d6585256f7683df4242488b5132669d0c3365a8912360837"
DENOMINATOR_SHA256 = "238242dfcb6274343a6413ed2628d0944bf0882c280b42608d8e19bad2c88dfc"
RECEIPT_ID = "S56-M-0533-PROOF-partial-20260715T051900+0800"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 590
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-0533-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert item["deliverable"] == (
        "Implement or pin/import the required proof bodies without placeholders."
    )
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b|"
        r"\b(?:implemented_by|native_decide)\b",
        re.MULTILINE,
    )
    assert prohibited.search(proof) is None
    for fragment in (
        "import ObligationTree",
        "theorem firstMap_comp_secondMap",
        "have hinc : interLeft U V ≫ Opens.inclusion' U =",
        "simp [firstMap, secondMap, ← Functor.map_comp, hinc]",
        "#print axioms firstMap_comp_secondMap",
    ):
        assert fragment in proof, fragment

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "ObligationTree.lean") == OBLIGATION_TREE_SHA256
    assert sha256(HERE / "obligation-registry.json") == REGISTRY_SHA256
    assert sha256(HERE / "typed-graphs.json") == GRAPHS_SHA256
    assert sha256(proof_path) == PROOF_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""

    assert receipt["receipt_id"] == blocker["partial_proof_receipt_id"] == RECEIPT_ID
    assert receipt["item_id"] == blocker["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert receipt["base_revision"] == blocker["base_revision"] == packet["base_revision"]
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["statement_sha256"] == blocker["statement_sha256"] == STATEMENT_SHA256
    assert receipt["inputs"]["obligation_tree_sha256"] == blocker["obligation_tree_sha256"] == OBLIGATION_TREE_SHA256
    assert receipt["obligation_registry_sha256"] == blocker["obligation_registry_sha256"] == REGISTRY_SHA256
    assert receipt["typed_graphs_sha256"] == blocker["typed_graphs_sha256"] == GRAPHS_SHA256
    assert receipt["proof_body"]["source_sha256"] == PROOF_SHA256
    assert receipt["replay_script_sha256"] == sha256(HERE / "check_proof.sh")
    assert receipt["closed_obligation_ids"] == blocker["provisionally_closed_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == ["M0533-T-CONSTRUCTION"]
    assert blocker["proof_body_added"] is True
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert receipt["result"]["root_closed"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == blocker["remaining_root_cut_set"]

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["known_failures"] == packet["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        path = ROOT / relative
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0533 proof phase: signed-map identity and evidence agree")
    print("closed frozen obligations: none; root closure: open (M3)")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
