#!/usr/bin/env python3
"""Elaborate THM-M-0043 and distinguish its four structural mutations."""

from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0043"
DECLARATIONS = [
    "SpectralTheoremTarget",
    "mutationRemovedNormalityHypothesis",
    "mutationChangedScalarDomain",
    "mutationChangedBinderScope",
    "mutationIncludedEmptyBoundary",
]
EXPECTED_STATEMENT_SHA256 = "a46ee23911b8027aa5de93149fd781def441429e386cb9181fc2064b2898557a"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def elaborate(source: Path) -> str:
    result = subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def expression(declaration: str) -> str:
    text = SOURCE.read_text(encoding="utf-8")
    marker = "#print SpectralTheoremTarget"
    replacement = f"#print {declaration}"
    if marker not in text:
        raise SystemExit("canonical #print marker missing")
    text = text.replace(marker, replacement, 1)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    match = re.search(rf"def {re.escape(NAMESPACE)}\.{declaration}\.\{{u\}} : Prop :=\n(?P<expression>.*)\Z", output, re.DOTALL)
    if not match:
        raise SystemExit(f"could not extract expression for {declaration}")
    return match.group("expression").strip()


def main() -> None:
    expressions = {name: expression(name) for name in DECLARATIONS}
    canonical = expressions[DECLARATIONS[0]]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    statement_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
    if statement_sha256 != EXPECTED_STATEMENT_SHA256:
        raise SystemExit(f"canonical expression drifted: {statement_sha256}")

    imports = re.findall(r"^import (\S+)$", SOURCE.read_text(encoding="utf-8"), re.MULTILINE)
    if imports != ["Mathlib.Data.Complex.Basic", "Mathlib.LinearAlgebra.UnitaryGroup"]:
        raise SystemExit(f"unexpected direct imports: {imports}")

    minimality_failures = []
    for direct_import in imports:
        text = SOURCE.read_text(encoding="utf-8").replace(f"import {direct_import}\n", "", 1)
        with tempfile.NamedTemporaryFile(
            "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
        ) as handle:
            handle.write(text)
            temporary = Path(handle.name)
        try:
            result = subprocess.run(
                ["lake", "env", "lean", str(temporary)],
                cwd=LEAN_DIR,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        finally:
            temporary.unlink()
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant for this target module: {direct_import}")
        minimality_failures.append(direct_import)

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit(f"unexpected mathlib revision: {mathlib_revision}")
    payload = {
        "statement_sha256": statement_sha256,
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "lean_output_sha256": hashlib.sha256(elaborate(SOURCE).encode()).hexdigest(),
        "killed_mutations": DECLARATIONS[1:],
        "minimal_direct_imports": imports,
        "removing_each_direct_import_failed": minimality_failures,
        "lean_executable": str(Path(shutil.which("lean") or "lean").resolve()),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "mathlib_revision": mathlib_revision,
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
