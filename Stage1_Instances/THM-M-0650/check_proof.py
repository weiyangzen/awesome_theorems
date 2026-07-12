#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-0650 proof integration."""

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0650"
proof = (OWNED / "Proof.lean").read_text()
registry = json.loads((OWNED / "obligation-registry.json").read_text())
audit = json.loads((OWNED / "anchor-audit.json").read_text())

assert registry["root_obligation_id"] == "M0650-ROOT"
assert registry["denominator_sha256"] == "76fcfa12ad9d8f829ca1f7cf79a690badfb720641a5d75376b1925f1f49a3132"
assert audit["immutable_environment"]["mathlib_revision"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert "theorem embeddingTarskiVaught" in proof
assert "f.isElementary_of_exists h" in proof
assert "theorem tarskiVaught : TarskiVaughtTarget" in proof
assert "S.isElementary_of_exists h" in proof

# Comments are removed so policy words used in explanatory prose do not trip
# the proof-body scan.
code = re.sub(r"/-.*?-\/", "", proof, flags=re.S)
code = re.sub(r"--.*", "", code)
for forbidden in (r"\bsorry\b", r"\badmit\b", r"\baxiom\b", r"sorryAx", r"\bunsafe\b"):
    assert not re.search(forbidden, code), f"forbidden proof token: {forbidden}"

digest = hashlib.sha256((OWNED / "Proof.lean").read_bytes()).hexdigest()
print(f"PASS THM-M-0650 proof source: sha256={digest}")
