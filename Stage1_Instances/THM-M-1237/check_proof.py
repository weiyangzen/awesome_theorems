#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1237 partial proof phase."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text(encoding="utf-8")
phase = json.loads((HERE / "proof-phase.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))

assert phase["item_id"] == "S56-M-1237-PROOF"
assert phase["theorem_id"] == "THM-M-1237"
assert phase["inputs"]["proof_source_sha256"] == hashlib.sha256(
    proof_path.read_bytes()
).hexdigest()
assert phase["inputs"]["statement_source_sha256"] == hashlib.sha256(
    (HERE / "Statement.lean").read_bytes()
).hexdigest()
assert phase["inputs"]["obligation_tree_source_sha256"] == hashlib.sha256(
    (HERE / "ObligationTree.lean").read_bytes()
).hexdigest()
assert phase["inputs"]["obligation_registry_sha256"] == hashlib.sha256(
    (HERE / "obligation-registry.json").read_bytes()
).hexdigest()
assert phase["inputs"]["typed_graphs_sha256"] == hashlib.sha256(
    (HERE / "typed-graphs.json").read_bytes()
).hexdigest()
assert phase["inputs"]["registry_denominator_sha256"] == registry["denominator_sha256"]
assert phase["inputs"]["registry_denominator_sha256"] == graphs["registry_denominator_sha256"]
assert phase["closed_obligation_ids"] == ["M1237-C"]
assert phase["disproved_interface_obligation_ids"] == ["M1237-L-VALUE"]
fingerprints = {
    row["obligation_id"]: row["statement_fingerprint"]
    for row in registry["obligations"]
}
implemented = {
    row["obligation_id"]: row["obligation_statement_fingerprint"]
    for row in phase["implemented_declarations"]
}
assert implemented == {
    "M1237-C": fingerprints["M1237-C"],
    "M1237-L-VALUE": fingerprints["M1237-L-VALUE"],
}
assert phase["first_failed_gate"] == "M1237-L-VALUE"
assert phase["remaining_root_cut_set"] == ["M1237-L-HOLDER", "M1237-L-VALUE"]
assert phase["phase_self_tested"] is True
assert phase["root_closed"] is False
assert phase["theorem_complete"] is False

required = (
    "theorem representativeFamily : RepresentativeFamily",
    "theorem not_valueEstimateFamily : ¬ ValueEstimateFamily",
    "#print axioms representativeFamily",
    "#print axioms not_valueEstimateFamily",
)
for needle in required:
    assert needle in proof, f"missing proof surface: {needle}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)
assert prohibited.search(proof) is None, "prohibited proof device found"

print("PASS THM-M-1237 proof phase: M1237-C local body and M1237-L-VALUE counterexample checked")
print("root closure: open (M3); frozen value-estimate interface is false")
