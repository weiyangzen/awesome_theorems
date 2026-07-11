#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0183-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0183"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode:
        raise SystemExit(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-0183-VALIDATION"
assert spec["theorem_id"] == "THM-M-0183"
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert statement["canonical_formal_target"]["declaration_or_expression"] == (
    "Stage1Instances.THMM0183.YauCalabiConjectureTarget"
)

source = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean")
)
for pattern in (r"\b(?:sorry|admit)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, source, re.MULTILINE) is None, pattern

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir(), "pinned mathlib artifact is missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert run(["git", "status", "--short"], cwd=mathlib) == ""
assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)

with tempfile.TemporaryDirectory(prefix="m0183-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "Proof.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"),
         str(tmp / "Statement.lean")], cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")],
        cwd=LEAN_ROOT, env=env,
    )

expected = (
    "'Stage1Instances.THMM0183.not_yauCalabiConjectureTarget' "
    "depends on axioms: [propext, Classical.choice, Quot.sound]"
)
assert expected in output, "countermodel axiom report changed"
closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert "M0183-T-METRIC" in closure["remaining_root_cut_set"]

print("ok: exact frozen target and checked countermodel elaborated in a fresh temporary module directory")
print("ok: countermodel reports only propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, source hashes, registry denominator, and clean pinned mathlib checks passed")
print("blocked: the exact positive target is refuted by the empty metric-interface countermodel")
print("blocked: cold hermetic replay, full TCB/SBOM closure, and distinct-runner independent verification")
