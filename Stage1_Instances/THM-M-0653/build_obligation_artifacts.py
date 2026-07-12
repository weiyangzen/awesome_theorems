#!/usr/bin/env python3
"""Generate the frozen THM-M-0653 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0653-OBLIGATION_TREE"
THEOREM = "THM-M-0653"

ROWS = [
    ("M0653-ROOT", "root", "The exact one-new-relation Beth equivalence.", "Stage1.THM_M_0653.BethDefinabilityTarget", "critical", "required"),
    ("M0653-S-ENCODING", "definition", "Audit the one-symbol language sum, reduct equality, nullary case, and parameter-free formula interface.", "Stage1.THM_M_0653.{OneRel,newRel,SameReduct,ImplicitlyDefines,ExplicitlyDefines}", "critical", "required"),
    ("M0653-D-CONVERSE", "lemma", "Derive implicit uniqueness from one uniform old-language definition.", "Stage1.THM_M_0653.ExplicitToImplicit", "high", "required"),
    ("M0653-D-BETH", "core_lemma", "Derive a uniform explicit definition from semantic implicit uniqueness.", "Stage1.THM_M_0653.ImplicitToExplicit", "critical", "required"),
    ("M0653-C-TWO-COPIES", "construction", "Construct two disjoint copies of the distinguished relation over one base language.", "planned exact two-copy expanded-language construction", "critical", "required"),
    ("M0653-L-UNSAT", "reduction", "Convert implicit uniqueness into inconsistency of T in both copies plus a tuple witnessing disagreement.", "planned semantic inconsistency lemma", "critical", "required"),
    ("M0653-L-COMPACT", "bridge", "Reduce the inconsistent theory pair to finite fragments without changing free-variable scope.", "planned compactness bridge", "critical", "required"),
    ("M0653-L-INTERPOLATE", "bridge", "Apply a source-faithful Craig interpolation theorem to the finite two-copy consequence.", "planned Craig interpolation bridge", "critical", "required"),
    ("M0653-L-VOCABULARY", "normalization", "Show the interpolant uses only the base-language vocabulary and the intended tuple variables.", "planned vocabulary-intersection lemma", "critical", "required"),
    ("M0653-T-FORMULA", "transport", "Transport the interpolant to an L.Formula (Fin n) and prove uniform realization equivalence.", "planned formula/reduct transport", "critical", "required"),
    ("M0653-T-ASSEMBLE", "transport", "Compose both directions into the exact canonical Iff.", "Stage1.THM_M_0653.root_of_directions", "high", "required"),
    ("M0653-X-SOURCE", "source_boundary", "Crosswalk every nontrivial inference to an inspected primary proof and errata record.", "primary source node map pending", "critical", "not_applicable"),
    ("M0653-X-FOUNDATION", "certificate", "Audit classical logic, compactness/interpolation axioms, TCB, and terminal proof provenance.", "planned trust and axiom report", "critical", "required"),
    ("M0653-X-PROVENANCE", "certificate", "Record terminal proof bodies, immutable revisions, licenses, receipts, and revocations.", "planned provenance ledger", "critical", "informational"),
]

PROOF_REQUIRES = [
    ("M0653-ROOT", "M0653-T-ASSEMBLE"),
    ("M0653-T-ASSEMBLE", "M0653-D-CONVERSE"),
    ("M0653-T-ASSEMBLE", "M0653-D-BETH"),
    ("M0653-D-BETH", "M0653-C-TWO-COPIES"),
    ("M0653-D-BETH", "M0653-L-UNSAT"),
    ("M0653-L-UNSAT", "M0653-L-COMPACT"),
    ("M0653-L-COMPACT", "M0653-L-INTERPOLATE"),
    ("M0653-L-INTERPOLATE", "M0653-L-VOCABULARY"),
    ("M0653-L-VOCABULARY", "M0653-T-FORMULA"),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def planned(oid, statement):
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, risk, machine in ROWS:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": ("lean-source-sha256:" + statement_sha) if oid in {"M0653-ROOT", "M0653-S-ENCODING"} else planned(oid, human),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "required" if oid not in {"M0653-S-ENCODING", "M0653-X-FOUNDATION", "M0653-X-PROVENANCE"} else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if oid == "M0653-X-SOURCE" else ("release_overlay_no_proof_credit" if oid == "M0653-X-PROVENANCE" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0653/ObligationTree.lean#root_of_directions" if oid == "M0653-T-ASSEMBLE" else None,
    })
fields = tuple(obligations[0])
denominator = sha(json.dumps([{k: r[k] for k in fields} for r in obligations], sort_keys=True, separators=(",", ":")).encode())
ids = [r[0] for r in ROWS]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus bounded anchor audit; two-copy Craig-interpolation architecture selected before proof closure observation.",
    "frozen_against_statement_sha256": statement_sha, "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0653-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0653-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for oid, kind, human, formal, risk, machine in ROWS:
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0653-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H2", "machine_debt": "M0-L" if oid == "M0653-T-ASSEMBLE" else ("M3" if oid in {"M0653-ROOT", "M0653-S-ENCODING"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib-classical/compactness-and-interpolation-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only declared proof-requires children and the exact formal context.", "inference": human, "output": human, "outgoing_use": "Only declared typed parent or non-proof support edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0653/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen interface only; no unlisted premise or root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0653-PROOF"], "owned_sources": [], "owner": "THM-M-0653 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in {"M0653-S-ENCODING", "M0653-T-ASSEMBLE"} else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in {"M0653-S-ENCODING", "M0653-T-ASSEMBLE"} else "open"},
    })

def graph(edges):
    out = {i: [] for i in ids}; incoming = {i: [] for i in ids}
    for e in edges: out[e["from"]].append(e["edge_id"]); incoming[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_edges = []
for i, (parent, child) in enumerate(PROOF_REQUIRES, 1):
    a, b = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": a, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": b}, {"edge_id": b, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": a}]

def edges(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "logical_decomposition", [("M0653-ROOT", "M0653-S-ENCODING"), ("M0653-D-BETH", "M0653-L-INTERPOLATE"), ("M0653-D-BETH", "M0653-T-FORMULA")])),
    "provenance": graph(edges("V", "provenance_of", [("M0653-X-PROVENANCE", x) for x in ids if x != "M0653-X-PROVENANCE"])),
    "evidence": graph(edges("E", "source_map", [("M0653-X-SOURCE", x) for x in ["M0653-D-BETH", "M0653-L-UNSAT", "M0653-L-COMPACT", "M0653-L-INTERPOLATE", "M0653-L-VOCABULARY", "M0653-T-FORMULA"]])),
    "trust": graph(edges("T", "trusts", [(x, "M0653-X-FOUNDATION") for x in ["M0653-ROOT", "M0653-D-BETH", "M0653-D-CONVERSE", "M0653-T-ASSEMBLE"]])),
    "documentation": graph(edges("D", "documents", [("M0653-X-SOURCE", "M0653-ROOT"), ("M0653-X-PROVENANCE", "M0653-ROOT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M0653-ROOT", "M0653-X-SOURCE"), ("M0653-ROOT", "M0653-X-FOUNDATION"), ("M0653-ROOT", "M0653-X-PROVENANCE")])),
}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
          "registry_id": "THM-M-0653-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
          "root_node_id": "M0653-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
          "nodes": nodes, "graphs": graphs,
          "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "theorem_complete": False, "first_open_cut": ["M0653-D-CONVERSE", "M0653-C-TWO-COPIES", "M0653-L-UNSAT", "M0653-X-SOURCE", "M0653-X-FOUNDATION"]}}
recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "open" if oid not in {"M0653-S-ENCODING", "M0653-T-ASSEMBLE"} else "provisional", "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}
for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)]:
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(denominator)
