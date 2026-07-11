#!/usr/bin/env python3
"""Build the frozen THM-M-0005 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0005-OBLIGATION_TREE"
PREFIX = "M0005-"

# id, kind, risk, statement, formal target, H, M, R, budget
SPECS = [
    ("ROOT", "root", "critical", "Construct the natural PID-coefficient Kunneth short exact sequence for every R, X, Y, and n.", "AwesomeTheorems.Stage1.THM_M_0005.KunnethFormula", "H1", "M3", "R3", 12),
    ("SCOPE", "definition", "high", "Retain the frozen universes, PID hypotheses, all degrees, product, direct sums, Tor_1, and two-variable naturality.", "NaturalKunnethSequence field boundary", "H1", "M3", "R3", 16),
    ("CHAIN-FREE", "bridge", "critical", "Establish the projective/free hypotheses required by the algebraic Kunneth argument for singular chains.", "planned: singular chain projectivity", "H1", "M4", "R4", 60),
    ("EZ-MAP", "construction", "critical", "Construct a natural chain comparison from the tensor product of singular chains to chains on X x Y.", "planned: Eilenberg-Zilber map", "H1", "M4", "R4", 80),
    ("EZ-EQUIV", "core_lemma", "critical", "Prove the product comparison is a chain homotopy equivalence and hence a homology isomorphism.", "planned: Eilenberg-Zilber equivalence", "H1", "M4", "R4", 95),
    ("EZ-NAT", "core_lemma", "critical", "Prove the product comparison is natural in maps of both spaces.", "planned: Eilenberg-Zilber naturality", "H1", "M4", "R4", 70),
    ("ALG-MAPS", "construction", "critical", "Construct the tensor inclusion and Tor boundary for the algebraic Kunneth sequence.", "planned: algebraic Kunneth maps", "H1", "M4", "R4", 90),
    ("ALG-ZERO", "core_lemma", "high", "Prove the algebraic Kunneth maps have zero composite.", "planned: Kunneth zero composite", "H1", "M4", "R4", 45),
    ("ALG-EXACT", "core_lemma", "critical", "Prove exactness of the algebraic Kunneth short complex over a PID.", "planned: algebraic Kunneth exactness", "H1", "M4", "R4", 100),
    ("ALG-NAT", "core_lemma", "critical", "Prove algebraic Kunneth naturality in both chain-complex variables.", "planned: algebraic Kunneth naturality", "H1", "M4", "R4", 90),
    ("DIRECT-SUM", "transport", "high", "Identify the graded tensor and Tor terms with the target's Sigma-indexed direct sums.", "TensorTerm; TorTerm", "H1", "M4", "R4", 55),
    ("TOP-MAPS", "transport", "critical", "Transport algebraic maps through Eilenberg-Zilber to the frozen topological inclusion and projection.", "NaturalKunnethSequence.inclusion; projection", "H1", "M4", "R4", 75),
    ("COMPONENTS", "core_lemma", "critical", "Prove tensorMap and torMap agree componentwise with the induced homology maps.", "tensorMap_component; torMap_component", "H1", "M4", "R4", 80),
    ("TOP-NAT", "core_lemma", "critical", "Prove the inclusion and projection naturality equations after transport.", "inclusion_natural; projection_natural", "H1", "M4", "R4", 80),
    ("ASSEMBLE", "terminal", "critical", "Assemble all ten structure fields and then quantify over the coefficient ring.", "ObligationTree.assemble_sequence; root_compose", "H1", "M3", "R3", 20),
    ("X-ATLAS", "provenance", "high", "Track the closest external architecture without importing its placeholder-bearing bodies.", "atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50", "H1", "M5", "R4", 25),
    ("X-SOURCE", "documentation", "high", "Pinpoint and review a primary proof source, assumptions, and errata for every material node.", "source crosswalk remains open", "H1", "M5", "R4", 30),
    ("X-TCB", "trust", "high", "Audit terminal bodies, axioms, toolchain, dependencies, and reproducibility closure.", "Lean 4.29.0; mathlib 8a178386; release audit open", "H1", "M3", "R4", 25),
]

def oid(short):
    return PREFIX + short

informational = {"X-ATLAS", "X-SOURCE", "X-TCB"}
statement_hash = hashlib.sha256((HERE / "KunnethStatement.lean").read_bytes()).hexdigest()
rows = []
for short, kind, risk, human, formal, hd, md, rd, budget in SPECS:
    fp_source = statement_hash if short in {"ROOT", "SCOPE"} else hashlib.sha256((human + "\n" + formal).encode()).hexdigest()
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": "sha256:" + fp_source,
        "kind": kind, "root_relevant": short not in informational,
        "machine_eligibility": "informational" if short in informational else "required",
        "human_source_eligibility": "required" if short not in {"SCOPE", "X-ATLAS", "X-TCB"} else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": "repo:AwesomeTheorems.Stage1.THM_M_0005.ObligationTree" if short == "ASSEMBLE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-0005",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated target and anchor audit fix this chain/algebraic/topological architecture before proof closure is observed.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor_candidates.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, eligibility, risk, or exclusion change requires registry version 2 with an append-only delta.",
    "obligations": rows,
}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-0005-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0005-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0005-ATLAS" if short in {"EZ-MAP", "EZ-EQUIV", "EZ-NAT", "ALG-MAPS", "ALG-EXACT", "ALG-NAT"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; no local axiom or placeholder admitted",
        "tcb_profile": "Lean 4.29.0; mathlib 8a178386; release closure open", "computation_record": "none",
        "step_budget": budget, "semantic_step_ledger": {"premises": ["typed children"], "inference": formal, "output": human, "outgoing_use": "typed parent edge or root"},
        "public_readable_target": "Stage1_Instances/THM-M-0005/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M0005-" + short, "status_boundary": "Architecture only; no proof closure is credited.",
        "task_ids": [ITEM, "S56-M-0005-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0005/obligation-registry.json", "Stage1_Instances/THM-M-0005/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain", "mathlib revision"], "revocation_state": "not-accepted"},
    })

def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [
    ("ROOT", "ASSEMBLE"), ("ASSEMBLE", "TOP-MAPS"), ("ASSEMBLE", "COMPONENTS"), ("ASSEMBLE", "TOP-NAT"),
    ("TOP-MAPS", "ALG-MAPS"), ("TOP-MAPS", "ALG-ZERO"), ("TOP-MAPS", "ALG-EXACT"),
    ("TOP-MAPS", "DIRECT-SUM"), ("TOP-MAPS", "EZ-EQUIV"), ("COMPONENTS", "ALG-NAT"),
    ("COMPONENTS", "DIRECT-SUM"), ("TOP-NAT", "ALG-NAT"), ("TOP-NAT", "EZ-NAT"),
    ("ALG-MAPS", "CHAIN-FREE"), ("ALG-EXACT", "CHAIN-FREE"), ("ALG-NAT", "CHAIN-FREE"),
    ("EZ-EQUIV", "EZ-MAP"), ("EZ-NAT", "EZ-MAP"),
]
proof_edges = []
for parent, child in proof_pairs:
    fwd, rev = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [{"edge_id": fwd, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": rev}, {"edge_id": rev, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": fwd}]

def simple(prefix, typ, pairs):
    return graph([{"edge_id": f"{prefix}-{a}-{b}", "from": oid(a), "type": typ, "to": oid(b)} for a, b in pairs])

graphs = {
    "proof": graph(proof_edges),
    "refinement": simple("REFINE", "logical_decomposition", [("ROOT", "SCOPE"), ("SCOPE", "DIRECT-SUM")]),
    "provenance": simple("PROV", "provenance_of", [(x, "X-ATLAS") for x in ("EZ-MAP", "EZ-EQUIV", "EZ-NAT", "ALG-MAPS", "ALG-EXACT", "ALG-NAT")]),
    "evidence": simple("EVID", "evidence_for", [("ASSEMBLE", "X-ATLAS")]),
    "trust": simple("TRUST", "trusts", [("ROOT", "X-TCB")]),
    "documentation": simple("DOC", "documents", [("ROOT", "X-SOURCE")]),
    "workflow": simple("FLOW", "workflow_depends_on", [("ROOT", "ASSEMBLE"), ("ASSEMBLE", "TOP-MAPS"), ("ASSEMBLE", "COMPONENTS"), ("ASSEMBLE", "TOP-NAT")]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0005",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M3", "remaining_root_cut_set": [oid(x) for x in ("CHAIN-FREE", "EZ-MAP", "EZ-EQUIV", "EZ-NAT", "ALG-MAPS", "ALG-ZERO", "ALG-EXACT", "ALG-NAT", "DIRECT-SUM", "COMPONENTS", "TOP-NAT")], "composition_certificates_checked": ["AwesomeTheorems.Stage1.THM_M_0005.ObligationTree.assemble_sequence", "AwesomeTheorems.Stage1.THM_M_0005.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False},
}
recipes = [{"recipe_id": "VAL-M0005-" + s[0], "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0005/ObligationTree.lean"], "env": {"LEAN_PATH": "temporary olean directory containing KunnethStatement.olean"}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(s[0])]} for s in SPECS]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0005", "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
