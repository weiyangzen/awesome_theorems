#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-1288-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1288"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


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
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-phase-spec.json").read_text(encoding="utf-8"))
statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
anchor = json.loads((HERE / "anchor-audit.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))

assert spec["item_id"] == "S56-M-1288-VALIDATION"
assert spec["theorem_id"] == "THM-M-1288"
assert spec["network_policy"] == "denied"
assert spec["argv"] == [
    "python3",
    "Stage1_Instances/THM-M-1288/check_validation.py",
]
assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha256(
    HERE / "anchor-audit.json"
)
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert registry["root_obligation_id"] == "M1288-ROOT"

lean_names = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
lean_source = "\n".join((HERE / name).read_text(encoding="utf-8") for name in lean_names)
for pattern in (r"\b(?:sorry|admit|sorryAx)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern
validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
assert "import Proof" not in validation_source
assert "import ObligationTree" not in validation_source
assert "talentiSharpSobolevTarget_of_packages" not in validation_source

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""
assert anchor["immutable_environment"]["mathlib_revision"] == MATHLIB_REVISION
upstream = mathlib / "Mathlib" / "Analysis" / "FunctionalSpaces" / "SobolevInequality.lean"
assert upstream.is_file()
assert sha256(upstream) == anchor["immutable_environment"]["mathlib_module_sha256"]

env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = TOOLCHAIN
with tempfile.TemporaryDirectory(prefix="m1288-validation-", dir=LEAN_ROOT) as tmp_name:
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

for filename, declaration in (
    ("ObligationTree.lean", "talentiSharpSobolevTarget_of_packages"),
    ("Proof.lean", "talentiSharpSobolevTarget_of_open_analytic_packages"),
    ("Validation.lean", "independentlyComposeRoot"),
    ("Validation.lean", "independentlyCheckDomain"),
    ("Validation.lean", "independentlyCheckGradient"),
    ("Validation.lean", "independentlyCheckZeroLpNorm"),
):
    output = outputs[filename]
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms: \[(.*?)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, (filename, declaration, output)
    observed = {
        item.strip() for item in match.group(1).replace("\n", "").split(",") if item.strip()
    }
    assert observed <= ALLOWED_AXIOMS, (declaration, observed)
    assert "sorryAx" not in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["audit_complete"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == [
    "M1288-T-ADMISSIBILITY",
    "M1288-T-OPTIMALITY",
]

print("ok: exact statement, conditional composition, bounded proof leaves, and independent local probes elaborated")
print("ok: observed declaration axioms are confined to propext, Classical.choice, and Quot.sound")
print("ok: placeholder/unsafe scan, frozen hashes, denominator, and clean pinned mathlib provenance checks passed")
print("open: exact root remains M3 with admissibility and optimality packages unproved")
print("blocked: cold empty-cache hermetic replay, complete trust/SBOM closure, and distinct-runner independent verification")
