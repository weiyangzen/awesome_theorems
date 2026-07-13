#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0957 obligation freeze."""

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
ITEM = "S56-M-0957-OBLIGATION_TREE"
THEOREM = "THM-M-0957"
ROOT_ID = "M0957-ROOT"
EXPRESSION_SHA256 = "e611db43ce6f3419553e3ebe0fe85a3ce89e4d3930b3842f5a09be8a7683d2ed"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE_SHA256 = "1f8c1813a75c722ee4d62d63185c53d0b52d27691e531c05e0ecb6c10c15cf65"
MATHLIB_SOURCE_BLOB = "7d3eb0e603040dcd72fe35e39c82f4d615b3e254"
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
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
    "proof_budget_status", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner",
    "reviewer", "validity",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
EXPECTED_PROOF_REACHABLE = {
    "M0957-ROOT", "M0957-T-ASSEMBLE",
    "M0957-T-CONSTRUCTION", "M0957-T-SHARP-PARAMETERS",
    "M0957-T-PARAM-ADMISSIBLE", "M0957-N-SHARP-DIMENSION",
    "M0957-L-RADIX-NONZERO", "M0957-L-AMBIENT-FIT", "M0957-T-SHARP-ESTIMATE",
    "M0957-N-RPOW-EXP", "M0957-T-RATIO-ASYMPTOTIC",
    "M0957-T-PROXY-ASYMPTOTIC", "M0957-L-RADIX-FLOOR",
    "M0957-L-OPTIMAL-EXPONENT", "M0957-N-INCLUSIVE-INDEX",
    "M0957-L-PROXY-LOG", "M0957-L-RECIPROCAL-LOSS",
    "M0957-L-LINEAR-LOSS", "M0957-L-SUBLEADING-LOSS",
    "M0957-L-PROXY-RPOW-IDENTITY", "M0957-L-PROXY-SLACK",
    "M0957-L-RECIPROCAL-CORE", "M0957-L-LINEAR-CEILING",
    "M0957-L-LINEAR-INCREMENT", "M0957-L-DIMENSION-SLACK",
    "M0957-L-LOG-DIMENSION",
}
BASE_REVISION = "dc600635160cace0916df5234bf8808c39dc656d"
BASE_TREE = "8ee34b31ec38be1ef067aaab38c9a4cb4935b75a"


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments_and_strings(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', source)


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def check_acyclic(edges: list[dict]) -> None:
    adjacency: dict[str, list[str]] = {}
    for value in edges:
        adjacency.setdefault(value["from"], []).append(value["to"])
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


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({
        "LC_ALL": "C", "LANG": "C", "TZ": "UTC", "NO_COLOR": "1",
    })
    return subprocess.run(
        ["lake", "env", "lean", "--trust=0", str(path)],
        cwd=LEAN_ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
        check=False,
    )


def composed_lean() -> subprocess.CompletedProcess[str]:
    """Elaborate the architecture beside the actual statement and prove root identity."""
    statement = (HERE / "Statement.lean").read_text(encoding="utf-8")
    obligation = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    body = "\n".join(
        line for line in obligation.splitlines() if not line.startswith("import ")
    ) + "\n"
    marker = "\nend Stage1Instances.THM_M_0957_ObligationTree\n"
    assert body.count(marker) == 1
    identity = (
        "\n/-- Validator-only identity with the actual canonical declaration. -/\n"
        "theorem root_eq_actualCanonical :\n"
        "    Canonical.Root = Stage1Instances.THM_M_0957.BehrendConstructionTarget := rfl\n"
        "assert_no_sorry root_eq_actualCanonical\n"
        "#print sorries root_eq_actualCanonical\n"
        "#print axioms root_eq_actualCanonical\n"
        "set_option pp.explicit true in\n"
        "set_option pp.universes true in\n"
        "#print Canonical.Root\n"
    )
    body = body.replace(marker, identity + marker)
    imports = (
        "import Mathlib.Combinatorics.Additive.AP.Three.Behrend\n"
        "import Mathlib.Util.AssertNoSorry\n"
        "import Mathlib.Util.PrintSorries\n"
    )
    with tempfile.TemporaryDirectory(prefix="thm-m-0957-obligation-") as temp_dir:
        temporary = Path(temp_dir) / "Composed.lean"
        temporary.write_text(imports + statement + body, encoding="utf-8")
        return run_lean(temporary)


def main() -> None:
    if sys.flags.optimize:
        raise SystemExit("checker requires Python assertions")
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    statement = load("statement.json")
    anchor = load("anchor-audit.json")
    instance = load("instance.json")
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8")
    )

    expected = build_obligation_artifacts.build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"),
        expected,
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated file: {name}"

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert instance["theorem_id"] == THEOREM
    target = statement["canonical_formal_target"]
    assert instance["canonical_statement"] == statement["canonical_statement"]
    assert instance["canonical_claim"] == statement["canonical_statement"]
    assert instance["canonical_claim_status"] == statement["canonical_claim_status"]
    assert instance["canonical_formal_target"]["module"] == target["module"]
    assert instance["canonical_formal_target"]["declaration_or_expression"] == target[
        "declaration_or_expression"
    ]
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{target['elaborated_expression_sha256']}"
    )
    assert instance["canonical_formal_target"]["environment_fingerprint"] == statement[
        "environment_fingerprint"
    ]
    for field in (
        "domain_and_universes", "quantifiers", "ordered_binders", "hypotheses",
        "conclusion", "alternate_encodings", "foundation_profile", "tcb_profile",
        "computation_profile",
    ):
        assert instance[field] == statement[field], field
    assert instance["discovery_protocol_hash"] == (
        f"sha256:{sha256(HERE / 'anchor-discovery-protocol.json')}"
    )

    item = next(value for value in execution["items"] if value["id"] == ITEM)
    assert item["execution_rank"] == 1491 and item["phase"] == "obligation_tree"
    assert item["layer"] == 3 and item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0957-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == (
        "Freeze the obligation registry and typed proof/provenance/workflow graphs."
    )
    predecessor = next(
        value for value in execution["items"]
        if value["id"] == "S56-M-0957-ANCHOR_AUDIT"
    )
    assert predecessor["state"] == "[_]"

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")

    rows = registry["obligations"]
    ids = [value["obligation_id"] for value in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == len(build_obligation_artifacts.ROWS) == 45
    assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == ROOT_ID
    for value in rows:
        assert set(value) == REGISTRY_FIELDS
        assert value["root_relevant"] is True
        assert value["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert value["human_source_eligibility"] in {"required", "not_applicable"}
        assert value["readable_eligibility"] in {"required", "not_applicable"}
        assert value["risk_class"] in {"critical", "high", "normal", "low"}
        excluded = (
            value["machine_eligibility"] != "required"
            or value["human_source_eligibility"] != "required"
            or value["readable_eligibility"] != "required"
        )
        assert bool(value["exclusion_reason"]) == excluded, value["obligation_id"]

    projection = [
        {field: value[field] for field in (
            "obligation_id", "statement_fingerprint", "kind", "root_relevant",
            "machine_eligibility", "human_source_eligibility", "readable_eligibility",
            "risk_class", "exclusion_reason", "terminal_proof_body_id",
        )} for value in rows
    ]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    obligation_artifacts = {
        "ObligationTree.lean", "build_obligation_artifacts.py",
        "check_obligation_tree.py", "obligation-registry.json",
        "typed-graphs.json", "validation-specs.json", "obligation-tree.md",
        "obligation-tree-validation.md", "obligation-tree-receipt.json",
    }
    assert obligation_artifacts <= set(instance["owned_artifacts"])
    assert {
        f"Stage1_Instances/{THEOREM}/{name}" for name in obligation_artifacts
    } <= set(instance["public_merge_targets"])
    assert registry["frozen_denominators"]["inventory"] == ids
    for key, field, value in (
        ("required_machine", "machine_eligibility", "required"),
        ("required_human_source", "human_source_eligibility", "required"),
        ("required_readable", "readable_eligibility", "required"),
        ("informational_overlays", "machine_eligibility", "informational"),
    ):
        assert registry["frozen_denominators"][key] == [
            row["obligation_id"] for row in rows if row[field] == value
        ]
    assert registry["append_only_delta"] == []
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["accepted_root_machine_debt"] == "M3"
    assert set(registry["layer_applicability"]) == {
        "S_statement_foundation", "N_normalization", "B_branch", "C_construction",
        "L_core_lemma", "X_external_and_computation", "T_terminal_transport",
        "ROOT_exact_theorem",
    }
    layer_membership = {
        layer: set(value["obligation_ids"])
        for layer, value in registry["layer_applicability"].items()
    }
    assert set().union(*layer_membership.values()) == id_set
    assert layer_membership["N_normalization"] == {
        "M0957-N-SHARP-DIMENSION", "M0957-N-RPOW-EXP",
        "M0957-L-PROXY-RPOW-IDENTITY", "M0957-L-LINEAR-CEILING",
    }
    assert "M0957-N-INCLUSIVE-INDEX" in layer_membership["T_terminal_transport"]

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({value["node_id"] for value in nodes})
    assert {value["obligation_id"] for value in nodes} == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    all_step_ids = {
        step["step_id"] for value in nodes for step in value["semantic_step_ledger"]
    }
    allowed_external = {"frozen-formal-context", "pinned-mathlib-source"}
    for value in nodes:
        assert set(value) == NODE_FIELDS, value["obligation_id"]
        assert value["node_id"] == f"{THEOREM}-{value['obligation_id'].removeprefix('M0957-')}"
        assert value["human_debt"] in {f"H{index}" for index in range(6)}
        assert value["machine_debt"] in {
            "M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"
        }
        assert value["readability_debt"] in {f"R{index}" for index in range(5)}
        assert 0 < value["step_budget"] <= 100
        ledger = value["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= value["step_budget"]
        for step in ledger:
            assert set(step) == {
                "step_id", "premise_ids", "inference", "source_locator", "output",
                "outgoing_use",
            }
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            assert set(step["premise_ids"]) <= id_set | allowed_external | all_step_ids
            step_ids.add(step["step_id"])
        path, anchor_name = value["public_readable_target"].split("#", 1)
        assert path == f"Stage1_Instances/{THEOREM}/obligation-tree.md"
        assert f"### {anchor_name}" in readable
        assert value["validation_spec_id"] == "VAL-M0957-OBLIGATION-BUNDLE"
        assert value["validity"]["revocation_state"] == "not-accepted"
        assert "no m0" in value["status_boundary"].lower()
        assert value["task_ids"] and value["task_ids"][0] == ITEM
        assert value["evidence_ids"] == []
        if value["obligation_id"] in {
            "M0957-N-SHARP-DIMENSION", "M0957-L-RADIX-NONZERO",
            "M0957-L-RADIX-FLOOR", "M0957-L-AMBIENT-FIT", "M0957-N-RPOW-EXP",
            "M0957-L-PROXY-RPOW-IDENTITY", "M0957-L-PROXY-SLACK",
            "M0957-L-RECIPROCAL-CORE", "M0957-L-LINEAR-CEILING",
            "M0957-L-LINEAR-INCREMENT", "M0957-L-DIMENSION-SLACK",
            "M0957-L-LOG-DIMENSION",
        }:
            assert len(ledger) >= 4
            assert value["proof_budget_status"].startswith("unchecked_open_proof_plan")

    assert set(bundle["graphs"]) == GRAPH_NAMES
    assert "not claimed to be machine-extracted Lean expression hashes" in bundle[
        "statement_fingerprint_boundary"
    ]
    workflow_nodes = set(bundle["workflow_task_nodes"])
    assert workflow_nodes == {
        "S56-M-0957-INTAKE", "S56-M-0957-STATEMENT",
        "S56-M-0957-ANCHOR_AUDIT", ITEM, "S56-M-0957-PROOF",
        "S56-M-0957-VALIDATION", "S56-M-0957-RELEASE",
    }
    allowed_types_by_graph = {
        "proof": {"proof_requires", "composes"},
        "refinement": {
            "logical_decomposition", "expository_decomposition",
            "equivalent_to", "transports",
        },
        "provenance": {"source_map", "provenance_of"},
        "evidence": {"evidence_for"},
        "trust": {"trusts"},
        "documentation": {"documents"},
        "workflow": {"workflow_depends_on"},
    }
    edge_ids: set[str] = set()
    for graph_name, graph_value in bundle["graphs"].items():
        endpoints = workflow_nodes if graph_name == "workflow" else id_set
        assert set(graph_value["out"]) == endpoints
        assert set(graph_value["in"]) == endpoints
        directed = graph_value["edges"]
        if graph_name == "proof":
            directed = [value for value in directed if value["type"] == "proof_requires"]
        check_acyclic(directed)
        for value in graph_value["edges"]:
            assert value["edge_id"] not in edge_ids
            assert value["type"] in ALLOWED_EDGES
            assert value["type"] in allowed_types_by_graph[graph_name]
            assert value["from"] in endpoints and value["to"] in endpoints
            assert value["edge_id"] in graph_value["out"][value["from"]]
            assert value["edge_id"] in graph_value["in"][value["to"]]
            edge_ids.add(value["edge_id"])
        assert {
            key: sorted(value) for key, value in graph_value["out"].items()
        } == {
            key: sorted(edge["edge_id"] for edge in graph_value["edges"] if edge["from"] == key)
            for key in endpoints
        }
        assert {
            key: sorted(value) for key, value in graph_value["in"].items()
        } == {
            key: sorted(edge["edge_id"] for edge in graph_value["edges"] if edge["to"] == key)
            for key in endpoints
        }

    proof = {value["edge_id"]: value for value in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for value in proof.values():
        reverse = proof[value["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == value["edge_id"]
        assert (reverse["from"], reverse["to"]) == (value["to"], value["from"])
        assert {value["type"], reverse["type"]} == {"proof_requires", "composes"}
        if value["type"] == "proof_requires":
            children.setdefault(value["from"], []).append(value["to"])
    reachable: set[str] = set()

    def visit(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            visit(child)

    visit(ROOT_ID)
    assert reachable == EXPECTED_PROOF_REACHABLE
    required_proof = {
        value["obligation_id"] for value in rows
        if value["machine_eligibility"] == "required"
        and not value["obligation_id"].startswith("M0957-S-")
    }
    assert required_proof <= reachable

    provenance_edges = bundle["graphs"]["provenance"]["edges"]
    source_mapped = {
        value["to"] for value in provenance_edges if value["type"] == "source_map"
    }
    required_source_mapped = {
        value["obligation_id"] for value in rows
        if value["human_source_eligibility"] == "required"
        and value["obligation_id"] != "M0957-X-SOURCE"
    }
    assert source_mapped == required_source_mapped
    provenance_mapped = {
        value["to"] for value in provenance_edges if value["type"] == "provenance_of"
    }
    required_provenance_mapped = {
        value["obligation_id"] for value in rows
        if value["terminal_proof_body_id"] is not None
    } | set(build_obligation_artifacts.CERTIFICATES) | {
        "M0957-S-PREDICATE", "M0957-S-EXTREMAL", "M0957-N-INCLUSIVE-INDEX",
    }
    assert required_provenance_mapped <= provenance_mapped
    high_risk_open_children = {
        "M0957-L-PROXY-SLACK", "M0957-L-RECIPROCAL-CORE",
        "M0957-L-LINEAR-INCREMENT", "M0957-L-DIMENSION-SLACK",
        "M0957-L-LOG-DIMENSION",
    }
    risk_by_id = {value["obligation_id"]: value["risk_class"] for value in rows}
    assert {risk_by_id[identifier] for identifier in high_risk_open_children} == {"high"}

    certificates = {
        value["parent_obligation_id"]: value
        for value in bundle["composition_certificates"]
    }
    assert len(certificates) == len(bundle["composition_certificates"])
    fingerprints = {value["obligation_id"]: value["statement_fingerprint"] for value in rows}
    for parent, certificate in certificates.items():
        assert certificate["required_child_ids"] == children[parent]
        assert certificate["parent_statement_fingerprint"] == fingerprints[parent]
        assert certificate["required_child_statement_fingerprints"] == {
            child: fingerprints[child] for child in children[parent]
        }
        assert certificate["introduces_undeclared_premises"] is False
        assert certificate["status"] == "provisionally_elaborated_not_accepted"
        assert certificate["declaration"] == build_obligation_artifacts.CERTIFICATES[parent]
    assert {value["parent_obligation_id"] for value in bundle["unverified_decomposition_plans"]} == (
        set(children) - set(certificates)
    )

    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    expected_unimplemented_leaves = {
        "M0957-N-SHARP-DIMENSION", "M0957-L-RADIX-NONZERO",
        "M0957-L-RADIX-FLOOR", "M0957-L-AMBIENT-FIT", "M0957-N-RPOW-EXP",
        "M0957-L-PROXY-RPOW-IDENTITY", "M0957-L-PROXY-SLACK",
        "M0957-L-RECIPROCAL-CORE", "M0957-L-LINEAR-CEILING",
        "M0957-L-LINEAR-INCREMENT", "M0957-L-DIMENSION-SLACK",
        "M0957-L-LOG-DIMENSION",
    }
    expected_checked_candidate_leaves = {
        "M0957-T-CONSTRUCTION", "M0957-N-INCLUSIVE-INDEX",
    }
    expected_leaf_cut = expected_unimplemented_leaves | expected_checked_candidate_leaves
    assert set(closure["required_proof_leaf_ids"]) == expected_leaf_cut
    assert set(closure["unimplemented_proof_leaf_ids"]) == expected_unimplemented_leaves
    assert set(closure["checked_candidate_leaf_ids"]) == expected_checked_candidate_leaves
    assert closure["accepted_proof_leaf_ids"] == []
    assert set(closure["proof_leaf_cut_set"]) == expected_leaf_cut
    assert expected_leaf_cut <= set(closure["remaining_root_cut_set"])
    assert "M0957-L-OPTIMAL-EXPONENT" not in closure["remaining_root_cut_set"]

    assert len(specs["recipes"]) == 1
    recipe = specs["recipes"][0]
    assert recipe["recipe_id"] == "VAL-M0957-OBLIGATION-BUNDLE"
    assert recipe["cwd"] == "." and isinstance(recipe["argv"], list)
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert set(recipe["covered_obligation_ids"]) == id_set

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    mathlib_source = MATHLIB / "Mathlib/Combinatorics/Additive/AP/Three/Behrend.lean"
    assert sha256(mathlib_source) == MATHLIB_SOURCE_SHA256
    assert output(
        "git", "rev-parse", "HEAD:Mathlib/Combinatorics/Additive/AP/Three/Behrend.lean",
        cwd=MATHLIB,
    ) == MATHLIB_SOURCE_BLOB
    mathlib_text = mathlib_source.read_text(encoding="utf-8")
    for marker in (
        "def sphere", "def map", "theorem threeAPFree_image_sphere",
        "theorem card_sphere_le_rothNumberNat", "theorem exists_large_sphere",
        "theorem bound_aux", "theorem roth_lower_bound_explicit",
        "theorem roth_lower_bound",
    ):
        assert marker in mathlib_text, marker

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    clean = without_comments_and_strings(source)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque|implemented_by|"
        r"extern|native_decide|TODO|FIXME)\b"
    )
    assert forbidden.search(clean) is None
    for marker in (
        "def OptimalExponentBridgePackage : Prop", "def ExactAssembly : Prop",
        "theorem pinnedQuantitativeConstruction", "theorem pinnedIndexMonotonicity",
        "theorem parameterAdmissibility_of_dimension_and_radix",
        "theorem proxyLogLower_of_identity_and_slack",
        "theorem reciprocalLoss_of_balanced_core",
        "theorem linearLoss_of_ceiling_and_increment",
        "theorem subleadingLoss_of_dimension_and_log",
        "theorem proxyAsymptotic_of_dimension_and_bridge",
        "theorem optimalExponent_of_components",
        "theorem ratioAsymptotic_of_proxy_floor_and_dimension",
        "theorem sharpEstimate_of_normalization_and_ratio",
        "theorem sharpParameters_of_components", "theorem exactAssembly_of_children",
        "theorem root_of_quantitative_and_parameters", "theorem root_of_exactAssembly",
        "#print_obligation_closure",
    ):
        assert marker in source, marker

    standalone = run_lean(HERE / "ObligationTree.lean")
    if standalone.returncode:
        sys.stdout.write(standalone.stdout)
        raise SystemExit(standalone.returncode)
    composed = composed_lean()
    if composed.returncode:
        sys.stdout.write(composed.stdout)
        raise SystemExit(composed.returncode)
    combined_stdout = standalone.stdout + composed.stdout
    if os.environ.get("STAGE1_PRINT_LEAN_EVIDENCE") == "1":
        closure_match = re.search(r"OBLIGATION_CLOSURE declarations=(\d+)", standalone.stdout)
        print(
            "LEAN_EVIDENCE "
            f"standalone_sha256={hashlib.sha256(standalone.stdout.encode()).hexdigest()} "
            f"composed_sha256={hashlib.sha256(composed.stdout.encode()).hexdigest()} "
            f"combined_sha256={hashlib.sha256(combined_stdout.encode()).hexdigest()} "
            f"closure={closure_match.group(1) if closure_match else 'missing'}"
        , flush=True)
    assert "sorryAx" not in combined_stdout and "declaration uses 'sorry'" not in combined_stdout
    normalized = re.sub(r"\s+", " ", combined_stdout)
    expected_axioms = "[propext, Classical.choice, Quot.sound]"
    assert normalized.count(expected_axioms) >= 21
    for marker in (
        "Declarations are sorry-free!", "OBLIGATION_CLOSURE declarations=",
        "OBLIGATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]",
        "OBLIGATION_CLOSURE bodyless_nonaxioms=[]", "OBLIGATION_CLOSURE unsafe=[]",
        "root_eq_actualCanonical",
    ):
        assert marker in combined_stdout, marker

    receipt = load("obligation-tree-receipt.json")
    assert receipt["schema_version"] == "stage1-worker-obligation-tree-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids)
    assert receipt["required_machine_obligation_count"] == len(
        registry["frozen_denominators"]["required_machine"]
    )
    assert receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["architecture_ledger_step_count"] == len(step_ids)
    assert receipt["graph_edge_counts"] == {
        name: len(bundle["graphs"][name]["edges"]) for name in sorted(GRAPH_NAMES)
    }
    assert receipt["composition_certificate_count"] == len(certificates)
    assert receipt["unverified_decomposition_count"] == len(
        bundle["unverified_decomposition_plans"]
    )
    assert receipt["composition_declarations"] == [
        value["declaration"] for value in bundle["composition_certificates"]
    ]
    assert receipt["candidate_only_obligations"] == closure["candidate_only_obligations"]
    assert receipt["proof_leaf_cut_set"] == closure["proof_leaf_cut_set"]
    assert receipt["remaining_root_cut_set"] == closure["remaining_root_cut_set"]
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["lean_output_sha256"] == hashlib.sha256(
        combined_stdout.encode()
    ).hexdigest()
    assert set(receipt["artifact_sha256"]) == {
        "ObligationTree.lean", "build_obligation_artifacts.py",
        "check_obligation_tree.py", "obligation-registry.json",
        "obligation-tree-validation.md", "obligation-tree.md",
        "typed-graphs.json", "validation-specs.json",
    }
    for name, expected_hash in receipt["artifact_sha256"].items():
        assert sha256(HERE / name) == expected_hash, name

    if args.worker_packet:
        packet = json.loads(args.worker_packet.read_text(encoding="utf-8"))
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["commands"] == receipt["commands_and_results"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["commands"] and packet["output_summary"].startswith("PASS:")
        check_text_file(args.worker_packet)

    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)

    print(
        f"PASS THM-M-0957 obligation tree: {len(ids)} registry records, "
        f"{len(edge_ids)} typed edges, {len(step_ids)} architecture ledger steps"
    )
    print(f"registry denominator sha256: {denominator}")
    print(
        "Lean: conditional sharp compositions and pinned implicit construction elaborate; "
        "actual canonical identity checked; no placeholders"
    )
    print(
        "accepted root remains H1/M3/R3; accepted obligations 0; theorem_complete=false"
    )


if __name__ == "__main__":
    main()
