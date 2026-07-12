#!/usr/bin/env python3
"""Elaborate THM-M-1146 and ensure its structural mutations differ."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_1146"
DECLARATIONS = [
    "SchwarzReflectionTarget",
    "mutationRemovedOpenness",
    "mutationRemovedSymmetry",
    "mutationRemovedContinuity",
    "mutationRemovedBoundaryVanishing",
    "mutationChangedOddSign",
]


def expression(declaration: str) -> str:
    text = SOURCE.read_text()
    marker = "#print SchwarzReflectionTarget"
    text = text.replace(marker, f"#print {declaration}")
    with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=SOURCE.parent, delete=False) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        result = subprocess.run(
            ["lake", "env", "lean", str(temporary)], cwd=LEAN_DIR, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        if result.returncode:
            raise SystemExit(result.stdout)
    finally:
        temporary.unlink()
    match = re.search(r" : Prop :=\n(?P<expression>.*)\Z", result.stdout, re.DOTALL)
    if not match:
        raise SystemExit(f"could not extract expression for {NAMESPACE}.{declaration}")
    return match.group("expression").strip()


def main() -> None:
    expressions = {name: expression(name) for name in DECLARATIONS}
    canonical = expressions[DECLARATIONS[0]]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    print(json.dumps({
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": DECLARATIONS[1:],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
