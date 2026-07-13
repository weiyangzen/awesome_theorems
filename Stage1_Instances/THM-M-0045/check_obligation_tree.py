#!/usr/bin/env python3
"""Fail-closed structural and Lean check for THM-M-0045 obligation artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import build_obligation_artifacts as builder


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB = LEAN_ROOT / ".lake/packages/mathlib"
ITEM = "S56-M-0045-OBLIGATION_TREE"
THEOREM = "THM-M-0045"
BASE_REVISION = "7d0965498598e684e3e3d0a01836c2bf36a02959"
BASE_TREE = "753e16a89fce09f051af066f8b58d3e6b2722ade"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXTERNAL_REVISION = "0a539f0ce764fd16726509b62ed7b870461070eb"
EXTERNAL_SOURCE_PATH = "Mathlib/LinearAlgebra/Matrix/SchurTriangulation.lean"
EXTERNAL_SOURCE_SHA256 = "8fc4d47249d8bcc75c02fedc6d9b0008f7c0127c501f608d4226a7f5872f4bc3"


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def output(*argv: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def check_acyclic(edges: list[dict], endpoints: set[str]) -> None:
    adjacency: dict[str, list[str]] = {}
    for row in edges:
        adjacency.setdefault(row["from"], []).append(row["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        assert node not in visiting, f"cycle at {node}"
        if node in visited:
            return
        visiting.add(node)
        for target in adjacency.get(node, []):
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for endpoint in endpoints:
        visit(endpoint)


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    instance = load("instance.json")
    task_dag = load("task-dag.json")
    receipt_path = HERE / "obligation-tree-receipt.json"
    receipt = load("obligation-tree-receipt.json") if receipt_path.exists() else None

    expected_registry, expected_bundle, expected_specs = (
        builder.registry, builder.bundle, builder.recipes
    )
    for name, value in (
        ("obligation-registry.json", expected_registry),
        ("typed-graphs.json", expected_bundle),
        ("validation-specs.json", expected_specs),
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())
    manifest = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1085
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1085
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0045-ANCHOR_AUDIT"]
    assert item["owned_paths"] == ["Stage1_Instances/THM-M-0045"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == len(builder.SPECS) == 37
    assert ids[0] == registry["root_obligation_id"] == "M0045-ROOT"
    required_registry_fields = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    }
    for row in rows:
        assert set(row) == required_registry_fields
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
            or row["readable_eligibility"] != "required"
        )
        assert (row["exclusion_reason"] is not None) == excluded

    projection = [{field: row[field] for field in builder.DENOMINATOR_FIELDS} for row in rows]
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
    assert registry["layer_exclusions"]["computation"]["status"].endswith("pending_independent_approval")
    assert registry["status_observed_after_freeze"]["closed_obligations"] == []

    required_node_fields = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
        "human_debt", "machine_debt", "readability_debt", "evidence_ids",
        "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
        "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
        "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
        "reviewer", "validity",
    }
    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == id_set
    assert bundle["root_node_id"] == "THM-M-0045-ROOT"
    assert bundle["root_node_id"] in {node["node_id"] for node in nodes}
    ledger_step_ids: set[str] = set()
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    for node in nodes:
        assert set(node) == required_node_fields
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert node["semantic_step_ledger"]
        for step in node["semantic_step_ledger"]:
            assert set(step) == {"step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"}
            assert step["step_id"] not in ledger_step_ids and step["premise_ids"]
            assert step["inference"] and step["source_locator"] and step["output"] and step["outgoing_use"]
            ledger_step_ids.add(step["step_id"])
        path, anchor = node["public_readable_target"].split("#", 1)
        assert path == "Stage1_Instances/THM-M-0045/obligation-tree.md"
        assert f"### {anchor}" in readable
        assert node["validation_spec_id"] == "VAL-M0045-OBLIGATION-BUNDLE"
        assert node["task_ids"] == [ITEM]
        assert node["validity"]["revocation_state"] == "not-accepted"

    allowed_premises = {"frozen-formal-context"}
    for node in nodes:
        for step in node["semantic_step_ledger"]:
            assert set(step["premise_ids"]) <= id_set | ledger_step_ids | allowed_premises

    assert set(bundle["graphs"]) == {
        "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
    }
    allowed_edges = {
        "proof_requires", "composes", "logical_decomposition", "source_map", "transports",
        "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on",
    }
    workflow_nodes = set(bundle["workflow_task_nodes"])
    edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        expected_in: dict[str, list[str]] = {}
        expected_out: dict[str, list[str]] = {}
        endpoints = workflow_nodes if name == "workflow" else id_set
        for row in graph["edges"]:
            assert row["edge_id"] not in edge_ids and row["type"] in allowed_edges
            assert row["from"] in endpoints and row["to"] in endpoints
            assert (row["type"] == "workflow_depends_on") == (name == "workflow")
            expected_out.setdefault(row["from"], []).append(row["edge_id"])
            expected_in.setdefault(row["to"], []).append(row["edge_id"])
            edge_ids.add(row["edge_id"])
        assert graph["out"] == expected_out and graph["in"] == expected_in

    for name in ("refinement", "provenance", "evidence", "trust", "documentation", "workflow"):
        check_acyclic(bundle["graphs"][name]["edges"], workflow_nodes if name == "workflow" else id_set)

    proof = {row["edge_id"]: row for row in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for row in proof.values():
        assert row["type"] in {"proof_requires", "composes", "logical_decomposition"}
        reverse = proof[row["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == row["edge_id"]
        assert (reverse["from"], reverse["to"]) == (row["to"], row["from"])
        assert "proof_requires" in {row["type"], reverse["type"]}
        if row["type"] == "proof_requires":
            children.setdefault(row["from"], []).append(row["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        assert node not in visiting, f"proof cycle at {node}"
        if node in visited:
            return
        visiting.add(node)
        for child in children.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)

    visit("M0045-ROOT")
    expected_reachable = {"M0045-ROOT"} | set(children) | {
        child for values in children.values() for child in values
    }
    assert visited == expected_reachable == {"M0045-ROOT", "M0045-T-PACKAGE"}

    certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
    assert set(certificates) == {"M0045-ROOT"}
    certificate = certificates["M0045-ROOT"]
    assert certificate["required_child_ids"] == children["M0045-ROOT"] == ["M0045-T-PACKAGE"]
    assert certificate["introduces_undeclared_premises"] is False
    assert certificate["status"] == "provisionally_elaborated_not_accepted"
    plans = {row["parent_obligation_id"]: row for row in bundle["unverified_decomposition_plans"]}
    assert set(plans) == set(builder.REQUIRES) - {"M0045-ROOT"}
    for parent, plan in plans.items():
        assert plan["planned_child_ids"] == builder.REQUIRES[parent]
        assert plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        assert all(
            any(
                row["from"] == parent
                and row["to"] == child
                and row["type"] == "logical_decomposition"
                for row in bundle["graphs"]["refinement"]["edges"]
            )
            for child in plan["planned_child_ids"]
        )

    closure = bundle["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M0045-T-PACKAGE"]
    assert closure["proof_leaf_cut_set"] == ["M0045-T-PACKAGE"]
    assert "M0045-X-EXTERNAL-PORT" not in registry["frozen_denominators"]["required_machine"]
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == "sha256:" + denominator
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []

    assert len(specs["recipes"]) == 1
    recipe = specs["recipes"][0]
    assert recipe["argv"] == ["python3", "-B", "Stage1_Instances/THM-M-0045/check_obligation_tree.py"]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert set(recipe["covered_obligation_ids"]) == id_set
    assert "kernel coverage is limited" in recipe["coverage_boundary"]
    assert any("theorem_complete=false" in row["semantic_hash_policy"] for row in recipe["expected_outputs"])
    by_id = {row["obligation_id"]: row for row in rows}
    for oid, expected in builder.CHECKED_TYPE_SHA256.items():
        assert by_id[oid]["statement_fingerprint"] == "lean-pp-universes-output-sha256:" + expected
    node_by_obligation = {row["obligation_id"]: row for row in nodes}
    assert node_by_obligation["M0045-S-EQUATION"]["formal_target"] != node_by_obligation["M0045-T-PACKAGE"]["formal_target"]
    assert by_id["M0045-S-TARGET"]["machine_eligibility"] == "informational"

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    external_source = subprocess.check_output(
        ["git", "show", f"{EXTERNAL_REVISION}:{EXTERNAL_SOURCE_PATH}"], cwd=MATHLIB
    )
    assert hashlib.sha256(external_source).hexdigest() == EXTERNAL_SOURCE_SHA256
    external_text = external_source.decode("utf-8")
    for marker in (
        "private noncomputable def SchurTriangulationAux.of",
        "if hE : Nontrivial E then",
        "let V : Submodule",
        "let W : Submodule",
        "let g : Module.End",
        "int.collectedOrthonormalBasis",
        "termination_by Module.finrank",
        "lemma schur_triangulation",
    ):
        assert marker in external_text, marker

    lean_source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", lean_source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b", without_comments)
    for marker in (
        "def SchurEquationPackage : Prop",
        "def DimensionBoundary : Prop",
        "theorem dimensionBoundary",
        "theorem equationWitness_implies_targetAt",
        "theorem root_of_equationPackage",
        "obtain ⟨U, T, hU, hT, hA⟩",
        "#print axioms root_of_equationPackage",
    ):
        assert marker in lean_source

    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0045-obligation-") as temp_dir:
        statement = subprocess.run(
            [lean_exe, "Statement.lean", "-o", str(Path(temp_dir) / "Statement.olean")],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        lean = subprocess.run(
            ["lake", "env", "lean", str(HERE / "ObligationTree.lean")],
            cwd=LEAN_ROOT,
            env=os.environ | {"LEAN_PATH": temp_dir + ":" + lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
        )
        if lean.returncode:
            sys.stdout.write(lean.stdout)
            raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    assert normalized.count("propext, Classical.choice, Quot.sound") == 2
    assert "equationWitness_implies_targetAt" in lean.stdout and "root_of_equationPackage" in lean.stdout
    printed_lines = lean.stdout.splitlines(keepends=True)

    def printed_section_sha256(start: str, end: str) -> str:
        first = next(index for index, line in enumerate(printed_lines) if line.startswith(start))
        last = next(index for index, line in enumerate(printed_lines[first + 1 :], first + 1) if line.startswith(end))
        return hashlib.sha256("".join(printed_lines[first:last]).encode()).hexdigest()

    machine_type_hashes = {
        "M0045-T-PACKAGE": printed_section_sha256(
            "def Stage1Instances.THM_M_0045.ObligationTree.SchurEquationPackage",
            "def Stage1Instances.THM_M_0045.ObligationTree.DimensionBoundary",
        ),
        "M0045-S-BOUNDARY": printed_section_sha256(
            "def Stage1Instances.THM_M_0045.ObligationTree.DimensionBoundary",
            "theorem Stage1Instances.THM_M_0045.ObligationTree.equationWitness_implies_targetAt",
        ),
        "M0045-S-EQUATION": printed_section_sha256(
            "theorem Stage1Instances.THM_M_0045.ObligationTree.equationWitness_implies_targetAt",
            "'Stage1Instances.THM_M_0045.ObligationTree.equationWitness_implies_targetAt' depends",
        ),
    }
    assert machine_type_hashes == builder.CHECKED_TYPE_SHA256
    for oid, actual in machine_type_hashes.items():
        assert by_id[oid]["statement_fingerprint"] == "lean-pp-universes-output-sha256:" + actual
    assert certificate["required_child_statement_fingerprints"]["M0045-T-PACKAGE"] == (
        "lean-pp-universes-output-sha256:" + machine_type_hashes["M0045-T-PACKAGE"]
    )

    if receipt is not None:
        assert receipt["schema_version"] == "stage1-obligation-tree-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["obligation_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["closed_obligations"] == []
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["audit_complete"] is receipt["theorem_complete"] is False

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        selftest = json.loads(selftest_path.read_text(encoding="utf-8"))
        assert set(selftest) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
        assert selftest["base_revision"] == BASE_REVISION
        if receipt is not None:
            assert selftest["known_failures"] == receipt["known_failures"]
            assert selftest["changed_paths"] == receipt["changed_paths"]
        assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")

    print(
        f"PASS THM-M-0045 obligation tree: {len(ids)} obligations, "
        f"{len(edge_ids)} typed edges, {len(ledger_step_ids)} ledger steps"
    )
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); theorem_complete=false; equation package is the immediate proof cut")


if __name__ == "__main__":
    main()
