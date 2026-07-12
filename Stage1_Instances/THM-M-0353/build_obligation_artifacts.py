#!/usr/bin/env python3
"""Generate the frozen THM-M-0353 registry and typed graph bundle."""
import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent
ids = [
    "M0353-ROOT", "M0353-T-ASSEMBLE", "M0353-P-MEMLP", "M0353-P-BASIS",
    "M0353-C-LP-VECTORS", "M0353-L-ORTHONORMAL", "M0353-L-DENSE",
    "M0353-C-HILBERT-BASIS", "M0353-L-GAUSSIAN-ORTH",
    "M0353-L-POLY-DENSE", "M0353-T-MEASURE", "M0353-S-NORMALIZATION",
    "M0353-X-HERMITE-POLY", "M0353-X-SOURCE", "M0353-X-TRUST",
    "M0353-X-PROVENANCE",
]
desc = {
    "M0353-ROOT": ("root", "Exact Hermite completeness target", "Stage1Instances.THM_M_0353.HermiteCompletenessTarget", "M3", 20),
    "M0353-T-ASSEMBLE": ("terminal", "Compose integrability and basis packages", "Stage1Instances.THM_M_0353.root_of_hermite_packages", "M0-L", 10),
    "M0353-P-MEMLP": ("lemma", "Prove every normalized Hermite function is in complex L2(volume)", "Stage1Instances.THM_M_0353.HermiteMemLpPackage", "M4", 70),
    "M0353-P-BASIS": ("construction", "Produce the exact Nat-indexed complex L2 Hilbert basis with a.e. representatives", "Stage1Instances.THM_M_0353.HermiteBasisPackage", "M4", 70),
    "M0353-C-LP-VECTORS": ("construction", "Construct L2 quotient vectors from the literal Hermite functions", "planned exact Lp construction signature", "M4", 60),
    "M0353-L-ORTHONORMAL": ("core_lemma", "Prove orthonormality of all constructed Hermite L2 vectors", "planned exact Orthonormal signature", "M4", 100),
    "M0353-L-DENSE": ("core_lemma", "Prove the closed span of the Hermite vectors is all complex L2(volume)", "planned exact dense-span signature", "M4", 100),
    "M0353-C-HILBERT-BASIS": ("construction", "Package the orthonormal dense family as a HilbertBasis without changing representatives", "planned exact HilbertBasis construction signature", "M4", 60),
    "M0353-L-GAUSSIAN-ORTH": ("core_lemma", "Derive Hermite-function inner products from Gaussian polynomial orthogonality", "planned exact inner-product identity", "M4", 100),
    "M0353-L-POLY-DENSE": ("core_lemma", "Establish density via the Gaussian-polynomial completeness route", "planned exact density transport theorem", "M4", 100),
    "M0353-T-MEASURE": ("transport", "Check the Gaussian weighted-space to Lebesgue Hermite-function isometry and complexification", "planned exact isometry and density transport", "M4", 100),
    "M0353-S-NORMALIZATION": ("normalization", "Preserve probabilists' polynomial scaling, constants, index zero, scalars, and volume", "Statement.lean normalization boundary", "M0-L", 40),
    "M0353-X-HERMITE-POLY": ("bridge", "Audit and use the pinned mathlib Hermite-polynomial identities", "Polynomial.hermite and pinned Gaussian identities", "M3", 60),
    "M0353-X-SOURCE": ("terminal", "Pin a primary proof and map every analytic node", "primary-source node map pending", "M4", 40),
    "M0353-X-TRUST": ("certificate", "Inventory axioms, imports, TCB, quotient soundness, and no-oracle policy", "planned trust certificate", "M4", 40),
    "M0353-X-PROVENANCE": ("certificate", "Track terminal proof bodies and immutable evidence", "planned provenance certificate", "M4", 40),
}
machine_na = {"M0353-X-SOURCE"}
info = {"M0353-X-PROVENANCE"}
human_na = {"M0353-S-NORMALIZATION", "M0353-X-TRUST", "M0353-X-PROVENANCE"}
rows = []
for oid in ids:
    kind, human, formal, _, _ = desc[oid]
    fp = hashlib.sha256(("THM-M-0353:v1:" + oid + ":" + human + ":" + formal).encode()).hexdigest()
    rows.append({
        "obligation_id": oid, "statement_fingerprint": "planned:v1:sha256:" + fp,
        "kind": kind, "root_relevant": True,
        "machine_eligibility": "not_applicable" if oid in machine_na else ("informational" if oid in info else "required"),
        "human_source_eligibility": "not_applicable" if oid in human_na else "required",
        "readable_eligibility": "required",
        "risk_class": "critical" if oid in {"M0353-ROOT", "M0353-L-ORTHONORMAL", "M0353-L-DENSE", "M0353-T-MEASURE", "M0353-X-TRUST"} else "high",
        "exclusion_reason": "human_source_boundary_only" if oid in machine_na else ("provenance_overlay_no_proof_credit" if oid in info else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0353/ObligationTree.lean#root_of_hermite_packages" if oid == "M0353-T-ASSEMBLE" else None,
    })
fields = tuple(rows[0])
digest = hashlib.sha256(json.dumps([{k: r[k] for k in fields} for r in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
reg = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0353-OBLIGATION_TREE",
    "theorem_id": "THM-M-0353", "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus bounded anchor audit; Gaussian-polynomial orthogonality and density transport route, frozen independently of proof availability.",
    "frozen_against_statement_sha256": hashlib.sha256((H / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((H / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": ids[0], "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids, "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0353-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": rows,
}
proof_children = {
    "M0353-ROOT": ["M0353-T-ASSEMBLE"],
    "M0353-T-ASSEMBLE": ["M0353-P-MEMLP", "M0353-P-BASIS"],
    "M0353-P-MEMLP": ["M0353-C-LP-VECTORS"],
    "M0353-P-BASIS": ["M0353-C-HILBERT-BASIS"],
    "M0353-C-HILBERT-BASIS": ["M0353-C-LP-VECTORS", "M0353-L-ORTHONORMAL", "M0353-L-DENSE"],
    "M0353-L-ORTHONORMAL": ["M0353-L-GAUSSIAN-ORTH"],
    "M0353-L-GAUSSIAN-ORTH": ["M0353-X-HERMITE-POLY", "M0353-S-NORMALIZATION"],
    "M0353-L-DENSE": ["M0353-L-POLY-DENSE", "M0353-T-MEASURE"],
    "M0353-L-POLY-DENSE": ["M0353-X-HERMITE-POLY"],
    "M0353-T-MEASURE": ["M0353-S-NORMALIZATION"],
}
def simple_edges(pairs, typ):
    return [{"edge_id": f"{typ}:{a}:{b}", "type": typ, "from": a, "to": b} for a, b in pairs]
proof_edges = []
for parent, children in proof_children.items():
    for child in children:
        req = f"requires:{parent}:{child}"; comp = f"composes:{child}:{parent}"
        proof_edges += [
            {"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp},
            {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req},
        ]
graphs = {
    "proof": {"edges": proof_edges},
    "refinement": {"edges": simple_edges([("M0353-S-NORMALIZATION", "M0353-ROOT")], "logical_decomposition")},
    "provenance": {"edges": simple_edges([("M0353-X-PROVENANCE", i) for i in ids if i != "M0353-X-PROVENANCE"], "provenance_of")},
    "evidence": {"edges": []},
    "trust": {"edges": simple_edges([("M0353-X-TRUST", i) for i in ids if i != "M0353-X-TRUST"], "trusts")},
    "documentation": {"edges": simple_edges([("M0353-X-SOURCE", i) for i in ids if i not in {"M0353-X-SOURCE", "M0353-X-TRUST", "M0353-X-PROVENANCE", "M0353-S-NORMALIZATION"}], "source_map")},
    "workflow": {"edges": simple_edges([("M0353-T-ASSEMBLE", "M0353-ROOT"), ("M0353-X-TRUST", "M0353-T-ASSEMBLE"), ("M0353-X-PROVENANCE", "M0353-T-ASSEMBLE")], "workflow_depends_on")},
}
for graph in graphs.values():
    graph["out"] = {i: [e["edge_id"] for e in graph["edges"] if e["from"] == i] for i in ids}
    graph["in"] = {i: [e["edge_id"] for e in graph["edges"] if e["to"] == i] for i in ids}
nodes = []
for oid in ids:
    kind, human, formal, machine, budget = desc[oid]
    nodes.append({
        "node_id": "THM-M-0353-" + oid[6:], "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H1", "machine_debt": machine, "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in human_na else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or unchecked computation may close this node", "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only declared proof-requirement children and the formal context.", "inference": human, "output": human, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0353/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen interface only; open premises receive no proof credit.",
        "task_ids": ["S56-M-0353-OBLIGATION_TREE", "S56-M-0353-PROOF"], "owned_sources": [],
        "owner": "THM-M-0353 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if machine == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if machine == "M0-L" else "open"},
    })
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0353-OBLIGATION_TREE", "theorem_id": "THM-M-0353",
    "registry_id": "THM-M-0353-OBLIGATIONS-v1", "registry_denominator_sha256": digest, "root_node_id": ids[0],
    "edge_direction": "proof_requires parent to child; composes child to parent", "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "theorem_complete": False, "minimal_open_root_cut": ["M0353-P-MEMLP", "M0353-P-BASIS"]},
}
(H / "obligation-registry.json").write_text(json.dumps(reg, indent=2) + "\n")
(H / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(digest)
