#!/usr/bin/env python3
"""Build the frozen THM-M-0981 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0981-OBLIGATION_TREE"
THEOREM = "THM-M-0981"
PREFIX = "M0981"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact universe-polymorphic Kolmogorov-axioms target for every normalized measure.", "Stage1Instances.THM_M_0981.KolmogorovAxiomsTarget", "The canonical proposition."),
    ("S-EXACT", "definition", "high", "Freeze the measurable sample type, measure, explicit probability premise, and the three ordered clauses.", "Stage1Instances.THM_M_0981.KolmogorovAxiomsTarget", "The exact binder and conclusion boundary."),
    ("S-BOUNDARY", "branch", "high", "Retain empty sample spaces and the empty event family without adding nonemptiness or positivity assumptions.", "Stage1Instances.THM_M_0981.emptyFamilyBoundary", "Boundary-complete quantification."),
    ("S-TRANSPORT", "transport", "normal", "Relate the explicit class premise to ProbabilityMeasure subtype packaging in both directions.", "Stage1Instances.THM_M_0981.target_iff_probabilityMeasurePackaging", "A checked bidirectional statement transport."),
    ("S-FOUNDATION", "certificate", "high", "Fix the Lean kernel, classical-choice, quotient, extensionality, no-oracle, and transitive trust policy.", "planned transitive foundation and axiom report", "The release trust boundary."),
    ("N-INSTANCE", "normalization", "normal", "Install the explicit IsProbabilityMeasure premise as the local instance needed by the unit-mass field.", "letI : IsProbabilityMeasure P := hP", "The explicit premise normalized to mathlib typeclass form."),
    ("B-CLAUSES", "branch", "high", "Split the nested conjunction into empty-event, unit-mass, and countable-additivity branches and recompose all three.", "Stage1Instances.THM_M_0981.ObligationTree.root_compose", "An exhaustive three-clause decomposition."),
    ("L-EMPTY", "core_lemma", "normal", "Every measure assigns zero to the empty measurable event.", "MeasureTheory.measure_empty", "P empty = 0."),
    ("L-UNIT", "core_lemma", "critical", "A measure carrying IsProbabilityMeasure assigns mass one to the whole sample space.", "MeasureTheory.IsProbabilityMeasure.measure_univ", "P univ = 1."),
    ("L-ADDITIVITY", "core_lemma", "critical", "A pairwise disjoint Nat-indexed measurable family has union measure equal to the sum of its measures.", "MeasureTheory.measure_iUnion", "Countable additivity in the exact target orientation."),
    ("T-ASSEMBLE", "terminal", "critical", "Consume the three universal clause packages and construct the exact canonical nested conjunction.", "Stage1Instances.THM_M_0981.ObligationTree.root_compose", "The canonical root conditional on all three packages."),
    ("X-PROVENANCE", "certificate", "critical", "Trace the three imported declarations to pinned terminal bodies, wrappers, imports, and revisions.", "anchor-audit.json candidate provenance plus future terminal-body closure", "Machine provenance without duplicate proof credit."),
    ("X-SOURCE", "terminal", "high", "Map each clause and assumption to primary-source theorem/page/errata records and independent review.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-TCB", "certificate", "critical", "Inventory transitive declarations, compiled artifacts, executable identity, axioms, and replay evidence.", "planned trust and reproducibility closure", "Release trust coverage without mathematical proof credit."),
]

statement_expression = "1170cf6dac37cd1a8b7dfbda1a3cc3d22ddb94a5c3846f16d90dd27541766c2a"
source_not_applicable = {"S-EXACT", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION", "X-PROVENANCE", "X-TCB"}
machine_overrides = {"X-SOURCE": "not_applicable", "X-PROVENANCE": "informational", "X-TCB": "informational"}
body_ids = {
    "S-TRANSPORT": "repo:Stage1Instances.THM_M_0981.target_iff_probabilityMeasurePackaging",
    "L-EMPTY": "mathlib:8a178386:MeasureTheory.measure_empty",
    "L-UNIT": "mathlib:8a178386:MeasureTheory.IsProbabilityMeasure.measure_univ",
    "L-ADDITIVITY": "mathlib:8a178386:MeasureTheory.measure_iUnion",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0981.ObligationTree.root_compose",
}

obligations = []
nodes = []
for short, kind, risk, claim, target, output in rows:
    oid = f"{PREFIX}-{short}"
    fp = (f"lean-expression-sha256:{statement_expression}" if short in {"ROOT", "S-EXACT"}
          else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_overrides.get(short, "required")
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "release_overlay_no_semantic_proof_credit"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": short not in {"X-PROVENANCE", "X-SOURCE", "X-TCB"},
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if short in source_not_applicable else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body_ids.get(short),
    })
    node_machine = "M1" if short in {"ROOT", "T-ASSEMBLE", "L-EMPTY", "L-UNIT", "L-ADDITIVITY"} else "M3"
    nodes.append({
        "node_id": f"THM-M-0981-{short}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": node_machine, "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if short in source_not_applicable else "SRC-M0981-PRIMARY-OPEN",
        "provenance_id": "ANCHOR-M0981-THREE-MATHLIB-BODIES" if short in {"L-EMPTY", "L-UNIT", "L-ADDITIVITY"} else "none",
        "foundation_profile": "lean4-mathlib classical foundations; release axiom acceptance pending",
        "tcb_profile": "Lean 4.29.0 98dc76e + mathlib 8a178386; transitive closure pending",
        "computation_record": "none; no computation or oracle closes this node",
        "step_budget": 24 if short == "L-ADDITIVITY" else 16,
        "semantic_step_ledger": {
            "premises": "Only incoming proof_requires children and the stated formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only declared typed parent or non-proof support edges consume this output."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0981/obligation-tree.md#{short.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or conditional interface only; no accepted closure or theorem completion is supplied.",
        "task_ids": [ITEM, "S56-M-0981-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0981/ObligationTree.lean"] if short == "T-ASSEMBLE" else [],
        "owner": "THM-M-0981 execution lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance",
                     "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain", "mathlib revision"],
                     "revocation_state": "self-tested-not-accepted"}
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated statement and immutable anchor audit select the three-clause mathlib route; eligibility is assigned by semantic role without closure credit.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-TCB"]
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility, weight, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": [], "root_machine_debt": "M1"},
    "status_boundary": "Registry and denominator freeze only; no node receives proof acceptance and the root remains open."
}


def edge(eid, source, relation, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": relation, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-B-CLAUSES"],
    f"{PREFIX}-B-CLAUSES": [f"{PREFIX}-L-EMPTY", f"{PREFIX}-L-UNIT", f"{PREFIX}-L-ADDITIVITY"],
    f"{PREFIX}-L-UNIT": [f"{PREFIX}-N-INSTANCE"],
}
proof_edges = []
for parent, children in requires.items():
    for child in children:
        req = f"REQ-{parent}-{child}"
        comp = f"CMP-{child}-{parent}"
        proof_edges.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof_edges,
    "refinement": [
        edge("REF-ROOT-EXACT", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-EXACT"),
        edge("REF-ROOT-BOUNDARY", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY"),
        edge("REF-ROOT-TRANSPORT", f"{PREFIX}-ROOT", "transports", f"{PREFIX}-S-TRANSPORT"),
    ],
    "provenance": [
        edge("PROV-EMPTY", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-L-EMPTY"),
        edge("PROV-UNIT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-L-UNIT"),
        edge("PROV-ADD", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-L-ADDITIVITY"),
        edge("SOURCE-CLAUSES", f"{PREFIX}-B-CLAUSES", "source_map", f"{PREFIX}-X-SOURCE"),
    ],
    "evidence": [],
    "trust": [
        edge("TRUST-FOUNDATION", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"),
        edge("TRUST-TCB", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-TCB"),
    ],
    "documentation": [edge(f"DOC-{short}", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-{short}") for short in ("ROOT", "L-EMPTY", "L-UNIT", "L-ADDITIVITY")],
    "workflow": [
        edge("FLOW-PROOF-TREE", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-B-CLAUSES"),
        edge("FLOW-UNIT-INSTANCE", f"{PREFIX}-L-UNIT", "workflow_depends_on", f"{PREFIX}-N-INSTANCE"),
        edge("FLOW-PROVENANCE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-L-ADDITIVITY"),
        edge("FLOW-TCB", f"{PREFIX}-X-TCB", "workflow_depends_on", f"{PREFIX}-X-PROVENANCE"),
    ],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0981-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": [f"{PREFIX}-L-EMPTY", f"{PREFIX}-L-UNIT", f"{PREFIX}-L-ADDITIVITY"],
        "composition_certificates": ["Stage1Instances.THM_M_0981.ObligationTree.root_compose"],
        "reason": "The checked assembly is conditional and this phase deliberately assigns no proof-node acceptance."
    }
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({
        "recipe_id": f"VAL-{oid}", "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-0981/check_obligation_tree.py"],
        "env": {"PYTHONDONTWRITEBYTECODE": "1"}, "timeout_seconds": 30,
        "network": "forbidden", "covered_ids": [oid], "expected_exit": 0
    })

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

print(f"wrote {len(ids)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
