#!/usr/bin/env python3
"""Build the frozen THM-M-0580 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0580-OBLIGATION_TREE"
THEOREM = "THM-M-0580"
PREFIX = "M0580"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# Eligibility is architectural, not based on the currently empty proof search.
rows = [
    ("ROOT", "root", "critical", "The exact compact Hausdorff simply connected topological three-manifold target.", "Stage1Instances.THM_M_0580.PerelmanPoincareTarget", "A homeomorphism with the unit three-sphere."),
    ("S-DEFINITIONS", "definition", "high", "Freeze the Euclidean three-space and unit three-sphere models and the meaning of homeomorphism.", "Stage1Instances.THM_M_0580.{Euclidean3,Sphere3,ExpandedTarget}", "The exact statement interface."),
    ("S-DOMAIN", "normalization", "critical", "Account for the universe, topology, Hausdorff, charted-space, simple-connectedness, and compactness binders without adding orientability or connectedness assumptions.", "planned binder-preservation checks against PerelmanPoincareTarget", "The canonical closed topological three-manifold context."),
    ("S-BOUNDARY", "terminal", "high", "Show that nonemptiness and connectedness follow through SimplyConnectedSpace and that the Euclidean chart model is boundaryless; reject empty, disconnected, noncompact, and boundary-manifold substitutions.", "planned exact boundary and mutation lemmas", "Validated degenerate-case boundary."),
    ("S-TRANSPORT", "transport", "critical", "Relate the alias-expanded target, homotopy-sphere formulation, smooth formulation, and source conventions only in checked directions.", "Stage1Instances.THM_M_0580.perelmanPoincareTarget_iff_expandedTarget plus planned bridges", "Checked formulation transports."),
    ("S-FOUNDATION", "certificate", "critical", "Fix classical choice, quotient, extensionality, TCB, and no-oracle policy for every terminal proof body.", "planned transitive axiom and trust report", "Accepted logical and trust boundary."),
    ("N-SMOOTH", "reduction", "critical", "Equip the canonical topological three-manifold with a compatible smooth structure while preserving its fixed topology and charts.", "Stage1Instances.THM_M_0580.TopologicalThreeManifoldSmoothable", "A compatible smooth manifold instance."),
    ("C-METRIC", "construction", "high", "Construct a smooth Riemannian metric on the compact smooth three-manifold and record completeness and bounded initial geometry.", "planned Riemannian metric construction and invariants", "Admissible initial Ricci-flow data."),
    ("L-SHORT-TIME", "core_lemma", "critical", "Establish short-time Ricci-flow existence and uniqueness for the initial metric.", "planned exact Ricci-flow existence theorem", "A maximal smooth Ricci flow before singular time."),
    ("L-NONCOLLAPSE", "core_lemma", "critical", "Prove the no-local-collapsing estimates required to analyze singular regions.", "planned Perelman noncollapsing package", "Uniform local noncollapsing control."),
    ("L-CANONICAL", "core_lemma", "critical", "Prove canonical-neighborhood and curvature-control results near sufficiently high curvature.", "planned canonical-neighborhood package", "Classified singular neighborhoods with quantitative control."),
    ("C-SURGERY", "construction", "critical", "Choose surgery scales and caps and prove post-surgery smoothness, geometric invariants, and independence sufficient for iteration.", "planned Ricci-flow-with-surgery construction", "A controlled surgery continuation."),
    ("L-SURGERY-EXISTS", "core_lemma", "critical", "Iterate Ricci flow with surgery without finite-time accumulation and with all required estimates preserved.", "planned long-time surgery-flow theorem", "A globally iterated surgery flow until extinction or long-time regime."),
    ("L-FINITE-EXTINCTION", "core_lemma", "critical", "For the simply connected compact case, prove finite extinction of the surgery flow.", "planned finite-extinction theorem with exact hypotheses", "Finite extinction of every component descending from the input."),
    ("B-DECOMPOSITION", "branch", "critical", "Translate finite extinction through prime decomposition into spherical space-form and S2-bundle summands, with an exhaustive recomposition theorem.", "planned extinction-to-prime-decomposition classification", "A connected-sum classification of the original manifold."),
    ("L-PI1-ELIMINATION", "core_lemma", "critical", "Use simple connectedness and free-product behavior of fundamental groups to eliminate nontrivial space forms, S2xS1 factors, and multiple connected-sum factors.", "planned fundamental-group elimination theorem", "The sole remaining prime factor is S3."),
    ("T-SMOOTH-POINCARE", "terminal", "critical", "Assemble the metric, flow, surgery, extinction, decomposition, and fundamental-group packages into the smooth three-dimensional Poincare conclusion.", "Stage1Instances.THM_M_0580.SmoothThreeDimensionalPoincare", "A homeomorphism to Sphere3 under a compatible smooth structure."),
    ("T-ASSEMBLE", "transport", "critical", "Compose topological smoothing and the smooth Poincare conclusion into the exact canonical target.", "Stage1Instances.THM_M_0580.root_of_smoothing_and_smooth_poincare", "The exact canonical proposition, conditional on both packages."),
    ("X-SOURCE", "terminal", "high", "Map every analytic, surgery, extinction, and topology obligation to pinpoint primary and reviewed expository source passages, assumptions, and errata.", "non-machine node-specific source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory every terminal Lean body, wrapper, import, axiom, unsafe boundary, TCB component, and replay receipt.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

source_na = {"S-DEFINITIONS", "S-DOMAIN", "S-BOUNDARY", "S-FOUNDATION", "X-PROVENANCE"}
checked = {"S-DEFINITIONS", "S-TRANSPORT", "T-ASSEMBLE"}
machine_special = {"X-SOURCE": "not_applicable", "X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
root_expression = "938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664"

obligations = []
nodes = []
for short, kind, risk, claim, target, output in rows:
    oid = f"{PREFIX}-{short}"
    fp = (f"lean-expression-sha256:{root_expression}" if short == "ROOT" else
          "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(short, "required")
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fp,
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if short in source_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_semantic_proof_credit"}.get(machine),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0580/ObligationTree.lean#root_of_smoothing_and_smooth_poincare" if short == "T-ASSEMBLE" else None),
    })
    is_checked = short in checked
    nodes.append({
        "node_id": f"{THEOREM}-{short}",
        "obligation_id": oid,
        "kind": kind,
        "human_statement": claim,
        "formal_target": target,
        "output": output,
        "human_debt": "H2" if short in {"ROOT", "X-SOURCE"} else "H3",
        "machine_debt": "M0-L" if is_checked else ("M4" if short != "ROOT" else "M4"),
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if short in source_na else "perelman-node-crosswalk-pending",
        "provenance_id": "local-conditional-composition" if short == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical experiment, oracle, or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 60,
        "semantic_step_ledger": {
            "premises": "Only exact incoming proof_requires children and the stated formal context.",
            "inference": claim,
            "output": output,
            "outgoing_use": "Only the declared typed parent or a non-proof support edge may consume this output.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0580/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0580-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0580/ObligationTree.lean"] if short == "T-ASSEMBLE" else [],
        "owner": "THM-M-0580 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if is_checked else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["statement", "registry", "source map", "toolchain"],
            "revocation_state": "provisional" if is_checked else "open",
        },
    })

denominator_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in denominator_fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact topological statement and bounded anchor audit; smoothing, Ricci-flow-with-surgery, finite-extinction, and geometric-topology architecture; eligibility assigned independently of proof availability.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": f"{PREFIX}-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [f"{PREFIX}-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new registry version and append-only old/new ID delta.",
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(f"{PREFIX}-{x}" for x in checked), "root_machine_debt": "M4"},
    "status_boundary": "Architecture and denominators only; no Perelman theorem proof, H0/R0 clearance, audit completion, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


def oid(short):
    return f"{PREFIX}-{short}"


requires = {
    "ROOT": ["T-ASSEMBLE"],
    "T-ASSEMBLE": ["N-SMOOTH", "T-SMOOTH-POINCARE"],
    "T-SMOOTH-POINCARE": ["C-METRIC", "L-SHORT-TIME", "L-NONCOLLAPSE", "L-CANONICAL", "C-SURGERY", "L-SURGERY-EXISTS", "L-FINITE-EXTINCTION", "B-DECOMPOSITION", "L-PI1-ELIMINATION"],
}
proof_edges = []
for parent, children in requires.items():
    for child in children:
        req = f"REQ-{parent}-{child}"
        comp = f"CMP-{child}-{parent}"
        proof_edges.extend([
            edge(req, oid(parent), "proof_requires", oid(child), comp),
            edge(comp, oid(child), "composes", oid(parent), req),
        ])

graph_edges = {
    "proof": proof_edges,
    "refinement": [edge(f"REF-ROOT-{x}", oid("ROOT"), "logical_decomposition", oid(x)) for x in ("S-DEFINITIONS", "S-DOMAIN", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION")],
    "provenance": [
        edge("SRC-ANALYTIC", oid("L-FINITE-EXTINCTION"), "source_map", oid("X-SOURCE")),
        edge("SRC-TOPOLOGY", oid("B-DECOMPOSITION"), "source_map", oid("X-SOURCE")),
        edge("PROV-ROOT", oid("X-PROVENANCE"), "provenance_of", oid("ROOT")),
    ],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", oid("ROOT"), "trusts", oid("S-FOUNDATION")), edge("TRUST-PROV", oid("ROOT"), "trusts", oid("X-PROVENANCE"))],
    "documentation": [edge("DOC-ROOT", oid("S-DEFINITIONS"), "documents", oid("ROOT")), edge("DOC-SOURCE", oid("X-SOURCE"), "documents", oid("T-SMOOTH-POINCARE"))],
    "workflow": [
        edge("FLOW-ASSEMBLE-SMOOTH", oid("T-ASSEMBLE"), "workflow_depends_on", oid("N-SMOOTH")),
        edge("FLOW-ASSEMBLE-ENGINE", oid("T-ASSEMBLE"), "workflow_depends_on", oid("T-SMOOTH-POINCARE")),
        edge("FLOW-EXTINCTION-SURGERY", oid("L-FINITE-EXTINCTION"), "workflow_depends_on", oid("L-SURGERY-EXISTS")),
        edge("FLOW-DECOMP-EXTINCTION", oid("B-DECOMPOSITION"), "workflow_depends_on", oid("L-FINITE-EXTINCTION")),
        edge("FLOW-PI1-DECOMP", oid("L-PI1-ELIMINATION"), "workflow_depends_on", oid("B-DECOMPOSITION")),
        edge("FLOW-PROV-ASSEMBLE", oid("X-PROVENANCE"), "workflow_depends_on", oid("T-ASSEMBLE")),
    ],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for relation in edges:
        outgoing.setdefault(relation["from"], []).append(relation["edge_id"])
        incoming.setdefault(relation["to"], []).append(relation["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": "THM-M-0580-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": oid("ROOT"),
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": sorted(f"{PREFIX}-{x}" for x in checked),
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": [oid("N-SMOOTH"), oid("T-SMOOTH-POINCARE")],
        "composition_certificates": ["Stage1Instances.THM_M_0580.root_of_smoothing_and_smooth_poincare"],
        "reason": "The checked composition is conditional; neither compatible smoothing nor the smooth Perelman package has a proof body.",
    },
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for obligation in ids:
    recipes["recipes"].append({
        "recipe_id": f"VAL-{obligation}",
        "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-0580/check_obligation_tree.py"],
        "env_allowlist": {},
        "timeout_seconds": 30,
        "network_policy": "denied",
        "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0580 obligation tree"}],
        "covered_obligation_ids": [obligation],
        "covered_declarations": [],
    })

for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / filename).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

print(denominator)
