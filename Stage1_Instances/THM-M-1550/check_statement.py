#!/usr/bin/env python3
"""Elaborate and fingerprint the canonical Lax target and its mutations."""

import hashlib
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LEAN_ROOT = HERE.parents[1] / "Formalizations" / "Lean"
SOURCE = pathlib.Path("../../Stage1_Instances/THM-M-1550/Statement.lean")
NAMES = [
    "LaxPairIsospectrality",
    "mutationRemovedLaxEquation",
    "mutationChangedIndexDomain",
    "mutationChangedBinderScope",
    "mutationChangedBoundaryPolicy",
]

run = subprocess.run(
    ["lake", "env", "lean", str(SOURCE)],
    cwd=LEAN_ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
if run.returncode:
    sys.stdout.write(run.stdout)
    raise SystemExit(run.returncode)

blocks = re.split(r"(?=def Stage1Instances\.THM_M_1550\.)", run.stdout)
expressions = {}
for block in blocks:
    match = re.match(r"def Stage1Instances\.THM_M_1550\.([A-Za-z0-9_]+).*", block)
    if match and match.group(1) in NAMES:
        expressions[match.group(1)] = block.strip()

missing = [name for name in NAMES if name not in expressions]
if missing:
    raise SystemExit(f"missing explicit elaborated expressions: {missing}")

hashes = {
    name: hashlib.sha256(expressions[name].encode("utf-8")).hexdigest()
    for name in NAMES
}
canonical = hashes[NAMES[0]]
collisions = [name for name in NAMES[1:] if hashes[name] == canonical]
if collisions:
    raise SystemExit(f"mutations not distinguished from canonical target: {collisions}")

print(f"canonical expression sha256: {canonical}")
for name in NAMES[1:]:
    print(f"killed mutation {name}: {hashes[name]}")
