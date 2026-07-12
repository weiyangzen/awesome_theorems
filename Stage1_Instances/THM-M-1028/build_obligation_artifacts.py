#!/usr/bin/env python3
"""Build the frozen THM-M-1028 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1028-OBLIGATION_TREE"
THEOREM = "THM-M-1028"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M1028-ROOT", "root", "critical", "The exact frozen real-time Wiener path-regularity proposition.", "AwesomeTheorems.Stage1.THM_M_1028.Statement", "The canonical proposition."),
    ("M1028-S-DEFINITIONS", "definition", "high", "Freeze real processes, grids, increments, modification, and domain-relative nowhere differentiability.", "AwesomeTheorems.Stage1.THM_M_1028.{RealProcess,increment,IsNonnegativeGrid,HasStandardWienerIncrements,IsModification,NowhereDifferentiableOnNonnegative}", "The elaborated statement vocabulary."),
    ("M1028-S-DOMAIN", "normalization", "high", "Preserve nonnegative real time, repeated grid points, zero increments, coordinatewise modification, and the one-sided endpoint derivative.", "planned exact boundary and coercion lemmas for Set.Ici (0 : Real)", "Checked domain and degenerate-case transports."),
    ("M1028-S-FOUNDATION", "certificate", "critical", "Fix classical choice, measure-theory axioms, imports, TCB, and the no-oracle policy.", "planned transitive axiom and trust report", "Accepted foundation boundary."),
    ("M1028-N-GAUSSIAN-MOMENTS", "reduction", "critical", "Derive measurable centered Gaussian increment moments and the Kolmogorov moment bound from the frozen finite-grid law.", "planned Lean Gaussian moment/Kolmogorov bridge", "A quantitative increment moment condition."),
    ("M1028-N-TIME-TRANSPORT", "transport", "critical", "Transport between the frozen Real/Ici process and any NNReal-indexed Kolmogorov or Brownian API without strengthening modification equality.", "planned checked Real-Ici/NNReal process transport", "An exact bidirectional interface for the continuity construction."),
    ("M1028-C-CONTINUOUS-MODIFICATION", "construction", "critical", "Construct a coordinatewise modification with almost surely continuous paths on nonnegative time.", "AwesomeTheorems.Stage1.THM_M_1028.ContinuousModificationPackage", "A modification Y and one full-measure continuity event."),
    ("M1028-L-SHORT-INCREMENT-BOUND", "core_lemma", "critical", "Prove the Gaussian small-increment probability estimate used to exclude a finite derivative on a fixed interval and scale.", "planned exact Gaussian probability bound", "A summable or uniformly controlled bad-increment bound."),
    ("M1028-B-DYADIC-GRIDS", "branch", "high", "Choose countable dyadic/rational grids on every bounded nonnegative interval and prove coverage and endpoint compatibility.", "planned dyadic grid construction and exhaustive enumeration", "A countable exhaustive family of local difference quotients."),
    ("M1028-L-BOREL-CANTELLI", "core_lemma", "critical", "Apply independence and probability bounds to show almost surely arbitrarily steep local oscillations at every enumerated location and scale.", "planned Borel-Cantelli/independent-increment argument", "A full-measure countable-grid oscillation event."),
    ("M1028-L-NONDIFF-TRANSFER", "core_lemma", "critical", "Use path continuity and countable interval coverage to transfer grid oscillation to failure of DifferentiableWithinAt at every point of Ici 0, including zero.", "planned deterministic continuity/differentiability contradiction", "Almost-sure nowhere domain-relative differentiability for Y."),
    ("M1028-T-NONDIFFERENTIABLE", "terminal", "critical", "Assemble the probabilistic and deterministic packages into the nowhere-differentiability package for every continuous modification.", "AwesomeTheorems.Stage1.THM_M_1028.NowhereDifferentiabilityPackage", "The a.e. nowhere-differentiability property."),
    ("M1028-T-MERGE-EVENTS", "transport", "high", "Intersect the continuity and nowhere-differentiability events without changing the chosen modification.", "AwesomeTheorems.Stage1.THM_M_1028.root_of_path_packages", "One full-measure event carrying both path properties."),
    ("M1028-T-ASSEMBLE", "transport", "high", "Compose both path packages into the exact canonical statement.", "AwesomeTheorems.Stage1.THM_M_1028.root_of_path_packages", "The exact root conditional on the two substantive packages."),
    ("M1028-X-SOURCE", "terminal", "high", "Map every material probabilistic and analytic step to pinpoint reviewed primary-source passages.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M1028-X-PROVENANCE", "certificate", "critical", "Inventory imports, external candidates, terminal bodies, wrappers, axioms, and replay receipts.", "planned machine-derived provenance and trust closure", "Release provenance without mathematical proof credit."),
]

checked = {"M1028-S-DEFINITIONS", "M1028-T-MERGE-EVENTS", "M1028-T-ASSEMBLE"}
source_na = {"M1028-S-DEFINITIONS", "M1028-S-DOMAIN", "M1028-S-FOUNDATION", "M1028-X-PROVENANCE"}
machine_special = {"M1028-X-SOURCE": "not_applicable", "M1028-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = ("lean-expression-sha256:b2b4d22cf67e788a83c50a50a8510737e5c3a82f972be439f3c5f3d27cdfbf40"
                   if oid in {"M1028-ROOT", "M1028-S-DEFINITIONS"}
                   else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "release_provenance_overlay_no_proof_credit"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-1028/ObligationTree.lean#root_of_path_packages"
                                   if oid in {"M1028-T-MERGE-EVENTS", "M1028-T-ASSEMBLE"} else None),
    })
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M1028-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M2" if oid == "M1028-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid in {"M1028-T-MERGE-EVENTS", "M1028-T-ASSEMBLE"} else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {
            "premises": "Only the exact incoming proof_requires children and the frozen process context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed parent or a non-proof support edge may consume this output."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-1028/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; no open substantive premise or root proof is supplied.",
        "task_ids": [ITEM, "S56-M-1028-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1028/ObligationTree.lean"] if oid in {"M1028-T-MERGE-EVENTS", "M1028-T-ASSEMBLE"} else [],
        "owner": "THM-M-1028 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None,
                     "review_due": "before proof acceptance",
                     "invalidation_inputs": ["statement", "registry", "source map", "toolchain"],
                     "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; continuity and classical nowhere-differentiability architecture; eligibility assigned independently of proof availability.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1028-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M1028-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M2"},
    "status_boundary": "Frozen scope and denominators only; neither path package nor the theorem is proved.",
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1028-ROOT": ["M1028-T-ASSEMBLE"],
    "M1028-T-ASSEMBLE": ["M1028-C-CONTINUOUS-MODIFICATION", "M1028-T-NONDIFFERENTIABLE", "M1028-T-MERGE-EVENTS"],
    "M1028-C-CONTINUOUS-MODIFICATION": ["M1028-N-GAUSSIAN-MOMENTS", "M1028-N-TIME-TRANSPORT"],
    "M1028-T-NONDIFFERENTIABLE": ["M1028-L-SHORT-INCREMENT-BOUND", "M1028-B-DYADIC-GRIDS", "M1028-L-BOREL-CANTELLI", "M1028-L-NONDIFF-TRANSFER"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1028-ROOT", "logical_decomposition", "M1028-S-DEFINITIONS"),
                   edge("REF-ROOT-DOMAIN", "M1028-ROOT", "logical_decomposition", "M1028-S-DOMAIN"),
                   edge("REF-ROOT-FOUND", "M1028-ROOT", "logical_decomposition", "M1028-S-FOUNDATION")],
    "provenance": [edge("SRC-CONT", "M1028-C-CONTINUOUS-MODIFICATION", "source_map", "M1028-X-SOURCE"),
                   edge("SRC-NONDIFF", "M1028-T-NONDIFFERENTIABLE", "source_map", "M1028-X-SOURCE"),
                   edge("PROV-ROOT", "M1028-X-PROVENANCE", "provenance_of", "M1028-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1028-ROOT", "trusts", "M1028-S-FOUNDATION"),
              edge("TRUST-PROV", "M1028-ROOT", "trusts", "M1028-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M1028-S-DEFINITIONS", "documents", "M1028-ROOT"),
                      edge("DOC-SOURCE", "M1028-X-SOURCE", "documents", "M1028-T-NONDIFFERENTIABLE")],
    "workflow": [edge("FLOW-ASSEMBLE-CONT", "M1028-T-ASSEMBLE", "workflow_depends_on", "M1028-C-CONTINUOUS-MODIFICATION"),
                 edge("FLOW-ASSEMBLE-NONDIFF", "M1028-T-ASSEMBLE", "workflow_depends_on", "M1028-T-NONDIFFERENTIABLE"),
                 edge("FLOW-NONDIFF-BOUND", "M1028-T-NONDIFFERENTIABLE", "workflow_depends_on", "M1028-L-SHORT-INCREMENT-BOUND"),
                 edge("FLOW-NONDIFF-BC", "M1028-T-NONDIFFERENTIABLE", "workflow_depends_on", "M1028-L-BOREL-CANTELLI"),
                 edge("FLOW-PROV-ASSEMBLE", "M1028-X-PROVENANCE", "workflow_depends_on", "M1028-T-ASSEMBLE")],
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
    "registry_id": "THM-M-1028-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1028-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False,
                         "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": ["M1028-C-CONTINUOUS-MODIFICATION", "M1028-T-NONDIFFERENTIABLE"],
                         "composition_certificates": ["AwesomeTheorems.Stage1.THM_M_1028.root_of_path_packages"],
                         "reason": "The exact final composition is conditional; both substantive path packages remain open."},
}

specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
         "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid,
                      "command": "python3 Stage1_Instances/THM-M-1028/check_obligation_tree.py",
                      "expected_exit": 0, "network_policy": "denied"} for oid, *_ in rows]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
