#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0131 statement boundary."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0131"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0131-STATEMENT"
THEOREM_ID = "THM-M-0131"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_BINDINGS = {
    "statement.json": (
        "9e22874acae9f3256bae291f14e1cde7d937cd3655150f25f40c4ece40abc844",
        "8fcef8d1178a9fb6d4f5cdae16e7b2ea2a9a878c",
    ),
    "Statement.lean": (
        "db8937901c8fcb00aaf2978f8f0b82b78358d88733b40d01da3cae2ef42a6562",
        "c6ebeeaeee77b95b64829c9c4bc082cdba60e7ef",
    ),
    "source_statement_crosswalk.md": (
        "7bfa94553a52d95a1a4168ba7179a91cd108bf73d4e1cd924fcf8e63d3199f60",
        "bee8245304496347624165ba7310699e7d044a8b",
    ),
    "dependency-reuse-ledger.json": (
        "1789d83b9fa8eb225af6af7e777427cc39567534176673a4ec84c50ab0ad2cab",
        "a9afac8ef91f89da03b11da0de6f74422dace974",
    ),
    "statement-blocker.json": (
        "fd4d0d166856513024782e369b9df42093883d59f613229a7a2e0d3f20bfac43",
        "89df20dea3fc8c6b9b2e4102b1a9d9ae6f5db3f4",
    ),
}
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0131/Statement.lean",
    "Stage1_Instances/THM-M-0131/check_statement.py",
    "Stage1_Instances/THM-M-0131/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0131/statement-blocker.json",
    "Stage1_Instances/THM-M-0131/statement-blocker-head-307c34d30-slot71.md",
    "Stage1_Instances/THM-M-0131/statement-blocker.md",
    "Stage1_Instances/THM-M-0131/statement-receipt.json",
    "Stage1_Instances/THM-M-0131/statement.json",
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
    "first_failed_gate": "S02-EXACT-TARGET.exact_source_statement_identity_and_theorem_family",
    "open_obligations": 1,
    "stale_inputs": [],
    "blocked": True,
    "message": "The repository does not identify one exact mathematical proposition for THM-M-0131.",
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
        "statement_record": "Stage1_Instances/THM-M-0131/statement.json",
        "statement_source": "Stage1_Instances/THM-M-0131/Statement.lean",
        "source_crosswalk": "Stage1_Instances/THM-M-0131/source_statement_crosswalk.md",
        "phase_receipt": "Stage1_Instances/THM-M-0131/statement-receipt.json",
    }
    for role in statement_contract["required_artifact_roles"]:
        candidates = [path.format(theorem_id=THEOREM_ID) for path in role["path_candidates"]]
        assert expected_roles[role["role"]] in candidates
        assert sum((ROOT / path).is_file() for path in candidates) == 1
    assert [row["path_pattern"] for row in statement_contract["validator_candidates"]] == [
        "Stage1_Instances/{theorem_id}/check_statement.py",
        "Stage1_Instances/{theorem_id}/check_statement_artifacts.py",
    ]
    assert (HERE / "check_statement.py").is_file()
    assert not (HERE / "check_statement_artifacts.py").exists()

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    line = next(row for row in blueprint.splitlines() if f"`{ITEM_ID}`" in row)
    assert line.startswith("- [ ]") and "{attempts=0}" in line
    dependency_line = blueprint.splitlines()[blueprint.splitlines().index(line) + 1]
    assert "Depends: `S56-M-0131-INTAKE`" in dependency_line

    graph_path = ROOT / "Docs/Stage1_Theorem_DAG_v2.json"
    graph = load(graph_path)
    assert sha256(graph_path) == GRAPH_SHA256
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["original_execution_rank"] == 48
    assert node["v2_execution_rank"] == 282
    assert node["phase_states"]["intake"] == "[_]"
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["phase_attempts"]["statement"] == 0
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == node["shared_lemma_group_ids"] == []

    intake = load(HERE / "intake.json")
    formal_intake = intake["canonical_formal_target"]
    assert intake["item_id"] == "S56-M-0131-INTAKE"
    assert formal_intake["module"] is formal_intake["declaration_or_expression"] is None
    assert formal_intake["elaborated_expression_hash"] is None
    assert formal_intake["environment_fingerprint"] is None
    assert intake["root_vector"] == {"human": "H4", "machine": "M4", "readability": "R3"}
    assert intake["theorem_complete"] is False

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
    dependency = statement["dependency_context"]
    assert dependency["parent_inspection_order"] == []
    assert dependency["direct_parent_ids"] == dependency["transitive_ancestor_ids"] == []
    assert dependency["hard_edge_ids"] == dependency["reuse_hint_ids"] == []
    assert dependency["shared_group_ids"] == []

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

    legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_048.lean"
    legacy_source = legacy.read_text(encoding="utf-8")
    assert sha256(legacy) == "5afb45f39d31340745024bb024dd04172352b58cdb3a819434a481b96b740fc5"
    assert "The three proposition fields are placeholders" in legacy_source
    assert all(name in legacy_source for name in (
        "conductorLevelCompatible : Prop",
        "qExpansionMatchesFrobeniusTraces : Prop",
        "lSeriesCompatible : Prop",
    ))
    legacy_result = run_lean(legacy)
    assert legacy_result.returncode == 0, legacy_result.stdout + legacy_result.stderr
    assert legacy_result.stdout == legacy_result.stderr == ""

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
    assert receipt["support_state"] == "provisional_worker_selftest_blocked"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["selftest_status"] == "passed"
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["statement_fingerprints"] == []
    assert set(receipt["mutation_tests"].values()) == {"not_run_no_canonical_target"}
    assert receipt["first_failed_gate"] == SEMANTIC_RESULT["first_failed_gate"]
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["commands"]
    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID
    assert packet["base_revision"] == BASE_REVISION and packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS
    assert packet["commands"] == receipt["selftest_result"]["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    assert set(selected) == {
        "statement_record", "statement_source", "source_crosswalk", "phase_receipt"
    }
    selected_names = {
        "statement_record": "statement.json",
        "statement_source": "Statement.lean",
        "source_crosswalk": "source_statement_crosswalk.md",
    }
    for role, name in selected_names.items():
        binding = selected[role]
        expected_sha, expected_blob = EXPECTED_BINDINGS[name]
        assert binding["sha256"] == expected_sha == sha256(HERE / name)
        assert binding["git_blob"] == expected_blob == git("hash-object", str(HERE / name))
    assert selected["phase_receipt"]["path"] == (
        "Stage1_Instances/THM-M-0131/statement-receipt.json"
    )
    assert selected["phase_receipt"]["sha256"] is selected["phase_receipt"]["git_blob"] is None
    for name, (expected_sha, expected_blob) in EXPECTED_BINDINGS.items():
        path = HERE / name
        assert sha256(path) == expected_sha
        assert git("hash-object", str(path)) == expected_blob

    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    assert status.returncode == 0, status.stderr.decode()
    changed = {
        entry.decode("utf-8")[3:] for entry in status.stdout.split(b"\x00") if entry
        and entry.decode("utf-8")[3:] != "Formalizations/Lean/.lake"
    }
    assert changed == EXPECTED_CHANGED_PATHS
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    assert prohibited.search(code) is None
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
        print(json.dumps(failure, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(SEMANTIC_RESULT, ensure_ascii=True, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
