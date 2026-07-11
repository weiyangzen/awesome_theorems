#!/usr/bin/env python3
"""Validate the immutable, locally checkable anchor-audit ledger."""

import hashlib
import json
import pathlib
import subprocess


ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
AUDIT_PATH = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
mathlib_package = next(p for p in manifest["packages"] if p["name"] == "mathlib")
env = audit["immutable_environment"]

assert audit["item_id"] == "S56-M-0086-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0086"
assert env["mathlib_revision"] == mathlib_package["rev"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == env["mathlib_tree"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

for candidate in audit["mathlib_candidates"]:
    source = MATHLIB / candidate["source_file"]
    assert sha256(source) == candidate["source_sha256"]
    source_text = source.read_text(encoding="utf-8")
    for declaration in candidate["declarations"]:
        assert declaration["source_needle"] in source_text

probe = pathlib.Path(__file__).with_name("AnchorAudit.lean").read_text(encoding="utf-8")
for name in audit["terminal_declarations"]:
    assert f"#check {name}" in probe
assert "theorem pinned_mathlib_closes_unfolded_target" in probe
assert audit["root_decision"]["classification"] == "M1"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is False
assert audit["theorem_complete"] is False

print("ok: immutable mathlib pins, source hashes, three terminal anchors, and M1 boundary verified")
