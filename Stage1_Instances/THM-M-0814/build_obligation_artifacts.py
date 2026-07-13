#!/usr/bin/env python3
"""Build the frozen THM-M-0814 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0814-OBLIGATION_TREE"
THEOREM = "THM-M-0814"
PREFIX = "M0814"
ROOT_EXPRESSION = "f9fc7813f437ebcd4b2b7327373dd76134d651c1624d2a06f689e84ec571a21e"
GRAPH_NAMES = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
STRUCTURE_RECIPE = "VAL-M0814-OBLIGATION-STRUCTURE"
LEAN_RECIPE = "VAL-M0814-OBLIGATION-LEAN"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


def exclusion(code: str, justification: str) -> dict[str, str]:
    return {
        "code": code,
        "justification": justification,
        "approval": "pending independent Stage1 integration review",
    }


# Semantic roles and eligibility are frozen here without candidate or closure status.  The last two
# fields are machine and human-source eligibility; readable eligibility is derived below.
ROWS = (
    ("ROOT", "root", "critical", "Prove the exact finite undirected chain-flow max-flow/min-cut target frozen in Statement.lean.", "Stage1Instances.THM_M_0814.MaxFlowMinCutTarget", "A maximum feasible flow and minimum disconnecting arc set with equal values.", "required", "required"),
    ("S-TARGET", "definition", "critical", "Preserve all binders, terminals, positive NNReal capacities, attained extrema, and equality of the canonical target.", "Stage1Instances.THM_M_0814.MaxFlowMinCutTarget", "The unchanged canonical target and its exact context.", "required", "required"),
    ("S-CHAIN", "definition", "high", "Freeze positive-length simple source-to-sink chains with injective vertex and arc arrays and Graph.IsLink witnesses.", "Stage1Instances.THM_M_0814.Chain", "The finite path objects indexed by the source proof.", "required", "required"),
    ("S-FLOW-CUT", "definition", "high", "Freeze Finsupp chain flows, arc loads, feasibility, disconnecting Finsets, and both NNReal value functions.", "Flow; arcLoad; flowValue; IsFeasible; IsDisconnecting; cutValue", "The exact flow, capacity, and cut semantics used downstream.", "required", "required"),
    ("S-BOUNDARY", "branch", "high", "Retain no-chain and no-edge networks, parallel arcs, isolated vertices, inert loops, zero flow, and empty cut where the frozen definitions allow them.", "canonical no-chain and finite-network boundary package", "An exhaustive boundary policy without an added path-existence premise.", "required", "required"),
    ("S-TRANSPORT", "transport", "high", "Keep the checked ExpandedTarget respelling while rejecting unproved directed-flow, partition-cut, and alternate-capacity transports.", "maxFlowMinCutTarget_iff_expanded", "Only the declared bidirectional direct respelling.", "required", "not_applicable"),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical finite enumeration, choice, quotient, imports, compiled artifacts, and the no-oracle computation boundary.", "planned transitive foundation and TCB report", "An accepted foundation, trust, and computation profile.", "required", "not_applicable"),
    ("N-CHAIN-ENUM", "normalization", "critical", "Construct a finite duplicate-free enumeration of proof-irrelevant Chain values despite their dependent proof fields.", "planned exact Finite/Fintype quotient or subtype representation of Chain", "Finite coordinates covering every semantic source-to-sink chain.", "required", "required"),
    ("N-FLOW-COORD", "normalization", "critical", "Transport Finsupp flows to finite nonnegative coordinate vectors and translate arc loads and flow value exactly.", "planned equivalence between Flow and finite NNReal coordinates", "A finite-dimensional feasible-region representation with checked value/load equations.", "required", "required"),
    ("B-NO-CHAIN", "branch", "high", "Close the no-source-to-sink-chain case with zero flow and empty disconnecting set under the canonical definitions.", "planned exact no-chain branch theorem", "The full root conclusion for networks with no Chain inhabitant.", "required", "required"),
    ("B-HAS-CHAIN", "branch", "critical", "Reduce the nonempty-chain case to the finite-coordinate maximal-flow and left-cut construction route.", "planned exact nonempty-chain branch theorem", "The full root conclusion for networks with at least one chain.", "required", "required"),
    ("B-MERGE", "transport", "high", "Recombine the no-chain and nonempty-chain branches without changing any canonical binder or conclusion.", "planned checked exhaustive branch merge", "Stage1Instances.THM_M_0814.MaxFlowMinCutTarget", "required", "required"),
    ("C-FEASIBLE-POLYTOPE", "construction", "critical", "Build the finite closed bounded feasible coordinate polytope from nonnegativity and all arc-capacity inequalities.", "planned compact feasible-flow coordinate set", "A nonempty compact feasible region containing the zero flow.", "required", "required"),
    ("L-MAX-ATTAIN", "core_lemma", "critical", "Use compactness and continuity of the coordinate sum to obtain a feasible maximum flow.", "Stage1Instances.THM_M_0814_Obligations.MaximalFlowAttainment", "An exact maximum feasible flow with the universal comparison.", "required", "required"),
    ("L-MAX-CONVEX", "core_lemma", "critical", "Show finite convex averages of maximal flows are feasible, maximal, and preserve strict slack on every selected unsaturated arc.", "planned maximal-flow convex-average theorem", "A single maximal flow simultaneously unsaturating finitely many chosen arcs.", "required", "required"),
    ("C-SATURATED-CORE", "construction", "high", "Define S as the graph arcs saturated in every maximal flow and relate membership to arcLoad equality.", "planned Finset of universally saturated arcs", "The finite saturated-core arc set S.", "required", "required"),
    ("L-S-DISCONNECTS", "core_lemma", "critical", "Prove source Lemma 1: S meets every source-to-sink chain by averaging witnesses and increasing that chain's flow.", "planned exact IsDisconnecting theorem for S", "S is a disconnecting set.", "required", "required"),
    ("L-REROUTE-BASIC", "core_lemma", "critical", "Formalize chain splicing, loop erasure, Finsupp coefficient updates, feasibility, and value preservation for one rerouting move.", "planned exact rerouting transformation and invariants", "A simple replacement chain and a same-value feasible rerouted flow.", "required", "required"),
    ("L-S-ORIENTATION", "core_lemma", "critical", "Show every S arc has one orientation across all positive component chains of all maximal flows, using rerouting and convex averaging.", "planned common-orientation theorem for universally saturated arcs", "A well-defined left and right endpoint for every arc in S.", "required", "required"),
    ("C-LEFT-ARCS", "construction", "critical", "Define L as the S arcs whose left endpoint is reachable from the source through arcs unsaturated by some maximal flow.", "planned Finset L with maximal-flow and unsaturated-prefix witnesses", "The source proof's left-arc set L.", "required", "required"),
    ("L-L-DISCONNECTS", "core_lemma", "critical", "Prove source Lemma 2: the first S arc of any chain is left, using averaged prefix slack and a rerouting contradiction.", "planned exact IsDisconnecting theorem for L", "L is a disconnecting set.", "required", "required"),
    ("L-L-AT-MOST-ONE", "core_lemma", "critical", "Prove source Lemma 3: a positive component chain of a maximal flow contains at most one L arc.", "planned exact at-most-one crossing theorem", "Every positive component chain crosses L at most once.", "required", "required"),
    ("L-L-EXACTLY-ONE", "core_lemma", "critical", "Combine L disconnecting with the at-most-one lemma so every positive component chain crosses L exactly once.", "planned exact one-crossing theorem", "Every positive supported chain crosses L exactly once.", "required", "required"),
    ("L-WEAK-DUALITY", "core_lemma", "critical", "Double-count chain weights against an arbitrary disconnecting set and use arc capacity bounds to prove weak duality.", "Stage1Instances.THM_M_0814_Obligations.WeakDuality", "flowValue flow <= cutValue capacity cut.", "required", "required"),
    ("L-COUNT-ONCE", "core_lemma", "critical", "Interchange finite sums and use saturation plus exactly-one crossing to identify the selected maximal-flow value with cutValue L.", "planned exact finite sum equality for a maximal flow and L", "flowValue maximalFlow = cutValue capacity L.", "required", "required"),
    ("T-EQUAL-CUT", "terminal", "critical", "Package L, disconnectivity, and the count-once identity for any selected maximum flow.", "Stage1Instances.THM_M_0814_Obligations.EqualCutForMaximalFlow", "An equal-value disconnecting set for every selected maximum flow.", "required", "required"),
    ("T-CUT-CERT", "terminal", "critical", "Use weak duality to strengthen the equal cut to a universally minimum cut.", "Stage1Instances.THM_M_0814_Obligations.CutCertificateForMaximalFlow", "A minimum disconnecting set equal in value to the selected maximum flow.", "required", "required"),
    ("T-ASSEMBLE", "terminal", "critical", "Consume maximum-flow attainment and the minimum-cut certificate and construct the exact canonical existential conjunction.", "Stage1Instances.THM_M_0814_Obligations.compose_root", "Stage1Instances.THM_M_0814.MaxFlowMinCutTarget", "required", "required"),
    ("X-SOURCE", "terminal", "critical", "Map definitions, Theorem 1, Lemmas 1-3, and every suppressed rerouting/sum step to the pinned pages and an independent review.", "Ford-Fulkerson 1956 pp. 399-402 source crosswalk", "Human-source evidence without machine proof credit.", "not_applicable", "required"),
    ("X-PROVENANCE", "certificate", "critical", "Bind every future terminal body, wrapper, import, revision, license, source slice, and transitive declaration origin.", "planned content-addressed provenance closure", "Release provenance without semantic proof credit.", "informational", "not_applicable"),
    ("X-TRUST", "certificate", "critical", "Close executable, imported-olean, axiom, unsafe/oracle, computation, reproducibility, and independent-verification boundaries.", "planned transitive trust and TCB closure", "Release trust evidence without semantic proof credit.", "informational", "not_applicable"),
    ("X-READABLE", "terminal", "high", "Produce and independently review a complete node-anchored readable reconstruction including every rerouting invariant.", "planned readable reconstruction", "Readable coverage without machine proof credit.", "not_applicable", "not_applicable"),
    ("X-WORKFLOW", "certificate", "high", "Bind proof, validation, release, freshness, revocation, and independent verification tasks.", "planned Stage1 workflow receipts", "Workflow acceptance without proof credit.", "informational", "not_applicable"),
)


CHECKED_INTERFACES = {oid("ROOT"), oid("T-ASSEMBLE"), oid("T-CUT-CERT"), oid("L-WEAK-DUALITY"), oid("T-EQUAL-CUT"), oid("L-MAX-ATTAIN")}
EXACT_INTERFACE_TARGETS = {
    oid("ROOT"): "lean-expression-sha256:" + ROOT_EXPRESSION,
    oid("S-TARGET"): "lean-expression-sha256:" + ROOT_EXPRESSION,
}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    row_by_id: dict[str, tuple] = {}
    for short, kind, risk, claim, target, output, machine, human_source in ROWS:
        identifier = oid(short)
        row_by_id[identifier] = (short, kind, risk, claim, target, output, machine, human_source)
        fingerprint = EXACT_INTERFACE_TARGETS.get(
            identifier,
            "planned:v1:sha256:" + digest([identifier, kind, claim, target, output]),
        )
        excluded = None
        if machine != "required" or human_source != "required":
            if machine == "required":
                excluded = exclusion(
                    "formal_or_trust_interface_not_human_claim",
                    "This formal transport or foundation boundary is not a separate human mathematical claim.",
                )
            elif identifier == oid("X-SOURCE"):
                excluded = exclusion(
                    "human_source_boundary_only",
                    "This obligation carries human-source review and never receives machine proof credit.",
                )
            elif identifier == oid("X-READABLE"):
                excluded = exclusion(
                    "readability_boundary_only",
                    "This obligation carries readable reconstruction and never receives machine or source proof credit.",
                )
            else:
                excluded = exclusion(
                    "assurance_overlay_no_proof_credit",
                    "This provenance, trust, or workflow overlay is informational for proof coverage.",
                )
        readable = "not_applicable" if identifier in {oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW")} else "required"
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": identifier not in {oid("X-PROVENANCE"), oid("X-WORKFLOW")},
            "machine_eligibility": machine,
            "human_source_eligibility": human_source,
            "readable_eligibility": readable,
            "risk_class": risk,
            "exclusion_reason": excluded,
            "terminal_proof_body_id": None,
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in fields} for row in obligations]
    denominator = digest(projection)
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0814-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T23:19:46+08:00",
        "freeze_basis": "The exact elaborated statement and the semantic architecture of Ford-Fulkerson Theorem 1, Lemmas 1-3, and their explicit suppressed formal steps. Eligibility is derived from these roles, not from candidate availability or closure.",
        "freeze_order_boundary": "ROWS contains no observed proof status and its canonical ten-field projection is hashed before status_observed_after_freeze is attached.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "canonical_projection_fields": list(fields),
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
            "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
            "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
            "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The selected proof is mathematical and uses no solver, native evaluator, external oracle, numerical experiment, or certificate. Finite enumeration and sums remain kernel-proof obligations.",
                "reviewer": "independent Stage1 integration lane",
            }
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility change, edge-role change, or terminal-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "candidate_machine_classification": "M3_no_exact_proof_candidate",
            "candidate_evidence_level": "E3_exact_statement_only",
            "candidate_closure_credit": False,
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope, eligibility, and denominators only. Conditional interface checks close no mathematical obligation; H1/M3/R4, AUDIT-Z, and theorem completion do not change.",
    }

    # The proof spine has exact conditional composition certificates at its top two parents.  All
    # deeper mathematical relations are frozen as unverified source-body decompositions.
    proof_pairs = (
        (oid("ROOT"), oid("T-ASSEMBLE"), "composes"),
        (oid("T-ASSEMBLE"), oid("L-MAX-ATTAIN"), "composes"),
        (oid("T-ASSEMBLE"), oid("T-CUT-CERT"), "composes"),
        (oid("T-CUT-CERT"), oid("L-WEAK-DUALITY"), "composes"),
        (oid("T-CUT-CERT"), oid("T-EQUAL-CUT"), "composes"),
        (oid("T-EQUAL-CUT"), oid("L-L-DISCONNECTS"), "logical_decomposition"),
        (oid("T-EQUAL-CUT"), oid("L-COUNT-ONCE"), "logical_decomposition"),
        (oid("L-COUNT-ONCE"), oid("L-L-EXACTLY-ONE"), "logical_decomposition"),
        (oid("L-COUNT-ONCE"), oid("C-SATURATED-CORE"), "logical_decomposition"),
        (oid("L-L-EXACTLY-ONE"), oid("L-L-DISCONNECTS"), "logical_decomposition"),
        (oid("L-L-EXACTLY-ONE"), oid("L-L-AT-MOST-ONE"), "logical_decomposition"),
        (oid("L-L-DISCONNECTS"), oid("C-LEFT-ARCS"), "logical_decomposition"),
        (oid("L-L-DISCONNECTS"), oid("L-S-DISCONNECTS"), "logical_decomposition"),
        (oid("L-L-DISCONNECTS"), oid("L-MAX-CONVEX"), "logical_decomposition"),
        (oid("L-L-DISCONNECTS"), oid("L-REROUTE-BASIC"), "logical_decomposition"),
        (oid("L-L-AT-MOST-ONE"), oid("C-LEFT-ARCS"), "logical_decomposition"),
        (oid("L-L-AT-MOST-ONE"), oid("L-MAX-CONVEX"), "logical_decomposition"),
        (oid("L-L-AT-MOST-ONE"), oid("L-REROUTE-BASIC"), "logical_decomposition"),
        (oid("C-LEFT-ARCS"), oid("L-S-ORIENTATION"), "logical_decomposition"),
        (oid("C-LEFT-ARCS"), oid("C-SATURATED-CORE"), "logical_decomposition"),
        (oid("L-S-ORIENTATION"), oid("L-REROUTE-BASIC"), "logical_decomposition"),
        (oid("L-S-ORIENTATION"), oid("L-MAX-CONVEX"), "logical_decomposition"),
        (oid("L-S-DISCONNECTS"), oid("C-SATURATED-CORE"), "logical_decomposition"),
        (oid("L-S-DISCONNECTS"), oid("L-MAX-CONVEX"), "logical_decomposition"),
        (oid("L-S-DISCONNECTS"), oid("S-CHAIN"), "logical_decomposition"),
        (oid("L-MAX-ATTAIN"), oid("C-FEASIBLE-POLYTOPE"), "logical_decomposition"),
        (oid("C-FEASIBLE-POLYTOPE"), oid("N-FLOW-COORD"), "logical_decomposition"),
        (oid("N-FLOW-COORD"), oid("N-CHAIN-ENUM"), "logical_decomposition"),
        (oid("N-FLOW-COORD"), oid("S-FLOW-CUT"), "logical_decomposition"),
        (oid("L-WEAK-DUALITY"), oid("S-FLOW-CUT"), "logical_decomposition"),
        (oid("L-WEAK-DUALITY"), oid("S-CHAIN"), "logical_decomposition"),
        (oid("B-MERGE"), oid("B-NO-CHAIN"), "logical_decomposition"),
        (oid("B-MERGE"), oid("B-HAS-CHAIN"), "logical_decomposition"),
        (oid("B-NO-CHAIN"), oid("S-BOUNDARY"), "logical_decomposition"),
        (oid("B-HAS-CHAIN"), oid("T-ASSEMBLE"), "logical_decomposition"),
    )
    proof_edges: list[dict] = []
    children: dict[str, list[str]] = {}
    for parent, child, reverse_type in proof_pairs:
        req_id = f"REQ-{parent}-{child}"
        reverse_id = f"{'CMP' if reverse_type == 'composes' else 'DEC'}-{child}-{parent}"
        proof_edges.extend((
            {"edge_id": req_id, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": reverse_id},
            {"edge_id": reverse_id, "from": child, "type": reverse_type, "to": parent, "reciprocal_edge_id": req_id},
        ))
        children.setdefault(parent, []).append(child)

    refinement_edges = [
        {"edge_id": "REF-ROOT-TARGET", "from": oid("ROOT"), "type": "logical_decomposition", "to": oid("S-TARGET")},
        {"edge_id": "REF-TARGET-TRANSPORT", "from": oid("S-TARGET"), "type": "transports", "to": oid("S-TRANSPORT")},
        {"edge_id": "REF-TARGET-BRANCHES", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("B-MERGE")},
        {"edge_id": "REF-TARGET-FOUNDATION", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("S-FOUNDATION")},
    ]

    source_required = [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required" and r["obligation_id"] != oid("X-SOURCE")]
    provenance_edges = []
    for identifier in source_required:
        provenance_edges.append({"edge_id": f"SOURCE-{identifier}", "from": identifier, "type": "source_map", "to": oid("X-SOURCE")})
    for identifier in ids:
        if identifier not in {oid("X-PROVENANCE"), oid("X-SOURCE"), oid("X-TRUST")}:
            provenance_edges.append({"edge_id": f"PROVENANCE-{identifier}", "from": oid("X-PROVENANCE"), "type": "provenance_of", "to": identifier})
    evidence_edges = [
        {"edge_id": f"EVIDENCE-{identifier}", "from": oid("X-PROVENANCE"), "type": "evidence_for", "to": identifier}
        for identifier in ids if identifier not in {oid("X-PROVENANCE"), oid("X-SOURCE"), oid("X-TRUST")}
    ]
    trust_edges = [
        {"edge_id": "TRUST-ROOT-FOUNDATION", "from": oid("ROOT"), "type": "trusts", "to": oid("S-FOUNDATION")},
        {"edge_id": "TRUST-ROOT-BOUNDARY", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TRUST")},
        {"edge_id": "TRUST-PROVENANCE", "from": oid("X-PROVENANCE"), "type": "trusts", "to": oid("X-TRUST")},
    ]
    documentation_edges = [
        {"edge_id": f"DOCUMENT-{identifier}", "from": oid("X-SOURCE"), "type": "documents", "to": identifier}
        for identifier in ids if identifier != oid("X-SOURCE")
    ]
    workflow_nodes = [
        "S56-M-0814-ANCHOR_AUDIT", ITEM, "S56-M-0814-PROOF",
        "S56-M-0814-VALIDATION", "S56-M-0814-RELEASE",
    ]
    workflow_edges = [
        {"edge_id": "FLOW-TREE-ANCHOR", "from": ITEM, "type": "workflow_depends_on", "to": "S56-M-0814-ANCHOR_AUDIT"},
        {"edge_id": "FLOW-PROOF-TREE", "from": "S56-M-0814-PROOF", "type": "workflow_depends_on", "to": ITEM},
        {"edge_id": "FLOW-VALIDATION-PROOF", "from": "S56-M-0814-VALIDATION", "type": "workflow_depends_on", "to": "S56-M-0814-PROOF"},
        {"edge_id": "FLOW-RELEASE-VALIDATION", "from": "S56-M-0814-RELEASE", "type": "workflow_depends_on", "to": "S56-M-0814-VALIDATION"},
    ]

    checked_source = "Stage1_Instances/THM-M-0814/ObligationTree.lean"
    nodes = []
    for obligation in obligations:
        identifier = obligation["obligation_id"]
        short, kind, risk, claim, target, output, machine, human_source = row_by_id[identifier]
        checked = identifier in CHECKED_INTERFACES
        source_locator = {
            oid("L-MAX-ATTAIN"): "Ford-Fulkerson-1956:p400:66-72",
            oid("L-S-DISCONNECTS"): "Ford-Fulkerson-1956:p400:73-86:Lemma-1",
            oid("L-S-ORIENTATION"): "Ford-Fulkerson-1956:pp400-401:87-112",
            oid("L-L-DISCONNECTS"): "Ford-Fulkerson-1956:p401:113-132:Lemma-2",
            oid("L-L-AT-MOST-ONE"): "Ford-Fulkerson-1956:pp401-402:133-154:Lemma-3",
            oid("L-WEAK-DUALITY"): "Ford-Fulkerson-1956:p402:155-160",
            oid("L-COUNT-ONCE"): "Ford-Fulkerson-1956:p402:155-160",
        }.get(identifier, "architecture:v1:" + identifier)
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": kind,
            "human_statement": claim,
            "formal_target": target,
            "output": output,
            "human_debt": "H1",
            "machine_debt": "M3" if machine == "required" else "M4",
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": "not-applicable" if human_source == "not_applicable" else "ford-fulkerson-1956-theorem1-map-v1-pending-review",
            "provenance_id": "conditional-local-composition:v1" if checked else "none",
            "foundation_profile": "lean4-mathlib-classical/v1-pending-transitive-review",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/v1-pending-release-closure",
            "computation_record": "none credited; finite enumeration and sums require kernel proof",
            "step_budget": 80 if risk == "critical" else 55,
            "semantic_step_ledger": [{
                "step_id": f"STEP-{identifier}-1",
                "premise_ids": children.get(identifier, ["frozen-formal-context"]),
                "inference": claim,
                "source_locator": source_locator,
                "output": output,
                "outgoing_use": "Consumed only by declared proof/refinement edges; no closure follows from this ledger.",
            }],
            "public_readable_target": f"Stage1_Instances/THM-M-0814/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": LEAN_RECIPE if checked else STRUCTURE_RECIPE,
            "status_boundary": "Open architecture obligation; no M0, accepted proof, H0, or R0 credit.",
            "task_ids": [ITEM],
            "owned_sources": [checked_source] if checked else [],
            "owner": "THM-M-0814 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": None,
                "review_due": "before any proof acceptance",
                "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation registry", "typed edges", "toolchain"],
                "revocation_state": "not-accepted",
            },
        })

    def graph(edges: list[dict]) -> dict:
        incoming: dict[str, list[str]] = {}
        outgoing: dict[str, list[str]] = {}
        for edge in edges:
            outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
            incoming.setdefault(edge["to"], []).append(edge["edge_id"])
        return {"edges": edges, "out": outgoing, "in": incoming}

    obligation_by_id = {row["obligation_id"]: row for row in obligations}
    composition_certificates = [
        {
            "certificate_id": "COMP-M0814-ROOT",
            "parent_obligation_id": oid("ROOT"),
            "parent_statement_fingerprint": obligation_by_id[oid("ROOT")]["statement_fingerprint"],
            "required_child_ids": [oid("T-ASSEMBLE")],
            "required_child_statement_fingerprints": {oid("T-ASSEMBLE"): obligation_by_id[oid("T-ASSEMBLE")]["statement_fingerprint"]},
            "checked_declaration": "Stage1Instances.THM_M_0814_Obligations.root_of_terminal",
            "certificate_kind": "lean_abstract_child_harness",
            "status": "provisionally_elaborated_not_accepted",
            "introduces_undeclared_premises": False,
        },
        {
            "certificate_id": "COMP-M0814-T-ASSEMBLE",
            "parent_obligation_id": oid("T-ASSEMBLE"),
            "parent_statement_fingerprint": obligation_by_id[oid("T-ASSEMBLE")]["statement_fingerprint"],
            "required_child_ids": [oid("L-MAX-ATTAIN"), oid("T-CUT-CERT")],
            "required_child_statement_fingerprints": {child: obligation_by_id[child]["statement_fingerprint"] for child in [oid("L-MAX-ATTAIN"), oid("T-CUT-CERT")]},
            "checked_declaration": "Stage1Instances.THM_M_0814_Obligations.compose_root",
            "certificate_kind": "lean_abstract_child_harness",
            "status": "provisionally_elaborated_not_accepted",
            "introduces_undeclared_premises": False,
        },
        {
            "certificate_id": "COMP-M0814-T-CUT-CERT",
            "parent_obligation_id": oid("T-CUT-CERT"),
            "parent_statement_fingerprint": obligation_by_id[oid("T-CUT-CERT")]["statement_fingerprint"],
            "required_child_ids": [oid("L-WEAK-DUALITY"), oid("T-EQUAL-CUT")],
            "required_child_statement_fingerprints": {child: obligation_by_id[child]["statement_fingerprint"] for child in [oid("L-WEAK-DUALITY"), oid("T-EQUAL-CUT")]},
            "checked_declaration": "Stage1Instances.THM_M_0814_Obligations.cutCertificate_compose",
            "certificate_kind": "lean_abstract_child_harness",
            "status": "provisionally_elaborated_not_accepted",
            "introduces_undeclared_premises": False,
        },
    ]
    certificate_parents = {row["parent_obligation_id"] for row in composition_certificates}
    unverified_plans = [
        {
            "plan_id": f"DECOMP-{parent}",
            "parent_obligation_id": parent,
            "planned_child_ids": child_ids,
            "source_declaration": "Ford-Fulkerson 1956 Theorem 1 proof architecture",
            "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
            "required_future_certificate": "An exact Lean abstract-child harness must bind these fingerprints and consume every child before parent closure.",
        }
        for parent, child_ids in children.items() if parent not in certificate_parents
    ]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_version": 1,
        "registry_denominator_sha256": denominator,
        "root_node_id": f"{THEOREM}-ROOT",
        "workflow_task_nodes": workflow_nodes,
        "nodes": nodes,
        "graphs": {
            "proof": graph(proof_edges),
            "refinement": graph(refinement_edges),
            "provenance": graph(provenance_edges),
            "evidence": graph(evidence_edges),
            "trust": graph(trust_edges),
            "documentation": graph(documentation_edges),
            "workflow": graph(workflow_edges),
        },
        "composition_certificates": composition_certificates,
        "unverified_decomposition_plans": unverified_plans,
        "closure_boundary": {
            "closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "proof_leaf_cut_set": sorted(identifier for identifier in set(ids) if identifier not in children and obligation_by_id[identifier]["machine_eligibility"] == "required"),
            "remaining_release_cut_set": [oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"), "master acceptance"],
            "candidate_evidence": "E3 exact-statement evidence only; no exact root proof candidate was located.",
            "reason": "Only conditional top-spine composition is checked. Every mathematical premise remains open and every deeper source relation requires a future exact certificate.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [
            {
                "recipe_id": STRUCTURE_RECIPE,
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0814/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 120,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0814 obligation tree"}],
                "covered_obligation_ids": ids,
                "covered_declarations": [],
                "coverage_boundary": "Checks registry, schemas, graph semantics, source mappings, and open state only; supplies no kernel proof closure.",
            },
            {
                "recipe_id": LEAN_RECIPE,
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0814/check_obligation_tree.py", "--run-lean"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains Lean composition: pass and no sorryAx"}],
                "covered_obligation_ids": sorted(CHECKED_INTERFACES),
                "covered_declarations": [
                    "Stage1Instances.THM_M_0814_Obligations.MaximalFlowAttainment",
                    "Stage1Instances.THM_M_0814_Obligations.WeakDuality",
                    "Stage1Instances.THM_M_0814_Obligations.EqualCutForMaximalFlow",
                    "Stage1Instances.THM_M_0814_Obligations.CutCertificateForMaximalFlow",
                    "Stage1Instances.THM_M_0814_Obligations.cutCertificate_compose",
                    "Stage1Instances.THM_M_0814_Obligations.compose_root",
                    "Stage1Instances.THM_M_0814_Obligations.root_of_terminal",
                ],
                "coverage_boundary": "Kernel-checks exact conditional interfaces and composition only. It supplies none of the mathematical premises and closes no obligation.",
            },
        ],
    }
    return registry, bundle, recipes


def main() -> None:
    registry, bundle, recipes = build()
    for name, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", recipes),
    ):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    print(f"wrote {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
