#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-0471 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0471-OBLIGATION_TREE"
THEOREM = "THM-M-0471"
ROOT_ID = "M0471-ROOT"
BASE_REVISION = "5fe11f4b5e32a06ffb4432460319fc8ae906fe7b"
BASE_TREE = "64c5aacf7cf3eb79008f5a1970151e3e53cb9966"
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
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "expository_decomposition",
    "equivalent_to", "transports", "source_map", "provenance_of", "evidence_for",
    "trusts", "documents", "workflow_depends_on",
}
PACKET_FILES = {
    "ObligationTree.lean",
    "build_obligation_artifacts.py",
    "check_obligation_tree.py",
    "obligation-registry.json",
    "typed-graphs.json",
    "validation-specs.json",
    "obligation-tree.md",
    "obligation-tree-validation.md",
    "obligation-tree-receipt.json",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


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
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1353
    assert item["phase"] == "obligation_tree" and item["layer"] == 3 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0471-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    prerequisite = next(row for row in execution["items"] if row["id"] == item["depends_on"][0])
    assert prerequisite["state"] == "[_]"
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert registry["frozen_against_statement_sha256"] == (
        "775b86743247571a1a5e5e7f1aa099683f26368e4dd7bee9e23a0b2a2ddbc715"
    )
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 22
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
        )
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]

    field_order = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{key: row[key] for key in field_order} for row in rows]
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
        "M0471-ROOT", "M0471-T-ROOT-COMPOSE", "M0471-T-ASSEMBLE", "M0471-C-WITNESS",
        "M0471-L-NONEMPTY", "M0471-S-BOUNDARY", "M0471-L-PRIMALITY",
        "M0471-L-PRODUCT", "M0471-N-NONZERO", "M0471-L-UNIQUENESS",
        "M0471-L-PERM-PRODUCT", "M0471-L-PRIME-DVD-PRODUCT",
        "M0471-L-MEM-PRIME-DIVISOR", "M0471-C-ERASE-PERM", "M0471-N-CANCEL-HEAD",
    }

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
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
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque|implemented_by|extern|native_decide)\b"
    )
    assert forbidden.search(source) is None
    for marker in (
        "(factors : PrimeFactorWitness)", "(nonempty : WitnessNonempty factors)",
        "(primality : WitnessPrimality factors)", "(product : WitnessProduct factors)",
        "(uniqueness : PrimeFactorUniqueness factors)",
        "(anchor : ExactPrimeListAnchor)", "#print axioms exactPrimeListAnchor_of_packages",
        "#print axioms root_of_exactPrimeListAnchor",
    ):
        assert marker in source

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    factors = mathlib / "Mathlib/Data/Nat/Factors.lean"
    list_prime = mathlib / "Mathlib/Data/List/Prime.lean"
    assert sha256(factors) == "3e64e2c8ba907c05209966a7bba8754cf2ab33f328a3010667ffe58c95e0bca3"
    assert sha256(list_prime) == "148cf3e70ddc39591270dd3c4d9da733a91ff574e8f5c1bd6fd8fd2f42e33591"
    factors_text = factors.read_text(encoding="utf-8")
    list_text = list_prime.read_text(encoding="utf-8")
    for marker in (
        "def primeFactorsList", "theorem prime_of_mem_primeFactorsList",
        "theorem prod_primeFactorsList", "theorem primeFactorsList_ne_nil",
        "theorem primeFactorsList_unique", "refine perm_of_prod_eq_prod",
    ):
        assert marker in factors_text
    for marker in (
        "theorem Prime.dvd_prod_iff", "theorem mem_list_primes_of_dvd_prod",
        "theorem perm_of_prod_eq_prod", "perm_cons_erase", "mul_right_inj'",
    ):
        assert marker in list_text

    receipt = load("obligation-tree-receipt.json")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert set(receipt["graph_names"]) == GRAPH_NAMES
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == set(receipt["changed_paths"])
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
        assert set(selftest) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
        assert selftest["base_revision"] == BASE_REVISION
        assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")
        assert actual_changes == set(selftest["changed_paths"])
        assert selftest["known_failures"] == receipt["known_failures"]

    expected_files = set(instance["owned_artifacts"])
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert PACKET_FILES <= actual_files
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

    print(f"PASS {THEOREM} obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); exact pinned factorization family remains the proof-phase cut")


if __name__ == "__main__":
    main()
