#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0028 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0028-OBLIGATION_TREE"
THEOREM = "THM-M-0028"
ROOT_ID = "M0028-ROOT"
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
REGISTRY_FIELDS = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
    "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
    "terminal_proof_body_id",
}
NODE_FIELDS = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
    "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
    "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
    "task_ids", "owned_sources", "owner", "reviewer", "validity",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def check_acyclic(edges: list[dict]) -> None:
    adjacency: dict[str, list[str]] = {}
    for item in edges:
        adjacency.setdefault(item["from"], []).append(item["to"])
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
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    instance = load("instance.json")
    local_dag = load("task-dag.json")
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())

    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"),
        build_obligation_artifacts.build(),
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1073, "phase": "obligation_tree",
        "layer": 3, "state": "[ ]", "depends_on": ["S56-M-0028-ANCHOR_AUDIT"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    local_item = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_item["state"] == "open" and local_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == len(build_obligation_artifacts.SPECS) == 25
    assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == ROOT_ID
    assert all(REGISTRY_FIELDS <= row.keys() for row in rows)
    for row in rows:
        assert row["kind"] in {"root", "definition", "reduction", "branch", "construction", "lemma", "computation", "transport", "terminal"}
        excluded = any(row[field] != "required" for field in ("machine_eligibility", "human_source_eligibility", "readable_eligibility"))
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert "pending" in row["exclusion_reason"]
    projection_fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
        "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
        "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in projection_fields} for row in rows]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for field, key in (
        ("machine_eligibility", "required_machine"),
        ("human_source_eligibility", "required_human_source"),
        ("readable_eligibility", "required_readable"),
    ):
        assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == "required"]
    assert all(value["status"].endswith("pending_independent_approval") for value in registry["layer_exclusions"].values())
    assert registry["proof_body_aliases"] == {
        "Stage1Instances.THM_M_0028_AnchorAudit.exactTarget_mathlib_candidate": ["M0028-X-FG-BODY", "M0028-X-CHAIN-BODY"],
        "facebookresearch/atlas-lean:noetherian_fg_iff_acc": ["M0028-X-FG-BODY", "M0028-X-CHAIN-BODY"],
        "NoetherianModules.noetherian_ring_iff_acc": ["M0028-X-CHAIN-BODY"],
    }

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert NODE_FIELDS <= node.keys()
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
        assert node["human_statement"] and node["formal_target"] and node["output"]
        assert node["public_readable_target"].startswith(f"Stage1_Instances/{THEOREM}/obligation-tree.md#")
        anchor = node["public_readable_target"].split("#", 1)[1]
        assert f'<a id="{anchor}"></a>' in (HERE / "obligation-tree.md").read_text()
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]

    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    for graph_data in bundle["graphs"].values():
        assert set(graph_data["out"]) == set(ids) == set(graph_data["in"])
        directional = []
        for item in graph_data["edges"]:
            assert item["edge_id"] not in edge_ids and item["type"] in ALLOWED_EDGES
            assert item["from"] in ids and item["to"] in ids
            assert item["edge_id"] in graph_data["out"][item["from"]]
            assert item["edge_id"] in graph_data["in"][item["to"]]
            edge_ids.add(item["edge_id"])
            if item["type"] != "composes":
                directional.append(item)
        check_acyclic(directional)

    proof = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
    proof_children: dict[str, list[str]] = {}
    for item in proof.values():
        reverse = proof[item["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == item["edge_id"]
        assert (reverse["from"], reverse["to"]) == (item["to"], item["from"])
        assert {item["type"], reverse["type"]} == {"proof_requires", "composes"}
        if item["type"] == "proof_requires":
            proof_children.setdefault(item["from"], []).append(item["to"])
    refinement_children: dict[str, list[str]] = {}
    for item in bundle["graphs"]["refinement"]["edges"]:
        assert item["type"] == "logical_decomposition"
        refinement_children.setdefault(item["from"], []).append(item["to"])
    reachable: set[str] = set()

    def reach(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in proof_children.get(node, []) + refinement_children.get(node, []):
            reach(child)

    reach(ROOT_ID)
    architecture = {ROOT_ID}
    architecture.update(proof_children)
    architecture.update(child for children in proof_children.values() for child in children)
    architecture.update(refinement_children)
    architecture.update(child for children in refinement_children.values() for child in children)
    assert reachable == architecture

    certificates = bundle["composition_certificates"]
    assert {(item["certificate_id"], item["declaration"], item["parent_obligation_id"]) for item in certificates} == {
        ("M0028-COMP-BRIDGE-PACKAGE-v1", "Stage1Instances.THM_M_0028.ObligationTree.bridgePackage_of_bridges", "M0028-T-ROOT-COMPOSE"),
        ("M0028-COMP-ROOT-PACKAGE-v1", "Stage1Instances.THM_M_0028.ObligationTree.root_of_bridgePackage", ROOT_ID),
    }
    for certificate in certificates:
        assert sorted(proof_children[certificate["parent_obligation_id"]]) == sorted(certificate["required_child_obligation_ids"])
        assert certificate["closure_credit"] is False

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
    for recipe in recipes:
        assert recipe["cwd"] == "." and isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {} and recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0 and recipe["closure_credit"] is False
        assert len(recipe["covered_obligation_ids"]) == 1

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["accepted_receipt_ids"] == []
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    prohibited_source = re.compile(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b")
    assert prohibited_source.search(source) is None
    for marker in (
        "(finiteGeneration : FiniteGenerationToNoetherian", "(chainStabilization : NoetherianToChainStabilization",
        "bridgePackage_of_bridges", "root_of_bridgePackage", "root_of_bridges",
        "#print axioms bridgePackage_of_bridges", "#print axioms root_of_bridgePackage",
    ):
        assert marker in source
    theorem_body = source[source.index("theorem bridgePackage_of_bridges"):source.index("#check isNoetherianRing_iff_ideal_fg")]
    assert "isNoetherianRing_iff_ideal_fg" not in theorem_body
    assert "monotone_stabilizes_iff_noetherian" not in theorem_body

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    source_pins = {
        "Mathlib/RingTheory/Noetherian/Defs.lean": ("a0e5c5a1aceb564f885573d5c51ec124be20abbd19fabc6af8c798b637530f0b", "66ddf1f73601e7dbeb04e37b95fcc61e34ee3c14", ["theorem isNoetherian_iff'", "theorem monotone_stabilizes_iff_noetherian", "theorem isNoetherianRing_iff_ideal_fg"]),
        "Mathlib/RingTheory/Finiteness/Basic.lean": ("500fc5473a4f78d7aa6a080adcf9b996c5860e8ed31da0461b8d0ec4b9c1b0b0", "5e83d4d993577f239286960f38eba10b4628d56e", ["theorem fg_iff_compact"]),
        "Mathlib/Order/CompactlyGenerated/Basic.lean": ("c63bfa13f84d3f138a4dd1deb83ecd8345bc60e55d76e357540e4b8b16a21a4d", "fd66d4dbebe5b64b7118a0a76dce9575cdec9507", ["theorem wellFoundedGT_characterisations"]),
        "Mathlib/Order/OrderIsoNat.lean": ("740b10ed011996c3caef968135fc98fddea63c81f3173a9acf052eeaa386b676", "531f93b96fe0fe5ef91fc07a8bff0a5cfbfe163f", ["theorem wellFoundedGT_iff_monotone_chain_condition'", "theorem wellFoundedGT_iff_monotone_chain_condition"]),
    }
    for relative, (digest, blob, markers) in source_pins.items():
        path = mathlib / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        assert subprocess.check_output(["git", "rev-parse", f"HEAD:{relative}"], cwd=mathlib, text=True).strip() == blob
        text = path.read_text(encoding="utf-8")
        assert all(marker in text for marker in markers)
    defs = (mathlib / "Mathlib/RingTheory/Noetherian/Defs.lean").read_text()
    assert "rw [isNoetherian_iff', wellFoundedGT_iff_monotone_chain_condition]" in defs
    assert "isNoetherianRing_iff.trans isNoetherian_def" in defs
    terminal_slices = [
        defs[defs.index("theorem monotone_stabilizes_iff_noetherian"):defs.index("variable [IsNoetherian R M]")],
        defs[defs.index("theorem isNoetherianRing_iff_ideal_fg"):defs.index("lemma Ideal.fg_of_isNoetherianRing")],
    ]
    prohibited_body = re.compile(r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b")
    assert all(prohibited_body.search(body) is None for body in terminal_slices)
    order = (mathlib / "Mathlib/Order/OrderIsoNat.lean").read_text()
    assert "rw [lt_iff_le_and_ne]" in order and "simp [a.mono h]" in order

    receipt = load("obligation-tree-receipt.json")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert set(receipt["graph_names"]) == GRAPH_NAMES
    assert receipt["canonical_obligation_ids"] == ids
    assert denominator in receipt["statement_fingerprints"]
    assert receipt["canonical_statement_fingerprint"] == "sha256:89e7e911ed4a5b75c153d824133091ad74ba20a0ecab19bd609b23a54badbee4"
    assert receipt["base_tree"] == "af0da30f285b30a34f3ead4689f614670d8bef98"
    assert set(receipt["composition_certificates"]) == {item["certificate_id"] for item in certificates}
    assert receipt["remaining_root_cut_set"] == boundary["remaining_root_cut_set"]
    assert set(receipt["provisionally_checked_interfaces"]) <= set(ids)
    assert set(receipt["candidate_only_obligations"]) <= set(ids)
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["support_state"] == "worker_self_tested_pending_master_acceptance"
    assert receipt["validation"]["commands"] and receipt["validation"]["output_summary"].startswith("All node-scoped")
    assert "PENDING_SELFTEST" not in (HERE / "obligation-tree-receipt.json").read_text()

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.is_file():
        selftest = json.loads(selftest_path.read_text())
        assert set(selftest) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
        assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
        assert selftest["base_revision"] == receipt["base_revision"]
        status = subprocess.check_output(["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True)
        actual = {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}
        assert actual == set(selftest["changed_paths"])

    required = {
        "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
        "obligation-registry.json", "typed-graphs.json", "validation-specs.json",
        "obligation-tree.md", "obligation-tree-validation.md", "obligation-tree-receipt.json",
    }
    assert required <= set(instance["owned_artifacts"])
    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "obligation-tree.md", "obligation-tree-validation.md"):
        text = (HERE / name).read_text()
        assert "/home/" not in text and ".cron/" not in text and "theorem_complete=true" not in text

    print(f"PASS THM-M-0028 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R3); both exact pinned bridges remain proof-phase cuts")


if __name__ == "__main__":
    main()
