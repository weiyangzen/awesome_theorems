#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0837 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


if not __debug__:
    raise RuntimeError("intake validation requires Python assertions; do not use -O/PYTHONOPTIMIZE")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0837"
ITEM_ID = "S56-M-0837-INTAKE"
RANK = 1394
BASE_REVISION = "be8701e88e791545c16a262edd1909486d5cef4b"
BASE_TREE = "78b0a751473bf6d71f453a6aad18b130268a3428"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_BLOCK_SHA256 = "7761e6a8dc05dc290a26c310351f0f85345792822c82244b8b699a156dc6acb9"
STAGE0_BLOCK_SHA256 = "1934fb1c90bc158e3523ca068b63c5d31a2a893d8ef8ee63704e0319f0297a9a"
NEIGHBOR_BLOCK_SHA256 = "92cf8025233ce63892e623338d8ef5db7e9fb4acd3ef21ef44ffeea90d8febaf"
MANIFEST_ENTRY_SHA256 = "e5cec88626c3a77e3a9974f88bb823b4d9652d243531842664863bf8ecb07c0a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_COLORING_SHA256 = "42c4c6ac9c763df08f33a9fc4cf329e19908dacc630be771a547fcb583f7be56"
LAKE_SYMLINK_TARGET_SHA256 = "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
ROOT_VECTOR = {"H": "H5", "M": "M4", "R": "R4"}
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
    "Docs/Stage1_Blueprint_rev-5.6.md": "201ff7722835a8360e3400c6f173b1e6684462b46ce5ed02e6b37ba51baf81bb",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0e2192895bfd08136cf7d965e1c9d942ff0d040568b72552bc7869c5801b41fb",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
PROBE_DECLARATIONS = [
    "SimpleGraph",
    "SimpleGraph.Coloring",
    "SimpleGraph.Colorable",
    "SimpleGraph.Coloring.mk",
    "SimpleGraph.Coloring.valid",
    "SimpleGraph.Colorable.chromaticNumber_le",
    "SimpleGraph.chromaticNumber",
    "Fin 4",
]


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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def canonical_manifest_entry(target: dict) -> str:
    encoded = (json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def check_authorities(instance: dict, *, worker_mode: bool) -> list[dict]:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    assert manifest["schema_version"] == "stage1-target-set/5.6.2"
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
            "name": "Robertson-Sanders-Seymour-Thomas证明",
            "category": "组合数学 / 图论",
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
    assert canonical_manifest_entry(target) == MANIFEST_ENTRY_SHA256
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "category",
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
    if worker_mode:
        assert intake["state"] == "[ ]" and intake["attempts"] == 0
    return items


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "proof_family" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    for field in (
        "module",
        "candidate_expression",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert "not_a_stable_truth_valued_proposition" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "does not refute or question" in instance["status_boundary"]
    assert "No canonical statement" in instance["status_boundary"]
    assert instance["source_status"].startswith("H5_")

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git(
        "rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md'
    ) == revisions["repository_source_record_blob"] == SOURCE_RECORD_BLOB
    assert revisions["repository_source_record_commit"] == SOURCE_RECORD_COMMIT
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6145, 6150) == (
        revisions["repository_record_block_sha256"]
    ) == SOURCE_RECORD_BLOCK_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 22847, 22872) == (
        revisions["stage0_projection_block_sha256"]
    ) == STAGE0_BLOCK_SHA256
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6124, 6157) == (
        revisions["neighbor_catalog_block_sha256"]
    ) == NEIGHBOR_BLOCK_SHA256
    assert revisions["manifest_entry_sha256"] == MANIFEST_ENTRY_SHA256
    for path, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / path) == expected, f"changed authoritative input: {path}"
    field_map = {
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
    for field, path in field_map.items():
        assert revisions[field] == SOURCE_HASHES[path], f"stale instance hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    coloring = mathlib / "Mathlib/Combinatorics/SimpleGraph/Coloring.lean"
    assert sha256(coloring) == revisions["mathlib_coloring_source_sha256"] == MATHLIB_COLORING_SHA256
    assert "* Planar graphs" in coloring.read_text(encoding="utf-8")
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    assert hashlib.sha256(str(lake.readlink()).encode()).hexdigest() == (
        revisions["lake_symlink_target_sha256"]
    ) == LAKE_SYMLINK_TARGET_SHA256


def check_catalog_and_boundaries(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Robertson-Sanders-Seymour-Thomas证明**") == 1
    assert "- 提出者: Robertson等" in catalog
    assert "- 时间: 1997" in catalog
    assert catalog.count("- 陈述: 四色定理的新证明") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert stage0.count("THM-M-0837 Robertson-Sanders-Seymour-Thomas证明") == 1
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert "- 现有 machine-checked 状态: 待补充" in stage0

    blocker = instance["statement_blocker"]
    for token in (
        "ordinary Four-Colour conclusion",
        "RSST provenance",
        "reducibility and unavoidability",
        "quadratic algorithm",
        "THM-M-0833",
    ):
        assert token in blocker, f"missing statement boundary: {token}"
    boundaries = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert boundaries == {"THM-M-0833", "THM-M-0836", "THM-M-0838"}
    lead = instance["bibliographic_leads_not_credited"][0]
    assert "10.1006/jctb.1997.1750" in lead["citation"]
    assert lead["crossref_response_sha256"] == (
        "935a9ba2d5dd08bdb4c6b095e8c882c53658d40e44dd6915ddcb37849ba61b61"
    )
    announcement = instance["inspected_discovery_sources_not_credited"][1]
    assert announcement["pdf_sha256"] == (
        "df597ecb200d7fcfecbebd00ce5d79c13e9e106fd47b39c9b9ddca225baeaca3"
    )
    assert "unresolved" in announcement["pagination_boundary"]
    assert {row["identifier"] for row in instance["computational_source_leads_not_credited"]} == {
        "arXiv:1401.6481v1",
        "arXiv:1401.6485v1",
    }


def check_task_dag(dag: dict, authoritative_items: list[dict]) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert dag["accepted_states"] == []
    assert [task["id"] for task in dag["tasks"]] == [
        f"S56-M-0837-{suffix}" for suffix in TASK_SUFFIXES
    ]
    for index, task in enumerate(dag["tasks"], start=1):
        expected_id = f"S56-M-0837-{TASK_SUFFIXES[index - 1]}"
        predecessor = ITEM_ID if index == 1 else dag["tasks"][index - 2]["id"]
        assert task["id"] == expected_id and task["depends_on"] == [predecessor]
        assert task["layer"] == index and task["state"] == "open"
        assert task["evidence_ids"] == []
        authority = next(row for row in authoritative_items if row["id"] == expected_id)
        for field in (
            "phase",
            "layer",
            "depends_on",
            "owned_paths",
            "deliverable",
            "completion_gate",
        ):
            assert task[field] == authority[field]
    assert "redirect" in dag["tasks"][0]["first_blocker"]


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["covered_task_ids"] == receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
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
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"] == "master acceptance of the provisional self-tested intake receipt"
    assert "proof-family" in receipt["first_failed_theorem_gate"]
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["dirty_input_evidence"]["preflight_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()
    }
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lake_symlink_target_string_sha256"] == LAKE_SYMLINK_TARGET_SHA256
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    assert worker_inputs["mathlib_coloring_source_sha256"] == MATHLIB_COLORING_SHA256

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    for recipe in recipes:
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        output = recipe["expected_outputs"][0]
        assert output["semantic_hash_policy"] == "exact_bytes_sha256"
        assert re.fullmatch(r"[0-9a-f]{64}", output["sha256"])
    assert recipes[0]["argv"] == [
        "python3",
        "-B",
        "Stage1_Instances/THM-M-0837/check_intake.py",
    ]
    assert recipes[0]["covered_declarations"] == []
    assert recipes[1]["argv"] == [
        "lake",
        "env",
        "lean",
        "../../Stage1_Instances/THM-M-0837/IntakeProbe.lean",
    ]
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
    checked_paths = list(HERE.iterdir())
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
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
    authoritative = check_authorities(instance, worker_mode=args.worker_packet is not None)
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    check_instance(instance)
    check_catalog_and_boundaries(instance)
    check_task_dag(dag, authoritative)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-0837 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
