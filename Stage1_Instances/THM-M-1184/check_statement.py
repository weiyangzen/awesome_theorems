#!/usr/bin/env python3
"""Validate the frozen target serialization and distinguish its mutations."""

import hashlib
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LEAN_ROOT = HERE.parents[1] / "Formalizations" / "Lean"
SOURCE = HERE / "Statement.lean"
NAMES = [
    "KantorovichDualityTarget",
    "mutationRemovedContinuity",
    "mutationENNRealCost",
    "mutationNonnegativePotentials",
    "mutationEqualityToWeakDuality",
]

probe = SOURCE.read_text()
for name in NAMES[1:]:
    probe += (
        "set_option pp.explicit true in\n"
        f"#print Stage1Instances.THM_M_1184.{name}\n"
    )

result = subprocess.run(
    ["lake", "env", "lean", "/dev/stdin"], cwd=LEAN_ROOT,
    input=probe, text=True, capture_output=True
)
if result.returncode:
    sys.stderr.write(result.stdout + result.stderr)
    raise SystemExit(result.returncode)

chunks = result.stdout.split("def Stage1Instances.THM_M_1184.")[1:]
if len(chunks) != len(NAMES):
    raise SystemExit("did not serialize every target and mutation")
expressions = {}
for chunk, expected in zip(chunks, NAMES):
    name, body = chunk.split(" : Prop :=\n", 1)
    if not name.startswith(expected):
        raise SystemExit(f"unexpected declaration order: {name}")
    expressions[expected] = body.rstrip()

target = expressions[NAMES[0]]
target_hash = hashlib.sha256(target.encode()).hexdigest()
for mutation in NAMES[1:]:
    if expressions[mutation] == target:
        raise SystemExit(f"mutation not distinguished: {mutation}")

source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
print(f"expression_sha256={target_hash}")
print(f"statement_file_sha256={source_hash}")
print("mutations_distinguished=4")
