#!/usr/bin/env python3
"""Build THM-M-0525's frozen obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0525-OBLIGATION_TREE"
THEOREM = "THM-M-0525"

SPECS = [
    ("M0525-ROOT", "root", "The exact Nonempty CanonicalBasedLoopGroup target for every based topological space.", "THM_M_0525.Statement", "The canonical proposition.", "critical", "H1", "M2"),
    ("M0525-S-SCOPE", "definition", "Fix the universe, topological-space instance, basepoint, loop quotient carrier, and forward concatenation convention.", "THM_M_0525.{BasedLoopClass,CanonicalBasedLoopGroup,Statement}", "The exact elaborated statement interface.", "high", "H1", "M0-L"),
    ("M0525-S-FOUNDATION", "certificate", "Audit quotient soundness, classical choice, propositional extensionality, the Lean kernel, and the no-oracle policy.", "planned transitive axiom and TCB report", "An accepted trust boundary.", "critical", "H1", "M4"),
    ("M0525-C-QUOTIENT", "construction", "Establish that concatenation, constant paths, and reversal descend to endpoint-fixed homotopy classes.", "Path.Homotopic.Quotient.{trans,refl,symm}", "Three well-defined operations on the frozen carrier.", "critical", "H1", "M0-W"),
    ("M0525-L-ASSOC", "core_lemma", "Prove associativity of forward concatenation on quotient classes.", "Path.Homotopic.Quotient.trans_assoc", "(a.trans b).trans c = a.trans (b.trans c).", "critical", "H1", "M0-W"),
    ("M0525-L-ONE-LEFT", "core_lemma", "Prove that the constant loop is a left identity for forward concatenation.", "Path.Homotopic.Quotient.refl_trans", "refl.trans a = a.", "high", "H1", "M0-W"),
    ("M0525-L-INV-LEFT", "core_lemma", "Prove that reversal is a left inverse for forward concatenation.", "Path.Homotopic.Quotient.symm_trans", "a.symm.trans a = refl.", "high", "H1", "M0-W"),
    ("M0525-T-GROUP", "terminal", "Use the three minimal left laws to construct Group and package the exact operation equations.", "THM_M_0525.statement_of_left_laws", "THM_M_0525.Statement, conditional on the three named laws.", "critical", "H1", "M3"),
    ("M0525-X-SOURCE", "terminal", "Map the construction and laws to primary human sources with exact assumptions and pinpoints.", "human-source boundary", "Reviewed source fidelity only.", "high", "H1", "M4"),
    ("M0525-X-PROVENANCE", "certificate", "Track wrapper, terminal body, dependency, axiom, and placeholder provenance for every machine node.", "formal provenance overlay", "A release provenance classification without proof credit.", "critical", "H1", "M4"),
]

ids = [row[0] for row in SPECS]
machine = ids[:-2]
human = [oid for oid in ids if oid not in {"M0525-S-SCOPE", "M0525-S-FOUNDATION", "M0525-C-QUOTIENT", "M0525-X-PROVENANCE"}]

def fp(oid, formal):
    if oid == "M0525-ROOT":
        return "lean-source-bound-sha256:" + hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    return "planned:v1:sha256:" + hashlib.sha256(f"{THEOREM}/v1/{oid}/{formal}".encode()).hexdigest()

obligations = []
nodes = []
for oid, kind, statement, formal, output, risk, hdebt, mdebt in SPECS:
    is_machine = oid in machine
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp(oid, formal), "kind": kind,
        "root_relevant": True, "machine_eligibility": "required" if is_machine else "informational",
        "human_source_eligibility": "required" if oid in human else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None if is_machine else "overlay_no_machine_proof_credit",
        "terminal_proof_body_id": "mathlib:" + formal if mdebt == "M0-W" else ("local:ObligationTree.lean#statement_of_left_laws" if oid == "M0525-T-GROUP" else None),
    })
    nodes.append({
        "node_id": f"{THEOREM}-{oid[6:]}", "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": output,
        "human_debt": hdebt, "machine_debt": mdebt, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source_statement_crosswalk.md" if oid in human else "not-applicable",
        "provenance_id": "anchor-audit.json" if mdebt == "M0-W" else "none",
        "foundation_profile": "lean4-mathlib-classical/accept-propext-choice-quot-sound; review-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-review-pending",
        "computation_record": "none; no solver, oracle, or experiment may close this node",
        "step_budget": 4,
        "semantic_step_ledger": {
            "premises": "Only the typed proof children and frozen topological context.",
            "inference": statement, "output": output,
            "outgoing_use": "Only the registered parent or non-proof support edge may consume this output."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0525/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Provisional architecture or component classification only; no accepted root closure or release evidence.",
        "task_ids": [ITEM, "S56-M-0525-PROOF"], "owned_sources": [],
        "owner": "THM-M-0525 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "obligation-registry.json", "anchor-audit.json", "toolchain"], "revocation_state": "open"}
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
denoms = {"inventory": ids, "required_machine": machine, "required_human_source": human, "required_readable": ids, "informational_overlays": ids[-2:]}
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; eligibility selected from the minimal left-axiom group construction before root closure was observed.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": ids[0], "denominator_sha256": digest, "frozen_denominators": denoms,
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new registry version and append-only delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"component_machine_debt": "M0-W", "root_machine_debt": "M2", "root_closed": False},
    "status_boundary": "This freezes scope and graph semantics only. Kernel-available components are not an accepted proof-phase root receipt."
}

def graph(name, triples):
    edges, out, incoming = [], {}, {}
    for i, (src, dst, typ) in enumerate(triples, 1):
        eid = f"{name.upper()}-{i:03d}"
        edge = {"edge_id": eid, "from": src, "to": dst, "type": typ}
        edges.append(edge); out.setdefault(src, []).append(eid); incoming.setdefault(dst, []).append(eid)
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = []
for child in ["M0525-S-SCOPE", "M0525-C-QUOTIENT", "M0525-L-ASSOC", "M0525-L-ONE-LEFT", "M0525-L-INV-LEFT"]:
    proof_pairs += [("M0525-T-GROUP", child, "proof_requires"), (child, "M0525-T-GROUP", "composes")]
proof_pairs += [("M0525-ROOT", "M0525-T-GROUP", "proof_requires"), ("M0525-T-GROUP", "M0525-ROOT", "composes")]
graphs = {
    "proof": graph("proof", proof_pairs),
    "refinement": graph("refinement", [("M0525-C-QUOTIENT", x, "logical_decomposition") for x in ["M0525-L-ASSOC", "M0525-L-ONE-LEFT", "M0525-L-INV-LEFT"]]),
    "provenance": graph("provenance", [("M0525-X-PROVENANCE", x, "provenance_of") for x in machine]),
    "evidence": graph("evidence", []),
    "trust": graph("trust", [(x, "M0525-S-FOUNDATION", "trusts") for x in machine if x != "M0525-S-FOUNDATION"]),
    "documentation": graph("documentation", [(x, "M0525-X-SOURCE", "documents") for x in human]),
    "workflow": graph("workflow", [("M0525-ROOT", "M0525-X-PROVENANCE", "workflow_depends_on"), ("M0525-X-PROVENANCE", "M0525-X-SOURCE", "workflow_depends_on")]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": f"{THEOREM}-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M0525-ROOT", "edge_direction": "proof_requires parent-to-child; composes child-to-parent; other graphs state their own typed relation",
    "nodes": nodes, "graphs": graphs,
    "composition_certificates": [{"certificate_id": "COMP-M0525-ROOT-V1", "parent": "M0525-ROOT", "required_children": ["M0525-T-GROUP"], "checked_declaration": "THM_M_0525.statement_of_left_laws", "status": "conditional-interface-kernel-checked; mathematical children not accepted"}],
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M2", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0525-L-ASSOC", "M0525-L-ONE-LEFT", "M0525-L-INV-LEFT", "M0525-S-FOUNDATION", "M0525-X-SOURCE", "M0525-X-PROVENANCE"]}
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(ids)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(digest)
