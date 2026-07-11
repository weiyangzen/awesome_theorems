#!/usr/bin/env python3
"""Fail-closed verifier for the THM-M-0397 validation handoff."""

import hashlib
import json
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0397"
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
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

expected_inputs = {
    "statement_sha256": sha256(DOSSIER / "Statement.lean"),
    "obligation_tree_sha256": sha256(DOSSIER / "ObligationTree.lean"),
    "obligation_registry_sha256": sha256(DOSSIER / "obligation-registry.json"),
}
if proof_receipt.get("inputs") != expected_inputs:
    fail("proof receipt input hashes are stale")
if proof_receipt.get("proof_body", {}).get("source_sha256") != sha256(DOSSIER / "Proof.lean"):
    fail("proof receipt source hash is stale")

mathlib_entry = next((entry for entry in manifest["packages"] if entry["name"] == "mathlib"), None)
if mathlib_entry is None or mathlib_entry["rev"] != proof_receipt["environment"]["mathlib_revision"]:
    fail("proof receipt mathlib revision does not match lake-manifest.json")
git_head = subprocess.run(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], check=True,
    capture_output=True, text=True,
).stdout.strip()
if git_head != mathlib_entry["rev"]:
    fail("checked-out mathlib revision does not match lake-manifest.json")

dependency_hashes = {
    "Mathlib/Analysis/SpecialFunctions/Complex/Log.lean":
        "283a467628b30facc2abef14332507c9ec9628713f9d01dfd3cfdebc0dc9aac2",
    "Mathlib/FieldTheory/AlgebraicClosure.lean":
        "f1d648fc418040759ac66e47788e06ea795a6f2c511f108a548fbeb7c28e2708",
    ".lake/build/lib/lean/Mathlib/Analysis/SpecialFunctions/Complex/Log.olean":
        "6ddabf38d5cffd77a23b8bab972be8ca59648afb3a466e10b5aab56cee2a60e9",
    ".lake/build/lib/lean/Mathlib/FieldTheory/AlgebraicClosure.olean":
        "184c45889ebeb9efbfbc410e58d640c9fd3cb48aa1785aecfeaa8a19c2a8a6b2",
}
for relative, expected in dependency_hashes.items():
    if sha256(MATHLIB / relative) != expected:
        fail(f"pinned dependency digest mismatch: {relative}")

registry_ids = {entry["obligation_id"] for entry in registry["obligations"]}
graph_ids = {entry["obligation_id"] for entry in graphs["nodes"]}
if registry_ids != graph_ids or graphs.get("root_obligation_id") != "M0397-ROOT":
    fail("registry and typed-graph identities disagree")
closed = set(proof_receipt.get("closed_obligation_ids", []))
expected_closed = {"M0397-ROOT", "M0397-COMP", "M0397-BOUND", "M0397-REDUCE", "M0397-ENUM", "M0397-FILTER"}
if closed != expected_closed or not closed < registry_ids:
    fail("proof receipt misstates the kernel-closed and assurance-open boundary")
if proof_receipt.get("result", {}).get("root_closed") is not True:
    fail("proof receipt does not report kernel closure of the frozen root")
if proof_receipt.get("result", {}).get("theorem_complete") is not False:
    fail("proof receipt improperly reports theorem completion")

prohibited = re.compile(r"\b(sorry|admit)\b|^\s*(axiom|unsafe)\b", re.MULTILINE)
for name in ("Proof.lean", "Validation.lean"):
    if prohibited.search((DOSSIER / name).read_text()):
        fail(f"{name} contains a prohibited construct")
proof = (DOSSIER / "Proof.lean").read_text()
probe = (DOSSIER / "Validation.lean").read_text()
if "theorem baker_method : Statement" not in proof:
    fail("proof root declaration is absent")
if "theorem independent_root : Statement" not in probe:
    fail("independent root declaration is absent")
if "import Proof" in probe or "import ObligationTree" in probe:
    fail("independent probe imports a proof-phase module")
for token in ("Finset.mem_filter", "heightBall_spec", "reduce_solution"):
    if token not in proof or token not in probe:
        fail(f"proof/probe construction token absent: {token}")

print(
    "validation: ok (8-node identity, proof-receipt freshness, pinned source/olean "
    "provenance, exact-root boundary, independent reconstruction, and placeholder policy verified)"
)
