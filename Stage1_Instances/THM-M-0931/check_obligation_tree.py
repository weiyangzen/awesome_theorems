#!/usr/bin/env python3
"""Fail-closed structural, source-pin, and Lean checks for THM-M-0931."""

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
ITEM = "S56-M-0931-OBLIGATION_TREE"
THEOREM = "THM-M-0931"
REGISTRY_ID = "THM-M-0931-OBLIGATIONS-v1"
BASE_REVISION = "b243ebc0f9058ba5afafef8240b92c2dfb2edc6e"
BASE_TREE = "b4b092069141ac54ea1ab5a6ea946192a30ec78c"
STATEMENT_SHA256 = "d0e7e43d896a0625e87b3fac55319d5e999351c8f74cdda4e699d9360d651020"
STATEMENT_JSON_SHA256 = "84e0e15bc6545467b3ed6442dd33c07a9f471d550546c17ebc2adb9040fe1b4d"
ANCHOR_SHA256 = "233ac0f45554eb565e7aab423a687a0a716e9d15760cd04acc0c8f604d09d53e"
ROOT_EXPRESSION = "b872e0de4aedbd0da8825d2c7dd9ecb30e01215131c61e73dc3050776711718a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EGZ_SHA256 = "13f8adfc07c9cffd89a0c2a2d3c265348b698fbf724d8b74e6de39434bbc79f7"
EGZ_BLOB = "dbe223c73d6c612461bc900d3d7dd70be3c1d747"
CHEVALLEY_SHA256 = "a47186d1cd0c94b9ce1660686e8986df54e338a821e3266a9280e7f28d138684"
CHEVALLEY_BLOB = "144087d302ebc67510cc3cf6903ab84706326b41"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
}
EXPECTED_IDS = [
    "M0931-ROOT", "M0931-S-INTERFACE", "M0931-S-BOUNDARY",
    "M0931-S-COUNT-TRANSPORT", "M0931-S-RESIDUE-TRANSPORT",
    "M0931-S-FOUNDATION", "M0931-T-ROOT-COMPOSE",
    "M0931-A-MULTISET-EGZ", "M0931-N-ENUMERATE",
    "M0931-L-INDEXED-EGZ", "M0931-B-INDUCTION", "M0931-B-ZERO",
    "M0931-B-ONE", "M0931-B-PRIME", "M0931-T-PRIME-CAST",
    "M0931-L-ZMOD-PRIME", "M0931-C-POLYNOMIALS",
    "M0931-L-DEGREE-BOUND", "M0931-X-CHEVALLEY-WARNING",
    "M0931-L-NONZERO-SOLUTION", "M0931-L-PRIME-CARD",
    "M0931-L-PRIME-SUM", "M0931-B-COMPOSITE",
    "M0931-C-DISJOINT-BLOCKS", "M0931-L-INNER-INDUCTION",
    "M0931-L-OUTER-INDUCTION", "M0931-T-COMPOSITE-ASSEMBLE",
    "M0931-X-SOURCE", "M0931-X-PROVENANCE", "M0931-X-TRUST",
    "M0931-X-READABLE", "M0931-X-WORKFLOW",
]


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def acyclic(edges: list[dict], name: str) -> None:
    adjacency: dict[str, list[str]] = {}
    for item in edges:
        adjacency.setdefault(item["from"], []).append(item["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        assert node not in visiting, f"{name} cycle at {node}"
        if node in visited:
            return
        visiting.add(node)
        for target in adjacency.get(node, []):
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for node in adjacency:
        visit(node)


def load_builder():
    path = HERE / "build_obligation_artifacts.py"
    spec = importlib.util.spec_from_file_location("m0931_obligation_builder", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    recipes = load("validation-specs.json")
    statement = load("statement.json")
    anchor = load("anchor-audit.json")

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert recipes["schema_version"] == "stage1-validation-specs/1.0"
    assert {registry["item_id"], bundle["item_id"], recipes["item_id"]} == {ITEM}
    assert {registry["theorem_id"], bundle["theorem_id"], recipes["theorem_id"]} == {THEOREM}
    assert registry["registry_id"] == bundle["registry_id"] == REGISTRY_ID
    assert registry["registry_version"] == 1 and registry["append_only_delta"] == []
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "statement.json") == STATEMENT_JSON_SHA256
    assert sha256(HERE / "anchor-audit.json") == ANCHOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget"
    )
    assert formal["elaborated_expression_sha256"] == ROOT_EXPRESSION
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert statement["audit_complete"] is False and statement["theorem_complete"] is False
    assert anchor["canonical_target_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["canonical_statement_file_sha256"] == STATEMENT_SHA256
    decision = anchor["inventory_decision"]
    assert decision["root_machine_candidate_classification"] == (
        "M0-W_candidate_pending_downstream_acceptance"
    )
    assert decision["candidate_accepted_by_master"] is False
    assert anchor["audit_complete"] is False and anchor["theorem_complete"] is False

    target_manifest = json.loads(
        (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
    )
    target = next(row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1470
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8")
    )
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0931-ANCHOR_AUDIT"]
    assert item["owned_paths"] == ["Stage1_Instances/THM-M-0931"]
    assert item["deliverable"] == (
        "Freeze the obligation registry and typed proof/provenance/workflow graphs."
    )

    builder = load_builder()
    expected_registry, expected_bundle, expected_recipes = builder.build()
    assert registry == expected_registry
    assert bundle == expected_bundle
    assert recipes == expected_recipes

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert ids == EXPECTED_IDS and len(ids) == len(id_set) == 32
    assert registry["root_obligation_id"] == bundle["root_node_id"] == "M0931-ROOT"
    required_obligation = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility",
        "readable_eligibility", "risk_class", "exclusion_reason",
        "terminal_proof_body_id",
    }
    allowed_kinds = {
        "root", "definition", "normalization", "reduction", "branch",
        "construction", "bridge", "core_lemma", "computation",
        "certificate", "transport", "terminal",
    }
    for row in rows:
        assert set(row) == required_obligation
        assert row["kind"] in allowed_kinds
        assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] in {"required", "not_applicable"}
        assert row["risk_class"] in {"critical", "high", "normal", "low"}
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
            or row["readable_eligibility"] != "required"
        )
        assert bool(row["exclusion_reason"]) == excluded

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility",
        "readable_eligibility", "risk_class", "exclusion_reason",
        "terminal_proof_body_id",
    )
    denominator = canonical_digest([{key: row[key] for key in fields} for row in rows])
    assert denominator == registry["denominator_sha256"]
    assert denominator == bundle["registry_denominator_sha256"]
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
    assert set(registry["layer_exclusions"]) == {
        "additional_symmetry_sign_order_or_representative_normalization",
        "external_computation",
    }
    assert all(
        value["status"] == "not_applicable_pending_independent_approval"
        and value["reason"]
        for value in registry["layer_exclusions"].values()
    )
    observed = registry["status_observed_after_freeze"]
    assert observed["accepted_closed_obligations"] == []
    assert observed["accepted_root_machine_debt"] == "M3"
    assert "M0-W candidate remains unaccepted" in observed["candidate_route"]

    required_node = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target",
        "output", "human_debt", "machine_debt", "readability_debt",
        "evidence_ids", "source_crosswalk_id", "provenance_id",
        "foundation_profile", "tcb_profile", "computation_record", "step_budget",
        "semantic_step_ledger", "public_readable_target", "validation_spec_id",
        "status_boundary", "task_ids", "owned_sources", "owner", "reviewer",
        "validity",
    }
    nodes = bundle["nodes"]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    assert len(nodes) == len(node_by_id) == len(ids) and set(node_by_id) == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    allowed_external = {"frozen-formal-context", "pinned-mathlib-source"}
    for node in nodes:
        assert set(node) == required_node
        assert node["node_id"] == THEOREM + "-" + node["obligation_id"].removeprefix("M0931-")
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert node["evidence_ids"] == []
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"]
        for step in ledger:
            assert set(step) == {
                "step_id", "premise_ids", "inference", "source_locator",
                "output", "outgoing_use",
            }
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            assert set(step["premise_ids"]) <= id_set | allowed_external
            step_ids.add(step["step_id"])
        path, anchor_name = node["public_readable_target"].split("#", 1)
        assert path == "Stage1_Instances/THM-M-0931/obligation-tree.md"
        assert f"### {anchor_name}" in readable
        assert node["validation_spec_id"] == "VAL-M0931-OBLIGATION-BUNDLE"
        assert "no accepted m0 root" in node["status_boundary"].lower()
        assert node["task_ids"] == [ITEM, "S56-M-0931-PROOF"]
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]

    allowed_edges = {
        "proof_requires", "composes", "logical_decomposition", "source_map",
        "expository_decomposition", "equivalent_to", "transports",
        "evidence_for", "provenance_of", "documents", "trusts",
        "workflow_depends_on",
    }
    assert set(bundle["graphs"]) == GRAPH_NAMES
    workflow_nodes = set(bundle["workflow_task_nodes"])
    assert workflow_nodes == {
        "S56-M-0931-STATEMENT", "S56-M-0931-ANCHOR_AUDIT", ITEM,
        "S56-M-0931-PROOF", "S56-M-0931-VALIDATION", "S56-M-0931-RELEASE",
    }
    edge_ids: set[str] = set()
    for name, graph_value in bundle["graphs"].items():
        expected_in: dict[str, list[str]] = {}
        expected_out: dict[str, list[str]] = {}
        for item_edge in graph_value["edges"]:
            assert item_edge["edge_id"] not in edge_ids
            assert item_edge["type"] in allowed_edges
            endpoints = workflow_nodes if name == "workflow" else id_set
            assert item_edge["from"] in endpoints and item_edge["to"] in endpoints
            if name == "workflow":
                assert item_edge["type"] == "workflow_depends_on"
            else:
                assert item_edge["type"] != "workflow_depends_on"
            expected_out.setdefault(item_edge["from"], []).append(item_edge["edge_id"])
            expected_in.setdefault(item_edge["to"], []).append(item_edge["edge_id"])
            edge_ids.add(item_edge["edge_id"])
        assert graph_value["out"] == expected_out
        assert graph_value["in"] == expected_in
        if name != "proof":
            acyclic(graph_value["edges"], name)
    assert len(edge_ids) == 46

    proof_rows = {item_edge["edge_id"]: item_edge for item_edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for item_edge in proof_rows.values():
        assert item_edge["type"] in {"proof_requires", "composes"}
        reverse = proof_rows[item_edge["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == item_edge["edge_id"]
        assert (reverse["from"], reverse["to"]) == (item_edge["to"], item_edge["from"])
        assert {item_edge["type"], reverse["type"]} == {"proof_requires", "composes"}
        if item_edge["type"] == "proof_requires":
            children.setdefault(item_edge["from"], []).append(item_edge["to"])

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit_proof(node: str) -> None:
        assert node not in visiting, f"proof cycle at {node}"
        if node in visited:
            return
        visiting.add(node)
        for child in children.get(node, []):
            visit_proof(child)
        visiting.remove(node)
        visited.add(node)

    visit_proof("M0931-ROOT")
    assert visited == {
        "M0931-ROOT", "M0931-T-ROOT-COMPOSE", "M0931-A-MULTISET-EGZ",
        "M0931-S-COUNT-TRANSPORT", "M0931-L-INDEXED-EGZ", "M0931-N-ENUMERATE",
    }
    certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
    assert set(certificates) == set(children) == {"M0931-ROOT", "M0931-A-MULTISET-EGZ"}
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in rows}
    for parent, certificate in certificates.items():
        assert certificate["required_child_ids"] == children[parent]
        assert certificate["parent_statement_fingerprint"] == fingerprints[parent]
        assert certificate["required_child_statement_fingerprints"] == {
            child: fingerprints[child] for child in children[parent]
        }
        assert certificate["certificate_kind"] == "lean_abstract_child_harness"
        assert certificate["introduces_undeclared_premises"] is False
        assert certificate["status"] == "provisionally_elaborated_not_accepted"
    plans = bundle["unverified_decomposition_plans"]
    assert len(plans) == 6
    for plan in plans:
        assert plan["parent_obligation_id"] in id_set
        assert set(plan["planned_child_ids"]) <= id_set
        assert plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        assert plan["required_future_certificate"]
    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False

    assert len(recipes["recipes"]) == 1
    recipe = recipes["recipes"][0]
    assert recipe["recipe_id"] == "VAL-M0931-OBLIGATION-BUNDLE"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "python3", "-B", "Stage1_Instances/THM-M-0931/check_obligation_tree.py"
    ]
    assert recipe["env_allowlist"] == {} and recipe["timeout_seconds"] == 240
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["closure_credit"] is False
    assert recipe["covered_obligation_ids"] == ids

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    egz_path = MATHLIB / "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean"
    cw_path = MATHLIB / "Mathlib/FieldTheory/ChevalleyWarning.lean"
    assert sha256(egz_path) == EGZ_SHA256 and sha256(cw_path) == CHEVALLEY_SHA256
    assert output("git", "rev-parse", "HEAD:Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean", cwd=MATHLIB) == EGZ_BLOB
    assert output("git", "rev-parse", "HEAD:Mathlib/FieldTheory/ChevalleyWarning.lean", cwd=MATHLIB) == CHEVALLEY_BLOB
    egz_source = egz_path.read_text(encoding="utf-8")
    for marker in (
        "private theorem ZMod.erdos_ginzburg_ziv_prime",
        "private theorem Int.erdos_ginzburg_ziv_prime",
        "induction n using Nat.prime_composite_induction generalizing ι",
        "| zero => exact",
        "| one => simpa using exists_subset_card_eq hs",
        "| prime p hp =>",
        "| composite m hm ihm n hn ihn =>",
        "theorem Int.erdos_ginzburg_ziv_multiset",
        "Multiset.map_fst_le_of_subset_toEnumFinset",
    ):
        assert marker in egz_source, marker
    cw_source = cw_path.read_text(encoding="utf-8")
    assert "theorem char_dvd_card_solutions_of_add_lt" in cw_source
    assert "char_dvd_card_solutions_of_fintype_sum_lt p this" in cw_source

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|implemented_by|extern|"
        r"native_decide|TODO|FIXME)\b"
    )
    assert forbidden.search(without_comments) is None
    for marker in (
        "import Statement", "def AtLeastCountAnchor : Prop",
        "def IndexedIntegerEGZ : Prop", "def MultisetEnumerationTransport : Prop",
        "def ExactCountTransport : Prop", "def RootComposition : Prop",
        "theorem multisetEnumerationTransport_checked",
        "theorem atLeastCountAnchor_of_indexed_and_enumeration",
        "theorem exactCountTransport_checked", "theorem rootComposition_checked",
        "theorem root_of_terminal_packages",
        "#print axioms Int.erdos_ginzburg_ziv_multiset",
        "#print axioms root_of_terminal_packages",
    ):
        assert marker in source, marker

    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0931-obligation-") as temp_dir:
        statement_run = subprocess.run(
            [lean_exe, "Statement.lean", "-o", str(Path(temp_dir) / "Statement.olean")],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement_run.returncode:
            sys.stdout.write(statement_run.stdout)
            raise SystemExit(statement_run.returncode)
        lean_run = subprocess.run(
            [lean_exe, "ObligationTree.lean"],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": temp_dir + ":" + lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if lean_run.returncode:
            sys.stdout.write(lean_run.stdout)
            raise SystemExit(lean_run.returncode)
    normalized = re.sub(r"\s+", " ", lean_run.stdout)
    assert normalized.count("propext, Classical.choice, Quot.sound") == 4
    assert normalized.count("propext, Quot.sound") == 4
    assert "sorryAx" not in lean_run.stdout and "declaration uses 'sorry'" not in lean_run.stdout
    for declaration in (
        "Int.erdos_ginzburg_ziv_multiset", "Int.erdos_ginzburg_ziv",
        "char_dvd_card_solutions_of_add_lt", "multisetEnumerationTransport_checked",
        "atLeastCountAnchor_of_indexed_and_enumeration",
        "exactCountTransport_checked", "rootComposition_checked",
        "root_of_terminal_packages",
    ):
        assert declaration in lean_run.stdout

    receipt_path = HERE / "obligation-tree-receipt.json"
    if receipt_path.exists():
        receipt = load("obligation-tree-receipt.json")
        assert receipt["schema_version"] == "stage1-obligation-tree-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["verdict"] == "no_state_change"
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["inventory_count"] == len(ids)
        assert receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["substantive_ledger_step_count"] == len(step_ids)
        assert receipt["accepted_closed_obligations"] == []
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
            "H": "H1", "M": "M3", "R": "R4"
        }
        assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
        packet_path = ROOT / ".stage1-worker-selftest.json"
        if packet_path.exists():
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            assert set(packet) == {
                "item_id", "changed_paths", "commands", "output_summary",
                "base_revision", "known_failures", "state",
            }
            assert packet["item_id"] == ITEM and packet["state"] == "[_]"
            assert packet["base_revision"] == BASE_REVISION
            assert packet["changed_paths"] == receipt["changed_paths"]
            assert packet["known_failures"] == receipt["known_failures"]
            assert packet["commands"] and packet["output_summary"].startswith("PASS:")

    print(
        f"PASS THM-M-0931 obligation tree: {len(ids)} registry records, "
        f"{len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps"
    )
    print(f"registry denominator sha256: {denominator}")
    print(f"Lean output sha256: {hashlib.sha256(lean_run.stdout.encode()).hexdigest()}")
    print(
        "Lean: occurrence and exact-root conditional compositions elaborate; "
        "pinned bodies remain proof-phase candidates"
    )
    print("accepted root remains H1/M3/R4; accepted obligations 0; theorem_complete=false")


if __name__ == "__main__":
    main()
