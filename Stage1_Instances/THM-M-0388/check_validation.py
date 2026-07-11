#!/usr/bin/env python3
"""Minimal validation-phase verifier, independent of the proof-phase scripts."""

import hashlib
import json
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0388"
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB = LEAN_ROOT / ".lake/packages/mathlib"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


receipt = json.loads((DOSSIER / "proof-receipt.json").read_text())
registry = json.loads((DOSSIER / "obligation-registry.json").read_text())
graphs = json.loads((DOSSIER / "typed-graphs.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

expected_inputs = {
    "proof_sha256": sha256(DOSSIER / "Proof.lean"),
    "statement_sha256": sha256(DOSSIER / "Statement.lean"),
    "obligation_registry_sha256": sha256(DOSSIER / "obligation-registry.json"),
}
if receipt.get("inputs") != expected_inputs:
    fail("proof receipt input hashes are stale")

mathlib_entry = next((p for p in manifest["packages"] if p["name"] == "mathlib"), None)
if mathlib_entry is None or mathlib_entry["rev"] != receipt["proof_body"]["dependency_revision"]:
    fail("proof receipt mathlib revision does not match the pinned manifest")

source = MATHLIB / "Mathlib/NumberTheory/Pell.lean"
olean = MATHLIB / ".lake/build/lib/lean/Mathlib/NumberTheory/Pell.olean"
if sha256(source) != receipt["proof_body"]["dependency_source_sha256"]:
    fail("pinned Pell source digest mismatch")
if sha256(olean) != receipt["proof_body"]["dependency_olean_sha256"]:
    fail("pinned Pell olean digest mismatch")

git_head = subprocess.run(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
if git_head != mathlib_entry["rev"]:
    fail("checked-out mathlib revision does not match lake-manifest.json")

ids = [node["obligation_id"] for node in registry["obligations"]]
if len(ids) != len(set(ids)) or set(ids) != set(graphs["nodes"]):
    fail("registry and typed-graph node sets disagree or contain duplicates")
if set(receipt["canonical_obligation_ids"]) != set(ids):
    fail("proof receipt does not cover the frozen canonical ID set")

proof_text = (DOSSIER / "Proof.lean").read_text()
validation_text = (DOSSIER / "Validation.lean").read_text()
prohibited = re.compile(r"\b(sorry|admit)\b|^\s*(axiom|unsafe)\b", re.MULTILINE)
if prohibited.search(proof_text) or prohibited.search(validation_text):
    fail("local proof or validation probe contains a prohibited construct")
if "Pell.exists_of_not_isSquare" not in proof_text or "Pell.exists_of_not_isSquare" not in validation_text:
    fail("proof and independent probe do not name the attested terminal declaration")

print(
    "validation: ok (proof receipt freshness, pinned source/olean provenance, "
    "canonical node identity, and local placeholder policy verified)"
)
