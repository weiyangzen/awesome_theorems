#!/usr/bin/env python3
"""Comment-aware prohibited-construct scan for owned and pinned obligation sources."""

from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FILES = (
    HERE / "ObligationTree.lean",
    HERE / "ObligationSignatures.lean",
    ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Tutte.lean",
)
FORBIDDEN = (
    "s" + "orry",
    "a" + "dmit",
    "s" + "orryAx",
    "a" + "xiom ",
    "unsafe ",
    "opaque ",
    "implemented_by",
    "native_decide",
)


def code_only(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.S)
    return re.sub(r"--.*", "", source)


for path in FILES:
    code = code_only(path.read_text())
    hits = [token for token in FORBIDDEN if token in code]
    if hits:
        raise SystemExit(f"FAIL {path.name}: prohibited constructs {hits}")

print("PASS prohibited-construct scan: ObligationTree.lean, ObligationSignatures.lean, pinned Tutte.lean")
