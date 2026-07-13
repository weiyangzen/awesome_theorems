#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-1463 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1463"
ITEM_ID = "S56-M-1463-INTAKE"
RANK = 1140
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
TASK_DELIVERABLES = [
    "Elaborate the exact Lean 4 target with the minimal pinned imports.",
    "Audit mathlib and external Lean 4 candidates at immutable revisions.",
    "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
    "Implement or pin/import the required proof bodies without placeholders.",
    "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "Reconcile evidence and decide the exact theorem-completion verdict.",
]
PROBE_DECLARATIONS = [
    "ContinuousLinearMap",
    "ContinuousLinearMap.opNorm_le_bound₂",
    "ContinuousLinearMap.le_opNorm₂",
    "Submodule.subtypeL",
    "Submodule.orthogonalProjection",
    "Submodule.orthogonalProjection_mem_subspace_eq_self",
    "IsCoercive",
    "IsCoercive.continuousLinearEquivOfBilin",
    "IsCoercive.continuousLinearEquivOfBilin_apply",
    "IsCoercive.unique_continuousLinearEquivOfBilin",
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


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_authorities(instance: dict) -> None:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Petrov-Galerkin方法",
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
    assert target["execution_rank"] == instance["execution_rank"]
    assert target["name"] == instance["name_zh"]
    assert target["category"] == instance["category"]

    nodes = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    scoped = sorted(
        (node for node in nodes if node["theorem_id"] == THEOREM_ID),
        key=lambda node: node["layer"],
    )
    assert len(scoped) == 7
    intake = scoped[0]
    assert intake["id"] == ITEM_ID and intake["execution_rank"] == RANK
    assert intake["phase"] == "intake" and intake["layer"] == 0
    assert intake["state"] == "[ ]" and intake["depends_on"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["execution_rank"] == RANK and instance["intake_score"] == 86
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["source_status_untrusted"] == "已验证"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "only the Petrov-Galerkin method name" in instance["statement_blocker"]
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert formal["backend"] == "lean4"
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
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0329",
        "THM-M-1462",
        "THM-M-1464",
    }

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    source_spec = (
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md'
    )
    assert git("rev-parse", source_spec) == revisions["repository_source_record_blob"]
    for path, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / path) == expected, f"changed authoritative input: {path}"
    assert revisions["target_manifest_sha256"] == SOURCE_HASHES[
        "Docs/Stage1_Targets_rev-5.6.json"
    ]
    assert revisions["authoritative_blueprint_sha256"] == SOURCE_HASHES[
        "Docs/Stage1_Blueprint_rev-5.6.md"
    ]
    assert revisions["execution_dag_sha256"] == SOURCE_HASHES[
        "Docs/Stage1_Execution_DAG_rev-5.6.json"
    ]

    catalog_lines = "\n".join(
        (ROOT / "Docs/researches/math_theorems.md")
        .read_text(encoding="utf-8")
        .splitlines()[10678:10684]
    ) + "\n"
    stage0_lines = "\n".join(
        (ROOT / "Docs/Stage0_Blueprint.md")
        .read_text(encoding="utf-8")
        .splitlines()[39783:39809]
    ) + "\n"
    assert hashlib.sha256(catalog_lines.encode()).hexdigest() == revisions[
        "repository_record_excerpt_sha256"
    ]
    assert hashlib.sha256(stage0_lines.encode()).hexdigest() == revisions[
        "stage0_projection_excerpt_sha256"
    ]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions[
        "mathlib_tree"
    ] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert revisions["bilinear_source_sha256"] == sha256(
        mathlib / "Mathlib/Analysis/Normed/Operator/Bilinear.lean"
    )
    assert revisions["projection_source_sha256"] == sha256(
        mathlib / "Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean"
    )
    assert revisions["lax_milgram_source_sha256"] == sha256(
        mathlib / "Mathlib/Analysis/InnerProductSpace/LaxMilgram.lean"
    )
    assert instance["source_candidates_not_credited"][0][
        "observed_crossref_sha256"
    ] == revisions["observed_crossref_babuska_sha256"]
    assert set(instance["owned_artifacts"]) == OWNED_FILES

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**Petrov-Galerkin方法**" in catalog
    assert "- 提出者: 众多数学家" in catalog
    assert "- 陈述: 推广的Galerkin方法" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1463 Petrov-Galerkin方法" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0


def check_task_dag(dag: dict) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == [] and dag["theorem_complete"] is False
    assert len(dag["tasks"]) == 6

    authorities = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    authorities = {
        node["id"]: node for node in authorities if node["theorem_id"] == THEOREM_ID
    }
    prior = ITEM_ID
    for layer, (task, phase, deliverable) in enumerate(
        zip(dag["tasks"], TASK_PHASES, TASK_DELIVERABLES), start=1
    ):
        expected_id = f"S56-M-1463-{phase}"
        assert task["id"] == expected_id and task["phase"] == phase.lower()
        assert task["depends_on"] == [prior]
        assert task["state"] == "open" and task["layer"] == layer
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == deliverable
        assert task["completion_gate"] == (
            "rev-5.6 node-specific receipt and master acceptance"
        )
        assert task["evidence_ids"] == []
        authority = authorities[expected_id]
        assert authority["state"] == "[ ]"
        for field in (
            "phase",
            "layer",
            "depends_on",
            "owned_paths",
            "deliverable",
            "completion_gate",
        ):
            assert task[field] == authority[field]
        prior = expected_id


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
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
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    required_recipe_keys = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "covered_declarations",
    }
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["env_allowlist"] == {} for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in recipes)
    assert recipes[0]["covered_declarations"] == []
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
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


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
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for relative, digest in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert digest == "self_referential_excluded_from_provisional_digest"
        else:
            assert digest == sha256(ROOT / relative), f"stale owned digest: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    public_prose = ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md")
    for name in public_prose:
        text = (HERE / name).read_text(encoding="utf-8")
        forbidden_public_fragments = ("/" + "home/", "." + "cron/", "theorem_complete=" + "true")
        assert all(fragment not in text for fragment in forbidden_public_fragments)
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(
        r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    check_authorities(instance)
    check_instance(instance)
    check_task_dag(dag)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-1463 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
