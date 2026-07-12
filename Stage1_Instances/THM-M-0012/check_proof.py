#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0012-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0012-PROOF"
THEOREM = "THM-M-0012"
BASE = "c2467750f2cdb3960045c83e819d96687253303d"
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE_SHA = "f6159d7625ca323846088b04ae89fca501bb040fcdce982f8f24c453e587d491"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


proof_path = HERE / "Proof.lean"
proof = proof_path.read_text(encoding="utf-8")
without_comments = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
without_comments = re.sub(r"--.*", "", without_comments)
forbidden = re.compile(
    r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b"
)
assert forbidden.search(without_comments) is None

for required in (
    "import ObligationTree",
    "theorem fundamentalTheoremOfAlgebra : FundamentalTheoremOfAlgebraTarget",
    "Complex.exists_root ((nonconstant_iff_degree_pos f).1 hf)",
    "theorem reciprocalDifferentiability : ReciprocalDifferentiabilityEngine",
    "theorem reciprocalDecay : ReciprocalDecayEngine",
    "theorem liouvilleZero : LiouvilleZeroEngine",
    "theorem polynomialConstant : PolynomialConstantEngine",
    "theorem noRootContradiction : NoRootContradictionEngine",
    "theorem positiveDegreeAnchor_expanded : PositiveDegreeAnchor",
    "theorem positiveDegreeAnchor_mathlib : PositiveDegreeAnchor",
    "theorem fundamentalTheoremOfAlgebra_via_frozen_composition",
    "theorem fundamentalTheoremOfAlgebra_via_pinned_composition",
    "root_of_degreeBridge_and_positiveDegreeAnchor nonconstantDegreeBridge",
    "noRootContradiction_of_engines reciprocalDifferentiability reciprocalDecay",
    "#print axioms fundamentalTheoremOfAlgebra",
    "#print axioms fundamentalTheoremOfAlgebra_via_frozen_composition",
    "#print axioms Complex.exists_root",
):
    assert required in proof, required

statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
task_dag = load(HERE / "task-dag.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
receipt = load(HERE / "proof-receipt.json")

assert statement["canonical_formal_target"]["declaration_or_expression"] == (
    "Stage1Instances.THM_M_0012.FundamentalTheoremOfAlgebraTarget"
)
assert registry["root_obligation_id"] == "M0012-ROOT"
assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM and item["phase"] == "proof" and item["layer"] == 4
assert item["state"] in {"[ ]", "[_]"}
assert item["depends_on"] == ["S56-M-0012-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
assert task["state"] == "open" and task_dag["accepted_states"] == []

assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["base_revision"] == BASE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["accepted"] is False
assert receipt["proposed_state"] == "[_]"
assert receipt["proof_body"]["source_sha256"] == sha(proof_path)
assert receipt["inputs"]["statement_sha256"] == sha(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_tree_sha256"] == sha(HERE / "ObligationTree.lean")
assert receipt["inputs"]["obligation_registry_sha256"] == sha(
    HERE / "obligation-registry.json"
)
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["theorem_complete"] is False

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True
).strip() == MATHLIB_REV
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD^{tree}"], text=True
).strip() == MATHLIB_TREE
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "status", "--short"], text=True
) == ""
mathlib_source = mathlib / "Mathlib/Analysis/Complex/Polynomial/Basic.lean"
assert sha(mathlib_source) == MATHLIB_SOURCE_SHA
mathlib_text = mathlib_source.read_text(encoding="utf-8")
for marker in (
    "theorem exists_root {f : ℂ[X]}",
    "by_contra! hf'",
    "(f.differentiable.inv hf').apply_eq_of_tendsto_cocompact",
    "Filter.tendsto_inv₀_cobounded.comp",
    "using f.tendsto_norm_atTop",
    "Polynomial.funext",
):
    assert marker in mathlib_text, marker
terminal_body = mathlib_text.split("theorem exists_root {f : ℂ[X]}", 1)[1].split(
    "instance isAlgClosed", 1
)[0]
assert forbidden.search(terminal_body) is None

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    assert set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == BASE
    assert selftest["changed_paths"] == receipt["changed_paths"]
    assert selftest["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == set(selftest["changed_paths"]), (
        actual_changes,
        set(selftest["changed_paths"]),
    )

print("PASS THM-M-0012 proof phase: exact root and frozen analytic composition checked")
print(f"proof source sha256: {sha(proof_path)}")
print("accepted state unchanged; proof proposal is provisional pending master acceptance")
