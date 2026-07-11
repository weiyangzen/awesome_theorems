#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0010-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0010"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    if result.returncode:
        raise SystemExit(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'(?:[^']*\.)?{re.escape(declaration)}' depends on axioms:\s*\[(?P<body>[^]]*)\]",
        output,
    )
    if not match:
        raise SystemExit(f"validation failed: missing axiom report for {declaration}")
    return {item.strip() for item in match.group("body").split(",") if item.strip()}


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == "S56-M-0010-VALIDATION"
assert spec["theorem_id"] == "THM-M-0010"
assert spec["network_policy"] == "denied"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["root_obligation_id"] == "M0010-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["item_id"] == "S56-M-0010-PROOF"
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == digest(
    HERE / "ObligationTree.lean"
)
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["result"]["root_closed"] is True
assert set(proof_receipt["closed_obligation_ids"]) == set(
    registry["frozen_denominators"]["required_machine"]
)

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited source token in {name}"
assert "import Proof" not in (HERE / "Validation.lean").read_text()
assert "artinRees" not in (HERE / "Validation.lean").read_text()

manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())
assert next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib") == EXPECTED_MATHLIB
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB
assert run(["git", "status", "--short"], cwd=mathlib) == ""
assert digest(mathlib / "Mathlib/RingTheory/Filtration.lean") == (
    "b161e2c4ce77f1224648467573dd4ba4c0ebc1ed734118e70df4cb39b33b1a72"
)

with tempfile.TemporaryDirectory(prefix="m0010-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", str(tmp / "ObligationTree.lean")], cwd=LEAN_ROOT, env=env
    )
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env
    )
    validation_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )

for declaration, output in (
    ("root_of_exact_candidate", obligation_output),
    ("artinRees", proof_output),
    ("independentlyReconstructedArtinRees", validation_output),
):
    axioms = reported_axioms(output, declaration)
    assert axioms <= ALLOWED_AXIOMS
    assert "sorryAx" not in output

assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False

print("PASS THM-M-0010 narrow validation")
print("kernel: exact proof, composition probe, and independently written exact-target probe elaborated")
print("trust: reported axioms are within propext, Classical.choice, Quot.sound")
print("provenance: proof receipt hashes, frozen denominator, and clean pinned mathlib source agree")
print("hygiene: no local sorry/admit/axiom/unsafe token")
print("stale: frozen typed graph predates proof closure and still reports root_closed=false")
print("blocked: warm shared cache; cold hermetic replay and distinct-runner verification remain open")
