#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0968."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0968"
ITEM_ID = "S56-M-0968-INTAKE"
RANK = 1502
BASE_REVISION = "fcabbf1e0ad9507eebe91663bccabfa87d22813e"
BASE_TREE = "873e589c594454b7f263c7ed2342089a4d15e842"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PRIMARY_SOURCE_SHA256 = "56e7147c8e58e48212120d5986d4285ef2fc8b9a3b7ee0c9cf897350e79509bf"
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
TASK_SUFFIXES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
]
SOURCE_HASHES = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_SOURCE_HASHES = {
    "mathlib_slice_source_sha256": "Mathlib/Data/Finset/Slice.lean",
    "mathlib_pairwise_source_sha256": "Mathlib/Data/Finset/Pairwise.lean",
    "mathlib_powerset_source_sha256": "Mathlib/Data/Finset/Powerset.lean",
    "mathlib_finset_card_source_sha256": "Mathlib/Data/Finset/Card.lean",
}
RECEIPT_KEYS = {
    "schema_version",
    "receipt_id",
    "receipt_class",
    "content_addressed",
    "content_addressing_boundary",
    "item_id",
    "theorem_id",
    "phase",
    "intent",
    "verdict",
    "proposed_state",
    "accepted",
    "acceptance_authority",
    "lifecycle_before",
    "lifecycle_after",
    "base_revision",
    "base_tree",
    "worker_branch_or_worktree",
    "worktree_state",
    "preexisting_untracked_paths",
    "attestor",
    "platform",
    "owner",
    "reviewer_policy",
    "support_window",
    "revocation_state",
    "archive_and_recovery_boundary",
    "source_inputs",
    "source_evidence",
    "worker_input_hashes",
    "dirty_input_evidence",
    "validated_scope",
    "changed_paths",
    "owned_artifact_sha256",
    "diff_summary",
    "exact_statement_change",
    "source_revision_and_proof_body_summary",
    "ownership_and_change_impact",
    "structured_validation_recipes",
    "validation_actions",
    "commands_and_results",
    "root_vector_before",
    "root_vector_after",
    "debt_delta_basis",
    "axiom_and_placeholder_result",
    "actual_source_ownership",
    "declaration_ownership",
    "readable_ownership",
    "change_impact_set",
    "covered_node_ids",
    "covered_declaration_ids",
    "proof_body_locations",
    "canonical_obligation_ids",
    "statement_fingerprints",
    "typed_graph_changes",
    "composition_certificates",
    "content_addressed_recipe_ids",
    "content_addressed_receipt_ids",
    "accepted_receipt_ids",
    "validation_started_at",
    "validation_ended_at",
    "validated_at",
    "review_due",
    "invalidation_inputs",
    "support_state",
    "supersession_state",
    "incident_path",
    "audit_complete",
    "theorem_complete",
    "first_failed_gate",
    "first_failed_theorem_gate",
    "retry_condition",
    "remaining_root_cut_set",
    "known_failures",
    "selftest_result",
    "status_boundary",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: object) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix().encode()
        data = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def check_receipt_inputs(receipt: dict) -> None:
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", (
            f"stale receipt input hash: {relative}"
        )


def check_worker_packet(path: Path, receipt: dict) -> None:
    resolved = path.resolve()
    packet = load(resolved)
    data = resolved.read_bytes()
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
    assert all(isinstance(command, str) and command for command in packet["commands"])
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    assert set(receipt) == RECEIPT_KEYS
    check_receipt_inputs(receipt)

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "Erdős盒原理"
    assert target["category"] == instance["category"] == "组合数学 / 计数组合"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["attempts"] == 0 and item["children"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "does_not_select" in instance["canonical_claim_status"]
    blocker = instance["statement_blocker"].lower()
    assert "box-principle" in blocker and "large-n" in blocker and "equation (9)" in blocker

    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert revisions["primary_source_pdf_sha256"] == PRIMARY_SOURCE_SHA256
    assert revisions["current_repository_math_source_blob"] == git(
        "rev-parse", "HEAD:Docs/researches/math_theorems.md"
    )
    assert revisions["current_stage0_blueprint_blob"] == git(
        "rev-parse", "HEAD:Docs/Stage0_Blueprint.md"
    )
    catalog_excerpt = b"".join(
        (ROOT / "Docs/researches/math_theorems.md").read_bytes().splitlines(keepends=True)[7070:7076]
    )
    stage0_excerpt = b"".join(
        (ROOT / "Docs/Stage0_Blueprint.md").read_bytes().splitlines(keepends=True)[26388:26414]
    )
    assert hashlib.sha256(catalog_excerpt).hexdigest() == revisions["repository_record_excerpt_sha256"]
    assert hashlib.sha256(stage0_excerpt).hexdigest() == revisions["stage0_projection_excerpt_sha256"]
    target_stream = json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n"
    execution_rows = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    execution_stream = "".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
        for row in execution_rows
    )
    assert hashlib.sha256(target_stream.encode()).hexdigest() == revisions["target_manifest_entry_sha256"]
    assert hashlib.sha256(execution_stream.encode()).hexdigest() == revisions["target_execution_items_sha256"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib source is dirty"
    for field, relative in MATHLIB_SOURCE_HASHES.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib source hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0968-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        assert authoritative["state"] == "[ ]"
        assert authoritative["attempts"] == 0 and authoritative["children"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert "equation (9)" in dag["tasks"][0]["first_blocker"]

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Erdős盒原理**") == 1
    assert "- 提出者: Paul Erdős" in catalog
    assert "- 时间: 1965" in catalog
    assert catalog.count("- 陈述: 超图中的匹配") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0968 Erdős盒原理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert "- 现有 machine-checked 状态: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0822", "THM-M-0914", "THM-M-0964", "THM-M-0965", "THM-M-0966", "THM-M-0967", "THM-M-0969"}
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {
        "THM-M-0822": "Erdős-Ko-Rado定理",
        "THM-M-0914": "鸽巢原理",
        "THM-M-0964": "Hilton-Milner定理",
        "THM-M-0965": "Ahlswede-Khachatrian完全相交定理",
        "THM-M-0966": "Kruskal-Katona定理",
        "THM-M-0967": "Lovász-Kneser定理",
        "THM-M-0969": "Lovász局部引理",
    }

    source_candidates = instance["primary_source_candidates_not_credited_as_H0"]
    assert len(source_candidates) == 1
    source = source_candidates[0]
    assert source["observed_pdf_sha256"] == PRIMARY_SOURCE_SHA256
    assert source["observed_pdf_bytes"] == 413744 and source["observed_pdf_pages"] == 4
    assert "n > c_r k" in source["proved_candidate"]
    assert "equation (9)" in source["conjectural_candidate"]
    assert "1 + g(n-1, r, k-2)" in source["correction_boundary"]

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
            continue
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "intake"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["lifecycle_before"] == "L0 / rework_required with no rev-5.6 instance"
    assert receipt["lifecycle_after"] == "planned"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at == validated_at <= datetime.now(timezone.utc).astimezone()
    for action in receipt["validation_actions"]:
        action_started = datetime.fromisoformat(action["started_at"])
        action_ended = datetime.fromisoformat(action["ended_at"])
        assert started_at <= action_started <= action_ended <= ended_at
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["content_addressed_receipt_ids"] == []
    assert receipt["first_failed_gate"] == (
        "rev-5.6 node-specific master acceptance remains pending after the worker self-test"
    )
    assert receipt["first_failed_theorem_gate"].startswith("canonical statement gate:")

    dirty = receipt["dirty_input_evidence"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert set(dirty["owned_untracked_paths"]) == expected_changed
    assert "excluded" in dirty["hash_boundary"]

    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    for field, relative in MATHLIB_SOURCE_HASHES.items():
        assert worker_inputs[field] == revisions[field] == sha256(mathlib / relative)

    required_recipe_keys = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_task_ids",
        "covered_obligation_ids",
        "covered_declarations",
    }
    recipes = receipt["structured_validation_recipes"]
    assert [recipe["recipe_id"] for recipe in recipes] == [
        "S56-M-0968-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0968-INTAKE-RECIPE-LEAN-PROBE",
    ]
    for recipe in recipes:
        assert set(recipe) == required_recipe_keys
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {"LC_ALL": "C", "TZ": "UTC"}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []

    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    actions = receipt["validation_actions"]
    assert len(actions) == 2
    assert {action["recipe_id"] for action in actions} == set(recipes_by_id)
    assert {action["action_id"] for action in actions} == {
        "S56-M-0968-INTAKE-ACTION-STRUCTURE",
        "S56-M-0968-INTAKE-ACTION-LEAN-PROBE",
    }
    for action in actions:
        assert set(action) == {
            "action_id",
            "recipe_id",
            "recipe_sha256",
            "input_manifest_sha256",
            "stdout_sha256",
            "log_sha256",
            "started_at",
            "ended_at",
            "exit_code",
            "covered_task_ids",
            "covered_obligation_ids",
            "covered_declarations",
        }
        assert action["exit_code"] == 0
        recipe = recipes_by_id[action["recipe_id"]]
        assert action["covered_task_ids"] == recipe["covered_task_ids"] == [ITEM_ID]
        assert action["covered_obligation_ids"] == recipe["covered_obligation_ids"] == []
        assert action["covered_declarations"] == recipe["covered_declarations"]
        identity = {
            "cwd": recipe["cwd"],
            "argv": recipe["argv"],
            "env_allowlist": recipe["env_allowlist"],
            "timeout_seconds": recipe["timeout_seconds"],
            "network_policy": recipe["network_policy"],
            "expected_exit": recipe["expected_exit"],
        }
        assert action["recipe_sha256"] == canonical_json_sha256(identity)
        for field in ("recipe_sha256", "input_manifest_sha256", "stdout_sha256", "log_sha256"):
            assert re.fullmatch(r"[0-9a-f]{64}", action[field])

    structure_action = next(action for action in actions if action["recipe_id"].endswith("RECIPE-STRUCTURE"))
    structure_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
        HERE / "check_intake.py",
    ]
    assert structure_action["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    structure_hash = hashlib.sha256(
        b"intake invariant check: ok (THM-M-0968 planned; H5/M4/R4; six open tasks)\n"
    ).hexdigest()
    assert structure_action["stdout_sha256"] == structure_action["log_sha256"] == structure_hash

    lean_action = next(action for action in actions if action["recipe_id"].endswith("RECIPE-LEAN-PROBE"))
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        HERE / "IntakeProbe.lean",
    ]
    assert lean_action["input_manifest_sha256"] == path_manifest_hash(lean_inputs)
    assert lean_action["stdout_sha256"] == lean_action["log_sha256"] == "1211f2485935c978b086759c1537c5c45c506112ba6fc2590d9c2a404c627f1e"
    assert lean_action["covered_declarations"] == [
        "Set.Sized",
        "Set.Sized.card_le",
        "Finset.powersetCard",
        "Finset.mem_powersetCard",
        "Set.PairwiseDisjoint",
        "Disjoint",
        "Finset.card",
    ]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

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
    prohibited = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b")
    assert prohibited.search(probe) is None

    changed_lines = git("status", "--short", "--untracked-files=all").splitlines()
    actual_changed = {line[3:] for line in changed_lines if line[3:] != "Formalizations/Lean/.lake"}
    assert actual_changed == expected_changed, f"unexpected worker delta: {sorted(actual_changed ^ expected_changed)}"

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0968 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
