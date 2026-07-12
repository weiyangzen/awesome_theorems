#!/usr/bin/env python3
"""Build the frozen THM-M-1269 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1269-OBLIGATION_TREE"
THEOREM = "THM-M-1269"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M1269-ROOT", "root", "critical", "The exact minimizing-sequence proposition frozen in Statement.lean.", "THM_M_1269_statement X F", "The canonical proposition."),
    ("M1269-S-DEFINITIONS", "definition", "high", "Fix Set.range, BddBelow, sInf, atTop, nhds, and Tendsto with their elaborated meanings.", "THM_M_1269_statement X F", "The exact statement interface."),
    ("M1269-S-DOMAIN", "definition", "high", "Preserve X : Type u, F : X -> Real, explicit Nonempty X, and boundedness of the range.", "Nonempty X /\\ BddBelow (Set.range F)", "All domain premises used by the proof route."),
    ("M1269-S-BOUNDARY", "terminal", "high", "Keep empty domains, unbounded ranges, convergence of points, and infimum attainment outside the claimed conclusion.", "statement mutations in Statement.lean", "Reviewed encoding boundary without a stronger theorem."),
    ("M1269-S-FOUNDATION", "certificate", "critical", "Track classical choice used to select one preimage for each range value and the transitive axiom report.", "Lean axiom report and pinned TCB profile", "The explicit foundation and trust boundary."),
    ("M1269-N-RANGE", "normalization", "high", "Normalize the variational problem to the nonempty bounded-below set Set.range F.", "S := Set.range F", "A set to which the pinned sInf sequence theorem applies."),
    ("M1269-B-NONE", "branch", "medium", "Record that the proof has no mathematical case split once nonemptiness and boundedness are hypotheses.", "not-applicable branch analysis", "No hidden branch or exhaustiveness obligation."),
    ("M1269-C-VALUES", "construction", "critical", "Construct a sequence of values in Set.range F converging to its infimum.", "THM_M_1269_RangeApproximation F", "Convergent range values with membership witnesses."),
    ("M1269-C-PREIMAGES", "construction", "critical", "Choose an X-preimage for every constructed range value.", "choose sequence hsequence using hmem", "A sequence in X pointwise mapping to the value sequence."),
    ("M1269-L-SINF", "bridge", "critical", "Apply the pinned mathlib theorem exists_seq_tendsto_sInf to the nonempty bounded-below range.", "exists_seq_tendsto_sInf (Set.range_nonempty F) hbelow", "The range-approximation package."),
    ("M1269-T-TRANSPORT", "transport", "high", "Transport Tendsto across the pointwise equality between F composed with the chosen preimages and the value sequence.", "funext hsequence followed by equality transport", "Convergence of the functional values."),
    ("M1269-T-ASSEMBLE", "terminal", "critical", "Compose range approximation, preimage choice, and convergence transport into the exact statement.", "THM_M_1269_root_of_rangeApproximation", "The exact root conditional on the bridge package."),
    ("M1269-X-SOURCE", "terminal", "high", "Map each mathematical node to a primary or authoritative source with assumptions and errata checked.", "node-specific source crosswalk pending", "Human-source coverage without machine proof credit."),
    ("M1269-X-PROVENANCE", "certificate", "critical", "Bind the mathlib terminal body, wrapper, imports, axioms, toolchain, and replay evidence.", "node-specific provenance record pending", "Release provenance without mathematical proof credit."),
]

checked = {"M1269-S-DEFINITIONS", "M1269-S-DOMAIN", "M1269-S-BOUNDARY", "M1269-B-NONE", "M1269-C-PREIMAGES", "M1269-T-TRANSPORT", "M1269-T-ASSEMBLE"}
source_na = {"M1269-S-DEFINITIONS", "M1269-S-DOMAIN", "M1269-S-BOUNDARY", "M1269-S-FOUNDATION", "M1269-B-NONE", "M1269-X-PROVENANCE"}
informational = {"M1269-B-NONE", "M1269-X-SOURCE", "M1269-X-PROVENANCE"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor_audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    eligibility = "informational" if oid in informational else "required"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "planned:v1:sha256:" + digest([oid, kind, claim, target, output]),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": eligibility,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "architecture/source/provenance overlay; no independent proof credit" if oid in informational else None,
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1269/ObligationTree.lean#THM_M_1269_root_of_rangeApproximation" if oid == "M1269-T-ASSEMBLE" else ("mathlib:Mathlib.Topology.Order.IsLUB#exists_seq_tendsto_sInf" if oid == "M1269-L-SINF" else None),
    })
    if oid in checked:
        machine = "M0-L"
    elif oid in {"M1269-ROOT", "M1269-C-VALUES", "M1269-L-SINF"}:
        machine = "M1"
    elif oid == "M1269-X-SOURCE":
        machine = "not_applicable"
    else:
        machine = "M4"
    nodes.append({
        "node_id": "THM-M-1269-" + oid.removeprefix("M1269-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": claim,
        "formal_target": target,
        "output": output,
        "human_debt": "H2",
        "machine_debt": machine,
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "anchor-audit:M1269-A1" if oid == "M1269-L-SINF" else ("local-conditional-composition" if oid == "M1269-T-ASSEMBLE" else "none"),
        "foundation_profile": "lean4-mathlib-classical/choice-audit-open",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation is used",
        "step_budget": 40,
        "semantic_step_ledger": {
            "premises": "Only exact incoming proof_requires children and the stated formal context.",
            "inference": claim,
            "output": output,
            "outgoing_use": "Only declared typed parent or non-proof support edges may consume this output.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-1269/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no master acceptance, audit closure, or theorem completion.",
        "task_ids": [ITEM, "S56-M-1269-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1269/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-1269 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: obligation[key] for key in fields} for obligation in obligations])
ids = [obligation["obligation_id"] for obligation in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and pinned-anchor audit; eligibility assigned before proof-phase closure is observed.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1269-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": sorted(informational),
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M1"},
    "status_boundary": "The registry freezes scope and denominators only; the proof phase, source audit, provenance closure, and theorem completion remain open.",
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {"M1269-ROOT": ["M1269-T-ASSEMBLE"], "M1269-T-ASSEMBLE": ["M1269-C-VALUES"], "M1269-C-VALUES": ["M1269-L-SINF"], "M1269-L-SINF": ["M1269-N-RANGE"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

edge_sets = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1269-ROOT", "logical_decomposition", "M1269-S-DEFINITIONS"), edge("REF-ROOT-DOMAIN", "M1269-ROOT", "logical_decomposition", "M1269-S-DOMAIN"), edge("REF-ROOT-BOUNDARY", "M1269-ROOT", "logical_decomposition", "M1269-S-BOUNDARY"), edge("REF-ROUTE-BRANCH", "M1269-T-ASSEMBLE", "logical_decomposition", "M1269-B-NONE"), edge("REF-ASSEMBLE-PREIMAGE", "M1269-T-ASSEMBLE", "logical_decomposition", "M1269-C-PREIMAGES"), edge("REF-ASSEMBLE-TRANSPORT", "M1269-T-ASSEMBLE", "logical_decomposition", "M1269-T-TRANSPORT")],
    "provenance": [edge("SRC-ANCHOR", "M1269-L-SINF", "source_map", "M1269-X-SOURCE"), edge("PROV-ROOT", "M1269-X-PROVENANCE", "provenance_of", "M1269-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M1269-ROOT", "trusts", "M1269-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M1269-ROOT", "trusts", "M1269-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", "M1269-S-DEFINITIONS", "documents", "M1269-ROOT"), edge("DOC-ANCHOR", "M1269-X-SOURCE", "documents", "M1269-L-SINF")],
    "workflow": [edge("FLOW-PROOF-ANCHOR", "M1269-C-VALUES", "workflow_depends_on", "M1269-L-SINF"), edge("FLOW-PROOF-ASSEMBLE", "M1269-T-ASSEMBLE", "workflow_depends_on", "M1269-C-VALUES"), edge("FLOW-PROVENANCE", "M1269-X-PROVENANCE", "workflow_depends_on", "M1269-T-ASSEMBLE")],
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
    "registry_id": "THM-M-1269-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1269-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1269-L-SINF"], "composition_certificates": ["THM_M_1269_root_of_rangeApproximation"], "reason": "The checked assembly is conditional; the pinned anchor bridge is not installed as proof-phase evidence."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1269/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)

