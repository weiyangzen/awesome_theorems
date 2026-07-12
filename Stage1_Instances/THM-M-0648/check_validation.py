#!/usr/bin/env python3
"""Fail-closed worker validator for THM-M-0648's exact paired proof."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0648"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    with (OWNED / name).open(encoding="utf-8") as handle:
        return json.load(handle)


expected_hashes = {
    OWNED / "Statement.lean": "27605643e4706bbcec0ea4db6c13ce95bc16b035db5de85adfaab245cf062ec2",
    OWNED / "Proof.lean": "dd5b6aa59ba2ea6584e6862ca05cb2a85aea7384e99eea9726eae43fc61250b1",
    OWNED / "ObligationTree.lean": "2ec0ad6001e7a7562dcf80d6ec2508d05e750c763d942323adb5544c48d0fb5b",
    OWNED / "obligation-registry.json": "e0ddc60285c1d6623b0d7b918979b732f2590c0c42a9219acf264a4ac3dafc4a",
    OWNED / "typed-graphs.json": "0f73d1da9f441764115624e9b39c482add1a96a02023d753595b53b58bd995d2",
    OWNED / "proof-receipt.json": "a57715834738705ef6ee268e4f648f55eeda2ed879c70cf64d561afc06a3577d",
    LEAN_ROOT / "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    LEAN_ROOT / "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    MATHLIB / "Mathlib/ModelTheory/Skolem.lean": "85c5fa3fd4f76381b02d46a8bfd515cceb14254543e0afae95004c1fc07137b0",
    MATHLIB / "Mathlib/ModelTheory/Satisfiability.lean": "0abb92d531851a57909945b740981d79a4cbb29238f2a3d21cb5fa57aa143edb",
}
for path, expected in expected_hashes.items():
    if not path.is_file() or digest(path) != expected:
        fail(f"missing or stale pinned input: {path.relative_to(ROOT)}")

registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof_receipt = load("proof-receipt.json")
required = set(registry["frozen_denominators"]["required_machine"])
closed = set(proof_receipt["closed_obligation_ids"])
if registry["root_obligation_id"] != "M0648-ROOT" or required != closed:
    fail("proof receipt does not close exactly the frozen machine denominator")
if proof_receipt["result"].get("root_closed") is not True:
    fail("proof receipt does not close the exact root")
if proof_receipt["result"].get("theorem_complete") is not False:
    fail("proof receipt falsely claims theorem completion")

nodes = {node["obligation_id"] for node in graphs["nodes"]}
if nodes != {item["obligation_id"] for item in registry["obligations"]}:
    fail("typed-graph and registry node sets disagree")
edges = graphs["graphs"]["proof"]["edges"]
by_id = {edge["edge_id"]: edge for edge in edges}
if len(by_id) != len(edges):
    fail("duplicate proof edge id")
for edge in edges:
    reciprocal = by_id.get(edge["reciprocal_edge_id"])
    if reciprocal is None or reciprocal["from"] != edge["to"] or reciprocal["to"] != edge["from"]:
        fail(f"invalid reciprocal edge: {edge['edge_id']}")

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|unsafe)\b|implemented_by", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "ObligationTree.lean", "Validation.lean"):
    source = (OWNED / name).read_text(encoding="utf-8")
    code = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith(("--", "/-", "*")))
    if prohibited.search(code):
        fail(f"prohibited local trust token in {name}")

commands = [
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0648/Statement.lean"],
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0648/Proof.lean"],
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0648/Validation.lean"],
]
outputs: list[str] = []
for command in commands:
    result = subprocess.run(command, cwd=LEAN_ROOT, capture_output=True, text=True, timeout=30)
    output = result.stdout + result.stderr
    if result.returncode != 0:
        fail(f"recipe exited {result.returncode}: {' '.join(command)}\n{output}")
    if "sorryAx" in output:
        fail(f"kernel axiom report contains sorryAx: {' '.join(command)}")
    outputs.append(output)

for output in outputs[1:]:
    if not all(axiom in output for axiom in ("propext", "Classical.choice", "Quot.sound")):
        fail("kernel axiom report differs from the recorded trust profile")

revision = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=MATHLIB, capture_output=True, text=True, timeout=10, check=True
).stdout.strip()
if revision != "8a178386ffc0f5fef0b77738bb5449d50efeea95":
    fail("mathlib revision differs from the pinned provenance record")

print("validation ok: exact root and independent probe elaborated; pins, graph, provenance, trust, and open release boundary agree")
