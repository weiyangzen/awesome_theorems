#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0889 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0889"
ITEM_ID = "S56-M-0889-INTAKE"
RANK = 1439
BASE_REVISION = "0c019b7194c9c43fa5f683fa82d637a0b275410d"
BASE_TREE = "43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
PRIMARY_PDF_SHA256 = "5942686400daeac3383624c285ae24d795f39de838726d5fa24c231a4e3fe868"
LEAN_OUTPUT_SHA256 = "0521ebbf5bcf2117e7160a635dce98b3e36cc21da3fa567d8cbd2770e127b835"
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
SOURCE_HASH_FIELDS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "applicable_targets_sha256": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_HASH_FIELDS = {
    "mathlib_simple_graph_basic_sha256": "Mathlib/Combinatorics/SimpleGraph/Basic.lean",
    "mathlib_simple_graph_finite_sha256": "Mathlib/Combinatorics/SimpleGraph/Finite.lean",
    "mathlib_simple_graph_adj_matrix_sha256": "Mathlib/Combinatorics/SimpleGraph/AdjMatrix.lean",
    "mathlib_simple_graph_lap_matrix_sha256": "Mathlib/Combinatorics/SimpleGraph/LapMatrix.lean",
    "mathlib_matrix_spectrum_sha256": "Mathlib/Analysis/Matrix/Spectrum.lean",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1:last])).hexdigest()


def run_lean_probe() -> bytes:
    result = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0889/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout.decode(errors="replace")
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
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Alon-Milman定理",
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
    for field in (
        "execution_rank", "legacy_priority_slot", "baseline", "rework_required",
        "legacy_artifacts_accepted", "target_lane", "intake_score",
        "source_status_untrusted", "lifecycle_mode", "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]

    intake = next(row for row in execution["items"] if row["id"] == ITEM_ID)
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

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    assert "result_family_identified" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in (
        "module", "declaration_or_expression", "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False
    assert "No canonical statement, H0, M0, R0" in instance["status_boundary"]

    source = instance["primary_source_candidates_not_credited"][0]
    assert source["doi"] == "10.1016/0095-8956(85)90092-9"
    assert source["author_hosted_pdf_sha256"] == PRIMARY_PDF_SHA256
    assert any("Theorem 4.3" in locator for locator in source["candidate_locators"])

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 6509, 6514
    )
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 24251, 24276
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", "--untracked-files=all", cwd=mathlib)
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert revisions["lake_symlink_target_string_sha256"] == hashlib.sha256(lake_target).hexdigest()

    dependency = ITEM_ID
    assert len(dag["tasks"]) == 6
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0889-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = dag["tasks"][layer - 1]
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    catalog_record = "\n".join(catalog.splitlines()[6508:6514])
    for literal in (
        "**Alon-Milman定理**",
        "- 提出者: Noga Alon/Vitali Milman",
        "- 时间: 1985",
        "- 陈述: 谱隙与扩展性",
    ):
        assert literal in catalog_record
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0889 Alon-Milman定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0881", "THM-M-0887", "THM-M-0888"
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert all((ROOT / path).is_file() for path in instance["public_merge_targets"])
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["content_addressed"] is False
    for key in (
        "accepted_receipt_ids", "proof_body_locations", "canonical_obligation_ids",
        "statement_fingerprints", "typed_graph_changes", "composition_certificates",
        "content_addressed_recipe_ids", "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["selftest_result"] == "pass"
    assert [action["exit_code"] for action in receipt["validation_actions"]] == [0, 0]
    expected_structure_output = (
        b"intake invariant check: ok (THM-M-0889 planned; H1/M4/R4; six open tasks)\n"
    )
    assert receipt["validation_actions"][0]["stdout_sha256"] == hashlib.sha256(
        expected_structure_output
    ).hexdigest()
    assert receipt["validation_actions"][1]["stdout_sha256"] == LEAN_OUTPUT_SHA256
    assert hashlib.sha256(run_lean_probe()).hexdigest() == LEAN_OUTPUT_SHA256
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"

    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n"), f"missing final newline: {path.name}"
            assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
                f"trailing whitespace: {path.name}"
            )
    for name in (
        "README.md", "instance.json", "scope-map.md", "source-statement-crosswalk.md",
        "task-dag.json", "validation.md", "intake-receipt.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0889 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
