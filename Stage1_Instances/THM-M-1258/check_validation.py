#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-1258-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1258"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None) -> str:
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


spec = json.loads((HERE / "validation-spec.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
assert spec["item_id"] == "S56-M-1258-VALIDATION"
assert spec["theorem_id"] == "THM-M-1258"
assert spec["network_policy"] == "denied"
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

lean_names = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
lean_source = "\n".join((HERE / name).read_text() for name in lean_names)
for pattern in (r"\b(?:sorry|admit|sorryAx)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""

env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = TOOLCHAIN
with tempfile.TemporaryDirectory(prefix="m1258-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in lean_names:
        (tmp / name).write_bytes((HERE / name).read_bytes())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
    local_env = env.copy()
    local_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs = {}
    for name in lean_names:
        argv = ["lake", "env", "lean"]
        if name != "Validation.lean":
            argv += ["-o", str(tmp / name.replace(".lean", ".olean"))]
        argv.append(str(tmp / name))
        outputs[name] = run(argv, cwd=LEAN_ROOT, env=local_env)

expected = {
    "ObligationTree.lean": ("compose_condition", "empty_domain", "zero_dimension"),
    "Proof.lean": ("of_pointwise_span", "coordinateFields_hormanderCondition"),
    "Validation.lean": ("independentlyReconstructed_coordinateCondition",),
}
allowed_axioms = {"propext", "Classical.choice", "Quot.sound"}
for filename, declarations in expected.items():
    output = outputs[filename]
    for declaration in declarations:
        match = re.search(
            rf"'[^']*{re.escape(declaration)}' depends on axioms: \[(.*?)\]",
            output,
            re.DOTALL,
        )
        assert match is not None, (filename, declaration, output)
        seen = {item.strip() for item in match.group(1).replace("\n", "").split(",")}
        assert seen == allowed_axioms, (declaration, seen)
    assert "sorryAx" not in output

assert "import Proof" not in (HERE / "Validation.lean").read_text()
assert "GeneratedBracket.square" in (HERE / "Validation.lean").read_text()
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert "M1258-L-SPAN" in graphs["root_cut_set"]

print("ok: exact statement, composition harness, proof, and independent local reconstruction elaborated")
print("ok: checked declarations report only propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, frozen hashes, denominator, and clean pinned mathlib checks passed")
print("open: authoritative graph predates proof and reports root_closed=false with M1258-L-SPAN cut")
print("blocked: cold empty-cache hermetic replay and distinct-runner independent verification")
