#!/usr/bin/env python3
"""Validate the THM-M-1011 immutable anchor-audit receipt."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit = json.loads((HERE / "anchor-audit.json").read_text())
    statement = json.loads((HERE / "statement.json").read_text())
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    mathlib = next(p for p in manifest["packages"] if p["name"] == "mathlib")

    assert audit["item_id"] == "S56-M-1011-ANCHOR_AUDIT"
    assert audit["root_decision"]["classification"] == "M5"
    assert not audit["root_decision"]["kernel_closed"]
    assert not audit["theorem_proved"] and not audit["theorem_complete"]
    assert audit["audited_target"]["elaborated_expression_sha256"] == \
        statement["canonical_formal_target"]["elaborated_expression_sha256"]
    assert audit["audited_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert audit["immutable_environment"]["mathlib_revision"] == mathlib["rev"]

    mathlib_root = LEAN_DIR / ".lake" / "packages" / "mathlib"
    head = subprocess.run(
        ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"], check=True,
        text=True, capture_output=True).stdout.strip()
    assert head == mathlib["rev"]
    for candidate in audit["candidates"][:2]:
        assert sha256(mathlib_root / candidate["file"]) == candidate["source_sha256"]

    source = (HERE / "AnchorAudit.lean").read_text()
    assert "fail_if_success haveI : T2Space X := inferInstance" in source
    for forbidden in ("sorry", "admit", "axiom "):
        assert forbidden not in source.lower()

    result = subprocess.run(
        ["lake", "env", "lean", str(HERE / "AnchorAudit.lean")], cwd=LEAN_DIR,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(result.stdout)
    if result.returncode:
        raise SystemExit(result.returncode)
    print(json.dumps({
        "item_id": audit["item_id"],
        "mathlib_revision": mathlib["rev"],
        "candidates_audited": len(audit["candidates"]),
        "root_classification": "M5",
        "first_failed_gate": "exact statement match"
    }, sort_keys=True))


if __name__ == "__main__":
    main()
