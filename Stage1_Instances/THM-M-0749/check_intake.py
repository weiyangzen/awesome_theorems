#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0749 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0749"
ITEM_ID = "S56-M-0749-INTAKE"
RANK = 1335
BASE_REVISION = "0e5ae82e6d507ee607c3f011900571ffd8096800"
BASE_TREE = "400e6edf1f69b971b60a367e3ea29be359b07907"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MANIFEST_ENTRY_SHA256 = "3320de7c4c094d2beef9f795b1180c4bc5bc031cc95ed719a148d10632251d2e"
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
    "Docs/Stage1_Blueprint_rev-5.6.md": "de6aa1e0d959d06feb390f9938ea78e9d43008fafc16e96141483f9c198eda22",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "d811d528aa5f9a83a03f5de32ca443180218e6357c4131b50c64fc63553accac",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/researches/cs_theorems.md": "32cc0824d326427cc66457b8eaed333a20b82df3269e019d52caa9fb1fccbc1e",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCE_HASHES = {
    "Mathlib/Computability/TuringDegree.lean": "d5fd0caf5c321343ec378e2601913aec152efac58f113ce3b602dca7345b1e5c",
    "Mathlib/Computability/Halting.lean": "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de",
    "Mathlib/Computability/RecursiveIn.lean": "bc4e768b130b905c4ce57770906041da3a2c5db7aa4e4e67e3cfcbc63c153247",
}


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


def canonical_manifest_entry(target: dict) -> str:
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
            "name": "Friedberg-Muchnik定理",
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
    assert canonical_manifest_entry(target) == MANIFEST_ENTRY_SHA256
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
    assert isinstance(intake["attempts"], int) and intake["attempts"] >= 0
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
    assert instance["source_status"].startswith("H1_")
    assert "No canonical mathematical or Lean proposition" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert revisions["repository_source_record_commit"] == (
        "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
    )
    assert git(
        "rev-parse", f"{revisions['repository_source_record_commit']}:Docs/researches/math_theorems.md"
    ) == revisions["repository_math_source_record_blob"]
    assert git(
        "rev-parse", f"{revisions['repository_source_record_commit']}:Docs/researches/cs_theorems.md"
    ) == revisions["repository_cs_source_record_blob"]
    excerpt_checks = (
        ("Docs/researches/math_theorems.md", 5521, 5526, "repository_record_block_sha256"),
        ("Docs/researches/cs_theorems.md", 43, 43, "duplicate_record_block_sha256"),
        ("Docs/Stage0_Blueprint.md", 20461, 20486, "stage0_projection_block_sha256"),
        ("Docs/Stage0_Blueprint.md", 81668, 81696, "duplicate_stage0_projection_block_sha256"),
    )
    for relative, first, last, field in excerpt_checks:
        assert excerpt_sha256(ROOT / relative, first, last) == revisions[field]
    assert revisions["manifest_entry_sha256"] == MANIFEST_ENTRY_SHA256
    for path, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / path) == expected, f"changed authoritative input: {path}"
    field_map = {
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
    for field, path in field_map.items():
        assert revisions[field] == SOURCE_HASHES[path], f"stale instance hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    source_fields = {
        "mathlib_turing_degree_source_sha256": "Mathlib/Computability/TuringDegree.lean",
        "mathlib_halting_source_sha256": "Mathlib/Computability/Halting.lean",
        "mathlib_recursive_in_source_sha256": "Mathlib/Computability/RecursiveIn.lean",
    }
    for field, relative in source_fields.items():
        assert revisions[field] == MATHLIB_SOURCE_HASHES[relative]
        assert sha256(mathlib / relative) == MATHLIB_SOURCE_HASHES[relative]


def check_catalog_and_boundaries(instance: dict) -> None:
    math_catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**Friedberg-Muchnik定理**" in math_catalog
    assert "- 陈述: Post问题的肯定解" in math_catalog
    cs_catalog = (ROOT / "Docs/researches/cs_theorems.md").read_text(encoding="utf-8")
    assert "存在不可比的递归可枚举度" in cs_catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert stage0.count("THM-M-0749 Friedberg-Muchnik定理") == 1
    assert stage0.count("THM-C-0016 Friedberg-Muchnik定理") == 1
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert "- 现有 machine-checked 状态: 待补充" in stage0

    blocker = instance["statement_blocker"].lower()
    for token in (
        "primary",
        "c.e.-set model",
        "oracle transport",
        "turing reducibility",
        "ordered binders",
        "intermediate-degree",
        "boundary cases",
    ):
        assert token in blocker, f"missing ambiguity boundary: {token}"
    exclusions = " ".join(instance["excluded_substitutions"])
    for token in ("Kleene-Post", "many-one", "simple set", "TuringDegree", "verified"):
        assert token in exclusions, f"missing non-substitution boundary: {token}"
    assert instance["duplicate_source_record_boundary"]["stage0_id"] == "THM-C-0016"
    assert instance["duplicate_source_record_boundary"]["credit"].endswith("no Stage1 status, exact statement, or proof credit")
    candidates = instance["source_candidates_not_credited"]
    assert candidates[0]["candidate_locator"].endswith(
        "SHA-256 7b22369f6750805cb99b4c846d797f6bdea8ad4a0f97229b2e23e1b890e6e83e"
    )
    assert candidates[1]["candidate_locator"].endswith(
        "SHA-256 4b2fd407056cb23988dc047f77c915444151532bb5120df9813d55d576b76726"
    )


def check_task_dag(dag: dict, authoritative_items: list[dict]) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert dag["accepted_states"] == []
    tasks = dag["tasks"]
    assert [task["id"] for task in tasks] == [f"S56-M-0749-{suffix}" for suffix in TASK_SUFFIXES]
    for index, task in enumerate(tasks, start=1):
        predecessor = ITEM_ID if index == 1 else tasks[index - 2]["id"]
        assert task["layer"] == index and task["depends_on"] == [predecessor]
        assert task["state"] == "open" and task["evidence_ids"] == []
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        authority = next(row for row in authoritative_items if row["id"] == task["id"])
        for field in ("phase", "layer", "depends_on", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authority[field]
        assert authority["state"] in {"[ ]", "[_]", "[x]"}
    assert "primary statements" in tasks[0]["first_blocker"]


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["proposed_state"] == "[_]"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["known_failures"] and receipt["first_failed_theorem_gate"]
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale source input: {relative}"
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES
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
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert whitespace.returncode in (0, 1), f"no-index check failed: {path.name}"
        assert not whitespace.stdout and not whitespace.stderr
    for name in OWNED_FILES - {"IntakeProbe.lean", "check_intake.py"}:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path)
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
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    authoritative = check_authorities(instance, worker_mode=args.worker_packet is not None)
    check_instance(instance)
    check_catalog_and_boundaries(instance)
    check_task_dag(dag, authoritative)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-0749 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
