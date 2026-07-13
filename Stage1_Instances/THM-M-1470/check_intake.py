#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-1470 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1470"
ITEM_ID = "S56-M-1470-INTAKE"
RANK = 1147
BASE_REVISION = "521bd42e5ab5e30513a3c2b7377ea4a1516c0d16"
BASE_TREE = "6f3d9fcf297fe5251a1dc839c1e67930001a86fc"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_EXCERPT_SHA256 = "b4073f9a91ac7afb5a432350a1623eaffba8301d8133c45df1dfe349bf9e1b56"
STAGE0_EXCERPT_SHA256 = "9702ee3d854fd714b68d642c6341cec300921585f2ad12ffd5fdd841eb6afd30"
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
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
TASK_DELIVERABLES = (
    "Elaborate the exact Lean 4 target with the minimal pinned imports.",
    "Audit mathlib and external Lean 4 candidates at immutable revisions.",
    "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
    "Implement or pin/import the required proof bodies without placeholders.",
    "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "Reconcile evidence and decide the exact theorem-completion verdict.",
)
PROBE_DECLARATIONS = [
    "IsCoercive.bounded_below",
    "IsCoercive.continuousLinearEquivOfBilin",
    "IsCoercive.continuousLinearEquivOfBilin_apply",
    "Submodule.starProjection_inner_eq_zero",
    "Submodule.starProjection_minimal",
    "ContractingWith.aposteriori_dist_iterate_fixedPoint_le",
]
SOURCE_HASH_FIELDS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    "lakefile_sha256": "Formalizations/Lean/lakefile.lean",
}
MATHLIB_HASH_FIELDS = {
    "lax_milgram_source_sha256": "Mathlib/Analysis/InnerProductSpace/LaxMilgram.lean",
    "projection_basic_source_sha256": (
        "Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean"
    ),
    "contracting_source_sha256": "Mathlib/Topology/MetricSpace/Contracting.lean",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode()).hexdigest()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def run_recorded_recipe(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"]
    return result.stdout


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
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
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def check_authorities(instance: dict, dag: dict) -> None:
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "后验误差估计",
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
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"]

    nodes = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
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
    assert "only an a posteriori error-estimation label" in instance["statement_blocker"]
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
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
        "THM-M-1461",
        "THM-M-1462",
        "THM-M-1469",
        "THM-M-1471",
    }

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 10728, 10733
    ) == revisions["repository_record_excerpt_sha256"] == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 39973, 39998
    ) == revisions["stage0_projection_excerpt_sha256"] == STAGE0_EXCERPT_SHA256
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions[
        "mathlib_tree"
    ] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    source = instance["source_candidates_not_credited"][0]
    assert source["observed_crossref_sha256"] == revisions[
        "observed_crossref_metadata_sha256"
    ]
    assert source["observed_publisher_page_sha256"] == revisions[
        "observed_publisher_page_sha256"
    ]

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    for literal in (
        "**后验误差估计**",
        "- 提出者: Ivo Babuška",
        "- 时间: 1971",
        "- 陈述: 数值解的误差估计",
    ):
        assert literal in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1470 后验误差估计" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0


def check_task_dag(dag: dict) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == [] and dag["theorem_complete"] is False
    assert len(dag["tasks"]) == 6

    authorities = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    authorities = {
        node["id"]: node for node in authorities if node["theorem_id"] == THEOREM_ID
    }
    prior = ITEM_ID
    for layer, (task, suffix, deliverable) in enumerate(
        zip(dag["tasks"], TASK_SUFFIXES, TASK_DELIVERABLES), start=1
    ):
        expected_id = f"S56-M-1470-{suffix}"
        assert task["id"] == expected_id and task["phase"] == suffix.lower()
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
    assert receipt["dirty_input_evidence"]["preexisting_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    actions = receipt["validation_actions"]
    assert len(actions) == 2
    for action in actions:
        recipe = recipes_by_id[action["recipe_id"]]
        identity = {
            key: recipe[key]
            for key in (
                "cwd",
                "argv",
                "env_allowlist",
                "timeout_seconds",
                "network_policy",
                "expected_exit",
            )
        }
        assert action["recipe_sha256"] == canonical_json_sha256(identity)
        assert action["exit_code"] == 0
        assert action["covered_obligation_ids"] == [ITEM_ID]
        for field in ("recipe_sha256", "input_manifest_sha256", "stdout_sha256"):
            assert re.fullmatch(r"[0-9a-f]{64}", action[field])
        assert recipe["expected_outputs"] == [
            {
                "path_or_stream": "stdout",
                "semantic_hash_policy": f'exact bytes SHA-256 {action["stdout_sha256"]}',
            }
        ]

    lean_recipe = recipes_by_id["S56-M-1470-INTAKE-RECIPE-LEAN-PROBE"]
    assert lean_recipe["covered_declarations"] == PROBE_DECLARATIONS
    lean_stdout = run_recorded_recipe(lean_recipe)
    lean_action = next(
        action for action in actions if action["recipe_id"] == lean_recipe["recipe_id"]
    )
    assert lean_action["stdout_sha256"] == hashlib.sha256(lean_stdout).hexdigest()

    structure_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
        HERE / "check_intake.py",
    ]
    structure_action = next(
        action for action in actions if action["recipe_id"].endswith("STRUCTURE")
    )
    assert structure_action["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    expected_structure_stdout = (
        b"intake invariant check: ok (THM-M-1470 planned; H5/M4/R4; six open tasks)\n"
    )
    assert structure_action["stdout_sha256"] == hashlib.sha256(
        expected_structure_stdout
    ).hexdigest()
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        HERE / "IntakeProbe.lean",
    ]
    assert lean_action["input_manifest_sha256"] == path_manifest_hash(lean_inputs)


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES, f"unexpected owned artifact inventory: {sorted(actual)}"
    assert set(instance["owned_artifacts"]) == OWNED_FILES
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
    public_prose = (
        "README.md",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "validation.md",
    )
    for name in public_prose:
        text = (HERE / name).read_text(encoding="utf-8")
        forbidden = ("/home/", ".cron/", "theorem_complete=true")
        assert all(fragment not in text for fragment in forbidden)
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(
        r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    check_authorities(instance, dag)
    check_instance(instance)
    check_task_dag(dag)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-1470 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
