#!/usr/bin/env python3
"""Fail-closed structural and Lean checks for THM-M-0821 obligations."""

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
ITEM = "S56-M-0821-OBLIGATION_TREE"
THEOREM = "THM-M-0821"
BASE_REVISION = "a3b18eec39bf04be025b1641cae02f4d44fdf11a"
BASE_TREE = "fdfff18dea4c6798c5b322b6088dfe556109c134"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
STATEMENT_SHA256 = "572f1655ca4d40ce6e1ce1bf6567cee2d640eb54534569d8a8980dff184c0100"
ANCHOR_SHA256 = "050fae06052c03a8556804d2481e089ffb8e5095cd2baaf2b6e42ace5387c682"
ROOT_EXPRESSION = "8f5d05428a35e3b6f13947097ac52417ba900b3cf9b1b45c0bb173766c914d7c"
SOURCE_HASHES = {
    "Mathlib/Combinatorics/SetFamily/LYM.lean": "b19d4cbe58af9422dc36864d1ad1eee717c264a90d94fd579d3c8305f0feb630",
    "Mathlib/Data/Finset/Slice.lean": "5a3986375f5c0035f8c66760ce41bd66582ac34007d910d56a4e3535cc48cec8",
    "Mathlib/Data/Finset/Powerset.lean": "8258811b25be77c6eb5ac680775a2e2665735d646d14de793a257992cd66b032",
    "Mathlib/Combinatorics/Enumerative/DoubleCounting.lean": "38c650047b9081d623eea8f3da6863cb273e391bcab7ab6be06e17a39dc44382",
}
RECEIPT_SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md": "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md": "skills/execute-stage1-rev56/SKILL.md",
    "Formalizations/Lean/lean-toolchain": "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json": "Formalizations/Lean/lake-manifest.json",
    "Stage1_Instances/THM-M-0821/Statement.lean": "Stage1_Instances/THM-M-0821/Statement.lean",
    "Stage1_Instances/THM-M-0821/statement.json": "Stage1_Instances/THM-M-0821/statement.json",
    "Stage1_Instances/THM-M-0821/anchor-audit.json": "Stage1_Instances/THM-M-0821/anchor-audit.json",
}
REGISTRY_FILES = {
    "obligation-registry.json",
    "typed-graphs.json",
    "validation-specs.json",
    "obligation-tree.md",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0821/ObligationTree.lean",
    "Stage1_Instances/THM-M-0821/build_obligation_artifacts.py",
    "Stage1_Instances/THM-M-0821/check_obligation_tree.py",
    "Stage1_Instances/THM-M-0821/obligation-registry.json",
    "Stage1_Instances/THM-M-0821/typed-graphs.json",
    "Stage1_Instances/THM-M-0821/validation-specs.json",
    "Stage1_Instances/THM-M-0821/obligation-tree.md",
    "Stage1_Instances/THM-M-0821/obligation-tree-receipt.json",
    "Stage1_Instances/THM-M-0821/obligation-tree-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def acyclic(edges: list[dict], ignored_types: set[str] | None = None) -> None:
    ignored_types = ignored_types or set()
    adjacency: dict[str, list[str]] = {}
    for item in edges:
        if item["type"] not in ignored_types:
            adjacency.setdefault(item["from"], []).append(item["to"])
    active: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        if node in active:
            raise AssertionError(f"cycle at {node}")
        if node in done:
            return
        active.add(node)
        for child in adjacency.get(node, []):
            visit(child)
        active.remove(node)
        done.add(node)

    for node in adjacency:
        visit(node)


def check_text(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert not any(line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path}"


def run_lean() -> str:
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    lean_bin = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0821-obligation-") as temporary:
        statement = subprocess.run(
            [lean_bin, "Statement.lean", "-o", str(Path(temporary) / "Statement.olean")],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        result = subprocess.run(
            ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0821/ObligationTree.lean"],
            cwd=LEAN_ROOT,
            env=os.environ | {"LEAN_PATH": temporary + os.pathsep + lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
            check=False,
        )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def serialized_definitions(lean_output: str) -> dict[str, str]:
    namespace = "Stage1Instances.THM_M_0821_Obligations."
    names = [
        "AttainmentPackage", "UpperBoundPackage", "MiddleLayerDefinitionPackage",
        "MiddleLayerSizedPackage", "MiddleLayerAntichainPackage",
        "MiddleLayerCardinalityPackage", "MaximumSplit",
    ]
    result: dict[str, str] = {}
    for index, name in enumerate(names):
        marker = f"def {namespace}{name}"
        start = lean_output.rfind(marker)
        assert start >= 0, marker
        later = [lean_output.find(f"def {namespace}{other}", start + len(marker)) for other in names[index + 1:]]
        end_candidates = [position for position in later if position >= 0]
        end = min(end_candidates) if end_candidates else len(lean_output)
        serialized = lean_output[start:end].strip()
        assert "?m." not in serialized and " : Prop :=" in serialized
        result[name] = "lean-expression-sha256:" + hashlib.sha256(serialized.encode()).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    registry = load(HERE / "obligation-registry.json")
    bundle = load(HERE / "typed-graphs.json")
    specs = load(HERE / "validation-specs.json")
    receipt_path = HERE / "obligation-tree-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None

    expected_registry, expected_bundle, expected_specs, expected_markdown = build_obligation_artifacts.build()
    assert (HERE / "obligation-registry.json").read_bytes() == canonical_json(expected_registry), "stale obligation registry"
    assert (HERE / "typed-graphs.json").read_bytes() == canonical_json(expected_bundle), "stale typed graph bundle"
    assert (HERE / "validation-specs.json").read_bytes() == canonical_json(expected_specs), "stale validation specifications"
    assert (HERE / "obligation-tree.md").read_text(encoding="utf-8") == expected_markdown, "stale readable obligation tree"

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert {registry["item_id"], bundle["item_id"], specs["item_id"]} == {ITEM}
    assert {registry["theorem_id"], bundle["theorem_id"], specs["theorem_id"]} == {THEOREM}
    assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0821-OBLIGATIONS-v2"
    assert registry["registry_version"] == 2
    assert registry["append_only_delta"] == [{
        "from_registry_id": "THM-M-0821-OBLIGATIONS-v1",
        "from_denominator_sha256": "5c2062c82371b379919339f413619d88b6c4c1e08c79acf4f3c89022f2adafaf",
        "from_inventory_count": 35,
        "to_registry_id": "THM-M-0821-OBLIGATIONS-v2",
        "to_denominator_sha256": registry["denominator_sha256"],
        "to_inventory_count": 36,
        "added_obligation_ids": ["M0821-L-FALLING-ZERO"],
        "removed_obligation_ids": [],
        "changed_existing_obligation_ids": [
            row["obligation_id"] for row in registry["obligations"]
            if row["obligation_id"] != "M0821-L-FALLING-ZERO"
            and row["statement_fingerprint"].startswith("planned:v2:")
        ],
        "reason": "Add the previously hidden falling-zero estimate and re-fingerprint every planned signature after exact formal-target and ledger correction; the root expression is unchanged.",
        "status_effect": "No obligation closes and accepted H1/M3/R4 remains unchanged.",
    }]
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert sha256(HERE / "Statement.lean") == registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "anchor-audit.json") == registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256

    target_manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1379 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0821-ANCHOR_AUDIT"]
    assert item["owned_paths"] == ["Stage1_Instances/THM-M-0821"]
    prerequisite = next(row for row in execution["items"] if row["id"] == "S56-M-0821-ANCHOR_AUDIT")
    assert prerequisite["state"] == "[_]"
    local_dag = load(HERE / "task-dag.json")
    local_item = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_item["state"] == "open" and local_dag["accepted_states"] == []

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 36
    assert registry["root_obligation_id"] == "M0821-ROOT"
    assert bundle["root_node_id"] == "THM-M-0821-ROOT"
    required_obligation = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    }
    for row in rows:
        assert set(row) == required_obligation
        assert row["root_relevant"] is True
        assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] in {"required", "not_applicable"}
        assert row["risk_class"] in {"critical", "high", "normal", "low"}
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
            or row["readable_eligibility"] != "required"
        )
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending_independent_approval" in row["exclusion_reason"]
    assert rows[0]["statement_fingerprint"] == "lean-expression-sha256:" + ROOT_EXPRESSION
    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in fields} for row in rows]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for denominator_key, eligibility_key, expected in (
        ("required_machine", "machine_eligibility", "required"),
        ("required_human_source", "human_source_eligibility", "required"),
        ("required_readable", "readable_eligibility", "required"),
    ):
        assert registry["frozen_denominators"][denominator_key] == [
            row["obligation_id"] for row in rows if row[eligibility_key] == expected
        ]
    assert set(registry["layer_exclusions"]) == {"additional_normalization", "additional_case_splits"}
    assert all(value["status"].endswith("pending_independent_approval") for value in registry["layer_exclusions"].values())
    assert set(registry["proof_body_aliases"].values()) == {
        "deduplicated_to:Finset.local_lubell_yamamoto_meshalkin_inequality_div",
        "deduplicated_to:Finset.local_lubell_yamamoto_meshalkin_inequality_mul",
        "deduplicated_to:Finset.lubell_yamamoto_meshalkin_inequality_sum_card_div_choose",
    }
    status = registry["status_observed_after_freeze"]
    assert status["closed_obligations"] == [] and status["accepted_root_machine_debt"] == "M3"
    assert "E2" in status["candidate_route"] and "M1 candidate status" in status["candidate_route"]

    nodes = bundle["nodes"]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    assert len(nodes) == len(node_by_id) == len(ids) and set(node_by_id) == id_set
    required_node = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target",
        "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
        "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
        "computation_record", "step_budget", "semantic_step_ledger",
        "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
        "owned_sources", "owner", "reviewer", "validity",
    }
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    for node in nodes:
        assert set(node) == required_node
        assert node["node_id"] == THEOREM + "-" + node["obligation_id"].removeprefix("M0821-")
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["machine_debt"] not in {"M0-L", "M0-W", "M0-P", "M1", "M2"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"]
        for step in ledger:
            assert set(step) == {"step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"}
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"] and step["output"] and step["outgoing_use"]
            step_ids.add(step["step_id"])
        path, anchor = node["public_readable_target"].split("#", 1)
        assert path == "Stage1_Instances/THM-M-0821/obligation-tree.md"
        assert f"### {anchor}" in readable
        assert node["validation_spec_id"] == "VAL-M0821-OBLIGATION-BUNDLE"
        assert node["task_ids"] == [ITEM]
        assert node["validity"]["revocation_state"] == "not-accepted"
        assert "no m0" in node["status_boundary"].lower()
    allowed_external = {"frozen-formal-context"}
    for node in nodes:
        for step in node["semantic_step_ledger"]:
            assert set(step["premise_ids"]) <= id_set | step_ids | allowed_external

    assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
    allowed_edges = {
        "proof_requires", "composes", "logical_decomposition", "source_map",
        "expository_decomposition", "equivalent_to", "transports", "evidence_for",
        "provenance_of", "documents", "trusts", "trusted_by", "refines",
        "workflow_depends_on",
    }
    workflow_nodes = set(bundle["workflow_task_nodes"])
    assert workflow_nodes == {
        "S56-M-0821-ANCHOR_AUDIT", ITEM, "S56-M-0821-PROOF",
        "S56-M-0821-VALIDATION", "S56-M-0821-RELEASE",
    }
    edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        expected_in: dict[str, list[str]] = {}
        expected_out: dict[str, list[str]] = {}
        for item in graph["edges"]:
            assert item["edge_id"] not in edge_ids and item["type"] in allowed_edges
            endpoints = workflow_nodes if name == "workflow" else id_set
            assert item["from"] in endpoints and item["to"] in endpoints
            if name == "workflow":
                assert item["type"] == "workflow_depends_on"
            else:
                assert item["type"] != "workflow_depends_on"
            expected_out.setdefault(item["from"], []).append(item["edge_id"])
            expected_in.setdefault(item["to"], []).append(item["edge_id"])
            edge_ids.add(item["edge_id"])
        assert graph["out"] == expected_out and graph["in"] == expected_in
        if name not in {"proof", "refinement", "trust"}:
            acyclic(graph["edges"])
    inverse_edge_types = {
        "logical_decomposition": "refines",
        "refines": "logical_decomposition",
        "expository_decomposition": "documents",
        "documents": "expository_decomposition",
        "equivalent_to": "equivalent_to",
        "trusts": "trusted_by",
        "trusted_by": "trusts",
    }
    assert bundle["reciprocal_edge_type_contract"] == {
        "proof": {
            "proof_requires": ["composes", "logical_decomposition"],
            "composes": ["proof_requires"],
            "logical_decomposition": ["proof_requires"],
        },
        "refinement": {
            "logical_decomposition": ["refines"],
            "refines": ["logical_decomposition"],
            "expository_decomposition": ["documents"],
            "documents": ["expository_decomposition"],
            "equivalent_to": ["equivalent_to"],
        },
        "trust": {"trusts": ["trusted_by"], "trusted_by": ["trusts"]},
    }
    assert set(inverse_edge_types) == {
        "logical_decomposition", "refines", "expository_decomposition", "documents",
        "equivalent_to", "trusts", "trusted_by",
    }
    for graph_name in ("refinement", "trust"):
        graph = bundle["graphs"][graph_name]
        by_id = {item["edge_id"]: item for item in graph["edges"]}
        for item in graph["edges"]:
            assert set(item) == {
                "edge_id", "from", "type", "to", "reciprocal_edge_id",
            }
            reverse = by_id[item["reciprocal_edge_id"]]
            assert reverse["reciprocal_edge_id"] == item["edge_id"]
            assert (reverse["from"], reverse["to"]) == (item["to"], item["from"])
            assert reverse["type"] == inverse_edge_types[item["type"]]
    assert {
        (item["from"], item["type"], item["to"])
        for item in bundle["graphs"]["refinement"]["edges"]
    } == {
        ("M0821-ROOT", "logical_decomposition", "M0821-S-INTERFACE"),
        ("M0821-S-INTERFACE", "refines", "M0821-ROOT"),
        ("M0821-ROOT", "logical_decomposition", "M0821-S-BOUNDARY"),
        ("M0821-S-BOUNDARY", "refines", "M0821-ROOT"),
        ("M0821-ROOT", "equivalent_to", "M0821-S-TRANSPORT"),
        ("M0821-S-TRANSPORT", "equivalent_to", "M0821-ROOT"),
        ("M0821-ROOT", "logical_decomposition", "M0821-N-LOWER-MIDDLE"),
        ("M0821-N-LOWER-MIDDLE", "refines", "M0821-ROOT"),
        ("M0821-ROOT", "expository_decomposition", "M0821-N-NO-OTHER"),
        ("M0821-N-NO-OTHER", "documents", "M0821-ROOT"),
        ("M0821-ROOT", "expository_decomposition", "M0821-B-NO-CASES"),
        ("M0821-B-NO-CASES", "documents", "M0821-ROOT"),
    }
    assert {
        (item["from"], item["type"], item["to"])
        for item in bundle["graphs"]["trust"]["edges"]
    } == {
        ("M0821-ROOT", "trusts", "M0821-S-FOUNDATION"),
        ("M0821-S-FOUNDATION", "trusted_by", "M0821-ROOT"),
        ("M0821-ROOT", "trusts", "M0821-X-TRUST"),
        ("M0821-X-TRUST", "trusted_by", "M0821-ROOT"),
    }

    candidate_nodes = {
        node["obligation_id"] for node in nodes
        if node["evidence_ids"] or node["provenance_id"] != "none"
    }
    assert candidate_nodes == build_obligation_artifacts.ANCHOR_EVIDENCE_OBLIGATIONS
    for node in nodes:
        is_candidate = node["obligation_id"] in candidate_nodes
        assert node["evidence_ids"] == (["M0821-C01-E2-UNACCEPTED"] if is_candidate else [])
        assert node["provenance_id"] == ("PROV-M0821-C01-PARTIAL" if is_candidate else "none")

    proof = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for item in proof.values():
        reverse = proof[item["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == item["edge_id"]
        assert (reverse["from"], reverse["to"]) == (item["to"], item["from"])
        assert "proof_requires" in {item["type"], reverse["type"]}
        other = reverse["type"] if item["type"] == "proof_requires" else item["type"]
        parent = item["from"] if item["type"] == "proof_requires" else item["to"]
        expected_reverse = "composes" if parent in build_obligation_artifacts.CHECKED_PARENTS else "logical_decomposition"
        assert other == expected_reverse
        if item["type"] == "proof_requires":
            children.setdefault(item["from"], []).append(item["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(oid: str) -> None:
        assert oid not in visiting, f"proof cycle at {oid}"
        if oid in visited:
            return
        visiting.add(oid)
        for child in children.get(oid, []):
            visit(child)
        visiting.remove(oid)
        visited.add(oid)

    visit("M0821-ROOT")
    expected_reachable = set(build_obligation_artifacts.REQUIRES)
    expected_reachable.update(child for values in build_obligation_artifacts.REQUIRES.values() for child in values)
    assert visited == expected_reachable
    for parent in id_set:
        required_children = children.get(parent, [])
        ledger_obligation_premises = {
            premise
            for step in node_by_id[parent]["semantic_step_ledger"]
            for premise in step["premise_ids"]
            if premise in id_set
        }
        assert ledger_obligation_premises == set(required_children), (
            parent, ledger_obligation_premises, set(required_children)
        )

    certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
    assert set(certificates) == set(build_obligation_artifacts.CHECKED_PARENTS)
    obligation_by_id = {row["obligation_id"]: row for row in rows}
    for parent, certificate in certificates.items():
        assert certificate["required_child_ids"] == children[parent]
        assert certificate["parent_statement_fingerprint"] == obligation_by_id[parent]["statement_fingerprint"]
        assert certificate["required_child_statement_fingerprints"] == {
            child: obligation_by_id[child]["statement_fingerprint"] for child in children[parent]
        }
        assert certificate["certificate_kind"] == "lean_abstract_child_harness"
        assert certificate["checked_declaration"] == build_obligation_artifacts.CHECKED_PARENTS[parent][0]
        assert certificate["status"] == "provisionally_elaborated_not_accepted"
        assert certificate["introduces_undeclared_premises"] is False
    plans = {row["parent_obligation_id"]: row for row in bundle["unverified_decomposition_plans"]}
    assert set(plans) == set(children) - set(certificates)
    for parent, plan in plans.items():
        assert plan["planned_child_ids"] == children[parent]
        assert plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        assert "exact abstract-child harness" in plan["required_future_certificate"]

    closure = bundle["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert set(closure["proof_leaf_cut_set"]) == visited - set(children)
    assert closure["mandatory_root_overlay_cut_set"] == [
        "M0821-S-INTERFACE", "M0821-S-BOUNDARY", "M0821-S-TRANSPORT",
        "M0821-S-FOUNDATION", "M0821-N-LOWER-MIDDLE",
    ]
    assert set(closure["mandatory_root_overlay_cut_set"]) <= set(closure["remaining_root_cut_set"])
    assert "M0821-C01/E2" in closure["candidate_evidence"] and "current candidate status is M1" in closure["candidate_evidence"]

    recipes = specs["recipes"]
    assert len(recipes) == 1
    recipe = recipes[0]
    assert recipe["recipe_id"] == "VAL-M0821-OBLIGATION-BUNDLE"
    assert recipe["argv"] == ["python3", "-B", "Stage1_Instances/THM-M-0821/check_obligation_tree.py"]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert set(recipe["covered_obligation_ids"]) == id_set
    assert "kernel declaration coverage is limited" in recipe["coverage_boundary"]
    assert set(recipe["env_allowlist"]) == {"PATH", "HOME", "TMPDIR", "PYTHONDONTWRITEBYTECODE"}

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    for relative, expected in SOURCE_HASHES.items():
        assert sha256(MATHLIB / relative) == expected, relative
    lym = (MATHLIB / "Mathlib/Combinatorics/SetFamily/LYM.lean").read_text(encoding="utf-8")
    for marker in (
        "theorem local_lubell_yamamoto_meshalkin_inequality_mul",
        "theorem local_lubell_yamamoto_meshalkin_inequality_div",
        "def falling",
        "theorem slice_union_shadow_falling_succ",
        "theorem IsAntichain.disjoint_slice_shadow_falling",
        "theorem le_card_falling_div_choose",
        "induction k with",
        "theorem lubell_yamamoto_meshalkin_inequality_sum_card_div_choose",
        "theorem lubell_yamamoto_meshalkin_inequality_sum_inv_choose",
        "sum_fiberwise_of_maps_to'",
        "theorem _root_.IsAntichain.sperner",
        "choose_le_middle _ _",
    ):
        assert marker in lym, marker

    lean_source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", lean_source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|implemented_by|opaque)\b", without_comments)
    for marker in (
        "import Statement",
        "def AttainmentPackage : Prop",
        "def UpperBoundPackage : Prop",
        "theorem middleLayerAntichain_of_sized",
        "theorem attainment_of_middleLayer",
        "theorem upperBound_of_sperner",
        "theorem maximumSplit_of_packages",
        "theorem compose_root",
        "theorem root_of_terminal",
        "#print sorries IsAntichain.sperner",
        "#print axioms compose_root",
        "#print axioms root_of_terminal",
        "#check Finset.falling",
        "#check Finset.mem_falling",
        "#check Finset.sized_falling",
        "#check Finset.slice_subset_falling",
        "#check Finset.falling_zero_subset",
        "#check Finset.slice_union_shadow_falling_succ",
        "#check Finset.IsAntichain.disjoint_slice_shadow_falling",
        "#check Finset.sum_fiberwise_of_maps_to'",
        "#check Set.Sized.card_le",
        "#check Finset.shadow",
        "#check Finset.mem_shadow_iff",
        "#check Finset.erase_mem_shadow",
        "#check Finset.mem_shadow_iff_insert_mem",
        "#check Set.Sized.shadow",
        "#check Finset.sized_shadow_iff",
        "#check Finset.card_mul_le_card_mul'",
        "#check Finset.mem_bipartiteBelow",
        "#check Finset.mem_bipartiteAbove",
    ):
        assert marker in lean_source, marker
    lean_output = run_lean()
    assert "Declarations are sorry-free!" in lean_output
    assert "sorryAx" not in lean_output and "declaration uses 'sorry'" not in lean_output
    normalized = re.sub(r"\s+", " ", lean_output)
    assert normalized.count("propext, Classical.choice, Quot.sound") == 7
    assert normalized.count("propext, Quot.sound") == 4
    for declaration in (
        "IsAntichain.sperner", "pinned_middleLayerDefinition",
        "pinned_middleLayerSized", "pinned_middleLayerCardinality",
        "pinned_upperBound", "middleLayerAntichain_of_sized",
        "attainment_of_middleLayer", "upperBound_of_sperner",
        "maximumSplit_of_packages", "compose_root",
        "root_of_terminal",
        "Finset.falling", "Finset.mem_falling", "Finset.sized_falling",
        "Finset.slice_subset_falling",
        "Finset.falling_zero_subset", "Finset.slice_union_shadow_falling_succ",
        "Finset.IsAntichain.disjoint_slice_shadow_falling",
        "Finset.sum_fiberwise_of_maps_to'", "Set.Sized.card_le",
        "Finset.shadow", "Finset.mem_shadow_iff", "Set.Sized.shadow",
        "Finset.erase_mem_shadow", "Finset.mem_shadow_iff_insert_mem",
        "Finset.sized_shadow_iff", "Finset.bipartiteBelow",
        "Finset.bipartiteAbove", "Finset.mem_bipartiteBelow",
        "Finset.mem_bipartiteAbove", "Finset.card_mul_le_card_mul'",
    ):
        assert declaration in lean_output
    lean_output_sha256 = hashlib.sha256(lean_output.encode()).hexdigest()
    serialized = serialized_definitions(lean_output)
    interface_nodes = {
        "M0821-ROOT": "root",
        "M0821-T-ROOT-COMPOSE": "root",
        "M0821-B-MAXIMUM": "MaximumSplit",
        "M0821-T-ATTAIN": "AttainmentPackage",
        "M0821-C-MIDDLE-LAYER": "MiddleLayerDefinitionPackage",
        "M0821-L-MIDDLE-ANTICHAIN": "MiddleLayerAntichainPackage",
        "M0821-C-MIDDLE-SIZED": "MiddleLayerSizedPackage",
        "M0821-L-MIDDLE-CARD": "MiddleLayerCardinalityPackage",
        "M0821-T-UPPER": "UpperBoundPackage",
        "M0821-L-SPERNER-UPPER": "UpperBoundPackage",
    }
    for oid, name in interface_nodes.items():
        expected = "lean-expression-sha256:" + ROOT_EXPRESSION if name == "root" else serialized[name]
        actual = bundle["interface_expression_fingerprints"][oid]
        if actual != "PENDING_LEAN_EXPRESSION":
            assert actual == expected
    for parent, certificate in certificates.items():
        assert certificate["parent_interface_expression_fingerprint"] == bundle["interface_expression_fingerprints"][parent]
        assert certificate["required_child_interface_expression_fingerprints"] == {
            child: bundle["interface_expression_fingerprints"][child] for child in children[parent]
        }

    if receipt is not None:
        assert receipt["schema_version"] == "stage1-worker-obligation-tree-receipt/1.0"
        assert receipt["receipt_id"] == "S56-M-0821-OBLIGATION-TREE-WORKER-20260713"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["phase"] == receipt["intent"] == "obligation_tree"
        assert receipt["receipt_class"] == "provisional_worker_selftest"
        assert receipt["acceptance_authority"] == "Stage1 integration lane"
        assert receipt["content_addressed"] is False
        assert receipt["content_addressed_recipe_ids"] == []
        assert receipt["content_addressed_receipt_ids"] == []
        assert receipt["recipe_ids"] == ["VAL-M0821-OBLIGATION-BUNDLE"]
        assert receipt["self_hash_boundary"].startswith("The receipt file is excluded")
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["registry_version"] == registry["registry_version"]
        if receipt["registry_denominator_sha256"] != "PENDING":
            assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
        assert receipt["candidate_current_classification"] == "M1"
        assert receipt["candidate_potential_classification"] == "M0-W_requires_E1"
        assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
        if receipt["obligation_count"] != 0:
            assert receipt["obligation_count"] == len(ids)
        if receipt["typed_edge_count"] != 0:
            assert receipt["typed_edge_count"] == len(edge_ids)
        if receipt["substantive_ledger_step_count"] != 0:
            assert receipt["substantive_ledger_step_count"] == len(step_ids)
        assert receipt["composition_certificate_count"] == len(certificates)
        assert receipt["unverified_internal_decomposition_count"] == len(plans)
        assert receipt["closed_obligations"] == []
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
        if receipt["lean_output_sha256"] != "PENDING":
            assert receipt["lean_output_sha256"] == lean_output_sha256
        assert receipt["source_inputs"] == {
            key: "sha256:" + sha256(ROOT / relative)
            for key, relative in RECEIPT_SOURCE_INPUTS.items()
        }
        assert receipt["repository_dirty_state"]["release_eligible"] is False
        assert receipt["repository_dirty_state"]["initial_status_sha256"] == (
            "sha256:8c616a936e1f6b2689a8955b4904494d5639a105b14cc0154b8805f96d28e97e"
        )
        assert receipt["worker_packet_sha256"] == (
            "sha256:" + sha256(ROOT / ".stage1-worker-selftest.json")
        )
        assert receipt["started_at"] < receipt["ended_at"]
        assert receipt["attestor"] and receipt["platform"]["lean"] and receipt["platform"]["python"]
        assert receipt["support_state"].startswith("provisional")
        assert receipt["review_due"] and receipt["freshness_policy"]
        assert receipt["invalidation_inputs"] and receipt["revocation_state"] and receipt["incident_procedure"]
        assert receipt["commands_and_results"] and all(
            isinstance(command["argv"], list)
            and command["argv"]
            and command["exit_code"] == 0
            and command["result"]
            for command in receipt["commands_and_results"]
        )
        assert receipt["commands_and_results"][3]["result"] == (
            f"{len(ids)} obligations; {len(edge_ids)} typed edges; denominator {denominator}"
        )
        if receipt["artifact_hashes"] != {}:
            assert receipt["artifact_hashes"] == {
                name: "sha256:" + sha256(HERE / name)
                for relative in sorted(CHANGED_PATHS)
                if relative.startswith("Stage1_Instances/THM-M-0821/")
                for name in [relative.removeprefix("Stage1_Instances/THM-M-0821/")]
                if name != "obligation-tree-receipt.json" and (HERE / name).exists()
            }

    if args.worker_packet is not None:
        if receipt is None:
            raise SystemExit("worker packet requires finalized receipt")
        packet = load(args.worker_packet)
        assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["commands"] and packet["output_summary"]

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        if (ROOT / relative).exists():
            check_text(ROOT / relative)

    print(
        f"PASS THM-M-0821 obligation tree: {len(ids)} obligations, "
        f"{len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps, "
        f"{len(certificates)} composition certificates, {len(plans)} unverified internal plans"
    )
    print(f"registry denominator sha256: {denominator}")
    print(f"Lean output sha256: {lean_output_sha256}")
    print("Lean: exact package interfaces and compositions elaborate; IsAntichain.sperner is sorry-free; candidate axioms propext, Classical.choice, Quot.sound")
    print("accepted root remains H1/M3/R4; closed obligations 0; audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
