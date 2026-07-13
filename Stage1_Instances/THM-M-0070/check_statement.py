#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0070 statement."""

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
THEOREM_ID = "THM-M-0070"
ITEM_ID = "S56-M-0070-STATEMENT"
NAMESPACE = "Stage1Instances.THM_M_0070"
CANONICAL = "OddOrderSolvabilityTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedOddness",
    "mutationChangedToCommutativeDomain",
    "mutationChangedOddnessScope",
    "mutationChangedToEvenOrder",
)
TRANSPORTS = (
    "oddOrderSolvabilityTarget_iff_fintypeCardTarget",
    "oddOrderSolvabilityTarget_iff_modTwoTarget",
    "oddOrderSolvabilityTarget_iff_derivedSeriesTarget",
)
BOUNDARIES = (
    "target_includes_order_one_group",
    "target_includes_commutative_groups",
)
DIRECT_IMPORTS = (
    "Mathlib.GroupTheory.Solvable",
    "Mathlib.SetTheory.Cardinal.Finite",
)
IMPORT_FILES = {
    "Mathlib.GroupTheory.Solvable": "Mathlib/GroupTheory/Solvable.lean",
    "Mathlib.SetTheory.Cardinal.Finite": "Mathlib/SetTheory/Cardinal/Finite.lean",
}
PRINT_MARKER = "#print OddOrderSolvabilityTarget"
EXPECTED_EXPRESSION_SHA256 = "51024e84c9b068a6de27ff2d3ba0f1e479c02dfd36d8072f3d243d46f3324c93"
EXPECTED_STATEMENT_FILE_SHA256 = "9e1c126d56f87c1d7dee24d17b13c9c9822ffba13142e836ecbe2a85055a7dcf"
EXPECTED_LEAN_OUTPUT_SHA256 = "395d768d516c68ca602a6b9c1a8f1868cbf58e8d589f91a24601b5954edfade5"
EXPECTED_BASE_REVISION = "0d2c3bdcd192266bc255ac3d5186da604517145a"
EXPECTED_BASE_TREE = "eafbcb48efd51d9cda34f0fc1afe780434abad64"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_IMPORT_SHA256 = {
    "Mathlib.GroupTheory.Solvable": "d665fe00fcf4bc1bc072cc053b1e47c8609552627386981feccd81a448b6153b",
    "Mathlib.SetTheory.Cardinal.Finite": "8de62ef138473b4c4b77917aa453f67b8e203cfb1d2e2c6cb6ebbabf62a9356f",
}


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


def run_text(source_text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", delete=False
    ) as handle:
        handle.write(source_text)
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
    expected_failures = {
        "#check_failure (show mutationRemovedOddness.{u} from hCanonical)",
        "#check_failure (show OddOrderSolvabilityTarget.{u} from hCommutative)",
        "#check_failure (show mutationChangedOddnessScope.{u} from hCanonical)",
        "#check_failure (show OddOrderSolvabilityTarget.{u} from hBoundary)",
    }
    if source_text.count("#check_failure") != len(expected_failures):
        raise SystemExit("mutation rejection fixture count changed")
    if any(fixture not in source_text for fixture in expected_failures):
        raise SystemExit("mutation rejection fixture changed")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["depends_on"] != ["S56-M-0070-INTAKE"]:
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

    deletion_exits = {}
    for direct_import in DIRECT_IMPORTS:
        deletion = run_text(source_text.replace(f"import {direct_import}\n", "", 1))
        deletion_exits[direct_import] = deletion.returncode
        if deletion.returncode == 0:
            raise SystemExit(f"direct import deletion unexpectedly elaborated: {direct_import}")

    expression_hash = sha256_bytes(expressions[CANONICAL].encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    expected = (
        ("expression", expression_hash, EXPECTED_EXPRESSION_SHA256),
        ("statement source", statement_file_hash, EXPECTED_STATEMENT_FILE_SHA256),
        ("Lean output", lean_output_hash, EXPECTED_LEAN_OUTPUT_SHA256),
    )
    for label, actual, wanted in expected:
        if actual != wanted:
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
    if local_item["state"] != "open" or local_item["depends_on"] != ["S56-M-0070-INTAKE"]:
        raise SystemExit("local statement task boundary changed")
    if statement["root_vector_before"] != receipt["root_vector_before"]:
        raise SystemExit("pre-statement debt vectors disagree")
    if statement["root_vector_after"] != instance["root_vector"]:
        raise SystemExit("statement and instance debt vectors disagree")
    if receipt["root_vector_after"] != instance["root_vector"]:
        raise SystemExit("receipt and instance debt vectors disagree")
    if receipt["audit_complete"] or receipt["theorem_complete"]:
        raise SystemExit("statement receipt overclaims completion")
    if any(instance[field] for field in ("audit_complete", "theorem_complete")):
        raise SystemExit("instance overclaims completion")
    for relative in receipt["changed_paths"]:
        if relative == ".stage1-worker-selftest.json":
            continue
        if not (ROOT / relative).is_file():
            raise SystemExit(f"receipt changed path is missing: {relative}")
    actual_owned_files = {path.name for path in SOURCE.parent.iterdir() if path.is_file()}
    if set(instance["owned_artifacts"]) != actual_owned_files:
        raise SystemExit("instance owned-artifact inventory is stale")

    for lean_path in SOURCE.parent.glob("*.lean"):
        if prohibited.search(lean_path.read_text(encoding="utf-8")):
            raise SystemExit(f"prohibited declaration or placeholder found: {lean_path.name}")
    checked_paths = [ROOT / relative for relative in receipt["changed_paths"]]
    for path in checked_paths:
        data = path.read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            raise SystemExit(f"invalid bytes or final newline: {path}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            raise SystemExit(f"trailing whitespace: {path}")

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

    status_output = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:] for line in status_output.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changed != set(receipt["changed_paths"]):
        raise SystemExit("receipt changed paths disagree with scoped git status")

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
    for module, relative in IMPORT_FILES.items():
        if sha256_bytes((mathlib / relative).read_bytes()) != EXPECTED_IMPORT_SHA256[module]:
            raise SystemExit(f"direct import source changed: {module}")
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
        "import_deletion_exits": deletion_exits,
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "mutation_expression_sha256": {
            name: sha256_bytes(expressions[name].encode("utf-8"))
            for name in DECLARATIONS[1:]
        },
        "statement_file_sha256": statement_file_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
        "transports": list(TRANSPORTS),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
