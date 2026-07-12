#!/usr/bin/env python3
"""Deterministically build the THM-M-1140 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEOREM = "THM-M-1140"
ITEM = "S56-M-1140-OBLIGATION_TREE"

ROWS = [
    ("ROOT", "root", "Exact frozen strong maximum principle for real harmonic functions.", "Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple", "canonical proposition", "critical", "required", "required"),
    ("S-DEFINITIONS", "definition", "Fix Euclidean ambient space, harmonic-on-neighborhood, topology, connectedness, and ordered maximum conventions.", "Types and predicates elaborated by Statement.lean", "exact typed vocabulary", "normal", "required", "not_applicable"),
    ("S-DOMAIN", "definition", "Preserve every ordered binder and hypothesis, including explicit nonemptiness and the dimension-zero case.", "Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple", "exact quantified context", "high", "required", "required"),
    ("S-BOUNDARY", "branch", "Account for dimension zero, singleton behavior, and the impossibility of deleting openness, connectedness, or harmonicity.", "Planned boundary and mutation ledger", "legal degenerate cases", "high", "required", "required"),
    ("S-FOUNDATION", "certificate", "Audit classical topology, imports, axioms, TCB closure, and the no-oracle policy.", "Planned transitive trust report", "release trust boundary", "critical", "required", "not_applicable"),
    ("N-MAX-LEVEL", "normalization", "Normalize the proof around the relative maximum-level set {x in Omega | u x = u x0}.", "Planned level-set definition and membership lemmas", "nonempty maximum-level set", "normal", "required", "required"),
    ("L-MEAN-VALUE", "bridge", "Derive that an interior maximizer of a harmonic function is locally constant, using an arbitrary-dimensional mean-value or equivalent rigidity theorem.", "Stage1Instances.THM_M_1140.InteriorLocalRigidity", "a neighborhood on which u equals its maximum value", "critical", "required", "required"),
    ("L-CONTINUITY", "bridge", "Obtain continuity on Omega from HarmonicOnNhd without changing the harmonicity predicate.", "InnerProductSpace.HarmonicOnNhd.continuousOn", "ContinuousOn u Omega", "normal", "required", "not_applicable"),
    ("L-LEVEL-CLOSED", "core_lemma", "Use continuity to prove the maximum-level set is relatively closed in Omega.", "Planned relative-closed level-set lemma", "relative closedness", "high", "required", "required"),
    ("L-LEVEL-OPEN", "core_lemma", "Apply local rigidity at every maximum-level point to prove the level set relatively open.", "Planned relative-open level-set lemma", "relative openness", "critical", "required", "required"),
    ("L-CONNECTED", "core_lemma", "Use connectedness and nonemptiness to show a nonempty relatively clopen level set equals Omega.", "Stage1Instances.THM_M_1140.ConnectedLevelPropagation", "all points lie at the maximum level", "critical", "required", "required"),
    ("T-LOCAL-PACKAGE", "terminal", "Package the arbitrary-dimensional local harmonic rigidity conclusion with its exact hypotheses.", "Stage1Instances.THM_M_1140.InteriorLocalRigidity", "local-rigidity package", "critical", "required", "required"),
    ("T-PROPAGATION-PACKAGE", "terminal", "Package the continuity and connected level-set propagation argument.", "Stage1Instances.THM_M_1140.ConnectedLevelPropagation", "connected-propagation package", "critical", "required", "required"),
    ("T-ASSEMBLE", "transport", "Consume both packages and produce the exact public root without an extra premise.", "Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple_of_packages", "exact canonical proposition", "high", "required", "not_applicable"),
    ("X-SOURCE", "terminal", "Map every material analytic and topological step to a reviewed primary source and errata record.", "Node-specific human-source crosswalk, pending", "human provenance only", "high", "not_applicable", "required"),
    ("X-PROVENANCE", "certificate", "Inventory terminal bodies, imports, axioms, placeholders, immutable revisions, and replay evidence.", "Machine-derived provenance closure, pending", "formal provenance only", "critical", "informational", "not_applicable"),
]

CHILDREN = {
    "ROOT": ["T-ASSEMBLE"],
    "T-ASSEMBLE": ["T-LOCAL-PACKAGE", "T-PROPAGATION-PACKAGE", "L-CONTINUITY"],
    "T-LOCAL-PACKAGE": ["L-MEAN-VALUE"],
    "T-PROPAGATION-PACKAGE": ["N-MAX-LEVEL", "L-LEVEL-CLOSED", "L-LEVEL-OPEN", "L-CONNECTED"],
    "L-LEVEL-CLOSED": ["L-CONTINUITY"],
    "L-LEVEL-OPEN": ["L-MEAN-VALUE"],
}

def oid(short):
    return "M1140-" + short

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def make_graph(edges, ids):
    return {"edges": edges, "out": {i: [e["edge_id"] for e in edges if e["from"] == i] for i in ids}, "in": {i: [e["edge_id"] for e in edges if e["to"] == i] for i in ids}}

def simple_edge(prefix, number, source, kind, target):
    return {"edge_id": f"M1140-{prefix}-{number:02d}", "from": oid(source), "type": kind, "to": oid(target)}

def main():
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    checked = {"S-DEFINITIONS", "S-DOMAIN", "L-CONTINUITY", "T-ASSEMBLE"}
    obligations = []
    nodes = []
    for short, kind, human, formal, output, risk, machine, source in ROWS:
        body = "local:Stage1_Instances/THM-M-1140/ObligationTree.lean#harmonicStrongMaximumPrinciple_of_packages" if short == "T-ASSEMBLE" else None
        obligations.append({
            "obligation_id": oid(short),
            "statement_fingerprint": ("lean-source:v1:sha256:" + statement_hash) if short in {"ROOT", "S-DEFINITIONS", "S-DOMAIN"} else "planned:v1:sha256:" + digest([short, kind, human, formal, output]),
            "kind": kind, "root_relevant": True, "machine_eligibility": machine,
            "human_source_eligibility": source, "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("release_provenance_overlay_no_proof_credit" if machine == "informational" else None),
            "terminal_proof_body_id": body,
        })
        is_checked = short in checked
        nodes.append({
            "node_id": f"{THEOREM}-{short}", "obligation_id": oid(short), "kind": kind,
            "human_statement": human, "formal_target": formal, "output": output,
            "human_debt": "H2", "machine_debt": "M0-L" if is_checked else ("M3" if short == "ROOT" else "M4"), "readability_debt": "R3",
            "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if source == "required" else "not-applicable",
            "provenance_id": "local-conditional-composition" if body else ("anchor-audit-v1" if short == "X-PROVENANCE" else "none"),
            "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
            "computation_record": "none; no numerical computation or oracle receives proof credit", "step_budget": 100 if risk == "critical" else 40,
            "semantic_step_ledger": {"premises": ", ".join(oid(c) for c in CHILDREN.get(short, [])) or "Exact frozen formal context", "inference": human, "output": output, "outgoing_use": "Only a declared typed edge may consume this output."},
            "public_readable_target": f"Stage1_Instances/THM-M-1140/obligation-tree.md#{oid(short).lower()}", "validation_spec_id": "VAL-" + oid(short),
            "status_boundary": "Frozen architecture or checked conditional composition only; no open analytic premise is credited.",
            "task_ids": [ITEM, "S56-M-1140-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1140/ObligationTree.lean"] if body else [],
            "owner": "THM-M-1140 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if is_checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if is_checked else "open"},
        })
    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    denominator = digest([{key: row[key] for key in fields} for row in obligations])
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
        "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact elaborated statement and bounded anchor audit; local-rigidity and connected-propagation architecture frozen before proof execution.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash, "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
        "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [oid("X-PROVENANCE")]},
        "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.", "obligations": obligations, "append_only_delta": [],
        "status_observed_after_freeze": {"closed_obligations": sorted(oid(s) for s in checked), "root_machine_debt": "M3"},
        "status_boundary": "Frozen denominators only; no local rigidity proof, source acceptance, root closure, or theorem completion.",
    }
    proof = []
    number = 1
    for parent, children in CHILDREN.items():
        for child in children:
            req, comp = f"M1140-PROOF-{number:02d}R", f"M1140-PROOF-{number:02d}C"
            proof += [{"edge_id": req, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": comp}, {"edge_id": comp, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": req}]
            number += 1
    refinement = [simple_edge("REFINE", i + 1, "ROOT", "logical_decomposition", s) for i, s in enumerate(["S-DEFINITIONS", "S-DOMAIN", "S-BOUNDARY", "S-FOUNDATION"])]
    provenance = [simple_edge("PROV", 1, "L-MEAN-VALUE", "source_map", "X-SOURCE"), simple_edge("PROV", 2, "X-PROVENANCE", "provenance_of", "T-ASSEMBLE")]
    evidence = [simple_edge("EVID", 1, "X-PROVENANCE", "evidence_for", "T-ASSEMBLE")]
    trust = [simple_edge("TRUST", 1, "ROOT", "trusts", "S-FOUNDATION"), simple_edge("TRUST", 2, "ROOT", "trusts", "X-PROVENANCE")]
    documentation = [simple_edge("DOC", 1, "X-SOURCE", "documents", "L-MEAN-VALUE"), simple_edge("DOC", 2, "X-PROVENANCE", "documents", "ROOT")]
    workflow = [simple_edge("FLOW", 1, "T-ASSEMBLE", "workflow_depends_on", "T-LOCAL-PACKAGE"), simple_edge("FLOW", 2, "T-ASSEMBLE", "workflow_depends_on", "T-PROPAGATION-PACKAGE"), simple_edge("FLOW", 3, "X-PROVENANCE", "workflow_depends_on", "T-ASSEMBLE")]
    graphs = {name: make_graph(edges, ids) for name, edges in {"proof": proof, "refinement": refinement, "provenance": provenance, "evidence": evidence, "trust": trust, "documentation": documentation, "workflow": workflow}.items()}
    bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-1140-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": oid("ROOT"), "edge_direction": "proof_requires is parent to child; composes is child to parent.", "nodes": nodes, "graphs": graphs,
        "closure_boundary": {"closed_obligations": sorted(oid(s) for s in checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [oid("T-LOCAL-PACKAGE"), oid("T-PROPAGATION-PACKAGE")], "composition_certificates": ["Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple_of_packages"], "reason": "The checked theorem is conditional; both substantive packages remain open."}}
    recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid(short), "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1140/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1140 obligation tree"}], "covered_obligation_ids": [oid(short)], "covered_declarations": [formal] if formal.startswith("Stage1Instances.") else []} for short, _, _, formal, _, _, _, _ in ROWS], "status_boundary": "Structural validation and conditional composition only; no analytic package closure."}
    for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    print(f"wrote {len(obligations)} obligations; denominator sha256 {denominator}")

if __name__ == "__main__":
    main()
