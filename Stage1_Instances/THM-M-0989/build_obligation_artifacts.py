#!/usr/bin/env python3
"""Build the frozen THM-M-0989 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0989-OBLIGATION_TREE"
THEOREM = "THM-M-0989"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# ID, kind, risk, human statement, formal target, output, machine debt.
rows = [
    ("M0989-ROOT", "root", "critical", "The exact normalized triangular-array Lindeberg-Feller statement.", "Stage1Instances.THM_M_0989.Statement", "Convergence in distribution of every frozen row sum to gaussianReal 0 1.", "M3"),
    ("M0989-S-DEFINITIONS", "definition", "high", "Preserve row indexing, centering, square integrability, unit variance, strict truncation, and the Gaussian convention.", "Stage1Instances.THM_M_0989.{NormalizedTriangularArray,truncatedSecondMoment,rowSum}", "The exact elaborated array interface.", "M0-L"),
    ("M0989-S-MEAS", "lemma", "medium", "Derive almost-everywhere measurability of each finite row sum.", "Stage1Instances.THM_M_0989.RowSumsAEMeasurable", "AEMeasurable (rowSum A n) for every n.", "M4"),
    ("M0989-S-FOUNDATION", "certificate", "critical", "Fix the classical-choice, quotient, analytic, TCB, and no-oracle policy for every terminal body.", "planned transitive axiom and trust report", "An accepted trust boundary.", "M4"),
    ("M0989-C-FACTOR", "construction", "critical", "Factor the characteristic function of each row sum into the finite product of increment characteristic functions using row independence.", "planned row-wise independent charFun product identity", "An exact finite-product expression for each row characteristic function.", "M4"),
    ("M0989-N-MOMENTS", "normalization", "high", "Convert centering and unit total variance into the first- and second-order identities needed by the expansion.", "planned expectation/variance/second-moment normalization lemmas", "Zero total linear term and Gaussian quadratic coefficient one half.", "M4"),
    ("M0989-L-INFINITESIMAL", "core_lemma", "critical", "Derive uniform asymptotic negligibility of all increments from the Lindeberg condition and unit row variance.", "planned max-tail and max-variance estimates", "Uniform smallness needed for logarithms and product errors.", "M4"),
    ("M0989-L-TRUNCATE", "core_lemma", "critical", "Bound the large-increment contribution to each characteristic-function remainder by the Lindeberg sum.", "planned truncated second-moment tail estimate", "A remainder bound tending to zero for every fixed frequency.", "M4"),
    ("M0989-L-TAYLOR", "core_lemma", "critical", "Control the small-increment complex exponential remainder to second order with a uniform quantitative bound.", "planned complex exponential Taylor estimate", "A summable small-increment remainder estimate.", "M4"),
    ("M0989-L-PRODUCT", "core_lemma", "critical", "Turn the sum of increment expansions into convergence of their finite product, including logarithm/zero avoidance errors.", "planned triangular-array product-to-exp lemma", "Row characteristic functions tend to exp (-t^2/2).", "M4"),
    ("M0989-T-CHARFUN", "terminal", "critical", "Assemble factorization, moment normalization, Lindeberg tails, Taylor bounds, and product control.", "Stage1Instances.THM_M_0989.RowLawCharFunConverges", "Pointwise convergence of row-law characteristic functions to the standard Gaussian characteristic function.", "M4"),
    ("M0989-T-LEVY", "bridge", "high", "Apply the pinned Levy characteristic-function criterion to the mapped row laws.", "ProbabilityMeasure.tendsto_iff_tendsto_charFun", "Weak convergence of the mapped row probability measures.", "M0-L"),
    ("M0989-T-ASSEMBLE", "transport", "high", "Compose row-sum measurability and characteristic-function convergence into the exact frozen TendstoInDistribution target.", "Stage1Instances.THM_M_0989.root_of_row_charFun_packages", "The exact root conditional on the two explicit packages.", "M0-L"),
    ("M0989-X-SOURCE", "terminal", "high", "Map every material estimate and bridge to reviewed primary-source pages, assumptions, conventions, and errata.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit.", "M4"),
    ("M0989-X-PROVENANCE", "certificate", "critical", "Inventory terminal proof bodies, wrappers, imports, axioms, TCB, and replay evidence.", "planned machine-derived provenance and trust closure", "Release provenance coverage without mathematical proof credit.", "M4"),
]

checked = {"M0989-S-DEFINITIONS", "M0989-T-LEVY", "M0989-T-ASSEMBLE"}
source_na = {"M0989-S-DEFINITIONS", "M0989-S-MEAS", "M0989-S-FOUNDATION", "M0989-X-PROVENANCE"}
machine_special = {"M0989-X-SOURCE": "not_applicable", "M0989-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor_audit.md").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output, debt in rows:
    fp = "lean-source:v1:sha256:" + statement_hash if oid in {"M0989-ROOT", "M0989-S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0989/ObligationTree.lean#root_of_row_charFun_packages" if oid == "M0989-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-0989-" + oid.removeprefix("M0989-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": debt, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M0989-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no simulation, oracle, or numerical approximation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires children and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0989/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0989-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0989/ObligationTree.lean"] if oid == "M0989-T-ASSEMBLE" else [],
        "owner": "THM-M-0989 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact normalized triangular-array statement and bounded anchor audit; characteristic-function proof route expanded before observing closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0989-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0989-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Lindeberg estimate, root proof, source acceptance, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0989-ROOT": ["M0989-T-ASSEMBLE"],
    "M0989-T-ASSEMBLE": ["M0989-S-MEAS", "M0989-T-CHARFUN", "M0989-T-LEVY"],
    "M0989-T-CHARFUN": ["M0989-C-FACTOR", "M0989-N-MOMENTS", "M0989-L-INFINITESIMAL", "M0989-L-TRUNCATE", "M0989-L-TAYLOR", "M0989-L-PRODUCT"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0989-ROOT", "logical_decomposition", "M0989-S-DEFINITIONS"), edge("REF-ROOT-FOUND", "M0989-ROOT", "logical_decomposition", "M0989-S-FOUNDATION")],
    "provenance": [edge("SRC-ESTIMATES", "M0989-T-CHARFUN", "source_map", "M0989-X-SOURCE"), edge("PROV-ROOT", "M0989-X-PROVENANCE", "provenance_of", "M0989-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0989-ROOT", "trusts", "M0989-S-FOUNDATION"), edge("TRUST-PROV", "M0989-ROOT", "trusts", "M0989-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M0989-S-DEFINITIONS", "documents", "M0989-ROOT"), edge("DOC-SOURCE", "M0989-X-SOURCE", "documents", "M0989-T-CHARFUN")],
    "workflow": [edge("FLOW-ASSEMBLE-MEAS", "M0989-T-ASSEMBLE", "workflow_depends_on", "M0989-S-MEAS"), edge("FLOW-ASSEMBLE-CHAR", "M0989-T-ASSEMBLE", "workflow_depends_on", "M0989-T-CHARFUN"), edge("FLOW-CHAR-PROD", "M0989-T-CHARFUN", "workflow_depends_on", "M0989-L-PRODUCT"), edge("FLOW-PROV-ASSEMBLE", "M0989-X-PROVENANCE", "workflow_depends_on", "M0989-T-ASSEMBLE")],
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
    "registry_id": "THM-M-0989-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0989-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0989-S-MEAS", "M0989-T-CHARFUN"], "composition_certificates": ["Stage1Instances.THM_M_0989.root_of_row_charFun_packages"], "reason": "The final composition is conditional; measurability and the substantive triangular-array characteristic-function package remain unproved."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0989/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
