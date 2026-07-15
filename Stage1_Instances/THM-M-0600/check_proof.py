#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and claim checks for THM-M-0600 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0600-PROOF"
THEOREM = "THM-M-0600"
BASE_REVISION = "557b928b377b386864527c9fb4831d45857837aa"
BASE_TREE = "e677879a6eb4cb9d6795ba1bd78726af06ab9465"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
REGISTRY_DENOMINATOR_SHA256 = (
    "071b084403b89cd9fb084d9fe7167cad1738e115f6353aaeabfab4516e93f981"
)
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
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 638
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-0600-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert item["deliverable"] == (
        "Implement or pin/import the required proof bodies without placeholders."
    )
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b|"
        r"\b(?:implemented_by|native_decide)\b",
        re.MULTILINE,
    )
    without_comments = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert prohibited.search(without_comments) is None
    for fragment in (
        "import ObligationTree",
        "def PositiveDimensionMorseNormalFormEngine : Prop",
        "theorem zeroDimensionBranch",
        "Subsingleton.elim",
        "base.left_inv base.mem_source",
        "theorem morseNormalFormEngine_of_positiveDimension",
        "(positive : PositiveDimensionMorseNormalFormEngine.{u})",
        "by_cases hn : n = 0",
        "theorem morseLemmaTarget_of_positiveDimension",
        "root_of_morseNormalFormEngine",
        "assert_no_sorry zeroDimensionBranch",
        "#print sorries morseNormalFormEngine_of_positiveDimension",
        "#print axioms morseLemmaTarget_of_positiveDimension",
    ):
        assert fragment in proof, fragment

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""

    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["root_machine_debt"] == "M3"
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == [
        "M0600-T-ENGINE"
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
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
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["provisionally_closed_obligation_ids"] == [
        "M0600-S-DIMZERO"
    ]
    assert receipt["accepted_closed_obligation_ids"] == []
    dimzero = next(
        row
        for row in registry["obligations"]
        if row["obligation_id"] == "M0600-S-DIMZERO"
    )
    assert receipt["obligation_bindings"] == [
        {
            "obligation_id": "M0600-S-DIMZERO",
            "registry_statement_fingerprint": dimzero["statement_fingerprint"],
            "registry_formal_target": "planned exact n = 0 branch",
            "implementation_declaration": (
                "Stage1Instances.THM_M_0600.zeroDimensionBranch"
            ),
            "binding_basis": (
                "The declaration specializes the exact canonical target binders, "
                "hypotheses, index bound, coordinate structure, and neighborhood "
                "identity to n = 0. Its proof derives the unique zero coordinate, "
                "inverse image p, and empty quadratic sums without changing any "
                "premise or conclusion."
            ),
            "acceptance_state": (
                "provisional_worker_selftest_pending_master_reconciliation"
            ),
        }
    ]
    assert set(receipt["exact_declarations"]) == {
        "Stage1Instances.THM_M_0600.zeroDimensionBranch",
        "Stage1Instances.THM_M_0600.morseNormalFormEngine_of_positiveDimension",
        "Stage1Instances.THM_M_0600.morseLemmaTarget_of_positiveDimension",
    }
    assert receipt["recipe"]["covered_ids"] == ["M0600-S-DIMZERO"]
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set_after"] == ["M0600-T-ENGINE"]
    assert receipt["inputs"]["lean_toolchain_sha256"] == sha256(
        ROOT / "Formalizations/Lean/lean-toolchain"
    )
    assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
        ROOT / "Formalizations/Lean/lake-manifest.json"
    )

    assert blocker["proof_body_added"] is True
    assert blocker["provisionally_closed_obligation_ids"] == [
        "M0600-S-DIMZERO"
    ]
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["first_failed_gate"].startswith("M0600-T-ENGINE")
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == ["M0600-T-ENGINE"]

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
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
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(
            not line.endswith((b" ", b"\t")) for line in data.splitlines()
        ), relative

    print("PASS THM-M-0600 partial proof: zero-dimensional branch checked")
    print("provisional obligation closure: M0600-S-DIMZERO")
    print("accepted obligation closure: none; master reconciliation pending")
    print("root closure: open (M3); theorem_complete=false")


if __name__ == "__main__":
    main()
