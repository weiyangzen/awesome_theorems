#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-1599 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1599"
ITEM_ID = "S56-M-1599-INTAKE"
RANK = 1219
BASE_REVISION = "62fad55ced807fdc06921c45d6fcd1f9ad86a1c2"
BASE_TREE = "9d7c8fe49a4c859d90f3069dc47973ffc5ced768"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
    "Docs/Stage1_Blueprint_rev-5.6.md": "f1c9b4df95f5a7a0e906979550df528cff599828cc9576f4afabb20386d1825f",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "f5c1dfb5eaed3928a62e529b6acdef23453d8ceac2e1f897f79d67b0a866e049",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/AlgebraicGeometry/EllipticCurve/Weierstrass.lean": "5e3a4c2282600bb96a48c950f5099dcb5a0febae318945b976a893d1a572bf22",
    "Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Point.lean": "3506899af1d461a468526a5488f5250038f68f7a5b33856a8655af3d32de77ea",
    "Mathlib/AlgebraicGeometry/EllipticCurve/Projective/Point.lean": "4c812c29538d69efffe56994e28533b3004f16f9ad6ea43688a7db81f0eeab8e",
}
EXCERPT_HASHES = {
    "catalog": "32cbeb2dc5270640b82db9032987e645bfe31e3e938376e319a9e46be3f6b289",
    "stage0": "6e8680bff0ec6515d98351fdce212fdbd1e019a3bc5ab0ce9167bdfbfd776cd3",
    "target_manifest_entry": "a546d9de6650a161a97175c931f9605da0e8ffb545fcdea9ccbdaa1eb3cfdec7",
    "execution_dag_intake_entry": "86970b6715c919d3fd4d50a69e6f315290e68540d2d2109a3c703c41b3988297",
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


def check_authorities(instance: dict) -> list[dict]:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    assert manifest["schema_version"] == "stage1-target-set/5.6.2"
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "椭圆曲线密码学",
            "category": "其他重要领域 / 离散数学",
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
    return items


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "no_stable_truth_valued_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert "not_a_stable_proposition" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "does not refute" in instance["status_boundary"]
    assert "master acceptance is claimed" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert (
        git("rev-parse", "HEAD:Docs/researches/math_theorems.md")
        == revisions["current_repository_math_source_blob"]
    )
    assert (
        git(
            "rev-parse",
            f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
        )
        == revisions["repository_source_record_blob"]
    )
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
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 11777, 11782) == EXCERPT_HASHES["catalog"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 43471, 43496) == EXCERPT_HASHES["stage0"]
    assert excerpt_sha256(ROOT / "Docs/Stage1_Targets_rev-5.6.json", 18295, 18308) == EXCERPT_HASHES["target_manifest_entry"]
    assert excerpt_sha256(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json", 151044, 151058) == EXCERPT_HASHES["execution_dag_intake_entry"]
    assert revisions["repository_record_excerpt_sha256"] == EXCERPT_HASHES["catalog"]
    assert revisions["stage0_projection_excerpt_sha256"] == EXCERPT_HASHES["stage0"]
    assert revisions["target_manifest_entry_sha256"] == EXCERPT_HASHES["target_manifest_entry"]
    assert revisions["execution_dag_intake_entry_sha256"] == EXCERPT_HASHES["execution_dag_intake_entry"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    mathlib_fields = {
        "mathlib_weierstrass_source_sha256": "Mathlib/AlgebraicGeometry/EllipticCurve/Weierstrass.lean",
        "mathlib_affine_point_source_sha256": "Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Point.lean",
        "mathlib_projective_point_source_sha256": "Mathlib/AlgebraicGeometry/EllipticCurve/Projective/Point.lean",
    }
    for field, path in mathlib_fields.items():
        assert revisions[field] == MATHLIB_HASHES[path] == sha256(mathlib / path)


def check_catalog_and_boundaries(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**椭圆曲线密码学**") == 1
    assert "- 提出者: Victor Miller/Neal Koblitz" in catalog
    assert "- 时间: 1985" in catalog
    assert catalog.count("- 陈述: 基于椭圆曲线的密码") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1599 椭圆曲线密码学" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    boundaries = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert boundaries == {"THM-M-1597", "THM-M-1598", "THM-C-0203"}


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
        task_id = f"S56-M-1599-{suffix}"
        source = next(row for row in authoritative if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["layer"] == source["layer"] == layer
        assert task["phase"] == source["phase"]
        assert task["owned_paths"] == source["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id


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
    assert receipt["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()
    }
    symlink = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        "sha256:" + hashlib.sha256(symlink).hexdigest()
    )
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_node_ids"] == [ITEM_ID] for recipe in recipes)


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
    for name in (
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
        "intake-receipt.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx)\b|^[ \t]*(axiom|constant|opaque|unsafe)[ \t]",
        re.MULTILINE,
    )
    assert prohibited.search(probe) is None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    authoritative = check_authorities(instance)
    check_instance(instance)
    check_catalog_and_boundaries(instance)
    check_task_dag(dag, authoritative)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        packet_path = args.worker_packet
        if not packet_path.is_absolute():
            packet_path = ROOT / packet_path
        check_worker_packet(packet_path, receipt)
    print("intake invariant check: ok (THM-M-1599 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
