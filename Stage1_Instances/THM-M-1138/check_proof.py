#!/usr/bin/env python3
"""Fail-closed local checks for S56-M-1138-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1138-PROOF"
THEOREM = "THM-M-1138"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
EXPRESSION_SHA256 = "7ae115564e67b7065344d9b323240a2694c3f1f1f01640d1b542dcc2152f4f5c"
DENOMINATOR_SHA256 = "a2093825a633069dc09fc9bf1597396052d7f9272bb33f44ace551aa7ba1ca49"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROVISIONAL_IDS = [
    "M1138-ROOT",
    "M1138-S-DEFINITIONS",
    "M1138-S-BOUNDARIES",
    "M1138-N-COMPACT-CLOSURE",
    "M1138-L-FRONTIER-NONEMPTY",
    "M1138-T-BOUNDARY-MAX",
    "M1138-T-ROOT-TRANSPORT",
]
WITHHELD_IDS = [
    "M1138-C-CLOSURE-MAXIMIZER",
    "M1138-B-MAXIMIZER-LOCATION",
    "M1138-L-INTERIOR-LOCAL",
    "M1138-L-CONNECTED-PROPAGATION",
    "M1138-L-CONTINUITY-EXTENSION",
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
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 343
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1138-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)[ \t]+|\bextern[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem isLocalMax_laplacian_nonpos",
        "theorem laplacian_norm_sq",
        "theorem strict_subharmonic_not_isLocalMax",
        "theorem perturbed_maximizer_mem_frontier",
        "theorem boundaryMaximumPackage : BoundaryMaximumPackage",
        "theorem harmonicWeakMaximumPrinciple : HarmonicWeakMaximumPrinciple",
        "root_of_boundaryMaximumPackage boundaryMaximumPackage",
        "#print sorries boundaryMaximumPackage",
        "#print axioms harmonicWeakMaximumPrinciple",
    ):
        assert marker in proof, marker

    assert statement["declaration"] == (
        "Stage1Instances.THM_M_1138.HarmonicWeakMaximumPrinciple"
    )
    assert statement["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    required = registry["frozen_denominators"]["required_machine"]
    assert set(PROVISIONAL_IDS + WITHHELD_IDS + ["M1138-S-FOUNDATION"]) == set(required)

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    inputs = receipt["inputs"]
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
    ):
        assert inputs[key] == sha256(HERE / filename), key

    evidence = receipt["root_evidence"]
    assert evidence["root_kernel_declaration_closed"] is True
    assert evidence["terminal_package_kernel_declaration_closed"] is True
    assert evidence["accepted_root_closed"] is False
    assert evidence["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert evidence["accepted_closed_obligation_ids"] == []
    assert evidence["withheld_frozen_route_ids"] == WITHHELD_IDS
    assert evidence["foundation_credit_withheld"] is True
    assert evidence["route_reconciliation_required"] is True
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not give those nodes individual closure credit" in validation
    assert "not theorem completion" in validation
    for path in [ROOT / path for path in CHANGED_PATHS]:
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1138 proof phase: exact terminal package and public root kernel-close")
    print("frozen route reconciliation required; bypassed-node credit withheld")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
