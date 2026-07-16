#!/usr/bin/env python3
"""Validate the target-scoped negative statement result for THM-M-0140."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
THEOREM_ID = "THM-M-0140"
ITEM_ID = "S56-M-0140-STATEMENT"
BASE_REVISION = "2dc5a410b68eff806858fd6ed0cb33d57f6209f7"
BASE_TREE = "841bdd6114e7436cff4a3a1ff248fc1e884a9ddc"
TARGET_SET_SHA256 = "e07deabaab3463cc1f92cdf5c0cf50ad9f8270d35554529c375d20a8512d8f1a"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FIRST_FAILED_GATE = "S02-EXACT-TARGET.source_statement_identity"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0140/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0140/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0140/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0140/statement-receipt.json",
}
ROLE_BINDINGS = {
    "statement_record": (
        "23f955de9cbd8166373e502c0cb837aac190e0a5a6388c4b4919b86035adb7cb",
        "e0b85d4926befb11d4ce53c85530612c51b7e599",
    ),
    "statement_source": (
        "181cd5a5174d2a083498c4f34b5f950d72d44f8cd4d74cdf171db5b45eb82935",
        "1c488622ad90f0453bd012c3f6ecf235448986fd",
    ),
    "source_crosswalk": (
        "852cca2d8e1ae210103ccc207ebedf1df51a77c473a50ed5ecec274512fef2a7",
        "47a747d9b29b554089322d3131b8666cd8451ff7",
    ),
}
SEMANTIC = {
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
    "first_failed_gate": FIRST_FAILED_GATE,
    "open_obligations": 1,
    "stale_inputs": [],
    "blocked": True,
    "message": "Exact source-bound target identity and required conventions are unresolved; the diagnostic Coxeter API elaborates, but no canonical Lean proposition is declared.",
}


def load(relative: str) -> dict:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{relative} must contain one JSON object"
    return value


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def check() -> None:
    manifest = load("Docs/Stage1_Targets_rev-5.6.json")
    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    statement = load(ROLE_PATHS["statement_record"])
    receipt = load(ROLE_PATHS["phase_receipt"])
    ledger = load("Stage1_Instances/THM-M-0140/dependency-reuse-ledger.json")
    handoff = load(".stage1-worker-selftest.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 56
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID
    assert item["phase"] == "statement" and item["layer"] == 1
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0140-INTAKE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 290 and node["topological_layer"] == 0
    assert node["phase_states"]["intake"] == "[_]"
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["direct_hard_parents"] == []
    assert node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == []
    assert node["shared_lemma_group_ids"] == []
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert theorem_dag["target_id_set_sha256"] == TARGET_SET_SHA256
    assert theorem_dag["execution_contract"]["claim_order"] == [
        "v2_execution_rank",
        "phase_layer",
        "phase_item_id",
    ]
    assert theorem_dag["execution_contract"]["proof_parent_inspection"] == {
        "scope": ["direct_hard_parents", "transitive_hard_ancestors"],
        "order": "ascending_v2_execution_rank_parent_before_child",
        "complete_closure_required": True,
    }
    assert sha256("Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256

    phase_contract = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert contract["schema_version"] == "stage1-phase-acceptance-contracts/1.0"
    assert sha256("Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256
    assert phase_contract["intent"] == "audit" and phase_contract["layer"] == 1
    assert phase_contract["raw_blocked_can_close_phase"] is False
    assert phase_contract["classified_negative_findings_may_satisfy_deliverable"] is False
    assert contract["verdict_protocol"]["blocked_policy"] == {
        "raw_blocked_can_close_phase": False,
        "raw_blocked_auto_promotes": False,
        "required_action": "remain_worker_self_tested_and_emit_repair_or_blocker",
    }
    selected = {
        role["role"]: next(
            path.format(theorem_id=THEOREM_ID)
            for path in role["path_candidates"]
            if (ROOT / path.format(theorem_id=THEOREM_ID)).is_file()
        )
        for role in phase_contract["required_artifact_roles"]
    }
    assert selected == ROLE_PATHS
    assert [row["path_pattern"] for row in phase_contract["validator_candidates"]] == [
        "Stage1_Instances/{theorem_id}/check_statement.py",
        "Stage1_Instances/{theorem_id}/check_statement_artifacts.py",
    ]
    assert not (HERE / "check_statement_artifacts.py").exists()

    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM_ID
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    assert ledger["claim_order"] == {
        "v2_execution_rank": 290,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }
    context_arrays = (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    )
    assert all(ledger[field] == [] for field in context_arrays)
    assert ledger["closure_audit"]["parent_inspection_order"] == []
    assert ledger["closure_audit"]["inspected_parent_ids"] == []
    assert ledger["closure_audit"]["status"] == "empty_context_audited"

    assert statement["schema_version"] == "stage1-statement/1.0"
    assert statement["item_id"] == ITEM_ID and statement["theorem_id"] == THEOREM_ID
    assert statement["canonical_statement"] == (
        "For a Coxeter system, its generic one-parameter Hecke algebra admits a unique "
        "canonical basis characterized by bar invariance and the prescribed triangular "
        "normalization relative to the standard basis."
    )
    formal = statement["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    assert formal["module"] is None
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_sha256"] is None
    assert formal["statement_file_sha256"] == ROLE_BINDINGS["statement_source"][0]
    assert statement["ordered_binders"] is None
    assert statement["ordered_binders_status"] == "unresolved_target_identity"
    assert statement["hypotheses"] is None
    assert statement["hypotheses_status"] == "unresolved_target_identity"
    assert statement["statement_elaborated"] is False
    assert statement["theorem_proved"] is statement["theorem_complete"] is False
    assert statement["root_vector_observed"] == {
        "human": "H1",
        "machine": "M5",
        "readability": "R3",
    }
    assert statement["gate_state"] == "blocked_exact_target_identity"
    assert statement["first_failed_gate"] == FIRST_FAILED_GATE
    assert len(statement["unresolved_target_identity"]) >= 7
    assert set(statement["mutation_tests"].values()) == {
        "not_run_target_identity_blocked"
    }
    assert statement["alternate_encodings"]["legacy_abstract_shape"]["relationship"] == (
        "not_credited_statement_substitution"
    )
    assert statement["alternate_encodings"]["atlas_lean_candidate"]["relationship"] == (
        "uncredited_anchor_lead"
    )
    assert statement["alternate_encodings"]["atlas_lean_candidate"]["source_sha256"] == (
        "71d5c6ea34f0156f41000e8a2babe87854c99954736b1d9ae46954544ca16766"
    )

    required_receipt_fields = {
        pointer.split("/")[-1]
        for pointer in phase_contract["phase_receipt_required_fields"]
        if pointer.count("/") == 1
    }
    assert required_receipt_fields <= set(receipt)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert receipt["worker_verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["inputs"]["dependency_state"] == {
        "item_id": "S56-M-0140-INTAKE",
        "authoritative_state": "[_]",
        "accepted": False,
        "assessment": "The intake predecessor is provisional and unaccepted. This negative statement audit is dependency-ordered evidence only and cannot become master-accepted before its predecessor.",
    }
    assert receipt["inputs"]["preexisting_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["selftest_status"] == "passed"
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["commands"]
    assert receipt["first_failed_gate"] == FIRST_FAILED_GATE
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["root_vector_before"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M5", "R": "R3"}
    assert receipt["statement_fingerprints"] == []
    assert [row["kind"] for row in receipt["mutation_tests"]] == [
        "removed_hypothesis",
        "changed_domain",
        "changed_binder_scope",
        "boundary_case",
    ]
    assert all(
        row["result"] == "not_run_target_identity_blocked"
        for row in receipt["mutation_tests"]
    )
    assert receipt["result"] == {
        "semantic_verdict": "blocked",
        "phase_accepted": False,
        "phase_predicate_proven": False,
        "blocked": True,
    }
    assert receipt["known_failures"] and receipt["retry_condition"]
    assert "fresh base" in receipt["retry_condition"]
    assert "primary-source" in receipt["retry_condition"]
    assert "phase_evidence_accepted=false" in receipt["status_boundary"]
    assert handoff["item_id"] == ITEM_ID and handoff["state"] == "[_]"
    assert handoff["worker_verdict"] == handoff["verdict"] == receipt["verdict"]
    assert handoff["base_revision"] == BASE_REVISION
    assert handoff["commands"] == receipt["selftest_result"]["commands"]
    assert handoff["known_failures"]
    assert set(handoff["changed_paths"]) == {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0140/Statement.lean",
        "Stage1_Instances/THM-M-0140/check_statement.py",
        "Stage1_Instances/THM-M-0140/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0140/source_statement_crosswalk.md",
        "Stage1_Instances/THM-M-0140/statement-blocker.md",
        "Stage1_Instances/THM-M-0140/statement-receipt.json",
        "Stage1_Instances/THM-M-0140/statement.json",
    }

    assert set(receipt["artifact_bindings"]) == set(ROLE_PATHS)
    for role, relative in ROLE_PATHS.items():
        binding = receipt["artifact_bindings"][role]
        assert binding["role"] == role and binding["path"] == relative
        if role == "phase_receipt":
            assert binding["sha256"] == "self_referential_excluded"
            assert binding["git_blob"] == "self_referential_excluded"
        else:
            expected_sha256, expected_blob = ROLE_BINDINGS[role]
            assert binding["sha256"] == expected_sha256 == sha256(relative)
            assert binding["git_blob"] == expected_blob == git_blob(relative)

    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    assert source.count("import ") == 1
    assert "import Mathlib.GroupTheory.Coxeter.Length" in source
    assert "#check CoxeterSystem.length" in source
    prohibited = ("sorry", "admit", "axiom", "opaque", "unsafe")
    assert all(token not in source.lower() for token in prohibited)
    assert not any(token in source for token in ("theorem ", "lemma ", "def "))

    result = subprocess.run(
        ["lake", "env", "lean", "--trust=0", "../../Stage1_Instances/THM-M-0140/Statement.lean"],
        cwd=LEAN_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout
    for name in (
        "CoxeterMatrix",
        "CoxeterSystem",
        "CoxeterSystem.simple",
        "CoxeterSystem.wordProd",
        "CoxeterSystem.length",
        "CoxeterSystem.IsReduced",
    ):
        assert name in result.stdout

    for relative in {
        *ROLE_PATHS.values(),
        "Stage1_Instances/THM-M-0140/check_statement.py",
        "Stage1_Instances/THM-M-0140/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0140/statement-blocker.md",
        ".stage1-worker-selftest.json",
    }:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {relative}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    check()
    print(json.dumps(SEMANTIC, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
