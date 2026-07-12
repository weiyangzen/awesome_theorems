#!/usr/bin/env python3
"""Build the frozen THM-M-0468 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0468-OBLIGATION_TREE"
THEOREM = "THM-M-0468"
PREFIX = "M0468"


def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen Ullmo--Zhang equivalence.", "Stage1Instances.THM_M_0468.BogomolovTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze small points, special subvarieties, geometric points, height, and density conventions.", "Stage1Instances.THM_M_0468.{BogomolovData,smallPoints,IsSpecial,DenseSmallPoints}", "The exact statement interface."),
    ("S-DOMAINS", "normalization", "critical", "Relate the semantic carrier to an abelian variety over a number field, geometric subvarieties, and an ample symmetric line bundle.", "planned checked interpretation of BogomolovData", "A source-faithful algebraic-geometric model."),
    ("S-BOUNDARY", "branch", "high", "Cover X=A, zero-dimensional integral X, and every positive epsilon while excluding empty and nonintegral loci.", "planned exact boundary lemmas", "Boundary cases matching the frozen quantifiers."),
    ("S-FOUNDATION", "certificate", "critical", "Fix classical choice, quotients, algebraic closures, TCB, and no-oracle policy.", "planned transitive axiom and trust report", "An accepted trust boundary."),
    ("N-BASECHANGE", "normalization", "critical", "Normalize geometric points and subvarieties after algebraic closure without changing height or specialness.", "planned base-change compatibility package", "A common geometric base for both directions."),
    ("N-HEIGHT", "normalization", "critical", "Normalize the Neron--Tate height attached to L, including nonnegativity, functoriality, and torsion vanishing.", "planned canonical-height package", "The height identities used downstream."),
    ("B-FORWARD", "branch", "critical", "Dense arbitrarily small points imply that X is a torsion translate of an abelian subvariety.", "Stage1Instances.THM_M_0468.DenseSmallPointsImplySpecial", "The forward implication."),
    ("C-GENERIC", "construction", "critical", "Choose a generic sequence of small points whose Galois orbits detect Zariski density.", "planned generic small-point sequence", "A generic small sequence in X."),
    ("L-EQUIDISTRIBUTION", "core_lemma", "critical", "Prove equidistribution of the generic small sequence for the canonical measure on X.", "planned Zhang equidistribution theorem", "Weak convergence to the canonical measure."),
    ("C-DIFFERENCE", "construction", "critical", "Construct a suitable difference morphism on a power of X and control its generic finiteness when X has trivial stabilizer.", "planned difference-map construction", "A comparison morphism with controlled fibers."),
    ("L-MEASURE", "core_lemma", "critical", "Compare pushed-forward canonical measures and derive the tangent/metric degeneracy contradiction.", "planned canonical-measure comparison", "Nontrivial stabilizer or contradiction."),
    ("L-STABILIZER", "core_lemma", "critical", "Pass from the positive-dimensional stabilizer/quotient analysis to a torsion translate classification.", "planned stabilizer descent and induction", "X is special."),
    ("B-CONVERSE", "branch", "critical", "A torsion translate of an abelian subvariety has dense points below every positive height threshold.", "Stage1Instances.THM_M_0468.SpecialImplyDenseSmallPoints", "The converse implication."),
    ("C-TORSION", "construction", "high", "Represent X=t+B and construct its geometric torsion points as translates of torsion points of B.", "planned torsion-translate construction", "A torsion subset of X."),
    ("L-TORSION-HEIGHT", "core_lemma", "high", "Canonical height vanishes on torsion points and respects translation by torsion.", "planned torsion-height theorem", "Every constructed point is epsilon-small."),
    ("L-TORSION-DENSE", "core_lemma", "critical", "Torsion points are Zariski dense in an abelian subvariety over the algebraic closure.", "planned torsion-density theorem", "Density of the constructed small subset."),
    ("T-ASSEMBLE", "transport", "high", "Compose the forward and converse packages into the exact canonical equivalence.", "Stage1Instances.THM_M_0468.root_of_direction_packages", "The exact root conditional on both directions."),
    ("X-SOURCE", "terminal", "high", "Map every material implication and lemma to primary-source theorem/page/assumption/errata records.", "non-machine node-specific source crosswalk", "Human-source coverage without proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, axioms, TCB, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without proof credit."),
]

checked = {"S-DEFINITIONS", "T-ASSEMBLE"}
source_na = {"S-DEFINITIONS", "S-DOMAINS", "S-BOUNDARY", "S-FOUNDATION", "X-PROVENANCE"}
machine_special = {"X-SOURCE": "not_applicable", "X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for short, kind, risk, claim, target, output in rows:
    oid = f"{PREFIX}-{short}"
    fingerprint = ("lean-source:v1:sha256:" + statement_hash if short in {"ROOT", "S-DEFINITIONS"}
                   else "planned:v1:sha256:" + canonical_hash([oid, kind, claim, target, output]))
    machine = machine_special.get(short, "required")
    body = ("local:Stage1_Instances/THM-M-0468/ObligationTree.lean#root_of_direction_packages"
            if short == "T-ASSEMBLE" else None)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if short in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": f"THM-M-0468-{short}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if short in checked else ("M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source_statement_crosswalk.md; node pinpoint pending" if short not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if body else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation or oracle may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact proof_requires children and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0468/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise or root proof is supplied.",
        "task_ids": [ITEM, "S56-M-0468-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0468/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0468 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if short in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if short in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = canonical_hash([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact Ullmo--Zhang statement and bounded anchor audit; forward equidistribution/stabilizer and converse torsion-density routes expanded before closure status was assigned.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(f"{PREFIX}-{x}" for x in checked), "root_machine_debt": "M4"},
    "status_boundary": "Scope and denominators only; neither implication, H0, audit completion, nor theorem completion is claimed.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


def oid(short):
    return f"{PREFIX}-{short}"


requires = {
    "ROOT": ["T-ASSEMBLE"], "T-ASSEMBLE": ["B-FORWARD", "B-CONVERSE"],
    "B-FORWARD": ["N-BASECHANGE", "N-HEIGHT", "C-GENERIC", "L-EQUIDISTRIBUTION", "C-DIFFERENCE", "L-MEASURE", "L-STABILIZER"],
    "B-CONVERSE": ["N-BASECHANGE", "N-HEIGHT", "C-TORSION", "L-TORSION-HEIGHT", "L-TORSION-DENSE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, oid(parent), "proof_requires", oid(child), comp), edge(comp, oid(child), "composes", oid(parent), req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-DEFS", oid("ROOT"), "logical_decomposition", oid("S-DEFINITIONS")), edge("REF-DOMAINS", oid("ROOT"), "logical_decomposition", oid("S-DOMAINS")), edge("REF-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY")), edge("REF-FOUNDATION", oid("ROOT"), "logical_decomposition", oid("S-FOUNDATION"))],
    "provenance": [edge("SRC-FORWARD", oid("B-FORWARD"), "source_map", oid("X-SOURCE")), edge("SRC-CONVERSE", oid("B-CONVERSE"), "source_map", oid("X-SOURCE")), edge("PROV-ROOT", oid("X-PROVENANCE"), "provenance_of", oid("ROOT"))],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", oid("ROOT"), "trusts", oid("S-FOUNDATION")), edge("TRUST-PROV", oid("ROOT"), "trusts", oid("X-PROVENANCE"))],
    "documentation": [edge("DOC-DEFS", oid("S-DEFINITIONS"), "documents", oid("ROOT")), edge("DOC-SOURCE", oid("X-SOURCE"), "documents", oid("B-FORWARD"))],
    "workflow": [edge("FLOW-ASSEMBLE-FORWARD", oid("T-ASSEMBLE"), "workflow_depends_on", oid("B-FORWARD")), edge("FLOW-ASSEMBLE-CONVERSE", oid("T-ASSEMBLE"), "workflow_depends_on", oid("B-CONVERSE")), edge("FLOW-PROV-ASSEMBLE", oid("X-PROVENANCE"), "workflow_depends_on", oid("T-ASSEMBLE"))],
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
    "registry_id": "THM-M-0468-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": oid("ROOT"), "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(oid(x) for x in checked), "root_closed": False, "root_machine_debt": "M4", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [oid("B-FORWARD"), oid("B-CONVERSE")], "composition_certificates": ["Stage1Instances.THM_M_0468.root_of_direction_packages"], "reason": "The final composition is conditional; neither implication package has a proof body."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for obligation in obligations:
    recipes["recipes"].append({"recipe_id": "VAL-" + obligation["obligation_id"], "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0468/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0468 obligation tree"}], "covered_obligation_ids": [obligation["obligation_id"]], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(v) for v in graph_edges.values())} typed edges")
print(denominator)
