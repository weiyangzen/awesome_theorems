#!/usr/bin/env python3
"""Fail-closed narrow validation for the THM-M-0452 proof deliverable."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import re


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None):
    completed = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False
    )
    if completed.returncode != 0:
        raise SystemExit(
            f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


spec = json.loads((HERE / "validation-phase-spec.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())

assert spec["item_id"] == "S56-M-0452-VALIDATION"
assert spec["theorem_id"] == registry["theorem_id"] == graphs["theorem_id"] == "THM-M-0452"
assert spec["recipe"]["network_policy"] == "denied"
assert spec["recipe"]["expected_exit"] == 0
assert set(spec["recipe"]["covered_obligation_ids"]) == {
    "M0452-D-WELLDEFINED", "M0452-D-POSITIVE"
}
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False

mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
mathlib_dir = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib_dir).strip() == mathlib["rev"]
assert run(["git", "status", "--porcelain"], cwd=mathlib_dir) == ""

for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    forbidden = ("sorry", "admit", "sorryAx", "axiom ", "unsafe ")
    # Avoid matching ordinary words such as "admits" while remaining a
    # deliberately redundant defense behind kernel elaboration.
    assert all(token not in source for token in forbidden if token != "admit"), f"forbidden token in {name}"
    assert not re.search(r"\badmit\b", source), f"forbidden token in {name}"

lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
env = os.environ.copy()

with tempfile.TemporaryDirectory(prefix="m0452-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    env["LEAN_PATH"] = lean_path
    outputs = []
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        outputs.append(run([lean, "-o", str(tmp / name.replace(".lean", ".olean")), name], cwd=tmp, env=env))

combined = "\n".join(outputs)
for declaration in (
    "quotientPairingCoreOfPolarization",
    "quotientPairingCoreTarget_of_polarization",
    "quotient_branch_probe",
):
    assert declaration in combined and "depends on axioms:" in combined
assert "sorryAx" not in combined
for axiom in ("propext", "Classical.choice", "Quot.sound"):
    assert axiom in combined

print("ok: fresh temporary kernel replay passed for the frozen statement, composition, quotient proof, and exact-type probe")
print("ok: observed axioms are propext, Classical.choice, and Quot.sound; no sorryAx or forbidden source token")
print(f"ok: mathlib pin and clean source tree verified at {mathlib['rev']}")
print(f"inputs: statement={sha256(HERE / 'Statement.lean')} proof={sha256(HERE / 'Proof.lean')} validation={sha256(HERE / 'Validation.lean')}")
print("open: exact root, height and polarization proof bodies, cold-cache hermetic replay, and distinct-runner verification")
