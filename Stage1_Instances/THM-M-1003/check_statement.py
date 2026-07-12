#!/usr/bin/env python3
"""Re-elaborate and distinguish the THM-M-1003 statement mutations."""

from hashlib import sha256
from pathlib import Path
import subprocess


instance_dir = Path(__file__).resolve().parent
lean_dir = instance_dir.parents[1] / "Formalizations" / "Lean"
statement = instance_dir / "Statement.lean"
relative_statement = Path("../../Stage1_Instances/THM-M-1003/Statement.lean")

run = subprocess.run(
    ["lake", "env", "lean", str(relative_statement)],
    cwd=lean_dir,
    text=True,
    capture_output=True,
    check=False,
)
if run.returncode != 0:
    raise SystemExit(run.stdout + run.stderr)

names = [
    "LpMartingaleConvergenceTarget",
    "mutationRemovedMartingale",
    "mutationRemovedLpBound",
    "mutationIncludesEndpointOne",
    "mutationLpConvergenceOnly",
]
blocks = {}
for name in names:
    marker = f"def Stage1Instances.THM_M_1003.{name}."
    start = run.stdout.find(marker)
    if start < 0:
        raise SystemExit(f"missing elaborated expression for {name}")
    next_start = run.stdout.find("\ndef Stage1Instances.THM_M_1003.", start + 1)
    blocks[name] = run.stdout[start : next_start if next_start >= 0 else None].strip()

hashes = {name: sha256(block.encode()).hexdigest() for name, block in blocks.items()}
if len(set(hashes.values())) != len(names):
    raise SystemExit("a structural mutation did not change the explicit expression")

print(f"statement_file_sha256={sha256(statement.read_bytes()).hexdigest()}")
for name in names:
    print(f"{name}_expression_sha256={hashes[name]}")
print("mutations_distinguished=4/4")
