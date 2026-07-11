#!/usr/bin/env python3
"""Validate the THM-M-0112 immutable anchor-audit receipt."""

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

    if audit["audited_target"]["elaborated_expression_sha256"] != \
            statement["canonical_formal_target"]["elaborated_expression_sha256"]:
        fail("anchor audit is detached from the frozen expression")
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    if statement_hash != audit["audited_target"]["statement_file_sha256"]:
        fail("anchor audit is detached from Statement.lean")
    for key, package_name in (("mathlib_revision", "mathlib"),
                              ("flt_regular_revision", "«flt-regular»")):
        if audit["immutable_environment"][key] != packages[package_name]["rev"]:
            fail(f"manifest revision mismatch: {package_name}")

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
        "mathlib_candidates_checked": len(audit["mathlib_candidates"]),
        "external_terminal_candidates": len(audit["external_candidates"]),
        "terminal_result": "open",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
