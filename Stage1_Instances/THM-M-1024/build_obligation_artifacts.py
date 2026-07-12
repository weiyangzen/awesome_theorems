#!/usr/bin/env python3
"""Build the frozen THM-M-1024 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1024-OBLIGATION_TREE"
THEOREM = "THM-M-1024"
PREFIX = "M1024"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact all-dimensional Levy-Khintchine equivalence with convention-relative unique triplet.", "Stage1Instances.THM_M_1024.LevyKhintchineTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze probability laws, convolution powers, infinite divisibility, triplets, covariance, Levy measures, and representation.", "Stage1Instances.THM_M_1024.{IsProbabilityLaw,convolutionPow,InfinitelyDivisible,LevyTriplet,IsLevyMeasure,IsCovariance,Represents}", "The exact elaborated vocabulary."),
    ("S-CONVENTIONS", "normalization", "critical", "Preserve +i Fourier sign, -1/2 Gaussian coefficient, closed-unit-ball compensation, and triplet uniqueness.", "Stage1Instances.THM_M_1024.{levyExponent,LevyKhintchineTarget}", "The frozen representation convention."),
    ("S-BOUNDARY", "terminal", "high", "Retain dimension zero and allow zero covariance or zero jump measure without added nondegeneracy assumptions.", "Stage1Instances.THM_M_1024.Space 0 and frozen predicates", "Checked boundary scope."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical Bochner integration, measure extensionality, imports, axioms, TCB, and the no-oracle boundary.", "planned transitive foundation and axiom certificate", "Accepted foundation and trust profile."),
    ("N-EXPONENT", "normalization", "critical", "Establish measurability and integrability of the compensated jump integrand and normalize the characteristic exponent.", "planned exact exponent well-definedness theorem", "A well-defined exponent under IsLevyMeasure."),
    ("B-FORWARD", "branch", "critical", "Expand infinite divisibility into existence of representation data in every finite dimension.", "Stage1Instances.THM_M_1024.ForwardExistencePackage", "Existence of a representing triplet."),
    ("C-ARRAY", "construction", "critical", "Construct the infinitesimal convolution-root triangular array and its truncated drift, covariance, and jump characteristics.", "planned triangular-array construction with invariants", "Normalized approximating characteristics."),
    ("L-TIGHTNESS", "core_lemma", "critical", "Prove tightness and extract compatible drift, covariance, and Levy-measure limits from the root array.", "planned compactness and Levy-measure convergence theorem", "A candidate Levy triplet and convergence certificates."),
    ("L-FORWARD-IDENTITY", "core_lemma", "critical", "Pass to the characteristic-function limit and identify the frozen Levy exponent.", "planned all-dimensional Levy continuity/limit theorem", "Represents mu data for the constructed triplet."),
    ("B-CONVERSE", "branch", "critical", "Construct probability convolution roots from arbitrary valid representation data.", "Stage1Instances.THM_M_1024.ConversePackage", "Infinite divisibility from a representation."),
    ("C-REALIZATION", "construction", "critical", "Realize every scaled valid triplet as a probability law with the required characteristic function.", "planned all-dimensional realization theorem", "Probability laws for scaled triplets."),
    ("L-CONVOLUTION-ROOTS", "core_lemma", "critical", "Show the n-fold convolution of the law for the triplet scaled by 1/n has the original characteristic function and hence equals mu.", "planned charFun convolution/extensionality bridge", "Probability convolution roots of every positive order."),
    ("B-UNIQUENESS", "branch", "critical", "Prove equality of two triplets representing the same law under the frozen truncation.", "Stage1Instances.THM_M_1024.UniquenessPackage", "Convention-relative equality of triplets."),
    ("L-JUMP-UNIQUENESS", "core_lemma", "critical", "Recover the Levy measure away from zero from the exponent identity.", "planned Fourier uniqueness theorem for Levy measures", "Equality of jump measures."),
    ("L-GAUSSIAN-UNIQUENESS", "core_lemma", "critical", "Recover the symmetric positive-semidefinite covariance operator after cancelling the jump terms.", "planned quadratic-form polarization theorem", "Equality of covariance operators."),
    ("L-DRIFT-UNIQUENESS", "core_lemma", "high", "Recover the drift after cancelling the common jump and Gaussian terms.", "planned inner-product extensionality theorem", "Equality of drift vectors."),
    ("T-FORWARD", "terminal", "critical", "Compose array construction, tightness, and exponent identification into the forward package.", "Stage1Instances.THM_M_1024.ForwardExistencePackage", "The complete forward package."),
    ("T-CONVERSE", "terminal", "critical", "Compose realization and convolution-root identification into the converse package.", "Stage1Instances.THM_M_1024.ConversePackage", "The complete converse package."),
    ("T-UNIQUENESS", "terminal", "critical", "Compose jump, covariance, and drift recovery into the uniqueness package.", "Stage1Instances.THM_M_1024.UniquenessPackage", "The complete uniqueness package."),
    ("T-ASSEMBLE", "transport", "high", "Consume the exact forward, converse, and uniqueness packages to obtain the canonical ExistsUnique equivalence.", "Stage1Instances.THM_M_1024.root_of_packages", "The exact canonical root conditional on all three packages."),
    ("X-SOURCE", "terminal", "high", "Map every analytic bridge to a reviewed primary-source theorem/page, assumptions, conventions, and errata record.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-EXTERNAL", "bridge", "high", "Audit the one-dimensional LeanLevy candidate and any future all-dimensional formal candidate without transferring proof credit across mismatched types.", "external candidate integration/transport boundary", "Pinned provenance or an explicit non-integration result."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory every terminal body, wrapper, import, axiom, TCB edge, and replay receipt.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-CONVENTIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-CONVENTIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-source-sha256:" + hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fingerprint = statement_fp if suffix in {"ROOT", "S-DEFINITIONS", "S-CONVENTIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    terminal = "local:Stage1_Instances/THM-M-1024/ObligationTree.lean#root_of_packages" if suffix == "T-ASSEMBLE" else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": terminal,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else ("anchor-audit:LeanLevy-93b635f" if suffix == "X-EXTERNAL" else "none"),
        "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only the exact declared proof children and formal context.", "inference": claim, "output": output, "source_anchors": "pending node-specific primary-source crosswalk" if oid not in source_na else "not-applicable", "outgoing_use": "Only the declared typed parent may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-1024/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1024-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1024/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1024 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and immutable anchor audit; classical all-dimensional triangular-array/realization/uniqueness architecture; eligibility frozen independently of closure.",
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
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Levy-Khintchine proof, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-FORWARD", f"{PREFIX}-T-CONVERSE", f"{PREFIX}-T-UNIQUENESS"],
    f"{PREFIX}-T-FORWARD": [f"{PREFIX}-B-FORWARD"],
    f"{PREFIX}-B-FORWARD": [f"{PREFIX}-C-ARRAY", f"{PREFIX}-L-TIGHTNESS", f"{PREFIX}-L-FORWARD-IDENTITY", f"{PREFIX}-N-EXPONENT"],
    f"{PREFIX}-L-TIGHTNESS": [f"{PREFIX}-C-ARRAY"],
    f"{PREFIX}-L-FORWARD-IDENTITY": [f"{PREFIX}-L-TIGHTNESS", f"{PREFIX}-N-EXPONENT"],
    f"{PREFIX}-T-CONVERSE": [f"{PREFIX}-B-CONVERSE"],
    f"{PREFIX}-B-CONVERSE": [f"{PREFIX}-C-REALIZATION", f"{PREFIX}-L-CONVOLUTION-ROOTS", f"{PREFIX}-N-EXPONENT"],
    f"{PREFIX}-L-CONVOLUTION-ROOTS": [f"{PREFIX}-C-REALIZATION"],
    f"{PREFIX}-T-UNIQUENESS": [f"{PREFIX}-B-UNIQUENESS"],
    f"{PREFIX}-B-UNIQUENESS": [f"{PREFIX}-L-JUMP-UNIQUENESS", f"{PREFIX}-L-GAUSSIAN-UNIQUENESS", f"{PREFIX}-L-DRIFT-UNIQUENESS", f"{PREFIX}-N-EXPONENT"],
    f"{PREFIX}-L-GAUSSIAN-UNIQUENESS": [f"{PREFIX}-L-JUMP-UNIQUENESS"],
    f"{PREFIX}-L-DRIFT-UNIQUENESS": [f"{PREFIX}-L-JUMP-UNIQUENESS", f"{PREFIX}-L-GAUSSIAN-UNIQUENESS"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-CONV", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-CONVENTIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-FORWARD", f"{PREFIX}-B-FORWARD", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-CONVERSE", f"{PREFIX}-B-CONVERSE", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-UNIQUE", f"{PREFIX}-B-UNIQUENESS", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-EXTERNAL", f"{PREFIX}-X-EXTERNAL", "provenance_of", f"{PREFIX}-B-FORWARD"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-ROOT")],
    "workflow": [edge("FLOW-ASSEMBLE-FWD", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-FORWARD"), edge("FLOW-ASSEMBLE-CONV", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-CONVERSE"), edge("FLOW-ASSEMBLE-UNIQ", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-UNIQUENESS"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-FORWARD", f"{PREFIX}-T-CONVERSE", f"{PREFIX}-T-UNIQUENESS"], "composition_certificates": ["Stage1Instances.THM_M_1024.root_of_packages"], "reason": "Final composition is conditional; all three mathematical packages have no proof bodies."},
}
recipes = []
for oid in oids:
    recipes.append({"recipe_id": f"VAL-{oid}", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1024/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1024 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": ["Stage1Instances.THM_M_1024.root_of_packages"] if oid == f"{PREFIX}-T-ASSEMBLE" else []})
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
