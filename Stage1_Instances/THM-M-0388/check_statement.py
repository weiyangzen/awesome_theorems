#!/usr/bin/env python3
"""Re-elaborate and fingerprint the THM-M-0388 statement and its mutations."""

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

marker = "def Stage1Instances.THMM0388.PellEquationStatement : Prop :=\n"
if marker not in result.stdout:
    raise SystemExit("canonical #print marker missing")
serialized = marker + result.stdout.split(marker, 1)[1].strip() + "\n"
digest = hashlib.sha256(serialized.encode()).hexdigest()

text = SOURCE.read_text()
canonical = text.split("def PellEquationStatement : Prop :=", 1)[1].split(
    "/-- A conjunction presentation", 1
)[0].strip()
mutations = [
    "MutationRemovedNonsquare",
    "MutationChangedDomain",
    "MutationChangedBinderScope",
    "MutationSquareBoundary",
]
for name in mutations:
    body = text.split(f"def {name} : Prop :=", 1)[1].split("\ndef ", 1)[0].split(
        "\nend Stage1Instances", 1
    )[0].strip()
    if body == canonical:
        raise SystemExit(f"mutation survived as identical source: {name}")

print(f"statement elaboration: ok")
print(f"elaborated_expression_sha256: {digest}")
print(f"mutation fixtures killed: {len(mutations)}/4")
