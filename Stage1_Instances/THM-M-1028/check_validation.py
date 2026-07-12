#!/usr/bin/env python3
"""Fail-closed kernel and evidence validation for THM-M-1028's open root."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-1028"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def load(name: str) -> dict:
    with (OWNED / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


statement = load("statement.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
instance = load("instance.json")
spec = load("validation-phase-spec.json")

if spec.get("item_id") != "S56-M-1028-VALIDATION" or spec.get("theorem_id") != "THM-M-1028":
    fail("validation recipe identity mismatch")
if statement.get("canonical_formal_target", {}).get("declaration_or_expression") != \
        "AwesomeTheorems.Stage1.THM_M_1028.Statement":
    fail("canonical target mismatch")
if sha256(OWNED / "Statement.lean") != statement["canonical_formal_target"]["statement_file_sha256"]:
    fail("statement source changed after freeze")
if registry.get("root_obligation_id") != "M1028-ROOT":
    fail("root obligation mismatch")
if instance.get("theorem_complete") is not False or graphs["closure_boundary"]["root_closed"] is not False:
    fail("open Wiener root is falsely marked closed")

obligations = {row["obligation_id"]: row for row in registry["obligations"]}
if len(obligations) != 16:
    fail("frozen obligation denominator changed")
for required_open in ("M1028-C-CONTINUOUS-MODIFICATION", "M1028-T-NONDIFFERENTIABLE"):
    node = next(item for item in graphs["nodes"] if item["obligation_id"] == required_open)
    if node.get("machine_debt") != "M4":
        fail(f"substantive package no longer has the expected open status: {required_open}")

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (OWNED / name).read_text(encoding="utf-8")
    code = "\n".join(line for line in source.splitlines()
                     if not line.lstrip().startswith(("--", "/-", "*")))
    if prohibited.search(code):
        fail(f"prohibited placeholder or trust declaration in {name}")

manifest = load("anchor-audit.json")["immutable_environment"]
if manifest["mathlib_revision"] != "8a178386ffc0f5fef0b77738bb5449d50efeea95":
    fail("unexpected pinned mathlib revision")
if sha256(LEAN_ROOT / "lean-toolchain") != \
        statement["environment_fingerprint"]["lean_toolchain_file_sha256"]:
    fail("Lean toolchain pin changed")
if sha256(LEAN_ROOT / "lake-manifest.json") != \
        statement["environment_fingerprint"]["lake_manifest_sha256"]:
    fail("Lake manifest pin changed")

env_probe = subprocess.run(
    ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT,
    capture_output=True, text=True, timeout=30)
if env_probe.returncode != 0:
    fail(f"cannot obtain pinned LEAN_PATH: {env_probe.stderr}")
dependency_path = env_probe.stdout.strip()
lean_probe = subprocess.run(
    ["lake", "env", "which", "lean"], cwd=LEAN_ROOT,
    capture_output=True, text=True, timeout=30)
if lean_probe.returncode != 0:
    fail(f"cannot locate pinned Lean executable: {lean_probe.stderr}")
lean_executable = lean_probe.stdout.strip()

outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="thm-m-1028-validation-") as temporary:
    tmp = Path(temporary)
    recipes = (
        ("Statement.lean", ["-o", str(tmp / "Statement.olean")], dependency_path),
        ("ObligationTree.lean", ["-o", str(tmp / "ObligationTree.olean")], f"{tmp}:{dependency_path}"),
        ("Proof.lean", [], f"{tmp}:{dependency_path}"),
        ("Validation.lean", [], f"{tmp}:{dependency_path}"),
    )
    for name, extra, lean_path in recipes:
        env = os.environ.copy()
        env["LEAN_PATH"] = lean_path
        command = [lean_executable, *extra, name]
        result = subprocess.run(command, cwd=OWNED, env=env,
                                capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
        if result.returncode != 0:
            fail(f"kernel recipe exited {result.returncode} for {name}:\n{output}")
        if "sorryAx" in output:
            fail(f"kernel axiom report contains sorryAx for {name}")
        outputs[name] = output

for name in ("ObligationTree.lean", "Proof.lean", "Validation.lean"):
    if not all(axiom in outputs[name] for axiom in ("propext", "Classical.choice", "Quot.sound")):
        fail(f"axiom report is outside the recorded classical mathlib profile for {name}")
if "statement_of_path_packages" not in outputs["Proof.lean"]:
    fail("proof declaration was not reached by kernel replay")
if "independent_statement_of_packages" not in outputs["Validation.lean"]:
    fail("independent validation declaration was not reached")

print("validation ok: exact conditional composition kernel-replayed; independent probe passed; root remains open (M2)")
