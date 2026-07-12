#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-1054 validation handoff."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


spec = json.loads((HERE / "validation-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == receipt["item_id"] == "S56-M-1054-VALIDATION"
assert receipt["depends_on"] == ["S56-M-1054-PROOF"]
assert len({recipe["recipe_id"] for recipe in spec["recipes"]}) == 3
assert all(isinstance(recipe["argv"], list) for recipe in spec["recipes"])
for name, expected in receipt["inputs"].items():
    assert digest(name) == expected, f"stale validation input: {name}"
assert proof_receipt["root_declaration"] == \
    "Stage1Instances.THM_M_1054.vonNeumannL2MeanErgodic"
assert proof_receipt["machine_root_cut_set"] == []
assert receipt["root_decision"] == {
    "machine_debt": "M1",
    "kernel_closed": True,
    "audit_complete": False,
    "theorem_complete": False,
}
assert set(receipt["first_failed_gates"]) == {
    "trust.accepted_foundation_profile",
    "trust.complete_tcb_inventory",
    "hermetic.cold_empty_cache_offline_replay",
    "independent.distinct_runner",
}
assert receipt["environment"]["cache_mode"].startswith("warm shared")
assert receipt["environment"]["network_isolation"].startswith("not established")
source = (HERE / "Proof.lean").read_text()
for forbidden in (r"\bsorry\b", r"\badmit\b", r"\bsorryAx\b", r"^\s*axiom\s", r"^\s*unsafe\s"):
    assert re.search(forbidden, source, re.MULTILINE) is None

print("PASS THM-M-1054 validation: kernel closure evidenced; release gates fail closed")
