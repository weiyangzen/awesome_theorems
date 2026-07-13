#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0063 statement."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0063"
THEOREM_ID = "THM-M-0063"
ITEM_ID = "S56-M-0063-STATEMENT"
CANONICAL = "CayleyTheoremTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationChangedDomain",
    "mutationChangedBinderScope",
    "mutationExcludedTrivialBoundary",
)
BOUNDARIES = ("trivialGroupBoundary", "infiniteCarrierBoundary")
TRANSPORTS = ("cayleyTheoremTarget_implies_permutationSubgroupExistenceTarget",)
DIRECT_IMPORTS = (
    "Mathlib.Algebra.Group.Action.End",
    "Mathlib.Algebra.Group.Subgroup.Ker",
)
PRINT_MARKER = "#print CayleyTheoremTarget"
EXPECTED_EXPRESSION_SHA256 = "40929846f1d1d1ff4479e5be6a989358a65ecebec5a2646f6e2dab508c641a1a"
EXPECTED_STATEMENT_FILE_SHA256 = "37e52256a1a3d1e5e56a00888309b208d7f2c2ee1b45932ac761c5f01e3bf950"
EXPECTED_LEAN_OUTPUT_SHA256 = "b5c7b70bae870c3881ad32b69b308dffe81b4419507772bde45818b26d6fe9f1"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROHIBITED_PATTERN = (
    r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b|"
    r"\b(TODO|FIXME|placeholder)\b"
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def run_text(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def elaborate_expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    if text.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    text = text.replace(PRINT_MARKER, f"#print {declaration}")
    result = run_text(text)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified}(?:\.\{{[^}}]+\}})? : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def import_deletion_fails(source_text: str, module_name: str) -> bool:
    reduced = source_text.replace(f"import {module_name}\n", "")
    result = run_text(reduced)
    return result.returncode != 0


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    owned_text_paths = [path for path in SOURCE.parent.iterdir() if path.is_file()]
    owned_text_paths.append(ROOT / ".stage1-worker-selftest.json")
    for path in owned_text_paths:
        data = path.read_bytes()
        if data and not data.endswith(b"\n"):
            raise SystemExit(f"missing final newline: {path}")
        for line_number, line in enumerate(data.splitlines(), start=1):
            if line.rstrip(b" \t") != line:
                raise SystemExit(f"trailing whitespace: {path}:{line_number}")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["depends_on"] != ["S56-M-0063-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    expressions: dict[str, str] = {}
    canonical_output = ""
    for declaration in DECLARATIONS:
        expression, output = elaborate_expression(declaration)
        expressions[declaration] = expression
        if declaration == CANONICAL:
            canonical_output = output
    canonical = expressions[CANONICAL]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    if "failed to synthesize instance of type class\n  Group G" not in canonical_output:
        raise SystemExit("removed-Group-hypothesis mutation did not fail as expected")
    if "Unknown constant `Equiv.Perm.subgroupOfMulAction`" not in canonical_output:
        raise SystemExit("proof-bearing anchor unexpectedly entered the statement import closure")
    for name in BOUNDARIES + TRANSPORTS:
        if not re.search(rf"^(theorem|def) {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing boundary or transport declaration: {name}")
    prohibited = re.compile(PROHIBITED_PATTERN)
    for lean_path in SOURCE.parent.glob("*.lean"):
        match = prohibited.search(lean_path.read_text(encoding="utf-8"))
        if match:
            raise SystemExit(f"prohibited token in {lean_path.name}: {match.group(0)}")

    deletion_failures = {
        module_name: import_deletion_fails(source_text, module_name)
        for module_name in DIRECT_IMPORTS
    }
    if not all(deletion_failures.values()):
        survivors = [name for name, failed in deletion_failures.items() if not failed]
        raise SystemExit(f"direct import survived deletion: {', '.join(survivors)}")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    expected = (
        (EXPECTED_EXPRESSION_SHA256, expression_hash, "elaborated expression"),
        (EXPECTED_STATEMENT_FILE_SHA256, statement_file_hash, "statement source"),
        (EXPECTED_LEAN_OUTPUT_SHA256, lean_output_hash, "canonical Lean output"),
    )
    for recorded, actual, label in expected:
        if recorded != "TO_BE_RECONCILED" and recorded != actual:
            raise SystemExit(f"{label} changed without reconciliation")

    toolchain_path = LEAN_DIR / "lean-toolchain"
    manifest_path = LEAN_DIR / "lake-manifest.json"
    manifest = load(manifest_path)
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    if toolchain_path.read_text(encoding="utf-8").strip() != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain pin changed")
    if sha256_bytes(toolchain_path.read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("toolchain file changed")
    if sha256_bytes(manifest_path.read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("Lake manifest changed")
    actual_revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip()
    actual_tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip()
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("manifest mathlib revision changed")
    if (actual_revision, actual_tree) != (EXPECTED_MATHLIB_REVISION, EXPECTED_MATHLIB_TREE):
        raise SystemExit("pinned mathlib checkout changed")

    structured_paths = (
        SOURCE.with_name("statement.json"),
        SOURCE.with_name("statement-receipt.json"),
        ROOT / ".stage1-worker-selftest.json",
    )
    if all(path.exists() for path in structured_paths):
        statement, receipt, packet = map(load, structured_paths)
        instance = load(SOURCE.with_name("instance.json"))
        formal = statement["canonical_formal_target"]
        if formal["elaborated_expression_sha256"] != expression_hash:
            raise SystemExit("structured statement expression fingerprint is stale")
        if formal["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("structured statement source fingerprint is stale")
        if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
            raise SystemExit("receipt expression fingerprint is stale")
        if receipt["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("receipt statement source fingerprint is stale")
        if receipt["lean_output_sha256"] != lean_output_hash:
            raise SystemExit("receipt Lean-output fingerprint is stale")
        if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
            raise SystemExit("statement direct-import record is stale")
        if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
            raise SystemExit("receipt direct-import record is stale")
        if instance["canonical_formal_target"]["elaborated_expression_hash"] != (
            f"sha256:{expression_hash}"
        ):
            raise SystemExit("instance expression fingerprint is stale")
        if receipt["base_revision"] != subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip():
            raise SystemExit("receipt base revision is stale")
        packet_fields = {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        if set(packet) != packet_fields:
            raise SystemExit("worker packet fields changed")
        if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet identity changed")
        if packet["base_revision"] != receipt["base_revision"]:
            raise SystemExit("worker packet base revision is stale")
        if packet["changed_paths"] != receipt["changed_paths"]:
            raise SystemExit("worker packet changed paths are stale")
        if packet["known_failures"] != receipt["known_failures"]:
            raise SystemExit("worker packet known failures are stale")
        actual_changed = {
            line[3:] for line in subprocess.check_output(
                ["git", "status", "--short", "--untracked-files=all"],
                cwd=ROOT,
                text=True,
            ).splitlines()
        }
        if set(receipt["changed_paths"]) != actual_changed - {"Formalizations/Lean/.lake"}:
            raise SystemExit("receipt changed paths do not match scoped git status")
        historical_validation = SOURCE.with_name("validation.md").read_text(encoding="utf-8")
        if "Historical intake" not in historical_validation or "not cited" not in historical_validation:
            raise SystemExit("historical intake validation boundary is stale")

    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "import_deletion_failures": deletion_failures,
        "killed_mutations": ["removedGroupHypothesis", *DECLARATIONS[1:]],
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
        "transports": list(TRANSPORTS),
        "validated_boundaries": list(BOUNDARIES),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
