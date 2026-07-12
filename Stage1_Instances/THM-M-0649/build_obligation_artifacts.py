#!/usr/bin/env python3
"""Generate the frozen THM-M-0649 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0649-OBLIGATION_TREE"


def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()


def planned(oid, statement):
    payload = f"THM-M-0649:v1:{oid}:{statement}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(payload).hexdigest()


# id, kind, statement, exact output, risk, machine debt, step budget, source eligibility
specs = [
    ("M0649-ROOT", "root", "Prove the exact typed elementary-chain target.", "Stage1.THM_M_0649.ElementaryChainTarget", "critical", "M3", 5, "required"),
    ("M0649-S-STATEMENT", "definition", "Preserve the frozen language, universe, binder, coherence, and canonical-map identity choices.", "The exact Statement.lean proposition without strengthening or weakening.", "critical", "M0-L", 20, "not_applicable"),
    ("M0649-S-BOUNDARY", "branch", "Retain nonempty linear chains, including singleton and greatest-element cases, without countability or common-carrier assumptions.", "The frozen degeneracy and scope policy.", "high", "M3", 25, "required"),
    ("M0649-S-FOUNDATION", "certificate", "Audit classical choice, quotient construction, accepted axioms, and the transitive Lean/mathlib trust boundary.", "An accepted foundation and TCB profile.", "critical", "M4", 45, "not_applicable"),
    ("M0649-C-COVER", "construction", "Use DirectLimit.exists_of to represent an arbitrary limit element at a chain stage.", "A stage j and y : G j whose canonical image is the chosen limit element.", "high", "M3", 25, "required"),
    ("M0649-C-UPPER", "construction", "Choose a common upper chain stage for the source stage, witness stage, and finite parameter support.", "A comparison stage k with the required order proofs.", "high", "M4", 35, "required"),
    ("M0649-L-TERM", "core_lemma", "Prove canonical direct-limit maps commute with term realization and coherent transition maps.", "The term-realization equality used by atomic and quantified cases.", "high", "M4", 70, "required"),
    ("M0649-L-REL", "core_lemma", "Prove atomic relation realization is invariant under passage to a sufficiently high chain stage and the quotient.", "The atomic relation equivalence.", "critical", "M4", 80, "required"),
    ("M0649-L-BOOL", "core_lemma", "Compose the induction hypotheses for falsum, implication, negation, conjunction, and derived Boolean syntax.", "Formula preservation for Boolean constructors.", "normal", "M4", 45, "required"),
    ("M0649-L-QUANT-FORTH", "core_lemma", "Transfer a quantified witness from a stage to its canonical image in the direct limit.", "The stage-to-limit quantified direction.", "critical", "M4", 75, "required"),
    ("M0649-L-QUANT-BACK", "core_lemma", "Represent a limit witness, move it and all parameters to a common stage, then use transition elementarity and coherence.", "The limit-to-stage quantified direction.", "critical", "M4", 100, "required"),
    ("M0649-L-FORMULA", "core_lemma", "Run structural induction on bounded formulas using the atomic, Boolean, and quantified packages.", "Preservation and reflection of every formula by each canonical map.", "critical", "M4", 90, "required"),
    ("M0649-T-TV", "bridge", "Specialize formula preservation to the exact Tarski-Vaught witness interface in ObligationTree.lean.", "Stage1.THM_M_0649.CanonicalTarskiVaught", "critical", "M4", 40, "required"),
    ("M0649-T-ASSEMBLE", "transport", "Bundle each canonical embedding with Tarski-Vaught elementarity and preserve definitional equality with DirectLimit.of.", "The exact root, conditional on CanonicalTarskiVaught.", "high", "M0-L", 8, "not_applicable"),
    ("M0649-X-SOURCE", "terminal", "Pinpoint the elementary-chain theorem and each material proof transition in an immutable primary source, including errata review.", "An independently reviewed H0 source crosswalk.", "high", "not_applicable", 80, "required"),
    ("M0649-X-PROVENANCE", "certificate", "Track wrappers and imports to distinct terminal proof bodies without duplicate credit.", "A complete terminal-body provenance map.", "high", "informational", 45, "not_applicable"),
    ("M0649-X-TRUST", "certificate", "Bind kernel, dependency, axiom, replay, freshness, and independent-verification evidence.", "Release-gate trust evidence.", "critical", "informational", 55, "not_applicable"),
]

obligations = []
nodes = []
for oid, kind, statement, output, risk, machine, budget, source in specs:
    machine_eligibility = "informational" if machine == "informational" else ("not_applicable" if machine == "not_applicable" else "required")
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-print-sha256:acb2ab29191a821685e73fdc4edb6d786a3f2c92913eeecdff15a50de43b1197" if oid == "M0649-ROOT" else planned(oid, statement),
        "kind": kind, "root_relevant": True,
        "machine_eligibility": machine_eligibility,
        "human_source_eligibility": source,
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None,
        "terminal_proof_body_id": "local:ObligationTree.lean#elementaryChainTarget_of_tarskiVaught" if oid == "M0649-T-ASSEMBLE" else None,
    })
    overlay = oid.startswith("M0649-X-")
    nodes.append({
        "node_id": "THM-M-0649-" + oid.removeprefix("M0649-"), "obligation_id": oid,
        "kind": kind, "human_statement": statement,
        "formal_target": output if oid in {"M0649-ROOT", "M0649-T-TV"} else ("Stage1.THM_M_0649.elementaryChainTarget_of_tarskiVaught" if oid == "M0649-T-ASSEMBLE" else "planned exact signature: " + output),
        "output": output, "human_debt": "H1", "machine_debt": machine, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source-statement-crosswalk.md" if source == "required" else "not-applicable",
        "provenance_id": "local-composition-body" if oid == "M0649-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, experiment, or unchecked certificate is credited",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Exact conclusions of incoming proof_requires edges.", "inference": statement, "output": output, "outgoing_use": "Only through typed edges in typed-graphs.json."},
        "public_readable_target": f"Stage1_Instances/THM-M-0649/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Release/source overlay only; it cannot close a proof premise." if overlay else "Architecture or conditional interface only; no open model-theory lemma is asserted.",
        "task_ids": [ITEM, "S56-M-0649-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0649/ObligationTree.lean"] if oid in {"M0649-T-TV", "M0649-T-ASSEMBLE"} else [],
        "owner": "THM-M-0649 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid == "M0649-T-ASSEMBLE" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if oid == "M0649-T-ASSEMBLE" else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "registry_id": "THM-M-0649-OBLIGATIONS-v1",
    "item_id": ITEM, "theorem_id": "THM-M-0649", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact typed direct-limit statement and bounded anchor inventory; eligibility was selected independently of closure status.",
    "frozen_against_statement_sha256": sha("Statement.lean"), "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "root_obligation_id": "M0649-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [row["obligation_id"] for row in obligations],
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": [row["obligation_id"] for row in obligations],
        "informational_overlays": ["M0649-X-PROVENANCE", "M0649-X-TRUST"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new registry version with an append-only old/new ID delta.",
    "obligations": obligations,
}

proof_pairs = [
    ("M0649-ROOT", "M0649-T-ASSEMBLE"), ("M0649-ROOT", "M0649-S-STATEMENT"),
    ("M0649-ROOT", "M0649-S-BOUNDARY"), ("M0649-ROOT", "M0649-S-FOUNDATION"),
    ("M0649-T-ASSEMBLE", "M0649-T-TV"), ("M0649-T-TV", "M0649-L-FORMULA"),
    ("M0649-L-FORMULA", "M0649-L-TERM"), ("M0649-L-FORMULA", "M0649-L-REL"),
    ("M0649-L-FORMULA", "M0649-L-BOOL"), ("M0649-L-FORMULA", "M0649-L-QUANT-FORTH"),
    ("M0649-L-FORMULA", "M0649-L-QUANT-BACK"), ("M0649-L-QUANT-BACK", "M0649-C-COVER"),
    ("M0649-L-QUANT-BACK", "M0649-C-UPPER"),
]
graph_names = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
ids = [row["obligation_id"] for row in obligations]
graphs = {name: {"edges": [], "out": {oid: [] for oid in ids}, "in": {oid: [] for oid in ids}} for name in graph_names}


def edge(graph, source, target, edge_type, reciprocal=None):
    edge_id = f"{graph.upper()}-{len(graphs[graph]['edges']) + 1:03d}"
    row = {"edge_id": edge_id, "from": source, "to": target, "type": edge_type}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(row)
    graphs[graph]["out"][source].append(edge_id)
    graphs[graph]["in"][target].append(edge_id)
    return edge_id


for parent, child in proof_pairs:
    forward = edge("proof", parent, child, "proof_requires")
    reverse = edge("proof", child, parent, "composes", forward)
    graphs["proof"]["edges"][-2]["reciprocal_edge_id"] = reverse
for child in ("M0649-C-COVER", "M0649-C-UPPER", "M0649-L-TERM", "M0649-L-REL", "M0649-L-BOOL", "M0649-L-QUANT-FORTH", "M0649-L-QUANT-BACK", "M0649-L-FORMULA"):
    edge("provenance", child, "M0649-X-SOURCE", "source_map")
    edge("provenance", child, "M0649-X-PROVENANCE", "provenance_of")
for child in ("M0649-L-TERM", "M0649-L-REL", "M0649-L-BOOL", "M0649-L-QUANT-FORTH", "M0649-L-QUANT-BACK"):
    edge("refinement", "M0649-L-FORMULA", child, "logical_decomposition")
for oid in ids:
    edge("documentation", oid, oid, "documents")
    if oid != "M0649-ROOT":
        edge("workflow", oid, "M0649-ROOT", "workflow_depends_on")
for oid in ("M0649-ROOT", "M0649-S-FOUNDATION", "M0649-T-TV", "M0649-T-ASSEMBLE"):
    edge("trust", oid, "M0649-X-TRUST", "trusts")

bundle = {
    "schema_version": "stage1-typed-graph-bundle/1.0", "item_id": ITEM, "theorem_id": "THM-M-0649",
    "registry_id": registry["registry_id"], "registry_denominator_sha256": denominator,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "theorem_complete": False,
        "remaining_root_cut_set": ["M0649-T-TV"],
        "checked_composition": "Stage1.THM_M_0649.elementaryChainTarget_of_tarskiVaught",
        "boundary": "The checked composition consumes CanonicalTarskiVaught but does not prove the formula-induction package."},
}
recipes = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0649",
    "recipes": [{"recipe_id": "VAL-" + oid, "cwd": "Formalizations/Lean", "argv": ["bash", "../../Stage1_Instances/THM-M-0649/check_lean.sh"], "environment": {}, "timeout_seconds": 120, "network_policy": "denied", "covered_obligation_ids": [oid], "status": "executable_composition_check" if oid == "M0649-T-ASSEMBLE" else "planned_node_check"} for oid in ids],
}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"generated {len(ids)} obligations; denominator {denominator}; typed edges {sum(len(graph['edges']) for graph in graphs.values())}")
