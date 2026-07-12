#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0025 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0025-OBLIGATION_TREE"
THEOREM = "THM-M-0025"
ROOT_ID = "M0025-ROOT"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow",
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
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())

    expected = build_obligation_artifacts.build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1070
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] == "[ ]", "worker must not modify authoritative DAG state"
    assert item["depends_on"] == ["S56-M-0025-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == hashlib.sha256(
        (HERE / "Statement.lean").read_bytes()
    ).hexdigest()
    assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256(
        (HERE / "anchor-audit.json").read_bytes()
    ).hexdigest()
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 26
    assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        excluded = row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required"
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]
    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in fields} for row in rows]
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
        value["status"].endswith("pending_independent_approval")
        for value in registry["layer_exclusions"].values()
    )
    aliases = registry["proof_body_aliases"]
    assert set(aliases.values()) == {"deduplicated_to:Polynomial.isNoetherianRing"}

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
        assert node["public_readable_target"].startswith(f"Stage1_Instances/{THEOREM}/obligation-tree.md#")
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]

    assert bundle["edge_endpoint_namespace"] == "canonical obligation_id"
    assert set(bundle["graphs"]) == GRAPH_NAMES
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
    required_proof = set(build_obligation_artifacts.REQUIRES)
    required_proof.update(
        child for values in build_obligation_artifacts.REQUIRES.values() for child in values
    )
    assert reachable == required_proof
    refinement = bundle["graphs"]["refinement"]["edges"]
    body_pairs = {
        (edge["from"], edge["to"])
        for edge in refinement if edge["type"] == "logical_decomposition"
    }
    expected_body_pairs = {
        (parent, child)
        for parent, values in build_obligation_artifacts.BODY_DECOMPOSITION.items()
        for child in values
    }
    assert expected_body_pairs <= body_pairs
    architecture_children = {parent: list(values) for parent, values in children.items()}
    for parent, child in body_pairs:
        architecture_children.setdefault(parent, []).append(child)
    architecture_reachable: set[str] = set()

    def reach_architecture(node: str) -> None:
        if node in architecture_reachable:
            return
        architecture_reachable.add(node)
        for child in architecture_children.get(node, []):
            reach_architecture(child)

    reach_architecture(ROOT_ID)
    assert required_proof | {
        parent for parent, _ in expected_body_pairs
    } | {
        child for _, child in expected_body_pairs
    } <= architecture_reachable

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {
        recipe["recipe_id"] for recipe in recipes
    }
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert len(recipe["covered_obligation_ids"]) == 1
        assert recipe["coverage_semantics"] == "architecture_validation_only"
        assert recipe["closure_credit"] is False

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["accepted_receipt_ids"] == []
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    forbidden = ("sorry", "admit", "sorryAx", "axiom ", "unsafe ", "implemented_by", "native_decide")
    assert all(token not in source for token in forbidden)
    for marker in (
        "(anchor : ExactPolynomialAnchor", "(idealFG : EveryPolynomialIdealFG",
        "root_of_exactPolynomialAnchor", "#print axioms root_of_exactPolynomialAnchor",
    ):
        assert marker in source

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    basic = mathlib / "Mathlib/RingTheory/Polynomial/Basic.lean"
    assert hashlib.sha256(basic.read_bytes()).hexdigest() == "7cedafd3e1fc910b152c699375e8670f0db7d6261d7ebdd3dd8ff2420fda5b9c"
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD:Mathlib/RingTheory/Polynomial/Basic.lean"],
        cwd=mathlib, text=True,
    ).strip() == "1ae18244a4534f336f1d9280a1f5f8fd1a5acd9f"
    basic_text = basic.read_text(encoding="utf-8")
    for marker in (
        "protected theorem Polynomial.isNoetherianRing",
        "inst.wf.min (Set.range I.leadingCoeffNth)",
        "let ⟨s, hs⟩ := I.is_fg_degreeLE N",
        "induction k using Nat.strong_induction_on",
        "rw [I.mem_leadingCoeffNth] at this",
        "have := Polynomial.degree_sub_lt h1 hp0 h2",
    ):
        assert marker in basic_text, marker
    body_start = basic_text.index("protected theorem Polynomial.isNoetherianRing")
    body_end = basic_text.index("attribute [instance] Polynomial.isNoetherianRing")
    terminal_body = basic_text[body_start:body_end]
    prohibited = re.compile(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|extern|opaque)\b")
    assert prohibited.search(terminal_body) is None

    receipt = load("obligation-tree-receipt.json")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert set(receipt["graph_names"]) == GRAPH_NAMES
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["support_state"] == "worker_self_tested_pending_master_acceptance"
    assert receipt["validation"]["commands"]
    assert receipt["validation"]["output_summary"].startswith("All node-scoped")
    assert "PENDING_SELFTEST" not in (HERE / "obligation-tree-receipt.json").read_text()

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.is_file():
        selftest = json.loads(selftest_path.read_text(encoding="utf-8"))
        assert set(selftest) == {
            "item_id", "changed_paths", "commands", "output_summary", "base_revision",
            "known_failures", "state",
        }
        assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
        assert selftest["base_revision"] == receipt["base_revision"]
        assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")
        status = subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
        )
        actual_changes = {
            line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == set(selftest["changed_paths"])

    required_artifacts = {
        "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
        "obligation-registry.json", "typed-graphs.json", "validation-specs.json",
        "obligation-tree.md", "obligation-tree-validation.md", "obligation-tree-receipt.json",
    }
    assert required_artifacts <= set(instance["owned_artifacts"])
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "obligation-tree.md", "obligation-tree-validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print(f"PASS THM-M-0025 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R3); exact pinned anchor remains the proof-phase cut")


if __name__ == "__main__":
    main()
