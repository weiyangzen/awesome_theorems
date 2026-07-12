#!/usr/bin/env python3
"""Run the narrow rev-5.6 statement checks for THM-M-0321."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
SOURCE = ROOT / "Stage1_Instances" / "THM-M-0321" / "Statement.lean"
RECORD = SOURCE.with_name("statement.json")


def run(argv: list[str], cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)


source = SOURCE.read_text(encoding="utf-8")
for forbidden in ("sorry", "admit", "axiom"):
    if re.search(rf"\b{forbidden}\b", source):
        raise SystemExit(f"forbidden token in Statement.lean: {forbidden}")

required = (
    "def MarkovKakutaniTarget",
    "theorem markovKakutaniTarget_iff_eqOnCommutationTarget",
    "def mutationRemovedCompactness",
    "def mutationChangedDomain",
    "def mutationChangedBinderScope",
    "def mutationNonemptyIndex",
    "theorem emptyFamily_boundary",
)
for marker in required:
    if marker not in source:
        raise SystemExit(f"missing statement marker: {marker}")

for mutation in (
    "mutationRemovedCompactness",
    "mutationChangedDomain",
    "mutationChangedBinderScope",
    "mutationNonemptyIndex",
):
    probe = (
        source
        + "\nexample : Stage1Instances.THM_M_0321.MarkovKakutaniTarget "
        + f"= Stage1Instances.THM_M_0321.{mutation} := rfl\n"
    )
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".lean", dir=SOURCE.parent, encoding="utf-8"
    ) as handle:
        handle.write(probe)
        handle.flush()
        mutated = run(
            ["lake", "env", "lean", os.path.relpath(handle.name, LEAN_ROOT)], LEAN_ROOT
        )
    if mutated.returncode == 0:
        raise SystemExit(f"mutation unexpectedly definitionally equals target: {mutation}")
    failure = mutated.stdout + mutated.stderr
    if not any(marker in failure for marker in ("type mismatch", "rfl", "not definitionally equal")):
        raise SystemExit(f"mutation failed for an unexpected reason: {mutation}: {failure[-500:]}")

lean = run(["lake", "env", "lean", os.path.relpath(SOURCE, LEAN_ROOT)], LEAN_ROOT)
sys.stdout.write(lean.stdout)
sys.stderr.write(lean.stderr)
if lean.returncode:
    raise SystemExit(lean.returncode)

printed = lean.stdout[lean.stdout.find("def Stage1Instances.THM_M_0321.MarkovKakutaniTarget") :]
if not printed:
    raise SystemExit("canonical #print output was not captured")
digest = hashlib.sha256(printed.encode("utf-8")).hexdigest()
recorded = json.loads(RECORD.read_text(encoding="utf-8"))["canonical_formal_target"][
    "expression_sha256"
]
if digest != recorded:
    raise SystemExit(f"expression hash mismatch: computed {digest}, recorded {recorded}")

version = run(["lake", "env", "lean", "--version"], LEAN_ROOT)
if version.returncode:
    raise SystemExit(version.returncode)
toolchain = (LEAN_ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
print(f"canonical_expression_sha256={digest}")
print(f"toolchain={toolchain}")
print(f"lean_version={version.stdout.strip()}")
print("statement checks: ok")
