#!/usr/bin/env python3
"""Build the frozen THM-M-0003 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0003-OBLIGATION_TREE"
THEOREM = "THM-M-0003"


def canonical_sha(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


# id, kind, risk, claim, formal target, output, H/M/R, budget
SPECS = [
    ("M0003-ROOT", "root", "critical", "Every snake input in an abelian category yields the exact frozen six-term kernel-to-cokernel sequence.", "Stage1Instances.THM_M_0003.SnakeLemmaTarget", "The exact universally quantified canonical proposition.", "H2", "M1", "R3", 8),
    ("M0003-S-INPUT", "definition", "high", "Freeze the abelian category and the complete SnakeInput package: four rows, three vertical maps, zero composites, kernel/cokernel limits, middle exactness, epi, and mono data.", "CategoryTheory.ShortComplex.SnakeInput", "The exact binder and hypothesis boundary.", "H2", "M1", "R3", 24),
    ("M0003-S-SIX", "definition", "high", "Freeze the six objects and five arrows L0.f, L0.g, delta, L3.f, and L3.g in composableArrows.", "CategoryTheory.ShortComplex.SnakeInput.composableArrows", "The exact six-term sequence interface.", "H2", "M1", "R3", 20),
    ("M0003-S-TRANSPORT", "transport", "normal", "Relate the closed canonical target to its pointwise SnakeInput formulation without changing binders or conclusion.", "Stage1Instances.THM_M_0003.snakeLemmaTarget_iff_pointwise", "A checked bidirectional statement transport.", "H2", "M1", "R3", 12),
    ("M0003-S-FOUNDATION", "certificate", "critical", "Fix the classical choice, quotient, propositional extensionality, kernel, mathlib, and Lean trust boundary.", "planned transitive axiom and TCB report", "An accepted foundation and TCB boundary.", "H2", "M3", "R4", 20),
    ("M0003-C-KERNELS", "construction", "critical", "Extract componentwise kernel witnesses and exact upper column segments from the SnakeInput kernel limit.", "SnakeInput.h₀τ₁/h₀τ₂/h₀τ₃ and exact_C₁_up/exact_C₂_up/exact_C₃_up", "Kernel-side column exactness used in the left half.", "H2", "M1", "R4", 70),
    ("M0003-C-COKERNELS", "construction", "critical", "Extract componentwise cokernel witnesses and exact lower column segments from the SnakeInput cokernel colimit.", "SnakeInput.h₃τ₁/h₃τ₂/h₃τ₃ and exact_C₁_down/exact_C₂_down/exact_C₃_down", "Cokernel-side column exactness used in both halves.", "H2", "M1", "R4", 70),
    ("M0003-L-KERNEL", "core_lemma", "critical", "Prove exactness of the kernel row L0 from the upper component exactness and exactness of L1.", "CategoryTheory.ShortComplex.SnakeInput.L₀_exact", "Exactness of the first two arrows of the six-term sequence.", "H2", "M1", "R4", 55),
    ("M0003-L-COKERNEL", "core_lemma", "critical", "Prove exactness of the cokernel row L3 by dualizing the kernel-row result.", "CategoryTheory.ShortComplex.SnakeInput.L₃_exact", "Exactness of the final two arrows of the six-term sequence.", "H2", "M1", "R4", 20),
    ("M0003-C-PULLBACK", "construction", "critical", "Construct P, phi2, phi1, L0', and its exactness, retaining the factorization invariants needed to descend the connecting map.", "SnakeInput.P/phi₂/phi₁/L₀'/L₀'_exact", "An exact auxiliary complex supporting delta.", "H2", "M1", "R4", 90),
    ("M0003-C-DELTA", "construction", "critical", "Descend phi1 followed by the cokernel map through L0' to construct the connecting morphism delta.", "CategoryTheory.ShortComplex.SnakeInput.δ", "The connecting morphism L0.X3 to L3.X1.", "H2", "M1", "R4", 30),
    ("M0003-C-ZERO", "construction", "high", "Prove L0.g composed with delta and delta composed with L3.f are zero, then form L1' and L2'.", "SnakeInput.L₀_g_δ/δ_L₃_f/L₁'/L₂'", "The two bridge short complexes around delta.", "H2", "M1", "R4", 48),
    ("M0003-L-LEFT", "core_lemma", "critical", "Prove exactness at L0.X3 for the bridge L0.g then delta using refinements and component exactness.", "CategoryTheory.ShortComplex.SnakeInput.L₁'_exact", "Exactness of the left connecting segment.", "H2", "M1", "R4", 82),
    ("M0003-C-DUALITY", "construction", "critical", "Identify delta under passage to the opposite category and transport the right bridge through the pullback/pushout duality isomorphisms.", "SnakeInput.op_δ and SnakeInput.L₂'OpIso", "A checked duality transport from the left bridge to the right bridge.", "H2", "M1", "R4", 75),
    ("M0003-L-RIGHT", "core_lemma", "critical", "Prove exactness at L3.X1 for delta then L3.f by applying the left bridge result in the opposite category.", "CategoryTheory.ShortComplex.SnakeInput.L₂'_exact", "Exactness of the right connecting segment.", "H2", "M1", "R4", 24),
    ("M0003-T-ASSEMBLE", "terminal", "critical", "Compose exactly the four adjacent exact short-complex segments into exactness of the six-term composable arrows.", "Stage1Instances.THM_M_0003.ObligationTree.root_compose", "The pointwise root conditional on the four segment premises.", "H2", "M1", "R3", 16),
    ("M0003-X-UPSTREAM", "certificate", "critical", "Inventory immutable mathlib bodies, direct imports, wrapper/body identity, licenses, and transitive declaration provenance.", "Mathlib.Algebra.Homology.ShortComplex.SnakeLemma at 8a178386", "Body-level provenance; transitive closure remains open.", "H2", "M3", "R4", 30),
    ("M0003-X-SOURCE", "terminal", "high", "Pinpoint and independently review a primary snake-lemma proof, assumptions, sign convention, and errata at every material node.", "primary-source crosswalk remains open", "Human-source coverage without machine proof credit.", "H2", "M5", "R4", 40),
    ("M0003-X-TCB", "certificate", "critical", "Audit Lean, mathlib, axioms, dependency artifacts, unsafe/oracle boundaries, replay, and supply-chain trust transitively.", "Lean 4.29.0; mathlib 8a178386; transitive closure pending", "Release-grade trust inventory without mathematical proof credit.", "H2", "M3", "R4", 35),
]

statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
informational = {"M0003-X-UPSTREAM", "M0003-X-SOURCE", "M0003-X-TCB"}
source_na = {"M0003-S-INPUT", "M0003-S-SIX", "M0003-S-TRANSPORT", "M0003-S-FOUNDATION", "M0003-X-UPSTREAM", "M0003-X-TCB"}
body_ids = {
    "M0003-S-TRANSPORT": "repo:Stage1Instances.THM_M_0003.snakeLemmaTarget_iff_pointwise",
    "M0003-L-KERNEL": "mathlib:8a178386:CategoryTheory.ShortComplex.SnakeInput.L₀_exact",
    "M0003-L-COKERNEL": "mathlib:8a178386:CategoryTheory.ShortComplex.SnakeInput.L₃_exact",
    "M0003-C-DELTA": "mathlib:8a178386:CategoryTheory.ShortComplex.SnakeInput.δ",
    "M0003-L-LEFT": "mathlib:8a178386:CategoryTheory.ShortComplex.SnakeInput.L₁'_exact",
    "M0003-L-RIGHT": "mathlib:8a178386:CategoryTheory.ShortComplex.SnakeInput.L₂'_exact",
    "M0003-T-ASSEMBLE": "repo:Stage1Instances.THM_M_0003.ObligationTree.root_compose",
}

obligations = []
for oid, kind, risk, claim, formal, output, hd, md, rd, budget in SPECS:
    fp = ("lean-expression-sha256:" + expression_hash if oid == "M0003-ROOT" else
          "planned:v1:sha256:" + canonical_sha([oid, claim, formal]))
    machine = "informational" if oid in informational else "required"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": oid not in informational, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "support_overlay_no_proof_credit" if oid in informational else None,
        "terminal_proof_body_id": body_ids.get(oid),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = canonical_sha([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated six-term target and immutable anchor audit determine the input/kernel/cokernel/connecting-map/duality/assembly architecture; eligibility is assigned before proof-phase closure credit.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0003-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "append_only_delta": [], "obligations": obligations,
    "status_observed_after_freeze": {"closed_obligations": [], "root_machine_debt": "M1"},
    "status_boundary": "Frozen scope only; M1 anchor availability is not node closure, accepted evidence, audit completion, or theorem completion.",
}

nodes = []
for spec, obligation in zip(SPECS, obligations):
    oid, kind, risk, claim, formal, output, hd, md, rd, budget = spec
    short = oid.removeprefix("M0003-").lower()
    nodes.append({
        "node_id": "THM-M-0003-" + oid.removeprefix("M0003-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0003-PRIMARY-OPEN" if obligation["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0003-MATHLIB-PARTIAL" if oid in body_ids and "mathlib" in body_ids[oid] else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; observed candidate axioms propext, Classical.choice, Quot.sound; policy acceptance open",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none; no external computation or oracle closes this node",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only typed proof children and the exact SnakeInput context.", "inference": formal, "output": output, "outgoing_use": "Only the declared parent or support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0003/obligation-tree.md#" + short,
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional interface only; no closure or acceptance is credited by this phase.",
        "task_ids": [ITEM, "S56-M-0003-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0003/ObligationTree.lean"] if oid == "M0003-T-ASSEMBLE" else [],
        "owner": "THM-M-0003 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain", "mathlib revision"], "revocation_state": "not-accepted"},
    })


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0003-ROOT": ["M0003-T-ASSEMBLE"],
    "M0003-T-ASSEMBLE": ["M0003-L-KERNEL", "M0003-L-LEFT", "M0003-L-RIGHT", "M0003-L-COKERNEL"],
    "M0003-L-KERNEL": ["M0003-C-KERNELS"],
    "M0003-L-COKERNEL": ["M0003-L-KERNEL", "M0003-C-DUALITY"],
    "M0003-C-DELTA": ["M0003-C-PULLBACK", "M0003-C-COKERNELS"],
    "M0003-C-ZERO": ["M0003-C-DELTA", "M0003-C-PULLBACK"],
    "M0003-L-LEFT": ["M0003-C-ZERO", "M0003-C-KERNELS", "M0003-C-COKERNELS"],
    "M0003-C-DUALITY": ["M0003-C-DELTA", "M0003-C-PULLBACK"],
    "M0003-L-RIGHT": ["M0003-L-LEFT", "M0003-C-DUALITY"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-INPUT", "M0003-ROOT", "logical_decomposition", "M0003-S-INPUT"), edge("REF-ROOT-SIX", "M0003-ROOT", "logical_decomposition", "M0003-S-SIX"), edge("REF-ROOT-TRANSPORT", "M0003-ROOT", "logical_decomposition", "M0003-S-TRANSPORT"), edge("REF-ROOT-FOUND", "M0003-ROOT", "logical_decomposition", "M0003-S-FOUNDATION")],
    "provenance": [edge("PROV-SEGMENTS", "M0003-T-ASSEMBLE", "provenance_of", "M0003-X-UPSTREAM"), edge("PROV-DELTA", "M0003-C-DELTA", "provenance_of", "M0003-X-UPSTREAM"), edge("SRC-ROOT", "M0003-ROOT", "source_map", "M0003-X-SOURCE")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0003-ROOT", "trusts", "M0003-S-FOUNDATION"), edge("TRUST-TCB", "M0003-ROOT", "trusts", "M0003-X-TCB")],
    "documentation": [edge("DOC-ROOT", "M0003-X-SOURCE", "documents", "M0003-ROOT"), edge("DOC-DELTA", "M0003-X-SOURCE", "documents", "M0003-C-DELTA")],
    "workflow": [edge("FLOW-ROOT-ASSEMBLE", "M0003-ROOT", "workflow_depends_on", "M0003-T-ASSEMBLE"), edge("FLOW-ASSEMBLE-PROV", "M0003-T-ASSEMBLE", "workflow_depends_on", "M0003-X-UPSTREAM"), edge("FLOW-ASSEMBLE-TCB", "M0003-T-ASSEMBLE", "workflow_depends_on", "M0003-X-TCB")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for value in edges:
        outgoing.setdefault(value["from"], []).append(value["edge_id"])
        incoming.setdefault(value["to"], []).append(value["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0003-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0003-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M1", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0003-L-KERNEL", "M0003-L-LEFT", "M0003-L-RIGHT", "M0003-L-COKERNEL"], "composition_certificates_checked": ["Stage1Instances.THM_M_0003.ObligationTree.root_compose"], "reason": "The final composition is conditional; upstream M1 candidates and elaboration do not provide accepted node-specific closure."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0003/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid]})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(ids)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
