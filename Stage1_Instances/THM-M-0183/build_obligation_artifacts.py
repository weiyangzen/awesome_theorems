#!/usr/bin/env python3
"""Build the frozen THM-M-0183 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0183-OBLIGATION_TREE"
THEOREM = "THM-M-0183"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


ROWS = [
    ("M0183-ROOT", "root", "critical", "Prove the exact frozen prescribed-class Ricci-flat target.", "Stage1Instances.THMM0183.YauCalabiConjectureTarget", "The canonical proposition."),
    ("M0183-S-NATIVE", "transport", "critical", "Realize every abstract statement interface by native Kahler, cohomology, Chern-class, and Ricci APIs without assuming metric existence.", "planned native realization and two-way statement transport", "A faithful native instance of the frozen interfaces."),
    ("M0183-S-BOUNDARY", "branch", "high", "Cover empty, zero-dimensional, and disconnected compact carriers retained by the frozen statement.", "planned boundary-case theorem", "The exact degenerate and componentwise cases."),
    ("M0183-S-FOUNDATION", "certificate", "critical", "Freeze classical choice, quotient, functional-analysis, TCB, and no-oracle policy for terminal bodies.", "planned transitive trust report", "An accepted foundation profile."),
    ("M0183-G-REFERENCE", "construction", "critical", "Choose a reference Kahler metric in the prescribed class and express the desired metric by a global potential.", "planned ddbar/potential construction", "Reference form and potential formulation in kappa."),
    ("M0183-G-RICCI", "transport", "critical", "Translate real first-Chern-class vanishing into an exact Ricci-form potential with correct normalizations.", "planned Chern-Weil and ddbar transport", "A global Ricci potential."),
    ("M0183-P-MONGEAMPERE", "core_lemma", "critical", "Reduce Ricci-flatness in the fixed class to the normalized complex Monge-Ampere equation.", "planned Calabi-Yau PDE reduction", "The exact normalized PDE and positivity condition."),
    ("M0183-P-ESTIMATES", "core_lemma", "critical", "Prove uniform C0, Laplacian/C2, and higher-order estimates along the continuity path.", "planned a-priori estimate package", "Parameter-independent estimates preventing loss of compactness."),
    ("M0183-P-CONTINUITY", "core_lemma", "critical", "Prove openness, closedness, and nonemptiness for the continuity family using the estimates.", "planned continuity-method closure", "A smooth solution at the target parameter."),
    ("M0183-P-REGULARITY", "core_lemma", "high", "Upgrade the weak/limit solution to the smooth positive solution required by the metric interface.", "planned elliptic regularity and positivity theorem", "A smooth Kahler potential."),
    ("M0183-T-METRIC", "terminal", "critical", "Construct the compatible Kahler metric, prove it represents kappa, and transport the PDE identity to vanishing Ricci tensor.", "Stage1Instances.THMM0183.PrescribedClassRicciFlatPackage", "The complete analytic package."),
    ("M0183-T-ASSEMBLE", "terminal", "high", "Apply the analytic package under the identical binders and hypotheses to obtain the frozen root.", "Stage1Instances.THMM0183.yauCalabiConjectureTarget_of_analyticPackage", "The exact canonical root conditional on the analytic package."),
    ("M0183-X-SOURCE", "documentation", "high", "Crosswalk every geometric, PDE, estimate, regularity, and boundary node to reviewed primary-source passages.", "non-machine node-specific source crosswalk", "Human-source coverage only."),
    ("M0183-X-PROVENANCE", "certificate", "critical", "Inventory imports, terminal bodies, axioms, TCB, replay evidence, and deduplicated proof-body identities.", "planned machine-derived provenance closure", "Release provenance without proof credit."),
]

statement = json.loads((HERE / "statement.json").read_text())
statement_fp = statement["canonical_formal_target"]["elaborated_expression_sha256"]
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
checked = {"M0183-T-ASSEMBLE"}
source_na = {"M0183-S-NATIVE", "M0183-S-FOUNDATION", "M0183-X-PROVENANCE"}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in ROWS:
    fingerprint = ("lean-expression-sha256:" + statement_fp if oid == "M0183-ROOT"
                   else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = "not_applicable" if oid == "M0183-X-SOURCE" else ("informational" if oid == "M0183-X-PROVENANCE" else "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only", "informational": "provenance_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0183/ObligationTree.lean#yauCalabiConjectureTarget_of_analyticPackage" if oid == "M0183-T-ASSEMBLE" else None),
    })
    nodes.append({
        "node_id": "THM-M-0183-" + oid.removeprefix("M0183-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else "M4",
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid in checked else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if oid in {"M0183-P-ESTIMATES", "M0183-P-CONTINUITY"} else 50,
        "semantic_step_ledger": {"premises": "Only declared proof children and the frozen formal context.", "inference": claim, "output": output, "outgoing_use": "Only a declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0183/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture or conditional composition only; no unlisted premise or root proof is supplied.",
        "task_ids": [ITEM, "S56-M-0183-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0183/ObligationTree.lean"] if oid == "M0183-T-ASSEMBLE" else [],
        "owner": "THM-M-0183 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact frozen target and bounded anchor audit; classical continuity-method architecture; eligibility fixed before closure observation.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0183-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0183-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M4"},
    "status_boundary": "Frozen architecture and conditional recomposition only; the analytic existence package and root remain open."
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0183-ROOT": ["M0183-T-ASSEMBLE"],
    "M0183-T-ASSEMBLE": ["M0183-T-METRIC"],
    "M0183-T-METRIC": ["M0183-S-NATIVE", "M0183-S-BOUNDARY", "M0183-G-REFERENCE", "M0183-G-RICCI", "M0183-P-REGULARITY"],
    "M0183-P-REGULARITY": ["M0183-P-CONTINUITY"],
    "M0183-P-CONTINUITY": ["M0183-P-MONGEAMPERE", "M0183-P-ESTIMATES"],
    "M0183-P-MONGEAMPERE": ["M0183-G-REFERENCE", "M0183-G-RICCI"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-BOUNDARY", "M0183-ROOT", "logical_decomposition", "M0183-S-BOUNDARY")],
    "provenance": [edge("SRC-PDE", "M0183-P-MONGEAMPERE", "source_map", "M0183-X-SOURCE"), edge("SRC-EST", "M0183-P-ESTIMATES", "source_map", "M0183-X-SOURCE"), edge("PROV-ROOT", "M0183-X-PROVENANCE", "provenance_of", "M0183-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M0183-ROOT", "trusts", "M0183-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0183-ROOT", "trusts", "M0183-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE", "M0183-X-SOURCE", "documents", "M0183-ROOT"), edge("DOC-BOUNDARY", "M0183-S-BOUNDARY", "documents", "M0183-T-METRIC")],
    "workflow": [edge("FLOW-METRIC-PDE", "M0183-T-METRIC", "workflow_depends_on", "M0183-P-REGULARITY"), edge("FLOW-ASSEMBLE-METRIC", "M0183-T-ASSEMBLE", "workflow_depends_on", "M0183-T-METRIC"), edge("FLOW-PROV-ASSEMBLE", "M0183-X-PROVENANCE", "workflow_depends_on", "M0183-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0183-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0183-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0183-T-METRIC"], "composition_certificates": ["Stage1Instances.THMM0183.yauCalabiConjectureTarget_of_analyticPackage"], "reason": "Final logical composition is checked, but its exact analytic package premise is open."}
}

recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0183/check_obligation_tree.py"], "env_allowlist": {"PATH": "runner-provided-pinned-toolchain"}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS and denominator digest"}], "covered_obligation_ids": [oid], "covered_declarations": ["Stage1Instances.THMM0183.yauCalabiConjectureTarget_of_analyticPackage"] if oid == "M0183-T-ASSEMBLE" else []} for oid, *_ in ROWS]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
