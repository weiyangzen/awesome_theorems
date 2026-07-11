#!/usr/bin/env python3
"""Fail-closed validator for the THM-M-0396 partial validation handoff."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0396"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def load(name: str) -> dict:
    with (OWNED / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof_receipt = load("proof-receipt.json")

if registry.get("theorem_id") != "THM-M-0396":
    fail("registry theorem identity mismatch")
if registry.get("root_obligation_id") != "M0396-ROOT":
    fail("canonical root identity mismatch")

obligation_ids = {item["obligation_id"] for item in registry["obligations"]}
graph_ids = {item["obligation_id"] for item in graphs["nodes"]}
if obligation_ids != graph_ids or len(obligation_ids) != 15:
    fail("15-node frozen registry and typed graph identity mismatch")
if set(proof_receipt.get("closed_obligation_ids", [])) != {"M0396-N1"}:
    fail("proof receipt claims an unexpected closure set")
result = proof_receipt.get("result", {})
if result.get("root_closed") is not False or result.get("theorem_complete") is not False:
    fail("partial proof receipt falsely closes the root")

nodes = {item["obligation_id"]: item for item in graphs["nodes"]}
if nodes["M0396-ROOT"].get("machine_debt") not in {"M3", "M4", "M5"}:
    fail("root does not remain explicitly machine-open")
for open_id in (
    "M0396-N2", "M0396-C1", "M0396-C2", "M0396-L1", "M0396-L2",
    "M0396-L3", "M0396-L4", "M0396-T", "M0396-X2",
):
    if nodes[open_id].get("machine_debt") not in {"M3", "M4", "M5"}:
        fail(f"required open obligation {open_id} is overstated")

expected_hashes = {
    "Statement.lean": "adc9e134e2e2164064f33d35c056fd66aac052127dff858fa5b4b3de4ad9d094",
    "ObligationTree.lean": "93551393a7489d5705b063a632952da8018d97285b32d4d2b25fdb2642dee81b",
    "Proof.lean": "e5b54890782c60ae76f4fdfed09fcdb873e86a08b6bdd26895adb90e9c33c34b",
    "Validation.lean": "d810532234e6982083b0b699945dcc047f6d64b74edf610654bb4edff7264a92",
    "obligation-registry.json": "d63c20b7d77043e656fd5e295e68171a5b3d4dabea527dd6c6d1a15c90ff97f3",
    "typed-graphs.json": "b0090e4f7389f2c9d26f350719b88ef2e40f49c530b561a896c909bd1a7ad942",
    "proof-receipt.json": "8e02797f44d3fc02d0c6ddee903a0803f6a0ed5c5a77430cf8c1675ec38807b1",
}
for name, expected in expected_hashes.items():
    actual = digest(OWNED / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")

if digest(LEAN_ROOT / "lean-toolchain") != \
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2":
    fail("Lean toolchain pin changed")
if digest(LEAN_ROOT / "lake-manifest.json") != \
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81":
    fail("Lake manifest pin changed")

prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (OWNED / name).read_text(encoding="utf-8")
    code = "\n".join(
        line for line in source.splitlines()
        if not line.lstrip().startswith(("--", "/-", "*"))
    )
    if prohibited.search(code):
        fail(f"prohibited placeholder or trust declaration in {name}")

commands = [
    ["bash", "../../Stage1_Instances/THM-M-0396/check_proof.sh"],
    ["bash", "../../Stage1_Instances/THM-M-0396/check_validation_lean.sh"],
]
outputs = []
for command in commands:
    completed = subprocess.run(
        command, cwd=LEAN_ROOT, capture_output=True, text=True, timeout=120
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        fail(f"recipe exited {completed.returncode}: {' '.join(command)}\n{output}")
    if "sorryAx" in output:
        fail(f"kernel report contains sorryAx: {' '.join(command)}")
    outputs.append(output)

required_axioms = ("propext", "Classical.choice", "Quot.sound")
if not all(name in outputs[0] for name in required_axioms):
    fail("proof axiom report is incomplete")
if not all(name in outputs[1] for name in required_axioms):
    fail("independent probe axiom report is incomplete")

print(
    "validation ok: frozen inputs and 15-node boundary verified; "
    "partial proof and independent probes elaborated; root remains open"
)
