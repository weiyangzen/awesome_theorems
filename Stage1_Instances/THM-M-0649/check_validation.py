#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0649-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0649"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'(?:Stage1\.THM_M_0649(?:\.Validation)?\.)?{re.escape(declaration)}' "
        r"depends on axioms:\s*\[(.*?)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}\n{output}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


spec = json.loads((HERE / "validation-phase-spec.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

assert spec["item_id"] == receipt["item_id"] == "S56-M-0649-VALIDATION"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-0649"
assert len({recipe["recipe_id"] for recipe in spec["recipes"]}) == len(spec["recipes"])
for recipe in spec["recipes"]:
    assert isinstance(recipe["argv"], list)
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
for name, expected in receipt["inputs"].items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b|\bimplemented_by\b",
    re.MULTILINE,
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited mechanism in {name}"

mathlib_entry = next(package for package in manifest["packages"] if package["name"] == "mathlib")
assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == EXPECTED_MATHLIB
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB
assert run(["git", "status", "--short"], cwd=mathlib) == ""

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
env = os.environ.copy()
env.update({"ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0649-validation-") as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    env["LEAN_PATH"] = lean_path
    outputs["Statement.lean"] = run(
        [lean, "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=tmp, env=env
    )
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["ObligationTree.lean"] = run(
        [lean, "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")], cwd=tmp, env=env
    )
    outputs["Proof.lean"] = run(
        [lean, "-o", str(tmp / "Proof.olean"), str(tmp / "Proof.lean")], cwd=tmp, env=env
    )
    outputs["Validation.lean"] = run([lean, str(tmp / "Validation.lean")], cwd=tmp, env=env)

assert printed_axioms(outputs["Proof.lean"], "elementaryChainTarget") == EXPECTED_AXIOMS
assert printed_axioms(outputs["Validation.lean"], "exactRootTypeCheck") == EXPECTED_AXIOMS
assert "sorryAx" not in outputs["Proof.lean"] + outputs["Validation.lean"]

# The frozen graph predates Proof.lean. Validation records that staleness rather than rewriting it.
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M0649-T-TV"]
assert receipt["root_decision"]["kernel_closed_in_worker"] is True
assert receipt["root_decision"]["theorem_complete"] is False

print("ok: exact root and independent exact-type wrapper kernel-elaborated from fresh temporary modules")
print("ok: both roots report exactly propext, Classical.choice, and Quot.sound")
print("ok: input hashes, placeholder hygiene, manifest pin, and clean pinned mathlib passed")
print("stale: frozen obligation graph predates Proof.lean and still reports M0649-T-TV open")
print("blocked: cold empty-cache replay, full TCB/SBOM, H0/R0, and distinct-runner verification")
