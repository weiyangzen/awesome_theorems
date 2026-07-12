#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1289-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1289"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


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
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = load("validation-spec.json")
statement = load("statement.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof = load("proof.json")

assert spec["item_id"] == "S56-M-1289-VALIDATION"
assert spec["theorem_id"] == "THM-M-1289"
assert spec["network_policy"] == "denied"
assert spec["argv"] == ["python3", "Stage1_Instances/THM-M-1289/check_validation.py"]
assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof["theorem_proved"] is False
assert proof["theorem_complete"] is False
assert set(proof["remaining_component_premises"]) == {
    "PDEComponent", "FunctionNormComponent", "GradientNormComponent", "ExtremalComponent"
}

lean_names = ("Statement.lean", "ObligationTree.lean", "Proof.lean")
source = "\n".join((HERE / name).read_text(encoding="utf-8") for name in lean_names)
source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
assert prohibited.search(source) is None, "prohibited proof mechanism in checked Lean sources"

assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifact missing"
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""
assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = TOOLCHAIN
with tempfile.TemporaryDirectory(prefix="m1289-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in lean_names:
        (tmp / name).write_bytes((HERE / name).read_bytes())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
    local_env = env.copy()
    local_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs: dict[str, str] = {}
    for name in ("Statement.lean", "ObligationTree.lean"):
        outputs[name] = run(
            ["lake", "env", "lean", "-o", str(tmp / name.replace(".lean", ".olean")), str(tmp / name)],
            cwd=LEAN_ROOT,
            env=local_env,
        )
    outputs["Proof.lean"] = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=local_env
    )

expected = {
    "ObligationTree.lean": ("aubinTalentiTarget_of_components",),
    "Proof.lean": ("bubble_pos", "contDiff_bubble", "aubinTalentiTarget_of_remaining_components"),
}
for filename, declarations in expected.items():
    output = outputs[filename]
    for declaration in declarations:
        match = re.search(
            rf"'[^']*{re.escape(declaration)}' depends on axioms: \[(.*?)\]",
            output,
            re.DOTALL,
        )
        assert match is not None, (filename, declaration, output)
        observed = {item.strip() for item in match.group(1).replace("\n", "").split(",")}
        assert observed == ALLOWED_AXIOMS, (declaration, observed)
    assert "sorryAx" not in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert set(closure["remaining_root_cut_set"]) == {
    "M1289-L-POS", "M1289-L-SMOOTH", "M1289-L-PDE",
    "M1289-L-FUN-NORM", "M1289-L-GRAD-NORM", "M1289-T-EXTREMAL",
}

print("ok: exact statement, frozen conditional composition, positivity, and smoothness kernel-replayed")
print("ok: checked declarations report only propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, frozen hashes, denominator, toolchain pins, and clean mathlib passed")
print("open: exact root retains PDE, function-norm, gradient-norm, and sharp-extremal premises")
print("stale: frozen graph predates proof and still lists positivity and smoothness in its cut set")
print("blocked: cold empty-cache hermetic replay and distinct-runner independent verification")
