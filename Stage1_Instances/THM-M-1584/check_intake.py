#!/usr/bin/env python3
"""Fail-closed structural replay for the THM-M-1584 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances" / "THM-M-1584"
BASE_REVISION = "62fad55ced807fdc06921c45d6fcd1f9ad86a1c2"
BASE_TREE = "9d7c8fe49a4c859d90f3069dc47973ffc5ced768"
EXPECTED_ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
EXPECTED_TASKS = [
    ("S56-M-1584-STATEMENT", "statement", 1, ["S56-M-1584-INTAKE"]),
    ("S56-M-1584-ANCHOR_AUDIT", "anchor_audit", 2, ["S56-M-1584-STATEMENT"]),
    ("S56-M-1584-OBLIGATION_TREE", "obligation_tree", 3, ["S56-M-1584-ANCHOR_AUDIT"]),
    ("S56-M-1584-PROOF", "proof", 4, ["S56-M-1584-OBLIGATION_TREE"]),
    ("S56-M-1584-VALIDATION", "validation", 5, ["S56-M-1584-PROOF"]),
    ("S56-M-1584-RELEASE", "release", 6, ["S56-M-1584-VALIDATION"]),
]
EXPECTED_ARTIFACTS = {
    "README.md",
    "instance.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "IntakeProbe.lean",
    "check_intake.py",
    "validation.md",
    "intake-receipt.json",
    "statement-blocker.md",
    "statement-blocker.json",
}
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "f1c9b4df95f5a7a0e906979550df528cff599828cc9576f4afabb20386d1825f",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "f5c1dfb5eaed3928a62e529b6acdef23453d8ceac2e1f897f79d67b0a866e049",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean": "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/PartrecCode.lean": "543fdfc34bbc62e0d2bdff524be58e58abdd4ebded0ca25fac7edf791aadb2df",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/InformationTheory/Coding/KraftMcMillan.lean": "14fdf0a116728f6f4acc5c95ec44b796473a6a3a41d525628e5b80acb179f210",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/InformationTheory/Coding/UniquelyDecodable.lean": "1d77f6aaa753df530e96edf4819026a453d32ae6fc473ac307ea722c26a6c807",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    assert isinstance(value, dict), f"expected JSON object: {path}"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == "THM-M-1584"
    assert instance["item_id"] == "S56-M-1584-INTAKE"
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["execution_rank"] == 1206
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["source_status_untrusted"] == "已验证"
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    assert formal["module"] is None
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is None
    assert formal["environment_fingerprint"] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == EXPECTED_ROOT_VECTOR
    assert instance["audit_complete"] is False
    assert instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert set(instance["owned_artifacts"]) == EXPECTED_ARTIFACTS
    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert revisions["mathlib"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    assert revisions["mathlib_tree"] == "bdc39a3123201dae413a9d9be56ec242c19e5c2b"


def check_task_dag(dag: dict) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["theorem_id"] == "THM-M-1584"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["theorem_complete"] is False
    assert dag["accepted_states"] == []
    tasks = dag["tasks"]
    assert len(tasks) == len(EXPECTED_TASKS)
    for task, (task_id, phase, layer, deps) in zip(tasks, EXPECTED_TASKS, strict=True):
        assert task["id"] == task_id
        assert task["phase"] == phase and task["layer"] == layer
        assert task["depends_on"] == deps
        assert task["state"] == "open"
        assert task["authoritative_state"] == "[ ]"
        assert task["owned_paths"] == ["Stage1_Instances/THM-M-1584"]
        assert task["evidence_ids"] == []
    assert dag["open_root_cut_set"] == [entry[0] for entry in EXPECTED_TASKS]


def check_blocker(blocker: dict) -> None:
    assert blocker["theorem_id"] == "THM-M-1584"
    assert blocker["blocked_item_id"] == "S56-M-1584-STATEMENT"
    assert blocker["state"] == "open"
    assert blocker["canonical_statement"] is None
    assert blocker["canonical_formal_target"] is None
    assert blocker["required_decisions"]
    assert blocker["retry_condition"]


def check_receipt(receipt: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == "S56-M-1584-INTAKE"
    assert receipt["theorem_id"] == "THM-M-1584"
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["root_vector_after"] == EXPECTED_ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["statement_fingerprints"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    expected_changed = {f"Stage1_Instances/THM-M-1584/{name}" for name in EXPECTED_ARTIFACTS}
    expected_changed.add(".stage1-worker-selftest.json")
    assert set(receipt["changed_paths"]) == expected_changed
    for relative, expected in SOURCE_HASHES.items():
        assert receipt["source_inputs"][relative] == f"sha256:{expected}"
    raw_hashes = receipt["dirty_input_evidence"]["untracked_input_hashes"]
    expected_raw_paths = expected_changed - {
        "Stage1_Instances/THM-M-1584/intake-receipt.json"
    }
    assert set(raw_hashes) == expected_raw_paths
    for relative in expected_raw_paths:
        assert raw_hashes[relative] == f"sha256:{sha256(ROOT / relative)}"


def check_worker_packet(packet_path: Path, receipt: dict) -> None:
    packet = load_json(packet_path)
    assert packet["item_id"] == "S56-M-1584-INTAKE"
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"]
    assert packet["commands"]
    assert packet["output_summary"]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    assert DOSSIER.is_dir(), "missing theorem dossier"
    actual_artifacts = {path.name for path in DOSSIER.iterdir() if path.is_file()}
    assert actual_artifacts == EXPECTED_ARTIFACTS, (
        f"artifact inventory mismatch: {sorted(actual_artifacts ^ EXPECTED_ARTIFACTS)}"
    )
    for relative, expected in SOURCE_HASHES.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"source hash drift: {relative}: {actual} != {expected}"

    instance = load_json(DOSSIER / "instance.json")
    dag = load_json(DOSSIER / "task-dag.json")
    blocker = load_json(DOSSIER / "statement-blocker.json")
    receipt = load_json(DOSSIER / "intake-receipt.json")
    check_instance(instance)
    check_task_dag(dag)
    check_blocker(blocker)
    check_receipt(receipt)
    if args.worker_packet is not None:
        packet_path = args.worker_packet
        if not packet_path.is_absolute():
            packet_path = ROOT / packet_path
        check_worker_packet(packet_path.resolve(), receipt)

    print("intake invariant check: ok (THM-M-1584 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
