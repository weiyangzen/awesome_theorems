#!/usr/bin/env python3
"""Generate the frozen THM-M-0669 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0669-OBLIGATION_TREE"
THEOREM = "THM-M-0669"

ROWS = [
    ("M0669-ROOT", "root", "The exact formula-level quantifier-elimination target over realClosedFieldTheory.", "Stage1.THM_M_0669.TarskiQuantifierEliminationTarget", "critical", "required"),
    ("M0669-S-THEORY", "definition", "Validate the pure-ring complete-theory presentation and its intended real-closed-field scope.", "Stage1.THM_M_0669.realClosedFieldTheory", "critical", "required"),
    ("M0669-C-ATOMIC", "normalization", "Normalize atomic pure-ring formulas to polynomial equalities and inequalities encoded without primitive order.", "planned atomic polynomial normalization", "critical", "required"),
    ("M0669-C-BOOLEAN", "normalization", "Prove quantifier-free formulas are closed under the Boolean connectives used by formula recursion.", "planned IsQF Boolean closure package", "high", "required"),
    ("M0669-E-ONE-VAR", "core_lemma", "Eliminate one existentially bound variable from a quantifier-free formula, uniformly in all remaining free variables.", "planned one-variable elimination theorem", "critical", "required"),
    ("M0669-E-SIGN", "reduction", "Reduce one-variable elimination to realizability of finite polynomial sign conditions.", "planned sign-condition reduction", "critical", "required"),
    ("M0669-E-ROOTS", "bridge", "Classify roots, order cells, and signs for a finite family of univariate polynomials over a real closed field.", "planned real-closed polynomial root/sign theorem", "critical", "required"),
    ("M0669-E-PROJECT", "construction", "Construct parameter-only projection conditions whose truth is equivalent to sign-condition realizability.", "planned projection-condition construction", "critical", "required"),
    ("M0669-E-SEMANTICS", "transport", "Transport the algebraic projection result to mathlib BoundedFormula semantics over the selected theory.", "planned algebra-to-semantics bridge", "critical", "required"),
    ("M0669-I-FORMULA", "induction", "Induct over formulas, using one-variable elimination at quantifiers and closure at Boolean nodes.", "planned formula recursion theorem", "critical", "required"),
    ("M0669-T-ASSEMBLE", "transport", "Assemble the recursion output with identical free-variable type into the exact canonical target.", "Stage1.THM_M_0669.root_of_elimination", "high", "required"),
    ("M0669-X-SOURCE", "source_boundary", "Crosswalk every algebraic and logical inference to an inspected primary proof and errata record.", "primary source node map pending", "critical", "not_applicable"),
    ("M0669-X-FOUNDATION", "certificate", "Audit classical logic, choice, noncomputability, import closure, axioms, and terminal bodies.", "planned foundation and trust report", "critical", "required"),
    ("M0669-X-PROVENANCE", "certificate", "Record terminal proof bodies, immutable revisions, licenses, receipts, and revocations.", "planned provenance ledger", "critical", "informational"),
]

PROOF_REQUIRES = [
    ("M0669-ROOT", "M0669-T-ASSEMBLE"),
    ("M0669-T-ASSEMBLE", "M0669-I-FORMULA"),
    ("M0669-I-FORMULA", "M0669-C-ATOMIC"),
    ("M0669-I-FORMULA", "M0669-C-BOOLEAN"),
    ("M0669-I-FORMULA", "M0669-E-ONE-VAR"),
    ("M0669-E-ONE-VAR", "M0669-E-SIGN"),
    ("M0669-E-SIGN", "M0669-E-ROOTS"),
    ("M0669-E-SIGN", "M0669-E-PROJECT"),
    ("M0669-E-PROJECT", "M0669-E-SEMANTICS"),
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
        "statement_fingerprint": ("lean-source-sha256:" + statement_sha) if oid in {"M0669-ROOT", "M0669-S-THEORY"} else planned(oid, human),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "required" if oid not in {"M0669-S-THEORY", "M0669-X-FOUNDATION", "M0669-X-PROVENANCE"} else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if oid == "M0669-X-SOURCE" else ("release_overlay_no_proof_credit" if oid == "M0669-X-PROVENANCE" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0669/ObligationTree.lean#root_of_elimination" if oid == "M0669-T-ASSEMBLE" else None,
    })
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
ids = [r[0] for r in ROWS]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus bounded anchor audit; algebraic one-variable elimination and formula-recursion architecture selected before proof closure observation.",
    "frozen_against_statement_sha256": statement_sha, "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0669-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0669-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for oid, kind, human, formal, risk, machine in ROWS:
    provisional = oid in {"M0669-S-THEORY", "M0669-T-ASSEMBLE"}
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0669-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H1", "machine_debt": "M0-L" if oid == "M0669-T-ASSEMBLE" else ("M3" if oid in {"M0669-ROOT", "M0669-S-THEORY"} else "M4"),
        "readability_debt": "R3", "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib/noncomputable-complete-theory; classical-and-choice-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; no external computation may close this node without a replayable checked certificate",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only declared proof-requires children and the exact formal context.", "inference": human, "output": human, "outgoing_use": "Only declared typed parent or non-proof support edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0669/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen interface only; no unlisted premise or root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0669-PROOF"], "owned_sources": [], "owner": "THM-M-0669 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if provisional else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if provisional else "open"},
    })

def graph(edge_rows):
    out = {i: [] for i in ids}; incoming = {i: [] for i in ids}
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
    "refinement": graph(edges("R", "logical_decomposition", [("M0669-ROOT", "M0669-S-THEORY"), ("M0669-E-ONE-VAR", "M0669-E-ROOTS"), ("M0669-I-FORMULA", "M0669-E-SEMANTICS")])),
    "provenance": graph(edges("V", "provenance_of", [("M0669-X-PROVENANCE", x) for x in ids if x != "M0669-X-PROVENANCE"])),
    "evidence": graph(edges("E", "source_map", [("M0669-X-SOURCE", x) for x in ["M0669-C-ATOMIC", "M0669-E-ONE-VAR", "M0669-E-SIGN", "M0669-E-ROOTS", "M0669-E-PROJECT", "M0669-I-FORMULA"]])),
    "trust": graph(edges("T", "trusts", [(x, "M0669-X-FOUNDATION") for x in ["M0669-ROOT", "M0669-E-ONE-VAR", "M0669-E-ROOTS", "M0669-T-ASSEMBLE"]])),
    "documentation": graph(edges("D", "documents", [("M0669-X-SOURCE", "M0669-ROOT"), ("M0669-X-PROVENANCE", "M0669-ROOT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M0669-ROOT", "M0669-X-SOURCE"), ("M0669-ROOT", "M0669-X-FOUNDATION"), ("M0669-ROOT", "M0669-X-PROVENANCE")])),
}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
          "registry_id": "THM-M-0669-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
          "root_node_id": "M0669-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
          "nodes": nodes, "graphs": graphs,
          "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "theorem_complete": False, "first_open_cut": ["M0669-C-ATOMIC", "M0669-C-BOOLEAN", "M0669-E-ONE-VAR", "M0669-X-SOURCE", "M0669-X-FOUNDATION"]}}
recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "provisional" if oid in {"M0669-S-THEORY", "M0669-T-ASSEMBLE"} else "open", "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}
for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)]:
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(denominator)
