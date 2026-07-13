#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-1445 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1445"
ITEM_ID = "S56-M-1445-INTAKE"
BASE_REVISION = "b4e1220a37cc10a96534cfd411e3b29523d7fd81"
BASE_TREE = "a67dd08a83c396119f4762e0ff109cd0df43ee60"
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
TASK_PHASES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
]
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "4c9b425b87ebb98c488fa5bb237018a16d9dc04757c89d2012f5e93d6e546c2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0f1a74af1e415166719dd8c440a31fa96428b549f761156eaefe185c54c171e6",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_authorities() -> None:
    targets = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")["targets"]
    target = next(row for row in targets if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": 1122,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "高斯消元法",
        "category": "其他重要领域 / 数值分析",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }

    nodes = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    item = next(node for node in nodes if node["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["execution_rank"] == 1122
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["source_status_untrusted"] == "已验证"
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    target = instance["canonical_formal_target"]
    for field in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert target[field] is None
    assert target["backend"] == "lean4"
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert "not yet a stable proposition" in instance["status_boundary"]
    assert "does not refute" in instance["status_boundary"]
    assert instance["source_revisions"]["repository_base"] == BASE_REVISION
    assert instance["source_revisions"]["repository_base_tree"] == BASE_TREE
    for path, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / path) == expected, f"changed authoritative input: {path}"
    assert instance["source_revisions"]["target_manifest_sha256"] == SOURCE_HASHES["Docs/Stage1_Targets_rev-5.6.json"]
    assert instance["source_revisions"]["authoritative_blueprint_sha256"] == SOURCE_HASHES["Docs/Stage1_Blueprint_rev-5.6.md"]
    assert instance["source_revisions"]["execution_dag_sha256"] == SOURCE_HASHES["Docs/Stage1_Execution_DAG_rev-5.6.json"]
    assert instance["source_revisions"]["mathlib"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    assert instance["source_revisions"]["mathlib_tree"] == "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
    assert set(instance["owned_artifacts"]) == OWNED_FILES


def check_task_dag(dag: dict) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == [] and dag["theorem_complete"] is False
    tasks = dag["tasks"]
    assert len(tasks) == 6
    prior = ITEM_ID
    for layer, (task, phase) in enumerate(zip(tasks, TASK_PHASES), start=1):
        expected_id = f"S56-M-1445-{phase}"
        assert task["id"] == expected_id
        assert task["depends_on"] == [prior]
        assert task["state"] == "open" and task["layer"] == layer
        assert task["phase"] == phase.lower()
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["evidence_ids"] == []
        prior = expected_id


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["acceptance_authority"] == "integration lane"
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
    assert receipt["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path)
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
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] and packet["known_failures"]


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES, f"unexpected owned artifact inventory: {sorted(actual)}"
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
    check_authorities()
    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    check_instance(instance)
    check_task_dag(dag)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)
    print("intake invariant check: ok (THM-M-1445 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
