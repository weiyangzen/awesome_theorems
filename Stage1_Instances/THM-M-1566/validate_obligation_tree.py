#!/usr/bin/env python3
"""Elaborate Statement plus ObligationTree without creating an unpinned olean."""

import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
statement = (HERE / "Statement.lean").read_text()
tree = (HERE / "ObligationTree.lean").read_text()
assert tree.startswith("import Statement\n")
combined = statement + "\n" + tree.removeprefix("import Statement\n")
with tempfile.NamedTemporaryFile(mode="w", suffix=".lean", dir=HERE, delete=True) as source:
    source.write(combined)
    source.flush()
    result = subprocess.run(
        ["lake", "env", "lean", "../../" + Path(source.name).relative_to(ROOT).as_posix()],
        cwd=ROOT / "Formalizations/Lean", text=True, capture_output=True, timeout=120)
print(result.stdout, end="")
print(result.stderr, end="")
if result.returncode:
    raise SystemExit(result.returncode)
assert "root_of_existence_and_uniqueness" in result.stdout
assert "depends on axioms:" in result.stdout
print("PASS conditional composition elaborated from exact Statement.lean source")
