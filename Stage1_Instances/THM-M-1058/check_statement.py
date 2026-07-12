#!/usr/bin/env python3
"""Elaborate THM-M-1058 and distinguish its four structural mutations."""

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
NAMESPACE = "Stage1Instances.THM_M_1058"
DECLARATIONS = [
    "LargeDeviationPrinciple",
    "mutationRemovedHypothesis",
    "mutationChangedDomain",
    "mutationChangedBinderScope",
    "mutationWeakLDP",
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
    text = SOURCE.read_text()
    marker = f"#print {NAMESPACE}.LargeDeviationPrinciple"
    text = text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    match = re.search(r"^(?:def|structure) .*", output, re.MULTILINE | re.DOTALL)
    if not match:
        raise SystemExit(f"could not extract expression for {declaration}")
    return match.group(0).strip()


def normalize(text: str, declaration: str) -> str:
    return text.replace(f"{NAMESPACE}.{declaration}", f"{NAMESPACE}.MUTATION")


def main() -> None:
    expressions = {name: printed(name) for name in DECLARATIONS}
    canonical = normalize(expressions[DECLARATIONS[0]], DECLARATIONS[0])
    survivors = [
        name for name in DECLARATIONS[1:]
        if normalize(expressions[name], name) == canonical
    ]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    payload = {
        "statement_sha256": hashlib.sha256(expressions[DECLARATIONS[0]].encode()).hexdigest(),
        "killed_mutations": DECLARATIONS[1:],
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text().strip(),
        "mathlib_revision": next(
            package["rev"] for package in manifest["packages"]
            if package["name"] == "mathlib"
        ),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
