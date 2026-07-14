#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-1140-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1140-PROOF"
THEOREM = "THM-M-1140"
BASE = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
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
    r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|implemented_by|"
    r"native_decide|extern)\b"
)
assert forbidden.search(without_comments) is None

for required in (
    "import ObligationTree",
    "theorem strictSubharmonic_le_of_boundary_le",
    "theorem gaussian_annulus_comparison",
    "theorem tangentBarrier_derivative_contradiction",
    "theorem tangentBall_geometry",
    "theorem no_strict_drop_in_tangent_neighborhood",
    "theorem interiorLocalRigidity : InteriorLocalRigidity := by",
    "theorem connectedLevelPropagation : ConnectedLevelPropagation := by",
    "theorem harmonicStrongMaximumPrinciple : HarmonicStrongMaximumPrinciple :=",
    "harmonicStrongMaximumPrinciple_of_packages interiorLocalRigidity connectedLevelPropagation",
    "#print axioms harmonicStrongMaximumPrinciple",
    "#print sorries harmonicStrongMaximumPrinciple",
):
    assert required in proof, required

statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
receipt = load(HERE / "proof-receipt.json")

assert statement["canonical_formal_target"]["declaration"] == (
    "Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple"
)
assert registry["root_obligation_id"] == "M1140-ROOT"
assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
assert registry["denominator_sha256"] == (
    "355cbcf3b25f5e8ac67d3d814a268744dbe8ba8ae8afaec651199e64d6520bee"
)
required_machine = set(registry["frozen_denominators"]["required_machine"])
assert required_machine == set(receipt["provisionally_closed_obligation_ids"])
assert graphs["closure_boundary"]["root_machine_debt"] == "M3"

item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM
assert item["phase"] == "proof" and item["layer"] == 4
assert item["state"] in {"[ ]", "[_]"}
assert item["depends_on"] == ["S56-M-1140-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["base_revision"] == BASE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
assert receipt["canonical_target"] == (
    "Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple"
)
assert receipt["proof_body"]["source_sha256"] == sha(proof_path)
assert receipt["inputs"]["check_proof_sh_sha256"] == sha(HERE / "check_proof.sh")
assert receipt["inputs"]["check_proof_py_sha256"] == sha(Path(__file__))
assert receipt["inputs"]["statement_sha256"] == sha(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_tree_sha256"] == sha(HERE / "ObligationTree.lean")
assert receipt["inputs"]["obligation_registry_sha256"] == sha(
    HERE / "obligation-registry.json"
)
assert receipt["inputs"]["typed_graphs_sha256"] == sha(HERE / "typed-graphs.json")
assert receipt["inputs"]["validation_specs_sha256"] == sha(HERE / "validation-specs.json")
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["accepted_root_closed"] is False
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

print("PASS THM-M-1140 proof phase: exact local strong maximum root checked")
print(f"proof source sha256: {sha(proof_path)}")
print("accepted state unchanged; proof proposal is provisional pending master acceptance")
