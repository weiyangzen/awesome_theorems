#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-1270-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1270"
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
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-1270-VALIDATION"
assert spec["theorem_id"] == "THM-M-1270"
assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "statement.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

lean_source = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
for pattern in (r"\b(?:sorry|admit)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m1270-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs = []
    for name in ("Statement", "ObligationTree", "Proof"):
        outputs.append(
            run(
                ["lake", "env", "lean", "-o", str(tmp / f"{name}.olean"), str(tmp / f"{name}.lean")],
                cwd=LEAN_ROOT,
                env=env,
            )
        )
    outputs.append(
        run(["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env)
    )

combined_output = "\n".join(outputs)
for declaration in (
    "root_compose",
    "target_of_maximalPoint",
    "proofTarget_iff_frozen",
    "independentlyStrictOfMaximal",
):
    assert declaration in combined_output
allowed_axioms = {"propext", "Classical.choice", "Quot.sound"}
axiom_reports = re.findall(r"depends on axioms: \[([^]]*)\]", combined_output, re.DOTALL)
assert axiom_reports
for report in axiom_reports:
    observed = {name.strip() for name in report.replace("\n", " ").split(",")}
    assert observed == allowed_axioms, observed
assert "sorryAx" not in combined_output

boundary = graphs["closure_boundary"]
assert boundary["root_closed"] is False
assert boundary["root_machine_debt"] == "M3"
assert boundary["theorem_complete"] is False
for obligation in ("M1270-C-SEQUENCE", "M1270-L-CAUCHY", "M1270-L-LIMIT"):
    assert obligation in boundary["remaining_root_cut_set"]
assert "hardCore :" in (HERE / "Proof.lean").read_text()

print("ok: statement, obligation composition, partial proof bodies, and independent probe elaborated in a fresh temporary module directory")
print("ok: exact ProofTarget-to-frozen-target bridge checked definitionally")
print("ok: observed axiom output contains only the expected propext, Classical.choice, and Quot.sound set")
print("ok: placeholder scan, frozen hashes, registry denominator, and clean pinned mathlib checks passed")
print("open: exact root remains conditional on construction of a descent-maximal point; frozen machine debt is M3")
print("blocked: cold hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
