#!/usr/bin/env python3
"""Validate the exact THM-M-0912 statement and its identity fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
STATEMENT_RECORD = SOURCE.with_name("statement.json")
RECEIPT = SOURCE.with_name("statement-receipt.json")
NAMESPACE = "Stage1Instances.THM_M_0912"
CANONICAL = "PascalIdentityTarget"
MUTATIONS = [
    "mutationRemovedPositiveColumnHypothesis",
    "mutationChangedDomainToFinTen",
    "mutationChangedColumnBinderScope",
    "mutationExcludesDiagonal",
]
DIRECT_IMPORTS = ["Mathlib.Data.Nat.Choose.Basic"]
ITEM_ID = "S56-M-0912-STATEMENT"
THEOREM_ID = "THM-M-0912"
BASE_REVISION = "fb0baac89ea0633612be3b47448464b4b8e4bef7"
BASE_TREE = "018557070da18ea1733a82de81a238750c59aa84"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ENVIRONMENT_FINGERPRINT = "8e8dc7bd4f64ddaca552ca92399f15d52a008ac0d44ad8db83731f9c453b0749"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0912/README.md",
    "Stage1_Instances/THM-M-0912/Statement.lean",
    "Stage1_Instances/THM-M-0912/check_statement.py",
    "Stage1_Instances/THM-M-0912/check_intake.py",
    "Stage1_Instances/THM-M-0912/statement-receipt.json",
    "Stage1_Instances/THM-M-0912/statement-validation.md",
    "Stage1_Instances/THM-M-0912/statement.json",
    "Stage1_Instances/THM-M-0912/instance.json",
    "Stage1_Instances/THM-M-0912/scope-map.md",
    "Stage1_Instances/THM-M-0912/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0912/task-dag.json",
}
SOURCE_INPUTS = {
    path: path
    for path in [
        "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "skills/execute-stage1-rev56/SKILL.md",
        "Docs/Blueprint_Guidelines.md",
        "Docs/researches/math_theorems.md",
        "Docs/Stage0_Blueprint.md",
        "Formalizations/Lean/lean-toolchain",
        "Formalizations/Lean/lake-manifest.json",
        "Stage1_Instances/THM-M-0912/intake-receipt.json",
    ]
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
        "w", suffix=".lean", delete=False, encoding="utf-8"
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


def check_mutation_fixtures(source_text: str) -> None:
    required = [
        "#check_failure\n  (rfl : PascalIdentityTarget = mutationRemovedPositiveColumnHypothesis)",
        "#check_failure\n  (rfl : PascalIdentityTarget = mutationChangedDomainToFinTen)",
        "#check_failure\n  (rfl : PascalIdentityTarget = mutationChangedColumnBinderScope)",
        "#check_failure\n  (rfl : PascalIdentityTarget = mutationExcludesDiagonal)",
        "theorem positivity_hypothesis_is_semantic",
        "theorem row_ten_has_no_fin_ten_representation",
        "theorem existential_column_scope_fails_at_zero",
        "theorem strict_boundary_excludes_diagonal",
    ]
    missing = [fixture for fixture in required if source_text.count(fixture) != 1]
    if missing:
        raise SystemExit(f"mutation fixture missing or ambiguous: {missing}")


def check_minimal_import(source_text: str) -> dict[str, str | int]:
    actual = [
        line.removeprefix("import ")
        for line in source_text.splitlines()
        if line.startswith("import ")
    ]
    if actual != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {actual}")

    canonical_start = "/-- The exact DLMF 26.3.5 predecessor recurrence"
    canonical_end = "/-- The same source constraint represented as one conjunction. -/"
    if source_text.count(canonical_start) != 1 or source_text.count(canonical_end) != 1:
        raise SystemExit("canonical fixture marker is missing or ambiguous")
    fixture = (
        source_text[: source_text.index(canonical_start)]
        + source_text[
            source_text.index(canonical_start) : source_text.index(canonical_end)
        ]
        + "\nend Stage1Instances.THM_M_0912\n"
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", delete=False, encoding="utf-8"
    ) as handle:
        handle.write(fixture)
        baseline = Path(handle.name)
    try:
        baseline_result = run_lean(baseline)
    finally:
        baseline.unlink()
    if baseline_result.returncode:
        sys.stdout.write(baseline_result.stdout)
        raise SystemExit("canonical target fixture did not elaborate")

    candidate = fixture.replace(f"import {DIRECT_IMPORTS[0]}\n", "", 1)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", delete=False, encoding="utf-8"
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
        "exit_code": result.returncode,
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

    if target["execution_rank"] != 1454 or statement["execution_rank"] != 1454:
        raise SystemExit("execution rank mismatch")
    if target["name"] != "帕斯卡恒等式" or target["baseline"] != "L0":
        raise SystemExit("target manifest identity mismatch")
    if not target["rework_required"] or target["theorem_complete"]:
        raise SystemExit("target lifecycle mismatch")
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement":
        raise SystemExit("statement DAG identity mismatch")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0912-INTAKE"]:
        raise SystemExit("statement DAG dependency/state mismatch")
    if item["owned_paths"] != ["Stage1_Instances/THM-M-0912"]:
        raise SystemExit("statement ownership mismatch")

    formal = statement["canonical_formal_target"]
    if statement["item_id"] != ITEM_ID or receipt["item_id"] != ITEM_ID:
        raise SystemExit("item id mismatch")
    if statement["theorem_id"] != THEOREM_ID or receipt["theorem_id"] != THEOREM_ID:
        raise SystemExit("theorem id mismatch")
    if formal["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("canonical declaration mismatch")
    if formal.get("backend") != "lean4" or statement.get("lifecycle_mode") != "planned":
        raise SystemExit("statement backend/lifecycle mismatch")
    if not statement.get("canonical_statement") or not statement.get("domain_and_universes"):
        raise SystemExit("canonical human statement or domain record missing")
    if statement.get("authoritative_blueprint") != "Docs/Stage1_Blueprint_rev-5.6.md":
        raise SystemExit("authoritative blueprint mismatch")
    if statement.get("obligation_registry_hash") is not None:
        raise SystemExit("statement phase must not invent an obligation registry hash")
    if statement.get("discovery_protocol_hash") is not None:
        raise SystemExit("statement phase must not invent a discovery protocol hash")
    if statement.get("ordered_binders") != [
        "m : Nat", "n : Nat", "hnm : n <= m", "hn : 1 <= n"
    ]:
        raise SystemExit("ordered binder record mismatch")
    if statement.get("hypotheses") != ["n <= m", "1 <= n"]:
        raise SystemExit("hypothesis record mismatch")
    if formal.get("unresolved_metavariables") is not False:
        raise SystemExit("formal target metavariable state is not closed")
    if formal["elaborated_expression_sha256"] != payload["elaborated_expression_sha256"]:
        raise SystemExit("statement expression hash mismatch")
    if formal["statement_file_sha256"] != payload["statement_file_sha256"]:
        raise SystemExit("statement file hash mismatch")
    if statement["direct_imports"] != DIRECT_IMPORTS:
        raise SystemExit("statement import mismatch")
    alternates = statement.get("alternate_encodings", [])
    expected_witnesses = {
        f"{NAMESPACE}.pascalIdentityTarget_iff_dlmfConjunctionTarget",
        f"{NAMESPACE}.pascalIdentityTarget_iff_mathlibSummandOrderTarget",
        f"{NAMESPACE}.pascalIdentityTarget_iff_restrictedSuccessorTarget",
    }
    if {row.get("checked_witness") for row in alternates} != expected_witnesses:
        raise SystemExit("checked alternate encoding record mismatch")
    if any(row.get("relationship") != "iff" for row in alternates):
        raise SystemExit("alternate encoding relationship mismatch")
    environment = statement.get("environment_fingerprint", {})
    if environment.get("base_revision") != BASE_REVISION:
        raise SystemExit("statement environment base mismatch")
    if environment.get("mathlib_revision") != MATHLIB_REVISION:
        raise SystemExit("statement environment mathlib mismatch")
    serialization = environment.get("canonical_serialization")
    if not isinstance(serialization, str):
        raise SystemExit("canonical environment serialization missing")
    if hashlib.sha256(serialization.encode()).hexdigest() != ENVIRONMENT_FINGERPRINT:
        raise SystemExit("computed environment fingerprint mismatch")
    if environment.get("canonical_sha256") != ENVIRONMENT_FINGERPRINT:
        raise SystemExit("recorded environment fingerprint mismatch")
    instance = load(ROOT / "Stage1_Instances/THM-M-0912/instance.json")
    if instance["canonical_statement"] != statement["canonical_statement"]:
        raise SystemExit("instance/statement human target mismatch")
    if instance["canonical_formal_target"]["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("instance/statement declaration mismatch")
    if instance["canonical_formal_target"]["elaborated_expression_hash"] != (
        f"sha256:{payload['elaborated_expression_sha256']}"
    ):
        raise SystemExit("instance/statement expression fingerprint mismatch")
    if instance["canonical_formal_target"]["environment_fingerprint"] != (
        f"sha256:{ENVIRONMENT_FINGERPRINT}"
    ):
        raise SystemExit("instance/statement environment fingerprint mismatch")
    task_dag = load(ROOT / "Stage1_Instances/THM-M-0912/task-dag.json")
    local_item = next(row for row in task_dag["tasks"] if row["id"] == ITEM_ID)
    if local_item.get("provisional_evidence_ids") != [receipt["receipt_id"]]:
        raise SystemExit("local task/receipt provisional evidence mismatch")
    if not statement["statement_elaborated"]:
        raise SystemExit("statement is not marked elaborated")
    if statement["root_vector_before"] != statement["root_vector_after"]:
        raise SystemExit("unexpected debt transition")
    if statement["root_vector_after"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("incorrect debt vector")
    if statement["theorem_proved"] or statement["audit_complete"] or statement["theorem_complete"]:
        raise SystemExit("statement record overclaims closure")
    if statement["accepted_receipt_ids"]:
        raise SystemExit("statement record claims acceptance")

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
        raise SystemExit("receipt expression fingerprint mismatch")
    for field in ["statement_file_sha256", "lean_output_sha256"]:
        if receipt[field] != payload[field]:
            raise SystemExit(f"receipt {field} mismatch")
    if receipt["checker_sha256"] != sha256(Path(__file__)):
        raise SystemExit("receipt checker hash mismatch")
    intake_checker = ROOT / "Stage1_Instances/THM-M-0912/check_intake.py"
    if receipt.get("reconciled_intake_checker_sha256") != sha256(intake_checker):
        raise SystemExit("receipt intake checker hash mismatch")
    if receipt["direct_imports"] != DIRECT_IMPORTS:
        raise SystemExit("receipt import mismatch")
    if receipt["root_vector_before"] != receipt["root_vector_after"]:
        raise SystemExit("receipt debt transition mismatch")
    if receipt["root_vector_after"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("receipt debt vector mismatch")
    if receipt["accepted_receipt_ids"] or receipt["proof_body_locations"]:
        raise SystemExit("receipt claims proof or acceptance")
    if receipt["audit_complete"] or receipt["theorem_complete"]:
        raise SystemExit("receipt overclaims closure")
    if receipt["selftest_result"] != "pass" or not receipt["commands_and_results"]:
        raise SystemExit("receipt evidence is unfinished")
    expected_cut_set = [
        "S56-M-0912-INTAKE",
        "S56-M-0912-STATEMENT",
        "S56-M-0912-ANCHOR_AUDIT",
        "S56-M-0912-OBLIGATION_TREE",
        "S56-M-0912-PROOF",
        "S56-M-0912-VALIDATION",
        "S56-M-0912-RELEASE",
    ]
    if receipt["remaining_root_cut_set"] != expected_cut_set:
        raise SystemExit("receipt root cut set mismatch")
    unfinished_token = "PEND" + "ING"
    if unfinished_token in json.dumps(receipt) or unfinished_token in json.dumps(statement):
        raise SystemExit("unfinished marker in finalized artifacts")

    for key, relative in SOURCE_INPUTS.items():
        expected = f"sha256:{sha256(ROOT / relative)}"
        if receipt["source_inputs"].get(key) != expected:
            raise SystemExit(f"stale receipt source hash: {key}")
    reconciled = receipt["source_inputs"].get("statement_phase_reconciled_inputs", "")
    for relative in [
        "Stage1_Instances/THM-M-0912/instance.json",
        "Stage1_Instances/THM-M-0912/scope-map.md",
        "Stage1_Instances/THM-M-0912/source-statement-crosswalk.md",
        "Stage1_Instances/THM-M-0912/task-dag.json",
    ]:
        if f"{Path(relative).name} sha256 {sha256(ROOT / relative)}" not in reconciled:
            raise SystemExit(f"stale reconciled input hash: {relative}")
    mathlib = LEAN_DIR / ".lake/packages/mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        raise SystemExit("mathlib revision mismatch")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        raise SystemExit("mathlib tree mismatch")
    if git("status", "--short", cwd=mathlib):
        raise SystemExit("mathlib worktree is dirty")
    direct_source = mathlib / "Mathlib/Data/Nat/Choose/Basic.lean"
    if receipt["worker_input_hashes"][DIRECT_IMPORTS[0]] != f"sha256:{sha256(direct_source)}":
        raise SystemExit("direct import source hash mismatch")

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    if worker_packet is not None:
        packet = load(worker_packet)
        if set(packet) != {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }:
            raise SystemExit("worker packet schema mismatch")
        if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet state mismatch")
        if packet["base_revision"] != BASE_REVISION:
            raise SystemExit("worker packet base mismatch")
        if set(packet["changed_paths"]) != CHANGED_PATHS:
            raise SystemExit("worker packet changed-path mismatch")
        if packet["known_failures"] != receipt["known_failures"]:
            raise SystemExit("worker packet known-failure mismatch")
        if not packet["commands"] or not packet["output_summary"]:
            raise SystemExit("worker packet evidence missing")
        check_text_file(worker_packet)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument("--measure-only", action="store_true")
    args = parser.parse_args()

    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)
    check_mutation_fixtures(source_text)
    import_failure = check_minimal_import(source_text)
    serialized: dict[str, str] = {}
    outputs: dict[str, str] = {}
    for declaration in [CANONICAL, *MUTATIONS]:
        serialized[declaration], outputs[declaration] = expression(declaration)
    survivors = [name for name in MUTATIONS if serialized[name] == serialized[CANONICAL]]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"]
        for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    payload = {
        "direct_imports": DIRECT_IMPORTS,
        "elaborated_expression_sha256": hashlib.sha256(
            serialized[CANONICAL].encode()
        ).hexdigest(),
        "killed_mutations": MUTATIONS,
        "lean_output_sha256": hashlib.sha256(outputs[CANONICAL].encode()).hexdigest(),
        "mathlib_revision": mathlib_revision,
        "minimal_import_deletion_failure": import_failure,
        "mutation_expression_sha256": {
            name: hashlib.sha256(serialized[name].encode()).hexdigest()
            for name in MUTATIONS
        },
        "statement_file_sha256": sha256(SOURCE),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
    }
    if not args.measure_only:
        check_artifacts(payload, args.worker_packet)
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
