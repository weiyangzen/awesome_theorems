#!/usr/bin/env python3
"""Build the deterministic THM-M-1247 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1247-OBLIGATION_TREE"
THEOREM = "THM-M-1247"
ROOT_FP = "lean-expression-sha256:4697dbbaaf7fd636a371bb293a47359a9b079a3857fcb85d6f7cf5a608a5c90e"

raw = [
    ("M1247-ROOT", "root", "critical", "Exact canonical Rellich inequality for every n >= 5 and every smooth compactly supported real u avoiding zero."),
    ("M1247-S-LAPLACIAN", "definition", "high", "Identify the coordinate trace of the second Frechet derivative with the Laplacian used by the analytic argument."),
    ("M1247-S-DOMAIN", "definition", "high", "Carry smoothness, compact support, and support avoidance through every derivative and weighted integral."),
    ("M1247-S-BOUNDARY", "terminal", "high", "Establish the n >= 5 coefficient and all zero-function, near-origin, measurability, and integrability boundary facts."),
    ("M1247-S-FOUNDATION", "certificate", "critical", "Audit classical choice, quotient, extensionality, Bochner integral, and real-analysis trust dependencies."),
    ("M1247-N-WEIGHTS", "normalization", "critical", "Normalize powers of the Euclidean norm and the sharp coefficient without changing the extended-integral semantics."),
    ("M1247-L-IBP", "core_lemma", "critical", "Prove the weighted multidimensional integration-by-parts identities with vanishing boundary terms."),
    ("M1247-L-HARDY", "core_lemma", "critical", "Prove the required sharp weighted Hardy estimate for first derivatives in dimension n >= 5."),
    ("M1247-L-CORE", "core_lemma", "critical", "Combine the weighted identities and Cauchy-Schwarz/Hardy bounds into the sharp expanded Rellich estimate."),
    ("M1247-T-TRANSPORT", "transport", "high", "Transport the expanded coordinate estimate to the canonical RellichInequalityTarget."),
    ("M1247-X-SOURCE", "terminal", "high", "Pinpoint and crosswalk a complete human proof of every analytic identity and sharp constant."),
    ("M1247-X-PROVENANCE", "certificate", "critical", "Record terminal Lean proof bodies and ensure wrappers do not duplicate proof credit."),
    ("M1247-X-TRUST", "certificate", "critical", "Record exact imports, axioms, computation boundaries, and reproducible validation recipes."),
]

def fp(oid, statement):
    if oid == "M1247-ROOT":
        return ROOT_FP
    return "planned:v1:sha256:" + hashlib.sha256(statement.encode()).hexdigest()

obligations = []
for oid, kind, risk, statement in raw:
    overlay = oid in {"M1247-X-PROVENANCE", "M1247-X-TRUST"}
    source_only = oid == "M1247-X-SOURCE"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp(oid, statement), "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "informational" if overlay else ("not_applicable" if source_only else "required"),
        "human_source_eligibility": "required" if oid not in {"M1247-S-LAPLACIAN", "M1247-S-DOMAIN", "M1247-S-FOUNDATION", "M1247-X-PROVENANCE", "M1247-X-TRUST"} else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if source_only else ("release_overlay_no_proof_credit" if overlay else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1247/ObligationTree.lean#root_of_coreRellichEstimate" if oid == "M1247-T-TRANSPORT" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denom = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [x[0] for x in raw]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus bounded immutable anchor audit; classical weighted integration-by-parts/Hardy architecture; eligibility assigned without regard to available closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": ids[0], "denominator_sha256": denom,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1247-X-PROVENANCE", "M1247-X-TRUST"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

node_kind = {r["obligation_id"]: r["kind"] for r in obligations}
statements = {oid: text for oid, _, _, text in raw}
formal = {
    "M1247-ROOT": "Stage1Instances.THM_M_1247.RellichInequalityTarget",
    "M1247-L-CORE": "Stage1Instances.THM_M_1247.CoreRellichEstimate",
    "M1247-T-TRANSPORT": "CoreRellichEstimate -> RellichInequalityTarget",
}
nodes = []
for oid in ids:
    nodes.append({
        "node_id": "THM-M-1247-" + oid.removeprefix("M1247-"), "obligation_id": oid,
        "kind": node_kind[oid], "human_statement": statements[oid],
        "formal_target": formal.get(oid, "planned:v1:" + oid), "output": statements[oid],
        "human_debt": "H1" if oid in {"M1247-X-SOURCE", "M1247-ROOT"} else "H3",
        "machine_debt": "M3" if oid in {"M1247-ROOT", "M1247-T-TRANSPORT"} else "M4",
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "THM-M-1247-SOURCE-CROSSWALK" if registry["obligations"][ids.index(oid)]["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "THM-M-1247-PROV-TRANSPORT" if oid == "M1247-T-TRANSPORT" else "none",
        "foundation_profile": "lean4-mathlib-pinned-v1", "tcb_profile": "lean-kernel-no-oracle-v1",
        "computation_record": "none", "step_budget": 12 if oid == "M1247-L-CORE" else 8,
        "semantic_step_ledger": {"premises": [], "inference": "planned exact analytic derivation" if oid != "M1247-T-TRANSPORT" else "checked iff transport", "output": statements[oid], "outgoing_use": "typed graph edges"},
        "public_readable_target": "Stage1_Instances/THM-M-1247/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "M1247-V-" + oid.removeprefix("M1247-"),
        "status_boundary": "Architecture only; no proof closure or theorem completion is claimed.",
        "task_ids": [ITEM, "S56-M-1247-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1247/obligation-registry.json"],
        "owner": "stage1-proof-worker", "reviewer": "independent-master-required",
        "validity": {"validated_at": "2026-07-12", "review_due": "on_any_input_change", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json"], "revocation_state": "active"},
    })

graphs = {name: {"edges": [], "out": {i: [] for i in ids}, "in": {i: [] for i in ids}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
def edge(graph, eid, typ, src, dst, reciprocal=None):
    e = {"edge_id": eid, "type": typ, "from": src, "to": dst}
    if reciprocal: e["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(e); graphs[graph]["out"][src].append(eid); graphs[graph]["in"][dst].append(eid)
def pair(parent, child, tag):
    edge("proof", "P-"+tag, "proof_requires", parent, child, "C-"+tag)
    edge("proof", "C-"+tag, "composes", child, parent, "P-"+tag)
pair("M1247-ROOT", "M1247-T-TRANSPORT", "ROOT-TRANSPORT")
pair("M1247-T-TRANSPORT", "M1247-L-CORE", "TRANSPORT-CORE")
for child, tag in (("M1247-L-IBP","CORE-IBP"), ("M1247-L-HARDY","CORE-HARDY"), ("M1247-N-WEIGHTS","CORE-WEIGHTS"), ("M1247-S-BOUNDARY","CORE-BOUNDARY"), ("M1247-S-DOMAIN","CORE-DOMAIN"), ("M1247-S-LAPLACIAN","CORE-LAPLACIAN")):
    pair("M1247-L-CORE", child, tag)
for child in ("M1247-S-FOUNDATION", "M1247-X-SOURCE", "M1247-X-PROVENANCE", "M1247-X-TRUST"):
    typ = "trusts" if child in {"M1247-S-FOUNDATION", "M1247-X-TRUST"} else ("source_map" if child == "M1247-X-SOURCE" else "provenance_of")
    graph = "trust" if typ == "trusts" else "provenance"
    edge(graph, "E-ROOT-"+child.removeprefix("M1247-"), typ, "M1247-ROOT", child)
for oid in ids:
    if oid != "M1247-X-SOURCE":
        edge("documentation", "D-"+oid.removeprefix("M1247-"), "documents", "M1247-X-SOURCE", oid)
for parent, child, tag in (("M1247-ROOT","M1247-T-TRANSPORT","ROOT-TRANSPORT"), ("M1247-T-TRANSPORT","M1247-L-CORE","TRANSPORT-CORE")):
    edge("workflow", "W-"+tag, "workflow_depends_on", parent, child)

bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_denominator_sha256": denom, "nodes": nodes, "graphs": graphs,
          "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "theorem_complete": False, "remaining_root_cut_set": ["M1247-L-IBP", "M1247-L-HARDY", "M1247-N-WEIGHTS", "M1247-S-BOUNDARY", "M1247-S-DOMAIN", "M1247-S-LAPLACIAN"]}}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
         "recipes": [{"recipe_id": "M1247-V-"+oid.removeprefix("M1247-"), "command": "python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py", "expected": "exit 0", "scope": oid} for oid in ids]}
for name, obj in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=True) + "\n")
print(denom)
