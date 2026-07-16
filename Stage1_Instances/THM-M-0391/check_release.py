#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0391-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0391"
ITEM = "S56-M-0391-RELEASE"
THEOREM = "THM-M-0391"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
VALIDATION_RECEIPT_SHA256 = (
    "5a391531af68aaf19870f20b832d9b2b2b70e6b6d2bfabcf09ece66be6fa8478"
)
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
EXPECTED_HASHES = {
    "dependency-reuse-ledger.json": (
        "00587a8522545cd651c2d923b0f4f38a0c35fec539c122686a343fa8b979fcba"
    ),
    "release-spec.json": (
        "42442c1580506cdb71802376a2df13e8ddcf57c5851f1315326c1c21985f55a3"
    ),
    "release-decision.json": (
        "a21a6506c5a3f222cf26d654484b726072e5f8e587aac22e3cadd6303b42e4f6"
    ),
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "proof-receipt.json": (
        "775bb98978e9d1da3f42fd2a8c4035a269c30db672f790ff952cc7b842ba0c14"
    ),
    "instance.json": (
        "3a355ea908bfc03ddd17ebbe2300da80b44e9b17105c59d35c6c242bd156ece6"
    ),
    "obligation-registry.json": (
        "c340453b27db47a49d59c81af6cfa88037cd3b8a4572f3fdf7df47425db7af1f"
    ),
    "obligation-nodes.json": (
        "d095791454971080adcfe310d267c6516b351ad8ad269d7f99364692033b305d"
    ),
    "typed-graphs.json": (
        "3f7ae2e9cf98aa7ee05ccd0c8cadcc0f2b9c3aec9eb1ea64500f6bd5252d0b17"
    ),
    "Statement.lean": (
        "a8665695641932dcea97bab10143a73155e45c685fff03cfec6a19689b3f936f"
    ),
    "Proof.lean": (
        "17723aea0ba702c2598c498797fef79b4c8056b65edb1ce952d53914cf8089b1"
    ),
    "Validation.lean": (
        "6455ddd26531415d28e71af89872802444ce331ab3fd1027be8d6ff0330fbaab"
    ),
    "README.md": (
        "3cecf3b3aed8050b9aa4a162f029e5918360a55ebff960d406a32a3b3ad760ae"
    ),
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Phase_Acceptance_Contracts.json": (
        "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
    ),
    "Docs/Stage1_Blueprint_v2.md": (
        "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1"
    ),
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8"
    ),
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "80b2ad4e2943128eeff5b4b2446dc0057a978de003d9c90140567d2f32aca5af"
    ),
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Blueprint_Guidelines.md": (
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454"
    ),
    "Formalizations/Lean/lean-toolchain": (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    ),
    "Formalizations/Lean/lake-manifest.json": (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    ),
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)


def fail(message: str) -> NoReturn:
    print(f"THM-M-0391 release validator: {message}", file=sys.stderr)
    raise SystemExit(1)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            value[key] = child
        return value

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def git(*argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=ROOT, capture_output=True, text=True, timeout=20
    )
    if result.returncode:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def require_binding(container: dict[str, Any], key: str, name: str) -> None:
    binding = container.get(key)
    expected_path = f"Stage1_Instances/THM-M-0391/{name}"
    if not isinstance(binding, dict) or binding.get("path") != expected_path:
        fail(f"receipt role {key} has the wrong target-owned path")
    if binding.get("sha256") != digest(HERE / name):
        fail(f"receipt role {key} has a stale SHA-256 binding")
    if binding.get("git_blob") != git("hash-object", str(HERE / name)):
        fail(f"receipt role {key} has a stale Git-blob binding")


def main() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", f"{BASE_REVISION}^{{tree}}") != BASE_TREE:
        fail("claimed worker base tree does not match its revision")

    for name, expected in EXPECTED_HASHES.items():
        actual = digest(HERE / name)
        if actual != expected:
            fail(f"stale target input {name}: expected {expected}, got {actual}")
    for relative, expected in EXPECTED_AUTHORITY_HASHES.items():
        actual = digest(ROOT / relative)
        if actual != expected:
            fail(f"stale authority input {relative}: expected {expected}, got {actual}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(
        (row for row in targets["targets"] if row.get("theorem_id") == THEOREM),
        None,
    )
    if target is None or target.get("execution_rank") != 5:
        fail("target manifest membership or execution rank disagrees")
    if target.get("lifecycle_mode") != "planned" or target.get("theorem_complete") is not False:
        fail("target manifest no longer supports the open release boundary")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    phase_items = {
        row["phase"]: row
        for row in execution["items"]
        if row.get("theorem_id") == THEOREM
    }
    if set(phase_items) != {
        "intake", "statement", "anchor_audit", "obligation_tree", "proof",
        "validation", "release",
    }:
        fail("execution DAG does not contain the exact seven target phases")
    if any(row.get("state") != "[_]" for row in phase_items.values()):
        fail("authoritative phase state changed from the inspected [_] closure")
    if phase_items["release"].get("layer") != 6 or phase_items["release"].get("id") != ITEM:
        fail("release phase claim order metadata disagrees")
    if phase_items["release"].get("depends_on") != ["S56-M-0391-VALIDATION"]:
        fail("release prerequisite disagrees")

    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    theorem_node = next(
        row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM
    )
    if theorem_node.get("v2_execution_rank") != 5:
        fail("v2 execution rank changed")
    if theorem_node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if theorem_node.get(field) != []:
            fail(f"theorem context field {field} is no longer empty")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger != {
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
    }:
        fail("dependency-reuse ledger is not the exact audited empty closure")

    instance = load(HERE / "instance.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    registry = load(HERE / "obligation-registry.json")
    nodes = load(HERE / "obligation-nodes.json")
    graphs = load(HERE / "typed-graphs.json")
    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")

    if instance.get("lifecycle") != "planned" or instance.get("root_vector") != ROOT_VECTOR:
        fail("instance lifecycle or root vector changed")
    if instance.get("audit_complete") is not False or instance.get("theorem_complete") is not False:
        fail("instance overstates a terminal decision")
    obligations = registry.get("obligations")
    node_rows = nodes.get("nodes")
    if not isinstance(obligations, list) or not isinstance(node_rows, list):
        fail("obligation artifacts are malformed")
    obligation_ids = {row.get("obligation_id") for row in obligations}
    node_ids = {row.get("obligation_id") for row in node_rows}
    if len(obligation_ids) != 15 or obligation_ids != node_ids:
        fail("frozen obligation denominator or node identity disagrees")
    if registry.get("root_obligation_id") != "M0391-ROOT":
        fail("root obligation identity changed")
    proof_edges = graphs.get("graphs", {}).get("proof")
    if not isinstance(proof_edges, list) or len(proof_edges) != 14:
        fail("typed proof graph changed")

    if proof.get("closed_obligation_ids") != ["M0391-B-EE"]:
        fail("proof receipt closure boundary changed")
    if proof.get("result", {}).get("root_closed") is not False:
        fail("proof receipt falsely closes the root")
    if validation.get("item_id") != "S56-M-0391-VALIDATION":
        fail("validation receipt identity changed")
    if validation.get("support_state") != "provisional_worker_selftest":
        fail("validation support state changed")
    if validation.get("result", {}).get("validated_closed_obligation_ids") != ["M0391-B-EE"]:
        fail("validation receipt closure boundary changed")
    if validation.get("result", {}).get("root_closed") is not False:
        fail("validation receipt falsely closes the root")
    if validation.get("selftest_status") is not None or validation.get("accepted") is not None:
        fail("legacy validation evidence unexpectedly acquired current acceptance fields")

    if spec.get("schema_version") != "stage1-release-recipe/1.0":
        fail("release specification schema changed")
    if spec.get("item_id") != ITEM or spec.get("theorem_id") != THEOREM:
        fail("release specification identity changed")
    expected_argv = [
        "/usr/bin/python3", "-I", "-B",
        "Stage1_Instances/THM-M-0391/check_release.py",
    ]
    if spec.get("argv") != expected_argv or spec.get("cwd") != ".":
        fail("release specification recipe changed")
    if spec.get("network_policy") != "denied" or spec.get("expected_exit") != 0:
        fail("release specification execution boundary changed")
    protocol = spec.get("release_protocol_recipes")
    if not isinstance(protocol, dict) or set(protocol) != {
        "immutable_clean_cold_offline", "supply_chain_sbom_licenses",
        "deterministic_bundle", "independent_verification",
    }:
        fail("release specification omits a required release protocol lane")
    if any(
        not isinstance(row, dict)
        or row.get("required") is not True
        or row.get("available") is not False
        or row.get("argv") is not None
        or row.get("evidence_credit") is not False
        or not str(row.get("status", "")).startswith("blocked_missing_")
        for row in protocol.values()
    ):
        fail("release specification falsely supplies an unavailable protocol recipe")

    if decision.get("schema_version") != "stage1-release-decision/1.0":
        fail("release decision schema changed")
    if decision.get("item_id") != ITEM or decision.get("theorem_id") != THEOREM:
        fail("release decision identity changed")
    if decision.get("base_revision") != BASE_REVISION or decision.get("base_tree") != BASE_TREE:
        fail("release decision base changed")
    if decision.get("claim_order") != {
        "v2_execution_rank": 5,
        "phase_layer": 6,
        "phase_item_id": ITEM,
    }:
        fail("release decision claim order changed")
    if decision.get("verdict") != "blocked" or decision.get("accepted") is not False:
        fail("release decision no longer preserves the blocked boundary")
    if decision.get("release_grade") is not False or decision.get("release_accepted") is not False:
        fail("release decision falsely claims release evidence")
    if decision.get("lifecycle_before") != "planned" or decision.get("lifecycle_after") != "planned":
        fail("release decision promotes lifecycle")
    if decision.get("root_vector", {}).get("before") != ROOT_VECTOR:
        fail("release decision input root vector changed")
    if decision.get("root_vector", {}).get("after") != ROOT_VECTOR:
        fail("release decision promotes root debt")
    terminals = decision.get("terminal_decisions", {})
    if terminals.get("audit_complete") is not False or terminals.get("theorem_complete") is not False:
        fail("release decision falsely closes AUDIT-Z or THEOREM-Z")
    if decision.get("accepted_receipt_ids") != []:
        fail("release decision invents accepted receipts")
    if decision.get("deterministic_bundle_sha256") is not None:
        fail("release decision invents a deterministic bundle")
    if decision.get("independent_attestations") != []:
        fail("release decision invents independent attestations")
    if decision.get("dependency", {}).get("receipt_sha256") != VALIDATION_RECEIPT_SHA256:
        fail("release dependency does not bind validation bytes")
    if decision.get("dependency", {}).get("master_accepted") is not False:
        fail("release dependency falsely transfers acceptance")
    if decision.get("evidence_reconciliation", {}).get("open_root_relevant_obligation_count") != 14:
        fail("release decision open-obligation count changed")
    if decision.get("remaining_root_cut_set") is None or len(decision["remaining_root_cut_set"]) != 10:
        fail("release decision does not preserve the complete remaining cut set")

    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        fail("release receipt schema changed")
    if receipt.get("receipt_id") != decision.get("decision_id"):
        fail("release receipt and decision identities disagree")
    if receipt.get("item_id") != ITEM or receipt.get("theorem_id") != THEOREM:
        fail("release receipt has the wrong node identity")
    if receipt.get("phase") != "release" or receipt.get("intent") != "release":
        fail("release receipt has the wrong phase or intent")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        fail("release receipt has a stale worker base")
    if receipt.get("verdict") != "blocked" or receipt.get("accepted") is not False:
        fail("release receipt falsely changes the blocked verdict")
    if receipt.get("selftest_status") != "passed":
        fail("release receipt lacks a passed negative self-test")
    selftest = receipt.get("selftest_result")
    if not isinstance(selftest, dict) or selftest.get("exit_code") != 0 or not selftest.get("commands"):
        fail("release receipt lacks exact self-test command evidence")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("release receipt falsely closes a terminal decision")
    if receipt.get("result", {}).get("semantic_verdict") != "blocked":
        fail("release receipt does not preserve the semantic blocker")
    if receipt.get("result", {}).get("phase_accepted") is not False:
        fail("release receipt falsely claims phase acceptance")
    inputs = receipt.get("inputs")
    if not isinstance(inputs, dict):
        fail("release receipt lacks artifact bindings")
    require_binding(inputs, "release_specification", "release-spec.json")
    require_binding(inputs, "release_decision", "release-decision.json")
    require_binding(inputs, "validation_receipt", "validation-receipt.json")
    require_binding(inputs, "dependency_reuse_ledger", "dependency-reuse-ledger.json")
    for key in ("deterministic_evidence_bundle", "independent_attestations"):
        rows = inputs.get(key)
        rows = rows if isinstance(rows, list) else [rows]
        if not rows or any(
            not isinstance(row, dict)
            or row.get("availability") != "missing"
            or row.get("evidence_credit") is not False
            or row.get("sha256") != "0" * 64
            or row.get("git_blob") is not None
            for row in rows
        ):
            fail(f"release receipt falsely supplies missing role {key}")

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
        "first_failed_gate": "dependency.S56-M-0391-VALIDATION.master_acceptance",
        "open_obligations": 14,
        "stale_inputs": ["Stage1_Instances/THM-M-0391/validation-receipt.json"],
        "blocked": True,
        "message": (
            "Negative release reconciliation self-tested; validation is not master "
            "accepted, AUDIT-Z is open, and the exact theorem root remains open."
        ),
    }
    if spec.get("expected_semantic_result") != semantic:
        fail("release specification and computed semantic result disagree")
    print(json.dumps(semantic, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
