#!/usr/bin/env python3
"""Fail-closed source and receipt checks for the THM-M-1009 proof node."""

import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name: str):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def require(value, message: str) -> None:
    if not value:
        raise SystemExit("proof check failed: " + message)


proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
without_comments = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
without_comments = re.sub(r"--.*", "", without_comments)
registry = load("obligation-registry.json")
receipt = load("proof-receipt.json")
status = load("proof-status.json")

require(registry["theorem_id"] == "THM-M-1009", "wrong obligation registry")
require(
    registry["frozen_against_statement_sha256"] == sha256("statement.json"),
    "statement record drifted after obligation freeze",
)
require("import Statement" in proof, "proof does not import the frozen statement")
require("import ObligationTree" in proof, "proof does not import the frozen obligation tree")
require(
    "theorem erdosRenyiLowerBoundTarget : ErdosRenyiLowerBoundTarget.{u}" in proof,
    "exact frozen root wrapper missing",
)
for declaration in (
    "theorem finite_secondMoment_bound",
    "theorem finite_eventMassRatio_le_eventUnion",
    "theorem shifted_secondMoment_bound",
    "theorem eventMassRatio_le_tail_add_error",
    "theorem limsup_eventMassRatio_le_eventTail",
    "theorem iInter_eventTail_eq_limsup",
    "theorem tendsto_eventTail_measureReal",
    "theorem erdosRenyiLowerBound",
    "theorem erdosRenyiObligationRoot : ObligationTree.Root",
    "theorem erdosRenyiObligationRoot_via_frozen_composition",
    "ObligationTree.root_compose erdosRenyiObligationRoot",
):
    require(declaration in proof, f"required proof component missing: {declaration}")
prohibited = re.compile(
    r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|extern|"
    r"implemented_by|native_decide)\b"
)
require(prohibited.search(without_comments) is None, "prohibited proof construct")

required_machine = registry["frozen_denominators"]["required_machine"]
require(receipt["item_id"] == "S56-M-1009-PROOF", "wrong receipt item")
require(receipt["support_state"] == "provisional_worker_selftest", "receipt is not provisional")
require(receipt["proposed_state"] == "[_]", "wrong proposed worker state")
require(receipt["accepted"] is False, "worker receipt cannot be accepted")
require(
    receipt["provisionally_closed_obligation_ids"] == required_machine,
    "provisional closure does not cover the frozen machine denominator",
)
require(receipt["accepted_closed_obligation_ids"] == [], "worker claimed accepted obligations")
require(receipt["inputs"]["proof_sha256"] == sha256("Proof.lean"), "stale proof hash")
require(receipt["inputs"]["statement_sha256"] == sha256("Statement.lean"), "stale statement hash")
require(
    receipt["inputs"]["obligation_tree_sha256"] == sha256("ObligationTree.lean"),
    "stale obligation-tree hash",
)
require(
    receipt["inputs"]["obligation_registry_sha256"] == sha256("obligation-registry.json"),
    "stale obligation-registry hash",
)
require(receipt["inputs"]["typed_graphs_sha256"] == sha256("typed-graphs.json"), "stale graph hash")
require(
    receipt["inputs"]["validation_specs_sha256"] == sha256("validation-specs.json"),
    "stale validation-spec hash",
)
require(receipt["inputs"]["anchor_audit_sha256"] == sha256("anchor-audit.json"), "stale anchor hash")
require(
    receipt["inputs"]["statement_expression_sha256"]
    == load("statement.json")["canonical_formal_target"]["elaborated_expression_sha256"],
    "wrong target expression hash",
)
require(
    receipt["inputs"]["registry_denominator_sha256"] == registry["denominator_sha256"],
    "wrong registry denominator hash",
)
require(receipt["result"]["root_kernel_closed"] is True, "kernel root closure not recorded")
require(receipt["result"]["accepted_root_closed"] is False, "worker claimed accepted root closure")
require(receipt["result"]["theorem_complete"] is False, "worker claimed theorem completion")
require(receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"], "wrong axiom set")

require(status["state"] == "provisional_worker_selftest", "wrong proof status")
require(status["root_closed"] is True, "status omits local root closure")
require(status["root_kernel_closed"] is True, "status omits kernel closure")
require(status["root_accepted"] is False, "status claims accepted root")
require(status["theorem_complete"] is False, "status claims theorem completion")

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
require(
    subprocess.check_output(["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True).strip()
    == "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "wrong pinned mathlib revision",
)
require(
    subprocess.check_output(["git", "-C", str(mathlib), "status", "--short"], text=True) == "",
    "pinned mathlib dependency is dirty",
)

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = json.loads(selftest_path.read_text(encoding="utf-8"))
    require(
        set(selftest)
        == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"},
        "wrong self-test schema",
    )
    require(selftest["item_id"] == "S56-M-1009-PROOF", "wrong self-test item")
    require(selftest["state"] == "[_]", "wrong self-test state")
    require(selftest["base_revision"] == receipt["base_revision"], "wrong self-test base")
    require(selftest["changed_paths"] == receipt["changed_paths"], "self-test paths differ from receipt")
    require(selftest["known_failures"] == receipt["known_failures"], "self-test failures differ from receipt")
    status_output = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:]
        for line in status_output.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    require(actual_changes == set(selftest["changed_paths"]), "self-test changed-path inventory is stale")

print("PASS THM-M-1009 proof phase: exact frozen root is provisionally kernel-closed")
