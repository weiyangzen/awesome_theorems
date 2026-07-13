#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0484 obligation freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
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
ITEM = "S56-M-0484-OBLIGATION_TREE"
THEOREM = "THM-M-0484"
ROOT_ID = "M0484-ROOT"
RANK = 1365
BASE_REVISION = "fcabbf1e0ad9507eebe91663bccabfa87d22813e"
BASE_TREE = "873e589c594454b7f263c7ed2342089a4d15e842"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SOURCE_SHA256 = "6321c156165f59d49954c0e6e47706e765c0277df20b97a20333ceba29e8bead"
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
    "human_debt", "machine_debt", "candidate_machine_classification",
    "candidate_evidence_level", "interface_check_status", "closure_credit",
    "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
    "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
    "reviewer", "validity",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_body_decomposition",
    "source_map", "provenance_of", "evidence_for", "trusts", "documents",
    "workflow_depends_on",
}
CHECKED_DECLARATIONS = {
    "root_of_directions", "root_of_terminal", "sufficiency_of_branch",
    "sufficiency_of_order_and_minFac", "necessity_of_branch",
    "orderInequality_of_order_and_card", "omegaOrder_of_power_boundaries",
    "omegaPowOne_of_negOne", "omegaPowNegOne_of_formula_and_vanishing",
    "necessity_of_recurrence_closedForm_trace",
}


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
    return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()


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


def run_lean() -> str:
    lean_bin = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0484-obligation-") as temporary:
        temp = Path(temporary)
        statement = subprocess.run(
            [lean_bin, "-o", str(temp / "Statement.olean"), str(HERE / "Statement.lean")],
            cwd=HERE,
            env={"LEAN_PATH": lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
            check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        obligation = subprocess.run(
            [lean_bin, "--trust=0", str(HERE / "ObligationTree.lean")],
            cwd=HERE,
            env={"LEAN_PATH": f"{temp}:{lean_path}"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if obligation.returncode:
            sys.stdout.write(obligation.stdout)
            raise SystemExit(obligation.returncode)
    assert "Declarations are sorry-free!" in obligation.stdout
    assert "sorryAx" not in obligation.stdout
    assert "lucas_lehmer_sufficiency" in obligation.stdout
    assert "lucas_lehmer_necessity" in obligation.stdout
    for name in CHECKED_DECLARATIONS:
        assert f"THM_M_0484.ObligationTree.{name}'" in obligation.stdout
    normalized = " ".join(obligation.stdout.split())
    assert normalized.count("propext, Classical.choice, Quot.sound") == 5
    assert normalized.count("propext, Quot.sound") == 5
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
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    receipt = load(HERE / "obligation-tree-receipt.json")

    expected = build_obligation_artifacts.build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": RANK,
        "phase": "obligation_tree",
        "layer": 3,
        "state": "[ ]",
        "depends_on": ["S56-M-0484-ANCHOR_AUDIT"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0484-ANCHOR_AUDIT")
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_task["evidence_ids"] == []
    assert task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 36
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(set(row) == REGISTRY_FIELDS for row in rows)
    for row in rows:
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
            or row["readable_eligibility"] != "required"
        )
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert set(row["exclusion_reason"]) == {"code", "justification", "approval"}
            assert "pending" in row["exclusion_reason"]["approval"]
    fields = tuple(registry["canonical_projection_fields"])
    projection = [{field: row[field] for field in fields} for row in rows]
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
    assert registry["append_only_delta"] == []
    assert registry["layer_exclusions"]["finite_computation"]["status"].endswith(
        "pending_independent_approval"
    )
    observed = registry["status_observed_after_freeze"]
    assert observed["candidate_machine_classification"] == "M1"
    assert observed["candidate_closure_credit"] is False
    assert observed["accepted_closed_obligations"] == []
    assert observed["root_machine_debt"] == "M3"

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids)
    assert len({node["node_id"] for node in nodes}) == len(nodes)
    assert {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert set(node) == NODE_FIELDS
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert node["semantic_step_ledger"]["substantive_step_cap"] == node["step_budget"]
        assert {"premises", "inference", "output", "outgoing_use", "split_rule"} <= set(
            node["semantic_step_ledger"]
        )
        assert node["public_readable_target"].startswith(
            f"Stage1_Instances/{THEOREM}/obligation-tree.md#"
        )
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]
        assert node["closure_credit"] is False and node["evidence_ids"] == []
        assert node["machine_debt"] in {"M3", "M4"}
        if node["interface_check_status"] == "kernel_checked_conditional_no_closure_credit":
            assert node["obligation_id"] in set(bundle["closure_boundary"]["interface_checked_obligations"])
        else:
            assert node["interface_check_status"] == "not_checked_in_this_phase"
        if node["candidate_machine_classification"] is not None:
            assert node["candidate_machine_classification"] == "M1"
            assert node["candidate_evidence_level"] == "E2_nonrelease_worker_probe"
            assert node["machine_debt"] == "M3"

    assert bundle["root_node_id"] == ROOT_ID
    assert bundle["edge_endpoint_namespace"] == "canonical obligation_id"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        assert set(graph["out"]) == set(ids) == set(graph["in"])
        directional: list[dict] = []
        for record in graph["edges"]:
            assert record["edge_id"] not in edge_ids
            assert record["type"] in ALLOWED_EDGES
            assert record["from"] in ids and record["to"] in ids
            assert record["edge_id"] in graph["out"][record["from"]]
            assert record["edge_id"] in graph["in"][record["to"]]
            edge_ids.add(record["edge_id"])
            if record["type"] != "composes":
                directional.append(record)
        check_acyclic(directional)

    proof = {record["edge_id"]: record for record in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for record in proof.values():
        reciprocal = proof[record["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == record["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (record["to"], record["from"])
        assert {record["type"], reciprocal["type"]} == {"proof_requires", "composes"}
        assert reciprocal["composition_declaration"] == record["composition_declaration"]
        assert record["composition_declaration"].rsplit(".", 1)[-1] in CHECKED_DECLARATIONS
        if record["type"] == "proof_requires":
            children.setdefault(record["from"], []).append(record["to"])
    reachable: set[str] = set()

    def reach(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            reach(child)

    reach(ROOT_ID)
    assert reachable == {
        "M0484-ROOT", "M0484-T-ASSEMBLE", "M0484-T-SUFFICIENCY",
        "M0484-B-SUFF-CONTRA", "M0484-L-ORDER-INEQ", "M0484-L-ORDER-OMEGA",
        "M0484-L-X-CARD-UNITS", "M0484-L-MINFAC-SQUARE", "M0484-L-OMEGA-NEGONE",
        "M0484-L-OMEGA-ONE", "M0484-L-TWO-LT-Q", "M0484-L-OMEGA-FORMULA",
        "M0484-L-MERSENNE-VANISH", "M0484-T-NECESSITY", "M0484-B-NEC-TRACE",
        "M0484-N-RECURRENCE-X", "M0484-L-CLOSED-FORM", "M0484-L-OMEGA-TRACE",
    }
    plans = bundle["unverified_decomposition_plans"]
    assert len(plans) == 17
    assert all(
        plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        and plan["required_before_parent_machine_acceptance"] is True
        and "exact abstract-child harness" in plan["required_future_certificate"]
        for plan in plans
    )
    refinement_plans = [
        record for record in bundle["graphs"]["refinement"]["edges"]
        if record["type"] == "source_body_decomposition"
    ]
    assert {(r["from"], r["to"]) for r in refinement_plans} == {
        (p["parent"], p["child"]) for p in plans
    }
    assert ("M0484-L-X-CARD-UNITS", "M0484-L-TWO-LT-Q") in {
        (p["parent"], p["child"]) for p in plans
    }
    assert ("M0484-B-SUFF-CONTRA", "M0484-N-INDEX") in {
        (p["parent"], p["child"]) for p in plans
    }
    assert ("M0484-B-NEC-TRACE", "M0484-N-INDEX") in {
        (p["parent"], p["child"]) for p in plans
    }
    assert all(
        record["closure_role"] == "unverified_as_child_to_parent_composition"
        and record["future_certificate_required"] is True
        for record in refinement_plans
    )

    assert len(bundle["composition_certificates"]) == len(CHECKED_DECLARATIONS) == 10
    assert {
        row["declaration"].rsplit(".", 1)[-1] for row in bundle["composition_certificates"]
    } == CHECKED_DECLARATIONS
    assert all(
        row["status"] == "provisionally_elaborated_not_accepted"
        and row["certificate_kind"] == "lean_abstract_child_harness"
        and row["introduces_undeclared_premises"] is False
        and row["accepted"] is False
        for row in bundle["composition_certificates"]
    )
    statement_fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"] for row in rows
    }
    for certificate in bundle["composition_certificates"]:
        name = certificate["declaration"].rsplit(".", 1)[-1]
        expected_by_parent: dict[str, list[str]] = {}
        for record in proof.values():
            if record["type"] != "proof_requires":
                continue
            if record["composition_declaration"].rsplit(".", 1)[-1] == name:
                expected_by_parent.setdefault(record["from"], []).append(record["to"])
        assert certificate["parent_obligation_ids"] == sorted(expected_by_parent)
        assert certificate["required_child_ids_by_parent"] == expected_by_parent
        flattened = {
            child for children_for_parent in expected_by_parent.values() for child in children_for_parent
        }
        assert certificate["required_child_statement_fingerprints"] == {
            child: statement_fingerprints[child] for child in flattened
        }
    boundary = bundle["closure_boundary"]
    assert boundary["candidate_classification"] == "M1"
    assert boundary["candidate_terminal_obligations"] == [
        "M0484-T-SUFFICIENCY", "M0484-T-NECESSITY",
    ]
    assert "candidate_closed_obligations" not in boundary
    assert boundary["candidate_closure_credit"] is False
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert boundary["remaining_machine_root_cut_set"] == [
        "M0484-T-SUFFICIENCY", "M0484-T-NECESSITY",
    ]
    assert set(boundary["remaining_release_cut_set"]) == {
        "M0484-X-SOURCE", "M0484-S-FOUNDATION", "M0484-X-PROVENANCE",
        "M0484-X-TRUST", "M0484-X-READABLE", "M0484-X-WORKFLOW",
    }
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] is None
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    recipes = specs["recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {
        build_obligation_artifacts.CHECKER_RECIPE, build_obligation_artifacts.LEAN_RECIPE,
    }
    assert {node["validation_spec_id"] for node in nodes} <= {
        recipe["recipe_id"] for recipe in recipes
    }
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["timeout_seconds"] > 0 and recipe["coverage_boundary"]
        assert set(recipe["covered_obligation_ids"]) <= set(ids)
    structural = next(r for r in recipes if r["recipe_id"] == build_obligation_artifacts.CHECKER_RECIPE)
    assert structural["covered_declarations"] == [] and set(structural["covered_obligation_ids"]) == set(ids)
    lean_recipe = next(r for r in recipes if r["recipe_id"] == build_obligation_artifacts.LEAN_RECIPE)
    assert {name.rsplit(".", 1)[-1] for name in lean_recipe["covered_declarations"] if ".ObligationTree." in name} == CHECKED_DECLARATIONS

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|extern|native_decide|proof_wanted)\b|"
        r"^\s*(?:axiom|constant|unsafe|opaque)\b",
        re.MULTILINE,
    )
    code = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    code = re.sub(r"--.*", "", code)
    code = re.sub(r"^.*(?:assert_no_sorry|#print sorries).*$", "", code, flags=re.MULTILINE)
    assert forbidden.search(code) is None
    for name in CHECKED_DECLARATIONS:
        assert f"theorem {name}" in source
        assert f"assert_no_sorry {name}" in source
        assert f"#print axioms {name}" in source
    assert "#check lucas_lehmer_sufficiency" in source
    assert "#check lucas_lehmer_necessity" in source

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    source_path = MATHLIB / "Mathlib/NumberTheory/LucasLehmer.lean"
    assert sha256(source_path) == SOURCE_SHA256
    assert output("git", "rev-parse", "HEAD:Mathlib/NumberTheory/LucasLehmer.lean", cwd=MATHLIB) == (
        build_obligation_artifacts.MATHLIB_BLOB
    )
    mathlib_source = source_path.read_text(encoding="utf-8")
    markers = (
        "theorem sZMod_eq_s", "theorem residue_eq_zero_iff_sMod_eq_zero",
        "theorem closed_form", "lemma omega_pow_trace", "theorem card_units_lt",
        "theorem two_lt_q", "theorem omega_pow_formula", "theorem mersenne_coe_X",
        "theorem omega_pow_eq_neg_one", "theorem omega_pow_eq_one", "def omegaUnit",
        "theorem order_omega", "theorem order_ineq", "theorem lucas_lehmer_sufficiency",
        "theorem lucas_lehmer_necessity",
    )
    # Source uses Greek omega; normalize only identifiers for stable ASCII validator markers.
    normalized_source = mathlib_source.replace("ω", "omega")
    assert all(marker in normalized_source for marker in markers)
    audit = load(HERE / "anchor-audit.json")
    candidate = next(row for row in audit["candidates"] if row["candidate_id"].endswith("EXACT-COMPOSITION"))
    assert candidate["file_blob"] == build_obligation_artifacts.MATHLIB_BLOB
    assert candidate["file_sha256"] == SOURCE_SHA256
    assert candidate["terminal_proof_body_ids"] == [
        build_obligation_artifacts.SUFFICIENCY_BODY,
        build_obligation_artifacts.NECESSITY_BODY,
    ]
    assert candidate["terminal_source_lines"] == ["581-591", "593-608"]
    # Preserve the immutable predecessor packet as an input, but do not inherit its overclassification:
    # rev-5.6 section 4 caps the predecessor's E2 evidence at M1 until release-grade E1 exists.
    assert candidate["candidate_machine_classification"] == "M0-W"
    assert candidate["evidence_level"] == "E2_nonrelease_worker_probe"

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["candidate_result"]["classification"] == "M1"
    assert receipt["candidate_result"]["evidence_level"] == "E2_nonrelease_worker_probe"
    assert receipt["candidate_result"]["predecessor_recorded_classification"] == "M0-W"
    assert receipt["candidate_result"]["classification_rule"] == (
        "rev-5.6 section 4: E2 supports M1; M0-W requires E1"
    )
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids)
    assert receipt["typed_edge_count"] == len(edge_ids)
    assert set(receipt["graph_names"]) == GRAPH_NAMES
    assert receipt["composition_certificate_count"] == len(CHECKED_DECLARATIONS)
    assert receipt["unverified_decomposition_count"] == len(plans)
    assert receipt["accepted_closed_obligations"] == receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["support_state"] == "worker_self_tested_pending_master_acceptance"
    assert receipt["selftest_result"] == "pass"
    assert set(receipt["source_inputs"]) == {
        "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "skills/execute-stage1-rev56/SKILL.md",
        "Docs/Blueprint_Guidelines.md",
        "Formalizations/Lean/lean-toolchain",
        "Formalizations/Lean/lake-manifest.json",
        "Stage1_Instances/THM-M-0484/Statement.lean",
        "Stage1_Instances/THM-M-0484/anchor-audit.json",
    }
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM}/{name}"
        for name in (
            "ObligationTree.lean",
            "build_obligation_artifacts.py",
            "check_obligation_tree.py",
            "obligation-registry.json",
            "obligation-tree-receipt.json",
            "obligation-tree-validation.md",
            "obligation-tree.md",
            "typed-graphs.json",
            "validation-specs.json",
        )
    ]
    assert receipt["changed_paths"] == expected_changed
    status = output(
        "git", "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == set(expected_changed)

    if args.run_lean:
        lean_stdout = run_lean()
        expected_hash = receipt["lean_output_sha256"]
        assert hashlib.sha256(lean_stdout.encode()).hexdigest() == expected_hash
        print(f"Lean composition: pass and no sorryAx; stdout sha256 {expected_hash}")

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == receipt["base_revision"]
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["commands"] == receipt["worker_packet_commands"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]

    for path in HERE.iterdir():
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
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    readable_anchors = set(re.findall(r"\{#([^}]+)\}|^###\s+([a-z0-9-]+)$", readable, re.MULTILINE))
    readable_anchor_names = {value for pair in readable_anchors for value in pair if value}
    for node in nodes:
        assert node["public_readable_target"].rsplit("#", 1)[-1] in readable_anchor_names

    print(f"PASS THM-M-0484 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); exact pinned directions remain proof-phase cuts")


if __name__ == "__main__":
    main()
