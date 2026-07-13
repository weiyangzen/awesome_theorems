#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0276 statement."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0276"
THEOREM_ID = "THM-M-0276"
ITEM_ID = "S56-M-0276-STATEMENT"
CANONICAL = "BanachOpenMappingTarget"
FINGERPRINT_DECLARATION = "ExpandedOpenMappingTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedSurjectivityHypothesis",
    "mutationChangedScalarDomain",
    "mutationChangedBinderScope",
    "mutationDroppedDomainCompleteness",
    "mutationExcludedNoninjectiveBoundary",
)
DIRECT_IMPORTS = ("Mathlib.Analysis.Complex.Basic",)
PRINT_MARKER = "#print BanachOpenMappingTarget"
EXPECTED_EXPRESSION_SHA256 = "ec2954c0a55ee364e73f3b49407d1ef62ba1ff03807b1e53771181ef27f04d80"
EXPECTED_EXPANDED_EXPRESSION_SHA256 = "0cfb9796471903d081ad67551a3f9c2c3414cce1f7adbf79394d364a467c82fa"
EXPECTED_STATEMENT_FILE_SHA256 = "ede62e0c7bbf3804f6a81c2f1115643048c69ced4750453af7e8ebd845c6aeea"
EXPECTED_LEAN_OUTPUT_SHA256 = "073326d6b764f93cff948bb4c23fc5fb9624edc8411227dfb8433a48a6182aae"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_IMPORT_SHA256 = "2233a892e4a9cbdc9250806652511d921b081773edf6f33e94e5652bb49f1b93"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )


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


def elaborate_expression(declaration: str) -> tuple[str, str]:
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    source = source.replace(PRINT_MARKER, f"#print {declaration}")
    result = run_text(source)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified}\.\{{u, v\}} : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {imports!r}")

    deletion = run_text(source.replace(f"import {DIRECT_IMPORTS[0]}\n", "", 1))
    if deletion.returncode == 0:
        raise SystemExit("the sole direct import is redundant")
    if "Unknown identifier `NormedAddCommGroup`" not in deletion.stdout:
        raise SystemExit("the no-import failure boundary changed")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0276-INTAKE"]:
        raise SystemExit("authoritative statement state or dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    root_expression, _ = elaborate_expression(CANONICAL)
    if sha256_bytes(root_expression.encode("utf-8")) != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit("named root expression fingerprint changed")

    fingerprint_declarations = (FINGERPRINT_DECLARATION, *DECLARATIONS[1:])
    expressions: dict[str, str] = {}
    for declaration in fingerprint_declarations:
        expression, output = elaborate_expression(declaration)
        expressions[declaration] = expression
    canonical = expressions[FINGERPRINT_DECLARATION]
    if len(set(expressions.values())) != len(expressions):
        raise SystemExit("a statement mutation shares an explicit expression with another target")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    if EXPECTED_EXPANDED_EXPRESSION_SHA256 != "TO_BE_RECONCILED" and (
        expression_hash != EXPECTED_EXPANDED_EXPRESSION_SHA256
    ):
        raise SystemExit("expanded expression fingerprint changed without reconciliation")
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_run = run_lean(SOURCE)
    if lean_run.returncode:
        print(lean_run.stdout, end="")
        raise SystemExit(lean_run.returncode)
    lean_output_hash = sha256_bytes(lean_run.stdout.encode("utf-8"))
    expected = {
        "statement": EXPECTED_STATEMENT_FILE_SHA256,
        "output": EXPECTED_LEAN_OUTPUT_SHA256,
    }
    actual = {
        "statement": statement_file_hash,
        "output": lean_output_hash,
    }
    for kind, value in expected.items():
        if value != "TO_BE_RECONCILED" and value != actual[kind]:
            raise SystemExit(f"{kind} fingerprint changed without reconciliation")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    dag = load(SOURCE.with_name("task-dag.json"))
    if statement["item_id"] != receipt["item_id"] or receipt["item_id"] != ITEM_ID:
        raise SystemExit("statement item identity is stale")
    if statement["theorem_id"] != receipt["theorem_id"] or receipt["theorem_id"] != THEOREM_ID:
        raise SystemExit("statement theorem identity is stale")
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("structured expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("structured source fingerprint is stale")
    if formal["named_root_expression_sha256"] != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit("structured named-root fingerprint is stale")
    serialization = formal["expression_serialization"]
    if serialization["declaration"] != f"{NAMESPACE}.{FINGERPRINT_DECLARATION}":
        raise SystemExit("structured serialization declaration is stale")
    if serialization["sha256"] != expression_hash:
        raise SystemExit("structured serialization fingerprint is stale")
    if statement["direct_imports"] != receipt["direct_imports"] or tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("structured import record is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("receipt source fingerprint is stale")
    if receipt["named_root_expression_sha256"] != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit("receipt named-root fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    if receipt["root_vector_before"] != receipt["root_vector_after"] or receipt["root_vector_after"] != instance["root_vector"]:
        raise SystemExit("statement debt vector is inconsistent")
    if receipt["accepted"] or receipt["audit_complete"] or receipt["theorem_complete"]:
        raise SystemExit("statement receipt overclaims acceptance or completion")
    instance_formal = instance["canonical_formal_target"]
    if instance_formal["module"] != f"Stage1_Instances/{THEOREM_ID}/Statement.lean":
        raise SystemExit("instance canonical module is stale")
    if instance_formal["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("instance canonical declaration is stale")
    if instance_formal["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    statement_task = next(task for task in dag["tasks"] if task["id"] == ITEM_ID)
    if statement_task["state"] != "open" or statement_task["depends_on"] != ["S56-M-0276-INTAKE"]:
        raise SystemExit("local statement task boundary changed")

    toolchain = LEAN_DIR / "lean-toolchain"
    manifest_path = LEAN_DIR / "lake-manifest.json"
    if toolchain.read_text(encoding="utf-8").strip() != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain changed")
    if sha256_bytes(toolchain.read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("Lean toolchain fingerprint changed")
    if sha256_bytes(manifest_path.read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("lake manifest fingerprint changed")
    manifest = load(manifest_path)
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("mathlib manifest revision changed")
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, check=True, text=True,
        capture_output=True,
    ).stdout.strip()
    if tree != EXPECTED_MATHLIB_TREE:
        raise SystemExit("mathlib tree changed")
    import_path = mathlib / "Mathlib/Analysis/Complex/Basic.lean"
    if sha256_bytes(import_path.read_bytes()) != EXPECTED_IMPORT_SHA256:
        raise SystemExit("direct import source changed")

    payload = {
        "deletion_failure": "no imports: unknown NormedAddCommGroup",
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "killed_mutations": list(DECLARATIONS[1:]),
        "named_root_expression_sha256": EXPECTED_EXPRESSION_SHA256,
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
