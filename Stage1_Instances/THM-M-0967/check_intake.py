#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0967 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0967"
ITEM_ID = "S56-M-0967-INTAKE"
RANK = 1501
BASE_REVISION = "fcabbf1e0ad9507eebe91663bccabfa87d22813e"
BASE_TREE = "873e589c594454b7f263c7ed2342089a4d15e842"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
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
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_SOURCE_HASH_FIELDS = {
    "mathlib_coloring_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Coloring.lean",
    "mathlib_powerset_source_sha256": "Mathlib/Data/Finset/Powerset.lean",
    "mathlib_fintype_powerset_source_sha256": "Mathlib/Data/Fintype/Powerset.lean",
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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1:last]).encode()).hexdigest()


def canonical_target_hash(target: dict) -> str:
    payload = json.dumps(
        target, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def canonical_recipe_hash(recipe: dict) -> str:
    payload = json.dumps(recipe, sort_keys=True, separators=(",", ":")).encode() + b"\n"
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


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
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["output_summary"]
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

    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [{
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Lovász-Kneser定理",
        "category": "组合数学 / 计数组合",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }]
    target = matches[0]
    assert instance["execution_rank"] == RANK
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]
    for field in (
        "legacy_priority_slot",
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
    assert canonical_target_hash(target) == instance["source_revisions"]["target_manifest_entry_canonical_sha256"]

    authoritative_items = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(authoritative_items) == 7
    intake = authoritative_items[0]
    assert intake == {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": RANK,
        "phase": "intake",
        "layer": 0,
        "state": "[ ]",
        "depends_on": [],
        "owned_paths": [f"Stage1_Instances/{THEOREM_ID}"],
        "deliverable": "Create the theorem dossier, scope map, and source-statement crosswalk.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == receipt["phase"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert formal["probe_declaration"] == "Stage1Instances.THM_M_0967.Intake.CandidateKneserGraph"
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    assert git(
        "rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md'
    ) == revisions["repository_source_record_blob"]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 7064, 7069) == revisions["repository_record_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 26362, 26387) == revisions["stage0_projection_excerpt_sha256"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib worktree is dirty"
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0967-{suffix}"
        task = dag["tasks"][layer - 1]
        authority = authoritative_items[layer]
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["evidence_ids"] == []
        assert task["layer"] == authority["layer"] == layer
        for field in ("id", "phase", "owned_paths", "deliverable", "completion_gate", "depends_on"):
            assert task[field] == authority[field]
        assert authority["state"] == "[ ]"
        dependency = task_id

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    for phrase in (
        "**Lovász-Kneser定理**",
        "- 提出者: László Lovász",
        "- 时间: 1978",
        "- 陈述: Kneser图的色数",
    ):
        assert phrase in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0967 Lovász-Kneser定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    for needle in (
        "10.1016/0097-3165(78)90022-5",
        "article body was not inspected",
        "provisional `H1`, not `H0`",
        "Kneser's conjecture",
    ):
        assert needle in crosswalk

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    expected_hashed = set(expected_changed) - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
    }
    assert set(receipt["owned_artifact_sha256"]) == expected_hashed
    for relative, expected in receipt["owned_artifact_sha256"].items():
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is receipt["signed"] is False
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["root_vector_before"] == {"H": "unclassified", "M": "unclassified", "R": "unclassified"}
    for key in (
        "accepted_receipt_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["dirty_input_evidence"]["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]

    required_recipe_keys = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "covered_declarations",
        "exit_code",
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == recipe["exit_code"] == 0 for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    for recipe in recipes:
        assert receipt["provisional_recipe_sha256"][recipe["recipe_id"]] == canonical_recipe_hash(recipe)

    lean_output = subprocess.check_output(
        ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        stderr=subprocess.STDOUT,
    )
    lean_hash = hashlib.sha256(lean_output).hexdigest()
    assert lean_hash == receipt["lean_probe_stdout_sha256"]
    recipe_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    assert recipe_by_id[f"{ITEM_ID}-RECIPE-LEAN-PROBE"]["expected_outputs"][0]["sha256"] == lean_hash
    expected_structure = b"intake invariant check: ok (THM-M-0967 planned; H1/M4/R4; six open tasks)\n"
    assert recipe_by_id[f"{ITEM_ID}-RECIPE-STRUCTURE"]["expected_outputs"][0]["sha256"] == hashlib.sha256(expected_structure).hexdigest()

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    code_lines = "\n".join(
        line for line in probe.splitlines() if not line.lstrip().startswith(("/", "*", "#"))
    )
    assert not re.search(r"\b(sorry|admit|axiom|constant|opaque|unsafe)\b", code_lines)
    assert "def CandidateKneserGraph" in probe
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
        checked_paths.append(args.worker_packet.resolve())
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path}"
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("intake invariant check: ok (THM-M-0967 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
