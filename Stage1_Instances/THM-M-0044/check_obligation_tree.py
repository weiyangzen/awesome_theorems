#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-0044 obligation freeze."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0044-OBLIGATION_TREE"
THEOREM = "THM-M-0044"
ROOT_ID = "M0044-ROOT"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_acyclic(edges: list[dict]) -> None:
    children: dict[str, list[str]] = {}
    for value in edges:
        children.setdefault(value["from"], []).append(value["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        assert node not in visiting, f"cycle through {node}"
        if node in visited:
            return
        visiting.add(node)
        for child in children.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for node in children:
        visit(node)


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    instance = load("instance.json")
    receipt = load("obligation-tree-receipt.json")

    module_spec = importlib.util.spec_from_file_location(
        "m0044_obligation_builder", HERE / "build_obligation_artifacts.py"
    )
    assert module_spec is not None and module_spec.loader is not None
    builder = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(builder)
    expected_registry, expected_bundle, expected_specs = builder.build()
    assert registry == expected_registry
    assert bundle == expected_bundle
    assert specs == expected_specs

    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
    assert registry["append_only_delta"] == [] and registry["registry_version"] == 1
    layers = registry["mandatory_layer_analysis"]
    assert set(layers) == {"S", "N", "B", "C", "L", "X", "T", "not_applicable_layers"}
    assert layers["not_applicable_layers"] == []
    assert all(layers[name] for name in ("S", "N", "B", "C", "L", "X", "T"))

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    obligations = registry["obligations"]
    ids = [row["obligation_id"] for row in obligations]
    assert len(ids) == len(set(ids)) == 39
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    projection = [{key: row[key] for key in fields} for row in obligations]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"]
    assert denominator == bundle["registry_denominator_sha256"]
    assert denominator == specs["registry_denominator_sha256"]
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    frozen = registry["frozen_denominators"]
    assert frozen["inventory"] == ids
    assert frozen["required_machine"] == [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"]
    assert frozen["required_human_source"] == [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"]
    assert frozen["required_readable"] == ids
    for row in obligations:
        assert set(row) == set(fields)
        assert row["kind"] in {"root", "definition", "reduction", "branch", "construction", "lemma", "computation", "transport", "terminal"}
        assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] in {"required", "not_applicable"}
        assert row["risk_class"] in {"critical", "high", "normal", "low"}
        if row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required":
            assert row["exclusion_reason"] and row["exclusion_reason"].endswith("pending_independent_approval")

    required_node_fields = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
        "human_debt", "machine_debt", "readability_debt", "evidence_ids",
        "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
        "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
        "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
        "reviewer", "validity",
    }
    nodes = bundle["nodes"]
    assert len(nodes) == len(ids)
    assert {node["obligation_id"] for node in nodes} == set(ids)
    assert len({node["node_id"] for node in nodes}) == len(nodes)
    node_by_obligation = {node["obligation_id"]: node for node in nodes}
    for node in nodes:
        assert set(node) == required_node_fields
        assert node["kind"] in {"root", "definition", "normalization", "reduction", "branch", "construction", "bridge", "core_lemma", "computation", "certificate", "transport", "terminal"}
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert set(node["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"}
        assert all(node["semantic_step_ledger"].values())
        assert node["public_readable_target"].startswith(f"Stage1_Instances/{THEOREM}/obligation-tree.md#")
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]
    assert node_by_obligation[ROOT_ID]["machine_debt"] == "M3"
    assert node_by_obligation["M0044-X-SPECTRAL"]["machine_debt"] == "M3"
    assert all(node_by_obligation[identifier]["machine_debt"] == "M3" for identifier in registry["status_observed_after_freeze"]["provisionally_checked_interfaces"])
    assert node_by_obligation["M0044-T-REAL"]["machine_debt"] == "M4"
    assert node_by_obligation["M0044-T-COMPLEX"]["machine_debt"] == "M4"

    assert bundle["root_node_id"] == ROOT_ID
    assert bundle["edge_endpoint_namespace"] == "canonical obligation_id"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    for graph in bundle["graphs"].values():
        assert set(graph["out"]) == set(ids) == set(graph["in"])
        directional = []
        for value in graph["edges"]:
            assert value["edge_id"] not in edge_ids
            assert value["type"] in ALLOWED_EDGES
            assert value["from"] in ids and value["to"] in ids
            assert value["edge_id"] in graph["out"][value["from"]]
            assert value["edge_id"] in graph["in"][value["to"]]
            edge_ids.add(value["edge_id"])
            if value["type"] != "composes":
                directional.append(value)
        check_acyclic(directional)

    proof = {value["edge_id"]: value for value in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for value in proof.values():
        reciprocal = proof[value["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == value["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (value["to"], value["from"])
        assert {value["type"], reciprocal["type"]} == {"proof_requires", "composes"}
        if value["type"] == "proof_requires":
            children.setdefault(value["from"], []).append(value["to"])
    reachable: set[str] = set()

    def reach(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            reach(child)

    reach(ROOT_ID)
    proof_overlay_exclusions = {
        "M0044-S-INTERFACE", "M0044-S-ENCODING", "M0044-S-FOUNDATION",
        "M0044-X-SOURCE", "M0044-X-PROVENANCE", "M0044-X-TRUST",
        "M0044-X-READABLE", "M0044-X-WORKFLOW",
    }
    assert reachable == set(ids) - proof_overlay_exclusions

    required_recipe_fields = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs", "covered_obligation_ids",
        "covered_declarations",
    }
    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
    for recipe in recipes:
        assert set(recipe) == required_recipe_fields
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["timeout_seconds"] > 0 and len(recipe["covered_obligation_ids"]) == 1

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_receipt_ids"] == []
    assert {"M0044-T-REAL", "M0044-T-COMPLEX"} <= set(boundary["remaining_root_cut_set"])

    lean = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", lean, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b")
    assert forbidden.search(without_comments) is None
    for marker in (
        "def SelectedEmptyDimensionPackage : Prop",
        "theorem selectedEmptyDimensions", "def RealFullSVDPackage : Prop",
        "def ComplexFullSVDPackage : Prop",
        "theorem root_of_real_and_complex",
        "SingularValueDecompositionTarget :=", "#print axioms root_of_real_and_complex",
    ):
        assert marker in lean, marker

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    pins = {
        "Mathlib/Analysis/InnerProductSpace/SingularValues.lean": (
            "cfc6d04849895b65fa0293d6cc3a234279e757726bc92fd99ce530ccc35863aa",
            ("singularValues_nonneg", "sq_singularValues_fin", "support_singularValues"),
        ),
        "Mathlib/Analysis/Matrix/Spectrum.lean": (
            "1a1a96a6f057a73b0d428b62cdbb3da824981928c162b52a15335abdafc8b0db",
            ("eigenvectorUnitary", "spectral_theorem"),
        ),
        "Mathlib/LinearAlgebra/UnitaryGroup.lean": (
            "0136abe584007ffe1b9e9b0016b792ed92bc2de36fa710e87af9cb87d0808f93",
            ("unitaryGroup", "mem_unitaryGroup_iff"),
        ),
    }
    for relative, (expected_sha, markers) in pins.items():
        source = mathlib / relative
        assert sha(source) == expected_sha
        source_text = source.read_text(encoding="utf-8")
        assert all(marker in source_text for marker in markers)

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False

    selftest = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
    assert set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == receipt["base_revision"]
    assert selftest["known_failures"] == receipt["known_failures"]
    assert selftest["changed_paths"] == receipt["changed_paths"]
    assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")

    print(f"PASS THM-M-0044 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R3); the real and complex positive-dimension packages remain M4")


if __name__ == "__main__":
    main()
