#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for S56-M-0063-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0063-PROOF"
THEOREM = "THM-M-0063"
BASE_REVISION = "ee8c1843ef3ce74178a990f4e64554c1558c51fa"
BASE_TREE = "3a34df1cc2089854dc563ab4909cc0586713ad20"
EXPRESSION_SHA256 = "40929846f1d1d1ff4479e5be6a989358a65ecebec5a2646f6e2dab508c641a1a"
DENOMINATOR_SHA256 = "384a00c490054109773a2b786763af466971bd50c093a6facd39b614133b74a1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE = "Mathlib/GroupTheory/Perm/Subgroup.lean"
MATHLIB_SOURCE_BLOB = "31512df634de3801bcc4802599139c5e90b84ff1"
MATHLIB_SOURCE_SHA256 = "342a5720c959ad335a6f8598ab52f2c12f2a6690f17dc64bfab7157929decd12"
MATHLIB_BODY_SHA256 = "ab83db4a51a8ac5e9f645c00385828f2cb1727ffec6dc2be542071ea583814e8"
MACHINE_PROOF_IDS = [
    "M0063-ROOT",
    "M0063-N-REGULAR",
    "M0063-C-PERM-HOM",
    "M0063-L-POINTWISE",
    "M0063-L-REGULAR-FAITHFUL",
    "M0063-L-INJECTIVE",
    "M0063-C-LEFT-INVERSE",
    "M0063-C-MRANGE-EQUIV",
    "M0063-N-MRANGE-RANGE",
    "M0063-T-GENERAL",
    "M0063-T-ASSEMBLE",
]
FOUNDATION_OPEN_IDS = ["M0063-S-FOUNDATION"]
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
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1094
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0063-OBLIGATION_TREE"]
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
        "import Mathlib.GroupTheory.Perm.Subgroup",
        "theorem pointwiseFaithfulness : PointwiseFaithfulness.{u, v}",
        "exact eq_of_smul_eq_smul actionEq",
        "theorem regularFaithfulness : RegularFaithfulness.{u}",
        "theorem permutationHomConstructor : PermutationHomConstructor.{u, v}",
        "theorem genericToPermInjectivity : GenericToPermInjectivity.{u, v}",
        "theorem leftInverseConstructor : LeftInverseConstructor.{u, v}",
        "Classical.choose_spec hf.hasLeftInverse",
        "theorem mrangeEquivFromLeftInverse : MRangeEquivFromLeftInverse.{u, v}",
        "MulEquiv.ofLeftInverse' f hg",
        "theorem mrangeToRange : MRangeToRangeTransport.{u, v}",
        "generalPackage_of_components permutationHomConstructor genericToPermInjectivity",
        "exactTarget_of_generalFaithfulAction regularFaithfulness",
        "exactAssembly_of_components regularSpecialization generalFaithfulActionPackage",
        "theorem cayleyTheorem : CayleyTheoremTarget.{u}",
        "root_of_exactAssembly exactAssembly",
        "exact \u27e8Equiv.Perm.subgroupOfMulAction G G\u27e9",
        "#print sorries cayleyTheorem",
        "#print axioms cayleyTheorem",
    ):
        assert marker in proof, marker

    required_machine = registry["frozen_denominators"]["required_machine"]
    assert required_machine == [
        "M0063-ROOT",
        "M0063-S-FOUNDATION",
        *MACHINE_PROOF_IDS[1:],
    ]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0063-ROOT"
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0063.CayleyTheoremTarget"
    )

    proof_pairs = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    assert proof_pairs == {
        ("M0063-ROOT", "M0063-T-ASSEMBLE"),
        ("M0063-T-ASSEMBLE", "M0063-N-REGULAR"),
        ("M0063-T-ASSEMBLE", "M0063-T-GENERAL"),
        ("M0063-N-REGULAR", "M0063-L-REGULAR-FAITHFUL"),
        ("M0063-T-GENERAL", "M0063-C-PERM-HOM"),
        ("M0063-T-GENERAL", "M0063-L-INJECTIVE"),
        ("M0063-T-GENERAL", "M0063-C-LEFT-INVERSE"),
        ("M0063-T-GENERAL", "M0063-C-MRANGE-EQUIV"),
        ("M0063-T-GENERAL", "M0063-N-MRANGE-RANGE"),
        ("M0063-L-INJECTIVE", "M0063-L-POINTWISE"),
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["provisionally_closed_proof_obligation_ids"] == MACHINE_PROOF_IDS
    assert receipt["required_machine_open_ids"] == FOUNDATION_OPEN_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
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

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    source = mathlib / MATHLIB_SOURCE
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git_output("rev-parse", f"HEAD:{MATHLIB_SOURCE}", cwd=mathlib) == MATHLIB_SOURCE_BLOB
    assert sha256(source) == MATHLIB_SOURCE_SHA256
    lines = source.read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(lines[67:73])).hexdigest() == MATHLIB_BODY_SHA256

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
    assert "M0-W" in validation and "M0063-S-FOUNDATION" in validation
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

    print("PASS THM-M-0063 proof phase: exact frozen root closes through every proof-graph child")


if __name__ == "__main__":
    main()
