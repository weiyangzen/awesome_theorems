#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0474-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0474-PROOF"
THEOREM = "THM-M-0474"
BASE_REVISION = "8c50139eafcb1c2e29e7ca69379648590820bf53"
EXPRESSION_SHA256 = "5475969fd23513d3b98134a6aaa747675a32a899f38be773a23cb330f2f590e8"
DENOMINATOR_SHA256 = "28dd518db2fe79a5006cbeb3fdd51b379f67cf388960c3f5fafdf2a7ad8b6a9e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
BASIC_SHA256 = "808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44"
ORDER_SHA256 = "42bef2580b87cd0fa6367cd2d57d30fb25fce373576a856cc84d27dad23fae23"
BASIC_OLEAN_SHA256 = "4cede73b3c7f85692307990d9cdaf819b5ac61dc50272e31586b7899d9f32119"
ORDER_OLEAN_SHA256 = "33d0d5970b2ec79349ee6335e9f76842ff648e8594994ddd3da18ca8941c2858"
CLOSED_IDS = [
    "M0474-ROOT",
    "M0474-T-COMPOSE",
    "M0474-L-NAT",
    "M0474-N-NAT-INT",
    "M0474-N-COPRIME",
    "M0474-L-INT",
    "M0474-C-ZMOD-NONZERO",
    "M0474-T-INT-ZMOD",
    "M0474-L-ZMOD",
    "M0474-T-ZMOD-CARD",
    "M0474-L-FINITE-FIELD",
    "M0474-C-UNIT",
    "M0474-L-GROUP-CARD",
]


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load("proof-receipt.json")
    statement = load("statement.json")
    registry = load("obligation-registry.json")
    instance = load("instance.json")
    dag = load("task-dag.json")
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8")
    )
    selftest = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 938,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0474-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    local_task = next(row for row in dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx)\b|^[ \t]*(axiom|unsafe)[ \t]+|"
        r"\b(implemented_by|native_decide)\b",
        re.MULTILINE,
    )
    assert prohibited.search(proof) is None
    required = (
        "import ObligationTree",
        "def NatIntNormalization : Prop :=",
        "def CoprimeNormalization : Prop :=",
        "def IntegerFermatAnchor : Prop :=",
        "def ZModNonzeroConstruction : Prop :=",
        "def IntZModTransport : Prop :=",
        "def ZModFermatAnchor : Prop :=",
        "def ZModCardTransport : Prop :=",
        "def FiniteFieldAnchor : Prop :=",
        "def UnitConstruction : Prop :=",
        "def GroupCardAnchor : Prop :=",
        "theorem finiteFieldAnchor_of_components",
        "theorem zModFermatAnchor_of_components",
        "theorem integerFermatAnchor_of_components",
        "theorem exactNatAnchor_of_components",
        "theorem fermatLittleTheorem : FermatLittleTheoremTarget := by",
        "exact Nat.ModEq.pow_card_sub_one_eq_one hp ha",
        "theorem exactNatAnchor : ObligationTree.ExactNatAnchor := by",
        "theorem fermatLittleTheorem_via_frozen_composition : FermatLittleTheoremTarget :=",
        "ObligationTree.root_of_exactNatAnchor <|",
        "exactNatAnchor_of_components natIntNormalization coprimeNormalization <|",
        "assert_no_sorry Nat.ModEq.pow_card_sub_one_eq_one",
        "#print axioms fermatLittleTheorem_via_frozen_composition",
    )
    assert all(fragment in proof for fragment in required)

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == selftest["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == selftest["base_revision"] == BASE_REVISION
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["closed_obligation_ids"] == CLOSED_IDS
    proof_edges = load("typed-graphs.json")["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0474-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert set(CLOSED_IDS) == reachable
    assert set(receipt["recipe"]["covered_ids"]) == reachable
    assert receipt["proof_body"]["source_sha256"] == digest(proof_path)
    assert receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == digest(HERE / "ObligationTree.lean")
    assert receipt["inputs"]["obligation_registry_sha256"] == digest(
        HERE / "obligation-registry.json"
    )
    assert receipt["inputs"]["typed_graphs_sha256"] == digest(HERE / "typed-graphs.json")
    assert receipt["inputs"]["check_proof_sh_sha256"] == digest(HERE / "check_proof.sh")
    assert receipt["inputs"]["lean_output_sha256"] == (
        "e93a6aac362ef0bef36790185b57e998f5ae687f1be4cb5aa39c9b8a194648ea"
    )
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    basic = mathlib / "Mathlib/FieldTheory/Finite/Basic.lean"
    order = mathlib / "Mathlib/GroupTheory/OrderOfElement.lean"
    basic_olean = mathlib / ".lake/build/lib/lean/Mathlib/FieldTheory/Finite/Basic.olean"
    order_olean = mathlib / ".lake/build/lib/lean/Mathlib/GroupTheory/OrderOfElement.olean"
    assert digest(basic) == receipt["proof_body"]["terminal_source_sha256"] == BASIC_SHA256
    assert digest(order) == receipt["proof_body"]["group_terminal_source_sha256"] == ORDER_SHA256
    assert (
        digest(basic_olean)
        == receipt["proof_body"]["terminal_olean_sha256"]
        == BASIC_OLEAN_SHA256
    )
    assert (
        digest(order_olean)
        == receipt["proof_body"]["group_terminal_olean_sha256"]
        == ORDER_OLEAN_SHA256
    )
    assert (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=mathlib, text=True).strip()
        == MATHLIB_REVISION
    )
    assert not subprocess.check_output(
        ["git", "status", "--porcelain=v1"], cwd=mathlib, text=True
    ).strip()
    assert receipt["result"]["exit_code"] == 0
    assert receipt["result"]["root_closed"] is True
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert set(instance["owned_artifacts"]) == {path.name for path in HERE.iterdir() if path.is_file()}

    expected_changed = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/Proof.lean",
        f"Stage1_Instances/{THEOREM}/README.md",
        f"Stage1_Instances/{THEOREM}/check_anchor_audit.py",
        f"Stage1_Instances/{THEOREM}/check_intake.py",
        f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
        f"Stage1_Instances/{THEOREM}/check_proof.py",
        f"Stage1_Instances/{THEOREM}/check_proof.sh",
        f"Stage1_Instances/{THEOREM}/check_statement.py",
        f"Stage1_Instances/{THEOREM}/instance.json",
        f"Stage1_Instances/{THEOREM}/proof-receipt.json",
        f"Stage1_Instances/{THEOREM}/proof-validation.md",
    }
    assert set(selftest) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert selftest["state"] == "[_]"
    assert set(selftest["changed_paths"]) == expected_changed
    assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")
    assert receipt["changed_paths"] == selftest["changed_paths"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == expected_changed

    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0474 proof phase: exact pinned root and frozen composition elaborate")
    print(f"proof sha256: {digest(proof_path)}")
    print("provisional root proposal: M0-W; theorem_complete=false")


if __name__ == "__main__":
    main()
