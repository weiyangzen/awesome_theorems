#!/usr/bin/env python3
"""Validate the frozen THM-M-0814 statement and structural mutations."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0814"
CANONICAL = "MaxFlowMinCutTarget"
MUTATIONS = [
    "mutationRemovedPositiveCapacity",
    "mutationNaturalCapacityDomain",
    "mutationExistentialNetwork",
    "mutationRequiresSourceSinkChain",
]
DIRECT_IMPORTS = [
    "Mathlib.Algebra.BigOperators.Finsupp.Basic",
    "Mathlib.Combinatorics.Graph.Basic",
    "Mathlib.Data.NNReal.Defs",
]
SERIALIZED_DECLARATIONS = [
    "Chain",
    "HasTerminals",
    "HasPositiveCapacities",
    "arcLoad",
    "flowValue",
    "IsFeasible",
    "IsDisconnecting",
    "cutValue",
    CANONICAL,
]


def run_lean(source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )


def elaborate(source: Path) -> str:
    result = run_lean(source)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def expression(declaration: str) -> tuple[str, str]:
    source_text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if source_text.count(marker) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
    source_text = source_text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    temporary = SOURCE.parent / f".statement-check-{declaration}.lean"
    temporary.write_text(source_text, encoding="utf-8")
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    marker_pattern = rf"(?:def|structure) {re.escape(NAMESPACE)}\.{re.escape(declaration)}"
    match = re.search(marker_pattern, output)
    if not match:
        raise SystemExit(f"could not locate serialized declaration {declaration}")
    serialized = output[match.start():].strip()
    if "?m." in serialized:
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return serialized, output


def check_minimal_imports(source_text: str) -> dict[str, dict[str, str | int]]:
    actual_imports = [
        line.removeprefix("import ")
        for line in source_text.splitlines()
        if line.startswith("import ")
    ]
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {actual_imports}")

    failures = {}
    for module in DIRECT_IMPORTS:
        candidate = source_text.replace(f"import {module}\n", "", 1)
        suffix = module.rsplit(".", 1)[-1]
        temporary = SOURCE.parent / f".statement-check-no-{suffix}.lean"
        temporary.write_text(candidate, encoding="utf-8")
        try:
            result = run_lean(temporary)
        finally:
            temporary.unlink()
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {module}")
        failures[module] = {
            "exit_code": result.returncode,
            "output_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        }
    return failures


def check_forbidden_constructs(source_text: str) -> None:
    without_comments = re.sub(r"/-.*?-/", "", source_text, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b")
    match = forbidden.search(without_comments)
    if match:
        raise SystemExit(f"forbidden Lean construct: {match.group(0)}")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)
    import_failures = check_minimal_imports(source_text)

    serialized = {}
    outputs = {}
    for declaration in [*SERIALIZED_DECLARATIONS, *MUTATIONS]:
        serialized[declaration], outputs[declaration] = expression(declaration)
    canonical = serialized[CANONICAL]
    survivors = [name for name in MUTATIONS if serialized[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    component_bundle = "\n\n".join(
        serialized[name] for name in SERIALIZED_DECLARATIONS
    )
    payload = {
        "direct_imports": DIRECT_IMPORTS,
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "statement_bundle_sha256": hashlib.sha256(component_bundle.encode()).hexdigest(),
        "component_expression_sha256": {
            name: hashlib.sha256(serialized[name].encode()).hexdigest()
            for name in SERIALIZED_DECLARATIONS
        },
        "killed_mutations": MUTATIONS,
        "lean_output_sha256": hashlib.sha256(outputs[CANONICAL].encode()).hexdigest(),
        "mathlib_revision": mathlib_revision,
        "minimal_import_deletion_failures": import_failures,
        "mutation_expression_sha256": {
            name: hashlib.sha256(serialized[name].encode()).hexdigest()
            for name in MUTATIONS
        },
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
