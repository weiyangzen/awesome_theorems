#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0010-PROOF."""

import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
proof = (here / "Proof.lean").read_text()
statement = json.loads((here / "statement.json").read_text())
registry = json.loads((here / "obligation-registry.json").read_text())

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for required in (
    "import Statement",
    "theorem artinRees : ArtinReesTarget.{u, v}",
    "Ideal.exists_pow_inf_eq_pow_smul I N",
    "#print axioms artinRees",
):
    assert required in proof

assert statement["canonical_formal_target"]["declaration_or_expression"] == \
    "Stage1Instances.THM_M_0010.ArtinReesTarget"
assert registry["root_obligation_id"] == "M0010-ROOT"
assert registry["frozen_against_statement_sha256"] == \
    hashlib.sha256((here / "Statement.lean").read_bytes()).hexdigest()

print("PASS THM-M-0010 proof phase: exact frozen target has a placeholder-free pinned proof body")
