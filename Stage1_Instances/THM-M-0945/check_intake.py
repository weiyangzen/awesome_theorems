#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0945."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0945"
ITEM_ID = "S56-M-0945-INTAKE"
RANK = 1484
BASE_REVISION = "a3b18eec39bf04be025b1641cae02f4d44fdf11a"
BASE_TREE = "fdfff18dea4c6798c5b322b6088dfe556109c134"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
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
SOURCE_HASH_PATHS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    "nat_prime_infinite_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Nat/Prime/Infinite.lean"
    ),
    "nat_prime_fin_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Nat/PrimeFin.lean"
    ),
    "three_ap_defs_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/Additive/AP/Three/Defs.lean"
    ),
    "roth_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/Additive/Corner/Roth.lean"
    ),
    "hales_jewett_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/HalesJewett.lean"
    ),
}
PROBE_DECLARATIONS = [
    "Nat.Prime",
    "Nat.exists_infinite_primes",
    "Nat.infinite_setOf_prime",
    "ThreeAPFree",
    "roth_3ap_theorem_nat",
    "rothNumberNat_isLittleO_id",
    "Combinatorics.Line.exists_mono_in_high_dimension",
    "Combinatorics.exists_mono_homothetic_copy",
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1 : last])).hexdigest()


def canonical_json_sha256(value: object) -> str:
    data = (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(data).hexdigest()


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


def check_authorities(instance: dict, dag: dict) -> list[dict]:
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Green-Tao定理",
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
    assert canonical_json_sha256(target) == instance["source_revisions"]["manifest_entry_sha256"]
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

    items = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    intake = next(row for row in items if row["id"] == ITEM_ID)
    assert intake["theorem_id"] == THEOREM_ID and intake["execution_rank"] == RANK
    assert intake["phase"] == "intake" and intake["layer"] == 0
    assert intake["state"] == "[ ]" and intake["depends_on"] == []
    assert intake["attempts"] == 0 and intake["children"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["audit_complete"] is dag["theorem_complete"] is False
    assert dag["accepted_states"] == []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0945-{suffix}"
        task = dag["tasks"][layer - 1]
        authority = next(row for row in items if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["evidence_ids"] == []
        for field in ("phase", "layer", "depends_on", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authority[field]
        assert authority["state"] == "[ ]"
        dependency = task_id
    assert len(dag["tasks"]) == 6
    return items


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "theorem_1_1_identified" in instance["canonical_claim_status"]
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
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["source_status"].startswith("H1_")
    assert "No canonical mathematical or Lean proposition" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    source_commit = revisions["repository_source_record_commit"]
    assert git("rev-parse", f"{source_commit}:Docs/researches/math_theorems.md") == (
        revisions["repository_source_record_blob"]
    )
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 6903, 6908) == (
        revisions["repository_record_block_sha256"]
    )
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 25768, 25793) == (
        revisions["stage0_projection_block_sha256"]
    )
    for field, relative in SOURCE_HASH_PATHS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"]
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"]
    assert git("status", "--short", cwd=mathlib) == ""

    source = instance["primary_source_candidates_not_credited"][0]
    assert source["doi"] == "10.4007/annals.2008.167.481"
    assert source["theorem_locator"].startswith("Theorem 1.1, printed page 482")
    assert source["observed_pdf_sha256"] == (
        "967dd6f5bb53d70abdbb07be0afe59e60b2a232e2c3387966013a09960e52c89"
    )
    assert source["observed_pdf_size_bytes"] == 488947 and source["observed_pdf_pages"] == 67


def check_catalog_and_scope(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Green-Tao定理**") == 1
    assert "- 提出者: Ben Green/Terence Tao" in catalog
    assert "- 时间: 2004" in catalog
    assert "- 陈述: 素数包含任意长的等差数列" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0945 Green-Tao定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert "- 现有 machine-checked 状态: 待补充" in stage0

    blocker = instance["statement_blocker"].lower()
    for token in (
        "small cases for k",
        "nat versus positive-integer primes",
        "arithmetic-progression witness",
        "positive common difference",
        "infinitely-many strength",
        "ordered binders",
        "errata",
        "independent review",
    ):
        assert token in blocker, f"missing statement boundary: {token}"
    excluded = " ".join(instance["excluded_substitutions"])
    for token in ("Dirichlet", "THM-M-0947", "THM-M-0948", "THM-M-0946", "Theorem 1.2", "已验证"):
        assert token in excluded, f"missing exclusion: {token}"
    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0479", "THM-M-0946", "THM-M-0947", "THM-M-0948"}


def check_receipt(receipt: dict, instance: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["proposed_state"] == "[_]"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at == validated_at <= datetime.now(timezone.utc).astimezone()
    assert receipt["root_vector_before"] == {"H": "unclassified", "M": "unclassified", "R": "unclassified"}
    assert receipt["root_vector_after"] == ROOT_VECTOR == instance["root_vector"]
    assert receipt["lifecycle_before"] == "no_instance_at_L0_baseline"
    assert receipt["lifecycle_after"] == "planned"
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["covered_task_ids"] == receipt["covered_node_ids"] == [ITEM_ID]
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
    dirty = receipt["dirty_input_evidence"]
    assert dirty["preflight_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    digest_paths = [HERE / name for name in OWNED_FILES if name != "intake-receipt.json"]
    assert dirty["owned_untracked_patch_sha256"] == path_bytes_hash(digest_paths)
    assert dirty["owned_untracked_manifest_sha256"] == path_manifest_hash(digest_paths)

    for relative, tagged in receipt["source_inputs"].items():
        assert tagged == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    artifacts = receipt["nonrelease_artifact_inputs"]
    assert set(artifacts["artifact_sha256"]) == OWNED_FILES - {"intake-receipt.json"}
    for name, digest in artifacts["artifact_sha256"].items():
        assert digest == sha256(HERE / name), f"stale owned artifact hash: {name}"

    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    lake_hash = hashlib.sha256(str(lake.readlink()).encode()).hexdigest()
    assert receipt["worker_input_hashes"]["lake_symlink_target_string_sha256"] == lake_hash
    assert receipt["worker_input_hashes"]["mathlib_revision"] == instance["source_revisions"]["mathlib"]
    assert receipt["worker_input_hashes"]["mathlib_tree"] == instance["source_revisions"]["mathlib_tree"]
    executable_hashes = receipt["tool_executable_sha256"]
    assert set(executable_hashes) == {"lean", "lake", "python3", "git", "rg"}
    for tool, record in executable_hashes.items():
        assert set(record) == {"resolution_method", "sha256"}
        assert record["resolution_method"] == (
            "PATH lookup via bash -lc command -v; absolute host path intentionally omitted"
        )
        resolved = subprocess.check_output(["bash", "-lc", f"command -v {tool}"], text=True).strip()
        assert record["sha256"] == sha256(Path(resolved))

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
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
    for recipe in recipes:
        assert set(recipe) == recipe_keys
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
        assert recipe["expected_outputs"]
    assert recipes[0]["argv"] == ["python3", "-B", "Stage1_Instances/THM-M-0945/check_intake.py"]
    assert recipes[1]["argv"] == ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0945/IntakeProbe.lean"]
    assert recipes[1]["covered_declarations"] == PROBE_DECLARATIONS

    assert receipt["diff_summary"].startswith("Created a nine-file")
    assert receipt["exact_statement_change"].startswith("No exact mathematical or Lean statement")
    assert receipt["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"]
    assert receipt["declaration_ownership"] == []
    assert receipt["readable_ownership"] == [
        f"Stage1_Instances/{THEOREM_ID}/README.md",
        f"Stage1_Instances/{THEOREM_ID}/scope-map.md",
        f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
        f"Stage1_Instances/{THEOREM_ID}/validation.md",
    ]
    assert receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["source_revision_and_proof_body_summary"].startswith("Repository catalog provenance")
    assert receipt["ownership_and_change_impact"].startswith("Only Stage1_Instances/THM-M-0945")


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES, f"unexpected owned artifact inventory: {sorted(actual)}"
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in OWNED_FILES - {"IntakeProbe.lean", "check_intake.py"}:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for token in ("sorry", "admit", "sorryAx", "axiom", "constant", "opaque", "unsafe"):
        assert token not in probe


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
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()
    assert receipt["dirty_input_evidence"]["worker_packet_sha256"] == sha256(path.resolve())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    check_authorities(instance, dag)
    check_instance(instance)
    check_catalog_and_scope(instance)
    check_receipt(receipt, instance, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    assert platform.system() == receipt["platform"]["operating_system"]
    assert platform.machine() == receipt["platform"]["architecture"]
    print("intake invariant check: ok (THM-M-0945 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
