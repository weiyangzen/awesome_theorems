#!/usr/bin/env python3
"""Validate the exact THM-M-0931 statement and its structural transports."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = HERE / "Statement.lean"
NAMESPACE = "Stage1Instances.THM_M_0931"
ITEM_ID = "S56-M-0931-STATEMENT"
THEOREM_ID = "THM-M-0931"
CANONICAL = "ErdosGinzburgZivTarget"
MUTATIONS = (
    "mutationRemovedPositivity",
    "mutationNaturalInputs",
    "mutationExistentialModulus",
    "mutationAtLeastInputCount",
)
DIRECT_IMPORTS = ("Mathlib.Data.ZMod.Basic",)
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_EXPRESSION_SHA256 = "b872e0de4aedbd0da8825d2c7dd9ecb30e01215131c61e73dc3050776711718a"
EXPECTED_STATEMENT_FILE_SHA256 = "d0e7e43d896a0625e87b3fac55319d5e999351c8f74cdda4e699d9360d651020"
EXPECTED_IMPORT_SOURCE_SHA256 = "b150e3bf79b154b28c1d3fa68cbd837f093f4305bf4fd2e9302db29081135358"
EXPECTED_AUTHORITY_SHA256 = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "5b546381c6d1d3beb0f63df382b897ba22124f9cca783accf42f4e657142306e",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "6f31b03a351477d6f0da0a8823f2544c9c6717c12762f73bc35a7f2901976a63",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Stage1_Instances/THM-M-0931/intake-receipt.json": "63438acc4ef6a67d26e1e19c3b4f0c30debcf8452129e5196179d566e131d452",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_lean(source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )


def expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if text.count(marker) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
    text = text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=HERE, delete=False, encoding="utf-8"
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
    match = re.search(r" : Prop :=\n(?P<expression>.*)\Z", result.stdout, re.DOTALL)
    if not match:
        raise SystemExit(f"could not serialize {declaration}")
    serialized = match.group("expression").strip()
    if "?m." in serialized:
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return serialized, result.stdout


def check_import_minimality(source_text: str) -> dict:
    actual = tuple(
        line.removeprefix("import ")
        for line in source_text.splitlines()
        if line.startswith("import ")
    )
    if actual != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {actual}")
    candidate = source_text.replace(f"import {DIRECT_IMPORTS[0]}\n", "", 1)
    temporary = HERE / "ImportDeletionProbe.lean"
    if temporary.exists():
        raise SystemExit(f"temporary import probe already exists: {temporary}")
    temporary.write_text(candidate, encoding="utf-8")
    try:
        result = run_lean(temporary)
    finally:
        temporary.unlink()
    if result.returncode == 0:
        raise SystemExit(f"direct import is redundant: {DIRECT_IMPORTS[0]}")
    normalized = result.stdout.replace(str(temporary), "<fixture>")
    first_error = next(
        (line for line in normalized.splitlines() if "error" in line.lower()),
        "Lean rejected the import-deletion fixture",
    )
    return {
        "exit_code": result.returncode,
        "first_error": first_error,
        "output_sha256": sha256(normalized.encode()),
    }


def check_transport_directions(source_text: str) -> None:
    required_fragments = (
        "AtLeastCountTarget -> ErdosGinzburgZivTarget",
        "ErdosGinzburgZivTarget <-> ResidueTarget",
    )
    for fragment in required_fragments:
        if fragment not in source_text:
            raise SystemExit(f"checked transport direction changed: {fragment}")


def check_forbidden_constructs(source_text: str) -> None:
    without_comments = re.sub(r"/-.*?-/", "", source_text, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    match = re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b",
        without_comments,
    )
    if match:
        raise SystemExit(f"forbidden Lean construct: {match.group(0)}")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)
    check_transport_directions(source_text)

    expressions: dict[str, str] = {}
    outputs: dict[str, str] = {}
    for declaration in (CANONICAL, *MUTATIONS):
        expressions[declaration], outputs[declaration] = expression(declaration)
    canonical = expressions[CANONICAL]
    expression_digest = sha256(canonical.encode())
    if expression_digest != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit(f"canonical expression changed: {expression_digest}")
    statement_digest = sha256(SOURCE.read_bytes())
    if statement_digest != EXPECTED_STATEMENT_FILE_SHA256:
        raise SystemExit(f"statement source changed: {statement_digest}")
    survivors = [name for name in MUTATIONS if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    toolchain = (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip()
    if toolchain != EXPECTED_TOOLCHAIN:
        raise SystemExit(f"unexpected Lean toolchain: {toolchain}")
    manifest = load(LEAN_DIR / "lake-manifest.json")
    revision = next(
        package["rev"] for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    if revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit(f"unexpected mathlib revision: {revision}")
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip()
    if tree != EXPECTED_MATHLIB_TREE:
        raise SystemExit(f"unexpected mathlib tree: {tree}")
    import_source = mathlib / "Mathlib" / "Data" / "ZMod" / "Basic.lean"
    if sha256(import_source.read_bytes()) != EXPECTED_IMPORT_SOURCE_SHA256:
        raise SystemExit("direct import source changed")

    statement = load(HERE / "statement.json")
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != expression_digest:
        raise SystemExit("statement metadata expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_digest:
        raise SystemExit("statement metadata source fingerprint is stale")
    if statement["direct_imports"] != list(DIRECT_IMPORTS):
        raise SystemExit("statement metadata imports changed")
    for relative, digest in EXPECTED_AUTHORITY_SHA256.items():
        if sha256((ROOT / relative).read_bytes()) != digest:
            raise SystemExit(f"authority or dependency snapshot changed: {relative}")

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    if target["execution_rank"] != 1470 or target["lifecycle_mode"] != "planned":
        raise SystemExit("target manifest identity changed")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["depends_on"] != ["S56-M-0931-INTAKE"]:
        raise SystemExit("authoritative statement item changed")
    local_dag = load(HERE / "task-dag.json")
    local_item = next(row for row in local_dag["tasks"] if row["id"] == ITEM_ID)
    if local_item["state"] != "open" or local_item["depends_on"] != item["depends_on"]:
        raise SystemExit("local statement dependency boundary changed")

    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "elaborated_expression_sha256": expression_digest,
        "fully_explicit_expression": canonical,
        "import_deletion_failure": check_import_minimality(source_text),
        "killed_mutations": list(MUTATIONS),
        "lean_output_sha256": sha256(outputs[CANONICAL].encode()),
        "mathlib_revision": revision,
        "mathlib_tree": tree,
        "mutation_expression_sha256": {
            name: sha256(expressions[name].encode()) for name in MUTATIONS
        },
        "statement_file_sha256": statement_digest,
        "toolchain": toolchain,
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
