#!/usr/bin/env python3
"""Fail-closed semantic validator for the THM-M-0115 obligation freeze."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_obligation_artifacts as builder


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0115-OBLIGATION_TREE"
THEOREM = "THM-M-0115"
BASE_REVISION = "c5037228977a81948bbd6119e1728b4b65b9924e"
BASE_TREE = "78b2627e717156dffe240bea12d14205af667d2a"
GRAPH_SHA256 = "fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
STATEMENT_SHA256 = "26648a8514a0a9240c831132918c9ad0f735eb7accce33f2287a45961394d538"
STATEMENT_RECORD_SHA256 = "241a8d4b943a6431050fece1beca135557777c42ff44e8169d30383c66763e3f"
ANCHOR_SHA256 = "1aa93316cb6fec237cf88f0ce4bf9633bbcc25a26f54a1c11a69c41225ff8d4f"
REGISTRY_DENOMINATOR = "f1455869731874b94cb533d3a6ee70bb15d428438472ffc205b63888eae68527"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
REQUIRED_NODE_FIELDS = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
ALLOWED_EDGE_TYPES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
REQUIRED_SEMANTIC_FIELDS = {
    "schema_version", "item_id", "theorem_id", "phase", "status", "verdict",
    "phase_accepted", "audit_complete", "theorem_complete",
    "phase_predicate_proven", "first_failed_gate", "open_obligations",
    "stale_inputs", "blocked", "message",
}


class GateFailure(Exception):
    def __init__(self, gate: str, message: str, *, stale: list[str] | None = None):
        super().__init__(message)
        self.gate = gate
        self.message = message
        self.stale = stale or []


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise GateFailure("T01-ARTIFACTS", f"duplicate JSON key {key}")
        result[key] = value
    return result


def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GateFailure("T01-ARTIFACTS", f"cannot read structured artifact {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise GateFailure("T01-ARTIFACTS", f"{path.name} must contain one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command_output(*argv: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()


def require(condition: bool, gate: str, message: str, *, stale: list[str] | None = None) -> None:
    if not condition:
        raise GateFailure(gate, message, stale=stale)


def canonical_projection(registry: dict) -> list[dict]:
    fields = registry["canonical_projection_fields"]
    return [{field: row[field] for field in fields} for row in registry["obligations"]]


def calculated_denominator(registry: dict) -> str:
    return hashlib.sha256(
        json.dumps(canonical_projection(registry), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def assert_authorities() -> None:
    required = {
        ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
        ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
        HERE / "Statement.lean": STATEMENT_SHA256,
        HERE / "statement.json": STATEMENT_RECORD_SHA256,
        HERE / "anchor-audit.json": ANCHOR_SHA256,
    }
    stale = [str(path.relative_to(ROOT)) for path, digest in required.items() if not path.is_file() or sha256(path) != digest]
    require(not stale, "G09-FRESHNESS", "one or more frozen authority inputs changed", stale=stale)
    require(command_output("git", "rev-parse", "HEAD") == BASE_REVISION, "G09-FRESHNESS", "validator replay revision differs from the worker base", stale=["HEAD"])
    require(command_output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "G09-FRESHNESS", "validator replay tree differs from the worker base", stale=["HEAD^{tree}"])


def assert_contract_and_target() -> None:
    contract = load(ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row["phase"] == "obligation_tree")
    require(phase["layer"] == 3 and phase["item_suffix"] == "OBLIGATION_TREE", "T01-ARTIFACTS", "phase contract identity changed")
    roles = {row["role"]: row for row in phase["required_artifact_roles"]}
    expected_roles = {"obligation_registry", "typed_graph_bundle", "readable_tree", "composition_source", "phase_receipt"}
    require(set(roles) == expected_roles, "T01-ARTIFACTS", "phase artifact roles are incomplete")
    expected_paths = {
        "obligation_registry": "obligation-registry.json",
        "typed_graph_bundle": "typed-graphs.json",
        "readable_tree": "obligation-tree.md",
        "composition_source": "ObligationTree.lean",
        "phase_receipt": "obligation-tree-receipt.json",
    }
    for role, name in expected_paths.items():
        candidates = [Path(path.replace("{theorem_id}", THEOREM)).name for path in roles[role]["path_candidates"]]
        require(candidates == [name], "T01-ARTIFACTS", f"role {role} candidate changed")
        require((HERE / name).is_file() and not (HERE / name).is_symlink(), "T01-ARTIFACTS", f"role {role} is missing or unsafe")
    validators = [Path(row["path_pattern"].replace("{theorem_id}", THEOREM)).name for row in phase["validator_candidates"]]
    present = [name for name in validators if (HERE / name).is_file()]
    require(present == ["check_obligation_tree.py"], "T01-ARTIFACTS", "validator candidate selection is not exact")

    blueprint = (ROOT / "Docs" / "Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    pattern = re.compile(r"^- \[ \] `S56-M-0115-OBLIGATION_TREE` / `THM-M-0115` / `obligation_tree`.*\{attempts=0\}$", re.MULTILINE)
    require(pattern.search(blueprint) is not None, "G01-SSOT-CAS", "authoritative phase row is not the assigned open item")
    require("- [_] `S56-M-0115-ANCHOR_AUDIT`" in blueprint, "G02-TOPOLOGY", "predecessor state is not the inspected provisional state")

    dag = load(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json")
    target = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM)
    require(target["v2_execution_rank"] == 260 and target["topological_layer"] == 0, "G08-V2-CONTEXT", "target v2 order changed")
    require(target["dependency_context_sha256"] == CONTEXT_SHA256, "G08-V2-CONTEXT", "dependency context changed")
    for field in ("direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids", "shared_lemma_group_ids"):
        require(target[field] == [], "G08-V2-CONTEXT", f"target {field} is no longer empty")


def assert_preflight_structure() -> None:
    # The fresh DAG generator inventories untracked owned files, while this
    # worker is forbidden to rewrite the checked-in projection. Reproduce the
    # base validator in a temporary checkout instead of mutating the live
    # worker directory to hide its delta.
    with tempfile.TemporaryDirectory(prefix="thm-m-0115-dag-preflight-") as temporary:
        checkout = Path(temporary)
        clone = subprocess.run(
            ["git", "clone", "--no-checkout", "--filter=blob:none", "--reference-if-able", str(ROOT), str(ROOT), str(checkout)],
            cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
        require(clone.returncode == 0, "G08-V2-CONTEXT", "temporary base DAG checkout could not be created")
        checkout_result = subprocess.run(
            ["git", "checkout", "--detach", BASE_REVISION], cwd=checkout,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
        require(checkout_result.returncode == 0, "G08-V2-CONTEXT", "temporary base DAG revision could not be checked out")
        result = subprocess.run(
            [sys.executable, "-B", "Docs/tools/check_stage1_theorem_dag_v2.py"],
            cwd=checkout, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
    require(result.returncode == 0 and "check_stage1_theorem_dag_v2: ok" in result.stdout, "G08-V2-CONTEXT", "base DAG preflight fails independently of the owned unintegrated inventory delta")


def assert_dependency_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1", "G08-V2-CONTEXT", "dependency ledger schema mismatch")
    require(ledger["consumer_theorem_id"] == THEOREM and ledger["item_id"] == ITEM, "G08-V2-CONTEXT", "dependency ledger identity mismatch")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256, "G08-V2-CONTEXT", "dependency ledger graph digest mismatch")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256 and ledger["repository_revision"] == BASE_REVISION, "G08-V2-CONTEXT", "dependency ledger context or base mismatch")
    require(ledger["claim_order"] == {"v2_execution_rank": 260, "phase_layer": 3, "phase_item_id": ITEM}, "G08-V2-CONTEXT", "claim order mismatch")
    for field in ("direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids", "shared_group_ids", "parent_inspection_order", "inspections", "reuse_decisions", "unresolved_compatibility_obligations"):
        require(ledger[field] == [], "G08-V2-CONTEXT", f"empty closure field {field} is not empty")
    require(ledger["closure_status"] == "empty_closure_audited" and ledger["provider_acceptance_inherited"] is False, "G08-V2-CONTEXT", "empty closure boundary is not fail-closed")


def assert_registry(registry: dict) -> tuple[list[str], str]:
    require(registry["schema_version"] == "stage1-obligation-registry/1.0", "T02-REGISTRY", "registry schema mismatch")
    require(registry["item_id"] == ITEM and registry["theorem_id"] == THEOREM, "T02-REGISTRY", "registry identity mismatch")
    require(registry["frozen_against_statement_sha256"] == STATEMENT_SHA256, "T02-REGISTRY", "registry statement binding is stale")
    require(registry["frozen_against_statement_record_sha256"] == STATEMENT_RECORD_SHA256, "T02-REGISTRY", "registry statement record binding is stale")
    require(registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256, "T02-REGISTRY", "registry anchor binding is stale")
    fields = list(builder.PROJECTION_FIELDS)
    require(registry["canonical_projection_fields"] == fields, "T02-REGISTRY", "registry projection fields changed")
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    require(len(ids) == len(set(ids)) == 32 and ids[0] == registry["root_obligation_id"] == "M0115-ROOT", "T02-REGISTRY", "registry IDs are missing, duplicated, or rootless")
    require(rows == builder.projection(builder.ROWS), "T02-REGISTRY", "registry is not the deterministic frozen projection")
    digest = calculated_denominator(registry)
    require(digest == registry["denominator_sha256"] == REGISTRY_DENOMINATOR, "T02-REGISTRY", "registry denominator is stale")
    required_row_fields = set(fields)
    for row in rows:
        require(set(row) == required_row_fields, "T02-REGISTRY", f"obligation {row.get('obligation_id')} has a noncanonical field set")
        require(row["root_relevant"] is True, "T02-REGISTRY", "root-relevant obligation was silently excluded")
        require(row["machine_eligibility"] in {"required", "informational"}, "T02-REGISTRY", "invalid machine eligibility")
        require(row["human_source_eligibility"] in {"required", "not_applicable"}, "T02-REGISTRY", "invalid human eligibility")
        require(row["readable_eligibility"] in {"required", "not_applicable"}, "T02-REGISTRY", "invalid readable eligibility")
        require(row["risk_class"] in {"critical", "high", "normal", "low"}, "T02-REGISTRY", "invalid risk")
        if "not_applicable" in {row["human_source_eligibility"], row["readable_eligibility"]}:
            exclusion = row["exclusion_reason"]
            require(isinstance(exclusion, dict) and set(exclusion) == {"code", "justification", "review"} and all(exclusion.values()), "T02-REGISTRY", "ineligible axis lacks explicit reviewed exclusion")
        require(row["terminal_proof_body_id"] is None, "T02-REGISTRY", "architecture fabricated a terminal proof body")
    denominators = registry["frozen_denominators"]
    require(denominators["inventory"] == ids, "T02-REGISTRY", "inventory denominator mismatch")
    for axis, key, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
        require(denominators[axis] == [row["obligation_id"] for row in rows if row[key] == value], "T02-REGISTRY", f"{axis} denominator mismatch")
    layers = registry["mandatory_layer_analysis"]
    require(set(layers) == {"S", "N", "B", "C", "L", "X", "T", "not_applicable_layers"}, "T02-REGISTRY", "mandatory layer analysis is incomplete")
    require(layers["not_applicable_layers"] == [] and all(layers[layer] for layer in "SNBCLXT"), "T02-REGISTRY", "a mandatory layer is missing")
    require(set(identifier for layer in "SNBCLXT" for identifier in layers[layer]) == set(ids), "T02-REGISTRY", "mandatory layer mapping does not cover the registry")
    require(registry["append_only_delta"] == [] and registry["registry_version"] == 1, "T02-REGISTRY", "initial freeze has an invalid delta")
    require(registry["status_observed_after_freeze"]["accepted_closed_obligations"] == [], "T02-REGISTRY", "registry inferred proof closure")
    return ids, digest


def proof_reachability(children: dict[str, list[str]], root: str) -> set[str]:
    visited: set[str] = set()
    visiting: set[str] = set()

    def visit(identifier: str) -> None:
        require(identifier not in visiting, "T03-GRAPHS", "proof graph contains a cycle")
        if identifier in visited:
            return
        visiting.add(identifier)
        for child in children.get(identifier, []):
            visit(child)
        visiting.remove(identifier)
        visited.add(identifier)

    visit(root)
    return visited


def assert_graphs(bundle: dict, registry: dict, ids: list[str], digest: str) -> None:
    require(bundle["schema_version"] == "stage1-typed-graphs/1.0", "T03-GRAPHS", "graph schema mismatch")
    require(bundle["item_id"] == ITEM and bundle["theorem_id"] == THEOREM and bundle["registry_denominator_sha256"] == digest, "T03-GRAPHS", "graph identity or denominator mismatch")
    nodes = bundle["nodes"]
    require(len(nodes) == len(ids) and [node["obligation_id"] for node in nodes] == ids, "T03-GRAPHS", "graph nodes do not exactly project registry order")
    statement_by_id = registry["obligation_statements"]
    markdown = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    for node in nodes:
        require(REQUIRED_NODE_FIELDS <= set(node), "T03-GRAPHS", f"node {node.get('obligation_id')} lacks required fields")
        identifier = node["obligation_id"]
        require(node["human_statement"] == statement_by_id[identifier], "T03-GRAPHS", f"node {identifier} statement drifted")
        require(isinstance(node["step_budget"], int) and 0 < node["step_budget"] <= 100, "T02-REGISTRY", f"node {identifier} exceeds leaf budget")
        ledger = node["semantic_step_ledger"]
        require(isinstance(ledger, list) and 1 <= len(ledger) <= node["step_budget"], "T02-REGISTRY", f"node {identifier} lacks a substantive step ledger")
        step_ids = [step["step_id"] for step in ledger]
        require(len(step_ids) == len(set(step_ids)), "T02-REGISTRY", f"node {identifier} duplicates step IDs")
        for step in ledger:
            require(set(step) == {"step_id", "premise_ids", "inference", "output", "outgoing_use"}, "T02-REGISTRY", f"node {identifier} step schema mismatch")
            require(isinstance(step["premise_ids"], list) and all(isinstance(value, str) and value for value in step["premise_ids"]), "T02-REGISTRY", f"node {identifier} step premises are malformed")
            require(all(isinstance(step[key], str) and step[key] for key in ("inference", "output", "outgoing_use")), "T02-REGISTRY", f"node {identifier} has filler or empty step fields")
        anchor = node["public_readable_target"].split("#", 1)[1]
        require(re.search(rf"^### {re.escape(identifier)}$", markdown, re.MULTILINE) is not None and anchor == identifier.lower(), "T03-GRAPHS", f"node {identifier} lacks its unique readable anchor")

    graphs = bundle["graphs"]
    require(set(graphs) == set(builder.GRAPH_NAMES), "T03-GRAPHS", "seven typed graphs are not separate and complete")
    edge_ids: set[str] = set()
    id_set = set(ids)
    for name, graph in graphs.items():
        require(set(graph["out"]) == id_set and set(graph["in"]) == id_set, "T03-GRAPHS", f"graph {name} indexes do not cover every node")
        for edge in graph["edges"]:
            require(edge["edge_id"] not in edge_ids, "T03-GRAPHS", "typed edge ID is duplicated")
            edge_ids.add(edge["edge_id"])
            require(edge["type"] in ALLOWED_EDGE_TYPES and edge["from"] in id_set and edge["to"] in id_set, "T03-GRAPHS", f"graph {name} has an illegal edge")
            require(edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]], "T03-GRAPHS", f"graph {name} reciprocity index is broken")
    require(len(edge_ids) == bundle["edge_count"] == 192, "T03-GRAPHS", "typed edge count mismatch")

    proof_edges = {edge["edge_id"]: edge for edge in graphs["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    reverse_types: dict[tuple[str, str], str] = {}
    for edge in proof_edges.values():
        reverse = proof_edges.get(edge["reciprocal_edge_id"])
        require(reverse is not None and reverse["reciprocal_edge_id"] == edge["edge_id"], "T03-GRAPHS", "proof edge lacks exact reciprocal")
        require((reverse["from"], reverse["to"]) == (edge["to"], edge["from"]), "T03-GRAPHS", "proof reciprocal endpoints disagree")
        require("proof_requires" in {edge["type"], reverse["type"]} and ({edge["type"], reverse["type"]} <= {"proof_requires", "composes", "logical_decomposition"}), "T03-GRAPHS", "proof reciprocal types are illegal")
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
            reverse_types[(edge["from"], edge["to"])] = reverse["type"]
    require(children == builder.PROOF_CHILDREN, "T03-GRAPHS", "proof child architecture changed")
    reachable = proof_reachability(children, "M0115-ROOT")
    required_machine = set(registry["frozen_denominators"]["required_machine"])
    proof_architecture = set(identifier for identifier in required_machine if not identifier.startswith("M0115-S-BOUNDARY") and identifier not in {"M0115-S-TARGET", "M0115-S-TRANSPORT", "M0115-S-FOUNDATION", "M0115-X-MATHLIB", "M0115-X-EXTERNAL"})
    require(proof_architecture <= reachable, "T03-GRAPHS", "a root-relevant proof obligation is orphaned")

    source_edges = graphs["provenance"]["edges"]
    for row in registry["obligations"]:
        identifier = row["obligation_id"]
        if row["human_source_eligibility"] == "required" and identifier != "M0115-X-SOURCE":
            require(any(edge["type"] == "source_map" and edge["from"] == identifier and edge["to"] == "M0115-X-SOURCE" for edge in source_edges), "T03-GRAPHS", f"source-required node {identifier} lacks a source map")
    require(graphs["evidence"]["edges"] == [], "T03-GRAPHS", "evidence graph fabricated an evidence relationship")
    require(not any(edge["type"] == "evidence_for" for edge in source_edges), "T03-GRAPHS", "provenance graph fabricated evidence")
    require(not any(edge["to"] == "M0115-ROOT" and edge["type"] == "provenance_of" for edge in source_edges), "T03-GRAPHS", "graph fabricated a root proof body")

    certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
    require(set(certificates) == set(builder.CHECKED_COMPOSITIONS), "T04-COMPOSITION", "checked certificate set changed")
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in registry["obligations"]}
    for parent, declaration in builder.CHECKED_COMPOSITIONS.items():
        cert = certificates[parent]
        expected_children = children[parent]
        require(cert["required_child_ids"] == expected_children, "T04-COMPOSITION", f"certificate {parent} omits or adds a child")
        require(cert["parent_statement_fingerprint"] == fingerprints[parent], "T04-COMPOSITION", f"certificate {parent} parent fingerprint mismatch")
        require(cert["required_child_statement_fingerprints"] == {child: fingerprints[child] for child in expected_children}, "T04-COMPOSITION", f"certificate {parent} child fingerprint mismatch")
        require(cert["checked_declaration"] == declaration and cert["certificate_kind"] == "lean_abstract_child_harness", "T04-COMPOSITION", f"certificate {parent} declaration mismatch")
        require(cert["consumes_all_required_children"] is True and cert["yields_exact_parent"] is True and cert["introduces_undeclared_premises"] is False, "T04-COMPOSITION", f"certificate {parent} has invalid composition semantics")
        require(all(reverse_types[(parent, child)] == "composes" for child in expected_children), "T04-COMPOSITION", f"certificate {parent} is not represented by composes edges")
    plans = {row["parent_obligation_id"]: row for row in bundle["unverified_decomposition_plans"]}
    require(set(plans) == set(children) - set(certificates), "T04-COMPOSITION", "unverified decompositions are hidden or overclaimed")
    for parent, plan in plans.items():
        require(plan["planned_child_ids"] == children[parent] and plan["status"] == "source_architecture_decomposition_unverified_as_child_to_parent_composition", "T04-COMPOSITION", f"unverified plan {parent} is malformed")
        require(all(reverse_types[(parent, child)] == "logical_decomposition" for child in children[parent]), "T04-COMPOSITION", f"unverified plan {parent} is mislabeled as checked")
    boundary = bundle["closure_boundary"]
    require(boundary["closed_obligations"] == [] and boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False, "T04-COMPOSITION", "architecture inferred closure")


def assert_hygiene() -> None:
    lean = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    stripped = re.sub(r"/-.*?-/", "", lean, flags=re.DOTALL)
    stripped = re.sub(r"--.*", "", stripped)
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|implemented_by|extern|native_decide|proof_wanted)\b|^\s*(?:axiom|constant|unsafe|opaque)\b", re.MULTILINE)
    require(forbidden.search(stripped) is None, "T04-COMPOSITION", "composition source contains a prohibited construct")
    for declaration in (
        "root_of_assembled_root_package",
        "assembled_root_package_of_formula_package",
        "formula_package_of_relative_and_todd",
    ):
        require(f"theorem {declaration}" in lean and f"#print axioms {declaration}" in lean, "T04-COMPOSITION", f"composition declaration {declaration} is missing or unaudited")


def run_lean() -> tuple[str, str]:
    require((LEAN_ROOT / ".lake").exists(), "T04-COMPOSITION", "canonical pinned .lake artifacts are unavailable")
    lean_bin = command_output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = command_output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    require(command_output("git", "rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION, "G09-FRESHNESS", "mathlib revision changed", stale=["Formalizations/Lean/.lake/packages/mathlib"])
    require(command_output("git", "rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE, "G09-FRESHNESS", "mathlib tree changed", stale=["Formalizations/Lean/.lake/packages/mathlib"])
    require(command_output("git", "status", "--short", cwd=mathlib) == "", "G09-FRESHNESS", "mathlib worktree is dirty", stale=["Formalizations/Lean/.lake/packages/mathlib"])
    env = {**os.environ, "LEAN_PATH": lean_path, "LC_ALL": "C", "LANG": "C", "TZ": "UTC", "NO_COLOR": "1"}
    with tempfile.TemporaryDirectory(prefix="thm-m-0115-obligation-") as temporary:
        temp = Path(temporary)
        statement = subprocess.run(
            [lean_bin, "--trust=0", "-o", str(temp / "Statement.olean"), str(HERE / "Statement.lean")],
            cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        require(statement.returncode == 0, "T04-COMPOSITION", "Statement.lean failed narrow --trust=0 elaboration")
        obligation = subprocess.run(
            [lean_bin, "--trust=0", str(HERE / "ObligationTree.lean")],
            cwd=ROOT, env={**env, "LEAN_PATH": f"{temp}:{lean_path}"}, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        require(obligation.returncode == 0, "T04-COMPOSITION", "ObligationTree.lean failed narrow --trust=0 elaboration")
    output = obligation.stdout
    require("sorryAx" not in output, "T04-COMPOSITION", "Lean output contains sorryAx")
    required_reports = (
        "root_of_assembled_root_package' depends on axioms: [propext,",
        "assembled_root_package_of_formula_package' depends on axioms: [propext,",
        "formula_package_of_relative_and_todd' depends on axioms: [propext,",
    )
    require(all(report in output for report in required_reports), "T04-COMPOSITION", "Lean axiom report is incomplete")
    require(output.count("Classical.choice") == 3 and output.count("Quot.sound") == 3, "T04-COMPOSITION", "Lean axiom set differs from the declared boundary")
    return output, hashlib.sha256(output.encode()).hexdigest()


def assert_receipt_binding(binding: dict, *, allow_worktree: bool = False) -> None:
    path = ROOT / binding["path"]
    require(path.is_file() and not path.is_symlink() and binding["sha256"] == sha256(path), "G09-FRESHNESS", f"receipt input binding is stale: {binding['path']}", stale=[binding["path"]])
    if binding["git_blob"] is not None:
        if allow_worktree:
            expected_blob = command_output("git", "hash-object", str(path))
        else:
            expected_blob = command_output("git", "rev-parse", f"HEAD:{binding['path']}")
        require(binding["git_blob"] == expected_blob, "G09-FRESHNESS", f"receipt input Git blob is stale: {binding['path']}", stale=[binding["path"]])


def is_head_tracked(relative: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{relative}"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    ).returncode == 0


def assert_receipt_worker_packet(receipt: dict) -> None:
    packet_path = ROOT / ".stage1-worker-selftest.json"
    if not packet_path.exists():
        return
    require(packet_path.is_file() and not packet_path.is_symlink(), "T01-ARTIFACTS", "worker packet is unsafe")
    packet = load(packet_path)
    required = {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
    require(set(packet) == required, "T01-ARTIFACTS", "worker packet fields are not exact")
    require(packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION and packet["state"] == "[_]", "T01-ARTIFACTS", "worker packet identity or state mismatch")
    require(packet["commands"] == receipt["selftest_result"]["commands"], "T01-ARTIFACTS", "worker packet commands differ from the receipt")
    require(packet["known_failures"] == receipt["known_failures"], "T01-ARTIFACTS", "worker packet known failures differ from the receipt")
    require(isinstance(packet["output_summary"], str) and packet["output_summary"], "T01-ARTIFACTS", "worker packet output summary is empty")
    expected_changed = [
        ".stage1-worker-selftest.json",
        *[
            f"Stage1_Instances/{THEOREM}/{name}"
            for name in (
                "ObligationTree.lean", "build_obligation_artifacts.py",
                "check_obligation_tree.py", "dependency-reuse-ledger.json",
                "obligation-registry.json", "obligation-tree-receipt.json",
                "obligation-tree.md", "typed-graphs.json",
            )
        ],
    ]
    require(packet["changed_paths"] == expected_changed, "T01-ARTIFACTS", "worker packet does not declare the exact owned delta")
    status = command_output(
        "git", "status", "--porcelain=v1", "--untracked-files=all", "--",
        f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
    )
    actual = {line[3:] if line.startswith("?? ") else line[2:].lstrip() for line in status.splitlines()}
    require(actual == set(expected_changed), "T01-ARTIFACTS", "worker packet changed paths differ from the worktree")


def assert_receipt(receipt: dict, registry: dict, bundle: dict, ids: list[str], lean_sha256: str) -> None:
    require(receipt["schema_version"] == "stage1-node-receipt/1.0", "T01-ARTIFACTS", "receipt schema mismatch")
    require(receipt["receipt_id"] == "S56-M-0115-OBLIGATION-TREE-WORKER-20260717" and receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM, "T01-ARTIFACTS", "receipt identity mismatch")
    require(receipt["phase"] == "obligation_tree" and receipt["intent"] == "audit", "T01-ARTIFACTS", "receipt phase or intent mismatch")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE, "G09-FRESHNESS", "receipt base binding mismatch")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False and receipt["verdict"] == "accepted", "T01-ARTIFACTS", "receipt worker-state semantics mismatch")
    require(receipt["support_state"] == "provisional_worker_selftest" and receipt["selftest_status"] == "passed", "T01-ARTIFACTS", "receipt does not report a provisional passed self-test")
    require(receipt["selftest_result"]["exit_code"] == 0 and isinstance(receipt["selftest_result"]["commands"], list) and receipt["selftest_result"]["commands"], "T01-ARTIFACTS", "receipt lacks exact successful self-test commands")
    require(receipt["registry_denominator_sha256"] == registry["denominator_sha256"] == REGISTRY_DENOMINATOR, "T02-REGISTRY", "receipt registry binding mismatch")
    require(receipt["canonical_obligation_ids"] == ids, "T02-REGISTRY", "receipt obligation IDs mismatch")
    require(receipt["composition_certificates"] == bundle["composition_certificates"], "T04-COMPOSITION", "receipt composition certificates mismatch")
    require(receipt["lean_output_sha256"] == lean_sha256, "T04-COMPOSITION", "receipt Lean output digest mismatch")
    require(receipt["audit_complete"] is receipt["theorem_complete"] is False, "T04-COMPOSITION", "receipt overclaims terminal completion")
    require(receipt["first_failed_gate"] is None and receipt["retry_condition"] == "Master integration must commit these exact bytes, accept the predecessor in DAG order, replay the unchanged HEAD validator, independently review the semantic phase predicate, and issue the master phase receipt.", "T01-ARTIFACTS", "receipt master boundary mismatch")
    require(isinstance(receipt["known_failures"], list) and receipt["known_failures"], "T01-ARTIFACTS", "receipt does not expose remaining proof debt")
    require(receipt["invalidation_inputs"] and receipt["status_boundary"], "G09-FRESHNESS", "receipt lacks invalidation or status boundary")
    inputs = receipt["inputs"]
    require(isinstance(inputs, dict) and set(inputs) == {"authorities", "phase_dependencies", "dependency_context", "selected_artifacts", "validation_inputs"}, "T01-ARTIFACTS", "receipt inputs are not complete")
    for section in ("authorities", "phase_dependencies"):
        for binding in inputs[section]:
            assert_receipt_binding(binding)
    for section in ("dependency_context", "validation_inputs"):
        for binding in inputs[section]:
            assert_receipt_binding(binding, allow_worktree=not is_head_tracked(binding["path"]))
    selected = {row["role"]: row for row in inputs["selected_artifacts"]}
    require(set(selected) == {"obligation_registry", "typed_graph_bundle", "readable_tree", "composition_source", "phase_receipt"}, "T01-ARTIFACTS", "receipt selected-role binding is incomplete")
    for role, binding in selected.items():
        path = ROOT / binding["path"]
        require(path.is_file() and not path.is_symlink(), "T01-ARTIFACTS", f"selected role {role} is missing")
        if role == "phase_receipt":
            require(binding["sha256"] == "scheduler_recomputed_after_integration" and binding["git_blob"] == "scheduler_recomputed_after_integration", "T01-ARTIFACTS", "self-referential receipt binding is not explicitly delegated")
        else:
            require(binding["sha256"] == sha256(path), "T01-ARTIFACTS", f"selected role {role} SHA-256 mismatch")
            expected_blob = command_output("git", "hash-object", str(path))
            require(binding["git_blob"] == expected_blob, "T01-ARTIFACTS", f"selected role {role} prospective Git blob mismatch")
    require(receipt["artifact_binding_boundary"] == "All non-self roles bind exact worker bytes by path, SHA-256, and prospective Git blob. The phase receipt cannot contain its own digest; its selected role uses an explicit scheduler-recomputed sentinel, and the master role map must replace it with the committed HEAD SHA-256 and Git blob before acceptance.", "T01-ARTIFACTS", "receipt self-binding boundary is unclear")
    assert_receipt_worker_packet(receipt)


def semantic_result(*, passed: bool, gate: str | None, message: str, stale: list[str] | None = None) -> dict:
    value = {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "obligation_tree",
        "status": "passed" if passed else ("stale" if stale else "failed"),
        "verdict": "phase_accepted" if passed else "repair_required",
        "phase_accepted": passed,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": passed,
        "first_failed_gate": gate,
        "open_obligations": 0 if passed else 1,
        "stale_inputs": stale or [],
        "blocked": False,
        "message": message,
    }
    require(set(value) == REQUIRED_SEMANTIC_FIELDS, "T01-ARTIFACTS", "internal semantic result schema mismatch")
    return value


def validate() -> tuple[dict, str]:
    assert_authorities()
    assert_contract_and_target()
    assert_preflight_structure()
    assert_dependency_ledger()
    registry = load(HERE / "obligation-registry.json")
    bundle = load(HERE / "typed-graphs.json")
    ids, digest = assert_registry(registry)
    assert_graphs(bundle, registry, ids, digest)
    assert_hygiene()
    _lean_output, lean_sha256 = run_lean()
    receipt = load(HERE / "obligation-tree-receipt.json")
    assert_receipt(receipt, registry, bundle, ids, lean_sha256)
    return semantic_result(
        passed=True,
        gate=None,
        message="T01-T04 and G01/G02/G08/G09 passed: 32 status-independent obligations, seven typed graphs, 192 typed edges, audited empty dependency context, substantive leaf ledgers, and three exact conditional Lean composition certificates are ready for independent master review; the theorem's mathematical proof obligations and all terminal completion flags remain open.",
    ), lean_sha256


def main() -> int:
    try:
        result, _ = validate()
    except GateFailure as exc:
        result = semantic_result(passed=False, gate=exc.gate, message=exc.message, stale=exc.stale)
    except Exception as exc:  # Fail closed without contaminating the one-object stdout protocol.
        result = semantic_result(passed=False, gate="VALIDATOR-INTERNAL", message=f"unexpected validator failure: {type(exc).__name__}: {exc}")
    sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
