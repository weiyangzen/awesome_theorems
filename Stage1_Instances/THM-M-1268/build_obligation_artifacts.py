#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

specs = [
    ("M1268-ROOT", "root", "The exact frozen equivalence between weak and norm lower semicontinuity.", "Stage1Instances.THM_M_1268.WeakLowerSemicontinuityTarget", "critical", "H2", "M4", True, True),
    ("M1268-S-DEFINITIONS", "definition", "Freeze EReal convexity, weak transport, and closed-sublevel encodings.", "Stage1Instances.THM_M_1268.ObligationTree.{Sublevel,ConvexSublevels,NormClosedSublevels,WeakClosedSublevels}", "high", "H2", "M0-L", False, True),
    ("M1268-S-BOUNDARIES", "normalization", "Preserve zero spaces, constant functionals, +infinity, empty sublevels, and exclusion of -infinity.", "planned exact boundary declarations", "high", "H2", "M4", True, True),
    ("M1268-S-FOUNDATION", "certificate", "Audit classical separation, choice, transitive axioms, TCB, and no-oracle policy.", "planned foundation and transitive trust receipt", "critical", "H2", "M4", False, True),
    ("M1268-L-CONVEX-SUBLEVEL", "core_lemma", "Derive real convexity of every EReal sublevel from the frozen Jensen predicate.", "Stage1Instances.THM_M_1268.ObligationTree.ConvexSublevelBridge", "critical", "H2", "M4", True, True),
    ("M1268-L-NORM-CLOSED", "bridge", "Convert norm lower semicontinuity to norm-closed EReal sublevels.", "Stage1Instances.THM_M_1268.ObligationTree.normClosedSublevels_iff", "high", "H2", "M0-L", True, True),
    ("M1268-L-WEAK-CLOSURE", "bridge", "Use convex weak/norm closure equality plus exact image/preimage identities to obtain weak-closed sublevels.", "Stage1Instances.THM_M_1268.ObligationTree.WeakClosureTransportBridge", "critical", "H2", "M4", True, True),
    ("M1268-T-NORM-TO-WEAK", "composition", "Compose convexity, norm-closedness, and weak-closure transport into norm-lsc implies weak-lsc.", "Stage1Instances.THM_M_1268.ObligationTree.normToWeak_of_sublevel_bridges", "critical", "H2", "M1", True, True),
    ("M1268-T-WEAK-TO-NORM", "transport", "Prove weak-lsc implies norm-lsc using continuity of the norm-to-weak identity map.", "Stage1Instances.THM_M_1268.ObligationTree.WeakToNormBridge", "high", "H2", "M4", True, True),
    ("M1268-T-ASSEMBLE", "composition", "Assemble both directions without changing binders or hypotheses.", "Stage1Instances.THM_M_1268.ObligationTree.root_of_bridges", "critical", "H2", "M1", True, True),
    ("M1268-X-SOURCE", "source_boundary", "Pinpoint a primary-source theorem, definitions, assumptions, page, edition, and errata.", "human source boundary only", "high", "H2", "M4", True, True),
    ("M1268-X-PROVENANCE", "certificate", "Bind every admitted terminal body to immutable source, license, placeholder, axiom, and trust evidence.", "planned provenance receipt set", "critical", "H2", "M4", False, True),
]

def fp(oid, target):
    if oid == "M1268-ROOT":
        return "lean-expression-sha256:abc6ebd5245bf9c98fb244875d5af316f780b6edf6af146a3ffaf6890bf47c54"
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

rows = []
nodes = []
for oid, kind, human, target, risk, hdebt, mdebt, human_required, readable in specs:
    machine = "not_applicable" if oid in {"M1268-X-SOURCE", "M1268-X-PROVENANCE"} else "required"
    if oid == "M1268-X-PROVENANCE": machine = "informational"
    rows.append({
        "obligation_id": oid, "statement_fingerprint": fp(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "required" if human_required else "not_applicable",
        "readable_eligibility": "required" if readable else "not_applicable",
        "risk_class": risk,
        "exclusion_reason": ("human_source_boundary_only" if oid == "M1268-X-SOURCE" else
            "provenance_overlay_no_proof_credit" if oid == "M1268-X-PROVENANCE" else None),
        "terminal_proof_body_id": None,
    })
    nodes.append({
        "node_id": "THM-M-1268-" + oid.removeprefix("M1268-"), "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": target,
        "output": human, "human_debt": hdebt, "machine_debt": mdebt,
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if human_required else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib-classical/separation-and-choice-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 24 if kind in {"definition", "certificate", "normalization"} else 80,
        "semantic_step_ledger": {"premises": "Only declared typed children and the frozen formal context.", "inference": human, "output": human, "outgoing_use": "Only a declared typed parent edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1268/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen interface or conditional composition only; no open bridge or root proof is supplied.",
        "task_ids": ["S56-M-1268-OBLIGATION_TREE", "S56-M-1268-PROOF"], "owned_sources": [],
        "owner": "THM-M-1268 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if mdebt in {"M0-L", "M1"} else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if mdebt in {"M0-L", "M1"} else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in rows]
denoms = {"inventory": ids, "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"], "required_readable": [r["obligation_id"] for r in rows if r["readable_eligibility"] == "required"], "informational_overlays": ["M1268-X-PROVENANCE"]}
registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-1268-OBLIGATION_TREE", "theorem_id": "THM-M-1268", "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact statement and bounded immutable anchor audit; eligibility selected without observing proof closure.", "frozen_against_statement_sha256": "72cef2c495524a276c2331b103277addc79b9271af24286fbc6c3c84c833ef09", "frozen_against_anchor_audit_sha256": "37444a1286b629a26a56c7029c66fa67c072a235eaadb6776d5cc7b745cb1684", "root_obligation_id": "M1268-ROOT", "denominator_sha256": digest, "frozen_denominators": denoms, "delta_policy": "Any split, merge, correction, exclusion, or eligibility change requires a new version and append-only old/new ID delta.", "obligations": rows}

edge_data = {
 "proof": [("L-CONVEX-SUBLEVEL","T-NORM-TO-WEAK"),("L-NORM-CLOSED","T-NORM-TO-WEAK"),("L-WEAK-CLOSURE","T-NORM-TO-WEAK"),("T-NORM-TO-WEAK","T-ASSEMBLE"),("T-WEAK-TO-NORM","T-ASSEMBLE"),("T-ASSEMBLE","ROOT")],
 "refinement": [("S-DEFINITIONS","ROOT"),("S-BOUNDARIES","ROOT")],
 "provenance": [("X-PROVENANCE", x) for x in ["ROOT","L-CONVEX-SUBLEVEL","L-NORM-CLOSED","L-WEAK-CLOSURE","T-WEAK-TO-NORM","T-ASSEMBLE"]],
 "evidence": [("S-DEFINITIONS","ROOT"),("X-SOURCE","ROOT"),("X-PROVENANCE","ROOT")],
 "trust": [("S-FOUNDATION","ROOT"),("X-PROVENANCE","S-FOUNDATION")],
 "documentation": [(x,"ROOT") for x in ["S-DEFINITIONS","S-BOUNDARIES","S-FOUNDATION","L-CONVEX-SUBLEVEL","L-NORM-CLOSED","L-WEAK-CLOSURE","T-NORM-TO-WEAK","T-WEAK-TO-NORM","T-ASSEMBLE","X-SOURCE","X-PROVENANCE"]],
 "workflow": [("X-SOURCE","X-PROVENANCE"),("X-PROVENANCE","S-FOUNDATION"),("L-CONVEX-SUBLEVEL","L-WEAK-CLOSURE"),("L-WEAK-CLOSURE","T-NORM-TO-WEAK"),("T-NORM-TO-WEAK","T-ASSEMBLE"),("T-WEAK-TO-NORM","T-ASSEMBLE"),("T-ASSEMBLE","ROOT")],
}
graphs = {}
for name, pairs in edge_data.items():
    edges=[]; ins={}; outs={}
    for i,(a,b) in enumerate(pairs,1):
        a="M1268-"+a; b="M1268-"+b; eid=f"{name.upper()}-{i:02d}"
        edges.append({"edge_id":eid,"from":a,"to":b}); outs.setdefault(a,[]).append(eid); ins.setdefault(b,[]).append(eid)
    graphs[name]={"edges":edges,"in":ins,"out":outs}
bundle={"schema_version":"stage1-typed-graphs/1.0","item_id":"S56-M-1268-OBLIGATION_TREE","theorem_id":"THM-M-1268","registry_id":"THM-M-1268-OBLIGATIONS-v1","registry_denominator_sha256":digest,"root_node_id":"M1268-ROOT","edge_direction":"Edges run prerequisite or support node to consumer node; graph type controls whether the edge carries proof credit.","nodes":nodes,"graphs":graphs,"closure_boundary":{"closed_obligations":[],"root_closed":False,"audit_complete":False,"theorem_complete":False,"remaining_root_cut_set":["M1268-L-CONVEX-SUBLEVEL","M1268-L-WEAK-CLOSURE","M1268-T-WEAK-TO-NORM"],"root_machine_debt":"M4"}}
(HERE/"obligation-registry.json").write_text(json.dumps(registry,indent=2)+"\n")
(HERE/"typed-graphs.json").write_text(json.dumps(bundle,indent=2)+"\n")
print(f"generated 12 obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges; denominator {digest}")
