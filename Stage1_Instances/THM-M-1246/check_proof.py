#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-1246-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1246-PROOF"
THEOREM = "THM-M-1246"
BASE = "92246ea92c0c44282c05728798bc7c7e4a5a1464"
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


lean_files = [
    HERE / name
    for name in ("RegularizedIBP.lean", "SharpEstimate.lean", "HardyLimit.lean", "Proof.lean")
]
for path in lean_files:
    source = path.read_text(encoding="utf-8")
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b"
    )
    assert forbidden.search(source) is None, path

proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
for marker in (
    "theorem hardyTerminal : HardyTerminal",
    "regularized_summed_ibp u hu huc eps heps",
    "regularized_sharp_from_ibp_lower u hu huc",
    "regularized_integral_tendsto n hn u hu.continuous huc",
    "theorem hardyInequality : HardyInequalityTarget",
    "root_of_hardyTerminal hardyTerminal",
    "#print axioms hardyTerminal",
    "#print axioms hardyInequality",
):
    assert marker in proof, marker

registry = load(HERE / "obligation-registry.json")
receipt = load(HERE / "proof-receipt.json")
assert registry["root_obligation_id"] == "M1246-ROOT"
assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["base_revision"] == BASE
assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
assert receipt["proof_body"]["source_sha256"] == sha(HERE / "Proof.lean")
assert receipt["inputs"]["statement_sha256"] == sha(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_tree_sha256"] == sha(HERE / "ObligationTree.lean")
assert receipt["inputs"]["obligation_registry_sha256"] == sha(
    HERE / "obligation-registry.json"
)
for name, digest in receipt["proof_body"]["supporting_sources_sha256"].items():
    assert digest == sha(HERE / name), name
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["theorem_complete"] is False

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True
).strip() == MATHLIB_REV

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
    if line[3:] != "Formalizations/Lean/.lake" and not line[3:].startswith(".m1246-proof.")
}
assert actual_changes == set(selftest["changed_paths"]), (
    actual_changes,
    set(selftest["changed_paths"]),
)

print("PASS THM-M-1246 proof phase: exact Hardy root has a local proof body")
print(f"proof source sha256: {sha(HERE / 'Proof.lean')}")
print("accepted state unchanged; proof proposal is provisional pending master acceptance")
