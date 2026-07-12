#!/usr/bin/env python3
"""Check the fail-closed THM-M-1396 planned-intake invariants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{path} must contain a JSON object"
    return data


parser = argparse.ArgumentParser()
parser.add_argument("--worker-packet", type=Path)
args = parser.parse_args()

manifest = load(WORKSPACE / "Docs/Stage1_Targets_rev-5.6.json")
execution_dag = load(WORKSPACE / "Docs/Stage1_Execution_DAG_rev-5.6.json")
instance = load(ROOT / "instance.json")
dag = load(ROOT / "task-dag.json")
receipt = load(ROOT / "intake-receipt.json")

target = next(item for item in manifest["targets"] if item["theorem_id"] == "THM-M-1396")
item = next(item for item in execution_dag["items"] if item["id"] == "S56-M-1396-INTAKE")

artifacts = {
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
task_ids = [
    "S56-M-1396-STATEMENT",
    "S56-M-1396-ANCHOR_AUDIT",
    "S56-M-1396-OBLIGATION_TREE",
    "S56-M-1396-PROOF",
    "S56-M-1396-VALIDATION",
    "S56-M-1396-RELEASE",
]

assert manifest["schema_version"] == "stage1-target-set/5.6.2"
assert instance["schema_version"] == "stage1-instance-intake/1.0"
assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-1396"
assert instance["item_id"] == receipt["item_id"] == item["id"] == "S56-M-1396-INTAKE"

assert target["execution_rank"] == instance["execution_rank"] == item["execution_rank"] == 1006
assert target["name"] == instance["name_zh"] == "Runge-Kutta方法"
assert target["category"] == instance["category_zh"] == "微分方程 / 常微分方程"
assert target["target_lane"] == instance["target_lane"] == "hard_statement_first_partial_verification"
assert target["intake_score"] == instance["intake_score"] == 108
assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
assert instance["lifecycle"] == dag["lifecycle"] == "planned"
assert instance["intent"] == receipt["intent"] == "intake"
assert receipt["verdict"] == "no_state_change"
assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

assert item["phase"] == "intake" and item["layer"] == 0
assert item["state"] in {"[ ]", "[_]"}
assert item["depends_on"] == []
assert item["owned_paths"] == ["Stage1_Instances/THM-M-1396"]
assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
formal = instance["canonical_formal_target"]
assert formal["backend"] == "lean4"
assert all(
    formal[key] is None
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    )
)
assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
assert instance["obligation_registry_hash"] is None
assert instance["discovery_protocol_hash"] is None
assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
assert instance["accepted_proof_state"] == dag["accepted_states"] == []
assert instance["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
assert not any(
    (
        instance["audit_complete"],
        dag["audit_complete"],
        instance["theorem_complete"],
        receipt["accepted"],
        receipt["audit_complete"],
        receipt["theorem_complete"],
    )
)
assert receipt["proposed_state"] == "[_]"
assert receipt["receipt_class"] == "provisional_worker_selftest"
assert receipt["content_addressed"] is False
assert receipt["proof_body_locations"] == []
assert receipt["canonical_obligation_ids"] == []
assert receipt["statement_fingerprints"] == []
assert receipt["typed_graph_changes"] == []
assert receipt["composition_certificates"] == []
assert receipt["content_addressed_receipt_ids"] == []

assert set(instance["owned_artifacts"]) == artifacts
assert {path.name for path in ROOT.iterdir() if path.is_file()} == artifacts
assert set(instance["public_merge_targets"]) == {
    f"Stage1_Instances/THM-M-1396/{artifact}" for artifact in artifacts
}
assert all((WORKSPACE / path).is_file() for path in instance["public_merge_targets"])

assert [task["id"] for task in dag["tasks"]] == task_ids
assert all(task["state"] == "open" for task in dag["tasks"])
assert dag["tasks"][0]["depends_on"] == ["S56-M-1396-INTAKE"]
assert all(after["depends_on"] == [before["id"]] for before, after in zip(dag["tasks"], dag["tasks"][1:]))

changed_paths = {".stage1-worker-selftest.json"} | {
    f"Stage1_Instances/THM-M-1396/{artifact}" for artifact in artifacts
}
assert set(receipt["changed_paths"]) == changed_paths
assert receipt["remaining_root_cut_set"] == task_ids
assert receipt["change_impact_set"] == ["S56-M-1396-INTAKE"]
assert receipt["actual_source_ownership"] == ["Stage1_Instances/THM-M-1396"]

if args.worker_packet is not None:
    packet_path = args.worker_packet
    if not packet_path.is_absolute():
        packet_path = WORKSPACE / packet_path
    packet = load(packet_path)
    assert packet["item_id"] == "S56-M-1396-INTAKE"
    assert packet["verdict"] == receipt["verdict"] == "no_state_change"
    assert packet["state"] == receipt["proposed_state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"]
    assert set(packet["changed_paths"]) == changed_paths
    assert packet["known_failures"] == receipt["known_failures"]

prohibited = re.compile(r"\b(sorry|admit|sorryAx)\b|^[ \t]*(axiom|constant|opaque|unsafe)[ \t]", re.MULTILINE)
assert prohibited.search((ROOT / "IntakeProbe.lean").read_text(encoding="utf-8")) is None

for path in ROOT.iterdir():
    if not path.is_file():
        continue
    raw = path.read_bytes()
    assert raw.endswith(b"\n"), f"{path.name} lacks final newline"
    text = raw.decode("utf-8")
    assert not any(line.endswith((" ", "\t")) for line in text.splitlines()), f"trailing whitespace: {path.name}"
    if path.suffix in {".md", ".json"}:
        assert "/home/" not in text and "/.cron/" not in text, f"private absolute path: {path.name}"

print("intake invariant check: ok (THM-M-1396 planned; H5/M4/R4; six open tasks)")
