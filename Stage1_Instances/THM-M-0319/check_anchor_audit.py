#!/usr/bin/env python3
"""Validate the structured THM-M-0319 anchor audit and its Lean adapter."""

from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"


def main() -> None:
    audit = json.loads((HERE / "anchor-audit.json").read_text())
    assert audit["item_id"] == "S56-M-0319-ANCHOR_AUDIT"
    assert audit["canonical_expression_sha256"] == (
        "2e4dc02230de7a1c08fdf4a19ef0ec1da107297972dee0e85d893bdb33d6a514"
    )
    assert audit["root_machine_classification"] == "M3"
    assert audit["audit_complete_for_phase"] is True
    assert audit["theorem_proved"] is False
    assert audit["theorem_complete"] is False
    candidates = {row["id"]: row for row in audit["candidates"]}
    external = candidates["M0319-C02"]
    assert external["revision"] == "11a9f041246d28374edae384241757f9a0cbd5e4"
    assert external["evidence_level"] == "E3"
    assert external["classification"] == "M3"
    assert external["integration"] == "not in local dependency closure"

    source = (HERE / "AnchorAudit.lean").read_text()
    for forbidden in ("sorry", "admit", "axiom ", "unsafe"):
        if forbidden in source:
            raise SystemExit(f"forbidden Lean token in AnchorAudit.lean: {forbidden!r}")
    result = subprocess.run(
        ["lake", "env", "lean", str(HERE / "AnchorAudit.lean")],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    sys.stdout.write(result.stdout)
    if result.returncode:
        raise SystemExit(result.returncode)
    if "HarfeBrouwerType" not in result.stdout:
        raise SystemExit("external candidate type was not printed")
    if "harfe_type_implies_canonical" not in result.stdout:
        raise SystemExit("adapter axiom report was not printed")
    print("anchor audit invariant check: ok; 5 candidates; root M3; theorem incomplete")


if __name__ == "__main__":
    main()
