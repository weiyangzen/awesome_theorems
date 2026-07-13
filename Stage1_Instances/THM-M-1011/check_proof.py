#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-1011-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text(encoding="utf-8")
registry_path = HERE / "obligation-registry.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))

if not __debug__:
    raise SystemExit("proof check failed: Python assertions are disabled")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert registry["theorem_id"] == "THM-M-1011"
assert registry["item_id"] == "S56-M-1011-OBLIGATION_TREE"
assert registry["denominator_sha256"] == (
    "3dd41addcf34fd9ca7d89e9d2231337be0e01df77f497acdcefff743020bdd90"
)
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")

for required in (
    "import Statement",
    "import Mathlib.MeasureTheory.Measure.Prokhorov",
    "noncomputable def representative",
    "theorem continuous_representative",
    "theorem sectionMap_quotientMap",
    "theorem quotientMap_sectionMap",
    "noncomputable def probabilityMeasureHomeomorph",
    "theorem quotientMap_isUniformlyTight",
    "theorem isCompact_closure_iff_quotientMap",
    "theorem tight_to_compact",
    "theorem canonical : THM_M_1011.CanonicalStatement X",
    "#print axioms canonical",
):
    assert required in proof, f"missing proof component: {required}"

for pattern in (
    r"\bsorry\b",
    r"\badmit\b",
    r"\bsorryAx\b",
    r"^[ \t]*axiom\b",
    r"^[ \t]*unsafe\b",
    r"\bimplemented_by\b",
    r"\bnative_decide\b",
):
    assert re.search(pattern, proof, re.MULTILINE) is None, f"prohibited token: {pattern}"

assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["item_id"] == "S56-M-1011-PROOF"
assert receipt["theorem_id"] == "THM-M-1011"
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]"
assert receipt["accepted"] is False
assert receipt["exact_declaration"] == (
    "Stage1Instances.THM_M_1011.Proof.canonical"
)
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["frozen_graph_closed"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["provisionally_closed_obligation_ids"] == []
assert receipt["accepted_closed_obligation_ids"] == []
assert receipt["kernel_evidenced_obligation_ids"] == [
    "M1011-ROOT",
    "M1011-S-DEFINITIONS",
    "M1011-S-DOMAIN",
    "M1011-S-BOUNDARY",
    "M1011-S-TRANSPORT",
    "M1011-N-SEPARATION",
    "M1011-B-TIGHT-COMPACT",
    "M1011-B-COMPACT-TIGHT",
    "M1011-L-PROKHOROV",
    "M1011-L-COMPACT-TIGHT",
    "M1011-T-ASSEMBLE",
]
assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
for key, filename in (
    ("statement_sha256", "Statement.lean"),
    ("obligation_tree_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
    ("anchor_audit_sha256", "anchor-audit.json"),
):
    assert receipt["inputs"][key] == sha256(HERE / filename)

worker_packet = ROOT / ".stage1-worker-selftest.json"
if worker_packet.exists():
    packet = json.loads(worker_packet.read_text(encoding="utf-8"))
    assert packet["item_id"] == "S56-M-1011-PROOF"
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"]

print("PASS THM-M-1011 proof: exact root kernel-closed via separation quotient")
print("frozen graph: open pending a versioned quotient-route architecture delta")
