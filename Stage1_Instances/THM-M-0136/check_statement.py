#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0136 statement packet."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0136"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0136-STATEMENT"
THEOREM_ID = "THM-M-0136"
BASE_REVISION = "dae1951609072752d49d111bf00e78e4512f2d14"
BASE_TREE = "9d8cc27cc0e09489c78b0bdbdeb57b15c5840f13"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = "S02-EXACT-TARGET.exact_source_statement_identity_and_equivalence_structure"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MUTATION_NAMES = {
    "removed_hypothesis",
    "changed_domain",
    "changed_binder_scope",
    "boundary_case",
}
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0136/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0136/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0136/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0136/statement-receipt.json",
}
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0136/Statement.lean",
    "Stage1_Instances/THM-M-0136/check_statement.py",
    "Stage1_Instances/THM-M-0136/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0136/statement-receipt.json",
    "Stage1_Instances/THM-M-0136/statement-recheck-2026-07-17-head-dae195160-slot72.json",
    "Stage1_Instances/THM-M-0136/statement-recheck-2026-07-17-head-dae195160-slot72.md",
    "Stage1_Instances/THM-M-0136/statement.json",
}
SEMANTIC_RESULT = {
    "schema_version": "stage1-validator-semantic-result/1.0",
    "item_id": ITEM_ID,
    "theorem_id": THEOREM_ID,
    "phase": "statement",
    "status": "blocked",
    "verdict": "blocked",
    "phase_accepted": False,
    "audit_complete": False,
    "theorem_complete": False,
    "phase_predicate_proven": False,
    "first_failed_gate": FAILED_GATE,
    "open_obligations": 4,
    "stale_inputs": [],
    "blocked": True,
    "message": "No exact source proposition or preserved Kac-Moody equivalence structure is selected.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def git(*args: str, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if check:
        assert result.returncode == 0, result.stderr
    return result


def pointer(document: dict[str, Any], raw: str) -> Any:
    value: Any = document
    for component in raw.removeprefix("/").split("/"):
        assert isinstance(value, dict) and component in value, raw
        value = value[component]
    return value


def lean_source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                index += 2
            elif source[index] == '"':
                in_string = False
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            end = source.find("\n", index)
            index = len(source) if end < 0 else end
        elif source[index] == '"':
            in_string = True
            output.append(source[index])
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def run_lean(relative: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "LANG": "C", "TZ": "UTC"})
    return subprocess.run(
        ["lake", "env", "lean", "--trust=0", relative], cwd=LEAN_ROOT,
        env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=180, check=False,
    )


def assert_text_boundary(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def validate() -> None:
    assert git("rev-parse", "HEAD").stdout.strip() == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}").stdout.strip() == BASE_TREE

    contract_path = ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json"
    contract = load(contract_path)
    assert sha256(contract_path) == CONTRACT_SHA256
    phase_contract = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert phase_contract["layer"] == 1
    assert phase_contract["raw_blocked_can_close_phase"] is False
    assert phase_contract["classified_negative_findings_may_satisfy_deliverable"] is False
    assert phase_contract["worker_verdicts_eligible_for_review"] == ["accepted", "no_state_change"]
    expected_roles = {
        row["role"]: [path.format(theorem_id=THEOREM_ID) for path in row["path_candidates"]]
        for row in phase_contract["required_artifact_roles"]
    }
    assert set(expected_roles) == set(ROLE_PATHS)
    for role, path in ROLE_PATHS.items():
        assert path in expected_roles[role]
        assert sum((ROOT / candidate).is_file() for candidate in expected_roles[role]) == 1
    assert [row["path_pattern"] for row in phase_contract["validator_candidates"]] == [
        "Stage1_Instances/{theorem_id}/check_statement.py",
        "Stage1_Instances/{theorem_id}/check_statement_artifacts.py",
    ]
    assert (HERE / "check_statement.py").is_file()
    assert not (HERE / "check_statement_artifacts.py").exists()

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    item_line = next(line for line in blueprint.splitlines() if f"`{ITEM_ID}`" in line)
    assert item_line.startswith("- [ ]") and "{attempts=0}" in item_line
    assert "Depends: `S56-M-0136-INTAKE`" in blueprint

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 52
    assert target["legacy_priority_slot"] == "S1-M-052"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is False

    graph_path = ROOT / "Docs/Stage1_Theorem_DAG_v2.json"
    graph = load(graph_path)
    assert sha256(graph_path) == GRAPH_SHA256
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 286 and node["topological_layer"] == 0
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["phase_attempts"]["statement"] == 0
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == []
    assert node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == []
    assert node["shared_lemma_group_ids"] == []

    instance = load(HERE / "instance.json")
    assert instance["canonical_claim_status"] == "provisional_prose_scope_source_mismatch_open"
    assert instance["source_status"] == "bibliographic_anchor_identified_exact_source_theorem_not_identified"
    assert instance["root_vector"] == {"H": "H4", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    ledger = load(HERE / "dependency-reuse-ledger.json")
    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM_ID
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        assert ledger[field] == []
    assert ledger["closure_audit"]["parent_inspection_order"] == []

    statement = load(HERE / "statement.json")
    assert statement["schema_version"] == "stage1-statement/1.0"
    assert statement["item_id"] == ITEM_ID and statement["theorem_id"] == THEOREM_ID
    assert statement["canonical_statement"] is None
    assert statement["canonical_formal_target"] is None
    assert statement["direct_imports_for_canonical_target"] is None
    assert statement["minimal_imports_proven"] is False
    assert statement["elaborated_expression_sha256"] is None
    assert statement["environment_fingerprint_for_canonical_target"] is None
    assert statement["statement_fingerprints"] == statement["credited_transports"] == []
    assert set(statement["mutation_tests"]) == MUTATION_NAMES
    assert set(statement["mutation_tests"].values()) == {
        "not_executable_without_a_canonical_statement"
    }
    assert statement["first_failed_gate"] == FAILED_GATE
    assert statement["statement_elaborated"] is statement["phase_predicate_proven"] is False
    assert statement["phase_accepted"] is statement["audit_complete"] is False
    assert statement["theorem_complete"] is False
    assert statement["dependency_context"]["parent_inspection_order"] == []
    assert statement["candidate_surface_probe"]["direct_imports"] == [
        "Mathlib.Algebra.Lie.SerreConstruction"
    ]

    source_text = (HERE / "Statement.lean").read_text(encoding="utf-8")
    code = lean_source_without_comments(source_text)
    assert re.findall(r"^import ([^\s]+)$", code, re.MULTILINE) == [
        "Mathlib.Algebra.Lie.SerreConstruction"
    ]
    for check in (
        "#check Matrix.ToLieAlgebra",
        "#check CartanMatrix.Generators",
        "#check CartanMatrix.Relations.toIdeal",
    ):
        assert check in code
    assert not re.search(
        r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance|axiom|constant|opaque|unsafe|extern)\b",
        code, re.MULTILINE,
    )
    assert not re.search(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b", code
    )
    probe = run_lean("../../Stage1_Instances/THM-M-0136/Statement.lean")
    assert probe.returncode == 0, probe.stdout + probe.stderr
    assert probe.stderr == ""
    for name in ("Matrix.ToLieAlgebra", "CartanMatrix.Generators", "CartanMatrix.Relations.toIdeal"):
        assert name in probe.stdout

    legacy = run_lean("AwesomeTheorems/Stage1/S1_M_052.lean")
    assert legacy.returncode == 0, legacy.stdout + legacy.stderr
    assert legacy.stderr == ""
    assert "StatementShape" in legacy.stdout and "NormalizedKacMoodyClassificationTarget" in legacy.stdout
    legacy_source = (LEAN_ROOT / "AwesomeTheorems/Stage1/S1_M_052.lean").read_text(encoding="utf-8")
    for phrase in (
        "Statement-shape candidate",
        "must replace this",
        "candidate with the standard classification statement",
        "not a completion theorem",
    ):
        assert phrase in legacy_source

    version = subprocess.run(
        ["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    assert version.returncode == 0 and LEAN_COMMIT in version.stdout
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib).stdout.strip() == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib).stdout.strip() == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib).stdout == ""

    blocker = load(HERE / "statement-recheck-2026-07-17-head-dae195160-slot72.json")
    assert blocker["item_id"] == ITEM_ID and blocker["theorem_id"] == THEOREM_ID
    assert blocker["base_revision"] == BASE_REVISION and blocker["base_tree"] == BASE_TREE
    assert blocker["verdict"] == "blocked" and blocker["state"] == "[ ]"
    assert blocker["first_failed_gate"] == "exact_source_statement_identity_and_equivalence_structure"
    assert blocker["canonical_human_statement"] is blocker["canonical_formal_target"] is None
    assert blocker["statement_gate_passed"] is blocker["statement_elaborated"] is False
    assert blocker["statement_accepted"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["dependency_reuse_context"]["parent_inspection_order"] == []

    receipt = load(HERE / "statement-receipt.json")
    for raw in phase_contract["phase_receipt_required_fields"]:
        pointer(receipt, raw)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest_negative_evidence"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["selftest_status"] == "passed"
    assert receipt["selftest_result"]["exit_code"] == 0
    assert isinstance(receipt["selftest_result"]["commands"], list)
    assert receipt["selftest_result"]["commands"]
    assert receipt["known_failures"] and receipt["retry_condition"]
    assert receipt["first_failed_gate"] == FAILED_GATE
    assert receipt["statement_fingerprints"] == []
    assert receipt["mutation_tests"] == statement["mutation_tests"]
    assert receipt["phase_predicate_proven"] is receipt["phase_accepted"] is False
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["inputs"]["dependency_context_sha256"] == CONTEXT_SHA256
    assert receipt["inputs"]["parent_inspection_order"] == []
    assert receipt["inputs"]["provider_acceptance_inherited"] is False

    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    assert set(selected) == set(ROLE_PATHS)
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        binding = selected[role]
        path = ROOT / binding["path"]
        assert binding["path"] == ROLE_PATHS[role]
        assert binding["sha256"] == sha256(path)
        assert binding["git_blob"] == git_blob(path)
    phase_binding = selected["phase_receipt"]
    assert phase_binding["path"] == ROLE_PATHS["phase_receipt"]
    assert phase_binding["sha256"] is phase_binding["git_blob"] is None
    assert phase_binding["binding_owner"] == "scheduler integration lane"

    for name in (
        "dependency_reuse_ledger", "statement_record", "statement_source",
        "source_crosswalk", "blocker_record", "blocker_report",
    ):
        binding = receipt["inputs"][name]
        path = ROOT / binding["path"]
        assert binding["sha256"] == sha256(path), name
        assert binding["git_blob"] == git_blob(path), name
    validator_binding = receipt["inputs"]["validator"]
    assert validator_binding["path"] == "Stage1_Instances/THM-M-0136/check_statement.py"
    assert validator_binding["sha256"] == sha256(Path(__file__).resolve())
    assert validator_binding["git_blob"] == git_blob(Path(__file__).resolve())

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["commands"] == receipt["selftest_result"]["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["selftest_result"]["output_summary"]
    assert set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS

    status = git("status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    actual_changed = {".stage1-worker-selftest.json"}
    for line in status:
        relative = line[3:]
        if relative in {"Formalizations/Lean/.lake", ".stage1-worker-selftest.json"}:
            continue
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/"), relative
        actual_changed.add(relative)
    assert actual_changed == EXPECTED_CHANGED_PATHS

    for relative in EXPECTED_CHANGED_PATHS:
        assert_text_boundary(ROOT / relative)


def main() -> None:
    validate()
    print(json.dumps(SEMANTIC_RESULT, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
