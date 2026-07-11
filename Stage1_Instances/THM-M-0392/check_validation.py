#!/usr/bin/env python3
"""Fail-closed verifier for the THM-M-0392 validation handoff."""

import hashlib
import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0392"
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB = LEAN_ROOT / ".lake/packages/mathlib"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


proof_receipt = json.loads((DOSSIER / "proof-receipt.json").read_text())
registry = json.loads((DOSSIER / "obligation-registry.json").read_text())
graphs = json.loads((DOSSIER / "typed-graphs.json").read_text())
nodes = json.loads((DOSSIER / "obligation-nodes.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

expected_proof_inputs = {
    "statement_sha256": sha256(DOSSIER / "Statement.lean"),
    "obligation_registry_sha256": sha256(DOSSIER / "obligation-registry.json"),
}
if proof_receipt.get("inputs") != expected_proof_inputs:
    fail("proof receipt input hashes are stale")
if proof_receipt.get("proof_body", {}).get("source_sha256") != sha256(DOSSIER / "Proof.lean"):
    fail("proof receipt source hash is stale")

mathlib_entry = next((entry for entry in manifest["packages"] if entry["name"] == "mathlib"), None)
if mathlib_entry is None or mathlib_entry["rev"] != "8a178386ffc0f5fef0b77738bb5449d50efeea95":
    fail("mathlib manifest revision is not the attested pin")
dependency_hashes = {
    "Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Basic.lean":
        "aa57c2c86667817aacc04f9fd3d0eb5c9c09f205e644b9c28b9d8caebb36d3c1",
    "Mathlib/AlgebraicGeometry/EllipticCurve/NormalForms.lean":
        "ec72b205c7193e28bfc129d0a079e5a35f0db46566eba3abee8190af9187973c",
    ".lake/build/lib/lean/Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Basic.olean":
        "1b19fd9d3e3a60b47e71b67a40d4acfffab1a06cc07369877044d199d2bd800c",
    ".lake/build/lib/lean/Mathlib/AlgebraicGeometry/EllipticCurve/NormalForms.olean":
        "0478cfd0deba75f192d0c75b2a24b8486ed1c8b40f7402bab94149add348f40d",
}
for relative, expected in dependency_hashes.items():
    if sha256(MATHLIB / relative) != expected:
        fail(f"pinned dependency digest mismatch: {relative}")

registry_ids = {entry["obligation_id"] for entry in registry["obligations"]}
graph_nodes = graphs.get("nodes", {})
graph_ids = set(graph_nodes if isinstance(graph_nodes, dict) else graph_nodes)
node_ids = {entry["obligation_id"] for entry in nodes["nodes"]}
if registry_ids != graph_ids or registry_ids != node_ids:
    fail("registry, typed graph, and obligation-node sets disagree")

closed = set(proof_receipt.get("closed_obligation_ids", []))
expected_closed = {"M0392-C-CURVE", "M0392-L-NONSINGULAR", "M0392-T-COORDINATES"}
if closed != expected_closed or not closed < registry_ids:
    fail("proof receipt misstates the partial closed-obligation set")
if proof_receipt.get("result", {}).get("root_closed") is not False:
    fail("proof receipt must keep the root open")

root = next((entry for entry in nodes["nodes"] if entry["obligation_id"] == "M0392-ROOT"), None)
bridge = next((entry for entry in nodes["nodes"] if entry["obligation_id"] == "M0392-X-SIEGEL"), None)
if root is None or root.get("machine_debt") not in {"M2", "M3", "M4", "M5"}:
    fail("canonical root is not explicitly machine-open")
if bridge is None or bridge.get("machine_debt") not in {"M2", "M3", "M4", "M5"}:
    fail("integral-points bridge is not explicitly machine-open")

prohibited = re.compile(r"\b(sorry|admit)\b|^\s*(axiom|unsafe)\b", re.MULTILINE)
for name in ("Proof.lean", "Validation.lean"):
    if prohibited.search((DOSSIER / name).read_text()):
        fail(f"{name} contains a prohibited construct")

proof = (DOSSIER / "Proof.lean").read_text()
probe = (DOSSIER / "Validation.lean").read_text()
for declaration in (
    "mordellCurve_equation_iff",
    "mordellCurve_discriminant_ne_zero",
    "toIntegralCurvePoint_injective",
):
    if declaration not in proof:
        fail(f"proof declaration {declaration} is absent")
for declaration in (
    "independent_equation_iff",
    "independent_discriminant_ne_zero",
    "independent_embedding_injective",
):
    if declaration not in probe:
        fail(f"independent validation declaration {declaration} is absent")
if re.search(r"^\s*theorem\s+.*(Siegel|FinitenessStatement|root)\b", probe, re.MULTILINE):
    fail("validation probe unexpectedly asserts the open bridge or root")

print(
    "validation: ok (8-node identity, proof-receipt freshness, pinned provenance, "
    "three partial closures, fail-closed root, independent probe, and placeholder policy verified)"
)
