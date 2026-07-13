#!/usr/bin/env python3
"""Cross-check the THM-M-0841 statement record, receipt, and worker packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0841-STATEMENT"
THEOREM_ID = "THM-M-0841"
BASE_REVISION = "a3b18eec39bf04be025b1641cae02f4d44fdf11a"
EXPRESSION_SHA256 = "ed4a8b422615bfafc69ab9f770dc99b77d308d78bca30e67790206426799a733"
ENVIRONMENT_SHA256 = "ec81286c0a60baa4a23af792af268e7efe87bed50264292a02f5646443bd276d"
SOURCE_SHA256 = "897dcc398df34c0dd6ad02dc2092a08f46a6cafc908c2e9f8497a895aa66663d"
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0841/README.md",
    "Stage1_Instances/THM-M-0841/Statement.lean",
    "Stage1_Instances/THM-M-0841/check_statement.py",
    "Stage1_Instances/THM-M-0841/check_statement_artifacts.py",
    "Stage1_Instances/THM-M-0841/instance.json",
    "Stage1_Instances/THM-M-0841/scope-map.md",
    "Stage1_Instances/THM-M-0841/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0841/statement-receipt.json",
    "Stage1_Instances/THM-M-0841/statement-validation.md",
    "Stage1_Instances/THM-M-0841/statement.json",
    "Stage1_Instances/THM-M-0841/task-dag.json",
]
OWNED_FILES = {
    "README.md",
    "instance.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "IntakeProbe.lean",
    "check_intake.py",
    "validation.md",
    "intake-receipt.json",
    "Statement.lean",
    "check_statement.py",
    "check_statement_artifacts.py",
    "statement.json",
    "statement-receipt.json",
    "statement-validation.md",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise SystemExit(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_lean_comments(source: str) -> str:
    result: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            result.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                result.append("\n")
            index += 1
        else:
            result.append(source[index])
            index += 1
    if depth:
        raise SystemExit("unterminated Lean block comment")
    return "".join(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    if actual_files != OWNED_FILES:
        raise SystemExit(f"owned file inventory mismatch: {actual_files ^ OWNED_FILES}")

    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    if statement["schema_version"] != "stage1-statement/1.0":
        raise SystemExit("statement schema mismatch")
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        raise SystemExit("receipt schema mismatch")
    if statement["normative_profile"] != "machine-theorem-assurance/1.0":
        raise SystemExit("statement normative profile mismatch")
    if receipt["normative_profile"] != statement["normative_profile"]:
        raise SystemExit("receipt normative profile mismatch")
    if statement["formal_system"] != "Lean 4 + pinned mathlib under the rev-5.6 adapter":
        raise SystemExit("formal system mismatch")
    authority = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in authority["items"] if row["id"] == ITEM_ID)
    if not (
        item["theorem_id"] == THEOREM_ID
        and item["execution_rank"] == 1398
        and item["phase"] == "statement"
        and item["layer"] == 1
        and item["state"] == "[ ]"
        and item["depends_on"] == ["S56-M-0841-INTAKE"]
        and item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    ):
        raise SystemExit("authoritative statement item changed")
    local_task = next(row for row in dag["tasks"] if row["id"] == ITEM_ID)
    if local_task["state"] != "open" or local_task["evidence_ids"] != []:
        raise SystemExit("local task must remain open pending master acceptance")

    if statement["item_id"] != receipt["item_id"] or receipt["item_id"] != ITEM_ID:
        raise SystemExit("statement item identity mismatch")
    if statement["theorem_id"] != receipt["theorem_id"] or receipt["theorem_id"] != THEOREM_ID:
        raise SystemExit("theorem identity mismatch")
    if statement["lifecycle_mode"] != instance["lifecycle_mode"] or instance["lifecycle_mode"] != "planned":
        raise SystemExit("lifecycle mismatch")
    if not statement["statement_elaborated"]:
        raise SystemExit("statement elaboration is not recorded")
    if statement["theorem_proved"] or statement["audit_complete"]:
        raise SystemExit("statement artifact overclaims proof or audit completion")
    if statement["theorem_complete"] or instance["theorem_complete"] or receipt["theorem_complete"]:
        raise SystemExit("statement artifact overclaims theorem completion")

    formal = statement["canonical_formal_target"]
    if formal["declaration_or_expression"] != f"Stage1Instances.THM_M_0841.ErdosStoneTarget":
        raise SystemExit("canonical declaration mismatch")
    if formal["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise SystemExit("statement expression fingerprint is stale")
    if formal["environment_fingerprint_sha256"] != ENVIRONMENT_SHA256:
        raise SystemExit("statement environment fingerprint is stale")
    if formal["statement_file_sha256"] != SOURCE_SHA256 or sha256(HERE / "Statement.lean") != SOURCE_SHA256:
        raise SystemExit("Statement.lean hash is stale")
    if instance["canonical_formal_target"]["elaborated_expression_hash"] != f"sha256:{EXPRESSION_SHA256}":
        raise SystemExit("instance expression fingerprint is stale")
    if instance["canonical_formal_target"]["declaration_or_expression"] != formal["declaration_or_expression"]:
        raise SystemExit("instance declaration mismatch")

    if receipt["phase"] != "statement" or receipt["intent"] != "statement":
        raise SystemExit("receipt phase mismatch")
    if receipt["receipt_class"] != "provisional_worker_selftest":
        raise SystemExit("receipt class mismatch")
    if receipt["proposed_state"] != "[_]" or receipt["accepted"]:
        raise SystemExit("receipt must remain provisional")
    if receipt["content_addressed"] or receipt["base_revision"] != BASE_REVISION:
        raise SystemExit("receipt snapshot boundary mismatch")
    if "Master acceptance must recapture" not in receipt["content_addressing_boundary"]:
        raise SystemExit("provisional content-addressing boundary missing")
    if receipt["statement_fingerprints"] != [f"sha256:{EXPRESSION_SHA256}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("receipt source hash is stale")
    if receipt["environment_fingerprint_sha256"] != ENVIRONMENT_SHA256:
        raise SystemExit("receipt environment fingerprint is stale")
    if receipt["changed_paths"] != CHANGED_PATHS:
        raise SystemExit("receipt changed_paths mismatch")
    if receipt["root_vector_before"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("unexpected root vector before")
    if receipt["root_vector_after"] != receipt["root_vector_before"]:
        raise SystemExit("statement work must not overpromote the root vector")
    if receipt["accepted_receipt_ids"] or receipt["proof_body_locations"]:
        raise SystemExit("statement receipt cannot accept proof evidence")
    if receipt["canonical_obligation_ids"] or receipt["typed_graph_changes"]:
        raise SystemExit("later-phase artifacts must remain empty")
    if receipt["composition_certificates"] or receipt["audit_complete"]:
        raise SystemExit("later-phase composition or audit claim found")
    if receipt["selftest_result"] != "pass":
        raise SystemExit("receipt does not record a passing self-test")

    recipe_ids = {recipe["recipe_id"] for recipe in receipt["structured_validation_recipes"]}
    if recipe_ids != {
        "S56-M-0841-STATEMENT-RECIPE-LEAN",
        "S56-M-0841-STATEMENT-RECIPE-CHECKER",
        "S56-M-0841-STATEMENT-RECIPE-ARTIFACTS",
    }:
        raise SystemExit("structured recipe inventory mismatch")
    for recipe in receipt["structured_validation_recipes"]:
        if recipe["network_policy"] != "denied" or recipe["expected_exit"] != 0:
            raise SystemExit("structured recipe policy mismatch")
        if recipe["env_allowlist"] != {
            "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"
        }:
            raise SystemExit("structured recipe environment mismatch")
        if recipe["covered_obligation_ids"] != [ITEM_ID]:
            raise SystemExit("structured recipe coverage mismatch")
        if not recipe["covered_declarations"] or not recipe["expected_outputs"]:
            raise SystemExit("structured recipe lacks declaration or output coverage")

    source_hashes = receipt["source_inputs"]
    for relative in (
        "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "skills/execute-stage1-rev56/SKILL.md",
        "Docs/Blueprint_Guidelines.md",
        "Formalizations/Lean/lean-toolchain",
        "Formalizations/Lean/lake-manifest.json",
    ):
        expected = f"sha256:{sha256(ROOT / relative)}"
        if source_hashes[relative] != expected:
            raise SystemExit(f"receipt source hash is stale: {relative}")
    if instance["source_revisions"]["authoritative_blueprint_sha256"] != sha256(
        ROOT / "Docs/Stage1_Blueprint_rev-5.6.md"
    ):
        raise SystemExit("instance blueprint hash is stale")
    if instance["source_revisions"]["execution_dag_sha256"] != sha256(
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    ):
        raise SystemExit("instance execution DAG hash is stale")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    if mathlib_revision != receipt["worker_input_hashes"]["mathlib_revision"]:
        raise SystemExit("mathlib revision mismatch")
    for relative, tagged_hash in receipt["validator_hashes"].items():
        algorithm, expected = tagged_hash.split(":", 1)
        if algorithm != "sha256" or sha256(ROOT / relative) != expected:
            raise SystemExit(f"validator hash mismatch: {relative}")
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    mathlib_tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip()
    if mathlib_tree != receipt["worker_input_hashes"]["mathlib_tree"]:
        raise SystemExit("mathlib tree mismatch")
    if subprocess.check_output(["git", "status", "--short"], cwd=mathlib, text=True).strip():
        raise SystemExit("pinned mathlib worktree is dirty")

    env = os.environ.copy()
    env.update({"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"})
    result = subprocess.run(
        ["python3", "-B", str(HERE / "check_statement.py")],
        cwd=LEAN_DIR,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    payload = json.loads(result.stdout)
    if payload["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise SystemExit("fresh elaborated expression disagrees with metadata")
    if payload["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("fresh source hash disagrees with metadata")
    if payload["environment_fingerprint_sha256"] != ENVIRONMENT_SHA256:
        raise SystemExit("fresh environment fingerprint disagrees with metadata")
    if payload["direct_imports"] != receipt["direct_imports"]:
        raise SystemExit("fresh direct imports disagree with receipt")
    if payload["direct_import_source_sha256"] != {
        "Mathlib.Analysis.SpecialFunctions.Log.Basic":
            receipt["worker_input_hashes"]["mathlib_log_basic_source_sha256"],
        "Mathlib.Combinatorics.SimpleGraph.CompleteMultipartite":
            receipt["worker_input_hashes"]["mathlib_complete_multipartite_source_sha256"],
    }:
        raise SystemExit("fresh import-source hashes disagree with receipt")
    if payload["lean_output_sha256"] != receipt["lean_output_sha256"]:
        raise SystemExit("fresh Lean output hash disagrees with receipt")
    if payload["mathlib_revision"] != receipt["worker_input_hashes"]["mathlib_revision"]:
        raise SystemExit("fresh mathlib revision disagrees with receipt")
    if payload["toolchain"] != "leanprover/lean4:v4.29.0":
        raise SystemExit("fresh toolchain disagrees with receipt")
    expected_mutations = [entry["declaration"] for entry in receipt["mutation_tests"]]
    if payload["killed_mutations"] != expected_mutations:
        raise SystemExit("fresh mutation inventory disagrees with receipt")
    if set(payload["minimal_import_deletion_failures"]) != set(receipt["direct_imports"]):
        raise SystemExit("fresh import-deletion inventory disagrees with receipt")
    if payload["transports"] != ["erdosStoneTarget_iff_expandedSourceTarget"]:
        raise SystemExit("fresh transport inventory mismatch")
    if payload["validated_boundaries"] != [
        "iteratedLog_zero", "iteratedLog_one", "one_part_excluded",
        "zero_tolerance_excluded", "one_tolerance_excluded",
    ]:
        raise SystemExit("fresh boundary inventory mismatch")

    lean = (HERE / "Statement.lean").read_text(encoding="utf-8")
    stripped = strip_lean_comments(lean)
    if re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", stripped):
        raise SystemExit("prohibited Lean construct in statement module")

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            raise SystemExit(f"invalid text file framing: {path.name}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            raise SystemExit(f"trailing whitespace: {path.name}")

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        if set(packet) != {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }:
            raise SystemExit("worker packet schema mismatch")
        if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet identity/state mismatch")
        if packet["base_revision"] != BASE_REVISION:
            raise SystemExit("worker packet base revision mismatch")
        if packet["changed_paths"] != receipt["changed_paths"]:
            raise SystemExit("worker packet changed_paths mismatch")
        if packet["commands"] != receipt["worker_packet_commands"]:
            raise SystemExit("worker packet commands mismatch")
        if packet["output_summary"] != receipt["output_summary"]:
            raise SystemExit("worker packet output summary mismatch")
        if packet["known_failures"] != receipt["known_failures"]:
            raise SystemExit("worker packet failure boundary mismatch")

    print("statement artifact check: ok (THM-M-0841; provisional; theorem_complete false)")


if __name__ == "__main__":
    main()
