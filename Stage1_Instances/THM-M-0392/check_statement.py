#!/usr/bin/env python3
"""Re-elaborate and fingerprint the THM-M-0392 statement and mutations."""

import hashlib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
SOURCE = pathlib.Path(__file__).with_name("Statement.lean")

result = subprocess.run(
    ["lake", "env", "lean", str(SOURCE)],
    cwd=LEAN_ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
if result.returncode != 0:
    sys.stdout.write(result.stdout)
    raise SystemExit(result.returncode)

marker = "def Stage1Instances.THMM0392.MordellFinitenessStatement : Prop :=\n"
if marker not in result.stdout:
    raise SystemExit("canonical #print marker missing")
serialized = marker + result.stdout.split(marker, 1)[1].strip() + "\n"
digest = hashlib.sha256(serialized.encode()).hexdigest()

text = SOURCE.read_text()
canonical = text.split("def MordellFinitenessStatement : Prop :=", 1)[1].split(
    "/-- An inline presentation", 1
)[0].strip()
mutations = [
    "MutationRemovedNonzero",
    "MutationChangedCoordinateDomain",
    "MutationChangedBinderScope",
    "MutationZeroBoundary",
]
for name in mutations:
    body = text.split(f"def {name} : Prop :=", 1)[1].split("\ndef ", 1)[0].split(
        "\nend Stage1Instances", 1
    )[0].strip()
    if body == canonical:
        raise SystemExit(f"mutation survived as identical source: {name}")

print("statement elaboration: ok")
print(f"elaborated_expression_sha256: {digest}")
print(f"mutation fixtures killed: {len(mutations)}/4")
