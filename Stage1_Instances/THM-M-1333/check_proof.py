#!/usr/bin/env python3
"""Elaborate the THM-M-1333 proof body with the pinned Lake environment."""

import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
statement = (HERE / "Statement.lean").read_text()
statement = statement.split("set_option pp.explicit true in", 1)[0]
proof = (HERE / "Proof.lean").read_text().replace("import Statement\n", "", 1)

with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=HERE, delete=False) as handle:
    handle.write(statement + "\n" + proof)
    temporary = Path(handle.name)
try:
    result = subprocess.run(
        ["lake", "env", "lean", str(temporary)],
        cwd=ROOT / "Formalizations" / "Lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(result.stdout, end="")
    raise SystemExit(result.returncode)
finally:
    temporary.unlink()
