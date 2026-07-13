#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0213 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0213"
ITEM_ID = "S56-M-0213-INTAKE"
RANK = 1228
BASE_REVISION = "62fad55ced807fdc06921c45d6fcd1f9ad86a1c2"
BASE_TREE = "9d7c8fe49a4c859d90f3069dc47973ffc5ced768"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_EXCERPT_SHA256 = "c6f388f47e7173c9a8544f849b348c0f970b9280c00203e6d26c6994d5c4cb21"
STAGE0_EXCERPT_SHA256 = "ad49bb6bd47ee652faa183ca9413e25f9eca25eac9a6099cb90a39168a36fe3e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_SYMLINK_TARGET_SHA256 = "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
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
    "upper_half_plane_metric_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/"
        "UpperHalfPlane/Metric.lean"
    ),
    "affine_map_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/LinearAlgebra/"
        "AffineSpace/AffineMap.lean"
    ),
    "set_finite_basic_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Set/Finite/Basic.lean"
    ),
}
PROBED_DECLARATIONS = [
    "UpperHalfPlane",
    "UpperHalfPlane.dist_eq",
    "UpperHalfPlane.isometry_vertical_line",
    "UpperHalfPlane.instMetricSpace",
    "AffineMap.lineMap",
    "AffineMap.lineMap_injective",
    "Set.Infinite",
    "Set.Infinite.natEmbedding",
]


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
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


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


def run_recorded_action(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"]
    return result.stdout


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
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
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["worker_packet_output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def assert_known_failures(receipt: dict) -> None:
    failures = receipt["known_failures"]
    assert len(failures) == 6
    assert all(isinstance(item, str) and item for item in failures)
    assert any("primary or authoritative source" in item for item in failures)
    assert any("ambient synthetic geometry" in item for item in failures)
    assert any("Canonical Lean target" in item for item in failures)
    assert any("Formal anchor audit" in item for item in failures)
    assert any("blocked by H5" in item for item in failures)
    assert failures[-1] == "Master acceptance is pending."


def check_source_inputs(instance: dict, receipt: dict, worker_mode: bool) -> None:
    revisions = instance["source_revisions"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        if not worker_mode and field in {
            "authoritative_blueprint_sha256",
            "execution_dag_sha256",
        }:
            continue
        actual = sha256(ROOT / relative)
        assert revisions[field] == actual, f"stale instance source hash: {field}"
        assert receipt["source_inputs"][relative] == f"sha256:{actual}", (
            f"stale receipt source hash: {relative}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "双曲平行公设"
    assert target["category"] == instance["category"] == "几何学 / 非欧几何"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert (
        target["theorem_complete"]
        is instance["theorem_complete"]
        is dag["theorem_complete"]
        is False
    )

    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]", "[x]"} and item["depends_on"] == []
    if args.worker_packet is not None:
        assert item["state"] == "[ ]", "worker base must precede provisional integration"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == receipt["phase"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "does_not_select_one_stable_proposition" in instance["canonical_claim_status"]
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
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert (
        instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    )
    assert (
        instance["theorem_complete"]
        is dag["theorem_complete"]
        is receipt["theorem_complete"]
        is False
    )
    assert receipt["root_vector_after"] == instance["root_vector"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    if args.worker_packet is not None:
        assert git("rev-parse", "HEAD") == BASE_REVISION
        assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    else:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
            cwd=ROOT,
            check=True,
        )
    assert (
        git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md")
        == revisions["repository_source_record_blob"]
        == SOURCE_RECORD_BLOB
    )
    catalog_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(
        encoding="utf-8"
    ).splitlines(True)
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(
        encoding="utf-8"
    ).splitlines(True)
    assert hashlib.sha256("".join(catalog_lines[1535:1541]).encode()).hexdigest() == (
        revisions["repository_record_excerpt_sha256"]
    ) == SOURCE_RECORD_EXCERPT_SHA256
    assert hashlib.sha256("".join(stage0_lines[5918:5944]).encode()).hexdigest() == (
        revisions["stage0_projection_excerpt_sha256"]
    ) == STAGE0_EXCERPT_SHA256
    assert revisions["mathlib"] == MATHLIB_REVISION
    assert revisions["mathlib_tree"] == MATHLIB_TREE
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    check_source_inputs(instance, receipt, args.worker_packet is not None)

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0213-{suffix}"
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = "".join(catalog_lines)
    assert "**双曲平行公设**" in catalog
    assert "- 提出者: Nikolai Lobachevsky/János Bolyai" in catalog
    assert "- 时间: 1830" in catalog
    assert "- 陈述: 过直线外一点可作无数条平行线" in catalog
    stage0 = "".join(stage0_lines)
    assert "THM-M-0213 双曲平行公设" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {
        "THM-M-0215",
        "THM-M-0217",
        "THM-M-0218",
        "THM-M-0219",
        "THM-M-0220",
    }
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {
        "THM-M-0215": "双曲余弦定理",
        "THM-M-0217": "克莱因模型",
        "THM-M-0218": "庞加莱圆盘模型",
        "THM-M-0219": "庞加莱半平面模型",
        "THM-M-0220": "双曲面积公式",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert set(receipt["artifact_sha256"]) == OWNED_FILES - {"intake-receipt.json"}
    for name, expected in receipt["artifact_sha256"].items():
        assert sha256(HERE / name) == expected, f"owned artifact hash mismatch: {name}"
    dirty = receipt["dirty_input_evidence"]
    nonrecursive_owned = [HERE / name for name in OWNED_FILES if name != "intake-receipt.json"]
    assert dirty["owned_untracked_patch_sha256"] == path_bytes_hash(nonrecursive_owned)
    assert dirty["owned_untracked_manifest_sha256"] == path_manifest_hash(nonrecursive_owned)

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is receipt["signed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at == validated_at <= datetime.now(timezone.utc).astimezone()
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert_known_failures(receipt)
    assert receipt["output_summary"]
    assert receipt["selftest_result"] == "pass"

    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink()
    lake_target_hash = hashlib.sha256(os.readlink(lake_link).encode()).hexdigest()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{lake_target_hash}"
    assert lake_target_hash == LAKE_SYMLINK_TARGET_SHA256
    recipes = receipt["structured_validation_recipes"]
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
    }
    assert len(recipes) == 2
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    assert recipes_by_id["S56-M-0213-INTAKE-RECIPE-STRUCTURE"]["covered_declarations"] == []
    assert recipes_by_id["S56-M-0213-INTAKE-RECIPE-LEAN-PROBE"]["covered_declarations"] == (
        PROBED_DECLARATIONS
    )
    actions = receipt["validation_actions"]
    assert len(actions) == 2
    for action in actions:
        recipe = recipes_by_id[action["recipe_id"]]
        identity = {
            "cwd": recipe["cwd"],
            "argv": recipe["argv"],
            "env_allowlist": recipe["env_allowlist"],
            "timeout_seconds": recipe["timeout_seconds"],
            "network_policy": recipe["network_policy"],
            "expected_exit": recipe["expected_exit"],
        }
        assert action["recipe_sha256"] == canonical_json_sha256(identity)
        assert action["exit_code"] == 0
        assert action["covered_obligation_ids"] == [ITEM_ID]
        assert action["covered_declarations"] == recipe["covered_declarations"]
        action_started = datetime.fromisoformat(action["started_at"])
        action_ended = datetime.fromisoformat(action["ended_at"])
        assert started_at <= action_started <= action_ended <= ended_at
    action_by_id = {action["action_id"]: action for action in actions}
    structure_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
        HERE / "check_intake.py",
    ]
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        HERE / "IntakeProbe.lean",
    ]
    structure = action_by_id["S56-M-0213-INTAKE-ACTION-STRUCTURE"]
    lean = action_by_id["S56-M-0213-INTAKE-ACTION-LEAN-PROBE"]
    if args.worker_packet is not None:
        assert structure["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    assert lean["input_manifest_sha256"] == path_manifest_hash(lean_inputs)
    structure_stdout = b"intake invariant check: ok (THM-M-0213 planned; H5/M4/R4; six open tasks)\n"
    assert structure["stdout_sha256"] == structure["log_sha256"] == hashlib.sha256(
        structure_stdout
    ).hexdigest()
    lean_stdout = run_recorded_action(recipes_by_id[lean["recipe_id"]])
    lean_hash = hashlib.sha256(lean_stdout).hexdigest()
    assert lean["stdout_sha256"] == lean["log_sha256"] == lean_hash

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

    public_files = {
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
        "intake-receipt.json",
    }
    forbidden_fragments = ("/" + "home" + "/", "." + "cron" + "/")
    forbidden_completion_claim = "theorem_complete" + "=true"
    for name in public_files:
        text = (HERE / name).read_text(encoding="utf-8")
        assert all(fragment not in text for fragment in forbidden_fragments)
        assert forbidden_completion_claim not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0213 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
