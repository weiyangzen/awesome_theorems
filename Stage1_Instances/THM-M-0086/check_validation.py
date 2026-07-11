#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0086-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0086"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
MATHLIB_PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"

EXPECTED_HASHES = {
    "Statement.lean": "98e2fce9832b23421c3084e1e7d3dfa84f1465fd700ab66a5eacf386b7c626f1",
    "ObligationTree.lean": "d949d44c5a011b0ad00a1dee413ecca466af1dea4e679424f70c00b875d15587",
    "Proof.lean": "897b7480d54dbb19c3a53734199f4d67cee50b726ee3772b9c229894489b22d7",
    "statement.json": "c356d97260baf57c665b46c1c260709b6322f4036821e5f7b3753a55b8b785a5",
    "anchor-audit.json": "1464cdd3bb625affb6a6d7530816975e0e125e9162abf6ca9536bc1aa78e67a3",
    "obligation-registry.json": "af09f8198e3ad5dd51c9d35eef14f42a451a4e8cbd33a0360946aeb1da259190",
    "typed-graphs.json": "e8ccefbd630d98d221d27e7260ddb2515fa7087dfc823473b8b4a2c38ef931f5",
    "validation-specs.json": "7e7de312131add8c5eb0192bb61d1df07700d7b57788ba14da56fd93fe5ab0bd",
}
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
UPSTREAM = {
    "Mathlib/CategoryTheory/Abelian/FreydMitchell.lean":
        "5eaa8e43e2116becda23df95559944990d7ff0b8411c8c517e96e0d54a494c79",
    "Mathlib/CategoryTheory/Generator/Abelian.lean":
        "e2952ea887763387582fd966bcaa7890973b527717726e02bfae4aafd3204443",
}


def digest(path: Path) -> str:
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


for name, expected in EXPECTED_HASHES.items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert digest(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert digest(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

anchor = load("anchor-audit.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
assert anchor["immutable_environment"]["mathlib_revision"] == MATHLIB_PIN
assert registry["root_obligation_id"] == "M0086-ROOT"
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
assert {row["obligation_id"] for row in registry["obligations"]} == {
    row["obligation_id"] for row in graphs["nodes"]
}

assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == MATHLIB_PIN
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""
for relative, expected in UPSTREAM.items():
    assert digest(MATHLIB / relative) == expected, f"upstream source changed: {relative}"

upstream_text = "\n".join((MATHLIB / relative).read_text() for relative in UPSTREAM)
for needle in (
    "theorem freyd_mitchell (C : Type u)",
    "theorem has_injective_coseparator [HasLimits C] [EnoughInjectives C]",
    "theorem has_projective_separator [HasColimits C] [EnoughProjectives C]",
):
    assert needle in upstream_text, f"terminal declaration missing: {needle}"

source = "\n".join(
    (HERE / name).read_text(encoding="utf-8")
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
code = "\n".join(
    line for line in source.splitlines()
    if not line.lstrip().startswith(("--", "/-", "*", "-/"))
)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
assert prohibited.search(code) is None

# Re-elaborate copied sources in a fresh target-local build directory. The shared pinned
# dependency cache is read but never built or modified.
with tempfile.TemporaryDirectory(prefix="m0086-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    module_dir = tmp / "THM-M-0086"
    module_dir.mkdir()
    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        (module_dir / name).write_bytes((HERE / name).read_bytes())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["ELAN_TOOLCHAIN"] = "leanprover/lean4:v4.29.0"
    env["LEAN_PATH"] = lean_path
    statement_output = run(
        ["lake", "env", "lean", "-o", str(module_dir / "Statement.olean"),
         str(module_dir / "Statement.lean")], cwd=LEAN_ROOT, env=env,
    )
    env["LEAN_PATH"] = f"{module_dir}:{lean_path}"
    proof_output = run(
        ["lake", "env", "lean", str(module_dir / "Proof.lean")], cwd=LEAN_ROOT, env=env,
    )
    validation_output = run(
        ["lake", "env", "lean", str(module_dir / "Validation.lean")], cwd=LEAN_ROOT, env=env,
    )

assert "CanonicalStatement" in statement_output
for declaration, output in (
    ("freydTheoremPackage", proof_output),
    ("independentFreydTheoremPackage", validation_output),
):
    assert declaration in output
    assert all(axiom in output for axiom in ("propext", "Classical.choice", "Quot.sound"))
    assert "sorryAx" not in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == [
    "M0086-L-EMBED", "M0086-L-INJECTIVE", "M0086-L-PROJECTIVE"
]

print("ok: exact statement and proof elaborate in a fresh temporary target directory")
print("ok: independent exact-root reconstruction elaborates without importing Proof")
print("ok: hashes, placeholder hygiene, registry, dependency pin, source provenance, and mathlib cleanliness passed")
print("observed axioms: propext, Classical.choice, Quot.sound")
print("stale: frozen graph predates Proof.lean and still reports three proof leaves open")
print("blocked: cold hermetic replay, complete TCB/SBOM, H0/R0, master reconciliation, and distinct-runner verification")
