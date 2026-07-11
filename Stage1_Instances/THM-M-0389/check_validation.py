#!/usr/bin/env python3
"""Fail-closed worker validator for THM-M-0389's exact-root proof."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0389"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_HASHES = {
    "Statement.lean": "b1c4763988d6843efc8b919871919506456ba0d6703b3e95d1abb21cba7904ac",
    "Proof.lean": "0911688a3c2a1a75a3d5a90a653b633fc69b186f7d70e096688e3bc5eb33d77a",
    "ObligationTree.lean": "6357925075d24dd7c4d2c6db84504f96dac00fe8ac728ef6524764d1b3b2de48",
    "obligation-registry.json": "0c56e9871381c62e487e510f5694632ef8a976daaedbfc174a2977cc8d16be97",
    "typed-graphs.json": "dc93a1456b5c9464f1e2c33898f48b65eede538bf287c6bf0ce4480907a1c747",
    "proof-units.json": "360626ffb2c9fc03fc232ad9fec562fd7cb9d825c7b092c6594e163fff30d14d",
}


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lean(source: Path) -> str:
    env = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"}
    result = subprocess.run(
        ["lake", "env", "lean", "-R", str(OWNED), str(source)],
        cwd=LEAN_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    output = result.stdout + result.stderr
    if result.returncode:
        fail(f"Lean exited {result.returncode} for {source.name}\n{output}")
    if "sorryAx" in output:
        fail(f"kernel report contains sorryAx for {source.name}")
    return output


def axiom_set(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms: \[(?P<body>[^]]*)\]",
        output,
    )
    if not match:
        fail(f"missing axiom report for {declaration}")
    return {item.strip() for item in match.group("body").split(",") if item.strip()}


def run_probe() -> str:
    combined = (OWNED / "Proof.lean").read_text() + "\n" + (OWNED / "Validation.lean").read_text()
    with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=OWNED, delete=False) as handle:
        handle.write(combined)
        probe = Path(handle.name)
    try:
        output = lean(probe)
    finally:
        probe.unlink()
    declaration = "Stage1Instances.THM_M_0389_Validation.validationExactRoot"
    if axiom_set(output, declaration) != EXPECTED_AXIOMS:
        fail("validation probe axiom set differs from the accepted standard profile")
    if "exactRoot_iff_frozen" not in combined:
        fail("exact-root definitional identity probe is absent")
    return output


parser = argparse.ArgumentParser()
parser.add_argument("--probe-only", action="store_true")
args = parser.parse_args()

if args.probe_only:
    run_probe()
    print("validation probe ok: independently spelled root is definitionally exact and inhabited")
    raise SystemExit(0)

for name, expected in EXPECTED_HASHES.items():
    actual = digest(OWNED / name)
    if actual != expected:
        fail(f"stale input {name}: expected {expected}, got {actual}")
if digest(LEAN_ROOT / "lean-toolchain") != "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2":
    fail("Lean toolchain pin changed")
if digest(LEAN_ROOT / "lake-manifest.json") != "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81":
    fail("Lake dependency manifest changed")

registry = json.loads((OWNED / "obligation-registry.json").read_text())
graphs = json.loads((OWNED / "typed-graphs.json").read_text())
units = json.loads((OWNED / "proof-units.json").read_text())
ids = {row["obligation_id"] for row in registry["obligations"]}
if len(ids) != 16 or ids != set(graphs["nodes"]):
    fail("frozen 16-obligation registry and graph identity disagree")
if registry["canonical_root"] != "M0389-ROOT":
    fail("canonical root changed")
if any(row["obligation_id"] not in ids for row in units["nodes"]):
    fail("proof-unit manifest contains a foreign obligation")

prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = (OWNED / name).read_text()
    code = "\n".join(
        line for line in source.splitlines()
        if not line.lstrip().startswith(("--", "/-", "*"))
    )
    if prohibited.search(code):
        fail(f"prohibited placeholder or trust declaration in {name}")

proof_output = lean(OWNED / "Proof.lean")
proof_decl = "Stage1Instances.THM_M_0389.integerMarkovClassification"
if axiom_set(proof_output, proof_decl) != EXPECTED_AXIOMS:
    fail("root proof axiom set differs from the accepted standard profile")
run_probe()

print(
    "validation ok: frozen inputs and 16-node identity verified; exact root and "
    "exact-type probe elaborated; standard axiom profile and placeholder policy passed"
)
