#!/usr/bin/env python3
"""Compile the frozen target, then check the exact pinned-mathlib anchor."""

from pathlib import Path
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
OWNED = Path(__file__).resolve().parent


def run(command: list[str], env: dict[str, str] | None = None) -> None:
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


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="thm-m-1521-anchor-") as directory:
        cache = Path(directory)
        olean = cache / "Stage1_Instances" / "THM-M-1521" / "Statement.olean"
        olean.parent.mkdir(parents=True)
        run([
            "lake", "env", "lean", "-R", str(ROOT), "-o", str(olean),
            str(OWNED / "Statement.lean"),
        ])
        env = os.environ.copy()
        env["LEAN_PATH"] = f"{cache}:{env.get('LEAN_PATH', '')}"
        run(["lake", "env", "lean", str(OWNED / "AnchorAudit.lean")], env)


if __name__ == "__main__":
    main()
