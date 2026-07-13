#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0862."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0862"
ITEM_ID = "S56-M-0862-INTAKE"
RANK = 1416
BASE_REVISION = "464759128569180ab640c412cd80bc5dd2c3b44a"
BASE_TREE = "8da3c9130640d08d4e179450a0418368d0454745"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "acddbc7c967786d595d8bce3393b249946d3bd2b5e495df6f246698d6b8c21d7"
MANIFEST_ENTRY_SHA256 = "ee55e4d7ba99bd4361652367b23c56c6d0100a7438552f75580040d075394214"
PRIMARY_PDF_SHA256 = "45f0dce723f85dae5d360892b6e9596aeaef70ea222b3ea9a0ea2e7c54ae3602"
PRIMARY_DOI_SHA256 = "5d801900763f0e3e77c229ecd27792c7170866b8035d6451ce8176a90b8b85cf"
PRIMARY_PAGE_HASHES = {
    "primary_source_page_100_101_png_sha256":
        "4e443f1841f3d63726e755151bddfd01b552eb054faa593ae3310721a904d033",
    "primary_source_page_102_103_png_sha256":
        "000f388444405791f7949a24bc61080248ba1dc829c6a0a8c53e2670db1cc853",
}
MODERN_SOURCE_HASHES = {
    "modern_source_chapter_sha256":
        "1d54f8cf0a846e8acedc5a5eb87839173a3145148a6c23eba49e4d4d6d0c8775",
    "modern_source_text_sha256":
        "32d3e2e70d912de714c2ec2529835627437be4a7b44382a2c529992a6baa0268",
    "modern_source_definitions_chapter_sha256":
        "ebd9084653a1a534b964cbe327eeb8ab6b46a5e98deeee94280b05ebb6f37b56",
    "modern_source_definitions_text_sha256":
        "94ff5b77d20b0499aed7aa377d9aa223f0fa610f68c67d7d21e1850790f6b6f7",
}
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
SOURCE_HASHES = {
    "target_manifest_sha256": (
        "Docs/Stage1_Targets_rev-5.6.json",
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    ),
    "authoritative_blueprint_sha256": (
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "1e508ba6dea246337ac6daf72d8d58fef1ec2d44422ab5fff19db56fac83d00b",
    ),
    "execution_dag_sha256": (
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "b0a766fc806a0dc4e9a8b4400e6ab0c92e39ca9265a23cd3a2feab451a63e4a9",
    ),
    "execution_skill_sha256": (
        "skills/execute-stage1-rev56/SKILL.md",
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    ),
    "blueprint_guidelines_sha256": (
        "Docs/Blueprint_Guidelines.md",
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    ),
    "repository_math_source_sha256": (
        "Docs/researches/math_theorems.md",
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    ),
    "stage0_blueprint_sha256": (
        "Docs/Stage0_Blueprint.md",
        "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    ),
    "lean_toolchain_file_sha256": (
        "Formalizations/Lean/lean-toolchain",
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    ),
    "lake_manifest_sha256": (
        "Formalizations/Lean/lake-manifest.json",
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    ),
}
MATHLIB_SOURCE_HASHES = {
    "mathlib_paths_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Paths.lean",
        "e5aa067bc2106430bb917da65dda897d8bd67c215706681b41b1078d771b43b5",
    ),
    "mathlib_connected_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Connectivity/Connected.lean",
        "9171842c49be5f8951c6a2d5c39ae374279d46eaa317efd69bdf3039d289eeff",
    ),
    "mathlib_edge_connectivity_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Connectivity/EdgeConnectivity.lean",
        "7b4d638ae2e98b8131a3d4eccc53f3e52afab999d39895c5d21bd23b49db06b2",
    ),
    "mathlib_maps_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Maps.lean",
        "60bcb9baa33451ed189091e3254004bf77f9b814a87a6ce9709042c4db6d7d2a",
    ),
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1 : last])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def canonical_manifest_entry(target: dict) -> str:
    data = (json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(data).hexdigest()


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
    assert all(
        isinstance(row, dict)
        and isinstance(row.get("command"), str)
        and isinstance(row.get("exit_code"), int)
        for row in packet["commands"]
    )
    assert packet["output_summary"] == receipt["output_summary"]
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

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(targets) == len(items) == 1
    target, item = targets[0], items[0]
    assert canonical_manifest_entry(target) == MANIFEST_ENTRY_SHA256

    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Menger定理",
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
        "execution_rank",
        "legacy_priority_slot",
        "category",
        "source_status_untrusted",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "lifecycle_mode",
        "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    if args.worker_packet is not None:
        assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    assert item["children"] == []

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
        "direct_theorem_candidate",
    ):
        assert formal[key] is None
    assert "open_pending" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    if args.worker_packet is not None:
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
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert revisions["target_manifest_entry_sha256"] == MANIFEST_ENTRY_SHA256
    for field, (relative, expected) in SOURCE_HASHES.items():
        assert sha256(ROOT / relative) == expected, f"changed authoritative input: {relative}"
        assert revisions[field] == expected, f"stale source hash: {field}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6320, 6325) == revisions["repository_record_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 5977, 5982) == revisions["overlap_record_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 23522, 23547) == revisions["stage0_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 22199, 22224) == revisions["overlap_stage0_excerpt_sha256"]

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Menger定理**") == 1
    assert catalog.count("**门格尔定理**") == 1
    assert "- 陈述: 顶点连通度与不相交路径" in catalog
    assert "- 陈述: 图中不相交路径的最大数目" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0862 Menger定理" in stage0 and "THM-M-0813 门格尔定理" in stage0

    primary = revisions["primary_source"]
    assert primary["doi"] == "10.4064/fm-10-1-96-115"
    assert primary["observed_pdf_sha256"] == PRIMARY_PDF_SHA256
    assert primary["observed_doi_metadata_sha256"] == PRIMARY_DOI_SHA256
    assert "Satz beta" in primary["pinpoint"] and "printed pages 100-102" in primary["pinpoint"]
    assert primary["credit"].endswith("not an exact E4 catalog crosswalk or H0")
    modern = revisions["modern_source_lead"]
    assert "Theorem 3.3.1" in modern["pinpoint"]
    assert "Theorem 3.3.6" in modern["pinpoint"]
    assert modern["observed_chapter_sha256"] == MODERN_SOURCE_HASHES["modern_source_chapter_sha256"]
    assert modern["observed_text_sha256"] == MODERN_SOURCE_HASHES["modern_source_text_sha256"]
    assert modern["observed_definitions_chapter_sha256"] == MODERN_SOURCE_HASHES["modern_source_definitions_chapter_sha256"]
    assert modern["observed_definitions_text_sha256"] == MODERN_SOURCE_HASHES["modern_source_definitions_text_sha256"]

    readme = (HERE / "README.md").read_text(encoding="utf-8")
    scope = (HERE / "scope-map.md").read_text(encoding="utf-8")
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    for text in (readme, scope, crosswalk):
        assert "THM-M-0813" in text
    assert "Satz beta" in readme and "printed pages 100-102" in readme
    assert "Ist K ein kompakter regulaerer eindimensionaler Raum" in crosswalk
    assert "not independently reviewed translation" in crosswalk
    assert "Whitney" in readme and "Whitney" in scope and "Whitney" in crosswalk
    assert "canonical statement and Lean target remain null" in readme

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, (relative, expected) in MATHLIB_SOURCE_HASHES.items():
        assert sha256(mathlib / relative) == expected
        assert revisions[field] == expected
    environment = instance["environment_fingerprint"]
    assert environment["lean_commit"] == "98dc76e3c0a9b856c9b98726b713fb04fab16740"
    assert environment["lean_toolchain_file_sha256"] == revisions["lean_toolchain_file_sha256"]
    assert environment["lake_manifest_sha256"] == revisions["lake_manifest_sha256"]
    assert environment["mathlib_revision"] == revisions["mathlib"]
    assert environment["mathlib_tree"] == revisions["mathlib_tree"]
    assert environment["probe_output_sha256"] == receipt["probe_output_sha256"] == PROBE_OUTPUT_SHA256

    evidence = receipt["source_evidence"]
    inputs = receipt["worker_input_hashes"]
    assert evidence["repository_source_record_commit"] == SOURCE_COMMIT
    assert evidence["repository_source_record_blob"] == SOURCE_BLOB
    assert evidence["primary_source_observed_pdf_sha256"] == PRIMARY_PDF_SHA256
    assert inputs["primary_source_pdf_sha256"] == PRIMARY_PDF_SHA256
    assert inputs["primary_source_doi_metadata_sha256"] == PRIMARY_DOI_SHA256
    for field, expected in PRIMARY_PAGE_HASHES.items():
        assert inputs[field] == expected
    for field, expected in MODERN_SOURCE_HASHES.items():
        assert inputs[field] == expected
    assert evidence["proof_body_locations"] == []
    observations = receipt["manual_observations"]
    assert len(observations) == 1
    assert observations[0]["kind"] == "visual_source_inspection"
    assert "not an executable command" in observations[0]["boundary"]

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0862-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(row["id"], row["depends_on"]) for row in dag["tasks"]] == expected_tasks

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["signed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["root_vector_before"] == {"H": "unclassified", "M": "unclassified", "R": "unclassified"}
    assert receipt["covered_node_ids"] == receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert receipt["declaration_ownership"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["output_summary"].endswith("No canonical statement or proof was tested or claimed.")
    assert receipt["known_failures"]
    assert any("THM-M-0813" in failure for failure in receipt["known_failures"])
    assert any("No direct pinned Menger formal artifact" in failure for failure in receipt["known_failures"])
    assert all(
        isinstance(row.get("argv"), list)
        and isinstance(row.get("exit_code"), int)
        and isinstance(row.get("result"), str)
        and row["result"]
        for row in receipt["commands_and_results"]
    )
    assert all(row["argv"][0] != "manual" for row in receipt["commands_and_results"])
    recipes = receipt["structured_validation_recipes"]
    assert {row["recipe_id"] for row in recipes} == {
        "S56-M-0862-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0862-INTAKE-RECIPE-LEAN-PROBE",
    }
    assert all(
        isinstance(row["argv"], list)
        and row["argv"]
        and row["network_policy"] == "denied"
        and row["expected_exit"] == row["exit_code"] == 0
        and row["covered_ids"] == [ITEM_ID]
        for row in recipes
    )
    assert all(
        isinstance(row["covered_obligation_ids"], list)
        and isinstance(row["covered_declarations"], list)
        and all("semantic_hash_policy" in output for output in row["expected_outputs"])
        for row in recipes
    )
    assert recipes[0]["covered_obligation_ids"] == recipes[0]["covered_declarations"] == []
    assert recipes[1]["covered_obligation_ids"] == []
    assert set(recipes[1]["covered_declarations"]) == {
        "SimpleGraph.Path",
        "SimpleGraph.Walk.IsPath",
        "SimpleGraph.Reachable",
        "SimpleGraph.Reachable.exists_isPath",
        "SimpleGraph.induce",
        "SimpleGraph.IsEdgeReachable",
        "SimpleGraph.IsEdgeConnected",
        "SimpleGraph.Walk.IsPath.disjoint_support_of_append",
    }

    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    expected_lake_hash = hashlib.sha256(lake_target).hexdigest()
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == f"sha256:{expected_lake_hash}"
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    checked = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked.append(args.worker_packet.resolve())
    for path in checked:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0862 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
