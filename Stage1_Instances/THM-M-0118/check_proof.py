#!/usr/bin/env python3
"""Validate the proof-phase countermodel for frozen THM-M-0118."""

from pathlib import Path
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
LEAN_DIR = HERE.parents[1] / "Formalizations" / "Lean"
STATEMENT_OLEAN = HERE / "Statement.olean"


def run(argv, *, cwd, env=None):
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    sys.stdout.write(result.stdout)
    if result.returncode:
        raise SystemExit(result.returncode)
    return result.stdout


def main() -> None:
    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_DIR).strip()
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_DIR
    ).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = lean_path
    try:
        run([lean, "-o", str(STATEMENT_OLEAN), "Statement.lean"], cwd=HERE, env=env)
        env["LEAN_PATH"] = f"{HERE}:{lean_path}"
        output = run([lean, "Proof.lean"], cwd=HERE, env=env)
    finally:
        STATEMENT_OLEAN.unlink(missing_ok=True)

    source = (HERE / "Proof.lean").read_text()
    forbidden = ("sorry", "admit", "axiom ", "sorryAx")
    if any(token in source for token in forbidden):
        raise SystemExit("forbidden proof token in Proof.lean")
    expected = (
        "'Stage1Instances.THMM0118.not_nakanoVanishingTarget' "
        "depends on axioms: [propext]"
    )
    if expected not in output:
        raise SystemExit("unexpected #print axioms result")
    print("PASS THM-M-0118 proof phase: exact frozen target has a checked countermodel")
    print("positive proof closure: blocked; the abstract statement interface is inconsistent with the intended theorem")


if __name__ == "__main__":
    main()
