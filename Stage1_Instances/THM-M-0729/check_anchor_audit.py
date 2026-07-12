#!/usr/bin/env python3
"""Verify immutable local inputs and fail-closed claims for THM-M-0729."""

import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == env["mathlib_tree"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""
assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]

local = next(c for c in audit["candidates"] if c["candidate_id"] == "M0729-A-LOCAL-STATEMENT")
assert sha256(ROOT / local["module"]) == local["source_sha256"]

support = next(c for c in audit["candidates"] if c["candidate_id"] == "M0729-A-MATHLIB-SUPPORT")
for relative, expected in support["source_sha256"].items():
    assert sha256(MATHLIB / relative) == expected

search = subprocess.run(
    [
        "rg", "-n", "-i", "--glob", "*.lean",
        r"probabilistically.checkable|PCP.?theorem|PCP\[|InPCP|proof.oracle|oracle.checker",
        str(MATHLIB / "Mathlib"),
    ],
    text=True,
    capture_output=True,
    check=False,
)
assert search.returncode == 1 and search.stdout == ""

verdict = audit["audit_verdict"]
assert verdict["exact_external_root_found"] is False
assert verdict["theorem_complete"] is False
assert audit["audit_complete"] is False
assert audit["theorem_complete"] is False

print(
    "anchor audit verified: immutable pins and source hashes agree; "
    "no exact PCP root candidate is claimed; root=M3"
)

