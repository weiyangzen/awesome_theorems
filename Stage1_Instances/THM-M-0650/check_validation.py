#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-0650-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0650"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env=None) -> str:
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


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.S)
    return re.sub(r"--.*", "", source)


statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
audit = json.loads((HERE / "anchor-audit.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

assert statement["theorem_id"] == registry["theorem_id"] == "THM-M-0650"
assert registry["root_obligation_id"] == "M0650-ROOT"
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == sha256(
    HERE / "obligation-registry.json"
)
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert audit["immutable_environment"]["mathlib_revision"] == MATHLIB_REV

mathlib_entry = next(package for package in manifest["packages"] if package["name"] == "mathlib")
assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REV
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REV
assert run(["git", "status", "--short"], cwd=mathlib) == ""

terminal_source = mathlib / "Mathlib" / "ModelTheory" / "ElementaryMaps.lean"
wrapper_source = mathlib / "Mathlib" / "ModelTheory" / "ElementarySubstructures.lean"
license_file = mathlib / "LICENSE"
immutable = audit["immutable_environment"]
assert sha256(terminal_source) == immutable["elementary_maps_sha256"]
assert sha256(wrapper_source) == immutable["elementary_substructures_sha256"]
assert sha256(license_file) == immutable["license_file_sha256"]

local_source = "\n".join(
    (HERE / name).read_text() for name in ("Statement.lean", "Proof.lean")
)
dependency_source = terminal_source.read_text() + "\n" + wrapper_source.read_text()
for source in (local_source, dependency_source):
    code = code_without_comments(source)
    for pattern in (r"\b(?:sorry|admit|sorryAx)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
        assert re.search(pattern, code, re.MULTILINE) is None, pattern

with tempfile.TemporaryDirectory(prefix="m0650-validation-") as tmp_name:
    tmp = Path(tmp_name)
    statement_output = run(
        [
            "lake", "env", "lean", "-R", "../..", "-o",
            str(tmp / "Statement.olean"),
            "../../Stage1_Instances/THM-M-0650/Statement.lean",
        ],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    proof_output = run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0650/Proof.lean"],
        cwd=LEAN_ROOT,
        env=env,
    )

assert "TarskiVaughtTarget" in statement_output
for declaration in ("embeddingTarskiVaught", "tarskiVaught"):
    assert declaration in proof_output
observed_axioms = set(re.findall(r"\b(?:propext|Classical\.choice|Quot\.sound)\b", proof_output))
assert observed_axioms == ALLOWED_AXIOMS
assert "depends on axioms" in proof_output

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["remaining_root_cut_set"] == ["M0650-T-EMBEDDING"]
assert proof_receipt["result"]["root_closed"] is True
assert proof_receipt["result"]["theorem_complete"] is False

print("ok: exact Tarski-Vaught statement and proof wrappers elaborated against pinned Lean/mathlib")
print("ok: both proof declarations report only propext, Classical.choice, and Quot.sound")
print("ok: placeholder, frozen-input, terminal-source, license, manifest-pin, and clean-mathlib checks passed")
print("stale: the frozen graph predates Proof.lean and still reports M0650-T-EMBEDDING open")
print("blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
