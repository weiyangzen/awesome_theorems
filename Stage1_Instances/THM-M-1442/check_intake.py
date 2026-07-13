#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1442"
THEOREM_ID = "THM-M-1442"
ITEM_ID = "S56-M-1442-INTAKE"
BASE_REVISION = "b4e1220a37cc10a96534cfd411e3b29523d7fd81"
BASE_TREE = "a67dd08a83c396119f4762e0ff109cd0df43ee60"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_FILES = {
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
EXPECTED_SELFTEST_KEYS = {
    "item_id",
    "changed_paths",
    "commands",
    "output_summary",
    "base_revision",
    "known_failures",
    "state",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True, stdout=subprocess.PIPE
    )
    return result.stdout.strip()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    assert set(packet) == EXPECTED_SELFTEST_KEYS
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["changed_paths"] == receipt["changed_paths"]

    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    target_data = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    targets = target_data if isinstance(target_data, list) else target_data["targets"]
    target = next(item for item in targets if item["theorem_id"] == THEOREM_ID)
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    assert target["execution_rank"] == instance["execution_rank"] == 1121
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal_target = instance["canonical_formal_target"]
    assert formal_target["module"] is None
    assert formal_target["declaration_or_expression"] is None
    assert formal_target["elaborated_expression_hash"] is None
    assert formal_target["environment_fingerprint"] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == [] and dag["theorem_complete"] is False

    expected_tasks = [
        ("S56-M-1442-STATEMENT", [ITEM_ID]),
        ("S56-M-1442-ANCHOR_AUDIT", ["S56-M-1442-STATEMENT"]),
        ("S56-M-1442-OBLIGATION_TREE", ["S56-M-1442-ANCHOR_AUDIT"]),
        ("S56-M-1442-PROOF", ["S56-M-1442-OBLIGATION_TREE"]),
        ("S56-M-1442-VALIDATION", ["S56-M-1442-PROOF"]),
        ("S56-M-1442-RELEASE", ["S56-M-1442-VALIDATION"]),
    ]
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])
    assert all(task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"] for task in dag["tasks"])

    source_revisions = instance["source_revisions"]
    assert source_revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert source_revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert source_revisions["repository_record_excerpt_sha256"] == (
        "e8ee94242c3c55e59beeb63c72c735146cb048ea0eb1957f075c42eefe6929df"
    )
    assert source_revisions["stage0_projection_excerpt_sha256"] == (
        "78c4e5e1e094f9d40482ed7584a92069b7123003d69c348fa006aba7b1bce201"
    )
    authority_hashes = {
        "target_manifest_sha256": ROOT / "Docs" / "Stage1_Targets_rev-5.6.json",
        "authoritative_blueprint_sha256": ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md",
        "execution_dag_sha256": ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json",
        "execution_skill_sha256": ROOT / "skills" / "execute-stage1-rev56" / "SKILL.md",
        "blueprint_guidelines_sha256": ROOT / "Docs" / "Blueprint_Guidelines.md",
        "repository_math_source_sha256": ROOT / "Docs" / "researches" / "math_theorems.md",
        "stage0_blueprint_sha256": ROOT / "Docs" / "Stage0_Blueprint.md",
        "lean_toolchain_file_sha256": ROOT / "Formalizations" / "Lean" / "lean-toolchain",
        "lake_manifest_sha256": ROOT / "Formalizations" / "Lean" / "lake-manifest.json",
    }
    for field, path in authority_hashes.items():
        assert source_revisions[field] == sha256(path), f"stale input hash: {field}"
    math_source = (ROOT / "Docs" / "researches" / "math_theorems.md").read_bytes().splitlines(True)
    stage0 = (ROOT / "Docs" / "Stage0_Blueprint.md").read_bytes().splitlines(True)
    assert hashlib.sha256(b"".join(math_source[10531:10537])).hexdigest() == (
        source_revisions["repository_record_excerpt_sha256"]
    )
    assert hashlib.sha256(b"".join(stage0[39216:39242])).hexdigest() == (
        source_revisions["stage0_projection_excerpt_sha256"]
    )
    assert source_revisions["mathlib"] == MATHLIB_REVISION
    assert source_revisions["mathlib_tree"] == MATHLIB_TREE
    mathlib = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == EXPECTED_FILES
    assert set(instance["owned_artifacts"]) == EXPECTED_FILES
    expected_merge_targets = {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in EXPECTED_FILES}
    assert set(instance["public_merge_targets"]) == expected_merge_targets

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "intake" and receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["selftest_result"] == "pass"
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["covered_node_ids"] == [ITEM_ID]
    for key in (
        "covered_declaration_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
        "accepted_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task[0] for task in expected_tasks]

    changed_paths = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(EXPECTED_FILES)
    ]
    assert receipt["changed_paths"] == changed_paths

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data, f"non-LF newline: {path.name}"
        assert b"\x00" not in data, f"NUL byte: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    hashed_artifacts = receipt["owned_artifact_sha256"]
    assert set(hashed_artifacts) == EXPECTED_FILES - {"intake-receipt.json", "check_intake.py"}
    for name, expected in hashed_artifacts.items():
        assert sha256(HERE / name) == expected, f"owned artifact hash mismatch: {name}"

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-1442 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
