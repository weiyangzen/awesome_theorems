#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-1272-PROOF."""

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

required = (
    "import ObligationTree",
    "theorem bounded_values_of_level_tendsto",
    "theorem palaisSmale_subsequence",
    "theorem critical_point_at_level_of_subsequence",
    "theorem fountainLimitPackage_proof : FountainLimitPackage.{u}",
    "theorem fountainTheoremTarget_of_minimax",
    "root_of_minimax_and_limit_packages minimax fountainLimitPackage_proof",
    "#print axioms fountainLimitPackage_proof",
    "#print axioms fountainTheoremTarget_of_minimax",
)
for fragment in required:
    assert fragment in proof, f"missing proof fragment: {fragment}"

assert not re.search(r"\b(sorry|admit|sorryAx)\b", proof), "forbidden placeholder"
assert not re.search(
    r"^\s*(axiom|unsafe|opaque)\b", proof, re.MULTILINE
), "added axiom, unsafe, or opaque declaration"

receipt = json.loads((HERE / "proof-receipt.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
assert receipt["item_id"] == "S56-M-1272-PROOF"
assert receipt["theorem_id"] == "THM-M-1272"
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["accepted"] is False
assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_tree_sha256"] == sha256(
    HERE / "ObligationTree.lean"
)
assert receipt["inputs"]["obligation_registry_sha256"] == sha256(
    HERE / "obligation-registry.json"
)
assert receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
assert receipt["inputs"]["validation_specs_sha256"] == sha256(
    HERE / "validation-specs.json"
)
assert receipt["inputs"]["anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
assert receipt["inputs"]["check_proof_py_sha256"] == sha256(HERE / "check_proof.py")
assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")
assert receipt["inputs"]["lean_toolchain_sha256"] == sha256(
    ROOT / "Formalizations/Lean/lean-toolchain"
)
assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
    ROOT / "Formalizations/Lean/lake-manifest.json"
)
assert receipt["provisionally_closed_obligation_ids"] == [
    "M1272-L-LEVEL-BOUNDED",
    "M1272-L-PS-SUBSEQUENCE",
    "M1272-L-LIMIT-PASSAGE",
    "M1272-T-CRITICAL-LEVELS",
]
registry_fingerprints = {
    entry["obligation_id"]: entry["statement_fingerprint"]
    for entry in registry["obligations"]
}
for obligation_id in receipt["provisionally_closed_obligation_ids"]:
    assert (
        receipt["obligation_statement_fingerprints"][obligation_id]
        == registry_fingerprints[obligation_id]
    ), f"fingerprint mismatch for {obligation_id}"
assert [entry["declaration"] for entry in receipt["obligation_declaration_map"]] == [
    "Stage1Instances.THM_M_1272.bounded_values_of_level_tendsto",
    "Stage1Instances.THM_M_1272.palaisSmale_subsequence",
    "Stage1Instances.THM_M_1272.critical_point_at_level_of_subsequence",
    "Stage1Instances.THM_M_1272.fountainLimitPackage_proof",
]
assert receipt["result"]["axioms"] == [
    "propext",
    "Classical.choice",
    "Quot.sound",
]
assert receipt["result"]["root_kernel_closed"] is False
assert receipt["result"]["theorem_complete"] is False

print(
    "PASS THM-M-1272 proof phase: compactness package closed; "
    "symmetric minimax package remains explicit and open"
)
