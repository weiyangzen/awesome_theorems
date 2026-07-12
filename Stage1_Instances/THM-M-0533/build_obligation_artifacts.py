#!/usr/bin/env python3
"""Build the frozen THM-M-0533 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0533-OBLIGATION_TREE"
THEOREM = "THM-M-0533"

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

rows = [
    ("M0533-ROOT", "root", "critical", "The exact open-cover integral singular-homology Mayer-Vietoris sequence.", "AwesomeTheorems.THM_M_0533.MayerVietorisSequence", "The canonical proposition."),
    ("M0533-S-DEFINITIONS", "definition", "high", "Freeze integral coefficients, open subspaces, inclusion maps, signs, and natural-degree indexing.", "Statement.lean definitions", "The exact elaborated interface."),
    ("M0533-S-BOUNDARY", "branch", "high", "Retain arbitrary spaces, empty intersection cases, degree zero, and the terminal map to zero.", "planned boundary-case audit", "All canonical quantifiers and endpoints are preserved."),
    ("M0533-S-FOUNDATION", "certificate", "critical", "Freeze classical choice, quotients, noncomputability, imports, TCB, and no-oracle policy.", "planned transitive trust report", "An accepted foundation profile."),
    ("M0533-C-SUBDIVISION", "construction", "critical", "Construct a sufficiently iterated barycentric subdivision and small-chain cover operator for U and V.", "planned singular-chain subdivision package", "Chains subordinate to the open cover, with chain homotopy to identity."),
    ("M0533-L-SMALL-QUASIISO", "core_lemma", "critical", "Prove inclusion of cover-small singular chains into all singular chains is a quasi-isomorphism.", "planned small-chain quasi-isomorphism", "Homology may be computed on the cover-small subcomplex."),
    ("M0533-C-CHAIN-SES", "construction", "critical", "Construct the short exact chain-complex sequence for intersection, biproduct, and cover-small chains.", "planned chain short exact sequence", "A degreewise exact short complex with the canonical signs."),
    ("M0533-L-CHAIN-KERNEL", "core_lemma", "critical", "Identify the kernel of the signed intersection map and the image of the sum map degreewise.", "planned degreewise chain exactness", "Exactness of the cover chain sequence."),
    ("M0533-C-BOUNDARY", "construction", "critical", "Obtain the connecting homomorphisms from the short exact sequence in homology.", "planned homology connecting morphism", "A boundary map in every natural degree."),
    ("M0533-L-NATURALITY", "core_lemma", "high", "Identify abstract induced maps with firstMap and secondMap, including the minus sign.", "planned map-identification lemmas", "The derived sequence uses exactly the frozen maps."),
    ("M0533-T-CONSTRUCTION", "terminal", "critical", "Package the boundary maps and all three consecutive-zero identities.", "AwesomeTheorems.THM_M_0533.ConstructionPackage", "ConstructionPackage for every covered pair."),
    ("M0533-T-EXACT-INTER", "terminal", "critical", "Prove exactness at each intersection-homology term.", "first conjunct of MayerVietorisDegree", "Exactness of boundary followed by firstMap."),
    ("M0533-T-EXACT-BIPROD", "terminal", "critical", "Prove exactness at each biproduct-homology term.", "second conjunct of MayerVietorisDegree", "Exactness of firstMap followed by secondMap."),
    ("M0533-T-EXACT-SPACE", "terminal", "critical", "Prove exactness at each ambient-space homology term.", "third conjunct of MayerVietorisDegree", "Exactness of secondMap followed by boundary."),
    ("M0533-T-DEGREE-ZERO", "terminal", "critical", "Prove exactness of H_0(U) direct-sum H_0(V) to H_0(X) to zero.", "canonical degree-zero endpoint", "Surjectivity at H_0(X)."),
    ("M0533-T-EXACTNESS", "transport", "high", "Combine all recurring exactness segments and the degree-zero endpoint.", "AwesomeTheorems.THM_M_0533.ExactnessPackage", "ExactnessPackage for each construction."),
    ("M0533-T-ASSEMBLE", "transport", "high", "Consume construction and exactness packages to obtain the exact root.", "AwesomeTheorems.THM_M_0533.root_of_construction_and_exactness", "The canonical root, conditional on open children."),
    ("M0533-X-SOURCE", "terminal", "high", "Map every substantive topology lemma and convention to reviewed primary-source passages.", "human source crosswalk", "Human-source coverage without machine credit."),
    ("M0533-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, axioms, placeholders, and replay evidence.", "planned provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"M0533-S-DEFINITIONS", "M0533-T-ASSEMBLE"}
source_na = {"M0533-S-DEFINITIONS", "M0533-S-BOUNDARY", "M0533-S-FOUNDATION", "M0533-T-ASSEMBLE", "M0533-X-PROVENANCE"}
machine_special = {"M0533-X-SOURCE": "not_applicable", "M0533-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest()

obligations, nodes = [], []
for oid, kind, risk, claim, target, output in rows:
    fp = ("lean-source:v1:sha256:" + statement_hash) if oid in {"M0533-ROOT", "M0533-S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    body = "local:Stage1_Instances/THM-M-0533/ObligationTree.lean#root_of_construction_and_exactness" if oid == "M0533-T-ASSEMBLE" else None
    obligations.append({"obligation_id": oid, "statement_fingerprint": fp, "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required", "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine), "terminal_proof_body_id": body})
    nodes.append({"node_id": oid, "obligation_id": oid, "kind": kind, "human_statement": claim, "formal_target": target, "output": output, "human_debt": "H3", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0533-ROOT" else "M4"), "readability_debt": "R4", "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending", "provenance_id": "local-conditional-composition" if body else "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; no oracle or experiment may close this node", "step_budget": 4, "semantic_step_ledger": {"premises": "Only exact incoming proof requirements and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only a declared typed edge may consume this output."}, "public_readable_target": "Stage1_Instances/THM-M-0533/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise or root closure.", "task_ids": [ITEM, "S56-M-0533-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0533/ObligationTree.lean"] if body else [], "owner": "THM-M-0533 proof lane", "reviewer": "independent Stage1 integration lane", "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"}})

ids = [o["obligation_id"] for o in obligations]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: o[k] for k in fields} for o in obligations])
registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact open-cover statement and bounded anchor audit; classical small-chain/excision architecture fixed before observing closure.", "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash, "root_obligation_id": "M0533-ROOT", "denominator_sha256": denominator, "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0533-X-PROVENANCE"]}, "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new registry version and append-only old/new ID delta.", "obligations": obligations, "append_only_delta": [], "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"}, "status_boundary": "Scope and denominators only; no Mayer-Vietoris proof, audit completion, or theorem completion."}

requires = {"M0533-ROOT": ["M0533-T-ASSEMBLE"], "M0533-T-ASSEMBLE": ["M0533-T-CONSTRUCTION", "M0533-T-EXACTNESS"], "M0533-T-CONSTRUCTION": ["M0533-C-BOUNDARY", "M0533-L-NATURALITY"], "M0533-T-EXACTNESS": ["M0533-T-EXACT-INTER", "M0533-T-EXACT-BIPROD", "M0533-T-EXACT-SPACE", "M0533-T-DEGREE-ZERO"], "M0533-C-BOUNDARY": ["M0533-C-CHAIN-SES"], "M0533-C-CHAIN-SES": ["M0533-C-SUBDIVISION", "M0533-L-SMALL-QUASIISO", "M0533-L-CHAIN-KERNEL"]}
def edge(eid, source, typ, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal: row["reciprocal_edge_id"] = reciprocal
    return row
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]
graph_edges = {"proof": proof, "refinement": [edge("REF-ROOT-DEFS", "M0533-ROOT", "logical_decomposition", "M0533-S-DEFINITIONS"), edge("REF-ROOT-BOUND", "M0533-ROOT", "logical_decomposition", "M0533-S-BOUNDARY")], "provenance": [edge("SRC-SMALL", "M0533-L-SMALL-QUASIISO", "source_map", "M0533-X-SOURCE"), edge("PROV-ROOT", "M0533-X-PROVENANCE", "provenance_of", "M0533-ROOT")], "evidence": [], "trust": [edge("TRUST-FOUND", "M0533-ROOT", "trusts", "M0533-S-FOUNDATION"), edge("TRUST-PROV", "M0533-ROOT", "trusts", "M0533-X-PROVENANCE")], "documentation": [edge("DOC-DEFS", "M0533-S-DEFINITIONS", "documents", "M0533-ROOT"), edge("DOC-SOURCE", "M0533-X-SOURCE", "documents", "M0533-C-SUBDIVISION")], "workflow": [edge("FLOW-ASSEMBLE-CONSTRUCTION", "M0533-T-ASSEMBLE", "workflow_depends_on", "M0533-T-CONSTRUCTION"), edge("FLOW-ASSEMBLE-EXACT", "M0533-T-ASSEMBLE", "workflow_depends_on", "M0533-T-EXACTNESS"), edge("FLOW-PROV-ASSEMBLE", "M0533-X-PROVENANCE", "workflow_depends_on", "M0533-T-ASSEMBLE")]}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-0533-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "statement_source_sha256": statement_hash, "root_node_id": "M0533-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs, "composition_certificates": [{"parent": "M0533-ROOT", "declaration": "AwesomeTheorems.THM_M_0533.root_of_construction_and_exactness", "premises": ["M0533-T-CONSTRUCTION", "M0533-T-EXACTNESS"], "status": "checked_conditional"}], "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0533-C-SUBDIVISION", "M0533-L-SMALL-QUASIISO", "M0533-L-CHAIN-KERNEL", "M0533-L-NATURALITY", "M0533-T-DEGREE-ZERO"], "reason": "Final composition is conditional; construction and exactness have no proof bodies."}}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(v) for v in graph_edges.values())} typed edges")
print(denominator)
