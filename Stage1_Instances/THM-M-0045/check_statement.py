#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0045 statement."""

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
BOUNDARY = Path(__file__).with_name("BoundaryProbe.lean")
THEOREM_ID = "THM-M-0045"
ITEM_ID = "S56-M-0045-STATEMENT"
NAMESPACE = "Stage1Instances.THM_M_0045"
CANONICAL = "SchurTriangularizationTarget"
PRINT_MARKER = f"#print {CANONICAL}"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedUnitarity",
    "mutationChangedDomainToRational",
    "mutationChangedMatrixBinderScope",
    "mutationExcludedZeroDimension",
)
DIRECT_IMPORTS = (
    "Mathlib.Data.Complex.Basic",
    "Mathlib.LinearAlgebra.Matrix.Block",
    "Mathlib.LinearAlgebra.UnitaryGroup",
)
EXPECTED_EXPRESSION_SHA256 = "275e1e43027f442607fc48e78ce4e189de66b328d39c61044e87a4c8f85c001b"
EXPECTED_STATEMENT_SHA256 = "1964c3edcb6c802bf15183733e98dbfa947d0d20ee125e29b687cf13cd2531f5"
EXPECTED_BOUNDARY_SHA256 = "aa36ec9e7f97ceea19afed618ffe959b3322c697a0e6d2af954f2a89fdc71b2b"
EXPECTED_LEAN_OUTPUT_SHA256 = "9ecf65c50f45dc9c43297ae60c05523c3fc8be55e68061abf3964b2eea50b985"
EXPECTED_IMPORT_HASHES = {
    "Mathlib.Data.Complex.Basic":
        "b26f6e653e122ea18e2dc1f790e46f6e3218b23bacd5d6b441324f11277c978b",
    "Mathlib.LinearAlgebra.Matrix.Block":
        "bdbdc046f6f10fdd634028259bbaae5dce9da670d8b95e37950f0a39390e3762",
    "Mathlib.LinearAlgebra.UnitaryGroup":
        "0136abe584007ffe1b9e9b0016b792ed92bc2de36fa710e87af9cb87d0808f93",
}
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_BASE_REVISION = "540472523b6c0717ed925193071191f81f62d6eb"
EXPECTED_BASE_TREE = "64b0c81418ef2c97b0250188444c672b9ae885d0"
EXPECTED_BLUEPRINT_SHA256 = "ca8885f9c340db27e99505eb3a580061f692efcee9c8731b8f9baf3bc647d762"
EXPECTED_EXECUTION_DAG_SHA256 = "662fe8784f391c2b62b32958609d352ba1c099dbec98a6bf40983ddb4475d134"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)], cwd=LEAN_DIR, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
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


def explicit_expression(declaration: str) -> tuple[str, str]:
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
        rf"def {qualified} : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    boundary_text = BOUNDARY.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {imports!r}")
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe)[ \t]",
        re.MULTILINE,
    )
    if prohibited.search(source_text) or prohibited.search(boundary_text):
        raise SystemExit("statement source contains a prohibited proof escape")

    deletion_failures: dict[str, str] = {}
    for module in DIRECT_IMPORTS:
        probe = source_text.replace(f"import {module}\n", "", 1)
        result = run_text(probe)
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {module}")
        diagnostic = next(
            (line.strip() for line in result.stdout.splitlines()
             if "unknown" in line.lower() or "failed to synthesize" in line.lower()
             or "invalid field" in line.lower()),
            "Lean rejected the deletion probe",
        )
        deletion_failures[module] = diagnostic

    boundary_result = run_lean(BOUNDARY)
    if boundary_result.returncode or boundary_result.stdout:
        print(boundary_result.stdout, end="")
        raise SystemExit("dimension or convention boundary probe failed")
    if sha256_bytes(BOUNDARY.read_bytes()) != EXPECTED_BOUNDARY_SHA256:
        raise SystemExit("boundary source changed without reconciliation")

    blueprint = ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md"
    execution_path = ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
    if sha256_bytes(blueprint.read_bytes()) != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("authoritative blueprint changed")
    if sha256_bytes(execution_path.read_bytes()) != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("authoritative execution DAG changed")
    execution = load(execution_path)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if (item["theorem_id"], item["phase"], item["layer"]) != (THEOREM_ID, "statement", 1):
        raise SystemExit("authoritative statement identity changed")
    if item["depends_on"] != ["S56-M-0045-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    expressions: dict[str, str] = {}
    canonical_output = ""
    for declaration in DECLARATIONS:
        expression, output = explicit_expression(declaration)
        expressions[declaration] = expression
        if declaration == CANONICAL:
            canonical_output = output
    if len(set(expressions.values())) != len(expressions):
        raise SystemExit("a statement mutation shares the canonical explicit expression")
    if "timeout" in canonical_output.lower() or "heartbeat" in canonical_output.lower():
        raise SystemExit("canonical Lean run contains a timeout or heartbeat diagnostic")

    expression_hash = sha256_bytes(expressions[CANONICAL].encode("utf-8"))
    statement_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    if expression_hash != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit(f"elaborated expression changed: {expression_hash}")
    if statement_hash != EXPECTED_STATEMENT_SHA256:
        raise SystemExit("statement source changed without reconciliation")
    if lean_output_hash != EXPECTED_LEAN_OUTPUT_SHA256:
        raise SystemExit("canonical Lean output changed without reconciliation")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    dag = load(SOURCE.with_name("task-dag.json"))
    formal = statement["canonical_formal_target"]
    if not statement["item_id"] == receipt["item_id"] == ITEM_ID:
        raise SystemExit("statement item identity is stale")
    if not statement["theorem_id"] == receipt["theorem_id"] == instance["theorem_id"] == THEOREM_ID:
        raise SystemExit("statement theorem identity is stale")
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("statement expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_hash:
        raise SystemExit("statement source fingerprint is stale")
    if formal["fully_explicit_expression"] != expressions[CANONICAL]:
        raise SystemExit("statement explicit expression is stale")
    if statement["boundary_probe_sha256"] != EXPECTED_BOUNDARY_SHA256:
        raise SystemExit("statement boundary fingerprint is stale")
    if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("statement direct-import inventory is stale")
    authority = statement["authority_inputs"]
    if authority["Docs/Stage1_Blueprint_rev-5.6.md"] != f"sha256:{EXPECTED_BLUEPRINT_SHA256}":
        raise SystemExit("statement blueprint fingerprint is stale")
    if authority["Docs/Stage1_Execution_DAG_rev-5.6.json"] != f"sha256:{EXPECTED_EXECUTION_DAG_SHA256}":
        raise SystemExit("statement execution DAG fingerprint is stale")
    instance_formal = instance["canonical_formal_target"]
    if instance_formal["module"] != f"Stage1_Instances/{THEOREM_ID}/Statement.lean":
        raise SystemExit("instance canonical module is stale")
    if instance_formal["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("instance canonical declaration is stale")
    if instance_formal["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_hash:
        raise SystemExit("receipt source fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    if receipt["boundary_probe_sha256"] != EXPECTED_BOUNDARY_SHA256:
        raise SystemExit("receipt boundary fingerprint is stale")
    if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("receipt direct-import inventory is stale")
    receipt_authority = receipt["authority_inputs"]
    if receipt_authority != authority:
        raise SystemExit("receipt authority fingerprints are stale")
    statement_task = next(task for task in dag["tasks"] if task["id"] == ITEM_ID)
    if statement_task["state"] != "open" or statement_task["depends_on"] != ["S56-M-0045-INTAKE"]:
        raise SystemExit("local statement task boundary changed")
    if not receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]:
        raise SystemExit("statement debt vector is inconsistent")
    if receipt["audit_complete"] or receipt["theorem_complete"]:
        raise SystemExit("statement receipt overclaims completion")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(packet) != packet_fields:
        raise SystemExit("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise SystemExit("worker packet item or state is stale")
    if packet["base_revision"] != receipt["base_revision"]:
        raise SystemExit("worker packet base revision is stale")
    if packet["changed_paths"] != receipt["changed_paths"]:
        raise SystemExit("worker packet changed paths are stale")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker packet known failures are stale")

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
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("manifest mathlib revision changed")
    actual_revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip()
    actual_tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip()
    if (actual_revision, actual_tree) != (EXPECTED_MATHLIB_REVISION, EXPECTED_MATHLIB_TREE):
        raise SystemExit("materialized mathlib revision or tree changed")
    for module, expected in EXPECTED_IMPORT_HASHES.items():
        path = mathlib / (module.replace(".", "/") + ".lean")
        if sha256_bytes(path.read_bytes()) != expected:
            raise SystemExit(f"direct import source changed: {module}")

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip()
    if (head, tree) != (EXPECTED_BASE_REVISION, EXPECTED_BASE_TREE):
        raise SystemExit("repository base revision or tree changed")
    if (receipt["base_revision"], receipt["base_tree"]) != (head, tree):
        raise SystemExit("receipt base revision or tree is stale")

    print(json.dumps({
        "boundary_probe_sha256": EXPECTED_BOUNDARY_SHA256,
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "fully_explicit_expression": expressions[CANONICAL],
        "import_deletion_failures": deletion_failures,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
