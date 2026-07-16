#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0112-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0112"
ITEM = "S56-M-0112-PROOF"
THEOREM = "THM-M-0112"
BASE_REVISION = "2dc5a410b68eff806858fd6ed0cb33d57f6209f7"
BASE_TREE = "841bdd6114e7436cff4a3a1ff248fc1e884a9ddc"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
TARGET_EXPRESSION_SHA256 = (
    "1daee7f6d7814d04bb7cefe87b3487fc78a862bedafbf8dc283bd6cf1a5eb654"
)
DENOMINATOR_SHA256 = (
    "5d119562299ca46e160d86947fd92a0cd5c0d50bfbac345da26eacee0b7df7f4"
)
STATEMENT_OLEAN_SHA256 = (
    "f869a1057c46e20107dd3464966d1b86c9d534d61224242ff1fc9576dffb2a77"
)
PROOF_OLEAN_SHA256 = (
    "5d11e1de5da347e936936bf2c5b4e965306a7639f98ee54404d58dfcd0173b82"
)
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "35bd5ca61ade63d95f8c4243be0a7aae1f153a0c527b54998c13f25302862dff",
    "ObligationTree.lean": "f82e2912f027091e8acc8bb9255c4f4c963fbef3f7686050d388c200b4c6e865",
    "Proof.lean": "10154b503f6927c4772054154ccd04d4691a329d2878a0e625b579c3688fbde7",
    "anchor-audit.json": "aabf178868dd890040088c04d70494b4e645af8d26df4ab1836c65ee7bda09e5",
    "obligation-registry.json": "5ebb5f85391d27ddd85fe9deb6dd8555c7657d57178e845f96a08ca8140dea13",
    "typed-graphs.json": "3db91c177026ca9a8f541049dcc82312f179d3d04c934efa8b51d19754f52894",
    "validation-specs.json": "e46182224d7c443752bdb6cc409ae15c9d69b4553e171c43c1fd32d9c31bdd38",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern|external)\b",
    re.MULTILINE,
)
# The exact candidate path becomes HEAD-tracked only after integration. Because
# it was absent at this worker base, the scheduler's unchanged-base replay gate
# remains a target-scoped blocker for this claim.
HEAD_TRACKING_BOUNDARY = "Stage1_Instances/THM-M-0112/check_proof.py"


def fail(message: str) -> None:
    raise SystemExit(message)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, child in pairs:
            if key in value:
                fail(f"duplicate JSON key in {path}: {key}")
            value[key] = child
        return value

    parsed = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(parsed, dict):
        fail(f"expected JSON object: {path}")
    return parsed


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_text(*argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if result.returncode != 0:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def main() -> None:
    if __debug__ is False:
        fail("proof validator requires Python assertions")

    receipt_path = HERE / "proof-receipt.json"
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    receipt = load(receipt_path)
    theorem_dag = load(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json")

    if git_text("rev-parse", "HEAD") != BASE_REVISION:
        fail("validator base revision drifted")
    if git_text("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("validator base tree drifted")
    if sha256(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        fail("authoritative theorem DAG drifted")
    for name, expected in EXPECTED_INPUT_HASHES.items():
        if sha256(HERE / name) != expected:
            fail(f"proof input drifted: {name}")

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM)
    if node["v2_execution_rank"] != 270 or node["topological_layer"] != 0:
        fail("v2 claim order identity drifted")
    if node["phase_states"]["proof"] != "[ ]" or node["phase_attempts"]["proof"] != 0:
        fail("authoritative proof phase is not the assigned open claim")
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        fail("dependency context drifted")
    for key in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        if node[key] != []:
            fail(f"unexpected dependency closure member in {key}")

    if ledger["schema_version"] != "stage1-dependency-reuse-ledger/1.1":
        fail("dependency ledger schema drifted")
    if ledger["consumer_theorem_id"] != THEOREM:
        fail("dependency ledger owner drifted")
    if ledger["observed_theorem_dag_sha256"] != GRAPH_SHA256:
        fail("dependency ledger graph binding is stale")
    if ledger["dependency_context_sha256"] != CONTEXT_SHA256:
        fail("dependency ledger context binding is stale")
    if ledger["repository_revision"] != BASE_REVISION:
        fail("dependency ledger revision binding is stale")
    for key in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        if ledger[key] != []:
            fail(f"empty dependency closure was not preserved: {key}")
    if ledger.get("closure_audit") != {
        "inspection_order": [],
        "expected_inspection_count": 0,
        "actual_inspection_count": 0,
        "status": "empty_closure_inspected",
        "note": (
            "The authoritative v2 node has no direct hard parents, transitive hard "
            "ancestors, reuse hints, or shared lemma groups. No provider evidence or "
            "acceptance was consumed."
        ),
    }:
        fail("empty dependency closure audit is incomplete")

    if statement["canonical_formal_target"]["elaborated_expression_sha256"] != TARGET_EXPRESSION_SHA256:
        fail("canonical target fingerprint drifted")
    if registry["root_obligation_id"] != "M0112-ROOT":
        fail("root obligation drifted")
    if registry["denominator_sha256"] != DENOMINATOR_SHA256:
        fail("obligation denominator drifted")
    if graphs["registry_denominator_sha256"] != DENOMINATOR_SHA256:
        fail("typed graph denominator drifted")
    if graphs["closure_boundary"]["root_closed"] is not False:
        fail("typed graph falsely closes the root")
    if graphs["closure_boundary"]["remaining_root_cut_set"] != [
        "M0112-B-BELOW", "M0112-B-EDGE"
    ]:
        fail("typed graph root cut set drifted")

    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        source = (HERE / name).read_text(encoding="utf-8")
        if PROHIBITED.search(source):
            fail(f"prohibited proof or trust construct in {name}")
    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    for marker in (
        "theorem not_weakTopologicalLefschetzTarget",
        "Not WeakTopologicalLefschetzTarget.{0, 0}",
        "#print axioms not_weakTopologicalLefschetzTarget",
    ):
        if marker not in proof_source:
            fail(f"negative kernel witness is missing: {marker}")

    required_receipt_fields = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent",
        "base_revision", "base_tree", "inputs", "support_state", "proposed_state",
        "accepted", "verdict", "selftest_status", "selftest_result", "known_failures",
        "first_failed_gate", "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "canonical_target",
        "exact_declarations", "closed_obligation_ids", "proof_body", "result",
    }
    if not required_receipt_fields <= set(receipt):
        fail("proof receipt omits contract-required fields")
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        fail("proof receipt schema drifted")
    if (receipt["item_id"], receipt["theorem_id"], receipt["phase"], receipt["intent"]) != (
        ITEM, THEOREM, "proof", "prove"
    ):
        fail("proof receipt identity drifted")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        fail("proof receipt base binding drifted")
    if receipt["support_state"] != "provisional_worker_selftest" or receipt["proposed_state"] != "[_]":
        fail("proof receipt does not preserve worker-only state semantics")
    if receipt["accepted"] is not False or receipt["verdict"] != "blocked":
        fail("proof receipt overstates acceptance")
    if receipt["selftest_status"] != "passed" or receipt["selftest_result"]["exit_code"] != 0:
        fail("proof receipt self-test is not passing")
    if not receipt["selftest_result"]["commands"]:
        fail("proof receipt has no exact self-test commands")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        fail("proof receipt crosses a terminal boundary")
    if receipt["closed_obligation_ids"] != []:
        fail("negative proof evidence cannot close positive obligations")
    if receipt["exact_declarations"] != [
        "Stage1Instances.THMM0112.Proof.not_weakTopologicalLefschetzTarget"
    ]:
        fail("proof receipt declaration inventory drifted")
    if receipt["proof_body"]["source_sha256"] != EXPECTED_INPUT_HASHES["Proof.lean"]:
        fail("proof receipt source hash drifted")
    validator_binding = receipt["inputs"]["validator_candidate"]
    if validator_binding != {
        "path": HEAD_TRACKING_BOUNDARY,
        "sha256": sha256(HERE / "check_proof.py"),
        "git_blob": git_text(
            "hash-object", "--no-filters",
            "Stage1_Instances/THM-M-0112/check_proof.py",
        ),
        "existed_at_base": False,
        "current_claim_selection_eligible": False,
    }:
        fail("proof receipt validator binding drifted")
    ledger_binding = receipt["inputs"]["dependency_reuse_ledger"]
    if ledger_binding != {
        "path": "Stage1_Instances/THM-M-0112/dependency-reuse-ledger.json",
        "sha256": sha256(HERE / "dependency-reuse-ledger.json"),
        "git_blob": git_text(
            "hash-object", "--no-filters",
            "Stage1_Instances/THM-M-0112/dependency-reuse-ledger.json",
        ),
    }:
        fail("proof receipt dependency ledger binding drifted")
    if receipt["result"] != {
        "exit_code": 0,
        "semantic_verdict": "blocked",
        "phase_predicate_proven": False,
        "phase_accepted": False,
        "blocked": True,
        "audit_complete": False,
        "theorem_complete": False,
        "open_obligations": 10,
        "stale_inputs": [],
        "statement_olean_sha256": STATEMENT_OLEAN_SHA256,
        "proof_olean_sha256": PROOF_OLEAN_SHA256,
        "machine_derived_axioms": ["propext", "Classical.choice", "Quot.sound"],
    }:
        fail("proof receipt result drifted")

    semantic = {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "proof",
        "status": "blocked",
        "verdict": "blocked",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": "P04-KERNEL/EXACT-TARGET-CONSISTENCY",
        "open_obligations": 10,
        "stale_inputs": [],
        "blocked": True,
        "message": (
            "The exact frozen proposition is refuted at universes (0,0); positive "
            "proof work must wait for an accepted statement repair."
        ),
    }
    print(json.dumps(semantic, ensure_ascii=True, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
