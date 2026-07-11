#!/usr/bin/env python3
"""Generate the frozen THM-M-0087 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0087-OBLIGATION_TREE"

ROWS = [
    ("M0087-ROOT", "root", "Exact four-component frozen Gabriel-Popescu target", "critical", "M3", 8),
    ("M0087-S-TARGET", "definition", "Freeze universes, category hypotheses, separator, module convention, and exact conjunction", "high", "M3", 20),
    ("M0087-S-BOUNDARY", "boundary", "Keep the explicit Serre-quotient equivalence outside this frozen target", "critical", "M4", 18),
    ("M0087-B-FULL", "branch", "Prove fullness of preadditiveCoyonedaObj G", "critical", "M3", 35),
    ("M0087-L-KERNEL", "core_lemma", "Prove kernel.ι (d g) followed by d f is zero", "critical", "M3", 90),
    ("M0087-L-EXTEND", "core_lemma", "Extend d f across d g into an injective target", "high", "M3", 45),
    ("M0087-B-FAITHFUL", "branch", "Transport separator data to faithfulness of preadditiveCoyonedaObj G", "high", "M3", 15),
    ("M0087-B-ADJUNCTION", "branch", "Construct the tensorObj/preadditiveCoyonedaObj adjunction witness", "high", "M3", 20),
    ("M0087-B-FINLIM", "branch", "Prove tensorObj G preserves finite limits", "critical", "M3", 35),
    ("M0087-L-INJECTIVE", "core_lemma", "Show preadditiveCoyonedaObj G preserves injective objects", "critical", "M3", 60),
    ("M0087-L-MONO", "core_lemma", "Derive preservation of monomorphisms by tensorObj G", "high", "M3", 20),
    ("M0087-L-ADDITIVE", "core_lemma", "Derive additivity from preservation of binary coproducts and biproducts", "high", "M3", 20),
    ("M0087-L-HOMOLOGY", "core_lemma", "Derive preservation of homology from monomorphisms and cokernels", "high", "M3", 20),
    ("M0087-T-ASSEMBLE", "terminal", "Compose the four exact conclusion packages into the root", "critical", "M3", 8),
    ("M0087-X-SOURCE", "documentation", "Pinpoint primary human sources, assumptions, variants, and errata", "high", "M4", 50),
    ("M0087-X-PROVENANCE", "provenance", "Resolve unique terminal bodies, transitive dependencies, and proof-body credit", "critical", "M3", 45),
    ("M0087-X-TRUST", "trust", "Audit kernel axioms, TCB, imports, replay, and revocation inputs", "critical", "M3", 45),
]


def sha(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def main():
    statement_hash = sha((HERE / "Statement.lean").read_bytes())
    audit_hash = sha((HERE / "anchor-audit.json").read_bytes())
    obligations = []
    overlays = {"M0087-X-SOURCE", "M0087-X-PROVENANCE", "M0087-X-TRUST"}
    for oid, kind, claim, risk, _, _ in ROWS:
        obligations.append({
            "obligation_id": oid,
            "statement_fingerprint": "lean-source-sha256:" + statement_hash if oid == "M0087-ROOT" else "planned:v1:sha256:" + sha(claim),
            "kind": kind,
            "root_relevant": oid not in overlays,
            "machine_eligibility": "informational" if oid in overlays else "required",
            "human_source_eligibility": "required" if oid in {"M0087-ROOT", "M0087-S-TARGET", "M0087-S-BOUNDARY", "M0087-B-FULL", "M0087-L-KERNEL", "M0087-L-EXTEND", "M0087-B-FAITHFUL", "M0087-B-ADJUNCTION", "M0087-B-FINLIM", "M0087-L-INJECTIVE", "M0087-X-SOURCE"} else "not_applicable",
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": "non-proof assurance overlay" if oid in overlays else None,
            "terminal_proof_body_id": None,
        })
    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    denominator = sha(json.dumps([{k: row[k] for k in fields} for row in obligations], sort_keys=True, separators=(",", ":")))
    ids = [row[0] for row in ROWS]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": "THM-M-0087",
        "registry_version": 1,
        "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": "Exact elaborated statement plus immutable pinned-anchor audit; eligibility assigned without accepting candidate closure.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": audit_hash,
        "root_obligation_id": "M0087-ROOT",
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
            "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": sorted(overlays),
        },
        "delta_policy": "Any correction, split, merge, exclusion, eligibility, statement, or anchor change requires registry version 2 and an append-only old/new ID delta.",
        "obligations": obligations,
    }

    recipes, nodes = [], []
    for oid, kind, claim, _, mdebt, budget in ROWS:
        rid = "VAL-" + oid
        recipes.append({
            "recipe_id": rid,
            "obligation_id": oid,
            "cwd": ".",
            "argv": ["python3", "Stage1_Instances/THM-M-0087/check_obligation_tree.py"],
            "env": {},
            "timeout_seconds": 30,
            "network_policy": "denied",
            "covered_obligation_ids": [oid],
            "expected_exit": 0,
        })
        nodes.append({
            "node_id": oid,
            "obligation_id": oid,
            "kind": kind,
            "human_statement": claim,
            "formal_target": "Stage1Instances.THM_M_0087.Statement" if oid == "M0087-ROOT" else "planned signature: " + claim,
            "output": claim,
            "human_debt": "H1",
            "machine_debt": mdebt,
            "readability_debt": "R3",
            "evidence_ids": [],
            "source_crosswalk_id": "anchor-audit:C02" if oid not in overlays else "open-assurance-overlay",
            "provenance_id": "mathlib:GabrielPopescu.lean" if oid not in overlays else "open",
            "foundation_profile": "lean4-mathlib-classical/5.6",
            "tcb_profile": "lean-4.29.0-pinned/transitive-audit-open",
            "computation_record": "none",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": [],
                "inference": "planned architecture; no proof closure credited",
                "output": claim,
                "outgoing_use": "typed graph edges",
            },
            "public_readable_target": "Stage1_Instances/THM-M-0087/obligation-tree.md#" + oid.lower(),
            "validation_spec_id": rid,
            "status_boundary": "Architecture only; candidate anchors are not accepted proof bodies at this node.",
            "task_ids": [ITEM],
            "owned_sources": ["Stage1_Instances/THM-M-0087"],
            "owner": "Stage1 rev-5.6 execution lane",
            "reviewer": "independent integration-lane reviewer",
            "validity": {"validated_at": None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "anchor audit", "registry", "toolchain"], "revocation_state": "active"},
        })

    graphs = {name: {"edges": [], "out": {}, "in": {}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}

    def edge(graph, eid, src, typ, dst, reciprocal=None):
        item = {"edge_id": eid, "from": src, "type": typ, "to": dst}
        if reciprocal:
            item["reciprocal_edge_id"] = reciprocal
        graphs[graph]["edges"].append(item)
        graphs[graph]["out"].setdefault(src, []).append(eid)
        graphs[graph]["in"].setdefault(dst, []).append(eid)

    def proof(parent, child, tag):
        edge("proof", "REQ-" + tag, parent, "proof_requires", child, "COMP-" + tag)
        edge("proof", "COMP-" + tag, child, "composes", parent, "REQ-" + tag)

    proof("M0087-ROOT", "M0087-T-ASSEMBLE", "ROOT-ASSEMBLE")
    for child in ("M0087-B-FULL", "M0087-B-FAITHFUL", "M0087-B-ADJUNCTION", "M0087-B-FINLIM"):
        proof("M0087-T-ASSEMBLE", child, "ASSEMBLE-" + child.split("-")[-1])
    proof("M0087-B-FULL", "M0087-L-KERNEL", "FULL-KERNEL")
    proof("M0087-L-EXTEND", "M0087-L-KERNEL", "EXTEND-KERNEL")
    proof("M0087-L-INJECTIVE", "M0087-L-EXTEND", "INJECTIVE-EXTEND")
    for child in ("M0087-L-INJECTIVE", "M0087-L-MONO", "M0087-L-ADDITIVE", "M0087-L-HOMOLOGY"):
        proof("M0087-B-FINLIM", child, "FINLIM-" + child.split("-")[-1])
    for child in ("M0087-S-TARGET", "M0087-S-BOUNDARY"):
        edge("refinement", "REF-" + child, "M0087-ROOT", "logical_decomposition", child)
    edge("provenance", "PROV-BODIES", "M0087-X-PROVENANCE", "provenance_of", "M0087-ROOT")
    edge("evidence", "EVIDENCE-ROOT", "M0087-X-PROVENANCE", "evidence_for", "M0087-ROOT")
    edge("trust", "TRUST-ROOT", "M0087-ROOT", "trusts", "M0087-X-TRUST")
    edge("documentation", "DOC-SOURCE", "M0087-X-SOURCE", "documents", "M0087-ROOT")
    edge("workflow", "FLOW-ASSEMBLY", "M0087-T-ASSEMBLE", "workflow_depends_on", "M0087-S-TARGET")
    edge("workflow", "FLOW-PROVENANCE", "M0087-X-PROVENANCE", "workflow_depends_on", "M0087-T-ASSEMBLE")
    edge("workflow", "FLOW-TRUST", "M0087-X-TRUST", "workflow_depends_on", "M0087-X-PROVENANCE")

    bundle = {
        "schema_version": "stage1-typed-graph-bundle/1.0",
        "item_id": ITEM,
        "theorem_id": "THM-M-0087",
        "registry_denominator_sha256": denominator,
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "closed_obligations": [],
            "root_closed": False,
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": ["M0087-B-FULL", "M0087-B-FAITHFUL", "M0087-B-ADJUNCTION", "M0087-B-FINLIM"],
            "composition_certificates": ["Stage1Instances.THM_M_0087.ObligationTree.root_of_packages"],
            "reason": "Exact conjunction assembly is checked conditionally; all four mathematical packages remain uncredited premises until the proof phase.",
        },
    }
    dump("obligation-registry.json", registry)
    dump("typed-graphs.json", bundle)
    dump("validation-specs.json", {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0087", "recipes": recipes})


if __name__ == "__main__":
    main()
