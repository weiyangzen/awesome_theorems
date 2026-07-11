#!/usr/bin/env python3
"""Fail-closed worker validator for S56-M-0085-VALIDATION."""

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0085"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


expected_hashes = {
    "Statement.lean": "54d3f1f5cd7e2380b158f64ba4d20c17296127b0da2e3c6b3c41908ccf8d8622",
    "Proof.lean": "a4dc2b5543a530b78d2bc95d11ae0e9375b82554d6bc5f3c06c614343b22e205",
    "Validation.lean": "a9f88e2cc99a5999e07455cbe9a301618e01fa9e26d5b5186d728debdaa67639",
    "statement.json": "6ae8405f98b638997b33aa5c44d1bbc34f0d6b65bf87666edc7e28438485cd21",
    "anchor-audit.json": "1b38f729be04c45c1515e256d73fe66c684e615d69553b14ef8d35beebfdf18a",
    "obligation-registry.json": "9bada45d7d79c345ff3992d077f3cbf853c5e3df440ffa745bd4fc91cb6b03c6",
    "typed-graphs.json": "1b8da39b8e596aa13f042fe5c5fa959b22e96c18a35c03123e9729e2c1066436",
    "validation-specs.json": "5381e3bed0ff40b4a0796fc82467f083b7c607c596aa37b33336764d74f2c678",
}
for name, expected in expected_hashes.items():
    actual = digest(OWNED / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")

if digest(LEAN_ROOT / "lean-toolchain") != \
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2":
    fail("Lean toolchain pin changed")
if digest(LEAN_ROOT / "lake-manifest.json") != \
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81":
    fail("Lake manifest pin changed")

anchor = json.loads((OWNED / "anchor-audit.json").read_text())
registry = json.loads((OWNED / "obligation-registry.json").read_text())
graphs = json.loads((OWNED / "typed-graphs.json").read_text())
if anchor["immutable_environment"]["mathlib_revision"] != \
        "8a178386ffc0f5fef0b77738bb5449d50efeea95":
    fail("anchor mathlib revision changed")
ids = {row["obligation_id"] for row in registry["obligations"]}
if registry["root_obligation_id"] != "M0085-ROOT" or \
        ids != {row["obligation_id"] for row in graphs["nodes"]}:
    fail("frozen registry and typed graph disagree")
if registry["obligations"][2]["terminal_proof_body_id"] != \
        "mathlib:Mathlib.CategoryTheory.Monad.Monadicity#CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers":
    fail("terminal proof-body provenance changed")

prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    source = (OWNED / name).read_text()
    code = "\n".join(line for line in source.splitlines()
                     if not line.lstrip().startswith(("--", "/-", "*")))
    if prohibited.search(code):
        fail(f"prohibited placeholder or trust declaration in {name}")

lake_env = subprocess.run(
    ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT,
    capture_output=True, text=True, timeout=30, check=True)
dependency_path = lake_env.stdout.strip()
env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = "leanprover/lean4:v4.29.0"
outputs = []
commands = (
    (["lake", "env", "lean", "-o", "Statement.olean", "Statement.lean"], dependency_path),
    (["lake", "env", "lean", "Proof.lean"], f".:{dependency_path}"),
    (["lake", "env", "lean", "Validation.lean"], f".:{dependency_path}"),
)
try:
    for argv, lean_path in commands:
        env["LEAN_PATH"] = lean_path
        run = subprocess.run(argv, cwd=OWNED, env=env, capture_output=True,
                             text=True, timeout=120)
        output = run.stdout + run.stderr
        if run.returncode != 0:
            fail(f"kernel recipe exited {run.returncode}: {' '.join(argv)}\n{output}")
        if "sorryAx" in output:
            fail(f"kernel report contains sorryAx: {' '.join(argv)}")
        outputs.append(output)
finally:
    (OWNED / "Statement.olean").unlink(missing_ok=True)

for output in outputs[1:]:
    if not all(name in output for name in ("propext", "Classical.choice", "Quot.sound")):
        fail("expected trust closure was not reported")

print("validation ok: frozen inputs, provenance, placeholder hygiene, exact proof, and independent same-checkout probe passed; hermetic and distinct-runner gates remain open")
