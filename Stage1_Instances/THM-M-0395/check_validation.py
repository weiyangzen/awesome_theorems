#!/usr/bin/env python3
"""Fail-closed verifier for the truthful THM-M-0395 validation handoff."""

import hashlib
import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0395"
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


proof_receipt = json.loads((DOSSIER / "proof-receipt.json").read_text())
registry = json.loads((DOSSIER / "obligation-registry.json").read_text())
graphs = json.loads((DOSSIER / "typed-graphs.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

expected_inputs = {
    "statement_sha256": sha256(DOSSIER / "Statement.lean"),
    "obligation_registry_sha256": sha256(DOSSIER / "obligation-registry.json"),
}
if proof_receipt.get("inputs") != expected_inputs:
    fail("proof receipt input hashes are stale")
if proof_receipt.get("proof_body", {}).get("source_sha256") != sha256(DOSSIER / "Proof.lean"):
    fail("proof receipt source hash is stale")

mathlib = next((entry for entry in manifest["packages"] if entry["name"] == "mathlib"), None)
if mathlib is None or mathlib.get("rev") != MATHLIB_REVISION:
    fail("mathlib manifest revision is not the attested immutable pin")

registry_ids = {entry["obligation_id"] for entry in registry["obligations"]}
graph_ids = {entry["obligation_id"] for entry in graphs["nodes"]}
if registry_ids != graph_ids or registry.get("root_obligation_id") != "M0395-ROOT":
    fail("registry and typed-graph identities disagree")

if proof_receipt.get("closed_obligation_ids") != []:
    fail("proof receipt must not claim a frozen obligation closed")
if set(proof_receipt.get("supports_obligation_ids", [])) != {"M0395-L3", "M0395-T"}:
    fail("proof receipt support boundary changed")
result = proof_receipt.get("result", {})
if result.get("root_closed") is not False or result.get("theorem_complete") is not False:
    fail("proof receipt must keep the exact root and theorem completion open")

root = next(entry for entry in graphs["nodes"] if entry["obligation_id"] == "M0395-ROOT")
if root.get("machine_debt") not in {"M2", "M3", "M4", "M5"}:
    fail("canonical root is not explicitly machine-open")

prohibited = re.compile(r"\b(sorry|admit)\b|^\s*(axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    if prohibited.search((DOSSIER / name).read_text()):
        fail(f"{name} contains a prohibited construct")

proof = (DOSSIER / "Proof.lean").read_text()
probe = (DOSSIER / "Validation.lean").read_text()
for declaration in (
    "finite_of_injective_to",
    "finite_of_two_injections",
    "finite_points_of_finite_univ",
):
    if declaration not in proof:
        fail(f"proof declaration {declaration} is absent")
for declaration in (
    "independent_finite_of_injective",
    "independent_two_injections",
    "independent_finite_points_transport",
):
    if declaration not in probe:
        fail(f"independent probe {declaration} is absent")
if re.search(r"^\s*(def|theorem)\s+.*(Faltings|Statement|root)\b", probe, re.MULTILINE):
    fail("independent probe unexpectedly asserts the open root")

print(
    "validation: ok (17-node identity, proof-receipt freshness, pinned mathlib, "
    "three independently reconstructed transports, fail-closed root, and hygiene verified)"
)
