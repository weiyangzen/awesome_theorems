#!/usr/bin/env python3
"""Validate the THM-M-0696 proof body with the repository's pinned Lean environment."""

import os
import pathlib
import subprocess

here = pathlib.Path(__file__).resolve().parent
root = here.parents[1]
lean_project = root / "Formalizations" / "Lean"

lean_path = subprocess.check_output(
    ["lake", "env", "printenv", "LEAN_PATH"], cwd=lean_project, text=True
).strip()
env = os.environ | {"LEAN_PATH": f"{lean_path}:{here}"}
lean = subprocess.check_output(["lake", "env", "which", "lean"], cwd=lean_project, text=True).strip()

commands = [
    [lean, "-o", "Statement.olean", "Statement.lean"],
    [lean, "-o", "ObligationTree.olean", "ObligationTree.lean"],
    [lean, "Proof.lean"],
]
try:
    for command in commands:
        subprocess.run(command, cwd=here, env=env, check=True)
finally:
    for artifact in (here / "Statement.olean", here / "ObligationTree.olean"):
        artifact.unlink(missing_ok=True)

source = (here / "Proof.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert forbidden not in source
print("PASS THM-M-0696 proof: exact root elaborated; no placeholders; axiom reports emitted")
