#!/usr/bin/env python3
"""Build the frozen THM-M-0009 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0009-OBLIGATION_TREE"
PREFIX = "M0009-"
REV = "8a178386"

# short id, kind, risk, statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "Every short exact sequence in an abelian category with Ext induces both universally indexed variance branches of the long exact Ext sequence.", "Stage1Instances.THM_M_0009.LongExactExtSequenceTarget", "The exact frozen conjunction.", "H2", "M1", "R4", 8),
    ("S-BINDERS", "definition", "high", "Preserve the arbitrary category, Abelian and HasExt instances, objects, short complex, ShortExact witness, and natural degree binders.", "Stage1Instances.THM_M_0009.LongExactExtSequenceTarget", "The exact quantified boundary.", "H2", "M3", "R3", 14),
    ("S-TRANSPORT", "transport", "normal", "Relate the conjunction to the two separately named variance propositions without changing scope.", "Stage1Instances.THM_M_0009.longExactExtSequenceTarget_iff_variance_branches", "A checked bidirectional transport.", "H2", "M1", "R3", 12),
    ("S-FOUNDATION", "certificate", "high", "Fix the kernel, classical, quotient, extensionality, dependency, and executable trust boundary.", "#print axioms root_compose and both terminal candidates", "A versioned foundation boundary.", "H2", "M3", "R4", 16),
    ("N-VARIANCE", "normalization", "high", "Split the root into covariant Ext in the second argument and contravariant Ext in the first argument.", "CovariantBranch and ContravariantBranch", "Two non-overlapping branch interfaces.", "H2", "M3", "R3", 14),
    ("B-COV", "branch", "critical", "For every short exact sequence, fixed X, and successive degrees, prove exactness of the covariant six-arrow window.", "ObligationTree.CovariantBranch", "The complete covariant branch.", "H2", "M1", "R4", 24),
    ("B-CONTRA", "branch", "critical", "For every short exact sequence, fixed Y, and successive degrees, prove exactness of the contravariant six-arrow window.", "ObligationTree.ContravariantBranch", "The complete contravariant branch.", "H2", "M1", "R4", 24),
    ("C-COV-SEQ", "construction", "high", "Construct the covariant composable-arrow window and its connecting morphisms at arbitrary successive degrees.", "CategoryTheory.Abelian.Ext.covariantSequence", "A well-typed covariant exactness input.", "H2", "M1", "R4", 36),
    ("C-CONTRA-SEQ", "construction", "high", "Construct the contravariant composable-arrow window and its connecting morphisms at arbitrary successive degrees.", "CategoryTheory.Abelian.Ext.contravariantSequence", "A well-typed contravariant exactness input.", "H2", "M1", "R4", 36),
    ("L-COV-EXACT", "core_lemma", "critical", "Establish exactness of every covariant window.", "CategoryTheory.Abelian.Ext.covariantSequence_exact", "CovariantBranch.", "H2", "M1", "R4", 48),
    ("L-CONTRA-EXACT", "core_lemma", "critical", "Establish exactness of every contravariant window.", "CategoryTheory.Abelian.Ext.contravariantSequence_exact", "ContravariantBranch.", "H2", "M1", "R4", 48),
    ("T-ASSEMBLE", "terminal", "critical", "Consume exactly the two variance branch premises and assemble the canonical root.", "Stage1Instances.THM_M_0009.ObligationTree.root_compose", "The conditional exact root.", "H2", "M1", "R3", 8),
    ("X-UPSTREAM", "provenance_boundary", "high", "Record the pinned mathlib source, terminal declarations, dependencies, and proof-body identities.", "Mathlib Ext.ExactSequences at " + REV, "Formal provenance for both branch bodies.", "H2", "M3", "R4", 24),
    ("X-SOURCE", "source_boundary", "high", "Pinpoint and independently review a primary mathematical source for both variance branches.", "primary source crosswalk remains open", "Human-source mappings for material nodes.", "H2", "M5", "R4", 24),
    ("X-TCB", "trust_boundary", "high", "Audit the transitive Lean, mathlib, compiled-artifact, axiom, and executable trust closure.", "Lean 4.29.0; mathlib " + REV + "; transitive audit open", "Release-grade trust inventory.", "H2", "M3", "R4", 24),
]

def oid(short): return PREFIX + short
def digest(data): return hashlib.sha256(data).hexdigest()

statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
informational = {"X-UPSTREAM", "X-SOURCE", "X-TCB"}
no_human = {"S-BINDERS", "S-TRANSPORT", "S-FOUNDATION", "X-UPSTREAM", "X-TCB"}
bodies = {
    "S-TRANSPORT": "repo:Stage1Instances.THM_M_0009.longExactExtSequenceTarget_iff_variance_branches",
    "L-COV-EXACT": f"mathlib:{REV}:CategoryTheory.Abelian.Ext.covariantSequence_exact",
    "L-CONTRA-EXACT": f"mathlib:{REV}:CategoryTheory.Abelian.Ext.contravariantSequence_exact",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0009.ObligationTree.root_compose",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fp = "lean-expression-sha256:" + expression_hash if short in {"ROOT", "S-BINDERS"} else "planned:v1:sha256:" + digest((human + "\n" + formal).encode())
    rows.append({"obligation_id": oid(short), "statement_fingerprint": fp, "kind": kind,
        "root_relevant": short not in informational,
        "machine_eligibility": "informational" if short in informational else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": bodies.get(short)})
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest(json.dumps([{k: r[k] for k in fields} for r in rows], sort_keys=True, separators=(",", ":")).encode())
ids = [r["obligation_id"] for r in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-0009", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated target and immutable anchor audit determine the variance/construction/lemma/assembly architecture before proof closure is observed.",
    "frozen_against_statement_sha256": digest((HERE / "statement.json").read_bytes()),
    "frozen_against_anchor_audit_sha256": digest((HERE / "anchor-audit.json").read_bytes()),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"]},
    "delta_policy": "Any split, merge, eligibility, exclusion, or risk change requires version 2 and an append-only old/new ID delta.", "obligations": rows}

recipe_ids = {oid(s[0]): "VAL-M0009-" + s[0] for s in SPECS}
nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({"node_id": "THM-M-0009-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0009-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0009-MATHLIB" if short in {"C-COV-SEQ", "C-CONTRA-SEQ", "L-COV-EXACT", "L-CONTRA-EXACT"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; observed candidate axioms: propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open", "computation_record": "none",
        "step_budget": budget, "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0009/obligation-tree.md#" + short.lower(), "validation_spec_id": recipe_ids[oid(short)],
        "status_boundary": "Architecture only; this node receives no closure credit in this phase.", "task_ids": [ITEM, "S56-M-0009-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0009/obligation-registry.json", "Stage1_Instances/THM-M-0009/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"}})

def graph(edges):
    out, incoming = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "L-COV-EXACT"), ("T-ASSEMBLE", "L-CONTRA-EXACT"), ("L-COV-EXACT", "B-COV"), ("L-COV-EXACT", "C-COV-SEQ"), ("L-CONTRA-EXACT", "B-CONTRA"), ("L-CONTRA-EXACT", "C-CONTRA-SEQ")]
proof_edges = []
for parent, child in proof_pairs:
    f, r = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [{"edge_id": f, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": r}, {"edge_id": r, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": f}]
refine = [("ROOT", "S-BINDERS"), ("S-BINDERS", "S-TRANSPORT"), ("S-BINDERS", "S-FOUNDATION"), ("ROOT", "N-VARIANCE"), ("N-VARIANCE", "B-COV"), ("N-VARIANCE", "B-CONTRA")]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refine]),
    "provenance": graph([{"edge_id": f"PROV-{s}", "from": oid(s), "type": "provenance_of", "to": oid("X-UPSTREAM")} for s in ("C-COV-SEQ", "C-CONTRA-SEQ", "L-COV-EXACT", "L-CONTRA-EXACT")] + [{"edge_id": f"SOURCE-{s}", "from": oid(s), "type": "source_map", "to": oid("X-SOURCE")} for s in ("ROOT", "B-COV", "B-CONTRA", "L-COV-EXACT", "L-CONTRA-EXACT")]),
    "evidence": graph([{"edge_id": "EVID-ROOT-UPSTREAM", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-UPSTREAM")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}])}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0009", "registry_denominator_sha256": denominator,
    "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M1",
    "remaining_root_cut_set": [oid("L-COV-EXACT"), oid("L-CONTRA-EXACT")], "composition_certificates_checked": ["Stage1Instances.THM_M_0009.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False}}
argv = ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0009/ObligationTree.lean"]
recipes = [{"recipe_id": rid, "cwd": "Formalizations/Lean", "argv": argv, "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0,
    "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "normalized Lean diagnostics"}], "covered_obligation_ids": [ob], "covered_declarations": ["Stage1Instances.THM_M_0009.ObligationTree.root_compose"]} for ob, rid in recipe_ids.items()]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0009", "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
