#!/usr/bin/env python3
"""Elaborate and fingerprint the THM-M-1015 target and mutations."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
SOURCE = Path("../../Stage1_Instances/THM-M-1015/Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_1015"
NAMES = [
    "Statement",
    "mutationRemovedMeasurability",
    "mutationChangedIndexDomain",
    "mutationChangedConstantScope",
    "mutationIncludesZeroDenominator",
]

result = subprocess.run(
    ["lake", "env", "lean", str(SOURCE)], cwd=LEAN_ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
)
if result.returncode:
    sys.stdout.write(result.stdout)
    raise SystemExit(result.returncode)

pattern = re.compile(
    rf"def {re.escape(NAMESPACE)}\.({'|'.join(NAMES)}).*?(?="
    rf"def {re.escape(NAMESPACE)}\.|theorem {re.escape(NAMESPACE)}\.|\Z)",
    re.DOTALL,
)
expressions = {}
for match in pattern.finditer(result.stdout):
    name = re.match(rf"def {re.escape(NAMESPACE)}\.([A-Za-z0-9_]+)", match.group()).group(1)
    expressions[name] = match.group().strip()

missing = [name for name in NAMES if name not in expressions]
if missing:
    raise SystemExit(f"missing elaborated expressions: {missing}")

hashes = {name: hashlib.sha256(expressions[name].encode()).hexdigest() for name in NAMES}
survivors = [name for name in NAMES[1:] if hashes[name] == hashes[NAMES[0]]]
if survivors:
    raise SystemExit(f"statement mutations survived: {survivors}")

manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())
print(json.dumps({
    "statement_sha256": hashes["Statement"],
    "killed_mutations": NAMES[1:],
    "toolchain": (LEAN_ROOT / "lean-toolchain").read_text().strip(),
    "mathlib_revision": next(
        package["rev"] for package in manifest["packages"]
        if package["name"] == "mathlib"
    ),
}, sort_keys=True))
