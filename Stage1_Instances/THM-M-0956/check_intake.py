#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0956 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0956"
ITEM_ID = "S56-M-0956-INTAKE"
BASE_REVISION = "a3b18eec39bf04be025b1641cae02f4d44fdf11a"
BASE_TREE = "fdfff18dea4c6798c5b322b6088dfe556109c134"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
    "Docs/Stage1_Blueprint_Applicable_Theorems.md": "779e4bd66e6a1c7615ca2884d899f02a871096125a30b8e229536fa5937cc85c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "75e29c1ae280b75e6a1b78c3658106332686beb1f9650f11d30c8624855233c4",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "603f3aa25a89d483dfbd0c40ccea727937dd4630feab2773b19a124377178b39",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path.resolve())
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
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert isinstance(packet["known_failures"], list) and packet["known_failures"]
    assert packet["known_failures"] == receipt["known_failures"]
    expected = {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    expected.add(".stage1-worker-selftest.json")
    assert set(packet["changed_paths"]) == expected
    assert set(receipt["changed_paths"]) == expected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    authority_dag = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)

    assert target["execution_rank"] == instance["execution_rank"] == 1490
    assert target["name"] == instance["name_zh"] == "Erdős-Turán构造"
    assert target["category"] == instance["category"] == "组合数学 / 计数组合"
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is instance["theorem_complete"] is False
    assert instance["item_id"] == ITEM_ID and instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    assert formal["module"] is None and formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is None
    assert formal["environment_fingerprint"] is None
    assert not instance["ordered_binders"] and not instance["quantifiers"]
    assert not instance["hypotheses"] and not instance["alternate_encodings"]
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert not instance["accepted_proof_state"] and not instance["accepted_receipt_ids"]
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert set(instance["owned_artifacts"]) == OWNED_FILES

    expected_ids = [
        "S56-M-0956-STATEMENT",
        "S56-M-0956-ANCHOR_AUDIT",
        "S56-M-0956-OBLIGATION_TREE",
        "S56-M-0956-PROOF",
        "S56-M-0956-VALIDATION",
        "S56-M-0956-RELEASE",
    ]
    assert dag["theorem_id"] == THEOREM_ID and dag["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == "planned"
    assert dag["theorem_complete"] is False and not dag["accepted_states"]
    assert [task["id"] for task in dag["tasks"]] == expected_ids
    assert [task["layer"] for task in dag["tasks"]] == list(range(1, 7))
    assert all(task["state"] == "open" and not task["evidence"] for task in dag["tasks"])
    assert dag["tasks"][0]["depends_on"] == [ITEM_ID]
    for previous, current in zip(dag["tasks"], dag["tasks"][1:]):
        assert current["depends_on"] == [previous["id"]]
    authority_rows = [row for row in authority_dag["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(authority_rows) == 7
    intake_row = authority_rows[0]
    assert intake_row["id"] == ITEM_ID and intake_row["phase"] == "intake"
    assert intake_row["layer"] == 0 and intake_row["state"] == "[ ]"
    assert not intake_row["depends_on"]
    assert intake_row["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    for local, authority in zip(dag["tasks"], authority_rows[1:]):
        for key in (
            "id",
            "phase",
            "layer",
            "depends_on",
            "owned_paths",
            "deliverable",
            "completion_gate",
        ):
            assert local[key] == authority[key], f"DAG authority mismatch: {local['id']} {key}"

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert not receipt["accepted_receipt_ids"] and not receipt["proof_body_locations"]
    assert not receipt["canonical_obligation_ids"] and not receipt["statement_fingerprints"]
    assert receipt["remaining_root_cut_set"] == expected_ids
    assert receipt["selftest_result"] == "pass" and receipt["verdict"] == "no_state_change"

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert revisions["mathlib"] == MATHLIB_REVISION
    assert revisions["mathlib_tree"] == MATHLIB_TREE
    lines = (ROOT / "Docs/researches/math_theorems.md").read_bytes().splitlines(keepends=True)
    excerpt = b"".join(lines[6979:6985])
    assert hashlib.sha256(excerpt).hexdigest() == revisions["repository_record_excerpt_sha256"]
    for relative, digest in SOURCE_HASHES.items():
        assert sha256(ROOT / relative) == digest, f"stale source input: {relative}"
        assert receipt["source_inputs"][relative] == f"sha256:{digest}"
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    )
    for relative, tagged_digest in receipt["untracked_artifact_sha256"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", (
            f"stale worker artifact: {relative}"
        )

    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert recipe["covered_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
    structure_recipe, lean_recipe = receipt["structured_validation_recipes"]
    assert structure_recipe["argv"] == [
        "python3",
        "-B",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
    ]
    assert lean_recipe["covered_declarations"] == [
        "Finset",
        "Finset.Icc",
        "Finset.card",
        "Finset.image",
        "Set.Pairwise",
        "Set.InjOn",
        "Finset.sum",
        "Nat.sqrt",
    ]
    actions = receipt["validation_actions"]
    assert [action["recipe_id"] for action in actions] == [
        structure_recipe["recipe_id"],
        lean_recipe["recipe_id"],
    ]
    assert all(
        action["exit_code"] == 0 and action["started_at"] <= action["ended_at"]
        for action in actions
    )

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md",
        "instance.json",
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/" + "home/" not in text and "." + "cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0956 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
