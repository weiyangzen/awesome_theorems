#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0752 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0752"
ITEM_ID = "S56-M-0752-INTAKE"
RANK = 1338
BASE_REVISION = "a75b2f3ac5b8b7d34eb73435734edfeecc41bd40"
BASE_TREE = "66a22e1dc2e1c14c27bd01396a99826ab2536bf1"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_BLOCK_SHA256 = "c442e62281545041d7d5542ce355180cd054dd6f876505e64687dda09309c0d1"
STAGE0_BLOCK_SHA256 = "1f633e9560e77ba667434b342ea63a07c1d8287815f77fe4d898870aaf6d4cd4"
MANIFEST_ENTRY_SHA256 = "934610f0bede222e604c7c1b9cf3d0f9670dcd386759f7295725d601a8f18cb0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
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
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "677bf9512823f253bd30a332150e6154afa55c665e314cf140b42129fe826f77",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "5e4d08eb4dabb1a445de740e429af94163240b34535737fb84a4841220bbf6a6",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCE_HASHES = {
    "Mathlib/Computability/TuringDegree.lean": "d5fd0caf5c321343ec378e2601913aec152efac58f113ce3b602dca7345b1e5c",
    "Mathlib/Computability/RecursiveIn.lean": "bc4e768b130b905c4ce57770906041da3a2c5db7aa4e4e67e3cfcbc63c153247",
}
PROBE_DECLARATIONS = [
    "RecursiveIn",
    "TuringReducible",
    "TuringEquivalent",
    "TuringReducible.refl",
    "TuringReducible.trans",
    "TuringEquivalent.equivalence",
    "TuringDegree",
    "TuringDegree.instPartialOrder",
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


def manifest_entry_hash(target: dict) -> str:
    encoded = (json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def check_authorities(instance: dict, *, worker_mode: bool) -> list[dict]:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    assert manifest["scope"]["covered_targets"] == 1546
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "跳跃算子",
            "category": "数理逻辑 / 递归论",
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
    assert manifest_entry_hash(target) == MANIFEST_ENTRY_SHA256
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "category",
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

    items = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    intake = next(row for row in items if row["id"] == ITEM_ID)
    assert intake["theorem_id"] == THEOREM_ID and intake["execution_rank"] == RANK
    assert intake["phase"] == "intake" and intake["layer"] == 0
    assert intake["state"] in {"[ ]", "[_]", "[x]"} and intake["depends_on"] == []
    if worker_mode:
        assert intake["state"] == "[ ]" and intake["attempts"] == 0
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    assert intake["children"] == []
    return items


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "does_not_select_one_truth_valued_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    for field in (
        "module",
        "candidate_expression",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert "blocked" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "No canonical mathematical or Lean proposition" in instance["status_boundary"]
    assert instance["source_status"].startswith("H1_")

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
        cwd=ROOT,
        check=False,
    ).returncode == 0
    assert revisions["repository_source_record_commit"] == SOURCE_RECORD_COMMIT
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == (
        revisions["repository_source_record_blob"]
    ) == SOURCE_RECORD_BLOB
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 5542, 5547) == (
        revisions["repository_record_block_sha256"]
    ) == SOURCE_RECORD_BLOCK_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 20542, 20567) == (
        revisions["stage0_projection_block_sha256"]
    ) == STAGE0_BLOCK_SHA256
    assert revisions["manifest_entry_sha256"] == MANIFEST_ENTRY_SHA256
    for path, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / path) == expected, f"changed authoritative input: {path}"
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
        assert revisions[field] == SOURCE_HASHES[path], f"stale instance hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    fields = {
        "turing_degree_source_sha256": "Mathlib/Computability/TuringDegree.lean",
        "recursive_in_source_sha256": "Mathlib/Computability/RecursiveIn.lean",
    }
    for field, relative in fields.items():
        assert revisions[field] == MATHLIB_SOURCE_HASHES[relative]
        assert sha256(mathlib / relative) == MATHLIB_SOURCE_HASHES[relative]


def check_scope_and_candidates(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**跳跃算子**") == 1
    assert "- 提出者: Stephen Kleene/Emil Post" in catalog
    assert "- 陈述: 图灵度的跳跃" in catalog
    blocker = instance["statement_blocker"].lower()
    for token in (
        "well-definedness",
        "noncomputability",
        "strict increase",
        "monotonicity",
        "relative completeness",
        "oracle-machine numbering",
        "ordered binders",
        "boundary cases",
    ):
        assert token in blocker, f"missing ambiguity boundary: {token}"
    assert len(instance["candidate_scope_not_credited"]) == 6
    neighbors = {item["theorem_id"] for item in instance["neighbor_target_boundaries"]}
    assert neighbors == {"THM-M-0741", "THM-M-0750", "THM-M-0751", "THM-M-0753", "THM-M-0754"}
    expected_neighbor_names = {
        "THM-M-0741": "停机问题",
        "THM-M-0750": "图灵度",
        "THM-M-0751": "图灵度的上确界",
        "THM-M-0753": "跳跃反演定理",
        "THM-M-0754": "算术层次",
    }
    assert {
        item["theorem_id"]: item["name"] for item in instance["neighbor_target_boundaries"]
    } == expected_neighbor_names
    assert instance["primary_source_candidates_not_credited"][0]["doi"] == "10.2307/1969708"
    candidates = {item["declaration"] for item in instance["formal_candidates_not_credited"]}
    assert candidates == {
        "RecursiveIn",
        "TuringReducible",
        "TuringEquivalent",
        "TuringDegree",
        "TuringDegree.instPartialOrder",
    }
    assert all(item["boundary"] for item in instance["formal_candidates_not_credited"])


def check_task_dag(dag: dict, authoritative_items: list[dict]) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert dag["accepted_states"] == []
    tasks = dag["tasks"]
    assert [task["id"] for task in tasks] == [f"S56-M-0752-{suffix}" for suffix in TASK_SUFFIXES]
    for index, task in enumerate(tasks, start=1):
        expected_id = f"S56-M-0752-{TASK_SUFFIXES[index - 1]}"
        predecessor = ITEM_ID if index == 1 else tasks[index - 2]["id"]
        assert task["id"] == expected_id
        assert task["layer"] == index and task["depends_on"] == [predecessor]
        assert task["state"] == "open" and task["evidence_ids"] == []
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        authority = next(row for row in authoritative_items if row["id"] == expected_id)
        for field in ("phase", "layer", "depends_on", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authority[field]
    assert "source proposition" in tasks[0]["first_blocker"]


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["selftest_result"] == "pass"
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["attestor"]["identity"] == "Stage1 rev-5.6 worker slot74"
    assert receipt["attestor"]["signature"] is None
    assert receipt["platform"]["architecture"] == "x86_64"
    assert receipt["dirty_input_evidence"]["preflight_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    lake_target_hash = hashlib.sha256(str(lake.readlink()).encode()).hexdigest()
    assert lake_target_hash == receipt["worker_input_hashes"][
        "lake_symlink_target_string_sha256"
    ]
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["root_vector_after"] == ROOT_VECTOR
    axiom_result = receipt["axiom_and_placeholder_result"]
    assert axiom_result["target_declarations_added"] == []
    assert axiom_result["proof_bodies_added"] == []
    assert axiom_result["placeholder_scan"].startswith("pass:")
    assert receipt["covered_task_ids"] == receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["content_addressed_receipt_ids"] == []
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["support_state"] == "provisional_worker_only"
    assert receipt["supersession_state"] == "current_unsuperseded_worker_report"
    assert receipt["revocation_state"] == "not_revoked"
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert receipt["declaration_ownership"] == []
    assert receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["known_failures"] and receipt["retry_condition"]
    assert receipt["first_failed_gate"] == (
        "master acceptance of the provisional self-tested intake receipt"
    )

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    required_recipe_fields = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "covered_declarations",
    }
    for recipe in recipes:
        assert required_recipe_fields <= set(recipe)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_obligation_ids"] == []
        assert recipe["covered_task_ids"]
        assert recipe["started_at"] <= recipe["ended_at"]
        assert len(recipe["output_log_sha256"]) == 64
        assert all(
            set(output) == {"path_or_stream", "semantic_hash_policy"}
            for output in recipe["expected_outputs"]
        )
    assert recipes[0]["argv"] == [
        "python3",
        "-B",
        "Stage1_Instances/THM-M-0752/check_intake.py",
    ]
    assert recipes[0]["covered_declarations"] == []
    assert recipes[1]["argv"] == [
        "lake",
        "env",
        "lean",
        "../../Stage1_Instances/THM-M-0752/IntakeProbe.lean",
    ]
    assert recipes[1]["covered_declarations"] == PROBE_DECLARATIONS


def check_packet(packet: dict, receipt: dict) -> None:
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"]
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["known_failures"] == receipt["known_failures"]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["node_ids"] == [ITEM_ID]
    assert packet["worker_branch_or_worktree"] == receipt["worker_branch_or_worktree"]
    assert packet["diff_summary"] == receipt["diff_summary"]
    assert packet["exact_statement_change"] == receipt["exact_statement_change"]
    assert packet["source_revisions"] == receipt["source_inputs"]
    assert packet["proof_body_locations"] == []
    assert packet["axiom_and_placeholder_result"] == receipt["axiom_and_placeholder_result"]
    assert packet["root_vector_before"] == receipt["root_vector_before"]
    assert packet["root_vector_after"] == receipt["root_vector_after"]
    assert packet["debt_delta_basis"] == receipt["debt_delta_basis"]
    assert packet["follow_up_nodes"] == receipt["remaining_root_cut_set"]
    assert packet["canonical_obligation_ids"] == packet["statement_fingerprints"] == []
    assert packet["typed_graph_changes"] == packet["composition_certificates"] == []
    assert packet["content_addressed_recipe_ids"] == []
    assert packet["content_addressed_receipt_ids"] == []
    assert packet["ownership_and_change_impact"] == receipt["ownership_and_change_impact"]
    assert packet["change_impact_set"] == [ITEM_ID]


def check_files(instance: dict, receipt: dict, packet: dict | None) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    hashes = receipt["non_self_referential_owned_artifact_sha256"]
    expected_hashed = expected_changed - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
    }
    assert set(hashes) == expected_hashed
    for relative, expected in hashes.items():
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    checked = list(HERE.iterdir())
    if packet is not None:
        checked.append(ROOT / ".stage1-worker-selftest.json")
    for path in checked:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--worker-packet",
        type=Path,
        help="optional provisional worker packet; absent after integration",
    )
    args = parser.parse_args()
    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    packet = load_json(args.worker_packet) if args.worker_packet is not None else None
    authoritative_items = check_authorities(instance, worker_mode=packet is not None)
    check_instance(instance)
    check_scope_and_candidates(instance)
    check_task_dag(dag, authoritative_items)
    check_receipt(receipt, dag)
    if packet is not None:
        check_packet(packet, receipt)
    check_files(instance, receipt, packet)
    print("intake invariant check: ok (THM-M-0752 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
