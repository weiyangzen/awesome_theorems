#!/usr/bin/env python3
"""Independently check the fail-closed M0387 validation handoff."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


spec = json.loads((HERE / "validation-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == receipt["item_id"] == "S56-M-0387-VALIDATION"
assert len({recipe["recipe_id"] for recipe in spec["recipes"]}) == 3
assert all(recipe["network_policy"] == "denied" for recipe in spec["recipes"])
assert all(isinstance(recipe["argv"], list) for recipe in spec["recipes"])
assert receipt["inputs"]["Proof.lean"] == digest(HERE / "Proof.lean")
assert receipt["inputs"]["Statement.lean"] == digest(HERE / "Statement.lean")
assert receipt["inputs"]["obligation-registry.json"] == digest(HERE / "obligation-registry.json")
assert receipt["inputs"]["typed-graphs.json"] == digest(HERE / "typed-graphs.json")
assert registry["root_obligation_id"] == "M0387-ROOT"
root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0387-ROOT")
assert root["machine_debt"] == "M2"
assert receipt["root_decision"]["machine_debt"] == "M2"
assert receipt["root_decision"]["kernel_closed"] is False
assert receipt["root_decision"]["theorem_complete"] is False
assert set(receipt["first_failed_gates"]) == {
    "proof.root_kernel_closure",
    "hermetic.cold_empty_cache",
    "independent.distinct_runner",
}
source = (HERE / "Proof.lean").read_text()
for forbidden in (r"\bsorry\b", r"\badmit\b", r"\bsorryAx\b", r"^\s*axiom\s", r"^\s*unsafe\s"):
    assert re.search(forbidden, source, re.MULTILINE) is None

print("PASS validation handoff: admitted bodies checked; root M2; release gates fail closed")
