#!/usr/bin/env python3
"""Independently check the fail-closed THM-M-0003 validation handoff."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1] / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


spec = json.loads((HERE / "validation-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())

assert spec["item_id"] == receipt["item_id"] == "S56-M-0003-VALIDATION"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-0003"
recipes = spec["recipes"]
assert len({recipe["recipe_id"] for recipe in recipes}) == len(recipes) == 4
assert all(isinstance(recipe["argv"], list) and recipe["argv"] for recipe in recipes)
assert all(recipe["network_policy"] == "denied_by_recipe_contract" for recipe in recipes)
assert {result["recipe_id"] for result in receipt["recipe_results"]} == {
    recipe["recipe_id"] for recipe in recipes
}
assert all(result["exit"] == 0 for result in receipt["recipe_results"])

for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean",
             "obligation-registry.json", "typed-graphs.json", "proof-receipt.json"):
    assert receipt["inputs"][name] == digest(HERE / name)
for name in ("lake-manifest.json", "lean-toolchain"):
    assert receipt["inputs"][name] == digest(LEAN / name)

proof = (HERE / "Proof.lean").read_text()
for forbidden in (r"\bsorry\b", r"\badmit\b", r"\bsorryAx\b",
                  r"^\s*axiom\s", r"^\s*unsafe\s"):
    assert re.search(forbidden, proof, re.MULTILINE) is None
assert receipt["kernel_evidence"]["exact_root_checked"] is True
assert receipt["kernel_evidence"]["composition_route_checked"] is True
assert receipt["trust_closure"]["observed_axioms"] == [
    "propext", "Classical.choice", "Quot.sound"
]
assert receipt["root_decision"]["kernel_closed"] is True
assert receipt["root_decision"]["theorem_complete"] is False
assert receipt["environment"]["cache_mode"].startswith("warm canonical")
assert {"hermetic.cold_empty_cache", "independent.distinct_runner",
        "trust.accepted_axiom_policy"} <= set(receipt["failed_gates"])

print("PASS THM-M-0003 validation handoff: kernel closes; release gates fail closed")
