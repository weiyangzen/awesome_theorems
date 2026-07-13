#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0826 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0826"
ITEM_ID = "S56-M-0826-INTAKE"
RANK = 1384
BASE_REVISION = "902d9ce008e88a35a2307c85355560a230cc33c2"
BASE_TREE = "dfc20d8141f18f6b09a03e818acfff408e836714"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_EXCERPT_SHA256 = "c67d8e4e474dbc7fe2d2611f3ba20ff91bea5f9599745878df8865a72c2fc6ec"
CS_EXCERPT_SHA256 = "7adfdcafd9f1014aae8d5985523e42f3aba0c70997f1e9ce2773602ba35a353c"
STAGE0_EXCERPT_SHA256 = "a068c4b45a3506f0e63ecc4055177107a1707c1620e2bcaebdc94d092e9031bd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "1b63986ff72da4809fb8d328b95298d4f268b874a7e2c695a6eedd065b384be5"
MIT_PDF_SHA256 = "7693bf7b5854cc4c45f13013a0ff9dbf0a46349e8f86877c7deed63f187e30b8"
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
PROBE_DECLARATIONS = (
    "Digraph",
    "Digraph.Adj",
    "Quiver.Path",
    "Quiver.Path.length",
    "Quiver.Path.addWeight",
    "Quiver.Path.addWeight_nil",
    "Quiver.Path.addWeight_cons",
    "Quiver.Path.addWeight_comp",
    "Quiver.Path.addWeightOfEPs",
    "Quiver.Path.addWeightOfEPs_comp",
)
PACKET_KEYS = {
    "item_id",
    "changed_paths",
    "commands",
    "output_summary",
    "base_revision",
    "known_failures",
    "state",
}
SOURCE_HASH_FIELDS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "repository_cs_source_sha256": "Docs/researches/cs_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
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


def check_mit_pdf(path: Path) -> None:
    """Replay the optional modern source lead without admitting it as H0."""
    assert sha256(path) == MIT_PDF_SHA256
    run = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    assert run.returncode == 0, run.stderr
    text = run.stdout
    assert "Lecture 17: Shortest Paths III:" in text
    assert "Bellman-Ford(G,W,s)" in text
    assert "for i = 1 to |V | − 1" in text
    assert "contains no negative weight cycles" in text
    assert "d[v] = δ(s, v) for all v ∈ V" in text
    assert "negative-weight" in text and "cycle reachable from s" in text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument("--mit-pdf", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "Bellman-Ford算法"
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

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["literal_source_claim_zh"] == "带负权边的最短路径算法"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "candidate_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is dag["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    source = instance["source_revisions"]
    assert source["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert source["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert source["repository_source_record_commit"] == SOURCE_COMMIT
    assert source["repository_source_record_blob"] == SOURCE_BLOB
    assert git("hash-object", "Docs/researches/math_theorems.md") == source["current_repository_math_source_blob"]
    assert git("hash-object", "Docs/researches/cs_theorems.md") == source["current_repository_cs_source_blob"]
    assert git("hash-object", "Docs/Stage0_Blueprint.md") == source["current_stage0_blueprint_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert source[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6068, 6073) == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/researches/cs_theorems.md", 167, 167) == CS_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 22550, 22575) == STAGE0_EXCERPT_SHA256
    assert source["repository_record_excerpt_sha256"] == SOURCE_EXCERPT_SHA256
    assert source["secondary_repository_record_excerpt_sha256"] == CS_EXCERPT_SHA256
    assert source["stage0_projection_excerpt_sha256"] == STAGE0_EXCERPT_SHA256
    assert source["inspected_mit_lecture17_pdf_sha256"] == MIT_PDF_SHA256
    if args.mit_pdf is not None:
        check_mit_pdf(args.mit_pdf.resolve())

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert source["mathlib"] == MATHLIB_REVISION and source["mathlib_tree"] == MATHLIB_TREE
    assert source["digraph_basic_source_sha256"] == sha256(mathlib / "Mathlib/Combinatorics/Digraph/Basic.lean")
    assert source["quiver_path_source_sha256"] == sha256(mathlib / "Mathlib/Combinatorics/Quiver/Path.lean")
    assert source["quiver_path_weight_source_sha256"] == sha256(mathlib / "Mathlib/Combinatorics/Quiver/Path/Weight.lean")

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0826-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("- 陈述: 带负权边的最短路径算法") == 1
    assert "| 3.2.2 | **Bellman-Ford算法**" in (ROOT / "Docs/researches/cs_theorems.md").read_text(encoding="utf-8")
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0823", "THM-M-0824", "THM-M-0825", "THM-M-0827"
    }
    assert len(instance["source_candidates_not_credited"]) == 3
    assert len(instance["formal_candidates_not_credited"]) == 2

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["content_addressed"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet.resolve())
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)
    lean_run = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0826/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert lean_run.returncode == 0, lean_run.stdout
    assert hashlib.sha256(lean_run.stdout.encode()).hexdigest() == PROBE_OUTPUT_SHA256
    for declaration in PROBE_DECLARATIONS:
        assert declaration in lean_run.stdout

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == PACKET_KEYS
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == expected_changed
        assert isinstance(packet["commands"], list) and packet["commands"]
        assert isinstance(packet["output_summary"], str) and packet["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]

    print("intake invariant check: ok (THM-M-0826 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
