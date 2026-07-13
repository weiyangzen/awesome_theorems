#!/usr/bin/env python3
"""Fail-closed structural and Lean checks for THM-M-0856 obligations."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("optimized Python disables assertion-based hard gates; rerun without -O/PYTHONOPTIMIZE")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0856-OBLIGATION_TREE"
THEOREM_ID = "THM-M-0856"
BASE_REVISION = "f023dbc3411d83201065d1a1156d7406b81135d4"
BASE_TREE = "3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4"
ROOT_EXPRESSION = "5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SOURCE_HASHES = {
    "Tutte.lean": "47072b914aa564222ef8013092c38fa62227fea8230e308cc3eb5f11afcdffc3",
    "Matching.lean": "7e8b873ee73808358dd1d1a36e0c72cd4b27f95b7ba29f23286d3f076f8abc4b",
    "Metric.lean": "4fa93451ec543582ab67d24e259914fdf550b65dadcb4bddceac9bec23557b5b",
    "Operations.lean": "1ebac8bef9890e35e8a4a9159c5a87038bfcbde41261551bca0051cc5f32035c",
    "UniversalVerts.lean": "023564a30e5b2b8b4b204e24f3d4557da7eeaf56378885c86b48dc648ea057dc",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise SystemExit(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain an object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*argv: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True).strip()


def changed_paths() -> list[str]:
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        check=True,
    ).stdout
    paths = []
    entries = status.split(b"\0")
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue
        if len(entry) < 4 or entry[2:3] != b" ":
            raise SystemExit("cannot parse git status")
        code = entry[:2]
        paths.append(entry[3:].decode(errors="surrogateescape"))
        if b"R" in code or b"C" in code:
            index += 1
    return sorted(paths)


def check_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    required = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def lean_check() -> tuple[str, str, str]:
    lean = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0856-obligation-") as temp_dir:
        temp = Path(temp_dir)
        for name in ("Statement.lean", "ObligationTree.lean", "ObligationSignatures.lean"):
            (temp / name).write_bytes((HERE / name).read_bytes())
        env = os.environ.copy()
        env["LEAN_PATH"] = lean_path
        statement_run = subprocess.run(
            [lean, "-o", "Statement.olean", "Statement.lean"],
            cwd=temp,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement_run.returncode:
            sys.stdout.write(statement_run.stdout)
            raise SystemExit(statement_run.returncode)
        env["LEAN_PATH"] = f"{temp}:{lean_path}"
        run = subprocess.run(
            [lean, "-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=temp,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if run.returncode:
            sys.stdout.write(run.stdout)
            raise SystemExit(run.returncode)
        signature_run = subprocess.run(
            [lean, "ObligationSignatures.lean"],
            cwd=temp,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if signature_run.returncode:
            sys.stdout.write(signature_run.stdout)
            raise SystemExit(signature_run.returncode)
    normalized = re.sub(r"\s+", " ", run.stdout)
    for declaration in (
        "SimpleGraph.not_isTutteViolator_of_isPerfectMatching",
        "SimpleGraph.exists_isTutteViolator",
        "SimpleGraph.tutte",
        "Stage1Instances.THM_M_0856.ObligationTree.terminal_adapter",
        "Stage1Instances.THM_M_0856.ObligationTree.pinned_mathlib_terminal",
        "Stage1Instances.THM_M_0856.ObligationTree.compose_root",
    ):
        assert declaration in run.stdout
    assert run.stdout.count("Declarations are sorry-free!") == 2
    assert normalized.count("propext, Classical.choice, Quot.sound") == 6
    assert "def Stage1Instances.THM_M_0856.TutteOneFactorTarget" in run.stdout
    exact_declarations = {
        node["formal_target"]["declaration"].rsplit(".", 1)[-1]
        for node in load(HERE / "typed-graphs.json")["nodes"]
        if node["formal_target"]["kind"] == "exact_lean_type"
    }
    for declaration in exact_declarations:
        assert declaration in signature_run.stdout
    return (
        hashlib.sha256(run.stdout.encode()).hexdigest(),
        hashlib.sha256(signature_run.stdout.encode()).hexdigest(),
        hashlib.sha256((run.stdout + "\n--- ObligationSignatures.lean ---\n" + signature_run.stdout).encode()).hexdigest(),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    registry = load(HERE / "obligation-registry.json")
    bundle = load(HERE / "typed-graphs.json")
    specs = load(HERE / "validation-specs.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    receipt = load(HERE / "obligation-tree-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")

    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM_ID
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM_ID
    assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0856-OBLIGATIONS-v1"
    assert registry["registry_version"] == 1 and registry["append_only_delta"] == []
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["canonical_target"]["expression_sha256"] == ROOT_EXPRESSION
    assert anchor["audit_result"]["accepted_root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 56
    assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M0856-ROOT"
    assert rows[0]["statement_fingerprint"] == rows[1]["statement_fingerprint"] == "lean-expression-sha256:" + ROOT_EXPRESSION
    assert all(set(row) == set(fields) for row in rows)
    projection = [{key: row[key] for key in fields} for row in rows]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    denominators = registry["frozen_denominators"]
    required_machine = set(denominators["required_machine"])
    assert denominators["inventory"] == ids
    assert denominators["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]
    assert denominators["required_human_source"] == [row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"]
    assert denominators["required_readable"] == ids
    assert set(registry["layer_applicability"]) == {
        "S_statement_foundation", "N_normalization", "B_branch", "C_construction",
        "L_core_lemma", "X_external_computation", "T_terminal",
    }
    assert "not_applicable_computation_pending_independent_approval" in registry["layer_applicability"]["X_external_computation"]["state"]
    body_ids = [row["terminal_proof_body_id"] for row in rows if row["terminal_proof_body_id"]]
    exact_root_bodies = [body for body in body_ids if body.endswith("#SimpleGraph.tutte")]
    assert exact_root_bodies == bundle["closure_boundary"]["distinct_exact_root_terminal_body_ids"]
    assert len(exact_root_bodies) == 1

    node_fields = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target",
        "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
        "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
        "computation_record", "step_budget", "semantic_step_ledger",
        "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
        "owned_sources", "owner", "reviewer", "validity",
    }
    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == id_set
    node_by_obligation = {node["obligation_id"]: node for node in nodes}
    assert all(
        node_by_obligation[row["obligation_id"]]["formal_target"]["kind"] == "exact_lean_type"
        for row in rows if row["terminal_proof_body_id"]
    )
    readable = (HERE / "obligation-tree.md").read_text().lower()
    step_ids = set()
    allowed_external_premises = {"frozen-formal-context"}
    for node in nodes:
        assert set(node) == node_fields
        target = node["formal_target"]
        assert set(target) == {
            "kind", "declaration", "type_or_record", "fingerprint", "fingerprint_basis"
        }
        assert target["kind"] in {
            "exact_lean_type", "planned_lean_signature", "nonformal_record"
        }
        assert target["type_or_record"] and re.fullmatch(r"sha256:[0-9a-f]{64}", target["fingerprint"])
        assert target["fingerprint"] == "sha256:" + hashlib.sha256(
            json.dumps(target["fingerprint_basis"], sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        if target["kind"] == "exact_lean_type":
            assert target["declaration"] and target["fingerprint_basis"]["declaration"] == target["declaration"]
        elif target["kind"] == "planned_lean_signature":
            assert target["declaration"].startswith(
                "Stage1Instances.THM_M_0856.ObligationSignatures.M0856_"
            )
            assert target["fingerprint_basis"]["declaration"] == target["declaration"]
            assert "..." not in target["type_or_record"] and "?" not in target["type_or_record"]
        else:
            assert target["declaration"] is None
            assert node["obligation_id"] not in required_machine
        assert 0 < node["step_budget"] <= 100
        assert node["human_debt"] == "H1" and node["machine_debt"] == "M3" and node["readability_debt"] == "R4"
        assert node["evidence_ids"] == []
        ledger = node["semantic_step_ledger"]
        assert {"premises", "inference", "source_anchors", "output", "outgoing_use", "steps"} == set(ledger)
        assert 0 < len(ledger["steps"]) <= node["step_budget"]
        for step in ledger["steps"]:
            assert set(step) == {"step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"}
            assert step["step_id"] not in step_ids
            assert set(step["premise_ids"]) <= id_set | allowed_external_premises
            assert step["inference"] and step["source_locator"] and step["output"] and step["outgoing_use"]
            step_ids.add(step["step_id"])
        path, anchor_name = node["public_readable_target"].split("#", 1)
        assert path == "Stage1_Instances/THM-M-0856/obligation-tree.md"
        assert f"### {anchor_name}" in readable
        assert node["validation_spec_id"] == "VAL-M0856-OBLIGATION-BUNDLE"
        assert node["validity"]["revocation_state"] == "open_not_accepted"

    allowed = {
        "proof": {"proof_requires", "composes", "logical_decomposition"},
        "refinement": {"expository_decomposition"},
        "provenance": {"source_map", "provenance_of"},
        "evidence": {"evidence_for"},
        "trust": {"trusts"},
        "documentation": {"documents"},
        "workflow": {"workflow_depends_on"},
    }
    assert set(bundle["graphs"]) == set(allowed)
    assert bundle["evidence_endpoint_policy"].startswith(
        "Evidence objects are external content-addressed packets"
    )
    assert bundle["evidence_objects"] == []
    edge_ids = set()
    for name, graph in bundle["graphs"].items():
        expected_out = {}
        expected_in = {}
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids and edge["type"] in allowed[name]
            if name == "evidence":
                assert edge["from"] in {item["evidence_id"] for item in bundle["evidence_objects"]}
                assert edge["to"] in id_set
            else:
                assert edge["from"] in id_set and edge["to"] in id_set
            expected_out.setdefault(edge["from"], []).append(edge["edge_id"])
            expected_in.setdefault(edge["to"], []).append(edge["edge_id"])
            edge_ids.add(edge["edge_id"])
        assert graph["out"] == expected_out and graph["in"] == expected_in

        adjacency = {}
        for edge in graph["edges"]:
            if name == "proof" and edge["type"] in {"composes", "logical_decomposition"}:
                continue
            adjacency.setdefault(edge["from"], []).append(edge["to"])
        graph_visiting = set()
        graph_visited = set()

        def visit_graph(node_id: str) -> None:
            assert node_id not in graph_visiting, f"{name} cycle at {node_id}"
            if node_id in graph_visited:
                return
            graph_visiting.add(node_id)
            for target_id in adjacency.get(node_id, []):
                visit_graph(target_id)
            graph_visiting.remove(node_id)
            graph_visited.add(node_id)

        for source_id in adjacency:
            visit_graph(source_id)

    assert bundle["graphs"]["evidence"] == {"edges": [], "out": {}, "in": {}}
    assert all(node["evidence_ids"] == [] for node in nodes)

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    children = {}
    for edge in proof.values():
        reverse = proof[edge["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == edge["edge_id"]
        assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
        assert "proof_requires" in {edge["type"], reverse["type"]}
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
            reverse_expected = "composes" if edge["from"] == "M0856-ROOT" else "logical_decomposition"
            assert reverse["type"] == reverse_expected

    visiting = set()
    visited = set()

    def visit(oid: str) -> None:
        assert oid not in visiting, f"proof cycle at {oid}"
        if oid in visited:
            return
        visiting.add(oid)
        for child in children.get(oid, []):
            visit(child)
        visiting.remove(oid)
        visited.add(oid)

    visit("M0856-ROOT")
    assert visited == required_machine
    assert set(children) <= visited
    recomputed_leaves = sorted(
        {child for child_ids in children.values() for child in child_ids} - set(children)
    )

    certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
    assert set(certificates) == {"M0856-ROOT"}
    root_cert = certificates["M0856-ROOT"]
    assert root_cert["required_child_ids"] == children["M0856-ROOT"]
    assert root_cert["checked_declaration"] == "Stage1Instances.THM_M_0856.ObligationTree.compose_root"
    assert root_cert["introduces_undeclared_premises"] is False
    plans = {row["parent_obligation_id"]: row for row in bundle["unverified_decomposition_plans"]}
    assert set(plans) == set(children) - {"M0856-ROOT"}
    for parent, plan in plans.items():
        assert plan["planned_child_ids"] == children[parent]
        assert "unverified" in plan["status"]

    closure = bundle["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert closure["unverified_internal_decomposition_count"] == len(plans)
    assert set(closure["proof_leaf_cut_set"]) == set(
        denominators["required_unique_logical_leaves"]
    )
    assert closure["proof_leaf_cut_set"] == recomputed_leaves

    execution_path = ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    execution_hash = sha256(execution_path)
    task_graph = bundle["workflow_task_graph"]
    authoritative = [item for item in load(execution_path)["items"] if item["theorem_id"] == THEOREM_ID]
    assert len(authoritative) == 7
    prerequisite = next(item for item in authoritative if item["id"] == "S56-M-0856-ANCHOR_AUDIT")
    assert prerequisite["state"] in {"[_]", "[x]"}
    assert bundle["frozen_against_execution_dag_sha256"] == task_graph["authority_sha256"] == execution_hash
    assert bundle["local_task_dag_projection_sha256"] == sha256(HERE / "task-dag.json")
    assert task_graph["nodes"] == [{"task_id": item["id"], "phase": item["phase"], "layer": item["layer"]} for item in authoritative]
    assert [(edge["from"], edge["to"]) for edge in task_graph["edges"]] == [(item["id"], dependency) for item in authoritative for dependency in item["depends_on"]]
    assert all(link["obligation_id"] in id_set for link in task_graph["task_obligation_links"])
    obligation_task = next(task for task in local_dag["tasks"] if task["id"] == ITEM_ID)
    assert obligation_task["state"] == "open" and obligation_task["provisional_worker_state"] == "[_]"
    assert obligation_task["covered_obligation_ids"] == ids
    assert obligation_task["worker_receipt"] == "Stage1_Instances/THM-M-0856/obligation-tree-receipt.json"

    assert instance["obligation_registry_hash"] == "sha256:" + denominator
    assert instance["item_id"] == ITEM_ID and instance["intent"] == "obligation_tree"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == [] and instance["accepted_receipt_ids"] == []
    required_artifacts = {
        "ObligationTree.lean", "ObligationSignatures.lean",
        "build_obligation_artifacts.py", "check_obligation_tree.py",
        "check_prohibited_constructs.py",
        "obligation-registry.json", "typed-graphs.json", "validation-specs.json",
        "obligation-tree.md", "obligation-tree-validation.md", "obligation-tree-receipt.json",
    }
    assert required_artifacts <= set(instance["owned_artifacts"])

    assert len(specs["recipes"]) == 2
    recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
    assert recipe_ids == {"VAL-M0856-OBLIGATION-BUNDLE", "VAL-M0856-OBLIGATION-GENERATOR"}
    for recipe in specs["recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert set(recipe["covered_obligation_ids"]) == id_set
        assert recipe["closure_credit"] is False

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    simple_graph = MATHLIB / "Mathlib/Combinatorics/SimpleGraph"
    blob_ids = {
        "Tutte.lean": "4b7931e61e4dd6a3aae37fcecf698ddc238fbc4e",
        "Matching.lean": "1c4940a10d3d4c6fc6462bd43ffa2e70ced8dacf",
        "Metric.lean": "9599bd6984b87caedfbf6a87c15a704b09339480",
        "Operations.lean": "4f725e6c5747ca3a5ff443d488402fd511ca0ada",
        "UniversalVerts.lean": "9ac099fcadc6d87bd9d1b3fd7a07bbe11c6af38f",
    }
    for name, expected in SOURCE_HASHES.items():
        assert sha256(simple_graph / name) == expected, name
        assert output(
            "git", "rev-parse", f"HEAD:Mathlib/Combinatorics/SimpleGraph/{name}", cwd=MATHLIB
        ) == blob_ids[name]
    external_body_ids = [body for body in body_ids if body.startswith("mathlib4@")]
    expected_external_body_ids = {
        f"mathlib4@{MATHLIB_REVISION}:{blob_ids['Tutte.lean']}#SimpleGraph.tutte",
        f"mathlib4@{MATHLIB_REVISION}:{blob_ids['Tutte.lean']}#SimpleGraph.not_isTutteViolator_of_isPerfectMatching",
        f"mathlib4@{MATHLIB_REVISION}:{blob_ids['Matching.lean']}#ConnectedComponent.odd_matches_node_outside",
        f"mathlib4@{MATHLIB_REVISION}:{blob_ids['Tutte.lean']}#SimpleGraph.IsTutteViolator.empty",
        f"mathlib4@{MATHLIB_REVISION}:{blob_ids['Tutte.lean']}#SimpleGraph.exists_isTutteViolator",
        f"mathlib4@{MATHLIB_REVISION}:{blob_ids['Matching.lean']}#SimpleGraph.exists_maximal_isMatchingFree",
        f"mathlib4@{MATHLIB_REVISION}:{blob_ids['Tutte.lean']}#SimpleGraph.IsTutteViolator.mono",
        f"mathlib4@{MATHLIB_REVISION}:{blob_ids['Tutte.lean']}#SimpleGraph.Subgraph.IsPerfectMatching.exists_of_isClique_supp",
    }
    assert set(external_body_ids) == expected_external_body_ids
    tutte_source = (simple_graph / "Tutte.lean").read_text()
    for marker in (
        "lemma not_isTutteViolator_of_isPerfectMatching",
        "lemma exists_isTutteViolator",
        "theorem tutte :",
        "by_cases hvOdd : Odd (Nat.card V)",
        "exists_maximal_isMatchingFree h",
        "Subgraph.IsPerfectMatching.exists_of_isClique_supp",
        "tutte_exists_isPerfectMatching_of_near_matchings",
        "tutte_exists_isAlternating_isCycles",
    ):
        assert marker in tutte_source

    lean_source = (HERE / "ObligationTree.lean").read_text()
    code = re.sub(r"/-.*?-/", "", lean_source, flags=re.S)
    code = re.sub(r"--.*", "", code)
    forbidden = (
        "s" + "orry", "a" + "dmit", "s" + "orryAx", "a" + "xiom ",
        "unsafe ", "opaque ", "extern ", "implemented_by", "native_decide",
    )
    assert all(token not in code for token in forbidden)
    for marker in (
        "def MathlibTerminal : Prop", "theorem terminal_adapter",
        "theorem pinned_mathlib_terminal", "theorem compose_root", "adapter terminal",
        "#print sorries SimpleGraph.tutte", "#print axioms compose_root",
    ):
        assert marker in lean_source
    signature_source = (HERE / "ObligationSignatures.lean").read_text()
    signature_code = re.sub(r"/-.*?-/", "", signature_source, flags=re.S)
    signature_code = re.sub(r"--.*", "", signature_code)
    assert all(token not in signature_code for token in forbidden)
    tutte_code = re.sub(r"/-.*?-/", "", tutte_source, flags=re.S)
    tutte_code = re.sub(r"--.*", "", tutte_code)
    assert all(token not in tutte_code for token in forbidden)
    assert signature_source.count("Frozen planned interface for") == sum(
        node["formal_target"]["kind"] == "planned_lean_signature" for node in nodes
    )
    obligation_output_sha256, signature_output_sha256, lean_output_sha256 = lean_check()

    assert receipt["schema_version"] == "stage1-worker-obligation-tree-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "obligation_tree"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert validated_at.tzinfo is not None
    assert validated_at <= datetime.now(validated_at.tzinfo)
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["obligation_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["substantive_ledger_step_count"] == len(step_ids)
    assert receipt["unverified_internal_decomposition_count"] == len(plans)
    assert receipt["canonical_obligation_ids"] == ids
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["placeholder_scan"] == "ObligationTree.lean, ObligationSignatures.lean, and pinned Tutte.lean comment-aware scan clean; pinned SimpleGraph.tutte reports sorry-free"
    assert receipt["evidence_object_ids"] == []
    for command in receipt["commands_and_results"]:
        assert isinstance(command["argv"], list) and command["argv"]
        assert all(isinstance(arg, str) and arg for arg in command["argv"])
        if command.get("expected_failure"):
            assert command["exit_code"] != 0
        else:
            assert command["exit_code"] == 0
    assert receipt["lean_output_sha256"] == lean_output_sha256
    assert receipt["obligation_tree_lean_output_sha256"] == obligation_output_sha256
    assert receipt["signature_lean_output_sha256"] == signature_output_sha256
    assert receipt["changed_paths"] == sorted(path for path in changed_paths() if path != "Formalizations/Lean/.lake")
    assert changed_paths() == sorted([*receipt["changed_paths"], "Formalizations/Lean/.lake"])
    assert receipt["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    for key, path in {
        "statement_sha256": HERE / "Statement.lean",
        "anchor_audit_sha256": HERE / "anchor-audit.json",
        "execution_dag_sha256": execution_path,
        "blueprint_sha256": ROOT / "Docs/Stage1_Blueprint_rev-5.6.md",
        "target_manifest_sha256": ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        "execution_skill_sha256": ROOT / "skills/execute-stage1-rev56/SKILL.md",
        "lean_toolchain_sha256": ROOT / "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": ROOT / "Formalizations/Lean/lake-manifest.json",
        "obligation_tree_lean_sha256": HERE / "ObligationTree.lean",
        "obligation_signatures_lean_sha256": HERE / "ObligationSignatures.lean",
        "registry_file_sha256": HERE / "obligation-registry.json",
        "typed_graphs_file_sha256": HERE / "typed-graphs.json",
        "validation_specs_file_sha256": HERE / "validation-specs.json",
        "generator_sha256": HERE / "build_obligation_artifacts.py",
        "checker_sha256": HERE / "check_obligation_tree.py",
        "prohibited_checker_sha256": HERE / "check_prohibited_constructs.py",
    }.items():
        assert receipt["source_revisions"][key] == sha256(path), key
    assert receipt["source_revisions"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["source_revisions"]["mathlib_tree"] == MATHLIB_TREE
    receipt_source_keys = {
        "Tutte.lean": "tutte_source_sha256",
        "Matching.lean": "matching_source_sha256",
        "Metric.lean": "metric_source_sha256",
        "Operations.lean": "operations_source_sha256",
        "UniversalVerts.lean": "universal_verts_source_sha256",
    }
    for name, key in receipt_source_keys.items():
        assert receipt["source_revisions"][key] == SOURCE_HASHES[name]

    if args.worker_packet:
        check_packet(args.worker_packet, receipt)

    print(f"PASS THM-M-0856 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps")
    print(f"registry denominator sha256: {denominator}")
    print(f"Lean output sha256: {lean_output_sha256}")
    print("accepted root remains H1/M3/R4; closed obligations 0; theorem_complete=false")


if __name__ == "__main__":
    main()
