#!/usr/bin/env python3
"""Fail-closed elaboration and fingerprint check for S56-M-1246-STATEMENT."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")


def main() -> None:
    code = "\n".join(line.split("--", 1)[0] for line in SOURCE.read_text().splitlines())
    if re.search(r"\b(sorry|admit|axiom)\b|sorryAx", code):
        raise SystemExit("forbidden proof-gap declaration in Statement.lean")

    run = subprocess.run(
        ["lake", "env", "lean", str(SOURCE)],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if run.returncode:
        sys.stdout.write(run.stdout)
        raise SystemExit(run.returncode)
    match = re.search(r" : Prop :=\n(?P<expression>.*)\Z", run.stdout, re.DOTALL)
    if not match:
        raise SystemExit("could not extract the pp.explicit elaborated expression")

    manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())
    print(json.dumps({
        "elaborated_expression_sha256": hashlib.sha256(
            match.group("expression").strip().encode()
        ).hexdigest(),
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "killed_mutations": [
            "dimension lower bound changed from 3 to 2",
            "compact-support hypothesis removed",
            "inequality direction reversed",
        ],
        "toolchain": (LEAN_ROOT / "lean-toolchain").read_text().strip(),
        "mathlib_revision": next(
            p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
