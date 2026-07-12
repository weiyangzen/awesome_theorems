#!/usr/bin/env python3
"""Elaborate the local statement and conditional composition with pinned Lake artifacts."""

import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN = ROOT / "Formalizations" / "Lean"
olean = HERE / "Statement.olean"

statement = ["lake", "env", "lean", "-R", "../..", "-o", "../../Stage1_Instances/THM-M-1271/Statement.olean", "../../Stage1_Instances/THM-M-1271/Statement.lean"]
composition = ["lake", "env", "lean", "-R", "../..", "../../Stage1_Instances/THM-M-1271/ObligationTree.lean"]
env = os.environ.copy()
env["LEAN_PATH"] = "../../Stage1_Instances/THM-M-1271"
try:
    subprocess.run(statement, cwd=LEAN, env=env, check=True)
    subprocess.run(composition, cwd=LEAN, env=env, check=True)
finally:
    olean.unlink(missing_ok=True)
print("PASS pinned Lean elaboration: conditional exact-root composition")
