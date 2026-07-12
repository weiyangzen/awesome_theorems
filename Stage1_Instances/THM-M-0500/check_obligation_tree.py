#!/usr/bin/env python3
"""Generate or fail-closed validate the THM-M-0500 obligation freeze."""

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0500-OBLIGATION_TREE"
THEOREM = "THM-M-0500"

ROWS = [
    ("M0500-ROOT", "root", "critical", "The exact infinitude target.", "Stage1Instances.THM_M_0500.DirichletPrimesInAPTarget", "The canonical proposition.", "M3"),
    ("M0500-S-SCOPE", "definition", "high", "Freeze the nonzero modulus, unit residue, natural-prime domain, and q = 1 boundary.", "Stage1Instances.THM_M_0500.DirichletPrimesInAPTarget", "The exact statement interface and boundary policy.", "M0-L"),
    ("M0500-S-FOUNDATION", "certificate", "critical", "Inventory classical logic, choice, quotient soundness, imports, TCB, and the no-oracle policy.", "planned exact foundation and transitive trust report", "An accepted foundation and TCB boundary.", "M4"),
    ("M0500-N-CHAR", "normalization", "critical", "Decompose the residue-class von Mangoldt function by Dirichlet-character orthogonality.", "ArithmeticFunction.vonMangoldt.residueClass_eq", "A finite character-sum formula for the residue-class arithmetic function.", "M3"),
    ("M0500-L-LSERIES", "bridge", "critical", "Lift the character decomposition to the L-series/logarithmic-derivative identity on re s > 1.", "ArithmeticFunction.vonMangoldt.LSeries_residueClass_eq", "The analytic L-series identity used to isolate the pole at one.", "M3"),
    ("M0500-L-NONVANISH", "bridge", "critical", "Provide analytic continuation and nonvanishing for Dirichlet L-functions on the closed half-plane.", "DirichletCharacter.LFunction_ne_zero_of_one_le_re and supporting continuation declarations", "The zero-free boundary needed for continuity after pole cancellation.", "M3"),
    ("M0500-C-AUX", "construction", "critical", "Construct the pole-cancelled auxiliary function and prove its continuity on re s >= 1.", "ArithmeticFunction.vonMangoldt.LFunctionResidueClassAux and continuousOn_LFunctionResidueClassAux", "A continuous remainder after subtracting the principal pole.", "M3"),
    ("M0500-L-LOWER", "core_lemma", "critical", "Derive the real-axis lower bound near one from the pole plus continuous remainder.", "ArithmeticFunction.vonMangoldt.LSeries_residueClass_lower_bound", "A lower bound forcing divergence as x tends to one from the right.", "M3"),
    ("M0500-L-NONPRIME", "core_lemma", "high", "Prove summability of the non-prime prime-power contribution by explicit majorants.", "ArithmeticFunction.vonMangoldt.summable_residueClass_non_primes_div", "Summability of the non-prime weighted residue-class terms.", "M3"),
    ("M0500-T-NONSUM", "terminal", "critical", "Contradict summability of the prime contribution using the lower bound and non-prime summability.", "ArithmeticFunction.vonMangoldt.not_summable_residueClass_prime_div", "Non-summability of the weighted prime-residue series.", "M3"),
    ("M0500-L-SUPPORT", "lemma", "high", "Identify the weighted prime-series support with the exact target set.", "ArithmeticFunction.vonMangoldt.support_residueClass_prime_div", "Equality of the weighted support and target prime set.", "M3"),
    ("M0500-T-ASSEMBLE", "transport", "high", "Convert target finiteness to finite support and summability, contradicting the analytic terminal result.", "Stage1Instances.THM_M_0500.ObligationTree.root_of_terminal_packages", "The exact canonical proposition, conditional on both terminal packages.", "M0-L"),
    ("M0500-X-SOURCE", "terminal", "high", "Map every mathematical node to a primary source theorem/page/assumption/errata record.", "non-machine human-source boundary", "An accepted node-specific human-source crosswalk.", "M4"),
    ("M0500-X-PROVENANCE", "certificate", "critical", "Resolve terminal bodies, transitive declaration closure, imports, axioms, license, and replay provenance.", "planned exact provenance and evidence report", "An accepted proof-body and trust provenance boundary.", "M4"),
]

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
PROOF_REQUIRES = [
    ("M0500-ROOT", "M0500-T-ASSEMBLE"),
    ("M0500-T-ASSEMBLE", "M0500-T-NONSUM"),
    ("M0500-T-ASSEMBLE", "M0500-L-SUPPORT"),
    ("M0500-T-NONSUM", "M0500-L-LOWER"),
    ("M0500-T-NONSUM", "M0500-L-NONPRIME"),
    ("M0500-L-LOWER", "M0500-C-AUX"),
    ("M0500-C-AUX", "M0500-L-LSERIES"),
    ("M0500-C-AUX", "M0500-L-NONVANISH"),
    ("M0500-L-LSERIES", "M0500-N-CHAR"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def planned_fingerprint(identifier, statement):
    return "planned:v1:sha256:" + sha((identifier + "\0" + statement).encode())


def edge(edge_id, kind, source, target, reciprocal=None):
    result = {"edge_id": edge_id, "type": kind, "from": source, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


def graph(edges):
    ids = [row[0] for row in ROWS]
    incoming = {identifier: [] for identifier in ids}
    outgoing = {identifier: [] for identifier in ids}
    for item in edges:
        outgoing[item["from"]].append(item["edge_id"])
        incoming[item["to"]].append(item["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build():
    statement_hash = sha((HERE / "Statement.lean").read_bytes())
    audit_hash = sha((HERE / "anchor-audit.json").read_bytes())
    obligations = []
    for identifier, kind, risk, human, formal, output, machine in ROWS:
        human_source = "not_applicable" if identifier in {"M0500-S-SCOPE", "M0500-S-FOUNDATION", "M0500-X-PROVENANCE"} else "required"
        machine_eligibility = "not_applicable" if identifier == "M0500-X-SOURCE" else ("informational" if identifier == "M0500-X-PROVENANCE" else "required")
        terminal = "local:Stage1_Instances/THM-M-0500/ObligationTree.lean#root_of_terminal_packages" if identifier == "M0500-T-ASSEMBLE" else None
        fingerprint = "lean-expression-sha256:23806a3d33ac195c516a56f94afada5049a257e6af85d8e9be61032c983269bc" if identifier in {"M0500-ROOT", "M0500-S-SCOPE"} else planned_fingerprint(identifier, human)
        obligations.append({
            "obligation_id": identifier, "statement_fingerprint": fingerprint, "kind": kind,
            "root_relevant": True, "machine_eligibility": machine_eligibility,
            "human_source_eligibility": human_source, "readable_eligibility": "required",
            "risk_class": risk, "exclusion_reason": "human_source_boundary_only" if identifier == "M0500-X-SOURCE" else ("release_provenance_overlay_no_proof_credit" if identifier == "M0500-X-PROVENANCE" else None),
            "terminal_proof_body_id": terminal,
        })
    projection = [{key: row[key] for key in FIELDS} for row in obligations]
    denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode())
    ids = [row[0] for row in ROWS]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": "Exact elaborated statement, bounded anchor audit, and the declared source architecture of the pinned mathlib proof; eligibility assigned independently of observed closure.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": audit_hash,
        "root_obligation_id": "M0500-ROOT", "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": ["M0500-X-PROVENANCE"],
        },
        "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
        "obligations": obligations, "append_only_delta": [],
        "status_observed_after_freeze": {
            "candidate_available": "Nat.infinite_setOf_prime_and_eq_mod at pinned mathlib revision; integration and acceptance deferred to proof and validation phases",
            "closed_obligations": ["M0500-S-SCOPE", "M0500-T-ASSEMBLE"], "root_machine_debt": "M3"
        },
        "status_boundary": "Frozen scope and typed architecture only; no accepted proof state, H0/R0, audit completion, or theorem completion."
    }
    nodes = []
    for identifier, kind, risk, human, formal, output, machine in ROWS:
        nodes.append({
            "node_id": "THM-M-0500-" + identifier.removeprefix("M0500-"), "obligation_id": identifier,
            "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
            "human_debt": "H1", "machine_debt": machine, "readability_debt": "R4", "evidence_ids": [],
            "source_crosswalk_id": "not-applicable" if identifier in {"M0500-S-SCOPE", "M0500-S-FOUNDATION", "M0500-X-PROVENANCE"} else "primary-source-node-map-pending",
            "provenance_id": "pinned-mathlib-body-audit-pending" if identifier not in {"M0500-X-SOURCE", "M0500-S-SCOPE"} else "none",
            "foundation_profile": "lean4-mathlib-classical/propext-choice-quotient; transitive audit pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure pending",
            "computation_record": "none; no oracle, experiment, or unchecked certificate may close this node",
            "step_budget": 100 if risk == "critical" else 60,
            "semantic_step_ledger": {"premises": "Only declared proof_requires children and the frozen formal context.", "inference": human, "output": output, "outgoing_use": "Only declared typed parents or non-proof support edges may consume this output."},
            "public_readable_target": "Stage1_Instances/THM-M-0500/obligation-tree.md#" + identifier.lower(),
            "validation_spec_id": "VAL-" + identifier, "status_boundary": "Frozen architecture, audited anchor, or conditional interface only; proof-phase integration and acceptance are not supplied.",
            "task_ids": [ITEM, "S56-M-0500-PROOF"], "owned_sources": [formal] if not formal.startswith("planned") and not formal.startswith("non-machine") else [],
            "owner": "THM-M-0500 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if machine == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if machine == "M0-L" else "open"},
        })
    proof_edges = []
    for index, (parent, child) in enumerate(PROOF_REQUIRES, 1):
        req, comp = f"P{index:02d}-REQ", f"P{index:02d}-COMP"
        proof_edges.extend([edge(req, "proof_requires", parent, child, comp), edge(comp, "composes", child, parent, req)])
    refinement_edges = [edge("R01-SCOPE", "logical_decomposition", "M0500-ROOT", "M0500-S-SCOPE")]
    provenance_edges = [edge("PV01-SOURCE", "source_map", "M0500-X-SOURCE", "M0500-ROOT"), edge("PV02-BODY", "provenance_of", "M0500-X-PROVENANCE", "M0500-ROOT")]
    trust_edges = [edge("TR01-FOUNDATION", "trusts", "M0500-ROOT", "M0500-S-FOUNDATION")]
    documentation_edges = [edge("D01-ROOT", "documents", "M0500-X-SOURCE", "M0500-ROOT"), edge("D02-PROV", "documents", "M0500-X-PROVENANCE", "M0500-T-ASSEMBLE")]
    workflow_edges = [edge("W01-SOURCE-PROVENANCE", "workflow_depends_on", "M0500-X-PROVENANCE", "M0500-X-SOURCE"), edge("W02-ROOT-PROVENANCE", "workflow_depends_on", "M0500-ROOT", "M0500-X-PROVENANCE")]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": "THM-M-0500-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
        "root_node_id": "M0500-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
        "nodes": nodes,
        "graphs": {"proof": graph(proof_edges), "refinement": graph(refinement_edges), "provenance": graph(provenance_edges), "evidence": graph([]), "trust": graph(trust_edges), "documentation": graph(documentation_edges), "workflow": graph(workflow_edges)},
        "closure_boundary": {"minimal_open_root_cut": ["M0500-T-NONSUM", "M0500-L-SUPPORT"], "conditional_composition_checked": True, "root_closed": False, "audit_complete": False, "theorem_complete": False}
    }
    recipes = [{"recipe_id": "VAL-" + identifier, "obligation_id": identifier, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0500/check_obligation_tree.py"], "env": {}, "timeout_seconds": 60, "network_policy": "denied", "covered_ids": [identifier], "expected_exit": 0} for identifier in ids]
    specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}
    return registry, bundle, specs


def validate(registry, bundle, specs):
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert registry["frozen_against_statement_sha256"] == sha((HERE / "Statement.lean").read_bytes())
    assert registry["frozen_against_anchor_audit_sha256"] == sha((HERE / "anchor-audit.json").read_bytes())
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 14 and ids[0] == registry["root_obligation_id"]
    projection = [{key: row[key] for key in FIELDS} for row in rows]
    digest = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode())
    assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    assert registry["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]
    required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert required_node <= node.keys() and 0 < node["step_budget"] <= 100
        assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
    assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
    all_edges = set()
    for current in bundle["graphs"].values():
        for item in current["edges"]:
            assert item["edge_id"] not in all_edges and item["type"] in allowed
            assert item["from"] in ids and item["to"] in ids
            assert item["edge_id"] in current["out"][item["from"]] and item["edge_id"] in current["in"][item["to"]]
            all_edges.add(item["edge_id"])
    proof = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
    children = {}
    for item in proof.values():
        reverse = proof[item["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == item["edge_id"] and (reverse["from"], reverse["to"]) == (item["to"], item["from"])
        assert {item["type"], reverse["type"]} == {"proof_requires", "composes"}
        if item["type"] == "proof_requires":
            children.setdefault(item["from"], []).append(item["to"])
    visiting, visited = set(), set()
    def visit(node):
        assert node not in visiting
        if node in visited:
            return
        visiting.add(node)
        for child in children.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)
    visit("M0500-ROOT")
    expected = {"M0500-ROOT", "M0500-T-ASSEMBLE", "M0500-T-NONSUM", "M0500-L-SUPPORT", "M0500-L-LOWER", "M0500-L-NONPRIME", "M0500-C-AUX", "M0500-L-LSERIES", "M0500-L-NONVANISH", "M0500-N-CHAR"}
    assert visited == expected
    assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
    assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
    lean = (HERE / "ObligationTree.lean").read_text()
    assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
    assert "root_of_terminal_packages" in lean and "#print axioms" in lean
    return digest, len(all_edges)


if __name__ == "__main__":
    generated = build()
    if "--write" in sys.argv:
        for name, value in zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), generated):
            (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    actual = tuple(json.loads((HERE / name).read_text()) for name in ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"))
    assert actual == generated, "generated obligation artifacts are stale; run with --write"
    digest, edge_count = validate(*actual)
    print(f"PASS THM-M-0500 obligation tree: {len(ROWS)} obligations, {edge_count} typed edges")
    print(f"registry denominator sha256: {digest}")
    print("root closure: open (M3); proof integration, H0/R0, audit, validation, and release remain open")
