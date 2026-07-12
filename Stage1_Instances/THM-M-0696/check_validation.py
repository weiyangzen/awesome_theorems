#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0696-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0696"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


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
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-0696-VALIDATION"
assert spec["theorem_id"] == statement["theorem_id"] == registry["theorem_id"] == "THM-M-0696"
assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

lean_files = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
lean_source = "\n".join((HERE / name).read_text() for name in lean_files)
for pattern in (
    r"\b(?:sorry|admit|sorryAx)\b",
    r"^[ \t]*axiom\b",
    r"^[ \t]*unsafe\b",
):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0696-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in lean_files:
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Proof.olean"), str(tmp / "Proof.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    validation_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )

axiom_line = next(
    line
    for line in validation_output.splitlines()
    if "propositional_completeness" in line and "depends on axioms" in line
)
for axiom in ("propext", "Classical.choice", "Quot.sound"):
    assert axiom in axiom_line, axiom_line

# The proof phase postdates the frozen graph. Validation observes the discrepancy; it does not
# rewrite scope authority or silently award graph closure.
closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["root_vector"] == ["H1", "M3", "R3"]
assert "propositional_completeness" in (HERE / "Proof.lean").read_text()

print("PASS narrow kernel replay: exact frozen root elaborated from a fresh temporary module directory")
print("PASS trust observation: exact root reports propext, Classical.choice, and Quot.sound")
print("PASS local provenance: statement, registry denominator, clean pinned mathlib, and source hygiene agree")
print("STALE frozen graph: it predates Proof.lean and remains H1/M3/R3 pending master reconciliation")
print("BLOCKED release gates: warm shared .lake, incomplete TCB/SBOM archive, and no distinct independent runner")
