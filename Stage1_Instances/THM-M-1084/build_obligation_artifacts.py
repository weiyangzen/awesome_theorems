#!/usr/bin/env python3
"""Build the frozen THM-M-1084 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1084-OBLIGATION_TREE"
THEOREM = "THM-M-1084"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


# The order is the frozen inventory denominator. Status is deliberately not an input.
rows = [
    ("M1084-ROOT", "root", "critical", "The exact constant-12 open-ball DudleyEntropyBoundTarget.", "Stage1Instances.THM_M_1084.DudleyEntropyBoundTarget", "The canonical proposition."),
    ("M1084-S-DEFINITIONS", "definition", "high", "Freeze open-ball covering numbers, entropyIntegral, canonicalDist, basedSupremum, and sample separation.", "Statement.lean definitions", "The exact statement interface."),
    ("M1084-S-BOUNDARY", "normalization", "high", "Preserve nonempty index, zero pseudodistance, singleton, zero diameter, epsilon-zero endpoint, and sInf conventions.", "Stage1Instances.THM_M_1084.singleton_coveringNumber and planned endpoint lemmas", "Boundary behavior without silently changing the theorem."),
    ("M1084-S-FOUNDATION", "certificate", "critical", "Freeze classical noncomputable measure theory, choice, imports, axioms, and no-oracle policy.", "planned transitive foundation certificate", "Audited trust boundary."),
    ("M1084-N-GAUSSIAN-MGF", "bridge", "critical", "Derive the exact sub-Gaussian increment MGF estimate from joint Gaussianity, centering, and canonicalDist.", "planned Gaussian-to-subGaussian increment theorem", "An MGF bound at scale dist for every increment."),
    ("M1084-C-NETS", "construction", "critical", "Choose finite open-ball nets at dyadic radii from total boundedness and the custom least-cardinality coveringNumber.", "planned finite-net construction with cardinality certificate", "Nested scales with certified cover sizes."),
    ("M1084-C-CHAIN", "construction", "critical", "Choose parent maps between successive nets and telescope each dense index through the chain.", "planned dyadic chaining construction", "A finite telescoping increment decomposition at every truncation."),
    ("M1084-L-MAX-INCREMENT", "core_lemma", "critical", "Bound the expectation of a finite maximum of sub-Gaussian increments by sqrt(log cardinality) times the scale.", "planned finite subGaussian maximum lemma", "One-scale expected-maximum bound."),
    ("M1084-L-DYADIC-SUM", "core_lemma", "critical", "Sum the one-scale estimates and compare the dyadic entropy sum with 12 times the frozen interval integral.", "planned entropy sum-to-integral comparison", "The exact constant-12 finite-chain bound."),
    ("M1084-L-LIMIT", "core_lemma", "critical", "Pass finite chains to the countable separating supremum with measurability and expectation control.", "planned sample-separable limit theorem", "The expected-supremum inequality for the dense sequence."),
    ("M1084-T-INTEGRABLE", "terminal", "critical", "Prove integrability of basedSupremum from the same chaining domination, not merely existence of an integral value.", "Stage1Instances.THM_M_1084.SupremumIntegrabilityPackage", "The exact first conjunct."),
    ("M1084-T-ENTROPY", "terminal", "critical", "Prove the exact constant-12 inequality with all original hypotheses retained.", "Stage1Instances.THM_M_1084.EntropyInequalityPackage", "The exact second conjunct."),
    ("M1084-T-ASSEMBLE", "transport", "high", "Combine the two exact conjunct packages without weakening or adding a premise to the root.", "Stage1Instances.THM_M_1084.root_of_integrability_and_entropy_packages", "The exact canonical root, conditional on both packages."),
    ("M1084-X-SOURCE", "source_boundary", "high", "Map every chaining step and normalization to reviewed primary-source passages and errata.", "planned node-specific primary-source crosswalk", "Human-source coverage only."),
    ("M1084-X-EXTERNAL", "provenance_boundary", "critical", "Track the audited SLT.Dudley candidate and every required incompatibility bridge without proof credit until pinned and replayed.", "anchor-audit candidate S56-M-1084-C03", "External-anchor provenance and compatibility record."),
    ("M1084-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, axioms, TCB, recipes, and independent replay evidence.", "planned release provenance certificate", "Machine provenance coverage without mathematical proof credit."),
]

checked = {"M1084-S-DEFINITIONS", "M1084-S-BOUNDARY", "M1084-T-ASSEMBLE"}
source_na = {"M1084-S-DEFINITIONS", "M1084-S-FOUNDATION", "M1084-X-EXTERNAL", "M1084-X-PROVENANCE"}
machine_special = {"M1084-X-SOURCE": "not_applicable", "M1084-X-EXTERNAL": "informational", "M1084-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = "lean-expression-sha256:25bdfe85eaaa67694f865e6af60c240b013b2fbcd9acfb2949e5abdb0b34ca99" if oid == "M1084-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "source overlay has no machine-proof credit", "informational": "provenance overlay has no terminal-proof credit"}.get(machine),
        "terminal_proof_body_id": "local:ObligationTree.lean#root_of_integrability_and_entropy_packages" if oid == "M1084-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": oid, "obligation_id": oid, "kind": kind, "human_statement": claim,
        "formal_target": target, "output": output,
        "human_debt": "not_applicable" if oid in source_na else "H2",
        "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1084-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "node-pinpoint-review-pending",
        "provenance_id": "local-conditional-composition" if oid == "M1084-T-ASSEMBLE" else ("anchor-S56-M-1084-C03" if oid == "M1084-X-EXTERNAL" else "none"),
        "foundation_profile": "lean4-classical-noncomputable-measure-theory/audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation or oracle may close this node",
        "step_budget": 100 if oid in {"M1084-N-GAUSSIAN-MGF", "M1084-L-LIMIT", "M1084-L-DYADIC-SUM"} else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires children and the frozen formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1084/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1084-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1084/ObligationTree.lean"] if oid in {"M1084-T-INTEGRABLE", "M1084-T-ENTROPY", "M1084-T-ASSEMBLE"} else [],
        "owner": "THM-M-1084 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; native dyadic chaining architecture selected before closure metrics were observed.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1084-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1084-X-EXTERNAL", "M1084-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen denominators and architecture only; neither terminal package is proved and the theorem remains open.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1084-ROOT": ["M1084-T-ASSEMBLE"],
    "M1084-T-ASSEMBLE": ["M1084-T-INTEGRABLE", "M1084-T-ENTROPY"],
    "M1084-T-INTEGRABLE": ["M1084-L-LIMIT"],
    "M1084-T-ENTROPY": ["M1084-L-LIMIT", "M1084-L-DYADIC-SUM"],
    "M1084-L-LIMIT": ["M1084-C-CHAIN", "M1084-L-MAX-INCREMENT"],
    "M1084-L-DYADIC-SUM": ["M1084-C-NETS", "M1084-L-MAX-INCREMENT"],
    "M1084-C-CHAIN": ["M1084-C-NETS"],
    "M1084-L-MAX-INCREMENT": ["M1084-N-GAUSSIAN-MGF"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1084-ROOT", "logical_decomposition", "M1084-S-DEFINITIONS"), edge("REF-ROOT-BOUNDARY", "M1084-ROOT", "logical_decomposition", "M1084-S-BOUNDARY")],
    "provenance": [edge("SRC-CHAIN", "M1084-L-DYADIC-SUM", "source_map", "M1084-X-SOURCE"), edge("PROV-EXTERNAL", "M1084-X-EXTERNAL", "provenance_of", "M1084-T-ENTROPY"), edge("PROV-ROOT", "M1084-X-PROVENANCE", "provenance_of", "M1084-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1084-ROOT", "trusts", "M1084-S-FOUNDATION"), edge("TRUST-PROV", "M1084-ROOT", "trusts", "M1084-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M1084-S-DEFINITIONS", "documents", "M1084-ROOT"), edge("DOC-SOURCE", "M1084-X-SOURCE", "documents", "M1084-L-DYADIC-SUM")],
    "workflow": [edge("FLOW-ASSEMBLE-I", "M1084-T-ASSEMBLE", "workflow_depends_on", "M1084-T-INTEGRABLE"), edge("FLOW-ASSEMBLE-E", "M1084-T-ASSEMBLE", "workflow_depends_on", "M1084-T-ENTROPY"), edge("FLOW-PROV-ASSEMBLE", "M1084-X-PROVENANCE", "workflow_depends_on", "M1084-T-ASSEMBLE")],
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
    "registry_id": "THM-M-1084-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "statement_source_sha256": statement_hash, "anchor_audit_sha256": anchor_hash,
    "root_node_id": "M1084-ROOT", "edge_direction": "proof_requires: parent to child; reciprocal composes: child to parent",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1084-T-INTEGRABLE", "M1084-T-ENTROPY"], "composition_certificates": ["Stage1Instances.THM_M_1084.root_of_integrability_and_entropy_packages"], "reason": "Final composition is checked but both exact package premises remain unproved."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1084/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
