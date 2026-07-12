#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for THM-M-0843 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0843-PROOF"
THEOREM = "THM-M-0843"
BASE_REVISION = "3815f6945257af057dfb5e6b6dfe2be5b6f451d9"
BASE_TREE = "21a4f0ff758e83ab68c05b7741cdc4720f95cb1c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TERMINAL_SOURCE_SHA256 = "eee7f2c505130c4a09fa8e62dca7bc1bbfaff90c18e86e9ad43f44f7f0ea8fd6"
TERMINAL_OLEAN_SHA256 = "15ff1ca1a19a299eacf3e96bdbd26da862bc4f1adf8e0e7881a5a4c579aa4718"
STATEMENT_EXPRESSION_SHA256 = "3fe13f3562cb642e45e467687508ac44f945e9848ff53d22b9cf068d7ec11219"
REGISTRY_DENOMINATOR_SHA256 = "5373c66a953b356d53f3849d2b3d2cb9657189e38b458964f992817b66751f06"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
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
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1032
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-0843-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert item["deliverable"] == "Implement or pin/import the required proof bodies without placeholders."
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_dag["accepted_states"] == []
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe)\b|"
        r"\b(?:implemented_by|native_decide)\b",
        re.MULTILINE,
    )
    assert prohibited.search(proof) is None
    for fragment in (
        "import ObligationTree",
        "theorem pinnedTerminal",
        "THM_M_0843_Obligations.pinned_mathlib_terminal",
        "theorem szemerediRegularity_via_frozen_composition",
        "THM_M_0843_Obligations.compose_root",
        "THM_M_0843_Obligations.terminal_adapter pinnedTerminal",
        "theorem szemerediRegularity",
        "exact _root_.szemeredi_regularity G hEpsilon hCard",
        "assert_no_sorry _root_.szemeredi_regularity",
        "#print axioms szemerediRegularity_via_frozen_composition",
    ):
        assert fragment in proof, fragment

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    terminal_source = mathlib / "Mathlib/Combinatorics/SimpleGraph/Regularity/Lemma.lean"
    terminal_olean = mathlib / ".lake/build/lib/lean/Mathlib/Combinatorics/SimpleGraph/Regularity/Lemma.olean"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    source = terminal_source.read_text(encoding="utf-8")
    for marker in (
        "theorem szemeredi_regularity",
        "obtain hα | hα := le_total (card α) (bound ε l)",
        "obtain hε₁ | hε₁ := le_total 1 ε",
        "suffices h : ∀ i",
        "induction i with",
        "energy_increment hP₁",
    ):
        assert marker in source

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0843-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert len(reachable) == 38
    assert {"M0843-ROOT", "M0843-T-UPSTREAM", "M0843-T-ADAPTER"} <= reachable
    plans = graphs["unverified_decomposition_plans"]
    assert len(plans) == 18
    assert all(
        row["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        for row in plans
    )

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert registry["status_observed_after_freeze"]["closed_obligations"] == []
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert receipt["proof_body"]["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(HERE / "obligation-registry.json")
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
    assert receipt["root_evidence"]["root_kernel_declaration_closed"] is True
    assert receipt["root_evidence"]["accepted_root_closed"] is False
    assert receipt["root_evidence"]["machine_debt_proposal"] == "M0-W"
    assert receipt["root_evidence"]["closed_obligation_ids"] == []
    assert receipt["root_evidence"]["exact_declaration_evidence_ids"] == [
        "M0843-ROOT", "M0843-T-UPSTREAM", "M0843-T-ADAPTER"
    ]
    assert set(receipt["root_evidence"]["mapped_proof_graph_ids"]) == reachable
    assert receipt["root_evidence"]["mapped_proof_graph_id_count"] == len(reachable)
    assert receipt["root_evidence"]["internal_per_node_composition_credit"] is False
    assert receipt["root_evidence"]["unverified_internal_composition_count"] == len(plans)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
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

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        path = ROOT / relative
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0843 proof phase: exact pinned root and frozen composition elaborate")
    print("provisional root proposal: M0-W; internal per-node composition credit withheld")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
