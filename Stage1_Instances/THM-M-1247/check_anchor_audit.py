#!/usr/bin/env python3
"""Validate THM-M-1247's immutable anchor-audit receipt."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    audit = json.loads((HERE / "anchor-audit.json").read_text())
    statement = json.loads((HERE / "statement.json").read_text())
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    packages = {package["name"]: package for package in manifest["packages"]}

    target = statement["canonical_formal_target"]
    audited = audit["audited_target"]
    if audited["elaborated_expression_sha256"] != target["elaborated_expression_sha256"]:
        fail("anchor audit is detached from the frozen expression")
    if audited["statement_file_sha256"] != digest(HERE / "Statement.lean"):
        fail("anchor audit is detached from Statement.lean")
    environment = audit["immutable_environment"]
    if environment["mathlib_revision"] != packages["mathlib"]["rev"]:
        fail("mathlib revision differs from the Lake manifest")
    if environment["lake_manifest_sha256"] != digest(LEAN_DIR / "lake-manifest.json"):
        fail("Lake manifest digest mismatch")
    if audit["theorem_proved"] or audit["theorem_complete"]:
        fail("anchor-only receipt overclaims theorem closure")
    if any(candidate["classification"] != "excluded_not_a_candidate"
           for candidate in audit["external_candidates"]):
        fail("unexpected external proof-credit classification")

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
        "external_exact_candidates": 0,
        "terminal_result": "open",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
