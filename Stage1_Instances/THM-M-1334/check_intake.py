#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-1334."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1334"
ITEM_ID = "S56-M-1334-INTAKE"
RANK = 945
BASE_REVISION = "bbb685ee4adcd9f19b5a727d1523cc7d6ad3b07f"
BASE_TREE = "aadea0300fd76d31a98264ab39039d2247f8e049"
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
EXPECTED_INPUT_HASHES = {
    "target_manifest_sha256": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "authoritative_blueprint_sha256": "2601660d860644ad0c8b5fad21821bcef2d90aadbec33b515ede8a97bca2ef75",
    "execution_dag_sha256": "a7bd241618ba853e5c8c42e2d4b1f9813ddaaf17275cb877401abccf939d6263",
    "execution_skill_sha256": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "blueprint_guidelines_sha256": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "repository_math_source_sha256": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "stage0_blueprint_sha256": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "lean_toolchain_file_sha256": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake_manifest_sha256": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_COMMAND_SIGNATURES = [
    ("argv", ("python3", "Docs/tools/check_stage1_standard.py"), 0),
    ("argv", ("python3", "scripts/stage1_target.py", "check"), 0),
    ("argv", ("python3", "scripts/stage1_target.py", "show", THEOREM_ID), 0),
    ("argv", ("git", "status", "--short", "--untracked-files=all"), 0),
    ("argv", ("git", "blame", "-L", "9733,9738", "--", "Docs/researches/math_theorems.md"), 0),
    ("shell_command", None, 0),
    ("shell_command", None, 0),
    ("shell_command", None, 0),
    ("argv", ("curl", "-L", "--max-time", "30", "-A", "Mozilla/5.0", "-sS", "-o", "/tmp/thm-m-1334-historical.html", "-w", "%{http_code} %{content_type} %{size_download}\\n", "https://doi.org/10.1515/crll.1875.80.1"), 0),
    ("argv", ("lake", "env", "lean", "--version"), 0),
    ("argv", ("git", "-C", "Formalizations/Lean/.lake/packages/mathlib", "rev-parse", "HEAD", "HEAD^{tree}"), 0),
    ("argv", ("sha256sum", "Formalizations/Lean/lean-toolchain", "Formalizations/Lean/lake-manifest.json"), 0),
    ("argv", ("lake", "env", "lean", "../../Stage1_Instances/THM-M-1334/IntakeProbe.lean"), 0),
    ("argv", ("rg", "-n", "-i", "--glob", "*.lean", "cauchy.{0,3}(kowalev|kovalev)|kowalevsk|kovalevsk", "Formalizations/Lean/AwesomeTheorems", "Formalizations/Lean/.lake/packages/mathlib/Mathlib"), 1),
    ("shell_command", None, 0),
    ("argv", ("python3", "-c", "import ast; from pathlib import Path; ast.parse(Path('Stage1_Instances/THM-M-1334/check_intake.py').read_text(encoding='utf-8'))"), 0),
    ("argv", ("python3", "-B", "Stage1_Instances/THM-M-1334/check_intake.py", "--worker-packet", ".stage1-worker-selftest.json"), 0),
    ("argv", ("rg", "-n", "--glob", "*.lean", "\\b(sorry|admit)\\b|\\bsorryAx\\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\\b", "Stage1_Instances/THM-M-1334"), 1),
    ("shell_command", None, 0),
]
EXPECTED_SHELL_FRAGMENTS = [
    "https://arxiv.org/pdf/1912.03836v3",
    "https://api.crossref.org/works/10.1007/s11784-020-00841-1",
    "https://api.crossref.org/works/10.1515/crll.1875.80.1",
    "python3 -m json.tool Stage1_Instances/THM-M-1334/instance.json",
    "git diff --check -- Stage1_Instances/THM-M-1334",
]
INPUT_PATHS = {
    "target_manifest_sha256": ROOT / "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": ROOT / "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": ROOT / "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": ROOT / "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": ROOT / "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": ROOT / "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": ROOT / "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": ROOT / "Formalizations/Lean/lake-manifest.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    assert packet["item_id"] == ITEM_ID
    assert packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake"
    assert packet["verdict"] == receipt["verdict"] == "no_state_change"
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["commands"] == receipt["commands_and_results"]
    assert all(("argv" in command) ^ ("shell_command" in command) for command in packet["commands"])
    assert len(packet["commands"]) == len(EXPECTED_COMMAND_SIGNATURES)
    for command, (kind, expected_argv, expected_exit) in zip(
        packet["commands"], EXPECTED_COMMAND_SIGNATURES, strict=True
    ):
        assert kind in command and command["exit_code"] == expected_exit
        if expected_argv is not None:
            assert tuple(command["argv"]) == expected_argv
    shell_commands = [command["shell_command"] for command in packet["commands"] if "shell_command" in command]
    assert len(shell_commands) == len(EXPECTED_SHELL_FRAGMENTS)
    assert all(fragment in command for fragment, command in zip(EXPECTED_SHELL_FRAGMENTS, shell_commands, strict=True))
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is False
    assert packet["theorem_complete"] is False
    assert packet["known_failures"] == receipt["known_failures"]


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
    assert target["name"] == instance["name_zh"] == "柯西-科瓦列夫斯卡娅定理"
    assert target["category"] == "微分方程 / 常微分方程"
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 108
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
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
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False

    expected_tasks = [f"S56-M-1334-{suffix}" for suffix in TASK_SUFFIXES]
    assert [task["id"] for task in dag["tasks"]] == expected_tasks
    dependency = ITEM_ID
    for task in dag["tasks"]:
        assert task["state"] == "open"
        assert task["depends_on"] == [dependency]
        dependency = task["id"]

    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == expected_tasks
    recipes = receipt["structured_validation_recipes"]
    assert [recipe["recipe_id"] for recipe in recipes] == [
        "S56-M-1334-INTAKE-RECIPE-STRUCTURE",
        "S56-M-1334-INTAKE-RECIPE-LEAN-PROBE",
    ]
    required_recipe_keys = {
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
        "covered_node_ids",
    }
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["covered_node_ids"] == [ITEM_ID] for recipe in recipes)

    hashed_files = OWNED_FILES - {"intake-receipt.json"}
    assert set(receipt["untracked_owned_artifact_sha256"]) == hashed_files
    for name in hashed_files:
        assert receipt["untracked_owned_artifact_sha256"][name] == sha256(HERE / name), name

    recorded = instance["source_revisions"]
    for key, expected in EXPECTED_INPUT_HASHES.items():
        assert recorded[key] == expected
        assert sha256(INPUT_PATHS[key]) == expected, key

    hygiene_paths = [path for path in HERE.iterdir() if path.is_file()]
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
        hygiene_paths.append(args.worker_packet)
    for path in hygiene_paths:
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data, f"non-LF newline: {path.name}"
        for line in data.splitlines():
            assert not line.endswith((b" ", b"\t")), f"trailing whitespace: {path.name}"

    print("intake invariant check: ok")


if __name__ == "__main__":
    main()
