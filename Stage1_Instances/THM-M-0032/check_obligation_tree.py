#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0032 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0032-OBLIGATION_TREE"
THEOREM = "THM-M-0032"
ROOT_ID = "M0032-ROOT"
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
REGISTRY_FIELDS = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
}
NODE_FIELDS = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
    "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
    "reviewer", "validity",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def check_acyclic(edges: list[dict]) -> None:
    adjacency: dict[str, list[str]] = {}
    for edge in edges:
        adjacency.setdefault(edge["from"], []).append(edge["to"])
    active: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        assert node not in active, f"cycle at {node}"
        if node in done:
            return
        active.add(node)
        for child in adjacency.get(node, []):
            visit(child)
        active.remove(node)
        done.add(node)

    for node in adjacency:
        visit(node)


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    instance = load("instance.json")
    task_dag = load("task-dag.json")
    anchor = load("anchor-audit.json")
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())

    expected = build_obligation_artifacts.build()
    for name, value in zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1076
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0032-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    assert anchor["audit_result"]["exact_placeholder_free_candidate_located"] is False
    assert anchor["audit_result"]["root_machine_debt_after"] == "M3"

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 38
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        excluded = row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required"
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert row["exclusion_reason"].endswith("pending_independent_approval")
    projection = [{field: row[field] for field in (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )} for row in rows]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for field, key in (
        ("machine_eligibility", "required_machine"),
        ("human_source_eligibility", "required_human_source"),
        ("readable_eligibility", "required_readable"),
    ):
        assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == "required"]
    assert registry["rejected_architecture_aliases"]["all_nonzero_primes_principal"].startswith("rejected_as_too_strong")
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    node_by_obligation = {node["obligation_id"]: node for node in nodes}
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
        assert node["public_readable_target"].startswith(f"Stage1_Instances/{THEOREM}/obligation-tree.md#")
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]
    assert node_by_obligation[ROOT_ID]["machine_debt"] == "M3"
    assert node_by_obligation["M0032-N-DOMAIN"]["machine_debt"] == "M4"
    assert node_by_obligation["M0032-A-PRIME-ELEMENT"]["machine_debt"] == "M4"
    assert node_by_obligation["M0032-X-KAPLANSKY"]["machine_debt"] == "M0-W"
    assert node_by_obligation["M0032-T-ASSEMBLE"]["machine_debt"] == "M0-L"

    assert bundle["root_node_id"] == ROOT_ID
    assert bundle["edge_endpoint_namespace"] == "canonical obligation_id"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    for graph in bundle["graphs"].values():
        assert set(graph["out"]) == set(ids) == set(graph["in"])
        directional = []
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids
            assert edge["type"] in ALLOWED_EDGES
            assert edge["from"] in ids and edge["to"] in ids
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            edge_ids.add(edge["edge_id"])
            if edge["type"] != "composes":
                directional.append(edge)
        check_acyclic(directional)

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for edge in proof.values():
        reciprocal = proof[edge["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == edge["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
        assert {edge["type"], reciprocal["type"]} == {"proof_requires", "composes"}
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()

    def reach(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            reach(child)

    reach(ROOT_ID)
    assert reachable == {
        row["obligation_id"] for row in rows
        if row["machine_eligibility"] == "required" and not row["obligation_id"].startswith("M0032-S-")
    }

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
    required_recipe_fields = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    }
    for recipe in recipes:
        assert set(recipe) == required_recipe_fields
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert len(recipe["covered_obligation_ids"]) == 1

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["accepted_receipt_ids"] == []
    assert {"M0032-N-DOMAIN", "M0032-A-PRIME-ELEMENT"} <= set(boundary["remaining_root_cut_set"])

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b")
    assert forbidden.search(without_comments) is None
    for marker in (
        "def RegularLocalDomainPackage : Prop",
        "def RegularLocalPrimeElementPackage : Prop",
        "def KaplanskyCriterionPackage : Prop",
        "pinnedKaplanskyCriterionPackage",
        "root_of_domain_primeElement_and_kaplansky",
        "letI : IsDomain R := domain R",
        "exact kaplansky R (primeElement R)",
        "#print axioms root_of_domain_primeElement_and_kaplansky",
        "Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget",
    ):
        assert marker in source, marker

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    kaplansky = mathlib / "Mathlib/RingTheory/UniqueFactorizationDomain/Kaplansky.lean"
    assert hashlib.sha256(kaplansky.read_bytes()).hexdigest() == "1ce495be94eba57eeac5e8d114b0ad548cd6266c8351abbd54138b426e9e40a6"
    kaplansky_text = kaplansky.read_text(encoding="utf-8")
    assert "public theorem iff_exists_prime_mem_of_isPrime" in kaplansky_text
    assert "UniqueFactorizationMonoid R ↔ ∀ I ≠ (⊥ : Ideal R), I.IsPrime → ∃ x ∈ I, Prime x" in kaplansky_text
    assert "fun H ↦ of_exists_prime_mem_of_isPrime H" in kaplansky_text

    receipt = load("obligation-tree-receipt.json")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False

    selftest = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
    assert set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"
    }
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == receipt["base_revision"]
    assert selftest["known_failures"] == receipt["known_failures"]
    assert selftest["changed_paths"] == receipt["changed_paths"]
    assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")

    print(f"PASS THM-M-0032 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); domain and prime-element packages remain the machine cut")


if __name__ == "__main__":
    main()
