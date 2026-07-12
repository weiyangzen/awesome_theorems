#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1379 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1379"
ITEM_ID = "S56-M-1379-INTAKE"
RANK = 989
BASE_REVISION = "d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9"
BASE_TREE = "829a47c47ae831cada4f8acc6c2c00ba5883215e"
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
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
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "bcbce90f45f8df2b674e642470a641bea5a6df5c750be2ac69aa7e686f1c1d72",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0f01e5060d405907103ce214fe2b550b50fc081fbb0dd39f6ca3713cc23bfcd0",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/researches/physics_theorems.md": "6abf9da63cf075b0c6a05f3a245838ec0d7848fe873c43f529a7e0ee72cf94fa",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_changed_paths() -> set[str]:
    return {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }


def check_source_inputs(instance: dict, receipt: dict) -> None:
    for relative, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / relative) == expected, f"stale source hash: {relative}"
        assert receipt["source_inputs"][relative] == f"sha256:{expected}"

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert revisions["repository_source_record_commit"] == (
        "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
    )
    assert revisions["current_repository_math_source_blob"] == (
        "b78ec1f48495aa5747ef252665ab58e418d195e4"
    )
    assert revisions["current_repository_physics_source_blob"] == (
        "b340a659c1bc858f3474dbc790dda2d6a024a4d5"
    )
    assert revisions["mathlib"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    assert revisions["mathlib_tree"] == "bdc39a3123201dae413a9d9be56ec242c19e5c2b"

    math_record = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**Hamilton-Jacobi方程**" in math_record
    assert "- 陈述: 经典力学的偏微分方程形式" in math_record
    physics_record = (ROOT / "Docs/researches/physics_theorems.md").read_text(encoding="utf-8")
    assert "**1. 哈密顿-雅可比方程**" in physics_record
    assert "H(q,∂S/∂q,t) + ∂S/∂t = 0" in physics_record


def check_authority(instance: dict, dag: dict, receipt: dict) -> None:
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 108
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    expected_tasks: list[tuple[str, list[str]]] = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-1379-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])

    authoritative_downstream = [
        row for row in execution["items"]
        if row["theorem_id"] == THEOREM_ID and row["id"] != ITEM_ID
    ]
    assert len(authoritative_downstream) == len(dag["tasks"]) == 6
    authoritative_by_id = {row["id"]: row for row in authoritative_downstream}
    for task in dag["tasks"]:
        source = authoritative_by_id[task["id"]]
        for key in ("depends_on", "phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[key] == source[key]
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]


def check_instance(instance: dict, dag: dict, receipt: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert formal["backend"] == "lean4"
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-P-0755", "THM-M-1380", "THM-M-1198", "THM-M-1516"
    }


def check_receipt(receipt: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert set(receipt["changed_paths"]) == expected_changed_paths()
    assert receipt["covered_node_ids"] == receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert receipt["declaration_ownership"] == []
    assert receipt["root_vector_before"] == {"H": "unclassified", "M": "unclassified", "R": "unclassified"}
    assert receipt["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}

    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    required_recipe_keys = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "covered_ids", "covered_obligation_ids",
        "covered_declarations",
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    assert recipes[0]["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM_ID}/check_intake.py"]
    assert recipes[1]["argv"] == [
        "lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"
    ]

    for key in (
        "owner", "validation_started_at", "validation_ended_at", "validated_at", "review_due",
        "support_state", "supersession_state", "incident_path", "first_failed_gate",
        "retry_condition", "status_boundary",
    ):
        assert isinstance(receipt[key], str) and receipt[key].strip()
    assert receipt["known_failures"]


def check_files(instance: dict) -> None:
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
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

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == expected_changed_paths()
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["accepted_receipt_ids"] == []
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    check_source_inputs(instance, receipt)
    check_authority(instance, dag, receipt)
    check_instance(instance, dag, receipt)
    check_receipt(receipt)
    check_files(instance)
    if args.worker_packet is not None:
        check_worker_packet((ROOT / args.worker_packet).resolve(), receipt)
    print("intake invariant check: ok (THM-M-1379 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
