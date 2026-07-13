#!/usr/bin/env python3
"""Fail-closed structural replay for the THM-M-0820 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0820"
ITEM_ID = "S56-M-0820-INTAKE"
RANK = 1378
BASE_REVISION = "902d9ce008e88a35a2307c85355560a230cc33c2"
BASE_TREE = "dfc20d8141f18f6b09a03e818acfff408e836714"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SUCCESS = "intake invariant check: ok (THM-M-0820 planned; H1/M3/R4; six open tasks)\n"
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
    "mathlib_antichain_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Order/Antichain.lean"
    ),
    "mathlib_height_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Order/Height.lean"
    ),
    "mathlib_finpartition_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Order/Partition/Finpartition.lean"
    ),
    "mathlib_relseries_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Order/RelSeries.lean"
    ),
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path}"
    )


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    check_text_file(path.resolve())
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
    assert packet["commands"] == receipt["worker_packet_commands"]
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
    assert len(targets) == 1
    target = targets[0]
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Mirsky定理",
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
    assert canonical_sha256(target) == instance["source_revisions"][
        "target_entry_canonical_sha256"
    ]

    items = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(items) == 7
    intake = next(row for row in items if row["id"] == ITEM_ID)
    assert intake["execution_rank"] == RANK
    assert intake["phase"] == "intake" and intake["layer"] == 0
    assert intake["state"] == "[ ]" and intake["depends_on"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["execution_rank"] == RANK
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["root_vector_status"] == "proposed_pending_master_acceptance"
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert revisions["repository_source_record_commit"] == (
        "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
    )
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    assert git("hash-object", "Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("hash-object", "Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(
        encoding="utf-8"
    ).splitlines(True)
    assert hashlib.sha256("".join(source_lines[6025:6031]).encode()).hexdigest() == revisions[
        "repository_record_excerpt_sha256"
    ]
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(
        encoding="utf-8"
    ).splitlines(True)
    assert hashlib.sha256("".join(stage0_lines[22387:22413]).encode()).hexdigest() == revisions[
        "stage0_projection_excerpt_sha256"
    ]
    assert revisions["singh_arxiv_pdf_sha256"] == (
        "929c77c123421d5bade2ccfc4e40085afe827f558bf8661d16977c9581c46d8a"
    )
    assert revisions["mirsky_crossref_response_sha256"] == (
        "65039965eefb0bf1c1b971310423b63102936848872211aa6ffd042000681dd1"
    )
    assert "Semantic Scholar" not in json.dumps(instance, ensure_ascii=False)

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib source is dirty"
    for key, relative in (
        ("mathlib_antichain_source_blob", "Mathlib/Order/Antichain.lean"),
        ("mathlib_height_source_blob", "Mathlib/Order/Height.lean"),
        ("mathlib_finpartition_source_blob", "Mathlib/Order/Partition/Finpartition.lean"),
        ("mathlib_relseries_source_blob", "Mathlib/Order/RelSeries.lean"),
    ):
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == revisions[key]

    authoritative = {row["id"]: row for row in items}
    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0820-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        auth = authoritative[task_id]
        assert task["phase"] == auth["phase"] and task["layer"] == auth["layer"] == layer
        assert task["owned_paths"] == auth["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == auth["deliverable"]
        assert task["completion_gate"] == auth["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Mirsky定理**") == 1
    assert "- 提出者: Leon Mirsky" in catalog
    assert "- 时间: 1971" in catalog
    assert "- 陈述: 偏序集分解为反链的最小数目" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0820 Mirsky定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    neighbor_names = {row["theorem_id"]: row["name"] for row in manifest["targets"]}
    for row in instance["neighbor_target_boundaries"]:
        assert neighbor_names[row["theorem_id"]] == row["name"]

    actual_artifacts = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_artifacts == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    status_paths = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
    }
    assert status_paths == expected_changed | {"Formalizations/Lean/.lake"}

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at == validated_at <= datetime.now(timezone.utc).astimezone()
    assert receipt["selftest_result"] == "pass"
    for relative, tagged_hash in receipt["source_inputs"].items():
        assert tagged_hash == f"sha256:{sha256(ROOT / relative)}"
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert recipe["expected_outputs"]
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []

    receipt_hashes = receipt["owned_artifact_sha256"]
    assert set(receipt_hashes) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for relative, digest in receipt_hashes.items():
        if relative.endswith("/intake-receipt.json"):
            assert digest == "self_referential_excluded_from_provisional_digest"
        else:
            assert digest == sha256(ROOT / relative), f"stale artifact hash: {relative}"

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)
    for name in (
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "validation.md",
        "intake-receipt.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    assert "minimum over admissible covers" in crosswalk
    assert "minimum over admissible partitions" not in crosswalk
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)
    assert (ROOT / "Formalizations/Lean/.lake").is_symlink()
    assert not git(
        "status",
        "--short",
        "--",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "Docs/Stage1_Blueprint_rev-5.6.md",
    )

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print(SUCCESS, end="")


if __name__ == "__main__":
    main()
