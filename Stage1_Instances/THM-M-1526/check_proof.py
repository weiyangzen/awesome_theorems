#!/usr/bin/env python3
"""Narrow elaboration and placeholder check for THM-M-1526's proof node."""

import os
import re
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN_ROOT = HERE.parents[1] / "Formalizations" / "Lean"


def run(command, **kwargs):
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, **kwargs)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    return result.stdout


lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()

source = (HERE / "Proof.lean").read_text()
assert not re.search(r"\b(sorry|sorryAx|admit)\b", source)
assert not re.search(r"(?m)^\s*axiom\s", source)

with tempfile.TemporaryDirectory(prefix="thm-m-1526-proof-") as output:
    env = {**os.environ, "LEAN_PATH": lean_path}
    run([lean, "-o", f"{output}/Statement.olean", "Statement.lean"], cwd=HERE, env=env)
    env["LEAN_PATH"] = output + ":" + lean_path
    run([lean, "-o", f"{output}/ObligationTree.olean", "ObligationTree.lean"], cwd=HERE, env=env)
    proof_output = run([lean, "Proof.lean"], cwd=HERE, env=env)

assert "freeDiracFactorizationTarget' depends on axioms" in proof_output
assert "sorryAx" not in proof_output
assert all(name in proof_output for name in
           ("paired_term", "slash_square", "freeDiracFactorization",
            "freeDiracFactorizationTarget"))
print("PASS THM-M-1526 proof: exact root elaborated without placeholders")
print("axioms: propext, Classical.choice, Quot.sound")
