#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0236 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0236"
ITEM_ID = "S56-M-0236-INTAKE"
RANK = 1248
BASE_REVISION = "c6fd6dad8fcfe5fd464416cd452f50286b546978"
BASE_TREE = "5a80b61d8fa09336779f8d1453dcfe4299c9472f"
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
AUTHORITY_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "9601541c3966336c2ea27797f4ff93e3dd3d7adc4de88410cc8a6b60a7782190",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "1e2eb8e8c86ccef96bb4dcd85b33f1a06fcf76a7c54c0b51772ddc0b6cebe2c5",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Homotopy/Lifting.lean": "e47671e27a60b6e7f3699df8b2ba1a3c40bc2c939971e972c8d6acb7bfc73291",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--worker-packet",
        type=Path,
        help="optional provisional worker packet; absent after integration",
    )
    args = parser.parse_args()

    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    selftest = load(args.worker_packet) if args.worker_packet is not None else None

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)

    assert manifest["scope"]["canonical_sorted_target_id_set_sha256"] == (
        "e07deabaab3463cc1f92cdf5c0cf50ad9f8270d35554529c375d20a8512d8f1a"
    )
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    if selftest is not None:
        assert item["state"] == "[ ]", "worker base must precede provisional integration"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "candidate_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert formal["candidate_declarations"] == [
        "IsLocalHomeomorph.monodromy_theorem",
        "SimplyConnectedSpace.paths_homotopic",
        "IsCoveringMap.existsUnique_continuousMap_lifts",
    ]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert instance["source_revisions"]["repository_base"] == BASE_REVISION
    assert instance["source_revisions"]["repository_base_tree"] == BASE_TREE

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0236-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    authoritative_downstream = [
        next(row for row in execution_dag["items"] if row["id"] == task["id"])
        for task in dag["tasks"]
    ]
    for task, authority in zip(dag["tasks"], authoritative_downstream, strict=True):
        assert task["phase"] == authority["phase"]
        assert task["layer"] == authority["layer"]
        assert task["owned_paths"] == authority["owned_paths"]
        assert task["deliverable"] == authority["deliverable"]
        assert task["completion_gate"] == authority["completion_gate"]
        assert task["evidence_ids"] == []

    source = (ROOT / "Docs" / "researches" / "math_theorems.md").read_text(encoding="utf-8")
    stage0 = (ROOT / "Docs" / "Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "**单值性定理**" in source and "- 陈述: 全纯函数沿曲线的解析延拓" in source
    assert "- [ ] THM-M-0236 单值性定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["attestor"]["signature"] is None
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.fromisoformat(receipt["validated_at"])
    assert started <= ended == validated <= datetime.now().astimezone()
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"

    for relative, digest in AUTHORITY_HASHES.items():
        assert sha256(ROOT / relative) == digest, f"authority hash mismatch: {relative}"
    for name, digest in receipt["untracked_owned_artifact_sha256"].items():
        assert name != "intake-receipt.json"
        assert digest == sha256(HERE / name), f"owned artifact hash mismatch: {name}"
    assert set(receipt["untracked_owned_artifact_sha256"]) == OWNED_FILES - {"intake-receipt.json"}
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    if selftest is not None:
        assert selftest["item_id"] == ITEM_ID
        assert selftest["theorem_id"] == THEOREM_ID and selftest["intent"] == "intake"
        assert selftest["audit_complete"] is selftest["theorem_complete"] is False
        assert set(selftest["changed_paths"]) == expected_changed
        assert selftest["state"] == "[_]"
        assert receipt["base_revision"] == selftest["base_revision"]
        assert receipt["receipt_id"] == selftest["receipt_id"]
        assert selftest["accepted_receipt_ids"] == selftest["proof_body_locations"] == []

    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet)
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("intake invariant check: ok (THM-M-0236 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
