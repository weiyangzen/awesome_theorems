#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0993 proof-phase artifact."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
proof = ROOT / "Proof.lean"
statement = ROOT / "Statement.lean"

proof_text = proof.read_text(encoding="utf-8")
statement_text = statement.read_text(encoding="utf-8")

for forbidden in (r"\bsorry\b", r"\badmit\b", r"\baxiom\b"):
    if re.search(forbidden, proof_text):
        raise SystemExit(f"forbidden proof placeholder matched: {forbidden}")

required = (
    "theorem sum_integrable",
    "theorem exponential_markov",
    "theorem sum_mgf_factorization",
    "theorem empty_family_boundary",
    "theorem chernoff_upper_tail",
    "hindep.integrable_exp_mul_sum",
    "measure_ge_le_exp_mul_mgf",
    "hindep.mgf_sum",
)
for token in required:
    if token not in proof_text:
        raise SystemExit(f"missing proof closure token: {token}")

def body(text: str) -> str:
    marker = "def ChernoffUpperTailTarget : Prop :="
    start = text.index(marker)
    end = text.index("\n\n/--", start)
    return "".join(text[start:end].split())

if body(proof_text) != body(statement_text):
    raise SystemExit("proof target is not textually identical to statement target")

print("check_proof: ok (exact target, 5 proof declarations, no placeholders)")
