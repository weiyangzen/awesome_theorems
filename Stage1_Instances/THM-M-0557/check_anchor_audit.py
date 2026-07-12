#!/usr/bin/env python3
"""Validate the immutable THM-M-0557 anchor-audit record."""

from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_DIR / ".lake" / "packages" / "mathlib"
AUDIT = Path(__file__).with_name("anchor-audit.json")
PROBE = Path(__file__).with_name("AnchorAudit.lean")
STATEMENT_CHECK = Path(__file__).with_name("check_statement.py")


def run(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        list(args), cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    return result.stdout


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit = json.loads(AUDIT.read_text())
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
    installed = run("git", "rev-parse", "HEAD", cwd=MATHLIB).strip()
    source = MATHLIB / "Mathlib/Topology/Homotopy/HomotopyGroup.lean"

    assert audit["item_id"] == "S56-M-0557-ANCHOR_AUDIT"
    assert audit["theorem_id"] == "THM-M-0557"
    assert audit["immutable_environment"]["mathlib_revision"] == pin == installed
    assert audit["immutable_environment"]["mathlib_source_sha256"] == sha256(source)
    assert audit["root_machine_classification_after_node"] == "M3"
    assert audit["eligible_anchor"] == "S56-M-0557-C02"
    assert audit["theorem_complete"] is False

    output = run("lake", "env", "lean", str(PROBE), cwd=LEAN_DIR)
    statement_output = run("python3", str(STATEMENT_CHECK))
    required = [
        "HomotopyGroup.group", "HomotopyGroup.commGroup",
        "HomotopyGroup.auxGroup_indep", "pinnedMathlibCandidate",
    ]
    assert all(name in output for name in required)
    assert "sorryAx" not in output
    assert "c194bd11441b036272cf4faff6e11fdcf62c833b4ba822276ffb2b0061845e70" in statement_output
    print(json.dumps({
        "candidate_probe": "passed",
        "mathlib_revision": pin,
        "mathlib_source_sha256": sha256(source),
        "forbidden_axiom": "absent",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
