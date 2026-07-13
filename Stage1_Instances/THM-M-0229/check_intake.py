#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0229 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0229"
ITEM_ID = "S56-M-0229-INTAKE"
RANK = 1241
BASE_REVISION = "c6fd6dad8fcfe5fd464416cd452f50286b546978"
BASE_TREE = "5a80b61d8fa09336779f8d1453dcfe4299c9472f"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
    "removable_singularity_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/"
        "Analysis/Complex/RemovableSingularity.lean"
    ),
    "meromorphic_basic_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/"
        "Analysis/Meromorphic/Basic.lean"
    ),
    "meromorphic_order_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/"
        "Analysis/Meromorphic/Order.lean"
    ),
    "cluster_point_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/"
        "Topology/ClusterPt.lean"
    ),
}
PRIVATE_REFERENCE_PARTS = (
    "/" + "home" + "/",
    "." + "cron" + "/",
    "." + "ops" + "/",
)
PLACEHOLDER = re.compile(r"\b(?:sorry|admit|sorryAx)\b")
BAD_DECLARATION = re.compile(
    r"^\s*(?:axiom|constant|opaque|unsafe)\b", re.MULTILINE
)


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


def check_public_files() -> None:
    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"{path.name} lacks final newline"
        assert b"\r" not in data, f"{path.name} contains a non-LF newline"
        assert b"\x00" not in data, f"{path.name} contains a NUL byte"
        text = data.decode("utf-8")
        assert not any(part in text for part in PRIVATE_REFERENCE_PARTS), (
            f"private/runtime path leaked in {path.name}"
        )
        assert all(line == line.rstrip() for line in text.splitlines()), (
            f"trailing whitespace in {path.name}"
        )


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet_path = path.resolve()
    packet = load(packet_path)
    packet_data = packet_path.read_bytes()
    assert packet_data.endswith(b"\n"), "worker packet lacks final newline"
    assert b"\r" not in packet_data and b"\x00" not in packet_data
    packet_text = packet_data.decode("utf-8")
    assert all(line == line.rstrip() for line in packet_text.splitlines()), (
        "worker packet contains trailing whitespace"
    )
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
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert receipt["worker_packet_sha256"] == sha256(packet_path)


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
        "name": "皮卡大定理",
        "category": "分析学 / 复分析",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }

    intake_item = next(item for item in execution["items"] if item["id"] == ITEM_ID)
    assert intake_item == {
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
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["execution_rank"] == RANK
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert instance["ordered_binders"] == instance["quantifiers"] == []
    assert instance["hypotheses"] == [] and instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert isinstance(instance["degenerate_cases_to_resolve"], list)
    assert instance["degenerate_cases_to_resolve"]
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R3"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(Path(path).name for path in instance["public_merge_targets"]) == OWNED_FILES

    source_revisions = instance["source_revisions"]
    assert source_revisions["repository_base"] == BASE_REVISION
    assert source_revisions["repository_base_tree"] == BASE_TREE
    assert source_revisions["repository_source_record_commit"] == (
        "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
    )
    assert source_revisions["repository_source_record_blob"] == (
        "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert source_revisions[field] == sha256(ROOT / relative), field
    assert source_revisions["mathlib"] == MATHLIB_REVISION
    assert source_revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""

    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["audit_complete"] is dag["theorem_complete"] is False
    assert dag["accepted_states"] == [] and len(dag["tasks"]) == len(TASK_SUFFIXES)
    previous = ITEM_ID
    for task, suffix in zip(dag["tasks"], TASK_SUFFIXES, strict=True):
        expected_id = f"S56-M-0229-{suffix}"
        assert task["id"] == expected_id
        assert task["phase"] == suffix.lower()
        assert task["depends_on"] == [previous]
        assert task["state"] == "open" and task["evidence_ids"] == []
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["completion_gate"] == (
            "rev-5.6 node-specific receipt and master acceptance"
        )
        execution_item = next(item for item in execution["items"] if item["id"] == expected_id)
        assert task["layer"] == execution_item["layer"]
        assert task["deliverable"] == execution_item["deliverable"]
        assert execution_item["depends_on"] == [previous]
        previous = expected_id
    assert "first_blocker" in dag["tasks"][0]

    lean = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert lean.count("import ") == 3
    assert "import Mathlib.Analysis.Complex.RemovableSingularity" in lean
    assert "import Mathlib.Analysis.Meromorphic.Order" in lean
    assert "import Mathlib.Topology.ClusterPt" in lean
    assert not PLACEHOLDER.search(lean)
    assert not BAD_DECLARATION.search(lean)
    assert "theorem " not in lean and "lemma " not in lean

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert isinstance(receipt["content_addressing_boundary"], str)
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M4", "R": "R3"}
    assert receipt["debt_vector_change_proposed"] is True
    assert isinstance(receipt["debt_delta_basis"], str) and receipt["debt_delta_basis"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["statement_fingerprints"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["validated_at"] == receipt["validation_ended_at"]
    assert receipt["validation_started_at"] < receipt["validation_ended_at"]
    assert isinstance(receipt["review_due"], str) and receipt["review_due"]
    assert isinstance(receipt["invalidation_inputs"], list)
    assert len(receipt["invalidation_inputs"]) >= 5
    assert receipt["support_state"] == "provisional_worker_only"
    assert receipt["supersession_state"] == "current_unsuperseded_worker_report"
    assert receipt["revocation_state"] == "not_revoked_but_unaccepted"
    assert isinstance(receipt["incident_path"], str) and receipt["incident_path"]
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    for recipe in recipes:
        assert isinstance(recipe["recipe_id"], str) and recipe["recipe_id"]
        assert isinstance(recipe["cwd"], str) and recipe["cwd"]
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert recipe["covered_ids"] == [ITEM_ID]
    lean_recipe = next(recipe for recipe in recipes if recipe["cwd"] == "Formalizations/Lean")
    assert lean_recipe["stdout_sha256"] == (
        "1c38c165d88ee0eb4f1e33770ad5f409f5a9c13b36490d08a8c974487ce35fcd"
    )
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert receipt["declaration_ownership"] == []
    assert set(receipt["changed_paths"]) == {
        ".stage1-worker-selftest.json",
        *(f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES),
    }
    for name, expected in receipt["untracked_owned_artifact_sha256"].items():
        assert name != "intake-receipt.json"
        assert expected == sha256(HERE / name), name

    check_public_files()
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print(
        "intake invariant check: ok "
        "(THM-M-0229 planned; H1/M4/R3; six open tasks)"
    )


if __name__ == "__main__":
    main()
