#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1269 proof-phase body."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
proof = (ROOT / "Proof.lean").read_text(encoding="utf-8")

required = [
    "theorem minimizingSequence_proof",
    "THM_M_1269_statement X F",
    "exists_seq_tendsto_sInf",
    "choose sequence hsequence using hmem",
]
missing = [item for item in required if item not in proof]
if missing:
    raise SystemExit(f"FAIL: missing required proof structure: {missing}")

prohibited = re.compile(r"\b(?:sorry|admit)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
match = prohibited.search(proof)
if match:
    raise SystemExit(f"FAIL: prohibited proof device: {match.group(0)!r}")

print("PASS: exact root wrapper, pinned bridge, preimage choice, and no prohibited proof device")
