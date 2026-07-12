#!/usr/bin/env python3
"""Fail-closed validation of the THM-M-0118 proof-phase blocker."""

from pathlib import Path
import hashlib
import json
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


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    statement = json.loads((HERE / "statement.json").read_text())
    blocker = json.loads((HERE / "proof-blocker.json").read_text())
    expected_statement = statement["canonical_formal_target"]["statement_file_sha256"]
    if sha256(HERE / "Statement.lean") != expected_statement:
        raise SystemExit("statement changed since its frozen receipt")
    if blocker["root_closed"] or blocker["theorem_complete"]:
        raise SystemExit("proof blocker illegally claims positive closure")
    if blocker["countermodel_declaration"] != (
        "Stage1Instances.THMM0118.not_nakanoVanishingTarget"
    ):
        raise SystemExit("unexpected proof-phase countermodel declaration")

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_DIR).strip()
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_DIR).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = lean_path
    try:
        run([lean, "-o", str(STATEMENT_OLEAN), "Statement.lean"], cwd=HERE, env=env)
        env["LEAN_PATH"] = f"{HERE}:{lean_path}"
        output = run([lean, "Validation.lean"], cwd=HERE, env=env)
    finally:
        STATEMENT_OLEAN.unlink(missing_ok=True)

    source = (HERE / "Validation.lean").read_text()
    forbidden = ("sorry", "admit", "axiom ", "sorryAx")
    if any(token in source for token in forbidden):
        raise SystemExit("forbidden proof token in Validation.lean")
    expected = (
        "'Stage1Instances.THMM0118.Validation.independent_root_countermodel' "
        "depends on axioms: [propext, Quot.sound]"
    )
    if expected not in output:
        raise SystemExit("unexpected independent trust report")

    print("PASS THM-M-0118 validation: independent ZMod 2 model confirms the frozen root is false")
    print("VALIDATION BLOCKED: no positive root exists for hermetic or release verification")


if __name__ == "__main__":
    main()
