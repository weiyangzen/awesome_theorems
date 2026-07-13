#!/usr/bin/env python3
"""Validate the frozen THM-M-0957 statement, transports, imports, and mutations."""

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
NAMESPACE = "Stage1Instances.THM_M_0957"
CANONICAL = "BehrendConstructionTarget"
SERIALIZED_DECLARATIONS = [
    "SourceThreeAPFree",
    CANONICAL,
    "BehrendFiniteSetTarget",
]
MUTATIONS = [
    "mutationRemovedPositiveEpsilon",
    "mutationRationalEpsilon",
    "mutationUniformThreshold",
    "mutationExclusiveInterval",
]
DIRECT_IMPORTS = [
    "Mathlib.Analysis.SpecialFunctions.Pow.Real",
    "Mathlib.Combinatorics.Additive.AP.Three.Defs",
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


def serialized_expression(declaration: str) -> tuple[str, str]:
    source_text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if source_text.count(marker) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
    source_text = source_text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", delete=False
    ) as handle:
        handle.write(source_text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()

    match = re.search(
        rf"def {re.escape(NAMESPACE)}\.{re.escape(declaration)}\b", output
    )
    if not match:
        raise SystemExit(f"could not locate serialized declaration {declaration}")
    printed = output[match.start() :].strip()
    assignment = ":=\n"
    if assignment not in printed:
        raise SystemExit(f"could not isolate expression for {declaration}")
    serialized = printed.split(assignment, 1)[1].strip()
    for boundary in (
        "\nType mismatch\n",
        "\n'Stage1Instances.THM_M_0957.sourceThreeAPFree_iff_threeAPFree'",
    ):
        serialized = serialized.split(boundary, 1)[0].strip()
    if "?m." in serialized or "sorryAx" in serialized:
        raise SystemExit(f"invalid elaboration residue in {declaration}")
    return serialized, output


def check_minimal_imports(source_text: str) -> dict[str, dict[str, str | int]]:
    actual = [
        line.removeprefix("import ")
        for line in source_text.splitlines()
        if line.startswith("import ")
    ]
    if actual != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {actual}")

    failures = {}
    for module in DIRECT_IMPORTS:
        candidate = source_text.replace(f"import {module}\n", "", 1)
        with tempfile.NamedTemporaryFile(
            "w", suffix=".lean", encoding="utf-8", delete=False
        ) as handle:
            handle.write(candidate)
            temporary = Path(handle.name)
        try:
            result = run_lean(temporary)
        finally:
            temporary.unlink()
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {module}")
        if "unknown module prefix 'Mathlib'" in result.stdout:
            raise SystemExit(
                f"import deletion failed only because the Mathlib root disappeared: {module}"
            )
        failures[module] = {
            "exit_code": result.returncode,
            "output_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        }
    return failures


def check_target_imports(
    source_text: str,
) -> tuple[dict[str, dict[str, str | int]], str]:
    """Check deletion-minimality for the canonical target before transport proofs."""
    transport_marker = "/-- The source's literal nontrivial-progression exclusion"
    namespace_marker = "namespace Stage1Instances.THM_M_0957"
    target_marker = "/-- Direct finite-set form of the same historical claim."
    if source_text.count(transport_marker) != 1 or source_text.count(target_marker) != 1:
        raise SystemExit("target-only fixture markers are missing or ambiguous")
    fixture = source_text.split(transport_marker, 1)[0]
    namespace_and_target = source_text.split(namespace_marker, 1)[1]
    canonical_block = namespace_and_target.split(target_marker, 1)[0]
    canonical_block = canonical_block.split(
        "/-- The historical Behrend claim", 1
    )[1]
    fixture += (
        "/-- The historical Behrend claim"
        f"{canonical_block}\n"
        "end Stage1Instances.THM_M_0957\n"
    )

    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", delete=False
    ) as handle:
        handle.write(fixture)
        complete_fixture = Path(handle.name)
    try:
        complete_result = run_lean(complete_fixture)
    finally:
        complete_fixture.unlink()
    if complete_result.returncode:
        sys.stdout.write(complete_result.stdout)
        raise SystemExit("canonical-target import fixture does not elaborate")

    failures = {}
    for module in DIRECT_IMPORTS:
        candidate = fixture.replace(f"import {module}\n", "", 1)
        with tempfile.NamedTemporaryFile(
            "w", suffix=".lean", encoding="utf-8", delete=False
        ) as handle:
            handle.write(candidate)
            temporary = Path(handle.name)
        try:
            result = run_lean(temporary)
        finally:
            temporary.unlink()
        if result.returncode == 0:
            raise SystemExit(f"canonical-target direct import is redundant: {module}")
        if "unknown module prefix 'Mathlib'" in result.stdout:
            raise SystemExit(
                f"target import deletion failed only because Mathlib disappeared: {module}"
            )
        failures[module] = {
            "exit_code": result.returncode,
            "output_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        }
    return failures, hashlib.sha256(complete_result.stdout.encode()).hexdigest()


def check_forbidden_constructs(source_text: str) -> None:
    without_comments = re.sub(r"/-.*?-/", "", source_text, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b"
    )
    match = forbidden.search(without_comments)
    if match:
        raise SystemExit(f"forbidden Lean construct: {match.group(0)}")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)
    import_failures = check_minimal_imports(source_text)
    target_import_failures, target_fixture_output_sha256 = check_target_imports(
        source_text
    )

    serialized = {}
    outputs = {}
    for declaration in [*SERIALIZED_DECLARATIONS, *MUTATIONS]:
        serialized[declaration], outputs[declaration] = serialized_expression(declaration)
    canonical = serialized[CANONICAL]
    survivors = [name for name in MUTATIONS if serialized[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    direct_run = elaborate(SOURCE)
    if "sorryAx" in direct_run:
        raise SystemExit("statement transport depends on sorryAx")
    for expected_axioms in (
        "'Stage1Instances.THM_M_0957.sourceThreeAPFree_iff_threeAPFree' depends on axioms: [propext]",
        "'Stage1Instances.THM_M_0957.behrendConstructionTarget_iff_finiteSet' depends on axioms: [propext,\n Classical.choice,\n Quot.sound]",
    ):
        if expected_axioms not in direct_run:
            raise SystemExit("unexpected checked-transport axiom report")

    manifest = json.loads(
        (LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8")
    )
    mathlib_revision = next(
        package["rev"]
        for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    bundle = "\n\n".join(serialized[name] for name in SERIALIZED_DECLARATIONS)
    payload = {
        "component_expression_sha256": {
            name: hashlib.sha256(serialized[name].encode()).hexdigest()
            for name in SERIALIZED_DECLARATIONS
        },
        "direct_imports": DIRECT_IMPORTS,
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": MUTATIONS,
        "lean_output_sha256": hashlib.sha256(direct_run.encode()).hexdigest(),
        "mathlib_revision": mathlib_revision,
        "minimal_import_deletion_failures": import_failures,
        "canonical_target_import_deletion_failures": target_import_failures,
        "canonical_target_fixture_output_sha256": target_fixture_output_sha256,
        "mutation_expression_sha256": {
            name: hashlib.sha256(serialized[name].encode()).hexdigest()
            for name in MUTATIONS
        },
        "statement_bundle_sha256": hashlib.sha256(bundle.encode()).hexdigest(),
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
