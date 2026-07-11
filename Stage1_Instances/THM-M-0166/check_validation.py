#!/usr/bin/env python3
"""Recheck the exact, fail-closed THM-M-0166 validation handoff."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0166"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((OWNED / name).read_text(encoding="utf-8"))


receipt = load("validation-receipt.json")
spec = load("validation-spec.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof_receipt = load("proof-receipt.json")

assert receipt["item_id"] == spec["item_id"] == "S56-M-0166-VALIDATION"
assert receipt["theorem_id"] == spec["theorem_id"] == "THM-M-0166"
assert len({recipe["recipe_id"] for recipe in spec["recipes"]}) == 4
assert all(recipe["network_policy"] == "denied" for recipe in spec["recipes"])
for name, expected in receipt["inputs"].items():
    path = LEAN_ROOT / name.removeprefix("Formalizations/Lean/") if name.startswith("Formalizations/Lean/") else OWNED / name
    assert digest(path) == expected, f"stale validation input: {name}"

obligations = {node["obligation_id"]: node for node in registry["obligations"]}
assert set(obligations) == set(graphs["coverage_denominators"]["canonical_obligations"])
assert obligations["M0166-ROOT"]["machine_debt"] == "M2"
assert obligations["M0166-C-PROPER"]["machine_debt"] == "M4"
assert proof_receipt["closed_obligation_ids"] == ["M0166-L-SUBSEGMENT"]
assert proof_receipt["remaining_root_cut_set"] == ["M0166-C-PROPER", "M0166-L-EXISTENCE"]
assert receipt["root_decision"] == {
    "machine_debt": "M2",
    "kernel_closed": False,
    "theorem_complete": False,
}
assert receipt["first_failed_gate"] == "proof.root_kernel_closure"

prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
    source = (OWNED / name).read_text(encoding="utf-8")
    code = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith(("--", "/-", "*")))
    assert prohibited.search(code) is None, f"prohibited proof token in {name}"

commands = [
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0166/Statement.lean"],
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0166/ObligationTree.lean"],
    ["bash", "../../Stage1_Instances/THM-M-0166/check_proof.sh"],
]
outputs: list[str] = []
for command in commands:
    result = subprocess.run(command, cwd=LEAN_ROOT, capture_output=True, text=True, timeout=60)
    output = result.stdout + result.stderr
    assert result.returncode == 0, f"recipe failed: {' '.join(command)}\n{output}"
    assert "sorryAx" not in output
    outputs.append(output)

expected_axioms = ("propext", "Classical.choice", "Quot.sound")
assert all(name in outputs[1] for name in expected_axioms)
assert all(name in outputs[2] for name in expected_axioms)
print("validation ok: exact statement, composition, and partial proof rechecked; root remains open M2")
