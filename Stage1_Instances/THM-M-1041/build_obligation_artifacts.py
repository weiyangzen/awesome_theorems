#!/usr/bin/env python3
"""Build the frozen THM-M-1041 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1041-OBLIGATION_TREE"
THEOREM = "THM-M-1041"
PREFIX = "M1041"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen real contraction Hille--Yosida equivalence.", "Stage1Instances.THM_M_1041.HilleYosidaContractionTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze the semigroup, generator, and bounded two-sided resolvent predicates.", "Stage1Instances.THM_M_1041.{IsC0ContractionSemigroup,IsGenerator,IsContractiveResolvent}", "The elaborated vocabulary."),
    ("S-BOUNDARY", "terminal", "high", "Preserve zero time, strict positivity of the resolvent parameter, the zero space, and real scalars.", "Stage1Instances.THM_M_1041.target_iff_expanded", "Checked statement boundary behavior."),
    ("S-FOUNDATION", "certificate", "critical", "Audit imports, classical choice, functional-analysis TCB, and the no-oracle boundary.", "planned transitive axiom and import certificate", "Accepted foundation profile."),
    ("F-CLOSED", "core_lemma", "critical", "Prove that the generator of the given C0 contraction semigroup is closed.", "planned generator closedness theorem", "A.IsClosed."),
    ("F-DENSE", "core_lemma", "critical", "Prove that the generator domain is dense using strong continuity at zero.", "planned generator-domain density theorem", "Dense (A.domain : Set X)."),
    ("F-RESOLVENT-CONSTRUCT", "construction", "critical", "For every positive a construct the Laplace-transform resolvent as a bounded linear map.", "planned Bochner/Laplace resolvent construction", "R : X ->L[Real] X with construction invariants."),
    ("F-RESOLVENT-RIGHT", "core_lemma", "critical", "Show (a I - A)(R y)=y and that R y lies in the generator domain.", "planned resolvent range and right-inverse theorem", "The first IsContractiveResolvent conjunct."),
    ("F-RESOLVENT-LEFT", "core_lemma", "critical", "Show R((a I - A)x)=x for every x in A.domain.", "planned resolvent left-inverse theorem", "The second IsContractiveResolvent conjunct."),
    ("F-RESOLVENT-BOUND", "core_lemma", "critical", "Derive the contraction bound norm(R y) <= a^-1 norm(y).", "planned Laplace resolvent norm estimate", "The third IsContractiveResolvent conjunct."),
    ("F-ASSEMBLE", "transport", "high", "Assemble closedness, density, and all resolvent fields into the forward package.", "Stage1Instances.THM_M_1041.ForwardPackage", "The complete forward implication."),
    ("C-YOSIDA-APPROX", "construction", "critical", "Define bounded Yosida approximants from the resolvent family and prove compatibility estimates.", "planned A_a = a A R(a,A) construction", "A coherent bounded approximation family."),
    ("C-SEMIGROUP-CONSTRUCT", "construction", "critical", "Construct the limiting semigroup from exponentials of the Yosida approximants.", "planned Yosida exponential limit construction", "T : NNReal -> X ->L[Real] X."),
    ("C-SEMIGROUP-LAWS", "core_lemma", "critical", "Prove T(0)=I and T(s+t)=T(s) comp T(t).", "planned limit semigroup-law theorem", "The algebraic semigroup fields."),
    ("C-STRONG-CONTINUITY", "core_lemma", "critical", "Prove continuity of every orbit of the constructed semigroup.", "planned strong-continuity theorem", "The orbit-continuity field."),
    ("C-CONTRACTION", "core_lemma", "critical", "Pass the approximant norm estimates to the contraction bound for T.", "planned contraction estimate", "The semigroup contraction field."),
    ("C-GENERATOR", "core_lemma", "critical", "Identify the strong right-derivative graph of T at zero with the original LinearPMap A.", "planned generator-identification theorem", "IsGenerator A T."),
    ("C-ASSEMBLE", "transport", "high", "Assemble construction and invariants into the converse package.", "Stage1Instances.THM_M_1041.ConversePackage", "The complete converse implication."),
    ("T-ASSEMBLE", "transport", "high", "Compose the forward and converse packages into the exact Iff root.", "Stage1Instances.THM_M_1041.root_of_directionPackages", "The exact root conditional on both directions."),
    ("X-SOURCE", "terminal", "high", "Map every analytic bridge to a reviewed primary-source theorem/page, assumptions, conventions, and errata.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, external child anchors, wrappers, imports, axioms, TCB edges, and replay receipts.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
root_fp = "lean-expression-sha256:e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d"

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fingerprint = root_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    proof_body = "local:Stage1_Instances/THM-M-1041/ObligationTree.lean#root_of_directionPackages" if suffix == "T-ASSEMBLE" else None
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
        "exclusion_reason": exclusion, "terminal_proof_body_id": proof_body,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M4" if suffix == "ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-functional-analysis/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only the declared proof children and exact formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parents may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1041/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1041-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1041/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1041 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus bounded anchor audit; forward Laplace-resolvent and converse Yosida-approximation architecture; eligibility frozen independently of closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": oids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M4"},
    "status_boundary": "Scope and denominators only; no Hille--Yosida proof, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-F-ASSEMBLE", f"{PREFIX}-C-ASSEMBLE"],
    f"{PREFIX}-F-ASSEMBLE": [f"{PREFIX}-F-CLOSED", f"{PREFIX}-F-DENSE", f"{PREFIX}-F-RESOLVENT-RIGHT", f"{PREFIX}-F-RESOLVENT-LEFT", f"{PREFIX}-F-RESOLVENT-BOUND"],
    f"{PREFIX}-F-RESOLVENT-RIGHT": [f"{PREFIX}-F-RESOLVENT-CONSTRUCT"],
    f"{PREFIX}-F-RESOLVENT-LEFT": [f"{PREFIX}-F-RESOLVENT-CONSTRUCT"],
    f"{PREFIX}-F-RESOLVENT-BOUND": [f"{PREFIX}-F-RESOLVENT-CONSTRUCT"],
    f"{PREFIX}-C-ASSEMBLE": [f"{PREFIX}-C-SEMIGROUP-CONSTRUCT", f"{PREFIX}-C-SEMIGROUP-LAWS", f"{PREFIX}-C-STRONG-CONTINUITY", f"{PREFIX}-C-CONTRACTION", f"{PREFIX}-C-GENERATOR"],
    f"{PREFIX}-C-SEMIGROUP-CONSTRUCT": [f"{PREFIX}-C-YOSIDA-APPROX"],
    f"{PREFIX}-C-SEMIGROUP-LAWS": [f"{PREFIX}-C-SEMIGROUP-CONSTRUCT"],
    f"{PREFIX}-C-STRONG-CONTINUITY": [f"{PREFIX}-C-SEMIGROUP-CONSTRUCT"],
    f"{PREFIX}-C-CONTRACTION": [f"{PREFIX}-C-SEMIGROUP-CONSTRUCT"],
    f"{PREFIX}-C-GENERATOR": [f"{PREFIX}-C-SEMIGROUP-CONSTRUCT", f"{PREFIX}-C-YOSIDA-APPROX"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-FORWARD", f"{PREFIX}-F-ASSEMBLE", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-CONVERSE", f"{PREFIX}-C-ASSEMBLE", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-ROOT")],
    "workflow": [edge("FLOW-ASSEMBLE-FWD", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-F-ASSEMBLE"), edge("FLOW-ASSEMBLE-CONV", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-C-ASSEMBLE"), edge("FLOW-PROV", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "registry_id": f"{THEOREM}-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-F-ASSEMBLE", f"{PREFIX}-C-ASSEMBLE"], "composition_certificates": ["Stage1Instances.THM_M_1041.root_of_directionPackages"], "reason": "Final composition is conditional; neither substantive direction has a proof body."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

instance_path = HERE / "instance.json"
instance = json.loads(instance_path.read_text())
instance["obligation_registry_hash"] = "sha256:" + denominator
instance["obligation_registry_version"] = 1
instance["obligation_tree_state"] = "self_tested_pending_master_acceptance"
instance["canonical_claim_status"] = "exact_formal_statement_elaborated_obligation_architecture_frozen"
instance["status_boundary"] = "Planned lifecycle with an elaborated exact statement and self-tested obligation freeze pending master acceptance. Root remains H2/M4/R4; no Hille--Yosida proof, H0 source fidelity, audit completion, or theorem completion is claimed."
new_files = ["ObligationTree.lean", "obligation-registry.json", "typed-graphs.json", "validation-specs.json", "obligation-tree.md", "obligation-tree-validation.md", "build_obligation_artifacts.py", "check_obligation_tree.py"]
instance["owned_artifacts"] = sorted(set(instance["owned_artifacts"] + new_files))
instance_path.write_text(json.dumps(instance, indent=2, ensure_ascii=True) + "\n")
print(denominator)
