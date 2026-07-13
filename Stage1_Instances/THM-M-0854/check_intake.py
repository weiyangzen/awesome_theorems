#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0854 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0854"
ITEM_ID = "S56-M-0854-INTAKE"
RANK = 1408
BASE_REVISION = "1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4"
BASE_TREE = "61214aa2a03c032134ddc4958b1df63df3430a85"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXTERNAL_REVISION = "c83689ab8f1abfba1f646e65dc8b131fd256b73f"
EXTERNAL_TREE = "1f6492c5aeafeec2cfe969d8afd0aad15e2bee81"
EXTERNAL_BLOB = "fe5f079d24abc6f3ceece4f9b67240022c06827a"
EXTERNAL_SHA256 = "624699fead58ca9ef346d7ed60bb68dc534508ac1ab66985e8610d5f2e41894d"
EXTERNAL_MERGE_BASE = "3bebc671e9c9c1b535ad7ce3a6f96a2263835424"
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
MATHLIB_SOURCE_FIELDS = {
    "simplegraph_hamiltonian_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Hamiltonian.lean"
    ),
    "simplegraph_finite_sha256": "Mathlib/Combinatorics/SimpleGraph/Finite.lean",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def git_bytes(*args: str, cwd: Path) -> bytes:
    return subprocess.check_output(["git", *args], cwd=cwd)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


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
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "Ore定理"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    intake = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert intake["theorem_id"] == THEOREM_ID and intake["execution_rank"] == RANK
    assert intake["phase"] == "intake" and intake["layer"] == 0
    assert intake["state"] == "[ ]" and intake["depends_on"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert intake["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert instance["source_candidates_not_credited"][1]["pdf_sha256"] == (
        "60e37541a790f905531f8fd9ff5f31deab3d6a6bc0ba7a97a56836683a66555b"
    )
    assert "source-visible body" in instance["formal_candidates_not_credited"][1]["status"]
    assert "no M1 or M0 credit" in instance["formal_candidates_not_credited"][1]["status"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_SOURCE_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    assert git("rev-parse", EXTERNAL_REVISION + "^{tree}", cwd=mathlib) == EXTERNAL_TREE
    external_path = "Mathlib/Combinatorics/SimpleGraph/BondyChvatal.lean"
    assert git("rev-parse", f"{EXTERNAL_REVISION}:{external_path}", cwd=mathlib) == EXTERNAL_BLOB
    external_bytes = git_bytes("show", f"{EXTERNAL_REVISION}:{external_path}", cwd=mathlib)
    assert hashlib.sha256(external_bytes).hexdigest() == EXTERNAL_SHA256
    external_text = external_bytes.decode("utf-8")
    assert "theorem ore_theorem" in external_text
    assert "hV : ‖V‖ ≥ 3" in external_text
    assert "G.degree u + G.degree v ≥ ‖V‖" in external_text
    assert "G.IsHamiltonian := by" in external_text
    imports = [
        line for line in external_text.splitlines() if line.startswith("import ")
    ]
    assert imports == [
        "import Mathlib.Dynamics.FixedPoints.Increasing",
        "import Mathlib.Combinatorics.SimpleGraph.Operations",
        "import Mathlib.Combinatorics.SimpleGraph.Hamiltonian",
    ]
    prohibited_external = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ", "extern ")
    assert all(token not in external_text for token in prohibited_external)
    assert git("merge-base", MATHLIB_REVISION, EXTERNAL_REVISION, cwd=mathlib) == EXTERNAL_MERGE_BASE
    assert git("rev-list", "--left-right", "--count", f"{MATHLIB_REVISION}...{EXTERNAL_REVISION}", cwd=mathlib).split() == ["16380", "79"]
    external_toolchain = git_bytes("show", f"{EXTERNAL_REVISION}:lean-toolchain", cwd=mathlib)
    assert external_toolchain == b"leanprover/lean4:v4.12.0-rc1\n"
    assert hashlib.sha256(external_toolchain).hexdigest() == revisions["external_candidate_toolchain_sha256"]

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0854-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == [] and task["state"] == "open"
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**Ore定理**" in catalog
    assert "- 提出者: Øystein Ore" in catalog
    assert "- 时间: 1960" in catalog
    assert "- 陈述: Hamilton圈存在的度和条件" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0854 Ore定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0852", "THM-M-0853", "THM-M-0855"
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["supersession_state"] == "current_unsuperseded_worker_report"
    assert receipt["revocation_state"] == "not_revoked"
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert receipt["declaration_ownership"] == []
    assert receipt["change_impact_set"] == [ITEM_ID]
    assert isinstance(receipt["diff_summary"], str) and receipt["diff_summary"]
    assert isinstance(receipt["worker_worktree_reference"], str) and receipt["worker_worktree_reference"]
    assert set(receipt["readable_ownership"]) == {
        f"Stage1_Instances/{THEOREM_ID}/README.md",
        f"Stage1_Instances/{THEOREM_ID}/scope-map.md",
        f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
        f"Stage1_Instances/{THEOREM_ID}/validation.md",
    }
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["worker_input_hashes"]["external_candidate_revision"] == EXTERNAL_REVISION
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
    recorded_argv = [entry.get("argv") for entry in receipt["commands_and_results"]]
    assert ["python3", "Docs/tools/check_stage1_standard.py"] in recorded_argv
    assert ["python3", "scripts/stage1_target.py", "check"] in recorded_argv
    assert ["python3", "scripts/stage1_target.py", "show", THEOREM_ID] in recorded_argv
    assert [
        "python3",
        "-B",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
    ] in recorded_argv
    assert any(
        entry.get("expected_no_match") is True and entry.get("exit_code") == 1
        for entry in receipt["commands_and_results"]
    )
    assert any("show-ref" in (entry.get("argv") or []) for entry in receipt["commands_and_results"])
    assert any("merge-base" in (entry.get("argv") or []) for entry in receipt["commands_and_results"])
    assert any("rev-list" in (entry.get("argv") or []) for entry in receipt["commands_and_results"])
    assert any("pipeline" in entry for entry in receipt["commands_and_results"])

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n"), f"missing final newline: {path.name}"
            assert b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in OWNED_FILES - {"IntakeProbe.lean", "check_intake.py"}:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0854 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
