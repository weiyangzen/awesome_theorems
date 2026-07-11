#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0081-OBLIGATION_TREE"

specs = [
    ("M0081-ROOT", "root", "The exact canonical iff for contravariant representables.", "Stage1Instances.THM_M_0081.CanonicalTarget C X Y", "M4", "high", "split-required"),
    ("M0081-S-EXACT", "statement", "Retain the universes, category, objects, variance, and Nonempty encoding of the frozen target.", "Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y)", "M4", "medium", 6),
    ("M0081-B-REFLECT", "bridge", "Reflect a natural isomorphism of representables to an object isomorphism.", "Reflection C X Y", "M4", "high", 12),
    ("M0081-L-FF", "imported_theorem", "Establish that the Yoneda embedding is fully faithful.", "CategoryTheory.Yoneda.fullyFaithful", "M4", "high", 35),
    ("M0081-L-PREIMAGE", "imported_theorem", "A fully faithful functor reflects an isomorphism via preimageIso.", "CategoryTheory.Functor.FullyFaithful.preimageIso", "M4", "high", 30),
    ("M0081-B-PRESERVE", "bridge", "Map an object isomorphism to a natural isomorphism of representables.", "Preservation C X Y", "M4", "medium", 8),
    ("M0081-L-MAPISO", "imported_theorem", "A functor maps an isomorphism to an isomorphism.", "CategoryTheory.Functor.mapIso", "M4", "medium", 20),
    ("M0081-T-ASSEMBLE", "composition", "Compose the reflection and preservation implications into the exact iff.", "Stage1Instances.THM_M_0081.ObligationTree.root_compose", "M4", "medium", 3),
    ("M0081-X-PROVENANCE", "provenance", "Resolve unique terminal bodies, declarations, imports, and wrapper identity.", "structured provenance packet", "M3", "high", 40),
    ("M0081-X-SOURCE", "human_source", "Pinpoint primary-source theorem, edition, assumptions, page, and errata mappings.", "reviewed source crosswalk", "M5", "high", 50),
    ("M0081-X-TCB", "trust", "Close transitive declarations, axioms, artifacts, dependency pins, and replay trust.", "accepted TCB closure", "M3", "high", 60),
]

def fingerprint(oid, statement, target):
    raw = f"THM-M-0081\n{oid}\n{statement}\n{target}".encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()

obligations = []
nodes = []
for oid, kind, statement, target, machine, risk, budget in specs:
    overlay = kind in {"provenance", "human_source", "trust"}
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint(oid, statement, target),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "informational" if overlay else "required",
        "human_source_eligibility": "required" if oid in {"M0081-ROOT", "M0081-B-REFLECT", "M0081-B-PRESERVE", "M0081-L-FF", "M0081-L-PREIMAGE", "M0081-L-MAPISO", "M0081-X-SOURCE"} else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None,
        "terminal_proof_body_id": ({
            "M0081-L-FF": "mathlib:CategoryTheory.Yoneda.fullyFaithful",
            "M0081-L-PREIMAGE": "mathlib:CategoryTheory.Functor.FullyFaithful.preimageIso",
            "M0081-L-MAPISO": "mathlib:CategoryTheory.Functor.mapIso",
            "M0081-T-ASSEMBLE": "local:ObligationTree.root_compose",
        }.get(oid)),
    })
    nodes.append({
        "node_id": "THM-M-0081-" + oid.removeprefix("M0081-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": statement,
        "formal_target": target,
        "output": statement,
        "human_debt": "H2",
        "machine_debt": machine,
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md" if oid in {"M0081-ROOT", "M0081-X-SOURCE"} else "pending-node-crosswalk",
        "provenance_id": "anchor-audit.json" if oid.startswith("M0081-L-") else "pending-transitive-provenance",
        "foundation_profile": "Lean 4 dependent type theory; accepted axiom policy pending",
        "tcb_profile": "Lean 4.29.0 + mathlib 8a178386; transitive closure pending",
        "computation_record": "none; structural categorical construction",
        "step_budget": budget,
        "semantic_step_ledger": f"Freeze inputs for {statement} Check the named formal interface {target}. Produce only the stated output and pass it through typed edges. Do not infer closure from anchor availability.",
        "public_readable_target": "Stage1_Instances/THM-M-0081/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid + "-PENDING",
        "status_boundary": "Architecture only; this node has no accepted proof, source, readability, trust, or release receipt.",
        "task_ids": [ITEM, "S56-M-0081-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0081/ObligationTree.lean"] if oid == "M0081-T-ASSEMBLE" else [],
        "owner": "THM-M-0081 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,graph,toolchain,source-map change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row[0] for row in specs]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-0081", "registry_version": 1,
    "freeze_basis": "The canonical statement and immutable anchor audit were read first; eligibility and denominator are frozen with zero closure credit before the proof phase.",
    "root_obligation_id": "M0081-ROOT",
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
    },
    "denominator_sha256": denominator,
    "exclusions": [],
    "anti_inflation": "Wrappers, aliases, statement transports, and graph overlays receive no distinct terminal-body proof credit.",
    "obligations": obligations,
}

edge_specs = {
    "proof": [("M0081-ROOT", "M0081-T-ASSEMBLE", "requires"), ("M0081-T-ASSEMBLE", "M0081-B-REFLECT", "requires"), ("M0081-T-ASSEMBLE", "M0081-B-PRESERVE", "requires"), ("M0081-B-REFLECT", "M0081-L-FF", "requires"), ("M0081-B-REFLECT", "M0081-L-PREIMAGE", "requires"), ("M0081-B-PRESERVE", "M0081-L-MAPISO", "requires")],
    "refinement": [("M0081-ROOT", "M0081-S-EXACT", "refines")],
    "provenance": [("M0081-X-PROVENANCE", x, "records_terminal_body") for x in ("M0081-L-FF", "M0081-L-PREIMAGE", "M0081-L-MAPISO", "M0081-T-ASSEMBLE")],
    "evidence": [("M0081-X-PROVENANCE", "M0081-ROOT", "supports_future_receipt")],
    "trust": [("M0081-X-TCB", x, "governs") for x in ("M0081-ROOT", "M0081-L-FF", "M0081-L-PREIMAGE", "M0081-L-MAPISO")],
    "documentation": [("M0081-X-SOURCE", x, "documents") for x in ("M0081-ROOT", "M0081-B-REFLECT", "M0081-B-PRESERVE")],
    "workflow": [("M0081-S-EXACT", "M0081-T-ASSEMBLE", "precedes"), ("M0081-X-PROVENANCE", "M0081-X-TCB", "precedes")],
}
graphs = {}
for name, triples in edge_specs.items():
    edges, outgoing, incoming = [], {}, {}
    for i, (src, dst, relation) in enumerate(triples, 1):
        eid = f"M0081-{name.upper()}-{i:02d}"
        edges.append({"edge_id": eid, "from": src, "to": dst, "relation": relation})
        outgoing.setdefault(src, []).append(eid)
        incoming.setdefault(dst, []).append(eid)
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0081",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [], "root_machine_debt": "M4", "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M0081-B-REFLECT", "M0081-B-PRESERVE"],
        "composition_certificate": "ObligationTree.root_compose is conditional and gives no premise closure.",
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote 11 obligations; denominator sha256: {denominator}")
