#!/usr/bin/env python3
"""Fail-closed validation for THM-M-0402's partial proof-phase results."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0402"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


expected_hashes = {
    "Statement.lean": "d9213f673e100c85d2330219b6dbcbaf3e7542c9ea01df0bd7b31f2f3faf518d",
    "Proof.lean": "8b843b5642858be5f4459a06677766008f8ca00a3e1bacf3fd3465d93e1a7ab7",
    "Validation.lean": "d4f1e34d15ce4d6d701c2dc973b1285f05b55343f323e1e5b450049469265db7",
    "instance.json": "ed2cbc3e30840b54083bd10b68fcf8182255b4ccaac88503c577f28f91efc954",
    "obligation-registry.json": "747078c8e1ec2a9daafede3c56eb7a1606fb1b44de1c1d09605b333960ee7912",
    "obligation-graphs.json": "ff83df80cd43b68d6a23fbed1b6cdbb7b926364541ff55877f7078292b759a69",
    "validate_obligation_tree.py": "8eb6c8f0581cdc1b4a088533806caa4160d77106aba5e649db9faa8c217444f3",
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
if instance.get("theorem_id") != "THM-M-0402":
    fail("instance theorem identity mismatch")
target = instance.get("canonical_formal_target", {})
if target.get("declaration_or_expression") != \
        "Stage1Instances.THMM0402.EvertseSUnitStatement":
    fail("canonical target mismatch")
if instance.get("assurance", {}).get("theorem_complete") is not False:
    fail("open theorem is falsely marked complete")

ids = [row["obligation_id"] for row in registry["obligations"]]
node_ids = [row["obligation_id"] for row in graphs["nodes"]]
if len(ids) != 10 or len(ids) != len(set(ids)) or set(ids) != set(node_ids):
    fail("frozen obligation/node identities differ")
closure = graphs.get("closure_boundary", {})
if closure.get("root_machine_debt") != "M3" or closure.get("closed_obligations") != []:
    fail("structured authority makes an unsupported closure claim")
if closure.get("composition_certificates") != [] or closure.get("theorem_complete") is not False:
    fail("graph bundle falsely closes the theorem")

tree = subprocess.run(
    ["python3", str(OWNED / "validate_obligation_tree.py")],
    cwd=ROOT, capture_output=True, text=True, timeout=30,
)
if tree.returncode != 0 or "root closure: open (M3)" not in tree.stdout:
    fail(f"obligation-tree validation failed\n{tree.stdout}{tree.stderr}")

block_comment = re.compile(r"/-.*?-/", re.DOTALL)
prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    source = block_comment.sub("", (OWNED / name).read_text(encoding="utf-8"))
    source = "\n".join(line.split("--", 1)[0] for line in source.splitlines())
    if prohibited.search(source):
        fail(f"prohibited local token in {name}")

outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0402-validation-", dir=LEAN_ROOT) as raw_tmp:
    tmp = Path(raw_tmp)
    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(OWNED / name, tmp / name)

    statement = subprocess.run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"),
         str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT, capture_output=True, text=True, timeout=60,
    )
    outputs["Statement.lean"] = statement.stdout + statement.stderr
    if statement.returncode != 0:
        fail(f"Lean recipe failed for Statement.lean\n{outputs['Statement.lean']}")

    printenv = subprocess.run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT,
        capture_output=True, text=True, timeout=30,
    )
    if printenv.returncode != 0:
        fail(f"could not resolve pinned LEAN_PATH\n{printenv.stdout}{printenv.stderr}")
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{printenv.stdout.strip()}"
    for name in ("Proof.lean", "Validation.lean"):
        result = subprocess.run(
            ["lake", "env", "lean", str(tmp / name)], cwd=LEAN_ROOT,
            env=env, capture_output=True, text=True, timeout=60,
        )
        outputs[name] = result.stdout + result.stderr
        if result.returncode != 0:
            fail(f"Lean recipe failed for {name}\n{outputs[name]}")

for name, output in outputs.items():
    if "sorryAx" in output:
        fail(f"Lean reported sorryAx for {name}")

for name in ("Proof.lean", "Validation.lean"):
    flattened = " ".join(outputs[name].split())
    for allowed in ("propext", "Classical.choice", "Quot.sound"):
        if allowed not in flattened:
            fail(f"{name} axiom report omitted expected permitted axiom {allowed}")

print(
    "validation ok: statement and partial normalization results re-elaborated; "
    "independent probe passed; root remains open M3"
)
