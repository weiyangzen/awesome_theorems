#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0476 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB = LEAN_ROOT / ".lake/packages/mathlib"
ITEM = "S56-M-0476-OBLIGATION_TREE"
THEOREM = "THM-M-0476"
ROOT_ID = "M0476-ROOT"
BASE_REVISION = "a3b18eec39bf04be025b1641cae02f4d44fdf11a"
BASE_TREE = "fdfff18dea4c6798c5b322b6088dfe556109c134"
ROOT_EXPRESSION = "ee76edb160426d3e8d95b11bfedca7febcfe915f50007e042875c922ebc8a4ac"
STATEMENT_SHA256 = "3903de3f1e1cdd6d2f048917005da8f2b744d6726507d09120661e79d217dff9"
ANCHOR_AUDIT_SHA256 = "5451205a7be624b019b9d8154fb6a42227006606a21578bdccf5bdba6d9eaddf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
}
REGISTRY_FIELDS = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
}
NODE_FIELDS = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
GRAPH_EDGE_TYPES = {
    "proof": {"proof_requires", "composes"},
    "refinement": {"logical_decomposition", "expository_decomposition", "equivalent_to", "transports"},
    "provenance": {"source_map", "provenance_of"},
    "evidence": {"evidence_for"},
    "trust": {"trusts"},
    "documentation": {"documents"},
    "workflow": {"workflow_depends_on"},
}
EXPECTED_SOURCE_HASHES = {
    "Mathlib/NumberTheory/Wilson.lean": "7bd6ec0e909f037f8632e1b495f9647a61fe950f3bfe3af98a5a22914622aeb7",
    "Mathlib/FieldTheory/Finite/Basic.lean": "808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44",
    "Mathlib/Algebra/BigOperators/Group/Finset/Defs.lean": "848a0c9491494de52f3767e43c6c8e4a07445237d2aaf8473a362f84011e85ab",
    "Mathlib/Algebra/BigOperators/Group/Finset/Basic.lean": "ea7bf2258d1d628feaf1e480f173f5015f1cfbdec5234bf475b50cb0922e1fcb",
    "Mathlib/Algebra/BigOperators/Intervals.lean": "bd51b3fd7cda225ba69f192b987085cc7001bb2c806f9a397c6fd59b355c33e3",
    "Mathlib/Algebra/BigOperators/Ring/Finset.lean": "2ed26aa75e75c02914d8a3fdc5ff08a3083937219f4276b6c58f88b1bc9e2674",
    "Mathlib/Algebra/Ring/Commute.lean": "4576787687d058561fb355ac1119091648b341c013329c1ec9c232d8099560c3",
    "Mathlib/Data/ZMod/Basic.lean": "b150e3bf79b154b28c1d3fa68cbd837f093f4305bf4fd2e9302db29081135358",
    "Mathlib/Algebra/GroupWithZero/Units/Basic.lean": "4b750b23a857bef9641ec8020842ece12c64b51ce8d7c31ad51d5fea0757a11f",
    "Mathlib/Algebra/Group/Units/Hom.lean": "41ba97721da86f90acb4f1d21057cfa149cb1c76a3bdf19a06c0df27abac184f",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{name} must contain a JSON object"
    return value


def serialized(value: dict) -> bytes:
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


def task_contract_projection(execution: dict) -> list[dict]:
    fields = (
        "id", "theorem_id", "execution_rank", "phase", "layer", "depends_on",
        "owned_paths", "deliverable", "completion_gate", "children",
    )
    return [
        {field: row[field] for field in fields}
        for row in execution["items"] if row["theorem_id"] == THEOREM
    ]


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    statement = load("statement.json")
    anchor = load("anchor-audit.json")
    anchor_receipt = load("anchor-audit-receipt.json")
    instance = load("instance.json")
    task_dag = load("task-dag.json")
    receipt = load("obligation-tree-receipt.json")
    selftest = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
    targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8"))

    expected = build_obligation_artifacts.build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected
    ):
        assert (HERE / name).read_bytes() == serialized(value), f"stale generated artifact: {name}"

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    dependency = next(
        row for row in execution["items"] if row["id"] == "S56-M-0476-ANCHOR_AUDIT"
    )
    assert target["execution_rank"] == item["execution_rank"] == 1357
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert item["phase"] == "obligation_tree" and item["layer"] == 3 and item["state"] == "[ ]"
    assert item["depends_on"] == [dependency["id"]]
    assert dependency["state"] == "[_]"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []
    assert all(row["state"] == "open" for row in task_dag["tasks"])
    local_by_id = {row["id"]: row for row in task_dag["tasks"]}
    authoritative_by_id = {
        row["id"]: row for row in execution["items"] if row["theorem_id"] == THEOREM
    }
    for task_id, local in local_by_id.items():
        authoritative = authoritative_by_id[task_id]
        assert local["depends_on"] == authoritative["depends_on"]
        assert local["phase"] == authoritative["phase"]
        assert local["layer"] == authoritative["layer"]
        assert local["owned_paths"] == authoritative["owned_paths"]
        assert local["authoritative_state"] in {"[ ]", "[_]"}
        assert local["authoritative_state"] == authoritative["state"]
    assert set(local_by_id) == set(authoritative_by_id) - {"S56-M-0476-INTAKE"}
    assert task_dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert task_dag["lifecycle_mode"] == "planned"
    assert task_dag["accepted_states"] == []

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "anchor-audit.json") == ANCHOR_AUDIT_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_AUDIT_SHA256
    task_projection = task_contract_projection(execution)
    task_contract_hash = hashlib.sha256(
        json.dumps(task_projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert registry["frozen_task_contract_projection"] == task_projection
    assert registry["frozen_task_contract_sha256"] == task_contract_hash
    assert bundle["frozen_task_contract_sha256"] == task_contract_hash
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["canonical_target_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert anchor["inventory_decision"]["candidate_accepted_by_master"] is False
    assert anchor["inventory_decision"]["kernel_closed_as_accepted_root"] is False
    assert anchor["accepted_receipt_ids"] == anchor_receipt["accepted_receipt_ids"] == []
    assert anchor["audit_complete"] is anchor["theorem_complete"] is False

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 26
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        assert row["kind"] in {
            "root", "definition", "reduction", "branch", "construction", "lemma",
            "computation", "transport", "terminal",
        }
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
        )
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]
        assert row["readable_eligibility"] == "required"

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = hashlib.sha256(
        json.dumps(
            [{field: row[field] for field in fields} for row in rows],
            sort_keys=True, separators=(",", ":"),
        ).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert build_obligation_artifacts.compute_registry_hash(registry) == registry[
        "registry_content_sha256"
    ]
    assert registry["frozen_denominators"]["inventory"] == ids
    for eligibility, key in (
        ("machine_eligibility", "required_machine"),
        ("human_source_eligibility", "required_human_source"),
        ("readable_eligibility", "required_readable"),
    ):
        assert registry["frozen_denominators"][key] == [
            row["obligation_id"] for row in rows if row[eligibility] == "required"
        ]
    assert registry["layer_exclusions"]["computation"]["status"].endswith(
        "pending_independent_approval"
    )
    assert all(row["root_relevant"] is True for row in rows)
    assert set(registry["proof_body_aliases"]) == {
        "ZMod.prod_Ico_one_prime", "Nat.prime_iff_fac_equiv_neg_one",
        "Nat.prime_of_fac_equiv_neg_one", "external_Int.ModEq_Wilson",
    }

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    parent_map: dict[str, list[str]] = {}
    for parent_id, child_ids in build_obligation_artifacts.REQUIRES.items():
        for child_id in child_ids:
            parent_map.setdefault(child_id, []).append(parent_id)
    descendants: dict[str, set[str]] = {}

    def collect_descendants(identifier: str) -> set[str]:
        if identifier in descendants:
            return descendants[identifier]
        value: set[str] = set()
        for child_id in build_obligation_artifacts.REQUIRES.get(identifier, []):
            value.add(child_id)
            value.update(collect_descendants(child_id))
        descendants[identifier] = value
        return value

    for identifier in ids:
        collect_descendants(identifier)

    overlay_ids = {
        "M0476-S-INTERFACE", "M0476-S-BOUNDARY", "M0476-S-FOUNDATION",
        "M0476-L-WILSON", "M0476-L-UNITS-PRODUCT",
        "M0476-X-SOURCE", "M0476-X-PROVENANCE", "M0476-X-TRUST",
        "M0476-X-READABLE", "M0476-X-WORKFLOW",
    }
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert not node["machine_debt"].startswith("M0-")
        assert node["evidence_ids"] == []
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert {"premises", "inference", "source_anchors", "output", "outgoing_use", "steps"} <= ledger.keys()
        assert ledger["source_anchors"]
        assert node["step_budget_semantics"] == "split_threshold_only_not_readability_or_leaf_adequacy"
        steps = ledger["steps"]
        assert 0 < len(steps) <= node["step_budget"]
        step_ids = [step["step_id"] for step in steps]
        assert len(step_ids) == len(set(step_ids))
        identifier = node["obligation_id"]
        allowed_obligation_premises = descendants[identifier] | set(
            build_obligation_artifacts.REQUIRES.get(identifier, [])
        ) | {"M0476-S-INTERFACE"}
        if identifier in overlay_ids:
            allowed_obligation_premises |= {"M0476-ROOT", "M0476-L-WILSON", "M0476-L-UNITS-PRODUCT", "M0476-S-FOUNDATION"}
            allowed_obligation_premises |= set(
                build_obligation_artifacts.PROVENANCE_EXPANSIONS.get(identifier, [])
            )
            if identifier == "M0476-L-WILSON":
                allowed_obligation_premises.add("M0476-T-COMPOSE")
        for index, step in enumerate(steps):
            assert {
                "step_id", "premise_ids", "inference_or_source", "output_claim",
                "outgoing_use_ids",
            } <= step.keys()
            assert step["premise_ids"] and step["inference_or_source"]
            assert step["output_claim"] and step["outgoing_use_ids"]
            obligation_premises = set(step["premise_ids"]) & set(ids)
            assert obligation_premises <= allowed_obligation_premises
            assert set(step["premise_ids"]) <= set(ids) | set(step_ids[:index])
            assert not (set(step["premise_ids"]) & set(step_ids[index:]))
            assert set(step["outgoing_use_ids"]) <= (
                set(step_ids[index + 1:]) | set(parent_map.get(identifier, [])) |
                {f"{node['obligation_id']}-PUBLIC-BOUNDARY"}
            )
        referenced = {
            premise for step in steps for premise in step["premise_ids"] if premise in set(ids)
        }
        assert set(build_obligation_artifacts.REQUIRES.get(node["obligation_id"], [])) <= referenced
        assert ledger["premises"] == [
            premise for step in steps for premise in step["premise_ids"]
        ]
        ledger_step_edges = [
            {"from": premise, "to": step["step_id"]}
            for step in steps for premise in step["premise_ids"] if premise in set(step_ids)
        ]
        check_acyclic(ledger_step_edges)
        assert node["public_readable_target"].startswith(
            f"Stage1_Instances/{THEOREM}/obligation-tree.md#"
        )
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]

    assert bundle["root_node_id"] == ROOT_ID
    assert bundle["edge_endpoint_namespace"] == "canonical obligation_id"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    for graph_name, graph in bundle["graphs"].items():
        assert set(graph["out"]) == set(ids) == set(graph["in"])
        directional = []
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids and edge["type"] in ALLOWED_EDGES
            assert edge["type"] in GRAPH_EDGE_TYPES[graph_name]
            assert edge["from"] in ids and edge["to"] in ids
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            edge_ids.add(edge["edge_id"])
            if edge["type"] != "composes":
                directional.append(edge)
        check_acyclic(directional)
    assert set(bundle["graph_endpoint_policy"]) == GRAPH_NAMES
    for graph_name, policy in bundle["graph_endpoint_policy"].items():
        assert set(policy["allowed_types"]) == GRAPH_EDGE_TYPES[graph_name]
        assert policy["endpoint_kind_policy"]
        graph_edges = bundle["graphs"][graph_name]["edges"]
        if "excluded_endpoint_ids" in policy:
            excluded = set(policy["excluded_endpoint_ids"])
            assert all(edge["from"] not in excluded and edge["to"] not in excluded for edge in graph_edges)
        if "allowed_target_ids" in policy:
            assert all(edge["to"] in set(policy["allowed_target_ids"]) for edge in graph_edges)
        if "allowed_source_ids" in policy:
            assert all(edge["from"] in set(policy["allowed_source_ids"]) for edge in graph_edges)
        if policy.get("must_be_empty"):
            assert graph_edges == []
    provenance_edges = bundle["graphs"]["provenance"]["edges"]
    assert set(bundle["graph_endpoint_policy"]["provenance"]["required_source_ids"]) <= {
        edge["from"] for edge in provenance_edges
    }

    workflow_tasks = bundle["workflow_task_graph"]
    assert workflow_tasks["endpoint_namespace"] == "authoritative Stage1 task id"
    assert workflow_tasks["task_contract_sha256"] == task_contract_hash
    assert workflow_tasks["nodes"] == task_projection
    task_ids = {row["id"] for row in task_projection}
    assert set(workflow_tasks["task_obligation_links"]) == task_ids
    assert all(workflow_tasks["task_obligation_links"][task_id] for task_id in task_ids)
    assert set().union(*map(set, workflow_tasks["task_obligation_links"].values())) == set(ids)
    node_tasks = {node["obligation_id"]: node["task_ids"] for node in nodes}
    for task_id, linked_ids in workflow_tasks["task_obligation_links"].items():
        assert linked_ids == [
            identifier for identifier in ids if task_id in node_tasks[identifier]
        ]
    assert {
        (edge["from"], edge["to"]) for edge in workflow_tasks["edges"]
    } == {
        (row["id"], dependency)
        for row in task_projection for dependency in row["depends_on"]
    }
    assert all(
        edge["type"] == "workflow_depends_on"
        and edge["from"] in task_ids and edge["to"] in task_ids
        for edge in workflow_tasks["edges"]
    )
    check_acyclic(workflow_tasks["edges"])

    assert bundle["graphs"]["evidence"]["edges"] == []
    assert bundle["evidence_endpoint_policy"].startswith("Receipts are external typed objects")
    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for edge in proof.values():
        reverse = proof[edge["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == edge["edge_id"]
        assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
        assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
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
    expected_reachable = {
        "M0476-ROOT", "M0476-S-FACT-TRANSPORT",
        "M0476-T-COMPOSE", "M0476-N-FACTORIAL-PRODUCT",
        "M0476-L-FACTORIAL-INTERVAL", "M0476-T-NAT-CAST-PRODUCT",
        "M0476-C-RESIDUE-UNITS-BIJECTION", "M0476-N-PRIME-ENDPOINT",
        "M0476-B-UNIT-VAL-RANGE", "M0476-L-UNIT-VAL-INJECTIVE",
        "M0476-C-RESIDUE-TO-UNIT", "M0476-T-REPRESENTATIVE-COE",
        "M0476-T-UNITS-COE-NEGONE",
        "M0476-T-INSERT-NEGONE", "M0476-C-INVERSE-PAIRING",
        "M0476-L-INVERSE-FIXED-POINTS",
    }
    assert reachable == expected_reachable

    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in rows}
    certificates = {row["parent_id"]: row for row in bundle["composition_certificates"]}
    assert set(certificates) == set(children)
    for parent, child_ids in children.items():
        certificate = certificates[parent]
        assert certificate["required_child_ids"] == child_ids
        assert certificate["parent_statement_fingerprint"] == fingerprints[parent]
        assert certificate["required_child_statement_fingerprints"] == {
            child: fingerprints[child] for child in child_ids
        }
        assert certificate["conditional"] is True and certificate["accepted"] is False
        if certificate["kernel_checked_interface"]:
            assert certificate["status"] == "conditional_kernel_checked"
        else:
            assert certificate["status"] == "planned_source_composition_pending_exact_child_harness"
    assert all(certificate["kernel_checked_interface"] for certificate in certificates.values())
    assert receipt["composition_declarations"] == [
        row["declaration"] for row in bundle["composition_certificates"]
    ]

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{registry['registry_content_sha256']}"
    assert instance["discovery_protocol_hash"] == (
        "sha256:2069bfed989cf0d0f8198d6e0a30a99dd84f0ea3442e5765040ea98f5cdac042"
    )
    assert instance["accepted_receipt_ids"] == []
    assert boundary["remaining_root_cut_set"] == ["M0476-S-FACT-TRANSPORT"]
    # Necessity: removing the sole cut node leaves no root-to-leaf proof path. Sufficiency: every
    # root-to-leaf path starts with this child because the root has exactly one proof requirement.
    assert children[ROOT_ID] == boundary["remaining_root_cut_set"]
    assert boundary["remaining_proof_leaf_frontier"] == build_obligation_artifacts.PROOF_LEAVES
    metrics = bundle["metrics"]
    assert metrics["inventory_classification"]["denominator_ids"] == ids
    assert metrics["inventory_classification"]["numerator_ids"] == ids
    for key in (
        "unique_logical_leaf_closure", "distinct_proof_body_closure",
        "interface_transport_closure", "readable_closure", "human_source_closure",
        "source_boundary_coverage", "critical_path_closure",
    ):
        assert metrics[key]["numerator_ids"] == [] and metrics[key]["denominator_ids"]
    assert metrics["root_closure"] == {"accepted": False, "root_id": ROOT_ID}

    recipes = specs["recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {
        "S56-M-0476-OBLIGATION-TREE-STRUCTURE",
        "S56-M-0476-OBLIGATION-TREE-LEAN",
    }
    assert {node["validation_spec_id"] for node in nodes} == {
        recipe["recipe_id"] for recipe in recipes
    }
    for recipe in recipes:
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["argv"] == [
            "python3", "-B", "Stage1_Instances/THM-M-0476/check_obligation_tree.py"
        ]
        if recipe["recipe_id"].endswith("STRUCTURE"):
            assert recipe["covered_obligation_ids"] == []
            assert "no M0" in recipe["coverage_boundary"]
        else:
            assert recipe["covered_obligation_ids"] == sorted(
                build_obligation_artifacts.CHECKED_INTERFACES
                | set(build_obligation_artifacts.LEAF_DECLARATIONS)
            )
            assert "accepted proof closure remains empty" in recipe["coverage_boundary"]

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b"
    )
    assert forbidden.search(without_comments) is None
    for marker in (
        "factorialProduct_of_identities", "residueUnitsProduct_of_components",
        "primeEndpointIdentity_from_prime", "unitRepresentativeInPrimeRange_from_unit",
        "residueRepresentativeSurjectiveAtEndpoint_from_mk0",
        "unitRepresentativeInjective_from_val",
        "representativeCastAgreement_from_natCast_val",
        "inverseFixedPointClassification_from_units",
        "unitEraseProduct_of_inversion", "unitProductIdentity_of_erase",
        "unitsProductBridge_of_components", "factWilsonAnchor_of_bridges",
        "root_of_factWilsonAnchor", "root_of_composedTarget",
        "#print axioms root_of_composedTarget",
    ):
        assert marker in source

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    for relative, expected_hash in EXPECTED_SOURCE_HASHES.items():
        assert sha256(MATHLIB / relative) == expected_hash, relative
    wilson = (MATHLIB / "Mathlib/NumberTheory/Wilson.lean").read_text(encoding="utf-8")
    finite = (MATHLIB / "Mathlib/FieldTheory/Finite/Basic.lean").read_text(encoding="utf-8")
    for marker in (
        "theorem wilsons_lemma : ((p - 1)! : ZMod p) = -1 := by",
        "Finset.prod_Ico_id_eq_factorial", "prod_natCast", "refine prod_bij",
        "prod_univ_units_id_eq_neg_one",
    ):
        assert marker in wilson
    for marker in (
        "theorem prod_univ_units_id_eq_neg_one", "prod_involution",
        "Units.inv_eq_self_iff", "insert_erase", "prod_insert",
    ):
        assert marker in finite

    lean_evidence = load("lean-elaboration-evidence.json")
    assert lean_evidence["schema_version"] == "stage1-scoped-lean-elaboration/1.0"
    assert lean_evidence["item_id"] == ITEM and lean_evidence["theorem_id"] == THEOREM
    assert lean_evidence["repository_revision"] == BASE_REVISION
    assert lean_evidence["repository_tree"] == BASE_TREE
    assert lean_evidence["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert lean_evidence["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
    assert lean_evidence["lean_toolchain_file_sha256"] == sha256(
        LEAN_ROOT / "lean-toolchain"
    )
    assert lean_evidence["lake_manifest_sha256"] == sha256(LEAN_ROOT / "lake-manifest.json")
    assert lean_evidence["mathlib_revision"] == MATHLIB_REVISION
    assert lean_evidence["mathlib_tree"] == MATHLIB_TREE
    assert lean_evidence["started_at"] <= lean_evidence["ended_at"]
    assert lean_evidence["command"][0:3] == ["lake", "env", "lean"]
    assert lean_evidence["exit_code"] == 0 and lean_evidence["network_policy"] == "denied"
    assert lean_evidence["lake_artifacts_mutated"] is False
    obligation_output = lean_evidence["stdout"]
    assert hashlib.sha256(obligation_output.encode()).hexdigest() == lean_evidence[
        "stdout_sha256"
    ]
    assert receipt["lean_output_sha256"] == lean_evidence["stdout_sha256"]
    assert receipt["lean_input_binding"] == {
        key: lean_evidence[key] for key in (
            "statement_sha256", "obligation_tree_sha256",
            "lean_toolchain_file_sha256", "lake_manifest_sha256",
        )
    }
    normalized = re.sub(r"\s+", " ", obligation_output)
    assert "root_of_composedTarget' depends on axioms: [propext, Quot.sound]" in normalized
    assert "sorry" not in obligation_output
    for declaration in next(
        recipe for recipe in recipes if recipe["recipe_id"].endswith("LEAN")
    )["covered_declarations"]:
        assert f"'{declaration}' depends on axioms:" in obligation_output

    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    for identifier in ids:
        assert f"### {identifier.lower()}" in readable
    assert "/home/" not in readable and ".cron/" not in readable
    assert "theorem_complete=true" not in readable

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "obligation_tree" and receipt["intent"] == "audit"
    assert receipt["proposed_state"] == "[_]" and receipt["verdict"] == "no_state_change"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["obligation_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["remaining_root_cut_set"] == boundary["remaining_root_cut_set"]
    assert receipt["remaining_proof_leaf_frontier"] == boundary[
        "remaining_proof_leaf_frontier"
    ]
    assert receipt["remaining_required_machine_assurance_frontier"] == boundary[
        "remaining_required_machine_assurance_frontier"
    ]
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["registry_content_sha256"] == registry["registry_content_sha256"]
    assert receipt["frozen_task_contract_sha256"] == task_contract_hash
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }
    assert set(selftest) == required_packet_fields
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == BASE_REVISION
    assert selftest["known_failures"] == receipt["known_failures"]
    assert set(selftest["changed_paths"]) == set(receipt["changed_paths"])
    assert selftest["commands"] == receipt["commands"]
    assert selftest["output_summary"] == receipt["output_summary"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    status_paths = {line[3:] for line in status.splitlines() if line}
    assert status_paths == set(receipt["changed_paths"]) | {"Formalizations/Lean/.lake"}

    expected_files = set(instance["owned_artifacts"])
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert expected_files == actual_files
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    for forbidden_public_fragment in ("/home/", ".cron/", "theorem_complete=true"):
        for name in ("README.md", "obligation-tree.md", "obligation-tree-validation.md"):
            assert forbidden_public_fragment not in (HERE / name).read_text(encoding="utf-8")

    changed = output("git", "diff", "--name-only").splitlines()
    assert "Stage1_Instances/THM-M-0476/check_intake.py" not in changed

    print(
        f"PASS THM-M-0476 obligation tree: {len(ids)} obligations, "
        f"{len(edge_ids)} typed edges"
    )
    print(f"registry denominator sha256: {denominator}")
    print(f"conditional Lean output sha256: {receipt['lean_output_sha256']}")
    print("root closure: open (H1/M3/R4); accepted closed obligations: 0")


if __name__ == "__main__":
    main()
