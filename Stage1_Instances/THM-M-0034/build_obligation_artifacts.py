#!/usr/bin/env python3
"""Build the frozen THM-M-0034 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0034-OBLIGATION_TREE"
THEOREM = "THM-M-0034"
PREFIX = "M0034-"
ROOT_EXPRESSION = "d80cc9860ed5a53c81a0851b4dc8e702aa5a23d448f373ae6d68ed0c9b5604b1"
EXTERNAL_REVISION = "e8d85a6f6fa210ba0be12bd02aa22009699f0c35"
EXTERNAL_ARCHIVE_SHA256 = "6072221d080e634f0a9775518855557fce0495cf4004848e4cb57dda4aa7e6d2"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(payload).hexdigest()


# Architecture is derived from the exact root and the visible high-level dependency route in the
# immutable candidate. No closure state occurs in this table; status is attached only after the
# denominator is frozen.
# short id, kind, risk, human claim, formal/planned target, output, machine eligibility,
# human-source eligibility, terminal body identity, local step budget
ROWS = (
    ("ROOT", "root", "critical",
     "Every finitely generated projective module over a positive finite-variable polynomial ring over a field is free.",
     "Stage1Instances.THM_M_0034.QuillenSuslinTarget",
     "The exact frozen positive-variable field proposition.", "required", "required", None, 8),
    ("S-INTERFACE", "definition", "critical",
     "Preserve independent universes, field coefficients, positive n, finite generation, projectivity, and the Module.Free conclusion.",
     "Stage1Instances.THM_M_0034.QuillenSuslinTarget",
     "The exact root context and conclusion without a strengthened coefficient class or weakened module claim.",
     "required", "not_applicable", None, 14),
    ("S-BOUNDARY", "branch", "high",
     "Retain zero modules and rank zero, require positive n, and exclude infinite-variable and non-field substitutions.",
     "Statement.lean boundary policy and four checked statement mutations",
     "The complete degenerate-case policy for this target.", "required", "required", None, 18),
    ("S-EXTERNAL-TRANSPORT", "transport", "high",
     "The all-natural-n field candidate implies the exact positive-variable target, without crediting the candidate body.",
     "Stage1Instances.THM_M_0034.ObligationTree.externalFieldCandidate_implies_target",
     "A checked one-way target-preserving transport.", "required", "not_applicable",
     "repo:ObligationTree.lean#externalFieldCandidate_implies_target", 5),
    ("S-FOUNDATION", "certificate", "critical",
     "Audit classical choice, quotient soundness, extensionality, imports, kernel, and the accepted TCB for the terminal body.",
     "planned transitive foundation and TCB certificate",
     "A release-grade foundation decision with no mathematical proof credit.", "informational", "not_applicable", None, 38),
    ("N-INDUCTION", "reduction", "critical",
     "Reduce the same-universe theorem to exhaustive zero and successor cases by induction on the number of variables.",
     "external:QuillenSuslin.quillenSuslin_aux_of_holes",
     "A theorem for all finite n once both branches compose.", "required", "required",
     "external:QuillenSuslin.quillenSuslin_aux_of_holes", 20),
    ("B-ZERO", "branch", "high",
     "At n = 0, transport along the empty-variable polynomial equivalence and use projective-over-PID freeness.",
     "external:QuillenSuslin.free_of_projective_mvPolynomial_fin_zero",
     "The induction base case, stronger than the public positive-n root but required by the candidate route.",
     "required", "required", "external:QuillenSuslin.free_of_projective_mvPolynomial_fin_zero", 28),
    ("B-SUCC", "branch", "critical",
     "For n = m+1, present the ring as B[X], produce a monic localization, patch extendedness, free the fibre, and transport back.",
     "external:QuillenSuslin.r3_step",
     "The complete successor branch.", "required", "required", "external:QuillenSuslin.r3_step", 20),
    ("C-FINSUCC", "construction", "high",
     "Use MvPolynomial.finSuccEquiv to view the successor-variable ring as a univariate polynomial ring B[X] and transport finite projectivity.",
     "external:r3_step scalar transport via MvPolynomial.finSuccEquiv",
     "A finite projective B[X]-module with an exact inverse transport.", "required", "required", None, 42),
    ("C-NAGATA-MONIC", "construction", "critical",
     "After a field-valid Nagata change of variables, choose a monic polynomial f such that localization of the shifted module at f is free.",
     "external:Module.exists_monic_localized_free_of_projective",
     "A ring self-equivalence, a monic f, and localized freeness.", "required", "required",
     "external:Module.exists_monic_localized_free_of_projective", 24),
    ("L-GENERIC-FREENESS", "core_lemma", "critical",
     "Produce a nonzero denominator whose localization makes the finite projective module free.",
     "external generic-freeness package",
     "Nonzero-denominator localized freeness before monic normalization.", "required", "required", None, 72),
    ("L-NAGATA-CHANGE", "core_lemma", "critical",
     "Apply the Nagata monomial change of variables and unit rescaling to make the denominator monic over B, including finite fields.",
     "external:exists_algEquiv_monic_smul_finSuccEquiv and associated-denominator transport",
     "A monic denominator with preserved localized freeness.", "required", "required", None, 78),
    ("C-SHIFT", "construction", "high",
     "Carry the module through restriction of scalars along the Nagata self-equivalence, preserving finiteness and projectivity.",
     "external:Module.compHomShift and compHomShiftEquiv",
     "The shifted finite projective B[X]-module used by descent.", "required", "required", None, 52),
    ("C-PER-MAXIMAL", "construction", "critical",
     "For every maximal ideal of B, form the localized module and establish that it is extended from the localized base.",
     "external:QuillenSuslin.perMaximal_extended",
     "The per-maximal IsExtended family consumed by Quillen patching.", "required", "required",
     "external:QuillenSuslin.perMaximal_extended", 30),
    ("L-GLOBAL-LOCAL-FREE", "core_lemma", "critical",
     "Descend global monic-localized freeness to the corresponding localization over every maximal ideal of B.",
     "external:Module.free_localized_descends_atPrime",
     "The GFD input at each maximal ideal.", "required", "required",
     "external:Module.free_localized_descends_atPrime", 82),
    ("L-MONIC-LOCAL", "core_lemma", "critical",
     "Over each local coefficient ring, turn freeness after inverting the descended monic polynomial into extendedness.",
     "external:Module.isExtended_atPrime_of_monicLocalized_free",
     "Local extendedness at every maximal ideal.", "required", "required", None, 88),
    ("L-QUILLEN-PATCH", "core_lemma", "critical",
     "Patch per-maximal extendedness into global extendedness of the B[X]-module from B.",
     "external:Module.quillen_patching and QuillenSuslin.qPatch",
     "Module.IsExtended B for the shifted module.", "required", "required",
     "external:Module.quillen_patching", 18),
    ("C-IDEMPOTENT", "construction", "critical",
     "Represent the finite projective module as the range of an idempotent matrix and transport its range under base change.",
     "external patching idempotent/range package",
     "Finite matrix data encoding the projective module on localization charts.", "required", "required", None, 92),
    ("C-LOCAL-CHARTS", "construction", "critical",
     "Choose localization charts and powers witnessing local extendedness, retaining compatibility with the idempotent presentation.",
     "external patching chart and localization package",
     "A finite cover by extended localization charts.", "required", "required", None, 88),
    ("L-DILATION", "core_lemma", "critical",
     "Clear denominators and dilate chart conjugacies so their equality data descends to the base polynomial ring.",
     "external patching dilation package",
     "Base-level conjugacy data on sufficiently large powers.", "required", "required", None, 96),
    ("L-LOCUS", "core_lemma", "critical",
     "Show the locus of base elements where the module is extended contains zero, is stable under scaling, and is closed under addition.",
     "external:isExtendedAtPow locus_zero/locus_smul/locus_add",
     "An ideal-like extendedness locus whose maximal-local coverage forces the unit case.", "required", "required", None, 94),
    ("L-TWO-CHART", "core_lemma", "critical",
     "Glue two coprime extendedness charts through compatible idempotent and matrix conjugacy data.",
     "external:TwoChartCore and Quillen patching composition",
     "Extendedness on the sum chart, closing the additive locus step.", "required", "required", None, 98),
    ("C-FIBRE", "construction", "high",
     "Form the fibre at X=0 and transfer finiteness and projectivity to the coefficient ring B.",
     "external:Module.fibreZero, finite_fibreZero, projective_fibreZero",
     "A finite projective B-module.", "required", "required", None, 52),
    ("L-FIBRE-IH", "core_lemma", "critical",
     "Apply the induction hypothesis to make the zero fibre free over B.",
     "external:r3_step induction-hypothesis application",
     "A free B-module instance on the fibre.", "required", "required", None, 18),
    ("L-ENDGAME", "core_lemma", "critical",
     "Combine global extendedness and fibre freeness to make the shifted module free over B[X].",
     "external:Module.free_of_isExtended_of_fibre_free",
     "Freeness of the shifted B[X]-module.", "required", "required",
     "external:Module.free_of_isExtended_of_fibre_free", 48),
    ("L-UNDO-TRANSPORT", "transport", "critical",
     "Undo the Nagata shift and finSuccEquiv through checked semilinear ring-equivalence transports.",
     "external:Module.Free.of_ringEquiv_semilinear",
     "Freeness in the original successor-variable module structure.", "required", "required", None, 54),
    ("T-SAME-UNIVERSE", "terminal", "critical",
     "Assemble the induction with the Quillen-patching and global-local-free seams for module and field in the same universe.",
     "external:QuillenSuslin.quillenSuslin_u",
     "The same-universe Quillen-Suslin theorem.", "required", "required",
     "external:QuillenSuslin.quillenSuslin_u", 16),
    ("C-ULIFT", "construction", "high",
     "ULift the field and module into a common universe and construct the induced multivariate-polynomial ring equivalence and semilinear module equivalence.",
     "external:QuillenSuslin.quillenSuslin_bridge ULift construction",
     "Same-universe finite projective data linked semilinearly to the original module.", "required", "required", None, 76),
    ("L-ULIFT-TRANSPORT", "transport", "critical",
     "Transport finiteness, projectivity, and final freeness across the ULift ring and semilinear module equivalences.",
     "external:Module.Finite.of_equiv', Projective.of_equiv, Free.of_ringEquiv_semilinear",
     "Freeness back in the original independent-universe context.", "required", "required", None, 74),
    ("T-INDEPENDENT", "terminal", "critical",
     "Compose the same-universe theorem and ULift transports into the independent-universe candidate statement.",
     "external:QuillenSuslin.quillenSuslin_bridge",
     "The exact all-natural-n external field candidate.", "required", "required",
     "external:QuillenSuslin.quillenSuslin_bridge", 14),
    ("X-EXTERNAL-BODY", "bridge", "critical",
     "Integrate and replay the exact all-natural-n external theorem at its immutable revision before it can supply the selected proof premise.",
     "external:QuillenSuslin.quillenSuslin at e8d85a6f6fa210ba0be12bd02aa22009699f0c35",
     "An authorized, locally checked ExternalFieldCandidate proof body.", "required", "required",
     "external:QuillenSuslin.quillenSuslin", 26),
    ("X-MATHLIB", "bridge", "high",
     "Audit the pinned mathlib projective, localization, free-module, polynomial, matrix, and ULift substrate used transitively by the candidate.",
     "mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 transitive declarations",
     "A complete substrate declaration and trust boundary.", "informational", "not_applicable", None, 72),
    ("X-ALT-PID", "transport", "high",
     "Retain the stronger PID/arbitrary-finite-variable candidate as an alternative, incompatible-pin route without duplicate proof credit.",
     "external:mbkybky/QuillenSuslin.quillenSuslin at 51ed173b17b274e61f759556ab3e1c090267d1bd",
     "A checked statement specialization only; no selected proof premise.", "informational", "not_applicable", None, 22),
    ("T-ADAPTER", "terminal", "critical",
     "Consume the exact ExternalFieldCandidate premise and drop only the unused n=0 case.",
     "Stage1Instances.THM_M_0034.ObligationTree.externalFieldCandidate_implies_adapted",
     "The exact AdaptedPositiveCandidate conclusion.", "required", "not_applicable",
     "repo:ObligationTree.lean#externalFieldCandidate_implies_adapted", 5),
    ("T-ROOT", "terminal", "critical",
     "Consume the adapted positive-variable conclusion and produce the exact canonical target.",
     "Stage1Instances.THM_M_0034.ObligationTree.terminalTarget_of_adapted",
     "The exact frozen root as a terminal conclusion.", "required", "required",
     "repo:ObligationTree.lean#terminalTarget_of_adapted", 4),
    ("X-SOURCE", "source_boundary", "critical",
     "Pinpoint-map every proof transition to Quillen, Suslin, and any modern dependencies, with translation, errata, and independent source review.",
     "planned primary-source node crosswalk",
     "H0 source coverage without machine proof credit.", "not_applicable", "required", None, 96),
    ("X-LICENSE", "certificate", "critical",
     "Establish reusable licensing permission for the selected external source and every non-mathlib dependency.",
     "selected candidate license artifact currently absent",
     "An accepted supply-chain license decision without mathematical proof credit.", "informational", "not_applicable", None, 24),
    ("X-PROVENANCE", "certificate", "critical",
     "Freeze terminal declaration, wrapper, body, all transitive declarations, source blobs, revisions, aliases, and distinct proof-body identities.",
     "planned external declaration and import provenance closure",
     "Complete body-level provenance without duplicate proof credit.", "informational", "not_applicable", None, 90),
    ("X-TRUST", "certificate", "critical",
     "Replay the external source locally and audit axioms, kernel, dependencies, unsafe/oracle boundaries, artifacts, and reproducibility transitively.",
     "planned external terminal trust closure",
     "Release-grade trust evidence without mathematical proof credit.", "informational", "not_applicable", None, 90),
    ("X-READABLE", "documentation", "high",
     "Produce node-specific readable ledgers with formal anchors, assumptions, branch logic, and independent mathematical review.",
     "planned readable reconstruction",
     "R0 coverage without machine proof credit.", "not_applicable", "not_applicable", None, 98),
    ("X-WORKFLOW", "workflow", "critical",
     "Bind proof integration, validation, source, readability, freshness, revocation, independent verification, and release in dependency order.",
     "planned Stage1 task and receipt closure",
     "Workflow acceptance without mathematical proof credit.", "informational", "not_applicable", None, 42),
)


PROOF_REQUIRES = {
    oid("ROOT"): [oid("T-ROOT")],
    oid("T-ROOT"): [oid("T-ADAPTER")],
    oid("T-ADAPTER"): [oid("X-EXTERNAL-BODY")],
}

REFINEMENT = {
    oid("ROOT"): [oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-EXTERNAL-TRANSPORT")],
    oid("X-EXTERNAL-BODY"): [oid("T-INDEPENDENT")],
    oid("T-INDEPENDENT"): [oid("T-SAME-UNIVERSE"), oid("C-ULIFT"), oid("L-ULIFT-TRANSPORT")],
    oid("T-SAME-UNIVERSE"): [oid("N-INDUCTION")],
    oid("N-INDUCTION"): [oid("B-ZERO"), oid("B-SUCC")],
    oid("B-SUCC"): [oid("C-FINSUCC"), oid("C-NAGATA-MONIC"), oid("C-SHIFT"),
                    oid("C-PER-MAXIMAL"), oid("L-QUILLEN-PATCH"), oid("C-FIBRE"),
                    oid("L-FIBRE-IH"), oid("L-ENDGAME"), oid("L-UNDO-TRANSPORT")],
    oid("C-NAGATA-MONIC"): [oid("L-GENERIC-FREENESS"), oid("L-NAGATA-CHANGE")],
    oid("C-PER-MAXIMAL"): [oid("L-GLOBAL-LOCAL-FREE"), oid("L-MONIC-LOCAL")],
    oid("L-QUILLEN-PATCH"): [oid("C-IDEMPOTENT"), oid("C-LOCAL-CHARTS"),
                             oid("L-DILATION"), oid("L-LOCUS"), oid("L-TWO-CHART")],
}

CHECKED_INTERFACES = {oid("S-EXTERNAL-TRANSPORT"), oid("T-ADAPTER"), oid("T-ROOT")}
SOURCE_NA = {
    oid("S-INTERFACE"), oid("S-EXTERNAL-TRANSPORT"), oid("S-FOUNDATION"),
    oid("X-MATHLIB"), oid("X-ALT-PID"), oid("T-ADAPTER"), oid("X-LICENSE"),
    oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
}


def build() -> tuple[dict, dict, dict, str]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    architecture = {**PROOF_REQUIRES, **REFINEMENT}
    parents: dict[str, list[str]] = {}
    for parent, children in architecture.items():
        for child in children:
            parents.setdefault(child, []).append(parent)

    obligations: list[dict] = []
    nodes: list[dict] = []
    for short, kind, risk, claim, target, output, machine, human, body, budget in ROWS:
        identifier = oid(short)
        registry_kind = {
            "core_lemma": "lemma",
            "bridge": "terminal",
            "certificate": "terminal",
            "source_boundary": "terminal",
            "documentation": "terminal",
            "workflow": "terminal",
        }.get(kind, kind)
        node_kind = {
            "source_boundary": "terminal",
            "documentation": "terminal",
            "workflow": "certificate",
        }.get(kind, kind)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if short in {"ROOT", "S-INTERFACE"} else
            "planned:v1:sha256:" + digest([identifier, kind, claim, target, output])
        )
        exclusions = {
            oid("S-INTERFACE"): "formal_interface_source_coverage_inherited_from_root_pending_independent_approval",
            oid("S-EXTERNAL-TRANSPORT"): "formal_transport_not_a_distinct_human_claim_pending_independent_approval",
            oid("S-FOUNDATION"): "trust_overlay_no_machine_or_human_proof_credit_pending_independent_approval",
            oid("X-MATHLIB"): "substrate_overlay_no_distinct_proof_credit_pending_independent_approval",
            oid("X-ALT-PID"): "nonselected_alternative_deduplicated_from_root_credit_pending_independent_approval",
            oid("T-ADAPTER"): "formal_transport_source_coverage_inherited_from_root_pending_independent_approval",
            oid("X-SOURCE"): "human_source_boundary_only_pending_independent_approval",
            oid("X-LICENSE"): "license_overlay_no_machine_or_human_proof_credit_pending_independent_approval",
            oid("X-PROVENANCE"): "provenance_overlay_no_machine_or_human_proof_credit_pending_independent_approval",
            oid("X-TRUST"): "trust_overlay_no_machine_or_human_proof_credit_pending_independent_approval",
            oid("X-READABLE"): "readability_boundary_only_pending_independent_approval",
            oid("X-WORKFLOW"): "workflow_overlay_no_machine_or_human_proof_credit_pending_independent_approval",
        }
        excluded = machine != "required" or human != "required"
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": registry_kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusions[identifier] if excluded else None,
            "terminal_proof_body_id": body,
        })
        children = architecture.get(identifier, [])
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": node_kind,
            "human_statement": claim,
            "formal_target": target,
            "output": output,
            "human_debt": "H1",
            "machine_debt": "M3" if identifier in CHECKED_INTERFACES or identifier == oid("X-EXTERNAL-BODY") or short == "ROOT" else "M4",
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": "not-applicable-pending-review" if identifier in SOURCE_NA else "primary-source-node-map-pending",
            "provenance_id": (
                "anchor-audit:M0034-C02-EDMUND-EXACT" if identifier == oid("X-EXTERNAL-BODY")
                else "local-conditional-composition" if identifier in CHECKED_INTERFACES
                else "external-visible-route-unaccepted" if body and body.startswith("external:")
                else "support-boundary-pending" if short.startswith("X-")
                else "none"
            ),
            "foundation_profile": "lean4-dependent-type-theory; accepted transitive axiom policy pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; external body absent and transitive closure pending",
            "computation_record": "none; no solver, oracle, native shortcut, experiment, or unchecked certificate is credited",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": children if children else ["exact formal context and no undeclared mathematical premise"],
                "inference": target,
                "output": output,
                "outgoing_use": parents.get(identifier, ["typed support edge only or canonical terminal output"]),
                "steps": [{
                    "step_id": f"{identifier}-STEP-01",
                    "premise_ids": children if children else ["EXACT-CONTEXT"],
                    "inference_or_boundary": target,
                    "output_claim": output,
                    "outgoing_use_ids": parents.get(identifier, ["SUPPORT-ONLY"]),
                }],
            },
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.",
            "task_ids": [ITEM, "S56-M-0034-PROOF", "S56-M-0034-VALIDATION"],
            "owned_sources": [f"Stage1_Instances/{THEOREM}/ObligationTree.lean"] if identifier in CHECKED_INTERFACES else [],
            "owner": "THM-M-0034 execution lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json",
                                        "typed-graphs.json", "external revision or source", "toolchain and dependency pins"],
                "revocation_state": "provisional_interface_check" if identifier in CHECKED_INTERFACES else "open",
            },
        })

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
              "machine_eligibility", "human_source_eligibility", "readable_eligibility",
              "risk_class", "exclusion_reason", "terminal_proof_body_id")
    denominator = digest([{field: row[field] for field in fields} for row in obligations])
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0034-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "The exact statement, completed candidate inventory, and visible high-level architecture of the selected immutable source candidate. Eligibility and denominators are independent of closure status.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "selected_external_revision": EXTERNAL_REVISION,
        "selected_external_archive_sha256": EXTERNAL_ARCHIVE_SHA256,
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
            "sign_order_symmetry_normalization": {"status": "not_applicable_pending_independent_approval", "reason": "Modules and variables have no sign, order, or symmetry quotient; finSucc and Nagata transports are explicit."},
            "finite_infinite_split": {"status": "not_applicable_pending_independent_approval", "reason": "The target quantifies only over Fin n; infinite-variable polynomial rings are outside the frozen statement."},
            "computation": {"status": "not_applicable_pending_independent_approval", "reason": "The visible route uses no finite computation, reflection, solver, oracle, or certificate."},
            "stable_free_unimodular_matrix_substitutions": {"status": "excluded_pending_independent_approval", "reason": "No checked equivalence maps these adjacent formulations to the selected module root."},
        },
        "proof_body_aliases": {
            "QuillenSuslin.quillenSuslin": "selected_terminal_body",
            "QuillenSuslin.quillenSuslin_bridge": "same_external_body_chain_no_duplicate_credit",
            "AnchorAudit.ExternalFieldCandidate": "statement_only_alias_no_proof_credit",
            "mbkybky.QuillenSuslin.quillenSuslin": "alternative_body_no_selected_credit",
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility/risk change, source revision, or terminal-body identity change requires registry version 2 and an append-only old/new-ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "provisionally_checked_interfaces": sorted(CHECKED_INTERFACES),
            "accepted_closed_obligations": [],
            "selected_candidate_classification": "M3_exact_external_source_anchor_E3",
            "root_machine_debt": "M3",
        },
        "status_boundary": "The registry freezes architecture only. The selected external source remains absent, unlicensed, locally unreplayed, and unaccepted; no proof or terminal closure is credited.",
    }

    def edge(eid: str, source: str, kind: str, target: str, reciprocal: str | None = None) -> dict:
        result = {"edge_id": eid, "from": source, "type": kind, "to": target}
        if reciprocal:
            result["reciprocal_edge_id"] = reciprocal
        return result

    proof: list[dict] = []
    for parent, children in PROOF_REQUIRES.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            comp = f"CMP-{child}-{parent}"
            proof.extend([edge(req, parent, "proof_requires", child, comp),
                          edge(comp, child, "composes", parent, req)])
    graph_edges = {
        "proof": proof,
        "refinement": [edge(f"REF-{parent}-{child}", parent, "expository_decomposition", child)
                       for parent, children in REFINEMENT.items() for child in children],
        "provenance": [
            edge("SRC-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-INDUCTION", oid("X-SOURCE"), "source_map", oid("N-INDUCTION")),
            edge("SRC-PATCH", oid("X-SOURCE"), "source_map", oid("L-QUILLEN-PATCH")),
            edge("PROV-EXTERNAL", oid("X-PROVENANCE"), "provenance_of", oid("X-EXTERNAL-BODY")),
            edge("PROV-MATHLIB", oid("X-PROVENANCE"), "provenance_of", oid("X-MATHLIB")),
            edge("PROV-ALT", oid("X-PROVENANCE"), "provenance_of", oid("X-ALT-PID")),
        ],
        "evidence": [
            edge("EVID-EXTERNAL", oid("X-PROVENANCE"), "evidence_for", oid("X-EXTERNAL-BODY")),
            edge("EVID-WORKFLOW", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-TCB", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-BODY-TCB", oid("X-EXTERNAL-BODY"), "trusts", oid("X-TRUST")),
            edge("TRUST-BODY-LICENSE", oid("X-EXTERNAL-BODY"), "trusts", oid("X-LICENSE")),
            edge("TRUST-BODY-MATHLIB", oid("X-EXTERNAL-BODY"), "trusts", oid("X-MATHLIB")),
        ],
        "documentation": [
            edge("DOC-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-INDUCTION", oid("X-READABLE"), "documents", oid("N-INDUCTION")),
            edge("DOC-PATCH", oid("X-READABLE"), "documents", oid("L-QUILLEN-PATCH")),
            edge("DOC-ULIFT", oid("X-READABLE"), "documents", oid("T-INDEPENDENT")),
        ],
        "workflow": [
            edge("FLOW-WORKFLOW-BODY", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-EXTERNAL-BODY")),
            edge("FLOW-WORKFLOW-SOURCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
            edge("FLOW-WORKFLOW-LICENSE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-LICENSE")),
            edge("FLOW-WORKFLOW-PROV", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-WORKFLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-WORKFLOW-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
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

    all_refinement_nodes: set[str] = set()
    frontier = [oid("ROOT")]
    while frontier:
        current = frontier.pop()
        if current in all_refinement_nodes:
            continue
        all_refinement_nodes.add(current)
        frontier.extend(REFINEMENT.get(current, []))
        frontier.extend(PROOF_REQUIRES.get(current, []))
    edge_count = sum(len(graph["edges"]) for graph in graphs.values())
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
        "metrics_projection": {
            "denominator_ids": ids,
            "architecture_reachable_ids": sorted(all_refinement_nodes),
            "proof_reachable_ids": [oid("ROOT"), oid("T-ROOT"), oid("T-ADAPTER"), oid("X-EXTERNAL-BODY")],
            "accepted_numerator_ids": [],
            "alias_and_presentation_nodes_receive_credit": False,
        },
        "closure_boundary": {
            "provisionally_checked_interfaces": sorted(CHECKED_INTERFACES),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [oid("X-EXTERNAL-BODY"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                                       oid("X-LICENSE"), oid("X-PROVENANCE"), oid("X-TRUST"),
                                       oid("X-READABLE"), oid("X-WORKFLOW")],
            "composition_certificates": [
                "Stage1Instances.THM_M_0034.ObligationTree.externalFieldCandidate_implies_adapted",
                "Stage1Instances.THM_M_0034.ObligationTree.terminalTarget_of_adapted",
                "Stage1Instances.THM_M_0034.ObligationTree.root_of_terminalTarget",
            ],
            "missing_composition_certificates": [
                "the complete external body refinement from quillenSuslin through every semantic child"
            ],
            "reason": "All local composition is conditional. The external body is outside the dependency closure, has no usable license artifact, and has not been locally kernel-replayed or provenance-audited.",
        },
        "typed_edge_count": edge_count,
    }

    lean_nodes = CHECKED_INTERFACES
    recipes = []
    for identifier in ids:
        lean = identifier in lean_nodes
        recipes.append({
            "recipe_id": f"VAL-{identifier}",
            "cwd": "Formalizations/Lean" if lean else ".",
            "argv": (["bash", "-c", "tmp=$(mktemp -d /tmp/stage1-m0034-obligation.XXXXXX); trap 'rm -rf \"$tmp\"' EXIT; lake env lean --root=../.. ../../Stage1_Instances/THM-M-0034/Statement.lean -o \"$tmp/Statement.olean\" && LEAN_PATH=\"$tmp:$(lake env printenv LEAN_PATH)\" lake env lean --root=../.. ../../Stage1_Instances/THM-M-0034/ObligationTree.lean"]
                     if lean else ["python3", "-B", "Stage1_Instances/THM-M-0034/check_obligation_tree.py"]),
            "env_allowlist": {},
            "timeout_seconds": 180 if lean else 30,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "successful exact command; raw hash recorded in worker receipt"}],
            "covered_obligation_ids": [identifier],
            "covered_declarations": (["Stage1Instances.THM_M_0034.ObligationTree.externalFieldCandidate_implies_target",
                                      "Stage1Instances.THM_M_0034.ObligationTree.externalFieldCandidate_implies_adapted",
                                      "Stage1Instances.THM_M_0034.ObligationTree.terminalTarget_of_adapted",
                                      "Stage1Instances.THM_M_0034.ObligationTree.root_of_terminalTarget"] if lean else []),
            "coverage_semantics": "conditional_interface_only" if lean else "architecture_validation_only",
            "closure_credit": False,
        })
    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": recipes,
        "status_boundary": "These recipes validate frozen structure and conditional local interfaces only. They do not import or prove the external candidate body.",
    }

    lines = [
        "# THM-M-0034 frozen obligation tree", "", f"Item: `{ITEM}`", "",
        "The denominator was fixed from the exact statement and the visible high-level route of the selected",
        "immutable external candidate before any closure credit was assigned. The candidate source is not a",
        "repository dependency and its missing license, local replay, and transitive provenance prevent proof",
        "credit. The graph therefore records a conditional route, not a completed Quillen-Suslin proof.", "",
        "## Checked route and boundary", "",
        "The only locally checked proof path is `ROOT -> T-ROOT -> T-ADAPTER -> X-EXTERNAL-BODY`.",
        "`ObligationTree.lean` verifies that an all-natural-n field theorem would imply the frozen",
        "positive-variable root. `X-EXTERNAL-BODY` stays an explicit open premise. Its visible source route",
        "is expanded by refinement edges through finite-variable induction, Nagata monic production,",
        "local-to-global Quillen patching, fibre freeness, and the independent-universe ULift bridge.", "",
        "`proof_requires`/`composes` edges carry conditional machine-closure semantics. The current",
        "external route is typed as expository decomposition because its child-to-parent certificates are",
        "not locally available; it carries no closure credit. Source, provenance, evidence, trust,",
        "documentation, and workflow edges also carry no proof credit. The stronger",
        "older PID candidate is an alternative provenance record and is not a second numerator.", "",
        "## Obligation ledger", "",
        "Every semantic leaf has a structured boundary ledger and a split ceiling at most 100. The ceiling",
        "is not a measured proof length, R0, or proof evidence. Nodes describing the external source remain",
        "M3/M4 until immutable authorized local",
        "integration, exact kernel replay, composition, and master validation exist.", "",
    ]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    for row in obligations:
        node = node_by_id[row["obligation_id"]]
        anchor = row["obligation_id"].lower()
        lines += [f'<a id="{anchor}"></a>', f'### `{row["obligation_id"]}` - {node["kind"]}', "",
                  node["human_statement"], "",
                  f'- Formal target: `{node["formal_target"]}`',
                  f'- Output: {node["output"]}',
                  f'- Eligibility: machine `{row["machine_eligibility"]}`, human source `{row["human_source_eligibility"]}`, readable `{row["readable_eligibility"]}`',
                  f'- Current debt: `{node["human_debt"]}/{node["machine_debt"]}/{node["readability_debt"]}`; risk `{row["risk_class"]}`; local split ceiling `{node["step_budget"]}`',
                  f'- Premises: {json.dumps(node["semantic_step_ledger"]["premises"], ensure_ascii=True)}',
                  f'- Inference: `{node["semantic_step_ledger"]["inference"]}`',
                  f'- Outgoing use: {json.dumps(node["semantic_step_ledger"]["outgoing_use"], ensure_ascii=True)}',
                  f'- Structured ledger: {json.dumps(node["semantic_step_ledger"]["steps"], ensure_ascii=True)}',
                  f'- Boundary: {node["status_boundary"]}', ""]
    lines += ["## Root cut", "",
              "The root remains `H1/M3/R4`. The first machine cut is `M0034-X-EXTERNAL-BODY`; source,",
              "foundation, license, provenance, trust, readability, workflow, validation, release, and master",
              "acceptance remain separate open gates. No node in this registry is accepted closed.", ""]
    return registry, bundle, specs, "\n".join(lines)


def main() -> None:
    registry, bundle, specs, readable = build()
    for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle),
                        ("validation-specs.json", specs)):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    (HERE / "obligation-tree.md").write_text(readable, encoding="utf-8")
    print(f"wrote {len(registry['obligations'])} obligations and {bundle['typed_edge_count']} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
