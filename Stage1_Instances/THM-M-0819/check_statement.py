#!/usr/bin/env python3
"""Validate the exact THM-M-0819 statement and structural mutations."""

from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
STATEMENT_RECORD = SOURCE.with_name("statement.json")
RECEIPT = SOURCE.with_name("statement-receipt.json")
NAMESPACE = "Stage1Instances.THM_M_0819"
CANONICAL = "DilworthPrimaryTarget"
MUTATIONS = [
    "mutationRemovedIndependentWitness",
    "mutationChangedToNatDomain",
    "mutationChangedWidthBinderScope",
    "mutationExcludesZeroWidth",
]
DIRECT_IMPORTS = ["Mathlib.Order.Antichain"]
ITEM_ID = "S56-M-0819-STATEMENT"
THEOREM_ID = "THM-M-0819"
BASE_REVISION = "fcabbf1e0ad9507eebe91663bccabfa87d22813e"
BASE_TREE = "873e589c594454b7f263c7ed2342089a4d15e842"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0819/Statement.lean",
    "Stage1_Instances/THM-M-0819/check_statement.py",
    "Stage1_Instances/THM-M-0819/statement-receipt.json",
    "Stage1_Instances/THM-M-0819/statement-validation.md",
    "Stage1_Instances/THM-M-0819/statement.json",
}
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md": "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md": "skills/execute-stage1-rev56/SKILL.md",
    "Docs/Blueprint_Guidelines.md": "Docs/Blueprint_Guidelines.md",
    "Docs/researches/math_theorems.md": "Docs/researches/math_theorems.md",
    "Docs/Stage0_Blueprint.md": "Docs/Stage0_Blueprint.md",
    "Formalizations/Lean/lean-toolchain": "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json": "Formalizations/Lean/lake-manifest.json",
}
OWNED_INPUTS = {
    "Stage1_Instances/THM-M-0819/instance.json": "Stage1_Instances/THM-M-0819/instance.json",
    "Stage1_Instances/THM-M-0819/source-statement-crosswalk.md":
        "Stage1_Instances/THM-M-0819/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0819/intake-receipt.json":
        "Stage1_Instances/THM-M-0819/intake-receipt.json",
    "Stage1_Instances/THM-M-0819/task-dag.json": "Stage1_Instances/THM-M-0819/task-dag.json",
    "Stage1_Instances/THM-M-0819/scope-map.md": "Stage1_Instances/THM-M-0819/scope-map.md",
}


def run_lean(source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )


def elaborate(source: Path) -> str:
    result = run_lean(source)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def expression(declaration: str) -> tuple[str, str]:
    source_text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if source_text.count(marker) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
    source_text = source_text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(source_text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    match = re.search(r" : Prop :=\n(?P<expression>.*)\Z", output, re.DOTALL)
    if not match:
        raise SystemExit(f"could not serialize {declaration}")
    serialized = match.group("expression").strip()
    if "?m." in serialized:
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return serialized, output


def support_expression(declaration: str) -> str:
    source_text = SOURCE.read_text(encoding="utf-8")
    print_marker = f"#print {NAMESPACE}.{CANONICAL}"
    if source_text.count(print_marker) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
    source_text = source_text.replace(
        print_marker,
        f"set_option pp.explicit true in\n"
        f"set_option pp.universes true in\n"
        f"#print {NAMESPACE}.{declaration}",
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(source_text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    match = re.search(rf"def {re.escape(NAMESPACE)}\.{re.escape(declaration)}.*? :=\n(?P<body>.*)\Z", output, re.DOTALL)
    if not match:
        raise SystemExit(f"could not serialize support definition {declaration}")
    serialized = match.group("body").strip()
    if "?m." in serialized:
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return serialized


def check_minimal_import(source_text: str) -> dict[str, str]:
    actual_imports = [
        line.removeprefix("import ")
        for line in source_text.splitlines()
        if line.startswith("import ")
    ]
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {actual_imports}")

    canonical_marker = "/--\nDilworth's Theorem 1.1 in its primary arbitrary-poset finite-width form."
    end_marker = "/-- The same target with chain decomposition expanded at the boundary. -/"
    if source_text.count(canonical_marker) != 1 or source_text.count(end_marker) != 1:
        raise SystemExit("canonical-target fixture marker is missing or ambiguous")
    canonical_fixture = (
        source_text[: source_text.index(canonical_marker)]
        + source_text[source_text.index(canonical_marker) : source_text.index(end_marker)]
        + "\nend Stage1Instances.THM_M_0819\n"
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(canonical_fixture)
        baseline = Path(handle.name)
    try:
        baseline_result = run_lean(baseline)
    finally:
        baseline.unlink()
    if baseline_result.returncode:
        sys.stdout.write(baseline_result.stdout)
        raise SystemExit("canonical target fixture does not elaborate with declared import")

    candidate = canonical_fixture.replace(f"import {DIRECT_IMPORTS[0]}\n", "", 1)
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
        raise SystemExit(f"direct import is redundant: {DIRECT_IMPORTS[0]}")
    return {
        "fixture": "canonical target and its three local definitions only",
        "exit_code": str(result.returncode),
        "output_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
    }


def check_forbidden_constructs(source_text: str) -> None:
    without_comments = re.sub(r"/-.*?-/", "", source_text, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    match = re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b",
        without_comments,
    )
    if match:
        raise SystemExit(f"forbidden Lean construct: {match.group(0)}")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        raise SystemExit(f"missing final newline: {path}")
    if b"\r" in data or b"\x00" in data:
        raise SystemExit(f"invalid byte in {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        raise SystemExit(f"trailing whitespace in {path}")


def check_artifacts(payload: dict, worker_packet: Path | None) -> None:
    statement = load(STATEMENT_RECORD)
    receipt = load(RECEIPT)
    target_manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    target = next(
        row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM_ID
    )
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if target["execution_rank"] != 1377 or statement["execution_rank"] != 1377:
        raise SystemExit("target execution rank mismatch")
    if target["name"] != "Dilworth定理" or target["baseline"] != "L0":
        raise SystemExit("target manifest identity mismatch")
    if not target["rework_required"] or target["theorem_complete"]:
        raise SystemExit("target manifest lifecycle mismatch")
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement":
        raise SystemExit("statement DAG identity mismatch")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0819-INTAKE"]:
        raise SystemExit("statement DAG dependency/state mismatch")
    if item["owned_paths"] != ["Stage1_Instances/THM-M-0819"]:
        raise SystemExit("statement ownership mismatch")

    formal = statement["canonical_formal_target"]
    if statement["item_id"] != receipt["item_id"] or statement["item_id"] != ITEM_ID:
        raise SystemExit("item id mismatch")
    if statement["theorem_id"] != receipt["theorem_id"] or statement["theorem_id"] != THEOREM_ID:
        raise SystemExit("theorem id mismatch")
    if formal["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("canonical declaration mismatch")
    if formal["elaborated_expression_sha256"] != payload["elaborated_expression_sha256"]:
        raise SystemExit("statement expression hash mismatch")
    if formal["statement_file_sha256"] != payload["statement_file_sha256"]:
        raise SystemExit("statement source hash mismatch")
    if formal["support_definition_expression_sha256"] != payload[
        "support_definition_expression_sha256"
    ]:
        raise SystemExit("statement support-definition hash mismatch")
    if formal["statement_bundle_sha256"] != payload["statement_bundle_sha256"]:
        raise SystemExit("statement semantic bundle hash mismatch")
    if statement["direct_imports"] != payload["direct_imports"]:
        raise SystemExit("statement import mismatch")
    if statement["root_vector_before"] != {"H": "H1", "M": "M5", "R": "R3"}:
        raise SystemExit("incorrect statement input debt vector")
    if statement["root_vector_after"] != {"H": "H1", "M": "M3", "R": "R3"}:
        raise SystemExit("incorrect statement output debt vector")
    if not statement["statement_elaborated"]:
        raise SystemExit("statement not marked elaborated")
    if statement["theorem_proved"] or statement["audit_complete"] or statement["theorem_complete"]:
        raise SystemExit("statement record overclaims closure")
    if statement["accepted_receipt_ids"]:
        raise SystemExit("statement record claims accepted receipt")

    if receipt["proposed_state"] != "[_]" or receipt["accepted"]:
        raise SystemExit("receipt authority/state mismatch")
    if receipt["verdict"] != "no_state_change" or receipt["content_addressed"]:
        raise SystemExit("receipt boundary mismatch")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise SystemExit("receipt base mismatch")
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise SystemExit("worker HEAD moved from recorded base")
    if set(receipt["changed_paths"]) != CHANGED_PATHS:
        raise SystemExit("receipt changed-path mismatch")
    if receipt["statement_fingerprints"] != [
        f"sha256:{payload['elaborated_expression_sha256']}"
    ]:
        raise SystemExit("receipt statement fingerprint mismatch")
    if receipt["statement_file_sha256"] != payload["statement_file_sha256"]:
        raise SystemExit("receipt statement file hash mismatch")
    if receipt["statement_bundle_sha256"] != payload["statement_bundle_sha256"]:
        raise SystemExit("receipt statement bundle hash mismatch")
    if receipt["support_definition_expression_sha256"] != payload[
        "support_definition_expression_sha256"
    ]:
        raise SystemExit("receipt support-definition hash mismatch")
    if receipt["checker_sha256"] != sha256(Path(__file__)):
        raise SystemExit("receipt checker hash mismatch")
    if receipt["lean_output_sha256"] != payload["lean_output_sha256"]:
        raise SystemExit("receipt Lean output hash mismatch")
    if receipt["direct_imports"] != DIRECT_IMPORTS:
        raise SystemExit("receipt import mismatch")
    recorded_mutations = {
        row["declaration"]: row["expression_sha256"] for row in receipt["mutation_tests"]
    }
    if recorded_mutations != payload["mutation_expression_sha256"]:
        raise SystemExit("receipt mutation fingerprint mismatch")
    if receipt["root_vector_before"] != statement["root_vector_before"]:
        raise SystemExit("receipt input debt vector mismatch")
    if receipt["root_vector_after"] != statement["root_vector_after"]:
        raise SystemExit("receipt output debt vector mismatch")
    if receipt["accepted_receipt_ids"] or receipt["proof_body_locations"]:
        raise SystemExit("receipt claims proof or acceptance")
    if receipt["audit_complete"] or receipt["theorem_complete"]:
        raise SystemExit("receipt overclaims closure")
    if receipt["selftest_result"] != "pass" or not receipt["commands_and_results"]:
        raise SystemExit("receipt self-test evidence is incomplete")
    expected_cut_set = [
        "S56-M-0819-INTAKE",
        "S56-M-0819-STATEMENT",
        "S56-M-0819-ANCHOR_AUDIT",
        "S56-M-0819-OBLIGATION_TREE",
        "S56-M-0819-PROOF",
        "S56-M-0819-VALIDATION",
        "S56-M-0819-RELEASE",
    ]
    if receipt["remaining_root_cut_set"] != expected_cut_set:
        raise SystemExit("receipt root cut set omits an unfinished dependency")

    for key, relative in SOURCE_INPUTS.items():
        if receipt["source_inputs"].get(key) != f"sha256:{sha256(ROOT / relative)}":
            raise SystemExit(f"stale receipt source hash: {key}")
    for key, relative in OWNED_INPUTS.items():
        if receipt["source_inputs"].get(key) != f"sha256:{sha256(ROOT / relative)}":
            raise SystemExit(f"stale owned intake input hash: {key}")
    mathlib = LEAN_DIR / ".lake/packages/mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        raise SystemExit("mathlib revision mismatch")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        raise SystemExit("mathlib tree mismatch")
    if git("status", "--short", cwd=mathlib):
        raise SystemExit("mathlib worktree is dirty")
    direct_source = mathlib / "Mathlib/Order/Antichain.lean"
    if receipt["worker_input_hashes"][DIRECT_IMPORTS[0]] != f"sha256:{sha256(direct_source)}":
        raise SystemExit("direct import source hash mismatch")

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    if worker_packet is not None:
        packet = load(worker_packet)
        if set(packet) != {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }:
            raise SystemExit("worker packet schema mismatch")
        if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet state mismatch")
        if packet["base_revision"] != BASE_REVISION:
            raise SystemExit("worker packet base mismatch")
        if set(packet["changed_paths"]) != CHANGED_PATHS:
            raise SystemExit("worker packet changed-path mismatch")
        if packet["known_failures"] != receipt["known_failures"]:
            raise SystemExit("worker packet failure ledger mismatch")
        if not packet["commands"] or not packet["output_summary"]:
            raise SystemExit("worker packet evidence missing")
        check_text_file(worker_packet)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)
    import_failure = check_minimal_import(source_text)

    serialized = {}
    outputs = {}
    for declaration in [CANONICAL, *MUTATIONS]:
        serialized[declaration], outputs[declaration] = expression(declaration)
    canonical = serialized[CANONICAL]
    survivors = [name for name in MUTATIONS if serialized[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    support = {
        declaration: support_expression(declaration)
        for declaration in ["HasExactly", "IsDependent", "IsDisjointChainDecomposition"]
    }
    support_hashes = {
        declaration: hashlib.sha256(value.encode()).hexdigest()
        for declaration, value in support.items()
    }
    bundle_input = json.dumps(
        {"canonical": canonical, "support": support},
        sort_keys=True,
        separators=(",", ":"),
    )

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    payload = {
        "direct_imports": DIRECT_IMPORTS,
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": MUTATIONS,
        "lean_output_sha256": hashlib.sha256(outputs[CANONICAL].encode()).hexdigest(),
        "mathlib_revision": mathlib_revision,
        "minimal_import_deletion_failure": import_failure,
        "mutation_expression_sha256": {
            name: hashlib.sha256(serialized[name].encode()).hexdigest() for name in MUTATIONS
        },
        "statement_bundle_sha256": hashlib.sha256(bundle_input.encode()).hexdigest(),
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "support_definition_expression_sha256": support_hashes,
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
    }
    check_artifacts(payload, args.worker_packet)
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
