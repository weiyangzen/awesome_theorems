#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0920 planned intake."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0920"
ITEM_ID = "S56-M-0920-INTAKE"
RANK = 1462
BASE_REVISION = "46a0f2a3ea74765a0467c489264b838ffbb70675"
BASE_TREE = "7b1b5269d7da840fd086da731d6f92903c209c35"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H5", "M": "M4", "R": "R4"}
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
    "Docs/Stage1_Blueprint_Applicable_Theorems.md": "779e4bd66e6a1c7615ca2884d899f02a871096125a30b8e229536fa5937cc85c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "39fd3d1b8a928c47ba57431542ad8f5a6377a018cf2b572eade6108bace84c0f",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "24e24538046572e3f3d12496aa42f8d49b5502c3b5d168618154ab10e55eaa52",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/Combinatorics/Enumerative/Partition/Basic.lean": "365f49db37156830a0c14cf5740024dcd8bea923175d4479ee2e370fdf833a09",
    "Mathlib/Combinatorics/Enumerative/Partition/GenFun.lean": "6c100971d90ae521c717e8b2ab58b34362e365704f5e525a4c22522f3bbbc34c",
    "Mathlib/Combinatorics/Enumerative/Partition/Glaisher.lean": "1609afc1da7752036198d78304607aa7e1e55bbbbe6901fdb96385268b2602bb",
    "Mathlib/Data/Nat/ModEq.lean": "247ec25633683d05aa1b7c276d5aebeb80ed4d1db5f07aa1a536a71a3d339054",
}


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        assert key not in result, f"duplicate JSON key: {key}"
        result[key] = value
    return result


def load_json(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return sha256_bytes(b"".join(lines[first - 1 : last]))


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def canonical_entry(value: dict) -> str:
    data = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode()
    return sha256_bytes(data)


def check_authorities(instance: dict) -> None:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(targets) == len(items) == 1
    target, item = targets[0], items[0]
    assert manifest["scope"]["covered_targets"] == 1546
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "安德鲁斯分裂定理",
        "category": "组合数学 / 计数组合",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    assert canonical_entry(target) == instance["source_revisions"][
        "manifest_entry_sha256"
    ]
    assert item == {
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
    assert canonical_entry(item) == instance["source_revisions"][
        "execution_item_sha256"
    ]


def check_instance(instance: dict, dag: dict, receipt: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"]
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["execution_rank"] == RANK
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["source_status_untrusted"] == "已验证"
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert "blocked" in formal["gate_state"]
    assert instance["ordered_binders"] == instance["quantifiers"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == receipt["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is False
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert "H5 classifies" in instance["status_boundary"]
    assert "No canonical proposition" in instance["status_boundary"]


def check_sources(instance: dict) -> None:
    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for relative, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / relative) == expected, f"changed authoritative input: {relative}"
    assert revisions["target_manifest_sha256"] == SOURCE_HASHES[
        "Docs/Stage1_Targets_rev-5.6.json"
    ]
    assert revisions["applicable_targets_sha256"] == SOURCE_HASHES[
        "Docs/Stage1_Blueprint_Applicable_Theorems.md"
    ]
    assert revisions["authoritative_blueprint_sha256"] == SOURCE_HASHES[
        "Docs/Stage1_Blueprint_rev-5.6.md"
    ]
    assert revisions["execution_dag_sha256"] == SOURCE_HASHES[
        "Docs/Stage1_Execution_DAG_rev-5.6.json"
    ]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6728, 6733) == (
        revisions["repository_record_excerpt_sha256"]
    )
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 25093, 25118) == (
        revisions["stage0_projection_excerpt_sha256"]
    )
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**安德鲁斯分裂定理**") == 1
    assert catalog.count("- 陈述: 分拆函数的进一步推广") == 1
    assert "- 提出者: George Andrews" in catalog and "- 时间: 1974" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0920 安德鲁斯分裂定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    primary = revisions["primary_source_lead"]
    assert primary["doi"] == "10.1073/pnas.71.10.4082"
    assert primary["pmcid"] == "PMC434332"
    assert primary["observed_pmc_html_sha256"] == (
        "0ee84ee03b6a6275390665f2512cc544ebd80ca86f9eb7ffebea5dd68c8cf375"
    )
    assert primary["observed_pmc_html_bytes"] == 92722
    assert set(primary["observed_page_image_sha256"]) == {
        "4082", "4083", "4084", "4085"
    }
    assert set(primary["observed_page_image_bytes"]) == {
        "4082", "4083", "4084", "4085"
    }
    assert "no catalog-root adoption" in primary["credit"]
    competing = revisions["competing_source_lead"]
    assert competing["doi"] == "10.1090/memo/0152"
    assert "competing lead" in competing["credit"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == (
        revisions["mathlib_tree"]
    ) == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib)
    for relative, expected in MATHLIB_HASHES.items():
        assert sha256(mathlib / relative) == expected, f"changed mathlib input: {relative}"
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert sha256_bytes(lake_target) == revisions["lake_symlink_target_sha256"]


def check_task_dag(dag: dict, receipt: dict) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    execution = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    expected = []
    prior = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0920-{suffix}"
        source = next(row for row in execution if row["id"] == task_id)
        task = dag["tasks"][layer - 1]
        expected.append((task_id, layer, [prior]))
        assert task["id"] == task_id and task["depends_on"] == [prior]
        assert task["phase"] == source["phase"]
        assert task["layer"] == source["layer"] == layer
        assert task["owned_paths"] == source["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        prior = task_id
    assert len(dag["tasks"]) == 6
    assert [(t["id"], t["layer"], t["depends_on"]) for t in dag["tasks"]] == expected
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]


def check_receipt(receipt: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["source_inputs"] == {
        relative: f"sha256:{digest}" for relative, digest in SOURCE_HASHES.items()
    }
    for key in (
        "accepted_receipt_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["selftest_result"] == "pass"
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert isinstance(recipe["expected_outputs"], list) and recipe["expected_outputs"]
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
        for output in recipe["expected_outputs"]:
            assert set(output) == {"path_or_stream", "semantic_hash_policy"}
            assert output["path_or_stream"] and output["semantic_hash_policy"]
        assert recipe["expected_exit"] == recipe["exit_code"] == 0


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
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
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
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(
        r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe
    )
    ast.parse((HERE / "check_intake.py").read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    check_authorities(instance)
    check_instance(instance, dag, receipt)
    check_sources(instance)
    check_task_dag(dag, receipt)
    check_receipt(receipt)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print(
        "check_intake: ok (THM-M-0920 planned H5/M4/R4 intake; "
        "identity, scope, pins, receipt, and six open tasks agree)"
    )


if __name__ == "__main__":
    main()
