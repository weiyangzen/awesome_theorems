#!/usr/bin/env python3
"""Fail-closed semantic release reconciliation for S56-M-0393-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0393"
ITEM = "S56-M-0393-RELEASE"
THEOREM = "THM-M-0393"
BASE_REVISION = "c5037228977a81948bbd6119e1728b4b65b9924e"
BASE_TREE = "78b2627e717156dffe240bea12d14205af667d2a"
GRAPH_SHA256 = "fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"

EXPECTED_HASHES = {
    "Statement.lean": "456c62756bc035e675135270bf6984c00bb1203bc6687d3495ae7663131d985f",
    "Proof.lean": "a77c1d1e431a36db1bd8ae48f2511150a2519e3a88a319e84256c88229c3f29f",
    "Validation.lean": "0086ee0ab6d416a49f51f476fbacb5d1f318bb2ce49e82b6b13a3c73c138696e",
    "obligation-registry.json": "57bd847a36b0883078dece89081bff185fae7b74cabf814c01daa7f7e184aa66",
    "typed-graphs.json": "3b6e634f6134346598fee300291daafa13b3d91aa2afc59dad0a66741595ae6c",
    "proof-receipt.json": "b74728f6a34837f467e2bf9beaad0aaeef7894c56c84ac3264ac3209b7372234",
    "validation-receipt.json": "e799386f8a5c361d7d2cd1fc310afd6d5b6de0b23ee19976e8bd828586e3921c",
    "dependency-reuse-ledger.json": "c6bb38200b521717fffa97270da37248eafd778cdb5d22b6dc18f78bebb43802",
    "release-spec.json": "3a198579b662eb1ea6a5de4fa0a9de3802ed4369492aec0b75968524eb42202d",
    "release-decision.json": "88deaddedf30405e4fca5e1ddf80d86543af697f0f40b68bc8b01a6f77ae1bcf",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_text(*argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    assert result.returncode == 0, (argv, result.returncode, result.stderr)
    return result.stdout.strip()


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    spec = load(HERE / "release-spec.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git_text("rev-parse", "HEAD") == BASE_REVISION
    assert git_text("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256
    for name, expected in EXPECTED_HASHES.items():
        assert sha256(HERE / name) == expected, f"release input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 6 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 6,
        "phase": "release",
        "layer": 6,
        "state": "[_]",
        "depends_on": ["S56-M-0393-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 1,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0393-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM)
    assert node["v2_execution_rank"] == 6
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == []
    assert node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == []
    assert node["shared_lemma_group_ids"] == []

    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    for key in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        assert ledger[key] == [], key
    assert ledger["closure_audit"]["inspection_order"] == []
    assert ledger["closure_audit"]["status"] == "empty_closure_inspected"

    ids = {row["id"] for row in registry["obligations"]}
    assert len(ids) == 17 and graphs["proof_graph"]["root"] == "M0393-ROOT"
    assert registry["root_vector"] == {"human": "H3", "machine": "M4", "readability": "R3"}
    assert registry["theorem_complete"] is False
    assert all(row["body"] is None for row in registry["obligations"])
    assert all(
        row["state"] == "planned_open"
        for row in graphs["proof_graph"]["composition_certificates"]
    )
    assert graphs["evidence_graph"]["evidence_nodes"] == []

    assert proof["support_state"] == validation["support_state"] == "provisional_worker_selftest"
    assert proof["result"]["root_closed"] is False
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["validated_closed_obligation_ids"] == []
    assert validation["result"]["validated_partial_obligation_ids"] == ["M0393-N1"]
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    for name, declaration in {
        "Proof.lean": "finite_pow_divisors",
        "Validation.lean": "independent_finite_pow_divisors",
    }.items():
        source = (HERE / name).read_text(encoding="utf-8")
        assert re.search(rf"\btheorem\s+{declaration}\b", source)
        assert not re.search(
            r"\b(sorry|admit)\b|^[ \t]*(axiom|unsafe)\b", source, re.MULTILINE
        )

    assert decision["item_id"] == ITEM and decision["verdict"] == "blocked"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }
    assert decision["first_failed_gate"]["gate_id"] == "G02-TOPOLOGY"
    assert decision["first_failed_release_assurance_gate"]["gate_id"] == "R01-ARTIFACTS"
    assert decision["dependency"]["master_accepted"] is False
    assert decision["dependency"]["receipt_sha256"] == EXPECTED_HASHES["validation-receipt.json"]
    assert decision["evidence_reconciliation"]["open_root_relevant_obligation_count"] == 17
    assert decision["evidence_reconciliation"]["closed_obligation_ids"] == []
    assert decision["evidence_reconciliation"]["partial_obligation_ids"] == ["M0393-N1"]
    assert len(decision["remaining_root_cut_set"]) == 14
    assert all(value is False for key, value in decision["release_protocol"].items()
               if key not in {"specification_path", "specification_sha256", "status"})

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["phase"] == "release"
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert set(spec["covered_obligation_ids"]) == ids
    assert set(spec["release_protocol"].values()) == {"required_not_satisfied"}

    required_receipt_fields = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent",
        "base_revision", "base_tree", "inputs", "support_state", "proposed_state",
        "accepted", "verdict", "selftest_status", "selftest_result", "known_failures",
        "first_failed_gate", "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "release_grade",
        "accepted_receipt_ids", "remaining_root_cut_set", "root_vector_after",
        "deterministic_bundle_sha256", "independent_attestations", "result",
    }
    assert required_receipt_fields <= set(receipt)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["selftest_status"] == "passed"
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["commands"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["deterministic_bundle_sha256"] is None
    assert receipt["independent_attestations"] == []
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]
    assert receipt["root_vector_after"] == {"H": "H3", "M": "M4", "R": "R3"}
    assert receipt["result"] == {
        "exit_code": 0,
        "semantic_verdict": "blocked",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "open_obligations": 17,
        "first_failed_gate": "G02-TOPOLOGY",
    }
    validator_binding = receipt["inputs"]["release_validator"]
    assert validator_binding["path"] == f"Stage1_Instances/{THEOREM}/check_release.py"
    assert validator_binding["sha256"] == sha256(HERE / "check_release.py")
    assert validator_binding["git_blob"] == git_text(
        "hash-object", f"Stage1_Instances/{THEOREM}/check_release.py"
    )

    semantic = {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "release",
        "status": "blocked",
        "verdict": "blocked",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": "G02-TOPOLOGY",
        "open_obligations": 17,
        "stale_inputs": [],
        "blocked": True,
        "message": (
            "Validation is not master accepted; AUDIT-Z and THEOREM-Z are false, "
            "the exact root is open, and required release evidence is absent."
        ),
    }
    print(json.dumps(semantic, ensure_ascii=True, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
