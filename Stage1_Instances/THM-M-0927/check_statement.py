#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0927 statement."""

from __future__ import annotations

import argparse
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
THEOREM_ID = "THM-M-0927"
ITEM_ID = "S56-M-0927-STATEMENT"
NAMESPACE = "Stage1Instances.THM_M_0927"
CANONICAL = "BinetFormulaTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedConjugateContribution",
    "mutationChangedDomainToFinTen",
    "mutationChangedBinderScope",
    "mutationExcludesZeroIndex",
)
TRANSPORTS = (
    "binetFormulaTarget_iff_functionEqualityTarget",
    "binetFormulaTarget_iff_characteristicRootTarget",
)
BOUNDARIES = (
    "zero_index_formula",
    "removed_conjugate_mutation_is_false",
    "sqrt_five_ne_zero",
    "one_index_formula",
    "ten_has_no_fin_ten_representation",
)
DIRECT_IMPORTS = (
    "Mathlib.Data.Nat.Fib.Basic",
    "Mathlib.Data.Real.Sqrt",
)
PRINT_MARKER = "#print BinetFormulaTarget"
EXPECTED_EXPRESSION_SHA256 = "0a05e8c4976c01759ef82d364afc86f498f700edc1a0fcb3f8935765992b5a2f"
EXPECTED_STATEMENT_FILE_SHA256 = "72172fb6015846b808a81dfc4995767dec5381de5845f68c47cbc5fdb2eeed8d"
EXPECTED_LEAN_OUTPUT_SHA256 = "4195b9753c2a0c73835c20766e3d2eeb72ed87f6ee6c624b5c26dc1a1ad23f4b"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise SystemExit(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        env={**os.environ, "LC_ALL": "C", "TZ": "UTC"},
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
        rf"def {qualified} : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def check_import_deletion(source_text: str) -> None:
    canonical_prefix = source_text.split("/-- The positive characteristic root", 1)[0]
    canonical_prefix += (
        "\nend Stage1Instances.THM_M_0927\n"
        "set_option pp.universes true in\n"
        "set_option pp.explicit true in\n"
        "#print Stage1Instances.THM_M_0927.BinetFormulaTarget\n"
    )
    baseline = run_text(canonical_prefix)
    if baseline.returncode:
        print(baseline.stdout, end="")
        raise SystemExit("canonical import-minimality fixture did not elaborate")
    for module in DIRECT_IMPORTS:
        mutation = canonical_prefix.replace(f"import {module}\n", "", 1)
        result = run_text(mutation)
        if result.returncode == 0:
            raise SystemExit(f"direct import is deletion-redundant: {module}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    source_text = SOURCE.read_text(encoding="utf-8")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement":
        raise SystemExit("authoritative statement item identity changed")
    if item["layer"] != 1 or item["depends_on"] != ["S56-M-0927-INTAKE"]:
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

    for name in TRANSPORTS + BOUNDARIES:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing transport or boundary declaration: {name}")
    if source_text.count("#check_failure") != 4:
        raise SystemExit("statement must contain exactly four mutation failure guards")
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|constant|opaque)\s+|"
        r"^\s*unsafe\b|\b(?:TODO|FIXME)\b",
        re.MULTILINE,
    )
    if prohibited.search(source_text):
        raise SystemExit("prohibited declaration or placeholder marker in statement source")

    check_import_deletion(source_text)

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
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

    expected_mutation_hashes = {
        "mutationRemovedConjugateContribution": (
            "324dea0021bbe2e3d643603e8af04c7cd4150046ad6b58f9399d19c9f697d56b"
        ),
        "mutationChangedDomainToFinTen": (
            "1c8011910910a59f5ca28c08d4de16b5353545df6a8ac71925dd56f324ef0b6c"
        ),
        "mutationChangedBinderScope": (
            "d1f6e2fcc08e01359024af6d894e49afcdc3c653cc992db2c8310098934c9079"
        ),
        "mutationExcludesZeroIndex": (
            "1789bde93d5828fe231cea81bcf82a17728007a6f4022d090f5ed9b43fe7e328"
        ),
    }
    mutation_hashes = {
        name: sha256_bytes(expressions[name].encode("utf-8"))
        for name in DECLARATIONS[1:]
    }
    if mutation_hashes != expected_mutation_hashes:
        raise SystemExit("mutation expression fingerprints changed without reconciliation")

    statement_path = SOURCE.with_name("statement.json")
    receipt_path = SOURCE.with_name("statement-receipt.json")
    if statement_path.exists() != receipt_path.exists():
        raise SystemExit("statement record and receipt must appear together")
    if statement_path.exists():
        statement = load(statement_path)
        receipt = load(receipt_path)
        packet_path = ROOT / ".stage1-worker-selftest.json"
        formal = statement["canonical_formal_target"]
        if formal["elaborated_expression_sha256"] != expression_hash:
            raise SystemExit("structured expression fingerprint is stale")
        if formal["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("structured statement source fingerprint is stale")
        if formal["fully_explicit_expression"] != " ".join(canonical.split()):
            raise SystemExit("serialized fully explicit expression is stale")
        environment = statement["environment_fingerprint"]
        if environment["canonical_sha256"] != sha256_bytes(
            environment["canonical_serialization"].encode("utf-8")
        ):
            raise SystemExit("canonical environment fingerprint is stale")
        if tuple(environment["serialization_options"]) != (
            "pp.explicit=true",
            "pp.universes=true",
        ):
            raise SystemExit("environment serialization options changed")
        if environment["namespace"] != NAMESPACE:
            raise SystemExit("environment namespace changed")
        if environment["lean_toolchain"] != (
            LEAN_DIR / "lean-toolchain"
        ).read_text(encoding="utf-8").strip():
            raise SystemExit("environment Lean toolchain changed")
        if environment["lean_toolchain_sha256"] != sha256_bytes(
            (LEAN_DIR / "lean-toolchain").read_bytes()
        ):
            raise SystemExit("environment Lean toolchain fingerprint is stale")
        if environment["lake_manifest_sha256"] != sha256_bytes(
            (LEAN_DIR / "lake-manifest.json").read_bytes()
        ):
            raise SystemExit("environment Lake manifest fingerprint is stale")
        mathlib_dir = LEAN_DIR / ".lake" / "packages" / "mathlib"
        actual_mathlib_revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=mathlib_dir, text=True
        ).strip()
        actual_mathlib_tree = subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib_dir, text=True
        ).strip()
        if environment["mathlib_revision"] != actual_mathlib_revision:
            raise SystemExit("environment mathlib revision changed")
        if environment["mathlib_tree"] != actual_mathlib_tree:
            raise SystemExit("environment mathlib tree changed")
        import_sources = {
            "nat_fib_basic_source_sha256": (
                mathlib_dir / "Mathlib" / "Data" / "Nat" / "Fib" / "Basic.lean"
            ),
            "real_sqrt_source_sha256": (
                mathlib_dir / "Mathlib" / "Data" / "Real" / "Sqrt.lean"
            ),
        }
        for field, path in import_sources.items():
            if environment[field] != sha256_bytes(path.read_bytes()):
                raise SystemExit(f"environment imported-source fingerprint is stale: {field}")
        if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
            raise SystemExit("receipt expression fingerprint is stale")
        if receipt["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("receipt statement source fingerprint is stale")
        if receipt["lean_output_sha256"] != lean_output_hash:
            raise SystemExit("receipt Lean-output fingerprint is stale")
        if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
            raise SystemExit("receipt direct-import record is stale")
        for relative, digest in receipt["source_inputs"].items():
            if relative.startswith("Stage1_Instances/"):
                continue
            if digest != f"sha256:{sha256_bytes((ROOT / relative).read_bytes())}":
                raise SystemExit(f"stale receipt source input: {relative}")
        if receipt["accepted"] or receipt["accepted_receipt_ids"]:
            raise SystemExit("worker receipt cannot claim acceptance")
        if receipt["audit_complete"] or receipt["theorem_complete"]:
            raise SystemExit("statement receipt cannot claim terminal completion")
        expected_changed = {
            ".stage1-worker-selftest.json",
            *{
                f"Stage1_Instances/{THEOREM_ID}/{name}"
                for name in (
                    "Statement.lean",
                    "check_statement.py",
                    "statement-receipt.json",
                    "statement-validation.md",
                    "statement.json",
                )
            },
        }
        if set(receipt["changed_paths"]) != expected_changed:
            raise SystemExit("receipt changed-path inventory is stale")
        instance = load(SOURCE.with_name("instance.json"))
        if instance["canonical_statement"] is not None:
            raise SystemExit("historical intake manifest was rewritten by statement phase")
        if instance["canonical_formal_target"]["elaborated_expression_hash"] is not None:
            raise SystemExit("historical intake target fingerprint was rewritten")
        dag = load(SOURCE.with_name("task-dag.json"))
        if dag["accepted_states"] or dag["audit_complete"] or dag["theorem_complete"]:
            raise SystemExit("historical open DAG cannot contain accepted or terminal state")
        if packet_path.exists():
            packet = load(packet_path)
            if set(packet["changed_paths"]) != expected_changed:
                raise SystemExit("worker packet changed-path inventory is stale")
            if packet["known_failures"] != receipt["known_failures"]:
                raise SystemExit("worker packet known failures disagree with receipt")

    if args.worker_packet:
        packet = load(args.worker_packet.resolve())
        required = {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }
        if set(packet) != required:
            raise SystemExit("worker packet fields changed")
        if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet identity or state changed")
        if packet["base_revision"] != subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip():
            raise SystemExit("worker packet base revision changed")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "fully_explicit_expression": " ".join(canonical.split()),
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "mutation_expression_sha256": mutation_hashes,
        "statement_file_sha256": statement_file_hash,
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "transports": list(TRANSPORTS),
        "validated_boundaries": list(BOUNDARIES),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
