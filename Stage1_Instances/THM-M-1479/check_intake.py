#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-1479 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1479"
ITEM_ID = "S56-M-1479-INTAKE"
RANK = 1156
BASE_REVISION = "fc0de001c634823043636f9380a991c027e42533"
BASE_TREE = "b2e4d058036a1e9ec56bfc6aa5de3b015efe6330"
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
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "8f8ad011d265e037711a992796d91ddb35e4cf56efeab858b66c8626784a92cf",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "a2f71a31ac21f7a74beee1fda20aa07f6cca3a799d38d1d8faf3cb81b6c887f3",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/researches/physics_theorems.md": "6abf9da63cf075b0c6a05f3a245838ec0d7848fe873c43f529a7e0ee72cf94fa",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/Probability/StrongLaw.lean": "b74c93434df44eb75b2567f43a58b9e0353138660ad07b99263d8019bcf4f1c6",
    "Mathlib/Probability/Moments/Variance.lean": "920c022075149257307335beccbc8a62c7360fb3d9d73571b8240093dc2d72f0",
}
EXCERPT_HASHES = {
    "catalog": "9ef1798572d0dcf31fc6fa16b6584bf77e8b48ac45b87a391b87987129720a7a",
    "stage0": "20b462b40a4798eed77d1d516881cd25612b48e099ba32b6b18f6153e990c737",
    "math_neighbors": "e8df98b3ab88dddb2a46784c6b91ea396e5503b97cefe17e826490e743b806cb",
    "physics_neighbor": "d157dfa829b2c57e072d9575b6ed3a2ce2ed9272955f8125b4f7fba3f0c4f530",
}
PROBE_DECLARATIONS = [
    "MeasureTheory.Integrable",
    "ProbabilityTheory.IndepFun",
    "ProbabilityTheory.IdentDistrib",
    "ProbabilityTheory.variance",
    "ProbabilityTheory.IndepFun.variance_sum",
    "ProbabilityTheory.meas_ge_le_variance_div_sq",
    "ProbabilityTheory.strong_law_ae_real",
    "ProbabilityTheory.strong_law_ae",
]


def load_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
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
    assert manifest["scope"]["covered_targets"] == 1546
    assert manifest["scope"]["canonical_sorted_target_id_set_sha256"] == (
        "e07deabaab3463cc1f92cdf5c0cf50ad9f8270d35554529c375d20a8512d8f1a"
    )
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "Monte Carlo方法",
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
    assert "do_not_select_one_stable_truth_valued_proposition" in instance[
        "canonical_claim_status"
    ]
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
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
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "does not refute" in instance["status_boundary"]
    assert "No canonical mathematical or Lean statement" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/researches/physics_theorems.md") == revisions[
        "current_repository_physics_source_blob"
    ]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
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
    assert revisions["repository_physics_source_sha256"] == SOURCE_HASHES[
        "Docs/researches/physics_theorems.md"
    ]
    assert (
        excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 10791, 10796)
        == revisions["repository_record_excerpt_sha256"]
        == EXCERPT_HASHES["catalog"]
    )
    assert (
        excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 40216, 40241)
        == revisions["stage0_projection_excerpt_sha256"]
        == EXCERPT_HASHES["stage0"]
    )
    assert (
        excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 10791, 10803)
        == revisions["math_neighbor_excerpt_sha256"]
        == EXCERPT_HASHES["math_neighbors"]
    )
    assert (
        excerpt_sha256(ROOT / "Docs/researches/physics_theorems.md", 955, 961)
        == revisions["physics_neighbor_excerpt_sha256"]
        == EXCERPT_HASHES["physics_neighbor"]
    )
    target = next(
        row
        for row in load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")["targets"]
        if row["theorem_id"] == THEOREM_ID
    )
    target_bytes = (json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    assert hashlib.sha256(target_bytes).hexdigest() == revisions["manifest_entry_sha256"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions[
        "mathlib_tree"
    ] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for path, expected in MATHLIB_HASHES.items():
        assert sha256(mathlib / path) == expected, f"changed mathlib input: {path}"


def check_catalog_and_boundaries(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Monte Carlo方法**") == 1
    assert catalog.count("- 陈述: 基于随机采样的数值方法") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1479 Monte Carlo方法" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    physics = (ROOT / "Docs/researches/physics_theorems.md").read_text(encoding="utf-8")
    assert "**8. 蒙特卡洛方法**" in physics
    assert "- **提出者**: Metropolis/Ulam" in physics
    assert "- **陈述**: 统计力学的随机采样方法" in physics
    boundaries = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert boundaries == {
        "THM-M-0983..THM-M-0987",
        "THM-M-1100..THM-M-1103",
        "THM-M-1480",
        "THM-M-1481",
        "THM-P-0108",
    }


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
        task_id = f"S56-M-1479-{suffix}"
        source = next(row for row in authoritative if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["layer"] == source["layer"] == layer
        assert task["phase"] == source["phase"]
        assert task["owned_paths"] == source["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
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
    assert receipt["first_failed_gate"] == (
        "master acceptance of the provisional self-tested intake receipt"
    )
    assert "canonical statement identity" in receipt["first_failed_theorem_gate"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["dirty_input_evidence"]["preflight_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    lake_target_hash = hashlib.sha256(str(lake.readlink()).encode()).hexdigest()
    assert lake_target_hash == receipt["worker_input_hashes"][
        "lake_symlink_target_string_sha256"
    ]
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in recipes)
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
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


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
        whitespace = subprocess.run(
            ["git", "diff", "--no-index", "--check", "/dev/null", str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert whitespace.returncode in (0, 1), f"no-index check failed: {path.name}"
        assert not whitespace.stdout and not whitespace.stderr, (
            f"no-index whitespace diagnostic: {path.name}"
        )
    for name in OWNED_FILES - {"IntakeProbe.lean", "check_intake.py"}:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)


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
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-1479 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
