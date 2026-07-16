#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0449 statement packet."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0449"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0449-STATEMENT"
THEOREM_ID = "THM-M-0449"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0449/README.md",
    "Stage1_Instances/THM-M-0449/Statement.lean",
    "Stage1_Instances/THM-M-0449/check_statement.py",
    "Stage1_Instances/THM-M-0449/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0449/statement-receipt.json",
    "Stage1_Instances/THM-M-0449/statement.json",
    "Stage1_Instances/THM-M-0449/source_statement_crosswalk.md",
}
REQUIRED_RECEIPT_POINTERS = (
    "/schema_version",
    "/receipt_id",
    "/item_id",
    "/theorem_id",
    "/phase",
    "/intent",
    "/base_revision",
    "/base_tree",
    "/inputs",
    "/support_state",
    "/proposed_state",
    "/accepted",
    "/verdict",
    "/selftest_status",
    "/selftest_result/exit_code",
    "/selftest_result/commands",
    "/known_failures",
    "/first_failed_gate",
    "/retry_condition",
    "/status_boundary",
    "/audit_complete",
    "/theorem_complete",
    "/invalidation_inputs",
    "/statement_fingerprints",
    "/mutation_tests",
)
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
    "first_failed_gate": "S02-EXACT-TARGET.exact_source_statement_identity",
    "open_obligations": 4,
    "stale_inputs": [],
    "blocked": True,
    "message": "The repository does not identify one exact mathematical proposition for THM-M-0449.",
}


if not __debug__:
    raise RuntimeError("statement validation requires Python assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


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
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC", "LEAN_NUM_THREADS": "1"})
    return subprocess.run(
        ["lake", "env", "lean", str(path)], cwd=LEAN_ROOT, env=environment,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=180, check=False,
    )


def validate_contract() -> None:
    contract_path = ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json"
    contract = load(contract_path)
    assert sha256(contract_path) == CONTRACT_SHA256
    assert git("hash-object", str(contract_path)) == CONTRACT_GIT_BLOB
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert phase["intent"] == "audit"
    assert phase["raw_blocked_can_close_phase"] is False
    assert phase["classified_negative_findings_may_satisfy_deliverable"] is False
    assert tuple(phase["phase_receipt_required_fields"]) == REQUIRED_RECEIPT_POINTERS
    assert [row["path_pattern"] for row in phase["validator_candidates"]] == [
        "Stage1_Instances/{theorem_id}/check_statement.py",
        "Stage1_Instances/{theorem_id}/check_statement_artifacts.py",
    ]
    assert not (HERE / "check_statement_artifacts.py").exists()
    expected_roles = {
        "statement_record": HERE / "statement.json",
        "statement_source": HERE / "Statement.lean",
        "source_crosswalk": HERE / "source_statement_crosswalk.md",
        "phase_receipt": HERE / "statement-receipt.json",
    }
    for role in phase["required_artifact_roles"]:
        candidates = [
            ROOT / path.format(theorem_id=THEOREM_ID)
            for path in role["path_candidates"]
        ]
        selected = [path for path in candidates if path.is_file()]
        assert selected == [expected_roles[role["role"]]]


def validate_authority() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    row = next(line for line in blueprint.splitlines() if f"`{ITEM_ID}`" in line)
    assert row.startswith("- [ ]") and "{attempts=0}" in row
    assert (
        "Depends: `S56-M-0449-INTAKE`. Owned paths: `Stage1_Instances/THM-M-0449`."
        in blueprint
    )

    graph_path = ROOT / "Docs/Stage1_Theorem_DAG_v2.json"
    graph = load(graph_path)
    assert sha256(graph_path) == GRAPH_SHA256
    assert graph["execution_contract"]["claim_order"] == [
        "v2_execution_rank", "phase_layer", "phase_item_id"
    ]
    assert graph["execution_contract"]["proof_parent_inspection"] == {
        "scope": ["direct_hard_parents", "transitive_hard_ancestors"],
        "order": "ascending_v2_execution_rank_parent_before_child",
        "complete_closure_required": True,
    }
    assert graph["execution_contract"]["provider_acceptance_inherited"] is False
    assert graph["execution_contract"]["consumer_acceptance_required"] is True
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 297
    assert node["phase_states"]["intake"] == "[_]"
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["phase_attempts"]["statement"] == 0
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == node["shared_lemma_group_ids"] == []
    inspection_order = sorted(
        set(node["direct_hard_parents"]) | set(node["transitive_hard_ancestors"]),
        key=lambda theorem_id: next(
            row["v2_execution_rank"] for row in graph["theorems"]
            if row["theorem_id"] == theorem_id
        ),
    )
    assert inspection_order == []


def validate_statement_boundary() -> None:
    intake = load(HERE / "intake.json")
    assert intake["canonical_formal_target"]["gate_state"] == (
        "blocked_source_identity_before_statement_phase"
    )
    assert intake["root_vector"] == {"human": "H4", "machine": "M4", "readability": "R4"}
    assert intake["theorem_complete"] is False

    statement = load(HERE / "statement.json")
    assert statement["item_id"] == ITEM_ID and statement["theorem_id"] == THEOREM_ID
    assert statement["canonical_human_statement"] is statement["canonical_statement"] is None
    formal = statement["canonical_formal_target"]
    assert formal["module"] == "Stage1_Instances/THM-M-0449/Statement.lean"
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_sha256"] is None
    assert formal["environment_expression_fingerprint"] is None
    assert statement["direct_imports"] == statement["statement_fingerprints"] == []
    assert statement["checked_alternate_encodings"] == []
    assert statement["ordered_binders"] == statement["hypotheses"] == []
    assert statement["statement_elaborated"] is statement["phase_predicate_proven"] is False
    assert statement["phase_accepted"] is statement["audit_complete"] is False
    assert statement["theorem_complete"] is False
    assert set(statement["mutation_tests"].values()) == {"not_run_no_canonical_target"}

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    code = lean_source_without_comments(source)
    assert not re.search(r"^\s*import\s", code, re.MULTILINE)
    assert not re.search(
        r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance|axiom|constant|opaque|unsafe|extern)\b",
        code,
        re.MULTILINE,
    )
    result = run_lean(HERE / "Statement.lean")
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout == result.stderr == ""

    legacy = run_lean(LEAN_ROOT / "AwesomeTheorems" / "Stage1" / "S1_M_063.lean")
    assert legacy.returncode == 0, legacy.stdout + legacy.stderr
    assert legacy.stdout == legacy.stderr == ""
    legacy_source = (
        LEAN_ROOT / "AwesomeTheorems" / "Stage1" / "S1_M_063.lean"
    ).read_text(encoding="utf-8")
    assert "it is not a terminal local Langlands proof" in legacy_source
    assert "FrozenTheoremVariant" in legacy_source


def validate_dependency_context() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM_ID
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    for key in (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        assert ledger[key] == []
    assert ledger["claim_order"] == {
        "v2_execution_rank": 297,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }
    audit = ledger["closure_audit"]
    assert audit["parent_inspection_order"] == audit["inspected_parent_ids"] == []
    assert audit["closure_complete"] is True
    assert audit["provider_acceptance_inherited"] is False
    assert audit["proof_credit_transferred"] is False


def validate_environment() -> None:
    version = subprocess.run(
        ["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    assert version.returncode == 0 and LEAN_COMMIT in version.stdout
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""


def validate_receipt_and_packet() -> None:
    receipt = load(HERE / "statement-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest_blocked"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["selftest_status"] == "passed"
    assert receipt["phase_predicate_proven"] is receipt["phase_accepted"] is False
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["statement_fingerprints"] == []
    assert set(receipt["mutation_tests"].values()) == {"not_run_no_canonical_target"}
    assert receipt["first_failed_gate"] == SEMANTIC_RESULT["first_failed_gate"]
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["commands"] == receipt["commands"]
    assert receipt["known_failures"] and receipt["invalidation_inputs"]

    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    assert set(selected) == {
        "statement_record", "statement_source", "source_crosswalk", "phase_receipt"
    }
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        binding = selected[role]
        path = ROOT / binding["path"]
        assert binding["sha256"] == sha256(path)
        assert binding["git_blob"] == git("hash-object", str(path))
    self_role = selected["phase_receipt"]
    assert self_role["path"] == "Stage1_Instances/THM-M-0449/statement-receipt.json"
    assert self_role["sha256"] is self_role["git_blob"] is None

    for binding in receipt["inputs"].values():
        path = ROOT / binding["path"]
        assert binding["sha256"] == sha256(path)
        assert binding["git_blob"] == git("hash-object", str(path))

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "worker_verdict", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["worker_verdict"] == "blocked"
    assert packet["base_revision"] == BASE_REVISION and packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert set(receipt["changed_paths"]) == EXPECTED_CHANGED_PATHS

    semantic_keys = {
        "schema_version", "item_id", "theorem_id", "phase", "status", "verdict",
        "phase_accepted", "audit_complete", "theorem_complete",
        "phase_predicate_proven", "first_failed_gate", "open_obligations",
        "stale_inputs", "blocked", "message",
    }
    assert set(SEMANTIC_RESULT) == semantic_keys
    assert SEMANTIC_RESULT["status"] == SEMANTIC_RESULT["verdict"] == "blocked"
    assert SEMANTIC_RESULT["phase_accepted"] is False
    assert SEMANTIC_RESULT["phase_predicate_proven"] is False
    assert SEMANTIC_RESULT["blocked"] is True

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(lean_source_without_comments(
        (HERE / "Statement.lean").read_text(encoding="utf-8")
    )) is None
    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    assert status.returncode == 0, status.stderr
    changed: set[str] = set()
    for line in status.stdout.splitlines():
        path = line[3:]
        if path == "Formalizations/Lean/.lake":
            continue
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        changed.add(path)
    assert changed == EXPECTED_CHANGED_PATHS


def validate() -> None:
    validate_contract()
    validate_authority()
    validate_statement_boundary()
    validate_dependency_context()
    validate_environment()
    validate_receipt_and_packet()


def main() -> None:
    try:
        validate()
    except Exception as exc:
        failure = dict(SEMANTIC_RESULT)
        failure.update({
            "status": "failed",
            "verdict": "repair_required",
            "first_failed_gate": "VALIDATOR-INTERNAL-CONSISTENCY",
            "blocked": False,
            "message": f"Validator consistency failure: {type(exc).__name__}: {exc}",
        })
        print(json.dumps(failure, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(SEMANTIC_RESULT, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
