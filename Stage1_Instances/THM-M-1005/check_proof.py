#!/usr/bin/env python3
"""Fail-closed source, provenance, and receipt checks for S56-M-1005-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1005-PROOF"
THEOREM = "THM-M-1005"
BASE = "bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad"
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
UPSTREAM_REV = "4b63335c679c15aab74a00d37714d41aa99d701d"
UPSTREAM_RAW_SHA = "0a23b4378b723fb19080d259ead92fca5eade70c64a76205581cf83ab88f9706"
UPSTREAM_BLOB = "c7750503d8ec2a973e6ab0655c1f43f5b122b8c2"
MATHLIB_LICENSE_SHA = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TOOLCHAIN_SHA = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


for source_name in ("DoobLp.lean", "Proof.lean"):
    source = (HERE / source_name).read_text(encoding="utf-8")
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b"
    )
    assert forbidden.search(code_without_comments(source)) is None, source_name

doob = (HERE / "DoobLp.lean").read_text(encoding="utf-8")
proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
for required in (
    "Copyright (c) 2026 Raphael Coelho",
    "Released under the Apache License, Version 2.0",
    UPSTREAM_REV,
    "theorem maximal_ineq_Lp",
    "holder_step_truncated",
    "fubini_swap_truncated",
):
    assert required in doob, required
for required in (
    "import DoobLp",
    "import ObligationTree",
    "theorem doobLpMomentEstimate : Stage1Instances.THM_M_1005.Statement",
    "MeasureTheory.maximal_ineq_Lp",
    "ENNReal.ofReal_toReal hp_ne_top",
    "root_of_strongDoobTerminal",
    "#print axioms doobLpMomentEstimate",
    "#print axioms doobLpMomentEstimate_via_frozen_composition",
):
    assert required in proof, required

statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
receipt = load(HERE / "proof-receipt.json")

assert statement["canonical_formal_target"]["declaration_or_expression"] == (
    "Stage1Instances.THM_M_1005.Statement"
)
assert registry["root_obligation_id"] == "M1005-ROOT"
assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM and item["phase"] == "proof" and item["layer"] == 4
assert item["state"] in {"[ ]", "[_]"}
assert item["depends_on"] == ["S56-M-1005-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["base_revision"] == BASE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
assert receipt["proof_body"]["source_sha256"] == sha(HERE / "Proof.lean")
assert receipt["proof_body"]["vendored_source_sha256"] == sha(HERE / "DoobLp.lean")
assert receipt["proof_body"]["upstream_revision"] == UPSTREAM_REV
assert receipt["proof_body"]["upstream_raw_sha256"] == UPSTREAM_RAW_SHA
assert receipt["proof_body"]["upstream_git_blob"] == UPSTREAM_BLOB
assert receipt["proof_body"]["vendored_git_blob"] == subprocess.check_output(
    ["git", "hash-object", str(HERE / "DoobLp.lean")], text=True
).strip()
assert receipt["proof_body"]["license"] == "Apache-2.0"
assert receipt["proof_body"]["license_sha256"] == MATHLIB_LICENSE_SHA
assert receipt["proof_body"]["upstream_status"] == (
    "closed_unmerged_submission_labeled_llm_generated_without_mathlib_acceptance"
)
assert receipt["inputs"]["statement_sha256"] == sha(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_tree_sha256"] == sha(HERE / "ObligationTree.lean")
assert receipt["inputs"]["obligation_registry_sha256"] == sha(
    HERE / "obligation-registry.json"
)
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["result"]["machine_debt_proposal"].startswith("M0-L ")
assert receipt["validation_results"]
assert all(row["exit_code"] == 0 for row in receipt["validation_results"])
blocker = load(HERE / "proof-blocker.json")
assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
assert blocker["verdict"] == "resolved_by_provisional_proof_receipt"
assert blocker["remaining_proof_cut_set"] == []
assert blocker["root_closed"] is True and blocker["accepted_root_closed"] is False
assert blocker["theorem_complete"] is False
registry_ids = {row["obligation_id"] for row in registry["obligations"]}
assert set(receipt["provisionally_closed_obligation_ids"]) <= registry_ids
assert set(receipt["open_proof_or_release_boundaries"]) <= registry_ids
assert not (
    set(receipt["provisionally_closed_obligation_ids"])
    & set(receipt["open_proof_or_release_boundaries"])
)
required_machine = set(registry["frozen_denominators"]["required_machine"])
assert required_machine <= (
    set(receipt["provisionally_closed_obligation_ids"])
    | set(receipt["open_proof_or_release_boundaries"])
)
assert required_machine - set(receipt["provisionally_closed_obligation_ids"]) == {
    "M1005-S-FOUNDATION"
}
crosswalk = receipt["obligation_body_crosswalk"]
assert {
    "M1005-N-ABS-SUBMARTINGALE",
    "M1005-C-MAXIMUM",
    "M1005-L-WEAK-MAXIMAL",
    "M1005-L-LAYER-CAKE",
    "M1005-L-HOLDER",
    "M1005-L-CONSTANT",
    "M1005-T-STRONG-ESTIMATE",
    "M1005-T-ROOT-TRANSPORT",
    "M1005-ROOT",
} <= set(crosswalk)

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
assert sha(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA
assert sha(ROOT / "Formalizations/Lean/lean-toolchain") == TOOLCHAIN_SHA
assert sha(ROOT / "Formalizations/Lean/lake-manifest.json") == MANIFEST_SHA

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
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == set(selftest["changed_paths"]), (
        actual_changes, set(selftest["changed_paths"])
    )

print("PASS THM-M-1005 proof phase: vendored analytic body and exact frozen root checked")
print(f"proof source sha256: {sha(HERE / 'Proof.lean')}")
print(f"vendored source sha256: {sha(HERE / 'DoobLp.lean')}")
print("accepted state unchanged; proof proposal is provisional pending master acceptance")
