#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
lean_dir = root / "Formalizations" / "Lean"
statement = Path(__file__).with_name("Statement.lean")
command = ["lake", "env", "lean", str(statement.relative_to(lean_dir))]
run = subprocess.run(command, cwd=lean_dir, text=True, capture_output=True)
if run.returncode:
    sys.stdout.write(run.stdout)
    sys.stderr.write(run.stderr)
    raise SystemExit(run.returncode)

out = run.stdout
names = ["OnofriInequality", "MutationZeroMeanOnly", "MutationEnergyCoefficient"]
blocks = {}
for name in names:
    marker = f"def Stage1Instances.THM_M_1278.{name}"
    start = out.find(marker)
    if start < 0:
        raise SystemExit(f"missing printed declaration: {name}")
    ends = [out.find(f"def Stage1Instances.THM_M_1278.{other}", start + 1) for other in names]
    ends = [end for end in ends if end >= 0]
    blocks[name] = out[start : min(ends) if ends else len(out)].strip()

if len(set(blocks.values())) != len(names):
    raise SystemExit("a statement mutation did not change the elaborated declaration")

digest = hashlib.sha256(blocks["OnofriInequality"].encode()).hexdigest()
expected = json.loads(Path(__file__).with_name("statement.json").read_text())[
    "canonical_formal_target"
]["elaborated_expression_sha256"]
if digest != expected:
    raise SystemExit(f"canonical expression digest mismatch: {digest} != {expected}")

print(f"ok: canonical expression sha256 {digest}; two mutations distinguished")
