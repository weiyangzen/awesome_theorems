#!/usr/bin/env python3
"""Fail-closed validator for THM-M-0401's single partial proof leaf."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0401"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


expected_hashes = {
    "Statement.lean": "cbd4391c84fe8368b9dcbdab0e0543dc0f91c9f27d92c163905796f0dcf735e1",
    "Proof.lean": "0578abd25edcd2864e3a2976771506bc914ecddef3c13c045b4232adeac6c2dd",
    "Validation.lean": "5c9673c739caa3040df2855e98bdc330b10f44dbbebefa0c9c5d60c3741fca45",
    "instance.json": "81ed6496dc7b95fe13114c0a67ad6a875884c8e921e7e55743e9977a53400d62",
    "obligation-registry.json": "6338a9ba59aa622ff3172c1cc91e4e277a37867eaf9db9a6c046fd0982ea2eed",
    "obligation-graphs.json": "ddb1b5509fdada08f0129692ab91219cdd2dcbefc13f5a7bae0cc8683f513015",
    "validate_obligation_tree.py": "c495cb39ca4bd9338b92f267001e90ea6c3a57d5fbffc33d7a4f12ce8638d0dd",
}
for name, expected in expected_hashes.items():
    actual = digest(OWNED / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")

pins = {
    LEAN_ROOT / "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    LEAN_ROOT / "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
for path, expected in pins.items():
    if digest(path) != expected:
        fail(f"dependency pin changed: {path.name}")

instance = json.loads((OWNED / "instance.json").read_text(encoding="utf-8"))
registry = json.loads((OWNED / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((OWNED / "obligation-graphs.json").read_text(encoding="utf-8"))
if instance.get("theorem_id") != "THM-M-0401":
    fail("instance theorem identity mismatch")
if instance.get("canonical_formal_target", {}).get("declaration") != \
        "Stage1Instances.THMM0401.SchmidtSimultaneousApproximationTarget":
    fail("canonical target mismatch")
if instance.get("theorem_complete") is not False:
    fail("open theorem is falsely marked complete")

ids = [row["obligation_id"] for row in registry["obligations"]]
node_ids = [row["obligation_id"] for row in graphs["nodes"]]
if len(ids) != 14 or len(ids) != len(set(ids)) or set(ids) != set(node_ids):
    fail("frozen obligation/node identities differ")
closure = graphs.get("closure_boundary", {})
if closure.get("root_machine_debt") != "M4" or closure.get("closed_obligations") != []:
    fail("structured authority makes an unsupported closure claim")
if closure.get("theorem_complete") is not False:
    fail("graph bundle falsely closes the theorem")

tree = subprocess.run(
    ["python3", str(OWNED / "validate_obligation_tree.py")],
    cwd=ROOT, capture_output=True, text=True, timeout=30,
)
if tree.returncode != 0 or "root closure: open (M4)" not in tree.stdout:
    fail(f"obligation-tree validation failed\n{tree.stdout}{tree.stderr}")

# Remove comments before applying the defense-in-depth token scan. Lean's
# elaborator remains the authority for the actual checked declarations.
block_comment = re.compile(r"/-.*?-/", re.DOTALL)
prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    source = block_comment.sub("", (OWNED / name).read_text(encoding="utf-8"))
    source = "\n".join(line.split("--", 1)[0] for line in source.splitlines())
    if prohibited.search(source):
        fail(f"prohibited local token in {name}")

outputs: dict[str, str] = {}
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    command = ["lake", "env", "lean", f"../../Stage1_Instances/THM-M-0401/{name}"]
    result = subprocess.run(
        command, cwd=LEAN_ROOT, capture_output=True, text=True, timeout=30,
    )
    output = result.stdout + result.stderr
    if result.returncode != 0:
        fail(f"Lean recipe failed for {name}\n{output}")
    if "sorryAx" in output:
        fail(f"Lean reported sorryAx for {name}")
    outputs[name] = output

proof_axioms = " ".join(outputs["Proof.lean"].split())
validation_axioms = " ".join(outputs["Validation.lean"].split())
allowed = ("propext", "Classical.choice", "Quot.sound")
if not all(item in proof_axioms for item in allowed):
    fail("proof leaf axiom report is incomplete or unexpected")
if not all(item in validation_axioms for item in allowed):
    fail("independent leaf axiom report is incomplete or unexpected")

print("validation ok: statement and partial leaf re-elaborated; independent leaf probe passed; root remains open M4")
