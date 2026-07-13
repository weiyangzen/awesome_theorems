#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0841 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


THEOREM_ID = "THM-M-0841"
ITEM_ID = "S56-M-0841-INTAKE"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
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
    "Docs/Stage1_Blueprint_rev-5.6.md": "ed5d9ee7195e64cf30505638068c9b030aac5d424dd9ac9d009fee822201211b",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "31931ede528f702ccf7765dbfaca1e65e6a82029f275aab8b4a966ad6e6ef07c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_bytes_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda value: value.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda value: value.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def tracked_blob(path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def git_text(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


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
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == OWNED_FILES, (actual_files, OWNED_FILES)

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    targets = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == 1398
    assert target["name"] == instance["name_zh"] == "Erdős-Stone定理"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    node = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert node["theorem_id"] == THEOREM_ID
    assert node["execution_rank"] == 1398
    assert node["phase"] == "intake" and node["layer"] == 0 and node["state"] == "[ ]"
    assert node["depends_on"] == []
    assert node["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert node["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert node["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    formal_target = instance["canonical_formal_target"]
    assert formal_target["module"] is None
    assert formal_target["declaration_or_expression"] is None
    assert formal_target["elaborated_expression_hash"] is None
    assert formal_target["environment_fingerprint"] is None
    assert formal_target["pinned_exact_conclusion_candidate"] is None
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False
    assert instance["theorem_complete"] is False
    assert instance["owned_artifacts"] == [
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "IntakeProbe.lean",
        "check_intake.py",
        "validation.md",
        "intake-receipt.json",
    ]

    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    tasks = dag["tasks"]
    phases = ["STATEMENT", "ANCHOR_AUDIT", "OBLIGATION_TREE", "PROOF", "VALIDATION", "RELEASE"]
    assert [task["id"] for task in tasks] == [f"S56-M-0841-{phase}" for phase in phases]
    assert [task["layer"] for task in tasks] == list(range(1, 7))
    assert all(task["state"] == "open" for task in tasks)
    assert tasks[0]["depends_on"] == [ITEM_ID]
    assert all(
        tasks[index]["depends_on"] == [tasks[index - 1]["id"]]
        for index in range(1, len(tasks))
    )
    assert all(task["covered_obligation_ids"] == [] for task in tasks)
    assert all(task["evidence_ids"] == [] for task in tasks)

    assert receipt["theorem_id"] == THEOREM_ID and receipt["item_id"] == ITEM_ID
    assert receipt["intent"] == "intake" and receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["statement_fingerprints"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert set(receipt["changed_paths"]) == {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in tasks]
    assert receipt["known_failures"] and all(
        isinstance(failure, str) and failure for failure in receipt["known_failures"]
    )
    dirty = receipt["dirty_input_evidence"]
    expected_changed = receipt["changed_paths"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert dirty["owned_untracked_paths"] == expected_changed
    digest_paths = [HERE / name for name in OWNED_FILES if name != "intake-receipt.json"]
    assert dirty["owned_untracked_patch_sha256"] == path_bytes_hash(digest_paths)
    assert dirty["owned_untracked_manifest_sha256"] == path_manifest_hash(digest_paths)
    packet_path = ROOT / ".stage1-worker-selftest.json"
    assert dirty["worker_packet_sha256"] == sha256(packet_path)
    artifact_hashes = receipt["owned_artifact_sha256"]
    assert artifact_hashes[f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"] == (
        "self_referential_excluded_from_provisional_digest"
    )
    for path in digest_paths:
        relative = path.relative_to(ROOT).as_posix()
        assert artifact_hashes[relative] == sha256(path)
    assert set(artifact_hashes) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert receipt["base_revision"] == instance["source_revisions"]["repository_base"] == git_text("rev-parse", "HEAD")
    assert receipt["base_tree"] == instance["source_revisions"]["repository_base_tree"] == git_text(
        "rev-parse", "HEAD^{tree}"
    )

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert instance["source_revisions"]["mathlib"] == git_text("rev-parse", "HEAD", cwd=mathlib)
    assert instance["source_revisions"]["mathlib_tree"] == git_text(
        "rev-parse", "HEAD^{tree}", cwd=mathlib
    )
    assert git_text("status", "--short", cwd=mathlib) == ""
    for field, relative in {
        "mathlib_turan_density_sha256": "Mathlib/Combinatorics/SimpleGraph/Extremal/TuranDensity.lean",
        "mathlib_complete_multipartite_sha256": "Mathlib/Combinatorics/SimpleGraph/CompleteMultipartite.lean",
        "mathlib_coloring_sha256": "Mathlib/Combinatorics/SimpleGraph/Coloring.lean",
    }.items():
        assert instance["source_revisions"][field] == sha256(mathlib / relative)

    for path, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / path) == expected, path
        assert receipt["source_inputs"][path] == f"sha256:{expected}"

    assert hashlib.sha256(tracked_blob("Docs/researches/math_theorems.md")).hexdigest() == SOURCE_HASHES[
        "Docs/researches/math_theorems.md"
    ]
    revisions = instance["source_revisions"]
    assert revisions["repository_source_record_current_blob"] == git_text(
        "rev-parse", "HEAD:Docs/researches/math_theorems.md"
    )
    assert revisions["repository_source_record_origin_blob"] == git_text(
        "rev-parse",
        f"{revisions['repository_source_record_commit']}:Docs/researches/math_theorems.md",
    )
    assert receipt["source_evidence"]["repository_source_record_origin_blob"] == revisions[
        "repository_source_record_origin_blob"
    ]
    assert receipt["source_evidence"]["repository_source_record_current_blob"] == revisions[
        "repository_source_record_current_blob"
    ]
    excerpt = "\n".join(
        [
            "**Erdős-Stone定理**",
            "- 提出者: Erdős/Stone",
            "- 时间: 1946",
            "- 陈述: 极值图论的基本定理",
            "- 重要性: 高",
            "- 形式化状态: 已验证",
            "",
        ]
    ).encode()
    assert hashlib.sha256(excerpt).hexdigest() == instance["source_revisions"][
        "repository_record_excerpt_sha256"
    ]

    expected_recipes = receipt["structured_validation_recipes"]
    recipe_keys = {
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
    assert len(expected_recipes) == 2
    assert len({recipe["recipe_id"] for recipe in expected_recipes}) == 2
    assert all(set(recipe) == recipe_keys for recipe in expected_recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in expected_recipes)
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in expected_recipes)
    assert all(recipe["expected_outputs"] for recipe in expected_recipes)
    structure = next(recipe for recipe in expected_recipes if recipe["recipe_id"].endswith("STRUCTURE"))
    assert structure["cwd"] == "."
    assert structure["argv"] == [
        "python3",
        "-B",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
    ]
    lean = next(recipe for recipe in expected_recipes if recipe["recipe_id"].endswith("LEAN-PROBE"))
    assert lean["cwd"] == "Formalizations/Lean"
    assert lean["argv"] == [
        "lake",
        "env",
        "lean",
        f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean",
    ]
    assert all(recipe["network_policy"] == "denied" for recipe in expected_recipes)

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

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
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0841 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
