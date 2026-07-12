#!/usr/bin/env python3
"""Generate the frozen THM-M-0347 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0347-OBLIGATION_TREE"
THEOREM = "THM-M-0347"

# The classical approximate-identity route is frozen independently of closure.
# Every central analytic package is retained as a bridge rather than hidden in
# a one-line invocation.
ROWS = [
    ("M0347-ROOT", "root", "The exact arbitrary-positive-period uniform Fejer theorem target.", "Stage1Instances.THM_M_0347.FejerTheoremTarget", "required", "required", 20),
    ("M0347-S-INTERFACE", "definition", "Preserve the symmetric Fourier sums, n+1 Cesaro indexing, continuous-map topology, and arbitrary positive period.", "Stage1Instances.THM_M_0347.FejerTheoremTarget", "required", "not_applicable", 30),
    ("M0347-N-CONVOLUTION", "reduction", "Rewrite each frozen Fejer mean as convolution with the period-T Fejer kernel, with all Haar and scalar normalizations checked.", "planned Lean convolution identity for fejerMean", "required", "required", 75),
    ("M0347-C-KERNEL", "construction", "Construct the finite period-T Fejer kernel and identify its weighted Fourier expansion.", "planned Lean period-T Fejer kernel definition and expansion", "required", "required", 70),
    ("M0347-L-POSITIVITY", "core_lemma", "Prove pointwise nonnegativity of the Fejer kernel from its squared geometric-sum representation.", "planned Lean Fejer-kernel nonnegativity theorem", "required", "required", 65),
    ("M0347-L-MASS", "core_lemma", "Prove that the normalized Fejer kernel has integral one for every index and positive period.", "planned Lean normalized Fejer-kernel mass theorem", "required", "required", 55),
    ("M0347-L-CONCENTRATION", "core_lemma", "Prove that kernel mass outside every neighborhood of zero tends to zero uniformly in the base point.", "planned Lean Fejer-kernel concentration theorem", "required", "required", 90),
    ("M0347-L-UNIFORM-CONTINUITY", "core_lemma", "Use compactness of AddCircle T to obtain the uniform translation estimate for the continuous function f.", "planned Lean uniform translation-continuity theorem", "required", "required", 55),
    ("M0347-L-ESTIMATE", "terminal", "Combine positivity, unit mass, concentration, and uniform continuity into the epsilon sup-distance estimate.", "Stage1Instances.THM_M_0347.ObligationTree.UniformFejerEstimate", "required", "required", 80),
    ("M0347-T-ASSEMBLE", "transport", "Convert the epsilon sup-distance estimate into Tendsto atTop in the continuous-map topology.", "Stage1Instances.THM_M_0347.ObligationTree.root_of_uniformFejerEstimate", "required", "required", 20),
    ("M0347-X-SOURCE", "source_boundary", "Map every analytic transition to an inspected primary theorem passage with normalization crosswalk.", "primary source node map pending", "not_applicable", "required", 70),
    ("M0347-X-FOUNDATION", "trust_boundary", "Audit classical logic, quotient, integration, imported declarations, axioms, and the no-oracle boundary.", "transitive foundation and TCB report pending", "required", "not_applicable", 40),
    ("M0347-X-PROVENANCE", "certificate", "Bind every terminal body and imported bridge to immutable origin, dependency, license, and trust records.", "provenance ledger pending proof phase", "informational", "not_applicable", 40),
    ("M0347-X-READABLE", "documentation", "Produce a uniquely anchored reconstruction of the convolution and approximate-identity argument.", "readable reconstruction pending", "not_applicable", "not_applicable", 80),
    ("M0347-X-WORKFLOW", "workflow_gate", "Require node proof, validation, and release receipts before root promotion.", "rev-5.6 proof -> validation -> release workflow", "informational", "not_applicable", 20),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def planned(oid, statement):
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, machine, source, budget in ROWS:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-expression-sha256:ae3d7a520ec1089f6b6a798ee280d598bb18738b4eecf0042a8d9e7fbd3fa564" if oid in {"M0347-ROOT", "M0347-S-INTERFACE"} else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": source,
        "readable_eligibility": "required",
        "risk_class": "critical" if oid in {"M0347-ROOT", "M0347-N-CONVOLUTION", "M0347-L-CONCENTRATION", "M0347-L-ESTIMATE", "M0347-X-FOUNDATION"} else "high",
        "exclusion_reason": "human_source_boundary_only" if oid == "M0347-X-SOURCE" else ("release_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0347/ObligationTree.lean#root_of_uniformFejerEstimate" if oid == "M0347-T-ASSEMBLE" else None,
    })
ids = [row[0] for row in ROWS]
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated target and bounded anchor audit; classical Fejer-kernel approximate-identity architecture selected without proof-availability credit.",
    "frozen_against_statement_sha256": statement_sha,
    "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0347-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility change, or re-fingerprint requires a new registry version and append-only old/new ID delta.",
    "obligations": obligations,
}

checked = {"M0347-S-INTERFACE", "M0347-T-ASSEMBLE"}
nodes = []
for oid, kind, human, formal, machine, source, budget in ROWS:
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0347-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H1", "machine_debt": "M0-L" if oid == "M0347-T-ASSEMBLE" else ("M3" if oid in {"M0347-ROOT", "M0347-S-INTERFACE"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md; primary theorem passage and node map pending" if source == "required" else "not-applicable",
        "provenance_id": "anchor-audit.json" if oid in {"M0347-N-CONVOLUTION", "M0347-X-PROVENANCE"} else "none",
        "foundation_profile": "Lean dependent type theory plus mathlib classical finite sums, quotient AddCircle, normalized Haar integration; exact terminal audit pending",
        "tcb_profile": "Lean 4.29.0 + mathlib 8a178386; transitive closure and release inventory pending",
        "computation_record": "none; symbolic proof only, with no oracle or numerical experiment credited",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the exact formal context and declared proof-requires children.", "inference": human, "output": human, "outgoing_use": "Only declared typed proof composition or non-proof support edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0347/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen interface" + (" and kernel-checked conditional composition" if oid in checked else " only") + "; no Fejer proof or root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0347-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0347/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-0347 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

def graph(edges):
    out, incoming = ({x: [] for x in ids}, {x: [] for x in ids})
    for e in edges:
        out[e["from"]].append(e["edge_id"]); incoming[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [
    ("M0347-ROOT", "M0347-S-INTERFACE"), ("M0347-ROOT", "M0347-T-ASSEMBLE"),
    ("M0347-T-ASSEMBLE", "M0347-L-ESTIMATE"), ("M0347-L-ESTIMATE", "M0347-N-CONVOLUTION"),
    ("M0347-L-ESTIMATE", "M0347-L-POSITIVITY"), ("M0347-L-ESTIMATE", "M0347-L-MASS"),
    ("M0347-L-ESTIMATE", "M0347-L-CONCENTRATION"), ("M0347-L-ESTIMATE", "M0347-L-UNIFORM-CONTINUITY"),
    ("M0347-N-CONVOLUTION", "M0347-C-KERNEL"), ("M0347-L-POSITIVITY", "M0347-C-KERNEL"),
    ("M0347-L-MASS", "M0347-C-KERNEL"), ("M0347-L-CONCENTRATION", "M0347-C-KERNEL"),
]
proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req}]

def simple(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]

analytic = ids[2:10]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(simple("R", "logical_decomposition", [("M0347-ROOT", x) for x in analytic])),
    "provenance": graph(simple("V", "provenance_of", [("M0347-X-PROVENANCE", x) for x in analytic + ["M0347-ROOT"]])),
    "evidence": graph(simple("E", "source_map", [("M0347-X-SOURCE", x) for x in analytic + ["M0347-ROOT"]])),
    "trust": graph(simple("T", "trusts", [(x, "M0347-X-FOUNDATION") for x in analytic + ["M0347-ROOT"]])),
    "documentation": graph(simple("D", "documents", [("M0347-X-READABLE", x) for x in analytic + ["M0347-ROOT"]])),
    "workflow": graph(simple("W", "workflow_depends_on", [("M0347-ROOT", x) for x in ["M0347-X-SOURCE", "M0347-X-FOUNDATION", "M0347-X-PROVENANCE", "M0347-X-READABLE", "M0347-X-WORKFLOW"]])),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0347-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0347-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "theorem_complete": False, "first_open_cut": ["M0347-N-CONVOLUTION", "M0347-C-KERNEL", "M0347-L-POSITIVITY", "M0347-L-MASS", "M0347-L-CONCENTRATION", "M0347-L-UNIFORM-CONTINUITY", "M0347-X-SOURCE", "M0347-X-FOUNDATION", "M0347-X-PROVENANCE", "M0347-X-READABLE", "M0347-X-WORKFLOW"]},
}
specs = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "provisional" if oid in checked else "open", "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0347/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "disabled", "covered_ids": [oid], "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids],
}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
