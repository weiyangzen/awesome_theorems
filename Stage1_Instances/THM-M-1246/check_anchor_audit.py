#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-1246-ANCHOR_AUDIT."""

from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
HERE = Path(__file__).parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit = json.loads((HERE / "anchor-audit.json").read_text())
    manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())
    expected_pin = audit["immutable_environment"]["mathlib_revision"]
    manifest_pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
    actual_pin = subprocess.check_output(
        ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
    ).strip()
    if not expected_pin == manifest_pin == actual_pin:
        raise SystemExit("mathlib revision mismatch")

    module = MATHLIB / "Mathlib" / "Analysis" / "FunctionalSpaces" / "SobolevInequality.lean"
    if sha256(module) != audit["mathlib_search"]["nearest_module_sha256"]:
        raise SystemExit("nearest mathlib module hash mismatch")
    if sha256(HERE / "Statement.lean") != audit["canonical_target"]["statement_file_sha256"]:
        raise SystemExit("canonical statement hash mismatch")

    candidates = {c["declaration"] for c in audit["mathlib_search"]["nearest_candidates"]}
    probe = (HERE / "AnchorAudit.lean").read_text()
    if len(candidates) != 4 or not all(name in probe for name in candidates):
        raise SystemExit("candidate inventory and Lean probe disagree")
    code = "\n".join(line.split("--", 1)[0] for line in probe.splitlines())
    if re.search(r"\b(sorry|admit|axiom)\b|sorryAx", code):
        raise SystemExit("forbidden proof-gap declaration in Lean probe")

    run = subprocess.run(
        ["lake", "env", "lean", str(HERE / "AnchorAudit.lean")],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if run.returncode:
        print(run.stdout, end="")
        raise SystemExit(run.returncode)
    print("anchor audit checks passed: pinned mathlib, hashes, four analogues, Lean elaboration")


if __name__ == "__main__":
    main()

