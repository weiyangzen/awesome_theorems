#!/usr/bin/env python3
"""Fail-closed narrow proof check for THM-M-1524."""

from pathlib import Path
import os
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"

proof = (HERE / "Proof.lean").read_text()
for token in ("sorry", "admit", "axiom ", "sorryAx"):
    assert token not in proof, f"forbidden proof token: {token!r}"

with tempfile.TemporaryDirectory(prefix="thm-m-1524-proof-") as directory:
    cache = Path(directory)
    module_dir = cache / "Stage1_Instances" / "THM-M-1524"
    module_dir.mkdir(parents=True)
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{cache}:{env.get('LEAN_PATH', '')}"
    commands = [
        ["lake", "env", "lean", "-R", str(ROOT), "-o", str(module_dir / "Statement.olean"), str(HERE / "Statement.lean")],
        ["lake", "env", "lean", "-R", str(ROOT), "-o", str(module_dir / "ObligationTree.olean"), str(HERE / "ObligationTree.lean")],
        ["lake", "env", "lean", str(HERE / "Proof.lean")],
    ]
    outputs = []
    for command in commands:
        run = subprocess.run(command, cwd=LEAN_DIR, env=env, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sys.stdout.write(run.stdout)
        assert run.returncode == 0, f"Lean command failed: {command}"
        outputs.append(run.stdout)

axiom_output = outputs[-1]
for declaration in (
    "Observable.robertson",
    "Observable.heisenbergCCR",
    "heisenberg_uncertainty",
):
    assert declaration in axiom_output
assert "sorryAx" not in axiom_output
assert "[propext, Classical.choice, Quot.sound]" in axiom_output
print("PASS THM-M-1524 proof: exact Robertson, CCR transport, and root composition elaborated")
print("axioms: [propext, Classical.choice, Quot.sound]; placeholders: none")
