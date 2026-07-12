#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0474 planned intake."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0474"
ITEM_ID = "S56-M-0474-INTAKE"
RANK = 938
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
    "Statement.lean",
    "check_statement.py",
    "statement.json",
    "statement-receipt.json",
    "statement-validation.md",
    "AnchorAudit.lean",
    "anchor-audit.json",
    "check_anchor_audit.py",
    "anchor-audit-validation.md",
    "anchor-audit-receipt.json",
    "ObligationTree.lean",
    "build_obligation_artifacts.py",
    "check_obligation_tree.py",
    "obligation-registry.json",
    "typed-graphs.json",
    "validation-specs.json",
    "obligation-tree.md",
    "obligation-tree-validation.md",
    "obligation-tree-receipt.json",
    "Proof.lean",
    "check_proof.py",
    "check_proof.sh",
    "proof-validation.md",
    "proof-receipt.json",
    "Validation.lean",
    "check_validation.py",
    "validation-spec.json",
    "validation-receipt.json",
    "validation-phase.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def main() -> None:
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[_]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_claim"] is not None
    formal = instance["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0474.FermatLittleTheoremTarget"
    )
    assert formal["elaborated_expression_hash"] == (
        "sha256:5475969fd23513d3b98134a6aaa747675a32a899f38be773a23cb330f2f590e8"
    )
    assert instance["obligation_registry_hash"] == (
        "sha256:28dd518db2fe79a5006cbeb3fdd51b379f67cf388960c3f5fafdf2a7ad8b6a9e"
    )
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0474-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    intake_owned_files = OWNED_FILES - {
        "Statement.lean",
        "check_statement.py",
        "statement.json",
        "statement-receipt.json",
        "statement-validation.md",
        "AnchorAudit.lean",
        "anchor-audit.json",
        "check_anchor_audit.py",
        "anchor-audit-validation.md",
        "anchor-audit-receipt.json",
        "ObligationTree.lean",
        "build_obligation_artifacts.py",
        "check_obligation_tree.py",
        "obligation-registry.json",
        "typed-graphs.json",
        "validation-specs.json",
        "obligation-tree.md",
        "obligation-tree-validation.md",
        "obligation-tree-receipt.json",
        "Proof.lean",
        "check_proof.py",
        "check_proof.sh",
        "proof-validation.md",
        "proof-receipt.json",
        "Validation.lean",
        "check_validation.py",
        "validation-spec.json",
        "validation-receipt.json",
        "validation-phase.md",
    }
    expected_intake_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in intake_owned_files
    }
    assert set(receipt["changed_paths"]) == expected_intake_changed
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("intake invariant check: ok (THM-M-0474 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
