#!/usr/bin/env python3
"""Fail-closed local validator for S56-M-1268-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1268"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(argv)}\n{result.stdout}")
    return result.stdout


spec = load("validation-spec.json")
statement = load("statement.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
assert spec["item_id"] == "S56-M-1268-VALIDATION"
assert spec["theorem_id"] == "THM-M-1268"
assert spec["network_policy"] == "denied"
assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

lean_names = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "ProofExact.lean", "Validation.lean")
source = "\n".join((HERE / name).read_text(encoding="utf-8") for name in lean_names)
code = "\n".join(
    line for line in source.splitlines()
    if not line.lstrip().startswith(("--", "/-", "*", "-/"))
)
prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
assert prohibited.search(code) is None
assert "import Proof" not in (HERE / "Validation.lean").read_text(encoding="utf-8")

assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""
assert sha256(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert sha256(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
assert sha256(MATHLIB / "Mathlib/Analysis/LocallyConvex/WeakSpace.lean") == "672356ee3118ce01af81cb09e6b78a9aa93389ff71b47b666e38a354cc51ac92"
assert sha256(MATHLIB / "Mathlib/Topology/Semicontinuity/Basic.lean") == "c60b70b03f2ca3bbc364d0d10e42d45fca727d40236311a70927760203f7aa98"

env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = TOOLCHAIN
with tempfile.TemporaryDirectory(prefix="m1268-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in lean_names:
        (tmp / name).write_bytes((HERE / name).read_bytes())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
    local_env = env.copy()
    local_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs: dict[str, str] = {}
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        outputs[name] = run(
            ["lake", "env", "lean", "-o", str(tmp / name.replace(".lean", ".olean")), str(tmp / name)],
            cwd=LEAN_ROOT, env=local_env,
        )
    for name in ("ProofExact.lean", "Validation.lean"):
        outputs[name] = run(["lake", "env", "lean", str(tmp / name)], cwd=LEAN_ROOT, env=local_env)

expected = {
    "Proof.lean": ("convexSublevelBridge", "weakClosed_of_convex_normClosed", "weakToNormBridge", "weakLowerSemicontinuity"),
    "ProofExact.lean": ("weakLowerSemicontinuity",),
    "Validation.lean": ("convex_sublevel", "convex_closed_is_weak_closed", "independentlyReconstructedWeakLowerSemicontinuity"),
}
allowed_axioms = {"propext", "Classical.choice", "Quot.sound"}
for filename, declarations in expected.items():
    for declaration in declarations:
        match = re.search(rf"'[^']*{re.escape(declaration)}' depends on axioms: \[(.*?)\]", outputs[filename], re.DOTALL)
        assert match is not None, (filename, declaration, outputs[filename])
        seen = {item.strip() for item in match.group(1).replace("\n", "").split(",")}
        assert seen == allowed_axioms, (declaration, seen)
    assert "sorryAx" not in outputs[filename]

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert set(closure["remaining_root_cut_set"]) == {
    "M1268-L-CONVEX-SUBLEVEL", "M1268-L-WEAK-CLOSURE", "M1268-T-WEAK-TO-NORM"
}

print("ok: exact statement, frozen composition, proof, exact wrapper, and independent reconstruction elaborated")
print("ok: checked declarations report only propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, source bindings, denominator, dependency pins, and mathlib cleanliness passed")
print("stale: authoritative frozen graph predates proof and still reports the three proof bridges open")
print("blocked: cold empty-cache hermetic replay and distinct-runner independent verification")
