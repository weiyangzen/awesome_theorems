#!/usr/bin/env python3
"""Fail-closed proof-phase checks for S56-M-1133-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1133-PROOF"
THEOREM = "THM-M-1133"
BASE_REVISION = "0afbf514f9bd5f339943542106f6b811869fe572"
PROOF = HERE / "Proof.lean"
RECEIPT = HERE / "proof-receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], *, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=LEAN_DIR,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=360,
    )
    sys.stdout.write(result.stdout)
    if result.returncode:
        raise SystemExit(result.returncode)
    return result.stdout


def main() -> None:
    proof = PROOF.read_text(encoding="utf-8")
    code = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
    code = re.sub(r"--.*", "", code)
    prohibited = re.compile(
        r"\b(?:s" + r"orry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(?:axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(code) is None
    for marker in (
        "import «Stage1_Instances».«THM-M-1133».ObligationTree",
        "theorem iteratedFDeriv_diag_nonpos_of_localMax",
        "theorem spatialLaplacian_nonpos_of_localMax",
        "theorem strictSubsolutionMaximumPrinciple",
        "lemma perturb_isStrictSubcaloric",
        "theorem weakSubsolutionMaximumPrinciple : WeakSubsolutionMaximumPrinciple",
        "root_of_subsolutionMaximumPrinciple weakSubsolutionMaximumPrinciple",
        "#print axioms heatEquationWeakMaximumPrinciple",
    ):
        assert marker in proof, marker

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["proof_body"]["source_sha256"] == sha256(PROOF)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]

    with tempfile.TemporaryDirectory(prefix="thm-m-1133-proof-") as directory:
        cache = Path(directory)
        module_dir = cache / "Stage1_Instances" / "THM-M-1133"
        module_dir.mkdir(parents=True)
        common = ["lake", "env", "lean", "-R", str(ROOT)]
        base_path = subprocess.check_output(
            ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_DIR, text=True
        ).strip()
        lean_env = os.environ.copy()
        lean_env["LEAN_NUM_THREADS"] = "1"
        run(common + ["-o", str(module_dir / "Statement.olean"), str(HERE / "Statement.lean")],
            env=lean_env)
        lean_env["LEAN_PATH"] = f"{cache}:{base_path}"
        run(common + [
            "-o", str(module_dir / "ObligationTree.olean"), str(HERE / "ObligationTree.lean")
        ], env=lean_env)
        output = run(common + [str(PROOF)], env=lean_env)

    normalized = " ".join(output.split())
    expected = "depends on axioms: [propext, Classical.choice, Quot.sound]"
    assert normalized.count(expected) == 8
    assert "declaration uses 'sorry'" not in output
    print("PASS THM-M-1133 proof phase: exact heat maximum-principle root kernel-closed")
    print(f"proof source sha256: {sha256(PROOF)}")
    print("accepted state unchanged; proof proposal is provisional pending master acceptance")


if __name__ == "__main__":
    main()
