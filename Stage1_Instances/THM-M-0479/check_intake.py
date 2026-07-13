#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0479 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0479"
ITEM_ID = "S56-M-0479-INTAKE"
RANK = 1360
BASE_REVISION = "0f70149d61a952d44f907f4662a143372bcb4c44"
BASE_TREE = "35328e4f56f47446a4e1dfdbe361a1b70a4b18a7"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_STDOUT_SHA256 = "f8ebef27763585acc203471f66dd47a3043450dcfbfe01a4baa171bc9d3e7537"
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
    "mathlib_primes_in_ap_source_sha256": "Mathlib/NumberTheory/LSeries/PrimesInAP.lean",
    "mathlib_zmod_coprime_source_sha256": "Mathlib/Data/ZMod/Coprime.lean",
    "mathlib_nat_prime_source_sha256": "Mathlib/Data/Nat/Prime/Basic.lean",
}
INTEGRATION_MUTABLE_FIELDS = {
    "authoritative_blueprint_sha256",
    "execution_dag_sha256",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_hash(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[start - 1 : end]).encode()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def git_blob_sha256(revision: str, relative: str) -> str:
    data = subprocess.check_output(
        ["git", "show", f"{revision}:{relative}"],
        cwd=ROOT,
        stderr=subprocess.DEVNULL,
    )
    return hashlib.sha256(data).hexdigest()


def expected_source_hash(field: str, relative: str) -> str:
    if field in INTEGRATION_MUTABLE_FIELDS:
        return git_blob_sha256(BASE_REVISION, relative)
    return sha256(ROOT / relative)


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
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
    assert all(isinstance(command, str) and command for command in packet["commands"])
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

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    intake_items = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(targets) == len(intake_items) == 1
    target, intake_item = targets[0], intake_items[0]

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "狄利克雷定理"
    assert target["category"] == instance["category"] == "数论 / 初等数论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    assert intake_item["theorem_id"] == THEOREM_ID and intake_item["execution_rank"] == RANK
    assert intake_item["phase"] == "intake" and intake_item["layer"] == 0
    assert intake_item["state"] in {"[ ]", "[_]"} and intake_item["depends_on"] == []
    if args.worker_packet is not None:
        assert intake_item["state"] == "[ ]", "worker base must precede provisional integration"
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
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert all(
        "candidate_type_summary" in candidate and "exact_candidate_type" not in candidate
        for candidate in instance["formal_candidates_not_credited"]
    )

    revisions = instance["source_revisions"]
    assert git("merge-base", "--is-ancestor", BASE_REVISION, "HEAD") == ""
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == revisions["repository_base_tree"] == BASE_TREE
    assert revisions["repository_base"] == BASE_REVISION
    source_commit = revisions["repository_source_record_commit"]
    assert git("rev-parse", f"{source_commit}:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob"]
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    assert revisions["repository_record_excerpt_sha256"] == excerpt_hash(ROOT / "Docs/researches/math_theorems.md", 3518, 3523)
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_hash(ROOT / "Docs/Stage0_Blueprint.md", 13136, 13161)
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == expected_source_hash(field, relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_SOURCE_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0479-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**狄利克雷定理**") == 1
    assert "- 陈述: 等差数列中存在无穷多素数\n" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0479 狄利克雷定理" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    dirty = receipt["dirty_input_evidence"]
    assert set(dirty["owned_untracked_paths"]) == expected_changed
    expected_hashed = expected_changed - {f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"}
    assert set(dirty["untracked_input_hashes"]) == expected_hashed
    for relative, tagged_digest in dirty["untracked_input_hashes"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale owned hash: {relative}"

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
    for field in ("reviewer_policy", "validated_at", "review_due", "support_state", "incident_path"):
        assert isinstance(receipt[field], str) and receipt[field]
    assert isinstance(receipt["invalidation_inputs"], list) and receipt["invalidation_inputs"]

    assert set(receipt["source_inputs"]) == set(SOURCE_HASH_FIELDS.values())
    for relative, tagged_digest in receipt["source_inputs"].items():
        field = next(name for name, path in SOURCE_HASH_FIELDS.items() if path == relative)
        assert tagged_digest == f"sha256:{expected_source_hash(field, relative)}"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    assert worker_inputs["lean_probe_stdout"] == f"sha256:{PROBE_STDOUT_SHA256}"
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"

    recipes = receipt["structured_validation_recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {
        "S56-M-0479-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0479-INTAKE-RECIPE-LEAN-PROBE",
    }
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    assert recipes_by_id["S56-M-0479-INTAKE-RECIPE-STRUCTURE"]["argv"] == [
        "python3", "-B", "Stage1_Instances/THM-M-0479/check_intake.py"
    ]
    assert recipes_by_id["S56-M-0479-INTAKE-RECIPE-LEAN-PROBE"]["argv"] == [
        "lake", "env", "lean", "../../Stage1_Instances/THM-M-0479/IntakeProbe.lean"
    ]
    assert recipes_by_id["S56-M-0479-INTAKE-RECIPE-LEAN-PROBE"]["expected_outputs"][0]["semantic_hash_policy"] == f"exact UTF-8 SHA-256 {PROBE_STDOUT_SHA256}"
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet.resolve())
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path.name}"
    for name in (
        "README.md", "instance.json", "intake-receipt.json", "scope-map.md",
        "source-statement-crosswalk.md", "task-dag.json", "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)
    for declaration in (
        "Nat.infinite_setOf_prime_and_eq_mod",
        "Nat.infinite_setOf_prime_and_modEq",
    ):
        assert declaration in probe

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0479 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
