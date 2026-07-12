#!/usr/bin/env python3
"""Build the frozen THM-M-0708 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0708-OBLIGATION_TREE"
THEOREM = "THM-M-0708"


def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0708-ROOT", "root", "critical", "The exact frozen functional Rice theorem.", "Stage1Instances.THM_M_0708.RiceTheoremTarget", "Noncomputability of every nontrivial semantic index predicate."),
    ("M0708-S-STATEMENT", "definition", "high", "Freeze unary partial-function semantics, code evaluation, predicate computability, and ordered witnesses.", "Stage1Instances.THM_M_0708.RiceTheoremTarget", "The exact canonical interface and context."),
    ("M0708-S-BOUNDARY", "branch", "high", "Account for empty and universal semantic classes and show why both witness premises are required.", "Stage1Instances.THM_M_0708.{empty_property_is_computable,universal_property_is_computable}", "Degenerate properties are excluded without weakening the target."),
    ("M0708-S-FOUNDATION", "certificate", "critical", "Fix the classical-choice, quotient, extensional semantic equality, kernel, and no-oracle policy.", "planned transitive axiom and trust report", "An accepted foundation and trust boundary."),
    ("M0708-N-WITNESSES", "normalization", "normal", "Unpack represented positive and negative witnesses while preserving their order and shared semantic class.", "planned witness-normalization interface", "Named f, g, their Partrec evidence, f membership, and g nonmembership."),
    ("M0708-L-RICE-BRIDGE", "bridge", "critical", "For a computable semantic code predicate, transfer membership from any represented f to any represented g.", "Stage1Instances.THM_M_0708.RiceBridge", "Represented semantic properties are constant under a computable index predicate."),
    ("M0708-L-FIXED-POINT", "bridge", "critical", "Audit and expose the fixed-point construction used by the pinned Rice theorem body.", "Nat.Partrec.Code.fixed_point2 dependency interface", "A self-referential code with the evaluation equation required by Rice's argument."),
    ("M0708-C-COND", "construction", "critical", "Construct the conditional partial-recursive program selected by the decidable semantic index predicate.", "Nat.Partrec.cond construction inside ComputablePred.rice", "A represented partial function switching between the two semantic witnesses."),
    ("M0708-L-SEMANTIC-TRANSFER", "core_lemma", "critical", "Use fixed-point evaluation and extensional semantic membership to force the conditional code into the positive branch.", "planned expansion of Mathlib.Computability.Halting.ComputablePred.rice", "Membership of the fixed-point evaluation in C."),
    ("M0708-T-CONTRADICTION", "terminal", "normal", "Apply the negative witness to the bridge-derived membership of g.", "planned exact contradiction interface", "False from g in C and g not in C."),
    ("M0708-T-ASSEMBLE", "transport", "high", "Consume the exact Rice bridge and both witnesses to yield the frozen root.", "Stage1Instances.THM_M_0708.root_of_riceBridge", "The exact RiceTheoremTarget, conditional only on RiceBridge."),
    ("M0708-X-SOURCE", "terminal", "high", "Map the central fixed-point proof and semantic conventions to reviewed human and upstream-source passages.", "node-specific source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0708-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, transitive declarations, axioms, TCB, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"M0708-S-STATEMENT", "M0708-S-BOUNDARY", "M0708-T-ASSEMBLE"}
source_na = {"M0708-S-STATEMENT", "M0708-S-BOUNDARY", "M0708-S-FOUNDATION", "M0708-N-WITNESSES", "M0708-T-CONTRADICTION", "M0708-T-ASSEMBLE", "M0708-X-PROVENANCE"}
machine_special = {"M0708-X-SOURCE": "not_applicable", "M0708-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = ("lean-source:v1:sha256:" + statement_hash) if oid in {"M0708-ROOT", "M0708-S-STATEMENT"} else ("planned:v1:sha256:" + canonical_hash([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    body = "local:Stage1_Instances/THM-M-0708/ObligationTree.lean#root_of_riceBridge" if oid == "M0708-T-ASSEMBLE" else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0708-" + oid.removeprefix("M0708-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0708-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "source-statement-crosswalk/pinpoint-node-review-pending",
        "provenance_id": "local-conditional-composition" if body else ("anchor-audit:MATHLIB-RICE-8A178386" if oid == "M0708-L-RICE-BRIDGE" else "none"),
        "foundation_profile": "lean4-mathlib-classical/propext-choice-quotient/transitive-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no external computation or oracle may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {
            "premises": "Only exact incoming proof_requires conclusions and the stated formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed parent or a non-proof support edge may consume this output.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0708/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise and no root proof closure is supplied.",
        "task_ids": [ITEM, "S56-M-0708-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0708/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0708 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = canonical_hash([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated functional statement and completed bounded anchor audit; fixed-point Rice architecture expanded before proof-node adoption.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0708-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0708-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; the audited Rice candidate is not adopted, and proof, release, audit completion, and theorem completion remain open.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0708-ROOT": ["M0708-T-ASSEMBLE"],
    "M0708-T-ASSEMBLE": ["M0708-N-WITNESSES", "M0708-L-RICE-BRIDGE", "M0708-T-CONTRADICTION"],
    "M0708-L-RICE-BRIDGE": ["M0708-L-FIXED-POINT", "M0708-C-COND", "M0708-L-SEMANTIC-TRANSFER"],
    "M0708-L-SEMANTIC-TRANSFER": ["M0708-L-FIXED-POINT", "M0708-C-COND"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [
        edge("REF-ROOT-STATEMENT", "M0708-ROOT", "logical_decomposition", "M0708-S-STATEMENT"),
        edge("REF-ROOT-BOUNDARY", "M0708-ROOT", "logical_decomposition", "M0708-S-BOUNDARY"),
        edge("REF-ROOT-FOUNDATION", "M0708-ROOT", "logical_decomposition", "M0708-S-FOUNDATION"),
    ],
    "provenance": [
        edge("SRC-RICE", "M0708-L-RICE-BRIDGE", "source_map", "M0708-X-SOURCE"),
        edge("SRC-FIXED", "M0708-L-FIXED-POINT", "source_map", "M0708-X-SOURCE"),
        edge("PROV-ROOT", "M0708-X-PROVENANCE", "provenance_of", "M0708-ROOT"),
    ],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M0708-ROOT", "trusts", "M0708-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0708-ROOT", "trusts", "M0708-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", "M0708-S-STATEMENT", "documents", "M0708-ROOT"), edge("DOC-BRIDGE", "M0708-X-SOURCE", "documents", "M0708-L-RICE-BRIDGE")],
    "workflow": [edge("FLOW-ASSEMBLE-BRIDGE", "M0708-T-ASSEMBLE", "workflow_depends_on", "M0708-L-RICE-BRIDGE"), edge("FLOW-BRIDGE-PROVENANCE", "M0708-L-RICE-BRIDGE", "workflow_depends_on", "M0708-X-PROVENANCE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0708-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0708-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3",
        "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M0708-L-RICE-BRIDGE"],
        "composition_certificates": ["Stage1Instances.THM_M_0708.root_of_riceBridge"],
        "reason": "Final composition is conditional; the audited ComputablePred.rice candidate has not been adopted by the proof phase.",
    },
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({
        "recipe_id": "VAL-" + oid, "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-0708/check_obligation_tree.py"],
        "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0708 obligation tree"}],
        "covered_obligation_ids": [oid], "covered_declarations": [],
    })

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
