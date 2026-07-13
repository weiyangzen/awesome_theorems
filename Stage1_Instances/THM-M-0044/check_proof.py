#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0044-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0044-PROOF"
THEOREM = "THM-M-0044"
BASE = "c5f6fb269f6eb84efa935ee66c4e9bab92495e61"
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"


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
    "private theorem svdBasisTall",
    "L.isSymmetric_adjoint_comp_self",
    "hSsym.eigenvectorBasis",
    "L.isPositive_adjoint_comp_self.nonneg_eigenvalues",
    "exists_orthonormalBasis_extension_of_card_eq",
    "private theorem isFullSVD_of_le",
    "toMatrix_orthonormalBasis_mem_unitary",
    "private theorem isFullSVD_of_ge",
    "isFullSVD_of_le hmn A.conjTranspose",
    "private theorem fullSVDOver",
    "theorem singularValueDecomposition : SingularValueDecompositionTarget",
    "⟨fullSVDOver Real, fullSVDOver Complex⟩",
    "#print axioms singularValueDecomposition",
):
    assert required in proof, required

registry = load(HERE / "obligation-registry.json")
task_dag = load(HERE / "task-dag.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
receipt = load(HERE / "proof-receipt.json")

assert registry["root_obligation_id"] == "M0044-ROOT"
assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM and item["phase"] == "proof" and item["layer"] == 4
assert item["state"] in {"[ ]", "[_]"}
assert item["depends_on"] == ["S56-M-0044-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
assert task["state"] == "open" and task_dag["accepted_states"] == []

assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["base_revision"] == BASE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
assert receipt["proof_body"]["source_sha256"] == sha(proof_path)
for key, name in (
    ("statement_sha256", "Statement.lean"),
    ("obligation_tree_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
    ("validation_specs_sha256", "validation-specs.json"),
    ("anchor_audit_sha256", "anchor-audit.json"),
):
    assert receipt["inputs"][key] == sha(HERE / name)
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["accepted_closed_obligation_ids"] == []

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

selftest = load(ROOT / ".stage1-worker-selftest.json")
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

print("PASS THM-M-0044 proof phase: exact Real-and-Complex rectangular SVD root checked")
print(f"proof source sha256: {sha(proof_path)}")
print("accepted state unchanged; proof proposal is provisional pending master acceptance")
