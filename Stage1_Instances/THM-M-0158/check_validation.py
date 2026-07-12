#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0158-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0158"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


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


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"(?:'{re.escape(declaration)}'|'Stage1Instances\.THM_M_0158\.{re.escape(declaration)}') "
        r"depends on axioms:\s*\[(.*?)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}\n{output}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


spec = json.loads((HERE / "validation-spec.json").read_text())
statement_record = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

assert spec["item_id"] == "S56-M-0158-VALIDATION"
assert spec["theorem_id"] == "THM-M-0158"
assert statement_record["canonical_formal_target"]["statement_file_sha256"] == sha256(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

lean_source = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean")
)
for pattern in (
    r"\b(?:sorry|admit)\b",
    r"^[ \t]*axiom\b",
    r"^[ \t]*unsafe\b",
    r"\bimplemented_by\b",
):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern

mathlib_entry = next(package for package in manifest["packages"] if package["name"] == "mathlib")
assert mathlib_entry["rev"] == EXPECTED_MATHLIB
assert mathlib_entry["inputRev"] == EXPECTED_MATHLIB
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0158-validation-", dir=LEAN_ROOT) as tmp_name:
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
        ["lake", "env", "lean", str(tmp / "Proof.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )

assert printed_axioms(obligation_output, "root_of_derivation_package") == EXPECTED_AXIOMS
assert printed_axioms(proof_output, "weingartenEquations") == EXPECTED_AXIOMS
assert "theorem weingartenEquations : WeingartenEquationsTarget" in lean_source
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert graphs["closure_boundary"]["minimal_open_root_cut"] == ["M0158-T-RECONSTRUCT"]

print("ok: exact statement, conditional composition, and direct proof elaborated in a fresh temporary module directory")
print("ok: checked declarations report exactly propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, statement/registry hashes, and clean pinned mathlib checks passed")
print("stale: frozen graph predates Proof.lean and still reports M0158-T-RECONSTRUCT open")
print("blocked: cold hermetic replay, complete TCB/SBOM closure, H0/R0 review, and distinct-runner independent verification")
