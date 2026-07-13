#!/usr/bin/env python3
"""Fail-closed statement-gate checks for S56-M-0626-STATEMENT."""

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
NAMESPACE = "Stage1Instances.THM_M_0626"
CANONICAL = "ConnectedImageTarget"
EXPANSION = "ExpandedConnectedImageTarget"
LOCAL_ALTERNATE = "ContinuousOnConnectedImageTarget"
TRANSPORT = "continuousOnTarget_implies_connectedImageTarget"
MUTATIONS = [
    "mutationRemovedConnectedness",
    "mutationRemovedContinuity",
    "mutationChangedDomain",
    "mutationChangedBinderScope",
    "mutationAllowsEmptySource",
]
EXPECTED_IMPORTS = ["Mathlib.Topology.Connected.Basic"]
SERIALIZATION_OPTIONS = ["pp.explicit=true", "pp.universes=true"]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run(
    argv: list[str], cwd: Path, timeout: int = 120
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
        timeout=timeout,
        check=False,
    )


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return run(["lake", "env", "lean", str(path)], LEAN_DIR)


def strip_lean_comments(text: str) -> str:
    """Remove nested block and line comments before scanning declarations."""
    result: list[str] = []
    index = 0
    depth = 0
    while index < len(text):
        if depth == 0 and text.startswith("--", index):
            newline = text.find("\n", index)
            if newline < 0:
                break
            result.append("\n")
            index = newline + 1
        elif text.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and text.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if text[index] == "\n":
                result.append("\n")
            index += 1
        else:
            result.append(text[index])
            index += 1
    if depth:
        raise SystemExit("unterminated Lean block comment")
    return "".join(result)


def explicit_expression(declaration: str) -> str:
    text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if text.count(marker) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    text = text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        result = run_lean(temporary)
    finally:
        temporary.unlink()
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified}(?:\.\{{[^\n]+\}})? : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not serialize explicit expression for {declaration}")
    expression = match.group("expression").strip()
    if re.search(r"\?m\.|syntheticOpaque|syntheticSorry", expression):
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return expression


def import_deletion_failures(source_text: str) -> dict[str, str]:
    import_lines = [
        line for line in source_text.splitlines() if line.startswith("import ")
    ]
    actual = [line.removeprefix("import ") for line in import_lines]
    if actual != EXPECTED_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {actual!r}")
    failures: dict[str, str] = {}
    for line, module in zip(import_lines, actual, strict=True):
        candidate = source_text.replace(line + "\n", "", 1)
        with tempfile.NamedTemporaryFile(
            "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
        ) as handle:
            handle.write(candidate)
            temporary = Path(handle.name)
        try:
            result = run_lean(temporary)
        finally:
            temporary.unlink()
        if result.returncode == 0:
            raise SystemExit(f"redundant direct import: {module}")
        failures[module] = "Lean rejected the import-deletion fixture as expected"
    return failures


def checked_output(name: str, result: subprocess.CompletedProcess[str]) -> str:
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(f"{name} failed with exit {result.returncode}")
    return result.stdout.strip()


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    code = strip_lean_comments(source_text)
    if re.search(r"\b(?:s[o]rry|a[d]mit|a[x]iom|o[p]aque|u[n]safe)\b|sorryAx", code):
        raise SystemExit("forbidden proof gap or trust-broadening declaration")
    for required in [CANONICAL, EXPANSION, LOCAL_ALTERNATE, TRANSPORT, *MUTATIONS]:
        if required not in code:
            raise SystemExit(f"required declaration missing: {required}")
    if code.count("#check_failure") != len(MUTATIONS):
        raise SystemExit("each structural mutation must have one #check_failure identity test")

    baseline = run_lean(SOURCE)
    baseline_output = checked_output("canonical Lean elaboration", baseline)
    if baseline_output.count("Type mismatch") != len(MUTATIONS):
        raise SystemExit("not every mutation produced the expected #check_failure diagnostic")
    expected_axiom_results = {
        "connectedImageTarget_iff_expanded": "does not depend on any axioms",
        TRANSPORT: "depends on axioms: [propext, Classical.choice, Quot.sound]",
    }
    normalized_output = re.sub(r"\s+", " ", baseline_output)
    for declaration, result in expected_axiom_results.items():
        expected = f"'{NAMESPACE}.{declaration}' {result}"
        if expected not in normalized_output:
            raise SystemExit(f"unexpected wrapper axiom result: missing {expected!r}")

    expressions = {
        name: explicit_expression(name) for name in [CANONICAL, *MUTATIONS]
    }
    canonical = expressions[CANONICAL]
    survivors = [name for name in MUTATIONS if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    manifest_mathlib = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    mathlib_dir = LEAN_DIR / ".lake" / "packages" / "mathlib"
    mathlib_revision = checked_output(
        "mathlib revision", run(["git", "rev-parse", "HEAD"], mathlib_dir)
    )
    mathlib_tree = checked_output(
        "mathlib tree", run(["git", "rev-parse", "HEAD^{tree}"], mathlib_dir)
    )
    mathlib_status = checked_output(
        "mathlib status", run(["git", "status", "--short"], mathlib_dir)
    )
    if mathlib_revision != manifest_mathlib:
        raise SystemExit("mathlib worktree revision disagrees with lake-manifest.json")
    if mathlib_status:
        raise SystemExit("pinned mathlib worktree is dirty")

    lean_version = checked_output(
        "Lean version", run(["lake", "env", "lean", "--version"], LEAN_DIR)
    )
    import_records = []
    for module in EXPECTED_IMPORTS:
        path = mathlib_dir / (module.replace(".", "/") + ".lean")
        if not path.is_file():
            raise SystemExit(f"direct import source missing: {path}")
        import_records.append(
            {"module": module, "source_sha256": sha256_file(path)}
        )

    environment = {
        "lean_toolchain": (LEAN_DIR / "lean-toolchain").read_text().strip(),
        "lean_version": lean_version,
        "lake_manifest_sha256": sha256_file(LEAN_DIR / "lake-manifest.json"),
        "mathlib_revision": mathlib_revision,
        "mathlib_tree": mathlib_tree,
        "direct_imports": import_records,
        "serialization_options": SERIALIZATION_OPTIONS,
        "namespace": NAMESPACE,
        "universes": ["u", "v"],
    }
    environment_serialized = json.dumps(
        environment, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    )
    payload = {
        "schema_version": "stage1-statement-check/1.0",
        "item_id": "S56-M-0626-STATEMENT",
        "theorem_id": "THM-M-0626",
        "canonical_declaration": f"{NAMESPACE}.{CANONICAL}",
        "elaborated_expression": canonical,
        "elaborated_expression_sha256": sha256_bytes(canonical.encode("utf-8")),
        "environment_fingerprint": environment,
        "environment_fingerprint_sha256": sha256_bytes(
            environment_serialized.encode("utf-8")
        ),
        "statement_file_sha256": sha256_file(SOURCE),
        "checker_file_sha256": sha256_file(Path(__file__)),
        "lean_output_sha256": sha256_bytes(baseline.stdout.encode("utf-8")),
        "killed_mutations": MUTATIONS,
        "minimal_import_deletion_failures": import_deletion_failures(source_text),
        "wrapper_axiom_results": expected_axiom_results,
        "unresolved_metavariables": False,
        "placeholder_scan": "clean",
    }
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
