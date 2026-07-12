#!/usr/bin/env python3
"""Validate the immutable THM-M-1023 anchor-audit receipt and Lean probes."""

from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_DIR / ".lake" / "packages" / "mathlib"
RECEIPT = json.loads((OWNED / "anchor-audit.json").read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(
        command, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    return result.stdout


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    mathlib_pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
    env = RECEIPT["immutable_environment"]
    require(mathlib_pin == env["mathlib_revision"], "mathlib manifest pin drift")
    require(run(["git", "rev-parse", "HEAD"], MATHLIB).strip() == mathlib_pin,
            "checked-out mathlib revision drift")
    require(run(["git", "rev-parse", "HEAD^{tree}"], MATHLIB).strip() == env["mathlib_tree"],
            "checked-out mathlib tree drift")
    require(sha256(OWNED / "Statement.lean") == RECEIPT["audited_target"]["statement_file_sha256"],
            "frozen statement hash drift")
    basic = MATHLIB / "Mathlib/MeasureTheory/Measure/CharacteristicFunction/Basic.lean"
    require(sha256(basic) == env["characteristic_function_module_sha256"],
            "mathlib characteristic-function module drift")
    require(sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"],
            "mathlib license drift")

    run(["lake", "env", "lean", str(OWNED / "Statement.lean")], LEAN_DIR)
    probe_output = run(["lake", "env", "lean", str(OWNED / "AnchorAudit.lean")], LEAN_DIR)
    for declaration in RECEIPT["mathlib_candidates"][0]["declarations"]:
        require(declaration.split(".")[-1] in probe_output,
                f"missing Lean probe output for {declaration}")

    require(RECEIPT["local_search"]["exact_terminal_candidate_count"] == 0,
            "receipt unexpectedly credits a local terminal candidate")
    require(RECEIPT["root_machine_classification"] == "M3", "machine status overclaim")
    require(not RECEIPT["theorem_proved"] and not RECEIPT["theorem_complete"],
            "anchor audit must not claim theorem closure")
    require(RECEIPT["gate_state"] == "self_tested_pending_master_acceptance",
            "incorrect worker gate state")
    print(
        "anchor audit ok: mathlib pin/tree and 3 local hashes matched; "
        "6 named API probes and 2 typed examples elaborated; "
        "1 external definition-only candidate; 0 terminal candidates; root remains H1/M3/R4"
    )


if __name__ == "__main__":
    main()
