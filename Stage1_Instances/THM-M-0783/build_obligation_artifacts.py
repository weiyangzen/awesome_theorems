#!/usr/bin/env python3
"""Generate the frozen THM-M-0783 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0783-OBLIGATION_TREE"
THEOREM = "THM-M-0783"

# Semantic inventory is frozen independently of proof availability. The
# expanded dense-family solver stays open: assuming it would merely assume MA.
ROWS = [
    ("M0783-ROOT", "root", "Martin's axiom for every cardinal strictly below the continuum.", "Stage1Instances.THM_M_0783.MartinsAxiom", "required", "required", 20),
    ("M0783-S-INTERFACE", "definition", "Preserve the forcing order, compatibility, ccc, density, filter, universe, and strict continuum-bound conventions.", "Stage1Instances.THM_M_0783.MartinsAxiom", "required", "not_applicable", 35),
    ("M0783-L-DENSE-FAMILY", "core_lemma", "For arbitrary kappa, ccc nonempty partial order, and at most kappa dense sets, construct one filter meeting every dense set.", "Stage1Instances.THM_M_0783.ObligationTree.DenseFamilySolver", "required", "required", 100),
    ("M0783-T-ASSEMBLE", "transport", "Transport the fully expanded dense-family solver to the canonical Martin's-axiom declaration.", "Stage1Instances.THM_M_0783.ObligationTree.root_of_denseFamilySolver", "required", "required", 10),
    ("M0783-N-NA", "normalization", "Record that no representative, symmetry, finite/infinite, or local/global normalization occurs beyond the checked definitional expansion.", "not applicable: canonical target is already the primitive universal formulation", "not_applicable", "not_applicable", 10),
    ("M0783-B-NA", "branch", "Record that the architecture has no mathematical case split; all quantified forcing instances remain uniform.", "not applicable: no branch split is used", "not_applicable", "not_applicable", 10),
    ("M0783-C-NA", "construction", "Record that filter construction is the still-open core obligation rather than a separately available construction package.", "not applicable as a separate layer; construction is exactly M0783-L-DENSE-FAMILY", "not_applicable", "not_applicable", 10),
    ("M0783-X-SOURCE", "source_boundary", "Bind every root-relevant claim to a reviewed primary definition and distinguish an axiom from a ZFC theorem.", "primary source node map pending", "not_applicable", "required", 60),
    ("M0783-X-FOUNDATION", "trust_boundary", "Forbid closing MA by an axiom declaration or assumption and audit the kernel, classical principles, and transitive dependencies.", "pinned foundation and transitive axiom report pending", "required", "not_applicable", 30),
    ("M0783-X-PROVENANCE", "certificate", "Bind any future terminal body to immutable source, license, exact type, axiom, placeholder, and freshness evidence.", "provenance ledger pending proof and validation phases", "informational", "not_applicable", 40),
    ("M0783-X-READABLE", "documentation", "Produce an independently reviewed reconstruction of the forcing conventions and dense-family obligation.", "readable reconstruction pending", "not_applicable", "not_applicable", 50),
    ("M0783-X-WORKFLOW", "workflow_gate", "Require proof, validation, independent verification, and release receipts before root promotion.", "rev-5.6 proof -> validation -> release workflow", "informational", "not_applicable", 20),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def planned(oid, statement):
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, machine, source, budget in ROWS:
    excluded = machine == "not_applicable" or machine == "informational"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-source-sha256:" + statement_sha if oid in {"M0783-ROOT", "M0783-S-INTERFACE"} else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": source,
        "readable_eligibility": "required",
        "risk_class": "critical" if oid in {"M0783-ROOT", "M0783-L-DENSE-FAMILY", "M0783-X-SOURCE", "M0783-X-FOUNDATION"} else "high",
        "step_budget": budget,
        "exclusion_reason": ("mandatory_layer_not_separate; integration_reviewer_acceptance_pending" if oid in {"M0783-N-NA", "M0783-B-NA", "M0783-C-NA"} else ("non_machine_boundary" if excluded else None)),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0783/ObligationTree.lean#root_of_denseFamilySolver" if oid == "M0783-T-ASSEMBLE" else None,
    })
ids = [row[0] for row in ROWS]
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated Martin's-axiom target and bounded pinned anchor audit; universal introduction, expanded dense-family content, and definitional transport selected without proof-candidate credit.",
    "frozen_against_statement_sha256": statement_sha, "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0783-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility change, or re-fingerprint requires a new registry version and append-only old/new ID delta.",
    "obligations": obligations,
}

checked = {"M0783-S-INTERFACE", "M0783-T-ASSEMBLE"}
nodes = []
for oid, kind, human, formal, machine, source, budget in ROWS:
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0783-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H5", "machine_debt": "M0-L" if oid in checked else ("M3" if oid in {"M0783-ROOT", "M0783-S-INTERFACE"} else "M4"), "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "source-statement-crosswalk.md; primary definition review pending",
        "provenance_id": "anchor-audit.json" if oid in {"M0783-L-DENSE-FAMILY", "M0783-X-FOUNDATION"} else "none",
        "foundation_profile": "Lean dependent type theory; MA must not be introduced as an axiom or assumption for proof credit",
        "tcb_profile": "Lean 4.29.0 + mathlib 8a178386; transitive release audit pending",
        "computation_record": "none; no oracle, solver, or external computation credited", "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the exact formal context and declared proof-requires children.", "inference": human, "output": human, "outgoing_use": "Only declared typed proof or support edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0783/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": ("Kernel-checked conditional interface only; " if oid in checked else "Frozen architecture only; ") + "no proof of Martin's axiom and no foundation extension is supplied.",
        "task_ids": [ITEM, "S56-M-0783-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0783/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-0783 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

def graph(edges):
    out, inc = {x: [] for x in ids}, {x: [] for x in ids}
    for e in edges: out[e["from"]].append(e["edge_id"]); inc[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": out, "in": inc}

proof_pairs = [("M0783-ROOT", "M0783-S-INTERFACE"), ("M0783-ROOT", "M0783-T-ASSEMBLE"), ("M0783-T-ASSEMBLE", "M0783-L-DENSE-FAMILY")]
proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req}]
def simple(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(simple("R", "logical_decomposition", [("M0783-ROOT", "M0783-L-DENSE-FAMILY"), ("M0783-ROOT", "M0783-T-ASSEMBLE")]) + simple("X", "expository_decomposition", [("M0783-ROOT", x) for x in ["M0783-N-NA", "M0783-B-NA", "M0783-C-NA"]])),
    "provenance": graph(simple("V", "provenance_of", [("M0783-X-PROVENANCE", x) for x in ["M0783-L-DENSE-FAMILY", "M0783-T-ASSEMBLE", "M0783-ROOT"]])),
    "evidence": graph(simple("E", "source_map", [("M0783-X-SOURCE", "M0783-ROOT"), ("M0783-X-SOURCE", "M0783-L-DENSE-FAMILY")])),
    "trust": graph(simple("T", "trusts", [(x, "M0783-X-FOUNDATION") for x in ["M0783-ROOT", "M0783-L-DENSE-FAMILY", "M0783-T-ASSEMBLE"]])),
    "documentation": graph(simple("D", "documents", [("M0783-X-READABLE", x) for x in ["M0783-ROOT", "M0783-S-INTERFACE", "M0783-L-DENSE-FAMILY", "M0783-T-ASSEMBLE"]])),
    "workflow": graph(simple("W", "workflow_depends_on", [("M0783-ROOT", x) for x in ["M0783-X-SOURCE", "M0783-X-FOUNDATION", "M0783-X-PROVENANCE", "M0783-X-READABLE", "M0783-X-WORKFLOW"]])),
}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-0783-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": "M0783-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs,
          "closure_boundary": {"root_closed": False, "root_machine_classification": "M4", "theorem_complete": False, "first_open_cut": ["M0783-L-DENSE-FAMILY", "M0783-X-SOURCE", "M0783-X-FOUNDATION", "M0783-X-PROVENANCE", "M0783-X-READABLE", "M0783-X-WORKFLOW"]}}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "provisional" if oid in checked else "open", "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
