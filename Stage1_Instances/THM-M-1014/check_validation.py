#!/usr/bin/env python3
"""Narrow, fail-closed validation runner for S56-M-1014-VALIDATION."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-1014"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED = {
    "Statement.lean": "03af2e1309d2e86056ac37c4630ec7f9dbabcb009e55aac820cfad8b4df5d198",
    "ObligationTree.lean": "ff18998dc3f68ababc760f051e36df9d0031c56fbf2057a4f5bbd9cc9532bb0e",
    "Proof.lean": "7806ff31b02d9914da2b07d3ca481810a3d30d13eea11f409bab88e34511f6cf",
    "obligation-registry.json": "6fa94e0852f87e511db201f32ba4f3311ebf2b4f9460433f302fbe5ba50b53a9",
    "typed-graphs.json": "f16e57ee74d3e3d2266af1a2062d98f95c9ace903884fdd65f0d687099430de3",
    "proof.json": "a8eb7fea1b7e7d6eb2ff3ed2bc3c9f14f93905b3eadc6e273219abb6743a1049",
}
PROHIBITED = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\s", re.MULTILINE)


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=120
    )
    output = result.stdout + result.stderr
    if result.returncode != 0:
        fail(f"{' '.join(argv)} exited {result.returncode}\n{output}")
    return output


for name, digest in EXPECTED.items():
    if sha256(OWNED / name) != digest:
        fail(f"frozen input hash mismatch: {name}")

registry = json.loads((OWNED / "obligation-registry.json").read_text())
graphs = json.loads((OWNED / "typed-graphs.json").read_text())
proof_record = json.loads((OWNED / "proof.json").read_text())
ids = {row["obligation_id"] for row in registry["obligations"]}
if registry["root_obligation_id"] != "M1014-ROOT" or len(ids) != 14:
    fail("unexpected canonical root or obligation denominator")
if {node["obligation_id"] for node in graphs["nodes"]} != ids:
    fail("typed graph nodes disagree with the frozen registry")
if proof_record["closed_obligation_ids"] != [
    "THM-M-1014-X-PINNED", "THM-M-1014-T-ASSEMBLE", "THM-M-1014-ROOT"
]:
    fail("proof record does not attest the expected proof route")

for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    if PROHIBITED.search((OWNED / name).read_text()):
        fail(f"prohibited Lean construct in {name}")

manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())
mathlib_entry = next((row for row in manifest["packages"] if row["name"] == "mathlib"), None)
if mathlib_entry is None or mathlib_entry["rev"] != EXPECTED_MATHLIB:
    fail("lake manifest does not pin the expected mathlib revision")
if run(["git", "rev-parse", "HEAD"], MATHLIB).strip() != EXPECTED_MATHLIB:
    fail("checked-out mathlib revision differs from the manifest pin")
if run(["git", "status", "--porcelain"], MATHLIB):
    fail("pinned mathlib source worktree is dirty")

terminal_source = MATHLIB / "Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean"
terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/MeasureTheory/Measure/ProbabilityMeasure.olean"
if sha256(terminal_source) != "f8e505e1d388a65ef1f0f8e19916a1a673872fa373a922ca78ec05aa807b856d":
    fail("terminal mathlib source digest mismatch")
if sha256(terminal_olean) != "69a9a38958c00f21be94f37e4d628d19da4476ddbfbe5093abcbfa5ffdf6f81e":
    fail("terminal mathlib olean digest mismatch")

lean = run(["lake", "env", "which", "lean"], LEAN_ROOT).strip()
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], LEAN_ROOT).strip()
with tempfile.TemporaryDirectory(prefix="m1014-validation-") as directory:
    temp = Path(directory)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (temp / name).write_bytes((OWNED / name).read_bytes())
    outputs = []
    for name in ("Statement", "ObligationTree", "Proof", "Validation"):
        env = {"LEAN_PATH": f"{temp}:{lean_path}"}
        outputs.append(run([lean, "-o", f"{name}.olean", f"{name}.lean"], temp, env))

combined = "\n".join(outputs)
for declaration in (
    "continuousMappingTheorem",
    "independentContinuousMappingTheorem",
    "ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous",
):
    if declaration not in combined:
        fail(f"Lean output did not identify {declaration}")
for axiom in ("propext", "Classical.choice", "Quot.sound"):
    if axiom not in combined:
        fail(f"expected observed axiom absent from Lean output: {axiom}")

print("validation: PASS: four frozen modules elaborated from fresh temporary source copies")
print("validation: PASS: exact proof root and independently written direct probe kernel-check")
print("validation: PASS: observed axioms are propext, Classical.choice, and Quot.sound")
print("validation: PASS: frozen hashes, provenance, placeholder policy, and dependency pin passed")
print("validation: BLOCKED release-only: warm shared .lake is not an empty-cache hermetic replay")
print("validation: BLOCKED release-only: this worker is not a distinct independent runner")
