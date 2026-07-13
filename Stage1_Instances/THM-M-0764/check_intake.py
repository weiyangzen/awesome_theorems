#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0764 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0764"
ITEM_ID = "S56-M-0764-INTAKE"
RANK = 1350
BASE_REVISION = "fd0fab2ab7f4f514a5cc625bbce92879e718ba13"
BASE_TREE = "4116d53bcf2573069e4b67205353fe3469dbe7bd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
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
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
SOURCE_HASH_FIELDS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "repository_cs_source_sha256": "Docs/researches/cs_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_SOURCE_HASH_FIELDS = {
    "context_free_grammar_source_sha256": "Mathlib/Computability/ContextFreeGrammar.lean",
    "language_source_sha256": "Mathlib/Computability/Language.lean",
    "stack_turing_machine_source_sha256": (
        "Mathlib/Computability/TuringMachine/StackTuringMachine.lean"
    ),
}
EXCERPT_HASHES = {
    ("Docs/researches/math_theorems.md", 5626, 5631): (
        "repository_record_excerpt_sha256",
        "cf2c3c79c4643376e86adf8d22e397f7e846bd399d70e72da519c3619be80f4a",
    ),
    ("Docs/Stage0_Blueprint.md", 20866, 20891): (
        "stage0_excerpt_sha256",
        "7661c3b0ed1afd64aacd4f8cd86806a4842cb6f6e9e3daf84f6c5168f8d0e715",
    ),
    ("Docs/researches/cs_theorems.md", 241, 250): (
        "neighbor_repository_excerpt_sha256",
        "5eaff2c09594561d3000c1c471f7a21ee8da7589874e0f0fa301b2ab15bc6411",
    ),
    ("Docs/Stage0_Blueprint.md", 85358, 85385): (
        "neighbor_stage0_excerpt_sha256",
        "ec1a0aa14bc0486be734169ee9a09addc442ed1cbbdc9589eaf4a2199c0644fe",
    ),
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owned_content_sha256() -> str:
    digest = hashlib.sha256()
    for name in sorted(OWNED_FILES - {"intake-receipt.json"}):
        path = HERE / name
        digest.update(name.encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def git_file_sha256(revision: str, relative: str) -> str:
    data = subprocess.check_output(["git", "show", f"{revision}:{relative}"], cwd=ROOT)
    return hashlib.sha256(data).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    data = path.read_bytes()
    assert data.endswith(b"\n"), "worker packet is missing a final newline"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def check_authorities(instance: dict, dag: dict, receipt: dict) -> None:
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "下推自动机",
        "category": "数理逻辑 / 递归论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "category",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "source_status_untrusted",
        "lifecycle_mode",
        "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]", "[x]"} and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    assert isinstance(item["attempts"], int) and item["attempts"] >= 0
    assert item["children"] == []

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0764-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["audit_complete"] is dag["theorem_complete"] is False
    assert dag["accepted_states"] == []
    for layer, task in enumerate(dag["tasks"], start=1):
        authoritative = next(row for row in execution["items"] if row["id"] == task["id"])
        for field in (
            "phase",
            "layer",
            "depends_on",
            "owned_paths",
            "deliverable",
            "completion_gate",
        ):
            assert task[field] == authoritative[field]
        assert task["layer"] == layer and task["evidence_ids"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]


def check_instance(instance: dict, receipt: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "pushdown_automaton_context_free_language" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert formal["backend"] == "lean4" and "blocked" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["first_failed_gate"] == "master_acceptance_of_provisional_intake"
    assert receipt["retry_condition"]
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert {recipe["recipe_id"] for recipe in receipt["validation_recipes"]} == {
        "S56-M-0764-INTAKE-RECIPE-INVARIANTS",
        "S56-M-0764-INTAKE-RECIPE-LEAN-PROBE",
    }
    for recipe in receipt["validation_recipes"]:
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_ids"] == [ITEM_ID]
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []

    boundaries = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert boundaries == {"THM-M-0762", "THM-M-0763", "THM-M-0765", "THM-C-0141"}
    assert any(
        row["theorem_id"] == "THM-C-0141" and "no accepted alias" in row["relationship"]
        for row in instance["neighbor_target_boundaries"]
    )
    assert instance["source_status"].startswith("H1_")
    assert "M3 is definition/interface debt" in instance["status_boundary"]
    assert "no explicitly named" in instance["bounded_formal_search_observation"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
        cwd=ROOT,
        check=False,
    ).returncode == 0
    assert revisions["repository_source_record_commit"] == SOURCE_RECORD_COMMIT
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == (
        revisions["repository_source_record_blob"]
    ) == SOURCE_RECORD_BLOB
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == (
        revisions["current_repository_math_source_blob"]
    )
    for (relative, first, last), (field, expected) in EXCERPT_HASHES.items():
        actual = excerpt_sha256(ROOT / relative, first, last)
        assert actual == revisions[field] == expected, f"changed excerpt: {relative}:{first}-{last}"
    mutable_projection_fields = {
        "authoritative_blueprint_sha256",
        "execution_dag_sha256",
    }
    for field, relative in SOURCE_HASH_FIELDS.items():
        expected = (
            git_file_sha256(BASE_REVISION, relative)
            if field in mutable_projection_fields
            else sha256(ROOT / relative)
        )
        assert revisions[field] == expected, f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"changed mathlib source: {relative}"

    search_roots = [
        ROOT / "Formalizations/Lean/AwesomeTheorems",
        mathlib / "Mathlib",
    ]
    topic_pattern = re.compile(
        r"\b(?:pushdown|push-down|pda)\b|context[ -]free.*autom",
        re.IGNORECASE,
    )
    topic_matches = []
    for search_root in search_roots:
        for path in search_root.rglob("*.lean"):
            if topic_pattern.search(path.read_text(encoding="utf-8")):
                topic_matches.append(path)
    assert topic_matches == [], "bounded exact-topic observation is stale"

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**下推自动机**" in catalog
    assert "- 陈述: 上下文无关语言的识别" in catalog
    cs_catalog = (ROOT / "Docs/researches/cs_theorems.md").read_text(encoding="utf-8")
    assert "**CFG与PDA等价性**" in cs_catalog
    assert "上下文无关文法与下推自动机等价" in cs_catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0764 下推自动机" in stage0 and "THM-C-0141 CFG与PDA等价性" in stage0


def check_artifacts(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["selftest_result"] == "pass"
    assert receipt["covered_node_ids"] == receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["known_failures"] and receipt["first_failed_theorem_gate"]
    expected_owned_hash = receipt["dirty_input_evidence"]["owned_artifact_content_sha256"]
    if "--worker-packet" in sys.argv:
        assert owned_content_sha256() == expected_owned_hash
    else:
        assert re.fullmatch(r"[0-9a-f]{64}", expected_owned_hash)
    mutable_projections = {
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
    }
    for relative, tagged in receipt["source_inputs"].items():
        expected = (
            git_file_sha256(BASE_REVISION, relative)
            if relative in mutable_projections
            else sha256(ROOT / relative)
        )
        assert tagged == f"sha256:{expected}", f"stale receipt input: {relative}"

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )
    for name in (
        "README.md",
        "instance.json",
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)
    checks = [line for line in probe.splitlines() if line.startswith("#check ")]
    assert len(checks) == 16
    assert "#check Language.IsContextFree" in checks
    assert "#check Turing.TM2.eval" in checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    check_authorities(instance, dag, receipt)
    check_instance(instance, receipt)
    check_artifacts(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0764 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
