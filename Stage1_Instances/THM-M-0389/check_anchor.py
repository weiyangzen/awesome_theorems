#!/usr/bin/env python3
"""Compile the immutable repo-local THM-M-0389 candidate and inspect axioms."""

from pathlib import Path
import subprocess
import sys
import tempfile
import re

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
LEGACY = LEAN_DIR / "AwesomeTheorems" / "Stage1" / "S1_M_020.lean"
DECLARATIONS = [
    "AwesomeTheorems.Stage1.S1_M_020.checked_local_algebra_package",
    "AwesomeTheorems.Stage1.S1_M_020.p3_descendant_markov_checked",
    "AwesomeTheorems.Stage1.S1_M_020.p4_height_decrease_bridge_checked",
    "AwesomeTheorems.Stage1.S1_M_020.p5_reverse_vieta_z_generation_checked",
    "AwesomeTheorems.Stage1.S1_M_020.integerWrapper_of_positiveGeneration_and_nonzeroSignLift",
    "AwesomeTheorems.Stage1.S1_M_020.statementShape_of_integerWrapperTarget",
]


def main() -> None:
    suffix = "\n" + "\n".join(f"#print axioms {name}" for name in DECLARATIONS) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=Path(__file__).parent, delete=False
    ) as handle:
        handle.write(LEGACY.read_text())
        handle.write(suffix)
        candidate = Path(handle.name)
    try:
        result = subprocess.run(
            ["lake", "env", "lean", str(candidate)],
            cwd=LEAN_DIR,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    finally:
        candidate.unlink()

    sys.stdout.write(result.stdout)
    if result.returncode:
        raise SystemExit(result.returncode)
    reports = re.findall(r"^'([^']+)' depends on axioms:", result.stdout, re.MULTILINE)
    if reports != DECLARATIONS:
        raise SystemExit(f"expected axiom reports for {DECLARATIONS}, found {reports}")
    print(f"anchor audit: ok ({len(reports)} checked declarations, axiom sets reported)")


if __name__ == "__main__":
    main()
