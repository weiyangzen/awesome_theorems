#!/usr/bin/env python3
"""Build the frozen THM-M-1091 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1091-OBLIGATION_TREE"
PREFIX = "M1091-"

# short id, kind, risk, statement, formal target, output, H/M/R, semantic step budget
SPECS = [
    ("ROOT", "root", "critical", "For every homogeneous discrete-time Markov kernel and natural m,n, the (m+n)-step kernel is the n-step kernel composed after the m-step kernel.", "Stage1Instances.THM_M_1091.ChapmanKolmogorovTarget", "The exact frozen kernel equality.", "H1", "M1", "R3", 5),
    ("S-CONTEXT", "definition", "high", "Fix an arbitrary measurable State, a Markov endokernel kappa, and natural step counts m,n, with no finiteness or nonemptiness premise.", "State; MeasurableSpace State; kappa : Kernel State State; IsMarkovKernel kappa; m n : Nat", "The exact binder, typeclass, and degenerate-case policy.", "H1", "M3", "R3", 8),
    ("S-ORIENTATION", "definition", "critical", "Read kernel composition chronologically: kappa^m acts first and kappa^n acts second.", "kappa^(m+n) = (kappa^n) comp (kappa^m)", "The frozen composition direction and index naming.", "H1", "M3", "R3", 6),
    ("S-INTEGRAL", "transport", "high", "Transport the kernel equality to its setwise lintegral form for every measurable target set.", "Stage1Instances.THM_M_1091.target_iff_integralTarget", "A checked bidirectional alternate encoding.", "H1", "M1", "R3", 12),
    ("N-ADD", "normalization", "high", "Swap the anchor indices and normalize n+m to m+n without changing composition order.", "add_comm n m", "The exact arithmetic normalization used by root composition.", "H1", "M1", "R3", 5),
    ("B-ZERO", "branch", "normal", "Cover both m=0 and n=0 identity-kernel boundaries.", "zero_first_boundary; zero_second_boundary", "Checked zero-step boundary theorems.", "H1", "M1", "R3", 8),
    ("C-POWCOMP", "construction", "high", "Interpret kernel powers as iterated kernel composition with power zero equal to the identity kernel.", "HPow.hPow kappa Nat; Kernel.id; Kernel.comp", "The construction semantics required by the semigroup equation.", "H1", "M3", "R4", 12),
    ("L-POWADD", "bridge", "critical", "Obtain the central power-add law for endokernels at arbitrary indices a,b.", "ProbabilityTheory.Kernel.pow_add", "kappa^(a+b) = (kappa^a) comp (kappa^b).", "H1", "M1", "R4", 18),
    ("T-ASSEMBLE", "terminal", "critical", "Instantiate the power-add child at n,m and use addition commutativity to yield the exact root.", "Stage1Instances.THM_M_1091_Obligations.compose_root", "The exact root conditionally composed from its required child and normalization.", "H1", "M1", "R3", 8),
    ("X-PROVENANCE", "terminal", "high", "Bind the central bridge to the pinned mathlib declaration, revision, source body, and axiom inventory.", "Mathlib.Probability.Kernel.Composition.Comp@8a178386:Kernel.pow_add", "Body-level provenance without duplicate wrapper credit.", "H1", "M3", "R4", 10),
    ("X-TCB", "certificate", "high", "Record Lean, mathlib, classical measure-theory, axiom, and reproducibility trust boundaries.", "Lean 4.29.0; mathlib 8a178386; release trust closure pending", "A release-gated trust overlay.", "H1", "M3", "R4", 10),
    ("W-FOLLOWUP", "certificate", "high", "Order proof adoption, node validation, trust replay, readable reconstruction, and release review.", "S56-M-1091-PROOF -> VALIDATION -> RELEASE", "A workflow-only gate with no mathematical credit.", "H1", "M5", "R4", 6),
]


def oid(short):
    return PREFIX + short


statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
informational = {"X-PROVENANCE", "X-TCB", "W-FOLLOWUP"}
no_human = {"S-CONTEXT", "N-ADD", "B-ZERO", "X-PROVENANCE", "X-TCB", "W-FOLLOWUP"}
body_ids = {
    "S-INTEGRAL": "repo:Stage1Instances.THM_M_1091.target_iff_integralTarget",
    "L-POWADD": "mathlib:8a178386:ProbabilityTheory.Kernel.pow_add",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_1091_Obligations.compose_root",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fingerprint = ("lean-expression-sha256:" + expression_hash if short == "ROOT" else
                   "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest())
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": short not in informational,
        "machine_eligibility": "informational" if short in informational else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "assurance_overlay_no_distinct_proof_credit" if short in informational else None,
        "terminal_proof_body_id": body_ids.get(short),
    })

projection = [{key: row[key] for key in row} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-1091", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact statement and immutable anchor audit determine the architecture and eligibility before proof-phase closure credit is observed.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility, or risk change requires a new version and an append-only old/new ID delta.",
    "obligations": rows,
}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    source_id = "SRC-M1091-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable"
    provenance_id = "PROV-M1091-MATHLIB-POWADD" if short in {"L-POWADD", "X-PROVENANCE"} else "none"
    nodes.append({
        "node_id": "THM-M-1091-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": source_id, "provenance_id": provenance_id,
        "foundation_profile": "Lean 4 dependent type theory plus pinned mathlib measure theory; observed candidate axioms are propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": [{
            "premises": "the exact context and typed children named by this node",
            "inference": formal, "output": output,
            "outgoing_use": "the typed parent edge or frozen root result",
        }],
        "public_readable_target": "Stage1_Instances/THM-M-1091/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M1091-" + short,
        "status_boundary": "Architecture only; this phase does not credit the obligation closed or accepted.",
        "task_ids": [ITEM, "S56-M-1091-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1091"],
        "owner": "THM-M-1091 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "typed edges", "anchor provenance", "toolchain"], "revocation_state": "not-accepted"},
    })


def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}


proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "L-POWADD"), ("T-ASSEMBLE", "N-ADD")]
proof_edges = []
for parent, child in proof_pairs:
    fwd, rev = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [
        {"edge_id": fwd, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": rev},
        {"edge_id": rev, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": fwd},
    ]
refine_pairs = [("ROOT", "S-CONTEXT"), ("ROOT", "S-ORIENTATION"), ("ROOT", "S-INTEGRAL"), ("ROOT", "B-ZERO"), ("L-POWADD", "C-POWCOMP")]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refine_pairs]),
    "provenance": graph([{"edge_id": "PROV-POWADD-BODY", "from": oid("L-POWADD"), "type": "provenance_of", "to": oid("X-PROVENANCE")}]),
    "evidence": graph([{"edge_id": "EVID-ROOT-PROVENANCE", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-PROVENANCE")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-INTEGRAL", "from": oid("ROOT"), "type": "documents", "to": oid("S-INTEGRAL")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-FOLLOWUP", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("W-FOLLOWUP")}]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1091",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_metrics_observed": False,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M1", "remaining_root_cut_set": [oid("L-POWADD")], "composition_certificates_checked": ["Stage1Instances.THM_M_1091_Obligations.compose_root"], "audit_complete": False, "theorem_complete": False},
}
recipes = [{
    "recipe_id": "VAL-M1091-" + spec[0], "cwd": "Formalizations/Lean",
    "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-1091/ObligationTree.lean"],
    "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0,
    "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "capture_exact"}],
    "covered_obligation_ids": [oid(spec[0])],
    "covered_declarations": ["Stage1Instances.THM_M_1091_Obligations.compose_root"],
} for spec in SPECS]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1091", "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
