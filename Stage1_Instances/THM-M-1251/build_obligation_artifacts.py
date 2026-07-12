#!/usr/bin/env python3
"""Generate the frozen THM-M-1251 obligation registry and graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1251-OBLIGATION_TREE"
THEOREM = "THM-M-1251"
PREFIX = "M1251"

rows = [
    ("ROOT", "root", True, "required", "required", "required", "critical", None, None),
    ("S-DEFINITIONS", "definition", True, "required", "not_applicable", "required", "high", None, None),
    ("S-DOMAIN", "definition", True, "required", "required", "required", "high", None, None),
    ("S-BOUNDARY", "terminal", True, "required", "not_applicable", "required", "normal", None, None),
    ("S-TRANSPORT", "transport", True, "required", "required", "required", "high", None, None),
    ("S-FOUNDATION", "certificate", True, "required", "not_applicable", "required", "critical", None, None),
    ("N-UNFOLD", "reduction", True, "required", "required", "required", "critical", None,
     "mathlib:Mathlib.Analysis.Distribution.TemperedDistribution#TemperedDistribution"),
    ("T-ASSEMBLE", "transport", True, "required", "required", "required", "high", None,
     "local:Stage1_Instances/THM-M-1251/ObligationTree.lean#root_of_importedDefinitionExpansion"),
    ("X-ANCHOR", "bridge", True, "informational", "required", "required", "critical",
     "formal_anchor_provenance_overlay_no_duplicate_proof_credit", None),
    ("X-SOURCE", "terminal", True, "not_applicable", "required", "required", "high",
     "human_source_boundary_only", None),
    ("X-PROVENANCE", "certificate", True, "informational", "not_applicable", "required", "critical",
     "release_provenance_overlay_no_proof_credit", None),
]

root_fp = "lean-expression-sha256:597f3e4b3a8dd3da2a6eb5e14d5451f854d866cfaa214245b3dfc65c078a8ab9"
def planned(s):
    return "planned:v1:sha256:" + hashlib.sha256(s.encode()).hexdigest()

obligations = []
for suffix, kind, relevant, machine, human, readable, risk, reason, body in rows:
    oid = f"{PREFIX}-{suffix}"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": root_fp if suffix in {"ROOT", "N-UNFOLD", "T-ASSEMBLE"} else planned(oid),
        "kind": kind,
        "root_relevant": relevant,
        "machine_eligibility": machine,
        "human_source_eligibility": human,
        "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": reason,
        "terminal_proof_body_id": body,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
          "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact pointwise-dual statement and bounded anchor inventory; eligibility follows the definitional-expansion architecture and is independent of closure availability.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "layer_applicability": {
        "statement_foundation": "required: definitions, domain, boundary, transport, and foundation nodes are explicit",
        "normalization": "required only as definitional unfolding; no representative, symmetry, or local/global normalization occurs",
        "branch": "not_applicable: abbreviation unfolding has no mathematical case split",
        "construction": "not_applicable: the equality constructs no object",
        "core_lemma": "not_applicable: no mathematical lemma is invoked beyond the imported definition body",
        "external_computational": "required: pinned mathlib definition and provenance/trust boundaries are explicit",
        "terminal": "required: checked exact child-to-root composition is explicit"
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {
        "closed_obligations": [f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-DOMAIN", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-N-UNFOLD", f"{PREFIX}-T-ASSEMBLE"],
        "root_machine_debt": "M0-W",
        "acceptance_boundary": "Anchor classification observed after the denominator freeze; proof and release acceptance remain downstream."
    },
    "status_boundary": "Frozen scope and typed architecture only; no proof-phase, H0, R0, audit-completion, or theorem-completion acceptance."
}

descriptions = {
    "ROOT": ("Exact complex pointwise-dual target over finite-dimensional real normed spaces.", "The canonical proposition.", "M0-W", 8),
    "S-DEFINITIONS": ("Fix mathlib's TemperedDistribution, SchwartzMap, and pointwise continuous-dual meanings.", "Exact notation interface.", "M0-L", 8),
    "S-DOMAIN": ("Fix universes, real base-space structure, finite dimensionality, and complex codomain.", "Exact quantified context.", "M0-L", 8),
    "S-BOUNDARY": ("Preserve the zero-dimensional base case without extra nontriviality assumptions.", "Checked degenerate-case coverage.", "M0-L", 8),
    "S-TRANSPORT": ("Relate the named pointwise-dual abbreviation to the directly expanded target by checked equivalence.", "Exact transport direction.", "M0-L", 8),
    "S-FOUNDATION": ("Account for extensional equality, classical choice, quotient soundness, kernel, and no-oracle policy.", "Trust-boundary input for release.", "M4", 20),
    "N-UNFOLD": ("Unfold the pinned mathlib TemperedDistribution abbreviation at codomain Complex.", "The exact canonical equality for every quantified base.", "M0-W", 6),
    "T-ASSEMBLE": ("Consume the exact imported-definition expansion and return the exact canonical root.", "The canonical proposition with no added premise after child discharge.", "M0-L", 6),
    "X-ANCHOR": ("Map the canonical reduction to the pinned mathlib declaration and audited wrapper.", "Non-duplicating formal-anchor record.", "M0-W", 10),
    "X-SOURCE": ("Map each semantic claim to an exact primary-source theorem/page/assumption/errata record.", "Accepted human-source boundary.", "M4", 30),
    "X-PROVENANCE": ("Audit terminal body, imports, transitive declarations, axioms, license, and replay identity.", "Release provenance certificate.", "M4", 30),
}

nodes = []
for r in obligations:
    suffix = r["obligation_id"].removeprefix(PREFIX + "-")
    statement, output, machine, budget = descriptions[suffix]
    nodes.append({
        "node_id": f"THM-M-1251-{suffix}", "obligation_id": r["obligation_id"], "kind": r["kind"],
        "human_statement": statement,
        "formal_target": ({
            "ROOT": "Stage1Instances.THM_M_1251.TemperedDistributionsAreSchwartzDual",
            "N-UNFOLD": "TemperedDistribution E Complex = PointwiseConvergenceCLM (RingHom.id Complex) (SchwartzMap E Complex) Complex",
            "T-ASSEMBLE": "Stage1Instances.THM_M_1251.ObligationTree.root_of_importedDefinitionExpansion"
        }).get(suffix, "structured audit target recorded by this node"),
        "output": output, "human_debt": "H2", "machine_debt": machine, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if r["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "S56-M-1251-C01" if suffix in {"N-UNFOLD", "X-ANCHOR"} else "none",
        "foundation_profile": "lean4-mathlib-standard/acceptance-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation is permitted",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only typed proof children and the frozen quantified context.", "inference": statement, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1251/obligation-tree.md#{r['obligation_id'].lower()}",
        "validation_spec_id": f"VAL-{r['obligation_id']}",
        "status_boundary": "Architecture or conditional composition only; downstream proof/release acceptance is not supplied.",
        "task_ids": [ITEM, "S56-M-1251-PROOF"], "owned_sources": [], "owner": "THM-M-1251 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if machine in {"M0-L", "M0-W"} else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if machine in {"M0-L", "M0-W"} else "open"}
    })

graphs = {name: {"edges": []} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
def edge(graph, eid, typ, src, dst, reciprocal=None):
    e = {"edge_id": eid, "type": typ, "from": f"{PREFIX}-{src}", "to": f"{PREFIX}-{dst}"}
    if reciprocal: e["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(e)

edge("proof", "P01", "proof_requires", "ROOT", "T-ASSEMBLE", "P02")
edge("proof", "P02", "composes", "T-ASSEMBLE", "ROOT", "P01")
edge("proof", "P03", "proof_requires", "T-ASSEMBLE", "N-UNFOLD", "P04")
edge("proof", "P04", "composes", "N-UNFOLD", "T-ASSEMBLE", "P03")
for i, child in enumerate(("S-DEFINITIONS", "S-DOMAIN", "S-BOUNDARY", "S-TRANSPORT"), 1):
    edge("refinement", f"R{i:02}", "logical_decomposition", "ROOT", child)
edge("provenance", "PV01", "provenance_of", "X-ANCHOR", "N-UNFOLD")
edge("provenance", "PV02", "provenance_of", "X-PROVENANCE", "T-ASSEMBLE")
edge("evidence", "E01", "provenance_of", "X-PROVENANCE", "ROOT")
edge("trust", "TR01", "trusts", "ROOT", "S-FOUNDATION")
for i, child in enumerate(ids[1:], 1): edge("documentation", f"D{i:02}", "documents", "ROOT", child.removeprefix(PREFIX + "-"))
for i, child in enumerate(("S-DEFINITIONS", "S-DOMAIN", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION", "N-UNFOLD", "X-ANCHOR", "X-SOURCE", "X-PROVENANCE", "T-ASSEMBLE"), 1):
    edge("workflow", f"W{i:02}", "workflow_depends_on", "ROOT", child)
for graph in graphs.values():
    graph["out"] = {oid: [e["edge_id"] for e in graph["edges"] if e["from"] == oid] for oid in ids}
    graph["in"] = {oid: [e["edge_id"] for e in graph["edges"] if e["to"] == oid] for oid in ids}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1251-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "minimal_open_root_cut": [],
    "closure_boundary": {"root_anchor_classification": "M0-W", "root_proof_phase_accepted": False, "root_closed": False, "audit_complete": False, "theorem_complete": False,
                         "reason": "Exact definitional anchor exists, but proof, human-source, readability, provenance, hermetic, and master-acceptance gates are downstream."}
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
         "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1251/check_obligation_tree.py"], "env": {}, "timeout_seconds": 30, "network_policy": "denied", "covered_ids": [oid], "expected_exit": 0} for oid in ids]}

for name, data in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
print(denominator)
