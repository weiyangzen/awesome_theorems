#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0061 statement."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
THEOREM_ID = "THM-M-0061"
ITEM_ID = "S56-M-0061-STATEMENT"
NAMESPACE = "Stage1Instances.THM_M_0061"
CANONICAL = "LagrangeDivisibilityTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedFiniteness",
    "mutationChangedToAdditiveDomain",
    "mutationExistentialSubgroup",
    "mutationExcludedTrivialGroup",
)
TRANSPORTS = ("lagrangeDivisibilityTarget_iff_fintypeCardTarget",)
BOUNDARIES = (
    "target_includes_order_one_group",
    "target_includes_bottom_subgroup",
    "target_includes_top_subgroup",
)
DIRECT_IMPORTS = ("Mathlib.Algebra.Group.Subgroup.Finite",)
PRINT_MARKER = "#print LagrangeDivisibilityTarget"
EXPECTED_EXPRESSION_SHA256 = "adff72e9052ea17e3b6e4349c23028f35f4b8e3c610ea5f9f3b4fc02fe136836"
EXPECTED_STATEMENT_FILE_SHA256 = "386d2d25cc7fe5f55f26438e1bc749eb5953e251b48591d3e47247b733bfdc7d"
EXPECTED_LEAN_OUTPUT_SHA256 = "cb4d37bde1cf888d2d29ddbae630a78eb8cae0166dca86c98bb1ccacf2702f59"
EXPECTED_BASE_REVISION = "ebd5f75831296a8a35e7b33013b964f2baf31bb9"
EXPECTED_BASE_TREE = "d1e4bc83c803eefcd9898aac57352265a29f0658"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_IMPORT_SOURCE_SHA256 = "f6b8c03be67cd42c56ed60499ff8f4c86af20caa4ea2e3eb3f7663535a9f4ac5"


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
        sys.stdout.write(result.stdout)
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


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")
    prohibited = re.compile(
        r"\b(sorry|admit)\b|\bsorryAx\b|^[ \t]*(axiom|constant|opaque|unsafe)[ \t]",
        re.MULTILINE,
    )
    if prohibited.search(source_text):
        raise SystemExit("prohibited declaration or placeholder found in Statement.lean")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["depends_on"] != ["S56-M-0061-INTAKE"]:
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
    if len(set(expressions.values())) != len(expressions):
        raise SystemExit("canonical statement and mutations must have distinct expressions")

    for name in TRANSPORTS + BOUNDARIES:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing statement witness: {name}")

    deletion = run_text(source_text.replace(f"import {DIRECT_IMPORTS[0]}\n", "", 1))
    if deletion.returncode == 0:
        raise SystemExit("direct import deletion unexpectedly elaborated")

    expression_hash = sha256_bytes(expressions[CANONICAL].encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    expected = (
        ("expression", expression_hash, EXPECTED_EXPRESSION_SHA256),
        ("statement source", statement_file_hash, EXPECTED_STATEMENT_FILE_SHA256),
        ("Lean output", lean_output_hash, EXPECTED_LEAN_OUTPUT_SHA256),
    )
    for label, actual, wanted in expected:
        if wanted != "TO_BE_RECONCILED" and actual != wanted:
            raise SystemExit(f"{label} changed without reconciliation")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("structured statement expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("structured statement source fingerprint is stale")
    if formal["fully_explicit_expression"] != expressions[CANONICAL]:
        raise SystemExit("structured fully explicit expression is stale")
    if instance["canonical_formal_target"]["elaborated_expression_hash"] != (
        f"sha256:{expression_hash}"
    ):
        raise SystemExit("instance expression fingerprint is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("receipt source fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("receipt direct-import record is stale")

    dag = load(SOURCE.with_name("task-dag.json"))
    local_item = next(row for row in dag["tasks"] if row["id"] == ITEM_ID)
    if local_item["state"] != "open" or local_item["depends_on"] != ["S56-M-0061-INTAKE"]:
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

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip() != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain pin changed")
    if sha256_bytes((LEAN_DIR / "lean-toolchain").read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("Lean toolchain file changed")
    if sha256_bytes((LEAN_DIR / "lake-manifest.json").read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("Lake manifest changed")
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("manifest mathlib revision changed")
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    actual_revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip()
    actual_tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip()
    if (actual_revision, actual_tree) != (EXPECTED_MATHLIB_REVISION, EXPECTED_MATHLIB_TREE):
        raise SystemExit("materialized mathlib revision or tree changed")
    import_path = mathlib / "Mathlib/Algebra/Group/Subgroup/Finite.lean"
    if sha256_bytes(import_path.read_bytes()) != EXPECTED_IMPORT_SOURCE_SHA256:
        raise SystemExit("direct import source changed")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip()
    if (head, tree) != (EXPECTED_BASE_REVISION, EXPECTED_BASE_TREE):
        raise SystemExit("repository base revision or tree changed")
    if (receipt["base_revision"], receipt["base_tree"]) != (head, tree):
        raise SystemExit("receipt base revision or tree is stale")

    payload = {
        "boundary_witnesses": list(BOUNDARIES),
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "import_deletion_exit": deletion.returncode,
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "mutation_expression_sha256": {
            name: sha256_bytes(expressions[name].encode("utf-8"))
            for name in DECLARATIONS[1:]
        },
        "statement_file_sha256": statement_file_hash,
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "transports": list(TRANSPORTS),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
