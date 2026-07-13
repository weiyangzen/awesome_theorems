#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0043 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0043-OBLIGATION_TREE"
THEOREM = "THM-M-0043"
ROOT_ID = "M0043-ROOT"
BASE_REVISION = "7d0965498598e684e3e3d0a01836c2bf36a02959"
BASE_TREE = "753e16a89fce09f051af066f8b58d3e6b2722ade"
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
ALLOWED_EDGES = {"proof_requires", "composes", "logical_decomposition", "source_map", "transports", "provenance_of", "evidence_for", "trusts", "documents", "expository_decomposition", "workflow_depends_on"}
REGISTRY_FIELDS = {"obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id"}
NODE_FIELDS = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
EXPECTED_CHANGED = {
    ".stage1-worker-selftest.json",
    *{f"Stage1_Instances/{THEOREM}/{name}" for name in (
        "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
        "obligation-registry.json", "typed-graphs.json", "validation-specs.json",
        "obligation-tree.md", "obligation-tree-validation.md", "obligation-tree-receipt.json",
        "instance.json",
    )},
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
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
    anchor = load("anchor-audit.json")
    receipt = load("obligation-tree-receipt.json")
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())

    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"),
        build_obligation_artifacts.build(),
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1083
    assert item["phase"] == "obligation_tree" and item["layer"] == 3 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0043-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == BASE_REVISION
    assert subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip() == BASE_TREE

    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 33
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        excluded = row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required"
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]
    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    projection = [{field: row[field] for field in fields} for row in rows]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for eligibility, key in (("machine_eligibility", "required_machine"), ("human_source_eligibility", "required_human_source"), ("readable_eligibility", "required_readable")):
        assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[eligibility] == "required"]
    assert all(record["status"].endswith("pending_independent_approval") for record in registry["layer_exclusions"].values())
    assert registry["append_only_delta"] == [] and registry["proof_body_aliases"]

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
    assert len({node["node_id"] for node in nodes}) == len(nodes)
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
        anchor_name = node["public_readable_target"].rsplit("#", 1)[1]
        assert f'id="{anchor_name}"' in readable
        assert node["validation_spec_id"] and node["owner"] and node["reviewer"]
        assert node["validity"]["review_due"] and node["validity"]["invalidation_inputs"]

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
    assert reachable == set(bundle["metrics_projection"]["proof_reachable_ids"])
    assert set(bundle["metrics_projection"]["unique_semantic_leaf_ids"]) == {node for node in reachable if node not in children}
    assert bundle["metrics_projection"]["accepted_numerator_ids"] == []
    assert bundle["metrics_projection"]["denominator_ids"] == ids
    assert bundle["metrics_projection"]["alias_and_presentation_nodes_receive_credit"] is False

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
    for recipe in recipes:
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert len(recipe["covered_obligation_ids"]) == 1

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["accepted_receipt_ids"] == []
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"

    audit_result = anchor["audit_result"]
    assert audit_result["root_machine_candidate_after"] == "M1"
    assert audit_result["accepted_root_machine_debt_after"] == "M3"
    atlas = next(row for row in anchor["candidates"] if row["candidate_id"] == "M0043-C01-ATLAS-EXACT")
    assert atlas["revision"] == "34ffed396f376454c1a9b297f3fd74c5c801fb50"
    assert atlas["file_sha256"] == "415d4e7784f21d5cf7327a4c6bee96bb3e3ac3e2d7ae18587738785a18b72cc9"
    assert atlas["candidate_classification"] == "M1" and atlas["evidence_level"] == "E2"
    assert "license" in atlas and "license/reuse" in atlas["integration_task"]

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    stripped = re.sub(r"/-.*?-/|--.*", "", source, flags=re.DOTALL)
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide)\b", stripped)
    assert "(anchor : ExactConjugatedDiagonalAnchor" in source
    assert "root_of_exactConjugatedDiagonalAnchor" in source and "#print axioms" in source

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert set(receipt["graph_names"]) == GRAPH_NAMES
    assert set(receipt["changed_paths"]) == EXPECTED_CHANGED
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["validation"]["commands"] and receipt["known_failures"]

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.is_file():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == EXPECTED_CHANGED
        assert packet["known_failures"] == receipt["known_failures"]

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files
    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("obligation-tree.md", "obligation-tree-validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print(f"PASS THM-M-0043 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); external Atlas M1 route remains uninstalled")


if __name__ == "__main__":
    main()
