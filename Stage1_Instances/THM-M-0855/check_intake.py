#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0855."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0855"
ITEM_ID = "S56-M-0855-INTAKE"
BASE_REVISION = "1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4"
BASE_TREE = "61214aa2a03c032134ddc4958b1df63df3430a85"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PRIMARY_SCAN_SHA256 = "a14dc030b3c2c6364aed0e093ced674d03bd2fc3390e660be036e4b5581492a7"
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
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
SOURCE_HASHES = {
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
MATHLIB_SOURCE_HASHES = {
    "mathlib_hamiltonian_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Hamiltonian.lean",
    "mathlib_clique_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Clique.lean",
    "mathlib_subgraph_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Subgraph.lean",
    "mathlib_connected_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Connectivity/Connected.lean",
    "mathlib_edge_connectivity_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Connectivity/EdgeConnectivity.lean",
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def path_bytes_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix().encode()
        digest.update(relative + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(f"{relative}\0{sha256(path)}\n".encode())
    return digest.hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True, capture_output=True
    ).stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument("--primary-pdf", type=Path)
    return parser.parse_args()


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
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"]
    assert packet["output_summary"]


def main() -> None:
    args = parse_args()
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == 1409
    assert target["name"] == "Chvátal-Erdős定理"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    intake_authority = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert intake_authority["theorem_id"] == THEOREM_ID
    assert intake_authority["phase"] == "intake"
    assert intake_authority["depends_on"] == []
    assert intake_authority["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_authority["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["item_id"] == ITEM_ID and instance["intent"] == "intake"
    assert instance["canonical_statement"].startswith("Let G be a graph with at least three vertices.")
    assert "primary_theorem_1_human_scope_frozen" in instance["canonical_claim_status"]
    assert instance["statement_blocker"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert formal["gate_state"] == "open_pending_incorporated_definition_audit_and_statement_phase"
    assert instance["quantifiers"] and instance["ordered_binders"] and instance["hypotheses"]
    assert instance["alternate_encodings"] == []
    candidates = instance["candidate_alternate_encodings_not_credited"]
    assert len(candidates) == 4
    assert all("uncredited" in candidate["status"] for candidate in candidates)
    assert instance["excluded_degenerate_cases"]
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_SOURCE_HASHES.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    assert revisions["primary_scan_sha256"] == PRIMARY_SCAN_SHA256
    assert revisions["primary_scan_size_bytes"] == 221449
    assert revisions["primary_scan_pages"] == 3

    dependency = ITEM_ID
    expected_task_ids = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0855-{suffix}"
        expected_task_ids.append(task_id)
        task = dag["tasks"][layer - 1]
        authority = next(row for row in execution["items"] if row["id"] == task_id)
        assert task["id"] == task_id
        assert task["phase"] == authority["phase"]
        assert task["layer"] == authority["layer"] == layer
        assert task["depends_on"] == authority["depends_on"] == [dependency]
        assert task["owned_paths"] == authority["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authority["deliverable"]
        assert task["completion_gate"] == authority["completion_gate"]
        assert task["stable_gate_id"] == f"{task_id}-GATE"
        for field in ("covered_obligation_ids", "owned_sources", "validation_spec_ids"):
            assert task[field] == []
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [task["id"] for task in dag["tasks"]] == expected_task_ids

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**Chvátal-Erdős定理**" in catalog
    assert "- 提出者: Václav Chvátal/Paul Erdős" in catalog
    assert "- 时间: 1972" in catalog
    assert "- 陈述: Hamilton圈存在的连通度与独立数条件" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0855 Chvátal-Erdős定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    assert "10.1016/0012-365X(72)90079-9" in crosswalk
    assert "Theorem 1 on printed page 111" in crosswalk
    assert "Theorem 2" in crosswalk and "Theorem 3" in crosswalk
    assert "IsEdgeConnected" in crosswalk

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == expected_task_ids
    for field in (
        "owner",
        "reviewer_policy",
        "validation_started_at",
        "validation_ended_at",
        "validated_at",
        "review_due",
        "support_state",
        "supersession_state",
        "revocation_state",
        "incident_path",
    ):
        assert isinstance(receipt[field], str) and receipt[field]
    for field in ("validation_started_at", "validation_ended_at", "validated_at"):
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", receipt[field])
    required_recipe_keys = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_ids",
        "covered_obligation_ids",
        "covered_declarations",
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    structure = next(recipe for recipe in recipes if recipe["recipe_id"].endswith("STRUCTURE"))
    assert structure["cwd"] == "."
    assert structure["argv"] == [
        "python3",
        "-B",
        "Stage1_Instances/THM-M-0855/check_intake.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
    ]
    lean_recipe = next(recipe for recipe in recipes if recipe["recipe_id"].endswith("LEAN-PROBE"))
    assert lean_recipe["cwd"] == "Formalizations/Lean"
    assert lean_recipe["argv"] == [
        "lake",
        "env",
        "lean",
        "../../Stage1_Instances/THM-M-0855/IntakeProbe.lean",
    ]

    dirty = receipt["dirty_input_evidence"]
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    nonrecursive = [HERE / name for name in OWNED_FILES if name != "intake-receipt.json"]
    assert dirty["owned_untracked_patch_sha256"] == path_bytes_hash(nonrecursive)
    assert dirty["owned_untracked_manifest_sha256"] == path_manifest_hash(nonrecursive)
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    status_paths = {
        line[3:] if line.startswith("?? ") else line[2:].lstrip()
        for line in git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert status_paths == expected_changed, f"actual changed paths differ: {sorted(status_paths)}"

    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n"), f"missing final newline: {path.name}"
            assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path.name}"
    for name in ("README.md", "instance.json", "scope-map.md", "source-statement-crosswalk.md", "task-dag.json", "validation.md", "intake-receipt.json"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for name in ("SimpleGraph.IsHamiltonian", "SimpleGraph.indepNum", "SimpleGraph.Subgraph.deleteVerts", "SimpleGraph.Connected"):
        assert name in probe
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.primary_pdf is not None:
        primary = args.primary_pdf.resolve()
        assert primary.is_file()
        assert sha256(primary) == PRIMARY_SCAN_SHA256
        assert primary.stat().st_size == 221449
        info = subprocess.run(
            ["pdfinfo", str(primary)], check=True, text=True, capture_output=True
        ).stdout
        assert re.search(r"^Pages:\s+3$", info, re.MULTILINE)
        extracted = subprocess.run(
            ["pdftotext", "-layout", str(primary), "-"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        normalized = " ".join(extracted.split())
        assert "Theorem 1 . Let G be a graph with at least three vertices" in normalized
        assert "G is s-connected and contains no independent set of more than s vertices" in normalized
        assert "then G has a Hamiltonian circuit" in normalized
        assert "Theorem 2" in normalized and "Theorem 3" in normalized
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0855 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
