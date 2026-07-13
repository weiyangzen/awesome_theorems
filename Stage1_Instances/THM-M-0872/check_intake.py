#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0872 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0872"
ITEM_ID = "S56-M-0872-INTAKE"
RANK = 1426
BASE_REVISION = "748243faadc15828fb087059337fd05b7be9fdeb"
BASE_TREE = "e46d642646f80980838b6f016f5d69b817bd464d"
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
TASK_PHASES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "8b93d52d753cdb6e3462080cf7f8315c9e8a07ef921a1b93a535a5fcba41f6c2",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "fcd54bfe658aa1577667cc24b732b82d3425164fbfcad212107c0a3b696a0431",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md":
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md":
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md":
        "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/Combinatorics/SimpleGraph/Acyclic.lean":
        "94a3dad09f48c9a2b1d0dc68914f4060bec2943e2977a7cdf4e2105df7afe50a",
    "Mathlib/Computability/TuringMachine/Computable.lean":
        "acb5fa046c00afd1f85570d4439653b009b7353d7ed93aa7a6fc52dae346a59b",
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1:last])).hexdigest()


def canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def check_authorities() -> tuple[dict, list[dict]]:
    for relative, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / relative) == expected, f"stale source input: {relative}"
    target_manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(
        row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM_ID
    )
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Bodlaender算法",
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
    assert canonical_sha256(target) == (
        "b2d58d15aa37a8d982c5ac42939a303f76f6305ec39a9f675c16f94e589fd803"
    )
    execution = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    authoritative = [
        row for row in execution["items"] if row["theorem_id"] == THEOREM_ID
    ]
    assert len(authoritative) == 7
    assert canonical_sha256(authoritative) == (
        "e8bb81ae914b141632a6ea53f37a892473d280cc67435db914ce7af022f0d84c"
    )
    intake = authoritative[0]
    assert intake["id"] == ITEM_ID and intake["phase"] == "intake"
    assert intake["layer"] == 0 and intake["depends_on"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["state"] == "[ ]"
    return target, authoritative


def check_catalog(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**Bodlaender算法**" in catalog
    assert "- 提出者: Hans Bodlaender" in catalog
    assert "- 时间: 1996" in catalog
    assert "- 陈述: 树宽的线性时间近似" in catalog
    assert "- 形式化状态: 已验证" in catalog
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6390, 6395) == (
        "2b939b59567573f923845dd559b522b888ac6ee8328f32d5b449b511716e9a7c"
    )
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 23792, 23817) == (
        "10c1c68134d1123167138de6627c07f8ea265e5595cc22055928075e27b52970"
    )
    assert git("rev-parse", "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md") == (
        "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
    )
    revisions = instance["source_revisions"]
    assert revisions["repository_record_excerpt_sha256"] == (
        "2b939b59567573f923845dd559b522b888ac6ee8328f32d5b449b511716e9a7c"
    )
    assert revisions["stage0_excerpt_sha256"] == (
        "10c1c68134d1123167138de6627c07f8ea265e5595cc22055928075e27b52970"
    )


def check_instance(instance: dict, target: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["execution_rank"] == target["execution_rank"] == RANK
    assert instance["baseline"] == target["baseline"] == "L0"
    assert instance["rework_required"] is target["rework_required"] is True
    assert instance["legacy_priority_slot"] is target["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["source_status_untrusted"] == target["source_status_untrusted"]
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    assert instance["statement_blocker"] and instance["target_decision"]
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    assert formal["module"] is None and formal["declaration_or_expression"] is None
    assert formal["candidate_expression"] is None
    assert formal["elaborated_expression_hash"] is None
    assert formal["environment_fingerprint"] is None
    assert formal["gate_state"].startswith("blocked_")
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["candidate_scope_not_credited"]
    assert instance["degenerate_cases_to_resolve"] and instance["excluded_substitutions"]
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["foundation_profile"] and instance["tcb_profile"]
    assert instance["computation_profile"] and instance["owners_and_reviewers"]
    freshness = instance["freshness_and_revocation_policy"]
    assert freshness["review_due"] and freshness["invalidation_inputs"]
    assert freshness["incident_path"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION == git("rev-parse", "HEAD")
    assert revisions["repository_base_tree"] == BASE_TREE == git("rev-parse", "HEAD^{tree}")
    assert revisions["mathlib"] == MATHLIB_REVISION
    assert revisions["mathlib_tree"] == MATHLIB_TREE
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    for relative, expected in MATHLIB_HASHES.items():
        assert sha256(mathlib / relative) == expected, f"stale mathlib input: {relative}"


def check_task_dag(dag: dict, authoritative: list[dict]) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert len(dag["tasks"]) == 6
    prior = ITEM_ID
    for layer, (task, suffix) in enumerate(zip(dag["tasks"], TASK_PHASES), start=1):
        task_id = f"S56-M-0872-{suffix}"
        source = next(row for row in authoritative if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [prior]
        assert task["state"] == "open" and task["layer"] == source["layer"] == layer
        assert task["phase"] == source["phase"]
        assert task["owned_paths"] == source["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["evidence_ids"] == []
        prior = task_id


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
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
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()
    }
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path)
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
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]


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
    for name in (
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
        "intake-receipt.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    target, authoritative = check_authorities()
    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    check_instance(instance, target)
    check_catalog(instance)
    check_task_dag(dag, authoritative)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)
    print("intake invariant check: ok (THM-M-0872 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
