#!/usr/bin/env python3
"""Fail-closed structural validator for the THM-M-0034 obligation freeze."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0034-OBLIGATION_TREE"
THEOREM = "THM-M-0034"
ROOT_ID = "M0034-ROOT"
BASE_REVISION = "2bfb272c83b2089e9b285d48dce2c30616ff6c36"
BASE_TREE = "f44853226ddecdf2a2b462fd6c85e770bbffbaa3"
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
REGISTRY_FIELDS = {"obligation_id", "statement_fingerprint", "kind", "root_relevant",
                   "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                   "risk_class", "exclusion_reason", "terminal_proof_body_id"}
NODE_FIELDS = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
               "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
               "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
               "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
               "task_ids", "owned_sources", "owner", "reviewer", "validity"}
ALLOWED_EDGES = {"proof_requires", "composes", "logical_decomposition", "source_map",
                 "expository_decomposition", "equivalent_to", "transports", "evidence_for",
                 "provenance_of", "documents", "trusts", "workflow_depends_on"}
REGISTRY_KINDS = {"root", "definition", "reduction", "branch", "construction", "lemma",
                  "computation", "transport", "terminal"}
NODE_KINDS = {"root", "definition", "normalization", "reduction", "branch", "construction",
              "bridge", "core_lemma", "computation", "certificate", "transport", "terminal"}


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
    receipt = load("obligation-tree-receipt.json")
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8"))

    expected_registry, expected_bundle, expected_specs, expected_readable = build_obligation_artifacts.build()
    for name, value in (("obligation-registry.json", expected_registry),
                        ("typed-graphs.json", expected_bundle),
                        ("validation-specs.json", expected_specs)):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"
    assert (HERE / "obligation-tree.md").read_text(encoding="utf-8") == expected_readable

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["execution_rank"] == 1078 and item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0034-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    assert registry["selected_external_revision"] == "e8d85a6f6fa210ba0be12bd02aa22009699f0c35"
    assert registry["selected_external_archive_sha256"] == "6072221d080e634f0a9775518855557fce0495cf4004848e4cb57dda4aa7e6d2"
    exact = next(row for row in anchor["candidates"] if row["candidate_id"] == "M0034-C02-EDMUND-EXACT")
    assert exact["revision"] == registry["selected_external_revision"]
    assert exact["archive_sha256"] == registry["selected_external_archive_sha256"]
    assert exact["candidate_classification"] == "M3_exact_formal_source_anchor" and exact["evidence_level"] == "E3"
    assert exact["license"].startswith("unknown")
    assert anchor["audit_result"]["root_machine_debt_accepted_after"] == "M3"

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 41 and ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        assert row["kind"] in REGISTRY_KINDS
        excluded = row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required"
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert row["exclusion_reason"].endswith("pending_independent_approval")
    projection = [{field: row[field] for field in (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
        "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
        "terminal_proof_body_id")} for row in rows]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for eligibility, key in (("machine_eligibility", "required_machine"),
                             ("human_source_eligibility", "required_human_source"),
                             ("readable_eligibility", "required_readable")):
        assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[eligibility] == "required"]
    assert registry["append_only_delta"] == []
    assert all(row["status"].endswith("pending_independent_approval") for row in registry["layer_exclusions"].values())
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    node_by_id = {node["obligation_id"]: node for node in nodes}
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["kind"] in NODE_KINDS
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert isinstance(node["step_budget"], int) and 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert {"premises", "inference", "output", "outgoing_use", "steps"} <= ledger.keys()
        assert isinstance(ledger["steps"], list) and ledger["steps"]
        for step in ledger["steps"]:
            assert set(step) == {"step_id", "premise_ids", "inference_or_boundary", "output_claim", "outgoing_use_ids"}
            assert step["step_id"] and step["premise_ids"] and step["inference_or_boundary"]
            assert step["output_claim"] and step["outgoing_use_ids"]
        anchor_name = node["public_readable_target"].rsplit("#", 1)[1]
        assert f'id="{anchor_name}"' in readable
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]
    assert node_by_id[ROOT_ID]["machine_debt"] == "M3"
    assert node_by_id["M0034-X-EXTERNAL-BODY"]["machine_debt"] == "M3"
    assert all(node_by_id[item]["machine_debt"] == "M3" for item in (
        "M0034-S-EXTERNAL-TRANSPORT", "M0034-T-ADAPTER", "M0034-T-ROOT"))

    assert bundle["root_node_id"] == ROOT_ID and set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    for graph in bundle["graphs"].values():
        assert set(graph["out"]) == set(ids) == set(graph["in"])
        directional = []
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids and edge["type"] in ALLOWED_EDGES
            assert edge["from"] in ids and edge["to"] in ids
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            edge_ids.add(edge["edge_id"])
            if edge["type"] != "composes":
                directional.append(edge)
        check_acyclic(directional)
    assert len(edge_ids) == bundle["typed_edge_count"] == 57
    assert all(edge["type"] == "expository_decomposition"
               for edge in bundle["graphs"]["refinement"]["edges"])

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
    assert reachable == set(bundle["metrics_projection"]["proof_reachable_ids"]) == {
        "M0034-ROOT", "M0034-T-ROOT", "M0034-T-ADAPTER", "M0034-X-EXTERNAL-BODY"}
    assert bundle["metrics_projection"]["accepted_numerator_ids"] == []

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
    for recipe in recipes:
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert len(recipe["covered_obligation_ids"]) == 1 and recipe["closure_credit"] is False

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert "M0034-X-EXTERNAL-BODY" in boundary["remaining_root_cut_set"]

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    stripped = re.sub(r"/-.*?-/|--.*", "", source, flags=re.DOTALL)
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b", stripped)
    for marker in ("def ExternalFieldCandidate : Prop", "def ExternalPIDCandidate : Prop",
                   "def AdaptedPositiveCandidate : Prop", "externalFieldCandidate_implies_target",
                   "externalFieldCandidate_implies_adapted", "externalPIDCandidate_implies_target",
                   "terminalTarget_of_adapted", "root_of_terminalTarget",
                   "#print axioms root_of_terminalTarget"):
        assert marker in source

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if len(sys.argv) > 1 and sys.argv[1] == "--worker-packet":
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["known_failures"] == receipt["known_failures"]

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files
    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    print(f"PASS THM-M-0034 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); external body remains absent and unaccepted")


if __name__ == "__main__":
    main()
