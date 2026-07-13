#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0619 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0619"
ITEM_ID = "S56-M-0619-INTAKE"
RANK = 1313
BASE_REVISION = "5bc32428da3d17f138ceca67f30fbc2d149da1ba"
BASE_TREE = "7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "unclassified", "M": "M3", "R": "R4"}
PROBE_OUTPUT_SHA256 = "d93c9a2c064586f9f08ce2b41e4388ceef9271a818a8b0eddd2483bb777fe38f"
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
PROBE_DECLARATIONS = [
    "CompactSpace.tendsto_subseq",
    "IsCompact.tendsto_subseq",
    "SeqCompactSpace.tendsto_subseq",
    "isCompact_iff_isSeqCompact",
    "compactSpace_iff_seqCompactSpace",
]
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "0ad83b1e2be2ebd75cf307334948fd3a6347435df605140484e75ed74389e08f",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "bf164d9974376dde827d50b07725bc7692a36dea3a203ac67b0ee24cd1db3dd1",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/Topology/Sequences.lean": "4f49427b838a566edb7c480fc0419cb49d3521790c32d002a176de234225e3a9",
    "Mathlib/Topology/Defs/Sequences.lean": "934cb61f9fd106ecf4965bd48c5543f2f67ad41ebfe55b548fe6f4c3854f3035",
}
EXCERPT_HASHES = {
    "catalog": "57cfd3cb8311338f3cea95b13ce0bae4ca6699d79235f5ee069df51f2dd35725",
    "stage0": "90ebf55b6a63cfcccc050820fc574e0d273db04a8751229e0bd93cac318707b8",
    "neighbor": "514ddfa34d8a0b5fad190adf971cfd0b528df22f9e782dafc053a55abb7cce48",
    "manifest": "e458df870367e9c1cd6a47a05defcb6c20da2ec9963fc48c2c8ac167f9b9de66",
    "dag": "379c58aec0a66f103aa1e33a9ccfc79e8b72c14a1ee8863518c9ea9c69ce1d2d",
}


def load_json(path: Path) -> dict:
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


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def canonical_object_sha256(value: object) -> str:
    payload = (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(payload).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_authorities(instance: dict) -> list[dict]:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    assert manifest["scope"]["covered_targets"] == 1546
    assert manifest["scope"]["canonical_sorted_target_id_set_sha256"] == (
        "e07deabaab3463cc1f92cdf5c0cf50ad9f8270d35554529c375d20a8512d8f1a"
    )
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "波尔查诺-魏尔斯特拉斯定理",
            "category": "拓扑学 / 点集拓扑",
            "source_status_untrusted": "已验证",
            "baseline": "L0",
            "rework_required": True,
            "legacy_artifacts_accepted": False,
            "target_lane": "hard_statement_first_partial_verification",
            "intake_score": 86,
            "lifecycle_mode": "planned",
            "theorem_complete": False,
        }
    ]
    target = matches[0]
    for field in (
        "execution_rank",
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
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]
    assert canonical_object_sha256(target) == EXCERPT_HASHES["manifest"]

    items = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    intake = next(row for row in items if row["id"] == ITEM_ID)
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
    assert canonical_object_sha256(intake) == EXCERPT_HASHES["dag"]
    return items


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    for field in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert formal["declaration_candidates"] == PROBE_DECLARATIONS
    assert "primary_source_selection" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["authoritative_blueprint"] == "Docs/Stage1_Blueprint_rev-5.6.md"
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    boundaries = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert boundaries == {"THM-M-0264", "THM-M-0618"}

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    revision_fields = {
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
    for field, path in revision_fields.items():
        assert revisions[field] == SOURCE_HASHES[path] == sha256(ROOT / path)
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 4594, 4599) == (
        revisions["repository_record_excerpt_sha256"]
    ) == EXCERPT_HASHES["catalog"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 16936, 16961) == (
        revisions["stage0_projection_excerpt_sha256"]
    ) == EXCERPT_HASHES["stage0"]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 1901, 1906) == (
        revisions["neighbor_thm_m_0264_excerpt_sha256"]
    ) == EXCERPT_HASHES["neighbor"]
    assert revisions["manifest_entry_sha256"] == EXCERPT_HASHES["manifest"]
    assert revisions["execution_dag_intake_entry_sha256"] == EXCERPT_HASHES["dag"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    mathlib_fields = {
        "mathlib_topology_sequences_sha256": "Mathlib/Topology/Sequences.lean",
        "mathlib_topology_defs_sequences_sha256": "Mathlib/Topology/Defs/Sequences.lean",
    }
    for field, path in mathlib_fields.items():
        assert revisions[field] == MATHLIB_HASHES[path] == sha256(mathlib / path)


def check_catalog() -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**波尔查诺-魏尔斯特拉斯定理**") == 2
    assert catalog.count("- 陈述: 有界数列必有收敛子列") == 1
    assert catalog.count("- 陈述: 紧度量空间序列有收敛子列") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0264 波尔查诺-魏尔斯特拉斯定理" in stage0
    assert "THM-M-0619 波尔查诺-魏尔斯特拉斯定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0


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
        task_id = f"S56-M-0619-{suffix}"
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
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
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
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"].startswith("canonical source-statement identity")
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()
    }
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    target_hash = hashlib.sha256((str(lake.readlink()) + "\n").encode()).hexdigest()
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == "sha256:" + target_hash
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_node_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    assert recipes[1]["covered_declarations"] == PROBE_DECLARATIONS


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
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]


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
    for name in OWNED_FILES - {"IntakeProbe.lean", "check_intake.py"}:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx)\b|^[ \t]*(axiom|constant|opaque|unsafe)[ \t]",
        re.MULTILINE,
    )
    assert prohibited.search(probe) is None
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe


def check_lean_probe() -> None:
    lean_run = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0619/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert lean_run.returncode == 0, lean_run.stdout
    assert hashlib.sha256(lean_run.stdout.encode()).hexdigest() == PROBE_OUTPUT_SHA256
    for declaration in PROBE_DECLARATIONS:
        assert declaration in lean_run.stdout
    assert "[propext, Classical.choice, Quot.sound]" in lean_run.stdout
    assert "[propext, Quot.sound]" in lean_run.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    authoritative = check_authorities(instance)
    check_instance(instance)
    check_catalog()
    check_task_dag(dag, authoritative)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    check_lean_probe()
    if args.worker_packet is not None:
        packet_path = args.worker_packet
        if not packet_path.is_absolute():
            packet_path = ROOT / packet_path
        check_worker_packet(packet_path, receipt)
    print("intake invariant check: ok (THM-M-0619 planned; H-unclassified/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
