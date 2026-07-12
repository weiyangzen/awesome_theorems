#!/usr/bin/env python3
"""Build the frozen THM-M-0330 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0330-OBLIGATION_TREE"
THEOREM = "THM-M-0330"
PREFIX = "M0330"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact real Banach-space contraction Hille-Yosida equivalence.", "Stage1Instances.THM_M_0330.HilleYosidaContractionTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze the C0 contraction semigroup, graph generator, and bounded two-sided resolvent definitions.", "Stage1Instances.THM_M_0330.{IsC0ContractionSemigroup,IsGenerator,IsContractiveResolvent}", "The exact statement interface."),
    ("S-BOUNDARY", "terminal", "high", "Preserve zero time, strict positivity of the resolvent parameter, the zero space, real scalars, and nonnegative time.", "planned boundary lemmas for the frozen definitions", "Checked boundary behavior without strengthening the theorem."),
    ("S-FOUNDATION", "certificate", "critical", "Fix classical choice, extensionality, TCB, axiom, and no-oracle policy for terminal bodies.", "planned transitive axiom and trust report", "Accepted foundation boundary."),
    ("B-FORWARD", "branch", "critical", "From a C0 contraction semigroup with graph generator, derive every condition on the resolvent side.", "Stage1Instances.THM_M_0330.ForwardPackage", "The exact forward implication."),
    ("L-FWD-DENSE", "core_lemma", "critical", "Prove that the strong right-derivative generator has dense domain.", "planned Dense (A.domain : Set X)", "Dense generator domain."),
    ("L-FWD-CLOSED", "core_lemma", "critical", "Prove that the strong right-derivative generator is a closed LinearPMap.", "planned A.IsClosed", "Closed generator graph."),
    ("C-LAPLACE-RESOLVENT", "construction", "critical", "For each a > 0 construct the Laplace-transform resolvent as a bounded linear map.", "planned ∃ R : X →L[ℝ] X, IsContractiveResolvent A a R", "A bounded resolvent candidate."),
    ("L-RESOLVENT-LAWS", "core_lemma", "critical", "Prove both inverse equations for a I - A and the pointwise 1/a norm estimate.", "planned IsContractiveResolvent A a R", "The complete frozen resolvent predicate."),
    ("B-CONVERSE", "branch", "critical", "From density, closedness, and all positive contractive resolvents, construct the required C0 contraction semigroup and identify its generator.", "Stage1Instances.THM_M_0330.ConversePackage", "The exact converse implication."),
    ("C-YOSIDA", "construction", "critical", "Construct bounded Yosida approximants from the positive-axis resolvents and establish their algebraic identities.", "planned bounded Yosida approximants A_a", "A compatible family of bounded approximating generators."),
    ("C-APPROX-SEMIGROUP", "construction", "critical", "Construct the exponential semigroup of each bounded approximant.", "planned T_a : ℝ≥0 → X →L[ℝ] X", "Approximate contraction semigroups."),
    ("L-CONTRACTION", "core_lemma", "critical", "Derive uniform contraction estimates and semigroup laws for the approximant exponentials.", "planned IsC0ContractionSemigroup T_a", "Uniform semigroup estimates needed for passage to the limit."),
    ("L-STRONG-LIMIT", "core_lemma", "critical", "Prove strong convergence of approximant semigroups, locally uniformly in nonnegative time, and preserve continuity and multiplication.", "planned strong-limit construction of T", "A C0 contraction semigroup T."),
    ("T-GENERATOR", "terminal", "critical", "Identify the strong right-derivative graph of the limiting semigroup with exactly A, using density and closedness.", "planned IsGenerator A T", "Exact generator equality."),
    ("T-ASSEMBLE", "transport", "high", "Compose the exact forward and converse packages into the canonical iff.", "Stage1Instances.THM_M_0330.root_of_direction_packages", "The exact canonical root conditional on both packages."),
    ("X-EXTERNAL", "bridge", "high", "Pin, build, adapt, and audit any reused external forward-direction declarations.", "planned exact adapter to an immutable external child", "Audited child evidence only; never automatic root credit."),
    ("X-SOURCE", "terminal", "high", "Map every material analytic step to reviewed theorem/page, assumptions, conventions, and errata.", "non-machine primary-source node crosswalk", "Human-source coverage without proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, wrappers, axioms, trust boundaries, and replay evidence.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
expression_hash = json.loads((HERE / "statement.json").read_text())["canonical_formal_target"]["elaborated_expression_sha256"]

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    fp = f"lean-expression-sha256:{expression_hash}" if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0330/ObligationTree.lean#root_of_direction_packages" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"THM-M-0330-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H3", "machine_debt": "M0-L" if oid in checked else ("M4" if suffix != "ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or unchecked computation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only the exact formal context and incoming proof_requires children.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parent edges may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-0330/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen obligation or conditional interface only; no unlisted premise and no root closure.",
        "task_ids": [ITEM, "S56-M-0330-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0330/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-0330 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T12:00:00+08:00",
    "freeze_basis": "Exact frozen contraction statement and bounded anchor audit; forward Laplace-resolvent and converse Yosida-approximation architecture; eligibility assigned without regard to proof availability.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": oids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M4"},
    "status_boundary": "Architecture and denominators only; no Hille-Yosida direction, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-B-FORWARD", f"{PREFIX}-B-CONVERSE"],
    f"{PREFIX}-B-FORWARD": [f"{PREFIX}-L-FWD-DENSE", f"{PREFIX}-L-FWD-CLOSED", f"{PREFIX}-C-LAPLACE-RESOLVENT"],
    f"{PREFIX}-C-LAPLACE-RESOLVENT": [f"{PREFIX}-L-RESOLVENT-LAWS"],
    f"{PREFIX}-B-CONVERSE": [f"{PREFIX}-C-YOSIDA", f"{PREFIX}-C-APPROX-SEMIGROUP", f"{PREFIX}-L-CONTRACTION", f"{PREFIX}-L-STRONG-LIMIT", f"{PREFIX}-T-GENERATOR"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY"), edge("REF-ROOT-FOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-FOUNDATION")],
    "provenance": [edge("SRC-FWD", f"{PREFIX}-B-FORWARD", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-CONVERSE", f"{PREFIX}-B-CONVERSE", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT"), edge("PROV-EXTERNAL", f"{PREFIX}-X-EXTERNAL", "provenance_of", f"{PREFIX}-B-FORWARD")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE-FWD", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-B-FORWARD"), edge("DOC-SOURCE-CONV", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-B-CONVERSE")],
    "workflow": [edge("FLOW-ASSEMBLE-FWD", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-B-FORWARD"), edge("FLOW-ASSEMBLE-CONV", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-B-CONVERSE"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE"), edge("FLOW-EXTERNAL-AUDIT", f"{PREFIX}-X-EXTERNAL", "workflow_depends_on", f"{PREFIX}-L-RESOLVENT-LAWS")],
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
    "registry_id": "THM-M-0330-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-B-FORWARD", f"{PREFIX}-B-CONVERSE"], "composition_certificates": ["Stage1Instances.THM_M_0330.root_of_direction_packages"], "reason": "Final iff composition is conditional; neither directional package has a proof body."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
