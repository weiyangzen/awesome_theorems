#!/usr/bin/env python3
"""Fail-closed node validation for S56-M-0416-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0416"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
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
        fail(f"recipe exited {result.returncode}: {argv!r}\n{result.stdout}")
    return result.stdout


statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
spec = json.loads((HERE / "validation-spec.json").read_text(encoding="utf-8"))

if spec.get("item_id") != "S56-M-0416-VALIDATION":
    fail("validation specification item identity mismatch")
if statement.get("theorem_id") != "THM-M-0416":
    fail("statement theorem identity mismatch")
if registry.get("root_obligation_id") != "M0416-ROOT":
    fail("registry root mismatch")
if registry.get("frozen_against_statement_sha256") != digest(HERE / "Statement.lean"):
    fail("registry is stale against Statement.lean")
if graphs.get("registry_denominator_sha256") != registry.get("denominator_sha256"):
    fail("typed graph denominator mismatch")
if proof_receipt.get("root_declaration") != \
        "Stage1Instances.THM_M_0416.Proof.dirichletUnitTheorem":
    fail("proof receipt root declaration mismatch")
if proof_receipt.get("machine_root_cut_set") != []:
    fail("proof receipt does not claim exact machine root closure")

expected_hashes = {
    "Statement.lean": "0d98e8292f77f134f3dc501cc671d93f9ca9915e7abbbf6721aa31c891000f4d",
    "ObligationTree.lean": "b30f5061822e796adefc100afcfb6ec13fe918a02509e270e42a2a39383915d0",
    "Proof.lean": "cbc77f0c690cc6aea8fd7bcc11e2bfb5bbb6d5fb8a8d2ceaa2bdbdc4822e09a0",
    "obligation-registry.json": "5c8bdb97fc222a201b7b940a20dfde39bcfdae488b3f2598638ebaaebf27db95",
    "typed-graphs.json": "f0ae41c76b14fcafb48fe3228b84c4750a0f940c1e97907e1446b9c5e4805df9",
    "proof-receipt.json": "26bf8054c90f2fec0cab2fe61bca3823af04929268bbebcefbe98e99a258612c",
}
for name, expected in expected_hashes.items():
    actual = digest(HERE / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")

source = "\n".join(
    (HERE / name).read_text(encoding="utf-8")
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(r"\b(?:sorry|admit)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
if prohibited.search(source):
    fail("local Lean source contains a prohibited placeholder or trust declaration")

if not MATHLIB.resolve().is_dir():
    fail("pinned mathlib checkout is missing")
if run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() != MATHLIB_REVISION:
    fail("mathlib revision differs from the pin")
if run(["git", "status", "--short"], cwd=MATHLIB):
    fail("mathlib checkout is dirty")
if digest(LEAN_ROOT / "lean-toolchain") != \
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2":
    fail("Lean toolchain pin changed")
if digest(LEAN_ROOT / "lake-manifest.json") != \
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81":
    fail("Lake manifest changed")

upstream = MATHLIB / "Mathlib/NumberTheory/NumberField/Units/DirichletTheorem.lean"
if digest(upstream) != "c4eb26b3512ed3d73f35cf41b62b519ed7fccd2d496220280f8c5a34d25e5500":
    fail("pinned terminal source digest changed")
upstream_text = upstream.read_text(encoding="utf-8")
for fragment in (
    "instance : Module.Free ℤ (Additive (",
    "instance : Module.Finite ℤ (Additive (",
    "theorem rank_modTorsion :",
    "theorem exist_unique_eq_mul_prod (x :",
):
    if fragment not in upstream_text:
        fail(f"terminal source declaration not found: {fragment}")

with tempfile.TemporaryDirectory(prefix="m0416-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    independent_output = run(["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env)

for declaration, output in (
    ("root_of_packages", obligation_output),
    ("dirichletUnitTheorem", proof_output),
    ("independentDirichletUnitTheorem", independent_output),
):
    if declaration not in output or "depends on axioms" not in output:
        fail(f"missing axiom report for {declaration}")
    for axiom in ("propext", "Classical.choice", "Quot.sound"):
        if axiom not in output:
            fail(f"{declaration} axiom report omits {axiom}")
    if "sorryAx" in output:
        fail(f"{declaration} transitively depends on sorryAx")

print("ok: exact root and independent reconstruction elaborate in a fresh temporary module directory")
print("ok: composition, proof root, and independent root report only propext, Classical.choice, and Quot.sound")
print("ok: frozen hashes, placeholder scan, clean pinned mathlib, and terminal source provenance checks passed")
print("blocked: release-grade cold hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
