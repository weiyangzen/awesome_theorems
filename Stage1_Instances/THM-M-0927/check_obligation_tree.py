#!/usr/bin/env python3
"""Fail-closed structural and Lean checks for the THM-M-0927 tree freeze."""

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
ITEM = "S56-M-0927-OBLIGATION_TREE"
THEOREM = "THM-M-0927"
REGISTRY_ID = "THM-M-0927-OBLIGATIONS-v1"
ROOT_ID = "M0927-ROOT"
BASE_REVISION = "ff3db6d51326417873f49c410421f8f3e13be993"
BASE_TREE = "9160a80a3e3588fd96fcd79323230668cc7d3df1"
STATEMENT_SHA256 = "72172fb6015846b808a81dfc4995767dec5381de5845f68c47cbc5fdb2eeed8d"
STATEMENT_JSON_SHA256 = "4649bc7f024d4dfd353d857ada5829b963c08da5549e060f63e9f6416a37bf95"
ANCHOR_SHA256 = "166999961169125272df80df7948f19be2e31b67fc072c8ae6b66286487a1933"
ROOT_EXPRESSION = "0a05e8c4976c01759ef82d364afc86f498f700edc1a0fcb3f8935765992b5a2f"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
GOLDEN_SHA256 = "e3a6e5160e654dfb4c5594c66a624fa7a5edffa4c1b839d992be7d1ba2dd7ac3"
GOLDEN_BLOB = "9e9a9f050354f828a54fb235846405987daa4971"
LINEAR_RECURRENCE_SHA256 = "244faec4c5500016dd0963852935ffb0be8a1adf5b9f330c5716d7d36dd4ccb1"
LINEAR_RECURRENCE_BLOB = "e644c74090240f527cc982d19d1e5f7cf342a387"
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
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
LEDGER_FIELDS = {
    "step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use",
}
ALLOWED_KINDS = {
    "root", "definition", "normalization", "reduction", "branch", "construction",
    "bridge", "core_lemma", "computation", "certificate", "transport", "terminal",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
HUMAN_DEBTS = {f"H{index}" for index in range(6)}
MACHINE_DEBTS = {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
READABILITY_DEBTS = {f"R{index}" for index in range(5)}


def load(name: str) -> dict:
    path = HERE / name

    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise AssertionError(f"duplicate JSON key in {name}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), name
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_slice(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1:end])).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def acyclic(edges: list[dict], name: str) -> None:
    adjacency: dict[str, list[str]] = {}
    for item in edges:
        adjacency.setdefault(item["from"], []).append(item["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        assert node not in visiting, f"cycle in {name} at {node}"
        if node in visited:
            return
        visiting.add(node)
        for target in adjacency.get(node, []):
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for node in adjacency:
        visit(node)


def run_lean() -> tuple[subprocess.CompletedProcess[str], subprocess.CompletedProcess[str]]:
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    environment = os.environ | {
        "LEAN_PATH": lean_path,
        "LC_ALL": "C",
        "LANG": "C",
        "NO_COLOR": "1",
        "TZ": "UTC",
    }
    with tempfile.TemporaryDirectory(prefix="thm-m-0927-obligation-") as temp_dir:
        statement = subprocess.run(
            [lean_exe, "Statement.lean", "-o", str(Path(temp_dir) / "Statement.olean")],
            cwd=HERE,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        obligation = subprocess.run(
            [lean_exe, "ObligationTree.lean"],
            cwd=HERE,
            env=environment | {"LEAN_PATH": temp_dir + ":" + lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if obligation.returncode:
            sys.stdout.write(obligation.stdout)
            raise SystemExit(obligation.returncode)
    return statement, obligation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    validation = load("validation-specs.json")
    statement = load("statement.json")
    anchor = load("anchor-audit.json")
    instance = load("instance.json")

    expected_registry, expected_bundle, expected_validation, expected_readable = (
        build_obligation_artifacts.build()
    )
    for name, value in (
        ("obligation-registry.json", expected_registry),
        ("typed-graphs.json", expected_bundle),
        ("validation-specs.json", expected_validation),
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"
    assert (HERE / "obligation-tree.md").read_text(encoding="utf-8") == expected_readable

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert validation["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["registry_id"] == bundle["registry_id"] == REGISTRY_ID
    assert {registry["item_id"], bundle["item_id"], validation["item_id"]} == {ITEM}
    assert {registry["theorem_id"], bundle["theorem_id"], validation["theorem_id"]} == {THEOREM}
    assert registry["registry_version"] == 1 and registry["append_only_delta"] == []
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "statement.json") == STATEMENT_JSON_SHA256
    assert sha256(HERE / "anchor-audit.json") == ANCHOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256
    assert registry["architecture_source_sha256"] == sha256(HERE / "ObligationTree.lean")
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0927.BinetFormulaTarget"
    assert formal["elaborated_expression_sha256"] == ROOT_EXPRESSION
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert anchor["canonical_target_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert anchor["inventory_decision"]["root_machine_candidate_classification"] == (
        "M0-W_candidate_pending_downstream_acceptance"
    )
    assert anchor["inventory_decision"]["candidate_accepted_by_master"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert statement["audit_complete"] is statement["theorem_complete"] is False
    assert anchor["audit_complete"] is anchor["theorem_complete"] is False

    targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1546 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0927-ANCHOR_AUDIT"
    )
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] == "[ ]" and item["depends_on"] == [predecessor["id"]]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == (
        "Freeze the obligation registry and typed proof/provenance/workflow graphs."
    )
    assert predecessor["state"] == "[_]"

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == len(build_obligation_artifacts.ROWS) == 26
    assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == ROOT_ID
    for row in rows:
        assert set(row) == REGISTRY_FIELDS
        assert row["kind"] in ALLOWED_KINDS
        assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] in {"required", "not_applicable"}
        assert row["risk_class"] in {"critical", "high", "normal", "low"}
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
            or row["readable_eligibility"] != "required"
        )
        assert bool(row["exclusion_reason"]) == excluded, row["obligation_id"]
    denominator = canonical_digest([
        {field: row[field] for field in (
            "obligation_id", "statement_fingerprint", "kind", "root_relevant",
            "machine_eligibility", "human_source_eligibility", "readable_eligibility",
            "risk_class", "exclusion_reason", "terminal_proof_body_id",
        )} for row in rows
    ])
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    frozen = registry["frozen_denominators"]
    assert frozen["inventory"] == ids
    for key, field, value in (
        ("required_machine", "machine_eligibility", "required"),
        ("required_human_source", "human_source_eligibility", "required"),
        ("required_readable", "readable_eligibility", "required"),
        ("informational_overlays", "machine_eligibility", "informational"),
    ):
        assert frozen[key] == [row["obligation_id"] for row in rows if row[field] == value]
    layers = registry["mandatory_layers"]
    assert set(layers) == {"S", "N", "B", "C", "L", "X", "T"}
    assert all(layers[layer] and set(layers[layer]) <= id_set for layer in layers)
    assert set(registry["layer_exclusions"]) == {"additional_case_splits", "external_computation"}
    assert all(
        value["status"] == "not_applicable_pending_independent_approval" and value["reason"]
        for value in registry["layer_exclusions"].values()
    )
    observed = registry["status_observed_after_freeze"]
    assert observed["accepted_closed_obligations"] == []
    assert observed["accepted_root_machine_debt"] == "M3"
    assert "M0-W route candidate" in observed["audited_candidate_classification"]
    assert registry["proof_body_aliases"]["Real.coe_fib_eq"].startswith(
        "pointwise wrapper over Real.coe_fib_eq'"
    )

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    allowed_external = {"frozen-formal-context", "frozen-source-context"}
    for node in nodes:
        assert set(node) == NODE_FIELDS
        assert node["node_id"] == THEOREM + "-" + node["obligation_id"].removeprefix("M0927-")
        assert node["human_debt"] in HUMAN_DEBTS
        assert node["machine_debt"] in MACHINE_DEBTS
        assert node["readability_debt"] in READABILITY_DEBTS
        assert node["evidence_ids"] == []
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"]
        for step in ledger:
            assert set(step) == LEDGER_FIELDS
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            assert set(step["premise_ids"]) <= id_set | allowed_external
            step_ids.add(step["step_id"])
        path, anchor_name = node["public_readable_target"].split("#", 1)
        assert path == f"Stage1_Instances/{THEOREM}/obligation-tree.md"
        assert f"### {anchor_name}" in readable
        assert node["validation_spec_id"] == "VAL-" + node["obligation_id"]
        assert node["task_ids"] == [ITEM, "S56-M-0927-PROOF"]
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]

    assert set(bundle["graphs"]) == GRAPH_NAMES
    workflow_nodes = set(bundle["workflow_task_nodes"])
    assert workflow_nodes == {
        "S56-M-0927-STATEMENT", "S56-M-0927-ANCHOR_AUDIT", ITEM,
        "S56-M-0927-PROOF", "S56-M-0927-VALIDATION", "S56-M-0927-RELEASE",
    }
    edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        expected_in: dict[str, list[str]] = {}
        expected_out: dict[str, list[str]] = {}
        for item_edge in graph["edges"]:
            assert item_edge["edge_id"] not in edge_ids
            assert item_edge["type"] in ALLOWED_EDGES
            endpoints = workflow_nodes if name == "workflow" else id_set
            assert item_edge["from"] in endpoints and item_edge["to"] in endpoints
            assert (item_edge["type"] == "workflow_depends_on") == (name == "workflow")
            expected_out.setdefault(item_edge["from"], []).append(item_edge["edge_id"])
            expected_in.setdefault(item_edge["to"], []).append(item_edge["edge_id"])
            edge_ids.add(item_edge["edge_id"])
        assert graph["out"] == expected_out and graph["in"] == expected_in
        if name != "proof":
            acyclic(graph["edges"], name)
    assert len(edge_ids) == 47

    proof = {item_edge["edge_id"]: item_edge for item_edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for item_edge in proof.values():
        assert item_edge["type"] in {"proof_requires", "composes"}
        reverse = proof[item_edge["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == item_edge["edge_id"]
        assert (reverse["from"], reverse["to"]) == (item_edge["to"], item_edge["from"])
        assert {item_edge["type"], reverse["type"]} == {"proof_requires", "composes"}
        if item_edge["type"] == "proof_requires":
            children.setdefault(item_edge["from"], []).append(item_edge["to"])
    reachable: set[str] = set()

    def visit_proof(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            visit_proof(child)

    visit_proof(ROOT_ID)
    assert reachable == {
        ROOT_ID, "M0927-T-ROOT-COMPOSE", "M0927-T-FUNCTION-BINET",
        "M0927-S-FUNCTION-TRANSPORT", "M0927-S-RADICAL-TRANSPORT",
    }
    certificates = {
        row["parent_obligation_id"]: row for row in bundle["composition_certificates"]
    }
    assert set(certificates) == set(children) == {ROOT_ID}
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in rows}
    certificate = certificates[ROOT_ID]
    assert certificate["required_child_ids"] == children[ROOT_ID]
    assert certificate["parent_statement_fingerprint"] == fingerprints[ROOT_ID]
    assert certificate["required_child_statement_fingerprints"] == {
        child: fingerprints[child] for child in children[ROOT_ID]
    }
    assert certificate["declaration"].endswith("root_of_terminal_packages")
    assert certificate["certificate_kind"] == "lean_abstract_child_harness"
    assert certificate["introduces_undeclared_premises"] is False
    assert certificate["status"] == "provisionally_elaborated_not_accepted"
    plans = bundle["unverified_decomposition_plans"]
    assert len(plans) == len(build_obligation_artifacts.LOGICAL_PLANS) == 8
    for plan in plans:
        assert plan["parent_obligation_id"] in id_set
        assert set(plan["planned_child_ids"]) <= id_set
        assert plan["status"] == (
            "source_body_decomposition_unverified_as_child_to_parent_composition"
        )
        assert plan["required_future_certificate"]

    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["minimal_open_machine_proof_cut_sets"] == [["M0927-T-FUNCTION-BINET"]]

    recipes = validation["recipes"]
    assert len(recipes) == len(ids)
    recipe_fields = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "closure_credit",
    }
    assert {recipe["recipe_id"] for recipe in recipes} == {"VAL-" + identifier for identifier in ids}
    for recipe in recipes:
        assert set(recipe) == recipe_fields
        assert recipe["cwd"] == "."
        assert recipe["argv"] == [
            "python3", "-B", "Stage1_Instances/THM-M-0927/check_obligation_tree.py",
        ]
        assert recipe["env_allowlist"] == {"LC_ALL": "C", "TZ": "UTC"}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["closure_credit"] is False and len(recipe["covered_obligation_ids"]) == 1

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    golden = MATHLIB / "Mathlib/NumberTheory/Real/GoldenRatio.lean"
    recurrence = MATHLIB / "Mathlib/Algebra/LinearRecurrence.lean"
    assert sha256(golden) == GOLDEN_SHA256
    assert sha256(recurrence) == LINEAR_RECURRENCE_SHA256
    assert output("git", "rev-parse", "HEAD:Mathlib/NumberTheory/Real/GoldenRatio.lean", cwd=MATHLIB) == GOLDEN_BLOB
    assert output("git", "rev-parse", "HEAD:Mathlib/Algebra/LinearRecurrence.lean", cwd=MATHLIB) == LINEAR_RECURRENCE_BLOB
    assert hash_slice(golden, 180, 195) == (
        "e3e11b1c82c6f3718202d10bc5fe89a811e4c0890b0dcd535014a2a6f1385814"
    )
    golden_source = golden.read_text(encoding="utf-8")
    for marker in (
        "def fibRec : LinearRecurrence", "theorem fibRec_charPoly_eq",
        "theorem fib_isSol_fibRec", "theorem geom_goldenRatio_isSol_fibRec",
        "theorem geom_goldenConj_isSol_fibRec", "theorem coe_fib_eq' :",
        "rw [fibRec.sol_eq_of_eq_init]", "theorem coe_fib_eq :",
    ):
        assert marker in golden_source
    assert "theorem sol_eq_of_eq_init" in recurrence.read_text(encoding="utf-8")

    lean_source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque|implemented_by|extern|"
        r"native_decide|TODO|FIXME|proof_wanted)\b"
    )
    assert forbidden.search(without_comments(lean_source)) is None
    for marker in (
        "import Statement", "def FunctionNamedRootPackage : Prop",
        "def PointwiseNamedRootPackage : Prop", "def FunctionToPointwiseTransport : Prop",
        "def NamedRootToRadicalTransport : Prop", "def RootComposition : Prop",
        "theorem functionToPointwiseTransport_checked",
        "theorem namedRootToRadicalTransport_checked", "theorem rootComposition_checked",
        "theorem root_of_terminal_packages", "#print axioms Real.coe_fib_eq'",
        "assert_no_sorry root_of_terminal_packages",
    ):
        assert marker in lean_source
    statement_run, lean_run = run_lean()
    normalized = re.sub(r"\s+", " ", lean_run.stdout)
    assert normalized.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 6
    assert lean_run.stdout.count("Declarations are sorry-free!") == 6
    assert "sorryAx" not in lean_run.stdout and "declaration uses 'sorry'" not in lean_run.stdout
    for declaration in (
        "Real.coe_fib_eq'", "Real.coe_fib_eq", "functionToPointwiseTransport_checked",
        "namedRootToRadicalTransport_checked", "rootComposition_checked",
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
        assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["substantive_ledger_step_count"] == len(step_ids)
        assert receipt["unverified_decomposition_count"] == len(plans)
        assert receipt["accepted_closed_obligations"] == receipt["accepted_receipt_ids"] == []
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]
        assert receipt["audit_complete"] is receipt["theorem_complete"] is False
        assert receipt["lean_output_sha256"] == hashlib.sha256(lean_run.stdout.encode()).hexdigest()
        assert receipt["artifact_hashes_before_receipt_and_packet"] == {
            name: f"sha256:{sha256(ROOT / name)}"
            for name in receipt["artifact_hashes_before_receipt_and_packet"]
        }
        if args.worker_packet:
            packet_path = args.worker_packet
            if not packet_path.is_absolute():
                packet_path = ROOT / packet_path
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            assert set(packet) == {
                "item_id", "changed_paths", "commands", "output_summary",
                "base_revision", "known_failures", "state",
            }
            assert packet["item_id"] == ITEM and packet["state"] == "[_]"
            assert packet["base_revision"] == BASE_REVISION
            assert packet["changed_paths"] == receipt["changed_paths"]
            assert packet["commands"] == receipt["commands_and_results"]
            assert packet["output_summary"] == receipt["output_summary"]
            assert packet["known_failures"] == receipt["known_failures"]
        for relative in receipt["changed_paths"]:
            check_text_file(ROOT / relative)

    print(
        f"PASS {THEOREM} obligation tree: {len(ids)} registry records, "
        f"{len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps"
    )
    print(f"registry denominator sha256: {denominator}")
    print(f"Lean output sha256: {hashlib.sha256(lean_run.stdout.encode()).hexdigest()}")
    print("Lean: exact abstract-child root composition elaborates; pinned body remains a candidate")
    print("accepted root remains H1/M3/R4; accepted obligations 0; theorem_complete=false")


if __name__ == "__main__":
    main()
