#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0857 planned intake."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0857"
ITEM_ID = "S56-M-0857-INTAKE"
RANK = 1411
BASE_REVISION = "561d83df037004ceb2259292d7c63be930b40391"
BASE_TREE = "6eb02475bf5a70139d60615c924b31c930efc2bb"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
SOURCE_HASHES = {
    "target_manifest_sha256": (
        "Docs/Stage1_Targets_rev-5.6.json",
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    ),
    "authoritative_blueprint_sha256": (
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "18d0d349f9108142784ac31f2b7dde5562b4c70dc6b4565a45aa915a00c27290",
    ),
    "execution_dag_sha256": (
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "3080f2fd70f4072f451fa25c213422dde8f940a73aa3a1eddc14b3a2382b0ea2",
    ),
    "execution_skill_sha256": (
        "skills/execute-stage1-rev56/SKILL.md",
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    ),
    "blueprint_guidelines_sha256": (
        "Docs/Blueprint_Guidelines.md",
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    ),
    "repository_math_source_sha256": (
        "Docs/researches/math_theorems.md",
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    ),
    "stage0_blueprint_sha256": (
        "Docs/Stage0_Blueprint.md",
        "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    ),
    "lean_toolchain_file_sha256": (
        "Formalizations/Lean/lean-toolchain",
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    ),
    "lake_manifest_sha256": (
        "Formalizations/Lean/lake-manifest.json",
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    ),
}
MATHLIB_HASHES = {
    "mathlib_matching_source_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Matching.lean",
        "7e8b873ee73808358dd1d1a36e0c72cd4b27f95b7ba29f23286d3f076f8abc4b",
    ),
    "mathlib_finite_source_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Finite.lean",
        "968b2c58d0e77e91c69815bf1ed5e3fafa7302eaebc08139d9fdbb323ad910e8",
    ),
    "mathlib_connected_source_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Connectivity/Connected.lean",
        "9171842c49be5f8951c6a2d5c39ae374279d46eaa317efd69bdf3039d289eeff",
    ),
    "mathlib_edge_connectivity_source_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Connectivity/EdgeConnectivity.lean",
        "7b4d638ae2e98b8131a3d4eccc53f3e52afab999d39895c5d21bd23b49db06b2",
    ),
    "mathlib_tutte_source_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Tutte.lean",
        "47072b914aa564222ef8013092c38fa62227fea8230e308cc3eb5f11afcdffc3",
    ),
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
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


def check_text(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path}"
    )


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
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    authoritative_dag = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Petersen定理",
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
    for key in (
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
        assert instance[key] == target[key]
    assert instance["name_zh"] == target["name"] and instance["category"] == target["category"]

    authoritative_rows = authoritative_dag["items"]
    intake = next(row for row in authoritative_rows if row["id"] == ITEM_ID)
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

    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert formal["gate_state"].startswith("blocked_")
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "No H0, M0, R0" in instance["status_boundary"]
    assert "master acceptance is claimed" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == (
        revisions["current_repository_math_source_blob"]
    )
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6285, 6290) == (
        revisions["repository_record_excerpt_sha256"]
    )
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 23387, 23412) == (
        revisions["stage0_projection_excerpt_sha256"]
    )
    for field, (relative, digest) in SOURCE_HASHES.items():
        assert revisions[field] == digest == sha256(ROOT / relative), f"stale hash: {relative}"
    assert revisions["primary_source_pdf_sha256"] == (
        instance["primary_source"]["observed_pdf_sha256"]
    )

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, (relative, digest) in MATHLIB_HASHES.items():
        assert revisions[field] == digest == sha256(mathlib / relative), f"stale mathlib hash: {relative}"

    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is dag["theorem_complete"] is False
    assert len(dag["tasks"]) == 6
    dependency = ITEM_ID
    for layer, (task, suffix) in enumerate(zip(dag["tasks"], TASK_SUFFIXES), start=1):
        task_id = f"S56-M-0857-{suffix}"
        authority = next(row for row in authoritative_rows if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["layer"] == authority["layer"] == layer
        assert task["phase"] == authority["phase"]
        assert task["owned_paths"] == authority["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authority["deliverable"]
        assert task["completion_gate"] == authority["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Petersen定理**") == 1
    assert "- 提出者: Julius Petersen" in catalog
    assert "- 时间: 1891" in catalog
    assert catalog.count("- 陈述: 三次桥less图有完美匹配") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0857 Petersen定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
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
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert receipt["support_state"] == "provisional_unaccepted"
    assert receipt["revocation_state"] == "not_accepted_so_not_release_active"
    assert receipt["platform"]["workspace"] == "isolated automation clone"
    assert receipt["debt_vector_delta"].startswith("unclassified -> H1/M3/R4")
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []

    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for relative in instance["public_merge_targets"]:
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if path.is_file():
            check_text(path)
    ast.parse((HERE / "check_intake.py").read_text(encoding="utf-8"))

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0857 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
