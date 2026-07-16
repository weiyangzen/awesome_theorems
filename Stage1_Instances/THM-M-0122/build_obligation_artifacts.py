#!/usr/bin/env python3
"""Build the frozen THM-M-0122 obligation registry and typed graphs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0122-OBLIGATION_TREE"
THEOREM = "THM-M-0122"
PREFIX = "M0122-"
ROOT_EXPRESSION = "f3e5f585b30ab9543bc47551d0d91c695523bace26fdb5484869add319ef7dac"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
)
REGISTRY_FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)


def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def oid(short: str) -> str:
    return PREFIX + short


# short id, kind, risk, claim, formal target, output, machine eligibility,
# human-source eligibility, terminal body identity, planned leaf budget
ROWS = (
    (
        "ROOT", "root", "critical",
        "Every smooth, concretely projective, geometrically connected curve over a number field whose concrete structure-sheaf H1 has cohomological genus greater than one has finitely many rational sections.",
        "Stage1Instances.THMM0122.FaltingsTarget",
        "The exact frozen Faltings/Mordell proposition.",
        "required", "required", None, 1,
    ),
    (
        "S-INTERFACE", "definition", "critical",
        "Freeze the universes, number-field binders, curve scheme and structure morphism, smoothness, concrete projectivity, geometric connectedness, cohomological genus, and rational-section conclusion.",
        "Stage1Instances.THMM0122.FaltingsTarget",
        "The unchanged elaborated canonical interface.",
        "required", "not_applicable", None, 1,
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Exclude genus zero and one, non-number-field bases, nonsmooth or nonprojective curves, and selected subsets or bounded-height substitutes without adding a hidden nonemptiness premise.",
        "Statement.lean mutation and boundary declarations",
        "The complete frozen domain and degenerate-case policy.",
        "required", "required", None, 1,
    ),
    (
        "S-POINT-TRANSPORT", "transport", "high",
        "Identify rational points represented as sections with the equivalent slice-category morphism encoding and preserve finiteness in both directions.",
        "Stage1Instances.THMM0122.faltingsTarget_iff_over",
        "A checked iff between the canonical target and its slice-category point form.",
        "required", "not_applicable", "repo:Stage1Instances.THMM0122.faltingsTarget_iff_over", 1,
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Audit the Lean kernel, propositional extensionality, classical choice, quotients, imported compiled artifacts, and the no-oracle computation boundary.",
        "Lean 4.29.0 foundation and transitive trust report",
        "An accepted foundation, computation, and TCB boundary.",
        "required", "not_applicable", None, 1,
    ),
    (
        "N-FINITE-EXTENSION", "normalization", "critical",
        "Pass to a finite number-field extension over which the curve has a rational point, preserve all curve hypotheses, and retain an injection from the original rational points.",
        "Stage1Instances.THMM0122.ObligationTree.FiniteExtensionNormalization",
        "A pointed normalized curve D/L and an injection C(K) to D(L).",
        "required", "required", None, 1,
    ),
    (
        "N-EXTENSION-EXISTS", "core_lemma", "critical",
        "Produce a finite extension carrying a rational point of the geometrically connected curve.",
        "planned: exists_finite_extension_with_curve_point",
        "A finite number field extension L/K and a point of the base-changed curve.",
        "required", "required", None, 8,
    ),
    (
        "N-BASE-CHANGE", "transport", "critical",
        "Base-change the curve and prove preservation of smoothness, concrete projectivity, geometric connectedness, and cohomological genus together with injectivity on rational points.",
        "planned: rationalPoint_baseChange_injective_and_preserves_hypotheses",
        "The normalized curve hypotheses and the point injection.",
        "required", "required", None, 10,
    ),
    (
        "C-ABEL-JACOBI", "construction", "critical",
        "From a pointed normalized curve construct its Jacobian and the based Abel-Jacobi map.",
        "Stage1Instances.THMM0122.ObligationTree.AbelJacobiPackage",
        "A Jacobian rational-point type and an injective map from curve points.",
        "required", "required", None, 1,
    ),
    (
        "C-JACOBIAN", "construction", "critical",
        "Construct the Jacobian abelian variety of the smooth projective geometrically connected curve and its rational-point group.",
        "planned: jacobian_construction",
        "The Jacobian and its rational-point group.",
        "required", "required", None, 16,
    ),
    (
        "L-ABEL-JACOBI-INJECTIVE", "core_lemma", "critical",
        "For genus greater than one, prove the based Abel-Jacobi map is a closed immersion and injective on rational points.",
        "planned: abelJacobi_isClosedImmersion_and_point_injective",
        "An injection of curve rational points into Jacobian rational points.",
        "required", "required", None, 14,
    ),
    (
        "L-MORDELL-WEIL", "bridge", "critical",
        "Prove finite generation of the Jacobian rational-point group over the normalized number field.",
        "planned: jacobian_rational_points_finitelyGenerated",
        "Finite generation of J(L).",
        "required", "required", None, 12,
    ),
    (
        "L-MORDELL-LANG", "bridge", "critical",
        "Apply the Faltings/Mordell-Lang theorem to the Abel-Jacobi curve image and the finitely generated group J(L).",
        "planned: mordellLang_finite_coset_decomposition",
        "A finite union of cosets describing the intersection with the curve image.",
        "required", "required", None, 1,
    ),
    (
        "L-NO-POSITIVE-COSET", "core_lemma", "critical",
        "Show that a genus-greater-than-one Abel-Jacobi curve contains no translate of a positive-dimensional abelian subvariety.",
        "planned: abelJacobi_image_contains_no_positive_dimensional_coset",
        "Every Mordell-Lang coset contained in the curve is zero-dimensional.",
        "required", "required", None, 18,
    ),
    (
        "L-FINITE-INTERSECTION", "core_lemma", "critical",
        "Turn a finite union of zero-dimensional cosets into finiteness of the Abel-Jacobi image intersection.",
        "planned: finite_of_finite_zeroDimensional_cosets",
        "Finiteness of the Abel-Jacobi image of the curve points.",
        "required", "required", None, 10,
    ),
    (
        "T-TERMINAL", "terminal", "critical",
        "Compose finite-extension normalization, Abel-Jacobi construction, Mordell-Weil, Mordell-Lang, the no-positive-coset lemma, and finiteness transports.",
        "Stage1Instances.THMM0122.ObligationTree.terminal_of_normalization_abelJacobi_mordellLang",
        "The exact terminal FaltingsTarget proposition.",
        "required", "required", "repo:terminal_of_normalization_abelJacobi_mordellLang", 1,
    ),
    (
        "T-RANGE-TRANSPORT", "transport", "normal",
        "Transport finiteness from the range of an injective map back to its domain.",
        "Stage1Instances.THMM0122.ObligationTree.finite_of_injective_and_finite_range",
        "Finite alpha from an injective alpha-to-beta map with finite range.",
        "required", "not_applicable", "repo:finite_of_injective_and_finite_range", 4,
    ),
    (
        "X-IMPORTED-BOUNDARY", "bridge", "critical",
        "Resolve the missing terminal Faltings/Mordell-Lang body or a compatible immutable checked implementation, rather than crediting Northcott, descent, a statement-only dossier, or a by-sorry external declaration.",
        "anchor-audit.json candidate and negative-result boundary",
        "A placeholder-free exact imported body, or an explicit unresolved formalization boundary.",
        "required", "required", None, 1,
    ),
    (
        "X-SOURCE", "certificate", "critical",
        "Pinpoint and independently review the primary proof source, theorem locator, assumptions, conventions, errata, and source-to-node mapping.",
        "Faltings 1983 source crosswalk pending independent review",
        "Human-source coverage without machine-proof credit.",
        "not_applicable", "required", None, 12,
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Resolve every wrapper, terminal declaration, proof body, dependency, origin, revision, source byte, and license without alias duplication.",
        "planned transitive declaration and body provenance packet",
        "Body-level provenance without proof credit.",
        "informational", "not_applicable", None, 12,
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit terminal axioms, unsafe and oracle boundaries, compiled imports, Lean executable, and replay TCB.",
        "planned machine-derived trust and TCB report",
        "Release trust coverage without mathematical proof credit.",
        "informational", "not_applicable", None, 12,
    ),
    (
        "X-READABLE", "terminal", "high",
        "Provide an independently reviewed node-anchored reconstruction of the selected Faltings/Mordell-Lang route.",
        "obligation-tree.md plus future proof outline/process review",
        "Readable coverage without machine-proof credit.",
        "not_applicable", "required", None, 12,
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind proof, validation, source and readability review, freshness, revocation, independent verification, and release acceptance.",
        "Stage1 seven-phase workflow receipts pending",
        "Dependency-legal workflow and terminal decision inputs.",
        "informational", "not_applicable", None, 8,
    ),
)


def edge(edge_id: str, source: str, kind: str, target: str,
         reciprocal: str | None = None) -> dict:
    result = {"edge_id": edge_id, "from": source, "type": kind, "to": target}
    if reciprocal is not None:
        result["reciprocal_edge_id"] = reciprocal
    return result


def graph(edges: list[dict], endpoints: list[str]) -> dict:
    incoming = {identifier: [] for identifier in endpoints}
    outgoing = {identifier: [] for identifier in endpoints}
    for item in edges:
        outgoing[item["from"]].append(item["edge_id"])
        incoming[item["to"]].append(item["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


PROOF_CHILDREN = {
    oid("ROOT"): [oid("T-TERMINAL")],
    oid("T-TERMINAL"): [
        oid("N-FINITE-EXTENSION"), oid("C-ABEL-JACOBI"),
        oid("L-MORDELL-LANG"),
    ],
    oid("N-FINITE-EXTENSION"): [
        oid("N-EXTENSION-EXISTS"), oid("N-BASE-CHANGE"),
    ],
    oid("C-ABEL-JACOBI"): [
        oid("C-JACOBIAN"), oid("L-ABEL-JACOBI-INJECTIVE"),
    ],
    oid("L-FINITE-INTERSECTION"): [
        oid("L-MORDELL-LANG"), oid("L-NO-POSITIVE-COSET"),
    ],
}

# These edges refine aggregate Lean packages.  They are deliberately not
# direct proof children of T-TERMINAL: the checked terminal declaration has
# exactly the three package premises listed above.
REFINEMENT_CHILDREN = {
    oid("ROOT"): [
        ("logical_decomposition", oid("S-INTERFACE")),
        ("logical_decomposition", oid("S-BOUNDARY")),
        ("transports", oid("S-POINT-TRANSPORT")),
    ],
    oid("L-MORDELL-LANG"): [
        ("logical_decomposition", oid("L-MORDELL-WEIL")),
        ("logical_decomposition", oid("L-FINITE-INTERSECTION")),
        ("transports", oid("T-RANGE-TRANSPORT")),
        ("logical_decomposition", oid("X-IMPORTED-BOUNDARY")),
    ],
}

CHECKED_PARENTS = {
    oid("ROOT"): {
        "declaration": "Stage1Instances.THMM0122.ObligationTree.root_of_exactTerminal",
        "lean_child_ids": [oid("T-TERMINAL")],
    },
    oid("T-TERMINAL"): {
        "declaration": "Stage1Instances.THMM0122.ObligationTree.terminal_of_normalization_abelJacobi_mordellLang",
        "lean_child_ids": [
            oid("N-FINITE-EXTENSION"), oid("C-ABEL-JACOBI"),
            oid("L-MORDELL-LANG"),
        ],
    },
}


def ledger(identifier: str, claim: str, target: str, output: str,
           premises: list[str], outgoing: list[str]) -> dict:
    if premises:
        inference = f"conditional child-to-parent composition target: {target}"
    elif target.startswith("planned:"):
        inference = f"open proof plan requiring future source/Lean realization: {target}"
    elif "pending" in target or "audit" in target or "workflow" in target:
        inference = f"open review or evidence boundary: {target}"
    else:
        inference = f"checked target declaration or transport: {target}"
    return {
        "premises": premises or ["frozen-formal-context"],
        "inference": inference,
        "output": output,
        "outgoing_use": outgoing or ["typed support or terminal decision edge"],
        "steps": [{
            "step_id": f"{identifier}-STEP-01",
            "premise_ids": premises or ["frozen-formal-context"],
            "inference_or_source": inference,
            "exact_output": output,
            "outgoing_use_ids": outgoing or ["typed support or terminal decision edge"],
        }],
    }


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    row_by_id: dict[str, tuple] = {}
    exclusions = {
        oid("S-INTERFACE"): "formal_interface_source_coverage_inherited_from_root_pending_independent_review",
        oid("S-POINT-TRANSPORT"): "formal_encoding_transport_not_a_separate_human_proof_pending_independent_review",
        oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_mathematical_claim_pending_independent_review",
        oid("T-RANGE-TRANSPORT"): "generic_formal_finiteness_transport_not_a_source_proof_step_pending_independent_review",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_review",
        oid("X-PROVENANCE"): "provenance_overlay_no_independent_proof_credit_pending_integration_review",
        oid("X-TRUST"): "trust_overlay_no_independent_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_independent_proof_credit_pending_integration_review",
    }
    for row in ROWS:
        short, kind, risk, claim, target, output, machine, human, body, _budget = row
        identifier = oid(short)
        row_by_id[identifier] = row
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")} else
            "planned:v1:sha256:" + digest([identifier, kind, claim, target, output])
        )
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusions.get(identifier),
            "terminal_proof_body_id": body,
        })

    projection = [{field: item[field] for field in REGISTRY_FIELDS} for item in obligations]
    denominator = digest(projection)
    ids = [item["obligation_id"] for item in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0122-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-17T00:00:00+08:00",
        "freeze_basis": (
            "The exact statement-phase proposition, bounded anchor inventory, and selected "
            "finite-extension/Abel-Jacobi/Mordell-Lang route were frozen without assigning "
            "closure from candidate availability."
        ),
        "freeze_status_independent": True,
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "canonical_projection_fields": list(REGISTRY_FIELDS),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [
                item["obligation_id"] for item in obligations
                if item["machine_eligibility"] == "required"
            ],
            "required_human_source": [
                item["obligation_id"] for item in obligations
                if item["human_source_eligibility"] == "required"
            ],
            "required_readable": ids,
            "informational_overlays": [
                item["obligation_id"] for item in obligations
                if item["machine_eligibility"] == "informational"
            ],
        },
        "layer_applicability": {
            "S_statement_foundation": {"state": "required", "obligation_ids": [item for item in ids if "-S-" in item]},
            "N_normalization": {"state": "required", "obligation_ids": [item for item in ids if "-N-" in item]},
            "B_mathematical_branch": {
                "state": "not_applicable_pending_independent_approval",
                "obligation_ids": [],
                "reason": "The selected proof route has no exhaustive case split beyond the statement boundary exclusions; all material choices are construction or normalization obligations."
            },
            "C_construction": {"state": "required", "obligation_ids": [item for item in ids if "-C-" in item]},
            "L_core_lemma": {"state": "required", "obligation_ids": [item for item in ids if "-L-" in item]},
            "X_external_computation": {"state": "required", "obligation_ids": [item for item in ids if "-X-" in item]},
            "T_terminal": {"state": "required", "obligation_ids": [item for item in ids if "-T-" in item]},
        },
        "computation_exclusion": {
            "status": "not_applicable_pending_independent_approval",
            "reason": "No solver, reflection, numerical experiment, native computation, external oracle, or finite certificate is credited by this route."
        },
        "deduplication": {
            "same_claim_dossier": "THM-M-0395 inspected as a mismatched statement-only peer and receives no proof-body or obligation credit",
            "northcott_and_descent": "support interfaces only; neither is the Faltings terminal body",
            "atlas_faltings": "explicit by-sorry body; rejected and never assigned a terminal body identity",
            "accepted_terminal_body_ids": [],
        },
        "delta_policy": "Any target correction, split, merge, eligibility change, or exclusion requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "provisionally_checked_composition_interfaces": [
                CHECKED_PARENTS[parent]["declaration"] for parent in CHECKED_PARENTS
            ],
            "root_vector": {"H": "H1", "M": "M3", "R": "R3"},
            "root_closed": False,
        },
        "status_boundary": "The denominator is frozen and independent of observed closure. No obligation or terminal body is accepted; the root remains H1/M3/R3 and open.",
    }

    parents_of: dict[str, list[str]] = {identifier: [] for identifier in ids}
    for parent, children in PROOF_CHILDREN.items():
        for child in children:
            parents_of[child].append(parent)
    nodes = []
    for identifier in ids:
        short, kind, _risk, claim, target, output, _machine, _human, _body, _budget = row_by_id[identifier]
        premises = PROOF_CHILDREN.get(identifier, [])
        outgoing = parents_of[identifier]
        checked = identifier in {oid("ROOT"), oid("T-TERMINAL"), oid("T-RANGE-TRANSPORT"), oid("S-POINT-TRANSPORT")}
        machine_debt = "M3" if checked or identifier in {oid("S-INTERFACE"), oid("S-BOUNDARY")} else "M4"
        source_id = (
            "not-applicable-pending-review"
            if identifier in exclusions and row_by_id[identifier][7] == "not_applicable"
            else "faltings-1983-source-node-map-pending-independent-review"
        )
        provenance = (
            "local-conditional-composition"
            if identifier in {oid("ROOT"), oid("T-TERMINAL"), oid("T-RANGE-TRANSPORT")}
            else "local-checked-statement-transport"
            if identifier == oid("S-POINT-TRANSPORT") else "none"
        )
        owned_sources = []
        if identifier in {oid("ROOT"), oid("T-TERMINAL"), oid("N-FINITE-EXTENSION"), oid("C-ABEL-JACOBI"), oid("L-MORDELL-LANG"), oid("T-RANGE-TRANSPORT")}:
            owned_sources = [f"Stage1_Instances/{THEOREM}/ObligationTree.lean"]
        elif identifier in {oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-POINT-TRANSPORT")}:
            owned_sources = [f"Stage1_Instances/{THEOREM}/Statement.lean"]
        node_ledger = ledger(identifier, claim, target, output, premises, outgoing)
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
            "source_crosswalk_id": source_id,
            "provenance_id": provenance,
            "foundation_profile": "lean4-mathlib-classical/v1; terminal proof closure pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/v1; transitive release closure pending",
            "computation_record": "none credited; no solver, oracle, native evaluation, experiment, or unchecked certificate",
            "step_budget": _budget,
            "semantic_step_ledger": node_ledger,
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or conditional interface only; no accepted proof, H0, R0, audit completion, or theorem completion.",
            "task_ids": [ITEM],
            "owned_sources": owned_sources,
            "owner": "THM-M-0122 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-17" if checked else None,
                "review_due": "before proof acceptance and after any invalidation input changes",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "toolchain or dependency pins",
                ],
                "revocation_state": "provisional" if checked else "open",
            },
        })

    proof_edges: list[dict] = []
    reverse_types: dict[tuple[str, str], str] = {}
    for parent, children in PROOF_CHILDREN.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            reverse_kind = "composes" if parent in CHECKED_PARENTS else "logical_decomposition"
            rev_prefix = "CMP" if reverse_kind == "composes" else "DEC"
            rev = f"{rev_prefix}-{child}-{parent}"
            proof_edges.extend([
                edge(req, parent, "proof_requires", child, rev),
                edge(rev, child, reverse_kind, parent, req),
            ])
            reverse_types[(parent, child)] = reverse_kind

    refinement_edges = []
    for parent, children in REFINEMENT_CHILDREN.items():
        for kind, child in children:
            refinement_edges.append(edge(f"REF-{parent}-{child}", parent, kind, child))
    provenance_edges = []
    for identifier in ids:
        item = next(row for row in obligations if row["obligation_id"] == identifier)
        if identifier != oid("X-SOURCE") and item["human_source_eligibility"] == "required":
            provenance_edges.append(edge(f"SRC-{identifier}", identifier, "source_map", oid("X-SOURCE")))
    provenance_edges.extend([
        edge("PROV-TERMINAL", oid("X-PROVENANCE"), "provenance_of", oid("T-TERMINAL")),
        edge("PROV-IMPORTED", oid("X-PROVENANCE"), "provenance_of", oid("X-IMPORTED-BOUNDARY")),
    ])
    trust_edges = [
        edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
        edge("TRUST-TERMINAL", oid("T-TERMINAL"), "trusts", oid("X-TRUST")),
        edge("TRUST-IMPORTED", oid("X-IMPORTED-BOUNDARY"), "trusts", oid("X-TRUST")),
    ]
    documentation_edges = [
        edge("DOC-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
        edge("DOC-SOURCE", oid("X-SOURCE"), "documents", oid("T-TERMINAL")),
        edge("DOC-BOUNDARY", oid("S-BOUNDARY"), "documents", oid("ROOT")),
    ]
    workflow_task_nodes = [
        "S56-M-0122-INTAKE", "S56-M-0122-STATEMENT", "S56-M-0122-ANCHOR_AUDIT",
        ITEM, "S56-M-0122-PROOF", "S56-M-0122-VALIDATION", "S56-M-0122-RELEASE",
    ]
    workflow_edges = []
    for index in range(1, len(workflow_task_nodes)):
        current = workflow_task_nodes[index]
        predecessor = workflow_task_nodes[index - 1]
        workflow_edges.append(edge(f"FLOW-{index}", current, "workflow_depends_on", predecessor))

    graphs = {
        "proof": graph(proof_edges, ids),
        "refinement": graph(refinement_edges, ids),
        "provenance": graph(provenance_edges, ids),
        "evidence": graph([], ids),
        "trust": graph(trust_edges, ids),
        "documentation": graph(documentation_edges, ids),
        "workflow": graph(workflow_edges, workflow_task_nodes),
    }

    obligation_by_id = {row["obligation_id"]: row for row in obligations}
    certificates = []
    for parent, record in CHECKED_PARENTS.items():
        all_children = PROOF_CHILDREN[parent]
        certificates.append({
            "certificate_id": f"COMP-{parent}",
            "parent_obligation_id": parent,
            "parent_statement_fingerprint": obligation_by_id[parent]["statement_fingerprint"],
            "required_child_ids": all_children,
            "required_child_statement_fingerprints": {
                child: obligation_by_id[child]["statement_fingerprint"] for child in all_children
            },
            "lean_consumed_child_ids": record["lean_child_ids"],
            "architecture_support_child_ids": [
                child for child in all_children if child not in record["lean_child_ids"]
            ],
            "checked_declaration": record["declaration"],
            "certificate_kind": "lean_abstract_child_harness",
            "status": "provisionally_elaborated_not_accepted",
            "introduces_undeclared_premises": False,
            "accepted": False,
            "consumes_all_required_children": record["lean_child_ids"] == all_children,
            "yields_exact_parent": True,
            "no_undeclared_inputs": True,
            "boundary": (
                "The Lean declaration consumes exactly the named package premises. More detailed "
                "architecture children refine those packages and retain separate future composition checks."
            ),
        })

    plans = []
    for parent, children in PROOF_CHILDREN.items():
        if parent in CHECKED_PARENTS:
            continue
        plans.append({
            "plan_id": f"DECOMP-{parent}",
            "parent_obligation_id": parent,
            "planned_child_ids": children,
            "status": "architecture_decomposition_pending_exact_child_to_parent_certificate",
            "required_future_certificate": "Bind every planned child fingerprint in an exact consumer-owned Lean composition harness before proof closure.",
        })

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes or logical_decomposition is child-to-parent; support graphs confer no proof credit.",
        "edge_endpoint_namespace": "All non-workflow endpoints are canonical obligation IDs; workflow endpoints are stable phase item IDs.",
        "nodes": nodes,
        "graphs": graphs,
        "workflow_task_nodes": workflow_task_nodes,
        "composition_certificates": certificates,
        "unverified_decomposition_plans": plans,
        "evidence_endpoint_policy": "No evidence object is accepted in this phase, so the evidence graph remains empty rather than treating a workflow node or receipt as mathematical evidence.",
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "root_closed": False,
            "accepted_root_vector": {"H": "H1", "M": "M3", "R": "R3"},
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_machine_root_cut_set": [
                oid("N-FINITE-EXTENSION"), oid("C-ABEL-JACOBI"),
                oid("L-MORDELL-WEIL"), oid("L-MORDELL-LANG"),
                oid("L-NO-POSITIVE-COSET"), oid("L-FINITE-INTERSECTION"),
            ],
            "remaining_release_cut_set": [
                oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"),
                oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "reason": "Only the exact abstract package composition and generic range-finiteness transport are checked; every arithmetic-geometric premise and terminal body remains open.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [{
            "recipe_id": f"VAL-{identifier}",
            "cwd": ".",
            "argv": ["/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{
                "path_or_stream": "stdout",
                "semantic_hash_policy": "exactly one stage1-validator-semantic-result/1.0 JSON object",
            }],
            "covered_obligation_ids": [identifier],
            "covered_declarations": [
                record["declaration"] for parent, record in CHECKED_PARENTS.items()
                if parent == identifier
            ],
            "coverage_semantics": (
                "provisional_conditional_composition_and_architecture_validation"
                if identifier in CHECKED_PARENTS else "open_state_architecture_classification_only"
            ),
            "closure_credit": False,
        } for identifier in ids],
        "status_boundary": "These recipes validate the frozen architecture and conditional composition only; they do not close a proof obligation or provide release evidence.",
    }
    return registry, bundle, recipes


def render(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=True) + "\n"


def main() -> None:
    registry, bundle, recipes = build()
    for name, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", recipes),
    ):
        (HERE / name).write_text(render(value), encoding="utf-8")
    count = sum(len(item["edges"]) for item in bundle["graphs"].values())
    print(f"generated {len(registry['obligations'])} obligations and {count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
