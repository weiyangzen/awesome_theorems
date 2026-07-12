#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0982-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0982"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
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
            f"validation command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
receipt = json.loads((HERE / "validation-receipt.json").read_text())

assert spec["item_id"] == "S56-M-0982-VALIDATION"
assert spec["theorem_id"] == "THM-M-0982"
assert spec["network_policy"] == "denied"
assert receipt["item_id"] == spec["item_id"]
assert receipt["inputs"]["validation_spec_sha256"] == digest(
    HERE / "validation-spec.json"
)
assert receipt["inputs"]["validator_sha256"] == digest(HERE / "check_validation.py")
assert receipt["inputs"]["validation_probe_sha256"] == digest(HERE / "Validation.lean")
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert set(spec["covered_obligation_ids"]) == set(
    registry["frozen_denominators"]["required_machine"]
)

sources = {
    name: (HERE / name).read_text()
    for name in ("Statement.lean", "Proof.lean", "Validation.lean")
}
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
for name, source in sources.items():
    assert prohibited.search(source) is None, f"prohibited Lean token in {name}"

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_PIN
assert run(["git", "status", "--short"], cwd=mathlib) == ""
measure_source = (
    mathlib / "Mathlib" / "MeasureTheory" / "Measure" / "MeasureSpace.lean"
)
measure_text = measure_source.read_text()
for token in (
    "theorem tendsto_measure_iUnion_atTop",
    "theorem tendsto_measure_iInter_atTop",
    "rw [hm.measure_iUnion]",
    "rw [hm.measure_iInter hs hf]",
):
    assert token in measure_text

with tempfile.TemporaryDirectory(prefix="m0982-validation-", dir=LEAN_ROOT) as temp_name:
    temp = Path(temp_name)
    for name, source in sources.items():
        (temp / name).write_text(source)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{temp}:{lean_path}"
    outputs: dict[str, str] = {}
    for name in ("Statement", "Proof", "Validation"):
        argv = ["lake", "env", "lean"]
        if name != "Validation":
            argv += ["-o", str(temp / f"{name}.olean")]
        argv.append(str(temp / f"{name}.lean"))
        outputs[name] = run(argv, cwd=LEAN_ROOT, env=env)

expected_reports = {
    "Proof": ("continuityFromBelow", "continuityFromAbove", "probabilityContinuity"),
    "Validation": ("proofReplay", "independentReconstruction"),
}
for module, declarations in expected_reports.items():
    output = outputs[module]
    for declaration in declarations:
        assert declaration in output and "depends on axioms" in output
    observed = {
        axiom for axiom in ALLOWED_AXIOMS if axiom in output
    }
    assert observed == ALLOWED_AXIOMS, (module, observed)
    assert "sorryAx" not in output

assert "Proof.probabilityContinuity" not in re.sub(
    r"theorem proofReplay.*?theorem independentReconstruction",
    "theorem independentReconstruction",
    sources["Validation.lean"],
    flags=re.DOTALL,
).split("#print axioms", 1)[0]

print("ok: exact statement and proof-phase root elaborated against the clean pinned mathlib revision")
print("ok: exact-type replay and separately implemented same-workspace reconstruction both passed")
print("ok: machine-reported axiom set is propext, Classical.choice, and Quot.sound; no sorryAx")
print("ok: placeholder/unsafe scan, frozen statement/registry hashes, and terminal source provenance passed")
print("blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
