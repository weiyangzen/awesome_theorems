#!/usr/bin/env python3
"""Build the frozen THM-M-1237 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1237-OBLIGATION_TREE"
THEOREM = "THM-M-1237"

specs = [
    ("ROOT", "root", "The exact supercritical first-order Morrey-Sobolev Statement.", "Stage1Rev56.THMM1237.Statement", "Exact canonical root.", "critical", "M3", "H1"),
    ("S", "definition", "Freeze dimensions, domain, exponent, W1p data, extension data, and conclusion structures.", "Definitions in Statement.lean", "Unambiguous statement interface.", "high", "M4", "H1"),
    ("N", "normalization", "Use the supplied whole-space extension and reduce the domain claim to estimates for that extension.", "ExtensionData u -> whole-space weak derivative data", "Whole-space analytic input.", "critical", "M3", "H1"),
    ("B", "branch", "Discharge admitted boundary cases and prove that p > n gives the selected positive Holder exponent.", "1 <= n -> n < p -> alpha = 1 - n/p -> boundary package", "Exhaustive exponent/domain boundary package.", "high", "M3", "H1"),
    ("C", "construction", "Construct a concrete representative agreeing almost everywhere with u on Omega.", "RepresentativeFamily", "Representative plus almost-everywhere agreement.", "critical", "M3", "H1"),
    ("L-HOLDER", "core_lemma", "Prove the quantitative Morrey Holder seminorm estimate on closure Omega.", "HolderEstimateFamily", "HolderOnWith estimate with the W1p norm.", "critical", "M3", "H1"),
    ("L-VALUE", "core_lemma", "Prove the quantitative pointwise value estimate on closure Omega.", "ValueEstimateFamily", "Pointwise norm estimate with the same constant.", "critical", "M3", "H1"),
    ("X-MATHLIB", "bridge", "Audit and use pinned measure, derivative, Lp seminorm, and Holder APIs without treating them as the missing Morrey theorem.", "Pinned mathlib bridge declarations from anchor-audit.json", "Classified imported API boundary.", "high", "M3", "H1"),
    ("X-TRUST", "terminal", "Replay exact declarations under the selected Lean foundation and transitive trust profile.", "#print axioms root_compose and terminal proof declarations", "Axiom and trust-closure record.", "high", "M4", "H1"),
    ("T", "terminal", "Consume construction and both quantitative estimates to build HolderRepresentative and the exact root.", "Stage1Rev56.THMM1237.ObligationTree.root_compose", "Exact child-to-root composition.", "critical", "M0-L", "H1"),
]

obligations = []
nodes = []
for suffix, kind, human, formal, output, risk, machine, human_debt in specs:
    oid = f"M1237-{suffix}"
    fingerprint = hashlib.sha256(f"{oid}\0{formal}\0{human}".encode()).hexdigest()
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": "required",
        "human_source_eligibility": "required", "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": "local:root_compose" if suffix == "T" else None,
    })
    anchor = oid.lower().replace(".", "").replace("-", "-")
    nodes.append({
        "node_id": f"THM-M-1237-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": human_debt, "machine_debt": machine, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "anchor-audit-source-boundary",
        "provenance_id": "local:Stage1_Instances/THM-M-1237/ObligationTree.lean" if suffix in {"C", "L-HOLDER", "L-VALUE", "T"} else "none",
        "foundation_profile": "lean4-dependent-type-theory/profile-review-pending",
        "tcb_profile": "lean-4.29.0/transitive-closure-pending", "computation_record": "none",
        "step_budget": 8, "semantic_step_ledger": {
            "premises": "Typed incoming proof/refinement edges listed in this bundle.",
            "inference": human,
            "output": output,
            "outgoing_use": "Typed outgoing edge to the next root-relevant obligation.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-1237/obligation-tree.md#{anchor}",
        "validation_spec_id": f"VAL-{oid}-PENDING",
        "status_boundary": "Architecture is frozen, but this node receives no proof or release credit in this phase.",
        "task_ids": [ITEM, "S56-M-1237-PROOF"], "owned_sources": [],
        "owner": "THM-M-1237 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; invalidate_on=statement,registry,source-map,toolchain change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "freeze_basis": "Exact Statement.lean plus the immutable anchor audit, before proof execution.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1237-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {"inventory": ids, "required_machine": ids, "required_human_source": ids, "required_readable": ids},
    "obligations": obligations,
}

graphs = {name: {"edges": [], "out": {}, "in": {}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
counter = 0
def edge(graph, typ, source, target, reciprocal=None):
    global counter
    counter += 1
    eid = f"E{counter:03d}"
    row = {"edge_id": eid, "type": typ, "from": source, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(row)
    graphs[graph]["out"].setdefault(source, []).append(eid)
    graphs[graph]["in"].setdefault(target, []).append(eid)
    return eid

def proof_pair(parent, child):
    a = edge("proof", "proof_requires", parent, child)
    b = edge("proof", "composes", child, parent, a)
    graphs["proof"]["edges"][-2]["reciprocal_edge_id"] = b

proof_pair("M1237-ROOT", "M1237-T")
for child in ("M1237-C", "M1237-L-HOLDER", "M1237-L-VALUE", "M1237-X-TRUST"):
    proof_pair("M1237-T", child)
for child in ("M1237-N", "M1237-B"):
    proof_pair("M1237-C", child)
proof_pair("M1237-L-HOLDER", "M1237-X-MATHLIB")
proof_pair("M1237-L-VALUE", "M1237-X-MATHLIB")
for child in ("M1237-S", "M1237-N", "M1237-B", "M1237-C", "M1237-L-HOLDER", "M1237-L-VALUE", "M1237-X-MATHLIB", "M1237-X-TRUST", "M1237-T"):
    edge("refinement", "logical_decomposition", "M1237-ROOT", child)
edge("provenance", "provenance_of", "M1237-X-MATHLIB", "M1237-L-HOLDER")
edge("evidence", "evidence_for", "M1237-X-TRUST", "M1237-T")
edge("trust", "trusts", "M1237-T", "M1237-X-TRUST")
edge("documentation", "documents", "M1237-S", "M1237-ROOT")
edge("workflow", "workflow_depends_on", "M1237-T", "M1237-C")

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_denominator_sha256": digest, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M3",
      "remaining_root_cut_set": ["M1237-C", "M1237-L-HOLDER", "M1237-L-VALUE"],
      "composition_certificates_checked": ["Stage1Rev56.THMM1237.ObligationTree.root_compose"],
      "audit_complete": False, "theorem_complete": False},
}
(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")
print(f"built {len(ids)} obligations, {counter} typed edges; denominator {digest}")
