#!/usr/bin/env python3
"""Read-only semantic validator for S56-M-0393-RELEASE.

The scheduler supplies Git/base bindings outside this process.  This checker is
therefore intentionally filesystem-only so it can run in the authority replay
sandbox, where the checkout is read-only and repository metadata is absent.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0393"
ITEM = "S56-M-0393-RELEASE"
THEOREM = "THM-M-0393"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
ROOT_VECTOR = {"H": "H3", "M": "M4", "R": "R3"}
EXPECTED_STABLE_HASHES = {
    "Statement.lean": "456c62756bc035e675135270bf6984c00bb1203bc6687d3495ae7663131d985f",
    "Proof.lean": "a77c1d1e431a36db1bd8ae48f2511150a2519e3a88a319e84256c88229c3f29f",
    "Validation.lean": "0086ee0ab6d416a49f51f476fbacb5d1f318bb2ce49e82b6b13a3c73c138696e",
    "obligation-registry.json": "57bd847a36b0883078dece89081bff185fae7b74cabf814c01daa7f7e184aa66",
    "typed-graphs.json": "3b6e634f6134346598fee300291daafa13b3d91aa2afc59dad0a66741595ae6c",
    "proof-receipt.json": "b74728f6a34837f467e2bf9beaad0aaeef7894c56c84ac3264ac3209b7372234",
    "validation-receipt.json": "e799386f8a5c361d7d2cd1fc310afd6d5b6de0b23ee19976e8bd828586e3921c",
}
OID_RE = re.compile(r"^[0-9a-f]{40,64}$")
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)


def fail(message: str) -> NoReturn:
    print(f"THM-M-0393 release validator: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            require(key not in value, f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            value[key] = child
        return value

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    require(isinstance(value, dict), f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(value: Any, expected_path: str, label: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label} is not an artifact binding")
    require(value.get("path") == expected_path, f"{label} path changed")
    path = ROOT / expected_path
    require(path.is_file() and not path.is_symlink(), f"{label} path is missing or unsafe")
    require(value.get("sha256") == sha256(path), f"{label} SHA-256 is stale")
    require(bool(OID_RE.fullmatch(str(value.get("git_blob", "")))), f"{label} Git blob is malformed")
    return value


def configured_binding(
    value: Any,
    expected_path: str,
    label: str,
    *,
    evidence_available: bool,
    artifact_kind: str | None = None,
) -> dict[str, Any]:
    bound = binding(value, expected_path, label)
    artifact = load(ROOT / expected_path)
    require(artifact.get("evidence_available") is evidence_available, f"{label} availability changed")
    if artifact_kind is not None:
        require(bound.get("artifact_kind") == artifact_kind, f"{label} kind changed")
    return bound


def receipt_declares_successful_command(receipt: dict[str, Any], expected: str) -> bool:
    commands = receipt.get("selftest_result", {}).get("commands", [])
    for command in commands:
        if command == expected:
            return True
        if (
            isinstance(command, dict)
            and command.get("exit_code") == 0
            and " ".join(str(part) for part in command.get("argv", [])) == expected
        ):
            return True
    return False


def checklist_row(text: str, item_id: str) -> tuple[str, int]:
    pattern = re.compile(
        rf"^- (?P<state>\[[_x ]\]) `{re.escape(item_id)}` / `{THEOREM}` / "
        rf"`[^`]+`:.*?\{{attempts=(?P<attempts>[0-9]+)\}}$",
        re.MULTILINE,
    )
    rows = list(pattern.finditer(text))
    require(len(rows) == 1, f"blueprint row for {item_id} is missing or ambiguous")
    return rows[0].group("state"), int(rows[0].group("attempts"))


def main() -> None:
    require(sys.flags.optimize == 0, "Python optimization disables required checks")

    for name, expected in EXPECTED_STABLE_HASHES.items():
        require(sha256(HERE / name) == expected, f"stable release input drifted: {name}")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    release_state, release_attempts = checklist_row(blueprint, ITEM)
    validation_state, validation_attempts = checklist_row(
        blueprint, "S56-M-0393-VALIDATION"
    )
    require(release_state == "[_]" and release_attempts >= 2, "release is not the claimed [_] revalidation item")
    require(validation_state == "[_]" and validation_attempts >= 1, "validation predecessor state changed")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next((row for row in targets.get("targets", []) if row.get("theorem_id") == THEOREM), None)
    require(isinstance(target, dict) and target.get("execution_rank") == 6, "target membership or execution rank changed")
    require(target.get("baseline") == "L0" and target.get("rework_required") is True, "uniform L0 baseline changed")
    require(target.get("legacy_artifacts_accepted") is False, "legacy artifacts acquired proof credit")
    require(target.get("lifecycle_mode") == "planned" and target.get("theorem_complete") is False, "target manifest overstates completion")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    phase_items = {
        row.get("phase"): row
        for row in execution.get("items", [])
        if row.get("theorem_id") == THEOREM
    }
    require(set(phase_items) == {"intake", "statement", "anchor_audit", "obligation_tree", "proof", "validation", "release"}, "execution DAG lacks the exact seven phases")
    release_item = phase_items["release"]
    predecessor = phase_items["validation"]
    require(release_item.get("id") == ITEM and release_item.get("layer") == 6, "release claim-order identity changed")
    require(release_item.get("state") == release_state and release_item.get("attempts") == release_attempts, "release projection disagrees with blueprint")
    require(release_item.get("depends_on") == ["S56-M-0393-VALIDATION"], "release predecessor changed")
    require(predecessor.get("state") == validation_state and predecessor.get("attempts") == validation_attempts, "validation projection disagrees with blueprint")

    theorem_dag_path = ROOT / "Docs/Stage1_Theorem_DAG_v2.json"
    graph_sha256 = sha256(theorem_dag_path)
    theorem_dag = load(theorem_dag_path)
    node = next((row for row in theorem_dag.get("theorems", []) if row.get("theorem_id") == THEOREM), None)
    require(isinstance(node, dict) and node.get("v2_execution_rank") == 6, "v2 rank changed")
    require(node.get("dependency_context_sha256") == CONTEXT_SHA256, "dependency context changed")
    require(node.get("phase_states", {}).get("release") == release_state, "theorem DAG release state is stale")
    require(node.get("phase_attempts", {}).get("release") == release_attempts, "theorem DAG release attempts are stale")
    for field in ("direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids", "shared_lemma_group_ids"):
        require(node.get(field) == [], f"declared empty dependency field changed: {field}")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    require(ledger.get("schema_version") == "stage1-dependency-reuse-ledger/1.1", "reuse ledger schema changed")
    require(ledger.get("consumer_theorem_id") == THEOREM, "reuse ledger owner changed")
    require(ledger.get("observed_theorem_dag_sha256") == graph_sha256, "reuse ledger graph digest is stale")
    require(ledger.get("dependency_context_sha256") == CONTEXT_SHA256, "reuse ledger context is stale")
    for field in ("direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions", "unresolved_compatibility_obligations"):
        require(ledger.get(field) == [], f"empty reuse closure changed: {field}")
    closure = ledger.get("closure_audit", {})
    require(closure.get("inspection_order") == [] and closure.get("status") == "empty_closure_inspected", "empty parent closure was not fully audited")

    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    obligations = registry.get("obligations")
    require(isinstance(obligations, list) and len(obligations) == 17, "frozen obligation denominator changed")
    require({row.get("id") for row in obligations} == {"M0393-ROOT", "M0393-S1", "M0393-S2", "M0393-S3", "M0393-N1", "M0393-N2", "M0393-C1", "M0393-C2", "M0393-L1", "M0393-L2", "M0393-L3", "M0393-X1", "M0393-B1", "M0393-B2", "M0393-T1", "M0393-T2", "M0393-X2"}, "canonical obligation IDs changed")
    require(registry.get("root_vector") == {"human": "H3", "machine": "M4", "readability": "R3"}, "registry root vector changed")
    require(registry.get("theorem_complete") is False and all(row.get("body") is None for row in obligations), "registry falsely closes an obligation")
    require(graphs.get("proof_graph", {}).get("root") == "M0393-ROOT", "proof root changed")
    require(all(row.get("state") == "planned_open" for row in graphs.get("proof_graph", {}).get("composition_certificates", [])), "composition state changed")
    require(graphs.get("evidence_graph", {}).get("evidence_nodes") == [], "accepted evidence was invented")
    require(proof.get("result", {}).get("root_closed") is False, "proof receipt falsely closes root")
    require(validation.get("item_id") == "S56-M-0393-VALIDATION", "validation receipt identity changed")
    require(validation.get("support_state") == "provisional_worker_selftest", "validation receipt support state changed")
    require(validation.get("result", {}).get("validated_closed_obligation_ids") == [], "validation receipt invents closed obligations")
    require(validation.get("result", {}).get("validated_partial_obligation_ids") == ["M0393-N1"], "partial validation boundary changed")
    require(validation.get("result", {}).get("root_closed") is False, "validation receipt falsely closes root")

    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        source = (HERE / name).read_text(encoding="utf-8")
        require(PROHIBITED.search(source) is None, f"prohibited proof/trust construct found in {name}")
    require("theorem finite_pow_divisors" in (HERE / "Proof.lean").read_text(encoding="utf-8"), "partial proof declaration is missing")
    require("theorem independent_finite_pow_divisors" in (HERE / "Validation.lean").read_text(encoding="utf-8"), "independent probe declaration is missing")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    base_revision = receipt.get("base_revision")
    base_tree = receipt.get("base_tree")
    require(bool(OID_RE.fullmatch(str(base_revision))) and bool(OID_RE.fullmatch(str(base_tree))), "receipt base identity is malformed")
    require(ledger.get("repository_revision") == base_revision, "reuse ledger and receipt use different bases")
    require(decision.get("base_revision") == base_revision and decision.get("base_tree") == base_tree, "decision and receipt use different bases")
    require(decision.get("claim_order") == {"v2_execution_rank": 6, "phase_layer": 6, "phase_item_id": ITEM}, "exact DAG claim order is missing")
    require(decision.get("verdict") == "blocked" and decision.get("accepted") is False, "decision does not preserve the blocked boundary")
    require(decision.get("lifecycle_before") == decision.get("lifecycle_after") == "planned", "decision promotes lifecycle")
    require(decision.get("dependency_context", {}).get("graph_sha256") == graph_sha256, "decision graph binding is stale")
    require(decision.get("dependency_context", {}).get("ledger_sha256") == sha256(HERE / "dependency-reuse-ledger.json"), "decision ledger binding is stale")
    require(decision.get("dependency", {}).get("master_accepted") is False, "decision transfers predecessor acceptance")
    require(decision.get("dependency", {}).get("receipt_sha256") == EXPECTED_STABLE_HASHES["validation-receipt.json"], "decision validation binding is stale")
    require(decision.get("terminal_decisions") == {"audit_complete": False, "theorem_complete": False, "audit_z": "blocked", "theorem_z": "blocked"}, "terminal decision changed")
    require(decision.get("first_failed_gate", {}).get("gate_id") == "G02-TOPOLOGY", "first failed gate is not topology")
    require(decision.get("evidence_reconciliation", {}).get("open_root_relevant_obligation_count") == 17, "open-obligation count changed")
    require(decision.get("evidence_reconciliation", {}).get("closed_obligation_ids") == [], "decision invents closed obligations")
    require(decision.get("evidence_reconciliation", {}).get("partial_obligation_ids") == ["M0393-N1"], "decision partial boundary changed")
    require(len(decision.get("remaining_root_cut_set", [])) == 14, "remaining root cut set is incomplete")
    require(all(value is False for key, value in decision.get("release_protocol", {}).items() if key not in {"specification_path", "specification_sha256", "status"}), "decision invents release protocol evidence")

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
        "stale_inputs": ["Stage1_Instances/THM-M-0393/validation-receipt.json"],
        "blocked": True,
        "message": "Validation is not master accepted; AUDIT-Z and THEOREM-Z are false, the exact root is open, and required release evidence is absent.",
    }
    require(spec.get("schema_version") == "stage1-validation-spec/1.0", "release specification schema changed")
    require(spec.get("item_id") == ITEM and spec.get("phase") == "release", "release specification identity changed")
    require(spec.get("argv") == ["/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"], "release specification argv changed")
    require(spec.get("network_policy") == "denied" and spec.get("expected_exit") == 0, "release specification weakens replay")
    require(spec.get("expected_semantic_result") == semantic, "release specification semantic result is stale")

    required_receipt_fields = {"schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent", "base_revision", "base_tree", "inputs", "support_state", "proposed_state", "accepted", "verdict", "selftest_status", "selftest_result", "known_failures", "first_failed_gate", "retry_condition", "status_boundary", "audit_complete", "theorem_complete", "invalidation_inputs", "release_grade", "accepted_receipt_ids", "remaining_root_cut_set", "root_vector_after", "deterministic_bundle_sha256", "independent_attestations", "result"}
    require(required_receipt_fields <= set(receipt), "phase receipt lacks contract-required fields")
    require(receipt.get("schema_version") == "stage1-node-receipt/1.0", "phase receipt schema changed")
    require(receipt.get("item_id") == ITEM and receipt.get("theorem_id") == THEOREM, "phase receipt identity changed")
    require(receipt.get("phase") == receipt.get("intent") == "release", "phase receipt intent changed")
    require(receipt.get("support_state") == "provisional_worker_selftest" and receipt.get("proposed_state") == "[_]", "phase receipt support state changed")
    require(receipt.get("accepted") is False and receipt.get("verdict") == "blocked", "phase receipt transfers acceptance")
    require(receipt.get("selftest_status") == "passed" and receipt.get("selftest_result", {}).get("exit_code") == 0, "phase receipt lacks successful self-test")
    require(isinstance(receipt.get("selftest_result", {}).get("commands"), list) and bool(receipt["selftest_result"]["commands"]), "phase receipt lacks exact commands")
    require(receipt_declares_successful_command(receipt, "/usr/bin/python3 -I -B Stage1_Instances/THM-M-0393/check_release.py"), "phase receipt omits its successful validator command")
    require(receipt.get("audit_complete") is False and receipt.get("theorem_complete") is False, "phase receipt closes a terminal decision")
    require(receipt.get("release_grade") is False and receipt.get("accepted_receipt_ids") == [], "phase receipt invents release evidence")
    require(receipt.get("deterministic_bundle_sha256") is None and receipt.get("independent_attestations") == [], "phase receipt invents bundle or attestations")
    require(receipt.get("remaining_root_cut_set") == decision.get("remaining_root_cut_set"), "receipt cut set disagrees with decision")
    require(receipt.get("root_vector_after") == ROOT_VECTOR, "receipt promotes root debt")
    require(receipt.get("result", {}).get("semantic_verdict") == "blocked" and receipt.get("result", {}).get("phase_predicate_proven") is False, "receipt result disagrees with blocked semantics")
    require(receipt.get("result", {}).get("stale_inputs") == semantic["stale_inputs"], "receipt stale-input set changed")

    inputs = receipt.get("inputs", {})
    binding(inputs.get("release_specification"), f"Stage1_Instances/{THEOREM}/release-spec.json", "release specification")
    binding(inputs.get("release_decision"), f"Stage1_Instances/{THEOREM}/release-decision.json", "release decision")
    binding(inputs.get("validation_receipt"), f"Stage1_Instances/{THEOREM}/validation-receipt.json", "validation receipt")
    binding(inputs.get("dependency_reuse_ledger"), f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json", "dependency reuse ledger")
    binding(inputs.get("obligation_registry"), f"Stage1_Instances/{THEOREM}/obligation-registry.json", "obligation registry")
    binding(inputs.get("typed_graphs"), f"Stage1_Instances/{THEOREM}/typed-graphs.json", "typed graphs")
    binding(inputs.get("release_validator"), f"Stage1_Instances/{THEOREM}/check_release.py", "release validator")
    configured_binding(inputs.get("deterministic_evidence_bundle"), f"Stage1_Instances/{THEOREM}/deterministic-evidence-bundle.json", "missing deterministic bundle", evidence_available=False, artifact_kind="required_release_bundle_missing")
    attestations = inputs.get("independent_attestations")
    require(isinstance(attestations, list) and len(attestations) == 2, "missing attestation inventory changed")
    for index, row in enumerate(attestations, 1):
        configured_binding(row, f"Stage1_Instances/{THEOREM}/independent-attestation-{index}.json", f"missing independent attestation {index}", evidence_available=False, artifact_kind="required_independent_attestation_missing")
    projections = inputs.get("public_projections")
    require(isinstance(projections, list) and len(projections) == 1, "public projection binding changed")
    binding(projections[0], f"Stage1_Instances/{THEOREM}/release-validation.md", "public negative projection")

    print(json.dumps(semantic, ensure_ascii=True, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
