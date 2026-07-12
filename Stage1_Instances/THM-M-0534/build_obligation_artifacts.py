#!/usr/bin/env python3
"""Build the frozen THM-M-0534 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0534-OBLIGATION_TREE"
THEOREM = "THM-M-0534"

def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()

rows = [
    ("M0534-ROOT", "root", "critical", "The exact universally indexed long-homology-sequence target frozen in Statement.lean.", "Stage1Instances.THM_M_0534.LongExactHomologySequenceTarget", "All three repeating exactness positions."),
    ("M0534-S-DEFINITIONS", "definition", "high", "Freeze homology maps, short exact complexes, shape relations, and local ShortComplex exactness.", "Stage1Instances.THM_M_0534.LongExactHomologySequenceTarget", "The exact formal interface."),
    ("M0534-S-BOUNDARY", "branch", "high", "Preserve every degree, including endpoints without an outgoing shape relation.", "planned endpoint coverage audit", "Same-degree exactness at all indices."),
    ("M0534-S-TRANSPORT", "transport", "normal", "Transport between paired and separately grouped exactness families.", "Stage1Instances.THM_M_0534.longExactHomologySequenceTarget_iff_grouped", "A checked bidirectional regrouping."),
    ("M0534-S-FOUNDATION", "certificate", "critical", "Fix classical choice, quotient, extensionality, TCB, and no-oracle policy.", "planned transitive axiom and trust report", "An accepted foundation boundary."),
    ("M0534-C-DELTA", "construction", "critical", "Construct the connecting morphism for every c.Rel i j and establish its two zero compositions.", "ShortComplex.ShortExact.{delta,comp_delta,delta_comp}", "Well-typed connecting maps in both adjacent windows."),
    ("M0534-L-SAME", "bridge", "critical", "Establish exactness at the same-degree homologyMap f, homologyMap g position for every index.", "ShortComplex.ShortExact.homology_exact2", "SameDegreeFamily."),
    ("M0534-L-INTO", "bridge", "critical", "Establish exactness at homologyMap g followed by delta for every related pair.", "ShortComplex.ShortExact.homology_exact3", "IntoDeltaFamily."),
    ("M0534-L-OUT", "bridge", "critical", "Establish exactness at delta followed by homologyMap f for every related pair.", "ShortComplex.ShortExact.homology_exact1", "OutOfDeltaFamily."),
    ("M0534-X-SNAKE", "bridge", "critical", "Audit the snakeInput package used by the three imported exactness theorems.", "HomologicalComplex.HomologySequence.snakeInput", "Non-endpoint exactness engine."),
    ("M0534-X-ENDPOINT", "bridge", "high", "Audit the endpoint opcycles right-exact package used when no next relation exists.", "HomologicalComplex.opcycles_right_exact", "Endpoint same-degree exactness engine."),
    ("M0534-T-ASSEMBLE", "terminal", "high", "Consume all three exactness families and produce the complete canonical target.", "Stage1Instances.THM_M_0534.ObligationTree.root_of_exactness_families", "The exact root conditional on three explicit premises."),
    ("M0534-X-SOURCE", "terminal", "high", "Map each material construction and exactness lemma to reviewed primary-source passages.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without proof credit."),
    ("M0534-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, axioms, TCB, placeholders, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without proof credit."),
]

checked = {"M0534-S-DEFINITIONS", "M0534-S-TRANSPORT", "M0534-T-ASSEMBLE"}
source_na = {"M0534-S-DEFINITIONS", "M0534-S-BOUNDARY", "M0534-S-TRANSPORT", "M0534-S-FOUNDATION", "M0534-X-PROVENANCE"}
machine_special = {"M0534-X-SOURCE": "not_applicable", "M0534-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations, nodes = [], []
for oid, kind, risk, claim, target, output in rows:
    fp = ("lean-expression-sha256:6846afc515ceb8a7479a074f21295620ef4f191bd0804e377b56ae37567b7677"
          if oid in {"M0534-ROOT", "M0534-S-DEFINITIONS"} else
          "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    body = ("local:Stage1_Instances/THM-M-0534/ObligationTree.lean#root_of_exactness_families"
            if oid == "M0534-T-ASSEMBLE" else None)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0534-" + oid.removeprefix("M0534-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M1" if oid in {"M0534-ROOT", "M0534-L-SAME", "M0534-L-INTO", "M0534-L-OUT"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if body else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires conclusions and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0534/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise or root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0534-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0534/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0534 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; three-position exactness architecture expanded before target-owned proof execution.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0534-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0534-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M1"},
    "status_boundary": "Scope and denominators only; no target-owned root proof, source acceptance, audit completion, or theorem completion.",
}

def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal: result["reciprocal_edge_id"] = reciprocal
    return result

requires = {
    "M0534-ROOT": ["M0534-T-ASSEMBLE"],
    "M0534-T-ASSEMBLE": ["M0534-L-SAME", "M0534-L-INTO", "M0534-L-OUT"],
    "M0534-L-SAME": ["M0534-X-SNAKE", "M0534-X-ENDPOINT"],
    "M0534-L-INTO": ["M0534-C-DELTA", "M0534-X-SNAKE"],
    "M0534-L-OUT": ["M0534-C-DELTA", "M0534-X-SNAKE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0534-ROOT", "logical_decomposition", "M0534-S-DEFINITIONS"), edge("REF-ROOT-BOUND", "M0534-ROOT", "logical_decomposition", "M0534-S-BOUNDARY"), edge("REF-ROOT-TRANS", "M0534-ROOT", "logical_decomposition", "M0534-S-TRANSPORT"), edge("REF-ROOT-FOUND", "M0534-ROOT", "logical_decomposition", "M0534-S-FOUNDATION")],
    "provenance": [edge("SRC-SNAKE", "M0534-X-SNAKE", "source_map", "M0534-X-SOURCE"), edge("SRC-ENDPOINT", "M0534-X-ENDPOINT", "source_map", "M0534-X-SOURCE"), edge("PROV-ROOT", "M0534-X-PROVENANCE", "provenance_of", "M0534-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0534-ROOT", "trusts", "M0534-S-FOUNDATION"), edge("TRUST-PROV", "M0534-ROOT", "trusts", "M0534-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", "M0534-S-DEFINITIONS", "documents", "M0534-ROOT"), edge("DOC-SOURCE", "M0534-X-SOURCE", "documents", "M0534-X-SNAKE")],
    "workflow": [edge("FLOW-ASSEMBLE-SAME", "M0534-T-ASSEMBLE", "workflow_depends_on", "M0534-L-SAME"), edge("FLOW-ASSEMBLE-INTO", "M0534-T-ASSEMBLE", "workflow_depends_on", "M0534-L-INTO"), edge("FLOW-ASSEMBLE-OUT", "M0534-T-ASSEMBLE", "workflow_depends_on", "M0534-L-OUT"), edge("FLOW-PROV-ASSEMBLE", "M0534-X-PROVENANCE", "workflow_depends_on", "M0534-T-ASSEMBLE")],
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
    "registry_id": "THM-M-0534-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0534-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M1", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0534-L-SAME", "M0534-L-INTO", "M0534-L-OUT"], "composition_certificates": ["Stage1Instances.THM_M_0534.ObligationTree.root_of_exactness_families"], "reason": "Final composition is conditional; the target-owned proof and accepted transitive trust/provenance closure remain downstream."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0534/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0534 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
