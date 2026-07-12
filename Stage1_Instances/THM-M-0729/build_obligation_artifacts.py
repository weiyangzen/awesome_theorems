#!/usr/bin/env python3
"""Generate the frozen THM-M-0729 obligation registry and graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0729-OBLIGATION_TREE"
THEOREM = "THM-M-0729"
PFX = "M0729-"

# id, kind, human statement, formal target, risk, machine eligibility, source eligibility, budget
ROWS = [
    ("M0729-ROOT", "root", "Binary verifier-based NP equals the frozen nonadaptive perfect-completeness PCP class.", "Stage1Instances.THM_M_0729.PCPTheorem", "critical", "required", "required", 20),
    ("M0729-S-ENCODING", "definition", "Audit binary words, prefix-free machine encodings, verifier cost, proof-oracle access, and finite-cardinality soundness.", "Stage1Instances.THM_M_0729.{InNP,Checker,InPCPLogConst,HasSoundnessHalf}", "critical", "required", "not_applicable", 80),
    ("M0729-S-BOUNDARY", "branch", "Cover zero randomness, empty query lists, empty input, and inputs below the asymptotic randomness threshold.", "planned exact boundary package", "high", "required", "required", 70),
    ("M0729-D-NP-PCP", "core_lemma", "For every binary language, transform an InNP verifier into an InPCPLogConst checker.", "forall L : Language, InNP L -> InPCPLogConst L", "critical", "required", "required", 100),
    ("M0729-N-CONSTRAINT", "reduction", "Normalize an accepting polynomial-time verifier computation to a bounded local constraint system with uniform encodings.", "planned verifier-to-constraint reduction", "critical", "required", "required", 100),
    ("M0729-L-ROBUST", "core_lemma", "Prove a constant-gap robust soundness theorem for the normalized constraint system.", "planned gap/robustness theorem", "critical", "required", "required", 100),
    ("M0729-L-COMPOSE", "core_lemma", "Compose and degree-reduce the robust verifier while preserving perfect completeness and constant soundness.", "planned PCP composition theorem", "critical", "required", "required", 100),
    ("M0729-L-RANDOM", "computation", "Derive the O(log n) random-bit bound, including encoding sizes and the frozen threshold convention.", "planned logarithmic-randomness bound", "high", "required", "required", 70),
    ("M0729-L-QUERY", "computation", "Derive one uniform O(1) bound for every well-sized nonadaptive query list.", "planned constant-query bound", "high", "required", "required", 60),
    ("M0729-L-PERFECT", "construction", "Construct the proof oracle for yes instances and establish acceptance for every random string.", "planned perfect-completeness construction", "critical", "required", "required", 80),
    ("M0729-L-SOUND", "core_lemma", "Translate the gap theorem to the exact finite-cardinality soundness-one-half inequality.", "planned soundness transport", "critical", "required", "required", 80),
    ("M0729-D-PCP-NP", "core_lemma", "For every binary language, transform an InPCPLogConst checker into an InNP verifier.", "forall L : Language, InPCPLogConst L -> InNP L", "critical", "required", "required", 100),
    ("M0729-C-CERTIFICATE", "construction", "Encode all proof-oracle bits reachable over the finite random space as one polynomially bounded certificate.", "planned finite oracle-certificate construction", "high", "required", "required", 80),
    ("M0729-L-ENUMERATE", "computation", "Build a deterministic polynomial-time verifier that enumerates every random string and checks all induced queries.", "planned exhaustive verifier and cost proof", "critical", "required", "required", 100),
    ("M0729-B-SHORT", "branch", "Handle the finitely many below-threshold inputs without assuming the asymptotic bound at those lengths.", "planned finite-short-input branch", "high", "required", "required", 70),
    ("M0729-T-ASSEMBLE", "transport", "Combine both inclusions into ExpandedTarget and transport it to the exact set equality PCPTheorem.", "Stage1Instances.THM_M_0729.root_of_directionalPackage", "high", "required", "required", 25),
    ("M0729-X-SOURCE", "source_boundary", "Crosswalk every central PCP reduction and parameter convention to an inspected primary proof and errata record.", "primary source node map pending", "critical", "not_applicable", "required", 60),
    ("M0729-X-FOUNDATION", "certificate", "Audit classical choice, finite enumeration, polynomial-time closure, kernel axioms, and transitive TCB.", "planned trust and axiom report", "critical", "required", "not_applicable", 80),
    ("M0729-X-PROVENANCE", "certificate", "Record terminal proof bodies, immutable revisions, licenses, receipts, and revocations.", "planned provenance ledger", "critical", "informational", "not_applicable", 40),
]

PROOF_REQUIRES = [
    ("M0729-ROOT", "M0729-T-ASSEMBLE"),
    ("M0729-T-ASSEMBLE", "M0729-D-NP-PCP"),
    ("M0729-T-ASSEMBLE", "M0729-D-PCP-NP"),
    ("M0729-D-NP-PCP", "M0729-N-CONSTRAINT"),
    ("M0729-D-NP-PCP", "M0729-L-COMPOSE"),
    ("M0729-D-NP-PCP", "M0729-L-RANDOM"),
    ("M0729-D-NP-PCP", "M0729-L-QUERY"),
    ("M0729-D-NP-PCP", "M0729-L-PERFECT"),
    ("M0729-D-NP-PCP", "M0729-L-SOUND"),
    ("M0729-N-CONSTRAINT", "M0729-S-ENCODING"),
    ("M0729-L-COMPOSE", "M0729-L-ROBUST"),
    ("M0729-L-PERFECT", "M0729-S-BOUNDARY"),
    ("M0729-L-SOUND", "M0729-S-BOUNDARY"),
    ("M0729-D-PCP-NP", "M0729-C-CERTIFICATE"),
    ("M0729-D-PCP-NP", "M0729-L-ENUMERATE"),
    ("M0729-D-PCP-NP", "M0729-B-SHORT"),
    ("M0729-C-CERTIFICATE", "M0729-S-ENCODING"),
    ("M0729-L-ENUMERATE", "M0729-L-RANDOM"),
    ("M0729-B-SHORT", "M0729-S-BOUNDARY"),
]

def sha(data): return hashlib.sha256(data).hexdigest()
def planned(oid, text): return "planned:v1:sha256:" + sha((oid + "\0" + text).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, risk, machine, source, budget in ROWS:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-expression-sha256:2a3d6c881d9d74079ecc6a7733b1b53a7500b85b9a4d075159cf8cd6cce7bbc5" if oid == "M0729-ROOT" else ("lean-source-sha256:" + statement_sha if oid == "M0729-S-ENCODING" else planned(oid, human)),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": source, "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if oid == "M0729-X-SOURCE" else ("release_overlay_no_proof_credit" if oid == "M0729-X-PROVENANCE" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0729/ObligationTree.lean#root_of_directionalPackage" if oid == "M0729-T-ASSEMBLE" else None,
    })
ids = [r[0] for r in ROWS]
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated binary PCP statement and bounded anchor audit; two-inclusion architecture frozen before any root proof discovery.",
    "frozen_against_statement_sha256": statement_sha,
    "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0729-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0729-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for oid, kind, human, formal, risk, machine, source, budget in ROWS:
    provisional = oid in {"M0729-S-ENCODING", "M0729-S-BOUNDARY", "M0729-T-ASSEMBLE"}
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PFX), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H3", "machine_debt": "M0-L" if oid == "M0729-T-ASSEMBLE" else ("M3" if provisional or oid == "M0729-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md; primary-proof-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M0729-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib; classical/choice and PCP reduction audit pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure pending",
        "computation_record": "finite enumeration and polynomial cost certificate pending" if kind == "computation" else "none",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Exact formal context plus only proof_requires children.", "inference": human, "output": human, "outgoing_use": "Only typed parent composition edges may consume this conclusion for proof credit."},
        "public_readable_target": "Stage1_Instances/THM-M-0729/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen interface only; no unlisted premise and no substantive PCP closure is supplied.",
        "task_ids": [ITEM, "S56-M-0729-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0729/ObligationTree.lean"] if oid == "M0729-T-ASSEMBLE" else [],
        "owner": "THM-M-0729 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if provisional else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry", "source map", "toolchain"], "revocation_state": "provisional" if provisional else "open"},
    })

def graph(edge_rows):
    out = {x: [] for x in ids}; incoming = {x: [] for x in ids}
    for edge in edge_rows:
        out[edge["from"]].append(edge["edge_id"]); incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edge_rows, "out": out, "in": incoming}

proof_edges = []
for i, (parent, child) in enumerate(PROOF_REQUIRES, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req}]
def edges(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "logical_decomposition", [("M0729-ROOT", "M0729-S-ENCODING"), ("M0729-D-NP-PCP", "M0729-S-BOUNDARY"), ("M0729-D-PCP-NP", "M0729-S-BOUNDARY")])),
    "provenance": graph(edges("V", "provenance_of", [("M0729-X-PROVENANCE", x) for x in ids if x != "M0729-X-PROVENANCE"])),
    "evidence": graph(edges("E", "source_map", [("M0729-X-SOURCE", x) for x in ids if x.startswith("M0729-L-") or x.startswith("M0729-N-")])),
    "trust": graph(edges("T", "trusts", [(x, "M0729-X-FOUNDATION") for x in ["M0729-ROOT", "M0729-D-NP-PCP", "M0729-D-PCP-NP", "M0729-T-ASSEMBLE"]])),
    "documentation": graph(edges("D", "documents", [("M0729-X-SOURCE", "M0729-ROOT"), ("M0729-X-PROVENANCE", "M0729-ROOT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M0729-ROOT", "M0729-X-SOURCE"), ("M0729-ROOT", "M0729-X-FOUNDATION"), ("M0729-ROOT", "M0729-X-PROVENANCE")])),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0729-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0729-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "theorem_complete": False, "first_open_cut": ["M0729-D-NP-PCP", "M0729-D-PCP-NP", "M0729-X-SOURCE", "M0729-X-FOUNDATION"]},
}
recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "provisional" if oid in {"M0729-S-ENCODING", "M0729-S-BOUNDARY", "M0729-T-ASSEMBLE"} else "open", "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}
for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)]:
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(denominator)
