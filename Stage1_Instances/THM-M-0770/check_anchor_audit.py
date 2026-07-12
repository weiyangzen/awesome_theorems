#!/usr/bin/env python3
"""Validate the pinned THM-M-0770 mathlib anchor and audit record."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "AnchorAudit.lean"
AUDIT = HERE / "anchor-audit.json"
EXPECTED_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def run(argv, cwd):
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def main() -> None:
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    revision = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
    if revision != EXPECTED_REV:
        raise SystemExit(f"mathlib revision mismatch: {revision}")

    mathlib = (LEAN_DIR / ".lake" / "packages" / "mathlib").resolve()
    checkout_revision = run(["git", "rev-parse", "HEAD"], mathlib).strip()
    if checkout_revision != EXPECTED_REV:
        raise SystemExit(f"mathlib checkout mismatch: {checkout_revision}")

    zorn_source = mathlib / "Mathlib" / "Order" / "Zorn.lean"
    audit = json.loads(AUDIT.read_text())
    if audit["immutable_environment"]["mathlib_revision"] != EXPECTED_REV:
        raise SystemExit("audit revision mismatch")
    digest = hashlib.sha256(zorn_source.read_bytes()).hexdigest()
    if audit["immutable_environment"]["mathlib_zorn_source_sha256"] != digest:
        raise SystemExit("pinned Zorn source digest mismatch")

    output = run(["lake", "env", "lean", str(SOURCE)], LEAN_DIR)
    required = [
        "zorn_le_nonempty",
        "canonical_of_pinned_mathlib",
        "[propext, Classical.choice, Quot.sound]",
    ]
    missing = [token for token in required if token not in output]
    if missing:
        raise SystemExit(f"Lean evidence missing: {missing}; output={output!r}")
    print(json.dumps({
        "item_id": audit["item_id"],
        "mathlib_revision": revision,
        "mathlib_zorn_source_sha256": digest,
        "lean_exit_code": 0,
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "exact_wrapper": "Stage1Instances.THM_M_0770.AnchorAudit.canonical_of_pinned_mathlib",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
