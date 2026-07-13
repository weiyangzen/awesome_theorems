#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0061 obligation freeze."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0061-OBLIGATION_TREE"
THEOREM = "THM-M-0061"
ROOT_ID = "M0061-ROOT"
BASE_REVISION = "0d2c3bdcd192266bc255ac3d5186da604517145a"
BASE_TREE = "eafbcb48efd51d9cda34f0fc1afe780434abad64"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_OUTPUT_SHA256 = "1c91b97ef22691e06589ac6affbe209c9a3b4da637898d897a30e265c04574fd"
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
EXPECTED_REACHABLE = {
    "M0061-ROOT", "M0061-T-FINITE-SCOPE", "M0061-A-LAGRANGE",
    "M0061-L-CARD-PRODUCT", "M0061-L-NATCARD-PROD",
    "M0061-L-NATCARD-CONGR", "M0061-C-COSET-PRODUCT-EQUIV",
    "M0061-C-FIBER-DECOMPOSITION", "M0061-T-FIBER-TO-COSET",
    "M0061-C-LEFT-COSET-EQUIV", "M0061-T-SIGMA-PRODUCT",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


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
    for name, value in zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1093
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0061-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 20
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        excluded = row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required"
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    denominator = hashlib.sha256(json.dumps([{field: row[field] for field in fields} for row in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for eligibility, key in (("machine_eligibility", "required_machine"), ("human_source_eligibility", "required_human_source"), ("readable_eligibility", "required_readable")):
        assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[eligibility] == "required"]
    assert all(record["status"].endswith("pending_independent_approval") for record in registry["layer_exclusions"].values())
    assert set(registry["proof_body_aliases"]) == {"AddSubgroup.card_addSubgroup_dvd_card", "Subgroup.card_eq_card_quotient_mul_card_subgroup", "Fintype.card_subgroup_dvd_card_encoding"}

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert {"premises", "inference", "source_anchors", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
        assert node["semantic_step_ledger"]["source_anchors"]
        assert node["public_readable_target"].startswith(f"Stage1_Instances/{THEOREM}/obligation-tree.md#")
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]
        if node["machine_debt"].startswith("M0-"):
            assert node["evidence_ids"], f"M0 node lacks evidence: {node['obligation_id']}"

    assert bundle["root_node_id"] == ROOT_ID
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
    assert reachable == EXPECTED_REACHABLE

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
    required_recipe_fields = {"recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy", "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations", "coverage_boundary"}
    for recipe in recipes:
        assert set(recipe) == required_recipe_fields
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        identifier = recipe["recipe_id"].removeprefix("VAL-")
        node = next(node for node in nodes if node["obligation_id"] == identifier)
        assert node["validation_spec_id"] == recipe["recipe_id"]
        if identifier in registry["status_observed_after_freeze"]["interface_checked_obligations"]:
            assert recipe["covered_obligation_ids"] == [identifier]
            assert recipe["coverage_boundary"] == "exact checked interface coverage"
        else:
            assert recipe["covered_obligation_ids"] == []
            assert "no M0 or proof-closure credit" in recipe["coverage_boundary"]

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["accepted_receipt_ids"] == []

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b")
    assert forbidden.search(without_comments) is None
    for marker in ("cosetProduct_of_fiber_engines", "cardProduct_of_engines", "divisibility_of_cardProduct", "finiteScope_of_arbitraryGroup", "root_of_finiteScope", "#print axioms cosetProduct_of_fiber_engines", "Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget"):
        assert marker in source

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert output("git", "rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=mathlib) == ""
    card = mathlib / "Mathlib/GroupTheory/Coset/Card.lean"
    basic = mathlib / "Mathlib/GroupTheory/Coset/Basic.lean"
    finite = mathlib / "Mathlib/SetTheory/Cardinal/Finite.lean"
    assert sha256(card) == "cb3efb11057211d161637ba7e6c75d64271faa95e5bdafff96f82168329b236e"
    assert sha256(basic) == "82a0bd5bdb5d5d0ee0f3378efbcd38109926384399473c97e202e6f40239d8e6"
    assert sha256(finite) == "8de62ef138473b4c4b77917aa453f67b8e203cfb1d2e2c6cb6ebbabf62a9356f"
    for marker in ("theorem card_eq_card_quotient_mul_card_subgroup", "rw [← Nat.card_prod]; exact Nat.card_congr Subgroup.groupEquivQuotientProdSubgroup", "theorem card_subgroup_dvd_card", "classical simp [card_eq_card_quotient_mul_card_subgroup s, @dvd_mul_left ℕ]"):
        assert marker in card.read_text(encoding="utf-8"), marker
    for marker in ("noncomputable def groupEquivQuotientProdSubgroup", "Equiv.sigmaFiberEquiv QuotientGroup.mk", "Equiv.sigmaCongrRight", "leftCosetEquivSubgroup", "Equiv.sigmaEquivProd"):
        assert marker in basic.read_text(encoding="utf-8"), marker

    lean_root = ROOT / "Formalizations/Lean"
    with tempfile.TemporaryDirectory(prefix="stage1-thm-m-0061-obligation-") as temporary:
        statement = subprocess.run(
            [
                "lake", "env", "lean", "--root=../..",
                "../../Stage1_Instances/THM-M-0061/Statement.lean",
                "-o", str(Path(temporary) / "Statement.olean"),
            ],
            cwd=lean_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement.returncode:
            raise AssertionError(statement.stdout)
        pinned_lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=lean_root)
        env = os.environ.copy()
        env["LEAN_PATH"] = f"{temporary}:{pinned_lean_path}"
        obligation = subprocess.run(
            [
                "lake", "env", "lean", "--root=../..",
                "../../Stage1_Instances/THM-M-0061/ObligationTree.lean",
            ],
            cwd=lean_root,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if obligation.returncode:
            raise AssertionError(obligation.stdout)
        normalized = re.sub(r"\s+", " ", obligation.stdout)
        assert normalized.count("propext, Classical.choice, Quot.sound") == 5
        assert "sorry" not in obligation.stdout
        assert hashlib.sha256(obligation.stdout.encode()).hexdigest() == LEAN_OUTPUT_SHA256
        for declaration in {
            declaration
            for recipe in recipes
            for declaration in recipe["covered_declarations"]
        }:
            assert declaration in obligation.stdout, declaration

    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    for identifier in ids:
        assert f"## {identifier.lower()}" in readable

    receipt_path = HERE / "obligation-tree-receipt.json"
    if receipt_path.exists():
        receipt = load("obligation-tree-receipt.json")
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["canonical_obligation_ids"] == ids
        assert set(receipt["graph_names"]) == GRAPH_NAMES
        assert set(receipt["composition_declarations"]) == set(boundary["composition_certificates"])
        assert set(receipt["provisionally_checked_interfaces"]) == set(bundle["closure_boundary"]["interface_checked_obligations"])
        assert set(receipt["candidate_only_obligations"]) == set(bundle["closure_boundary"]["candidate_only_obligations"])
        assert receipt["typed_graph_changes"].startswith(f"Added {len(edge_ids)} directed edges")
        assert f"freezes {len(ids)} semantic obligations" in readable
        assert "frozen `M0061-A-LAGRANGE` node and authoritative root remain `M3`" in readable
        validation_text = (HERE / "obligation-tree-validation.md").read_text(encoding="utf-8")
        assert f"freezes {len(ids)} obligations and {len(edge_ids)} directed typed edges" in validation_text
        assert "frozen anchor node remains `M3`" in validation_text
        changed = set()
        status = subprocess.check_output(
            [
                "git", "status", "--porcelain=v1", "--untracked-files=all", "--",
                f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
            ],
            cwd=ROOT,
            text=True,
        ).rstrip("\n")
        for line in status.splitlines():
            changed.add(line[3:])
        assert changed == set(receipt["changed_paths"])
        assert all(command["exit_code"] == 0 for command in receipt["validation"]["commands"])
        assert receipt["source_revisions"]["Mathlib.GroupTheory.Coset.Card_sha256"] == sha256(card)
        assert receipt["source_revisions"]["Mathlib.GroupTheory.Coset.Basic_sha256"] == sha256(basic)
        assert receipt["source_revisions"]["Mathlib.SetTheory.Cardinal.Finite_sha256"] == sha256(finite)
        assert receipt["accepted_closed_obligations"] == []
        assert receipt["root_vector_after"] == instance["root_vector"]
        assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
        assert receipt["audit_complete"] is receipt["theorem_complete"] is False

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        selftest = json.loads(selftest_path.read_text(encoding="utf-8"))
        assert set(selftest) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
        assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
        assert selftest["base_revision"] == BASE_REVISION
        assert selftest["known_failures"] == receipt["known_failures"]
        assert selftest["changed_paths"] == receipt["changed_paths"]
        assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")

    print(f"PASS THM-M-0061 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); exact pinned anchor remains the proof-phase cut")


if __name__ == "__main__":
    main()
