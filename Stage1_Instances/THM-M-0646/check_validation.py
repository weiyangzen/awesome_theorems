#!/usr/bin/env python3
"""Fail-closed narrow verifier for S56-M-0646-VALIDATION."""

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0646"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"validation: FAIL: {message}")


proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

if proof_receipt["item_id"] != "S56-M-0646-PROOF":
    fail("proof receipt identity mismatch")
if proof_receipt["proof_body"]["source_sha256"] != sha256(HERE / "Proof.lean"):
    fail("proof receipt source hash is stale")
expected_inputs = {
    "statement_sha256": sha256(HERE / "Statement.lean"),
    # The proof-phase receipt uses this field for the checked Lean composition module.
    "obligation_tree_sha256": sha256(HERE / "ObligationTree.lean"),
    "obligation_registry_sha256": sha256(HERE / "obligation-registry.json"),
}
if proof_receipt["inputs"] != expected_inputs:
    fail("proof receipt input hashes are stale")

mathlib_entry = next((p for p in manifest["packages"] if p["name"] == "mathlib"), None)
if mathlib_entry is None:
    fail("mathlib is absent from the pinned manifest")
if mathlib_entry["rev"] != proof_receipt["proof_body"]["dependency_revision"]:
    fail("proof receipt revision differs from the manifest")
head = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=MATHLIB, check=True, capture_output=True, text=True
).stdout.strip()
dirty = subprocess.run(
    ["git", "status", "--short"], cwd=MATHLIB, check=True, capture_output=True, text=True
).stdout
if head != mathlib_entry["rev"] or dirty:
    fail("installed mathlib source is not the clean pinned revision")

ids = [node["obligation_id"] for node in registry["obligations"]]
graph_ids = [node["obligation_id"] for node in graphs["nodes"]]
if len(ids) != len(set(ids)) or set(ids) != set(graph_ids):
    fail("registry and typed graph identities disagree")
if graphs["registry_denominator_sha256"] != registry["denominator_sha256"]:
    fail("registry denominator and typed graph disagree")

local_text = "\n".join(
    (HERE / name).read_text() for name in ("Statement.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(
    r"\b(?:sorry|admit)\b|^[ \t]*(?:axiom|unsafe)\b|sorryAx|implemented_by",
    re.MULTILINE,
)
if prohibited.search(local_text):
    fail("local checked surface contains a prohibited construct")

terminal = "FirstOrder.Language.exists_elementarilyEquivalent_card_eq"
if terminal not in (HERE / "Proof.lean").read_text():
    fail("proof does not use the attested terminal declaration")
if terminal not in (HERE / "Validation.lean").read_text():
    fail("independent probe does not use the attested terminal declaration")

artifacts = {
    "satisfiability source": MATHLIB / "Mathlib/ModelTheory/Satisfiability.lean",
    "skolem source": MATHLIB / "Mathlib/ModelTheory/Skolem.lean",
    "satisfiability olean": MATHLIB / ".lake/build/lib/lean/Mathlib/ModelTheory/Satisfiability.olean",
    "skolem olean": MATHLIB / ".lake/build/lib/lean/Mathlib/ModelTheory/Skolem.olean",
}
for label, path in artifacts.items():
    if not path.is_file():
        fail(f"missing pinned {label}")
    expected = proof_receipt["proof_body"].get(label.replace(" ", "_") + "_sha256")
    if expected is not None and expected != sha256(path):
        fail(f"stale proof receipt hash for {label}")

print("validation: ok (fresh proof receipt, graph identity, clean pin, provenance, and hygiene)")
for label, path in artifacts.items():
    print(f"{label} sha256: {sha256(path)}")
