#!/usr/bin/env python3
"""Elaborate THM-M-0085 and reject four structural statement mutations."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1.THM_M_0085"
DECLARATIONS = [
    "Statement",
    "mutationRemovedCreatesHypothesis",
    "mutationChangedDomain",
    "mutationChangedBinderScope",
    "mutationExcludeEmptyRightCategory",
]


def elaborate(source: Path) -> str:
    result = subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    return result.stdout


def expression(declaration: str) -> str:
    text = SOURCE.read_text()
    marker = "#print Statement"
    text = text.replace(marker, f"#print {declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    pattern = rf"def {re.escape(NAMESPACE)}\.{re.escape(declaration)}.*? : Prop :=\n(?P<expression>.*)\Z"
    match = re.search(pattern, output, re.DOTALL)
    if not match:
        raise SystemExit(f"could not extract expression for {declaration}")
    return match.group("expression").strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    expressions = {name: expression(name) for name in DECLARATIONS}
    canonical = expressions["Statement"]
    survivors = [
        name for name in DECLARATIONS[1:] if expressions[name] == canonical
    ]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    environment_inputs = [
        LEAN_DIR / "lean-toolchain",
        LEAN_DIR / "lakefile.lean",
        LEAN_DIR / "lake-manifest.json",
        SOURCE,
    ]
    environment = "\n".join(
        f"{path.relative_to(ROOT)}:{sha256(path)}" for path in environment_inputs
    )
    payload = {
        "elaborated_expression_sha256": hashlib.sha256(
            canonical.encode()
        ).hexdigest(),
        "environment_fingerprint_sha256": hashlib.sha256(
            environment.encode()
        ).hexdigest(),
        "killed_mutations": DECLARATIONS[1:],
        "mathlib_revision": next(
            package["rev"]
            for package in manifest["packages"]
            if package["name"] == "mathlib"
        ),
        "statement_file_sha256": sha256(SOURCE),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text().strip(),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
