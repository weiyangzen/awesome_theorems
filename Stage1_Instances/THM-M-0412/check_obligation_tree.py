#!/usr/bin/env python3
"""Fail-closed semantic validator for the THM-M-0412 obligation freeze."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_obligation_artifacts as builder


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0412-OBLIGATION_TREE"
THEOREM = "THM-M-0412"
BASE_REVISION = "a103f2e1e75a1fb43dd82b47c30f80ca7df18b7d"
BASE_TREE = "5988efc9a45479903b8d1aeb8a34b21c0630c97c"
GRAPH_SHA256 = "d5b27da9fcb355d5edf9d63ad5d0c4c3ec3410eba4e8e94303d5cef4895a49b9"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
STATEMENT_SHA256 = "1c4ca90f92ad2d74e7e6abe4124b57e623a8218312ed88f38626ae0b096edd65"
STATEMENT_RECORD_SHA256 = "f1c06c651eb29495e03b0c833941f55ebe61bbacdf08f93b50d045e50ef28cfd"
ANCHOR_SHA256 = "bac3854ea0523b4b7b977e71a2f81924d69a72e353b0cc8fd6f7f9b2e85f919f"
REGISTRY_DENOMINATOR = "1726b8e6f6d48ec652a86fd62675be0ea4d8d3fe2f7ca5fb733adfa45e4e4ab5"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_SELECTED_HASHES = {
    "obligation_registry": "f189224826e60a2f286a535617332fd41f338356b8440fc2273b820b3350908e",
    "typed_graph_bundle": "fe488b63dbbc69f1d1cd45e65f928c2c6d791aab8ee274befbbcae7502d8d726",
    "readable_tree": "0fc12a7611cbf900b383995469fa0b8281c8fb6ce394b510d2fa6af2edafbf8e",
    "composition_source": "a5e6362b44625d22be2eaa13f5e2f3fe52be29f122097f4ec18b2082885b44a9",
}
REQUIRED_NODE_FIELDS = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
REQUIRED_RECEIPT_POINTERS = (
    "/schema_version", "/receipt_id", "/item_id", "/theorem_id", "/phase",
    "/intent", "/base_revision", "/base_tree", "/inputs", "/support_state",
    "/proposed_state", "/accepted", "/verdict", "/selftest_status",
    "/selftest_result/exit_code", "/selftest_result/commands", "/known_failures",
    "/first_failed_gate", "/retry_condition", "/status_boundary", "/audit_complete",
    "/theorem_complete", "/invalidation_inputs", "/registry_denominator_sha256",
    "/canonical_obligation_ids", "/composition_certificates",
)
ALLOWED_EDGE_TYPES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
SEMANTIC_RESULT = {
    "schema_version": "stage1-validator-semantic-result/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "phase": "obligation_tree",
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
        "T01-T04 and worker G01/G08/G09 checks passed: 29 status-independent "
        "identity-dependent obligations, seven reciprocal typed graphs with 122 edges, "
        "an audited empty dependency context, substantive <=100-step ledgers, and a "
        "truthful no-exact-signature composition ineligibility boundary are ready for "
        "independent master review; all mathematical proof and terminal gates remain open."
    ),
}


class GateFailure(Exception):
    def __init__(self, gate: str, message: str, stale: list[str] | None = None):
        super().__init__(message)
        self.gate = gate
        self.message = message
        self.stale = stale or []


def require(condition: bool, gate: str, message: str, stale: list[str] | None = None) -> None:
    if not condition:
        raise GateFailure(gate, message, stale)


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GateFailure("T01-ARTIFACTS", f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateFailure("T01-ARTIFACTS", f"cannot load {path.name}: {exc}") from exc
    require(isinstance(value, dict), "T01-ARTIFACTS", f"{path.name} is not one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    require(result.returncode == 0, "G09-FRESHNESS", result.stderr or "git command failed")
    return result.stdout.strip()


def pointer(document: dict[str, Any], raw: str) -> Any:
    value: Any = document
    for component in raw.removeprefix("/").split("/"):
        require(isinstance(value, dict) and component in value, "T01-ARTIFACTS", f"missing receipt pointer {raw}")
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
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        elif source[index] == '"':
            in_string = True
            index += 1
        else:
            output.append(source[index])
            index += 1
    require(depth == 0 and not in_string, "T04-COMPOSITION", "unterminated Lean comment or string")
    return "".join(output)


def canonical_projection(registry: dict[str, Any]) -> list[dict[str, Any]]:
    fields = registry["canonical_projection_fields"]
    return [{field: row[field] for field in fields} for row in registry["obligations"]]


def calculated_denominator(registry: dict[str, Any]) -> str:
    raw = json.dumps(canonical_projection(registry), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def assert_authorities() -> None:
    expected = {
        ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
        ROOT / "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
        HERE / "Statement.lean": STATEMENT_SHA256,
        HERE / "statement.json": STATEMENT_RECORD_SHA256,
        HERE / "anchor-audit.json": ANCHOR_SHA256,
    }
    stale = [str(path.relative_to(ROOT)) for path, digest in expected.items() if not path.is_file() or sha256(path) != digest]
    require(not stale, "G09-FRESHNESS", "a frozen authority input changed", stale)
    require(git("rev-parse", "HEAD") == BASE_REVISION, "G09-FRESHNESS", "HEAD differs from worker base", ["HEAD"])
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "G09-FRESHNESS", "HEAD tree differs from worker base", ["HEAD^{tree}"])


def assert_contract_and_target() -> None:
    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row["phase"] == "obligation_tree")
    require(phase["layer"] == 3 and phase["item_suffix"] == "OBLIGATION_TREE", "T01-ARTIFACTS", "phase contract identity changed")
    require(tuple(phase["phase_receipt_required_fields"]) == REQUIRED_RECEIPT_POINTERS, "T01-ARTIFACTS", "receipt contract changed")
    roles = {row["role"]: row for row in phase["required_artifact_roles"]}
    require(set(roles) == {"obligation_registry", "typed_graph_bundle", "readable_tree", "composition_source", "phase_receipt"}, "T01-ARTIFACTS", "artifact roles changed")
    expected_names = {
        "obligation_registry": "obligation-registry.json",
        "typed_graph_bundle": "typed-graphs.json",
        "readable_tree": "obligation-tree.md",
        "composition_source": "ObligationTree.lean",
        "phase_receipt": "obligation-tree-receipt.json",
    }
    for role, name in expected_names.items():
        candidates = [Path(path.replace("{theorem_id}", THEOREM)).name for path in roles[role]["path_candidates"]]
        require(candidates == [name] and (HERE / name).is_file() and not (HERE / name).is_symlink(), "T01-ARTIFACTS", f"role {role} is unresolved")
    validators = [Path(row["path_pattern"].replace("{theorem_id}", THEOREM)).name for row in phase["validator_candidates"]]
    require([name for name in validators if (HERE / name).is_file()] == ["check_obligation_tree.py"], "T01-ARTIFACTS", "validator selection is missing or ambiguous")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    row_pattern = re.compile(r"^- \[ \] `S56-M-0412-OBLIGATION_TREE` / `THM-M-0412` / `obligation_tree`.*\{attempts=0\}$", re.MULTILINE)
    require(row_pattern.search(blueprint) is not None, "G01-SSOT-CAS", "assigned phase is not the exact open authority row")
    require("- [_] `S56-M-0412-ANCHOR_AUDIT`" in blueprint, "G02-TOPOLOGY", "predecessor observation changed")

    dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    target = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM)
    require(target["v2_execution_rank"] == 259 and target["phase_states"]["obligation_tree"] == "[ ]", "G08-V2-CONTEXT", "claim order or phase state changed")
    require(target["phase_attempts"]["obligation_tree"] == 0 and target["dependency_context_sha256"] == CONTEXT_SHA256, "G08-V2-CONTEXT", "attempt or context changed")
    for field in ("direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids", "shared_lemma_group_ids"):
        require(target[field] == [], "G08-V2-CONTEXT", f"target {field} is no longer empty")


def assert_dependency_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1", "G08-V2-CONTEXT", "dependency ledger schema mismatch")
    require(ledger["consumer_theorem_id"] == THEOREM and ledger["item_id"] == ITEM, "G08-V2-CONTEXT", "dependency ledger identity mismatch")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256 and ledger["dependency_context_sha256"] == CONTEXT_SHA256, "G08-V2-CONTEXT", "dependency graph or context digest mismatch")
    require(ledger["repository_revision"] == BASE_REVISION, "G08-V2-CONTEXT", "dependency ledger base mismatch")
    require(ledger["claim_order"] == {"v2_execution_rank": 259, "phase_layer": 3, "phase_item_id": ITEM}, "G08-V2-CONTEXT", "claim tuple mismatch")
    empty_fields = (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids",
        "shared_group_ids", "parent_inspection_order", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    )
    for field in empty_fields:
        require(ledger[field] == [], "G08-V2-CONTEXT", f"declared empty closure field {field} is nonempty")
    require(ledger["closure_status"] == "empty_closure_audited" and ledger["closure_audit"]["traversal_count"] == 0, "G08-V2-CONTEXT", "empty closure was not audited exactly once")
    require(ledger["provider_acceptance_inherited"] is False and ledger["consumer_acceptance_required"] is True, "G08-V2-CONTEXT", "acceptance boundary is unsound")


def assert_registry(registry: dict[str, Any]) -> list[str]:
    require(registry["schema_version"] == "stage1-obligation-registry/1.0", "T02-REGISTRY", "registry schema mismatch")
    require(registry["item_id"] == ITEM and registry["theorem_id"] == THEOREM, "T02-REGISTRY", "registry identity mismatch")
    require(registry["frozen_against_statement_sha256"] == STATEMENT_SHA256 and registry["frozen_against_statement_record_sha256"] == STATEMENT_RECORD_SHA256, "T02-REGISTRY", "statement binding changed")
    require(registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256, "T02-REGISTRY", "anchor binding changed")
    rows = registry["obligations"]
    identifiers = [row["obligation_id"] for row in rows]
    require(len(identifiers) == len(set(identifiers)) == 29, "T02-REGISTRY", "obligation IDs are missing or duplicated")
    require(identifiers[0] == registry["root_obligation_id"] == "M0412-ROOT-IDENTITY", "T02-REGISTRY", "root obligation mismatch")
    require(calculated_denominator(registry) == registry["denominator_sha256"] == REGISTRY_DENOMINATOR, "T02-REGISTRY", "denominator hash mismatch")
    require(registry["frozen_denominators"]["inventory"] == identifiers, "T02-REGISTRY", "inventory denominator mismatch")
    for key, field, value in (
        ("required_machine", "machine_eligibility", "required"),
        ("required_human_source", "human_source_eligibility", "required"),
        ("required_readable", "readable_eligibility", "required"),
    ):
        require(registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == value], "T02-REGISTRY", f"{key} denominator mismatch")
    projection_fields = set(registry["canonical_projection_fields"])
    for row in rows:
        require(set(row) == projection_fields, "T02-REGISTRY", f"noncanonical row schema: {row.get('obligation_id')}")
        require(row["root_relevant"] is True and row["terminal_proof_body_id"] is None, "T02-REGISTRY", "registry hid an obligation or fabricated a body")
        require(row["statement_fingerprint"].startswith("planned-identity-dependent-sha256:") and len(row["statement_fingerprint"].split(":")[-1]) == 64, "T02-REGISTRY", "planned fingerprint is malformed")
        if "not_applicable" in {row["human_source_eligibility"], row["readable_eligibility"]}:
            exclusion = row["exclusion_reason"]
            require(isinstance(exclusion, dict) and set(exclusion) == {"code", "justification", "review"} and all(exclusion.values()), "T02-REGISTRY", "axis exclusion lacks explicit review")
    layers = registry["mandatory_layer_analysis"]
    require(set(layers) == {"S", "N", "B", "C", "L", "X", "T", "not_applicable_layers"}, "T02-REGISTRY", "mandatory layer analysis incomplete")
    require(layers["not_applicable_layers"] == [] and all(layers[layer] for layer in "SNBCLXT"), "T02-REGISTRY", "mandatory layer missing")
    require({identifier for layer in "SNBCLXT" for identifier in layers[layer]} == set(identifiers) - {"M0412-ROOT-IDENTITY"}, "T02-REGISTRY", "layer coverage mismatch")
    require(registry["append_only_delta"] == [] and registry["registry_version"] == 1, "T02-REGISTRY", "initial freeze has an invalid delta")
    status = registry["status_observed_after_freeze"]
    require(status["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"} and status["accepted_closed_obligations"] == [], "T02-REGISTRY", "status was inferred into the denominator")
    require(status["exact_formal_targets"] == [] and status["terminal_proof_body_ids"] == [], "T02-REGISTRY", "registry fabricated an exact target or body")
    return identifiers


def reachable(edges: list[dict[str, Any]], root: str) -> set[str]:
    adjacency: dict[str, list[str]] = {}
    for edge in edges:
        if edge["type"] in {"proof_requires", "logical_decomposition"}:
            adjacency.setdefault(edge["from"], []).append(edge["to"])
    visited: set[str] = set()
    active: set[str] = set()

    def visit(identifier: str) -> None:
        require(identifier not in active, "T03-GRAPHS", f"cycle at {identifier}")
        if identifier in visited:
            return
        active.add(identifier)
        for child in adjacency.get(identifier, []):
            visit(child)
        active.remove(identifier)
        visited.add(identifier)

    visit(root)
    return visited


def assert_graphs(bundle: dict[str, Any], registry: dict[str, Any], identifiers: list[str]) -> None:
    require(bundle["schema_version"] == "stage1-typed-graphs/1.0" and bundle["item_id"] == ITEM and bundle["theorem_id"] == THEOREM, "T03-GRAPHS", "bundle identity mismatch")
    require(bundle["registry_denominator_sha256"] == REGISTRY_DENOMINATOR, "T03-GRAPHS", "bundle denominator mismatch")
    nodes = bundle["nodes"]
    require([node["obligation_id"] for node in nodes] == identifiers, "T03-GRAPHS", "nodes do not exactly project the registry")
    markdown = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    for node in nodes:
        require(REQUIRED_NODE_FIELDS <= set(node), "T03-GRAPHS", f"node fields incomplete: {node.get('obligation_id')}")
        identifier = node["obligation_id"]
        require(node["human_statement"] == registry["obligation_statements"][identifier], "T03-GRAPHS", f"node statement drift: {identifier}")
        require(isinstance(node["step_budget"], int) and 0 < node["step_budget"] <= 100, "T02-REGISTRY", f"leaf budget invalid: {identifier}")
        ledger = node["semantic_step_ledger"]
        require(isinstance(ledger, list) and 1 <= len(ledger) <= node["step_budget"], "T02-REGISTRY", f"leaf ledger invalid: {identifier}")
        step_ids = [step["step_id"] for step in ledger]
        require(len(step_ids) == len(set(step_ids)), "T02-REGISTRY", f"duplicate leaf step: {identifier}")
        for step in ledger:
            require(set(step) == {"step_id", "premise_ids", "inference", "output", "outgoing_use"}, "T02-REGISTRY", f"step schema invalid: {identifier}")
            require(isinstance(step["premise_ids"], list) and all(isinstance(value, str) and value for value in step["premise_ids"]), "T02-REGISTRY", f"step premises invalid: {identifier}")
            require(all(isinstance(step[key], str) and step[key] for key in ("inference", "output", "outgoing_use")), "T02-REGISTRY", f"empty leaf step: {identifier}")
        require(re.search(rf"^### {re.escape(identifier)}$", markdown, re.MULTILINE) is not None, "T03-GRAPHS", f"readable node missing: {identifier}")
        require(node["public_readable_target"].endswith("#" + identifier.lower()), "T03-GRAPHS", f"readable anchor mismatch: {identifier}")

    graphs = bundle["graphs"]
    require(set(graphs) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}, "T03-GRAPHS", "seven graph classes are not separate")
    id_set = set(identifiers)
    edge_ids: set[str] = set()
    semantic_edges: list[dict[str, Any]] = []
    for name, graph in graphs.items():
        require(set(graph["out"]) == id_set and set(graph["in"]) == id_set, "T03-GRAPHS", f"graph indexes incomplete: {name}")
        for edge in graph["edges"]:
            require(edge["edge_id"] not in edge_ids and edge["from"] in id_set and edge["to"] in id_set, "T03-GRAPHS", f"illegal or duplicate edge in {name}")
            edge_ids.add(edge["edge_id"])
            require(edge["type"] in ALLOWED_EDGE_TYPES, "T03-GRAPHS", f"untyped semantics in {name}")
            require(edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]], "T03-GRAPHS", f"broken graph index in {name}")
            if name in {"proof", "refinement"}:
                semantic_edges.append(edge)
        if name in {"proof", "refinement"}:
            indexed = {edge["edge_id"]: edge for edge in graph["edges"]}
            for edge in graph["edges"]:
                reverse = indexed.get(edge["reciprocal_edge_id"])
                require(reverse is not None and reverse["reciprocal_edge_id"] == edge["edge_id"], "T03-GRAPHS", f"missing reciprocal in {name}")
                require((reverse["from"], reverse["to"]) == (edge["to"], edge["from"]), "T03-GRAPHS", f"reciprocal endpoint mismatch in {name}")
                require("composes" in {edge["type"], reverse["type"]}, "T03-GRAPHS", f"reciprocal types invalid in {name}")
    require(len(edge_ids) == bundle["edge_count"] == 122, "T03-GRAPHS", "typed edge count mismatch")
    require(reachable(semantic_edges, "M0412-ROOT-IDENTITY") == id_set - {"M0412-X-IMPORTED", "M0412-X-SOURCE", "M0412-X-PROVENANCE", "M0412-X-TRUST", "M0412-X-READABLE", "M0412-X-WORKFLOW"}, "T03-GRAPHS", "proof/refinement root reachability mismatch")
    for name in ("provenance", "evidence", "trust", "documentation", "workflow"):
        touched = {edge["from"] for edge in graphs[name]["edges"]} | {edge["to"] for edge in graphs[name]["edges"]}
        require(touched, "T03-GRAPHS", f"support graph {name} is empty")


def assert_composition(bundle: dict[str, Any]) -> None:
    require(bundle["composition_certificates"] == [], "T04-COMPOSITION", "a composition certificate was fabricated")
    boundary = bundle["composition_ineligibility"]
    require(boundary["status"] == "not_machine_eligible_no_exact_parent_or_child_targets", "T04-COMPOSITION", "composition ineligibility status changed")
    require(boundary["source_is_declaration_free"] is True and boundary["composition_source"].endswith("/ObligationTree.lean"), "T04-COMPOSITION", "composition boundary source mismatch")
    source_path = HERE / "ObligationTree.lean"
    code = lean_source_without_comments(source_path.read_text(encoding="utf-8"))
    prohibited_declaration = re.compile(r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance|axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE)
    require(prohibited_declaration.search(code) is None, "T04-COMPOSITION", "declaration-free boundary contains a formal declaration")
    require(not re.search(r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b", code), "T04-COMPOSITION", "composition source contains a placeholder or oracle")
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    result = subprocess.run(
        ["lake", "env", "lean", str(source_path)], cwd=LEAN_ROOT, env=environment,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120, check=False,
    )
    require(result.returncode == 0 and result.stdout == result.stderr == "", "T04-COMPOSITION", "declaration-free Lean boundary does not elaborate")
    closure = bundle["closure_boundary"]
    require(closure["closed_obligations"] == [] and closure["root_closed"] is False, "T04-COMPOSITION", "open root was marked closed")
    require(closure["remaining_machine_root_cut_set"] == ["M0412-ROOT-IDENTITY"], "T04-COMPOSITION", "root cut set mismatch")
    require(closure["audit_complete"] is closure["theorem_complete"] is False, "T04-COMPOSITION", "terminal flag was inferred")


def assert_deterministic_build() -> None:
    generator_source = (HERE / "build_obligation_artifacts.py").read_text(encoding="utf-8")
    require("sorry" not in generator_source and "admit" not in generator_source, "T02-REGISTRY", "generator contains prohibited proof vocabulary")
    generated_registry = builder.registry()
    generated_bundle = builder.bundle(generated_registry)
    expected_registry = json.dumps(generated_registry, ensure_ascii=True, indent=2) + "\n"
    expected_bundle = json.dumps(generated_bundle, ensure_ascii=True, indent=2) + "\n"
    require((HERE / "obligation-registry.json").read_text(encoding="utf-8") == expected_registry, "T02-REGISTRY", "generator does not reproduce obligation-registry.json")
    require((HERE / "typed-graphs.json").read_text(encoding="utf-8") == expected_bundle, "T02-REGISTRY", "generator does not reproduce typed-graphs.json")


def assert_receipt(registry: dict[str, Any], bundle: dict[str, Any]) -> None:
    receipt = load(HERE / "obligation-tree-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    require(receipt["schema_version"] == "stage1-node-receipt/1.0" and receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM, "T01-ARTIFACTS", "receipt identity mismatch")
    require(receipt["phase"] == "obligation_tree" and receipt["intent"] == "audit", "T01-ARTIFACTS", "receipt phase or intent mismatch")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE, "G09-FRESHNESS", "receipt base mismatch")
    require(receipt["support_state"] == "provisional_worker_selftest" and receipt["proposed_state"] == "[_]", "T01-ARTIFACTS", "receipt support state mismatch")
    require(receipt["accepted"] is False and receipt["verdict"] == "accepted", "T01-ARTIFACTS", "worker/master acceptance boundary mismatch")
    require(receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR, "T02-REGISTRY", "receipt denominator mismatch")
    identifiers = [row["obligation_id"] for row in registry["obligations"]]
    require(receipt["canonical_obligation_ids"] == identifiers, "T02-REGISTRY", "receipt obligation IDs mismatch")
    require(receipt["composition_certificates"] == bundle["composition_certificates"] == [], "T04-COMPOSITION", "receipt fabricated composition evidence")
    require(receipt["composition_ineligibility"]["status"] == bundle["composition_ineligibility"]["status"], "T04-COMPOSITION", "receipt composition boundary mismatch")
    require(receipt["audit_complete"] is receipt["theorem_complete"] is False, "T04-COMPOSITION", "receipt terminal flags invalid")
    require(receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}, "T02-REGISTRY", "receipt debt vector changed")
    require(receipt["dependency_context"]["parent_inspection_order"] == [] and receipt["dependency_context"]["provider_acceptance_inherited"] is False, "G08-V2-CONTEXT", "receipt dependency boundary invalid")

    selected = {row["role"]: row for row in receipt["inputs"]["selected_artifacts"]}
    require(set(selected) == {"obligation_registry", "typed_graph_bundle", "readable_tree", "composition_source", "phase_receipt"}, "T01-ARTIFACTS", "receipt selected roles mismatch")
    for role, expected_hash in EXPECTED_SELECTED_HASHES.items():
        path = ROOT / selected[role]["path"]
        require(sha256(path) == selected[role]["sha256"] == expected_hash, "G03-ARTIFACT-BINDING", f"selected role hash mismatch: {role}")
        require(git("hash-object", str(path)) == selected[role]["git_blob"], "G03-ARTIFACT-BINDING", f"selected role blob mismatch: {role}")
    phase_receipt = selected["phase_receipt"]
    require(phase_receipt["path"].endswith("/obligation-tree-receipt.json") and phase_receipt["sha256"] is phase_receipt["git_blob"] is None, "G03-ARTIFACT-BINDING", "receipt self-reference boundary invalid")

    generator_binding = receipt["inputs"]["validation_inputs"][0]
    require(sha256(ROOT / generator_binding["path"]) == generator_binding["sha256"], "G09-FRESHNESS", "generator input hash mismatch")
    validator_binding = receipt["inputs"]["validation_inputs"][1]
    validator_path = ROOT / validator_binding["path"]
    require(sha256(validator_path) == validator_binding["sha256"] and git("hash-object", str(validator_path)) == validator_binding["git_blob"], "G09-FRESHNESS", "validator input binding mismatch")
    phase_dependencies = {Path(row["path"]).name: row for row in receipt["inputs"]["phase_dependencies"]}
    for name in ("statement-receipt.json", "anchor-audit-receipt.json"):
        path = HERE / name
        require(sha256(path) == phase_dependencies[name]["sha256"] and git("hash-object", str(path)) == phase_dependencies[name]["git_blob"], "G09-FRESHNESS", f"predecessor receipt binding mismatch: {name}")
        require(phase_dependencies[name]["acceptance_inherited"] is False, "G02-TOPOLOGY", "predecessor acceptance was inherited")

    if receipt["selftest_status"] == "passed":
        require(receipt["phase_predicate_proven"] is receipt["phase_accepted"] is True, "T01-ARTIFACTS", "passed receipt lacks semantic phase result")
        require(receipt["first_failed_gate"] is None and receipt["selftest_result"]["exit_code"] == 0, "T01-ARTIFACTS", "passed receipt has a failed gate")
        require(receipt["selftest_result"]["commands"], "T01-ARTIFACTS", "passed receipt has no commands")
        packet = load(ROOT / ".stage1-worker-selftest.json")
        require(packet["item_id"] == ITEM and packet["state"] == "[_]" and packet["base_revision"] == BASE_REVISION, "T01-ARTIFACTS", "worker packet identity mismatch")
        require(packet["commands"] == receipt["selftest_result"]["commands"] and packet["commands"] == receipt["commands"], "T01-ARTIFACTS", "worker commands do not bind receipt")
        require(packet["changed_paths"] == receipt["changed_paths"] and packet["known_failures"] == receipt["known_failures"], "T01-ARTIFACTS", "worker packet evidence differs from receipt")
        require(packet["output_summary"] == receipt["output_summary"], "T01-ARTIFACTS", "worker packet summary differs from receipt")
    else:
        require(receipt["selftest_status"] == "pending" and receipt["selftest_result"] == {"exit_code": None, "commands": []}, "T01-ARTIFACTS", "pre-selftest receipt has invalid state")


def assert_hygiene() -> None:
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for path in (HERE / "Statement.lean", HERE / "StatementProbe.lean", HERE / "AnchorAudit.lean", HERE / "ObligationTree.lean"):
        require(prohibited.search(lean_source_without_comments(path.read_text(encoding="utf-8"))) is None, "T04-COMPOSITION", f"prohibited Lean construct in {path.name}")
    changed_paths = load(HERE / "obligation-tree-receipt.json")["changed_paths"]
    for relative in changed_paths:
        path = ROOT / relative
        if not path.exists():
            require(relative == ".stage1-worker-selftest.json", "T01-ARTIFACTS", f"changed path missing: {relative}")
            continue
        data = path.read_bytes()
        require(data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, "T01-ARTIFACTS", f"file hygiene failed: {relative}")
        require(all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), "T01-ARTIFACTS", f"trailing whitespace: {relative}")


def validate() -> None:
    assert_authorities()
    assert_contract_and_target()
    assert_dependency_ledger()
    registry = load(HERE / "obligation-registry.json")
    identifiers = assert_registry(registry)
    bundle = load(HERE / "typed-graphs.json")
    assert_graphs(bundle, registry, identifiers)
    assert_composition(bundle)
    assert_deterministic_build()
    assert_receipt(registry, bundle)
    assert_hygiene()
    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    require(git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION, "G09-FRESHNESS", "mathlib revision changed")
    require(git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE, "G09-FRESHNESS", "mathlib tree changed")
    require(git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == "", "G09-FRESHNESS", "pinned mathlib is dirty")


def failure_result(failure: GateFailure) -> dict[str, Any]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "obligation_tree",
        "status": "failed",
        "verdict": "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": failure.gate,
        "open_obligations": 1,
        "stale_inputs": failure.stale,
        "blocked": True,
        "message": failure.message,
    }


def main() -> int:
    try:
        validate()
    except GateFailure as failure:
        print(json.dumps(failure_result(failure), sort_keys=True, separators=(",", ":")))
        return 1
    except Exception as exc:
        failure = GateFailure("T01-ARTIFACTS", f"unexpected validator failure: {type(exc).__name__}: {exc}")
        print(json.dumps(failure_result(failure), sort_keys=True, separators=(",", ":")))
        return 1
    print(json.dumps(SEMANTIC_RESULT, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
