#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0079 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0079"
THEOREM_ID = "THM-M-0079"
ITEM_ID = "S56-M-0079-STATEMENT"
CANONICAL = "NielsenSchreierTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedAmbientFreeness",
    "mutationChangedDomain",
    "mutationChangedBinderScope",
    "mutationExcludedBottomBoundary",
)
BOUNDARIES = (
    "trivialAmbientBottomBoundary",
    "genericTopBoundary",
    "infiniteRankBoundary",
)
TRANSPORTS = (
    "nielsenSchreierTarget_implies_literalFreeGroupTarget",
    "literalFreeGroupTarget_implies_nielsenSchreierTarget",
    "nielsenSchreierTarget_iff_literalFreeGroupTarget",
    "nielsenSchreierTarget_iff_basisExistenceTarget",
)
DIRECT_IMPORTS = ("Mathlib.GroupTheory.FreeGroup.IsFreeGroup",)
PRINT_MARKER = "#print NielsenSchreierTarget"
EXPECTED_EXPRESSION_SHA256 = "bb109f77dcbd6884a4ac90b32230cc213c08f19df6bc797ad04afac1a10da553"
EXPECTED_STATEMENT_FILE_SHA256 = "fdacf7f7c9a39400ce02e8d82e3ed2a3a66e33dcd57b553d9e01a1dd991878c5"
EXPECTED_LEAN_OUTPUT_SHA256 = "87cb8af02f09002c193b5b0aa6923bb74526248650e94ab3089752ce05d3221d"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_IMPORT_SHA256 = "b5d6c1ae4fbeb1c2a5256d16d652a43f1615e4c945e03dcbf99f0cbb12558905"
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
    result = run_text(text.replace(PRINT_MARKER, f"#print {declaration}"))
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


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    for path in [p for p in SOURCE.parent.iterdir() if p.is_file()] + [
        ROOT / ".stage1-worker-selftest.json"
    ]:
        if not path.exists():
            continue
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
    items = {row["id"]: row for row in execution["items"]}
    item = items[ITEM_ID]
    intake = items["S56-M-0079-INTAKE"]
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement identity changed")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0079-INTAKE"]:
        raise SystemExit("authoritative statement state or dependency changed")
    if intake["state"] != "[_]":
        raise SystemExit("intake dependency is not provisionally available")
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

    for name in DECLARATIONS[1:]:
        diagnostic = f"{name}\nbut is expected to have type\n  {CANONICAL}"
        if diagnostic not in canonical_output:
            raise SystemExit(f"mutation did not fail exact-type check: {name}")
    if "Unknown identifier `subgroupIsFreeOfIsFree`" not in canonical_output:
        raise SystemExit("proof-bearing anchor unexpectedly entered the import closure")
    for name in BOUNDARIES + TRANSPORTS:
        if not re.search(rf"^(theorem|def) {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing boundary or transport declaration: {name}")
    prohibited = re.compile(PROHIBITED_PATTERN)
    for lean_path in SOURCE.parent.glob("*.lean"):
        match = prohibited.search(lean_path.read_text(encoding="utf-8"))
        if match:
            raise SystemExit(f"prohibited token in {lean_path.name}: {match.group(0)}")

    reduced = source_text.replace(f"import {DIRECT_IMPORTS[0]}\n", "")
    if run_text(reduced).returncode == 0:
        raise SystemExit("the sole direct import survived deletion")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    for recorded, actual, label in (
        (EXPECTED_EXPRESSION_SHA256, expression_hash, "elaborated expression"),
        (EXPECTED_STATEMENT_FILE_SHA256, statement_file_hash, "statement source"),
        (EXPECTED_LEAN_OUTPUT_SHA256, lean_output_hash, "canonical Lean output"),
    ):
        if recorded != "TO_BE_RECONCILED" and recorded != actual:
            raise SystemExit(f"{label} changed without reconciliation")

    toolchain_path = LEAN_DIR / "lean-toolchain"
    manifest_path = LEAN_DIR / "lake-manifest.json"
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    import_path = mathlib / "Mathlib/GroupTheory/FreeGroup/IsFreeGroup.lean"
    manifest = load(manifest_path)
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if toolchain_path.read_text(encoding="utf-8").strip() != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain pin changed")
    if sha256_bytes(toolchain_path.read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("toolchain file changed")
    if sha256_bytes(manifest_path.read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("Lake manifest changed")
    if sha256_bytes(import_path.read_bytes()) != EXPECTED_IMPORT_SHA256:
        raise SystemExit("minimal import source changed")
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
    if subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=mathlib,
        text=True,
    ).strip():
        raise SystemExit("pinned mathlib checkout is dirty")

    structured_paths = (
        SOURCE.with_name("statement.json"),
        SOURCE.with_name("statement-receipt.json"),
        ROOT / ".stage1-worker-selftest.json",
    )
    missing_structured = [str(path) for path in structured_paths if not path.exists()]
    if missing_structured:
        raise SystemExit(f"missing required structured artifacts: {', '.join(missing_structured)}")
    else:
        statement, receipt, packet = map(load, structured_paths)
        instance = load(SOURCE.with_name("instance.json"))
        formal = statement["canonical_formal_target"]
        if formal["elaborated_expression_sha256"] != expression_hash:
            raise SystemExit("structured expression fingerprint is stale")
        if formal["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("structured statement source fingerprint is stale")
        if formal["fully_explicit_expression"] != canonical:
            raise SystemExit("structured fully explicit expression is stale")
        if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
            raise SystemExit("receipt expression fingerprint is stale")
        if receipt["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("receipt statement source fingerprint is stale")
        if receipt["lean_output_sha256"] != lean_output_hash:
            raise SystemExit("receipt Lean output fingerprint is stale")
        if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
            raise SystemExit("statement direct-import record is stale")
        if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
            raise SystemExit("receipt direct-import record is stale")
        if instance["canonical_formal_target"]["elaborated_expression_hash"] != (
            f"sha256:{expression_hash}"
        ):
            raise SystemExit("instance expression fingerprint is stale")
        if statement["root_vector_after"] != instance["root_vector"]:
            raise SystemExit("statement and instance debt vectors disagree")
        if receipt["root_vector_after"] != instance["root_vector"]:
            raise SystemExit("receipt and instance debt vectors disagree")
        if receipt["audit_complete"] or receipt["theorem_complete"]:
            raise SystemExit("statement receipt overclaims completion")
        if instance["audit_complete"] or instance["theorem_complete"]:
            raise SystemExit("instance overclaims completion")
        local_dag = load(SOURCE.with_name("task-dag.json"))
        local_item = next(row for row in local_dag["tasks"] if row["id"] == ITEM_ID)
        if local_item["state"] != "open" or local_item["depends_on"] != [
            "S56-M-0079-INTAKE"
        ]:
            raise SystemExit("local statement task boundary changed")
        actual_owned_files = {path.name for path in SOURCE.parent.iterdir() if path.is_file()}
        if set(instance["owned_artifacts"]) != actual_owned_files:
            raise SystemExit("instance owned-artifact inventory is stale")
        base_revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
        if receipt["base_revision"] != base_revision:
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
            raise SystemExit("receipt paths do not match scoped git status")
        historical = SOURCE.with_name("validation.md").read_text(encoding="utf-8")
        if "Historical intake" not in historical or "not current statement evidence" not in historical:
            raise SystemExit("historical intake validation boundary is stale")

    print(json.dumps({
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "import_deletion_failed": True,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
        "transports": list(TRANSPORTS),
        "validated_boundaries": list(BOUNDARIES),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
