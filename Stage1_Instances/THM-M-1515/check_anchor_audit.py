#!/usr/bin/env python3
"""Validate the THM-M-1515 immutable anchor-audit artifacts."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], cwd: Path) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    sys.stdout.write(result.stdout)
    if result.returncode:
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    audit = json.loads((HERE / "anchor-audit.json").read_text())
    statement = json.loads((HERE / "statement.json").read_text())
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    packages = {package["name"]: package for package in manifest["packages"]}

    target = audit["audited_target"]
    frozen = statement["canonical_formal_target"]
    require(target["elaborated_expression_sha256"] == frozen["elaborated_expression_sha256"],
            "audit is detached from the frozen expression")
    require(target["statement_file_sha256"] == digest(HERE / "Statement.lean"),
            "audit is detached from Statement.lean")
    env = audit["immutable_environment"]
    require(env["mathlib_revision"] == packages["mathlib"]["rev"],
            "manifest mathlib pin mismatch")
    require(env["lake_manifest_sha256"] == digest(LEAN_DIR / "lake-manifest.json"),
            "manifest content hash mismatch")

    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    head = run(["git", "rev-parse", "HEAD"], mathlib)
    tree = run(["git", "rev-parse", "HEAD^{tree}"], mathlib)
    require(head == env["mathlib_revision"], "installed mathlib HEAD mismatch")
    require(tree == env["mathlib_tree"], "installed mathlib tree mismatch")
    require(run(["git", "status", "--short"], mathlib) == "",
            "installed mathlib worktree is dirty")
    require(env["mathlib_license_sha256"] == digest(mathlib / "LICENSE"),
            "mathlib license hash mismatch")

    run(["lake", "env", "lean", str(HERE / "AnchorAudit.lean")], LEAN_DIR)
    require(all(row["type_checked"] and not row["terminal"]
                for row in audit["mathlib_candidates"]),
            "candidate classification is not fail-closed")
    require(not audit["external_lean4_search"]["external_candidates"],
            "unexpected external candidate lacks integration audit")
    require(audit["classification"]["machine"] == "M3", "root machine state changed")
    require(not audit["classification"]["theorem_complete"],
            "anchor audit cannot claim theorem completion")
    print(json.dumps({
        "item_id": audit["item_id"],
        "mathlib_revision": head,
        "mathlib_candidates_checked": len(audit["mathlib_candidates"]),
        "external_terminal_candidates": 0,
        "root_machine_state": "M3",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
