#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0079-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0079-PROOF"
THEOREM = "THM-M-0079"
BASE_REVISION = "2b649e7f3c2c6e3617cfb58c680e29f34d2ca5d7"
BASE_TREE = "c9dfabc312a58c05c89917f6d7298a8e140356fc"
EXPRESSION_SHA256 = "bb109f77dcbd6884a4ac90b32230cc213c08f19df6bc797ad04afac1a10da553"
DENOMINATOR_SHA256 = "88cf0ea4157fed371957616088fbbbbc9c0662d6d49d2ee1c502007b88956b92"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE_BLOB = "08cc647c220b852784860c281f06a6ede45bb06f"
MATHLIB_SOURCE_SHA256 = "e777c40c3902fd54747eac57d2952b985aff464e5d6bf803c5c78037e4c0c847"
MATHLIB_BODY_SHA256 = "1ab685e13340e3ee539c977dcd78b5f83b2cf8614feb23e5efef6b918cf6557d"
MAPPED_PROOF_IDS = [
    "M0079-ROOT",
    "M0079-L-QUOTIENT-PRETRANSITIVE",
    "M0079-C-QUOTIENT-NONEMPTY",
    "M0079-C-ACTION-CONNECTED",
    "M0079-C-ACTION-GENERATORS",
    "M0079-C-SEMIDIRECT-LABELLING",
    "M0079-L-AMBIENT-UNIQUE-LIFT",
    "M0079-C-CURRY-UNCURRY",
    "M0079-L-FUNCTOR-UNIQUENESS",
    "M0079-C-ACTION-GROUPOID-FREE",
    "M0079-L-HOM-PATH",
    "M0079-C-ROOTED-CONNECTED",
    "M0079-C-GEODESIC-TREE",
    "M0079-L-GEODESIC-ARBORESCENCE",
    "M0079-C-TREE-PATHS",
    "M0079-C-TREE-LOOPS",
    "M0079-L-TREE-EDGE-IDENTITY",
    "M0079-C-FUNCTOR-END-HOM",
    "M0079-C-COMPLEMENT-GENERATORS",
    "M0079-L-SPANNING-END-FREE",
    "M0079-L-CONNECTED-END-FREE",
    "M0079-N-QUOTIENT-END-FREE",
    "M0079-C-STABILIZER-END",
    "M0079-L-QUOTIENT-STABILIZER",
    "M0079-C-END-SUBGROUP-EQUIV",
    "M0079-T-MULEQUIV-FREENESS",
    "M0079-T-ASSEMBLE",
]
EXACT_DECLARATION_EVIDENCE_IDS = [
    "M0079-ROOT",
    "M0079-L-QUOTIENT-PRETRANSITIVE",
    "M0079-C-QUOTIENT-NONEMPTY",
    "M0079-C-ACTION-CONNECTED",
    "M0079-C-ACTION-GROUPOID-FREE",
    "M0079-L-CONNECTED-END-FREE",
    "M0079-N-QUOTIENT-END-FREE",
    "M0079-C-STABILIZER-END",
    "M0079-L-QUOTIENT-STABILIZER",
    "M0079-C-END-SUBGROUP-EQUIV",
    "M0079-T-MULEQUIV-FREENESS",
    "M0079-T-ASSEMBLE",
]
UNVERIFIED_CERTIFICATES = [
    "M0079-CERT-C-ACTION-GROUPOID-FREE",
    "M0079-CERT-C-ROOTED-CONNECTED",
    "M0079-CERT-C-GEODESIC-TREE",
    "M0079-CERT-L-GEODESIC-ARBORESCENCE",
    "M0079-CERT-C-TREE-LOOPS",
    "M0079-CERT-L-TREE-EDGE-IDENTITY",
    "M0079-CERT-C-FUNCTOR-END-HOM",
    "M0079-CERT-L-SPANNING-END-FREE",
    "M0079-CERT-L-CONNECTED-END-FREE",
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
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1 : last])).hexdigest()


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
    anchor = load(HERE / "anchor-audit.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip() == BASE_REVISION
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True
    ).strip() == BASE_TREE

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1105
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0079-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem quotientActionPretransitive : QuotientActionPretransitive.{u}",
        "exact MulAction.isPretransitive_quotient G H",
        "theorem quotientNonempty : QuotientNonempty.{u}",
        "def actionGroupoidFreeConstructor : ActionGroupoidFreeConstructor.{u}",
        "exact IsFreeGroupoid.actionGroupoidIsFree",
        "theorem connectedFreeEndConstructor : ConnectedFreeEndConstructor.{u}",
        "exact IsFreeGroupoid.endIsFreeOfConnectedFree r",
        "def stabilizerEndConstructor : StabilizerEndConstructor.{u}",
        "theorem quotientStabilizerIdentification : QuotientStabilizerIdentification.{u}",
        "exact MulAction.stabilizer_quotient H",
        "theorem mulEquivFreenessTransport : MulEquivFreenessTransport.{u}",
        "quotientActionConnected_of_components quotientActionPretransitive quotientNonempty",
        "endSubgroupEquiv_of_components stabilizerEndConstructor quotientStabilizerIdentification",
        "quotientVertexEndFree_of_components actionGroupoidFreeConstructor connectedFreeEndConstructor",
        "exactAssembly_of_end_packages quotientVertexEndFree endSubgroupEquivConstructor",
        "root_of_exactAssembly exactAssembly",
        "theorem nielsenSchreier_direct : NielsenSchreierTarget.{u}",
        "exact subgroupIsFreeOfIsFree H",
        "#print sorries subgroupIsFreeOfIsFree",
        "#print axioms nielsenSchreier_via_frozen_composition",
    ):
        assert marker in proof, marker

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    root_evidence = receipt["root_evidence"]
    assert root_evidence["root_kernel_declaration_closed"] is True
    assert root_evidence["accepted_root_closed"] is False
    assert root_evidence["machine_debt_proposal"] == "M0-W"
    assert root_evidence["closed_obligation_ids"] == []
    assert root_evidence["exact_declaration_evidence_ids"] == EXACT_DECLARATION_EVIDENCE_IDS
    assert root_evidence["mapped_proof_graph_ids"] == MAPPED_PROOF_IDS
    assert root_evidence["mapped_proof_graph_id_count"] == len(MAPPED_PROOF_IDS)
    assert root_evidence["internal_per_node_composition_credit"] is False
    assert root_evidence["unverified_internal_composition_count"] == len(
        UNVERIFIED_CERTIFICATES
    )
    assert root_evidence["unverified_internal_composition_certificate_ids"] == (
        UNVERIFIED_CERTIFICATES
    )
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(
        HERE / "obligation-registry.json"
    )
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
    assert receipt["inputs"]["anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")
    assert receipt["inputs"]["execution_dag_sha256"] == sha256(
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    )
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["theorem_complete"] is False

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0079-ROOT"
    required_machine = registry["frozen_denominators"]["required_machine"]
    assert required_machine == ["M0079-ROOT", "M0079-S-FOUNDATION", *MAPPED_PROOF_IDS[1:]]
    assert receipt["recipe"]["mapped_ids"] == MAPPED_PROOF_IDS

    proof_edges = graphs["graphs"]["proof"]["edges"]
    proof_pairs = {
        (edge["from"], edge["to"])
        for edge in proof_edges
        if edge["type"] == "proof_requires"
    }
    assert len(proof_pairs) == 30
    for pair in (
        ("M0079-ROOT", "M0079-T-ASSEMBLE"),
        ("M0079-T-ASSEMBLE", "M0079-N-QUOTIENT-END-FREE"),
        ("M0079-T-ASSEMBLE", "M0079-C-END-SUBGROUP-EQUIV"),
        ("M0079-T-ASSEMBLE", "M0079-T-MULEQUIV-FREENESS"),
    ):
        assert pair in proof_pairs
    unverified = [
        row["certificate_id"]
        for row in graphs["composition_certificates"]
        if not row["kernel_checked_interface"]
    ]
    assert unverified == UNVERIFIED_CERTIFICATES
    assert all(
        row["status"] == "planned_source_composition_pending_exact_child_harness"
        for row in graphs["composition_certificates"]
        if row["certificate_id"] in UNVERIFIED_CERTIFICATES
    )

    direct = anchor["candidates"][0]
    assert direct["candidate_id"] == "M0079-C01-MATHLIB-DIRECT"
    assert direct["declaration"] == "subgroupIsFreeOfIsFree"
    assert direct["revision"] == MATHLIB_REVISION
    assert direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == MATHLIB_SOURCE_BLOB
    assert direct["file_sha256"] == MATHLIB_SOURCE_SHA256
    assert direct["source_region_sha256"] == MATHLIB_BODY_SHA256

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    source_rel = Path("Mathlib/GroupTheory/FreeGroup/NielsenSchreier.lean")
    source = mathlib / source_rel
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip() == MATHLIB_REVISION
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip() == MATHLIB_TREE
    assert subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{source_rel}"], cwd=mathlib, text=True
    ).strip() == MATHLIB_SOURCE_BLOB
    assert not subprocess.check_output(
        ["git", "status", "--porcelain=v1"], cwd=mathlib, text=True
    ).strip()
    assert sha256(source) == MATHLIB_SOURCE_SHA256
    assert sha256_lines(source, 313, 316) == MATHLIB_BODY_SHA256
    terminal = without_comments("".join(source.read_text(encoding="utf-8").splitlines(True)[312:316]))
    assert prohibited.search(terminal) is None
    assert "IsFreeGroup.ofMulEquiv (endMulEquivSubgroup H)" in terminal

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0079-S-FOUNDATION" in validation
    for path in (
        proof_path,
        HERE / "check_proof.py",
        HERE / "check_proof.sh",
        HERE / "proof-receipt.json",
        HERE / "proof-validation.md",
        ROOT / ".stage1-worker-selftest.json",
    ):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "PASS THM-M-0079 proof phase: exact pinned M0-W root elaborates; internal composition credit withheld"
    )


if __name__ == "__main__":
    main()
