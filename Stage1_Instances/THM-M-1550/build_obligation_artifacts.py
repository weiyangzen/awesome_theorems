#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1550-OBLIGATION_TREE"
PREFIX = "M1550"

specs = [
    ("M1550-ROOT", "root", "The exact frozen conditional Lax-pair isospectrality proposition.", "Stage1Instances.THM_M_1550.LaxPairIsospectrality", "critical", "split-required"),
    ("M1550-S-EXACT", "definition", "Retain the universe, finite matrix model, real time domain, ordered binders, hypotheses, and spectrum conclusion.", "Stage1Instances.THM_M_1550.LaxPairIsospectrality", "high", 14),
    ("M1550-S-LAX", "definition", "Retain the Lax-equation premise even though the supplied conjugating evolution makes it logically redundant for this root.", "Stage1Instances.THM_M_1550.LaxEquationOn L P timeDomain", "high", 6),
    ("M1550-B-TIMES", "branch", "For arbitrary t0 and t in the time domain, specialize the conjugating-evolution hypothesis.", "ConjugatingEvolutionOn L timeDomain -> ConjugatesAt L t0 t", "high", 5),
    ("M1550-C-WITNESS", "construction", "Unpack ConjugatesAt to obtain a unit U and the exact matrix equality L t = U * L t0 * U^-1.", "Stage1Instances.THM_M_1550.ConjugatesAt L t0 t", "critical", 7),
    ("M1550-L-SPECTRUM", "core_lemma", "Transport the exact conjugation equality through spectrum.units_conjugate.", "spectrum.units_conjugate", "critical", 12),
    ("M1550-T-ASSEMBLE", "terminal", "Compose the time specialization and spectrum leaf into the exact frozen root.", "Stage1Instances.THM_M_1550.ObligationTree.root_compose", "critical", 5),
    ("M1550-X-PROVENANCE", "provenance", "Resolve wrapper, terminal proof body, imports, and transitive declaration identity.", "structured provenance packet", "high", 35),
    ("M1550-X-SOURCE", "human_source", "Pinpoint the primary Lax source and map the conservative strengthening and every material transition.", "reviewed source crosswalk", "high", 45),
    ("M1550-X-TCB", "trust", "Close the axiom, artifact, toolchain, dependency, replay, and supply-chain trust boundary.", "accepted TCB closure", "high", 55),
]

def fingerprint(oid, statement, target):
    raw = f"THM-M-1550\n{oid}\n{statement}\n{target}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(raw).hexdigest()

overlays = {"provenance", "human_source", "trust"}
human_required = {"M1550-ROOT", "M1550-S-LAX", "M1550-B-TIMES", "M1550-C-WITNESS", "M1550-L-SPECTRUM", "M1550-T-ASSEMBLE", "M1550-X-SOURCE"}
terminal_ids = {
    "M1550-L-SPECTRUM": "mathlib:8a178386:spectrum.units_conjugate",
    "M1550-T-ASSEMBLE": "repo:Stage1Instances.THM_M_1550.ObligationTree.root_compose",
}
obligations = []
nodes = []
for oid, kind, statement, target, risk, budget in specs:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint(oid, statement, target),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "informational" if kind in overlays else "required",
        "human_source_eligibility": "required" if oid in human_required else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": None,
        "terminal_proof_body_id": terminal_ids.get(oid),
    })
    nodes.append({
        "node_id": "THM-M-1550-" + oid.removeprefix(PREFIX + "-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": statement,
        "formal_target": target,
        "output": statement,
        "human_debt": "H1" if oid in human_required else "H1",
        "machine_debt": "M1" if oid in {"M1550-L-SPECTRUM", "M1550-T-ASSEMBLE"} else "M3",
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "source_statement_crosswalk.md" if oid in human_required else "not-applicable",
        "provenance_id": "anchor-audit.json" if oid == "M1550-L-SPECTRUM" else "pending-transitive-provenance",
        "foundation_profile": "Lean 4 dependent type theory; accepted classical/choice policy pending",
        "tcb_profile": "Lean 4.29.0 + mathlib 8a178386; transitive release closure pending",
        "computation_record": "none; no native computation, oracle, or external solver",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children shown in proof/refinement graphs"], "inference": target, "output": statement, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-1550/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid + "-PENDING",
        "status_boundary": "Architecture only; no obligation receives accepted proof, source, readability, trust, or release closure in this phase.",
        "task_ids": [ITEM, "S56-M-1550-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1550/ObligationTree.lean"] if oid == "M1550-T-ASSEMBLE" else [],
        "owner": "THM-M-1550 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "graphs", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row[0] for row in specs]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-1550", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated target and anchor audit were fixed before this denominator. Eligibility follows semantic role and assigns zero closure credit.",
    "frozen_against_statement_sha256": "06bf95d6ab99a8104283895708b151324e761530d80e8ec00c5fda20bdfca744",
    "frozen_against_anchor_audit_sha256": "f16ece9a452a4c3077e120357cf79a42c72de735b81f6636663cd3b4c5fae75c",
    "root_obligation_id": "M1550-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 with an append-only ID delta.",
    "anti_inflation": "Aliases, wrappers, transports, and overlays cannot create distinct semantic or terminal-body proof credit.",
    "obligations": obligations,
}

edge_specs = {
    "proof": [("M1550-ROOT", "M1550-T-ASSEMBLE", "proof_requires"), ("M1550-T-ASSEMBLE", "M1550-B-TIMES", "proof_requires"), ("M1550-T-ASSEMBLE", "M1550-L-SPECTRUM", "proof_requires"), ("M1550-B-TIMES", "M1550-C-WITNESS", "proof_requires")],
    "refinement": [("M1550-ROOT", "M1550-S-EXACT", "logical_decomposition"), ("M1550-S-EXACT", "M1550-S-LAX", "logical_decomposition")],
    "provenance": [("M1550-X-PROVENANCE", "M1550-L-SPECTRUM", "provenance_of"), ("M1550-X-PROVENANCE", "M1550-T-ASSEMBLE", "provenance_of")],
    "evidence": [("M1550-X-PROVENANCE", "M1550-ROOT", "evidence_for")],
    "trust": [("M1550-X-TCB", x, "trusts") for x in ("M1550-ROOT", "M1550-L-SPECTRUM", "M1550-T-ASSEMBLE")],
    "documentation": [("M1550-X-SOURCE", x, "documents") for x in ("M1550-ROOT", "M1550-S-LAX", "M1550-B-TIMES", "M1550-C-WITNESS", "M1550-L-SPECTRUM")],
    "workflow": [("M1550-S-EXACT", "M1550-T-ASSEMBLE", "workflow_depends_on"), ("M1550-X-PROVENANCE", "M1550-X-TCB", "workflow_depends_on")],
}
graphs = {}
for name, triples in edge_specs.items():
    edges, outgoing, incoming = [], {}, {}
    for i, (src, dst, relation) in enumerate(triples, 1):
        eid = f"M1550-{name.upper()}-{i:02d}"
        edges.append({"edge_id": eid, "from": src, "to": dst, "relation": relation})
        outgoing.setdefault(src, []).append(eid)
        incoming.setdefault(dst, []).append(eid)
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1550",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1550-L-SPECTRUM"], "composition_certificate": "ObligationTree.root_compose is conditional on SpectrumUnderConjugation and supplies no leaf or root closure."},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(obligations)} obligations; denominator sha256: {denominator}")
