#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0624."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0624"
ITEM_ID = "S56-M-0624-INTAKE"
RANK = 1318
BASE_REVISION = "5bc32428da3d17f138ceca67f30fbc2d149da1ba"
BASE_TREE = "7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f"
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
INTEGRATION_MUTABLE_HASHES = {
    "authoritative_blueprint_sha256",
    "execution_dag_sha256",
}
MATHLIB_SOURCE_HASHES = {
    "mathlib_metrizable_basic_source_sha256": "Mathlib/Topology/Metrizable/Basic.lean",
    "mathlib_locally_finite_source_sha256": "Mathlib/Topology/LocallyFinite.lean",
    "mathlib_separation_regular_source_sha256": "Mathlib/Topology/Separation/Regular.lean",
    "mathlib_bases_source_sha256": "Mathlib/Topology/Bases.lean",
}


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


def git_blob_sha256(revision: str, relative: str) -> str:
    data = subprocess.check_output(
        ["git", "show", f"{revision}:{relative}"], cwd=ROOT, stderr=subprocess.DEVNULL
    )
    return hashlib.sha256(data).hexdigest()


def expected_source_hash(field: str, relative: str) -> str:
    if field in INTEGRATION_MUTABLE_HASHES:
        return git_blob_sha256(BASE_REVISION, relative)
    return sha256(ROOT / relative)


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode()).hexdigest()


def check_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte in {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path}"
    )


def check_worker_packet(path: Path, receipt: dict) -> None:
    check_text_hygiene(path.resolve())
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
    assert set(packet) == required
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert all(
        isinstance(command, dict)
        and isinstance(command.get("command"), str)
        and isinstance(command.get("exit_code"), int)
        for command in packet["commands"]
    )
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

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(targets) == len(items) == 1
    target, item = targets[0], items[0]

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "Nagata-Smirnov度量化定理"
    assert target["category"] == instance["category"] == "拓扑学 / 点集拓扑"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
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
    assert instance["literal_source_claim_zh"] == "拓扑空间可度量化的充要条件"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
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
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
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
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == expected_source_hash(field, relative), (
            f"stale source hash: {field}"
        )
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 4629, 4634
    )
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 17071, 17096
    )

    catalog_excerpt = "".join(
        (ROOT / "Docs/researches/math_theorems.md")
        .read_text(encoding="utf-8")
        .splitlines(keepends=True)[4628:4634]
    )
    assert "**Nagata-Smirnov度量化定理**" in catalog_excerpt
    assert "- 提出者: Jun-iti Nagata/Yuri Smirnov" in catalog_excerpt
    assert "- 时间: 1950" in catalog_excerpt
    assert "- 陈述: 拓扑空间可度量化的充要条件" in catalog_excerpt
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0624 Nagata-Smirnov度量化定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    for field, relative in MATHLIB_SOURCE_HASHES.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0624-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    recipes = receipt["structured_validation_recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {
        "S56-M-0624-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0624-INTAKE-RECIPE-LEAN-PROBE",
    }
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["covered_task_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet.resolve())
    for path in checked_paths:
        if path.is_file():
            check_text_hygiene(path)
    for name in (
        "README.md",
        "instance.json",
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0624 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
