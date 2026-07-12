#!/usr/bin/env python3
"""Fail-closed validation verifier for S56-M-0644-VALIDATION."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0644"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

if proof_receipt["theorem_id"] != "THM-M-0644":
    fail("proof receipt theorem identity mismatch")
if proof_receipt["proof_body"]["source_sha256"] != sha256(HERE / "Proof.lean"):
    fail("proof receipt source hash is stale")
if proof_receipt["inputs"] != {
    "statement_sha256": sha256(HERE / "Statement.lean"),
    "obligation_registry_sha256": sha256(HERE / "obligation-registry.json"),
}:
    fail("proof receipt input hashes are stale")

mathlib_entry = next((p for p in manifest["packages"] if p["name"] == "mathlib"), None)
if mathlib_entry is None:
    fail("mathlib is absent from the pinned manifest")
if mathlib_entry["rev"] != proof_receipt["proof_body"]["terminal_revision"]:
    fail("proof receipt terminal revision differs from the pinned manifest")

head = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=MATHLIB, check=True, capture_output=True, text=True
).stdout.strip()
dirty = subprocess.run(
    ["git", "status", "--short"], cwd=MATHLIB, check=True, capture_output=True, text=True
).stdout
if head != mathlib_entry["rev"]:
    fail("installed mathlib revision differs from the pinned manifest")
if dirty:
    fail("installed mathlib source checkout is dirty")

ids = [item["obligation_id"] for item in registry["obligations"]]
graph_ids = [item["obligation_id"] for item in graphs["nodes"]]
if len(ids) != len(set(ids)) or set(ids) != set(graph_ids):
    fail("registry and typed-graph node identities disagree")
if graphs["registry_denominator_sha256"] != registry["denominator_sha256"]:
    fail("registry denominator and typed graph disagree")

local_text = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(r"\b(?:sorry|admit)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
if prohibited.search(local_text):
    fail("local kernel surface contains a prohibited construct")
terminal = "FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable"
if terminal not in (HERE / "Proof.lean").read_text() or terminal not in (HERE / "Validation.lean").read_text():
    fail("proof and validation probe do not share the attested terminal declaration")

source = MATHLIB / "Mathlib" / "ModelTheory" / "Satisfiability.lean"
olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / "Mathlib" / "ModelTheory" / "Satisfiability.olean"
if not source.is_file() or not olean.is_file():
    fail("pinned terminal source or compiled artifact is missing")

print("validation: ok (fresh proof inputs, canonical graph identity, clean pinned dependency, and placeholder policy)")
print(f"terminal source sha256: {sha256(source)}")
print(f"terminal olean sha256: {sha256(olean)}")
