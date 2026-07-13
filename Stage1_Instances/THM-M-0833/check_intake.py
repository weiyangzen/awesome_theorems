#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0833 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0833"
ITEM_ID = "S56-M-0833-INTAKE"
BASE_REVISION = "be8701e88e791545c16a262edd1909486d5cef4b"
BASE_TREE = "78b0a751473bf6d71f453a6aad18b130268a3428"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXTERNAL_REVISION = "f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2"
EXTERNAL_TREE = "b2da69f860096cce9480f2645298a2d04587f360"
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
    "Docs/Stage1_Blueprint_rev-5.6.md": "201ff7722835a8360e3400c6f173b1e6684462b46ce5ed02e6b37ba51baf81bb",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0e2192895bfd08136cf7d965e1c9d942ff0d040568b72552bc7869c5801b41fb",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/researches/classified_theorems.md": "e63fe0cc581a1b7a70eedbb2bbcf96046d6c1bd4418cd13b41fc6de81919d9d5",
    "Docs/researches/formalization_classification.md": "5879347fb5f14df7beed1ef4f30e7702d7b33a63b0c7959963d87195ae30b648",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/Combinatorics/SimpleGraph/Coloring.lean": "42c4c6ac9c763df08f33a9fc4cf329e19908dacc630be771a547fcb583f7be56",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_authorities() -> None:
    targets = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")["targets"]
    target = next(row for row in targets if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": 1391,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "四色定理",
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

    items = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    item = next(node for node in items if node["id"] == ITEM_ID)
    assert item == {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 1391,
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


def check_catalog() -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**四色定理**") == 1
    assert "- 提出者: Appel/Haken" in catalog
    assert "- 时间: 1976" in catalog
    assert catalog.count("- 陈述: 平面图可用四种颜色着色") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0833 四色定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    classified = (ROOT / "Docs/researches/classified_theorems.md").read_text(encoding="utf-8")
    assert "### 6.1 四色定理 (Four Color Theorem)" in classified
    assert "Gonthier, G. (2008). Formal proof—the Four Color Theorem" in classified


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["execution_rank"] == 1391
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["source_status_untrusted"] == "已验证"
    assert "Provisional theorem-family scope" in instance["canonical_statement"]
    assert "exact planarity" in instance["canonical_statement"]
    formal = instance["canonical_formal_target"]
    for field in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[field] is None
    assert "blocked_source_planarity" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["root_vector_status"] == "proposed_pending_master_acceptance"
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert "No accepted state" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    assert revisions["external_fourcolor_revision"] == EXTERNAL_REVISION
    assert revisions["external_fourcolor_tree"] == EXTERNAL_TREE
    for path, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / path) == expected, f"changed authoritative input: {path}"
    assert revisions["target_manifest_sha256"] == SOURCE_HASHES["Docs/Stage1_Targets_rev-5.6.json"]
    assert revisions["authoritative_blueprint_sha256"] == SOURCE_HASHES["Docs/Stage1_Blueprint_rev-5.6.md"]
    assert revisions["execution_dag_sha256"] == SOURCE_HASHES["Docs/Stage1_Execution_DAG_rev-5.6.json"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    for path, expected in MATHLIB_HASHES.items():
        assert sha256(mathlib / path) == expected, f"changed mathlib input: {path}"
    assert set(instance["owned_artifacts"]) == OWNED_FILES


def check_task_dag(dag: dict) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    authoritative = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    previous = ITEM_ID
    assert len(dag["tasks"]) == 6
    for layer, (task, suffix) in enumerate(zip(dag["tasks"], TASK_PHASES), start=1):
        task_id = f"S56-M-0833-{suffix}"
        source = next(node for node in authoritative if node["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [previous]
        assert task["state"] == "open" and task["layer"] == source["layer"] == layer
        assert task["phase"] == source["phase"]
        assert task["owned_paths"] == source["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["evidence_ids"] == []
        previous = task_id


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
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
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()
    }
    assert set(receipt["non_self_referential_owned_artifact_sha256"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}"
        for name in OWNED_FILES - {"intake-receipt.json"}
    }
    for path, expected in receipt["non_self_referential_owned_artifact_sha256"].items():
        assert sha256(ROOT / path) == expected, f"changed owned artifact: {path}"


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
    assert packet["item_id"] == ITEM_ID
    assert packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == {
        ".stage1-worker-selftest.json",
        *{f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES},
    }
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert "No exact Lean statement or proof was tested" in packet["output_summary"]


def check_text_boundaries() -> None:
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    scope = (HERE / "scope-map.md").read_text(encoding="utf-8")
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    validation = (HERE / "validation.md").read_text(encoding="utf-8")
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert "No exact Lean statement" in readme
    assert "Explicit exclusions" in scope
    assert "hal-04034866v1" in crosswalk
    assert EXTERNAL_REVISION in crosswalk
    assert "four_color_hypermap" in crosswalk
    assert "no target theorem" in validation
    assert "do not define graph planarity" in probe
    assert "theorem " not in probe.lower()
    assert re.search(r"#check SimpleGraph\.Colorable\b", probe)

    prohibited = re.compile(r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b")
    assert not prohibited.search(probe), "prohibited Lean declaration in intake probe"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    check_authorities()
    check_catalog()
    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    check_instance(instance)
    check_task_dag(dag)
    check_receipt(receipt, dag)
    check_text_boundaries()
    if args.worker_packet is not None:
        check_worker_packet((ROOT / args.worker_packet).resolve(), receipt)
    print("check_intake: ok (THM-M-0833 planned intake; no statement or proof claim)")


if __name__ == "__main__":
    main()
