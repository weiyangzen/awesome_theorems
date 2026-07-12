#!/usr/bin/env python3
"""Validate the THM-M-0118 immutable anchor-audit artifact."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
HERE = Path(__file__).resolve().parent


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    audit = json.loads((HERE / "anchor-audit.json").read_text())
    statement = json.loads((HERE / "statement.json").read_text())
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    packages = {package["name"]: package for package in manifest["packages"]}

    target = audit["audited_target"]
    formal_target = statement["canonical_formal_target"]
    if target["elaborated_expression_sha256"] != formal_target["elaborated_expression_sha256"]:
        fail("anchor audit is detached from the frozen expression")
    if hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() != target["statement_file_sha256"]:
        fail("anchor audit is detached from Statement.lean")
    if audit["immutable_environment"]["mathlib_revision"] != packages["mathlib"]["rev"]:
        fail("mathlib revision does not match lake-manifest.json")
    if audit["external_candidates"] or audit["machine_debt"] != "M3":
        fail("unexpected terminal-candidate classification")

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
    print(json.dumps({
        "item_id": audit["item_id"],
        "mathlib_revision": packages["mathlib"]["rev"],
        "mathlib_candidate_families_checked": len(audit["mathlib_candidates"]),
        "external_terminal_candidates": len(audit["external_candidates"]),
        "terminal_result": "open_M3",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
