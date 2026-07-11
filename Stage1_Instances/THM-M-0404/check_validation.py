#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0404-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0404"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement_record = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-0404-VALIDATION"
assert spec["theorem_id"] == "THM-M-0404"
assert statement_record["canonical_formal_target"]["statement_file_sha256"] == sha256(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

lean_source = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean")
)
for pattern in (r"\b(?:sorry|admit)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0404-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env
    )

for declaration, output in (
    ("root_of_eventualPeriodic_packages", obligation_output),
    ("eventualPeriodic_to_finiteUnion", proof_output),
    ("root_of_eventuallyPeriodicZeroSets", proof_output),
):
    assert f"'{declaration}' depends on axioms" in output or (
        f"'Stage1Instances.THM_M_0404.{declaration}' depends on axioms" in output
    )
    for axiom in ("propext", "Classical.choice", "Quot.sound"):
        assert axiom in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert "M0404-T-EVENTUAL" in closure["remaining_root_cut_set"]
assert "M0404-L-COMBINATORIAL" in closure["remaining_root_cut_set"]
assert "eventualPeriodic_to_finiteUnion" in lean_source
assert "root_of_eventuallyPeriodicZeroSets" in lean_source

print("ok: pinned statement, conditional composition, and combinatorial proof elaborated in a fresh temporary module directory")
print("ok: checked declarations report only propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, statement fingerprint, registry denominator, and clean pinned mathlib checks passed")
print("open: exact root has an explicit EventuallyPeriodicZeroSets premise (M0404-T-EVENTUAL)")
print("stale: frozen graph still reports M0404-L-COMBINATORIAL open despite the proof-phase body")
print("blocked: cold hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
