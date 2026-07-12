#!/usr/bin/env python3
"""Build the frozen THM-M-1070 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1070-OBLIGATION_TREE"
THEOREM = "THM-M-1070"
ROOT = "M1070-ROOT"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


SPECS = [
    (ROOT, "root", "critical", "Establish the exact frozen Levy-process predicate for the given process.", "Stage1Instances.THM_M_1070.IsLevyProcess P X", "The exact canonical proposition.", "H1", "M3"),
    ("M1070-S-DEFINITIONS", "definition", "high", "Fix nonnegative-real time, real state space, the measurable sample space, measure, and process binder order.", "Statement.lean definitions and ExpandedSourceShape", "The exact objects and quantifier scopes used below.", "not_applicable", "M0-L"),
    ("M1070-S-BOUNDARY", "normalization", "high", "Preserve zero and repeated endpoints, almost-everywhere initial value, joint rather than pairwise independence, and exclusion of cadlag regularity.", "Canonical statement boundary package", "No discrete-time, pairwise-only, pointwise-zero, continuous-path, or cadlag substitution.", "H1", "M4"),
    ("M1070-S-FOUNDATION", "certificate", "critical", "Freeze classical measure theory, quotient/extensionality, kernel, and no-oracle policies.", "Foundation and transitive trust certificate", "An audited trust boundary for eventual terminal bodies.", "not_applicable", "M4"),
    ("M1070-L-PROBABILITY", "terminal", "high", "Show that P is a probability measure.", "IsProbabilityMeasure P", "The probability-space clause.", "H1", "M4"),
    ("M1070-L-MEASURABLE", "terminal", "critical", "Show every time marginal X t is P-almost-everywhere measurable.", "forall t, AEMeasurable (X t) P", "Measurable random variables at every time.", "H1", "M4"),
    ("M1070-L-ZERO", "terminal", "high", "Show that the process starts at zero P-almost everywhere.", "X 0 =m[P] 0", "The exact initial-value clause.", "H1", "M4"),
    ("M1070-L-INDEPENDENT", "bridge", "critical", "Prove joint independence for every finite ordered family of consecutive increments.", "ProbabilityTheory.HasIndepIncrements X P", "The full joint independent-increment clause.", "H1", "M4"),
    ("M1070-L-STATIONARY", "bridge", "critical", "Prove every increment X(s+t)-X(s) has the same law as X(t).", "forall s t, IdentDistrib (X (s + t) - X s) (X t) P P", "Stationarity of all increment laws.", "H1", "M4"),
    ("M1070-L-STOCH-CONT", "bridge", "critical", "Prove convergence in P-measure of X along every neighborhood filter in time.", "forall t, TendstoInMeasure P X (nhds t) (X t)", "Stochastic continuity at every nonnegative time.", "H1", "M4"),
    ("M1070-T-COMPOSE", "transport", "critical", "Conjoin the six exact clauses and transport the package definitionally to IsLevyProcess.", "Stage1Instances.THM_M_1070.isLevyProcess_of_components", "The exact root conditional on every clause.", "H1", "M0-L"),
    ("M1070-X-SOURCE", "terminal", "high", "Pinpoint primary definitions and regularization results for every convention and material bridge.", "Reviewed node-specific human-source crosswalk", "Human-source evidence without machine-proof credit.", "H1", "not_applicable"),
    ("M1070-X-PROVENANCE", "certificate", "critical", "Resolve all terminal bodies, revisions, wrappers, licenses, axioms, and transitive trust dependencies.", "Transitive provenance and trust closure", "No component API or near-match is mistaken for a root proof body.", "not_applicable", "M4"),
]

REQUIRES = {
    ROOT: ["M1070-T-COMPOSE"],
    "M1070-T-COMPOSE": [
        "M1070-L-PROBABILITY", "M1070-L-MEASURABLE", "M1070-L-ZERO",
        "M1070-L-INDEPENDENT", "M1070-L-STATIONARY", "M1070-L-STOCH-CONT",
    ],
}
INFO = {"M1070-X-SOURCE", "M1070-X-PROVENANCE"}
SOURCE_NA = {"M1070-S-DEFINITIONS", "M1070-S-FOUNDATION", "M1070-X-PROVENANCE"}
CHECKED = {"M1070-S-DEFINITIONS", "M1070-T-COMPOSE"}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


def graph(edges):
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def main():
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations, nodes = [], []
    parents = set(REQUIRES)
    for oid, kind, risk, claim, target, output, human, machine_debt in SPECS:
        machine = "informational" if oid == "M1070-X-PROVENANCE" else ("not_applicable" if oid == "M1070-X-SOURCE" else "required")
        obligations.append({
            "obligation_id": oid,
            "statement_fingerprint": ("lean-expression-sha256:" + digest([statement_hash, target]) if oid in {ROOT, "M1070-S-DEFINITIONS", "M1070-T-COMPOSE"} else "planned:v1:sha256:" + digest([oid, claim, target, output])),
            "kind": kind, "root_relevant": oid not in INFO, "machine_eligibility": machine,
            "human_source_eligibility": "not_applicable" if oid in SOURCE_NA else "required",
            "readable_eligibility": "required", "risk_class": risk,
            "exclusion_reason": "human_source_overlay_no_machine_proof_credit" if oid == "M1070-X-SOURCE" else ("provenance_overlay_no_semantic_proof_credit" if oid == "M1070-X-PROVENANCE" else None),
            "terminal_proof_body_id": "local:ObligationTree.lean#isLevyProcess_of_components" if oid == "M1070-T-COMPOSE" else None,
        })
        if oid in parents:
            ledger = ["Consume every exact incoming proof_requires child.", f"Derive the declared output: {output}", "Use the registered reciprocal composition edge without any undeclared premise."]
        else:
            ledger = ["Freeze the exact formal context and named premises.", f"Establish: {claim}", f"Derive: {output}", "Pass only that output through the registered typed edge."]
        nodes.append({
            "node_id": oid, "obligation_id": oid, "kind": kind, "human_statement": claim,
            "formal_target": target, "output": output, "human_debt": human,
            "machine_debt": machine_debt, "readability_debt": "R4", "evidence_ids": [],
            "source_crosswalk_id": "not-applicable" if oid in SOURCE_NA else "node-pinpoint-review-pending",
            "provenance_id": "local-conditional-composition" if oid == "M1070-T-COMPOSE" else "none",
            "foundation_profile": "lean4-mathlib-classical-measure-theory/policy-audit-pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
            "computation_record": "none; no computation or oracle closes this node",
            "step_budget": len(ledger), "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/THM-M-1070/obligation-tree.md#{oid.lower()}",
            "validation_spec_id": f"VAL-{oid}",
            "status_boundary": "Frozen architecture or conditional interface only; no arbitrary process is proved to satisfy the clause and the root remains open.",
            "task_ids": [ITEM, "S56-M-1070-PROOF"],
            "owned_sources": ["Stage1_Instances/THM-M-1070/ObligationTree.lean"] if oid == "M1070-T-COMPOSE" else [],
            "owner": "THM-M-1070 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if oid in CHECKED else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain", "source map"], "revocation_state": "provisional" if oid in CHECKED else "open"},
        })

    ids = [item[0] for item in SPECS]
    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    denominator_hash = digest([{key: row[key] for key in fields} for row in obligations])
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": "Exact statement and bounded anchor audit; clause eligibility was assigned before inspecting proof closure.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": ROOT, "denominator_sha256": denominator_hash,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": ids, "informational_overlays": sorted(INFO),
        },
        "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new registry version with an append-only old/new ID delta.",
        "obligations": obligations, "append_only_delta": [],
        "status_observed_after_freeze": {"closed_obligations": sorted(CHECKED), "root_machine_debt": "M3"},
        "status_boundary": "The registry and a conditional conjunction transport are frozen; no existence, regularization, characterization, or theorem completion is claimed.",
    }

    proof = []
    for parent, children in REQUIRES.items():
        for child in children:
            req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
            proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]
    graphs = {
        "proof": graph(proof),
        "refinement": graph([edge("REF-ROOT-DEFS", ROOT, "logical_decomposition", "M1070-S-DEFINITIONS"), edge("REF-ROOT-BOUNDARY", ROOT, "logical_decomposition", "M1070-S-BOUNDARY")]),
        "provenance": graph([edge("PROV-BRIDGES", "M1070-X-PROVENANCE", "provenance_of", "M1070-L-INDEPENDENT"), edge("SRC-BRIDGES", "M1070-L-STATIONARY", "source_map", "M1070-X-SOURCE")]),
        "evidence": graph([]),
        "trust": graph([edge("TRUST-ROOT", ROOT, "trusts", "M1070-S-FOUNDATION"), edge("TRUST-PROV", ROOT, "trusts", "M1070-X-PROVENANCE")]),
        "documentation": graph([edge("DOC-ROOT", "M1070-S-DEFINITIONS", "documents", ROOT), edge("DOC-SOURCE", "M1070-X-SOURCE", "documents", "M1070-L-INDEPENDENT")]),
        "workflow": graph([edge("FLOW-COMPOSE-INDEP", "M1070-T-COMPOSE", "workflow_depends_on", "M1070-L-INDEPENDENT"), edge("FLOW-COMPOSE-STATIONARY", "M1070-T-COMPOSE", "workflow_depends_on", "M1070-L-STATIONARY"), edge("FLOW-COMPOSE-CONT", "M1070-T-COMPOSE", "workflow_depends_on", "M1070-L-STOCH-CONT"), edge("FLOW-PROV-COMPOSE", "M1070-X-PROVENANCE", "workflow_depends_on", "M1070-T-COMPOSE")]),
    }
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": "THM-M-1070-OBLIGATIONS-v1", "registry_denominator_sha256": denominator_hash,
        "statement_source_sha256": statement_hash, "root_node_id": ROOT,
        "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent",
        "nodes": nodes, "graphs": graphs,
        "closure_boundary": {"closed_obligations": sorted(CHECKED), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1070-L-INDEPENDENT", "M1070-L-STATIONARY", "M1070-L-STOCH-CONT"], "root_machine_debt": "M3", "composition_certificates": ["Stage1Instances.THM_M_1070.isLevyProcess_of_components"], "reason": "The composition is conditional and every substantive process clause remains an open premise."},
    }
    recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1070/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
    for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
        (HERE / filename).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

    children = {parent: values for parent, values in REQUIRES.items()}
    spec_by_id = {row[0]: row for row in SPECS}
    lines = ["# THM-M-1070 obligation tree", "", "This is the frozen architecture for the exact real-valued Levy-process predicate. Checked conjunction transport does not establish any open process clause.", "", "## Proof route", ""]
    def render(oid, depth=0):
        row = spec_by_id[oid]
        lines.extend([f"{'  ' * depth}- **{oid}** ({row[1]}): {row[3]}", f"{'  ' * depth}  Output: {row[5]}"])
        for child in children.get(oid, []):
            render(child, depth + 1)
    render(ROOT)
    lines += ["", "## Node ledgers", ""]
    for node in nodes:
        lines += [f"### {node['node_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:"]
        lines += [f"{i}. {step}" for i, step in enumerate(node["semantic_step_ledger"], 1)]
        lines += [""]
    lines += ["## Typed overlays", "", "`M1070-X-SOURCE` and `M1070-X-PROVENANCE` cover human-source and terminal-body boundaries. They cannot supply semantic proof credit.", "", "## Closure boundary", "", "The conditional conjunction transport is locally checked, but the six semantic clause premises remain open. The first critical cut is independent increments, stationary increment laws, and stochastic continuity. No arbitrary process is proved Levy, no cadlag regularization theorem is asserted, and audit/theorem completion remain false.", ""]
    (HERE / "obligation-tree.md").write_text("\n".join(lines))
    print(f"wrote {len(ids)} obligations; denominator sha256 {denominator_hash}")


if __name__ == "__main__":
    main()
