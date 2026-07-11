#!/usr/bin/env python3
"""Build the deterministic THM-M-0545 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0545-OBLIGATION_TREE"
THEOREM = "THM-M-0545"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


specs = [
    ("M0545-ROOT", "root", "Exact HodgeDecompositionTarget for every admitted geometric realization.", "Stage1Instances.THMM0545.HodgeDecompositionTarget", "The canonical proposition.", "critical", "H3", "M4", 20),
    ("M0545-S-INTERFACE", "definition", "Preserve the exact manifold, form, operator, degree, and uniqueness interface.", "Stage1Instances.THMM0545.{HodgeAnalyticData,HodgeDecompositionTarget}", "The elaborated statement interface.", "high", "H3", "M0-L", 20),
    ("M0545-S-REALIZATION", "bridge", "Show that the realization predicates entail the concrete smooth-form, d, codifferential, Laplacian, orientation, and boundaryless semantics used below.", "planned faithful-realization elimination API for HodgeAnalyticData", "Typed access to the geometric analytic structures, without assuming decomposition.", "critical", "H3", "M4", 80),
    ("M0545-S-BOUNDARY", "terminal", "Handle degree zero and degrees above dimension without silently adding a predecessor or excluding a form.", "planned boundary-degree lemmas for IsExact and realized form spaces", "Correct degree-boundary behavior.", "high", "H3", "M4", 40),
    ("M0545-S-FOUNDATION", "certificate", "Freeze classical logic, functional-analysis axioms, TCB, and no-oracle policy.", "planned foundation and transitive axiom certificate", "Accepted trust boundary for every terminal body.", "critical", "H3", "M4", 30),
    ("M0545-A-COMPLETION", "construction", "Construct the L2 and Sobolev completions of smooth complex k-forms and the dense smooth inclusions.", "planned Lean Hilbert/Sobolev realization package", "Hilbert spaces on which unbounded Hodge operators act.", "critical", "H3", "M4", 100),
    ("M0545-A-D", "construction", "Realize exterior derivative as a densely defined closed operator and prove d composed with d is zero.", "planned closed exterior-derivative package", "Closed de Rham differential with square zero.", "critical", "H3", "M4", 100),
    ("M0545-A-ADJOINT", "construction", "Construct the Hilbert adjoint codifferential and identify it with the frozen smooth codifferential.", "planned codifferential/adjoint identification", "Closed adjoint delta and smooth compatibility.", "critical", "H3", "M4", 100),
    ("M0545-A-LAPLACIAN", "construction", "Construct Delta = d delta + delta d on its correct domain and identify it with the frozen Laplacian.", "planned Hodge-Laplacian domain and compatibility package", "A nonnegative self-adjoint Hodge Laplacian.", "critical", "H3", "M4", 100),
    ("M0545-A-ELLIPTIC", "core_lemma", "Prove elliptic regularity and compact resolvent for the Hodge Laplacian on the compact boundaryless manifold.", "planned elliptic-regularity and compact-resolvent theorem", "Finite-dimensional smooth kernel and spectral control.", "critical", "H3", "M4", 100),
    ("M0545-A-GREEN", "construction", "Construct the harmonic projection and Green operator and establish their commutation identities with d and delta.", "planned harmonic projection/Green operator package", "Operators H and G with identity = H + Delta G.", "critical", "H3", "M4", 100),
    ("M0545-L-CLOSED-RANGES", "core_lemma", "Prove the exact and coexact ranges are closed and mutually orthogonal, including orthogonality to harmonic forms.", "planned closed-range and orthogonality theorem", "Closed pairwise-orthogonal harmonic, exact, and coexact subspaces.", "critical", "H3", "M4", 100),
    ("M0545-T-EXISTENCE", "terminal", "Use omega = H omega + d delta G omega + delta d G omega and regularity to obtain smooth summands.", "planned exact HasUniqueDecomposition existence component", "Harmonic, exact, coexact, pairwise-orthogonal summands whose sum is omega.", "critical", "H3", "M4", 70),
    ("M0545-T-UNIQUENESS", "terminal", "Deduce equality of two triples from pairwise orthogonality of the three subspaces.", "planned exact HasUniqueDecomposition uniqueness component", "Uniqueness of all three summands.", "high", "H3", "M4", 50),
    ("M0545-T-ASSEMBLE", "transport", "Assemble existence and uniqueness for every k and omega into the exact canonical root.", "planned checked child-to-parent composition declaration", "Stage1Instances.THMM0545.HodgeDecompositionTarget", "critical", "H3", "M4", 30),
    ("M0545-X-SOURCE", "terminal", "Pin a primary theorem and map every analytic premise and transition, including errata.", "non-Lean primary-source crosswalk receipt", "Node-specific human-source provenance.", "high", "H3", "M4", 50),
    ("M0545-X-PROVENANCE", "terminal", "Record terminal bodies, imports, licenses, placeholders, axioms, TCB, and replay provenance.", "structured terminal-body provenance packet", "Fail-closed provenance and trust inventory.", "critical", "H3", "M4", 40),
]

machine_required = {row[0] for row in specs if not row[0].startswith("M0545-X-")}
human_required = {row[0] for row in specs if row[0] not in {"M0545-S-INTERFACE", "M0545-S-BOUNDARY", "M0545-S-FOUNDATION", "M0545-X-PROVENANCE"}}
rows = []
nodes = []
for oid, kind, claim, formal, output, risk, h_debt, m_debt, budget in specs:
    if oid == "M0545-ROOT":
        fingerprint = "lean-elaborated-print-sha256:afcc4739ad6536f2f83577f6076cdcd38cbb3c15d867ddadac48cc5e417227a9"
    elif oid == "M0545-S-INTERFACE":
        fingerprint = "lean-source-sha256:" + hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    else:
        fingerprint = "planned:v1:sha256:" + sha(formal + "\n" + claim)
    rows.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": not oid.startswith("M0545-X-"),
        "machine_eligibility": "required" if oid in machine_required else "informational",
        "human_source_eligibility": "required" if oid in human_required else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None if oid in machine_required else "non_mathematical_source_or_provenance_overlay",
        "terminal_proof_body_id": None,
    })
    anchor = oid.lower().replace(".", "").replace("-", "-")
    nodes.append({
        "node_id": f"THM-M-0545-{oid.removeprefix('M0545-')}", "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": formal, "output": output,
        "human_debt": h_debt, "machine_debt": m_debt, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if oid in human_required else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, numerical approximation, or unchecked PDE solver may close this node",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only typed proof/refinement children and the frozen geometric context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or support edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0545/obligation-tree.md#{anchor}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Architecture only; no planned signature, analytic assertion, or conditional assembly is proof credit.",
        "task_ids": [ITEM, "S56-M-0545-PROOF"], "owned_sources": [],
        "owner": "THM-M-0545 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
digest = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))

inventory = [r["obligation_id"] for r in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded immutable anchor audit; analytic Hodge-theory architecture; eligibility assigned without proof-availability credit.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0545-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": inventory,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": inventory,
        "informational_overlays": ["M0545-X-SOURCE", "M0545-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new registry version and an append-only old/new ID delta.",
    "obligations": rows,
}

graph_names = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
graphs = {name: {"edges": [], "out": {}, "in": {}} for name in graph_names}


def edge(graph, source, target, role):
    number = len(graphs[graph]["edges"]) + 1
    eid = f"M0545-{graph.upper()}-{number:02d}"
    value = {"edge_id": eid, "from": source, "to": target, "type": role}
    graphs[graph]["edges"].append(value)
    graphs[graph]["out"].setdefault(source, []).append(eid)
    graphs[graph]["in"].setdefault(target, []).append(eid)


proof_edges = [
    ("M0545-ROOT", "M0545-T-ASSEMBLE"),
    ("M0545-T-ASSEMBLE", "M0545-T-EXISTENCE"), ("M0545-T-ASSEMBLE", "M0545-T-UNIQUENESS"),
    ("M0545-T-EXISTENCE", "M0545-A-GREEN"), ("M0545-T-EXISTENCE", "M0545-L-CLOSED-RANGES"), ("M0545-T-EXISTENCE", "M0545-S-BOUNDARY"),
    ("M0545-T-UNIQUENESS", "M0545-L-CLOSED-RANGES"),
    ("M0545-A-GREEN", "M0545-A-LAPLACIAN"), ("M0545-A-GREEN", "M0545-A-ELLIPTIC"),
    ("M0545-L-CLOSED-RANGES", "M0545-A-D"), ("M0545-L-CLOSED-RANGES", "M0545-A-ADJOINT"), ("M0545-L-CLOSED-RANGES", "M0545-A-ELLIPTIC"),
    ("M0545-A-ELLIPTIC", "M0545-A-LAPLACIAN"),
    ("M0545-A-LAPLACIAN", "M0545-A-D"), ("M0545-A-LAPLACIAN", "M0545-A-ADJOINT"),
    ("M0545-A-D", "M0545-A-COMPLETION"), ("M0545-A-ADJOINT", "M0545-A-COMPLETION"),
]
for parent, child in proof_edges:
    edge("proof", parent, child, "proof_requires")
    edge("proof", child, parent, "composes")

for child in ("M0545-S-INTERFACE", "M0545-S-REALIZATION", "M0545-S-FOUNDATION"):
    edge("refinement", "M0545-ROOT", child, "logical_decomposition")
edge("refinement", "M0545-A-COMPLETION", "M0545-S-REALIZATION", "logical_decomposition")
edge("refinement", "M0545-A-D", "M0545-S-REALIZATION", "logical_decomposition")
edge("refinement", "M0545-A-ADJOINT", "M0545-S-REALIZATION", "logical_decomposition")
edge("refinement", "M0545-A-LAPLACIAN", "M0545-S-REALIZATION", "logical_decomposition")
for oid in inventory:
    if oid != "M0545-X-SOURCE" and oid in human_required:
        edge("provenance", oid, "M0545-X-SOURCE", "source_map")
    if oid not in {"M0545-X-PROVENANCE", "M0545-X-SOURCE"}:
        edge("provenance", oid, "M0545-X-PROVENANCE", "provenance_of")
for oid in inventory:
    if oid not in {"M0545-X-PROVENANCE", "M0545-S-FOUNDATION"}:
        edge("trust", oid, "M0545-S-FOUNDATION", "trusts")
    if oid != "M0545-X-PROVENANCE":
        edge("evidence", oid, "M0545-X-PROVENANCE", "evidence_requires")
    if oid != "M0545-ROOT":
        edge("documentation", "M0545-ROOT", oid, "documents")
for parent, child in proof_edges:
    edge("workflow", parent, child, "workflow_depends_on")

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0545-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M0545-ROOT", "edge_direction": "Proof requirements run parent to child; composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "closed_obligations": ["M0545-S-INTERFACE"], "root_machine_debt": "M4", "remaining_root_cut_set": ["M0545-S-REALIZATION", "M0545-A-COMPLETION", "M0545-A-D", "M0545-A-ADJOINT", "M0545-A-LAPLACIAN", "M0545-A-ELLIPTIC", "M0545-A-GREEN", "M0545-L-CLOSED-RANGES", "M0545-S-BOUNDARY"], "audit_complete": False, "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(rows)} obligations; denominator {digest}")
