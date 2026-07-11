#!/usr/bin/env python3
"""Fail-closed validator for the THM-M-0400 partial validation handoff."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0400"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


def load(name: str) -> dict:
    return json.loads((OWNED / name).read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


tree = load("obligation-tree.json")
proof_receipt = load("proof-receipt.json")
receipt = load("validation-receipt.json")

if tree.get("theorem_id") != "THM-M-0400" or tree.get("obligations", [{}])[0].get("obligation_id") != "M0400-ROOT":
    fail("obligation-tree identity mismatch")
ids = [item["obligation_id"] for item in tree["obligations"]]
if len(ids) != 13 or len(set(ids)) != 13:
    fail("expected 13 unique frozen obligations")
if tree["denominators"].get("closed_machine_ids") != []:
    fail("frozen tree unexpectedly claims machine closure")
if tree.get("theorem_complete") is not False or tree.get("root_vector", {}).get("M") != "M3":
    fail("root must remain M3 and theorem-open")
if proof_receipt.get("closed_obligation_ids") != []:
    fail("proof receipt unexpectedly closes an obligation")
if proof_receipt.get("supported_obligation_ids") != ["M0400-S-BOUNDARY"]:
    fail("proof receipt support boundary changed")
result = receipt.get("result", {})
if result.get("root_closed") is not False or result.get("theorem_complete") is not False:
    fail("validation receipt falsely closes the root")
if receipt.get("canonical_obligation_ids") != ids:
    fail("receipt obligation identity/order mismatch")

expected = {
    "statement_sha256": ("Statement.lean", "29752f8af82237ba47ef9a22c8c73e641b8efc679eee94d324fe13ce62918e24"),
    "proof_sha256": ("Proof.lean", "456cdc2670e9bc3931840f34af3192b714cdca0db60e705050d34926f78519cd"),
    "validation_probe_sha256": ("Validation.lean", "51f9d440c1259de84d280cdf114ca2c1da99e40b902d73712446a1746b5040f5"),
    "obligation_tree_sha256": ("obligation-tree.json", "5c638ca364766c85234df59945dc1152dc82a82f4a70392fd470bb1aa3dc32f8"),
    "proof_receipt_sha256": ("proof-receipt.json", "f55f6c88cf3927c03949fef632656a1b2cba84a4209bcb318d7170c8642b7bca"),
}
for key, (name, frozen) in expected.items():
    actual = digest(OWNED / name)
    if actual != frozen or receipt["inputs"].get(key) != actual:
        fail(f"stale or unbound input {name}: {actual}")
for key, path, frozen in (
    ("lean_toolchain_sha256", LEAN_ROOT / "lean-toolchain", "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"),
    ("lake_manifest_sha256", LEAN_ROOT / "lake-manifest.json", "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"),
):
    actual = digest(path)
    if actual != frozen or receipt["inputs"].get(key) != actual:
        fail(f"pin changed or receipt unbound: {path.name}")

validation_source = (OWNED / "Validation.lean").read_text(encoding="utf-8")
if "Proof" in validation_source.splitlines()[0]:
    fail("independent validation probe imports Proof")
prohibited = re.compile(r"\b(?:sorry|admit)\b|^\s*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    source = (OWNED / name).read_text(encoding="utf-8")
    code = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith(("--", "/-", "*")))
    if prohibited.search(code):
        fail(f"prohibited proof mechanism in {name}")

outputs = []
for command in (
    ["bash", "../../Stage1_Instances/THM-M-0400/check_proof.sh"],
    ["bash", "../../Stage1_Instances/THM-M-0400/check_validation_lean.sh"],
):
    completed = subprocess.run(command, cwd=LEAN_ROOT, capture_output=True, text=True, timeout=120)
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        fail(f"recipe exited {completed.returncode}: {' '.join(command)}\n{output}")
    if "sorryAx" in output:
        fail(f"kernel output contains sorryAx: {' '.join(command)}")
    for axiom in ("propext", "Classical.choice", "Quot.sound"):
        if axiom not in output:
            fail(f"missing expected axiom report {axiom}: {' '.join(command)}")
    outputs.append(output)

print("validation ok: frozen 13-node boundary and inputs verified; proof and independent probes elaborate; root remains M3/open")
