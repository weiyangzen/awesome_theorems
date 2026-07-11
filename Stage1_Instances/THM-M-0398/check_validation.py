#!/usr/bin/env python3
"""Fail-closed validator for THM-M-0398's partial validation packet."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0398"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def load(name: str) -> dict:
    return json.loads((OWNED / name).read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


expected_hashes = {
    "Statement.lean": "65d901d6ab3f5659638a302037c0b116a0b5293165a9f096fd40d958a0963dc9",
    "ObligationTree.lean": "6c9fe6c2d133f90556a6c629d4d2155c95222b9c8c90fb3c308a0134482d90d0",
    "Proof.lean": "3ca0cd5bf7808a0f28e65d0e79506ebfa84eb7c6094cff7e64e70713b4598b84",
    "Validation.lean": "abb21cee8a9bbb9d852ce432bf2680b436999b8c08384ba5966d1abc3da1e366",
    "obligation-registry.json": "3c246db0239fff016e115bea83143d5ca8a90d3f11e8cc9a213d58f3e0533fad",
    "typed-graphs.json": "6aa42622c96676d7093180c6c8fede71492f55742e913ccde73082ec85896a15",
    "proof-receipt.json": "d9aaed2ccce203c9297ad4da0103e84cafa98972a2fb9df98ee7814588eeb484",
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

registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
receipt = load("proof-receipt.json")
ids = {row["obligation_id"] for row in registry["obligations"]}
if registry.get("theorem_id") != "THM-M-0398" or registry.get("root_obligation_id") != "M0398-ROOT":
    fail("canonical theorem or root identity mismatch")
if len(ids) != 15 or ids != {row["obligation_id"] for row in graphs["nodes"]}:
    fail("frozen 15-node registry and graph disagree")
if receipt.get("closed_obligation_ids") != ["M0398-T"]:
    fail("proof receipt claims an unexpected closure set")
if receipt.get("result", {}).get("root_closed") is not False or \
        receipt.get("result", {}).get("theorem_complete") is not False:
    fail("partial proof receipt falsely closes the root")

nodes = {row["obligation_id"]: row for row in graphs["nodes"]}
if nodes["M0398-ROOT"].get("machine_debt") != "M3":
    fail("root is not explicitly open at M3")
for obligation_id in ("M0398-N1", "M0398-C1", "M0398-C2", "M0398-L1",
                      "M0398-L2", "M0398-L3", "M0398-L4"):
    if nodes[obligation_id].get("machine_debt") not in {"M3", "M4", "M5"}:
        fail(f"open root dependency {obligation_id} is overstated")

prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (OWNED / name).read_text(encoding="utf-8")
    code = "\n".join(line for line in source.splitlines()
                     if not line.lstrip().startswith(("--", "/-", "*")))
    if prohibited.search(code):
        fail(f"prohibited placeholder or trust declaration in {name}")

outputs = []
for command in (
    ["bash", "../../Stage1_Instances/THM-M-0398/check_proof.sh"],
    ["bash", "../../Stage1_Instances/THM-M-0398/check_validation_lean.sh"],
):
    run = subprocess.run(command, cwd=LEAN_ROOT, capture_output=True, text=True, timeout=120)
    output = run.stdout + run.stderr
    if run.returncode != 0:
        fail(f"recipe exited {run.returncode}: {' '.join(command)}\n{output}")
    if "sorryAx" in output:
        fail(f"kernel report contains sorryAx: {' '.join(command)}")
    outputs.append(output)

for output in outputs:
    if not all(axiom in output for axiom in ("propext", "Classical.choice", "Quot.sound")):
        fail("axiom report is incomplete")

print("validation ok: frozen hashes and 15-node boundary verified; partial proof and independent probes elaborated; root remains open")
