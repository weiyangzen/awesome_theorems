#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0546 statement boundary."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0546"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0546-STATEMENT"
THEOREM_ID = "THM-M-0546"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
PROBE_STDOUT_SHA256 = "4d14ccd0fc7ef066d2c0f833f00d9b8f1f651d2a419feca841d2275642bda08a"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0546/Statement.lean",
    "Stage1_Instances/THM-M-0546/check_statement.py",
    "Stage1_Instances/THM-M-0546/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0546/statement-blocker.json",
    "Stage1_Instances/THM-M-0546/statement-blocker.md",
    "Stage1_Instances/THM-M-0546/statement-receipt.json",
    "Stage1_Instances/THM-M-0546/statement.json",
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
    "first_failed_gate": "S02-EXACT-TARGET.variant_and_source_claim_not_frozen",
    "open_obligations": 5,
    "stale_inputs": [],
    "blocked": True,
    "message": (
        "The exact source variant and concrete Lean interfaces needed for "
        "THM-M-0546 remain unfrozen."
    ),
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
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(
        ["lake", "env", "lean", "--trust=0", str(path)], cwd=LEAN_ROOT,
        env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=120, check=False,
    )


def validate_contract() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    contract_path = ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json"
    contract = load(contract_path)
    assert sha256(contract_path) == CONTRACT_SHA256
    assert git("hash-object", str(contract_path)) == CONTRACT_GIT_BLOB
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert phase["raw_blocked_can_close_phase"] is False
    assert phase["classified_negative_findings_may_satisfy_deliverable"] is False
    assert tuple(phase["phase_receipt_required_fields"]) == REQUIRED_RECEIPT_POINTERS
    expected_roles = {
        "statement_record": "Stage1_Instances/THM-M-0546/statement.json",
        "statement_source": "Stage1_Instances/THM-M-0546/Statement.lean",
        "source_crosswalk": "Stage1_Instances/THM-M-0546/source-statement-crosswalk.md",
        "phase_receipt": "Stage1_Instances/THM-M-0546/statement-receipt.json",
    }
    selected: dict[str, str] = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            path.format(theorem_id=THEOREM_ID) for path in role["path_candidates"]
            if (ROOT / path.format(theorem_id=THEOREM_ID)).is_file()
        ]
        assert len(candidates) == 1, (role["role"], candidates)
        selected[role["role"]] = candidates[0]
    assert selected == expected_roles
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    assert validators == ["Stage1_Instances/THM-M-0546/check_statement.py"]

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    line = next(row for row in blueprint.splitlines() if f"`{ITEM_ID}`" in row)
    assert line.startswith("- [ ]") and "{attempts=0}" in line
    dependency_line = next(
        row for index, row in enumerate(blueprint.splitlines())
        if index and f"`{ITEM_ID}`" in blueprint.splitlines()[index - 1]
    )
    assert "Depends: `S56-M-0546-INTAKE`" in dependency_line

    graph_path = ROOT / "Docs/Stage1_Theorem_DAG_v2.json"
    graph = load(graph_path)
    assert sha256(graph_path) == GRAPH_SHA256
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 323 and node["topological_layer"] == 0
    assert node["phase_states"]["intake"] == "[_]"
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["phase_attempts"]["statement"] == 0
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == node["shared_lemma_group_ids"] == []


def validate_statement_boundary() -> None:
    instance = load(HERE / "instance.json")
    assert instance["canonical_claim_status"] == "blocked_on_variant_and_source_freeze"
    assert instance["canonical_claim"] is None
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    statement = load(HERE / "statement.json")
    assert statement["item_id"] == ITEM_ID and statement["theorem_id"] == THEOREM_ID
    assert statement["canonical_statement"] is None
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_sha256"] is None
    assert formal["environment_fingerprint"] is None
    assert statement["direct_imports"] == []
    assert statement["statement_fingerprints"] == []
    assert statement["statement_elaborated"] is statement["phase_predicate_proven"] is False
    assert statement["phase_accepted"] is statement["audit_complete"] is False
    assert statement["theorem_complete"] is False
    assert set(statement["mutation_tests"].values()) == {"not_run_no_canonical_target"}

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    code = lean_source_without_comments(source)
    assert not re.search(r"^\s*import\s", code, re.MULTILINE)
    assert not re.search(
        r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance|axiom|constant|opaque|unsafe|extern)\b",
        code, re.MULTILINE,
    )
    source_result = run_lean(HERE / "Statement.lean")
    assert source_result.returncode == 0, source_result.stdout + source_result.stderr
    assert source_result.stdout == source_result.stderr == ""

    probe = run_lean(HERE / "StatementInfrastructure.lean")
    assert probe.returncode == 0, probe.stdout + probe.stderr
    assert hashlib.sha256(probe.stdout.encode()).hexdigest() == PROBE_STDOUT_SHA256
    assert hashlib.sha256(probe.stderr.encode()).hexdigest() == EMPTY_SHA256
    assert "singularHomologyFunctor" in probe.stdout
    assert "BoundarylessManifold" in probe.stdout

    legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_107.lean").read_text(
        encoding="utf-8"
    )
    assert "structure PoincareDualityData" in legacy
    assert "capProduct_isomorphism : capProductIsomorphism" in legacy
    assert "def StatementShape" in legacy
    assert "intentionally not a proof of Poincare duality" in legacy


def validate_ledger_and_blocker() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM_ID
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    assert ledger["claim_order"] == {
        "v2_execution_rank": 323,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "parent_inspection_order",
        "inspections", "reuse_decisions", "unresolved_compatibility_obligations",
    ):
        assert ledger[field] == [], field
    assert ledger["closure_audit"]["inspection_order"] == []
    assert ledger["closure_audit"]["status"] == "empty_complete_closure_audited"

    blocker = load(HERE / "statement-blocker.json")
    assert blocker["item_id"] == ITEM_ID and blocker["theorem_id"] == THEOREM_ID
    assert blocker["base_revision"] == BASE_REVISION and blocker["base_tree"] == BASE_TREE
    assert blocker["first_failed_gate"] == SEMANTIC_RESULT["first_failed_gate"]
    assert blocker["phase_predicate_proven"] is blocker["phase_accepted"] is False
    assert blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert blocker["dependency_context"]["parent_inspection_order"] == []
    assert blocker["canonical_statement"] is blocker["canonical_formal_target"] is None
    assert blocker["minimal_imports"] is blocker["elaborated_expression_sha256"] is None


def validate_receipt_and_packet() -> None:
    receipt = load(HERE / "statement-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["worker_verdict"] == "blocked"
    assert receipt["selftest_status"] == "passed"
    assert receipt["phase_predicate_proven"] is receipt["phase_accepted"] is False
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["statement_fingerprints"] == []
    assert set(receipt["mutation_tests"].values()) == {"not_run_no_canonical_target"}
    assert receipt["first_failed_gate"] == SEMANTIC_RESULT["first_failed_gate"]
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["commands"]

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "worker_verdict", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["worker_verdict"] == "blocked"
    assert packet["base_revision"] == BASE_REVISION and packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS
    assert packet["commands"] == receipt["selftest_result"]["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert receipt["changed_paths"] == packet["changed_paths"]

    expected_roles = {
        "statement_record", "statement_source", "source_crosswalk", "phase_receipt"
    }
    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    assert set(selected) == expected_roles
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        binding = selected[role]
        path = ROOT / binding["path"]
        assert binding["sha256"] == sha256(path)
        assert binding["git_blob"] == git("hash-object", str(path))
    assert selected["phase_receipt"]["path"] == (
        "Stage1_Instances/THM-M-0546/statement-receipt.json"
    )
    assert selected["phase_receipt"]["sha256"] is selected["phase_receipt"]["git_blob"] is None

    for name, binding in receipt["inputs"].items():
        if name == "check_statement.py":
            assert binding["sha256"] == sha256(Path(__file__).resolve())
            assert binding["git_blob"] == git("hash-object", str(Path(__file__).resolve()))
            continue
        path = ROOT / binding["path"]
        assert sha256(path) == binding["sha256"], name
        assert git("hash-object", str(path)) == binding["git_blob"], name


def validate_environment_and_hygiene() -> None:
    version = subprocess.run(
        ["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    assert version.returncode == 0 and LEAN_COMMIT in version.stdout
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    for path in (HERE / "Statement.lean", HERE / "StatementInfrastructure.lean"):
        code = lean_source_without_comments(path.read_text(encoding="utf-8"))
        assert prohibited.search(code) is None
    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def validate() -> None:
    validate_contract()
    validate_statement_boundary()
    validate_ledger_and_blocker()
    validate_receipt_and_packet()
    validate_environment_and_hygiene()


def main() -> None:
    try:
        validate()
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
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
