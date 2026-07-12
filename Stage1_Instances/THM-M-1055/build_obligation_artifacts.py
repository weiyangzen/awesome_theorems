#!/usr/bin/env python3
"""Build the frozen THM-M-1055 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM, THEOREM, PREFIX = "S56-M-1055-OBLIGATION_TREE", "THM-M-1055", "M1055"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen real-valued ergodic Birkhoff target.", "Stage1Instances.THM_M_1055.BirkhoffErgodicTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze mathlib's Ergodic, Integrable, birkhoffAverage, integral, and almost-everywhere conventions.", "Stage1Instances.THM_M_1055.BirkhoffErgodicTarget", "The exact elaborated vocabulary."),
    ("S-BOUNDARY", "terminal", "high", "Preserve the zero-length average, empty-space semantics, probability normalization, and real-valued observable.", "Stage1Instances.THM_M_1055.birkhoffErgodicTarget_iff_expandedTarget", "Checked statement and boundary encoding."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, integration axioms, imports, TCB, and the no-oracle boundary.", "planned transitive axiom and import certificate", "Accepted foundation and trust profile."),
    ("A-EXTERNAL-INTEGRATION", "integration", "critical", "Pin and port the external pointwise-birkhoff theorem without name collisions or toolchain drift.", "lua-vr/pointwise-birkhoff@fc06094ca0506d8d74eba8b45b34882ce5930bf4", "A locally kernel-checked general pointwise theorem."),
    ("L-POINTWISE-LIMIT", "core_lemma", "critical", "Obtain almost-everywhere convergence of the averages to the invariant conditional expectation for every integrable observable.", "planned exact general pointwise Birkhoff theorem", "An almost-everywhere limit function with conditional-expectation provenance."),
    ("L-LIMIT-MEASURABLE", "core_lemma", "high", "Prove the selected limit has the measurability and integrability needed by the ergodic function API.", "planned limit measurability/integrability bridge", "A measurable integrable representative of the pointwise limit."),
    ("L-LIMIT-INVARIANT", "core_lemma", "critical", "Prove the selected limit is almost everywhere invariant under T.", "planned birkhoff-limit shift-invariance theorem", "g ∘ T = g almost everywhere."),
    ("L-ERGODIC-CONSTANCY", "bridge", "critical", "Use ergodicity to identify every measurable almost-everywhere invariant real limit with an almost-everywhere constant.", "Ergodic.ae_eq_const_of_ae_eq_comp_ae plus checked hypotheses", "g is almost everywhere equal to some constant."),
    ("L-INTEGRAL-IDENTIFICATION", "core_lemma", "critical", "Show the constant limit has the same integral as f and use probability normalization to identify it with integral f.", "planned integral-preservation and constant-integral bridge", "g = integral f almost everywhere."),
    ("T-INVARIANT-LIMIT", "terminal", "critical", "Combine pointwise convergence, invariance, ergodic constancy, and integral identification.", "Stage1Instances.THM_M_1055.InvariantLimitPackage", "The complete invariant-limit package."),
    ("T-ASSEMBLE", "transport", "high", "Rewrite the almost-everywhere pointwise limit to the constant integral and obtain the exact root.", "Stage1Instances.THM_M_1055.root_of_invariantLimitPackage", "The exact canonical root, conditional on the invariant-limit package."),
    ("X-SOURCE", "terminal", "high", "Map every analytic bridge to primary-source theorem/page, hypotheses, conventions, and errata.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, external origins, wrappers, imports, axioms, TCB edges, and replay receipts.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:8d7956f1f5f46ae435293eef17df7881f26d9c18fad6ac54c870e232cdb26181"
obligations, nodes = [], []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fp = statement_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind, "root_relevant": True,
        "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1055/ObligationTree.lean#root_of_invariantLimitPackage" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind, "human_statement": claim,
        "formal_target": target, "output": output, "human_debt": "H2",
        "machine_debt": "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else ("external-anchor-audit" if suffix == "A-EXTERNAL-INTEGRATION" else "none"),
        "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if suffix in {"A-EXTERNAL-INTEGRATION", "L-POINTWISE-LIMIT", "L-INTEGRAL-IDENTIFICATION"} else 40,
        "semantic_step_ledger": {"premises": "Only the exact declared proof children and formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-1055/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1055-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1055/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1055 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and anchor audit; external pointwise-limit then ergodic-collapse architecture; eligibility frozen independently of closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": oids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no pointwise ergodic proof, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-INVARIANT-LIMIT"],
    f"{PREFIX}-T-INVARIANT-LIMIT": [f"{PREFIX}-L-POINTWISE-LIMIT", f"{PREFIX}-L-ERGODIC-CONSTANCY", f"{PREFIX}-L-INTEGRAL-IDENTIFICATION"],
    f"{PREFIX}-L-POINTWISE-LIMIT": [f"{PREFIX}-A-EXTERNAL-INTEGRATION"],
    f"{PREFIX}-L-ERGODIC-CONSTANCY": [f"{PREFIX}-L-LIMIT-MEASURABLE", f"{PREFIX}-L-LIMIT-INVARIANT"],
    f"{PREFIX}-L-INTEGRAL-IDENTIFICATION": [f"{PREFIX}-L-POINTWISE-LIMIT", f"{PREFIX}-L-ERGODIC-CONSTANCY"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]
graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-POINTWISE", f"{PREFIX}-L-POINTWISE-LIMIT", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-EXTERNAL", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-A-EXTERNAL-INTEGRATION")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-L-POINTWISE-LIMIT")],
    "workflow": [edge("FLOW-INTEGRATE", f"{PREFIX}-L-POINTWISE-LIMIT", "workflow_depends_on", f"{PREFIX}-A-EXTERNAL-INTEGRATION"), edge("FLOW-PROV", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-A-EXTERNAL-INTEGRATION")],
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
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-INVARIANT-LIMIT"], "composition_certificates": ["Stage1Instances.THM_M_1055.root_of_invariantLimitPackage"], "reason": "Final composition is conditional; the invariant-limit package has no proof body."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1055/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact-pass-prefix"}], "covered_obligation_ids": [oid], "covered_declarations": [], "network_policy": "denied"} for oid in oids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
instance_path = HERE / "instance.json"
instance = json.loads(instance_path.read_text())
instance.update({"obligation_registry_hash": "sha256:" + denominator, "obligation_registry_version": 1, "obligation_tree_state": "self_tested_pending_master_acceptance", "canonical_claim_status": "exact_formal_statement_elaborated_obligation_architecture_frozen", "status_boundary": "Planned lifecycle with a self-tested obligation freeze pending master acceptance. Root remains H2/M3/R4; no pointwise ergodic proof, H0, audit completion, or theorem completion."})
instance["owned_artifacts"] = sorted(set(instance["owned_artifacts"] + ["ObligationTree.lean", "obligation-registry.json", "typed-graphs.json", "validation-specs.json", "obligation-tree.md", "obligation-tree-validation.md", "build_obligation_artifacts.py", "check_obligation_tree.py"]))
instance_path.write_text(json.dumps(instance, indent=2, ensure_ascii=True) + "\n")
print(denominator)
