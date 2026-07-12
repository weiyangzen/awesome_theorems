#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1333-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1333"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement_record = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == "S56-M-1333-VALIDATION"
assert spec["theorem_id"] == registry["theorem_id"] == "THM-M-1333"
assert statement_record["canonical_formal_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == sha256(HERE / "obligation-registry.json")
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert proof_receipt["result"]["root_closed"] is False

lean_files = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
lean_source = "\n".join((HERE / name).read_text() for name in lean_files)
for pattern in (r"\b(?:sorry|admit|sorryAx)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m1333-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in lean_files:
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(["lake", "env", "lean", str(tmp / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env)
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    validation_output = run(["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env)

for declaration, output in (
    ("isSolutionWithin_of_components", obligation_output),
    ("peanoExistence_fin_zero", proof_output),
    ("peanoExistenceTarget_of_positive_dimension", proof_output),
    ("peanoExistenceFinZeroDirect", validation_output),
    ("peanoExistenceTargetConditionalDirect", validation_output),
):
    lines = output.splitlines()
    index = next(i for i, line in enumerate(lines) if declaration in line and "depends on axioms" in line)
    report = " ".join(lines[index:index + 4])
    for axiom in ("propext", "Classical.choice", "Quot.sound"):
        assert axiom in report, (declaration, report)
    assert "sorryAx" not in report, (declaration, report)

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M4"
assert "M1333-C-EULER" in closure["remaining_root_cut_set"]
assert re.search(r"^[ \t]*(?:theorem|def)\s+peanoExistenceTarget\b", lean_source, re.MULTILINE) is None

print("PASS narrow kernel replay: statement, packaging, zero-dimensional proof, and conditional assembly elaborated")
print("PASS trust observation: five declarations report propext, Classical.choice, and Quot.sound, without sorryAx")
print("PASS local provenance: statement, registry, proof receipt, proof body, and clean pinned mathlib hashes agree")
print("PASS same-worker differential probe: Validation.lean reconstructs the checked branch without importing Proof")
print("OPEN exact root: the positive-dimensional Peano-existence route has no proof body")
print("STALE frozen graph: proof-phase partial closures await master reconciliation")
print("BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, and no distinct independent runner")
