#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0623 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0623"
ITEM_ID = "S56-M-0623-INTAKE"
RANK = 1317
BASE_REVISION = "5bc32428da3d17f138ceca67f30fbc2d149da1ba"
BASE_TREE = "7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f"
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
    "mathlib_urysohn_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Metrizable/Urysohn.lean"
    ),
    "mathlib_regular_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Separation/Regular.lean"
    ),
    "mathlib_metrizable_basic_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Metrizable/Basic.lean"
    ),
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_bytes_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def line_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode()).hexdigest()


def check_text_hygiene(path: Path) -> None:
    content = path.read_bytes()
    assert content.endswith(b"\n"), f"missing final newline: {path}"
    assert not content.endswith(b"\n\n"), f"extra blank line at EOF: {path}"
    assert b"\r" not in content and b"\0" not in content, f"invalid bytes: {path}"
    for number, line in enumerate(content.splitlines(), start=1):
        assert line.rstrip() == line, f"trailing whitespace: {path}:{number}"


def check_worker_packet(path: Path, receipt: dict) -> None:
    path = path.resolve()
    check_text_hygiene(path)
    packet = load(path)
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
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def run_recorded_action(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        text=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"]
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "乌雷松度量化定理"
    assert target["category"] == instance["category"] == "拓扑学 / 点集拓扑"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "第二可数正则空间可度量化"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert formal["declaration_candidates"] == [
        "TopologicalSpace.PseudoMetrizableSpace.of_regularSpace_secondCountableTopology",
        "TopologicalSpace.metrizableSpace_of_t3_secondCountable",
    ]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert revisions["repository_record_excerpt_sha256"] == line_sha256(
        ROOT / "Docs/researches/math_theorems.md", 4622, 4627
    )
    assert revisions["stage0_projection_excerpt_sha256"] == line_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 17044, 17069
    )
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    for commit in (
        revisions["mathlib_current_split_origin_commit"],
        revisions["mathlib_original_lean4_port_commit"],
    ):
        assert git("merge-base", "--is-ancestor", commit, "HEAD", cwd=mathlib) == ""

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0623-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == [] and task["state"] == "open"
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**乌雷松度量化定理**" in catalog
    assert "- 提出者: Pavel Urysohn" in catalog
    assert "- 时间: 1925" in catalog
    assert "- 陈述: 第二可数正则空间可度量化" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0623 乌雷松度量化定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    urysohn = (ROOT / SOURCE_HASH_FIELDS["mathlib_urysohn_source_sha256"]).read_text(encoding="utf-8")
    regular = (ROOT / SOURCE_HASH_FIELDS["mathlib_regular_source_sha256"]).read_text(encoding="utf-8")
    basic = (ROOT / SOURCE_HASH_FIELDS["mathlib_metrizable_basic_source_sha256"]).read_text(encoding="utf-8")
    assert "instance (priority := 90) metrizableSpace_of_t3_secondCountable" in urysohn
    assert "PseudoMetrizableSpace.of_regularSpace_secondCountableTopology" in urysohn
    assert "Such a space is not necessarily\n  Hausdorff" in regular
    assert "class T3Space" in regular and "extends T0Space X, RegularSpace X" in regular
    assert "class MetrizableSpace" in basic and "PseudoMetrizableSpace X, T0Space X" in basic

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    for name in OWNED_FILES:
        check_text_hygiene(HERE / name)
    expected_changes = {
        ".stage1-worker-selftest.json",
        *(f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES),
    }
    assert set(receipt["changed_paths"]) == expected_changes
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
            continue
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["verdict"] == "no_state_change"
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["proof_body_locations"] == receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["selftest_result"] == "pass"
    dirty = receipt["dirty_input_evidence"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    nonrecursive_owned = [HERE / name for name in OWNED_FILES if name != "intake-receipt.json"]
    assert dirty["owned_untracked_patch_sha256"] == path_bytes_hash(nonrecursive_owned)
    assert dirty["owned_untracked_manifest_sha256"] == path_manifest_hash(nonrecursive_owned)

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {} and recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    actions = receipt["validation_actions"]
    assert {action["action_id"] for action in actions} == {
        "S56-M-0623-INTAKE-ACTION-STRUCTURE",
        "S56-M-0623-INTAKE-ACTION-LEAN-PROBE",
    }
    for action in actions:
        recipe = recipes_by_id[action["recipe_id"]]
        recipe_identity = {
            "cwd": recipe["cwd"],
            "argv": recipe["argv"],
            "env_allowlist": recipe["env_allowlist"],
            "timeout_seconds": recipe["timeout_seconds"],
            "network_policy": recipe["network_policy"],
            "expected_exit": recipe["expected_exit"],
        }
        assert action["recipe_sha256"] == canonical_json_sha256(recipe_identity)
        assert action["exit_code"] == 0
        assert action["covered_obligation_ids"] == [ITEM_ID]
    actions_by_id = {action["action_id"]: action for action in actions}
    structure_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
        HERE / "check_intake.py",
    ]
    assert actions_by_id["S56-M-0623-INTAKE-ACTION-STRUCTURE"]["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        HERE / "IntakeProbe.lean",
    ]
    assert actions_by_id["S56-M-0623-INTAKE-ACTION-LEAN-PROBE"]["input_manifest_sha256"] == path_manifest_hash(lean_inputs)
    structure_hash = hashlib.sha256(
        b"intake invariant check: ok (THM-M-0623 planned; H1/M3/R4; six open tasks)\n"
    ).hexdigest()
    assert actions_by_id["S56-M-0623-INTAKE-ACTION-STRUCTURE"]["stdout_sha256"] == structure_hash
    assert actions_by_id["S56-M-0623-INTAKE-ACTION-STRUCTURE"]["log_sha256"] == structure_hash
    assert actions_by_id["S56-M-0623-INTAKE-ACTION-LEAN-PROBE"]["stdout_sha256"] == receipt["worker_input_hashes"]["lean_probe_stdout_sha256"]
    assert actions_by_id["S56-M-0623-INTAKE-ACTION-LEAN-PROBE"]["log_sha256"] == receipt["worker_input_hashes"]["lean_probe_stdout_sha256"]
    lean_action = actions_by_id["S56-M-0623-INTAKE-ACTION-LEAN-PROBE"]
    lean_stdout = run_recorded_action(recipes_by_id[lean_action["recipe_id"]])
    lean_hash = hashlib.sha256(lean_stdout).hexdigest()
    assert lean_action["stdout_sha256"] == lean_hash
    assert lean_action["log_sha256"] == lean_hash

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for name in ("README.md", "instance.json", "scope-map.md", "source-statement-crosswalk.md", "task-dag.json", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in lean_probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0623 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
