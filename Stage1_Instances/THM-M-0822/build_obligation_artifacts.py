#!/usr/bin/env python3
"""Build the frozen THM-M-0822 obligation registry and typed graphs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0822-OBLIGATION_TREE"
THEOREM = "THM-M-0822"
PREFIX = "M0822-"
ROOT_EXPRESSION = "646e9860afcf5efd962b6f69c9c2825220f23418d05f7675490b783e63afe209"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_BLOB = "f388fc0bfd201e1d9eb1279b5bd1c6dcbd253b34"
MATHLIB_TERMINAL_BODY = (
    f"mathlib4@{MATHLIB_REVISION}:{MATHLIB_BLOB}#Finset.erdos_ko_rado"
)
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
)
TASK_IDS = (
    "S56-M-0822-INTAKE",
    "S56-M-0822-STATEMENT",
    "S56-M-0822-ANCHOR_AUDIT",
    ITEM,
    "S56-M-0822-PROOF",
    "S56-M-0822-VALIDATION",
    "S56-M-0822-RELEASE",
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


# short ID, kind, risk, human claim, formal target, output, machine eligibility,
# human-source eligibility, terminal body, inference, source locator
ROWS = (
    (
        "ROOT", "root", "critical",
        "For every positive r at most n/2, an intersecting r-uniform family on Fin n attains choose(n-1,r-1), and every such family has at most that size.",
        "Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget",
        "The exact frozen maximum-value proposition.",
        "required", "required", None,
        "Consume the exact terminal assembly without changing binders, range, or conclusion.",
        "Stage1_Instances/THM-M-0822/ObligationTree.lean#rootOfExactAssembly",
    ),
    (
        "S-TARGET", "definition", "critical",
        "Freeze Nat parameters, Fin n, finite families of finite subsets, positive rank, the inclusive n/2 boundary, attainment, and the universal bound.",
        "Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget",
        "The exact statement interface and expression fingerprint.",
        "informational", "not_applicable", None,
        "Preserve the elaborated expression and its checked concrete-star alternate without importing proof credit.",
        "Stage1_Instances/THM-M-0822/statement.json",
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Exclude r=0 and the inadmissible n=0,1 cases, retain r=1 and r=n/2, and make no equality-family classification.",
        "no_admissible_rank_fin_zero; no_admissible_rank_fin_one; star_attains_equality_boundary",
        "The complete parameter and extremal-scope boundary.",
        "informational", "required", None,
        "Use the statement fixtures to separate admissible parameters from excluded or stronger variants.",
        "Stage1_Instances/THM-M-0822/Statement.lean:135",
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Audit Lean, classical choice, quotient soundness, propositional extensionality, and the no-oracle computation policy.",
        "Lean 4.29.0 foundation and transitive axiom report",
        "An accepted foundation, computation, and TCB boundary.",
        "informational", "not_applicable", None,
        "Compare machine-derived declarations, axioms, artifacts, and executables with the selected profiles.",
        "Stage1_Instances/THM-M-0822/anchor-audit.json",
    ),
    (
        "T-ASSEMBLE", "terminal", "critical",
        "Recompose the complete maximum theorem from its attaining-family and universal-bound conjuncts.",
        "Stage1Instances.THM_M_0822.ObligationTree.composeRoot",
        "The exact canonical target, conditional on both children.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0822/ObligationTree.lean#composeRoot",
        "Apply the abstract-child composition harness, consuming both packages.",
        "Stage1_Instances/THM-M-0822/ObligationTree.lean#composeRoot",
    ),
    (
        "T-ATTAINMENT", "terminal", "critical",
        "Provide an intersecting r-uniform family of cardinality choose(n-1,r-1) throughout the admissible range.",
        "Stage1Instances.THM_M_0822.ObligationTree.AttainmentPackage",
        "The complete existential conjunct.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0822/ObligationTree.lean#attainment_of_starPackages",
        "Select a ground element, construct its star, and combine intersection, uniformity, and cardinality facts.",
        "Stage1_Instances/THM-M-0822/Statement.lean:97",
    ),
    (
        "C-STAR", "construction", "high",
        "For every admissible n and r, select a center in Fin n and construct its canonical star.",
        "Stage1Instances.THM_M_0822.ObligationTree.StarConstructionPackage",
        "A center and finite canonical star for the admissible parameters.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0822/ObligationTree.lean#starConstruction_of_groundElement",
        "Consume the ground-element package, choose its center, and return the corresponding filtered r-slice.",
        "Stage1_Instances/THM-M-0822/ObligationTree.lean#starConstruction_of_groundElement",
    ),
    (
        "L-STAR-IMAGE", "core_lemma", "high",
        "Identify the star with insertion of x into every (r-1)-subset avoiding x.",
        "Stage1Instances.THM_M_0822.ObligationTree.StarImagePackage",
        "A bijective image representation used for cardinality.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0822/Statement.lean#erdosKoRadoStar_eq_image",
        "Erase x in one direction and insert x in the other, using positive rank for the card equation.",
        "Stage1_Instances/THM-M-0822/Statement.lean:38",
    ),
    (
        "L-STAR-INTERSECTING", "core_lemma", "normal",
        "Show that any two members of a fixed-center star meet at the center.",
        "Stage1Instances.THM_M_0822.ObligationTree.StarIntersectingPackage",
        "Set.Intersecting for the constructed star.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0822/Statement.lean#erdosKoRadoStar_intersecting",
        "Contradict disjointness using membership of the shared center in both members.",
        "Stage1_Instances/THM-M-0822/Statement.lean:54",
    ),
    (
        "L-STAR-SIZED", "core_lemma", "normal",
        "Show every member of the star has cardinality r.",
        "Stage1Instances.THM_M_0822.ObligationTree.StarSizedPackage",
        "Set.Sized r for the constructed star.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0822/Statement.lean#erdosKoRadoStar_sized",
        "Project the powersetCard membership cardinality equation.",
        "Stage1_Instances/THM-M-0822/Statement.lean:62",
    ),
    (
        "L-STAR-CARD", "core_lemma", "critical",
        "Compute the positive-rank star cardinality as choose(n-1,r-1).",
        "Stage1Instances.THM_M_0822.ObligationTree.StarCardPackage",
        "The sharp cardinality equality.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0822/ObligationTree.lean#starCard_of_image",
        "Consume the image package, prove insertion is injective away from x, and apply powersetCard cardinality.",
        "Stage1_Instances/THM-M-0822/ObligationTree.lean#starCard_of_image",
    ),
    (
        "L-GROUND-ELEMENT", "construction", "high",
        "Derive n>0 from 1<=r<=n/2 and select a center x : Fin n.",
        "Stage1Instances.THM_M_0822.ObligationTree.GroundElementPackage",
        "A ground element for the attaining star.",
        "required", "required", None,
        "Use positivity of n/2 and Nat.pos_of_div_pos to construct x with value zero.",
        "Stage1_Instances/THM-M-0822/Statement.lean:104",
    ),
    (
        "T-UPPER-ADAPTER", "transport", "critical",
        "Transport the pinned terminal binder order into the target's positive-range universal-bound package.",
        "Stage1Instances.THM_M_0822.ObligationTree.upperBound_of_mathlibTerminal",
        "The complete universal-bound conjunct.",
        "required", "required",
        "local:Stage1_Instances/THM-M-0822/ObligationTree.lean#upperBound_of_mathlibTerminal",
        "Instantiate the terminal with n, r, A, intersection, sizing, and hhalf; the positive premise remains intentionally unused.",
        "Stage1_Instances/THM-M-0822/ObligationTree.lean#upperBound_of_mathlibTerminal",
    ),
    (
        "T-MATHLIB-EKR", "bridge", "critical",
        "Every intersecting r-uniform family on Fin n with r<=n/2 has cardinality at most choose(n-1,r-1).",
        "Finset.erdos_ko_rado",
        "The exact pinned upper-bound terminal interface.",
        "required", "required", MATHLIB_TERMINAL_BODY,
        "Invoke the immutable pinned terminal; keep the substantive source-body route explicit as non-credit overlays.",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SetFamily/KruskalKatona.lean:343",
    ),
    (
        "B-RZERO", "branch", "high",
        "Handle r=0 by showing an intersecting sized family is empty.",
        "r=0 branch in Finset.erdos_ko_rado",
        "The upper bound in the zero-rank branch.",
        "informational", "required", MATHLIB_TERMINAL_BODY,
        "Split r=0 from positive r, use self-intersection to rule out the empty set as a family member.",
        "KruskalKatona.lean:351",
    ),
    (
        "C-COMPLEMENTS", "construction", "critical",
        "Construct the complement family and its (n-2r)-fold iterated shadow.",
        "Finset.compls and Finset.shadow iteration in Finset.erdos_ko_rado",
        "The comparison family used in the positive-rank contradiction.",
        "informational", "required", MATHLIB_TERMINAL_BODY,
        "Take set complements of every family member and iterate the shadow to return to rank r.",
        "KruskalKatona.lean:359",
    ),
    (
        "L-SHADOW-DISJOINT", "core_lemma", "critical",
        "Show the original family is disjoint from the iterated shadow of its complement family.",
        "the Disjoint claim in Finset.erdos_ko_rado",
        "A disjoint union whose cardinality is bounded by the r-slice.",
        "informational", "required", MATHLIB_TERMINAL_BODY,
        "An overlap would put one family member inside the complement of another and contradict intersection.",
        "KruskalKatona.lean:361",
    ),
    (
        "L-COMPLEMENT-CARD", "core_lemma", "high",
        "Transfer the assumed excessive cardinality to the complement family in the symmetric binomial form.",
        "Finset.card_compls and Nat.choose symmetry",
        "choose(n-1,n-r) < card(complements A).",
        "informational", "required", MATHLIB_TERMINAL_BODY,
        "Use complement-card preservation and binomial symmetry under r<=n and r>0.",
        "KruskalKatona.lean:367",
    ),
    (
        "L-COMPLEMENT-SIZED", "core_lemma", "high",
        "Show complements of an r-uniform family are (n-r)-uniform.",
        "Set.Sized.compls",
        "Set.Sized (n-r) for the complement family.",
        "informational", "required", MATHLIB_TERMINAL_BODY,
        "Apply the sized-complement transport to the original family.",
        "KruskalKatona.lean:370",
    ),
    (
        "L-KK-LOVASZ", "bridge", "critical",
        "Lower-bound the relevant iterated shadow by choose(n-1,r).",
        "Finset.kruskal_katona_lovasz_form",
        "choose(n-1,r) <= card(iterated shadow of complements).",
        "informational", "required",
        f"mathlib4@{MATHLIB_REVISION}:{MATHLIB_BLOB}#Finset.kruskal_katona_lovasz_form",
        "Instantiate the Lovasz Kruskal-Katona form at i=n-2r, rank n-r, and k=n-1.",
        "KruskalKatona.lean:372",
    ),
    (
        "L-BINOMIAL-CONTRADICTION", "core_lemma", "critical",
        "Combine the allegedly oversized family and shadow lower bound to exceed choose(n,r).",
        "Nat.choose_succ_succ and Finset.card_union_of_disjoint",
        "choose(n,r) < card(A union iterated shadow).",
        "informational", "required", MATHLIB_TERMINAL_BODY,
        "Apply the binomial recurrence and add the strict and weak cardinal inequalities.",
        "KruskalKatona.lean:377",
    ),
    (
        "L-SLICE-CARD", "core_lemma", "critical",
        "Bound every r-uniform family in Fin n by choose(n,r).",
        "Set.Sized.card_le",
        "card(A union iterated shadow) <= choose(n,r).",
        "informational", "required", MATHLIB_TERMINAL_BODY,
        "Prove the disjoint union remains r-uniform and apply the finite slice cardinality bound.",
        "KruskalKatona.lean:383",
    ),
    (
        "X-SOURCE", "terminal", "critical",
        "Pinpoint and independently review the original EKR theorem, star sharpness argument, assumptions, proof transitions, and errata.",
        "1961 paper node-specific source packet pending",
        "Human-source coverage without machine proof credit.",
        "not_applicable", "required", None,
        "Map every material premise and inference to the primary paper and a reviewed modern transport.",
        "Stage1_Instances/THM-M-0822/source-statement-crosswalk.md",
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Bind local wrappers, the target-owned star bodies, pinned terminal, internal imports, source blobs, aliases, and licenses.",
        "content-addressed declaration and terminal-body provenance closure",
        "Release-grade provenance without proof credit.",
        "informational", "not_applicable", None,
        "Deduplicate wrappers while tracing both actual terminal bodies and their transitive dependencies.",
        "Stage1_Instances/THM-M-0822/anchor-audit.json",
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit toolchain, compiled artifacts, axioms, unsafe/oracle boundaries, replay, and supply-chain trust transitively.",
        "Lean 4.29.0 and mathlib 8a178386 transitive trust closure",
        "Release trust evidence without proof credit.",
        "informational", "not_applicable", None,
        "Recompute declaration, artifact, executable, axiom, no-placeholder, and no-oracle closure hermetically.",
        "Stage1_Instances/THM-M-0822/anchor-audit.json",
    ),
    (
        "X-READABLE", "terminal", "high",
        "Provide a complete independently reviewed reconstruction of both the star and Kruskal-Katona upper-bound routes.",
        "node-specific readable reconstruction and independent review pending",
        "Readable coverage without machine proof credit.",
        "not_applicable", "not_applicable", None,
        "Expand each high-risk bridge into a complete premise-to-output mathematical ledger.",
        "Stage1_Instances/THM-M-0822/obligation-tree.md",
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind dependency-legal proof adoption, validation, release, freshness, revocation, and independent verification.",
        "Stage1 rev-5.6 task and receipt workflow",
        "Workflow acceptance without proof credit.",
        "informational", "not_applicable", None,
        "Require accepted predecessors and node receipts before any downstream state transition.",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
    ),
)


REQUIRES = {
    oid("ROOT"): [oid("T-ASSEMBLE")],
    oid("T-ASSEMBLE"): [oid("T-ATTAINMENT"), oid("T-UPPER-ADAPTER")],
    oid("T-ATTAINMENT"): [
        oid("C-STAR"), oid("L-STAR-INTERSECTING"),
        oid("L-STAR-SIZED"), oid("L-STAR-CARD"),
    ],
    oid("C-STAR"): [oid("L-GROUND-ELEMENT")],
    oid("L-STAR-CARD"): [oid("L-STAR-IMAGE")],
    oid("T-UPPER-ADAPTER"): [oid("T-MATHLIB-EKR")],
}

CERTIFICATES = {
    oid("ROOT"): "Stage1Instances.THM_M_0822.ObligationTree.rootOfExactAssembly",
    oid("T-ASSEMBLE"): "Stage1Instances.THM_M_0822.ObligationTree.composeRoot",
    oid("T-ATTAINMENT"): "Stage1Instances.THM_M_0822.ObligationTree.attainment_of_starPackages",
    oid("C-STAR"): "Stage1Instances.THM_M_0822.ObligationTree.starConstruction_of_groundElement",
    oid("L-STAR-CARD"): "Stage1Instances.THM_M_0822.ObligationTree.starCard_of_image",
    oid("T-UPPER-ADAPTER"): "Stage1Instances.THM_M_0822.ObligationTree.upperBound_of_mathlibTerminal",
}

INTERNAL_OVERLAYS = (
    "B-RZERO", "C-COMPLEMENTS", "L-SHADOW-DISJOINT", "L-COMPLEMENT-CARD",
    "L-COMPLEMENT-SIZED", "L-KK-LOVASZ", "L-BINOMIAL-CONTRADICTION",
    "L-SLICE-CARD",
)


def edge(edge_id: str, source: str, edge_type: str, target: str,
         reciprocal: str | None = None) -> dict:
    value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal is not None:
        value["reciprocal_edge_id"] = reciprocal
    return value


def graph(edges: list[dict]) -> dict:
    outgoing: dict[str, list[str]] = {}
    incoming: dict[str, list[str]] = {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []
    exclusions = {
        oid("S-TARGET"): "statement_overlay_no_independent_machine_credit_pending_independent_approval",
        oid("S-BOUNDARY"): "boundary_overlay_no_independent_machine_credit_pending_independent_approval",
        oid("S-FOUNDATION"): "foundation_overlay_no_proof_credit_pending_independent_approval",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-PROVENANCE"): "provenance_overlay_no_proof_credit_pending_integration_review",
        oid("X-TRUST"): "trust_overlay_no_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
    }
    for short in INTERNAL_OVERLAYS:
        exclusions[oid(short)] = (
            "imported_source_body_overlay_no_independent_machine_credit_pending_"
            "child_signature_and_composition_review"
        )

    parent_of: dict[str, list[str]] = {}
    for parent, children in REQUIRES.items():
        for child in children:
            parent_of.setdefault(child, []).append(parent)

    for (short, kind, risk, claim, formal, output, machine, human_source,
         body, inference, locator) in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if short in {"ROOT", "S-TARGET"}
            else "planned:v1:sha256:" + digest(
                [identifier, kind, claim, formal, output]
            )
        )
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human_source,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusions.get(identifier),
            "terminal_proof_body_id": body,
        })

        if identifier == oid("T-MATHLIB-EKR"):
            provenance = "anchor-audit:M0822-C02-MATHLIB-UPPER-BOUND"
        elif identifier in {oid("T-ATTAINMENT"), oid("C-STAR"), oid("L-STAR-IMAGE"),
                            oid("L-STAR-INTERSECTING"), oid("L-STAR-SIZED"),
                            oid("L-STAR-CARD"), oid("L-GROUND-ELEMENT")}:
            provenance = "anchor-audit:M0822-C01-LOCAL-STATEMENT-STAR"
        elif short in INTERNAL_OVERLAYS:
            provenance = "pinned-mathlib-terminal-body-overlay"
        elif body and body.startswith("local:"):
            provenance = "target-local-conditional-composition"
        else:
            provenance = "none"

        premises = REQUIRES.get(identifier, [])
        if not premises:
            premises = [
                "pinned-mathlib-source" if short in INTERNAL_OVERLAYS or
                identifier == oid("T-MATHLIB-EKR") else "frozen-formal-context"
            ]
        outgoing_use = (
            "Consumed by " + ", ".join(parent_of[identifier]) + "."
            if identifier in parent_of
            else "Supports a typed refinement, release, documentation, or workflow edge only."
        )
        task_ids = [ITEM]
        if machine == "required":
            task_ids.append(TASK_IDS[4])
        if identifier in {oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST")}:
            task_ids.extend([TASK_IDS[5], TASK_IDS[6]])
        if identifier in {oid("X-SOURCE"), oid("X-READABLE"), oid("X-WORKFLOW")}:
            task_ids.append(TASK_IDS[6])

        owned_sources: list[str] = []
        if short in {"S-TARGET", "S-BOUNDARY", "T-ATTAINMENT", "C-STAR",
                     "L-STAR-IMAGE", "L-STAR-INTERSECTING", "L-STAR-SIZED",
                     "L-STAR-CARD", "L-GROUND-ELEMENT"}:
            owned_sources = ["Stage1_Instances/THM-M-0822/Statement.lean"]
        elif short in {"ROOT", "T-ASSEMBLE", "T-UPPER-ADAPTER", "T-MATHLIB-EKR"}:
            owned_sources = ["Stage1_Instances/THM-M-0822/ObligationTree.lean"]
        elif short == "X-SOURCE":
            owned_sources = ["Stage1_Instances/THM-M-0822/source-statement-crosswalk.md"]
        elif short == "X-READABLE":
            owned_sources = ["Stage1_Instances/THM-M-0822/obligation-tree.md"]

        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": kind,
            "human_statement": claim,
            "formal_target": formal,
            "output": output,
            "human_debt": "H1",
            "machine_debt": "M3" if machine != "not_applicable" else "M4",
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "primary-source-node-map-pending" if human_source == "required"
                else "not-applicable-pending-review"
            ),
            "provenance_id": provenance,
            "foundation_profile": (
                "Lean 4 dependent type theory; observed candidate axioms propext, "
                "Classical.choice, Quot.sound; transitive acceptance pending"
            ),
            "tcb_profile": (
                "Lean 4.29.0 plus mathlib 8a178386; compiled-artifact, executable, "
                "and transitive declaration closure pending"
            ),
            "computation_record": (
                "none; no native computation, solver, oracle, experiment, or unchecked "
                "certificate is credited"
            ),
            "step_budget": 1,
            "semantic_step_ledger": [{
                "step_id": f"{identifier}-STEP-01",
                "premise_ids": premises,
                "inference": inference,
                "source_locator": locator,
                "output": output,
                "outgoing_use": outgoing_use,
            }],
            "public_readable_target": (
                f"Stage1_Instances/THM-M-0822/obligation-tree.md#{identifier.lower()}"
            ),
            "validation_spec_id": "VAL-M0822-OBLIGATION-BUNDLE",
            "status_boundary": (
                "Frozen architecture or provisionally elaborated interface only; no M0, "
                "accepted obligation, audit completion, or theorem completion."
            ),
            "task_ids": list(dict.fromkeys(task_ids)),
            "owned_sources": owned_sources,
            "owner": "THM-M-0822 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": None,
                "review_due": "before master acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "toolchain and dependency pins",
                ],
                "revocation_state": "not-accepted",
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
        "registry_id": "THM-M-0822-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T23:15:00+08:00",
        "freeze_basis": (
            "The exact frozen maximum-value statement, target-owned star construction, and "
            "visible pinned Finset.erdos_ko_rado body determine the architecture. Eligibility, "
            "risks, and denominators were selected before proof-phase installation or accepted "
            "closure metrics were observed."
        ),
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations
                                 if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations
                                      if row["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [row["obligation_id"] for row in obligations
                                       if row["machine_eligibility"] == "informational"],
        },
        "layer_applicability": {
            "S_statement_foundation": {
                "status": "required",
                "obligation_ids": [oid("S-TARGET"), oid("S-BOUNDARY"), oid("S-FOUNDATION")],
            },
            "N_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No representation, symmetry, order, finite/infinite, or local/global normalization is used beyond the explicit upper-terminal binder transport.",
                "obligation_ids": [],
            },
            "B_branch": {"status": "required", "obligation_ids": [oid("S-BOUNDARY"), oid("B-RZERO")]},
            "C_construction": {"status": "required", "obligation_ids": [oid("C-STAR"), oid("L-GROUND-ELEMENT"), oid("C-COMPLEMENTS")]},
            "L_core_lemma": {"status": "required", "obligation_ids": [oid(short) for short in (
                "L-STAR-IMAGE", "L-STAR-INTERSECTING", "L-STAR-SIZED", "L-STAR-CARD",
                "L-SHADOW-DISJOINT", "L-COMPLEMENT-CARD", "L-COMPLEMENT-SIZED",
                "L-KK-LOVASZ", "L-BINOMIAL-CONTRADICTION", "L-SLICE-CARD",
            )]},
            "X_external_and_computation": {
                "status": "required_external_boundary_and_not_applicable_computation_pending_independent_approval",
                "reason": "Pinned mathlib bodies and trust are material; no external computation, solver, oracle, experiment, or certificate is credited.",
                "obligation_ids": [oid(short) for short in (
                    "T-MATHLIB-EKR", "X-SOURCE", "X-PROVENANCE", "X-TRUST",
                    "X-READABLE", "X-WORKFLOW",
                )],
            },
            "T_terminal_transport": {"status": "required", "obligation_ids": [oid("T-ASSEMBLE"), oid("T-ATTAINMENT"), oid("T-UPPER-ADAPTER")]},
            "ROOT_exact_theorem": {"status": "required", "obligation_ids": [oid("ROOT")]},
        },
        "layer_exclusions": {
            "additional_symmetry_or_order_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The chosen labeled Fin n and star route need no quotient, relabeling, ordering, sign, or representative normalization.",
            },
            "equality_classification_branch": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The frozen root is maximum value only and intentionally makes no classification claim at or away from n=2r.",
            },
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, solver, native computation, numerical search, oracle, experiment, or unchecked certificate participates.",
            },
        },
        "proof_body_aliases": {
            "Stage1Instances.THM_M_0822.ObligationTree.attainment_of_localStar": "candidate_composition_through:attainment_of_starPackages+starConstruction_of_groundElement+starCard_of_image",
            "Stage1Instances.THM_M_0822.ObligationTree.pinnedMathlibUpperBound": "wrapper_only_deduplicated_to:Finset.erdos_ko_rado",
            "Stage1Instances.THM_M_0822.ObligationTree.upperBound_of_mathlibTerminal": "adapter_only_no_terminal_body_credit",
            "Stage1Instances.THM_M_0822_AnchorAudit.upperBound_of_pinnedMathlib": "wrapper_only_deduplicated_to:Finset.erdos_ko_rado",
            "ErdosKoRado.erdos_ko_rado_theorem": "external_wrapper_deduplicated_to:Finset.erdos_ko_rado",
        },
        "delta_policy": (
            "Any target correction, split, merge, exclusion, eligibility/risk change, or "
            "terminal-body identity change requires registry version 2 and an append-only delta."
        ),
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "provisionally_elaborated_interfaces": [
                oid("ROOT"), oid("T-ASSEMBLE"), oid("T-ATTAINMENT"),
                oid("T-UPPER-ADAPTER"), oid("T-MATHLIB-EKR"),
            ],
            "candidate_route": "exact pinned route kernel-checked below E1 and not master-accepted",
            "accepted_closed_obligations": [],
            "accepted_root_machine_debt": "M3",
        },
        "classification_metrics": {
            "inventory_classified_numerator_ids": ids,
            "inventory_classified_denominator_ids": ids,
            "required_machine_leaf_denominator_ids": [
                oid("L-GROUND-ELEMENT"), oid("L-STAR-IMAGE"),
                oid("L-STAR-INTERSECTING"), oid("L-STAR-SIZED"),
                oid("T-MATHLIB-EKR"),
            ],
            "accepted_machine_leaf_numerator_ids": [],
            "required_terminal_body_denominator_ids": sorted({
                row["terminal_proof_body_id"] for row in obligations
                if row["terminal_proof_body_id"] is not None
            }),
            "accepted_terminal_body_numerator_ids": [],
            "required_interface_denominator_ids": [
                oid("ROOT"), oid("T-ASSEMBLE"), oid("T-ATTAINMENT"),
                oid("C-STAR"), oid("L-STAR-CARD"), oid("T-UPPER-ADAPTER"),
            ],
            "accepted_interface_numerator_ids": [],
            "required_readable_denominator_ids": ids,
            "accepted_r0_numerator_ids": [],
            "required_human_source_denominator_ids": [
                row["obligation_id"] for row in obligations
                if row["human_source_eligibility"] == "required"
            ],
            "accepted_h0_numerator_ids": [],
            "required_formal_source_boundary_denominator_ids": [
                row["obligation_id"] for row in obligations
                if row["machine_eligibility"] in {"required", "informational"}
            ],
            "classified_formal_source_boundary_numerator_ids": [
                row["obligation_id"] for row in obligations
                if row["machine_eligibility"] in {"required", "informational"}
            ],
            "root_closed": False,
            "critical_path_closed": False,
            "risk_bucket_accepted_ids": {
                risk: [] for risk in ("critical", "high", "normal", "low")
            },
            "disputed_eligibility_bounds": {
                "optimistic_accepted_machine_ids": [],
                "pessimistic_accepted_machine_ids": [],
                "reason": "No obligation has accepted proof credit, so both bounds are zero.",
            },
            "metamorphic_boundary": (
                "Aliases, wrappers, and the eight imported presentation nodes are excluded "
                "or deduplicated by canonical obligation and terminal proof-body IDs; no "
                "acceptance metric is inferred from raw node count."
            ),
        },
        "status_boundary": (
            "Registry scope and denominators only. The local attainment and pinned upper-bound "
            "route are not installed or accepted; H0, R0, validation, release, AUDIT-Z, and "
            "theorem completion remain open."
        ),
    }

    proof_edges: list[dict] = []
    for parent, children in REQUIRES.items():
        for child in children:
            if parent in CERTIFICATES:
                requirement = f"REQ-{parent}-{child}"
                composition = f"CMP-{child}-{parent}"
                proof_edges.extend([
                    edge(requirement, parent, "proof_requires", child, composition),
                    edge(composition, child, "composes", parent, requirement),
                ])

    refinement_edges = [
        edge("REF-ROOT-TARGET", oid("ROOT"), "expository_decomposition", oid("S-TARGET")),
        edge("REF-ROOT-BOUNDARY", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
    ]
    for short in INTERNAL_OVERLAYS:
        refinement_edges.append(edge(
            f"REF-MATHLIB-{short}", oid("T-MATHLIB-EKR"),
            "expository_decomposition", oid(short),
        ))

    graph_edges = {
        "proof": proof_edges,
        "refinement": refinement_edges,
        "provenance": [
            edge("PROV-STAR", oid("X-PROVENANCE"), "provenance_of", oid("T-ATTAINMENT")),
            edge("PROV-EKR", oid("X-PROVENANCE"), "provenance_of", oid("T-MATHLIB-EKR")),
            edge("SOURCE-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SOURCE-UPPER", oid("X-SOURCE"), "source_map", oid("T-MATHLIB-EKR")),
        ],
        "evidence": [
            edge("EVID-PROVENANCE-UPPER", oid("X-PROVENANCE"), "evidence_for", oid("T-MATHLIB-EKR")),
            edge("EVID-WORKFLOW-ROOT", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-EKR-CLOSURE", oid("T-MATHLIB-EKR"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-STAR", oid("X-READABLE"), "documents", oid("T-ATTAINMENT")),
            edge("DOC-READABLE-UPPER", oid("X-READABLE"), "documents", oid("T-MATHLIB-EKR")),
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge(f"TASK-{index}", TASK_IDS[index], "workflow_depends_on", TASK_IDS[index - 1])
            for index in range(1, len(TASK_IDS))
        ],
    }

    graphs = {name: graph(graph_edges[name]) for name in GRAPH_NAMES}
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in obligations}
    composition_certificates = []
    for parent, declaration in CERTIFICATES.items():
        children = REQUIRES[parent]
        composition_certificates.append({
            "certificate_id": f"CERT-{parent}",
            "parent_obligation_id": parent,
            "required_child_ids": children,
            "parent_statement_fingerprint": fingerprints[parent],
            "required_child_statement_fingerprints": {
                child: fingerprints[child] for child in children
            },
            "declaration": declaration,
            "certificate_kind": "lean_abstract_child_harness",
            "introduces_undeclared_premises": False,
            "status": "provisionally_elaborated_not_accepted",
        })

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0822-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": (
            "canonical obligation_id except workflow, which uses authoritative task IDs"
        ),
        "edge_direction": (
            "proof_requires is parent-to-child; reciprocal composes is child-to-parent; "
            "workflow_depends_on is task-to-prerequisite"
        ),
        "workflow_task_nodes": list(TASK_IDS),
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": composition_certificates,
        "unverified_decomposition_plans": [],
        "closure_boundary": {
            "provisionally_elaborated_interfaces": [
                oid("ROOT"), oid("T-ASSEMBLE"), oid("T-ATTAINMENT"),
                oid("T-UPPER-ADAPTER"), oid("T-MATHLIB-EKR"),
            ],
            "candidate_only_obligations": [oid("T-ATTAINMENT"), oid("T-MATHLIB-EKR")],
            "accepted_closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "proof_leaf_cut_set": [
                oid("L-GROUND-ELEMENT"), oid("L-STAR-IMAGE"),
                oid("L-STAR-INTERSECTING"), oid("L-STAR-SIZED"),
                oid("T-MATHLIB-EKR"),
            ],
            "remaining_root_cut_set": [
                oid("T-ATTAINMENT"), oid("T-MATHLIB-EKR"), oid("S-FOUNDATION"),
                oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"),
                oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "reason": (
                "All composition checks are provisional. The concrete star and pinned terminal "
                "remain uninstalled, below release-grade E1, and unaccepted."
            ),
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [{
            "recipe_id": "VAL-M0822-OBLIGATION-BUNDLE",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0822/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 240,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{
                "path_or_stream": "stdout",
                "semantic_hash_policy": "contains PASS THM-M-0822 obligation tree",
            }],
            "covered_obligation_ids": ids,
            "covered_declarations": [
                "Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget",
                "Stage1Instances.THM_M_0822.erdosKoRadoStar_attains",
                "Finset.erdos_ko_rado",
                "Stage1Instances.THM_M_0822.ObligationTree.attainment_of_localStar",
                "Stage1Instances.THM_M_0822.ObligationTree.upperBound_of_mathlibTerminal",
                "Stage1Instances.THM_M_0822.ObligationTree.pinnedMathlibUpperBound",
                "Stage1Instances.THM_M_0822.ObligationTree.composeRoot",
                "Stage1Instances.THM_M_0822.ObligationTree.rootOfExactAssembly",
            ],
        }],
    }
    return registry, bundle, recipes


def main() -> None:
    values = build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"),
        values,
    ):
        (HERE / name).write_text(
            json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
    edge_count = sum(len(graph_value["edges"])
                     for graph_value in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {values[0]['denominator_sha256']}")


if __name__ == "__main__":
    main()
