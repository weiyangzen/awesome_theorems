#!/usr/bin/env python3
"""Narrow, fail-closed validation for S56-M-0985-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "Stage1_Instances" / "THM-M-0985"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
FORBIDDEN = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)[ \t]",
    re.MULTILINE,
)


def run(argv: list[str], cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"command failed ({result.returncode}): {' '.join(argv)}\n{result.stdout}"
        )
    return result.stdout


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    spec = json.loads((TARGET / "validation-phase-spec.json").read_text())
    registry = json.loads((TARGET / "obligation-registry.json").read_text())
    receipt = json.loads((TARGET / "proof-receipt.json").read_text())
    if spec["item_id"] != "S56-M-0985-VALIDATION":
        raise SystemExit("validation recipe is bound to the wrong item")
    if registry["root_obligation_id"] != "M0985-ROOT":
        raise SystemExit("unexpected frozen root obligation")
    if receipt["result"]["root_closed"] is not True:
        raise SystemExit("proof prerequisite does not report kernel root closure")
    if sha256(TARGET / "Statement.lean") != receipt["inputs"]["statement_sha256"]:
        raise SystemExit("statement differs from the proof receipt input")
    if sha256(TARGET / "ObligationTree.lean") != receipt["inputs"]["obligation_tree_sha256"]:
        raise SystemExit("obligation interface differs from the proof receipt input")
    if sha256(TARGET / "Proof.lean") != receipt["proof_body"]["source_sha256"]:
        raise SystemExit("proof source differs from the proof receipt input")

    revision = run(["git", "rev-parse", "HEAD"], MATHLIB).strip()
    if revision != PIN:
        raise SystemExit(f"mathlib pin mismatch: expected {PIN}, got {revision}")
    if run(["git", "status", "--porcelain"], MATHLIB).strip():
        raise SystemExit("pinned mathlib source checkout is dirty")
    terminal = MATHLIB / "Mathlib" / "Probability" / "StrongLaw.lean"
    expected_terminal_hash = receipt["proof_body"]["terminal_source_sha256"]
    if sha256(terminal) != expected_terminal_hash:
        raise SystemExit("pinned terminal source hash differs from proof receipt")

    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        if FORBIDDEN.search((TARGET / name).read_text()):
            raise SystemExit(f"prohibited proof construct in {name}")
    if re.search(r"^\s*import\s+Proof\s*$", (TARGET / "Validation.lean").read_text(), re.M):
        raise SystemExit("independent probe must not import Proof.lean")

    base_path = run(["lake", "env", "printenv", "LEAN_PATH"], LEAN_ROOT).strip()
    env = os.environ.copy()
    env.update({"ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0", "LANG": "C.UTF-8", "TZ": "UTC"})
    with tempfile.TemporaryDirectory(prefix=".validation-check.", dir=TARGET) as raw_tmp:
        tmp = Path(raw_tmp)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(TARGET / name, tmp / name)
        env["LEAN_PATH"] = base_path
        run(["lake", "env", "lean", "-o", "Statement.olean", "Statement.lean"], tmp, env)
        env["LEAN_PATH"] = f".{os.pathsep}{base_path}"
        run(["lake", "env", "lean", "-o", "ObligationTree.olean", "ObligationTree.lean"], tmp, env)
        proof_output = run(["lake", "env", "lean", "Proof.lean"], tmp, env)
        independent_output = run(["lake", "env", "lean", "Validation.lean"], tmp, env)

    for declaration, output in (
        ("kolmogorovStrongLaw", proof_output),
        ("kolmogorovStrongLaw_independent", independent_output),
    ):
        if declaration not in output:
            raise SystemExit(f"Lean output did not identify {declaration}")
        observed = set(re.findall(r"(?:propext|Classical\.choice|Quot\.sound|sorryAx)", output))
        if observed != EXPECTED_AXIOMS:
            raise SystemExit(f"unexpected axiom profile for {declaration}: {sorted(observed)}")

    print("PASS THM-M-0985 validation: exact proof root and independent reconstruction elaborate")
    print("axioms: [propext, Classical.choice, Quot.sound]; placeholder/unsafe scan: pass")
    print(f"provenance: mathlib {revision}; StrongLaw.lean sha256 {sha256(terminal)}")
    print("FAIL-CLOSED hermetic release: shared warm .lake cache; no cold empty-cache offline replay or complete TCB/SBOM")
    print("FAIL-CLOSED independent release: same checkout/runner; no distinct signed attestation or independent minimal verifier")


if __name__ == "__main__":
    main()
