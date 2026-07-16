#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0412 statement boundary."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0412"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0412-STATEMENT"
THEOREM_ID = "THM-M-0412"
BASE_REVISION = "c5037228977a81948bbd6119e1728b4b65b9924e"
BASE_TREE = "78b2627e717156dffe240bea12d14205af667d2a"
GRAPH_SHA256 = "fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
PROBE_STDOUT_SHA256 = "52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0412/Statement.lean",
    "Stage1_Instances/THM-M-0412/check_statement.py",
    "Stage1_Instances/THM-M-0412/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0412/statement-blocker.json",
    "Stage1_Instances/THM-M-0412/statement-blocker.md",
    "Stage1_Instances/THM-M-0412/statement-receipt.json",
    "Stage1_Instances/THM-M-0412/statement.json",
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
    "open_obligations": 1,
    "stale_inputs": [],
    "blocked": True,
    "message": "The repository does not identify an exact mathematical proposition for THM-M-0412.",
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
        ["lake", "env", "lean", str(path)], cwd=LEAN_ROOT, env=environment,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=120, check=False,
    )


def validate() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    contract_path = ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json"
    contract = load(contract_path)
    assert sha256(contract_path) == CONTRACT_SHA256
    assert git("hash-object", str(contract_path)) == CONTRACT_GIT_BLOB
    statement_contract = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert statement_contract["raw_blocked_can_close_phase"] is False
    assert statement_contract["classified_negative_findings_may_satisfy_deliverable"] is False
    assert tuple(statement_contract["phase_receipt_required_fields"]) == REQUIRED_RECEIPT_POINTERS
    expected_roles = {
        "statement_record": "Stage1_Instances/THM-M-0412/statement.json",
        "statement_source": "Stage1_Instances/THM-M-0412/Statement.lean",
        "source_crosswalk": "Stage1_Instances/THM-M-0412/source-statement-crosswalk.md",
        "phase_receipt": "Stage1_Instances/THM-M-0412/statement-receipt.json",
    }
    for role in statement_contract["required_artifact_roles"]:
        candidates = [path.format(theorem_id=THEOREM_ID) for path in role["path_candidates"]]
        if expected_roles[role["role"]] in candidates:
            assert sum((ROOT / path).is_file() for path in candidates) == 1
    assert [row["path_pattern"] for row in statement_contract["validator_candidates"]] == [
        "Stage1_Instances/{theorem_id}/check_statement.py",
        "Stage1_Instances/{theorem_id}/check_statement_artifacts.py",
    ]

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    line = next(row for row in blueprint.splitlines() if f"`{ITEM_ID}`" in row)
    assert line.startswith("- [ ]") and "{attempts=0}" in line
    assert "Depends: `S56-M-0412-INTAKE`" in blueprint

    graph_path = ROOT / "Docs/Stage1_Theorem_DAG_v2.json"
    graph = load(graph_path)
    assert sha256(graph_path) == GRAPH_SHA256
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 259
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["phase_attempts"]["statement"] == 0
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == node["shared_lemma_group_ids"] == []

    instance = load(HERE / "instance.json")
    assert instance["canonical_statement_status"] == "unresolved_source_identity"
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_execution_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    statement = load(HERE / "statement.json")
    assert statement["item_id"] == ITEM_ID and statement["theorem_id"] == THEOREM_ID
    assert statement["canonical_statement"] is None
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_sha256"] is None
    assert formal["environment_fingerprint"] is None
    assert statement["direct_imports"] == statement["statement_fingerprints"] == []
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

    ledger = load(HERE / "dependency-reuse-ledger.json")
    assert ledger == {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM_ID,
        "observed_theorem_dag_sha256": GRAPH_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [],
        "inspections": [],
        "reuse_decisions": [],
        "unresolved_compatibility_obligations": [],
    }

    probe = run_lean(HERE / "StatementProbe.lean")
    assert probe.returncode == 0, probe.stdout + probe.stderr
    assert hashlib.sha256(probe.stdout.encode()).hexdigest() == PROBE_STDOUT_SHA256
    assert hashlib.sha256(probe.stderr.encode()).hexdigest() == EMPTY_SHA256
    assert probe.stdout.count("WeierstrassCurve") >= 6

    version = subprocess.run(
        ["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    assert version.returncode == 0 and LEAN_COMMIT in version.stdout
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""

    blocker = load(HERE / "statement-blocker.json")
    assert blocker["item_id"] == ITEM_ID and blocker["theorem_id"] == THEOREM_ID
    assert blocker["base_revision"] == BASE_REVISION and blocker["base_tree"] == BASE_TREE
    assert blocker["first_failed_gate"] == SEMANTIC_RESULT["first_failed_gate"]
    assert blocker["phase_predicate_proven"] is blocker["phase_accepted"] is False
    assert blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert blocker["dependency_context"]["parent_inspection_order"] == []
    assert blocker["canonical_statement"] is blocker["canonical_formal_target"] is None
    assert blocker["minimal_imports"] is blocker["elaborated_expression_sha256"] is None

    receipt = load(HERE / "statement-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked"
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
    assert receipt["inputs"]["dependency-reuse-ledger.json"]["sha256"] == sha256(
        HERE / "dependency-reuse-ledger.json"
    )
    assert receipt["inputs"]["statement.json"]["sha256"] == sha256(HERE / "statement.json")
    assert receipt["inputs"]["Statement.lean"]["sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["source-statement-crosswalk.md"]["sha256"] == sha256(
        HERE / "source-statement-crosswalk.md"
    )
    assert receipt["inputs"]["check_statement.py"]["sha256"] == sha256(Path(__file__).resolve())
    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    assert set(selected) == {
        "statement_record", "statement_source", "source_crosswalk", "phase_receipt"
    }
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        binding = selected[role]
        path = ROOT / binding["path"]
        assert binding["sha256"] == sha256(path)
        assert binding["git_blob"] == git("hash-object", str(path))
    assert selected["phase_receipt"]["path"] == (
        "Stage1_Instances/THM-M-0412/statement-receipt.json"
    )
    assert selected["phase_receipt"]["sha256"] is selected["phase_receipt"]["git_blob"] is None
    for binding in receipt["inputs"].values():
        path = ROOT / binding["path"]
        assert sha256(path) == binding["sha256"]
        assert git("hash-object", str(path)) == binding["git_blob"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    for path in (HERE / "Statement.lean", HERE / "StatementProbe.lean"):
        assert prohibited.search(lean_source_without_comments(path.read_text(encoding="utf-8"))) is None
    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


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
