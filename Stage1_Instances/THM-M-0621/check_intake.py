#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0621 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0621"
ITEM_ID = "S56-M-0621-INTAKE"
RANK = 1315
BASE_REVISION = "5bc32428da3d17f138ceca67f30fbc2d149da1ba"
BASE_TREE = "7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_EXCERPT_SHA256 = "dfeefe23344b865af25424e52e7d5735fadcb6365e6eb3b70dd77e65012679a9"
STAGE0_EXCERPT_SHA256 = "d4dd8126e8daea45a53c90501c16c229583c092123d25f35b957f2a844230dc4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "14e804991e42d6c82801e9ac7f84dca022e5de508280950b9523206935b45328"
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
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
PROBE_DECLARATIONS = (
    "NormalSpace",
    "NormalSpace.normal",
    "normal_separation",
    "normal_exists_closure_subset",
    "@exists_continuous_zero_one_of_isClosed",
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
INTEGRATION_MUTABLE_HASH_FIELDS = {
    "authoritative_blueprint_sha256",
    "execution_dag_sha256",
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


def git_blob_sha256(revision: str, relative: str) -> str:
    data = subprocess.check_output(
        ["git", "show", f"{revision}:{relative}"], cwd=ROOT, stderr=subprocess.DEVNULL
    )
    return hashlib.sha256(data).hexdigest()


def expected_source_hash(field: str, relative: str) -> str:
    if field in INTEGRATION_MUTABLE_HASH_FIELDS:
        return git_blob_sha256(BASE_REVISION, relative)
    return sha256(ROOT / relative)


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode("utf-8")).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    required = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert required <= set(packet), "worker packet omits a scheduler-required field"
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert sha256(path.resolve()) == receipt["worker_packet_sha256"]
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["first_failed_gate"] == receipt["first_failed_gate"]
    assert packet["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert packet["status_boundary"] == receipt["status_boundary"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def check_recipe(recipe: dict) -> None:
    required = {
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
    assert required <= set(recipe), "structured recipe omits a normative field"
    assert isinstance(recipe["argv"], list) and recipe["argv"]
    assert all(isinstance(arg, str) and arg for arg in recipe["argv"])
    assert isinstance(recipe["env_allowlist"], dict)
    assert isinstance(recipe["timeout_seconds"], int) and recipe["timeout_seconds"] > 0
    assert recipe["network_policy"] in {"fetch_only", "denied", "explicitly_required"}
    assert recipe["expected_exit"] == 0
    assert isinstance(recipe["expected_outputs"], list) and recipe["expected_outputs"]
    assert isinstance(recipe["covered_obligation_ids"], list)
    assert isinstance(recipe["covered_declarations"], list)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    source_field_by_path = {relative: field for field, relative in SOURCE_HASH_FIELDS.items()}
    for relative, tagged_digest in receipt["source_inputs"].items():
        field = source_field_by_path[relative]
        assert tagged_digest == f"sha256:{expected_source_hash(field, relative)}"

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "乌雷松引理"
    assert target["category"] == instance["category"] == "拓扑学 / 点集拓扑"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in ("[ ]", "[_]") and item["depends_on"] == []
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
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert formal["declaration_candidates"] == ["exists_continuous_zero_one_of_isClosed"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["provisional_family_intake_vector"] == {"H": None, "M": "M3", "R": "R4"}
    assert instance["root_vector"] is None
    assert instance["root_vector_status"].startswith("unclassified_until_canonical_statement")
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == revisions["repository_base_tree"] == BASE_TREE
    if args.worker_packet is not None:
        assert git("rev-parse", "HEAD") == BASE_REVISION
    else:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert git("hash-object", "Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == expected_source_hash(field, relative), f"stale source hash: {field}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 4608, 4613) == SOURCE_EXCERPT_SHA256
    assert revisions["repository_record_excerpt_sha256"] == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 16990, 17015) == STAGE0_EXCERPT_SHA256
    assert revisions["stage0_projection_excerpt_sha256"] == STAGE0_EXCERPT_SHA256

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert revisions["urysohns_lemma_source_sha256"] == sha256(
        mathlib / "Mathlib/Topology/UrysohnsLemma.lean"
    )
    assert revisions["urysohns_bounded_source_sha256"] == sha256(
        mathlib / "Mathlib/Topology/UrysohnsBounded.lean"
    )
    assert revisions["separation_regular_source_sha256"] == sha256(
        mathlib / "Mathlib/Topology/Separation/Regular.lean"
    )

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0621-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**乌雷松引理**" in catalog
    assert "- 提出者: Pavel Urysohn" in catalog
    assert "- 时间: 1925" in catalog
    assert "- 陈述: 正规空间中闭集的分离" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0621 乌雷松引理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0622", "THM-M-0623"}

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    if args.worker_packet is not None:
        assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
            f"sha256:{LAKE_SYMLINK_TARGET_SHA256}"
        )
        lake_path = ROOT / "Formalizations/Lean/.lake"
        assert lake_path.is_symlink()
        lake_target = lake_path.readlink().as_posix().encode()
        assert hashlib.sha256(lake_target).hexdigest() == LAKE_SYMLINK_TARGET_SHA256
        packet_patch = subprocess.run(
            ["git", "diff", "--no-index", "--binary", "/dev/null", ".stage1-worker-selftest.json"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        assert packet_patch.returncode == 1
        assert hashlib.sha256(packet_patch.stdout).hexdigest() == receipt["worker_packet_no_index_patch_sha256"]
    packet_fields = {
        "platform",
        "environment",
        "validation_started_at",
        "validation_ended_at",
        "validated_at",
        "owner",
        "attestor",
        "review_due",
        "invalidation_inputs",
        "support_state",
        "supersession_state",
        "revocation_state",
        "incident_path",
    }
    assert packet_fields <= set(receipt), "receipt omits a section 9.1 packet field"
    assert receipt["invalidation_inputs"] and receipt["support_state"] == "provisional_worker_selftest_only"
    assert receipt["validation_ended_at"] == receipt["validated_at"]
    assert receipt["validated_at"] != "PENDING_FINAL_REPLAY"
    assert len(receipt["structured_validation_recipes"]) == 2
    for recipe in receipt["structured_validation_recipes"]:
        check_recipe(recipe)

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe
    assert "#print axioms exists_continuous_zero_one_of_isClosed" in probe
    lean_run = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0621/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert lean_run.returncode == 0, lean_run.stdout
    assert hashlib.sha256(lean_run.stdout.encode()).hexdigest() == PROBE_OUTPUT_SHA256
    assert "exists_continuous_zero_one_of_isClosed" in lean_run.stdout
    assert "[propext, Classical.choice, Quot.sound]" in lean_run.stdout

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0621 planned; H-unclassified/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
