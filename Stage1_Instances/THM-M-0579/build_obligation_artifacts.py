#!/usr/bin/env python3
"""Build the frozen THM-M-0579 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0579-OBLIGATION_TREE"
THEOREM = "THM-M-0579"


def sha(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0579-ROOT", "root", "critical", "The exact compact simply connected topological three-manifold target.", "Stage1Instances.THMM0579.Statement", "The canonical proposition."),
    ("M0579-S-OBJECT", "definition", "high", "Freeze the Hausdorff compact boundaryless three-manifold and unit three-sphere object model.", "Stage1Instances.THMM0579.{Statement,ModelSpace3,Sphere3}", "The exact elaborated object-model interface."),
    ("M0579-S-BOUNDARY", "terminal", "high", "Account for connectedness, nonemptiness, compactness, absence of boundary, and the empty-type exclusion.", "planned checked instance and boundary lemmas", "Checked statement boundary cases."),
    ("M0579-S-FOUNDATION", "certificate", "critical", "Freeze classical choice, quotient, extensionality, TCB, and no-oracle policies.", "planned exact foundation and transitive axiom report", "Accepted trust boundary."),
    ("M0579-N-SMOOTH", "reduction", "critical", "Pass from the topological chart model to a compatible smooth/PL structure suitable for geometric evolution, without changing the homeomorphism target.", "planned topological-to-smooth three-manifold reduction", "A compatible smooth closed three-manifold."),
    ("M0579-N-PRIME", "normalization", "high", "Normalize by orientability and prime decomposition and show simple connectedness selects the relevant prime branch.", "planned orientability and prime-decomposition package", "A normalized simply connected prime input."),
    ("M0579-C-FLOW", "construction", "critical", "Construct Ricci flow with surgery from the normalized manifold.", "planned Ricci-flow-with-surgery construction", "A surgery flow with controlled time slices."),
    ("M0579-C-INVARIANTS", "construction", "critical", "Prove surgery choices, canonical neighborhoods, curvature control, and topology tracking preserve the required invariants.", "planned surgery invariant and independence package", "A well-defined topologically tracked evolution."),
    ("M0579-L-ANALYTIC", "core_lemma", "critical", "Establish the noncollapsing, canonical-neighborhood, and long-time estimates required to continue the surgery flow.", "planned Perelman analytic estimates package", "Continuation and control for every surgery stage."),
    ("M0579-L-EXTINCTION", "core_lemma", "critical", "Prove finite-time extinction for the simply connected closed case.", "planned finite-extinction theorem", "Finite extinction of every normalized input flow."),
    ("M0579-B-SURGERY", "branch", "critical", "Classify every surgery component and prove exhaustive recomposition of discarded and surviving pieces.", "planned surgery branch classification and recomposition", "A complete topological history of the input."),
    ("M0579-T-RECOGNITION", "terminal", "critical", "Deduce that the original manifold is homotopy equivalent to the three-sphere.", "Stage1Instances.THMM0579.HomotopySphereRecognition", "A homotopy equivalence with Sphere3."),
    ("M0579-T-RIGIDITY", "terminal", "critical", "Upgrade the three-dimensional homotopy-sphere conclusion to a homeomorphism in the exact target model.", "Stage1Instances.THMM0579.HomotopySphereTopologicalRigidity", "A homeomorphism with Sphere3."),
    ("M0579-T-ASSEMBLE", "transport", "high", "Compose recognition and rigidity into the exact canonical target.", "Stage1Instances.THMM0579.root_of_recognition_and_rigidity", "The exact root conditional on both packages."),
    ("M0579-X-SOURCE", "terminal", "high", "Map every material reduction, analytic theorem, and surgery step to reviewed primary-source passages and conventions.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0579-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, axioms, TCB, computation, and replay evidence.", "planned machine-derived provenance and trust closure", "Release provenance without proof credit."),
]

checked = {"M0579-S-OBJECT", "M0579-T-ASSEMBLE"}
source_na = {"M0579-S-OBJECT", "M0579-S-BOUNDARY", "M0579-S-FOUNDATION", "M0579-X-PROVENANCE"}
machine_special = {"M0579-X-SOURCE": "not_applicable", "M0579-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
expression_hash = json.loads((HERE / "statement.json").read_text())["canonical_formal_target"]["elaborated_expression_hash"]

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fp = ("lean-expression-sha256:" + expression_hash if oid in {"M0579-ROOT", "M0579-S-OBJECT"}
          else "planned:v1:sha256:" + sha([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0579/ObligationTree.lean#root_of_recognition_and_rigidity" if oid == "M0579-T-ASSEMBLE" else None),
    })
    nodes.append({
        "node_id": "THM-M-0579-" + oid.removeprefix("M0579-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H3", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0579-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M0579-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if oid in {"M0579-C-FLOW", "M0579-L-ANALYTIC", "M0579-L-EXTINCTION"} else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires children and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only a declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0579/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0579-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0579/ObligationTree.lean"] if oid == "M0579-T-ASSEMBLE" else [],
        "owner": "THM-M-0579 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = sha([{k: o[k] for k in fields} for o in obligations])
ids = [o["obligation_id"] for o in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; Ricci-flow/surgery/extinction architecture; eligibility assigned independently of proof availability.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0579-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0579-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Poincare proof, source acceptance, audit completion, or theorem completion."
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0579-ROOT": ["M0579-T-ASSEMBLE"],
    "M0579-T-ASSEMBLE": ["M0579-T-RECOGNITION", "M0579-T-RIGIDITY"],
    "M0579-T-RECOGNITION": ["M0579-N-SMOOTH", "M0579-N-PRIME", "M0579-C-FLOW", "M0579-C-INVARIANTS", "M0579-L-ANALYTIC", "M0579-L-EXTINCTION", "M0579-B-SURGERY"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-OBJECT", "M0579-ROOT", "logical_decomposition", "M0579-S-OBJECT"), edge("REF-ROOT-BOUNDARY", "M0579-ROOT", "logical_decomposition", "M0579-S-BOUNDARY"), edge("REF-ROOT-FOUNDATION", "M0579-ROOT", "logical_decomposition", "M0579-S-FOUNDATION")],
    "provenance": [edge("SRC-FLOW", "M0579-C-FLOW", "source_map", "M0579-X-SOURCE"), edge("SRC-ANALYTIC", "M0579-L-ANALYTIC", "source_map", "M0579-X-SOURCE"), edge("PROV-ROOT", "M0579-X-PROVENANCE", "provenance_of", "M0579-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0579-ROOT", "trusts", "M0579-S-FOUNDATION"), edge("TRUST-PROV", "M0579-ROOT", "trusts", "M0579-X-PROVENANCE")],
    "documentation": [edge("DOC-OBJECT", "M0579-S-OBJECT", "documents", "M0579-ROOT"), edge("DOC-SOURCE", "M0579-X-SOURCE", "documents", "M0579-L-ANALYTIC")],
    "workflow": [edge("FLOW-ASSEMBLE-RECOGNITION", "M0579-T-ASSEMBLE", "workflow_depends_on", "M0579-T-RECOGNITION"), edge("FLOW-ASSEMBLE-RIGIDITY", "M0579-T-ASSEMBLE", "workflow_depends_on", "M0579-T-RIGIDITY"), edge("FLOW-RECOGNITION-EXTINCTION", "M0579-T-RECOGNITION", "workflow_depends_on", "M0579-L-EXTINCTION"), edge("FLOW-PROV-ASSEMBLE", "M0579-X-PROVENANCE", "workflow_depends_on", "M0579-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0579-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0579-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0579-T-RECOGNITION", "M0579-T-RIGIDITY"], "composition_certificates": ["Stage1Instances.THMM0579.root_of_recognition_and_rigidity"], "reason": "Final composition is conditional; neither terminal package has a proof body."}
}

specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0579/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
