#!/usr/bin/env python3
"""Fail closed over the THM-M-0395 negative release reconciliation."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances/THM-M-0395"
ITEM = "S56-M-0395-RELEASE"
THEOREM = "THM-M-0395"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
VALIDATION_RECEIPT_SHA256 = "b5300fb5d7061a63859580b6ec108392dc6b68e92a7739d898869734a3da987f"
PROOF_RECEIPT_SHA256 = "942ac39e8e2cec5c84a561f0f3a0a0035a754ec2106287f1fa4287f26921e51a"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R3"}
EXPECTED_PHASE_STATES = {
    "intake": "[_]",
    "statement": "[_]",
    "anchor_audit": "[_]",
    "obligation_tree": "[_]",
    "proof": "[_]",
    "validation": "[_]",
    "release": "[_]",
}
EXPECTED_LEGACY_HASHES = {
    "Statement.lean": "de1bfb399ccec48a224e867c55f6eab12589e458949d6d409260be65f0920ba6",
    "Proof.lean": "1c0139a56ce605ecf2ff09231f91a78ca777a0733711a480adc429400517d643",
    "Validation.lean": "fe80b39bfa6648b4039a2db58ac696661b3153f8f4ea043728c34098f090c1d1",
    "obligation-registry.json": "2461eef24bec0c53faf36b2a16f1cb7c61fb13341544fad2cc64113be64381be",
    "typed-graphs.json": "c130159ff5c46af19263bae478720e4fe33ec8007f8d6bb15c6e444096bb1e81",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
}
EXPECTED_CURRENT_RUNNER_HASHES = {
    "check_proof.sh": "ca97bd0d570ee91561651f1750325bd6c5c07eef8f1bf43417ea94faaa53dcaa",
    "check_validation_lean.sh": "35acd4262f80bbfeef4be2db757f155f7054b449d1df1a7ffa8d16f5eb3c37c6",
}
REQUIRED_RECEIPT_FIELDS = {
    "schema_version",
    "receipt_id",
    "item_id",
    "theorem_id",
    "phase",
    "intent",
    "base_revision",
    "base_tree",
    "inputs",
    "support_state",
    "proposed_state",
    "accepted",
    "verdict",
    "selftest_status",
    "selftest_result",
    "known_failures",
    "first_failed_gate",
    "retry_condition",
    "status_boundary",
    "audit_complete",
    "theorem_complete",
    "invalidation_inputs",
    "release_grade",
    "accepted_receipt_ids",
    "remaining_root_cut_set",
    "root_vector_after",
    "deterministic_bundle_sha256",
    "independent_attestations",
    "result",
}
REQUIRED_INPUT_ROLES = {
    "release_specification",
    "release_decision",
    "validation_receipt",
    "deterministic_evidence_bundle",
    "independent_attestations",
    "public_projections",
}
PROHIBITED = re.compile(
    r"\b(sorry|admit)\b|^[ \t]*(axiom|unsafe)\b",
    re.MULTILINE,
)


def fail(message: str) -> None:
    print(f"release-decision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(relative: str) -> dict[str, Any]:
    path = HERE / relative
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read strict JSON {relative}: {exc}")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_text(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        fail(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def assert_regular_owned(relative: str) -> pathlib.Path:
    path = ROOT / relative
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        fail(f"missing bound artifact {relative}: {exc}")
    if path.is_symlink() or not path.is_file() or HERE.resolve() not in resolved.parents:
        fail(f"artifact is not a regular target-owned file: {relative}")
    return path


def assert_binding(binding: dict[str, Any], role: str) -> None:
    if set(binding) < {"path", "sha256", "git_blob"}:
        fail(f"{role} lacks path/SHA-256/Git-blob binding")
    path = assert_regular_owned(binding["path"])
    if sha256(path) != binding["sha256"]:
        fail(f"{role} SHA-256 binding drifted")
    if git_text("hash-object", binding["path"]) != binding["git_blob"]:
        fail(f"{role} Git-blob binding drifted")


def blueprint_states() -> dict[str, str]:
    text = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    phases = {
        "INTAKE": "intake",
        "STATEMENT": "statement",
        "ANCHOR_AUDIT": "anchor_audit",
        "OBLIGATION_TREE": "obligation_tree",
        "PROOF": "proof",
        "VALIDATION": "validation",
        "RELEASE": "release",
    }
    found: dict[str, str] = {}
    for suffix, phase in phases.items():
        match = re.search(
            rf"^- \[([ x_])\] `S56-M-0395-{suffix}` / `THM-M-0395` / `{phase}`:",
            text,
            re.MULTILINE,
        )
        if match is None:
            fail(f"authoritative blueprint lacks S56-M-0395-{suffix}")
        found[phase] = f"[{match.group(1)}]"
    return found


def main() -> None:
    targets = json.loads(
        (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
    )
    target = next(
        (row for row in targets["targets"] if row["theorem_id"] == THEOREM), None
    )
    if target is None or target["execution_rank"] != 8:
        fail("target membership or original execution rank drifted")
    if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
        fail("target manifest no longer supports the negative release decision")
    if blueprint_states() != EXPECTED_PHASE_STATES:
        fail("authoritative seven-phase state no longer matches the claimed release frontier")

    theorem_dag_path = ROOT / "Docs/Stage1_Theorem_DAG_v2.json"
    if sha256(theorem_dag_path) != GRAPH_SHA256:
        fail("observed theorem-DAG digest drifted")
    theorem_dag = json.loads(theorem_dag_path.read_text(encoding="utf-8"))
    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM)
    if node["v2_execution_rank"] != 8 or node["phase_states"] != EXPECTED_PHASE_STATES:
        fail("theorem-DAG rank or phase projection drifted")
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        fail("theorem dependency-context digest drifted")
    for key in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node[key] != []:
            fail(f"declared empty dependency context changed at {key}")

    for relative, expected in EXPECTED_LEGACY_HASHES.items():
        if sha256(HERE / relative) != expected:
            fail(f"predecessor input drifted: {relative}")
    for relative, expected in EXPECTED_CURRENT_RUNNER_HASHES.items():
        if sha256(HERE / relative) != expected:
            fail(f"repaired target-owned runner drifted: {relative}")

    ledger = load("dependency-reuse-ledger.json")
    if ledger["schema_version"] != "stage1-dependency-reuse-ledger/1.1":
        fail("dependency ledger schema drifted")
    if ledger["consumer_theorem_id"] != THEOREM:
        fail("dependency ledger consumer drifted")
    if ledger["observed_theorem_dag_sha256"] != GRAPH_SHA256:
        fail("dependency ledger graph digest drifted")
    if ledger["dependency_context_sha256"] != CONTEXT_SHA256:
        fail("dependency ledger context digest drifted")
    if ledger["repository_revision"] != BASE_REVISION:
        fail("dependency ledger base revision drifted")
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
        if ledger[key] != []:
            fail(f"dependency ledger falsely populates empty context at {key}")
    if ledger["closure_audit"]["inspection_order"] != []:
        fail("dependency ledger inspection order is not exactly empty")
    if ledger["closure_audit"]["status"] != "empty_closure_inspected":
        fail("dependency ledger does not certify the declared empty closure")

    registry = load("obligation-registry.json")
    graphs = load("typed-graphs.json")
    ids = {row["obligation_id"] for row in registry["obligations"]}
    nodes = {row["obligation_id"]: row for row in graphs["nodes"]}
    if len(ids) != 17 or ids != set(nodes):
        fail("frozen 17-obligation registry and typed graph disagree")
    if registry["root_obligation_id"] != "M0395-ROOT":
        fail("canonical root identity drifted")
    root = nodes["M0395-ROOT"]
    if {
        "H": root["human_debt"],
        "M": root["machine_debt"],
        "R": root["readability_debt"],
    } != ROOT_VECTOR:
        fail("frozen root vector drifted")
    closure = graphs["closure_boundary"]
    if closure["root_closed"] is not False or closure["theorem_complete"] is not False:
        fail("typed graph no longer supports an open root")

    proof = load("proof-receipt.json")
    validation = load("validation-receipt.json")
    if proof["receipt_id"] != "S56-M-0395-PROOF-local-20260711T193336Z":
        fail("proof receipt identity drifted")
    if validation["receipt_id"] != "S56-M-0395-VALIDATION-local-20260712":
        fail("validation receipt identity drifted")
    if proof["support_state"] != validation["support_state"] or proof["support_state"] != "provisional_worker_selftest":
        fail("predecessor receipts are not exactly provisional worker evidence")
    if proof["closed_obligation_ids"] != []:
        fail("proof receipt unexpectedly closes a frozen obligation")
    result = validation["result"]
    if result["validated_closed_obligation_ids"] != []:
        fail("validation receipt unexpectedly closes a frozen obligation")
    if result["root_closed"] is not False or result["theorem_complete"] is not False:
        fail("validation receipt no longer supports an open-root decision")
    if validation["inputs"]["lean_runner_sha256"] == EXPECTED_CURRENT_RUNNER_HASHES["check_validation_lean.sh"]:
        fail("legacy validation receipt unexpectedly claims the repaired runner bytes")

    decision = load("release-decision.json")
    if decision["item_id"] != ITEM or decision["theorem_id"] != THEOREM:
        fail("release decision identity drifted")
    if decision["base_revision"] != BASE_REVISION or decision["base_tree"] != BASE_TREE:
        fail("release decision base binding drifted")
    if decision["claim_order"] != {
        "v2_execution_rank": 8,
        "phase_layer": 6,
        "phase_item_id": ITEM,
    }:
        fail("release decision claim order drifted")
    if decision["verdict"] != "blocked" or decision["accepted"] is not False:
        fail("release decision overstates acceptance")
    if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
        fail("release decision promotes lifecycle")
    if decision["root_vector"]["before"] != ROOT_VECTOR or decision["root_vector"]["after"] != ROOT_VECTOR:
        fail("release decision promotes the root vector")
    if decision["terminal_decisions"] != {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }:
        fail("release decision falsely closes AUDIT-Z or THEOREM-Z")
    if decision["accepted_receipt_ids"] != []:
        fail("release decision invents accepted receipts")
    if decision["deterministic_bundle_sha256"] is not None:
        fail("release decision invents a deterministic release bundle")
    if decision["independent_attestations"] != []:
        fail("release decision invents independent attestations")
    dependency = decision["dependency"]
    if dependency["receipt_sha256"] != VALIDATION_RECEIPT_SHA256:
        fail("release dependency does not bind validation-receipt bytes")
    if dependency["master_accepted"] is not False or dependency["current_for_release_acceptance"] is not False:
        fail("release decision transfers predecessor acceptance")
    if decision["first_failed_gate"]["gate_id"] != "G02-TOPOLOGY":
        fail("release decision does not fail first at topology")
    reconciliation = decision["evidence_reconciliation"]
    if reconciliation["open_root_relevant_obligation_count"] != 17:
        fail("release reconciliation has the wrong open-obligation count")
    if reconciliation["accepted_closed_obligation_ids"] != [] or reconciliation["provisional_closed_obligation_ids"] != []:
        fail("release reconciliation overstates frozen obligation closure")
    if set(decision["release_protocol"].values()) - {
        "Stage1_Instances/THM-M-0395/release-spec.json",
        False,
        "not_release_grade",
    }:
        fail("release protocol invents positive evidence")
    if len(decision["remaining_root_cut_set"]) != 13:
        fail("release decision does not preserve the complete remaining cut set")

    spec = load("release-spec.json")
    if spec["schema_version"] != "stage1-release-recipe/1.0":
        fail("release specification schema drifted")
    if spec["item_id"] != ITEM or spec["phase"] != "release" or spec["intent"] != "release":
        fail("release specification identity drifted")
    if spec["base_revision"] != BASE_REVISION or spec["base_tree"] != BASE_TREE:
        fail("release specification base binding drifted")
    if spec["argv"] != [
        "/usr/bin/python3",
        "-I",
        "-B",
        "Stage1_Instances/THM-M-0395/check_release.py",
    ]:
        fail("release specification does not use the declared validator argv")
    if spec["network_policy"] != "denied" or spec["expected_exit"] != 0:
        fail("release specification is not fail-closed and network denied")
    if set(spec["covered_obligation_ids"]) != ids:
        fail("release specification does not cover the frozen denominator")
    if any(row["status"] != "not_satisfied" for row in spec["release_protocol"].values()):
        fail("release specification falsely satisfies a release protocol gate")

    receipt = load("release-receipt.json")
    if not REQUIRED_RECEIPT_FIELDS <= set(receipt):
        fail(f"release receipt lacks required fields: {sorted(REQUIRED_RECEIPT_FIELDS - set(receipt))}")
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        fail("release receipt schema drifted")
    if receipt["item_id"] != ITEM or receipt["theorem_id"] != THEOREM:
        fail("release receipt identity drifted")
    if receipt["phase"] != "release" or receipt["intent"] != "release":
        fail("release receipt phase or intent drifted")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        fail("release receipt base binding drifted")
    if receipt["support_state"] != "provisional_worker_selftest" or receipt["proposed_state"] != "[_]":
        fail("release receipt has the wrong support/proposed state")
    if receipt["accepted"] is not False or receipt["verdict"] != "blocked":
        fail("release receipt overstates acceptance")
    if receipt["selftest_status"] != "passed" or receipt["selftest_result"]["exit_code"] != 0:
        fail("release receipt does not record a passing worker self-test")
    if not receipt["selftest_result"]["commands"]:
        fail("release receipt lacks exact nonempty self-test commands")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        fail("release receipt falsely closes AUDIT-Z or THEOREM-Z")
    if receipt["release_grade"] is not False or receipt["accepted_receipt_ids"] != []:
        fail("release receipt invents release-grade or accepted evidence")
    if receipt["remaining_root_cut_set"] != decision["remaining_root_cut_set"]:
        fail("release receipt and decision cut sets disagree")
    if receipt["root_vector_after"] != ROOT_VECTOR:
        fail("release receipt promotes the root vector")
    if receipt["deterministic_bundle_sha256"] is not None or receipt["independent_attestations"] != []:
        fail("release receipt invents bundle or attestation evidence")
    if receipt["result"] != {
        "exit_code": 0,
        "semantic_verdict": "blocked",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "open_obligations": 17,
        "first_failed_gate": "G02-TOPOLOGY",
    }:
        fail("release receipt result is not the exact negative semantic decision")
    if not REQUIRED_INPUT_ROLES <= set(receipt["inputs"]):
        fail("release receipt lacks a contract-selected artifact role")
    for role in (
        "release_specification",
        "release_decision",
        "validation_receipt",
        "dependency_reuse_ledger",
        "obligation_registry",
        "typed_graphs",
        "release_validator",
        "proof_runner",
        "validation_runner",
        "deterministic_evidence_bundle",
    ):
        assert_binding(receipt["inputs"][role], role)
    for role in ("independent_attestations", "public_projections"):
        bindings = receipt["inputs"][role]
        if not isinstance(bindings, list) or not bindings:
            fail(f"release receipt role {role} has wrong cardinality")
        for binding in bindings:
            assert_binding(binding, role)
    if receipt["inputs"]["validation_receipt"]["sha256"] != VALIDATION_RECEIPT_SHA256:
        fail("release receipt does not bind the exact validation receipt")
    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        source = (HERE / name).read_text(encoding="utf-8")
        if PROHIBITED.search(source):
            fail(f"prohibited placeholder or trust construct found in {name}")

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
        "stale_inputs": ["Stage1_Instances/THM-M-0395/validation-receipt.json"],
        "blocked": True,
        "message": (
            "Negative release reconciliation self-tested; validation is not master "
            "accepted, AUDIT-Z is open, and the exact Faltings root remains open."
        ),
    }
    if spec["expected_semantic_result"] != semantic:
        fail("release specification and computed semantic result disagree")
    print(json.dumps(semantic, ensure_ascii=True, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
