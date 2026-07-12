#!/usr/bin/env python3
"""Build the frozen THM-M-1023 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM, THEOREM, PREFIX = "S56-M-1023-OBLIGATION_TREE", "THM-M-1023", "M1023"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "Exact real-line infinitely-divisible iff Levy-Khinchin target.", "Stage1Instances.THM_M_1023.InfinitelyDivisibleIffLevyKhintchine", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze convolution powers, infinite divisibility, triplet data, exponent, representation, and uniqueness.", "Stage1Instances.THM_M_1023.{convolutionPower,IsInfinitelyDivisible,LevyKhintchineData,Represents,HasLevyKhintchineRepresentation}", "Exact elaborated vocabulary."),
    ("S-BOUNDARY", "terminal", "high", "Preserve positive root order, probability roots, Dirac laws, and zero Gaussian or jump components.", "Stage1Instances.THM_M_1023.target_iff_expanded", "Checked target expansion and boundary scope."),
    ("S-FOUNDATION", "certificate", "critical", "Audit imports, classical choice, quotient/extensionality use, TCB, and no-oracle policy.", "planned transitive axiom/import certificate", "Accepted foundation profile."),
    ("N-CONVENTION", "normalization", "critical", "Normalize every source theorem to positive-sign charFun and truncation x*1_{|x|<=1}, including the induced drift transport.", "planned checked convention transport", "Claims in the frozen exponent convention."),
    ("F-COHERENT-ROOTS", "core_lemma", "critical", "From roots of every order obtain a coherent characteristic-exponent/logarithm object without assuming nonvanishing or branch compatibility.", "planned coherent logarithm theorem", "A continuous negative-definite exponent for mu."),
    ("F-TRIPLET-EXISTS", "construction", "critical", "Construct drift, nonnegative Gaussian variance, and a Levy measure satisfying no-atom and min-one-square integrability.", "planned Levy triplet construction", "Valid LevyKhintchineData."),
    ("F-REPRESENTS", "core_lemma", "critical", "Prove the constructed data's exponent is integrable and its exponential equals charFun mu at every real frequency.", "planned representation identity", "Represents mu d."),
    ("F-UNIQUE", "core_lemma", "critical", "Prove uniqueness of drift, Gaussian variance, and jump measure in the selected truncation convention.", "planned triplet uniqueness theorem", "All representing data equal the constructed data."),
    ("T-FORWARD", "terminal", "critical", "Assemble exponent construction, representation, and uniqueness into the complete forward implication.", "Stage1Instances.THM_M_1023.ForwardPackage", "Infinite divisibility implies the selected unique representation."),
    ("R-SCALE-DATA", "construction", "critical", "For each positive n scale the Levy triplet by 1/n and verify all structure side conditions.", "planned scaled-triplet construction", "Valid nth-root Levy data."),
    ("R-ROOT-MEASURE", "core_lemma", "critical", "Construct a probability measure having the scaled exponent; do not assume the desired measure-existence theorem as data.", "planned positive-definite/existence theorem", "A probability root candidate with the scaled characteristic function."),
    ("R-CONVOLUTION-POWER", "core_lemma", "critical", "Use charFun convolution multiplicativity, exponential scaling, and ext_of_charFun to identify the nth convolution power with mu.", "planned characteristic-function power and extensionality theorem", "convolutionPower root n = mu."),
    ("T-REVERSE", "terminal", "critical", "Produce a probability convolution root for every strictly positive n.", "Stage1Instances.THM_M_1023.ReversePackage", "Representation implies infinite divisibility."),
    ("T-ASSEMBLE", "transport", "high", "Combine the exact forward and reverse packages into the frozen biconditional.", "Stage1Instances.THM_M_1023.root_of_directionPackages", "The exact canonical root, conditional on both directions."),
    ("X-SOURCE", "terminal", "high", "Map every analytic bridge to primary-source theorem/page, assumptions, convention, and errata records.", "non-machine node-specific source crosswalk", "Human-source coverage without proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, axioms, TCB edges, and replay receipts.", "planned machine-derived provenance closure", "Release provenance without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
root_fp = "lean-expression-sha256:f84253c83a8c31d9b77246bc0b3eef7715b0d0a04b707bb91cd5c329fdde1a2f"

obligations, nodes = [], []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fingerprint = root_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1023/ObligationTree.lean#root_of_directionPackages" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact declared proof children and formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parents may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1023/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1023-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1023/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1023 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and anchor audit; two-direction Levy-Khinchin architecture; eligibility frozen independently of observed closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": oids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Levy-Khinchin direction, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-FORWARD", f"{PREFIX}-T-REVERSE"],
    f"{PREFIX}-T-FORWARD": [f"{PREFIX}-N-CONVENTION", f"{PREFIX}-F-COHERENT-ROOTS", f"{PREFIX}-F-TRIPLET-EXISTS", f"{PREFIX}-F-REPRESENTS", f"{PREFIX}-F-UNIQUE"],
    f"{PREFIX}-F-TRIPLET-EXISTS": [f"{PREFIX}-F-COHERENT-ROOTS"],
    f"{PREFIX}-F-REPRESENTS": [f"{PREFIX}-F-TRIPLET-EXISTS"],
    f"{PREFIX}-F-UNIQUE": [f"{PREFIX}-N-CONVENTION"],
    f"{PREFIX}-T-REVERSE": [f"{PREFIX}-N-CONVENTION", f"{PREFIX}-R-SCALE-DATA", f"{PREFIX}-R-ROOT-MEASURE", f"{PREFIX}-R-CONVOLUTION-POWER"],
    f"{PREFIX}-R-ROOT-MEASURE": [f"{PREFIX}-R-SCALE-DATA"],
    f"{PREFIX}-R-CONVOLUTION-POWER": [f"{PREFIX}-R-ROOT-MEASURE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-FORWARD", f"{PREFIX}-T-FORWARD", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-REVERSE", f"{PREFIX}-T-REVERSE", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-T-FORWARD")],
    "workflow": [edge("FLOW-ASSEMBLE-F", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-FORWARD"), edge("FLOW-ASSEMBLE-R", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-REVERSE"), edge("FLOW-PROV", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-FORWARD", f"{PREFIX}-T-REVERSE"], "composition_certificates": ["Stage1Instances.THM_M_1023.root_of_directionPackages"], "reason": "Final composition is conditional; neither mathematical direction has a proof body."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1023/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

instance_path = HERE / "instance.json"
instance = json.loads(instance_path.read_text())
instance["obligation_registry_hash"] = "sha256:" + denominator
instance["obligation_registry_version"] = 1
instance["obligation_tree_state"] = "self_tested_pending_master_acceptance"
instance["status_boundary"] = "Planned lifecycle with exact statement and self-tested obligation freeze pending master acceptance. Root remains H1/M3/R4; neither Levy-Khinchin direction, H0 source fidelity, audit completion, nor theorem completion is claimed."
new_files = ["ObligationTree.lean", "obligation-registry.json", "typed-graphs.json", "validation-specs.json", "obligation-tree.md", "obligation-tree-validation.md", "build_obligation_artifacts.py", "check_obligation_tree.py"]
instance["public_merge_targets"] = sorted(set(instance["public_merge_targets"] + [f"Stage1_Instances/THM-M-1023/{name}" for name in new_files]))
instance_path.write_text(json.dumps(instance, indent=2, ensure_ascii=True) + "\n")
print(denominator)
