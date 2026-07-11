#!/usr/bin/env python3
"""Fail-closed node validation for S56-M-0418-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0418"
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

if spec.get("item_id") != "S56-M-0418-VALIDATION":
    fail("validation specification item identity mismatch")
if statement.get("theorem_id") != "THM-M-0418":
    fail("statement theorem identity mismatch")
if registry.get("root_obligation_id") != "M0418-ROOT":
    fail("registry root mismatch")
if registry.get("frozen_against_statement_sha256") != digest(HERE / "Statement.lean"):
    fail("registry is stale against Statement.lean")
if graphs.get("registry_denominator_sha256") != registry.get("denominator_sha256"):
    fail("typed graph denominator mismatch")
if proof_receipt.get("closed_obligation_ids") != [
    "M0418-ROOT", "M0418-T-ADAPTER", "M0418-T-UPSTREAM-BODY"
]:
    fail("proof receipt does not claim the exact machine root closure")

expected_hashes = {
    "Statement.lean": "84b8b52b8afc0b9b6ff4d6689815c230e99cffd2db2a57f8e4ac5bcc5daeaabc",
    "ObligationTree.lean": "247e6563e430a305d8bc7681650dcc860d71d898d684a9407c126269707be4a9",
    "Proof.lean": "84857a936c29627de8a6c3c79b1a4076b8595a610bbac2f4f244235f455e2b1d",
    "obligation-registry.json": "a24bce3a0c4b61ed36e0ca8bb05551b3ba20b5189c8558070166c883ed2cd8ce",
    "typed-graphs.json": "05d1f3df3f55f4f049e4a1c3ca17d8607272f0267125f6a47cd51f92bacb6db0",
    "proof-receipt.json": "beb3c6da6111fba947f8190106400d25ff92938189cfdd2f800257b7688916e5",
}
for name, expected in expected_hashes.items():
    actual = digest(HERE / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")

source = "\n".join(
    (HERE / name).read_text(encoding="utf-8")
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
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

upstream = MATHLIB / "Mathlib/NumberTheory/NumberField/ClassNumber.lean"
if digest(upstream) != "abe0ed06630f8104a02380912074d7eb1edc656969dea029c2b25ffdef7f6624":
    fail("pinned terminal source digest changed")
upstream_text = upstream.read_text(encoding="utf-8")
if "theorem exists_ideal_in_class_of_norm_le (C : ClassGroup (𝓞 K)) :" not in upstream_text:
    fail("terminal source declaration not found")

with tempfile.TemporaryDirectory(prefix="m0418-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", str(tmp / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env
    )
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    independent_output = run(["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env)

for declaration, output in (
    ("minkowskiIdealClassBound_obligationRoot", obligation_output),
    ("minkowskiIdealClassBound_proof", proof_output),
    ("independentMinkowskiIdealClassBound", independent_output),
):
    if declaration not in output or "depends on axioms" not in output:
        fail(f"missing axiom report for {declaration}")
    for axiom in ("propext", "Classical.choice", "Quot.sound"):
        if axiom not in output:
            fail(f"{declaration} axiom report omits {axiom}")
    if "sorryAx" in output:
        fail(f"{declaration} transitively depends on sorryAx")

print("ok: exact root and separate reconstruction elaborate in a fresh temporary module directory")
print("ok: composition, proof root, and separate root report only propext, Classical.choice, and Quot.sound")
print("ok: frozen hashes, placeholder scan, clean pinned mathlib, and terminal source provenance checks passed")
print("blocked: release-grade cold hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
