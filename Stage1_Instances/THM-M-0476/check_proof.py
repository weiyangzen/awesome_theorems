#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for S56-M-0476-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0476-PROOF"
THEOREM = "THM-M-0476"
BASE_REVISION = "dc600635160cace0916df5234bf8808c39dc656d"
BASE_TREE = "8ee34b31ec38be1ef067aaab38c9a4cb4935b75a"
EXPRESSION_SHA256 = "ee76edb160426d3e8d95b11bfedca7febcfe915f50007e042875c922ebc8a4ac"
DENOMINATOR_SHA256 = "9375f9b987132465572c04a019d70b32638823c1279dd91a7935007f108fe62b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
WILSON_SOURCE = Path("Mathlib/NumberTheory/Wilson.lean")
WILSON_BLOB = "9401f7b96b43c2c0afa1f823857bd31a20ae0ac2"
WILSON_SHA256 = "7bd6ec0e909f037f8632e1b495f9647a61fe950f3bfe3af98a5a22914622aeb7"
WILSON_OLEAN_SHA256 = "c932050e2dca74d0ba033d36338122b2927bad7800f2ac592a20daf42c91d9eb"
FINITE_SOURCE = Path("Mathlib/FieldTheory/Finite/Basic.lean")
FINITE_BLOB = "fb3668d594f865e52f20c8af45e91e7e3b1eebd8"
FINITE_SHA256 = "808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44"
FINITE_OLEAN_SHA256 = "4cede73b3c7f85692307990d9cdaf819b5ac61dc50272e31586b7899d9f32119"
PROOF_GRAPH_IDS = [
    "M0476-ROOT",
    "M0476-S-FACT-TRANSPORT",
    "M0476-T-COMPOSE",
    "M0476-N-FACTORIAL-PRODUCT",
    "M0476-L-FACTORIAL-INTERVAL",
    "M0476-T-NAT-CAST-PRODUCT",
    "M0476-C-RESIDUE-UNITS-BIJECTION",
    "M0476-N-PRIME-ENDPOINT",
    "M0476-B-UNIT-VAL-RANGE",
    "M0476-L-UNIT-VAL-INJECTIVE",
    "M0476-C-RESIDUE-TO-UNIT",
    "M0476-T-REPRESENTATIVE-COE",
    "M0476-T-UNITS-COE-NEGONE",
    "M0476-T-INSERT-NEGONE",
    "M0476-C-INVERSE-PAIRING",
    "M0476-L-INVERSE-FIXED-POINTS",
]
PINNED_BRIDGE_IDS = ["M0476-L-WILSON", "M0476-L-UNITS-PRODUCT"]
PROVISIONAL_IDS = [
    "M0476-ROOT",
    "M0476-S-FACT-TRANSPORT",
    "M0476-T-COMPOSE",
    "M0476-L-WILSON",
    "M0476-N-FACTORIAL-PRODUCT",
    "M0476-L-FACTORIAL-INTERVAL",
    "M0476-T-NAT-CAST-PRODUCT",
    "M0476-N-PRIME-ENDPOINT",
    "M0476-C-RESIDUE-UNITS-BIJECTION",
    "M0476-B-UNIT-VAL-RANGE",
    "M0476-L-UNIT-VAL-INJECTIVE",
    "M0476-C-RESIDUE-TO-UNIT",
    "M0476-T-REPRESENTATIVE-COE",
    "M0476-L-UNITS-PRODUCT",
    "M0476-C-INVERSE-PAIRING",
    "M0476-L-INVERSE-FIXED-POINTS",
    "M0476-T-INSERT-NEGONE",
    "M0476-T-UNITS-COE-NEGONE",
]
OPEN_MACHINE_IDS = [
    "M0476-S-INTERFACE",
    "M0476-S-BOUNDARY",
    "M0476-S-FOUNDATION",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_intake.py",
    f"Stage1_Instances/{THEOREM}/check_statement.py",
    f"Stage1_Instances/{THEOREM}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/instance.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
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
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1357,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0476-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0476-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"
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
        "theorem factWilsonAnchor_mathlib : FactWilsonAnchor := by",
        "exact ZMod.wilsons_lemma p",
        "theorem unitProductIdentity_mathlib : UnitProductIdentity := by",
        "exact FiniteField.prod_univ_units_id_eq_neg_one",
        "theorem factorialIntervalIdentity : FactorialIntervalIdentity := by",
        "theorem natIntervalCastIdentity : NatIntervalCastIdentity := by",
        "factorialProduct_of_identities factorialIntervalIdentity natIntervalCastIdentity",
        "residueUnitsProduct_of_components primeEndpointIdentity unitRepresentativeInPrimeRange",
        "unitEraseProduct_of_inversion inverseFixedPointClassification",
        "unitProductIdentity_of_erase unitEraseNegOneProduct",
        "unitsProductBridge_of_components unitProductIdentity_expanded",
        "factWilsonAnchor_of_bridges factorialProduct residueUnitsProduct unitsProductBridge",
        "theorem wilsonTheorem_after_factTransport : WilsonTheoremTarget :=",
        "root_of_factWilsonAnchor factWilsonAnchor_expanded",
        "theorem wilsonTheorem_via_frozen_composition : WilsonTheoremTarget :=",
        "theorem wilsonTheorem : WilsonTheoremTarget :=",
        "root_of_composedTarget (root_of_factWilsonAnchor factWilsonAnchor_mathlib)",
        "assert_no_sorry wilsonTheorem_via_frozen_composition",
        "assert_no_sorry wilsonTheorem",
        "#print axioms wilsonTheorem_via_frozen_composition",
        "#print axioms wilsonTheorem",
    ):
        assert marker in proof, marker

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0476-ROOT"
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert set(registry["frozen_denominators"]["required_machine"]) == set(
        PROVISIONAL_IDS + OPEN_MACHINE_IDS
    )

    children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0476-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert reachable == set(PROOF_GRAPH_IDS)
    assert set(PINNED_BRIDGE_IDS).isdisjoint(reachable)
    assert set(PROVISIONAL_IDS) == reachable | set(PINNED_BRIDGE_IDS)

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["provisionally_closed_proof_obligation_ids"] == PROVISIONAL_IDS
    assert receipt["required_machine_open_ids"] == OPEN_MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["recipe"]["covered_obligation_ids"]) == set(PROVISIONAL_IDS)
    receipt_certificates = {
        row["parent"]: row for row in receipt["composition_certificates"]
    }
    expected_certificate_declarations = {
        "M0476-N-FACTORIAL-PRODUCT": "Stage1Instances.THM_M_0476.Proof.factorialProduct",
        "M0476-C-RESIDUE-UNITS-BIJECTION": "Stage1Instances.THM_M_0476.Proof.residueUnitsProduct",
        "M0476-C-INVERSE-PAIRING": "Stage1Instances.THM_M_0476.Proof.unitEraseNegOneProduct",
        "M0476-T-INSERT-NEGONE": "Stage1Instances.THM_M_0476.Proof.unitProductIdentity_expanded",
        "M0476-T-UNITS-COE-NEGONE": "Stage1Instances.THM_M_0476.Proof.unitsProductBridge",
        "M0476-T-COMPOSE": "Stage1Instances.THM_M_0476.Proof.factWilsonAnchor_expanded",
        "M0476-S-FACT-TRANSPORT": "Stage1Instances.THM_M_0476.Proof.wilsonTheorem_after_factTransport",
        "M0476-ROOT": "Stage1Instances.THM_M_0476.Proof.wilsonTheorem_via_frozen_composition",
    }
    assert set(receipt_certificates) == set(children)
    assert set(expected_certificate_declarations) == set(children)
    for parent, child_ids in children.items():
        certificate = receipt_certificates[parent]
        assert certificate["children"] == child_ids
        assert certificate["declaration"] == expected_certificate_declarations[parent]
        frozen = next(
            row for row in graphs["composition_certificates"] if row["parent_id"] == parent
        )
        assert certificate["checked_composer"] == frozen["declaration"]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["source_git_blob"] == git_output(
        "hash-object", str(proof_path.relative_to(ROOT))
    )
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
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    for source_rel, blob, source_hash, olean_hash in (
        (WILSON_SOURCE, WILSON_BLOB, WILSON_SHA256, WILSON_OLEAN_SHA256),
        (FINITE_SOURCE, FINITE_BLOB, FINITE_SHA256, FINITE_OLEAN_SHA256),
    ):
        source = mathlib / source_rel
        olean = mathlib / ".lake/build/lib/lean" / source_rel.with_suffix(".olean")
        assert git_output("rev-parse", f"HEAD:{source_rel}", cwd=mathlib) == blob
        assert sha256(source) == source_hash
        assert sha256(olean) == olean_hash
        assert prohibited.search(without_comments(source.read_text(encoding="utf-8"))) is None
    wilson = (mathlib / WILSON_SOURCE).read_text(encoding="utf-8")
    finite = (mathlib / FINITE_SOURCE).read_text(encoding="utf-8")
    for marker in (
        "theorem wilsons_lemma : ((p - 1)! : ZMod p) = -1 := by",
        "Finset.prod_Ico_id_eq_factorial",
        "prod_natCast",
        "refine prod_bij",
        "prod_univ_units_id_eq_neg_one",
    ):
        assert marker in wilson
    for marker in (
        "theorem prod_univ_units_id_eq_neg_one",
        "prod_involution",
        "Units.inv_eq_self_iff",
        "insert_erase",
        "prod_insert",
    ):
        assert marker in finite

    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert set(instance["owned_artifacts"]) == {
        path.name for path in HERE.iterdir() if path.is_file()
    }

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
        if (line[3:] if line[:2] == "??" else line[2:].lstrip()).rstrip("/")
        != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0476-S-FOUNDATION" in validation
    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0476 proof phase: exact pinned root and frozen composition close")
    print(f"proof source sha256: {sha256(proof_path)}")
    print("provisional root proposal: M0-W; theorem_complete=false")


if __name__ == "__main__":
    main()
