#!/usr/bin/env python3
"""Narrow, fail-closed validation runner for THM-M-0413."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0413"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED = {
    "Statement.lean": "772249ff06b39a69095c6d7fd1b490592ee488e76d0248f24e0d5bfdac76c56b",
    "ObligationTree.lean": "7a0ff39c63384b37b6f1b55cfbf3529b92caa2caece7ef257ed00cb9076b30f0",
    "Proof.lean": "782bd491c5722f2d8ae6a392001212b23943ad44fd4d54f7e869cef004cdbb0a",
    "obligation-registry.json": "884be3f3bf1c3ab8a7b18463147e604c55d020d399b0abcb9ceb7c39c16e752d",
    "typed-graphs.json": "167d81820491367fab533ed337b7b780a0c3e5b0c3ea711d288aac88be54a2a2",
    "proof-receipt.json": "13f84f3ae0b1b176b9ed7f94e8fa7c3c09d082a7ec63ba10bbfb837ab05eb8d7",
}
PROHIBITED = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\s", re.MULTILINE)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], cwd: Path) -> str:
    result = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, timeout=120)
    output = result.stdout + result.stderr
    if result.returncode != 0:
        fail(f"{' '.join(argv)} exited {result.returncode}\n{output}")
    return output


for name, digest in EXPECTED.items():
    path = OWNED / name
    if sha256(path) != digest:
        fail(f"frozen input hash mismatch: {name}")

registry = json.loads((OWNED / "obligation-registry.json").read_text())
graphs = json.loads((OWNED / "typed-graphs.json").read_text())
if registry["canonical_root"] != "THM-M-0413-ROOT" or len(registry["obligations"]) != 10:
    fail("unexpected canonical root or obligation denominator")
if set(graphs["nodes"]) != {row["obligation_id"] for row in registry["obligations"]}:
    fail("typed graph nodes disagree with the frozen registry")

for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    if PROHIBITED.search((OWNED / name).read_text()):
        fail(f"prohibited Lean token in {name}")

revision = run(["git", "rev-parse", "HEAD"], MATHLIB).strip()
if revision != EXPECTED_MATHLIB:
    fail(f"mathlib revision drift: {revision}")
if run(["git", "status", "--porcelain"], MATHLIB):
    fail("pinned mathlib source worktree is dirty")

with tempfile.TemporaryDirectory(prefix="m0413-validation-", dir=LEAN_ROOT) as directory:
    temp = Path(directory)
    outputs = []
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        probe = temp / name
        probe.write_bytes((OWNED / name).read_bytes())
        outputs.append(run(["lake", "env", "lean", str(probe)], LEAN_ROOT))

combined = "\n".join(outputs)
for declaration in ("exactRoot", "exactRootFromComponents", "independentExactRoot"):
    if declaration not in combined:
        fail(f"Lean output did not identify {declaration}")
for axiom in ("propext", "Classical.choice", "Quot.sound"):
    if axiom not in combined:
        fail(f"expected observed axiom absent from Lean output: {axiom}")

print("ok: four frozen/narrow modules elaborated from fresh temporary source copies")
print("ok: exact root, component assembly, and independently written exact-type probe checked")
print("ok: observed axioms are propext, Classical.choice, and Quot.sound")
print("ok: frozen hashes, registry denominator, placeholder scan, and clean pinned mathlib passed")
print("blocked: warm shared .lake cache is not an empty-cache hermetic release replay")
print("blocked: one mutable worker is not a distinct independently provisioned verifier")
