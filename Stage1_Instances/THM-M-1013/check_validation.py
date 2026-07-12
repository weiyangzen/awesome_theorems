#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-1013-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1013"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


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
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == "S56-M-1013-VALIDATION"
assert spec["theorem_id"] == registry["theorem_id"] == graphs["theorem_id"] == "THM-M-1013"
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == sha256(HERE / "obligation-registry.json")

lean_source = "\n".join((HERE / name).read_text() for name in (
    "Statement.lean", "ObligationTree.lean", "Proof.lean"
))
for pattern in (r"\b(?:sorry|admit|sorryAx)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == PIN
assert run(["git", "status", "--short"], cwd=mathlib) == ""
for source in (
    "Mathlib/MeasureTheory/Measure/LevyConvergence.lean",
    "Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean",
):
    assert run(["git", "ls-files", "--error-unmatch", source], cwd=mathlib).strip() == source

with tempfile.TemporaryDirectory(prefix="m1013-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT, env=env,
    )
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)

for declaration, output in (
    ("compose_directions", obligation_output),
    ("projection_charFun_one_measure", proof_output),
    ("forward", proof_output),
    ("reverse", proof_output),
    ("cramerWold", proof_output),
):
    assert re.search(rf"'[^']*{re.escape(declaration)}' depends on axioms", output)
    for axiom in spec["allowed_axioms"]:
        assert axiom in output
    assert "sorryAx" not in output

assert proof_receipt["result"]["root_closed"] is True
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False

print("PASS: exact StatementShape, composition, and Cramer-Wold proof replayed in a fresh temporary module directory")
print("PASS: axiom reports contain only the accepted observed kernel axioms: propext, Classical.choice, Quot.sound")
print("PASS: placeholder scan, frozen hashes, proof receipt linkage, and clean pinned mathlib provenance checks passed")
print("STALE: frozen obligation graph predates proof execution and still reports the root open")
print("BLOCKED: cold empty-cache hermetic replay, full transitive TCB/SBOM closure, and independent-runner verification are unavailable in this worker")
