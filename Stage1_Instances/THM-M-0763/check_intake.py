#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0763."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0763"
ITEM_ID = "S56-M-0763-INTAKE"
RANK = 1349
BASE_REVISION = "fd0fab2ab7f4f514a5cc625bbce92879e718ba13"
BASE_TREE = "4116d53bcf2573069e4b67205353fe3469dbe7bd"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H5", "M": "M4", "R": "R4"}
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
SOURCE_HASHES = {
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
    "mathlib_language_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Language.lean"
    ),
    "mathlib_dfa_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/DFA.lean"
    ),
    "mathlib_context_free_grammar_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/ContextFreeGrammar.lean"
    ),
    "mathlib_halting_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean"
    ),
}
PROBE_DECLARATIONS = [
    "Language",
    "Language.IsRegular",
    "ContextFreeRule",
    "ContextFreeGrammar",
    "ContextFreeGrammar.language",
    "ContextFreeGrammar.mem_language_iff",
    "Language.IsContextFree",
    "ComputablePred",
    "REPred",
]


def load_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def canonical_hash(value: dict) -> str:
    encoded = (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path.resolve())
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()


def check_authorities(instance: dict, execution_items: list[dict]) -> None:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    assert manifest["scope"]["covered_targets"] == 1546
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "乔姆斯基层次",
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
    assert canonical_hash(target) == instance["source_revisions"][
        "target_manifest_entry_canonical_sha256"
    ]
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "category",
        "source_status_untrusted",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "lifecycle_mode",
        "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]

    intake = next(row for row in execution_items if row["id"] == ITEM_ID)
    assert canonical_hash(intake) == instance["source_revisions"][
        "execution_dag_intake_entry_canonical_sha256"
    ]
    assert intake["theorem_id"] == THEOREM_ID and intake["execution_rank"] == RANK
    assert intake["phase"] == "intake" and intake["layer"] == 0
    assert intake["state"] == "[ ]" and intake["depends_on"] == []
    assert intake["attempts"] == 0 and intake["children"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "does_not_supply_one_stable_truth_valued_proposition" in instance[
        "canonical_claim_status"
    ]
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "candidate_expression",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert "blocked" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["source_status"].startswith("H5_")
    assert "No canonical proposition" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
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
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/cs_theorems.md") == revisions[
        "repository_cs_record_blob"
    ]
    excerpt_fields = {
        "repository_record_excerpt_sha256": (
            "Docs/researches/math_theorems.md",
            5619,
            5624,
        ),
        "repository_cs_record_excerpt_sha256": ("Docs/researches/cs_theorems.md", 260, 260),
        "stage0_projection_excerpt_sha256": ("Docs/Stage0_Blueprint.md", 20839, 20864),
        "stage0_cs_boundary_excerpt_sha256": ("Docs/Stage0_Blueprint.md", 85653, 85678),
    }
    for field, (relative, first, last) in excerpt_fields.items():
        assert revisions[field] == excerpt_sha256(ROOT / relative, first, last)
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/researches/cs_theorems.md") == revisions[
        "current_repository_cs_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blob"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions[
        "mathlib_tree"
    ] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""


def check_scope(instance: dict) -> None:
    math_catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert math_catalog.count("**乔姆斯基层次**") == 1
    assert math_catalog.count("- 陈述: 形式语言的分类") == 1
    assert "- 提出者: Noam Chomsky" in math_catalog
    cs_catalog = (ROOT / "Docs/researches/cs_theorems.md").read_text(encoding="utf-8")
    assert "| 4.3.1 | **Chomsky层级**" in cs_catalog
    assert "形式语言的四层层级" in cs_catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert stage0.count("THM-M-0763 乔姆斯基层次") == 1
    assert stage0.count("THM-C-0151 Chomsky层级") == 1
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert "- 现有 machine-checked 状态: 待补充" in stage0

    blocker = instance["statement_blocker"].lower()
    for token in (
        "1956 three-class",
        "modern four grammar types",
        "weak inclusions",
        "strict inclusions",
        "grammar-machine equivalences",
        "ordered binders",
        "degenerate cases",
    ):
        assert token in blocker, f"missing statement ambiguity: {token}"
    candidates = " ".join(instance["candidate_scope_not_credited"]).lower()
    for token in ("unrestricted", "weak inclusion", "strictness", "automata", "theorem (27)"):
        assert token in candidates, f"missing candidate boundary: {token}"
    exclusions = " ".join(instance["excluded_substitutions"])
    for token in ("THM-M-0764", "THM-M-0765", "THM-C-0151", "已验证"):
        assert token in exclusions, f"missing non-substitution boundary: {token}"
    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {
        "THM-M-0759",
        "THM-M-0760",
        "THM-M-0761",
        "THM-M-0762",
        "THM-M-0764",
        "THM-M-0765",
        "THM-M-0766",
        "THM-C-0151",
    }
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {
        "THM-M-0759": "自动机理论",
        "THM-M-0760": "Myhill-Nerode定理",
        "THM-M-0761": "泵引理",
        "THM-M-0762": "上下文无关语言的性质",
        "THM-M-0764": "下推自动机",
        "THM-M-0765": "图灵机可识别语言",
        "THM-M-0766": "线性有界自动机",
    }
    boundary = next(
        row for row in instance["neighbor_target_boundaries"] if row["theorem_id"] == "THM-C-0151"
    )
    assert boundary["name"] == "Chomsky层级"
    source_leads = instance["primary_source_candidates_not_credited"]
    assert [row["doi"] for row in source_leads] == [
        "10.1109/TIT.1956.1056813",
        "10.1016/S0019-9958(59)90362-6",
    ]
    assert source_leads[0]["temporary_pdf_sha256"] == (
        "a3bfc97156feead2609ee9f0384eef4138f22b97776505d4bc852d882a5e1799"
    )
    assert source_leads[0]["temporary_pdf_bytes"] == 1532335
    assert "not the modern four-type hierarchy" in source_leads[0]["candidate_summary"]


def check_dag(dag: dict, execution_items: list[dict]) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert dag["accepted_states"] == []
    tasks = dag["tasks"]
    assert [task["id"] for task in tasks] == [
        f"S56-M-0763-{suffix}" for suffix in TASK_SUFFIXES
    ]
    for index, task in enumerate(tasks, start=1):
        predecessor = ITEM_ID if index == 1 else tasks[index - 2]["id"]
        assert task["layer"] == index and task["depends_on"] == [predecessor]
        assert task["state"] == "open" and task["evidence_ids"] == []
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        authority = next(row for row in execution_items if row["id"] == task["id"])
        for field in (
            "phase",
            "layer",
            "depends_on",
            "owned_paths",
            "deliverable",
            "completion_gate",
        ):
            assert task[field] == authority[field]
    assert "1956 three-class" in tasks[0]["first_blocker"]
    assert "modern four-level" in tasks[0]["first_blocker"]


def check_receipt(receipt: dict, instance: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"] == (
        "master acceptance of the provisional self-tested intake receipt"
    )
    assert "exact source-statement identity" in receipt["first_failed_theorem_gate"]
    assert receipt["covered_node_ids"] == receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert receipt["declaration_ownership"] == []

    assert receipt["source_inputs"] == {
        relative: f"sha256:{sha256(ROOT / relative)}"
        for relative in (
            "Docs/Stage1_Targets_rev-5.6.json",
            "Docs/Stage1_Blueprint_rev-5.6.md",
            "Docs/Stage1_Execution_DAG_rev-5.6.json",
            "skills/execute-stage1-rev56/SKILL.md",
            "Docs/Blueprint_Guidelines.md",
            "Docs/researches/math_theorems.md",
            "Docs/researches/cs_theorems.md",
            "Docs/Stage0_Blueprint.md",
            "Formalizations/Lean/lean-toolchain",
            "Formalizations/Lean/lake-manifest.json",
        )
    }
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    link_hash = hashlib.sha256(str(lake.readlink()).encode()).hexdigest()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{link_hash}"

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert receipt["dirty_input_evidence"]["preflight_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    assert receipt["dirty_input_evidence"]["owned_untracked_paths"] == expected_changed
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 4
    for recipe in recipes:
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
    assert recipes[2]["covered_declarations"] == PROBE_DECLARATIONS

    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.fromisoformat(receipt["validated_at"])
    assert started <= ended == validated
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()


def check_files(instance: dict) -> None:
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    execution_items = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]

    check_authorities(instance, execution_items)
    check_instance(instance)
    check_scope(instance)
    check_dag(dag, execution_items)
    check_receipt(receipt, instance, dag)
    check_files(instance)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0763 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
