#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0759 planned intake."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0759"
ITEM_ID = "S56-M-0759-INTAKE"
RANK = 1345
BASE_REVISION = "d05520867fab3367a9b61b9544c3e12241204f54"
BASE_TREE = "fb2cfc62077d5b53e9938632cd6361dd60872067"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_BLOCK_SHA256 = "054b6673812fa78e3c52f80214ade8fd5778e61a442039090a88b3ac140faafe"
STAGE0_RECORD_BLOCK_SHA256 = "33c179cb940554a1aa41cabe7b035d4f2bcf945ed3b9492e57c4eaa2b2a29e74"
CS_SURVEY_BLOCK_SHA256 = "1d98967fd53d506c3c671357c9920757c3286925ceae6b6c680e2a74c11fc055"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_SYMLINK_TARGET_SHA256 = "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
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
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "58f0fe34e1443dd92bc0f587793dcba33c9e03931fa08df3af7d587919537b64",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "5279ae201a4642841cd6bda73600a6e979d402e1ef3fe059c226ecd3602cd7e9",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/researches/cs_theorems.md": "32cc0824d326427cc66457b8eaed333a20b82df3269e019d52caa9fb1fccbc1e",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
INTEGRATION_MUTABLE_HASHES = {
    "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json",
}
MATHLIB_SOURCE_HASHES = {
    "Mathlib/Computability/Language.lean": "f4c3964d5713b752c02906354e5366a8367b94804b4dcdac9b07964c36bb8d2e",
    "Mathlib/Computability/DFA.lean": "d311736c5c10a198822373cddf98947a208f4870758c7148ec4ee3bab6c7d021",
    "Mathlib/Computability/NFA.lean": "6cd98626649b2041f643a1631e9ef843005993653ce5a1c797eca50cce12fd1e",
    "Mathlib/Computability/EpsilonNFA.lean": "63cec03f379e7843ad13fbfa688f11df9b2d571235f387d1071f807d88136a71",
    "Mathlib/Computability/MyhillNerode.lean": "c5e64f8def4527f5e1049d8fa5949fd004b7356326685931a91043d2983eea5e",
    "Mathlib/Computability/RegularExpressions.lean": "df6a2bcfca75fa1ad332e5aae2086851863953f83c1ba1eb7957f1bc9319d1c0",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_timestamp(value: object) -> dt.datetime:
    assert isinstance(value, str) and value
    parsed = dt.datetime.fromisoformat(value)
    assert parsed.tzinfo is not None
    return parsed


def lines_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(True)
    return hashlib.sha256("".join(lines[start - 1 : end]).encode()).hexdigest()


def canonical_manifest_sha256(entries: dict[str, str]) -> str:
    payload = "".join(f"{path}\0{digest}\n" for path, digest in sorted(entries.items()))
    return hashlib.sha256(payload.encode()).hexdigest()


def structure_input_manifest(receipt: dict) -> dict[str, str]:
    entries = {relative: SOURCE_HASHES[relative] for relative in SOURCE_HASHES}
    artifact_hashes = receipt["artifact_sha256"]
    entries.update(
        {
            f"Stage1_Instances/{THEOREM_ID}/{name}": artifact_hashes[name]
            for name in OWNED_FILES - {"intake-receipt.json"}
        }
    )
    entries.update(
        {
            f"mathlib:{relative}": digest
            for relative, digest in MATHLIB_SOURCE_HASHES.items()
        }
    )
    entries["git:repository_base_tree"] = BASE_TREE
    entries["git:mathlib_tree"] = MATHLIB_TREE
    return entries


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def git_blob_sha256(revision: str, relative: str) -> str:
    data = subprocess.check_output(
        ["git", "show", f"{revision}:{relative}"], cwd=ROOT, stderr=subprocess.DEVNULL
    )
    return hashlib.sha256(data).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    required = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert set(packet) == required
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert all(
        isinstance(command, dict)
        and isinstance(command.get("argv"), list)
        and command["argv"]
        and isinstance(command.get("exit_code"), int)
        for command in packet["commands"]
    )
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()
    assert packet["known_failures"] == receipt["known_failures"]


def check_source_hashes(instance: dict, receipt: dict) -> None:
    revisions = instance["source_revisions"]
    for relative, expected in SOURCE_HASHES.items():
        current = sha256(ROOT / relative)
        base = git_blob_sha256(BASE_REVISION, relative)
        assert base == expected, f"unexpected base input hash: {relative}"
        if relative not in INTEGRATION_MUTABLE_HASHES:
            assert current == expected, f"unexpected pinned input hash: {relative}"
        assert receipt["source_inputs"][relative] == f"sha256:{expected}"

    field_map = {
        "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
        "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
        "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
        "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
        "repository_math_source_sha256": "Docs/researches/math_theorems.md",
        "repository_computer_science_source_sha256": "Docs/researches/cs_theorems.md",
        "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
        "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    }
    for field, relative in field_map.items():
        assert revisions[field] == SOURCE_HASHES[relative], f"stale instance hash: {field}"

    mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib_root) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib_root) == MATHLIB_TREE
    for relative, expected in MATHLIB_SOURCE_HASHES.items():
        assert sha256(mathlib_root / relative) == expected, f"stale mathlib source: {relative}"


def check_receipt(receipt: dict, instance: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert isinstance(receipt["content_addressing_boundary"], str)
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["covered_task_ids"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["first_failed_gate"] == "master_acceptance_of_provisional_intake"
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["support_state"] == "provisional_worker_only"
    assert receipt["supersession_state"] == "current_unsuperseded_worker_report"
    assert receipt["revocation_state"] == "not_revoked"
    assert isinstance(receipt["review_due"], str) and receipt["review_due"]
    assert isinstance(receipt["incident_path"], str) and receipt["incident_path"]
    assert isinstance(receipt["invalidation_inputs"], list) and receipt["invalidation_inputs"]
    assert all(isinstance(value, str) and value for value in receipt["invalidation_inputs"])
    assert isinstance(receipt["attestor"], dict)
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    started = parse_timestamp(receipt["validation_started_at"])
    ended = parse_timestamp(receipt["validation_ended_at"])
    validated = parse_timestamp(receipt["validated_at"])
    assert started <= ended == validated
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        f"sha256:{LAKE_SYMLINK_TARGET_SHA256}"
    )

    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert set(receipt["artifact_sha256"]) == OWNED_FILES - {"intake-receipt.json"}
    for name, expected in receipt["artifact_sha256"].items():
        assert sha256(HERE / name) == expected, f"owned artifact hash mismatch: {name}"

    recipes = receipt["structured_validation_recipes"]
    assert isinstance(recipes, list) and len(recipes) == 2
    required_recipe_fields = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_task_ids",
        "covered_obligation_ids",
        "covered_declarations",
        "observed_exit",
    }
    for recipe in recipes:
        assert required_recipe_fields <= recipe.keys()
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        assert recipe["covered_declarations"] == []
        assert isinstance(recipe["input_hashes"], dict) and recipe["input_hashes"]
        assert recipe["stdout_sha256"].startswith("sha256:")
        assert recipe["stderr_sha256"].startswith("sha256:")
    structure, lean_probe = recipes
    assert structure["recipe_id"] == f"{ITEM_ID}-RECIPE-STRUCTURE"
    assert structure["cwd"] == "."
    assert structure["argv"] == [
        "python3",
        "-B",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
    ]
    assert structure["stdout_sha256"] == (
        "sha256:7062ba97ab17c12bae4245b5c301a558fe3706b0637a35f1402beaeb75af0a2a"
    )
    assert structure["input_hashes"]["complete_input_manifest_sha256"] == (
        f"sha256:{canonical_manifest_sha256(structure_input_manifest(receipt))}"
    )
    assert lean_probe["recipe_id"] == f"{ITEM_ID}-RECIPE-LEAN-PROBE"
    assert lean_probe["cwd"] == "Formalizations/Lean"
    assert lean_probe["argv"] == [
        "lake",
        "env",
        "lean",
        f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean",
    ]
    assert isinstance(receipt["commands_and_results"], list) and receipt["commands_and_results"]
    assert instance["accepted_receipt_ids"] == []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "自动机理论"
    assert target["category"] == instance["category"] == "数理逻辑 / 递归论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    if args.worker_packet is not None:
        assert item["state"] == "[ ]", "worker base must precede provisional integration"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "有限自动机的理论"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == revisions["repository_base_tree"] == BASE_TREE
    if args.worker_packet is not None:
        assert git("rev-parse", "HEAD") == BASE_REVISION
    else:
        subprocess.check_call(
            ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"], cwd=ROOT
        )
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == (
        revisions["repository_source_record_blob"]
    ) == SOURCE_RECORD_BLOB
    assert lines_sha256(ROOT / "Docs/researches/math_theorems.md", 5591, 5596) == (
        revisions["repository_record_block_sha256"]
    ) == SOURCE_RECORD_BLOCK_SHA256
    assert lines_sha256(ROOT / "Docs/Stage0_Blueprint.md", 20731, 20756) == (
        revisions["stage0_record_block_sha256"]
    ) == STAGE0_RECORD_BLOCK_SHA256
    assert lines_sha256(ROOT / "Docs/researches/cs_theorems.md", 224, 239) == (
        revisions["computer_science_survey_block_sha256"]
    ) == CS_SURVEY_BLOCK_SHA256
    assert revisions["mathlib"] == MATHLIB_REVISION and revisions["mathlib_tree"] == MATHLIB_TREE
    check_source_hashes(instance, receipt)

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0759-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])
    assert all(task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"] for task in dag["tasks"])
    authoritative_tasks = {
        row["id"]: row for row in execution_dag["items"] if row["theorem_id"] == THEOREM_ID
    }
    for task in dag["tasks"]:
        authoritative = authoritative_tasks[task["id"]]
        for field in (
            "phase",
            "layer",
            "depends_on",
            "owned_paths",
            "deliverable",
            "completion_gate",
        ):
            assert task[field] == authoritative[field], f"task authority drift: {task['id']} {field}"

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**自动机理论**" in catalog
    assert "- 提出者: 众多数学家" in catalog
    assert "- 时间: 20世纪" in catalog
    assert "- 陈述: 有限自动机的理论" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0759 自动机理论" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {f"THM-M-{number:04d}" for number in range(760, 767)}
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {row["theorem_id"]: row["name"] for row in instance["neighbor_target_boundaries"]}

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    check_receipt(receipt, instance, dag)
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    for name in ("README.md", "instance.json", "scope-map.md", "source-statement-crosswalk.md", "validation.md", "intake-receipt.json"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    lean = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", lean)

    lake_root = ROOT / "Formalizations/Lean/.lake"
    if args.worker_packet is not None:
        assert lake_root.is_symlink()
        assert hashlib.sha256(os.readlink(lake_root).encode()).hexdigest() == LAKE_SYMLINK_TARGET_SHA256
    else:
        assert lake_root.is_dir(), "public replay requires an existing pinned .lake directory"
    assert (lake_root / "packages/mathlib/Mathlib").is_dir()
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0759 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
