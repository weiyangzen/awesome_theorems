#!/usr/bin/env python3
"""Fail-closed proof-phase checks for S56-M-1521-PROOF."""

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
PROOF = HERE / "Proof.lean"
RECEIPT = HERE / "proof-receipt.json"


def run(command: list[str], env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=LEAN_DIR,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    sys.stdout.write(result.stdout)
    if result.returncode:
        raise SystemExit(result.returncode)
    return result.stdout


def main() -> None:
    source = PROOF.read_text()
    prohibited = re.compile(
        r"\b(?:s" + r"orry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b",
        re.MULTILINE,
    )
    assert prohibited.search(source) is None
    for declaration in (
        "theorem preservingToConservative_proof",
        "theorem conservativeToSetRecurrence_proof",
        "theorem poincareRecurrence_proof",
    ):
        assert declaration in source

    receipt = json.loads(RECEIPT.read_text())
    assert receipt["item_id"] == "S56-M-1521-PROOF"
    assert receipt["theorem_id"] == "THM-M-1521"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["result"]["root_closed"] is True
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(PROOF.read_bytes()).hexdigest()
    assert receipt["inputs"]["statement_sha256"] == hashlib.sha256(
        (HERE / "Statement.lean").read_bytes()
    ).hexdigest()
    assert receipt["inputs"]["obligation_tree_sha256"] == hashlib.sha256(
        (HERE / "ObligationTree.lean").read_bytes()
    ).hexdigest()
    assert receipt["inputs"]["obligation_registry_sha256"] == hashlib.sha256(
        (HERE / "obligation-registry.json").read_bytes()
    ).hexdigest()

    with tempfile.TemporaryDirectory(prefix="thm-m-1521-proof-") as directory:
        cache = Path(directory)
        module_dir = cache / "Stage1_Instances" / "THM-M-1521"
        module_dir.mkdir(parents=True)
        common = ["lake", "env", "lean", "-R", str(ROOT)]
        run(common + ["-o", str(module_dir / "Statement.olean"), str(HERE / "Statement.lean")])
        env = os.environ.copy()
        env["LEAN_PATH"] = f"{cache}:{env.get('LEAN_PATH', '')}"
        run(
            common + [
                "-o", str(module_dir / "ObligationTree.olean"),
                str(HERE / "ObligationTree.lean"),
            ],
            env,
        )
        output = run(["lake", "env", "lean", str(PROOF)], env)

    normalized = " ".join(output.split())
    expected = "depends on axioms: [propext, Classical.choice, Quot.sound]"
    assert normalized.count(expected) == 5
    assert "declaration uses 'sorry'" not in output
    print(
        "PASS THM-M-1521 proof phase: both frozen bridge packages and the "
        "exact root wrapper elaborated"
    )


if __name__ == "__main__":
    main()
