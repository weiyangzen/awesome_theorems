#!/usr/bin/env python3
"""Fail-closed freshness, provenance, trust, and scope checks for THM-M-0081."""

import hashlib
import json
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0081"
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_DENOMINATOR = "f38e8efb0c7df7d14e55dc7e7e2a39d88921b21c20eda3ecfb2d6287dbbbf69d"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


proof_receipt = json.loads((DOSSIER / "proof-receipt.json").read_text())
registry = json.loads((DOSSIER / "obligation-registry.json").read_text())
graphs = json.loads((DOSSIER / "typed-graphs.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

if proof_receipt.get("item_id") != "S56-M-0081-PROOF":
    fail("proof prerequisite receipt has the wrong item identity")
if proof_receipt.get("proof_body", {}).get("source_sha256") != sha256(DOSSIER / "Proof.lean"):
    fail("proof receipt source hash is stale")
expected_inputs = {
    "canonical_statement_sha256": sha256(DOSSIER / "CanonicalStatement.lean"),
    "obligation_tree_sha256": sha256(DOSSIER / "ObligationTree.lean"),
    "obligation_registry_sha256": sha256(DOSSIER / "obligation-registry.json"),
    "registry_denominator_sha256": registry["denominator_sha256"],
}
if proof_receipt.get("inputs") != expected_inputs:
    fail("proof receipt input hashes are stale")

mathlib = next((package for package in manifest["packages"] if package["name"] == "mathlib"), None)
if mathlib is None or mathlib.get("rev") != MATHLIB_REVISION:
    fail("lake manifest does not contain the attested mathlib revision")
mathlib_dir = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
if subprocess.run(
    ["git", "-C", str(mathlib_dir), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
).stdout.strip() != MATHLIB_REVISION:
    fail("checked-out mathlib revision disagrees with the manifest")
if subprocess.run(
    ["git", "-C", str(mathlib_dir), "status", "--porcelain"], capture_output=True, text=True, check=True
).stdout:
    fail("checked-out mathlib dependency is dirty")

ids = [entry["obligation_id"] for entry in registry["obligations"]]
graph_ids = [entry["obligation_id"] for entry in graphs["nodes"]]
if len(ids) != len(set(ids)) or set(ids) != set(graph_ids) or len(ids) != 11:
    fail("registry and typed-graph identities disagree")
if registry.get("root_obligation_id") != "M0081-ROOT":
    fail("canonical root identity changed")
if registry.get("denominator_sha256") != EXPECTED_DENOMINATOR:
    fail("frozen denominator changed")
if set(proof_receipt.get("closed_obligation_ids", [])) != set(
    registry["frozen_denominators"]["required_machine"]
):
    fail("proof receipt does not cover exactly the frozen machine denominator")
result = proof_receipt.get("result", {})
if result.get("root_closed") is not True or result.get("theorem_complete") is not False:
    fail("proof receipt root/completion boundary changed")

prohibited = re.compile(r"\b(sorry|admit|sorryAx)\b|^\s*(axiom|unsafe)\b", re.MULTILINE)
for name in ("CanonicalStatement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    if prohibited.search((DOSSIER / name).read_text()):
        fail(f"{name} contains a prohibited construct")
probe = (DOSSIER / "Validation.lean").read_text()
if "import «Stage1_Instances».«THM-M-0081».Proof" in probe or "import Stage1_Instances" in probe:
    fail("independent validation probe imports the primary proof")
if not re.search(r"\btheorem\s+independentYonedaObjectDetection\b", probe):
    fail("independent exact-root declaration is absent")
if "Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y)" not in probe:
    fail("independent probe no longer states the exact frozen expression")

closure = graphs.get("closure_boundary", {})
if closure.get("theorem_complete") is not False:
    fail("typed graph illegally claims theorem completion")

print(
    "validation: ok (11-node identity, proof-receipt freshness, pinned clean mathlib, "
    "exact-root independent reconstruction, trust boundary, and hygiene verified)"
)
