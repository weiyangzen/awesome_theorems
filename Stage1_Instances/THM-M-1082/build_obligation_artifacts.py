#!/usr/bin/env python3
"""Build the frozen THM-M-1082 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1082-OBLIGATION_TREE"
THEOREM = "THM-M-1082"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


ROWS = [
    ("M1082-ROOT", "root", "critical", "The exact finite-dimensional-law characterization of a Gaussian process.", "ProbabilityTheory.IsGaussianProcess X P <-> forall I : Finset T, ProbabilityTheory.HasGaussianLaw (fun omega => I.restrict (X . omega)) P", "The frozen canonical proposition."),
    ("M1082-S-CONTEXT", "definition", "high", "Freeze universes, measurable spaces, topology, additive monoid, real module, process, and measure in their exact binder order.", "Statement.lean binder context", "The exact context shared by both directions."),
    ("M1082-S-BOUNDARY", "normalization", "high", "Retain the empty Finset and allow degenerate, noncentered Gaussian laws; add no continuity, covariance, or independence premise.", "forall I : Finset T (including empty), HasGaussianLaw ...", "The statement boundary with no strengthened or weakened side condition."),
    ("M1082-S-FOUNDATION", "certificate", "critical", "Bind the proof to Lean 4.29.0, pinned mathlib, and the audited classical quotient/extensionality trust profile.", "foundation/trust certificate for the imported definition and local composition", "The trust boundary required by later validation."),
    ("M1082-X-DEFINITION", "bridge", "critical", "Audit the imported IsGaussianProcess structure as exactly one field with the frozen finite-dimensional type.", "ProbabilityTheory.IsGaussianProcess and .hasGaussianLaw", "A pinned exact-definition interface, not a theorem-name analogy."),
    ("M1082-T-FORWARD", "terminal", "high", "Project the finite-dimensional Gaussian-law family from an IsGaussianProcess witness.", "ObligationTree.forward_from_projection", "The forward implication at the exact context."),
    ("M1082-T-REVERSE", "terminal", "high", "Construct an IsGaussianProcess witness from the complete finite-dimensional Gaussian-law family.", "ObligationTree.reverse_from_constructor", "The reverse implication at the exact context."),
    ("M1082-T-COMPOSE", "terminal", "critical", "Consume both directional conclusions and form the exact iff without an undeclared premise.", "ObligationTree.root_of_directions", "The exact root conditional on both registered directions."),
    ("M1082-X-SOURCE", "terminal", "high", "Map the characterization and boundary conventions to pinpoint human sources.", "node-specific human-source crosswalk", "Human-source coverage only; no machine proof credit."),
    ("M1082-X-PROVENANCE", "certificate", "critical", "Record imported definition, local bodies, axioms, toolchain, and replay evidence.", "terminal proof-body and transitive provenance record", "Release provenance only; no mathematical proof credit."),
]

source_na = {"M1082-S-CONTEXT", "M1082-S-FOUNDATION", "M1082-X-PROVENANCE"}
informational = {"M1082-X-SOURCE", "M1082-X-PROVENANCE"}
checked = {"M1082-S-CONTEXT", "M1082-S-BOUNDARY", "M1082-X-DEFINITION", "M1082-T-FORWARD", "M1082-T-REVERSE", "M1082-T-COMPOSE"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in ROWS:
    machine = "informational" if oid in informational else "required"
    fp = ("lean-expression-sha256:26f4a571d703862aca5ccf41d7b75c6166d2fa67ca78a23db60d3f674d5ea592"
          if oid == "M1082-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    body = {
        "M1082-T-FORWARD": "local:ObligationTree.lean#forward_from_projection",
        "M1082-T-REVERSE": "local:ObligationTree.lean#reverse_from_constructor",
        "M1082-T-COMPOSE": "local:ObligationTree.lean#root_of_directions",
    }.get(oid)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "governance_overlay_no_proof_credit" if oid in informational else None,
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-1082-" + oid.removeprefix("M1082-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "not_applicable" if oid in source_na else "H2",
        "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1082-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-node-pinpoint" if oid == "M1082-X-DEFINITION" else ("not-applicable" if oid in source_na else "pending-node-pinpoint-review"),
        "provenance_id": "local-kernel-checked-interface" if oid in checked else "none",
        "foundation_profile": "lean4-dependent-type-theory/classical-choice-quotient-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386ffc0f5fef0b77738bb5449d50efeea95",
        "computation_record": "none; no computation, solver, oracle, or unsafe code supplies proof credit",
        "step_budget": 4,
        "semantic_step_ledger": {
            "premises": "Only the exact context and incoming proof_requires conclusions.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed edge may consume this output."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-1082/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or checked conditional interface only; no master acceptance, H0, release, or theorem completion.",
        "task_ids": [ITEM, "S56-M-1082-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1082/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-1082 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus bounded pinned anchor audit; constructor/projection architecture selected independently of workflow acceptance.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1082-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": sorted(informational),
    },
    "eligibility_policy": "The imported definition is a substantive bridge despite the short wrapper. Source and provenance overlays cannot earn proof credit.",
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only delta.",
    "exclusions": ["Linear-combination, covariance, continuity, existence, comparison, and concentration theorems are outside the frozen root.", "Aliases and wrappers cannot duplicate semantic or terminal-body credit."],
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"provisionally_checked_interfaces": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen architecture only; no authoritative proof promotion, H0, AUDIT-Z, or theorem completion."
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1082-ROOT": ["M1082-T-COMPOSE"],
    "M1082-T-COMPOSE": ["M1082-T-FORWARD", "M1082-T-REVERSE"],
    "M1082-T-FORWARD": ["M1082-S-CONTEXT", "M1082-S-BOUNDARY", "M1082-X-DEFINITION"],
    "M1082-T-REVERSE": ["M1082-S-CONTEXT", "M1082-S-BOUNDARY", "M1082-X-DEFINITION"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = f"REQ-{parent}-{child}"
        comp = f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

edge_sets = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-CONTEXT", "M1082-ROOT", "logical_decomposition", "M1082-S-CONTEXT"), edge("REF-ROOT-BOUNDARY", "M1082-ROOT", "logical_decomposition", "M1082-S-BOUNDARY")],
    "provenance": [edge("PROV-DEF", "M1082-X-PROVENANCE", "provenance_of", "M1082-X-DEFINITION"), edge("PROV-COMPOSE", "M1082-X-PROVENANCE", "provenance_of", "M1082-T-COMPOSE")],
    "evidence": [],
    "trust": [edge("TRUST-ROOT", "M1082-ROOT", "trusts", "M1082-S-FOUNDATION"), edge("TRUST-PROV", "M1082-ROOT", "trusts", "M1082-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE-ROOT", "M1082-X-SOURCE", "documents", "M1082-ROOT"), edge("DOC-SOURCE-DEF", "M1082-X-SOURCE", "documents", "M1082-X-DEFINITION")],
    "workflow": [edge("FLOW-PROOF-TREE", "M1082-T-COMPOSE", "workflow_depends_on", "M1082-T-FORWARD"), edge("FLOW-PROOF-REVERSE", "M1082-T-COMPOSE", "workflow_depends_on", "M1082-T-REVERSE"), edge("FLOW-VALIDATION", "M1082-X-PROVENANCE", "workflow_depends_on", "M1082-T-COMPOSE")],
}
graphs = {}
for name, edges in edge_sets.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1082-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "statement_source_sha256": statement_hash, "anchor_audit_sha256": anchor_hash,
    "root_node_id": "M1082-ROOT", "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent",
    "nodes": nodes, "graphs": graphs,
    "composition_certificates": [{
        "certificate_id": "COMP-M1082-IFF-V1", "parent": "M1082-T-COMPOSE",
        "required_children": ["M1082-T-FORWARD", "M1082-T-REVERSE"],
        "checked_declaration": "AwesomeTheorems.THM_M_1082.ObligationTree.root_of_directions",
        "status": "interface-composition-kernel-checked; master acceptance open"
    }],
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1082-X-SOURCE", "M1082-S-FOUNDATION", "M1082-X-PROVENANCE"], "reason": "Kernel-checked local interfaces do not substitute for proof-phase acceptance, source closure, trust/provenance validation, or release."}
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1082/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"})

for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / filename).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

lines = ["# THM-M-1082 obligation tree", "", "This registry freezes the constructor/projection architecture. Checked interfaces remain provisional and no theorem-completion claim follows.", ""]
for node in nodes:
    lines += [f"## {node['obligation_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:", "", f"1. Premises: {node['semantic_step_ledger']['premises']}", f"2. Inference: {node['semantic_step_ledger']['inference']}", f"3. Output: {node['semantic_step_ledger']['output']}", f"4. Outgoing use: {node['semantic_step_ledger']['outgoing_use']}", "", f"Boundary: {node['status_boundary']}", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(ids)} obligations; denominator sha256 {denominator}")
