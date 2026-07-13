#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0041 obligation freeze."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from datetime import datetime

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0041-OBLIGATION_TREE"
THEOREM = "THM-M-0041"
ROOT_ID = "M0041-ROOT"
BASE_REVISION = "c76fe0f1a7514b41f191d16840eff25e64ee9d17"
BASE_TREE = "388bc991837bae9741d7e7cb88b43c216eab966a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_EXPRESSION = "5aad8415af4578ca43d0ec58eee038ed4470dce17896766215d3bf9f49d8e711"
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
    "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
    "reviewer", "validity",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
EXPECTED_PROOF_REACHABLE = {
    "M0041-ROOT", "M0041-T-CHARPOLY", "M0041-A-MATHLIB-ANCHOR",
}
ALLOWED_KINDS = {
    "root", "definition", "normalization", "reduction", "branch", "construction",
    "bridge", "core_lemma", "computation", "certificate", "transport", "terminal",
}
ALLOWED_MACHINE = {"required", "not_applicable", "informational"}
ALLOWED_HUMAN = {"required", "not_applicable"}
ALLOWED_READABLE = {"required", "not_applicable"}
ALLOWED_RISK = {"critical", "high", "normal", "low"}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def output(*argv: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def validate_graphs(registry: dict, bundle: dict) -> tuple[int, set[str]]:
    rows = registry["obligations"]
    ids = {row["obligation_id"] for row in rows}
    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    proof_edges: dict[str, dict] = {}
    children: dict[str, list[str]] = {}

    for graph_name, graph in bundle["graphs"].items():
        assert set(graph) == {"edges", "out", "in"}, graph_name
        indexed_edge_ids = {
            edge_id for values in graph["out"].values() for edge_id in values
        } | {
            edge_id for values in graph["in"].values() for edge_id in values
        }
        assert indexed_edge_ids == {item["edge_id"] for item in graph["edges"]}
        directional: dict[str, list[str]] = {}
        for item in graph["edges"]:
            assert item["edge_id"] not in edge_ids
            assert item["type"] in ALLOWED_EDGES
            assert item["from"] in ids and item["to"] in ids
            assert item["edge_id"] in graph["out"][item["from"]]
            assert item["edge_id"] in graph["in"][item["to"]]
            edge_ids.add(item["edge_id"])
            if graph_name == "proof":
                proof_edges[item["edge_id"]] = item
            if item["type"] != "composes":
                directional.setdefault(item["from"], []).append(item["to"])

        graph_visiting: set[str] = set()
        graph_visited: set[str] = set()

        def graph_visit(identifier: str) -> None:
            assert identifier not in graph_visiting, f"{graph_name} cycle at {identifier}"
            if identifier in graph_visited:
                return
            graph_visiting.add(identifier)
            for child in directional.get(identifier, []):
                graph_visit(child)
            graph_visiting.remove(identifier)
            graph_visited.add(identifier)

        for identifier in ids:
            graph_visit(identifier)

    for item in proof_edges.values():
        reciprocal = proof_edges[item["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == item["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (item["to"], item["from"])
        assert {reciprocal["type"], item["type"]} == {"proof_requires", "composes"}
        if item["type"] == "proof_requires":
            children.setdefault(item["from"], []).append(item["to"])

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str) -> None:
        assert identifier not in visiting, f"proof cycle at {identifier}"
        if identifier in visited:
            return
        visiting.add(identifier)
        for child in children.get(identifier, []):
            visit(child)
        visiting.remove(identifier)
        visited.add(identifier)

    visit(ROOT_ID)
    assert visited == EXPECTED_PROOF_REACHABLE

    # Proof plus refinement must expose every semantic proof/statement architecture node. Support
    # edges are deliberately excluded so documentation cannot conceal an orphan.
    architecture = set(visited)
    changed = True
    while changed:
        changed = False
        for graph_name in ("proof", "refinement"):
            graph = bundle["graphs"][graph_name]
            for item in graph["edges"]:
                if item["from"] in architecture:
                    before = len(architecture)
                    architecture.add(item["to"])
                    changed |= len(architecture) != before
    semantic_ids = ids - {"M0041-S-FOUNDATION", "M0041-X-SOURCE", "M0041-X-PROVENANCE", "M0041-X-TRUST", "M0041-X-READABLE", "M0041-X-WORKFLOW"}
    assert architecture == semantic_ids
    return len(edge_ids), visited


def lean_check() -> str:
    lean = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0041-obligation-") as temp_dir:
        temp = Path(temp_dir)
        for name in ("Statement.lean", "ObligationTree.lean"):
            (temp / name).write_bytes((HERE / name).read_bytes())
        env = os.environ.copy()
        env["LEAN_PATH"] = lean_path
        statement = subprocess.run(
            [lean, "-o", "Statement.olean", "Statement.lean"], cwd=temp, env=env,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180,
            check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        env["LEAN_PATH"] = f"{temp}:{lean_path}"
        obligation = subprocess.run(
            [lean, "ObligationTree.lean"], cwd=temp, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        if obligation.returncode:
            sys.stdout.write(obligation.stdout)
            raise SystemExit(obligation.returncode)
    for marker in (
        "Matrix.adjugate_mul",
        "matPolyEquiv_smul_one",
        "Polynomial.eval_mul_X_sub_C",
        "'Stage1Instances.THM_M_0041.ObligationTree.matrixCayleyHamilton_of_engines' depends on axioms: [propext,",
        "'Stage1Instances.THM_M_0041.ObligationTree.characteristicPolynomialTransport' depends on axioms: [propext,",
        "'Stage1Instances.THM_M_0041.ObligationTree.root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton' depends on axioms: [propext,",
        "Classical.choice",
        "Quot.sound",
        "def Stage1Instances.THM_M_0041.CayleyHamiltonTarget",
    ):
        assert marker in obligation.stdout, marker
    return hashlib.sha256(obligation.stdout.encode()).hexdigest()


def main() -> None:
    registry = load(HERE / "obligation-registry.json")
    bundle = load(HERE / "typed-graphs.json")
    recipes = load(HERE / "validation-specs.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    receipt = load(HERE / "obligation-tree-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1081
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0041-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert recipes["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == recipes["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == recipes["theorem_id"] == THEOREM
    assert registry["registry_version"] == 1
    assert registry["root_obligation_id"] == bundle["root_node_id"] == ROOT_ID
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["canonical_expression_sha256"] == ROOT_EXPRESSION

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 17
    assert ids[0] == ROOT_ID
    for row in rows:
        assert set(row) == REGISTRY_FIELDS
        assert row["kind"] in ALLOWED_KINDS
        assert row["machine_eligibility"] in ALLOWED_MACHINE
        assert row["human_source_eligibility"] in ALLOWED_HUMAN
        assert row["readable_eligibility"] in ALLOWED_READABLE
        assert row["risk_class"] in ALLOWED_RISK
        if row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required":
            assert row["exclusion_reason"]
    projection = [{field: row[field] for field in build_obligation_artifacts.REGISTRY_FIELDS}
                  for row in rows]
    denominator = canonical_digest(projection)
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert registry["frozen_denominators"]["inventory"] == ids
    for field, key, value in (
        ("machine_eligibility", "required_machine", "required"),
        ("human_source_eligibility", "required_human_source", "required"),
        ("readable_eligibility", "required_readable", "required"),
    ):
        assert registry["frozen_denominators"][key] == [
            row["obligation_id"] for row in rows if row[field] == value
        ]
    assert registry["append_only_delta"] == []
    assert all(value["status"].endswith("pending_independent_approval")
               for value in registry["layer_exclusions"].values())
    assert registry["deduplication"]["terminal_body_id"].endswith("Matrix.aeval_self_charpoly")
    assert "LinearMap.aeval_self_charpoly" in registry["deduplication"]["aliases_without_independent_credit"]

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids)
    assert {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert set(node) == NODE_FIELDS
        assert 0 < node["step_budget"] <= 100
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert set(node["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use", "steps"}
        assert node["semantic_step_ledger"] == build_obligation_artifacts.LEDGERS[node["obligation_id"]]
        assert all(node["semantic_step_ledger"][key] for key in ("premises", "inference", "output", "outgoing_use", "steps"))
        assert node["step_budget"] == len(node["semantic_step_ledger"]["steps"]) <= 100
        for step in node["semantic_step_ledger"]["steps"]:
            assert set(step) == {"step_id", "premise_ids", "inference_or_source", "exact_output", "outgoing_use_ids"}
        assert node["validation_spec_id"] == f"VAL-{node['obligation_id']}"
        assert "#m0041-" in node["public_readable_target"]

    edge_count, proof_reachable = validate_graphs(registry, bundle)
    assert proof_reachable == EXPECTED_PROOF_REACHABLE
    assert edge_count == 27
    assert len(recipes["recipes"]) == len(ids)
    assert {recipe["recipe_id"] for recipe in recipes["recipes"]} == {
        node["validation_spec_id"] for node in nodes
    }
    covered = []
    for recipe in recipes["recipes"]:
        assert recipe["cwd"] == "." and recipe["network_policy"] == "denied"
        assert recipe["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"]
        assert recipe["expected_exit"] == 0 and len(recipe["covered_obligation_ids"]) == 1
        assert recipe["closure_credit"] is False
        assert recipe["coverage_semantics"] in {
            "provisional_interface_and_architecture_validation", "open_state_classification_only"
        }
        covered.extend(recipe["covered_obligation_ids"])
    assert covered == ids
    assert set(bundle["closure_boundary"]["composition_certificates"]) == {
        declaration for recipe in recipes["recipes"] for declaration in recipe["covered_declarations"]
    }

    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == [] and instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    workflow = bundle["workflow_task_graph"]
    expected_tasks = {
        "S56-M-0041-INTAKE", "S56-M-0041-STATEMENT", "S56-M-0041-ANCHOR_AUDIT",
        ITEM, "S56-M-0041-PROOF", "S56-M-0041-VALIDATION", "S56-M-0041-RELEASE",
    }
    assert {node["task_id"] for node in workflow["nodes"]} == expected_tasks
    assert {(edge["from"], edge["to"]) for edge in workflow["edges"]} == {
        ("S56-M-0041-STATEMENT", "S56-M-0041-INTAKE"),
        ("S56-M-0041-ANCHOR_AUDIT", "S56-M-0041-STATEMENT"),
        (ITEM, "S56-M-0041-ANCHOR_AUDIT"),
        ("S56-M-0041-PROOF", ITEM),
        ("S56-M-0041-VALIDATION", "S56-M-0041-PROOF"),
        ("S56-M-0041-RELEASE", "S56-M-0041-VALIDATION"),
    }
    assert all(link["task_id"] in expected_tasks and link["obligation_id"] in set(ids)
               for link in workflow["task_obligation_links"])
    assert bundle["graphs"]["evidence"]["edges"] == []
    assert "provisional worker receipt" in bundle["evidence_endpoint_policy"]
    required_artifacts = {
        "README.md", "ObligationTree.lean", "build_obligation_artifacts.py",
        "check_obligation_tree.py", "obligation-registry.json", "typed-graphs.json",
        "validation-specs.json", "obligation-tree.md", "obligation-tree-validation.md",
        "obligation-tree-receipt.json",
    }
    assert required_artifacts <= set(instance["owned_artifacts"])

    built_registry, built_bundle, built_recipes, built_instance = build_obligation_artifacts.build()
    assert build_obligation_artifacts.render(built_registry) == (HERE / "obligation-registry.json").read_text()
    assert build_obligation_artifacts.render(built_bundle) == (HERE / "typed-graphs.json").read_text()
    assert build_obligation_artifacts.render(built_recipes) == (HERE / "validation-specs.json").read_text()
    assert build_obligation_artifacts.render(built_instance) == (HERE / "instance.json").read_text()

    lean_source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    for marker in (
        "def CharacteristicPolynomialTransport",
        "def AdjugateIdentityEngine",
        "def MatrixPolynomialTransportEngine",
        "def RightFactorEvaluationEngine",
        "def ScalarEvaluationTransportEngine",
        "theorem matrixCayleyHamilton_of_engines",
        "theorem root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton",
        "#print axioms matrixCayleyHamilton_of_engines",
    ):
        assert marker in lean_source, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(lean_source))
    lean_output_sha = lean_check()
    assert receipt["validation"]["lean_output_sha256"] == lean_output_sha

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["source_revisions"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["source_revisions"]["anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert receipt["source_revisions"]["matrix_charpoly_basic_sha256"] == sha256(
        MATHLIB / "Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean"
    )
    assert receipt["inventory_count"] == 17 and receipt["typed_edge_count"] == edge_count
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert datetime.fromisoformat(receipt["validated_at"]) <= datetime.now().astimezone()
    assert datetime.fromisoformat(registry["frozen_at"]) <= datetime.fromisoformat(receipt["validated_at"])

    required_packet = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required_packet
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"] == receipt["known_failures"]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == set(packet["changed_paths"])

    for name in receipt["changed_paths"]:
        path = ROOT / name
        if path == ROOT / ".stage1-worker-selftest.json":
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "obligation-tree.md", "obligation-tree-validation.md"):
        public = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in public and ".cron/" not in public
        assert "theorem_complete=true" not in public

    print(f"PASS THM-M-0041 obligation tree: {len(ids)} obligations, {edge_count} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print(f"conditional Lean output sha256: {lean_output_sha}")
    print("root closure: open (H1/M3/R3); accepted obligations: 0; theorem_complete=false")


if __name__ == "__main__":
    main()
