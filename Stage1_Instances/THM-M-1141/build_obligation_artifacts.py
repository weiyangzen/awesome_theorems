#!/usr/bin/env python3
"""Generate the frozen THM-M-1141 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1141-OBLIGATION_TREE"
THEOREM = "THM-M-1141"

rows = [
    ("M1141-ROOT", "root", "The exact compact-subset Harnack inequality.", "Stage1Instances.THM_M_1141.HarnackInequality", "M3", 40),
    ("M1141-L-LOCAL", "core_lemma", "Prove a dimension-uniform local Harnack estimate on a ball whose closure lies in the domain.", "planned local-ball Harnack lemma for HarmonicOnNhd", "M4", 100),
    ("M1141-L-POSITIVE", "lemma", "Preserve strict positivity and justify every division and comparison multiplication.", "planned positivity/nonzero denominator package", "M4", 40),
    ("M1141-C-COVER", "construction", "Extract a finite interior ball cover of the compact set, with quantitative room inside the domain.", "planned compact finite subcover package", "M4", 80),
    ("M1141-C-CHAIN", "construction", "Use connectedness of the open domain to build finite overlapping-ball chains between cover centers.", "planned connected-domain Harnack-chain package", "M4", 100),
    ("M1141-L-PROPAGATE", "core_lemma", "Propagate local comparisons along each finite chain and control the product constant.", "planned finite-chain comparison lemma", "M4", 80),
    ("M1141-T-UNIFORM", "assembly", "Take a finite maximum/product to obtain one A independent of u, x, and y.", "Stage1Instances.THM_M_1141.UniformValueComparison", "M4", 80),
    ("M1141-T-RATIO", "transport", "Convert symmetric value comparison into the exact two-sided ratio bound with C > 1.", "Stage1Instances.THM_M_1141.harnackInequality_of_uniformValueComparison", "M0-L", 40),
    ("M1141-X-SOURCE", "source_boundary", "Map every analytic and topological leaf to inspected human proof passages.", "human source crosswalk; no Lean proposition", "not_applicable", 40),
    ("M1141-X-TRUST", "certificate", "Audit axioms, imports, TCB, and absence of oracle or placeholder proof credit.", "planned transitive trust report", "M4", 40),
    ("M1141-X-PROVENANCE", "certificate", "Bind terminal proof bodies and validation evidence to immutable revisions and hashes.", "planned provenance receipt", "informational", 40),
]

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

obligations = []
for oid, kind, human, formal, machine, budget in rows:
    source = "not_applicable" if oid in {"M1141-L-POSITIVE", "M1141-T-RATIO", "M1141-X-TRUST", "M1141-X-PROVENANCE"} else "required"
    machine_eligibility = "required" if machine not in {"not_applicable", "informational"} else machine
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "planned:v1:sha256:" + sha(human + "\n" + formal),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine_eligibility,
        "human_source_eligibility": source,
        "readable_eligibility": "required",
        "risk_class": "critical" if machine == "M4" or oid == "M1141-ROOT" else "high",
        "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("release_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1141/ObligationTree.lean#harnackInequality_of_uniformValueComparison" if oid == "M1141-T-RATIO" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in obligations]
digest = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))
ids = [r[0] for r in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated compact-subset target and bounded anchor audit; local estimate, compact-cover, connected-chain, propagation, and ratio architecture frozen before proof execution.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1141-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1141-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for oid, kind, human, formal, machine, budget in rows:
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M1141-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human, "human_debt": "H1",
        "machine_debt": machine, "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md" if oid not in {"M1141-L-POSITIVE", "M1141-T-RATIO", "M1141-X-TRUST", "M1141-X-PROVENANCE"} else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node", "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only typed proof-requirement children and the formal context.", "inference": human, "output": human, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1141/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise or root closure.",
        "task_ids": [ITEM, "S56-M-1141-PROOF"], "owned_sources": [], "owner": "THM-M-1141 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid == "M1141-T-RATIO" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid == "M1141-T-RATIO" else "open"},
    })

proof_pairs = [
    ("M1141-ROOT", "M1141-T-RATIO"), ("M1141-T-RATIO", "M1141-T-UNIFORM"),
    ("M1141-T-UNIFORM", "M1141-C-COVER"), ("M1141-T-UNIFORM", "M1141-C-CHAIN"),
    ("M1141-T-UNIFORM", "M1141-L-PROPAGATE"), ("M1141-L-PROPAGATE", "M1141-L-LOCAL"),
    ("M1141-L-PROPAGATE", "M1141-L-POSITIVE"),
]
graphs = {name: {"edges": [], "out": {i: [] for i in ids}, "in": {i: [] for i in ids}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
def edge(graph, eid, typ, src, dst, reciprocal=None):
    e = {"edge_id": eid, "type": typ, "from": src, "to": dst}
    if reciprocal: e["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(e); graphs[graph]["out"][src].append(eid); graphs[graph]["in"][dst].append(eid)
for i, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{i:02}-REQ", f"P{i:02}-COMP"
    edge("proof", req, "proof_requires", parent, child, comp); edge("proof", comp, "composes", child, parent, req)
for i, child in enumerate(ids[1:], 1): edge("refinement", f"R{i:02}", "logical_decomposition", "M1141-ROOT", child)
for i, oid in enumerate(ids[:-2], 1): edge("provenance", f"V{i:02}", "provenance_of", "M1141-X-PROVENANCE", oid)
for i, oid in enumerate(ids[:-2], 1): edge("evidence", f"E{i:02}", "provenance_of", "M1141-X-PROVENANCE", oid)
for i, oid in enumerate(ids[:-2], 1): edge("trust", f"T{i:02}", "trusts", oid, "M1141-X-TRUST")
for i, oid in enumerate(ids[:-2], 1): edge("documentation", f"D{i:02}", "documents", "M1141-X-SOURCE", oid)
for i, (parent, child) in enumerate(proof_pairs, 1): edge("workflow", f"W{i:02}", "workflow_depends_on", parent, child)

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": THEOREM + "-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M1141-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "theorem_complete": False, "remaining_root_cut_set": ["M1141-L-LOCAL", "M1141-C-COVER", "M1141-C-CHAIN", "M1141-L-PROPAGATE", "M1141-T-UNIFORM", "M1141-X-TRUST"]},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "required_check": "exact type, axiom, placeholder, provenance, composition, and freshness as applicable", "state": "open" if machine != "M0-L" else "provisional_self_tested"} for oid, _, _, _, machine, _ in rows]}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
(HERE / "validation-specs.json").write_text(json.dumps(specs, indent=2) + "\n")
(HERE / "obligation-tree.md").write_text("# THM-M-1141 obligation tree\n\nThe registry is frozen at v1. All nodes below are obligations, not proof claims.\n\n" + "\n".join(f"## {oid.lower()}\n\n**{kind}.** {human}\n\nFormal target: `{formal}`. Machine debt: `{machine}`. Step budget: {budget}." for oid, kind, human, formal, machine, budget in rows) + "\n\nThe root remains M3 and theorem completion is false.\n")
print(digest)
