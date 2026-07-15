#!/usr/bin/env python3
"""Fail-closed structural and optional Lean validation for THM-M-0841 obligations."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0841-OBLIGATION_TREE"
THEOREM = "THM-M-0841"
ROOT_ID = "M0841-ROOT"
RANK = 1398
BASE_REVISION = "c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb"
BASE_TREE = "d8ea21a05ed52ff43d984128352a07f479aae6e6"
STATEMENT_SHA256 = "897dcc398df34c0dd6ad02dc2092a08f46a6cafc908c2e9f8497a895aa66663d"
ANCHOR_SHA256 = "10275b8946fb134c2788e7104f39c1cf0dbeb6e28bbf293303846726a4f0cc4b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
    "proof_requires", "composes", "logical_decomposition", "source_map", "transports",
    "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on",
}
CHECKED_DECLARATIONS = {
    "denseFamily_compose", "sparse_compose", "compose_root", "exactRoot_iff_canonical",
    "root_of_terminal",
}
EXPECTED_LEAN_SHA256 = "2ec4662b366bc15dfb956ae890cbdc68d19f64dbbf13ddbea6647b606b7ae962"
EXPECTED_CHANGED = [".stage1-worker-selftest.json"] + [
    f"Stage1_Instances/{THEOREM}/{name}" for name in (
        "ObligationTree.lean",
        "README.md",
        "build_obligation_artifacts.py",
        "check_obligation_tree.py",
        "instance.json",
        "obligation-registry.json",
        "obligation-tree-receipt.json",
        "obligation-tree-validation.md",
        "obligation-tree.md",
        "task-dag.json",
        "typed-graphs.json",
        "validation-specs.json",
    )
]


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        args, cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def check_acyclic(edges: list[dict]) -> None:
    adjacency: dict[str, list[str]] = {}
    for edge in edges:
        adjacency.setdefault(edge["from"], []).append(edge["to"])
    active: set[str] = set()
    complete: set[str] = set()

    def visit(node: str) -> None:
        assert node not in active, f"cycle at {node}"
        if node in complete:
            return
        active.add(node)
        for child in adjacency.get(node, []):
            visit(child)
        active.remove(node)
        complete.add(node)

    for node in adjacency:
        visit(node)


def run_lean() -> str:
    lean_bin = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0841-obligation-") as temporary:
        temp = Path(temporary)
        env = {
            **os.environ,
            "LEAN_PATH": lean_path,
            "LC_ALL": "C",
            "LANG": "C",
            "NO_COLOR": "1",
        }
        statement = subprocess.run(
            [lean_bin, "--trust=0", "-o", str(temp / "Statement.olean"), str(HERE / "Statement.lean")],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        obligation = subprocess.run(
            [lean_bin, "--trust=0", str(HERE / "ObligationTree.lean")],
            cwd=ROOT,
            env={**env, "LEAN_PATH": f"{temp}:{lean_path}"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if obligation.returncode:
            sys.stdout.write(obligation.stdout)
            raise SystemExit(obligation.returncode)
    assert obligation.stdout.count("Declarations are sorry-free!") == 1
    assert "sorryAx" not in obligation.stdout
    normalized = re.sub(r"\s+", " ", obligation.stdout)
    assert normalized.count("propext, Classical.choice, Quot.sound") == 5
    expected_types = {
        "denseFamily_compose": "(base : DenseBase) (step : DenseStep) : DenseFamily",
        "sparse_compose": "(transport : SparseFromDense) (dense : DenseFamily) : ExactRoot",
        "compose_root": "(base : DenseBase) (step : DenseStep) (transport : SparseFromDense) : ExactRoot",
        "exactRoot_iff_canonical": ": ExactRoot ↔ ErdosStoneTarget",
        "root_of_terminal": "(terminal : ExactRoot) : ExactRoot",
    }
    for name, signature in expected_types.items():
        assert f"THM_M_0841_Obligations.{name} {signature}" in normalized
    for name in CHECKED_DECLARATIONS:
        assert f"THM_M_0841_Obligations.{name}" in obligation.stdout
    return obligation.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-lean", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    registry = load(HERE / "obligation-registry.json")
    bundle = load(HERE / "typed-graphs.json")
    specs = load(HERE / "validation-specs.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    receipt = load(HERE / "obligation-tree-receipt.json")

    expected_registry, expected_bundle, expected_specs, expected_markdown = (
        build_obligation_artifacts.build()
    )
    for name, value in (
        ("obligation-registry.json", expected_registry),
        ("typed-graphs.json", expected_bundle),
        ("validation-specs.json", expected_specs),
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"
    assert (HERE / "obligation-tree.md").read_text(encoding="utf-8") == expected_markdown

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == RANK
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": RANK,
        "phase": "obligation_tree",
        "layer": 3,
        "state": "[ ]",
        "depends_on": ["S56-M-0841-ANCHOR_AUDIT"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == item["depends_on"][0])
    assert predecessor["state"] in {"[_]", "[x]"}
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_task["evidence_ids"] == []
    assert task_dag["accepted_states"] == []

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "anchor-audit.json") == ANCHOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == len(build_obligation_artifacts.SPECS) == 53
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(set(row) == REGISTRY_FIELDS for row in rows)
    allowed_kinds = {
        "root", "definition", "normalization", "reduction", "branch", "construction",
        "bridge", "core_lemma", "computation", "certificate", "transport", "terminal",
    }
    for row in rows:
        assert row["kind"] in allowed_kinds
        assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] in {"required", "not_applicable"}
        excluded = any(
            row[field] != "required"
            for field in ("machine_eligibility", "human_source_eligibility", "readable_eligibility")
        )
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert set(row["exclusion_reason"]) == {"code", "justification", "approval"}
            assert "pending independent" in row["exclusion_reason"]["approval"]
    fields = tuple(registry["canonical_projection_fields"])
    assert set(fields) == REGISTRY_FIELDS
    projection = [{field: row[field] for field in fields} for row in rows]
    denominator = build_obligation_artifacts.digest(projection)
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
    assert registry["registry_id"] == "THM-M-0841-OBLIGATIONS-v2"
    assert registry["registry_version"] == 2
    assert registry["append_only_delta"] == [{
        "from_registry_id": "THM-M-0841-OBLIGATIONS-v1",
        "from_denominator_sha256": "f7e5b07b6580e7933e3e2f0cc320eb120080fafa9ca442737ed0c5beaa29fd56",
        "from_inventory_count": 53,
        "to_registry_id": "THM-M-0841-OBLIGATIONS-v2",
        "to_denominator_sha256": denominator,
        "to_inventory_count": len(ids),
        "added_obligation_ids": [],
        "removed_obligation_ids": [],
        "changed_existing_obligation_ids": ["M0841-T-ROOT-COMPOSE"],
        "changed_obligations": {
            "M0841-T-ROOT-COMPOSE": {
                "old_statement_fingerprint": "planned:v1:sha256:1fe56018a4d73c16b86bf409c1fa8d2382942c57fd5cab52bdab00ec86cb0d31",
                "new_statement_fingerprint": "planned:v1:sha256:4adf60927a01a35061ab932b9ff1d074bf4c5c9e6dacaebd36bd701d4292d8f3",
                "old_formal_target": "Stage1Instances.THM_M_0841_Obligations.compose_root",
                "new_formal_target": "Stage1Instances.THM_M_0841_Obligations.sparse_compose",
                "old_terminal_proof_body_id": "local:ObligationTree.lean#compose_root",
                "new_terminal_proof_body_id": "local:ObligationTree.lean#sparse_compose",
            },
        },
        "proof_edge_changes": {
            "removed": [
                ["M0841-T-ROOT-COMPOSE", "M0841-B-R-TWO"],
                ["M0841-T-ROOT-COMPOSE", "M0841-B-R-GE-THREE"],
            ],
            "added": [["M0841-T-ROOT-COMPOSE", "M0841-T-DENSE-ASSEMBLE"]],
        },
        "reason": "Repair the root proof spine so the sparse composition consumes the assembled dense family and every required machine obligation is root-reachable.",
        "status_effect": "No obligation closes and accepted H1/M3/R4 remains unchanged.",
    }]
    observed = registry["status_observed_after_freeze"]
    assert observed["candidate_machine_classification"] == "M3_no_exact_proof_candidate"
    assert observed["candidate_closure_credit"] is False
    assert observed["accepted_closed_obligations"] == []
    assert observed["root_machine_debt"] == "M3"
    assert local_task["covered_obligation_ids"] == ids
    assert local_task["validation_spec_ids"] == [
        build_obligation_artifacts.STRUCTURE_RECIPE,
        build_obligation_artifacts.LEAN_RECIPE,
    ]
    assert local_task["provisional_worker_state"] == "[_]"
    assert local_task["accepted_state"] == "open"
    assert "all mathematical obligations" in local_task["status_boundary"]

    nodes = bundle["nodes"]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    assert len(nodes) == len(node_by_id) == len(ids) and set(node_by_id) == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    for node in nodes:
        assert set(node) == NODE_FIELDS
        assert node["node_id"] == f"{THEOREM}-{node['obligation_id'].removeprefix('M0841-')}"
        assert node["human_debt"] == "H1" and node["machine_debt"] in {"M3", "M4"}
        assert node["readability_debt"] == "R4" and node["evidence_ids"] == []
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"]
        for step in ledger:
            assert set(step) == {
                "step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use",
            }
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            step_ids.add(step["step_id"])
        path, anchor = node["public_readable_target"].split("#", 1)
        assert path == f"Stage1_Instances/{THEOREM}/obligation-tree.md"
        assert f"### {anchor}" in readable
        assert node["task_ids"] == [ITEM]
        assert node["validity"]["revocation_state"] == "not-accepted"
        assert all(not source.startswith("Formalizations/Lean/.lake") for source in node["owned_sources"])
    for node in nodes:
        for step in node["semantic_step_ledger"]:
            assert set(step["premise_ids"]) <= id_set | step_ids | {"frozen-formal-context"}

    assert bundle["root_node_id"] == ROOT_ID
    assert set(bundle["graphs"]) == GRAPH_NAMES
    workflow_nodes = set(bundle["workflow_task_nodes"])
    edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        endpoints = workflow_nodes if name == "workflow" else id_set
        assert set(graph["out"]) == endpoints == set(graph["in"])
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids
            assert edge["type"] in ALLOWED_EDGES
            assert edge["from"] in endpoints and edge["to"] in endpoints
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            if name == "workflow":
                assert edge["type"] == "workflow_depends_on"
            else:
                assert edge["type"] != "workflow_depends_on"
            edge_ids.add(edge["edge_id"])
        if name != "proof":
            check_acyclic(graph["edges"])

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    reverse_types: dict[tuple[str, str], str] = {}
    for edge in proof.values():
        assert edge["type"] in {"proof_requires", "composes", "logical_decomposition"}
        reverse = proof[edge["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == edge["edge_id"]
        assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
        assert "proof_requires" in {edge["type"], reverse["type"]}
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
            reverse_types[(edge["from"], edge["to"])] = reverse["type"]
    check_acyclic([edge for edge in proof.values() if edge["type"] == "proof_requires"])
    assert children[ROOT_ID] == ["M0841-T-ROOT-COMPOSE"]
    assert children["M0841-T-ROOT-COMPOSE"] == [
        "M0841-T-DENSE-ASSEMBLE", "M0841-S-COMPLEMENT-TRANSPORT",
    ]
    assert children["M0841-T-DENSE-ASSEMBLE"] == [
        "M0841-B-R-TWO", "M0841-B-R-GE-THREE",
    ]
    refinement_children: dict[str, list[str]] = {}
    for edge in bundle["graphs"]["refinement"]["edges"]:
        if edge["type"] in {"logical_decomposition", "transports"}:
            refinement_children.setdefault(edge["from"], []).append(edge["to"])

    closure_reachable: set[str] = set()

    def reach_closure(identifier: str) -> None:
        if identifier in closure_reachable:
            return
        closure_reachable.add(identifier)
        for child in children.get(identifier, []):
            reach_closure(child)
        for child in refinement_children.get(identifier, []):
            reach_closure(child)

    reach_closure(ROOT_ID)
    required_machine = set(registry["frozen_denominators"]["required_machine"])
    assert required_machine == closure_reachable, (
        f"root closure reachability mismatch; missing={sorted(required_machine - closure_reachable)}, "
        f"unexpected={sorted(closure_reachable - required_machine)}"
    )

    obligation_by_id = {row["obligation_id"]: row for row in rows}
    certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
    assert set(certificates) == set(build_obligation_artifacts.CHECKED_PARENTS)
    for parent, certificate in certificates.items():
        assert certificate["required_child_ids"] == children.get(parent, [])
        assert certificate["parent_statement_fingerprint"] == obligation_by_id[parent]["statement_fingerprint"]
        assert certificate["required_child_statement_fingerprints"] == {
            child: obligation_by_id[child]["statement_fingerprint"]
            for child in children.get(parent, [])
        }
        assert certificate["certificate_kind"] == "lean_abstract_child_harness"
        assert certificate["status"] == "provisionally_elaborated_not_accepted"
        assert certificate["introduces_undeclared_premises"] is False
        assert certificate["accepted"] is False
        assert all(reverse_types[(parent, child)] == "composes" for child in children.get(parent, []))
    plans = {row["parent_obligation_id"]: row for row in bundle["unverified_decomposition_plans"]}
    assert set(plans) == set(children) - set(certificates)
    for parent, plan in plans.items():
        assert plan["planned_child_ids"] == children[parent]
        assert plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        assert "exact Lean abstract-child harness" in plan["required_future_certificate"]
        assert all(reverse_types[(parent, child)] == "logical_decomposition" for child in children[parent])

    source_edges = bundle["graphs"]["provenance"]["edges"]
    for row in rows:
        identifier = row["obligation_id"]
        if identifier != "M0841-X-SOURCE" and row["human_source_eligibility"] == "required":
            assert any(
                edge["from"] == identifier
                and edge["type"] == "source_map"
                and edge["to"] == "M0841-X-SOURCE"
                for edge in source_edges
            )
    refinement = bundle["graphs"]["refinement"]["edges"]
    expanded = next(edge for edge in refinement if edge["edge_id"] == "REF-TARGET-EXPANDED")
    assert expanded["type"] == "transports" and expanded["checked_direction"] == "iff"
    assert not any(
        edge["type"] == "transports"
        and {edge["from"], edge["to"]} == {"M0841-S-TARGET", "M0841-N-DENSE-FORM"}
        for edge in refinement
    )

    boundary = bundle["closure_boundary"]
    assert boundary["closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["accepted_root_machine_debt"] == "M3"
    assert boundary["remaining_machine_root_cut_set"] == [
        "M0841-B-R-TWO", "M0841-B-R-GE-THREE", "M0841-S-COMPLEMENT-TRANSPORT",
    ]
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["source_revisions"]["authoritative_blueprint_sha256"] == sha256(
        ROOT / "Docs/Stage1_Blueprint_rev-5.6.md"
    )
    assert instance["source_revisions"]["execution_dag_sha256"] == sha256(
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    )
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    recipes = specs["recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {
        build_obligation_artifacts.STRUCTURE_RECIPE,
        build_obligation_artifacts.LEAN_RECIPE,
    }
    for recipe in recipes:
        assert recipe["cwd"] == "." and isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["timeout_seconds"] > 0 and recipe["coverage_boundary"]
        assert set(recipe["covered_obligation_ids"]) <= id_set
    structural = next(recipe for recipe in recipes if recipe["recipe_id"] == build_obligation_artifacts.STRUCTURE_RECIPE)
    assert set(structural["covered_obligation_ids"]) == id_set
    lean_recipe = next(recipe for recipe in recipes if recipe["recipe_id"] == build_obligation_artifacts.LEAN_RECIPE)
    assert {name.rsplit(".", 1)[-1] for name in lean_recipe["covered_declarations"]} >= CHECKED_DECLARATIONS
    embedded_recipes = receipt["structured_validation_recipes"]
    assert [row["recipe_id"] for row in embedded_recipes] == [
        row["recipe_id"] for row in recipes
    ]
    for embedded, recipe in zip(embedded_recipes, recipes, strict=True):
        assert embedded["cwd"] == recipe["cwd"]
        assert embedded["argv"] == recipe["argv"]
        assert embedded["timeout_seconds"] == recipe["timeout_seconds"]
        assert embedded["network_policy"] == recipe["network_policy"]
        assert embedded["expected_exit"] == recipe["expected_exit"]
        assert embedded["covered_obligation_count"] == len(recipe["covered_obligation_ids"])
        assert embedded["covered_declarations"] == recipe["covered_declarations"]
        assert embedded["coverage_boundary"] == recipe["coverage_boundary"]

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    code = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    code = re.sub(r"--.*", "", code)
    code = re.sub(r"^.*(?:assert_no_sorry|#print sorries).*$", "", code, flags=re.MULTILINE)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|extern|native_decide|proof_wanted)\b|"
        r"^\s*(?:axiom|constant|unsafe|opaque)\b",
        re.MULTILINE,
    )
    assert forbidden.search(code) is None
    for name in CHECKED_DECLARATIONS:
        assert f"theorem {name}" in source
        assert f"assert_no_sorry {name}" in source
        assert f"#print axioms {name}" in source
    assert "def DenseClaim" in source and "def SparseFromDense" in source
    assert "(base : DenseBase) (step : DenseStep) (transport : SparseFromDense)" in source

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["validated_at"] == "2026-07-15T19:28:00+08:00"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["registry_id"] == registry["registry_id"]
    assert receipt["registry_version"] == registry["registry_version"]
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["owner"] == "THM-M-0841 proof lane"
    assert "master attestation pending" in receipt["attestor"]
    assert receipt["platform"] == {
        "os_kernel_arch": "Linux 7.0.0-27-generic x86_64",
        "python": "3.14.4",
        "lake": "5.0.0-src+98dc76e",
        "lean": "4.29.0 / x86_64-unknown-linux-gnu / 98dc76e3c0a9b856c9b98726b713fb04fab16740 / Release",
        "lean_executable_sha256": "sha256:3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        "lean_path_sha256": "sha256:3d86ee1798843e92a1c0b9149c1013cf0567281c3b6ea4e2dc5b650354fa70a0",
        "timezone": "Asia/Shanghai",
        "locale": "C during Lean validation",
    }
    lean_bin = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    assert receipt["platform"]["lean_executable_sha256"] == f"sha256:{sha256(Path(lean_bin))}"
    assert receipt["platform"]["lean_path_sha256"] == f"sha256:{sha256_text(output('lake', 'env', 'printenv', 'LEAN_PATH', cwd=LEAN_ROOT))}"
    assert receipt["covered_node_ids"] == [node["node_id"] for node in nodes]
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["content_addressed_receipt_ids"] == []
    assert receipt["worker_input_integrity"]["tracked_base_revision"] == BASE_REVISION
    assert "exact 13-path" in receipt["worker_input_integrity"]["changed_path_manifest_policy"]
    assert "non-self-addressed" in receipt["worker_input_integrity"]["artifact_hash_boundary"]
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["substantive_ledger_step_count"] == len(step_ids)
    assert receipt["canonical_obligation_ids"] == ids
    assert receipt["obligation_statement_fingerprints"] == {
        row["obligation_id"]: row["statement_fingerprint"] for row in rows
    }
    assert receipt["composition_certificate_count"] == len(certificates)
    assert receipt["unverified_decomposition_count"] == len(plans)
    assert receipt["composition_certificates"] == bundle["composition_certificates"]
    assert receipt["lean_output_sha256"] == EXPECTED_LEAN_SHA256
    assert receipt["accepted_closed_obligations"] == receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["changed_paths"] == EXPECTED_CHANGED
    assert receipt["artifact_hashes"] == {
        name: f"sha256:{sha256(HERE / name)}" for name in receipt["artifact_hashes"]
    }
    assert set(receipt["artifact_hashes"]) == {
        Path(path).name for path in EXPECTED_CHANGED
        if path.startswith(f"Stage1_Instances/{THEOREM}/")
        and not path.endswith("obligation-tree-receipt.json")
    }
    assert "excluded" in receipt["artifact_hash_boundary"]
    validation_text = (HERE / "obligation-tree-validation.md").read_text(encoding="utf-8")
    assert f"Registry version {registry['registry_version']} freezes {len(ids)} unique obligations" in validation_text
    assert registry["denominator_sha256"] in validation_text
    assert f"Seven typed graphs contain {len(edge_ids)} edges" in validation_text
    assert f"All {len(required_machine)} required machine obligations are reachable" in validation_text
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM}/{name}" for name in actual_files
    }

    if args.worker_packet:
        packet = load(args.worker_packet)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["commands"] == receipt["commands"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]
        status = output(
            "git", "status", "--porcelain=v1", "--untracked-files=all", "--",
            str(HERE), str(args.worker_packet.resolve()),
        )
        actual_changed = {
            line[3:] if line[:2] == "??" else line[2:].lstrip()
            for line in status.splitlines()
        }
        assert actual_changed == set(EXPECTED_CHANGED)

    for path in [*HERE.iterdir(), ROOT / ".stage1-worker-selftest.json"]:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "obligation-tree.md", "obligation-tree-validation.md", "obligation-tree-receipt.json",
        "obligation-registry.json", "typed-graphs.json", "validation-specs.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print(
        f"PASS {THEOREM} obligation tree: {len(ids)} obligations, "
        f"{len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps"
    )
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); accepted closed obligations: 0")
    if args.run_lean:
        lean_output = run_lean()
        lean_hash = hashlib.sha256(lean_output.encode()).hexdigest()
        assert lean_hash == EXPECTED_LEAN_SHA256
        print(f"Lean conditional composition: pass and no sorryAx; output sha256 {lean_hash}")


if __name__ == "__main__":
    main()
