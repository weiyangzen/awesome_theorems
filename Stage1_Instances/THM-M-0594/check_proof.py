#!/usr/bin/env python3
"""Isolated trust-zero validation for the THM-M-0594 partial proof."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
TARGET = ROOT / "Stage1_Instances" / "THM-M-0594"
FILES = ("Statement.lean", "ProofSupport.lean", "Proof.lean")
PROOF_DECLARATIONS = (
    "properInjectiveEuclideanMap_isEmbedding",
    "whitneyEmbeddingTarget_of_properInjectiveImmersion",
)
PROHIBITED = re.compile(
    r"(?:^|\s)(?:axiom|opaque|constant)\s+|"
    r"\b(?:sorry|admit)\b|sorryAx|unsafe|implemented_by|"
    r"native_decide|proof_wanted|extern"
)


def capture(*argv: str) -> str:
    result = subprocess.run(
        argv,
        cwd=LEAN_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.stdout.strip()


def run_lean(lean: str, lean_path: str, source: Path, output: Path | None = None) -> str:
    argv = [lean, "--trust=0", "-t0", "-R", str(source.parent)]
    if output is not None:
        argv.extend(["-o", str(output)])
    argv.append(str(source))
    env = os.environ.copy()
    env.pop("LEAN_PATH", None)
    env["LEAN_PATH"] = lean_path
    env["LEAN_NUM_THREADS"] = "1"
    result = subprocess.run(
        argv,
        cwd=LEAN_ROOT,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    if result.returncode != 0:
        raise SystemExit(result.stdout or f"Lean exited {result.returncode}")
    return result.stdout


def main() -> None:
    for name in FILES:
        text = (TARGET / name).read_text()
        match = PROHIBITED.search(text)
        assert match is None, f"prohibited construct in {name}: {match.group(0)!r}"

    lean = capture("lake", "env", "which", "lean")
    package_path = capture("lake", "env", "printenv", "LEAN_PATH")
    version = capture("lake", "env", "lean", "--version")

    with tempfile.TemporaryDirectory(prefix="thm-m-0594-proof-") as raw_tmp:
        tmp = Path(raw_tmp)
        for name in FILES:
            shutil.copy2(TARGET / name, tmp / name)

        run_lean(lean, package_path, tmp / "Statement.lean", tmp / "Statement.olean")
        run_lean(lean, package_path, tmp / "ProofSupport.lean", tmp / "ProofSupport.olean")
        proof_output = run_lean(
            lean, f"{tmp}{os.pathsep}{package_path}", tmp / "Proof.lean"
        )

    assert proof_output.count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS)
    for declaration in PROOF_DECLARATIONS:
        marker = f"'Stage1Instances.THM_M_0594.{declaration}' depends on axioms:"
        assert marker in proof_output, f"missing axiom report for {declaration}"
    assert proof_output.count("Classical.choice") == len(PROOF_DECLARATIONS)
    assert proof_output.count("Quot.sound") == len(PROOF_DECLARATIONS)
    assert proof_output.count("propext") == len(PROOF_DECLARATIONS)
    assert "sorryAx" not in proof_output

    for name in FILES:
        assert not (TARGET / name).with_suffix(".olean").exists()

    print("PASS THM-M-0594 partial proof: M0594-L-TOPOLOGICAL")
    print(version)
    print("declarations: " + ", ".join(PROOF_DECLARATIONS))
    print("axioms for each declaration: propext, Classical.choice, Quot.sound")
    print("root closure: open; M0594-C-GLOBAL remains unimplemented")


if __name__ == "__main__":
    main()
