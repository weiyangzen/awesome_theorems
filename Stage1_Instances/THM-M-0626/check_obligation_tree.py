#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0626 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0626-OBLIGATION_TREE"
THEOREM = "THM-M-0626"
ROOT_ID = "M0626-ROOT"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
}
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
TASK_IDS = (
    "S56-M-0626-INTAKE", "S56-M-0626-STATEMENT", "S56-M-0626-ANCHOR_AUDIT",
    "S56-M-0626-OBLIGATION_TREE", "S56-M-0626-PROOF",
    "S56-M-0626-VALIDATION", "S56-M-0626-RELEASE",
)
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
EXPECTED_REACHABLE = {
    "M0626-ROOT", "M0626-T-ASSEMBLE", "M0626-S-GLOBAL-LOCAL",
    "M0626-A-ISCONNECTED-IMAGE",
}
BASE_REVISION = "0c019b7194c9c43fa5f683fa82d637a0b275410d"


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
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())

    expected = build_obligation_artifacts.build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM

    target_manifest = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
    target = next(row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1320 and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1320
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0626-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == "Freeze the obligation registry and typed proof/provenance/workflow graphs."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == hashlib.sha256(
        (HERE / "Statement.lean").read_bytes()
    ).hexdigest()
    assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256(
        (HERE / "anchor-audit.json").read_bytes()
    ).hexdigest()
    assert registry["obligations"][0]["statement_fingerprint"] == (
        "lean-expression-sha256:5c32b45abf131975cd4673ca095ca1a8e0122e4104bf616a4afab09a03289231"
    )
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 22
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    allowed_kinds = {
        "root", "definition", "normalization", "reduction", "branch", "construction",
        "bridge", "core_lemma", "computation", "certificate", "transport", "terminal",
    }
    for row in rows:
        assert row["kind"] in allowed_kinds
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
        )
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]
    assert next(row for row in rows if row["obligation_id"] == "M0626-N-SEPARATION-GOAL")["kind"] == "reduction"
    assert next(row for row in rows if row["obligation_id"] == "M0626-S-BOUNDARY")["kind"] == "definition"

    field_order = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in field_order} for row in rows]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for eligibility, key in (
        ("machine_eligibility", "required_machine"),
        ("human_source_eligibility", "required_human_source"),
        ("readable_eligibility", "required_readable"),
    ):
        assert registry["frozen_denominators"][key] == [
            row["obligation_id"] for row in rows if row[eligibility] == "required"
        ]
    assert all(
        record["status"].endswith("pending_independent_approval")
        for record in registry["layer_exclusions"].values()
    )
    assert registry["layer_applicability"]["B_branch"]["status"] == (
        "not_applicable_pending_independent_approval"
    )
    aliases = registry["proof_body_aliases"]
    assert any("formal-conjectures" in key for key in aliases)
    assert "conditional_reconstruction" in aliases[
        "Stage1Instances.THM_M_0626.ObligationTree.localConnectedImage_of_components"
    ]

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"] <= 100
        assert len({entry["step_id"] for entry in ledger}) == len(ledger)
        for entry in ledger:
            assert set(entry) == {
                "step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"
            }
            assert entry["step_id"].startswith(node["obligation_id"] + "-STEP-")
            assert isinstance(entry["premise_ids"], list) and entry["premise_ids"]
            assert all(
                premise.startswith(("P-", "OUT-M0626-"))
                for premise in entry["premise_ids"]
            )
            for field in ("step_id", "inference", "source_locator", "output", "outgoing_use"):
                assert isinstance(entry[field], str) and entry[field]
        assert node["public_readable_target"].startswith(
            f"Stage1_Instances/{THEOREM}/obligation-tree.md#"
        )
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]
    candidate = next(node for node in nodes if node["obligation_id"] == "M0626-A-ISCONNECTED-IMAGE")
    assert candidate["machine_debt"] == "M3"
    assert candidate["machine_candidate_status"] == (
        "M0-W_candidate_pending_proof_phase_and_master_acceptance"
    )
    assert all(not node["machine_debt"].startswith("M0") for node in nodes)
    for node in nodes:
        if node["obligation_id"] in bundle["closure_boundary"]["interface_checked_obligations"]:
            assert node["machine_debt"] == "M3"
            assert node["machine_candidate_status"] == (
                "M0-L_worker_checked_interface_pending_master_acceptance"
            )
    assert all(recipe["covered_declarations"] == [] for recipe in specs["recipes"])

    assert bundle["root_node_id"] == ROOT_ID
    assert bundle["edge_endpoint_namespace"] == (
        "canonical obligation_id except workflow, which uses authoritative task IDs"
    )
    assert [entry["task_id"] for entry in bundle["workflow_task_nodes"]] == list(TASK_IDS)
    links = {(entry["task_id"], entry["obligation_id"], entry["role"])
             for entry in bundle["task_obligation_links"]}
    assert len(links) == len(bundle["task_obligation_links"])
    assert {(task_id, obligation_id) for task_id, obligation_id, _ in links} == {
        (task_id, node["obligation_id"]) for node in nodes for task_id in node["task_ids"]
    }
    assert all(entry["role"] for entry in bundle["task_obligation_links"])
    assert all(set(node["task_ids"]) <= set(TASK_IDS) for node in nodes)
    premise_ids = {
        premise
        for node in nodes for entry in node["semantic_step_ledger"]
        for premise in entry["premise_ids"] if premise.startswith("P-")
    }
    assert set(bundle["premise_registry"]) == premise_ids
    for premise_id, record in bundle["premise_registry"].items():
        assert premise_id.startswith("P-")
        assert record["owning_obligation_id"] in ids
        assert record["claim_or_context"] and record["source_locator"]
    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    for graph_name, graph in bundle["graphs"].items():
        endpoints = set(TASK_IDS) if graph_name == "workflow" else set(ids)
        assert set(graph["out"]) == endpoints == set(graph["in"])
        directional = []
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids
            assert edge["type"] in ALLOWED_EDGES
            assert edge["from"] in endpoints and edge["to"] in endpoints
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
    assert reachable == EXPECTED_REACHABLE
    assert all(
        edge["type"] != "logical_decomposition"
        for edge in bundle["graphs"]["refinement"]["edges"]
    )

    authoritative_tasks = [row for row in execution["items"] if row["theorem_id"] == THEOREM]
    authoritative_by_id = {row["id"]: row for row in authoritative_tasks}
    assert set(authoritative_by_id) == set(TASK_IDS)
    for snapshot in bundle["workflow_task_nodes"]:
        authoritative = authoritative_by_id[snapshot["task_id"]]
        assert snapshot["phase"] == authoritative["phase"]
        assert snapshot["layer"] == authoritative["layer"]
        assert snapshot["state_at_freeze"] == authoritative["state"]
        assert snapshot["depends_on"] == authoritative["depends_on"]
    workflow_edges = bundle["graphs"]["workflow"]["edges"]
    assert {(edge["from"], edge["to"]) for edge in workflow_edges} == {
        (task_id, dependency)
        for task_id, row in authoritative_by_id.items() for dependency in row["depends_on"]
    }

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {
        recipe["recipe_id"] for recipe in recipes
    }
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
    assert boundary["unchecked_composition_parents"] == []
    assert set(boundary["checked_composition_parents"]) == {
        "M0626-ROOT", "M0626-T-ASSEMBLE",
        "M0626-T-LOCAL-COMPOSE", "M0626-L-IMAGE-PRECONNECTED", "M0626-N-SEPARATION-GOAL",
    }
    assert boundary["minimal_open_root_cut_set"] == ["M0626-A-ISCONNECTED-IMAGE"]
    assert len(boundary["composition_certificates"]) == len(
        boundary["checked_composition_parents"]
    ) == 5
    assert "localAnchor_of_bodyComposition" not in boundary["composition_certificates"]
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["source_revisions"]["authoritative_blueprint_sha256"] == hashlib.sha256(
        (ROOT / "Docs/Stage1_Blueprint_rev-5.6.md").read_bytes()
    ).hexdigest()
    assert instance["source_revisions"]["execution_dag_sha256"] == hashlib.sha256(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_bytes()
    ).hexdigest()
    assert instance["accepted_receipt_ids"] == []
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b"
    )
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert forbidden.search(without_comments) is None
    for marker in (
        "separationEngine_of_components",
        "imagePreconnected_of_separationEngine",
        "localConnectedImage_of_components",
        "localAnchor_of_bodyComposition",
        "exactAssembly_of_packages",
        "root_of_exactAssembly",
        "#print axioms separationEngine_of_components",
        "#print axioms root_of_exactAssembly",
        "Stage1Instances.THM_M_0626.ConnectedImageTarget",
    ):
        assert marker in source

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    basic = mathlib / "Mathlib/Topology/Connected/Basic.lean"
    assert hashlib.sha256(basic.read_bytes()).hexdigest() == (
        "929f0e1c789b8c0ed10c3164aa174e369b9b250317c525a8ad2f2dcca2a65e9c"
    )
    basic_text = basic.read_text(encoding="utf-8")
    for marker in (
        "def IsPreconnected (s : Set \u03b1) : Prop",
        "def IsConnected (s : Set \u03b1) : Prop",
        "protected theorem IsPreconnected.image",
        "continuousOn_iff'.1 hf u hu",
        "rw [image_subset_iff, preimage_union] at huv",
        "obtain \u27e8z, hz\u27e9 : (s \u2229 (u' \u2229 v')).Nonempty",
        "protected theorem IsConnected.image",
        "image_nonempty.mpr H.nonempty",
    ):
        assert marker in basic_text, marker

    receipt_path = HERE / "obligation-tree-receipt.json"
    assert receipt_path.is_file(), "missing required worker receipt"
    receipt = load("obligation-tree-receipt.json")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids)
    assert receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    for name, expected_hash in receipt["artifact_sha256"].items():
        assert re.fullmatch(r"[0-9a-f]{64}", expected_hash), name
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected_hash

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    assert selftest_path.is_file(), "missing required root worker self-test"
    selftest = json.loads(selftest_path.read_text(encoding="utf-8"))
    assert set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == BASE_REVISION
    assert selftest["known_failures"] == receipt["known_failures"]
    assert selftest["changed_paths"] == receipt["changed_paths"]
    assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")
    assert hashlib.sha256(selftest_path.read_bytes()).hexdigest() == receipt["root_selftest_sha256"]

    print(f"PASS THM-M-0626 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); exact pinned anchor remains the proof-phase cut")


if __name__ == "__main__":
    main()
