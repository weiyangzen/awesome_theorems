#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0825 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0825"
ITEM_ID = "S56-M-0825-INTAKE"
RANK = 1383
BASE_REVISION = "902d9ce008e88a35a2307c85355560a230cc33c2"
BASE_TREE = "dfc20d8141f18f6b09a03e818acfff408e836714"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
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
    "Docs/Stage1_Blueprint_rev-5.6.md": "34e913419c1f9e24ed1d91fda9f1450d19f01ab22d60a7af5f9a00152cb04373",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "b1cd5bf2e918865015bab425e20c42df1c2ad26aff9a4e849960d8bc7539e58c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/researches/cs_theorems.md": "32cc0824d326427cc66457b8eaed333a20b82df3269e019d52caa9fb1fccbc1e",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/Combinatorics/SimpleGraph/Metric.lean": "4fa93451ec543582ab67d24e259914fdf550b65dadcb4bddceac9bec23557b5b",
    "Mathlib/Combinatorics/Quiver/Path/Weight.lean": "0e29fbdc2cea79e0cac5ad564f9c6b6181baf0057ccafdcbce88e3d92f9c4178",
    "Mathlib/Combinatorics/Quiver/Arborescence.lean": "4653df221c528c1ab125af7d56407d7186ca6fff6fefdff7c81cf7d9e1d68a25",
}
PROBE_DECLARATIONS = [
    "SimpleGraph.edist",
    "SimpleGraph.edist_eq_sInf",
    "SimpleGraph.Reachable.exists_walk_length_eq_edist",
    "SimpleGraph.edist_le",
    "SimpleGraph.reachable_of_edist_ne_top",
    "SimpleGraph.dist",
    "SimpleGraph.dist_eq_sInf",
    "SimpleGraph.dist_le",
    "Quiver.Path.addWeight",
    "Quiver.Path.addWeightOfEPs",
    "Quiver.Path.addWeight_comp",
    "Quiver.Path.addWeight_cons",
    "Quiver.Path.addWeightOfEPs_comp",
    "Quiver.shortestPath",
    "Quiver.shortest_path_spec",
]


def load_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1 : last])).hexdigest()


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
    assert matches == [{
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Dijkstra算法",
        "category": "组合数学 / 图论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }]
    target = matches[0]
    for field in (
        "execution_rank", "legacy_priority_slot", "baseline", "rework_required",
        "legacy_artifacts_accepted", "target_lane", "intake_score",
        "source_status_untrusted", "lifecycle_mode", "theorem_complete",
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
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    for field in (
        "module", "declaration_or_expression", "candidate_expression",
        "elaborated_expression_hash", "environment_fingerprint",
    ):
        assert formal[field] is None
    assert formal["gate_state"].startswith("blocked_exact_source_to_catalog")
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "no exact canonical statement" in instance["status_boundary"]
    assert "H1 does not claim" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/researches/cs_theorems.md") == revisions[
        "current_repository_cs_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for path, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / path) == expected, f"changed authoritative input: {path}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6061, 6066) == revisions[
        "repository_record_excerpt_sha256"
    ]
    assert excerpt_sha256(ROOT / "Docs/researches/cs_theorems.md", 166, 166) == revisions[
        "neighbor_cs_record_excerpt_sha256"
    ]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 22523, 22548) == revisions[
        "stage0_projection_excerpt_sha256"
    ]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6054, 6073) == revisions[
        "neighbor_math_excerpt_sha256"
    ]
    target = next(
        row for row in load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")["targets"]
        if row["theorem_id"] == THEOREM_ID
    )
    target_bytes = (json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    assert hashlib.sha256(target_bytes).hexdigest() == revisions["manifest_entry_sha256"]
    assert revisions["observed_primary_scan_sha256"] == (
        "baa66780e853ef06e8bf9c0d8c37e2e0a652e9f5252811e97fb2848d0514fba5"
    )
    assert revisions["observed_primary_scan_bytes"] == 192652
    assert revisions["observed_primary_scan_url"] == (
        "https://www.cs.yale.edu/homes/lans/readings/routing/dijkstra-routing-1959.pdf"
    )
    source = instance["source_candidates_not_credited"]
    assert len(source) == 1
    assert "10.1007/BF01386390" in source[0]["citation"]
    assert "page 269" in source[0]["candidate_summary"]
    assert "page 270" in source[0]["candidate_summary"]
    assert "visually inspected" in source[0]["inspection_status"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", "--untracked-files=all", cwd=mathlib) == ""
    for path, expected in MATHLIB_HASHES.items():
        assert sha256(mathlib / path) == expected, f"changed mathlib input: {path}"


def check_catalog_and_boundaries(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Dijkstra算法**") == 1
    assert catalog.count("- 陈述: 单源最短路径算法") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0825 Dijkstra算法" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    cs = (ROOT / "Docs/researches/cs_theorems.md").read_text(encoding="utf-8")
    assert "Dijkstra算法求最短路径正确" in cs
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0823", "THM-M-0824", "THM-M-0826", "THM-M-0827", "THM-C-0091"
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
        task_id = f"S56-M-0825-{suffix}"
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
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    for key in (
        "accepted_receipt_ids", "proof_body_locations", "canonical_obligation_ids",
        "statement_fingerprints", "typed_graph_changes", "composition_certificates",
        "content_addressed_recipe_ids", "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"] == "master acceptance of the provisional self-tested intake receipt"
    assert "canonical statement identity" in receipt["first_failed_theorem_gate"]
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
    evidence = receipt["source_evidence"]
    assert "10.1007/BF01386390" in evidence["citation"]
    assert evidence["observed_url"].endswith("dijkstra-routing-1959.pdf")
    assert evidence["observed_pdf_sha256"] == (
        "baa66780e853ef06e8bf9c0d8c37e2e0a652e9f5252811e97fb2848d0514fba5"
    )
    assert evidence["observed_pdf_bytes"] == 192652
    assert "visual inspection" in evidence["inspection_method"]
    assert "page 270" in evidence["page_boundary"]
    assert "Problem 2" in evidence["pinpoint_statement"]
    assert "H1" in evidence["h1_rationale"]
    assert receipt["dirty_input_evidence"]["preflight_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    assert hashlib.sha256(str(lake.readlink()).encode()).hexdigest() == receipt[
        "worker_input_hashes"
    ]["lake_symlink_target_string_sha256"]
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == recipe["exit_code"] == 0 for recipe in recipes)
    assert all(recipe["covered_ids"] == [ITEM_ID] for recipe in recipes)
    assert recipes[1]["covered_declarations"] == PROBE_DECLARATIONS


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path.resolve())
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
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
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        assert whitespace.returncode in (0, 1)
        assert not whitespace.stdout and not whitespace.stderr, f"whitespace diagnostic: {path.name}"
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
    print("intake invariant check: ok (THM-M-0825 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
