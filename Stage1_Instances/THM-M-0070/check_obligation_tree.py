#!/usr/bin/env python3
"""Fail-closed structural validator for the THM-M-0070 obligation freeze."""

from __future__ import annotations

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
ITEM = "S56-M-0070-OBLIGATION_TREE"
THEOREM = "THM-M-0070"
ROOT_ID = "M0070-ROOT"
BASE_REVISION = "250f9e73cbbb3ebd2da9d0cefff78f0ab8c0d056"
BASE_TREE = "b6e8138c58e31e82f8209cb70fbc0fb253f3654a"
DENOMINATOR = "b9832ebb2a8e07834e24753c74f59a665c5c012f873bfc06eabb637def4c5686"
LEAN_OUTPUT_SHA256 = "a5972c2a49eb05d2004f21e6cc3d58863567d5ee319ac0f6c3dbcdb34141b1f3"
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
REGISTRY_FIELDS = {"obligation_id", "statement_fingerprint", "kind", "root_relevant",
                   "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                   "risk_class", "exclusion_reason", "terminal_proof_body_id"}
NODE_FIELDS = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
               "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
               "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
               "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
               "task_ids", "owned_sources", "owner", "reviewer", "validity"}
ALLOWED_EDGES = {"proof_requires", "composes", "logical_decomposition", "source_map",
                 "expository_decomposition", "equivalent_to", "transports", "evidence_for",
                 "provenance_of", "documents", "trusts", "workflow_depends_on"}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ObligationTree.lean",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/build_obligation_artifacts.py",
    f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
    f"Stage1_Instances/{THEOREM}/instance.json",
    f"Stage1_Instances/{THEOREM}/obligation-registry.json",
    f"Stage1_Instances/{THEOREM}/obligation-tree-receipt.json",
    f"Stage1_Instances/{THEOREM}/obligation-tree-validation.md",
    f"Stage1_Instances/{THEOREM}/obligation-tree.md",
    f"Stage1_Instances/{THEOREM}/source-obligation-index.json",
    f"Stage1_Instances/{THEOREM}/typed-graphs.json",
    f"Stage1_Instances/{THEOREM}/validation-specs.json",
]


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


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


def check_lean() -> str:
    with tempfile.TemporaryDirectory(prefix="stage1-m0070-obligation-") as tmp:
        compile_statement = subprocess.run(
            ["lake", "env", "lean", "--root=../..",
             "../../Stage1_Instances/THM-M-0070/Statement.lean", "-o", f"{tmp}/Statement.olean"],
            cwd=LEAN_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
        if compile_statement.returncode:
            sys.stdout.write(compile_statement.stdout)
            raise SystemExit(compile_statement.returncode)
        lean_path = subprocess.check_output(
            ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, text=True
        ).strip()
        env = os.environ.copy()
        env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        result = subprocess.run(
            ["lake", "env", "lean", "--root=../..",
             "../../Stage1_Instances/THM-M-0070/ObligationTree.lean"],
            cwd=LEAN_ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
        if result.returncode:
            sys.stdout.write(result.stdout)
            raise SystemExit(result.returncode)
    normalized = re.sub(r"\s+", " ", result.stdout)
    assert normalized.count("propext, Classical.choice, Quot.sound") == 4
    assert "def Stage1Instances.THM_M_0070.ObligationTree.TranslatedOddOrderBody" in result.stdout
    assert "OddOrderSolvabilityTarget" in result.stdout
    assert hashlib.sha256(result.stdout.encode()).hexdigest() == LEAN_OUTPUT_SHA256
    return result.stdout


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    instance = load("instance.json")
    task_dag = load("task-dag.json")
    anchor = load("anchor-audit.json")
    source_index = load("source-obligation-index.json")
    receipt = load("obligation-tree-receipt.json")
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8"))

    expected_registry, expected_bundle, expected_specs, expected_readable = build_obligation_artifacts.build()
    for name, value in (("obligation-registry.json", expected_registry),
                        ("typed-graphs.json", expected_bundle),
                        ("validation-specs.json", expected_specs)):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"
    assert (HERE / "obligation-tree.md").read_text(encoding="utf-8") == expected_readable

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["execution_rank"] == 1101 and item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0070-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == hashlib.sha256(
        (HERE / "Statement.lean").read_bytes()).hexdigest() == "9e1c126d56f87c1d7dee24d17b13c9c9822ffba13142e836ecbe2a85055a7dcf"
    assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256(
        (HERE / "anchor-audit.json").read_bytes()).hexdigest() == "901aebaf08dd06f32c8772e9f68fd78bf2b09a926d35b6b586d83457bc521792"
    assert registry["selected_architecture_source_revision"] == "6afa795b9018c64ab5c7cd2f9b3c9ab5dd45d93f"
    assert registry["selected_architecture_source_tree"] == "0ddbbe81c42419e179d75d4baaea800b601ccf73"
    coq = next(row for row in anchor["candidates"] if row["candidate_id"] == "M0070-C06-MATHCOMP-ODD-ORDER-COQ")
    placeholder = next(row for row in anchor["candidates"] if row["candidate_id"] == "M0070-C05-ODD-ORDER-LEAN-PLACEHOLDER")
    assert coq["revision"] == registry["selected_architecture_source_revision"]
    assert coq["terminal_proof_body"] == "minSimpleOdd_ind no_minSimple_odd_group"
    assert coq["candidate_classification"] == "M3_other_prover_exact_source_anchor"
    assert placeholder["revision"] == "0f4a5daeaf6f26efd5af808ecd05e4744d8a2924"
    assert placeholder["terminal_proof_body"] == "by sorry"
    assert placeholder["candidate_classification"] == "M5_exact_statement_placeholder_and_incompatible_pins"

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 61 and ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        excluded = row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required"
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert row["exclusion_reason"].endswith("pending_independent_approval")
    field_order = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
                   "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                   "risk_class", "exclusion_reason", "terminal_proof_body_id")
    projection = [{field: row[field] for field in field_order} for row in rows]
    denominator = hashlib.sha256(json.dumps(
        projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"] == DENOMINATOR
    assert registry["frozen_denominators"]["inventory"] == ids
    for eligibility, key in (("machine_eligibility", "required_machine"),
                             ("human_source_eligibility", "required_human_source"),
                             ("readable_eligibility", "required_readable")):
        assert registry["frozen_denominators"][key] == [
            row["obligation_id"] for row in rows if row[eligibility] == "required"]
    assert registry["append_only_delta"] == []
    assert all(row["status"].endswith("pending_independent_approval")
               for row in registry["layer_exclusions"].values())
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    node_by_id = {node["obligation_id"]: node for node in nodes}
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert isinstance(node["step_budget"], int) and 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert {"premises", "inference", "output", "outgoing_use", "steps", "package_expansion_state"} <= ledger.keys()
        assert isinstance(ledger["steps"], list) and ledger["steps"]
        for step in ledger["steps"]:
            assert set(step) == {"step_id", "premise_ids", "inference_or_boundary", "output_claim", "outgoing_use_ids"}
            assert step["step_id"] and step["premise_ids"] and step["inference_or_boundary"]
            assert step["output_claim"] and step["outgoing_use_ids"]
        if node["obligation_id"].startswith(("M0070-BG-", "M0070-PF-")):
            assert ledger["package_expansion_state"] == "split_required_before_proof_acceptance"
        anchor_name = node["public_readable_target"].rsplit("#", 1)[1]
        assert f'id="{anchor_name}"' in readable
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]
    assert node_by_id[ROOT_ID]["machine_debt"] == "M3"
    assert node_by_id["M0070-X-LEAN-BODY"]["machine_debt"] == "M3"
    assert node_by_id["M0070-X-LEAN-PLACEHOLDER"]["machine_debt"] == "M5"
    assert node_by_id["M0070-X-COQ-SOURCE"]["machine_debt"] == "M3"

    assert bundle["root_node_id"] == ROOT_ID and set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    for graph in bundle["graphs"].values():
        assert set(graph["out"]) == set(ids) == set(graph["in"])
        directional = []
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids and edge["type"] in ALLOWED_EDGES
            assert edge["from"] in ids and edge["to"] in ids
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            edge_ids.add(edge["edge_id"])
            if edge["type"] != "composes":
                directional.append(edge)
        check_acyclic(directional)
    assert len(edge_ids) == bundle["typed_edge_count"] == 89
    assert all(edge["type"] == "logical_decomposition"
               for edge in bundle["graphs"]["refinement"]["edges"])

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
    assert reachable == set(bundle["metrics_projection"]["proof_requires_reachable_ids"]) == {
        "M0070-ROOT", "M0070-T-ROOT", "M0070-T-ADAPTER", "M0070-X-LEAN-BODY"}
    assert bundle["metrics_projection"]["accepted_numerator_ids"] == []
    architecture_ids = set(bundle["metrics_projection"]["architecture_reachable_ids"])
    assert set(bundle["metrics_projection"]["machine_closure_reachable_ids"]) == architecture_ids
    for identifier in ("M0070-BG-1", "M0070-BG-16", "M0070-PF-1", "M0070-PF-14",
                       "M0070-BG-APPENDIX-AB", "M0070-BG-APPENDIX-C"):
        assert identifier in architecture_ids
    source_entries = source_index["entries"]
    assert source_index["source_revision"] == registry["selected_architecture_source_revision"]
    assert len(source_entries) == source_index["entry_count"] == (
        bundle["metrics_projection"]["source_declaration_index_count"]
    ) == 2084
    assert hashlib.sha256((HERE / "source-obligation-index.json").read_bytes()).hexdigest() == (
        bundle["metrics_projection"]["source_declaration_index_sha256"]
    )
    assert hashlib.sha256(json.dumps(
        source_entries, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == (
        source_index["denominator_sha256"]
    )
    assert source_index["entry_schema"] == ["obligation_id", "source_file", "source_package_id",
        "source_declaration", "source_occurrence", "source_kind", "line_start", "line_end",
        "source_command_sha256", "exact_source_command", "source_block_sha256",
        "substantive_line_count", "chunks"]
    assert source_index["chunk_schema"] == ["obligation_id", "line_start", "line_end",
                                               "substantive_line_count", "source_lines_sha256"]
    defaults = source_index["eligibility_defaults"]
    assert defaults == {"root_relevant": True, "machine_eligibility": "required",
                        "human_source_eligibility": "required", "readable_eligibility": "required",
                        "risk_class": "critical", "machine_debt": "M4",
                        "expansion_state": "exact_source_command_and_bounded_body_chunks_frozen_lean_translation_open"}
    assert all(len(entry) == 13 for entry in source_entries)
    source_ids = [entry[0] for entry in source_entries]
    assert len(source_ids) == len(set(source_ids))
    source_keys = [(entry[1], entry[3], entry[4]) for entry in source_entries]
    assert len(source_keys) == len(set(source_keys))
    assert all(re.fullmatch(r"[0-9a-f]{64}", entry[8]) and entry[9]
               and re.fullmatch(r"[0-9a-f]{64}", entry[10])
               and entry[11] > 0 for entry in source_entries)
    assert {entry[2] for entry in source_entries} <= set(ids)
    package_ids = [item for item in ids if item.startswith(("M0070-BG-", "M0070-PF-"))]
    for identifier in package_ids:
        assert any(entry[2] == identifier for entry in source_entries), identifier
    source_count_by_package = {
        identifier: sum(entry[2] == identifier for entry in source_entries)
        for identifier in package_ids
    }
    assert min(source_count_by_package.values()) >= 3
    assert source_count_by_package["M0070-PF-14"] == 119
    assert source_count_by_package["M0070-BG-APPENDIX-C"] == 63
    chunk_ids = [chunk[0] for entry in source_entries for chunk in entry[12]]
    assert len(chunk_ids) == len(set(chunk_ids)) == source_index["chunk_count"] == 229
    assert all(0 < chunk[3] <= 80 and re.fullmatch(r"[0-9a-f]{64}", chunk[4])
               for entry in source_entries for chunk in entry[12])
    subregistry = registry["source_obligation_subregistry"]
    assert subregistry["entry_count"] == len(source_entries)
    assert subregistry["chunk_count"] == len(chunk_ids)
    assert subregistry["denominator_sha256"] == source_index["denominator_sha256"]
    assert registry["frozen_denominators"]["source_declaration_obligation_ids"] == source_ids
    assert registry["frozen_denominators"]["source_body_chunk_obligation_ids"] == chunk_ids

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
    for recipe in recipes:
        assert set(recipe) == {"recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
                               "network_policy", "expected_exit", "expected_outputs",
                               "covered_obligation_ids", "covered_declarations",
                               "coverage_semantics", "closure_credit"}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert len(recipe["covered_obligation_ids"]) == 1 and recipe["closure_credit"] is False

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["proof_architecture"]["inventory_count"] == len(ids)
    assert instance["proof_architecture"]["typed_edge_count"] == len(edge_ids)
    assert boundary["remaining_root_cut_set"][0] == "M0070-X-LEAN-BODY"
    assert set(boundary["open_logical_decomposition_ids"]) <= architecture_ids
    assert len(boundary["open_logical_decomposition_ids"]) == len(set(
        boundary["open_logical_decomposition_ids"]))
    assert boundary["open_source_declaration_obligation_ids"] == source_ids
    assert boundary["open_source_body_chunk_obligation_ids"] == chunk_ids

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    stripped = re.sub(r"/-.*?-/|--.*", "", source, flags=re.DOTALL)
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b", stripped)
    for marker in ("def TranslatedOddOrderBody : Prop", "translatedOddOrderBody_iff_target",
                   "target_of_translatedOddOrderBody", "terminalTarget_of_target",
                   "root_of_terminalTarget", "#print axioms root_of_terminalTarget"):
        assert marker in source
    assert check_lean()

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["changed_paths"] == CHANGED_PATHS
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if len(sys.argv) > 1 and sys.argv[1] == "--worker-packet":
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary",
                               "base_revision", "known_failures", "state"}
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["known_failures"] == receipt["known_failures"]

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files
    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    print(f"PASS THM-M-0070 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); exact Lean body remains placeholder or absent")


if __name__ == "__main__":
    main()
