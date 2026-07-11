#!/usr/bin/env python3
"""Validate the frozen THM-M-0417 statement against fresh Lean output."""

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN_ROOT = HERE.parents[1] / "Formalizations" / "Lean"
SOURCE = HERE / "Statement.lean"
RECORD = HERE / "statement.json"

run = subprocess.run(
    ["lake", "env", "lean", str(SOURCE)],
    cwd=LEAN_ROOT,
    check=True,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

markers = [
    "def Stage1Instances.THM_M_0417.Statement.{u} : Prop :=",
    "def Stage1Instances.THM_M_0417.mutationRemovedSymmetry.{u} : Prop :=",
    "def Stage1Instances.THM_M_0417.mutationRemovedConvexity.{u} : Prop :=",
    "def Stage1Instances.THM_M_0417.mutationNonStrictThreshold.{u} : Prop :=",
    "def Stage1Instances.THM_M_0417.mutationAllowsZeroWitness.{u} : Prop :=",
]
positions = [run.stdout.index(marker) for marker in markers]
sections = []
for index, start in enumerate(positions):
    end = positions[index + 1] if index + 1 < len(positions) else len(run.stdout)
    sections.append(run.stdout[start:end].rstrip() + "\n")

digests = [hashlib.sha256(section.encode()).hexdigest() for section in sections]
assert len(set(digests)) == len(digests), "a mutation did not change the elaborated expression"

record = json.loads(RECORD.read_text())
assert record["canonical_formal_target"]["elaborated_expression_sha256"] == digests[0]
assert record["canonical_formal_target"]["statement_file_sha256"] == hashlib.sha256(
    SOURCE.read_bytes()
).hexdigest()

print(f"canonical expression sha256: {digests[0]}")
print("four structural mutations elaborate and have distinct explicit expressions")
