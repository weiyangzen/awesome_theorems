#!/usr/bin/env python3
"""Fail-closed structural and conditional-composition checks for THM-M-0030."""

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
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0030-OBLIGATION_TREE"
THEOREM = "THM-M-0030"
ROOT_ID = "M0030-ROOT"
BASE_REVISION = "a16584a808446057f9ca2f2f26e76230cf45b84f"
BASE_TREE = "af0da30f285b30a34f3ead4689f614670d8bef98"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


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


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def run_lean_composition() -> str:
    lean = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="stage1-thm-m-0030-") as temporary:
        temp = Path(temporary)
        statement = subprocess.run(
            [lean, "-o", str(temp / "Statement.olean"), str(HERE / "Statement.lean")],
            cwd=HERE,
            env={**os.environ, "LEAN_PATH": lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        assert statement.returncode == 0, statement.stdout
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


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    instance = load("instance.json")
    task_dag = load("task-dag.json")
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())

    expected = build_obligation_artifacts.build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1075
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] == "[ ]", "worker must not modify authoritative DAG state"
    assert item["depends_on"] == ["S56-M-0030-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == hashlib.sha256(
        (HERE / "Statement.lean").read_bytes()
    ).hexdigest()
    assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256(
        (HERE / "anchor-audit.json").read_bytes()
    ).hexdigest()
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 28
    assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    assert {row["kind"] for row in rows} <= {
        "root", "definition", "reduction", "branch", "construction", "lemma",
        "computation", "transport", "terminal",
    }
    for row in rows:
        excluded = row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required"
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]
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
    expected_hash_fields = {
        "schema_version", "item_id", "theorem_id", "registry_id", "registry_version",
        "frozen_at", "freeze_basis", "frozen_against_statement_sha256",
        "frozen_against_anchor_audit_sha256", "root_obligation_id", "denominator_sha256",
        "frozen_denominators", "layer_exclusions", "proof_body_aliases",
        "supporting_same_path_declarations", "delta_policy", "append_only_delta", "obligations",
        "status_boundary",
    }
    assert set(registry["registry_hash_fields"]) == expected_hash_fields
    registry_content = {field: registry[field] for field in registry["registry_hash_fields"]}
    registry_hash = hashlib.sha256(
        json.dumps(registry_content, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert registry_hash == registry["registry_content_sha256"]
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
        value["status"].endswith("pending_independent_approval")
        for value in registry["layer_exclusions"].values()
    )
    assert registry["proof_body_aliases"][
        "Stage1Instances.THM_M_0030_AnchorAudit.exactTarget_mathlib_candidate"
    ] == "deduplicated_to:Ideal.iInf_pow_eq_bot_of_isLocalRing"
    required_body_ids = {
        row["obligation_id"]: row["terminal_proof_body_id"]
        for row in rows if row["terminal_proof_body_id"] is not None
    }
    for required in (
        "M0030-X-MATHLIB-BODY", "M0030-N-FINITE-MODULE", "M0030-N-JACOBSON",
        "M0030-L-PROPER-MAXIMAL", "M0030-L-MAXIMAL-JACOBSON",
        "M0030-X-JACOBSON-UNIT-SOURCE", "M0030-N-FIXEDPOINT-IFF",
        "M0030-C-STABLE-INTERSECTION", "M0030-L-FG-NAKAYAMA",
    ):
        assert required in required_body_ids

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["kind"] in {
            "root", "definition", "normalization", "reduction", "branch", "construction",
            "bridge", "core_lemma", "computation", "certificate", "transport", "terminal",
        }
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
        steps = node["semantic_step_ledger"]["steps"]
        assert 0 < len(steps) <= node["step_budget"]
        for step in steps:
            assert {"step_id", "premise_ids", "inference_or_source", "output_claim", "outgoing_use_ids"} <= step.keys()
            assert step["premise_ids"] and step["inference_or_source"] and step["output_claim"] and step["outgoing_use_ids"]
        assert node["public_readable_target"].startswith(f"Stage1_Instances/{THEOREM}/obligation-tree.md#")
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]
        assert node["evidence_ids"] == []

    architecture_children = {
        parent: list(values) for parent, values in build_obligation_artifacts.REQUIRES.items()
    }
    for parent, values in build_obligation_artifacts.BODY_DECOMPOSITION.items():
        architecture_children.setdefault(parent, []).extend(values)
    parent_map: dict[str, list[str]] = {}
    for parent, values in architecture_children.items():
        for child in values:
            parent_map.setdefault(child, []).append(parent)
    descendants: dict[str, set[str]] = {}

    def collect_descendants(identifier: str) -> set[str]:
        if identifier in descendants:
            return descendants[identifier]
        result: set[str] = set()
        for child in architecture_children.get(identifier, []):
            result.add(child)
            result.update(collect_descendants(child))
        descendants[identifier] = result
        return result

    for identifier in ids:
        collect_descendants(identifier)
    for node in nodes:
        identifier = node["obligation_id"]
        allowed_obligation_premises = descendants[identifier] | {identifier, "M0030-S-INTERFACE"}
        if identifier.startswith("M0030-S-") or identifier in {
            "M0030-X-SOURCE", "M0030-X-PROVENANCE", "M0030-X-TRUST",
            "M0030-X-READABLE", "M0030-X-WORKFLOW",
        }:
            allowed_obligation_premises.add("M0030-ROOT")
        steps = node["semantic_step_ledger"]["steps"]
        step_ids = [step["step_id"] for step in steps]
        assert len(step_ids) == len(set(step_ids))
        local_context_ids = {
            "M0030-X-JACOBSON-UNIT-SOURCE": {
                "M0030-X-JACOBSON-UNIT-SOURCE-COMM-RING-CONTEXT",
                "M0030-X-JACOBSON-UNIT-SOURCE-JACOBSON-MEMBERSHIP",
            },
            "M0030-L-POWER-INDUCTION": {
                "M0030-L-POWER-INDUCTION-FIXED-POINT-CONTEXT",
                "M0030-L-POWER-INDUCTION-INDUCTION-HYPOTHESIS",
            },
        }.get(identifier, set())
        referenced_obligation_premises: set[str] = set()
        ledger_edges: list[dict] = []
        for index, step in enumerate(steps):
            referenced = {premise for premise in step["premise_ids"] if premise in set(ids)}
            referenced_obligation_premises.update(referenced)
            assert referenced <= allowed_obligation_premises, (
                f"ledger premise points to an ancestor/unrelated obligation: {identifier} -> {referenced}"
            )
            prior_steps = set(step_ids[:index])
            later_steps = set(step_ids[index + 1:])
            for premise in step["premise_ids"]:
                assert premise in set(ids) | prior_steps | local_context_ids, (
                    f"unregistered or forward ledger premise: {step['step_id']} <- {premise}"
                )
                if premise in prior_steps:
                    ledger_edges.append({"from": premise, "to": step["step_id"]})
            allowed_outputs = (
                set(parent_map.get(identifier, []))
                | later_steps
                | {f"{identifier}-PUBLIC-BOUNDARY"}
            )
            for outgoing in step["outgoing_use_ids"]:
                assert outgoing in allowed_outputs, (
                    f"unregistered, backward, or unrelated ledger use: {step['step_id']} -> {outgoing}"
                )
                if outgoing in later_steps:
                    ledger_edges.append({"from": step["step_id"], "to": outgoing})
        assert set(architecture_children.get(identifier, [])) <= referenced_obligation_premises, (
            f"declared architecture child omitted from ledger premises: {identifier}"
        )
        check_acyclic(ledger_edges)

    assert bundle["edge_endpoint_namespace"] == "canonical obligation_id"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    incident: set[str] = set()
    for graph in bundle["graphs"].values():
        assert set(graph["out"]) == set(ids) == set(graph["in"])
        directional = []
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids and edge["type"] in ALLOWED_EDGES
            assert edge["from"] in ids and edge["to"] in ids
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            edge_ids.add(edge["edge_id"])
            incident.update((edge["from"], edge["to"]))
            if edge["type"] != "composes":
                directional.append(edge)
        check_acyclic([edge for edge in directional if edge["type"] != "equivalent_to"])
    assert incident == set(ids)

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for edge in proof.values():
        reciprocal = proof[edge["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == edge["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
        assert {edge["type"], reciprocal["type"]} == {"proof_requires", "composes"}
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    assert children == {key: list(value) for key, value in build_obligation_artifacts.REQUIRES.items()}
    check_acyclic([edge for edge in proof.values() if edge["type"] == "proof_requires"])

    refinement_pairs = {
        (edge["from"], edge["to"])
        for edge in bundle["graphs"]["refinement"]["edges"]
        if edge["type"] == "logical_decomposition"
    }
    expected_body_pairs = {
        (parent, child)
        for parent, values in build_obligation_artifacts.BODY_DECOMPOSITION.items()
        for child in values
    }
    assert expected_body_pairs <= refinement_pairs
    provenance_targets = {
        edge["to"] for edge in bundle["graphs"]["provenance"]["edges"]
        if edge["type"] == "provenance_of"
    }
    assert set(required_body_ids) <= provenance_targets
    trust_sources = {
        edge["from"] for edge in bundle["graphs"]["trust"]["edges"]
        if edge["type"] == "trusts" and edge["to"] == "M0030-X-TRUST"
    }
    assert set(required_body_ids) <= trust_sources
    architecture_children = {parent: list(values) for parent, values in children.items()}
    for parent, child in refinement_pairs:
        architecture_children.setdefault(parent, []).append(child)
    reachable: set[str] = set()

    def reach(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in architecture_children.get(node, []):
            reach(child)

    reach(ROOT_ID)
    semantic_ids = {
        row["obligation_id"] for row in rows
        if row["machine_eligibility"] == "required" and not row["obligation_id"].startswith("M0030-S-")
    }
    assert semantic_ids - {"M0030-S-FOUNDATION"} <= reachable

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert len(recipe["covered_obligation_ids"]) == 1
        assert recipe["coverage_semantics"] == "architecture_validation_only"
        assert recipe["closure_credit"] is False

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["obligation_registry_hash"] == f"sha256:{registry_hash}"
    assert instance["accepted_receipt_ids"] == []
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    forbidden = re.compile(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b")
    assert forbidden.search(without_comments(source)) is None
    for marker in (
        "(anchor : ExactMathlibAnchor", "(finiteModule : FiniteModuleIntersectionTarget",
        "(jacobson : JacobsonIntersectionTarget", "(fixedPoint : FixedPointCharacterizationTarget",
        "(jacobsonUnit : JacobsonUnitTarget", "(source : JacobsonUnitSourceTarget",
        "localProperIdealJacobson_of_bounds",
    ):
        assert marker in source

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    filtration = MATHLIB / "Mathlib/RingTheory/Filtration.lean"
    assert hashlib.sha256(filtration.read_bytes()).hexdigest() == "b161e2c4ce77f1224648467573dd4ba4c0ebc1ed734118e70df4cb39b33b1a72"
    assert output("git", "rev-parse", "HEAD:Mathlib/RingTheory/Filtration.lean", cwd=MATHLIB) == "c4fc3737f1859f1e22d387b199b46fe32d5f5093"
    pinned = filtration.read_text(encoding="utf-8")
    for marker in (
        "theorem Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "Submodule.exists_mem_and_smul_eq_self_of_fg_of_le_smul",
        "theorem Ideal.iInf_pow_smul_eq_bot_of_le_jacobson",
        "theorem Ideal.iInf_pow_smul_eq_bot_of_isLocalRing",
        "theorem Ideal.iInf_pow_eq_bot_of_isLocalRing",
        "convert I.iInf_pow_smul_eq_bot_of_isLocalRing (M := R) h",
    ):
        assert marker in pinned
    body = "\n".join(pinned.splitlines()[391:435])
    assert forbidden.search(without_comments(body)) is None
    supporting_files = {
        "Mathlib/RingTheory/Jacobson/Ideal.lean": (
            "3d8cf7766394242fb36c5998b52b6c6600f96451",
            "theorem isUnit_of_sub_one_mem_jacobson_bot",
        ),
        "Mathlib/RingTheory/Finiteness/Nakayama.lean": (
            "2ec71ea73c3b8e45cb27c597ae51fb94d5d82b07",
            "theorem exists_mem_and_smul_eq_self_of_fg_of_le_smul",
        ),
        "Mathlib/RingTheory/LocalRing/MaximalIdeal/Basic.lean": (
            "9d336345775f1676fb0685c8a1fb8e4e2bdf27ff",
            "theorem le_maximalIdeal",
        ),
    }
    for relative, (blob, marker) in supporting_files.items():
        assert output("git", "rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert marker in (MATHLIB / relative).read_text(encoding="utf-8")

    lean_output = run_lean_composition()
    assert lean_output.count("depends on axioms: [propext") == 7
    assert "sorryAx" not in lean_output
    for declaration in (
        "root_of_exactMathlibAnchor", "exactMathlibAnchor_of_finiteModuleIntersection",
        "finiteModuleIntersection_of_jacobson", "jacobsonIntersection_of_fixedPoint",
        "localProperIdealJacobson_of_bounds", "jacobsonUnit_of_source",
        "fixedPointCharacterization_of_branches",
    ):
        assert declaration in lean_output
    assert lean_output.count("propext") == 7
    assert lean_output.count("Classical.choice") == 5
    assert lean_output.count("Quot.sound") == 7

    receipt = load("obligation-tree-receipt.json")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["registry_content_sha256"] == registry_hash
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert set(receipt["graph_names"]) == GRAPH_NAMES
    assert set(receipt["conditional_composition_declarations"]) == {
        entry["declaration"] for entry in boundary["composition_certificates"]
    }
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["support_state"] == "worker_self_tested_pending_master_acceptance"

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.is_file():
        selftest = json.loads(selftest_path.read_text(encoding="utf-8"))
        assert set(selftest) == {
            "item_id", "changed_paths", "commands", "output_summary", "base_revision",
            "known_failures", "state",
        }
        assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
        assert selftest["base_revision"] == BASE_REVISION
        assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")
        status = subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
        )
        actual_changes = {
            line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == set(selftest["changed_paths"])

    required_artifacts = {
        "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
        "obligation-registry.json", "typed-graphs.json", "validation-specs.json",
        "obligation-tree.md", "obligation-tree-validation.md", "obligation-tree-receipt.json",
    }
    assert required_artifacts <= set(instance["owned_artifacts"])
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

    print(f"PASS THM-M-0030 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("conditional Lean composition: 7 declarations checked; no sorryAx; root remains H1/M3/R3")
    print("root closure: open; exact pinned mathlib anchor remains the proof-phase cut")


if __name__ == "__main__":
    main()
