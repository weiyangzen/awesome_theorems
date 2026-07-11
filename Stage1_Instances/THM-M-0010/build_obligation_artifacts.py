#!/usr/bin/env python3
"""Build the frozen THM-M-0010 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0010-OBLIGATION_TREE"
THEOREM = "THM-M-0010"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


ROWS = [
    ("M0010-ROOT", "root", "critical", "The exact frozen Artin-Rees equality for every finite module and submodule over a commutative Noetherian ring.", "Stage1Instances.THM_M_0010.ArtinReesTarget", "The canonical proposition."),
    ("M0010-S-EXACT", "definition", "critical", "Preserve the ordered universes, typeclasses, ideal, module, submodule, existential witness, lower-bound guard, and equality.", "Stage1Instances.THM_M_0010.ArtinReesTarget", "The exact binder and conclusion boundary."),
    ("M0010-S-BOUNDARY", "branch", "high", "Retain the bottom/top ideal, bottom submodule, and n = k boundary behavior under natural subtraction.", "Stage1Instances.THM_M_0010.boundaryBottomIdeal and related statement probes", "An explicit degenerate-case policy."),
    ("M0010-C-STABLE", "construction", "critical", "Construct the stable I-adic filtration on the top submodule using Noetherianity and module finiteness.", "Ideal.stableFiltration_stable", "Stability of the ambient I-adic filtration."),
    ("M0010-C-INTER", "construction", "critical", "Intersect the stable ambient filtration with the trivial filtration on N and preserve stability.", "Ideal.Filtration.Stable.inter_right", "Stability of the induced filtration on N."),
    ("M0010-L-EVENTUAL", "core_lemma", "critical", "Extract a uniform k from filtration stability and derive the eventual shifted power equality for all n at least k.", "Ideal.Filtration.Stable.exists_pow_smul_eq_of_ge", "The quantified eventual equality."),
    ("M0010-B-UPSTREAM", "bridge", "critical", "Audit the pinned mathlib Artin-Rees theorem as the composition of the stable-filtration construction, intersection, and eventual-equality lemma.", "Ideal.exists_pow_inf_eq_pow_smul", "One exact terminal candidate body."),
    ("M0010-T-COMPOSE", "terminal", "high", "Transport the exact candidate package to the identical frozen root without changing assumptions or conclusion.", "Stage1Instances.THM_M_0010.ObligationTree.root_of_exact_candidate", "The exact canonical root conditional on the candidate package."),
    ("M0010-X-SOURCE", "terminal", "high", "Map the stable-filtration route and equality to pinpoint reviewed primary-source passages and errata records.", "non-machine node-specific source crosswalk", "Human-source coverage only."),
    ("M0010-X-FOUNDATION", "certificate", "critical", "Inventory terminal declarations, transitive imports, axioms, TCB, body identity, and replay evidence.", "planned machine-derived trust and provenance report", "Release trust/provenance coverage without proof credit."),
]

statement = json.loads((HERE / "statement.json").read_text())
statement_fp = statement["canonical_formal_target"]["elaborated_expression_sha256"]
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
source_na = {"M0010-S-EXACT", "M0010-S-BOUNDARY", "M0010-X-FOUNDATION"}
machine_special = {"M0010-X-SOURCE": "not_applicable", "M0010-X-FOUNDATION": "informational"}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in ROWS:
    fp = ("lean-expression-sha256:" + statement_fp if oid in {"M0010-ROOT", "M0010-S-EXACT"}
          else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    terminal = {
        "M0010-B-UPSTREAM": "mathlib:8a178386:Ideal.exists_pow_inf_eq_pow_smul",
        "M0010-T-COMPOSE": "local:Stage1_Instances/THM-M-0010/ObligationTree.lean#root_of_exact_candidate",
    }.get(oid)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": oid not in {"M0010-X-SOURCE", "M0010-X-FOUNDATION"},
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "trust_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": terminal,
    })
    nodes.append({
        "node_id": "THM-M-0010-" + oid.removeprefix("M0010-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M1" if oid == "M0010-B-UPSTREAM" else ("M3" if oid == "M0010-T-COMPOSE" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "pinned-mathlib-candidate-audited" if oid == "M0010-B-UPSTREAM" else "none",
        "foundation_profile": "Lean kernel plus pinned mathlib; candidate reports propext, Classical.choice, Quot.sound; acceptance pending",
        "tcb_profile": "Lean 4.29.0 and mathlib 8a178386; transitive release audit pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if oid in {"M0010-C-STABLE", "M0010-C-INTER", "M0010-L-EVENTUAL"} else 40,
        "semantic_step_ledger": {"premises": "Only declared proof children and the frozen formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or support edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0010/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture only; no obligation is credited closed or accepted in this phase.",
        "task_ids": [ITEM, "S56-M-0010-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0010/ObligationTree.lean"] if oid == "M0010-T-COMPOSE" else [],
        "owner": "THM-M-0010 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain", "mathlib revision"], "revocation_state": "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and pinned anchor audit; stable-filtration architecture assigned before proof-phase closure observation.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0010-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0010-X-SOURCE", "M0010-X-FOUNDATION"]},
    "delta_policy": "Any correction, split, merge, exclusion, risk, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": [], "root_machine_debt": "M4"},
    "status_boundary": "The architecture is frozen; proof, source, readable, trust, validation, and release acceptance remain open.",
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0010-ROOT": ["M0010-S-EXACT", "M0010-S-BOUNDARY", "M0010-T-COMPOSE"],
    "M0010-T-COMPOSE": ["M0010-B-UPSTREAM"],
    "M0010-B-UPSTREAM": ["M0010-C-STABLE", "M0010-C-INTER", "M0010-L-EVENTUAL"],
    "M0010-C-INTER": ["M0010-C-STABLE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-BOUNDARY", "M0010-ROOT", "logical_decomposition", "M0010-S-BOUNDARY")],
    "provenance": [edge("PROV-UPSTREAM", "M0010-X-FOUNDATION", "provenance_of", "M0010-B-UPSTREAM"), edge("SRC-EVENTUAL", "M0010-L-EVENTUAL", "source_map", "M0010-X-SOURCE")],
    "evidence": [],
    "trust": [edge("TRUST-ROOT", "M0010-ROOT", "trusts", "M0010-X-FOUNDATION")],
    "documentation": [edge("DOC-SOURCE", "M0010-X-SOURCE", "documents", "M0010-ROOT"), edge("DOC-BOUNDARY", "M0010-S-BOUNDARY", "documents", "M0010-ROOT")],
    "workflow": [edge("FLOW-CANDIDATE-COMPOSE", "M0010-T-COMPOSE", "workflow_depends_on", "M0010-B-UPSTREAM"), edge("FLOW-PROVENANCE-CANDIDATE", "M0010-X-FOUNDATION", "workflow_depends_on", "M0010-B-UPSTREAM")],
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
    "registry_id": "THM-M-0010-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0010-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0010-S-EXACT", "M0010-S-BOUNDARY", "M0010-B-UPSTREAM"], "composition_certificates": ["Stage1Instances.THM_M_0010.ObligationTree.root_of_exact_candidate"], "reason": "Only a conditional identity composition is checked; all proof and acceptance credit remains for later phases."},
}

recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0010/check_obligation_tree.py"], "env_allowlist": {"PATH": "runner-provided-pinned-toolchain"}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS and denominator digest"}], "covered_obligation_ids": [oid], "covered_declarations": ["Stage1Instances.THM_M_0010.ObligationTree.root_of_exact_candidate"] if oid == "M0010-T-COMPOSE" else []} for oid, *_ in ROWS]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
