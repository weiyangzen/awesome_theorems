#!/usr/bin/env python3
"""Generate the frozen THM-M-0170 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0170-OBLIGATION_TREE"

ROWS = [
    ("M0170-ROOT", "root", "Exact smooth Nash isometric embedding target", "critical", "H1", "M4", 8),
    ("M0170-S-INTERFACE", "definition", "Relate pointwise mfderiv inner-product preservation to pullback metric equality", "critical", "H1", "M3", 35),
    ("M0170-S-BOUNDARY", "branch", "Handle empty, zero-dimensional, disconnected, and zero-target cases without strengthening the target", "high", "H1", "M4", 30),
    ("M0170-S-FOUNDATION", "certificate", "Audit classical choice, quotients, extensionality, kernel, and transitive imports", "critical", "H1", "M3", 25),
    ("M0170-N-COMPACT", "normalization", "Normalize the compact branch to finite charts and a controlled initial embedding", "critical", "H1", "M4", 80),
    ("M0170-N-EXHAUST", "normalization", "Construct a locally finite compact exhaustion with quantitative error budgets", "critical", "H1", "M4", 90),
    ("M0170-C-FREE", "construction", "Construct a smooth free initial embedding in sufficiently large Euclidean dimension", "critical", "H1", "M4", 95),
    ("M0170-L-DEFECT", "core_lemma", "Represent and reduce the positive metric defect by primitive metric corrections", "critical", "H1", "M4", 95),
    ("M0170-L-PERTURB", "core_lemma", "Realize one metric correction by a controlled smooth high-frequency perturbation", "critical", "H1", "M4", 100),
    ("M0170-L-SMOOTH", "core_lemma", "Prove smoothing estimates with derivative loss required by the iteration", "critical", "H1", "M4", 100),
    ("M0170-C-ITER", "construction", "Run the Nash iteration and prove smooth convergence, injectivity, and exact metric equality", "critical", "H1", "M4", 100),
    ("M0170-L-COMPAT", "core_lemma", "Make exhaustion-stage perturbations locally finite and compatible on earlier compact sets", "critical", "H1", "M4", 90),
    ("M0170-B-COMPACT", "branch", "Derive the exact target for compact source manifolds", "critical", "H1", "M4", 70),
    ("M0170-B-NONCOMPACT", "branch", "Derive the exact target for noncompact second-countable source manifolds", "critical", "H1", "M4", 90),
    ("M0170-T-ASSEMBLE", "terminal", "Exhaustively combine compact and noncompact packages into the exact root", "critical", "H1", "M3", 12),
    ("M0170-X-SOURCE", "terminal", "Pinpoint source statements, assumptions, proof stages, and errata", "high", "H1", "M4", 60),
    ("M0170-X-PROVENANCE", "terminal", "Track terminal bodies, wrappers, dependencies, receipts, and axiom closure", "critical", "H1", "M3", 40),
]

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

def main():
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    audit_hash = hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest()
    obligations = []
    for oid, kind, claim, risk, _, _, _ in ROWS:
        obligations.append({
            "obligation_id": oid,
            "statement_fingerprint": ("lean-source-sha256:" + statement_hash if oid == "M0170-ROOT" else "planned:v1:sha256:" + sha(claim)),
            "kind": kind, "root_relevant": not oid.startswith("M0170-X-"),
            "machine_eligibility": "informational" if oid in {"M0170-X-SOURCE", "M0170-X-PROVENANCE"} else "required",
            "human_source_eligibility": "not_applicable" if oid in {"M0170-S-INTERFACE", "M0170-S-FOUNDATION", "M0170-X-PROVENANCE"} else "required",
            "readable_eligibility": "required", "risk_class": risk,
            "exclusion_reason": "non-proof release overlay" if oid.startswith("M0170-X-") else None,
            "terminal_proof_body_id": None,
        })
    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    denominator = sha(json.dumps([{k: r[k] for k in fields} for r in obligations], sort_keys=True, separators=(",", ":")))
    ids = [r[0] for r in ROWS]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
        "theorem_id": "THM-M-0170", "registry_version": 1,
        "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": "Exact elaborated target and bounded anchor audit; classical smooth Nash proof architecture; eligibility assigned without proof closure credit.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": audit_hash,
        "root_obligation_id": "M0170-ROOT", "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
            "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": ["M0170-X-SOURCE", "M0170-X-PROVENANCE"],
        },
        "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
        "obligations": obligations,
    }
    recipes = []
    nodes = []
    for oid, kind, claim, _, hdebt, mdebt, budget in ROWS:
        rid = "VAL-" + oid
        recipes.append({"recipe_id": rid, "obligation_id": oid, "covered_obligation_ids": [oid], "argv": ["python3", "Stage1_Instances/THM-M-0170/check_obligation_tree.py"], "expected_exit": 0, "network_policy": "denied"})
        nodes.append({
            "node_id": oid, "obligation_id": oid, "kind": kind,
            "human_statement": claim, "formal_target": "Stage1Instances.THM_M_0170.Statement" if oid == "M0170-ROOT" else "planned signature: " + claim,
            "output": claim, "human_debt": hdebt, "machine_debt": mdebt, "readability_debt": "R2",
            "evidence_ids": [], "source_crosswalk_id": "SRC-UNPINNED" if "SOURCE" not in oid else "SRC-REGISTRY",
            "provenance_id": "PROV-OPEN", "foundation_profile": "lean4-mathlib-classical/5.6",
            "tcb_profile": "lean4-kernel-pinned/5.6", "computation_record": "none",
            "step_budget": budget,
            "semantic_step_ledger": {"premises": [], "inference": "planned; no closure credited", "output": claim, "outgoing_use": "typed graph edges"},
            "public_readable_target": "Stage1_Instances/THM-M-0170/obligation-tree.md#" + oid.lower(),
            "validation_spec_id": rid, "status_boundary": "Architecture only; this node is not machine-closed.",
            "task_ids": [ITEM], "owned_sources": ["Stage1_Instances/THM-M-0170"],
            "owner": "Stage1 rev-5.6 execution lane", "reviewer": "independent integration-lane reviewer",
            "validity": {"validated_at": None, "review_due": "on any input change", "invalidation_inputs": ["statement", "source", "toolchain", "architecture"], "revocation_state": "active"},
        })

    graphs = {name: {"edges": [], "out": {}, "in": {}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
    def edge(graph, eid, src, typ, dst, reciprocal=None):
        e = {"edge_id": eid, "from": src, "type": typ, "to": dst}
        if reciprocal: e["reciprocal_edge_id"] = reciprocal
        graphs[graph]["edges"].append(e)
        graphs[graph]["out"].setdefault(src, []).append(eid)
        graphs[graph]["in"].setdefault(dst, []).append(eid)
    def proof(parent, child, tag):
        edge("proof", "REQ-" + tag, parent, "proof_requires", child, "COMP-" + tag)
        edge("proof", "COMP-" + tag, child, "composes", parent, "REQ-" + tag)
    proof("M0170-ROOT", "M0170-T-ASSEMBLE", "ROOT-ASSEMBLE")
    proof("M0170-T-ASSEMBLE", "M0170-B-COMPACT", "ASSEMBLE-COMPACT")
    proof("M0170-T-ASSEMBLE", "M0170-B-NONCOMPACT", "ASSEMBLE-NONCOMPACT")
    for child in ("M0170-N-COMPACT", "M0170-C-FREE", "M0170-L-DEFECT", "M0170-L-PERTURB", "M0170-L-SMOOTH", "M0170-C-ITER"):
        proof("M0170-B-COMPACT", child, "COMPACT-" + child.split("-")[-1])
    for child in ("M0170-N-EXHAUST", "M0170-C-FREE", "M0170-L-DEFECT", "M0170-L-PERTURB", "M0170-L-SMOOTH", "M0170-C-ITER", "M0170-L-COMPAT"):
        proof("M0170-B-NONCOMPACT", child, "NONCOMPACT-" + child.split("-")[-1])
    for child in ("M0170-S-INTERFACE", "M0170-S-BOUNDARY"):
        edge("refinement", "REF-" + child, "M0170-ROOT", "logical_decomposition", child)
    edge("provenance", "PROV-SOURCE", "M0170-X-SOURCE", "provenance_of", "M0170-ROOT")
    edge("provenance", "PROV-BODIES", "M0170-X-PROVENANCE", "provenance_of", "M0170-ROOT")
    edge("trust", "TRUST-FOUNDATION", "M0170-ROOT", "trusts", "M0170-S-FOUNDATION")
    edge("documentation", "DOC-SOURCE", "M0170-X-SOURCE", "documents", "M0170-ROOT")
    edge("workflow", "FLOW-PROOF", "M0170-T-ASSEMBLE", "workflow_depends_on", "M0170-B-COMPACT")
    edge("workflow", "FLOW-PROOF-NC", "M0170-T-ASSEMBLE", "workflow_depends_on", "M0170-B-NONCOMPACT")
    edge("workflow", "FLOW-PROVENANCE", "M0170-X-PROVENANCE", "workflow_depends_on", "M0170-T-ASSEMBLE")
    bundle = {
        "schema_version": "stage1-typed-graph-bundle/1.0", "item_id": ITEM, "theorem_id": "THM-M-0170",
        "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
        "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False,
            "theorem_complete": False, "remaining_root_cut_set": ["M0170-B-COMPACT", "M0170-B-NONCOMPACT"],
            "composition_certificates": ["Stage1Instances.THM_M_0170.statement_of_compact_and_noncompact"],
            "reason": "The exhaustive recomposition is checked conditionally, but both Nash construction branches and their dependencies remain open."},
    }
    dump("obligation-registry.json", registry)
    dump("typed-graphs.json", bundle)
    dump("validation-specs.json", {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0170", "recipes": recipes})

if __name__ == "__main__":
    main()
