#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-1464 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1464"
ITEM_ID = "S56-M-1464-INTAKE"
BASE_REVISION = "2d82479e32843fd52283dcd9bb305954729c1199"
BASE_TREE = "30134b43ab41e973d2558be90371bf18d6edb259"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
    "Docs/Stage1_Blueprint_rev-5.6.md": "c289bdc0ac996ea46d5572abf6fcf668914e0628aaef117c0b7fcbfe0cab6a4d",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "a4b27794d9a08c4a1059302f4712e571d2b5489bb9e90942e5342bccfe5ab344",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/LinearAlgebra/AffineSpace/Simplex/Basic.lean": "ae1f875bd98114e03aff5f07dc3050ca54267a7b6c20b919243831ad04129414",
    "Mathlib/MeasureTheory/Integral/Bochner/Set.lean": "9f59492f94baadca56ded06a83dc2c3435fec5019725c440230a3fc94a8653ef",
    "Mathlib/Analysis/InnerProductSpace/LaxMilgram.lean": "79643570d2052a66114e0f87f7b284e2dc72f79638b3c6c962ba18300a9abc6d",
}


def reject_duplicate_keys(path: Path):
    def hook(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    return hook


def load_json(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys(path),
    )
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(relative: str, first: int, last: int) -> str:
    lines = (ROOT / relative).read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1:last]).encode()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_authorities() -> None:
    targets = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")["targets"]
    matches = [row for row in targets if row["theorem_id"] == THEOREM_ID]
    assert matches == [{
        "execution_rank": 1141,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "间断Galerkin方法",
        "category": "其他重要领域 / 数值分析",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }]

    nodes = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    matches = [node for node in nodes if node["id"] == ITEM_ID]
    assert len(matches) == 1
    item = matches[0]
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1141
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["execution_rank"] == 1141
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["source_status_untrusted"] == "已验证"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "not_a_stable_proposition" in instance["canonical_formal_target"]["gate_state"]
    for field in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert instance["canonical_formal_target"][field] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert "not yet a stable proposition" in instance["status_boundary"]
    assert "does not refute" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    assert excerpt_sha256("Docs/researches/math_theorems.md", 10686, 10691) == revisions["repository_record_excerpt_sha256"]
    assert excerpt_sha256("Docs/Stage0_Blueprint.md", 39811, 39837) == revisions["stage0_projection_excerpt_sha256"]
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


def check_catalog_and_source(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**间断Galerkin方法**") == 1
    assert "- 提出者: W.H. Reed/T.R. Hill" in catalog
    assert "- 时间: 1973" in catalog
    assert catalog.count("- 陈述: 允许间断的有限元") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1464 间断Galerkin方法" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    lead = instance["source_candidates_not_credited_as_H0"][0]
    assert lead["observed_size_bytes"] == 591992
    assert lead["observed_pdf_leaves"] == 23
    assert lead["observed_sha256"] == instance["source_revisions"]["observed_reed_hill_pdf_sha256"]
    assert instance["source_revisions"]["observed_osti_api_sha256"] == "841f59fe6c37395b5faa228492ab364c72ee9a1925374a75eaf5d65596099319"


def check_task_dag(dag: dict) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    authoritative = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    prior = ITEM_ID
    assert len(dag["tasks"]) == 6
    for layer, (task, suffix) in enumerate(zip(dag["tasks"], TASK_PHASES), start=1):
        task_id = f"S56-M-1464-{suffix}"
        source = next(node for node in authoritative if node["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [prior]
        assert task["state"] == "open" and task["layer"] == source["layer"] == layer
        assert task["phase"] == source["phase"]
        assert task["owned_paths"] == source["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["evidence_ids"] == []
        prior = task_id


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
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["source_inputs"] == {path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()}


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
    check_catalog_and_source(instance)
    check_task_dag(dag)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)
    print("intake invariant check: ok (THM-M-1464 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
