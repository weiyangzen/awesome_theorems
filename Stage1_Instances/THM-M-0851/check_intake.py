#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0851."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0851"
ITEM_ID = "S56-M-0851-INTAKE"
RANK = 1406
BASE_REVISION = "1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4"
BASE_TREE = "61214aa2a03c032134ddc4958b1df63df3430a85"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "a476e104e4ac2229f842934e26a7f910de85b937a5f46993b984344de4fd8de5"
SUCCESS = "intake invariant check: ok (THM-M-0851 planned; H1/M4/R4; six open tasks)\n"
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
SOURCE_HASH_FIELDS = {
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
MATHLIB_HASH_FIELDS = {
    "mathlib_binomial_random_graph_source_sha256": (
        "Mathlib/Probability/Combinatorics/BinomialRandomGraph/Defs.lean"
    ),
    "mathlib_connected_source_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Connectivity/Connected.lean"
    ),
}
PROBE_DECLARATIONS = [
    "SimpleGraph.binomialRandom",
    "SimpleGraph.binomialRandom_zero",
    "SimpleGraph.binomialRandom_one",
    "SimpleGraph.Preconnected",
    "SimpleGraph.Connected",
    "SimpleGraph.connected_bot_iff",
    "SimpleGraph.connected_top_iff",
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def excerpt_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def canonical_sha256(value: object) -> str:
    data = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(data).hexdigest()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    check_text_file(path.resolve())
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
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def check_receipt_inputs(receipt: dict, instance: dict) -> None:
    expected_sources = {
        relative: f"sha256:{instance['source_revisions'][field]}"
        for field, relative in SOURCE_HASH_FIELDS.items()
    }
    assert receipt["source_inputs"] == expected_sources
    worker = receipt["worker_input_hashes"]
    revisions = instance["source_revisions"]
    assert worker["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker["mathlib_revision"] == revisions["mathlib"]
    assert worker["mathlib_tree"] == revisions["mathlib_tree"]
    for field in MATHLIB_HASH_FIELDS:
        assert worker[field] == revisions[field]
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink(), "automation-provided .lake symlink is unavailable"
    symlink_hash = hashlib.sha256(str(lake.readlink()).encode()).hexdigest()
    assert worker["lake_symlink_target_string"] == f"sha256:{symlink_hash}"
    assert receipt["nonrelease_dirty_input_manifest"]["preexisting_untracked"] == {
        "Formalizations/Lean/.lake": f"symlink-target-string-sha256:{symlink_hash}"
    }


def check_recipe(recipe: dict) -> None:
    assert set(recipe) == {
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
    assert isinstance(recipe["cwd"], str) and recipe["cwd"]
    assert isinstance(recipe["argv"], list) and recipe["argv"]
    assert isinstance(recipe["env_allowlist"], dict)
    assert isinstance(recipe["timeout_seconds"], int) and recipe["timeout_seconds"] > 0
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert isinstance(recipe["expected_outputs"], list) and recipe["expected_outputs"]
    assert all(
        set(output) == {"path_or_stream", "semantic_hash_policy"}
        for output in recipe["expected_outputs"]
    )
    assert recipe["covered_task_ids"] == [ITEM_ID]
    assert recipe["covered_obligation_ids"] == []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    check_receipt_inputs(receipt, instance)

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(targets) == 1 and len(items) == 7
    target = targets[0]
    assert target["execution_rank"] == instance["execution_rank"] == receipt["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "连通性阈值"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    intake_item = next(row for row in items if row["id"] == ITEM_ID)
    assert intake_item["phase"] == "intake" and intake_item["layer"] == 0
    assert intake_item["state"] in {"[ ]", "[_]"} and intake_item["depends_on"] == []
    if args.worker_packet is not None:
        assert intake_item["state"] == "[ ]", "worker base must precede provisional integration"
        assert git("rev-parse", "HEAD") == BASE_REVISION
    else:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert intake_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert intake_item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "not_one_stable_truth_valued_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    assert git("rev-parse", f"{BASE_REVISION}:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", f"{BASE_REVISION}:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6243, 6248)
    assert revisions["duplicate_record_excerpt_sha256"] == excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 8164, 8169)
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 23225, 23250)
    assert revisions["manifest_entry_canonical_sha256"] == canonical_sha256(target)
    if args.worker_packet is not None:
        assert revisions["execution_dag_target_entries_canonical_sha256"] == canonical_sha256(items)
        assert revisions["manifest_entry_sha256"] == excerpt_sha256(ROOT / "Docs/Stage1_Targets_rev-5.6.json", 21100, 21114)
        assert revisions["execution_dag_target_entries_sha256"] == excerpt_sha256(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json", 174232, 174354)
        for field, relative in SOURCE_HASH_FIELDS.items():
            assert revisions[field] == sha256(ROOT / relative), f"stale worker input: {field}"
    else:
        base_execution = json.loads(
            subprocess.check_output(
                ["git", "show", f"{BASE_REVISION}:Docs/Stage1_Execution_DAG_rev-5.6.json"],
                cwd=ROOT,
            )
        )
        base_items = [
            row for row in base_execution["items"] if row["theorem_id"] == THEOREM_ID
        ]
        assert revisions["execution_dag_target_entries_canonical_sha256"] == canonical_sha256(base_items)
        for field, relative in SOURCE_HASH_FIELDS.items():
            if field not in {"authoritative_blueprint_sha256", "execution_dag_sha256"}:
                assert revisions[field] == sha256(ROOT / relative), f"stale stable input: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib input: {field}"

    target_by_id = {row["theorem_id"]: row for row in manifest["targets"]}
    neighbor_ids = [row["theorem_id"] for row in instance["neighbor_target_boundaries"]]
    assert len(neighbor_ids) == len(set(neighbor_ids))
    for neighbor in instance["neighbor_target_boundaries"]:
        assert target_by_id[neighbor["theorem_id"]]["name"] == neighbor["name"]

    authoritative = {row["id"]: row for row in items}
    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0851-{suffix}"
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        auth = authoritative[task_id]
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == auth["phase"] and task["layer"] == auth["layer"] == layer
        assert task["owned_paths"] == auth["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == auth["deliverable"]
        assert task["completion_gate"] == auth["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**连通性阈值**") == 2
    assert catalog.count("- 陈述: 随机图连通的阈值") == 2
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0851 连通性阈值" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    for marker in ("On Random Graphs I", "Theorem 1", "Theorem 4", "H1", "binomialRandom"):
        assert marker in crosswalk

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected_hash in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected_hash == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected_hash, f"stale owned hash: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["deliverable"] == intake_item["deliverable"]
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["known_failures"] and receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"].startswith("S56-M-0851-STATEMENT")
    assert receipt["invalidation_inputs"] and receipt["support_state"] == "provisional_worker_selftest_only"
    assert receipt["validation_started_at"] is None
    assert receipt["validated_at"] == receipt["validation_ended_at"]
    if args.worker_packet is None:
        assert receipt["validated_at"] != "PENDING_FINAL_REPLAY"
    assert len(receipt["structured_validation_recipes"]) == 2
    for recipe in receipt["structured_validation_recipes"]:
        check_recipe(recipe)
    structure_recipe, probe_recipe = receipt["structured_validation_recipes"]
    assert structure_recipe["recipe_id"].endswith("STRUCTURE")
    assert structure_recipe["cwd"] == "."
    assert structure_recipe["argv"] == ["python3", "-B", "Stage1_Instances/THM-M-0851/check_intake.py"]
    assert structure_recipe["covered_declarations"] == []
    assert probe_recipe["recipe_id"].endswith("LEAN-PROBE")
    assert probe_recipe["cwd"] == "Formalizations/Lean"
    assert probe_recipe["argv"] == ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0851/IntakeProbe.lean"]
    assert probe_recipe["covered_declarations"] == PROBE_DECLARATIONS

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for name in ("README.md", "instance.json", "intake-receipt.json", "scope-map.md", "source-statement-crosswalk.md", "task-dag.json", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe
    assert "#print axioms SimpleGraph.connected_bot_iff" in probe
    assert "#print axioms SimpleGraph.connected_top_iff" in probe
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    lean_run = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0851/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        env={"PATH": __import__("os").environ["PATH"], "HOME": __import__("os").environ.get("HOME", ""), "LC_ALL": "C.UTF-8", "TZ": "UTC"},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert lean_run.returncode == 0, lean_run.stdout
    assert hashlib.sha256(lean_run.stdout.encode()).hexdigest() == PROBE_OUTPUT_SHA256
    assert lean_run.stdout.count("[propext, Classical.choice, Quot.sound]") == 2

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print(SUCCESS, end="")


if __name__ == "__main__":
    main()
