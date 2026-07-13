#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for THM-M-0484 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0484-PROOF"
THEOREM = "THM-M-0484"
BASE_REVISION = "a1c9974d7fb28cd680e6494b968544bf801a93a2"
BASE_TREE = "1fa287bc821355aca2ca9e3ce107830a3eb58e64"
EXPRESSION_SHA256 = "6bd6024bd44d0bd9c50f6425b9ce5fdaecaf783ac84d32688717d3bde3151aea"
DENOMINATOR_SHA256 = "af0c1b5d7bfd4da0a7f1b982646906d20217976af4c5805295d37e43d0b39edf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TERMINAL_SOURCE_SHA256 = "6321c156165f59d49954c0e6e47706e765c0277df20b97a20333ceba29e8bead"
TERMINAL_SOURCE_BLOB = "36af70028d43c613055738999815ed2e88e84bd4"
TERMINAL_OLEAN_SHA256 = "c02832844a7c1605945cf05750cbcc0909909124ea7ba45f335888bae0157844"
TERMINAL_BODY_IDS = [
    "8ec5fa60da0232f21b8a79ca9a7a846be51b71ed8b5bae0016943f880599efaf",
    "8f45e13a6d27e866e46e24320d770ad4c0a4e1b01412b2c32e708c00a29d01dd",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}
EXACT_EVIDENCE_IDS = {
    "M0484-ROOT",
    "M0484-T-ASSEMBLE",
    "M0484-T-SUFFICIENCY",
    "M0484-T-NECESSITY",
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
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).rstrip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    audit = load(HERE / "anchor-audit.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1365
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0484-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0484-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for fragment in (
        "import ObligationTree",
        "theorem pinnedSufficiency : ObligationTree.SufficiencyTarget",
        "exact lucas_lehmer_sufficiency p (by omega) htest",
        "theorem pinnedNecessity : ObligationTree.NecessityTarget",
        "exact lucas_lehmer_necessity p hp hprime",
        "theorem assembledRoot : LucasLehmerTestTarget",
        "ObligationTree.root_of_directions",
        "theorem lucasLehmerCriterion : LucasLehmerTestTarget",
        "ObligationTree.root_of_terminal assembledRoot",
        "assert_no_sorry lucas_lehmer_sufficiency",
        "#print axioms lucasLehmerCriterion",
    ):
        assert fragment in proof, fragment

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0484.LucasLehmerTestTarget"
    )
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0484-ROOT"
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["accepted_closed_obligations"] == []
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0484-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert len(reachable) == 18
    assert EXACT_EVIDENCE_IDS <= reachable
    plans = graphs["unverified_decomposition_plans"]
    assert len(plans) == 17
    assert len({plan["parent"] for plan in plans}) == 10
    assert all(
        plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        and plan["required_before_parent_machine_acceptance"] is True
        for plan in plans
    )

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    terminal_source_rel = Path("Mathlib/NumberTheory/LucasLehmer.lean")
    terminal_source = mathlib / terminal_source_rel
    terminal_olean = mathlib / ".lake/build/lib/lean/Mathlib/NumberTheory/LucasLehmer.olean"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git("rev-parse", f"HEAD:{terminal_source_rel}", cwd=mathlib) == TERMINAL_SOURCE_BLOB
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert terminal_olean.stat().st_size == 516240
    source_lines = terminal_source.read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(source_lines[580:591])).hexdigest() == TERMINAL_BODY_IDS[0]
    assert hashlib.sha256(b"".join(source_lines[592:608])).hexdigest() == TERMINAL_BODY_IDS[1]
    assert hashlib.sha256(b"".join(source_lines[580:608])).hexdigest() == (
        "02f91496f97c76dca5e982eecba7b79b463e5c4a597c8e1067113aa38b37f266"
    )
    source = terminal_source.read_text(encoding="utf-8")
    for marker in (
        "theorem lucas_lehmer_sufficiency",
        "have h\u2081 := order_ineq p' t",
        "have h\u2082 := Nat.minFac_sq_le_self",
        "theorem lucas_lehmer_necessity",
        "rw [sZMod_eq_s p', \u2190 X.fst_intCast, X.closed_form",
        "have := X.\u03c9_pow_trace",
    ):
        assert marker in source, marker
    direct = next(
        row
        for row in audit["candidates"]
        if row["candidate_id"] == "M0484-C01-MATHLIB-EXACT-COMPOSITION"
    )
    assert [value.split(":", 1)[1] for value in direct["terminal_proof_body_ids"]] == (
        TERMINAL_BODY_IDS
    )

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert receipt["proof_body"]["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert {row["obligation_id"] for row in receipt["exact_declaration_evidence"]} == (
        EXACT_EVIDENCE_IDS
    )
    assert receipt["closed_obligation_ids"] == receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["mapped_proof_graph_ids"]) == reachable
    assert receipt["mapped_proof_graph_id_count"] == len(reachable)
    assert receipt["internal_composition_boundary"]["internal_per_node_composition_credit"] is False
    assert receipt["internal_composition_boundary"]["unverified_internal_composition_count"] == 17
    assert receipt["recipe"]["covered_ids"] == [
        "M0484-ROOT",
        "M0484-T-ASSEMBLE",
        "M0484-T-SUFFICIENCY",
        "M0484-T-NECESSITY",
    ]
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_declaration_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "17" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0484 proof phase: exact pinned terminals and frozen root elaborate")
    print("provisional root proposal: M0-W; internal per-node composition credit withheld")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
