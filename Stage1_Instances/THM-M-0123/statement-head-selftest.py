#!/usr/bin/env python3
"""Reconcile the immutable statement validator result with the current HEAD context."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ITEM_ID = "S56-M-0123-STATEMENT"
THEOREM_ID = "THM-M-0123"
BASE_REVISION = "6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049"
BASE_TREE = "28c148dbd84fbd549c749f060c92c9a3f00b16d0"
GRAPH_SHA256 = "80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5"
CONTEXT_SHA256 = "0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
VALIDATOR_BASE_GIT_BLOB = "7e8361406b58df1ec9fb56994f171b21d896a537"
VALIDATOR_SHA256 = "8b0047cdbb7df962f2f3bbbebf2bb06bc10d298166975b15e608026fc06b0470"
LEDGER_SHA256 = "030c115cec3df51cfaf330691704941c26cc83e27b0a6f0753d5078325a1939a"
STATEMENT_RECORD_SHA256 = "b694c7bda539f8a71cc519141d812119dca160726d805a11d83e0547d84b642c"
STATEMENT_SOURCE_SHA256 = "62c3d5936d64ed2225d239246ac8139663bc4f722f896625b94bb9a11e59ca8f"
CROSSWALK_SHA256 = "c4e661c736bca150a662d8d3dafa82bf6bcfde428b2e45a0715c394f81468205"
EXPRESSION_SHA256 = "9fa3c7a0bff55098e7cc234793cb06ec1628e84e003ddb273a6dc47094f58dbd"
LEAN_OUTPUT_SHA256 = "f57215dfa63c8993cf43abfd1a3bbe60715bdda3e635f2c4a9a8cf35591748a6"
SHARED_GROUP_ID = "SHARED-MODULE-dff4d00d3b45e946"
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0123/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0123/statement-head-selftest.py",
    "Stage1_Instances/THM-M-0123/statement-receipt.json",
    "Stage1_Instances/THM-M-0123/statement-validation.md",
    "Stage1_Instances/THM-M-0123/statement.json",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} is not a JSON object")
    return value


def git(*argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False
    )
    if result.returncode:
        raise ValueError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def verify() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        raise ValueError("repository HEAD differs from the worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("repository tree differs from the worker base")
    if sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        raise ValueError("v2 theorem DAG digest changed")
    if sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        raise ValueError("phase contract digest changed")

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    candidates = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if candidates != ["Stage1_Instances/THM-M-0123/check_statement.py"]:
        raise ValueError("scheduler validator candidate is missing or ambiguous")
    validator = ROOT / candidates[0]
    if git("rev-parse", f"HEAD:{candidates[0]}") != VALIDATOR_BASE_GIT_BLOB:
        raise ValueError("scheduler validator base blob changed")
    if sha256(validator) != VALIDATOR_SHA256:
        raise ValueError("scheduler validator worktree bytes changed")

    dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    if node["v2_execution_rank"] != 276 or node["topological_layer"] != 0:
        raise ValueError("v2 claim order changed")
    if node["phase_states"]["statement"] != "[_]" or node["phase_attempts"]["statement"] != 1:
        raise ValueError("authoritative statement cursor changed")
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("dependency context changed")
    for field in ("direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids"):
        if node[field] != []:
            raise ValueError(f"unexpected nonempty dependency field {field}")
    if node["shared_lemma_group_ids"] != [SHARED_GROUP_ID]:
        raise ValueError("shared-group context changed")

    fixed = {
        "Statement.lean": STATEMENT_SOURCE_SHA256,
        "statement.json": STATEMENT_RECORD_SHA256,
        "source-statement-crosswalk.md": CROSSWALK_SHA256,
        "dependency-reuse-ledger.json": LEDGER_SHA256,
    }
    for name, expected in fixed.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned statement input changed: {name}")

    statement = load(HERE / "statement.json")
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise ValueError("canonical expression fingerprint changed")
    if formal["statement_file_sha256"] != STATEMENT_SOURCE_SHA256:
        raise ValueError("canonical source fingerprint changed")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema changed")
    if ledger.get("consumer_theorem_id") != THEOREM_ID:
        raise ValueError("dependency ledger owner changed")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        raise ValueError("dependency ledger graph binding changed")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency ledger context binding changed")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "parent_inspection_order", "inspections",
        "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            raise ValueError(f"empty dependency field changed: {field}")
    if ledger.get("shared_group_ids") != [SHARED_GROUP_ID]:
        raise ValueError("shared group is missing from the ledger")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list) or len(decisions) != 1:
        raise ValueError("shared-group decision is missing or ambiguous")
    decision = decisions[0]
    if decision.get("source_id") != SHARED_GROUP_ID or decision.get("decision") != "not_applicable":
        raise ValueError("shared-group reuse boundary changed")
    for path_string, expected in decision["inspected_member"]["artifact_digests"].items():
        if sha256(ROOT / path_string) != expected:
            raise ValueError(f"inspected provider artifact changed: {path_string}")
    if ledger.get("closure_audit", {}).get("accepted_reuse") != []:
        raise ValueError("provider proof or acceptance was transferred")

    receipt = load(HERE / "statement-receipt.json")
    required = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent",
        "base_revision", "base_tree", "inputs", "support_state", "proposed_state",
        "accepted", "verdict", "selftest_status", "selftest_result", "known_failures",
        "first_failed_gate", "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "statement_fingerprints", "mutation_tests",
    }
    if not required.issubset(receipt):
        raise ValueError("phase receipt omits contract-required fields")
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        raise ValueError("phase receipt schema changed")
    if receipt["item_id"] != ITEM_ID or receipt["theorem_id"] != THEOREM_ID:
        raise ValueError("phase receipt identity changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise ValueError("phase receipt base changed")
    if receipt["accepted"] is not False or receipt["proposed_state"] != "[_]":
        raise ValueError("phase receipt transfers master acceptance")
    if receipt["selftest_status"] != "passed" or receipt["selftest_result"]["exit_code"] != 0:
        raise ValueError("phase receipt self-test status changed")
    if receipt["validator_sha256"] != VALIDATOR_SHA256:
        raise ValueError("phase receipt validator binding changed")
    if receipt["statement_fingerprints"] != [f"sha256:{EXPRESSION_SHA256}"]:
        raise ValueError("phase receipt statement fingerprint changed")
    if receipt["lean_output_sha256"] != LEAN_OUTPUT_SHA256:
        raise ValueError("phase receipt Lean-output fingerprint changed")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("phase receipt overclaims a terminal state")
    if receipt.get("changed_paths") != CHANGED_PATHS:
        raise ValueError("phase receipt changed-path inventory changed")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise ValueError("worker packet identity changed")
    if packet["base_revision"] != BASE_REVISION:
        raise ValueError("worker packet base changed")
    if packet.get("changed_paths") != CHANGED_PATHS:
        raise ValueError("worker packet changed-path inventory changed")
    if packet["commands"] != receipt["selftest_result"]["commands"]:
        raise ValueError("worker packet commands differ from the phase receipt")


def main() -> None:
    try:
        verify()
    except Exception as error:
        result = {
            "schema_version": "stage1-validator-semantic-result/1.0",
            "item_id": ITEM_ID,
            "theorem_id": THEOREM_ID,
            "phase": "statement",
            "status": "failed",
            "verdict": "repair_required",
            "phase_accepted": False,
            "audit_complete": False,
            "theorem_complete": False,
            "phase_predicate_proven": False,
            "first_failed_gate": "S56-M-0123-STATEMENT.head_reconciliation",
            "open_obligations": 1,
            "stale_inputs": [],
            "blocked": False,
            "message": f"HEAD statement reconciliation failed closed: {error}",
        }
    else:
        result = {
            "schema_version": "stage1-validator-semantic-result/1.0",
            "item_id": ITEM_ID,
            "theorem_id": THEOREM_ID,
            "phase": "statement",
            "status": "passed",
            "verdict": "phase_accepted",
            "phase_accepted": True,
            "audit_complete": False,
            "theorem_complete": False,
            "phase_predicate_proven": True,
            "first_failed_gate": None,
            "open_obligations": 0,
            "stale_inputs": [],
            "blocked": False,
            "message": (
                "The unchanged scheduler validator's prior Lean fingerprints remain byte-bound; "
                "current HEAD claim order, unique validator selection, statement artifacts, empty "
                "hard closure, weak-group non-reuse, receipt, and worker packet agree."
            ),
        }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
