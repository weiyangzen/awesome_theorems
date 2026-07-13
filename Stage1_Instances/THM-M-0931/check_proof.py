#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for S56-M-0931-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0931-PROOF"
THEOREM = "THM-M-0931"
BASE_REVISION = "5931467f7eefac7a6e57777cc3082e4a2edc03d4"
BASE_TREE = "45a10c953e5dc79c1eb9ae7d755ee84866717775"
EXPRESSION_SHA256 = "b872e0de4aedbd0da8825d2c7dd9ecb30e01215131c61e73dc3050776711718a"
DENOMINATOR_SHA256 = "2b96d10afc8120ac78b0b3029f490c99406b9ea53a07ec3a933108354ae5cd6a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EGZ_SOURCE = "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean"
EGZ_BLOB = "dbe223c73d6c612461bc900d3d7dd70be3c1d747"
EGZ_SHA256 = "13f8adfc07c9cffd89a0c2a2d3c265348b698fbf724d8b74e6de39434bbc79f7"
INDEXED_BODY_SHA256 = "cc6b5e2b4a77fb2fd1e2fdeb38fa41aebe0a804b7212eee65b973b37f4b5145a"
MULTISET_BODY_SHA256 = "8607537347277f54f4096d259d938d96edb8408876cb9e069f52710a6a72cec4"
CHEVALLEY_SOURCE = "Mathlib/FieldTheory/ChevalleyWarning.lean"
CHEVALLEY_BLOB = "144087d302ebc67510cc3cf6903ab84706326b41"
CHEVALLEY_SHA256 = "a47186d1cd0c94b9ce1660686e8986df54e338a821e3266a9280e7f28d138684"
CHEVALLEY_BODY_SHA256 = "c2d0c18a4688430f3563715783123e7dfee1f9f0eaf50a91e9147df638da49f6"
EXACT_DECLARATION_EVIDENCE_IDS = [
    "M0931-ROOT",
    "M0931-T-ROOT-COMPOSE",
    "M0931-S-COUNT-TRANSPORT",
    "M0931-A-MULTISET-EGZ",
    "M0931-N-ENUMERATE",
    "M0931-L-INDEXED-EGZ",
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
    value = json.loads(path.read_text(encoding="utf-8"))
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
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1470
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0931-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == (
        "Implement or pin/import the required proof bodies without placeholders."
    )
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem pinnedIndexedIntegerEGZ : IndexedIntegerEGZ",
        "exact Int.erdos_ginzburg_ziv a hs",
        "theorem pinnedAtLeastCountAnchor : AtLeastCountAnchor",
        "exact Int.erdos_ginzburg_ziv_multiset s hs",
        "theorem atLeastCountAnchor_via_frozen_enumeration",
        "atLeastCountAnchor_of_indexed_and_enumeration pinnedIndexedIntegerEGZ",
        "multisetEnumerationTransport_checked",
        "theorem erdosGinzburgZiv_via_frozen_composition",
        "root_of_terminal_packages rootComposition_checked",
        "exactCountTransport_checked",
        "theorem erdosGinzburgZiv_direct : ErdosGinzburgZivTarget",
        "exact Int.erdos_ginzburg_ziv_multiset s hs.ge",
        "theorem erdosGinzburgZiv : ErdosGinzburgZivTarget",
        "assert_no_sorry Int.erdos_ginzburg_ziv_multiset",
        "#print axioms erdosGinzburgZiv",
    ):
        assert marker in proof, marker

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0931-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

    proof_children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            proof_children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0931-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(proof_children.get(obligation, []))
    assert reachable == set(EXACT_DECLARATION_EVIDENCE_IDS)
    plans = graphs["unverified_decomposition_plans"]
    assert len(plans) == 6
    assert all(
        row["status"]
        == "source_body_decomposition_unverified_as_child_to_parent_composition"
        for row in plans
    )

    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

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
    assert receipt["proof_body"]["indexed_body_sha256"] == INDEXED_BODY_SHA256
    assert receipt["proof_body"]["multiset_body_sha256"] == MULTISET_BODY_SHA256
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
    root_evidence = receipt["root_evidence"]
    assert root_evidence["root_kernel_declaration_closed"] is True
    assert root_evidence["accepted_root_closed"] is False
    assert root_evidence["machine_debt_proposal"] == "M0-W"
    assert root_evidence["closed_obligation_ids"] == []
    assert root_evidence["exact_declaration_evidence_ids"] == EXACT_DECLARATION_EVIDENCE_IDS
    assert set(root_evidence["mapped_proof_graph_ids"]) == reachable
    assert root_evidence["mapped_proof_graph_id_count"] == len(reachable)
    assert root_evidence["internal_per_node_composition_credit"] is False
    assert root_evidence["unverified_internal_composition_count"] == len(plans)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["placeholder_scan"] == "pass"
    assert receipt["result"]["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    egz = mathlib / EGZ_SOURCE
    chevalley = mathlib / CHEVALLEY_SOURCE
    assert git("rev-parse", f"HEAD:{EGZ_SOURCE}", cwd=mathlib) == EGZ_BLOB
    assert git("rev-parse", f"HEAD:{CHEVALLEY_SOURCE}", cwd=mathlib) == CHEVALLEY_BLOB
    assert sha256(egz) == EGZ_SHA256 and sha256(chevalley) == CHEVALLEY_SHA256
    egz_lines = egz.read_bytes().splitlines(keepends=True)
    chevalley_lines = chevalley.read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(egz_lines[109:178])).hexdigest() == INDEXED_BODY_SHA256
    assert hashlib.sha256(b"".join(egz_lines[191:195])).hexdigest() == MULTISET_BODY_SHA256
    assert hashlib.sha256(b"".join(chevalley_lines[188:194])).hexdigest() == CHEVALLEY_BODY_SHA256
    terminal_sources = without_comments(egz.read_text(encoding="utf-8"))
    terminal_sources += without_comments(chevalley.read_text(encoding="utf-8"))
    assert prohibited.search(terminal_sources) is None

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
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "six internal" in validation
    for relative in CHANGED_PATHS:
        path = ROOT / relative
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0931 proof phase: exact pinned root and frozen composition elaborate")
    print("provisional root proposal: M0-W; internal per-node composition credit withheld")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
