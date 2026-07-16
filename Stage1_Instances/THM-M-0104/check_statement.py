#!/usr/bin/env python3
"""Validate THM-M-0104's fail-closed statement evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0104-STATEMENT"
THEOREM = "THM-M-0104"
BASE_REVISION = "74d4c272070069bc62df15798895293b4795940a"
BASE_TREE = "6693e584a3d529077306168fe38abd693d210ef0"
GRAPH_SHA256 = "cb4b83c4c4a5474fce51f98098f1421315fe7f1bd8cd52205932e57eced9f675"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
STATEMENT_SHA256 = "9587255d33e025d5d3454cdc9a73bc5354fbed064df61f7f8633a2088033fe9e"
RECORD_SHA256 = "4c60674e14947720efdefb8b4de0e135e0bd70275a57242db4d2cf21b5f79ce7"
CROSSWALK_SHA256 = "fd12d8f25f6c77a678c285a749c95d898b998806d687698cc09b3055aee511b0"
LEDGER_SHA256 = "a4083aaed0474dd2ff6d6d729cbb660a65cb9d3b10050eb0a2c9817f91a62876"
BLOCKER_SHA256 = "ac5eea251bca2eb134910bd77681300e146220fa7b6a2d0c975fd4b6701aa9fa"
FAILED_GATE = "S02-EXACT-TARGET.exact_source_statement_identity_and_intersection_conventions"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0104/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0104/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0104/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0104/statement-receipt.json",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
    r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def load(relative: str) -> dict[str, Any]:
    path = ROOT / relative

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key in {relative}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        fail(f"{relative} must contain one JSON object")
    return value


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git(*argv: str) -> str:
    result = subprocess.run(
        ["/usr/bin/git", *argv], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode != 0:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def pointer(document: dict[str, Any], raw: str) -> Any:
    value: Any = document
    for component in raw.removeprefix("/").split("/"):
        if not isinstance(value, dict) or component not in value:
            fail(f"missing required receipt pointer {raw}")
        value = value[component]
    return value


def strip_lean_comments(source: str) -> str:
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
    if depth or in_string:
        fail("unclosed Lean comment or string")
    return "".join(output)


def check() -> None:
    if sys.flags.optimize != 0:
        fail("statement validation requires ordinary Python mode")
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository base tree differs from receipt")

    contract_path = "Docs/Stage1_Phase_Acceptance_Contracts.json"
    dag_path = "Docs/Stage1_Theorem_DAG_v2.json"
    contract = load(contract_path)
    theorem_dag = load(dag_path)
    record = load(ROLE_PATHS["statement_record"])
    receipt = load(ROLE_PATHS["phase_receipt"])
    ledger = load("Stage1_Instances/THM-M-0104/dependency-reuse-ledger.json")

    for name, binding in receipt["inputs"].items():
        if not isinstance(binding, dict) or "path" not in binding:
            continue
        relative = binding["path"]
        if binding.get("sha256") != sha256(relative):
            fail(f"receipt input SHA-256 binding changed: {name}")
        if binding.get("git_blob") != git_blob(relative):
            fail(f"receipt input Git blob binding changed: {name}")

    if sha256(contract_path) != CONTRACT_SHA256:
        fail("phase acceptance contract changed")
    if sha256(dag_path) != GRAPH_SHA256:
        fail("theorem DAG changed")
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    if phase["intent"] != "audit":
        fail("statement intent changed")
    if phase["raw_blocked_can_close_phase"] is not False:
        fail("blocked statement unexpectedly became phase-completing")
    if phase["classified_negative_findings_may_satisfy_deliverable"] is not False:
        fail("negative evidence unexpectedly became the positive deliverable")
    if [row["gate_id"] for row in phase["semantic_gates"]] != [
        "S01-ARTIFACTS", "S02-EXACT-TARGET", "S03-MUTATIONS"
    ]:
        fail("statement semantic gates changed")

    selected: dict[str, str] = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            raw.format(theorem_id=THEOREM)
            for raw in role["path_candidates"]
            if (ROOT / raw.format(theorem_id=THEOREM)).is_file()
        ]
        if len(candidates) != 1:
            fail(f"artifact role {role['role']} does not resolve exactly once")
        selected[role["role"]] = candidates[0]
    if selected != ROLE_PATHS:
        fail("contract-selected statement artifact roles changed")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0104/check_statement.py"]:
        fail("statement validator candidate is missing or ambiguous")

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM)
    if node["v2_execution_rank"] != 266:
        fail("target v2 rank changed")
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        fail("target dependency context changed")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        if node[field] != []:
            fail(f"declared empty dependency field changed: {field}")
    expected_ledger = {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM,
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
    if ledger != expected_ledger:
        fail("dependency ledger is not the exact audited empty context")
    if sha256("Stage1_Instances/THM-M-0104/dependency-reuse-ledger.json") != LEDGER_SHA256:
        fail("dependency ledger bytes changed")

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    code = strip_lean_comments(source)
    if re.findall(r"^import (\S+)$", code, re.MULTILINE) != [
        "Mathlib.RingTheory.MvPolynomial.Homogeneous"
    ]:
        fail("negative substrate import changed")
    checks = re.findall(r"^#check (\S+)$", code, re.MULTILINE)
    for symbol in ("MvPolynomial", "MvPolynomial.IsHomogeneous", "MvPolynomial.totalDegree"):
        if checks.count(symbol) != 1:
            fail(f"substrate check changed: {symbol}")
    if re.search(r"^\s*(?:def|theorem|lemma|example|structure|class|inductive)\s+", code, re.MULTILINE):
        fail("Statement.lean invents a canonical declaration")
    if PROHIBITED.search(code):
        fail("Statement.lean contains a prohibited construct")
    if sha256(ROLE_PATHS["statement_source"]) != STATEMENT_SHA256:
        fail("statement source bytes changed")
    if sha256(ROLE_PATHS["statement_record"]) != RECORD_SHA256:
        fail("statement record bytes changed")
    if sha256(ROLE_PATHS["source_crosswalk"]) != CROSSWALK_SHA256:
        fail("source crosswalk bytes changed")
    if sha256("Stage1_Instances/THM-M-0104/statement-blocker-head-74d4c272-slot42.md") != BLOCKER_SHA256:
        fail("blocker report bytes changed")

    if record["schema_version"] != "stage1-statement/1.0":
        fail("statement record schema changed")
    if record["item_id"] != ITEM or record["theorem_id"] != THEOREM:
        fail("statement record identity changed")
    if record["status"] != "blocked_unfrozen" or record["canonical_statement"] is not None:
        fail("statement record invents a canonical human claim")
    formal = record["canonical_formal_target"]
    for field in (
        "module", "declaration_or_expression", "elaborated_expression_sha256",
        "environment_fingerprint_sha256",
    ):
        if formal[field] is not None:
            fail(f"statement record invents formal target field {field}")
    if formal["statement_file_sha256"] != STATEMENT_SHA256:
        fail("statement record source binding changed")
    if record["statement_fingerprints"] != [] or record["alternate_encodings"] != []:
        fail("statement record invents fingerprints or transports")
    if record["statement_elaborated"] is not False:
        fail("statement record falsely claims target elaboration")
    if record["first_failed_gate"] != FAILED_GATE:
        fail("statement record failed-gate boundary changed")
    if record["audit_complete"] is not False or record["theorem_complete"] is not False:
        fail("statement record overclaims a terminal decision")
    mutations = record["mutation_tests"]
    if set(mutations) != {
        "removed_hypothesis", "changed_domain", "changed_binder_scope", "boundary_case"
    } or set(mutations.values()) != {"undefined_without_canonical_statement"}:
        fail("undefined statement mutations changed")

    for raw in phase["phase_receipt_required_fields"]:
        pointer(receipt, raw)
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        fail("statement receipt schema changed")
    if (receipt["item_id"], receipt["theorem_id"], receipt["phase"], receipt["intent"]) != (
        ITEM, THEOREM, "statement", "audit"
    ):
        fail("statement receipt identity changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        fail("statement receipt base changed")
    if receipt["claim_order"] != {
        "v2_execution_rank": 266,
        "phase_layer": 1,
        "phase_item_id": ITEM,
    }:
        fail("claim order binding changed")
    if receipt["verdict"] != "blocked" or receipt["accepted"] is not False:
        fail("receipt does not preserve blocked worker semantics")
    if receipt["proposed_state"] != "[_]" or receipt["selftest_status"] != "passed":
        fail("receipt does not represent a checked unfinished worker handoff")
    if receipt["selftest_result"]["exit_code"] != 0 or not receipt["selftest_result"]["commands"]:
        fail("receipt lacks successful self-test command evidence")
    if receipt["selftest_result"]["phase_predicate_passed"] is not False:
        fail("receipt falsely claims the phase predicate")
    if receipt["statement_fingerprints"] != []:
        fail("receipt invents a statement fingerprint")
    receipt_mutations = receipt["mutation_tests"]
    if {row["kind"] for row in receipt_mutations} != set(mutations):
        fail("receipt mutation classes are incomplete")
    if any(row["passed"] is not False for row in receipt_mutations):
        fail("receipt falsely passes a statement mutation")
    if receipt["first_failed_gate"] != FAILED_GATE:
        fail("receipt failed-gate boundary changed")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        fail("receipt overclaims a terminal decision")
    dependency = receipt["dependency_context"]
    for field in (
        "parent_inspection_order", "inspected_parent_ids", "direct_parent_ids",
        "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids",
        "shared_group_ids", "reuse_decisions", "unresolved_compatibility_obligations",
    ):
        if dependency[field] != []:
            fail(f"receipt invents dependency context: {field}")

    selected_receipt = {row["role"]: row for row in receipt["selected_artifacts"]}
    if set(selected_receipt) != set(ROLE_PATHS):
        fail("receipt selected-artifact role set changed")
    input_keys = {
        "statement_record": "statement_record",
        "statement_source": "statement_source",
        "source_crosswalk": "source_crosswalk",
    }
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        binding = selected_receipt[role]
        relative = ROLE_PATHS[role]
        if binding != {
            "role": role, "path": relative,
            "sha256": sha256(relative), "git_blob": git_blob(relative),
        }:
            fail(f"receipt role binding changed: {role}")
        input_binding = receipt["inputs"][input_keys[role]]
        if input_binding != binding:
            fail(f"receipt input binding changed: {role}")
    self_binding = selected_receipt["phase_receipt"]
    if self_binding["path"] != ROLE_PATHS["phase_receipt"]:
        fail("receipt self-role path changed")
    if self_binding["sha256"] is not None or self_binding["git_blob"] is not None:
        fail("receipt recursively binds itself")
    validator_relative = "Stage1_Instances/THM-M-0104/check_statement.py"
    if receipt["inputs"]["statement_validator"] != {
        "path": validator_relative,
        "sha256": sha256(validator_relative),
        "git_blob": git_blob(validator_relative),
    }:
        fail("receipt validator binding changed")

    packet = load(".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "worker_verdict", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }:
        fail("worker handoff field set changed")
    if packet["item_id"] != ITEM or packet["worker_verdict"] != "blocked":
        fail("worker handoff identity or verdict changed")
    if packet["base_revision"] != BASE_REVISION or packet["state"] != "[_]":
        fail("worker handoff base or state changed")
    if packet["commands"] != receipt["selftest_result"]["commands"]:
        fail("worker handoff commands differ from receipt")
    if packet["known_failures"] != receipt["known_failures"]:
        fail("worker handoff known failures differ from receipt")
    if packet["output_summary"] != receipt["selftest_result"]["output_summary"]:
        fail("worker handoff summary differs from receipt")
    expected_paths = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0104/Statement.lean",
        "Stage1_Instances/THM-M-0104/check_statement.py",
        "Stage1_Instances/THM-M-0104/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0104/statement-blocker-head-74d4c272-slot42.md",
        "Stage1_Instances/THM-M-0104/statement-receipt.json",
        "Stage1_Instances/THM-M-0104/statement.json",
    }
    if set(packet["changed_paths"]) != expected_paths:
        fail("worker handoff does not cover the exact changed paths")
    status = subprocess.run(
        ["/usr/bin/git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if status.returncode != 0:
        fail(f"git status failed: {status.stderr.strip()}")
    actual_changes = set(status.stdout.splitlines())
    actual_paths = {
        line[3:] for line in actual_changes
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_paths != expected_paths:
        fail("worktree changes differ from worker handoff")
    for relative in expected_paths:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"changed artifact has invalid text boundary: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"changed artifact has trailing whitespace: {relative}")


def semantic_result(*, failed: bool, message: str) -> dict[str, Any]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "statement",
        "status": "failed" if failed else "blocked",
        "verdict": "repair_required" if failed else "blocked",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": "S01-ARTIFACTS.negative_evidence_validation" if failed else FAILED_GATE,
        "open_obligations": 4,
        "stale_inputs": [],
        "blocked": not failed,
        "message": message,
    }


def main() -> None:
    try:
        check()
    except Exception as exc:
        print(json.dumps(
            semantic_result(failed=True, message=f"Negative statement validation failed: {exc}"),
            ensure_ascii=True, sort_keys=True, separators=(",", ":"),
        ))
        raise SystemExit(1)
    print(json.dumps(
        semantic_result(
            failed=False,
            message=(
                "The target-owned packet truthfully proves that no source-authorized exact "
                "Bezout proposition, expression fingerprint, checked transport, or mutation "
                "suite exists; S56-M-0104-STATEMENT remains blocked."
            ),
        ),
        ensure_ascii=True, sort_keys=True, separators=(",", ":"),
    ))


if __name__ == "__main__":
    main()
