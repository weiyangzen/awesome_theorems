#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0474 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0474-OBLIGATION_TREE"
THEOREM = "THM-M-0474"
ROOT_ID = "M0474-ROOT"
GRAPH_NAMES = {
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
}
REGISTRY_FIELDS = {
    "obligation_id",
    "statement_fingerprint",
    "kind",
    "root_relevant",
    "machine_eligibility",
    "human_source_eligibility",
    "readable_eligibility",
    "risk_class",
    "exclusion_reason",
    "terminal_proof_body_id",
}
NODE_FIELDS = {
    "node_id",
    "obligation_id",
    "kind",
    "human_statement",
    "formal_target",
    "output",
    "human_debt",
    "machine_debt",
    "readability_debt",
    "evidence_ids",
    "source_crosswalk_id",
    "provenance_id",
    "foundation_profile",
    "tcb_profile",
    "computation_record",
    "step_budget",
    "semantic_step_ledger",
    "public_readable_target",
    "validation_spec_id",
    "status_boundary",
    "task_ids",
    "owned_sources",
    "owner",
    "reviewer",
    "validity",
}
ALLOWED_EDGES = {
    "proof_requires",
    "composes",
    "logical_decomposition",
    "source_map",
    "provenance_of",
    "evidence_for",
    "trusts",
    "documents",
    "workflow_depends_on",
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
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 938
    assert item["phase"] == "obligation_tree" and item["layer"] == 3 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0474-ANCHOR_AUDIT"]
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
    assert len(ids) == len(set(ids)) == 21
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        excluded = row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required"
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]

    field_order = (
        "obligation_id",
        "statement_fingerprint",
        "kind",
        "root_relevant",
        "machine_eligibility",
        "human_source_eligibility",
        "readable_eligibility",
        "risk_class",
        "exclusion_reason",
        "terminal_proof_body_id",
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

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids)
    assert len({node["node_id"] for node in nodes}) == len(nodes)
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

    assert bundle["root_node_id"] == ROOT_ID
    assert bundle["edge_endpoint_namespace"] == "canonical obligation_id"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
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
    required_proof = {
        "M0474-ROOT",
        "M0474-T-COMPOSE",
        "M0474-L-NAT",
        "M0474-N-NAT-INT",
        "M0474-N-COPRIME",
        "M0474-L-INT",
        "M0474-C-ZMOD-NONZERO",
        "M0474-T-INT-ZMOD",
        "M0474-L-ZMOD",
        "M0474-T-ZMOD-CARD",
        "M0474-L-FINITE-FIELD",
        "M0474-C-UNIT",
        "M0474-L-GROUP-CARD",
    }
    assert reachable == required_proof

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

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["accepted_receipt_ids"] == []
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    forbidden = ("sorry", "admit", "sorryAx", "axiom ", "unsafe ", "implemented_by", "native_decide")
    assert all(token not in source for token in forbidden)
    assert "root_of_exactNatAnchor" in source and "(anchor : ExactNatAnchor)" in source
    assert "exact anchor" in source and "#print axioms root_of_exactNatAnchor" in source

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    basic = mathlib / "Mathlib/FieldTheory/Finite/Basic.lean"
    order = mathlib / "Mathlib/GroupTheory/OrderOfElement.lean"
    assert hashlib.sha256(basic.read_bytes()).hexdigest() == (
        "808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44"
    )
    assert hashlib.sha256(order.read_bytes()).hexdigest() == (
        "42bef2580b87cd0fa6367cd2d57d30fb25fce373576a856cc84d27dad23fae23"
    )
    basic_text = basic.read_text(encoding="utf-8")
    order_text = order.read_text(encoding="utf-8")
    for marker in (
        "theorem Nat.ModEq.pow_card_sub_one_eq_one",
        "rw [← Int.natCast_modEq_iff, Nat.cast_pow, Nat.cast_one]",
        "exact Int.ModEq.pow_card_sub_one_eq_one hp (isCoprime_iff_coprime.mpr hpn)",
        "theorem Int.ModEq.pow_card_sub_one_eq_one",
        "simpa [← ZMod.intCast_eq_intCast_iff] using ZMod.pow_card_sub_one_eq_one this",
        "theorem pow_card_sub_one_eq_one {a : ZMod p}",
        "have h := FiniteField.pow_card_sub_one_eq_one a ha",
        "theorem pow_card_sub_one_eq_one (a : K)",
        "rw [← Fintype.card_units, pow_card_eq_one]",
    ):
        assert marker in basic_text, marker
    for marker in (
        "theorem orderOf_dvd_card",
        "theorem pow_card_eq_one'",
        "theorem pow_card_eq_one : x ^ Fintype.card G = 1 := by",
    ):
        assert marker in order_text, marker
    visible_chain = basic_text + order_text
    prohibited_mathlib = re.compile(
        r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|extern|opaque)\b"
    )
    assert prohibited_mathlib.search(visible_chain) is None

    receipt = load("obligation-tree-receipt.json")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids)
    assert receipt["typed_edge_count"] == len(edge_ids)
    assert set(receipt["graph_names"]) == GRAPH_NAMES
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["support_state"] == "worker_self_tested_pending_master_acceptance"
    assert receipt["validation"]["commands"]
    assert receipt["validation"]["output_summary"].startswith("All node-scoped")
    assert not any(
        "PENDING_SELFTEST" in (HERE / name).read_text(encoding="utf-8")
        for name in ("obligation-tree-receipt.json", "obligation-tree-validation.md")
    )

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.is_file():
        selftest = json.loads(selftest_path.read_text(encoding="utf-8"))
        assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
        assert selftest["base_revision"] == receipt["base_revision"]
        assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")
        assert set(selftest) == {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }
        status = __import__("subprocess").check_output(
            ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
        )
        actual_changes = {
            line[3:]
            for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == set(selftest["changed_paths"])

    expected_files = set(instance["owned_artifacts"])
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert expected_files == actual_files
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

    print(f"PASS THM-M-0474 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); exact pinned anchor remains the proof-phase cut")


if __name__ == "__main__":
    main()
