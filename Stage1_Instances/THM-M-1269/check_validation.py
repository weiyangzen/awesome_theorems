#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-1269-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1269"
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
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text(encoding="utf-8"))
statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
anchor = json.loads((HERE / "anchor_audit.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))

assert spec["item_id"] == "S56-M-1269-VALIDATION"
assert spec["theorem_id"] == "THM-M-1269"
assert spec["network_policy"] == "denied"
assert spec["argv"] == ["python3", "Stage1_Instances/THM-M-1269/check_validation.py"]
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor_audit.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert statement["declaration"] == "THM_M_1269_statement"
assert registry["root_obligation_id"] == "M1269-ROOT"

lean_names = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
lean_source = "\n".join((HERE / name).read_text(encoding="utf-8") for name in lean_names)
for pattern in (r"\b(?:sorry|admit|sorryAx)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern
validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
assert "import Proof" not in validation_source
assert "import ObligationTree" not in validation_source
assert "minimizingSequence_proof" not in validation_source

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""
assert anchor["environment"]["mathlib_revision"] == MATHLIB_REVISION
upstream = mathlib / anchor["candidates"][0]["source_path"]
assert upstream.is_file()
assert "theorem exists_seq_tendsto_sInf" in upstream.read_text(encoding="utf-8")

env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = TOOLCHAIN
with tempfile.TemporaryDirectory(prefix="m1269-validation-", dir=LEAN_ROOT) as tmp_name:
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
    ("ObligationTree.lean", "THM_M_1269_root_of_rangeApproximation"),
    ("Proof.lean", "minimizingSequence_proof"),
    ("Validation.lean", "independentMinimizingSequence"),
):
    output = outputs[filename]
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms: \[(.*?)\]",
        output,
        re.DOTALL,
    ) or re.search(
        rf"'[^']*\.{re.escape(declaration)}' depends on axioms: \[(.*?)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, (filename, declaration, output)
    seen = {item.strip() for item in match.group(1).replace("\n", "").split(",")}
    assert seen == ALLOWED_AXIOMS, (declaration, seen)
    assert "sorryAx" not in output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M1269-L-SINF"]

print("ok: exact statement, frozen composition, proof root, and independent local reconstruction elaborated")
print("ok: checked declarations report only propext, Classical.choice, and Quot.sound")
print("ok: placeholder/unsafe scan, proof provenance, frozen hashes, denominator, and clean pinned mathlib checks passed")
print("stale: the frozen pre-proof graph still reports root_closed=false with M1269-L-SINF as its cut")
print("blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
