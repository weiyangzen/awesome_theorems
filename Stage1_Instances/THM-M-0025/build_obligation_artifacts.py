#!/usr/bin/env python3
"""Build the frozen THM-M-0025 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0025-OBLIGATION_TREE"
THEOREM = "THM-M-0025"
PREFIX = "M0025"
ROOT_EXPRESSION = "9bb5ed6dd01550f3481d4a66e1d81009272b717997f9752ff422029da2828564"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_BLOB = "1ae18244a4534f336f1d9280a1f5f8fd1a5acd9f"
GRAPH_NAMES = (
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
)


def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(data).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


# Eligibility and risk are architecture inputs. Machine status is deliberately assigned only after
# the registry projection and denominator have been frozen.
ROWS = (
    (
        "ROOT", "root", "critical",
        "Prove the exact one-variable Hilbert basis theorem target frozen in Statement.lean.",
        "Stage1Instances.THM_M_0025.HilbertBasisTheoremTarget",
        "Every univariate polynomial ring over a commutative Noetherian ring is Noetherian.",
        "required", "required", None, 25,
    ),
    (
        "S-INTERFACE", "definition", "high",
        "Preserve the universe, implicit ring binder, CommRing and IsNoetherianRing instances, and Polynomial conclusion.",
        "Stage1Instances.THM_M_0025.HilbertBasisTheoremTarget",
        "The exact canonical root interface with no Nontrivial, domain, field, or characteristic premise.",
        "required", "required", None, 30,
    ),
    (
        "S-FG-TRANSPORT", "transport", "high",
        "Relate typeclass Noetherianity to finite generation of every ideal in both checked directions.",
        "Stage1Instances.THM_M_0025.hilbertBasisTheoremTarget_iff_idealFiniteGenerationTarget",
        "A checked iff between the canonical target and the every-ideal-FG encoding.",
        "required", "not_applicable", "repo:Statement.lean#hilbertBasisTheoremTarget_iff_idealFiniteGenerationTarget", 30,
    ),
    (
        "S-ZERO-RING-BOUNDARY", "branch", "high",
        "Keep the subsingleton zero ring in scope and forbid insertion of a Nontrivial coefficient-ring premise.",
        "Stage1Instances.THM_M_0025.subsingleton_boundary_has_no_nontrivial plus BoundaryProbe.lean",
        "A checked boundary showing that the exact antecedent includes a commutative Noetherian zero ring.",
        "required", "required", None, 25,
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Audit classical choice, propositional extensionality, quotient soundness, kernel, imports, and no-oracle policy.",
        "planned transitive axiom, foundation, computation, and TCB report",
        "An accepted foundation and computation boundary for the exact terminal body.",
        "required", "not_applicable", None, 45,
    ),
    (
        "T-ROOT-COMPOSE", "terminal", "high",
        "Consume the every-ideal-FG conclusion and return the exact canonical IsNoetherianRing target.",
        "Stage1Instances.THM_M_0025.ObligationTree.root_of_everyPolynomialIdealFG",
        "Stage1Instances.THM_M_0025.HilbertBasisTheoremTarget.",
        "required", "required", "local:ObligationTree.lean#root_of_everyPolynomialIdealFG", 20,
    ),
    (
        "T-IDEAL-FG-COMPOSE", "transport", "high",
        "Consume the exact polynomial Noetherian anchor and expose finite generation of every polynomial ideal.",
        "Stage1Instances.THM_M_0025.ObligationTree.everyPolynomialIdealFG_of_exactPolynomialAnchor",
        "Stage1Instances.THM_M_0025.ObligationTree.EveryPolynomialIdealFG.",
        "required", "required", "local:ObligationTree.lean#everyPolynomialIdealFG_of_exactPolynomialAnchor", 20,
    ),
    (
        "X-MATHLIB-BODY", "bridge", "critical",
        "Audit and later install the exact pinned Polynomial.isNoetherianRing terminal body without counting its wrapper twice.",
        "Polynomial.isNoetherianRing",
        "The exact Noetherian polynomial-ring proposition consumed by T-IDEAL-FG-COMPOSE.",
        "required", "required", f"git-blob:{MATHLIB_BLOB}:Polynomial.isNoetherianRing", 70,
    ),
    (
        "N-IDEAL-FG", "reduction", "critical",
        "Reduce polynomial-ring Noetherianity to constructing a finite spanning set for each ideal I of R[X].",
        "isNoetherianRing_iff together with Ideal.FG",
        "For arbitrary I : Ideal R[X], a Finset s with Ideal.span s = I.",
        "required", "required", f"pinned-mathlib:{MATHLIB_REVISION}#isNoetherianRing_iff", 35,
    ),
    (
        "C-WF-MIN", "construction", "critical",
        "Choose a well-founded minimum M among the coefficient ideals I.leadingCoeffNth k and recover its index N.",
        "IsNoetherian.wf.min, WellFounded.min_mem, and Set.range I.leadingCoeffNth",
        "N with M = I.leadingCoeffNth N and minimality of M in the range.",
        "required", "required", None, 55,
    ),
    (
        "L-MIN-DOMINATES", "core_lemma", "critical",
        "Use minimality and monotonicity to show every I.leadingCoeffNth k is contained in M.",
        "WellFounded.not_lt_min and Ideal.leadingCoeffNth_mono",
        "For every k, I.leadingCoeffNth k <= M.",
        "required", "required", None, 75,
    ),
    (
        "C-BOUNDED-GENERATORS", "construction", "critical",
        "Obtain a finite generating set for the bounded-degree submodule I.degreeLE N.",
        "Ideal.is_fg_degreeLE",
        "A Finset s whose submodule span is I.degreeLE N.",
        "required", "required", f"pinned-mathlib:{MATHLIB_REVISION}#Ideal.is_fg_degreeLE", 75,
    ),
    (
        "L-BOUNDED-SPAN", "core_lemma", "high",
        "Transport bounded-degree submodule generation into membership in the ideal span of the same finite set.",
        "Submodule.span_induction and ideal closure under zero, addition, and multiplication",
        "Every x in I.degreeLE N belongs to Ideal.span s.",
        "required", "required", None, 70,
    ),
    (
        "L-GENERATOR-SPAN-SUBSET", "core_lemma", "high",
        "Show every selected bounded-degree generator belongs to I and hence its ideal span is contained in I.",
        "Ideal.span_le applied to generator membership through I.degreeLE N",
        "Ideal.span s <= I.",
        "required", "required", None, 45,
    ),
    (
        "L-STRONG-INDUCTION-SPAN", "core_lemma", "critical",
        "Prove every p in I belongs to Ideal.span s by strong induction on p.natDegree.",
        "Nat.strong_induction_on",
        "I <= Ideal.span s, completing finite generation of I.",
        "required", "required", None, 85,
    ),
    (
        "B-DEGREE-SPLIT", "branch", "high",
        "Split the induction step exhaustively into natDegree p <= N and N < natDegree p.",
        "le_or_gt (p.natDegree) N",
        "Either bounded-span membership or the high-degree cancellation branch.",
        "required", "required", None, 35,
    ),
    (
        "B-HIGH-DEGREE-NONTRIVIAL", "branch", "high",
        "In the high-degree branch, prove p is nonzero and derive Nontrivial R locally, leaving the zero ring handled by contradiction.",
        "p != 0 from positive degree and a local 0 != 1 argument",
        "A valid Nontrivial R instance for leading-coefficient degree calculations in this branch.",
        "required", "required", None, 55,
    ),
    (
        "C-LEADING-REPRESENTATIVE", "construction", "critical",
        "Use leading-coefficient-ideal domination to choose q in I of degree at most N with q.leadingCoeff = p.leadingCoeff.",
        "Ideal.mem_leadingCoeffNth",
        "q in I, degree q <= N, and matching leading coefficient.",
        "required", "required", None, 70,
    ),
    (
        "L-DEGREE-CANCELLATION", "core_lemma", "critical",
        "Shift q by X^(k-q.natDegree), match degree and leading coefficient, and strictly lower the degree after subtraction.",
        "Polynomial.degree_mul', Polynomial.leadingCoeff_mul_X_pow, and Polynomial.degree_sub_lt",
        "degree (p - q * X^(k-q.natDegree)) < degree p.",
        "required", "required", None, 90,
    ),
    (
        "T-SPAN-COMPOSE", "terminal", "critical",
        "Apply the induction hypothesis to the smaller remainder and combine it with bounded-span membership of q to reconstruct p in Ideal.span s.",
        "Nat.strong_induction_on hypothesis plus Ideal.span add_mem and mul_mem_right",
        "High-degree p belongs to Ideal.span s, completing the induction step.",
        "required", "required", None, 75,
    ),
    (
        "T-FG-COMPOSE", "terminal", "critical",
        "Combine both ideal-span inclusions to identify I with the span of the finite bounded-degree generator set.",
        "le_antisymm applied to Ideal.span s <= I and I <= Ideal.span s",
        "A finite set s with Ideal.span s = I, establishing I.FG.",
        "required", "required", None, 35,
    ),
    (
        "X-SOURCE", "terminal", "critical",
        "Pinpoint and independently review primary-source definitions, assumptions, proof steps, and errata for every material node.",
        "non-machine primary-source crosswalk",
        "Human-source evidence without machine proof credit.",
        "not_applicable", "required", None, 80,
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Resolve the terminal body, source blob, import graph, aliases, licenses, and transitive declaration origins.",
        "planned machine-derived provenance closure",
        "Release provenance without mathematical proof credit.",
        "informational", "not_applicable", None, 60,
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Resolve kernel, compiled artifacts, executables, axiom closure, supply chain, and offline replay boundaries.",
        "planned release trust and TCB closure",
        "Release trust evidence without mathematical proof credit.",
        "informational", "not_applicable", None, 60,
    ),
    (
        "X-READABLE", "terminal", "high",
        "Produce and independently review a complete readable reconstruction of the leading-coefficient induction proof.",
        "planned node-specific readable reconstruction",
        "Readable coverage and independent review without machine proof credit.",
        "not_applicable", "required", None, 95,
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind proof, validation, release, freshness, revocation, and independent-verification task acceptance.",
        "planned Stage1 workflow receipts",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", None, 45,
    ),
)


REQUIRES = {
    oid("ROOT"): [oid("T-ROOT-COMPOSE")],
    oid("T-ROOT-COMPOSE"): [oid("T-IDEAL-FG-COMPOSE")],
    oid("T-IDEAL-FG-COMPOSE"): [oid("X-MATHLIB-BODY")],
}

# Internal edges expand the visible pinned body but have no local composition certificate in this
# phase. They are logical decomposition edges, never machine-closure `composes` edges.
BODY_DECOMPOSITION = {
    oid("X-MATHLIB-BODY"): [oid("N-IDEAL-FG")],
    oid("N-IDEAL-FG"): [oid("T-FG-COMPOSE")],
    oid("T-FG-COMPOSE"): [oid("L-GENERATOR-SPAN-SUBSET"), oid("L-STRONG-INDUCTION-SPAN")],
    oid("L-GENERATOR-SPAN-SUBSET"): [oid("C-BOUNDED-GENERATORS")],
    oid("L-BOUNDED-SPAN"): [oid("C-BOUNDED-GENERATORS")],
    oid("L-STRONG-INDUCTION-SPAN"): [oid("B-DEGREE-SPLIT")],
    oid("B-DEGREE-SPLIT"): [oid("L-BOUNDED-SPAN"), oid("T-SPAN-COMPOSE")],
    oid("T-SPAN-COMPOSE"): [oid("L-BOUNDED-SPAN"), oid("L-DEGREE-CANCELLATION")],
    oid("L-DEGREE-CANCELLATION"): [oid("B-HIGH-DEGREE-NONTRIVIAL"), oid("C-LEADING-REPRESENTATIVE")],
    oid("C-LEADING-REPRESENTATIVE"): [oid("L-MIN-DOMINATES")],
    oid("L-MIN-DOMINATES"): [oid("C-WF-MIN")],
}

CHECKED_INTERFACES = {
    oid("S-INTERFACE"), oid("S-FG-TRANSPORT"), oid("S-ZERO-RING-BOUNDARY"),
    oid("T-ROOT-COMPOSE"), oid("T-IDEAL-FG-COMPOSE"),
}
SOURCE_NA = {
    oid("S-FG-TRANSPORT"), oid("S-FOUNDATION"), oid("X-PROVENANCE"),
    oid("X-TRUST"), oid("X-WORKFLOW"),
}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    parent_map: dict[str, list[str]] = {}
    all_architecture_edges = {**REQUIRES, **BODY_DECOMPOSITION}
    for parent, children in all_architecture_edges.items():
        for child in children:
            parent_map.setdefault(child, []).append(parent)

    obligations: list[dict] = []
    nodes: list[dict] = []
    for short, kind, risk, claim, target, output, machine, human_source, body, budget in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")} else
            "planned:v1:sha256:" + digest([identifier, kind, claim, target, output])
        )
        exclusion = None
        if machine != "required" or human_source != "required":
            exclusion = {
                oid("S-FG-TRANSPORT"): "formal_transport_source_coverage_inherited_from_root_pending_reviewer_acceptance",
                oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_claim_pending_reviewer_acceptance",
                oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
                oid("X-PROVENANCE"): "provenance_overlay_no_proof_credit_pending_integration_review",
                oid("X-TRUST"): "trust_overlay_no_proof_credit_pending_integration_review",
                oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
                oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
            }[identifier]
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human_source,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusion,
            "terminal_proof_body_id": body,
        })

        if identifier in CHECKED_INTERFACES:
            machine_debt = "M0-L"
        elif identifier == oid("ROOT"):
            machine_debt = "M3"
        elif identifier == oid("X-MATHLIB-BODY"):
            machine_debt = "M0-W"
        else:
            machine_debt = "M4"
        if identifier == oid("X-MATHLIB-BODY"):
            provenance = "anchor-audit:M0025-C01-MATHLIB-DIRECT"
        elif identifier in {oid("T-ROOT-COMPOSE"), oid("T-IDEAL-FG-COMPOSE")}:
            provenance = "local-conditional-composition"
        elif identifier in {item for children in all_architecture_edges.values() for item in children}:
            provenance = "pinned-visible-terminal-body"
        else:
            provenance = "none"
        owned_sources = []
        if identifier in {oid("T-ROOT-COMPOSE"), oid("T-IDEAL-FG-COMPOSE")}:
            owned_sources = [f"Stage1_Instances/{THEOREM}/ObligationTree.lean"]
        elif identifier in {oid("S-FG-TRANSPORT"), oid("S-ZERO-RING-BOUNDARY")}:
            owned_sources = [f"Stage1_Instances/{THEOREM}/Statement.lean"]
        children = all_architecture_edges.get(identifier, [])
        parents = parent_map.get(identifier, [])
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": kind,
            "human_statement": claim,
            "formal_target": target,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R3",
            "evidence_ids": [],
            "source_crosswalk_id": "not-applicable-pending-review" if identifier in SOURCE_NA else "primary-source-node-map-pending",
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; accepted axiom policy and transitive review pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
            "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": children if children else ["exact formal context and no undeclared mathematical premise"],
                "inference": claim,
                "output": output,
                "outgoing_use": parents if parents else ["typed support edge only or canonical terminal output"],
            },
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture, audited candidate, or conditional interface only; no accepted root proof or theorem completion.",
            "task_ids": [ITEM, "S56-M-0025-PROOF"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0025 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "toolchain and dependency pins",
                ],
                "revocation_state": "provisional" if identifier in CHECKED_INTERFACES else "open",
            },
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = digest([{field: row[field] for field in fields} for row in obligations])
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0025-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "The exact statement and the visible semantic architecture of the pinned terminal body. Eligibility and denominators are architecture-derived and do not use candidate closure status.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "representative_symmetry_sign_order_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The visible route has no quotient representative, symmetry, sign, or order normalization; degree normalization and its exhaustive split are explicit obligations.",
            },
            "local_global_or_finite_infinite_reduction": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The exact one-variable ideal argument is uniform and contains no local/global or finite/infinite reduction.",
            },
            "computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, solver, native code, oracle, experiment, finite computation, or certificate occurs in the visible terminal body.",
            },
        },
        "proof_body_aliases": {
            "Stage1Instances.THM_M_0025_AnchorAudit.exactTarget_mathlib_candidate": "deduplicated_to:Polynomial.isNoetherianRing",
            "Polynomial.instIsNoetherianRing": "deduplicated_to:Polynomial.isNoetherianRing",
        },
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "audited_candidate_obligation": oid("X-MATHLIB-BODY"),
            "audited_candidate_classification": "M0-W_candidate_pending_proof_phase_and_master_acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry and typed architecture only. The exact candidate is not installed or accepted; H0, R0, audit completion, validation, release, and theorem completion remain open.",
    }

    def edge(edge_id: str, source: str, edge_type: str, target: str, reciprocal: str | None = None) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        return value

    proof: list[dict] = []
    for parent, children in REQUIRES.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            comp = f"CMP-{child}-{parent}"
            proof.extend([
                edge(req, parent, "proof_requires", child, comp),
                edge(comp, child, "composes", parent, req),
            ])
    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "logical_decomposition", oid("S-INTERFACE")),
            edge("REF-ROOT-FG", oid("ROOT"), "logical_decomposition", oid("S-FG-TRANSPORT")),
            edge("REF-ROOT-ZERO", oid("ROOT"), "logical_decomposition", oid("S-ZERO-RING-BOUNDARY")),
        ] + [
            edge(f"REF-{parent}-{child}", parent, "logical_decomposition", child)
            for parent, children in BODY_DECOMPOSITION.items() for child in children
        ],
        "provenance": [
            edge("SRC-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-MIN", oid("X-SOURCE"), "source_map", oid("C-WF-MIN")),
            edge("SRC-INDUCTION", oid("X-SOURCE"), "source_map", oid("L-STRONG-INDUCTION-SPAN")),
            edge("PROV-BODY", oid("X-PROVENANCE"), "provenance_of", oid("X-MATHLIB-BODY")),
            edge("PROV-HELPER", oid("X-PROVENANCE"), "provenance_of", oid("C-BOUNDED-GENERATORS")),
        ],
        "evidence": [
            edge("EVID-BODY", oid("X-PROVENANCE"), "evidence_for", oid("X-MATHLIB-BODY")),
            edge("EVID-WORKFLOW", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-TCB", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-BODY-TCB", oid("X-MATHLIB-BODY"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-MIN", oid("X-READABLE"), "documents", oid("C-WF-MIN")),
            edge("DOC-READABLE-INDUCTION", oid("X-READABLE"), "documents", oid("L-STRONG-INDUCTION-SPAN")),
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge("FLOW-ROOT-PROOF", oid("ROOT"), "workflow_depends_on", oid("X-MATHLIB-BODY")),
            edge("FLOW-PROV-PROOF", oid("X-PROVENANCE"), "workflow_depends_on", oid("X-MATHLIB-BODY")),
            edge("FLOW-TRUST-PROV", oid("X-TRUST"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-WORKFLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-WORKFLOW-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
            edge("FLOW-WORKFLOW-SOURCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
        ],
    }
    graphs = {}
    for name in GRAPH_NAMES:
        outgoing = {identifier: [] for identifier in ids}
        incoming = {identifier: [] for identifier in ids}
        for row in graph_edges[name]:
            outgoing[row["from"]].append(row["edge_id"])
            incoming[row["to"]].append(row["edge_id"])
        graphs[name] = {"edges": graph_edges[name], "out": outgoing, "in": incoming}

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [
                oid("X-MATHLIB-BODY"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "composition_certificates": [
                "Stage1Instances.THM_M_0025.ObligationTree.everyPolynomialIdealFG_of_exactPolynomialAnchor",
                "Stage1Instances.THM_M_0025.ObligationTree.root_of_everyPolynomialIdealFG",
                "Stage1Instances.THM_M_0025.ObligationTree.root_of_exactPolynomialAnchor",
            ],
            "reason": "All local compositions are conditional. The exact pinned anchor remains uninstalled and unaccepted until the proof phase and master validation.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [],
    }
    for identifier in ids:
        declarations = []
        if identifier == oid("T-ROOT-COMPOSE"):
            declarations = ["Stage1Instances.THM_M_0025.ObligationTree.root_of_everyPolynomialIdealFG"]
        elif identifier == oid("T-IDEAL-FG-COMPOSE"):
            declarations = ["Stage1Instances.THM_M_0025.ObligationTree.everyPolynomialIdealFG_of_exactPolynomialAnchor"]
        elif identifier == oid("X-MATHLIB-BODY"):
            declarations = ["Polynomial.isNoetherianRing"]
        recipes["recipes"].append({
            "recipe_id": f"VAL-{identifier}",
            "cwd": ".",
            "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 90,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{
                "path_or_stream": "stdout",
                "semantic_hash_policy": "contains PASS THM-M-0025 obligation tree",
            }],
            "covered_obligation_ids": [identifier],
            "covered_declarations": declarations,
            "coverage_semantics": "architecture_validation_only",
            "closure_credit": False,
        })
    return registry, bundle, recipes


def main() -> None:
    values = build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), values
    ):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    edge_count = sum(len(graph["edges"]) for graph in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(values[0]["denominator_sha256"])


if __name__ == "__main__":
    main()
