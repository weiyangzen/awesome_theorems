#!/usr/bin/env python3
"""Build the frozen THM-M-0768 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0768-OBLIGATION_TREE"
THEOREM = "THM-M-0768"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M0768-ROOT", "root", "critical", "The exact frozen raw-function Cantor-Bernstein-Schroeder proposition.", "Stage1Instances.THM_M_0768.CantorBernsteinSchroederTarget", 20),
    ("M0768-S-INTERFACE", "definition", "high", "Preserve two arbitrary universes, raw functions, both injectivity hypotheses, and an existential bijection.", "Stage1Instances.THM_M_0768.CantorBernsteinSchroederTarget", 20),
    ("M0768-S-TRANSPORT", "transport", "normal", "Relate the raw-function target to the bundled embedding/equivalence target in both directions.", "Stage1Instances.THM_M_0768.target_iff_bundled", 25),
    ("M0768-S-BOUNDARY", "branch", "high", "Account for empty carriers without adding nonemptiness assumptions.", "Mathlib source branch: isEmpty_or_nonempty beta", 20),
    ("M0768-L-RELATIONAL", "bridge", "critical", "Supply the stronger relation-preserving Schroeder-Bernstein package at the exact universes.", "Stage1Instances.THM_M_0768.RelationalPackage", 100),
    ("M0768-C-FIXPOINT", "construction", "critical", "Construct the least fixed point of s |-> complement (g '' complement (f '' s)).", "Mathlib source: F : Set alpha ->o Set alpha; s := F.lfp", 55),
    ("M0768-L-FIXPOINT", "core_lemma", "critical", "Show the least fixed point partitions the complements used by the piecewise map.", "Mathlib source: F.map_lfp and compl_injective", 35),
    ("M0768-C-INVERSE", "construction", "high", "Construct invFun g and identify its image of the fixed-point complement.", "Mathlib source: g' := invFun g; hg'ns", 45),
    ("M0768-C-PIECEWISE", "construction", "critical", "Define the piecewise function using f on the fixed point and invFun g elsewhere.", "Mathlib source: h := s.piecewise f g'", 25),
    ("M0768-L-SURJECTIVE", "lemma", "high", "Prove the piecewise function is surjective from its two image pieces.", "Mathlib source: range_piecewise, hg'ns, union_compl_self", 35),
    ("M0768-L-INJECTIVE", "lemma", "critical", "Prove the piecewise function is injective, including both cross-piece cases.", "Mathlib source: injective_piecewise_iff proof", 70),
    ("M0768-T-RELATION", "terminal", "high", "Show the selected branch preserves the arbitrary pointwise relation.", "Mathlib source: final split using hp1, hp2 and invFun_eq", 45),
    ("M0768-T-SPECIALIZE", "transport", "high", "Specialize the relational package to True and discard only its relation witness.", "Stage1Instances.THM_M_0768.root_of_relational_package", 15),
    ("M0768-X-SOURCE", "terminal", "high", "Map the construction and lemma nodes to reviewed primary mathematical sources.", "non-machine primary-source crosswalk", 40),
    ("M0768-X-FOUNDATION", "certificate", "critical", "Freeze classical logic, choice, quotient, propext, kernel, and no-oracle policy.", "planned transitive axiom and TCB certificate", 35),
    ("M0768-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, revisions, hashes, and replay evidence.", "planned terminal-body provenance certificate", 40),
]

checked = {"M0768-S-INTERFACE", "M0768-S-TRANSPORT", "M0768-T-SPECIALIZE"}
source_na = {"M0768-S-INTERFACE", "M0768-S-TRANSPORT", "M0768-X-FOUNDATION", "M0768-X-PROVENANCE"}
machine_special = {"M0768-X-SOURCE": "not_applicable", "M0768-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, budget in rows:
    machine = machine_special.get(oid, "required")
    fp = "planned:v1:sha256:" + digest([oid, kind, claim, target])
    if oid in {"M0768-ROOT", "M0768-S-INTERFACE"}:
        fp = "lean-expression-sha256:6de4e6083a9f47066dfed88584ba5366362c0774b16762b5fbab6d09fc39dcc0"
    body = None
    if oid == "M0768-T-SPECIALIZE":
        body = "local:Stage1_Instances/THM-M-0768/ObligationTree.lean#root_of_relational_package"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "provenance_overlay_no_independent_proof_credit"}.get(machine),
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0768-" + oid.removeprefix("M0768-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": claim,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0768-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M0768-T-SPECIALIZE" else "none",
        "foundation_profile": "lean4-mathlib-classical/propext-choice-quotient-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires children and the declared formal context.", "inference": claim, "output": claim, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0768/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen interface or architecture only; no unlisted premise and no root proof credit is supplied.",
        "task_ids": [ITEM, "S56-M-0768-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0768/ObligationTree.lean"] if oid == "M0768-T-SPECIALIZE" else [],
        "owner": "THM-M-0768 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated target and bounded anchor audit; the stronger relational fixed-point architecture was selected before proof-node closure observation.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0768-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0768-X-PROVENANCE"]},
    "mandatory_layer_analysis": {"normalization": "not_applicable: the exact bridge consumes arbitrary functions directly, with no representative or finite/infinite normalization", "branch": "applicable: empty-carrier and piecewise cross-branch obligations are explicit", "computation": "not_applicable: no finite computation, reflection, solver, or oracle participates; trust remains separately required"},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; no imported bridge is credited and no theorem, source, provenance, or release completion is claimed.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {"M0768-ROOT": ["M0768-T-SPECIALIZE"], "M0768-T-SPECIALIZE": ["M0768-L-RELATIONAL"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req = f"REQ-{parent}-{child}"
        comp = f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

internal = ["M0768-S-BOUNDARY", "M0768-C-FIXPOINT", "M0768-L-FIXPOINT", "M0768-C-INVERSE", "M0768-C-PIECEWISE", "M0768-L-SURJECTIVE", "M0768-L-INJECTIVE", "M0768-T-RELATION"]
graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-INTERFACE", "M0768-ROOT", "logical_decomposition", "M0768-S-INTERFACE"), edge("REF-ROOT-TRANSPORT", "M0768-ROOT", "logical_decomposition", "M0768-S-TRANSPORT")] + [edge("REF-REL-" + x, "M0768-L-RELATIONAL", "logical_decomposition", x) for x in internal],
    "provenance": [edge("SRC-REL", "M0768-L-RELATIONAL", "source_map", "M0768-X-SOURCE"), edge("PROV-BRIDGE", "M0768-X-PROVENANCE", "provenance_of", "M0768-L-RELATIONAL")],
    "evidence": [],
    "trust": [edge("TRUST-ROOT", "M0768-ROOT", "trusts", "M0768-X-FOUNDATION"), edge("TRUST-PROV", "M0768-ROOT", "trusts", "M0768-X-PROVENANCE")],
    "documentation": [edge("DOC-INTERFACE", "M0768-S-INTERFACE", "documents", "M0768-ROOT"), edge("DOC-SOURCE", "M0768-X-SOURCE", "documents", "M0768-L-RELATIONAL")],
    "workflow": [edge("FLOW-SPECIALIZE-BRIDGE", "M0768-T-SPECIALIZE", "workflow_depends_on", "M0768-L-RELATIONAL"), edge("FLOW-PROV-BRIDGE", "M0768-X-PROVENANCE", "workflow_depends_on", "M0768-L-RELATIONAL")],
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
    "registry_id": "THM-M-0768-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0768-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0768-L-RELATIONAL"], "composition_certificates": ["Stage1Instances.THM_M_0768.root_of_relational_package"], "reason": "The checked specialization is conditional; the relational package remains an uncredited bridge until the proof phase."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0768/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid, *_ in rows]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
