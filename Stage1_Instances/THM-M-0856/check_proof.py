#!/usr/bin/env python3
"""Fail-closed source, pin, graph, receipt, and packet checks for THM-M-0856 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0856-PROOF"
THEOREM = "THM-M-0856"
BASE_REVISION = "29a69c34f06bf3444399287853ea7806767d0944"
BASE_TREE = "de0efce35b6fcc6f851b9c2e643d61ec49d831e0"
EXPRESSION_SHA256 = "5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae"
DENOMINATOR_SHA256 = "9d6a920afceb2d2c42ce432e12008329977aa733eecb42c28ed2c44686aca20c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TERMINAL_SOURCE = "Mathlib/Combinatorics/SimpleGraph/Tutte.lean"
TERMINAL_BLOB = "4b7931e61e4dd6a3aae37fcecf698ddc238fbc4e"
TERMINAL_SOURCE_SHA256 = "47072b914aa564222ef8013092c38fa62227fea8230e308cc3eb5f11afcdffc3"
TERMINAL_OLEAN_SHA256 = "d0669fb8cd3a48f382490d39a102c7033f7a81e9582d09bda2c2ae172ff399ee"
TERMINAL_BODY_SHA256 = "424b3cde58e3407307ef398cd52eeaf2a7ce122fd5049275745c445aceeac132"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def code_only(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


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

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1410
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0856-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == "Implement or pin/import the required proof bodies without placeholders."
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    assert prohibited.search(code_only(proof)) is None
    for fragment in (
        "import ObligationTree",
        "theorem pinnedTerminal : MathlibTerminal",
        "pinned_mathlib_terminal",
        "theorem tutteOneFactor_via_frozen_composition : TutteOneFactorTarget",
        "compose_root terminal_adapter pinnedTerminal",
        "theorem tutteOneFactor_direct : TutteOneFactorTarget",
        "SimpleGraph.tutte (G := G)",
        "assert_no_sorry SimpleGraph.tutte",
        "#print axioms tutteOneFactor_via_frozen_composition",
    ):
        assert fragment in proof, fragment

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    terminal_source = mathlib / TERMINAL_SOURCE
    terminal_olean = mathlib / ".lake/build/lib/lean/Mathlib/Combinatorics/SimpleGraph/Tutte.olean"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git("rev-parse", f"HEAD:{TERMINAL_SOURCE}", cwd=mathlib) == TERMINAL_BLOB
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256_lines(terminal_source, 315, 322) == TERMINAL_BODY_SHA256
    source = terminal_source.read_text(encoding="utf-8")
    for marker in (
        "theorem tutte :",
        "not_isTutteViolator_of_isPerfectMatching hM",
        "by_cases hvOdd : Odd (Nat.card V)",
        "exact exists_isTutteViolator h",
    ):
        assert marker in source

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0856-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    required_machine = registry["frozen_denominators"]["required_machine"]
    assert len(reachable) == len(required_machine) == 44
    assert reachable == set(required_machine)
    plans = graphs["unverified_decomposition_plans"]
    assert len(plans) == 16
    assert all(
        row["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        for row in plans
    )
    composition = graphs["composition_certificates"]
    assert len(composition) == 1
    assert composition[0]["parent_obligation_id"] == "M0856-ROOT"
    assert composition[0]["required_child_ids"] == ["M0856-T-ADAPTER", "M0856-T-UPSTREAM"]
    assert composition[0]["checked_declaration"].endswith("compose_root")

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert graphs["closure_boundary"]["accepted_closed_obligations"] == []
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert receipt["proof_body"]["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert receipt["proof_body"]["terminal_body_sha256"] == TERMINAL_BODY_SHA256
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation.md"),
        ("readme_sha256", "README.md"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    root_evidence = receipt["root_evidence"]
    assert root_evidence["root_kernel_declaration_closed"] is True
    assert root_evidence["accepted_root_closed"] is False
    assert root_evidence["machine_debt_proposal"] == "M0-W"
    assert root_evidence["accepted_closed_obligation_ids"] == []
    assert root_evidence["exact_declaration_evidence_ids"] == [
        "M0856-ROOT", "M0856-T-UPSTREAM", "M0856-T-ADAPTER"
    ]
    assert set(root_evidence["mapped_proof_graph_ids"]) == reachable
    assert root_evidence["mapped_proof_graph_id_count"] == len(reachable)
    assert root_evidence["internal_per_node_composition_credit"] is False
    assert root_evidence["unverified_internal_composition_count"] == len(plans)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert receipt["inputs"]["worker_packet_sha256"] == sha256(
        ROOT / ".stage1-worker-selftest.json"
    )
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] if line.startswith("?? ") else line[2:].lstrip()
        for line in status.splitlines()
        if (line[3:] if line.startswith("?? ") else line[2:].lstrip())
        != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "16 internal" in validation
    for relative in CHANGED_PATHS:
        path = ROOT / relative
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0856 proof phase: exact pinned Tutte root and frozen composition elaborate")
    print("provisional root proposal: M0-W; 16 internal composition credits withheld")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
