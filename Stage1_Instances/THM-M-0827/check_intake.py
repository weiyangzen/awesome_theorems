#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0827 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


if not __debug__:
    raise RuntimeError("intake validation requires Python assertions; do not use -O")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0827"
ITEM_ID = "S56-M-0827-INTAKE"
RANK = 1385
BASE_REVISION = "46a0f2a3ea74765a0467c489264b838ffbb70675"
BASE_TREE = "7b1b5269d7da840fd086da731d6f92903c209c35"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
OWNED_FILES = {
    "IntakeProbe.lean",
    "README.md",
    "check_intake.py",
    "instance.json",
    "intake-receipt.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "validation.md",
}
PACKET_KEYS = {
    "item_id",
    "changed_paths",
    "commands",
    "output_summary",
    "base_revision",
    "known_failures",
    "state",
}
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
EXCERPT_HASH_FIELDS = {
    "repository_record_excerpt_sha256": ("Docs/researches/math_theorems.md", 6075, 6080),
    "companion_cs_record_excerpt_sha256": ("Docs/researches/cs_theorems.md", 168, 168),
    "stage0_projection_excerpt_sha256": ("Docs/Stage0_Blueprint.md", 22577, 22602),
    "companion_cs_stage0_excerpt_sha256": ("Docs/Stage0_Blueprint.md", 83941, 83968),
    "neighbor_math_excerpt_sha256": ("Docs/researches/math_theorems.md", 6061, 6087),
}
MATHLIB_HASH_FIELDS = {
    "mathlib_digraph_basic_sha256": "Mathlib/Combinatorics/Digraph/Basic.lean",
    "mathlib_quiver_path_weight_sha256": "Mathlib/Combinatorics/Quiver/Path/Weight.lean",
    "mathlib_simplegraph_metric_sha256": "Mathlib/Combinatorics/SimpleGraph/Metric.lean",
}
PROBE_DECLARATIONS = [
    "Digraph",
    "Digraph.Adj",
    "Quiver.Path",
    "Quiver.Path.length",
    "Quiver.Path.addWeight",
    "Quiver.Path.addWeight_nil",
    "Quiver.Path.addWeight_cons",
    "Quiver.Path.addWeight_comp",
    "SimpleGraph.edist",
    "SimpleGraph.edist_eq_sInf",
    "SimpleGraph.Reachable.exists_walk_length_eq_edist",
    "SimpleGraph.edist_le",
    "SimpleGraph.dist",
    "SimpleGraph.dist_eq_sInf",
    "SimpleGraph.dist_le",
]


def load_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1:last])).hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def canonical_hashes(values: list[object]) -> str:
    payload = "".join(
        json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"
        for value in values
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_authorities(instance: dict) -> list[dict]:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    assert manifest["scope"]["covered_targets"] == 1546
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [{
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Floyd-Warshall算法",
        "category": "组合数学 / 图论",
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
    for field in (
        "execution_rank", "legacy_priority_slot", "baseline", "rework_required",
        "legacy_artifacts_accepted", "target_lane", "intake_score",
        "source_status_untrusted", "lifecycle_mode", "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]
    assert canonical_hash(target) == instance["source_revisions"][
        "manifest_entry_canonical_sha256"
    ]

    items = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    rows = [row for row in items if row["theorem_id"] == THEOREM_ID]
    assert len(rows) == 7
    assert canonical_hashes(rows) == instance["source_revisions"][
        "target_dag_rows_canonical_sha256"
    ]
    intake = next(row for row in rows if row["id"] == ITEM_ID)
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
    return rows


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "全源最短路径算法"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    for field in (
        "module", "declaration_or_expression", "candidate_expression",
        "elaborated_expression_hash", "environment_fingerprint",
    ):
        assert formal[field] is None
    assert formal["gate_state"].startswith("blocked_pending_source_root")
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "H1 records" in instance["status_boundary"]
    assert "No canonical mathematical or Lean proposition" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/researches/cs_theorems.md") == revisions[
        "current_repository_cs_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    for field, (relative, first, last) in EXCERPT_HASH_FIELDS.items():
        assert revisions[field] == excerpt_sha256(ROOT / relative, first, last), (
            f"stale excerpt hash: {field}"
        )

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions[
        "mathlib_tree"
    ] == MATHLIB_TREE
    assert git("status", "--short", "--untracked-files=all", cwd=mathlib) == ""
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"


def check_catalog_and_boundaries(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Floyd-Warshall算法**") == 1
    assert catalog.count("- 陈述: 全源最短路径算法") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0827 Floyd-Warshall算法" in stage0
    assert "THM-C-0093 Floyd-Warshall算法" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    cs = (ROOT / "Docs/researches/cs_theorems.md").read_text(encoding="utf-8")
    assert "全源最短路径O(n^3)算法" in cs
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0825", "THM-M-0826", "THM-C-0093"
    }
    citations = " ".join(row["citation"] for row in instance["source_candidates_not_credited"])
    assert "10.1145/367766.368168" in citations
    assert "10.1145/321105.321107" in citations


def check_task_dag(dag: dict, authoritative: list[dict]) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert len(dag["tasks"]) == 6
    dependency = ITEM_ID
    for layer, (task, suffix) in enumerate(zip(dag["tasks"], TASK_SUFFIXES), start=1):
        task_id = f"S56-M-0827-{suffix}"
        source = next(row for row in authoritative if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["layer"] == source["layer"] == layer
        assert task["phase"] == source["phase"]
        assert task["owned_paths"] == source["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert "not release evidence" in receipt["content_addressing_boundary"]
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["acceptance_authority"] == receipt["owner"] == "Stage1 integration lane"
    assert receipt["review_due"] and receipt["reviewer_policy"]
    assert receipt["invalidation_inputs"] and receipt["support_state"]
    assert receipt["supersession_state"] and receipt["revocation_state"]
    assert receipt["incident_path"] and receipt["archive_and_recovery_boundary"]
    outputs = receipt["action_output_hashes"]
    assert outputs["lean_probe_stdout_sha256"] == (
        "26c08241afe0333e857956272de2899489e98d7ee53a4ac92e706bb54e027feb"
    )
    assert outputs["lean_probe_stdout_bytes"] == 2078
    assert outputs["structural_validator_stdout_sha256"] == (
        "f76531b21d20e8f4808cdcd464ce42bcf295abfa9a6efcc3ae16ca9d053b8c25"
    )
    assert outputs["structural_validator_stdout_bytes"] == 74
    for key in (
        "accepted_receipt_ids", "proof_body_locations", "canonical_obligation_ids",
        "statement_fingerprints", "typed_graph_changes", "composition_certificates",
        "content_addressed_recipe_ids", "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["output_summary"]
    assert receipt["first_failed_gate"] == (
        "master acceptance of the provisional self-tested intake receipt"
    )
    assert "canonical statement identity" in receipt["first_failed_theorem_gate"]
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
    assert receipt["dirty_input_evidence"]["preflight_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    assert hashlib.sha256(str(lake.readlink()).encode()).hexdigest() == receipt[
        "worker_input_hashes"
    ]["lake_symlink_target_string_sha256"]
    assert receipt["source_inputs"] == {
        relative: f"sha256:{sha256(ROOT / relative)}"
        for relative in SOURCE_HASH_FIELDS.values()
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == recipe["exit_code"] == 0 for recipe in recipes)
    assert all(recipe["covered_ids"] == [ITEM_ID] for recipe in recipes)
    assert recipes[1]["covered_declarations"] == PROBE_DECLARATIONS


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path.resolve())
    assert set(packet) == PACKET_KEYS
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES, f"unexpected owned artifact inventory: {sorted(actual)}"
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    hashes = receipt["non_self_referential_owned_artifact_sha256"]
    expected_hashed = set(expected_changed) - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
    }
    assert set(hashes) == expected_hashed
    for relative, expected in hashes.items():
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
        whitespace = subprocess.run(
            ["git", "diff", "--no-index", "--check", "/dev/null", str(path)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        assert whitespace.returncode in (0, 1)
        assert not whitespace.stdout and not whitespace.stderr, (
            f"whitespace diagnostic: {path.name}"
        )
    for name in OWNED_FILES - {"IntakeProbe.lean", "check_intake.py"}:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    authoritative = check_authorities(instance)
    check_instance(instance)
    check_catalog_and_boundaries(instance)
    check_task_dag(dag, authoritative)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-0827 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
