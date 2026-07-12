#!/usr/bin/env python3
"""Fail-closed local validator for S56-M-0652-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0652"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def run(argv: list[str], *, cwd: Path = ROOT,
        env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode != 0:
        fail(f"recipe exited {result.returncode}: {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
if spec.get("item_id") != "S56-M-0652-VALIDATION":
    fail("validation specification item identity mismatch")
if registry.get("root_obligation_id") != "M0652-ROOT":
    fail("registry root identity mismatch")
if registry.get("denominator_sha256") != graphs.get("registry_denominator_sha256"):
    fail("registry and typed-graph denominator mismatch")
if registry.get("frozen_against_statement_sha256") != digest(HERE / "Statement.lean"):
    fail("registry is stale against Statement.lean")

expected_hashes = {
    "Statement.lean": "0688e793479810070b0d7afe2b93ffa85bb132e80f4c79840532ae5add69d793",
    "ObligationTree.lean": "b930f451c31f1d5bf54da6dd149efaa3b5255ee2396671670056d7d18e233d74",
    "Proof.lean": "d2d3d50130fc9960c0c1068b501ccb8427868959aec5c964e712b53ca31261a7",
    "Validation.lean": "ef3235d99f1aca9954abe271cfec2a9d1b58e009ff2d2fca346f09253a82f9fd",
    "validation-spec.json": "6b3e35b5b8a8846aa9b28c735b6d13dddbbd7bd8fa2b28073299bdb6ed1ecbbd",
    "obligation-registry.json": "7b47fa834b29d099e2a36c23e28146b84022c7340d9b7f15eac3cba40cdb0b9f",
    "typed-graphs.json": "f69923218cd402f0e9c03fd4f335aa02226e12d89b2bfca7104d7d8a6aba23e4",
    "check_obligation_tree.py": "809726f3a0c84ada2fccd50bcacb75c558bcaebc1b7d27db4863570dbb4b4f48",
}
for name, expected in expected_hashes.items():
    actual = digest(HERE / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")

pins = {
    LEAN_ROOT / "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    LEAN_ROOT / "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
for path, expected in pins.items():
    if digest(path) != expected:
        fail(f"dependency pin changed: {path.name}")
if not MATHLIB.resolve().is_dir():
    fail("pinned mathlib checkout is missing")
if run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() != \
        "8a178386ffc0f5fef0b77738bb5449d50efeea95":
    fail("mathlib revision differs from the pin")
if run(["git", "status", "--short"], cwd=MATHLIB):
    fail("mathlib checkout is dirty")

tree_output = run(["python3", str(HERE / "check_obligation_tree.py")])
if "root closure: open (M3)" not in tree_output:
    fail("obligation validator did not preserve the open M3 root")

block_comment = re.compile(r"/-.*?-/", re.DOTALL)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = block_comment.sub("", (HERE / name).read_text(encoding="utf-8"))
    source = "\n".join(line.split("--", 1)[0] for line in source.splitlines())
    if prohibited.search(source):
        fail(f"prohibited local token in {name}")

outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0652-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"),
         str(tmp / "Statement.lean")], cwd=LEAN_ROOT)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["ObligationTree.lean"] = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"),
         str(tmp / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env
    )
    for name in ("Proof.lean", "Validation.lean"):
        outputs[name] = run(["lake", "env", "lean", str(tmp / name)],
                            cwd=LEAN_ROOT, env=env)

checks = {
    "ObligationTree.lean": ("statement_of_calculus_packages",),
    "Proof.lean": (
        "interpolation_of_antecedent_vocabulary",
        "interpolation_of_consequent_vocabulary",
    ),
    "Validation.lean": (
        "independent_antecedent_boundary",
        "independent_consequent_boundary",
    ),
}
for name, declarations in checks.items():
    output = outputs[name]
    if "sorryAx" in output:
        fail(f"Lean reported sorryAx for {name}")
    for declaration in declarations:
        if declaration not in output:
            fail(f"missing axiom report for {declaration}")

if "Quot.sound" not in outputs["ObligationTree.lean"]:
    fail("conditional composition trust report omitted Quot.sound")
if "Quot.sound" not in outputs["Proof.lean"]:
    fail("boundary proof trust report omitted Quot.sound")
if "Quot.sound" not in outputs["Validation.lean"]:
    fail("independent boundary trust report omitted Quot.sound")

root_body = re.compile(r"\b(?:theorem|def)\s+\w+[^\n]*:\s*Statement(?:\.|\s|:=)")
if root_body.search((HERE / "Proof.lean").read_text(encoding="utf-8")):
    fail("Proof.lean unexpectedly asserts an unconditional Statement root")

print("ok: frozen statement, conditional composition, and boundary proofs re-elaborated")
print("ok: independent boundary reconstruction passed without importing Proof or ObligationTree")
print("ok: hashes, pins, clean mathlib, placeholders, trust output, and open graph passed")
print("blocked: general Craig interpolation root remains M3; cold hermetic and distinct-runner gates remain open")
