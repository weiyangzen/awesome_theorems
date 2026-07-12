#!/usr/bin/env python3
"""Build the frozen THM-M-0156 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0156-OBLIGATION_TREE"
THEOREM = "THM-M-0156"
PREFIX = "M0156"

specs = [
    ("ROOT", "root", "The exact frozen rectangular divergence theorem target.", "critical", "required", "required"),
    ("S-STATEMENT", "definition", "Preserve every binder and conclusion of DivergenceTheoremTarget.", "critical", "required", "required"),
    ("S-HYPOTHESES", "definition", "Preserve a <= b, closed-box continuity, interior Frechet derivative, and divergence integrability.", "high", "required", "required"),
    ("S-DIVERGENCE", "definition", "Identify divergence with the coordinate trace of f'.", "high", "required", "required"),
    ("S-FLUX", "definition", "Identify outward flux with the signed upper-minus-lower face integrals.", "high", "required", "required"),
    ("S-DEGENERATE", "boundary", "Retain n = 0 and boxes with zero-width coordinates.", "high", "required", "required"),
    ("S-FOUNDATION", "certificate", "Audit the classical measure-theory foundation, imports, axioms, and TCB.", "critical", "not_applicable", "required"),
    ("B-CANDIDATE", "bridge", "Supply the pinned off-countable mathlib divergence theorem package at its exact type.", "critical", "required", "required"),
    ("L-EMPTY", "terminal", "Establish that the empty exceptional set is countable and excludes no interior point.", "normal", "not_applicable", "required"),
    ("T-ADAPTER", "transport", "Specialize the off-countable package to the empty exceptional set.", "critical", "required", "required"),
    ("T-ASSEMBLE", "terminal", "Compose the exact adapter output into the canonical root.", "critical", "required", "required"),
    ("X-SOURCE", "source_boundary", "Pinpoint and review a primary human source for every mathematical transition.", "high", "required", "required"),
    ("X-PROVENANCE", "certificate", "Resolve wrapper, terminal body, immutable origin, and transitive declaration provenance.", "critical", "not_applicable", "required"),
    ("X-TRUST", "certificate", "Resolve terminal axioms, dependency trust closure, and TCB acceptance.", "critical", "not_applicable", "required"),
    ("X-DOCUMENTATION", "documentation", "Provide node-specific readable reconstructions and independent review.", "high", "not_applicable", "required"),
    ("X-WORKFLOW", "workflow", "Run proof, validation, release, and independent-verification gates in dependency order.", "critical", "not_applicable", "required"),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

rows = []
for suffix, kind, claim, risk, human, readable in specs:
    oid = f"{PREFIX}-{suffix}"
    if suffix in ("ROOT", "S-STATEMENT"):
        fingerprint = f"lean-source:v1:sha256:{statement_hash}"
    else:
        digest = hashlib.sha256(claim.encode()).hexdigest()
        fingerprint = f"planned:v1:sha256:{digest}"
    machine = "informational" if suffix.startswith("X-") else "required"
    exclusion = None
    if suffix == "X-SOURCE":
        machine, exclusion = "not_applicable", "human_source_boundary_only"
    elif suffix.startswith("X-"):
        exclusion = "support_overlay_no_mathematical_proof_credit"
    terminal = None
    if suffix in ("L-EMPTY", "T-ADAPTER", "T-ASSEMBLE"):
        terminal = f"local:Stage1_Instances/THM-M-0156/ObligationTree.lean#{'root_of_offCountablePackage' if suffix != 'L-EMPTY' else 'empty_exception_is_countable'}"
    rows.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human,
        "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": terminal,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact box-scoped statement and immutable candidate audit; the empty-exception adapter route and all support boundaries were enumerated before this phase credited closure.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": f"{PREFIX}-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in rows if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows,
    "append_only_delta": [],
    "status_observed_after_freeze": {
        "closed_obligations": [f"{PREFIX}-S-STATEMENT", f"{PREFIX}-S-HYPOTHESES", f"{PREFIX}-S-DIVERGENCE", f"{PREFIX}-S-FLUX", f"{PREFIX}-S-DEGENERATE", f"{PREFIX}-L-EMPTY", f"{PREFIX}-T-ADAPTER", f"{PREFIX}-T-ASSEMBLE"],
        "candidate_state": "M0-W-candidate_pending_proof_and_validation_acceptance",
        "root_machine_debt": "M3",
    },
    "status_boundary": "Frozen architecture and conditional composition only; the candidate is not accepted here as the proof node, and root/audit/theorem completion remain false.",
}

claims = {f"{PREFIX}-{suffix}": claim for suffix, _, claim, _, _, _ in specs}
kinds = {f"{PREFIX}-{suffix}": kind for suffix, kind, _, _, _, _ in specs}
formal = {
    f"{PREFIX}-ROOT": "Stage1Instances.THM_M_0156.DivergenceTheoremTarget",
    f"{PREFIX}-S-STATEMENT": "Stage1Instances.THM_M_0156.DivergenceTheoremTarget",
    f"{PREFIX}-B-CANDIDATE": "MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable",
    f"{PREFIX}-L-EMPTY": "Stage1Instances.THM_M_0156.ObligationTree.empty_exception_is_countable",
    f"{PREFIX}-T-ADAPTER": "Stage1Instances.THM_M_0156.ObligationTree.root_of_offCountablePackage",
    f"{PREFIX}-T-ASSEMBLE": "Stage1Instances.THM_M_0156.ObligationTree.root_of_offCountablePackage",
}
closed = set(registry["status_observed_after_freeze"]["closed_obligations"])
nodes = []
for row in rows:
    oid = row["obligation_id"]
    suffix = oid[len(PREFIX) + 1:]
    node = {
        "node_id": f"{THEOREM}-{suffix}",
        "obligation_id": oid,
        "kind": kinds[oid],
        "human_statement": claims[oid],
        "formal_target": formal.get(oid, "planned structured acceptance record"),
        "output": claims[oid],
        "human_debt": "H1",
        "machine_debt": "M0-L" if oid in closed else ("M0-W-candidate" if suffix == "B-CANDIDATE" else "M4"),
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "M0156-C01" if suffix == "B-CANDIDATE" else "pending",
        "foundation_profile": "lean4-mathlib-classical/audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no external computation or oracle receives proof credit",
        "step_budget": 100 if suffix in ("B-CANDIDATE", "X-PROVENANCE", "X-TRUST") else 40,
        "semantic_step_ledger": {
            "premises": "Only the exact canonical context and declared proof_requires children.",
            "inference": claims[oid],
            "output": claims[oid],
            "outgoing_use": "Only reciprocal composes edges carry mathematical proof; support graphs carry no proof credit.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0156/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or checked conditional interface only; no root acceptance or theorem completion.",
        "task_ids": [ITEM, "S56-M-0156-PROOF"],
        "owned_sources": [],
        "owner": "THM-M-0156 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if oid in closed else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"],
            "revocation_state": "provisional" if oid in closed else "open",
        },
    }
    nodes.append(node)

graphs = {name: {"edges": [], "out": {oid: [] for oid in ids}, "in": {oid: [] for oid in ids}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}

def edge(graph, eid, typ, source, target, reciprocal=None):
    value = {"edge_id": eid, "type": typ, "from": source, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(value)
    graphs[graph]["out"][source].append(eid)
    graphs[graph]["in"][target].append(eid)

proof_pairs = [
    ("ROOT-ASSEMBLE", "ROOT", "T-ASSEMBLE"),
    ("ASSEMBLE-ADAPTER", "T-ASSEMBLE", "T-ADAPTER"),
    ("ADAPTER-CANDIDATE", "T-ADAPTER", "B-CANDIDATE"),
    ("ADAPTER-EMPTY", "T-ADAPTER", "L-EMPTY"),
]
for label, parent, child in proof_pairs:
    req, comp = f"P-{label}-REQ", f"P-{label}-COMP"
    edge("proof", req, "proof_requires", f"{PREFIX}-{parent}", f"{PREFIX}-{child}", comp)
    edge("proof", comp, "composes", f"{PREFIX}-{child}", f"{PREFIX}-{parent}", req)

for i, suffix in enumerate(("S-STATEMENT", "S-HYPOTHESES", "S-DIVERGENCE", "S-FLUX", "S-DEGENERATE"), 1):
    edge("refinement", f"R-{i:02d}", "logical_decomposition", f"{PREFIX}-ROOT", f"{PREFIX}-{suffix}")
edge("provenance", "PR-01", "provenance_of", f"{PREFIX}-B-CANDIDATE", f"{PREFIX}-X-PROVENANCE")
edge("provenance", "PR-02", "source_map", f"{PREFIX}-B-CANDIDATE", f"{PREFIX}-X-SOURCE")
edge("evidence", "EV-01", "documents", f"{PREFIX}-T-ADAPTER", f"{PREFIX}-X-WORKFLOW")
edge("trust", "TR-01", "trusts", f"{PREFIX}-B-CANDIDATE", f"{PREFIX}-X-TRUST")
edge("trust", "TR-02", "trusts", f"{PREFIX}-ROOT", f"{PREFIX}-S-FOUNDATION")
edge("documentation", "D-01", "documents", f"{PREFIX}-ROOT", f"{PREFIX}-X-DOCUMENTATION")
for i, suffix in enumerate(("B-CANDIDATE", "X-PROVENANCE", "X-TRUST", "X-DOCUMENTATION"), 1):
    edge("workflow", f"W-{i:02d}", "workflow_depends_on", f"{PREFIX}-X-WORKFLOW", f"{PREFIX}-{suffix}")

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": f"{THEOREM}-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": [f"{PREFIX}-B-CANDIDATE"],
        "reason": "The exact mathlib candidate is inventoried but proof-node acceptance, transitive provenance/trust, source/readability, validation, and release gates are later phases.",
    },
}

recipes = [{
    "recipe_id": f"VAL-{oid}",
    "cwd": ".",
    "argv": ["python3", "Stage1_Instances/THM-M-0156/check_obligation_tree.py"],
    "env_allowlist": {},
    "timeout_seconds": 30,
    "network_policy": "denied",
    "expected_exit": 0,
    "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0156 obligation tree"}],
    "covered_obligation_ids": [oid],
    "covered_declarations": [],
} for oid in ids]

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
(HERE / "validation-specs.json").write_text(json.dumps({"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}, indent=2) + "\n")
print(f"built {len(rows)} obligations; denominator sha256 {denominator}")
