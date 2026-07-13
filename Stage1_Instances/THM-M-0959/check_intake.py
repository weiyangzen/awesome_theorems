#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0959."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0959"
ITEM_ID = "S56-M-0959-INTAKE"
RANK = 1493
BASE_REVISION = "a3b18eec39bf04be025b1641cae02f4d44fdf11a"
BASE_TREE = "fdfff18dea4c6798c5b322b6088dfe556109c134"
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
SOURCE_HASH_FIELDS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "applicable_targets_sha256": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_HASH_FIELDS = {
    "mathlib_three_ap_defs_sha256": "Mathlib/Combinatorics/Additive/AP/Three/Defs.lean",
    "mathlib_behrend_sha256": "Mathlib/Combinatorics/Additive/AP/Three/Behrend.lean",
    "mathlib_zmod_basic_sha256": "Mathlib/Data/ZMod/Basic.lean",
    "mathlib_binary_entropy_sha256": "Mathlib/Analysis/SpecialFunctions/BinaryEntropy.lean",
    "mathlib_fintype_bigoperators_sha256": "Mathlib/Data/Fintype/BigOperators.lean",
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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def path_bytes_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def run_recipe(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {"LC_ALL": "C", "TZ": "UTC"}
    assert recipe["network_policy"] == "denied"
    env = {**dict(__import__("os").environ), **recipe["env_allowlist"]}
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"]
    return result.stdout


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
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
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Croot-Lev-Pach方法",
        "category": "组合数学 / 计数组合",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    for key in (
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
        assert instance[key] == target[key]
    assert instance["name_zh"] == target["name"]

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
    assert instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "method_and_cap_set_application_not_one_truth_valued_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["root_vector_status"] == "proposed_pending_master_acceptance"
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 7001, 7006) == revisions["repository_record_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 26146, 26171) == revisions["stage0_projection_excerpt_sha256"]
    assert canonical_json_sha256(target) == revisions["manifest_entry_sha256"]
    assert canonical_json_sha256(item) == revisions["intake_dag_entry_sha256"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == "", "pinned mathlib source is dirty"
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    authoritative_tasks = {
        row["id"]: row for row in execution["items"] if row["theorem_id"] == THEOREM_ID
    }
    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0959-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        authoritative = authoritative_tasks[task_id]
        for field in (
            "theorem_id", "execution_rank", "phase", "layer", "owned_paths",
            "deliverable", "completion_gate", "attempts", "children",
        ):
            assert task[field] == authoritative[field]
        assert task["layer"] == layer and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Croot-Lev-Pach方法**") == 1
    assert catalog.count("- 提出者: Croot/Lev/Pach") == 1
    assert catalog.count("- 陈述: 多项式方法在cap集问题中的应用") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0959 Croot-Lev-Pach方法" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0957", "THM-M-0958", "THM-M-0960", "THM-M-0961"}
    manifest_names = {row["theorem_id"]: row["name"] for row in manifest["targets"] if row["theorem_id"] in neighbor_ids}
    assert manifest_names == {row["theorem_id"]: row["name"] for row in instance["neighbor_target_boundaries"]}
    primary = instance["primary_source_candidates_not_credited"][0]
    assert primary["publisher_pdf_sha256"] == revisions["primary_source_pdf_sha256"]
    assert primary["preprint"].startswith("arXiv:1605.01506v2")
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    assert "(H(1/2-epsilon)+H(2*epsilon))/2" in crosswalk
    assert "outer factor `1/2`" in crosswalk

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["selftest_result"] == "pass"
    for field in (
        "reviewer_policy", "review_due", "support_window", "support_state",
        "supersession_state", "revocation_state", "incident_path",
        "archive_and_recovery_boundary",
    ):
        assert receipt[field]
    for field in ("validation_started_at", "validation_ended_at", "validated_at"):
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", receipt[field])

    for relative, tagged in receipt["source_inputs"].items():
        assert tagged == f"sha256:{sha256(ROOT / relative)}"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    assert worker_inputs["lean_toolchain"] == f'sha256:{revisions["lean_toolchain_file_sha256"]}'
    assert worker_inputs["lake_manifest"] == f'sha256:{revisions["lake_manifest_sha256"]}'

    dirty = receipt["dirty_input_evidence"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    nonrecursive_owned = [HERE / name for name in OWNED_FILES if name != "intake-receipt.json"]
    assert dirty["owned_untracked_patch_sha256"] == path_bytes_hash(nonrecursive_owned)
    assert dirty["owned_untracked_manifest_sha256"] == path_manifest_hash(nonrecursive_owned)

    recipes = {recipe["recipe_id"]: recipe for recipe in receipt["structured_validation_recipes"]}
    assert set(recipes) == {
        "S56-M-0959-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0959-INTAKE-RECIPE-LEAN-PROBE",
    }
    actions = {action["action_id"]: action for action in receipt["validation_actions"]}
    assert set(actions) == {
        "S56-M-0959-INTAKE-ACTION-STRUCTURE",
        "S56-M-0959-INTAKE-ACTION-LEAN-PROBE",
    }
    for action in actions.values():
        recipe = recipes[action["recipe_id"]]
        identity = {key: recipe[key] for key in (
            "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy", "expected_exit",
        )}
        assert action["recipe_sha256"] == canonical_json_sha256(identity)
        assert action["exit_code"] == 0 and action["covered_obligation_ids"] == []
        assert action["covered_node_ids"] == [ITEM_ID]
    structure_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
        HERE / "check_intake.py",
    ]
    assert actions["S56-M-0959-INTAKE-ACTION-STRUCTURE"]["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        HERE / "IntakeProbe.lean",
    ]
    lean_action = actions["S56-M-0959-INTAKE-ACTION-LEAN-PROBE"]
    assert lean_action["input_manifest_sha256"] == path_manifest_hash(lean_inputs)
    lean_stdout = run_recipe(recipes[lean_action["recipe_id"]])
    assert lean_action["stdout_sha256"] == lean_action["log_sha256"] == hashlib.sha256(lean_stdout).hexdigest()
    structure_stdout = b"intake invariant check: ok (THM-M-0959 planned; H5/M4/R4; six open tasks)\n"
    structure_action = actions["S56-M-0959-INTAKE-ACTION-STRUCTURE"]
    assert structure_action["stdout_sha256"] == structure_action["log_sha256"] == hashlib.sha256(structure_stdout).hexdigest()

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/") and (ROOT / relative).is_file()
    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet)
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md", "instance.json", "intake-receipt.json", "scope-map.md",
        "source-statement-crosswalk.md", "task-dag.json", "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text and "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0959 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
