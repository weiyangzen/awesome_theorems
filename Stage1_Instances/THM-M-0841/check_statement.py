#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0841 statement."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0841"
CANONICAL = "ErdosStoneTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedEpsilonUpperBound",
    "mutationRationalTolerance",
    "mutationUniformThreshold",
    "mutationAllowsZeroTolerance",
)
TRANSPORTS = ("erdosStoneTarget_iff_expandedSourceTarget",)
BOUNDARIES = (
    "iteratedLog_zero",
    "iteratedLog_one",
    "one_part_excluded",
    "zero_tolerance_excluded",
    "one_tolerance_excluded",
)
SERIALIZATION_OPTIONS = (
    "autoImplicit=false",
    "pp.explicit=true",
    "pp.universes=true",
)
DIRECT_IMPORTS = (
    "Mathlib.Analysis.SpecialFunctions.Log.Basic",
    "Mathlib.Combinatorics.SimpleGraph.CompleteMultipartite",
)
PRINT_MARKER = f"#print {NAMESPACE}.{CANONICAL}"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_EXPRESSION_SHA256 = "ed4a8b422615bfafc69ab9f770dc99b77d308d78bca30e67790206426799a733"
FORBIDDEN = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b")


def run(
    argv: list[str], cwd: Path, timeout: int = 180
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"})
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=timeout,
    )


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return run(["lake", "env", "lean", str(path)], LEAN_DIR)


def run_text(source: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", delete=False
    ) as handle:
        handle.write(source)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def explicit_expression(declaration: str) -> tuple[str, str]:
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    source = source.replace(PRINT_MARKER, f"#print {NAMESPACE}.{declaration}")
    result = run_text(source)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    match = re.search(
        rf"def {re.escape(NAMESPACE)}\.{re.escape(declaration)} : Prop :=\n"
        rf"(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    expression = match.group("expression").strip()
    if "?m." in expression:
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return expression, result.stdout


def uncommented(source: str) -> str:
    result: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            result.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                result.append("\n")
            index += 1
        else:
            result.append(source[index])
            index += 1
    if depth:
        raise SystemExit("unterminated Lean block comment")
    return "".join(result)


def check_import_deletions(source: str) -> dict[str, dict[str, object]]:
    failures: dict[str, dict[str, object]] = {}
    for module in DIRECT_IMPORTS:
        candidate = source.replace(f"import {module}\n", "", 1)
        result = run_text(candidate)
        if result.returncode == 0:
            raise SystemExit(f"declared direct import is redundant: {module}")
        failures[module] = {
            "exit_code": result.returncode,
            "output_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        }
    return failures


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import (\S+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {imports!r}")
    if "set_option autoImplicit false" not in source:
        raise SystemExit("fixed autoImplicit option missing")
    match = FORBIDDEN.search(uncommented(source))
    if match:
        raise SystemExit(f"forbidden Lean construct: {match.group(0)}")

    expressions: dict[str, str] = {}
    outputs: dict[str, str] = {}
    for declaration in DECLARATIONS:
        expressions[declaration], outputs[declaration] = explicit_expression(declaration)
    canonical = expressions[CANONICAL]
    canonical_hash = hashlib.sha256(canonical.encode()).hexdigest()
    if canonical_hash != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit(f"canonical elaborated expression changed: {canonical_hash}")
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    for declaration in TRANSPORTS + BOUNDARIES:
        if not re.search(rf"^theorem {re.escape(declaration)}\b", source, re.MULTILINE):
            raise SystemExit(f"missing transport or boundary declaration: {declaration}")

    ordinary = run_lean(SOURCE)
    if ordinary.returncode:
        sys.stdout.write(ordinary.stdout)
        raise SystemExit(ordinary.returncode)

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit(f"unexpected mathlib revision: {mathlib_revision}")

    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib" / "Mathlib"
    import_sources = {
        "Mathlib.Analysis.SpecialFunctions.Log.Basic":
            mathlib / "Analysis/SpecialFunctions/Log/Basic.lean",
        "Mathlib.Combinatorics.SimpleGraph.CompleteMultipartite":
            mathlib / "Combinatorics/SimpleGraph/CompleteMultipartite.lean",
    }
    mathlib_root = mathlib.parent
    mathlib_tree = run(["git", "rev-parse", "HEAD^{tree}"], mathlib_root)
    if mathlib_tree.returncode:
        sys.stdout.write(mathlib_tree.stdout)
        raise SystemExit(mathlib_tree.returncode)
    lean_version = run(["lake", "env", "lean", "--version"], LEAN_DIR)
    if lean_version.returncode:
        sys.stdout.write(lean_version.stdout)
        raise SystemExit(lean_version.returncode)
    import_hashes = {
        module: hashlib.sha256(path.read_bytes()).hexdigest()
        for module, path in import_sources.items()
    }
    environment = {
        "direct_imports": [
            {"module": module, "source_sha256": import_hashes[module]}
            for module in DIRECT_IMPORTS
        ],
        "lake_manifest_sha256": hashlib.sha256(
            (LEAN_DIR / "lake-manifest.json").read_bytes()
        ).hexdigest(),
        "lean_toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "lean_version": lean_version.stdout.strip(),
        "mathlib_revision": mathlib_revision,
        "mathlib_tree": mathlib_tree.stdout.strip(),
        "namespace": NAMESPACE,
        "serialization_options": list(SERIALIZATION_OPTIONS),
        "universes": [],
    }
    serialized_environment = json.dumps(
        environment, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    )
    result = {
        "direct_import_source_sha256": {
            module: import_hashes[module] for module in DIRECT_IMPORTS
        },
        "direct_imports": list(imports),
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "environment_fingerprint": environment,
        "environment_fingerprint_sha256": hashlib.sha256(
            serialized_environment.encode()
        ).hexdigest(),
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": hashlib.sha256(ordinary.stdout.encode()).hexdigest(),
        "mathlib_revision": mathlib_revision,
        "minimal_import_deletion_failures": check_import_deletions(source),
        "mutation_expression_sha256": {
            name: hashlib.sha256(expressions[name].encode()).hexdigest()
            for name in DECLARATIONS[1:]
        },
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "transports": list(TRANSPORTS),
        "validated_boundaries": list(BOUNDARIES),
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
