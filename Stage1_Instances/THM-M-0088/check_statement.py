#!/usr/bin/env python3
"""Elaborate THM-M-0088 and distinguish structural statement mutations."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0088"
DECLARATIONS = [
    "YonedaEmbeddingTarget",
    "MutationFaithfulOnly",
    "MutationCoyoneda",
    "MutationUniverseRaised",
]


def elaborate(source: Path) -> str:
    result = subprocess.run(
        ["lake", "env", "lean", str(source)], cwd=LEAN_DIR, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def printed(declaration: str) -> str:
    prefix = SOURCE.read_text().split(
        "set_option pp.universes true in\nset_option pp.explicit true in\n#check"
    )[0]
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False
    ) as handle:
        handle.write(prefix)
        handle.write("set_option pp.universes true in\n")
        handle.write("set_option pp.explicit true in\n")
        handle.write(f"#print {NAMESPACE}.{declaration}\n")
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    match = re.search(r" :=\n(?P<body>.*)\Z", output, re.DOTALL)
    if not match:
        raise SystemExit(f"could not extract elaborated declaration {declaration}")
    return match.group("body").strip()


def main() -> None:
    expressions = {name: printed(name) for name in DECLARATIONS}
    canonical = expressions[DECLARATIONS[0]]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    print(json.dumps({
        "expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": DECLARATIONS[1:],
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text().strip(),
        "mathlib_revision": next(
            p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"
        ),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
