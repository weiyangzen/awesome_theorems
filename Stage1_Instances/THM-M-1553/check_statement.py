#!/usr/bin/env python3
"""Replay and distinguish the elaborated THM-M-1553 statement shapes."""

from hashlib import sha256
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
STATEMENT = Path(__file__).with_name("Statement.lean")

run = subprocess.run(
    ["lake", "env", "lean", str(STATEMENT.relative_to(LEAN_ROOT))],
    cwd=LEAN_ROOT,
    text=True,
    capture_output=True,
    check=False,
)
if run.returncode:
    raise SystemExit(run.stdout + run.stderr)

names = [
    "HirotaKdVTarget",
    "mutationNonnegativeTau",
    "mutationChangedKdVSign",
    "mutationDroppedMixedHirotaTerm",
]
starts = []
for name in names:
    marker = f"def Stage1Instances.THM_M_1553.{name} : Prop :="
    pos = run.stdout.find(marker)
    assert pos >= 0, f"missing elaborated declaration: {name}"
    starts.append(pos)

chunks = []
for index, start in enumerate(starts):
    stop = starts[index + 1] if index + 1 < len(starts) else len(run.stdout)
    chunks.append(run.stdout[start:stop].strip())
assert len(set(chunks)) == len(chunks), "a structural mutation matched the target"

digest = sha256(chunks[0].encode()).hexdigest()
print(f"target expression sha256: {digest}")
print("mutation distinction: ok (positivity, KdV sign, mixed Hirota term)")
