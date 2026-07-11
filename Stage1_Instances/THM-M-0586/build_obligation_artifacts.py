#!/usr/bin/env python3
"""Build the frozen THM-M-0586 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0586-OBLIGATION_TREE"
THEOREM = "THM-M-0586"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# Eligibility is fixed from the classical proof architecture, before considering closure.
ROWS = [
    ("M0586-ROOT", "root", "critical", "The exact frozen high-dimensional Poincare target.", "Stage1Instances.THMM0586.HighDimensionalPoincareTarget", "The canonical proposition."),
    ("M0586-S-DEFINITIONS", "definition", "high", "Fix the sphere, smooth boundaryless manifold, homotopy-equivalence, and homeomorphism interfaces.", "Stage1Instances.THMM0586.{EuclideanModel,UnitSphere,HighDimensionalPoincareTarget}", "The elaborated target interface."),
    ("M0586-S-BOUNDARY", "branch", "critical", "Include dimension five and exclude dimensions below five without silently applying a stable-range theorem there.", "the n = 5 / 6 <= n exhaustive split", "An exhaustive dimension split under 5 <= n."),
    ("M0586-S-TRANSPORT", "transport", "critical", "Relate the selected smooth closed formulation to any topological, homology-sphere, or cobordism formulation in the direction actually used.", "planned checked formulation transports", "Exact directional transports with all hypotheses visible."),
    ("M0586-S-FOUNDATION", "certificate", "critical", "Freeze the classical-choice, quotient, extensionality, axiom, TCB, and no-oracle policy.", "planned transitive axiom and trust report", "An accepted foundation and TCB profile."),
    ("M0586-N-PUNCTURE", "reduction", "critical", "Choose two manifold disks and reduce sphere recognition to a cobordism statement for the twice-punctured manifold.", "planned puncturing reduction", "A compact cobordism with two sphere boundaries and a checked reconstruction map."),
    ("M0586-B-DIMENSION", "branch", "critical", "Split exhaustively into n = 5 and 6 <= n and preserve identical manifold hypotheses.", "Stage1Instances.THMM0586.{DimensionFivePackage,StableDimensionPackage}", "The two exact branch packages."),
    ("M0586-C-DISKS", "construction", "critical", "Construct disjoint embedded disks with collared sphere boundaries and prove complement well-definedness.", "planned embedded-disk construction", "A twice-punctured manifold with controlled boundary."),
    ("M0586-C-COBORDISM", "construction", "critical", "Equip the complement with the required cobordism structure and prove both boundary inclusions are homotopy equivalences.", "planned h-cobordism construction", "A simply connected h-cobordism in the applicable range."),
    ("M0586-C-GLUE", "construction", "critical", "Glue the product-cobordism result back across both disks and identify the resulting homeomorphism with the unit sphere.", "planned collar and gluing theorem", "A homeomorphism of the original manifold with UnitSphere n."),
    ("M0586-L-HCOB", "core_lemma", "critical", "Apply a precisely ranged smooth/topological h-cobordism theorem, including simple connectivity and torsion hypotheses.", "planned h-cobordism bridge", "A product description of the punctured cobordism."),
    ("M0586-L-FIVE", "core_lemma", "critical", "Supply the dimension-five recognition argument without importing an out-of-range stable h-cobordism theorem.", "planned dimension-five Poincare engine", "Stage1Instances.THMM0586.DimensionFivePackage"),
    ("M0586-L-STABLE", "core_lemma", "critical", "Complete sphere recognition for every n >= 6 from puncturing, h-cobordism, and gluing.", "planned stable-dimensional recognition engine", "Stage1Instances.THMM0586.StableDimensionPackage"),
    ("M0586-T-FIVE", "terminal", "critical", "Deliver the exact dimension-five package to final recomposition.", "Stage1Instances.THMM0586.DimensionFivePackage", "The complete n = 5 branch."),
    ("M0586-T-STABLE", "terminal", "critical", "Deliver the exact n >= 6 package to final recomposition.", "Stage1Instances.THMM0586.StableDimensionPackage", "The complete stable branch."),
    ("M0586-T-ASSEMBLE", "terminal", "high", "Recombine n = 5 and n >= 6 into the exact canonical target.", "Stage1Instances.THMM0586.highDimensionalPoincare_of_dimension_packages", "The exact root conditional on both packages."),
    ("M0586-X-SOURCE", "terminal", "high", "Map every material reduction, construction, and engine to pinpoint reviewed primary-source passages.", "non-machine node-specific source crosswalk", "Human-source coverage only."),
    ("M0586-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, declaration closure, axioms, TCB, replay evidence, and unique proof-body identities.", "planned machine-derived provenance closure", "Release provenance without proof credit."),
]

statement = json.loads((HERE / "statement.json").read_text())
statement_fp = statement["canonical_formal_target"]["elaborated_expression_sha256"]
checked = {"M0586-T-ASSEMBLE"}
source_na = {"M0586-S-DEFINITIONS", "M0586-S-BOUNDARY", "M0586-S-FOUNDATION", "M0586-X-PROVENANCE"}
machine_special = {"M0586-X-SOURCE": "not_applicable", "M0586-X-PROVENANCE": "informational"}
obligations, nodes = [], []
for oid, kind, risk, claim, target, output in ROWS:
    fp = "lean-expression-sha256:" + statement_fp if oid == "M0586-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind, "root_relevant": True,
        "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0586/ObligationTree.lean#highDimensionalPoincare_of_dimension_packages" if oid in checked else None,
    })
    nodes.append({
        "node_id": "THM-M-0586-" + oid.removeprefix("M0586-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if oid in {"M0586-ROOT", "M0586-S-DEFINITIONS", "M0586-B-DIMENSION"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid in checked else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if oid in {"M0586-N-PUNCTURE", "M0586-C-COBORDISM", "M0586-L-HCOB", "M0586-L-FIVE"} else 40,
        "semantic_step_ledger": {"premises": "Only exact typed proof children and the frozen formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or a non-proof support edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0586/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; no unlisted premise or root proof is supplied.",
        "task_ids": [ITEM, "S56-M-0586-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0586/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-0586 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus bounded anchor audit and the classical puncture/cobordism/gluing architecture; eligibility assigned before closure observation.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0586-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0586-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "The denominator and architecture are frozen; both mathematical branch packages and the root remain open.",
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0586-ROOT": ["M0586-T-ASSEMBLE"],
    "M0586-T-ASSEMBLE": ["M0586-T-FIVE", "M0586-T-STABLE"],
    "M0586-T-FIVE": ["M0586-L-FIVE"],
    "M0586-T-STABLE": ["M0586-L-STABLE"],
    "M0586-L-STABLE": ["M0586-N-PUNCTURE", "M0586-L-HCOB", "M0586-C-GLUE"],
    "M0586-L-FIVE": ["M0586-S-TRANSPORT"],
    "M0586-N-PUNCTURE": ["M0586-C-DISKS", "M0586-C-COBORDISM"],
    "M0586-C-COBORDISM": ["M0586-L-HCOB"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0586-ROOT", "logical_decomposition", "M0586-S-DEFINITIONS"), edge("REF-ROOT-BOUNDARY", "M0586-ROOT", "logical_decomposition", "M0586-S-BOUNDARY"), edge("REF-BRANCH-DIM", "M0586-B-DIMENSION", "logical_decomposition", "M0586-T-FIVE"), edge("REF-BRANCH-STABLE", "M0586-B-DIMENSION", "logical_decomposition", "M0586-T-STABLE")],
    "provenance": [edge("SRC-FIVE", "M0586-L-FIVE", "source_map", "M0586-X-SOURCE"), edge("SRC-HCOB", "M0586-L-HCOB", "source_map", "M0586-X-SOURCE"), edge("PROV-ROOT", "M0586-X-PROVENANCE", "provenance_of", "M0586-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M0586-ROOT", "trusts", "M0586-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0586-ROOT", "trusts", "M0586-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE", "M0586-X-SOURCE", "documents", "M0586-ROOT"), edge("DOC-BOUNDARY", "M0586-S-BOUNDARY", "documents", "M0586-B-DIMENSION")],
    "workflow": [edge("FLOW-ASSEMBLE-FIVE", "M0586-T-ASSEMBLE", "workflow_depends_on", "M0586-T-FIVE"), edge("FLOW-ASSEMBLE-STABLE", "M0586-T-ASSEMBLE", "workflow_depends_on", "M0586-T-STABLE"), edge("FLOW-PROV-ASSEMBLE", "M0586-X-PROVENANCE", "workflow_depends_on", "M0586-T-ASSEMBLE")],
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
    "registry_id": "THM-M-0586-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0586-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0586-T-FIVE", "M0586-T-STABLE"], "composition_certificates": ["Stage1Instances.THMM0586.highDimensionalPoincare_of_dimension_packages"], "reason": "Final dimension recomposition is checked, but both mathematical branch packages remain open."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0586/check_obligation_tree.py"], "env_allowlist": {"PATH": "runner-provided-pinned-toolchain"}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS and denominator digest"}], "covered_obligation_ids": [oid], "covered_declarations": ["Stage1Instances.THMM0586.highDimensionalPoincare_of_dimension_packages"] if oid == "M0586-T-ASSEMBLE" else []} for oid, *_ in ROWS]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
