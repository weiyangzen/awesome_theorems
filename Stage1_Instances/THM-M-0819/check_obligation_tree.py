#!/usr/bin/env python3
"""Fail-closed validation of the THM-M-0819 obligation freeze."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0819-OBLIGATION_TREE"
THEOREM = "THM-M-0819"
ROOT_ID = "M0819-ROOT"
BASE_REVISION = "dc600635160cace0916df5234bf8808c39dc656d"
BASE_TREE = "8ee34b31ec38be1ef067aaab38c9a4cb4935b75a"
STATEMENT_SHA256 = "c3e600a4a5c2b48686bf244915aea79972e4537a2d89120ad739018716056b52"
ANCHOR_SHA256 = "a97aa82bbe42e49bee4a689d477ed9d574bbf8680b15feedf2c12fb508da85b1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
STATEMENT_OUTPUT_SHA256 = "abf1d640ea8c8596d75c5efdad4b2871723e562cf058e03af92feb289fdc3134"
LEAN_OUTPUT_SHA256 = "005cb8a50051b3ecaaf661d1618dbc0d75d11a988fc1677b141c62f689012419"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
}
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md": "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md": "skills/execute-stage1-rev56/SKILL.md",
    "Docs/Blueprint_Guidelines.md": "Docs/Blueprint_Guidelines.md",
    "Formalizations/Lean/lean-toolchain": "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json": "Formalizations/Lean/lake-manifest.json",
    f"Stage1_Instances/{THEOREM}/Statement.lean": f"Stage1_Instances/{THEOREM}/Statement.lean",
    f"Stage1_Instances/{THEOREM}/statement.json": f"Stage1_Instances/{THEOREM}/statement.json",
    f"Stage1_Instances/{THEOREM}/anchor-audit.json": f"Stage1_Instances/{THEOREM}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM}/anchor-audit-receipt.json": f"Stage1_Instances/{THEOREM}/anchor-audit-receipt.json",
}
HASHED_ARTIFACTS = {
    "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
    "obligation-registry.json", "typed-graphs.json", "validation-specs.json",
    "obligation-tree.md", "obligation-tree-validation.md",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "trusted_by", "refines",
    "workflow_depends_on",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


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


def assert_exact_index(graph: dict, endpoints: set[str]) -> None:
    expected_out = {identifier: [] for identifier in endpoints}
    expected_in = {identifier: [] for identifier in endpoints}
    for value in graph["edges"]:
        expected_out[value["from"]].append(value["edge_id"])
        expected_in[value["to"]].append(value["edge_id"])
    assert graph["out"] == expected_out
    assert graph["in"] == expected_in


def reachable_from(edges: list[dict], roots: set[str]) -> set[str]:
    outgoing: dict[str, list[str]] = {}
    for value in edges:
        outgoing.setdefault(value["from"], []).append(value["to"])
    visited: set[str] = set()
    pending = list(roots)
    while pending:
        identifier = pending.pop()
        if identifier in visited:
            continue
        visited.add(identifier)
        pending.extend(outgoing.get(identifier, []))
    return visited


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', source)


def check_text(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert not any(line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    receipt = load("obligation-tree-receipt.json") if (HERE / "obligation-tree-receipt.json").exists() else None

    module_spec = importlib.util.spec_from_file_location(
        "m0819_obligation_builder", HERE / "build_obligation_artifacts.py"
    )
    assert module_spec is not None and module_spec.loader is not None
    builder = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(builder)
    expected_registry, expected_bundle, expected_specs = builder.build()
    assert registry == expected_registry
    assert bundle == expected_bundle
    assert specs == expected_specs

    registry_top_fields = {
        "schema_version", "normative_profile", "lifecycle_mode", "registry_id", "item_id",
        "theorem_id", "registry_version", "frozen_at", "freeze_basis",
        "freeze_order_boundary", "frozen_against_statement_sha256",
        "frozen_against_statement_bundle_sha256", "frozen_against_anchor_audit_sha256",
        "root_obligation_id", "denominator_sha256", "canonical_projection_fields",
        "frozen_denominators", "layer_exclusions", "mandatory_layer_analysis", "delta_policy",
        "append_only_delta", "obligations", "status_observed_after_freeze", "status_boundary",
        "registry_sha256",
    }
    bundle_top_fields = {
        "schema_version", "normative_profile", "lifecycle_mode", "item_id", "theorem_id",
        "registry_id", "registry_version", "registry_denominator_sha256", "registry_sha256",
        "root_node_id", "root_obligation_id", "edge_endpoint_namespace", "edge_direction",
        "workflow_task_nodes", "task_to_obligation_ids", "reciprocal_edge_type_contract",
        "interface_expression_fingerprints", "graph_reachability_contract", "nodes", "graphs",
        "composition_certificates", "unverified_decomposition_plans", "closure_boundary",
    }
    specs_top_fields = {
        "schema_version", "normative_profile", "lifecycle_mode", "item_id", "theorem_id",
        "registry_denominator_sha256", "registry_sha256", "recipes", "status_boundary",
    }
    assert set(registry) == registry_top_fields
    assert set(bundle) == bundle_top_fields
    assert set(specs) == specs_top_fields
    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["lifecycle_mode"] == bundle["lifecycle_mode"] == specs["lifecycle_mode"] == "executing"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean") == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json") == ANCHOR_SHA256
    assert registry["append_only_delta"] == [] and registry["registry_version"] == 1
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    instance = json.loads((HERE / "instance.json").read_text(encoding="utf-8"))
    assert instance["lifecycle_mode"] == "planned"
    assert instance["obligation_registry_hash"] is None
    assert instance["theorem_complete"] is False and instance["accepted_receipt_ids"] == []

    manifest = json.loads((ROOT / "Docs" / "Stage1_Targets_rev-5.6.json").read_text())
    target = next(value for value in manifest["targets"] if value["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1377
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    execution = json.loads((ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json").read_text())
    item = next(value for value in execution["items"] if value["id"] == ITEM)
    predecessor = next(value for value in execution["items"] if value["id"] == "S56-M-0819-ANCHOR_AUDIT")
    assert item["phase"] == "obligation_tree" and item["layer"] == 3 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0819-ANCHOR_AUDIT"]
    assert predecessor["state"] == "[_]"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    layers = registry["mandatory_layer_analysis"]
    assert set(layers) == {"S", "N", "B", "C", "L", "X", "T", "not_applicable_layers"}
    assert layers["not_applicable_layers"] == []
    assert all(layers[name] for name in ("S", "N", "B", "C", "L", "X", "T"))

    registry_fields = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    }
    obligations = registry["obligations"]
    ids = [value["obligation_id"] for value in obligations]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 33
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    projection = [{key: value[key] for key in registry["canonical_projection_fields"]}
                  for value in obligations]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"]
    assert denominator == bundle["registry_denominator_sha256"] == specs["registry_denominator_sha256"]
    registry_scope = {
        key: value for key, value in registry.items()
        if key not in {"status_observed_after_freeze", "status_boundary", "registry_sha256"}
    }
    registry_sha256 = hashlib.sha256(
        json.dumps(registry_scope, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()
    assert registry_sha256 == registry["registry_sha256"]
    assert registry_sha256 == bundle["registry_sha256"] == specs["registry_sha256"]
    for value in obligations:
        assert set(value) == registry_fields
        assert value["kind"] in {
            "root", "definition", "reduction", "branch", "construction", "lemma",
            "computation", "transport", "terminal",
        }
        assert value["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert value["human_source_eligibility"] in {"required", "not_applicable"}
        assert value["readable_eligibility"] in {"required", "not_applicable"}
        assert value["risk_class"] in {"critical", "high", "normal", "low"}
        if value["machine_eligibility"] != "required" or value["human_source_eligibility"] != "required":
            assert set(value["exclusion_reason"]) == {"code", "justification", "approval"}
            assert value["exclusion_reason"]["approval"].startswith("pending independent")
        else:
            assert value["exclusion_reason"] is None
    frozen = registry["frozen_denominators"]
    assert frozen["inventory"] == ids
    assert frozen["required_machine"] == [
        value["obligation_id"] for value in obligations if value["machine_eligibility"] == "required"
    ]
    assert frozen["required_human_source"] == [
        value["obligation_id"] for value in obligations if value["human_source_eligibility"] == "required"
    ]
    assert frozen["required_readable"] == [
        value["obligation_id"] for value in obligations if value["readable_eligibility"] == "required"
    ]
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"

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
    assert {value["obligation_id"] for value in nodes} == id_set
    assert len({value["node_id"] for value in nodes}) == len(nodes)
    node_by_id = {value["obligation_id"]: value for value in nodes}
    step_ids: set[str] = set()
    markdown = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    for value in nodes:
        assert set(value) == required_node_fields
        assert value["kind"] in {
            "root", "definition", "normalization", "reduction", "branch", "construction",
            "bridge", "core_lemma", "computation", "certificate", "transport", "terminal",
        }
        assert value["human_debt"] in {f"H{index}" for index in range(6)}
        assert value["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert value["readability_debt"] in {f"R{index}" for index in range(5)}
        if value["obligation_id"] in builder.REQUIRES:
            assert value["step_budget"] == "split-required"
        else:
            assert isinstance(value["step_budget"], int)
            assert 0 < value["step_budget"] <= 100
        assert value["semantic_step_ledger"]
        if isinstance(value["step_budget"], int):
            assert len(value["semantic_step_ledger"]) <= value["step_budget"]
        for step in value["semantic_step_ledger"]:
            assert set(step) == {
                "step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use",
                "status",
            }
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            assert step["status"] in {"checked_interface", "planned_substantive_not_proof_accepted"}
            step_ids.add(step["step_id"])
        assert value["public_readable_target"].startswith(f"Stage1_Instances/{THEOREM}/obligation-tree.md#")
        anchor = value["public_readable_target"].split("#", 1)[1]
        assert f'<a id="{anchor}"></a>' in markdown
        assert value["owner"] and value["reviewer"] and value["validity"]["review_due"]
        assert value["validity"]["validated_at"] == "2026-07-14"
        assert value["validity"]["revocation_state"] in {
            "provisional_interface_check", "structurally_validated_not_proof_accepted",
        }
    allowed_ledger_boundaries = {
        "FROZEN-FORMAL-CONTEXT", "typed-non-proof-edge-or-canonical-root-boundary"
    }
    for value in nodes:
        ledger = value["semantic_step_ledger"]
        for index, step in enumerate(ledger):
            assert set(step["premise_ids"]) <= id_set | step_ids | allowed_ledger_boundaries
            assert set(step["outgoing_use"]) <= id_set | step_ids | allowed_ledger_boundaries
            if index + 1 < len(ledger):
                assert step["outgoing_use"] == [ledger[index + 1]["step_id"]]
                assert ledger[index + 1]["premise_ids"] == [step["step_id"]]
        for premise in ledger[0]["premise_ids"]:
            if premise in id_set:
                assert value["obligation_id"] in node_by_id[premise]["semantic_step_ledger"][-1]["outgoing_use"]
    assert node_by_id[ROOT_ID]["machine_debt"] == "M3"
    assert node_by_id["M0819-B-WIDTH-POSITIVE"]["machine_debt"] == "M3"
    assert node_by_id["M0819-X-FINITE-CANDIDATE"]["machine_debt"] == "M5"
    assert all(not value["evidence_ids"] for value in nodes)
    terminal_bodies = {
        value["obligation_id"]: value["terminal_proof_body_id"]
        for value in obligations if value["terminal_proof_body_id"] is not None
    }
    assert terminal_bodies == {
        "M0819-B-WIDTH-ZERO": "Stage1Instances.THM_M_0819_Obligations.zeroWidth_of_statement",
        "M0819-T-WIDTH-BRANCHES": "Stage1Instances.THM_M_0819_Obligations.widthBranches_of_positive_and_zero",
        "M0819-T-ROOT-ASSEMBLE": "Stage1Instances.THM_M_0819_Obligations.root_of_widthBranches",
    }

    assert bundle["root_node_id"] == f"{THEOREM}-ROOT"
    assert bundle["root_obligation_id"] == ROOT_ID
    assert node_by_id[ROOT_ID]["node_id"] == bundle["root_node_id"]
    assert set(bundle["graphs"]) == GRAPH_NAMES
    all_edge_ids: set[str] = set()
    workflow_ids = set(bundle["workflow_task_nodes"])
    for name, graph in bundle["graphs"].items():
        endpoints = workflow_ids if name == "workflow" else id_set
        assert set(graph["out"]) == set(graph["in"]) == endpoints
        assert_exact_index(graph, endpoints)
        directional = []
        for value in graph["edges"]:
            assert value["edge_id"] not in all_edge_ids
            assert value["type"] in ALLOWED_EDGES
            assert value["from"] in endpoints and value["to"] in endpoints
            assert value["edge_id"] in graph["out"][value["from"]]
            assert value["edge_id"] in graph["in"][value["to"]]
            all_edge_ids.add(value["edge_id"])
            if not (
                (name == "proof" and value["type"] in {"composes", "refines"})
                or (name == "refinement" and value["type"] in {"refines", "equivalent_to"})
                or (name == "trust" and value["type"] == "trusted_by")
            ):
                directional.append(value)
        check_acyclic(directional)
    reachability_contract = bundle["graph_reachability_contract"]
    assert set(reachability_contract) == GRAPH_NAMES
    for name, contract in reachability_contract.items():
        assert set(contract) == {"roots", "required_reachable"}
        traversed = reachable_from(bundle["graphs"][name]["edges"], set(contract["roots"]))
        assert traversed == set(contract["required_reachable"])
    assert len(all_edge_ids) == 154
    assert bundle["graphs"]["evidence"]["edges"] == []
    source_mapped = {
        value["from"] for value in bundle["graphs"]["provenance"]["edges"]
        if value["type"] == "source_map"
    }
    assert source_mapped == (
        set(frozen["required_human_source"]) - {"M0819-X-PRIMARY-SOURCE"}
    )
    assert reachable_from(
        [value for value in bundle["graphs"]["provenance"]["edges"]
         if value["type"] == "source_map"],
        source_mapped,
    ) == source_mapped | {"M0819-X-PRIMARY-SOURCE"}
    documented = id_set - {"M0819-X-READABLE"}
    assert reachable_from(bundle["graphs"]["documentation"]["edges"], {"M0819-X-READABLE"}) == id_set
    assert {
        value["to"] for value in bundle["graphs"]["documentation"]["edges"]
        if value["type"] == "documents"
    } == documented
    assert reachable_from(bundle["graphs"]["workflow"]["edges"], {"S56-M-0819-RELEASE"}) == workflow_ids

    graph_edge_types = {
        "proof": {"proof_requires", "composes", "refines"},
        "refinement": {"logical_decomposition", "refines", "equivalent_to", "transports"},
        "provenance": {"source_map", "provenance_of"},
        "evidence": {"evidence_for"},
        "trust": {"trusts", "trusted_by"},
        "documentation": {"documents", "expository_decomposition"},
        "workflow": {"workflow_depends_on"},
    }
    for name, graph in bundle["graphs"].items():
        assert {value["type"] for value in graph["edges"]} <= graph_edge_types[name]
        for value in graph["edges"]:
            expected_fields = {"edge_id", "from", "type", "to"}
            if name in {"proof", "refinement", "trust"}:
                expected_fields.add("reciprocal_edge_id")
            if name == "proof" and value["type"] == "composes":
                expected_fields.add("composition_certificate_id")
            assert set(value) == expected_fields
    overlay_kinds = {"certificate", "terminal"}
    for value in bundle["graphs"]["provenance"]["edges"]:
        if value["type"] == "provenance_of":
            assert node_by_id[value["from"]]["kind"] in overlay_kinds | {"bridge"}
    for value in bundle["graphs"]["documentation"]["edges"]:
        assert value["from"] == "M0819-X-READABLE"
        assert value["to"] != "M0819-X-READABLE"
    for value in bundle["graphs"]["provenance"]["edges"]:
        if value["type"] == "source_map":
            assert value["to"] == "M0819-X-PRIMARY-SOURCE"
    for value in bundle["graphs"]["trust"]["edges"]:
        if value["type"] == "trusts":
            assert node_by_id[value["to"]]["kind"] == "certificate"

    proof = {value["edge_id"]: value for value in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    composes = []
    for value in proof.values():
        reciprocal = proof[value["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == value["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (value["to"], value["from"])
        assert value["type"] == "proof_requires" or reciprocal["type"] == "proof_requires"
        assert {value["type"], reciprocal["type"]} in (
            {"proof_requires", "composes"}, {"proof_requires", "refines"}
        )
        if value["type"] == "proof_requires":
            children.setdefault(value["from"], []).append(value["to"])
        if value["type"] == "composes":
            composes.append(value)
    assert {(value["from"], value["to"]) for value in composes} == {
        ("M0819-T-ROOT-ASSEMBLE", ROOT_ID),
        ("M0819-S-TRANSPORT", "M0819-T-ROOT-ASSEMBLE"),
        ("M0819-T-WIDTH-BRANCHES", "M0819-T-ROOT-ASSEMBLE"),
        ("M0819-B-WIDTH-ZERO", "M0819-T-WIDTH-BRANCHES"),
        ("M0819-B-WIDTH-POSITIVE", "M0819-T-WIDTH-BRANCHES"),
    }
    for value in composes:
        assert value["composition_certificate_id"] == (
            "COMP-M0819-ROOT" if value["to"] == ROOT_ID
            else "COMP-M0819-T-ROOT-ASSEMBLE" if value["to"] == "M0819-T-ROOT-ASSEMBLE"
            else "COMP-M0819-T-WIDTH-BRANCHES"
        )
    inverse_types = {
        "logical_decomposition": "refines", "refines": "logical_decomposition",
        "equivalent_to": "equivalent_to",
        "trusts": "trusted_by", "trusted_by": "trusts",
    }
    for graph_name in ("refinement", "trust"):
        edge_by_id = {
            value["edge_id"]: value for value in bundle["graphs"][graph_name]["edges"]
        }
        for value in edge_by_id.values():
            reverse = edge_by_id[value["reciprocal_edge_id"]]
            assert reverse["reciprocal_edge_id"] == value["edge_id"]
            assert (reverse["from"], reverse["to"]) == (value["to"], value["from"])
            assert reverse["type"] == inverse_types[value["type"]]
    refinement_relations = {
        (value["from"], value["type"], value["to"])
        for value in bundle["graphs"]["refinement"]["edges"]
    }
    assert (ROOT_ID, "equivalent_to", "M0819-S-TRANSPORT") in refinement_relations
    assert not any(
        "M0819-S-FOUNDATION" in {source, target}
        for source, _edge_type, target in refinement_relations
    )
    certificates = {value["parent_obligation_id"]: value for value in bundle["composition_certificates"]}
    for parent in {value["to"] for value in composes}:
        certificate = certificates[parent]
        assert set(certificate) == {
            "certificate_id", "parent_obligation_id", "parent_statement_fingerprint",
            "required_child_ids", "required_child_statement_fingerprints",
            "parent_interface_expression_fingerprint",
            "required_child_interface_expression_fingerprints", "consumed_child_ids",
            "unused_child_ids", "undeclared_premises", "declarations", "kind", "status",
        }
        assert certificate["status"].startswith("provisional conditional composition")
        assert certificate["required_child_ids"] == children[parent]
        assert certificate["consumed_child_ids"] == children[parent]
        assert certificate["unused_child_ids"] == certificate["undeclared_premises"] == []
        assert certificate["required_child_statement_fingerprints"] == {
            child: next(row["statement_fingerprint"] for row in obligations
                        if row["obligation_id"] == child)
            for child in children[parent]
        }
        assert certificate["parent_statement_fingerprint"] == next(
            value["statement_fingerprint"] for value in obligations if value["obligation_id"] == parent
        )
    reachable: set[str] = set()

    def reach(identifier: str) -> None:
        if identifier in reachable:
            return
        reachable.add(identifier)
        for child in children.get(identifier, []):
            reach(child)

    reach(ROOT_ID)
    proof_overlays = {
        "M0819-S-DEFINITIONS", "M0819-S-DOMAIN", "M0819-S-FOUNDATION",
        "M0819-X-PRIMARY-SOURCE", "M0819-X-FINITE-CANDIDATE",
        "M0819-X-RADO-PROVENANCE", "M0819-X-PROVENANCE", "M0819-X-TRUST",
        "M0819-X-READABLE", "M0819-X-WORKFLOW",
    }
    assert reachable == id_set - proof_overlays
    for parent in id_set:
        ledger_obligations = {
            premise
            for step in node_by_id[parent]["semantic_step_ledger"]
            for premise in step["premise_ids"]
            if premise in id_set
        }
        assert ledger_obligations == set(children.get(parent, []))
    assert len(bundle["unverified_decomposition_plans"]) == 12
    assert {value["parent_obligation_id"] for value in bundle["unverified_decomposition_plans"]} == (
        set(children) - set(builder.CHECKED_PARENT_DECLARATIONS)
    )
    for value in bundle["unverified_decomposition_plans"]:
        assert set(value) == {
            "plan_id", "parent_obligation_id", "parent_statement_fingerprint",
            "planned_child_ids", "planned_child_statement_fingerprints", "status",
            "required_future_certificate",
        }
        assert value["status"] == "planned_semantic_decomposition_not_proof_accepted"
        parent = value["parent_obligation_id"]
        assert value["planned_child_ids"] == children[parent]
        assert value["planned_child_statement_fingerprints"] == {
            child: next(row["statement_fingerprint"] for row in obligations
                        if row["obligation_id"] == child)
            for child in children[parent]
        }
    assert {value["parent_obligation_id"] for value in bundle["composition_certificates"]} == {
        ROOT_ID, "M0819-T-ROOT-ASSEMBLE", "M0819-T-WIDTH-BRANCHES"
    }
    assert bundle["workflow_task_nodes"] == list(builder.WORKFLOW_TASKS)
    assert bundle["task_to_obligation_ids"] == {
        ITEM: ids,
        "S56-M-0819-PROOF": frozen["required_machine"],
        "S56-M-0819-VALIDATION": ids,
        "S56-M-0819-RELEASE": ids,
    }
    expected_task_ids = {
        identifier: [ITEM]
        + (["S56-M-0819-PROOF"] if identifier in frozen["required_machine"] else [])
        + ["S56-M-0819-VALIDATION", "S56-M-0819-RELEASE"]
        for identifier in ids
    }
    assert {
        value["obligation_id"]: value["task_ids"] for value in nodes
    } == expected_task_ids
    assert {
        task: [identifier for identifier in ids if task in node_by_id[identifier]["task_ids"]]
        for task in bundle["task_to_obligation_ids"]
    } == bundle["task_to_obligation_ids"]

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == []
    derived_closed = {
        identifier for identifier in id_set
        if node_by_id[identifier]["evidence_ids"]
        and node_by_id[identifier]["machine_debt"].startswith("M0-")
    }
    assert derived_closed == set(boundary["accepted_closed_obligations"])
    derived_root_closed = ROOT_ID in derived_closed
    assert boundary["root_closed"] is derived_root_closed is False
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["authoritative_root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert boundary["minimal_open_proof_cut_set"] == ["M0819-B-WIDTH-POSITIVE"]
    positive_descendants: set[str] = set()

    def descend(identifier: str) -> None:
        if identifier in positive_descendants:
            return
        positive_descendants.add(identifier)
        for child in children.get(identifier, []):
            descend(child)

    descend("M0819-B-WIDTH-POSITIVE")
    assert boundary["open_proof_leaf_frontier"] == sorted(
        identifier for identifier in positive_descendants if identifier not in children
    )

    required_recipe_fields = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations",
        "coverage_boundary",
    }
    recipes = specs["recipes"]
    assert len(recipes) == 1
    recipe = recipes[0]
    assert set(recipe) == required_recipe_fields
    assert {value["validation_spec_id"] for value in nodes} == {recipe["recipe_id"]}
    assert recipe["recipe_id"] == "VAL-M0819-OBLIGATION-STRUCTURE-AND-LEAN"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"]
    assert recipe["env_allowlist"] == {
        "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1", "PYTHONDONTWRITEBYTECODE": "1"
    }
    assert recipe["timeout_seconds"] == 240 and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == ids
    assert set(recipe["covered_declarations"]) == {
        "Stage1Instances.THM_M_0819.DilworthPrimaryTarget",
        "Stage1Instances.THM_M_0819_Obligations.zeroWidth_of_statement",
        "Stage1Instances.THM_M_0819_Obligations.widthBranches_of_positive_and_zero",
        "Stage1Instances.THM_M_0819_Obligations.expanded_of_widthBranches",
        "Stage1Instances.THM_M_0819_Obligations.checked_root_transport",
        "Stage1Instances.THM_M_0819_Obligations.root_of_widthBranches",
        "Stage1Instances.THM_M_0819_Obligations.root_of_terminal",
    }

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    assert sha(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    compactness = MATHLIB / "Mathlib" / "Combinatorics" / "Compactness.lean"
    assert "theorem Finset.rado_selection_subtype" in compactness.read_text(encoding="utf-8")

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    assert not re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|implemented_by|native_decide|extern|opaque)\b",
        without_comments(source),
    )
    for marker in (
        "import Statement", "def PositiveWidthPackage", "def ZeroWidthPackage",
        "def WidthBranchPackage", "def RootTransportPackage", "def TerminalRootPackage",
        "#check Finset.rado_selection_subtype", "theorem zeroWidth_of_statement",
        "theorem widthBranches_of_positive_and_zero", "theorem expanded_of_widthBranches",
        "theorem checked_root_transport", "theorem root_of_widthBranches",
        "theorem root_of_terminal", "theorem root_of_positiveWidth",
        "assert_no_sorry root_of_positiveWidth",
        "#print axioms root_of_positiveWidth",
    ):
        assert marker in source, marker

    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    base_lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    environment = os.environ | {
        "LEAN_PATH": base_lean_path, "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1",
    }
    with tempfile.TemporaryDirectory(prefix="thm-m-0819-obligation-") as temp_dir:
        statement = subprocess.run(
            [lean_exe, "Statement.lean", "-o", str(Path(temp_dir) / "Statement.olean")],
            cwd=HERE, env=environment, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        lean = subprocess.run(
            ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM}/ObligationTree.lean"],
            cwd=LEAN_ROOT,
            env=environment | {"LEAN_PATH": temp_dir + ":" + base_lean_path},
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    assert hashlib.sha256(statement.stdout.encode()).hexdigest() == STATEMENT_OUTPUT_SHA256
    actual_lean_output_sha256 = hashlib.sha256(lean.stdout.encode()).hexdigest()
    assert actual_lean_output_sha256 == LEAN_OUTPUT_SHA256
    assert "Declarations are sorry-free!" in lean.stdout and "sorryAx" not in lean.stdout
    normalized = re.sub(r"\s+", " ", lean.stdout)
    assert normalized.count("depends on axioms: [propext]") == 2
    assert normalized.count("does not depend on any axioms") == 5
    for declaration in (
        "PositiveWidthPackage", "ZeroWidthPackage", "WidthBranchPackage", "RootTransportPackage",
        "TerminalRootPackage", "Finset.rado_selection_subtype",
        "zeroWidth_of_statement", "widthBranches_of_positive_and_zero",
        "expanded_of_widthBranches", "checked_root_transport", "root_of_widthBranches", "root_of_terminal",
        "root_of_positiveWidth",
    ):
        assert declaration in lean.stdout

    namespace = "Stage1Instances.THM_M_0819_Obligations."
    interface_names = {
        "M0819-S-TRANSPORT": "RootTransportPackage",
        "M0819-B-WIDTH-ZERO": "ZeroWidthPackage",
        "M0819-B-WIDTH-POSITIVE": "PositiveWidthPackage",
        "M0819-T-WIDTH-BRANCHES": "WidthBranchPackage",
        "M0819-T-ROOT-ASSEMBLE": "TerminalRootPackage",
    }
    serialized: dict[str, str] = {}
    markers = [f"def {namespace}{name}" for name in interface_names.values()]
    positions = {marker: lean.stdout.rfind(marker) for marker in markers}
    assert all(position >= 0 for position in positions.values())
    for identifier, name in interface_names.items():
        marker = f"def {namespace}{name}"
        start = positions[marker]
        later = [position for position in positions.values() if position > start]
        end = min(later) if later else lean.stdout.find("Declarations are sorry-free!", start)
        body = lean.stdout[start:end].strip()
        assert "?m." not in body and " : Prop :=" in body
        serialized[identifier] = "lean-expression-sha256:" + hashlib.sha256(body.encode()).hexdigest()
    expected_interfaces = bundle["interface_expression_fingerprints"]
    assert expected_interfaces[ROOT_ID] == "lean-expression-sha256:" + builder.ROOT_EXPRESSION
    for identifier, fingerprint in serialized.items():
        assert expected_interfaces[identifier] == fingerprint
    for parent, certificate in certificates.items():
        assert certificate["parent_interface_expression_fingerprint"] == expected_interfaces[parent]
        assert certificate["required_child_interface_expression_fingerprints"] == {
            child: expected_interfaces[child] for child in children[parent]
        }

    changed_paths = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/ObligationTree.lean",
        f"Stage1_Instances/{THEOREM}/build_obligation_artifacts.py",
        f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
        f"Stage1_Instances/{THEOREM}/obligation-registry.json",
        f"Stage1_Instances/{THEOREM}/obligation-tree-receipt.json",
        f"Stage1_Instances/{THEOREM}/obligation-tree-validation.md",
        f"Stage1_Instances/{THEOREM}/obligation-tree.md",
        f"Stage1_Instances/{THEOREM}/typed-graphs.json",
        f"Stage1_Instances/{THEOREM}/validation-specs.json",
    }
    if receipt is not None:
        receipt_fields = {
            "schema_version", "normative_profile", "lifecycle_mode", "receipt_id", "item_id",
            "theorem_id", "execution_rank", "phase", "intent", "receipt_class",
            "content_addressed", "content_addressed_recipe_ids", "content_addressed_receipt_ids",
            "self_hash_boundary", "depends_on", "verdict", "proposed_state", "accepted",
            "acceptance_authority", "base_revision", "base_tree", "worker_branch_or_worktree",
            "repository_dirty_state", "worktree_state", "preexisting_untracked_paths",
            "dependency_boundary", "instance_reconciliation_boundary", "validated_at", "timezone",
            "started_at", "ended_at", "attestor", "platform", "owner", "reviewer", "review_due",
            "freshness_policy", "support_state", "supersession_state",
            "revocation_state", "incident_path", "source_inputs", "artifact_hashes",
            "immutable_environment", "registry_id", "registry_version", "registry_sha256",
            "registry_denominator_sha256", "obligation_count", "typed_edge_count",
            "semantic_ledger_step_count", "composition_certificate_count",
            "unverified_decomposition_count", "graph_names", "canonical_declaration",
            "canonical_statement_fingerprints", "canonical_obligation_ids",
            "composition_declarations", "conditional_premises", "proof_body_locations",
            "candidate_result", "new_bridge_boundary", "elaborated_open_interface_ids",
            "provisionally_checked_interfaces", "accepted_closed_obligations",
            "accepted_receipt_ids", "axiom_and_placeholder_result", "statement_output_sha256",
            "lean_output_sha256", "changed_paths", "diff_summary", "exact_statement_change",
            "typed_graph_changes", "composition_changes", "actual_source_ownership",
            "declaration_ownership", "readable_ownership", "change_impact_set",
            "historical_instance_root_vector", "historical_instance_boundary",
            "root_vector_before", "root_vector_after", "debt_vector_delta", "audit_complete",
            "theorem_complete", "remaining_machine_root_cut_set", "machine_cut_set_classification",
            "remaining_release_cut_set", "first_failed_gate", "retry_condition", "known_failures",
            "structured_validation_recipes", "commands_and_results", "output_summary",
            "invalidation_inputs", "status_boundary",
        }
        assert set(receipt) == receipt_fields
        assert receipt["schema_version"] == "stage1-worker-obligation-tree-receipt/1.0"
        assert receipt["lifecycle_mode"] == "executing"
        assert receipt["receipt_id"] == "S56-M-0819-OBLIGATION-TREE-WORKER-20260714"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["started_at"] < receipt["ended_at"] == receipt["validated_at"]
        assert receipt["attestor"] == "Stage1 rev-5.6 worker slot8"
        assert receipt["platform"]["lean_discovery_argv"] == ["lake", "env", "which", "lean"]
        assert receipt["platform"]["lean_executable_sha256"] == "sha256:" + sha(Path(lean_exe))
        assert receipt["platform"]["lean_path_sha256"] == (
            "sha256:" + hashlib.sha256(base_lean_path.encode()).hexdigest()
        )
        assert receipt["freshness_policy"].startswith("invalidate on any source")
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["registry_sha256"] == registry_sha256
        assert receipt["obligation_count"] == len(ids)
        assert receipt["typed_edge_count"] == len(all_edge_ids)
        assert receipt["semantic_ledger_step_count"] == len(step_ids)
        assert receipt["composition_certificate_count"] == len(bundle["composition_certificates"])
        assert receipt["unverified_decomposition_count"] == len(bundle["unverified_decomposition_plans"])
        assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
        assert receipt["accepted_closed_obligations"] == []
        assert receipt["proof_body_locations"] and all(
            value.startswith(f"local:Stage1_Instances/{THEOREM}/ObligationTree.lean#")
            for value in receipt["proof_body_locations"]
        )
        assert receipt["canonical_obligation_ids"] == ids
        assert set(receipt["graph_names"]) == GRAPH_NAMES
        assert receipt["provisionally_checked_interfaces"] == sorted(builder.CHECKED_INTERFACES)
        assert receipt["source_inputs"] == {
            key: "sha256:" + sha(ROOT / relative) for key, relative in SOURCE_INPUTS.items()
        }
        assert receipt["artifact_hashes"] == {
            name: "sha256:" + sha(HERE / name) for name in sorted(HASHED_ARTIFACTS)
        }
        assert receipt["repository_dirty_state"]["release_eligible"] is False
        assert receipt["repository_dirty_state"]["initial_status_sha256"] == (
            "sha256:8c616a936e1f6b2689a8955b4904494d5639a105b14cc0154b8805f96d28e97e"
        )
        assert receipt["repository_dirty_state"]["tracked_patch_sha256"] == (
            "sha256:e3b0c44298fc1c149afbf4c8996fb25a8fe879c2"
            "4649b934ca495991b7852b855"
        )
        assert receipt["self_hash_boundary"].startswith("The receipt file and root worker packet")
        assert receipt["instance_reconciliation_boundary"].startswith(
            "The tracked planned intake manifest remains historical"
        )
        assert receipt["commands_and_results"] and all(
            row["cwd"] and isinstance(row["argv"], list) and row["argv"]
            and row["exit_code"] == 0 and row["result"]
            for row in receipt["commands_and_results"]
        )
        assert receipt["structured_validation_recipes"] == recipes
        assert not any(
            "<" in argument or ">" in argument
            for row in receipt["commands_and_results"]
            for argument in row["argv"]
        )
        assert receipt["historical_instance_root_vector"] == instance["root_vector"] == {
            "H": "H1", "M": "M5", "R": "R3"
        }
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R3"}
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["audit_complete"] is receipt["theorem_complete"] is False
        assert set(receipt["changed_paths"]) == changed_paths
        packet = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == changed_paths
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]
        actual_changed = {
            line[3:] for line in output("git", "status", "--short", "--untracked-files=all").splitlines()
        }
        assert actual_changed - {"Formalizations/Lean/.lake"} == changed_paths

    for relative in changed_paths:
        path = ROOT / relative
        if path.exists():
            check_text(path)
    print(
        f"PASS {THEOREM} obligation tree: {len(ids)} obligations, "
        f"{len(all_edge_ids)} typed edge records, {len(step_ids)} structured ledger steps, "
        f"{len(bundle['unverified_decomposition_plans'])} unverified decompositions"
    )
    print(f"registry denominator sha256: {denominator}")
    print(f"Lean conditional composition stdout sha256: {LEAN_OUTPUT_SHA256}")
    print("root closure: open (H1/M3/R3); accepted_closed_obligations=0; theorem_complete=false")


if __name__ == "__main__":
    main()
