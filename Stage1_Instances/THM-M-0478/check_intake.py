#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0478 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0478"
ITEM_ID = "S56-M-0478-INTAKE"
RANK = 1359
BASE_REVISION = "0f70149d61a952d44f907f4662a143372bcb4c44"
BASE_TREE = "35328e4f56f47446a4e1dfdbe361a1b70a4b18a7"
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
    "Docs/Stage1_Blueprint_rev-5.6.md": "4ab62ab0dcbdc6a10fb319b112be7dce0d425b636bfcb82f548ec241203981c0",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "5b582a1621e8fb8aa1c16fc98fd053e1d50fa6f2b43d28c677ad7a2c890f265c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/NumberTheory/LegendreSymbol/QuadraticReciprocity.lean": (
        "24ffbf256f6f6f7a2617901323c2d532e2d7871c826a8b11f0580b283e994302"
    ),
    "Mathlib/NumberTheory/LegendreSymbol/Basic.lean": (
        "54d109c9c6d6d5d94b2be7622f9589c78fb7cb80b869235df07dd651799da92e"
    ),
}
EXCERPT_HASHES = {
    "catalog": "997c9f44d9f01db0f23c9fced1b134783a6e173f85b81b8932b4af061132df20",
    "stage0": "e2025caf809fa837dddf1abdcf2410bd51374755eb5c17bf6b39d72a688a1b03",
    "target_manifest_entry": "6cef9eb6ed10f956e5814384edee51389fa8d429523b4759610b359764823eec",
    "execution_dag_intake_entry": "6db1177a3785f0ce1e7214912a08b1c3b5ba2051062f00d0b28e8d7b36685912",
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


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def path_bytes_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def run_recorded_action(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    cwd = ROOT / recipe["cwd"]
    completed = subprocess.run(
        recipe["argv"],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert completed.returncode == recipe["expected_exit"], completed.stdout.decode(
        errors="replace"
    )
    return completed.stdout


def check_authorities(instance: dict) -> list[dict]:
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "二次互反律",
            "category": "数论 / 初等数论",
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

    items = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
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
    assert instance["canonical_formal_target"]["declaration_or_expression"] is None
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] is None
    assert instance["canonical_formal_target"]["environment_fingerprint"] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []

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
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 3511, 3516) == (
        EXCERPT_HASHES["catalog"]
    )
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 13109, 13134) == (
        EXCERPT_HASHES["stage0"]
    )
    assert excerpt_sha256(ROOT / "Docs/Stage1_Targets_rev-5.6.json", 20395, 20408) == (
        EXCERPT_HASHES["target_manifest_entry"]
    )
    assert excerpt_sha256(
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json", 168405, 168419
    ) == EXCERPT_HASHES["execution_dag_intake_entry"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    fields = {
        "mathlib_quadratic_reciprocity_source_sha256": (
            "Mathlib/NumberTheory/LegendreSymbol/QuadraticReciprocity.lean"
        ),
        "mathlib_legendre_basic_source_sha256": (
            "Mathlib/NumberTheory/LegendreSymbol/Basic.lean"
        ),
    }
    for field, path in fields.items():
        assert revisions[field] == MATHLIB_HASHES[path] == sha256(mathlib / path)


def check_catalog_and_prose(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**二次互反律**") == 1
    assert "- 提出者: Carl Friedrich Gauss" in catalog
    assert "- 时间: 1796" in catalog
    assert catalog.count("- 陈述: 勒让德符号的互反性质") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0478 二次互反律" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    boundaries = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert boundaries == {"THM-M-0476", "THM-M-0477", "THM-M-0479"}

    combined = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md")
    )
    for token in (
        "p = 2",
        "q = 2",
        "p = q",
        "quadratic_reciprocity",
        "M3",
        "H1",
        "R4",
        "M0-W",
        "Jacobi",
        "master acceptance",
    ):
        assert token in combined


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
        task_id = f"S56-M-0478-{suffix}"
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
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
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
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()
    }
    symlink = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert receipt["worker_input_hashes"]["lake_symlink_target_sha256"] == (
        "sha256:" + hashlib.sha256(symlink).hexdigest()
    )
    artifacts = receipt["owned_artifact_sha256"]
    for name in OWNED_FILES - {"intake-receipt.json"}:
        path = HERE / name
        assert artifacts[path.relative_to(ROOT).as_posix()] == sha256(path)
    assert artifacts[f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"] == (
        "self_referential_excluded_from_provisional_digest"
    )
    hashed_paths = [
        HERE / name
        for name in sorted(OWNED_FILES - {"intake-receipt.json", "validation.md"})
    ]
    # validation.md is finalized after the receipt; its individual digest is still checked above.
    assert receipt["dirty_input_evidence"]["owned_untracked_patch_sha256"] == (
        path_bytes_hash(hashed_paths)
    )
    assert receipt["dirty_input_evidence"]["owned_untracked_manifest_sha256"] == (
        path_manifest_hash(hashed_paths)
    )
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == [
        row["command"] for row in receipt["commands_and_results"]
    ]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"].startswith("PASS:")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()

    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    authoritative = check_authorities(instance)
    check_instance(instance)
    check_catalog_and_prose(instance)
    check_task_dag(dag, authoritative)
    check_receipt(receipt, dag)

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for declaration in (
        "legendreSym",
        "legendreSym.quadratic_reciprocity",
        "legendreSym.quadratic_reciprocity'",
        "legendreSym.quadratic_reciprocity_one_mod_four",
        "legendreSym.quadratic_reciprocity_three_mod_four",
        "ZMod.exists_sq_eq_prime_iff_of_mod_four_eq_one",
        "ZMod.exists_sq_eq_prime_iff_of_mod_four_eq_three",
    ):
        assert declaration in probe
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    assert prohibited.search(probe) is None

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    if args.replay:
        for recipe in receipt["structured_validation_recipes"]:
            output = run_recorded_action(recipe)
            action = next(
                row
                for row in receipt["validation_actions"]
                if row["recipe_id"] == recipe["recipe_id"]
            )
            assert hashlib.sha256(output).hexdigest() == action["stdout_sha256"]

    print("intake invariant check: ok (THM-M-0478 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
