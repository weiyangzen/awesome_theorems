#!/usr/bin/env python3
"""Elaborate and fingerprint the THM-M-1016 statement and mutation probes."""

import hashlib
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
SOURCE = pathlib.Path("../../Stage1_Instances/THM-M-1016/Statement.lean")
NAMES = [
    "StatementShape",
    "MutationNoScalingLimit",
    "MutationRealDomain",
    "MutationVaryingCenter",
    "MutationZeroScaling",
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

blocks = re.split(r"(?=def Stage1Instances\.THM_M_1016\.)", run.stdout)
expressions = {}
for block in blocks:
    match = re.match(r"def Stage1Instances\.THM_M_1016\.([A-Za-z0-9_]+).*", block)
    if match and match.group(1) in NAMES:
        expressions[match.group(1)] = block.strip()

missing = [name for name in NAMES if name not in expressions]
if missing:
    raise SystemExit(f"missing elaborated expressions: {missing}")

hashes = {name: hashlib.sha256(expressions[name].encode()).hexdigest() for name in NAMES}
canonical = hashes[NAMES[0]]
collisions = [name for name in NAMES[1:] if hashes[name] == canonical]
if collisions:
    raise SystemExit(f"mutations not distinguished: {collisions}")

source_text = (HERE / "Statement.lean").read_text()
for forbidden in ("sorry", "admit", "axiom", "sorryAx"):
    if re.search(rf"\b{forbidden}\b", source_text):
        raise SystemExit(f"forbidden token in executable statement: {forbidden}")

print(f"canonical expression sha256: {canonical}")
for name in NAMES[1:]:
    print(f"distinguished {name}: {hashes[name]}")
print(f"statement file sha256: {hashlib.sha256(source_text.encode()).hexdigest()}")
