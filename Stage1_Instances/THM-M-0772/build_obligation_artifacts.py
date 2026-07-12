#!/usr/bin/env python3
"""Build the frozen THM-M-0772 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0772-OBLIGATION_TREE"
THEOREM = "THM-M-0772"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0772-ROOT", "root", "critical", "Every partially ordered type has an inclusion-maximal chain.", "Stage1Instances.THM_M_0772.HausdorffMaximalPrinciple", "The exact frozen existential target."),
    ("M0772-S-DEFINITIONS", "definition", "high", "Freeze IsChain and IsMaxChain as comparability and inclusion-maximality, respectively.", "IsChain (fun x y => x <= y) c; IsMaxChain (fun x y => x <= y) c", "The predicates used by the canonical statement."),
    ("M0772-S-DOMAIN", "definition", "high", "Preserve universe-polymorphic P : Type u and its PartialOrder instance without a nonemptiness assumption.", "(P : Type u) [PartialOrder P]", "The exact domain and typeclass context."),
    ("M0772-S-BOUNDARY", "branch", "normal", "Account for empty and singleton carriers without excluding either from the theorem.", "emptyBoundary; singletonBoundary", "Checked maximal-chain witnesses for both boundary carriers."),
    ("M0772-S-EXPANDED", "transport", "normal", "Relate IsMaxChain to chainhood plus equality with every containing chain.", "hausdorffMaximalPrinciple_iff_expanded", "A checked bidirectional statement transport."),
    ("M0772-S-FOUNDATION", "certificate", "critical", "Record the allowed classical-choice, quotient, propositional-extensionality, kernel, and no-oracle boundary.", "planned transitive foundation and trust certificate", "A release-grade foundation report."),
    ("M0772-N-RELATION", "normalization", "high", "Specialize the relation-generic maximal-chain theorem to the partial-order relation (fun x y => x <= y).", "RelationGenericMaxChain -> CanonicalTarget", "The exact order-specific bridge input."),
    ("M0772-C-WITNESS", "construction", "high", "Choose maxChain (fun x y => x <= y) as the existential witness.", "maxChain (fun x y => x <= y)", "A Set P witness for the root existential."),
    ("M0772-L-MAXCHAIN", "bridge", "critical", "Supply a maximal chain for every type and binary relation.", "forall P r, exists c, IsMaxChain r c", "The relation-generic existence fact consumed by the adapter."),
    ("M0772-T-ADAPTER", "terminal", "critical", "Consume the relation-generic bridge, specialize it, and package the witness at the canonical target.", "root_of_relationGenericMaxChain", "CanonicalTarget under exactly one named bridge premise."),
    ("M0772-X-MATHLIB-BODY", "terminal", "critical", "Audit the terminal mathlib proof body and its transitive construction dependencies at the pinned revision.", "Mathlib.Order.CompleteLattice.Chain.maxChain_spec", "Pinned imported proof-body provenance for M0772-L-MAXCHAIN."),
    ("M0772-X-PROVENANCE", "certificate", "critical", "Close transitive declarations, imports, axioms, placeholders, TCB, license, and replay provenance.", "planned machine-derived provenance closure", "Release provenance without duplicate mathematical credit."),
    ("M0772-X-SOURCE", "terminal", "high", "Map the maximal-chain construction and maximality argument to independently reviewed primary-source passages.", "node-specific human source crosswalk", "Human-source coverage without machine proof credit."),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
checked = {"M0772-S-DEFINITIONS", "M0772-S-DOMAIN", "M0772-S-BOUNDARY", "M0772-S-EXPANDED", "M0772-N-RELATION", "M0772-C-WITNESS", "M0772-T-ADAPTER"}
source_na = {"M0772-S-DEFINITIONS", "M0772-S-DOMAIN", "M0772-S-BOUNDARY", "M0772-S-EXPANDED", "M0772-S-FOUNDATION", "M0772-X-PROVENANCE"}
machine_special = {"M0772-X-SOURCE": "not_applicable", "M0772-X-PROVENANCE": "informational"}
body_ids = {
    "M0772-L-MAXCHAIN": "mathlib:8a178386:Mathlib.Order.CompleteLattice.Chain#maxChain_spec",
    "M0772-T-ADAPTER": "local:Stage1_Instances/THM-M-0772/ObligationTree.lean#root_of_relationGenericMaxChain",
    "M0772-X-MATHLIB-BODY": "mathlib:8a178386:Mathlib.Order.CompleteLattice.Chain#maxChain_spec",
}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = ("lean-source:v1:sha256:" + statement_hash) if oid in {"M0772-ROOT", "M0772-S-DEFINITIONS", "M0772-S-DOMAIN", "M0772-S-BOUNDARY", "M0772-S-EXPANDED"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    registry_kind = {"normalization": "reduction", "bridge": "lemma", "certificate": "terminal"}.get(kind, kind)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": registry_kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body_ids.get(oid),
    })
    machine_debt = "M0-L" if oid in checked else ("M3" if oid in {"M0772-ROOT", "M0772-T-ADAPTER"} else ("M0-W" if oid == "M0772-L-MAXCHAIN" else "M4"))
    nodes.append({
        "node_id": "THM-M-0772-" + oid.removeprefix("M0772-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": machine_debt, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "C-MATHLIB-01" if oid in {"M0772-L-MAXCHAIN", "M0772-X-MATHLIB-BODY"} else ("local-conditional-composition" if oid == "M0772-T-ADAPTER" else "none"),
        "foundation_profile": "lean4-mathlib-classical/propext+choice+Quot.sound/policy-acceptance-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation, solver, or oracle closes this node",
        "step_budget": 40 if risk != "critical" else 100,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires conclusions and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0772/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no master acceptance, source closure, or release claim.",
        "task_ids": [ITEM, "S56-M-0772-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0772/ObligationTree.lean"] if oid in checked or oid == "M0772-L-MAXCHAIN" else [],
        "owner": "THM-M-0772 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; the relation-generic imported theorem is a bridge obligation rather than a one-line root proof.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0772-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0772-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "provisional_anchor": "M0772-L-MAXCHAIN", "root_machine_debt": "M3"},
    "status_boundary": "Frozen architecture and conditional composition only; proof acceptance, human-source review, provenance closure, audit completion, and theorem completion remain open.",
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0772-ROOT": ["M0772-T-ADAPTER"],
    "M0772-T-ADAPTER": ["M0772-N-RELATION", "M0772-C-WITNESS", "M0772-L-MAXCHAIN"],
    "M0772-L-MAXCHAIN": ["M0772-X-MATHLIB-BODY"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0772-ROOT", "logical_decomposition", "M0772-S-DEFINITIONS"), edge("REF-ROOT-DOMAIN", "M0772-ROOT", "logical_decomposition", "M0772-S-DOMAIN"), edge("REF-ROOT-BOUNDARY", "M0772-ROOT", "logical_decomposition", "M0772-S-BOUNDARY"), edge("REF-ROOT-EXPANDED", "M0772-ROOT", "logical_decomposition", "M0772-S-EXPANDED")],
    "provenance": [edge("PROV-BRIDGE-BODY", "M0772-X-MATHLIB-BODY", "provenance_of", "M0772-L-MAXCHAIN"), edge("SOURCE-BRIDGE", "M0772-L-MAXCHAIN", "source_map", "M0772-X-SOURCE"), edge("PROV-ROOT", "M0772-X-PROVENANCE", "provenance_of", "M0772-ROOT")],
    "evidence": [edge("EVIDENCE-BOUNDARY", "M0772-S-BOUNDARY", "evidence_for", "M0772-ROOT")],
    "trust": [edge("TRUST-FOUNDATION", "M0772-ROOT", "trusts", "M0772-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0772-ROOT", "trusts", "M0772-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFINITIONS", "M0772-S-DEFINITIONS", "documents", "M0772-ROOT"), edge("DOC-SOURCE", "M0772-X-SOURCE", "documents", "M0772-L-MAXCHAIN")],
    "workflow": [edge("FLOW-ROOT-ADAPTER", "M0772-ROOT", "workflow_depends_on", "M0772-T-ADAPTER"), edge("FLOW-ADAPTER-BRIDGE", "M0772-T-ADAPTER", "workflow_depends_on", "M0772-L-MAXCHAIN"), edge("FLOW-PROVENANCE-BODY", "M0772-X-PROVENANCE", "workflow_depends_on", "M0772-X-MATHLIB-BODY")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0772-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0772-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "provisional_obligations": ["M0772-L-MAXCHAIN"], "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0772-X-MATHLIB-BODY"], "composition_certificates": ["Stage1Instances.THM_M_0772.ObligationTree.root_of_relationGenericMaxChain"], "reason": "The adapter is checked only as a conditional composition; proof-body provenance and master proof acceptance are downstream."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0772/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0772 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
