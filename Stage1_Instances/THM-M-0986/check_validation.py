#!/usr/bin/env python3
"""Fail-closed freshness, scope, provenance, and trust checks for THM-M-0986."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances/THM-M-0986"
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
DENOMINATOR = "7051508e4dd19f51c8eba3519376d3f60514dbec784f028a50b748d7ec8d6dec"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


proof_receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text(encoding="utf-8"))

if proof_receipt.get("item_id") != "S56-M-0986-PROOF":
    fail("proof prerequisite receipt has the wrong identity")
if proof_receipt.get("proof_body", {}).get("source_sha256") != digest(HERE / "Proof.lean"):
    fail("proof receipt is stale against Proof.lean")
expected_inputs = {
    "statement_sha256": digest(HERE / "Statement.lean"),
    "obligation_tree_sha256": digest(HERE / "ObligationTree.lean"),
    "obligation_registry_sha256": digest(HERE / "obligation-registry.json"),
}
if proof_receipt.get("inputs") != expected_inputs:
    fail("proof receipt input hashes are stale")

ids = [entry["obligation_id"] for entry in registry["obligations"]]
graph_ids = [entry["obligation_id"] for entry in graphs["nodes"]]
if len(ids) != 11 or len(ids) != len(set(ids)) or set(ids) != set(graph_ids):
    fail("frozen registry and typed-graph identities disagree")
if registry.get("root_obligation_id") != "M0986-ROOT":
    fail("canonical root identity changed")
if registry.get("denominator_sha256") != DENOMINATOR:
    fail("frozen denominator changed")
if not set(proof_receipt.get("closed_obligation_ids", [])).issubset(set(ids)):
    fail("proof receipt names an obligation outside the frozen registry")
result = proof_receipt.get("result", {})
if result.get("root_proof_body_present") is not True or result.get("theorem_complete") is not False:
    fail("proof receipt root/completion boundary changed")

mathlib = next((p for p in manifest["packages"] if p["name"] == "mathlib"), None)
if mathlib is None or mathlib.get("rev") != MATHLIB_REVISION:
    fail("lake manifest does not attest the expected mathlib revision")
mathlib_dir = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_dir), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
if head != MATHLIB_REVISION:
    fail("checked-out mathlib revision disagrees with the manifest")
dirty = subprocess.run(
    ["git", "-C", str(mathlib_dir), "status", "--porcelain"],
    check=True, capture_output=True, text=True,
).stdout
if dirty:
    fail("checked-out mathlib dependency is dirty")

prohibited = re.compile(r"\b(sorry|admit|sorryAx)\b|^\s*(axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    if prohibited.search((HERE / name).read_text(encoding="utf-8")):
        fail(f"{name} contains a prohibited construct")
probe = (HERE / "Validation.lean").read_text(encoding="utf-8")
if re.search(r"^\s*import\s+.*Proof", probe, re.MULTILINE):
    fail("independent validation probe imports the primary proof")
if "theorem independentKhinchinWeakLaw" not in probe:
    fail("independent exact-root declaration is absent")
if "KhinchinWeakLawTarget" not in probe or "ProbabilityTheory.strong_law_ae" not in probe:
    fail("independent probe no longer targets the frozen root through the pinned terminal")

print(
    "validation: ok (11-node identity, proof freshness, pinned clean mathlib, "
    "independent exact-root reconstruction, trust boundary, and hygiene verified)"
)
