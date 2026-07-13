#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0293."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0293"
ITEM_ID = "S56-M-0293-INTAKE"
RANK = 1543
BASE_REVISION = "72e9e8092182121a6794921f61fcc9cae22f726d"
BASE_TREE = "0d6c1fdf06d1573c256af331c6b198e5a787af43"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SUCCESS = "intake invariant check: ok (THM-M-0293 planned; H1/M3/R4; six open tasks)\n"
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
TASK_SUFFIXES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
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
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def excerpt_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    check_text_file(path.resolve())
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
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument("--skip-probe-replay", action="store_true")
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(targets) == 1 and len(items) == 7
    target = targets[0]
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "赫维茨定理"
    assert target["category"] == instance["category"] == "分析学 / 实分析"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 78
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    intake_item = next(row for row in items if row["id"] == ITEM_ID)
    assert intake_item["phase"] == "intake" and intake_item["layer"] == 0
    assert intake_item["state"] in {"[ ]", "[_]"} and intake_item["depends_on"] == []
    if args.worker_packet is not None:
        assert intake_item["state"] == "[ ]", "worker base must precede provisional integration"
        assert git("rev-parse", "HEAD") == BASE_REVISION
    else:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert intake_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert intake_item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "absolute_coefficient_product_series" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    assert git("rev-parse", f"{BASE_REVISION}:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", f"{BASE_REVISION}:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 2104, 2109)
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 8089, 8114)
    assert revisions["manifest_entry_sha256"] == excerpt_sha256(ROOT / "Docs/Stage1_Targets_rev-5.6.json", 23155, 23169)
    assert revisions["execution_dag_target_entries_sha256"] == excerpt_sha256(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json", 191221, 191343)
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert revisions["mathlib_addcircle_source_sha256"] == sha256(
        mathlib / "Mathlib/Analysis/Fourier/AddCircle.lean"
    )

    target_by_id = {row["theorem_id"]: row for row in manifest["targets"]}
    neighbor_ids = [row["theorem_id"] for row in instance["neighbor_target_boundaries"]]
    assert len(neighbor_ids) == len(set(neighbor_ids))
    for neighbor in instance["neighbor_target_boundaries"]:
        assert target_by_id[neighbor["theorem_id"]]["name"] == neighbor["name"]

    authoritative = {row["id"]: row for row in items}
    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0293-{suffix}"
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        auth = authoritative[task_id]
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == auth["phase"] and task["layer"] == auth["layer"] == layer
        assert task["owned_paths"] == auth["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == auth["deliverable"]
        assert task["completion_gate"] == auth["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    for marker in ("**赫维茨定理**", "- 提出者: Adolf Hurwitz", "- 陈述: 傅里叶级数的绝对收敛"):
        assert marker in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0293 赫维茨定理" in stage0
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    for marker in ("10.1007/BF01445179", "pp. 438-439", "Sturm-Hurwitz", "H1", "M3"):
        assert marker in crosswalk

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected_hash in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected_hash == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected_hash, f"stale owned hash: {relative}"

    expected_sources = {
        relative: f"sha256:{revisions[field]}" for field, relative in SOURCE_HASH_FIELDS.items()
    }
    assert receipt["source_inputs"] == expected_sources
    worker = receipt["worker_input_hashes"]
    lake = ROOT / "Formalizations/Lean/.lake"
    expected_symlink = hashlib.sha256(str(lake.readlink()).encode()).hexdigest()
    assert worker["lake_symlink_target_string"] == f"sha256:{expected_symlink}"
    assert worker["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker["mathlib_revision"] == revisions["mathlib"]
    assert worker["mathlib_tree"] == revisions["mathlib_tree"]
    assert worker["mathlib_addcircle_source_sha256"] == f"sha256:{revisions['mathlib_addcircle_source_sha256']}"
    assert worker["crossref_metadata_sha256"] == f"sha256:{revisions['inspected_crossref_payload_sha256']}"
    assert worker["gdz_pdf_sha256"] == f"sha256:{revisions['inspected_gdz_pdf_sha256']}"
    assert worker["gdz_manifest_sha256"] == f"sha256:{revisions['inspected_gdz_iiif_manifest_sha256']}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["known_failures"] and receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"].startswith("S56-M-0293-STATEMENT")
    assert {recipe["recipe_id"] for recipe in receipt["structured_validation_recipes"]} == {
        "S56-M-0293-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0293-INTAKE-RECIPE-LEAN-PROBE",
    }

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    for name in OWNED_FILES - {"IntakeProbe.lean", "check_intake.py"}:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    ast.parse((HERE / "check_intake.py").read_text(encoding="utf-8"))
    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in lean_probe for token in prohibited)

    if not args.skip_probe_replay:
        result = subprocess.run(
            ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"],
            cwd=ROOT / "Formalizations/Lean",
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert hashlib.sha256(result.stdout).hexdigest() == receipt["probe_stdout_sha256"]
        assert hashlib.sha256(result.stderr).hexdigest() == receipt["probe_stderr_sha256"]

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print(SUCCESS, end="")


if __name__ == "__main__":
    main()
