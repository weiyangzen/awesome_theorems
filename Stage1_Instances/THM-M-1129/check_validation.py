#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-1129-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1129"
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
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == "S56-M-1129-VALIDATION"
assert spec["theorem_id"] == "THM-M-1129"
assert spec["network_policy"] == "denied"
assert statement_record["canonical_formal_target"]["source_sha256"] == (
    "sha256:" + sha256(HERE / "Statement.lean")
)
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == sha256(
    HERE / "obligation-registry.json"
)

lean_source = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean")
)
for pattern in (r"\b(?:sorry|admit)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern
assert "theorem PoissonFormulaTarget" not in lean_source

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m1129-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    statement_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env
    )

assert "PoissonFormulaTarget : Prop" in statement_output
assert "poissonFormulaTarget_of_analyticPackage" in obligation_output
for declaration in (
    "poissonDiskTerm_zero_time",
    "poissonDiskTerm_zero_data",
    "deriv_poissonDiskTerm_zero_data",
    "poissonExpression_zero_data",
):
    assert declaration in proof_output
for output in (obligation_output, proof_output):
    for disallowed in ("sorryAx", "Lean.ofReduceBool", "implemented_by"):
        assert disallowed not in output
for axiom in ("propext", "Classical.choice", "Quot.sound"):
    assert axiom in proof_output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M3"
assert closure["remaining_root_cut_set"] == ["M1129-T-REPRESENT"]

print("ok: exact statement, conditional composition, and four local boundary bodies elaborated in a fresh temporary module directory")
print("ok: proof bodies report only the permitted classical mathlib axiom profile")
print("ok: placeholder scan, source fingerprints, registry denominator, proof provenance hashes, and clean pinned mathlib checks passed")
print("open: exact root still requires PoissonAnalyticPackage; M1129-T-REPRESENT is the root cut")
print("blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
