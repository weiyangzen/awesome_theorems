#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0877"
BASE = "748243faadc15828fb087059337fd05b7be9fdeb"
BASE_TREE = "e46d642646f80980838b6f016f5d69b817bd464d"
MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
TARGET_EXCERPT_SHA256 = "fead24a2dd6923f74d5d9aca3a2549931d9c97676e61c13fc0e62ce4556e09a1"
STAGE0_EXCERPT_SHA256 = "92e32d205102eb05a00f9a51d5786a9532c517f8cc3a516dda0509d065bcb3e2"
MANIFEST_ENTRY_SHA256 = "49da9e89df882c675a747a4a1f00156fb9e47eae4ead54cb0d30c4d709e0a961"
WORKER_SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_Applicable_Theorems.md": "779e4bd66e6a1c7615ca2884d899f02a871096125a30b8e229536fa5937cc85c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "8b93d52d753cdb6e3462080cf7f8315c9e8a07ef921a1b93a535a5fcba41f6c2",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "fcd54bfe658aa1577667cc24b732b82d3425164fbfcad212107c0a3b696a0431",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": LEAN_TOOLCHAIN_SHA256,
    "Formalizations/Lean/lake-manifest.json": LAKE_MANIFEST_SHA256,
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/Graph/Basic.lean": "dc3f9c7793f8de09261868afeb7e1d8804914b90b1fc4615feb139f2452dd2b9",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/Digraph/Basic.lean": "3062fbe7844161d29d885206e013c2c644e3f855f3603956bc3f243ab4808d81",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Algebra/BigOperators/Group/Finset/Basic.lean": "ea7bf2258d1d628feaf1e480f173f5015f1cfbdec5234bf475b50cb0922e1fcb",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Finset/Max.lean": "9eedb2d575fbf11a34aecc84bb6c515bfca033650d4835968f41e3f5f4d38904",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_line(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True, capture_output=True
    ).stdout.strip()


def check_worker_packet(path: Path, receipt: dict) -> None:
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
    assert packet["item_id"] == "S56-M-0877-INTAKE"
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE
    assert packet["commands"] and packet["output_summary"] and packet["known_failures"]
    assert all(
        isinstance(command, dict)
        and isinstance(command.get("argv"), list)
        and command["argv"]
        and isinstance(command.get("exit_code"), int)
        and isinstance(command.get("result"), str)
        and command["result"]
        for command in packet["commands"]
    )
    owned_files = {path.name for path in OWNED.iterdir() if path.is_file()}
    expected = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/THM-M-0877/{name}" for name in owned_files
    }
    assert set(packet["changed_paths"]) == expected
    assert set(receipt["changed_paths"]) == expected
    assert packet["known_failures"] == receipt["known_failures"]
    receipt_commands = {
        (tuple(command["argv"]), command["exit_code"])
        for command in receipt["commands_and_results"]
    }
    assert all(
        (tuple(command["argv"]), command["exit_code"]) in receipt_commands
        for command in packet["commands"]
    )
    for relative, expected_digest in WORKER_SOURCE_HASHES.items():
        assert digest(ROOT / relative) == expected_digest, f"worker source drift: {relative}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    target_manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(item for item in target_manifest["targets"] if item["theorem_id"] == "THM-M-0877")
    authority = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    authority_item = next(item for item in authority["items"] if item["id"] == "S56-M-0877-INTAKE")
    instance = load(OWNED / "instance.json")
    dag = load(OWNED / "task-dag.json")
    receipt = load(OWNED / "intake-receipt.json")

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert instance["normative_profile"] == dag["normative_profile"] == (
        "machine-theorem-assurance/1.0"
    )

    assert target["execution_rank"] == instance["execution_rank"] == 1430
    assert target["name"] == instance["name_zh"] == "网络流"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["target_lane"] == instance["target_lane"]
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    assert authority_item["theorem_id"] == "THM-M-0877"
    assert authority_item["phase"] == "intake"
    assert authority_item["depends_on"] == []
    assert authority_item["owned_paths"] == ["Stage1_Instances/THM-M-0877"]
    assert authority_item["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert authority_item["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )
    assert authority_item["state"] in {"[ ]", "[_]"}
    if args.worker_packet is not None:
        assert authority_item["state"] == "[ ]"

    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-0877"
    assert instance["item_id"] == receipt["item_id"] == "S56-M-0877-INTAKE"
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert dag["lifecycle"] == dag["lifecycle_mode"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal_target = instance["canonical_formal_target"]
    assert formal_target["module"] is None
    assert formal_target["declaration_or_expression"] is None
    assert formal_target["elaborated_expression_hash"] is None
    assert formal_target["environment_fingerprint"] is None
    assert instance["ordered_binders"] == instance["quantifiers"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert dag["audit_complete"] is dag["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []

    expected_tasks = [
        ("S56-M-0877-STATEMENT", ["S56-M-0877-INTAKE"]),
        ("S56-M-0877-ANCHOR_AUDIT", ["S56-M-0877-STATEMENT"]),
        ("S56-M-0877-OBLIGATION_TREE", ["S56-M-0877-ANCHOR_AUDIT"]),
        ("S56-M-0877-PROOF", ["S56-M-0877-OBLIGATION_TREE"]),
        ("S56-M-0877-VALIDATION", ["S56-M-0877-PROOF"]),
        ("S56-M-0877-RELEASE", ["S56-M-0877-VALIDATION"]),
    ]
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    authority_by_id = {
        item["id"]: item
        for item in authority["items"]
        if item["theorem_id"] == "THM-M-0877"
    }
    for task in dag["tasks"]:
        authoritative = authority_by_id[task["id"]]
        for field in (
            "phase",
            "layer",
            "owned_paths",
            "deliverable",
            "completion_gate",
            "depends_on",
        ):
            assert task[field] == authoritative[field], f"task drift: {task['id']}.{field}"
        assert task["evidence_ids"] == []

    owned_files = sorted(path.name for path in OWNED.iterdir() if path.is_file())
    assert owned_files == sorted(instance["owned_artifacts"])
    assert instance["public_merge_targets"] == [
        f"Stage1_Instances/THM-M-0877/{name}" for name in instance["owned_artifacts"]
    ]
    hashed_files = [name for name in owned_files if name != "intake-receipt.json"]
    assert sorted(receipt["untracked_owned_artifact_sha256"]) == sorted(hashed_files)
    for name in hashed_files:
        assert receipt["untracked_owned_artifact_sha256"][name] == digest(OWNED / name), (
            f"owned artifact hash mismatch: {name}"
        )

    source_revisions = instance["source_revisions"]
    assert source_revisions["repository_base"] == receipt["base_revision"] == BASE
    assert source_revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert source_revisions["mathlib"] == MATHLIB
    assert source_revisions["mathlib_tree"] == MATHLIB_TREE
    assert source_revisions["lean_toolchain_file_sha256"] == LEAN_TOOLCHAIN_SHA256
    assert source_revisions["lake_manifest_sha256"] == LAKE_MANIFEST_SHA256
    assert digest(ROOT / "Formalizations/Lean/lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert digest(ROOT / "Formalizations/Lean/lake-manifest.json") == LAKE_MANIFEST_SHA256
    assert git_output("rev-parse", "HEAD:Docs/researches/math_theorems.md") == (
        source_revisions["repository_math_source_current_blob"]
    )
    assert git_output(
        "rev-parse",
        f"{source_revisions['repository_source_record_commit']}:Docs/researches/math_theorems.md",
    ) == source_revisions["repository_source_record_blob"]
    mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib_root) == MATHLIB
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib_root) == MATHLIB_TREE
    assert git_output("status", "--short", cwd=mathlib_root) == ""

    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(keepends=True)
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8").splitlines(keepends=True)
    assert hashlib.sha256("".join(source_lines[6424:6430]).encode()).hexdigest() == TARGET_EXCERPT_SHA256
    assert hashlib.sha256("".join(stage0_lines[23926:23952]).encode()).hexdigest() == STAGE0_EXCERPT_SHA256
    assert hashlib.sha256(canonical_json_line(target)).hexdigest() == MANIFEST_ENTRY_SHA256

    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["content_addressed"] is False
    assert receipt["root_vector_before"] == {"H": "unclassified", "M": "unclassified", "R": "unclassified"}
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["canonical_obligation_ids"] == receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == receipt["content_addressed_recipe_ids"] == []
    assert receipt["content_addressed_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["change_impact_set"] == ["S56-M-0877-INTAKE"]
    assert receipt["remaining_root_cut_set"] == [task_id for task_id, _ in expected_tasks]
    assert receipt["covered_node_ids"] == ["S56-M-0877-INTAKE"]
    assert receipt["covered_declaration_ids"] == []
    assert receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"] == "master_acceptance_of_node_specific_intake_receipt"
    assert receipt["first_failed_theorem_gate"].startswith("S56-M-0877-STATEMENT:")
    started = dt.datetime.fromisoformat(receipt["validation_started_at"])
    ended = dt.datetime.fromisoformat(receipt["validation_ended_at"])
    validated = dt.datetime.fromisoformat(receipt["validated_at"])
    assert started <= ended == validated
    assert receipt["known_failures"] and receipt["status_boundary"]
    assert [recipe["recipe_id"] for recipe in receipt["structured_validation_recipes"]] == [
        "S56-M-0877-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0877-INTAKE-RECIPE-LEAN-PROBE",
    ]
    structure_recipe, lean_recipe = receipt["structured_validation_recipes"]
    assert all(
        recipe["expected_exit"] == recipe["exit_code"] == 0
        and recipe["covered_ids"] == ["S56-M-0877-INTAKE"]
        for recipe in (structure_recipe, lean_recipe)
    )
    assert structure_recipe["covered_obligation_ids"] == ["S56-M-0877-INTAKE"]
    assert structure_recipe["covered_declarations"] == []
    assert structure_recipe["argv"] == [
        "python3",
        "-B",
        "Stage1_Instances/THM-M-0877/check_intake.py",
    ]
    assert lean_recipe["covered_obligation_ids"] == []
    assert lean_recipe["covered_declarations"] == [
        "Graph",
        "Graph.IsLink",
        "Graph.Inc",
        "Digraph",
        "Finset.sum",
        "Finset.max'",
    ]
    for recipe in (structure_recipe, lean_recipe):
        recipe_started = dt.datetime.fromisoformat(recipe["execution_started_at"])
        recipe_ended = dt.datetime.fromisoformat(recipe["execution_ended_at"])
        assert started <= recipe_started <= recipe_ended <= ended
        assert len(recipe["stdout_sha256"]) == len(recipe["stderr_sha256"]) == 64
        assert recipe["log_retention"]
    assert all(
        isinstance(command.get("argv"), list)
        and command["argv"]
        and isinstance(command.get("exit_code"), int)
        and isinstance(command.get("result"), str)
        and command["result"]
        for command in receipt["commands_and_results"]
    )

    for path in OWNED.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )
    for name in ("README.md", "instance.json", "intake-receipt.json", "scope-map.md", "source-statement-crosswalk.md", "task-dag.json", "validation.md"):
        text = (OWNED / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "slot80" not in text
        assert "theorem_complete=true" not in text
    probe = (OWNED / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        path = args.worker_packet if args.worker_packet.is_absolute() else ROOT / args.worker_packet
        check_worker_packet(path.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0877 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
