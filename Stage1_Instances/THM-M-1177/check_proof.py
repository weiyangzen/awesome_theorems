#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-1177-PROOF."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text(encoding="utf-8")
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))

for pattern in (
    r"\bsorry\b",
    r"\badmit\b",
    r"\bsorryAx\b",
    r"^[ \t]*axiom\b",
    r"^[ \t]*unsafe\b",
    r"^[ \t]*opaque\b",
    r"^[ \t]*extern\b",
    r"implemented_by",
    r"native_decide",
):
    assert re.search(pattern, proof, re.MULTILINE) is None, pattern

for declaration in (
    "theorem frozenSPD_to_posDef",
    "theorem weightedIntegrand_nonneg_on_domain",
    "theorem upperContactSet_subset_domain",
    "theorem upperContactSet_volume_ne_top",
    "theorem weightedIntegral_nonneg",
    "theorem weightedNegativeNorm_nonneg",
    "theorem degenerateMaximumPackage",
    "theorem abpTarget_of_positiveMaximumPackage",
):
    assert declaration in proof, declaration

assert "(positive : forall n : Nat" in proof
assert "root_of_architecture" in proof
assert registry["root_obligation_id"] == "M1177-ROOT"
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
assert receipt["item_id"] == "S56-M-1177-PROOF"
assert receipt["theorem_id"] == "THM-M-1177"
assert receipt["accepted"] is False
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(
    proof_path.read_bytes()
).hexdigest()
assert receipt["registry_denominator_sha256"] == registry["denominator_sha256"]
assert receipt["provisionally_closed_obligation_ids"] == [
    "M1177-B-DEGENERATE"
]
assert receipt["result"]["degenerate_package_kernel_closed"] is True
assert receipt["result"]["root_kernel_closed"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["remaining_root_cut_set"] == ["M1177-T-POSITIVE"]

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = json.loads(selftest_path.read_text(encoding="utf-8"))
    assert set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    # A later phase legitimately replaces the root handoff manifest. Validate
    # proof-specific handoff fields only while this is the active proof packet.
    if selftest["item_id"] == receipt["item_id"]:
        assert selftest["state"] == "[_]"
        assert selftest["base_revision"] == receipt["base_revision"]
        assert selftest["changed_paths"] == receipt["changed_paths"]
        assert selftest["known_failures"] == receipt["known_failures"]
        status = subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
        )
        actual_changes = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == set(selftest["changed_paths"]), (
            actual_changes, set(selftest["changed_paths"])
        )

print(
    "PASS THM-M-1177 proof phase: degenerate package closed; "
    "positive-maximum package and root remain open"
)
