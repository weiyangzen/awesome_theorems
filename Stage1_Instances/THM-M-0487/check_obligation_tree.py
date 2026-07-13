#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0487 obligation freeze."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0487-OBLIGATION_TREE"
THEOREM = "THM-M-0487"
ROOT_ID = "M0487-ROOT"
BASE_REVISION = "b56df790fc94c5366cf919a6fe5411d06b427c59"
BASE_TREE = "18ba629d4c00333f6e17018905f4fbd30558bb4c"
ROOT_EXPRESSION = "29ac94dd615869191754270061d8fe7123991d403a07bbdf27a09f706665e703"
STATEMENT_SHA256 = "9d0200046173c0b0d9d0b52cbf696087f4beea6946c92bfa41f03402a4090b0d"
ANCHOR_SHA256 = "569ce7bc7b56c01ae6a8a57f03071e2d95d0bc01aeae28cdd2181217f8a99f36"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
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
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
ALLOWED_NODE_KINDS = {
    "root", "definition", "normalization", "reduction", "branch", "construction",
    "bridge", "core_lemma", "computation", "certificate", "transport", "terminal",
    "source_boundary",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
GRAPH_EDGE_TYPES = {
    "proof": {"proof_requires", "composes"},
    "refinement": {"logical_decomposition", "equivalent_to", "transports"},
    "provenance": {"source_map", "provenance_of"},
    "evidence": {"evidence_for"},
    "trust": {"trusts"},
    "documentation": {"documents"},
    "workflow": {"workflow_depends_on"},
}
EXPECTED_IDS = tuple(build_obligation_artifacts.oid(row[0]) for row in build_obligation_artifacts.ROWS)
CHECKED = build_obligation_artifacts.CHECKED_INTERFACES
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ObligationTree.lean",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/build_obligation_artifacts.py",
    f"Stage1_Instances/{THEOREM}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM}/check_intake.py",
    f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
    f"Stage1_Instances/{THEOREM}/check_statement_artifacts.py",
    f"Stage1_Instances/{THEOREM}/instance.json",
    f"Stage1_Instances/{THEOREM}/obligation-registry.json",
    f"Stage1_Instances/{THEOREM}/obligation-tree-receipt.json",
    f"Stage1_Instances/{THEOREM}/obligation-tree-validation.md",
    f"Stage1_Instances/{THEOREM}/obligation-tree.md",
    f"Stage1_Instances/{THEOREM}/typed-graphs.json",
    f"Stage1_Instances/{THEOREM}/validation-specs.json",
}
NEW_FILES = {
    "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
    "obligation-registry.json", "obligation-tree-receipt.json",
    "obligation-tree-validation.md", "obligation-tree.md", "typed-graphs.json",
    "validation-specs.json",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command_output(*args: str, cwd: Path) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def run_lean_composition() -> str:
    lean = command_output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = command_output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="stage1-thm-m-0487-obligation-") as temporary:
        temp = Path(temporary)
        statement = subprocess.run(
            [
                lean,
                "-o", str(temp / "Statement.olean"),
                "-i", str(temp / "Statement.ilean"),
                str(HERE / "Statement.lean"),
            ],
            cwd=HERE,
            env={**os.environ, "LEAN_PATH": lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        assert statement.returncode == 0, statement.stdout
        assert (temp / "Statement.olean").is_file()
        assert (temp / "Statement.ilean").is_file()
        tree = subprocess.run(
            [lean, str(HERE / "ObligationTree.lean")],
            cwd=HERE,
            env={**os.environ, "LEAN_PATH": f"{temporary}:{lean_path}"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        assert tree.returncode == 0, tree.stdout
        return tree.stdout


def check_edge_semantics(graph_name: str, row: dict, obligations: dict[str, dict]) -> None:
    assert row["type"] in GRAPH_EDGE_TYPES[graph_name]
    source = obligations[row["from"]]
    target = obligations[row["to"]]
    if graph_name == "proof":
        assert source["root_relevant"] is target["root_relevant"] is True
        assert source["machine_eligibility"] == target["machine_eligibility"] == "required"
    elif row["type"] == "source_map":
        assert source["kind"] == "source_boundary" and source["root_relevant"] is False
        assert target["root_relevant"] is True
    elif row["type"] == "provenance_of":
        assert source["kind"] == "certificate" and source["root_relevant"] is False
    elif graph_name == "evidence":
        assert source["kind"] == "certificate" and source["root_relevant"] is False
        assert row["to"] != "M0487-X-EVIDENCE"
    elif graph_name == "trust":
        assert source["root_relevant"] is True
        assert row["to"] in {"M0487-S-FOUNDATION", "M0487-X-COMPUTATION", "M0487-X-TRUST"}
    elif graph_name == "documentation":
        assert row["from"] == "M0487-X-READABLE"
    elif graph_name == "workflow":
        assert row["from"] == "M0487-X-WORKFLOW"
    else:
        assert source["root_relevant"] is target["root_relevant"] is True


def check_acyclic(edges: list[dict]) -> None:
    adjacency: dict[str, list[str]] = {}
    for row in edges:
        adjacency.setdefault(row["from"], []).append(row["to"])
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


def main() -> None:
    registry = load(HERE / "obligation-registry.json")
    bundle = load(HERE / "typed-graphs.json")
    specs = load(HERE / "validation-specs.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    expected = build_obligation_artifacts.build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0487-OBLIGATIONS-v1"

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1366,
        "phase": "obligation_tree", "layer": 3, "state": "[ ]",
        "depends_on": ["S56-M-0487-ANCHOR_AUDIT"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0487-ANCHOR_AUDIT"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_task["evidence_ids"] == []
    assert task_dag["accepted_states"] == []

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "anchor-audit.json") == ANCHOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256
    source_inputs = registry["source_architecture_inputs"]
    assert source_inputs["helfgott_main_tex_sha256"] == (
        "86ea555015d974174c744dbf7b78d777015e959f2986c0b9b6873634f44e0fed"
    )
    assert source_inputs["helfgott_platt_arxiv"] == "1305.3062v2"
    assert source_inputs["helfgott_platt_compressed_source_sha256"] == (
        "376ec723223d4f014e55f80263137b88800c3a71d6c021cdab0a476b171bf408"
    )
    assert source_inputs["helfgott_platt_decompressed_tex_sha256"] == (
        "5a9026c9850de02d7e5e78e8da734afadde0104a4be76d2cfabc74b1aae50dac"
    )
    assert source_inputs["helfgott_platt_exact_upper_endpoint"] == (
        "8875694145621773516800000000000"
    )

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert tuple(ids) == EXPECTED_IDS and len(ids) == len(set(ids)) == 54
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(set(row) == REGISTRY_FIELDS for row in rows)
    for row in rows:
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
        )
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]
        if row["obligation_id"].startswith("M0487-X-"):
            assert row["obligation_id"] not in bundle["closure_boundary"]["proof_reachable_obligations"]

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
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
    assert all(
        row["status"].endswith("pending_independent_approval")
        for row in registry["layer_exclusions"].values()
    )
    assert set(registry["candidate_dispositions"]) == {
        f"M0487-C0{i}-{suffix}" for i, suffix in (
            (1, "LOCAL-STATEMENT"), (2, "MATHLIB-SUPPORT"),
            (3, "FORMAL-CONJECTURES-EXACT-PLACEHOLDER"),
            (4, "PRIME-NUMBER-THEOREM-AND-FINITE"),
            (5, "GOLDBACH-TM-BINARY"), (6, "FOOLISHAIR-EXACT-SCAFFOLD"),
            (7, "OPENCODE-MIRROR"),
        )
    }
    assert all("no_proof_edge" in value or "no_proof_credit" in value
               for value in registry["candidate_dispositions"].values())

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert set(node) == NODE_FIELDS
        assert node["kind"] in ALLOWED_NODE_KINDS
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert node["evidence_ids"] == [] and 0 < node["step_budget"] <= 100
        assert set(node["semantic_step_ledger"]) == {
            "premises", "inference", "output", "outgoing_use"
        }
        assert isinstance(node["semantic_step_ledger"]["premises"], list)
        assert isinstance(node["semantic_step_ledger"]["outgoing_use"], list)
        assert "exact context" not in node["semantic_step_ledger"]["inference"]
        assert node["owned_sources"]
        assert node["public_readable_target"].startswith(
            f"Stage1_Instances/{THEOREM}/obligation-tree.md#"
        )
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]
        if node["obligation_id"] in CHECKED:
            assert node["machine_debt"] == "M0-L"
        elif node["obligation_id"] == ROOT_ID:
            assert node["machine_debt"] == "M3"
        elif node["obligation_id"] == "M0487-X-REJECTED-CANDIDATES":
            assert node["machine_debt"] == "M5"
        else:
            assert node["machine_debt"] == "M4"

    assert bundle["root_node_id"] == f"{THEOREM}-ROOT"
    assert bundle["root_obligation_id"] == ROOT_ID
    assert bundle["edge_endpoint_namespace"] == "canonical obligation_id"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    obligations_by_id = {row["obligation_id"]: row for row in rows}
    edge_ids: set[str] = set()
    for graph_name, graph in bundle["graphs"].items():
        assert set(graph["out"]) == set(ids) == set(graph["in"])
        directional = []
        for row in graph["edges"]:
            assert row["edge_id"] not in edge_ids and row["type"] in ALLOWED_EDGES
            assert row["from"] in ids and row["to"] in ids
            check_edge_semantics(graph_name, row, obligations_by_id)
            assert row["edge_id"] in graph["out"][row["from"]]
            assert row["edge_id"] in graph["in"][row["to"]]
            edge_ids.add(row["edge_id"])
            if row["type"] != "composes":
                directional.append(row)
        check_acyclic(directional)

    for identifier in ids:
        if identifier != "M0487-X-EVIDENCE":
            assert bundle["graphs"]["evidence"]["in"][identifier]
        if identifier not in {"M0487-X-PROVENANCE", "M0487-X-EVIDENCE"}:
            assert bundle["graphs"]["provenance"]["in"][identifier]
        if identifier != "M0487-X-READABLE":
            assert bundle["graphs"]["documentation"]["in"][identifier]

    proof = {row["edge_id"]: row for row in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for row in proof.values():
        reverse = proof[row["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == row["edge_id"]
        assert (reverse["from"], reverse["to"]) == (row["to"], row["from"])
        assert {row["type"], reverse["type"]} == {"proof_requires", "composes"}
        if row["type"] == "proof_requires":
            children.setdefault(row["from"], []).append(row["to"])
    reachable: set[str] = set()

    def reach(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            reach(child)

    reach(ROOT_ID)
    assert sorted(reachable) == bundle["closure_boundary"]["proof_reachable_obligations"]
    assert len(reachable) == 37
    proof_required = set(registry["frozen_denominators"]["required_machine"])
    assert proof_required - reachable == {
        "M0487-S-INTERFACE", "M0487-S-DOMAIN", "M0487-S-BOUNDARY",
        "M0487-S-TRANSPORT", "M0487-S-FOUNDATION",
    }
    assert "M0487-X-REJECTED-CANDIDATES" not in reachable

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {
        recipe["recipe_id"] for recipe in recipes
    }
    recipe_fields = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    }
    for recipe in recipes:
        assert set(recipe) == recipe_fields
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["argv"] == [
            "python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"
        ]
        assert len(recipe["covered_obligation_ids"]) == 1
        identifier = recipe["covered_obligation_ids"][0]
        if identifier in CHECKED:
            assert recipe["covered_declarations"]
            assert "provisional M0-L interface only" in recipe["expected_outputs"][1]["semantic_hash_policy"]
        else:
            assert recipe["covered_declarations"] == []
            assert "no M/H/R closure credit" in recipe["expected_outputs"][1]["semantic_hash_policy"]

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["accepted_receipt_ids"] == []
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert boundary["minimal_open_proof_cut_sets"] == [[
        "M0487-T-ANALYTIC", "M0487-T-FINITE-UPPER"
    ]]
    assert set(boundary["open_release_gates"]) == {
        "M0487-X-SOURCE-MAIN", "M0487-X-SOURCE-MAJOR", "M0487-X-SOURCE-MINOR",
        "M0487-X-SOURCE-PRIME-BOUNDS", "M0487-X-SOURCE-FINITE",
        "M0487-S-FOUNDATION", "M0487-X-COMPUTATION", "M0487-X-EVIDENCE",
        "M0487-X-PROVENANCE", "M0487-X-TRUST", "M0487-X-READABLE",
        "M0487-X-WORKFLOW",
    }

    lean = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", lean, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b"
    )
    assert forbidden.search(without_comments) is None
    for marker in (
        "def analyticCutoff : Nat := 10 ^ 27",
        "def publishedFiniteUpper : Nat := 8875694145621773516800000000000",
        "theorem analyticCutoff_le_publishedFiniteUpper",
        "theorem finiteCoverage_of_publishedUpper",
        "theorem finiteRange_of_publishedFiniteUpper",
        "theorem root_of_analytic_and_finite",
        "theorem root_iff_analytic_and_finite",
        "#print axioms root_of_analytic_and_finite",
        "Stage1Instances.THM_M_0487.WeakGoldbachTarget",
    ):
        assert marker in lean

    lean_output = run_lean_composition()
    assert "sorryAx" not in lean_output
    assert lean_output.count("depends on axioms: [propext]") == 7
    for declaration in (
        "threePrimeRepresentation_iff",
        "cutoff_cases",
        "analyticCutoff_le_publishedFiniteUpper",
        "finiteCoverage_of_publishedUpper",
        "finiteRange_of_publishedFiniteUpper",
        "root_of_analytic_and_finite",
        "root_iff_analytic_and_finite",
        "def Stage1Instances.THM_M_0487.WeakGoldbachTarget",
    ):
        assert declaration in lean_output

    expected_declarations = {
        "M0487-S-INTERFACE": ["Stage1Instances.THM_M_0487.WeakGoldbachTarget"],
        "M0487-S-DOMAIN": ["weakGoldbachTarget_iff_integerWeakGoldbachTarget"],
        "M0487-S-BOUNDARY": [
            "five_excluded", "five_not_three_prime_sum",
            "mutationIncludedFiveBoundary_is_false",
            "mutationChangedDomainToFinEight_is_true", "seven_included",
            "seven_repeated_prime_representation", "eight_not_odd",
        ],
        "M0487-S-TRANSPORT": ["weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget"],
        "M0487-N-REPRESENTATION": ["threePrimeRepresentation_iff"],
        "M0487-N-CUTOFF": [
            "analyticCutoff", "publishedFiniteUpper", "five_lt_analyticCutoff",
            "analyticCutoff_le_publishedFiniteUpper",
        ],
        "M0487-B-RANGE-SPLIT": ["cutoff_cases"],
        "M0487-N-FINITE-COVERAGE": ["finiteCoverage_of_publishedUpper"],
        "M0487-T-FINITE": ["finiteRange_of_publishedFiniteUpper"],
        "M0487-T-ASSEMBLE": ["root_of_analytic_and_finite"],
    }
    assert set(expected_declarations) == CHECKED
    declarations_by_recipe = {
        recipe["covered_obligation_ids"][0]: recipe["covered_declarations"]
        for recipe in recipes
    }
    for identifier, declarations in expected_declarations.items():
        recorded = declarations_by_recipe[identifier]
        assert len(recorded) == len(declarations)
        assert all(any(marker in declaration for declaration in recorded) for marker in declarations)

    receipt_path = HERE / "obligation-tree-receipt.json"
    if receipt_path.exists():
        receipt = load(receipt_path)
        assert receipt["schema_version"] == "stage1-worker-obligation-tree-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["canonical_obligation_ids"] == ids
        assert receipt["lean_output_sha256"] == hashlib.sha256(lean_output.encode()).hexdigest()
        assert receipt["minimal_open_proof_cut_sets"] == boundary["minimal_open_proof_cut_sets"]
        assert receipt["open_release_gates"] == boundary["open_release_gates"]
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
        assert receipt["accepted_closed_obligations"] == []
        assert receipt["root_vector_after"] == instance["root_vector"]
        assert receipt["audit_complete"] is receipt["theorem_complete"] is False
        assert receipt["known_failures"] and receipt["validation"]["commands"]

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        selftest = load(selftest_path)
        assert set(selftest) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
        assert selftest["base_revision"] == BASE_REVISION
        assert set(selftest["changed_paths"]) == CHANGED_PATHS
        assert selftest["known_failures"] == load(receipt_path)["known_failures"]
        assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files
    assert NEW_FILES <= actual_files
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM}/")
        assert (ROOT / relative).is_file()
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("*.ilean"))
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "obligation-tree.md", "obligation-tree-validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    if selftest_path.exists():
        assert actual_changes == CHANGED_PATHS

    print(f"PASS THM-M-0487 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R3); analytic and finite-upper substantive packages remain M4")


if __name__ == "__main__":
    main()
