#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0978 planned intake."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0978"
ITEM_ID = "S56-M-0978-INTAKE"
RANK = 1512
BASE_REVISION = "9c75282d42a7ef447d885d1d56997a79418bcd8a"
BASE_TREE = "cc5285432a02107fadffb68c698690d1b98ac5f2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
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
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_Applicable_Theorems.md": "779e4bd66e6a1c7615ca2884d899f02a871096125a30b8e229536fa5937cc85c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "8b838b50928f814c8f1250be02504dd42366e1d50b3fc2c885e8b2b0d3b3bbbd",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "4e9660ad9c7ae52649dc1744e8bb25c1a9d0ac25f7c2566a3ef05fb9d0b836e7",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        assert key not in result, f"duplicate JSON key: {key}"
        result[key] = value
    return result


def load_json(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return sha256_bytes(b"".join(lines[first - 1 : last]))


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def manifest_entry_sha256(target: dict) -> str:
    data = (json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return sha256_bytes(data)


def check_authorities(instance: dict) -> None:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(targets) == len(items) == 1
    target, item = targets[0], items[0]
    assert manifest["scope"]["covered_targets"] == 1546
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Hoeffding不等式",
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
    assert manifest_entry_sha256(target) == instance["source_revisions"][
        "manifest_entry_sha256"
    ]
    assert item == {
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

    duplicate = next(
        row for row in manifest["targets"] if row["theorem_id"] == "THM-M-0994"
    )
    assert duplicate["name"] == "霍夫丁不等式"
    assert duplicate["legacy_priority_slot"] == "S1-M-274"
    assert duplicate["category"] == "概率论与随机过程 / 概率论基础"
    assert duplicate["legacy_artifacts_accepted"] is False


def check_instance(instance: dict, dag: dict, receipt: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"]
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["execution_rank"] == RANK
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["source_status_untrusted"] == "已验证"
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert "blocked" in formal["gate_state"]
    assert formal["excluded_neighbor_target"] == "THM-M-0994"
    assert instance["ordered_binders"] == instance["quantifiers"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == receipt["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is False
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert "H1 records" in instance["status_boundary"]
    assert "No canonical proposition" in instance["status_boundary"]


def check_sources(instance: dict) -> None:
    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for relative, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / relative) == expected, f"changed authoritative input: {relative}"
    source_fields = {
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
    for field, relative in source_fields.items():
        assert revisions[field] == SOURCE_HASHES[relative]

    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 7141, 7146) == (
        revisions["repository_record_excerpt_sha256"]
    )
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 7266, 7271) == (
        revisions["duplicate_repository_record_excerpt_sha256"]
    )
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 26659, 26684) == (
        revisions["stage0_projection_excerpt_sha256"]
    )
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 27096, 27121) == (
        revisions["duplicate_stage0_projection_excerpt_sha256"]
    )

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Hoeffding不等式**") == 1
    assert catalog.count("**霍夫丁不等式**") == 1
    assert catalog.count("- 陈述: 有界随机变量和的集中") >= 2
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0978 Hoeffding不等式" in stage0
    assert "THM-M-0994 霍夫丁不等式" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    primary = revisions["primary_source"]
    assert primary["doi"] == "10.1080/01621459.1963.10500830"
    assert primary["observed_pdf_sha256"] == (
        "e4c1f30fef09d420bc4b791a53f95cb461f47b363d0d9debaf13e15fbaaef203"
    )
    assert primary["observed_pdf_bytes"] == 891780
    assert primary["observed_pdf_pages"] == 25
    assert "Theorem 2" in primary["inspected_boundary"]
    assert "H1" in primary["credit"] and "H0" in primary["credit"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == (
        revisions["mathlib_tree"]
    ) == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib)
    assert revisions["mathlib_subgaussian_source_sha256"] == sha256(
        mathlib / "Mathlib/Probability/Moments/SubGaussian.lean"
    )
    assert revisions["historical_stage1_candidate_sha256"] == sha256(
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_274.lean"
    )
    assert revisions["duplicate_intake_sha256"] == sha256(
        ROOT / "Stage1_Instances/THM-M-0994/instance.json"
    )
    assert revisions["duplicate_crosswalk_sha256"] == sha256(
        ROOT / "Stage1_Instances/THM-M-0994/source-statement-crosswalk.md"
    )
    assert revisions["duplicate_statement_sha256"] == sha256(
        ROOT / "Stage1_Instances/THM-M-0994/Statement.lean"
    )
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert sha256_bytes(lake_target) == revisions["lake_symlink_target_string_sha256"]


def check_task_dag(dag: dict, receipt: dict) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    execution = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    expected = []
    prior = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0978-{suffix}"
        source = next(row for row in execution if row["id"] == task_id)
        task = dag["tasks"][layer - 1]
        expected.append((task_id, layer, [prior]))
        assert task["id"] == task_id and task["depends_on"] == [prior]
        assert task["theorem_id"] == THEOREM_ID
        assert task["execution_rank"] == RANK
        assert task["phase"] == source["phase"]
        assert task["layer"] == source["layer"] == layer
        assert task["owned_paths"] == source["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["attempts"] == source["attempts"] == 0
        assert task["children"] == source["children"] == []
        assert task["state"] == "open" and task["evidence_ids"] == []
        prior = task_id
    assert len(dag["tasks"]) == 6
    assert [(t["id"], t["layer"], t["depends_on"]) for t in dag["tasks"]] == expected
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]


def check_receipt(receipt: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["source_inputs"] == {
        relative: f"sha256:{digest}" for relative, digest in SOURCE_HASHES.items()
    }
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
    assert receipt["selftest_result"] == "pass"
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert isinstance(recipe["expected_outputs"], list) and recipe["expected_outputs"]
        assert recipe["covered_obligation_ids"] == []
        assert recipe["covered_ids"] == [ITEM_ID]
        assert recipe["expected_exit"] == recipe["exit_code"] == 0


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path.resolve())
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
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    hashes = receipt["non_self_referential_owned_artifact_sha256"]
    expected_hashed = set(expected_changed) - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
        f"Stage1_Instances/{THEOREM_ID}/validation.md",
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
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        content = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in content and ".cron/" not in content
        assert "theorem_complete=true" not in content
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|admit|sorryAx)\b", probe)
    assert not re.search(
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)[ \t]", probe, re.MULTILINE
    )
    ast.parse((HERE / "check_intake.py").read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    check_authorities(instance)
    check_instance(instance, dag, receipt)
    check_sources(instance)
    check_task_dag(dag, receipt)
    check_receipt(receipt)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print(
        "check_intake: ok (THM-M-0978 planned H1/M3/R4 intake; "
        "source, duplicate boundary, pins, receipt, and six open tasks agree)"
    )


if __name__ == "__main__":
    main()
