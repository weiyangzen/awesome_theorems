#!/usr/bin/env python3
"""Build the frozen THM-M-0032 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0032-OBLIGATION_TREE"
THEOREM = "THM-M-0032"
PREFIX = "M0032-"
ROOT_EXPRESSION = "199d16d669438ea6e1cd556adbc4a9475805acf048379e01ae1a1f75f453a8d8"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# short id, kind, risk, claim, formal target, output, machine eligibility,
# human-source eligibility, terminal body, step budget
ROWS = (
    ("ROOT", "root", "critical",
     "Every commutative regular local ring is a unique factorization domain.",
     "Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget",
     "The exact frozen unrestricted regular-local-to-UFD proposition.",
     "required", "required", None, 10),
    ("S-INTERFACE", "definition", "critical",
     "Preserve the universe, CommRing and IsRegularLocalRing binders, and UniqueFactorizationMonoid conclusion.",
     "Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget",
     "The exact formal domain, antecedent, and conclusion.",
     "required", "not_applicable", None, 12),
    ("S-BOUNDARY", "branch", "high",
     "Exclude the zero ring through inherited Nontrivial while retaining fields, dimension zero, and arbitrary positive dimension.",
     "IsRegularLocalRing Rat; IsField Rat; zero-ring antecedent exclusion",
     "The exact degenerate and dimension boundary policy.",
     "required", "required", None, 18),
    ("S-ENCODING", "transport", "high",
     "Transport exactly between instance-bound and explicit regularity without adding an IsDomain premise.",
     "Stage1Instances.THM_M_0032.auslanderBuchsbaumUFDTarget_iff_explicitRegularityTarget",
     "A checked bidirectional regularity-binder transport.",
     "required", "not_applicable",
     "repo:Stage1Instances.THM_M_0032.auslanderBuchsbaumUFDTarget_iff_explicitRegularityTarget", 12),
    ("S-FOUNDATION", "certificate", "critical",
     "Audit the logical foundation, axioms, computation policy, imports, and trusted computing base.",
     "Lean 4.29.0 and pinned mathlib transitive trust closure",
     "A release-grade foundation and trust decision.",
     "required", "not_applicable", None, 36),
    ("N-DOMAIN", "reduction", "critical",
     "Derive IsDomain R from CommRing R and IsRegularLocalRing R without strengthening the root.",
     "Stage1Instances.THM_M_0032.ObligationTree.RegularLocalDomainPackage",
     "A domain instance usable by Kaplansky's criterion.",
     "required", "required", None, 100),
    ("A-PRIME-ELEMENT", "core_lemma", "critical",
     "Every nonzero prime ideal of a regular local domain contains a prime element.",
     "Stage1Instances.THM_M_0032.ObligationTree.RegularLocalPrimeElementPackage",
     "The theorem-specific premise of Kaplansky's criterion.",
     "required", "required", None, 24),
    ("C-MINIMAL-PRIME", "construction", "high",
     "For nonzero a in a prime ideal P, choose a prime Q minimal over (a) with Q contained in P.",
     "planned Lean signature over Ideal R and Ideal.minimalPrimes",
     "A minimal prime Q over a principal ideal, with Q <= P.",
     "required", "required", None, 70),
    ("L-PRINCIPAL-HEIGHT", "core_lemma", "high",
     "A prime minimal over a nonzero principal ideal has height at most one.",
     "Ideal.height_le_one_of_isPrincipal_of_mem_minimalPrimes plus nonzero side conditions",
     "The upper height bound for Q.",
     "required", "required", None, 45),
    ("L-MINIMAL-HEIGHT-ONE", "core_lemma", "high",
     "In a domain, that nonzero minimal prime has positive height and hence height exactly one.",
     "planned Lean height and domain bridge",
     "The equality Q.height = 1.",
     "required", "required", None, 55),
    ("L-HEIGHT-ONE-PRINCIPAL", "core_lemma", "critical",
     "Every height-one prime ideal of a regular local ring is principal.",
     "planned Lean signature; central arbitrary-dimension engine",
     "A principal generator for Q, not for every nonzero prime P.",
     "required", "required", None, 20),
    ("B-DIMENSION-INDUCTION", "branch", "critical",
     "Prove height-one principality by induction on the dimension of the regular local ring.",
     "planned well-founded dimension induction",
     "An exhaustive zero/positive-dimension induction package.",
     "required", "required", None, 30),
    ("B-DIM-ZERO", "branch", "high",
     "In dimension zero the regular local domain is a field, so no height-one prime exists.",
     "planned dimension-zero contradiction branch",
     "The base branch of dimension induction.",
     "required", "required", None, 45),
    ("B-DIM-POSITIVE", "branch", "critical",
     "In positive dimension, choose a regular parameter and split on membership in the height-one prime.",
     "planned positive-dimension branch",
     "The positive-dimensional induction branch.",
     "required", "required", None, 25),
    ("C-PARAMETER", "construction", "critical",
     "Choose x in the maximal ideal but outside its square.",
     "planned x : R with x in m and x notin m^2",
     "A regular parameter x.",
     "required", "required", None, 65),
    ("L-QUOTIENT-REGULAR", "core_lemma", "critical",
     "The quotient R/(x) by the regular parameter is regular local.",
     "planned quotient regularity theorem",
     "Regular-local structure on R/(x).",
     "required", "required", None, 90),
    ("L-QUOTIENT-DOMAIN", "core_lemma", "high",
     "The regular quotient R/(x) is a domain.",
     "planned use of the domain package on the quotient",
     "IsDomain (R/(x)).",
     "required", "required", None, 30),
    ("L-PARAMETER-PRIME", "core_lemma", "high",
     "The quotient-domain result makes x a prime element and (x) a prime ideal.",
     "Ideal.span_singleton_prime and quotient-domain bridge",
     "Primality of x and its principal ideal.",
     "required", "required", None, 55),
    ("B-PRIME-CONTAINS", "branch", "high",
     "If x belongs to the height-one prime P, height one forces P = (x).",
     "planned height-one equality branch",
     "Principality of P in the contains-x branch.",
     "required", "required", None, 45),
    ("B-PRIME-AVOIDS", "branch", "critical",
     "If x is not in P, principalize P after localization and descend a prime generator to R.",
     "planned localization and descent branch",
     "Principality of P in the avoids-x branch.",
     "required", "required", None, 20),
    ("L-LOCALIZATION-REGULAR", "core_lemma", "critical",
     "Every nonmaximal prime localization of R is regular local.",
     "planned localization regularity theorem",
     "Regular-local structure at each relevant localization.",
     "required", "required", None, 70),
    ("L-DIMENSION-DROP", "core_lemma", "critical",
     "Those nonmaximal localizations have smaller dimension and satisfy the induction hypothesis.",
     "planned dimension drop and induction application",
     "Local principality of the localized height-one ideal.",
     "required", "required", None, 80),
    ("C-LOCALIZED-IDEAL", "construction", "high",
     "Form P localized in R_x and prove it is finitely presented and locally free of rank one.",
     "planned localized ideal module package",
     "A rank-one locally free R_x-module.",
     "required", "required", None, 85),
    ("L-INVERTIBLE", "core_lemma", "high",
     "Convert finite presentation and local rank one into invertibility of P_x.",
     "planned invertible-module criterion",
     "P_x as an invertible R_x-module.",
     "required", "required", None, 55),
    ("L-TRIVIALIZATION", "core_lemma", "critical",
     "Trivialize the invertible ideal over R_x and choose a generator y.",
     "Stacks tag 0AFZ route; planned Lean signature",
     "An element y generating P_x.",
     "required", "required", None, 100),
    ("C-CLEAR-DENOMINATOR", "construction", "high",
     "Write y as x^e f with f in P after clearing localization denominators.",
     "planned localization denominator construction",
     "An element f in P representing the localized generator up to a power of x.",
     "required", "required", None, 65),
    ("L-ATOMIC-FACTORIZATION", "core_lemma", "high",
     "Factor f into irreducibles and select a factor a in the prime ideal P.",
     "planned Noetherian-domain atomic factorization",
     "An irreducible factor a in P whose image divides y.",
     "required", "required", None, 65),
    ("L-LIFT-PRIMALITY", "core_lemma", "critical",
     "Lift primality of the image of a from R_x to R using primality of x.",
     "planned localization primality lift",
     "Prime a in R.",
     "required", "required", None, 80),
    ("T-HEIGHT-ONE", "terminal", "critical",
     "Recompose both parameter-membership branches into height-one-prime principality.",
     "planned checked composition declaration",
     "Every height-one prime of R is principal.",
     "required", "required", None, 30),
    ("T-PRIME-GENERATOR", "terminal", "critical",
     "Extract a prime generator of Q and place it in the original nonzero prime P.",
     "planned use of Ideal.span_singleton_prime and Q <= P",
     "A prime element belonging to P.",
     "required", "required", None, 55),
    ("X-KAPLANSKY", "bridge", "critical",
     "Apply the pinned Kaplansky criterion after the domain and prime-element packages are supplied.",
     "Stage1Instances.THM_M_0032.ObligationTree.pinnedKaplanskyCriterionPackage",
     "UniqueFactorizationMonoid R from the exact nonzero-prime premise.",
     "required", "not_applicable",
     "mathlib:UniqueFactorizationMonoid.iff_exists_prime_mem_of_isPrime", 18),
    ("T-ASSEMBLE", "terminal", "critical",
     "Install the derived domain instance and consume domain, prime-element, and Kaplansky packages to obtain the exact root.",
     "Stage1Instances.THM_M_0032.ObligationTree.root_of_domain_primeElement_and_kaplansky",
     "The exact frozen AuslanderBuchsbaumUFDTarget, conditional on all proof children.",
     "required", "required",
     "repo:Stage1Instances.THM_M_0032.ObligationTree.root_of_domain_primeElement_and_kaplansky", 18),
    ("X-PRIMARY-SOURCE", "source_boundary", "high",
     "Map the PNAS propositions, dimension-three result, Nagata reduction, Theorem 5, definitions, dates, and errata.",
     "Auslander-Buchsbaum PNAS 45(5), pages 733-734",
     "Primary-source coverage without machine proof credit.",
     "not_applicable", "required", None, 70),
    ("X-MODERN-SOURCE", "source_boundary", "high",
     "Map every transition of the modern dimension-induction route and its cited dependencies.",
     "Stacks Project tag 0AG0 and dependencies",
     "Modern route coverage without primary-source substitution.",
     "not_applicable", "required", None, 80),
    ("X-PROVENANCE", "certificate", "critical",
     "Audit wrappers, terminal bodies, aliases, source blobs, dependencies, revisions, and licenses.",
     "terminal declaration and proof-body provenance packets pending",
     "Body-level provenance without duplicate proof credit.",
     "informational", "not_applicable", None, 45),
    ("X-TRUST", "certificate", "critical",
     "Audit Lean, mathlib, axioms, artifacts, unsafe/oracle boundaries, replay, and supply-chain trust transitively.",
     "Lean 4.29.0 and mathlib 8a178386 transitive closure pending",
     "Release-grade trust evidence without mathematical proof credit.",
     "informational", "not_applicable", None, 45),
    ("X-READABLE", "documentation", "high",
     "Produce and independently review the complete node-by-node mathematical reconstruction.",
     "proof outline, process appendix, and independent reader receipt pending",
     "Readable coverage without machine proof credit.",
     "not_applicable", "required", None, 80),
    ("X-WORKFLOW", "workflow", "critical",
     "Bind proof, validation, source, readability, freshness, revocation, independent verification, and release tasks.",
     "Stage1 task and receipt closure pending",
     "Workflow acceptance without mathematical proof credit.",
     "informational", "not_applicable", None, 32),
)


CHECKED_LOCAL = {oid("S-ENCODING"), oid("T-ASSEMBLE")}
CHECKED_LIBRARY = {oid("X-KAPLANSKY")}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []

    for short, kind, risk, claim, target, output, machine, human, body, budget in ROWS:
        identifier = oid(short)
        if short in {"ROOT", "S-INTERFACE"}:
            fingerprint = f"lean-expression-sha256:{ROOT_EXPRESSION}"
        else:
            fingerprint = "planned:v1:sha256:" + digest([identifier, kind, claim, target, output])
        reasons = []
        if machine != "required":
            reasons.append("no_machine_proof_credit")
        if human != "required":
            reasons.append("not_a_distinct_human_mathematical_claim")
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": "_and_".join(reasons) + "_pending_independent_approval" if reasons else None,
            "terminal_proof_body_id": body,
        })
        if identifier in CHECKED_LOCAL:
            machine_debt = "M0-L"
        elif identifier in CHECKED_LIBRARY:
            machine_debt = "M0-W"
        elif short == "ROOT":
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        if identifier == oid("X-KAPLANSKY"):
            provenance = "anchor-audit:M0032-C01-MATHLIB-SUPPORT"
        elif identifier in CHECKED_LOCAL:
            provenance = "repo-local-checked-interface"
        elif short.startswith("X-"):
            provenance = "support-boundary-pending"
        else:
            provenance = "none"
        owned_sources = []
        if identifier in {oid("X-KAPLANSKY"), oid("T-ASSEMBLE")}:
            owned_sources = ["Stage1_Instances/THM-M-0032/ObligationTree.lean"]
        elif identifier == oid("S-ENCODING"):
            owned_sources = ["Stage1_Instances/THM-M-0032/Statement.lean"]
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": kind,
            "human_statement": claim,
            "formal_target": target,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "not-applicable-pending-review" if human != "required"
                else "primary-and-modern-node-map-pending"
            ),
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; accepted transitive axiom policy pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
            "computation_record": "none; no solver, oracle, experiment, native shortcut, or unchecked certificate is credited",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": "The exact formal context and only conclusions named by incoming proof_requires edges.",
                "inference": target,
                "output": output,
                "outgoing_use": "Only a declared proof parent or typed non-proof support edge may consume this output.",
            },
            "public_readable_target": f"Stage1_Instances/THM-M-0032/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or conditional interface only; no accepted root proof, H0, R0, or theorem completion.",
            "task_ids": [ITEM, "S56-M-0032-PROOF", "S56-M-0032-VALIDATION"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0032 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_LOCAL | CHECKED_LIBRARY else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "toolchain and dependency pins",
                ],
                "revocation_state": "provisional" if identifier in CHECKED_LOCAL | CHECKED_LIBRARY else "open",
            },
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
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0032-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "The exact frozen statement, immutable anchor audit, primary proof-node leads, and modern Kaplansky/dimension-induction route. Eligibility and denominators are fixed independently of proof availability.",
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
            "symmetry_and_order_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The ring-theoretic target has no symmetry, sign, ordering, or representative normalization; domain derivation is retained explicitly.",
            },
            "computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No finite computation, reflection, solver, numerical approximation, oracle, or certificate occurs in either frozen proof route.",
            },
        },
        "rejected_architecture_aliases": {
            "all_nonzero_primes_principal": "rejected_as_too_strong_in_dimension_greater_than_one",
            "dimension_at_most_three_only": "rejected_as_a_strict_weakening_of_the_unrestricted_root",
            "explicit_IsDomain_root": "rejected_as_an_unchecked_strengthening_of_the_antecedent",
        },
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_LOCAL),
            "library_bridge_obligation": oid("X-KAPLANSKY"),
            "library_bridge_classification": "M0-W_interface_pending_proof_phase_and_master_acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope, semantic expansion, and denominators only. The two theorem-specific engines are open; H0, R0, audit completion, validation, release, and theorem completion remain false.",
    }

    def edge(edge_id: str, source: str, edge_type: str, target: str, reciprocal: str | None = None) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        return value

    requires = {
        oid("ROOT"): [oid("T-ASSEMBLE")],
        oid("T-ASSEMBLE"): [oid("N-DOMAIN"), oid("A-PRIME-ELEMENT"), oid("X-KAPLANSKY")],
        oid("A-PRIME-ELEMENT"): [oid("T-PRIME-GENERATOR")],
        oid("T-PRIME-GENERATOR"): [
            oid("C-MINIMAL-PRIME"), oid("L-PRINCIPAL-HEIGHT"),
            oid("L-MINIMAL-HEIGHT-ONE"), oid("L-HEIGHT-ONE-PRINCIPAL"),
        ],
        oid("L-HEIGHT-ONE-PRINCIPAL"): [oid("T-HEIGHT-ONE")],
        oid("T-HEIGHT-ONE"): [oid("B-DIMENSION-INDUCTION")],
        oid("B-DIMENSION-INDUCTION"): [oid("B-DIM-ZERO"), oid("B-DIM-POSITIVE")],
        oid("B-DIM-POSITIVE"): [
            oid("C-PARAMETER"), oid("L-QUOTIENT-REGULAR"), oid("L-QUOTIENT-DOMAIN"),
            oid("L-PARAMETER-PRIME"), oid("B-PRIME-CONTAINS"), oid("B-PRIME-AVOIDS"),
        ],
        oid("B-PRIME-AVOIDS"): [
            oid("L-LOCALIZATION-REGULAR"), oid("L-DIMENSION-DROP"),
            oid("C-LOCALIZED-IDEAL"), oid("L-INVERTIBLE"), oid("L-TRIVIALIZATION"),
            oid("C-CLEAR-DENOMINATOR"), oid("L-ATOMIC-FACTORIZATION"), oid("L-LIFT-PRIMALITY"),
        ],
    }
    proof: list[dict] = []
    for parent, children in requires.items():
        for child in children:
            requirement = f"REQ-{parent}-{child}"
            composition = f"CMP-{child}-{parent}"
            proof.extend([
                edge(requirement, parent, "proof_requires", child, composition),
                edge(composition, child, "composes", parent, requirement),
            ])

    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "equivalent_to", oid("S-INTERFACE")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY")),
            edge("REF-ROOT-ENCODING", oid("ROOT"), "transports", oid("S-ENCODING")),
            edge("REF-PRIME-MINIMAL", oid("A-PRIME-ELEMENT"), "expository_decomposition", oid("C-MINIMAL-PRIME")),
            edge("REF-HEIGHT-INDUCTION", oid("L-HEIGHT-ONE-PRINCIPAL"), "expository_decomposition", oid("B-DIMENSION-INDUCTION")),
        ],
        "provenance": [
            edge("PROV-KAPLANSKY", oid("X-PROVENANCE"), "provenance_of", oid("X-KAPLANSKY")),
            edge("PROV-COMPOSITION", oid("X-PROVENANCE"), "provenance_of", oid("T-ASSEMBLE")),
            edge("SRC-PRIMARY-ROOT", oid("X-PRIMARY-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-PRIMARY-HEIGHT", oid("X-PRIMARY-SOURCE"), "source_map", oid("L-HEIGHT-ONE-PRINCIPAL")),
            edge("SRC-MODERN-HEIGHT", oid("X-MODERN-SOURCE"), "source_map", oid("L-HEIGHT-ONE-PRINCIPAL")),
            edge("SRC-MODERN-LOCAL", oid("X-MODERN-SOURCE"), "source_map", oid("B-PRIME-AVOIDS")),
        ],
        "evidence": [
            edge("EVID-PROVENANCE-KAPLANSKY", oid("X-PROVENANCE"), "evidence_for", oid("X-KAPLANSKY")),
            edge("EVID-WORKFLOW-ROOT", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-KAPLANSKY-CLOSURE", oid("X-KAPLANSKY"), "trusts", oid("X-TRUST")),
            edge("TRUST-COMPOSITION-CLOSURE", oid("T-ASSEMBLE"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-PRIME", oid("X-READABLE"), "documents", oid("A-PRIME-ELEMENT")),
            edge("DOC-READABLE-HEIGHT", oid("X-READABLE"), "documents", oid("L-HEIGHT-ONE-PRINCIPAL")),
            edge("DOC-PRIMARY-ROOT", oid("X-PRIMARY-SOURCE"), "documents", oid("ROOT")),
            edge("DOC-MODERN-HEIGHT", oid("X-MODERN-SOURCE"), "documents", oid("L-HEIGHT-ONE-PRINCIPAL")),
        ],
        "workflow": [
            edge("FLOW-PROOF-DOMAIN", oid("X-WORKFLOW"), "workflow_depends_on", oid("N-DOMAIN")),
            edge("FLOW-PROOF-PRIME", oid("X-WORKFLOW"), "workflow_depends_on", oid("A-PRIME-ELEMENT")),
            edge("FLOW-PROVENANCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-PRIMARY", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PRIMARY-SOURCE")),
            edge("FLOW-MODERN", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-MODERN-SOURCE")),
            edge("FLOW-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
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
        "registry_id": "THM-M-0032-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_LOCAL | CHECKED_LIBRARY),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [
                oid("N-DOMAIN"), oid("A-PRIME-ELEMENT"), oid("X-PRIMARY-SOURCE"),
                oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"),
                oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "composition_certificates": [
                "Stage1Instances.THM_M_0032.ObligationTree.pinnedKaplanskyCriterionPackage",
                "Stage1Instances.THM_M_0032.ObligationTree.root_of_domain_primeElement_and_kaplansky",
            ],
            "reason": "The exact root composition is conditional. The domain and prime-element engines remain open and no obligation has accepted proof state.",
        },
    }

    recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
    declaration_map = {
        oid("ROOT"): ["Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget"],
        oid("S-ENCODING"): ["Stage1Instances.THM_M_0032.auslanderBuchsbaumUFDTarget_iff_explicitRegularityTarget"],
        oid("N-DOMAIN"): ["Stage1Instances.THM_M_0032.ObligationTree.RegularLocalDomainPackage"],
        oid("A-PRIME-ELEMENT"): ["Stage1Instances.THM_M_0032.ObligationTree.RegularLocalPrimeElementPackage"],
        oid("X-KAPLANSKY"): ["Stage1Instances.THM_M_0032.ObligationTree.pinnedKaplanskyCriterionPackage"],
        oid("T-ASSEMBLE"): ["Stage1Instances.THM_M_0032.ObligationTree.root_of_domain_primeElement_and_kaplansky"],
    }
    for identifier in ids:
        recipes["recipes"].append({
            "recipe_id": f"VAL-{identifier}",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0032/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0032 obligation tree"}],
            "covered_obligation_ids": [identifier],
            "covered_declarations": declaration_map.get(identifier, []),
        })
    return registry, bundle, recipes


def main() -> None:
    values = build()
    for name, value in zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), values):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    edge_count = sum(len(graph["edges"]) for graph in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {values[0]['denominator_sha256']}")


if __name__ == "__main__":
    main()
