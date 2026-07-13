#!/usr/bin/env python3
"""Build the frozen THM-M-0484 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0484-OBLIGATION_TREE"
THEOREM = "THM-M-0484"
PREFIX = "M0484"
ROOT_EXPRESSION = "6bd6024bd44d0bd9c50f6425b9ce5fdaecaf783ac84d32688717d3bde3151aea"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_BLOB = "36af70028d43c613055738999815ed2e88e84bd4"
MATHLIB_SOURCE = "6321c156165f59d49954c0e6e47706e765c0277df20b97a20333ceba29e8bead"
SUFFICIENCY_BODY = "sha256:8ec5fa60da0232f21b8a79ca9a7a846be51b71ed8b5bae0016943f880599efaf"
NECESSITY_BODY = "sha256:8f45e13a6d27e866e46e24320d770ad4c0a4e1b01412b2c32e708c00a29d01dd"
GRAPH_NAMES = (
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
)
CHECKER_RECIPE = "VAL-M0484-STRUCTURE"
LEAN_RECIPE = "VAL-M0484-LEAN-COMPOSITION"


def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(data).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


def exclusion(code: str, justification: str) -> dict[str, str]:
    return {
        "code": code,
        "justification": justification,
        "approval": "pending independent Stage1 integration review",
    }


# These architecture rows contain no observed closure status. Eligibility is therefore frozen before
# candidate state is attached below. The two final fields are machine and source eligibility.
ROWS = (
    ("ROOT", "root", "critical", "Prove the exact all-natural p >= 3 Lucas-Lehmer correctness iff frozen in Statement.lean.", "Stage1Instances.THM_M_0484.LucasLehmerTestTarget", "For every p >= 3, the test passes exactly when mersenne p is prime.", "required", "required"),
    ("S-TARGET", "definition", "high", "Preserve the ordered Nat binder, lower bound, iff direction, test predicate, and Nat.Prime conclusion.", "Stage1Instances.THM_M_0484.LucasLehmerTestTarget", "The exact canonical interface with no added or removed premise.", "required", "required"),
    ("S-ENCODINGS", "definition", "high", "Freeze mersenne, the integer/ZMod recurrences, zero-based residue index, and LucasLehmerTest vocabulary.", "mersenne; LucasLehmer.s; sZMod; sMod; lucasLehmerResidue; LucasLehmerTest", "The exact objects appearing in every proof branch.", "required", "required"),
    ("S-BOUNDARY", "branch", "high", "Retain every natural p >= 3, including composite p, while excluding 0, 1, and the genuine p = 2 counterexample.", "Stage1Instances.THM_M_0484.exponentTwo_boundary and canonical lower bound", "An exhaustive low-exponent and domain boundary policy.", "required", "required"),
    ("S-TRANSPORT", "transport", "high", "Relate the test predicate to ZMod and reduced-integer residues without changing theorem scope.", "lucasLehmerTestTarget_iff_residueTarget; lucasLehmerTestTarget_iff_integerResidueTarget", "Two checked representation transports with no extra proof-body credit.", "required", "not_applicable"),
    ("S-FOUNDATION", "certificate", "critical", "Audit the selected axioms, kernel, imported modules, compiled artifacts, and no-oracle computation policy.", "planned transitive foundation and TCB report", "An accepted foundation, trust, and computation boundary.", "required", "not_applicable"),
    ("N-INDEX", "normalization", "high", "Write p = p' + 2 and reduce p - 2 to p' in both terminal directions.", "natural subtraction/index normalization in both terminal bodies", "A shared normalized exponent and recurrence index.", "required", "required"),
    ("T-ASSEMBLE", "terminal", "critical", "Consume the exact forward and reverse conclusions and construct the canonical iff.", "root_of_directions then root_of_terminal", "Stage1Instances.THM_M_0484.LucasLehmerTestTarget", "required", "required"),
    ("T-SUFFICIENCY", "terminal", "critical", "Prove that a passing Lucas-Lehmer test implies primality at the canonical lower bound.", "SufficiencyTarget; pinned lucas_lehmer_sufficiency", "LucasLehmerTest p -> Nat.Prime (mersenne p).", "required", "required"),
    ("B-SUFF-CONTRA", "branch", "critical", "Contrapose primality and derive a contradiction between order and minimum-factor bounds.", "sufficiency_of_order_and_minFac", "The exact forward direction from both inequalities.", "required", "required"),
    ("L-ORDER-INEQ", "core_lemma", "critical", "Bound 2^(p'+2) below the square of the least Mersenne factor using the omega unit order.", "OrderInequalityTarget; orderInequality_of_order_and_card; LucasLehmer.order_ineq", "2^(p'+2) < q(p'+2)^2.", "required", "required"),
    ("L-ORDER-OMEGA", "core_lemma", "critical", "Prove that the quadratic-extension unit omega has exact order 2^(p'+2).", "OmegaOrderTarget; omegaOrder_of_power_boundaries; LucasLehmer.order_omega", "orderOf omegaUnit = 2^(p'+2).", "required", "required"),
    ("C-OMEGA-UNIT", "construction", "high", "Bundle omega with omegab as its inverse and preserve the coercion back to the quadratic extension.", "LucasLehmer.omegaUnit; omega_mul_omegab; omegab_mul_omega", "A unit whose powers are compared in X (q p).", "required", "required"),
    ("L-OMEGA-NEGONE", "core_lemma", "critical", "Derive omega^(2^(p'+1)) = -1 from the recurrence divisibility formula.", "OmegaPowNegOneTarget; omegaPowNegOne_of_formula_and_vanishing; omega_pow_eq_neg_one", "The lower power boundary excluding smaller powers equal to one.", "required", "required"),
    ("L-OMEGA-ONE", "core_lemma", "high", "Square the negative-one identity to obtain omega^(2^(p'+2)) = 1.", "OmegaPowOneTarget; omegaPowOne_of_negOne; omega_pow_eq_one", "The upper power boundary showing order divisibility.", "required", "required"),
    ("L-OMEGA-FORMULA", "core_lemma", "critical", "Use residue divisibility and the closed recurrence form to isolate omega^(2^(p'+1)).", "OmegaFormulaTarget; LucasLehmer.omega_pow_formula", "The integer-coefficient Mersenne multiple formula.", "required", "required"),
    ("C-X-RING", "construction", "critical", "Construct X q = ZMod q x ZMod q with its quadratic-extension ring, omega, and inverse.", "LucasLehmer.X and its CommRing/CharP structures", "The ring hosting the order and trace arguments.", "required", "required"),
    ("L-CLOSED-FORM", "core_lemma", "critical", "Prove s i = omega^(2^i) + omegab^(2^i) in X q.", "ClosedFormTarget; LucasLehmer.X.closed_form", "A closed form connecting recurrence residues to powers.", "required", "required"),
    ("L-MERSENNE-VANISH", "core_lemma", "high", "Show mersenne p maps to zero in X (q p) because q p is its least factor.", "MersenneCoeXTarget; LucasLehmer.mersenne_coe_X", "The Mersenne coefficient vanishes in the omega formula.", "required", "required"),
    ("C-MINFAC", "construction", "high", "Choose q p as the positive minimum factor of mersenne p and expose its value as Nat.minFac.", "LucasLehmer.q", "A positive least-factor object shared by order and primality bounds.", "required", "required"),
    ("L-MINFAC-SQUARE", "core_lemma", "critical", "For a nonprime positive Mersenne number, bound the square of its least factor by the number.", "MinFacSquareBoundTarget; Nat.minFac_sq_le_self", "q p ^ 2 <= mersenne p.", "required", "required"),
    ("L-X-CARD-UNITS", "core_lemma", "critical", "Bound the omega order by the unit group and show that group has fewer than q^2 elements.", "UnitCardBoundTarget; X.card_eq; X.card_units_lt", "Fintype.card (X q)^* < q^2.", "required", "required"),
    ("L-TWO-LT-Q", "core_lemma", "high", "Prove that the least Mersenne factor is larger than two for p' + 2.", "TwoLtQTarget; LucasLehmer.two_lt_q", "A nondegeneracy fact excluding one = negative one in ZMod q.", "required", "required"),
    ("T-NECESSITY", "terminal", "critical", "Prove that prime mersenne p implies a passing Lucas-Lehmer test.", "NecessityTarget; pinned lucas_lehmer_necessity", "Nat.Prime (mersenne p) -> LucasLehmerTest p.", "required", "required"),
    ("B-NEC-TRACE", "branch", "critical", "Reduce the reverse direction to the recurrence representation, closed form, and zero trace in X (mersenne p).", "necessity_of_recurrence_closedForm_trace", "The exact reverse direction from the three child conclusions.", "required", "required"),
    ("N-RECURRENCE-X", "normalization", "critical", "Transport the ZMod recurrence to the integer recurrence and then into the quadratic extension first component.", "RecurrenceBridgeTarget; sZMod_eq_s; X.fst_intCast", "The canonical residue represented as the first component of the closed form.", "required", "required"),
    ("N-PRIME-EXPONENT", "normalization", "high", "Derive primality, oddness, and non-two facts for p from primality of mersenne p.", "Nat.Prime.of_mersenne and odd_of_ne_two", "The exponent facts required by the Legendre-symbol branch.", "required", "required"),
    ("L-LEGENDRE-TWO", "core_lemma", "high", "Show that 2 is a quadratic residue modulo the prime Mersenne number.", "legendreSym_mersenne_two", "legendreSym (mersenne p) 2 = 1.", "required", "required"),
    ("L-LEGENDRE-THREE", "core_lemma", "high", "Show that 3 is a quadratic nonresidue modulo the prime Mersenne number.", "legendreSym_mersenne_three", "legendreSym (mersenne p) 3 = -1.", "required", "required"),
    ("L-OMEGA-TRACE", "core_lemma", "critical", "Use the Legendre facts to prove the zero trace of the required omega power.", "MersenneTraceTarget; LucasLehmer.X.omega_pow_trace", "omega^(2^p') + omegab^(2^p') = 0.", "required", "required"),
    ("C-X-FROBENIUS", "construction", "critical", "Build the quadratic Frobenius/power identities through alpha, omega, and characteristic q.", "X.one_add_alpha_pow_q; two_mul_omega_pow; pow_omega", "The half-power identity consumed by omega_pow_trace.", "required", "required"),
    ("X-SOURCE", "terminal", "critical", "Map the exact statement and every material proof node to an approved primary source, assumptions, and errata.", "non-machine primary-source crosswalk", "Human-source evidence without machine proof credit.", "not_applicable", "required"),
    ("X-PROVENANCE", "certificate", "critical", "Bind terminal bodies, source slices, transitive declarations, revisions, artifacts, licenses, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without semantic proof credit.", "informational", "not_applicable"),
    ("X-TRUST", "certificate", "critical", "Close imported-olean, executable TCB, foundation, computation, and no-unsafe/no-oracle boundaries.", "planned trust and TCB closure", "Release trust evidence without semantic proof credit.", "informational", "not_applicable"),
    ("X-READABLE", "terminal", "high", "Provide and independently review a complete node-anchored readable reconstruction.", "planned readable reconstruction", "Readable coverage without machine proof credit.", "not_applicable", "not_applicable"),
    ("X-WORKFLOW", "certificate", "high", "Bind proof, validation, release, freshness, revocation, and independent verification tasks.", "planned Stage1 workflow receipts", "Workflow acceptance without proof credit.", "informational", "not_applicable"),
)


TERMINAL_BODIES = {
    oid("T-SUFFICIENCY"): SUFFICIENCY_BODY,
    oid("T-NECESSITY"): NECESSITY_BODY,
    oid("T-ASSEMBLE"): "local:Stage1_Instances/THM-M-0484/ObligationTree.lean#root_of_directions+root_of_terminal",
}
CHECKED_INTERFACES = {
    oid("S-TARGET"),
    oid("S-TRANSPORT"),
    oid("T-ASSEMBLE"),
    oid("T-SUFFICIENCY"),
    oid("B-SUFF-CONTRA"),
    oid("L-ORDER-INEQ"),
    oid("L-ORDER-OMEGA"),
    oid("L-OMEGA-NEGONE"),
    oid("L-OMEGA-ONE"),
    oid("B-NEC-TRACE"),
    oid("T-NECESSITY"),
}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []

    for short, kind, risk, claim, target, output, machine, human_source in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-TARGET")}
            else "planned:v1:sha256:" + digest([identifier, kind, claim, target, output])
        )
        excluded = None
        if machine != "required" or human_source != "required":
            if human_source == "not_applicable" and machine == "required":
                excluded = exclusion(
                    "formal_encoding_or_trust_only",
                    "This formal interface or trust boundary is not a separate human mathematical claim.",
                )
            elif identifier == oid("X-SOURCE"):
                excluded = exclusion(
                    "human_source_boundary_only",
                    "This node carries human-source review and never receives machine proof credit.",
                )
            elif identifier == oid("X-READABLE"):
                excluded = exclusion(
                    "readability_boundary_only",
                    "This node carries readable reconstruction and never receives machine or human-source proof credit.",
                )
            else:
                excluded = exclusion(
                    "assurance_overlay_no_proof_credit",
                    "This provenance, trust, or workflow overlay is informational for proof coverage.",
                )
        obligations.append(
            {
                "obligation_id": identifier,
                "statement_fingerprint": fingerprint,
                "kind": kind,
                "root_relevant": identifier not in {oid("X-PROVENANCE"), oid("X-WORKFLOW")},
                "machine_eligibility": machine,
                "human_source_eligibility": human_source,
                "readable_eligibility": (
                    "not_applicable"
                    if identifier in {oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW")}
                    else "required"
                ),
                "risk_class": risk,
                "exclusion_reason": excluded,
                "terminal_proof_body_id": TERMINAL_BODIES.get(identifier),
            }
        )

    fields = (
        "obligation_id",
        "statement_fingerprint",
        "kind",
        "root_relevant",
        "machine_eligibility",
        "human_source_eligibility",
        "readable_eligibility",
        "risk_class",
        "exclusion_reason",
        "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in fields} for row in obligations]
    denominator = digest(projection)
    ids = [row["obligation_id"] for row in obligations]

    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0484-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T22:11:46+08:00",
        "freeze_basis": "The exact elaborated statement plus the visible semantic architecture of the immutable pinned terminal source. Eligibility is derived from claim roles and source-body structure, not from observed candidate closure.",
        "freeze_order_boundary": "Scheduler order exposed the predecessor anchor audit, but ROWS contains no status and is hashed before status_observed_after_freeze is attached.",
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
            "finite_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The universal correctness proof uses no finite certificate, solver, native computation, oracle, or experiment. Concrete Mersenne-prime examples are explicitly deduplicated boundary evidence.",
                "reviewer": "independent Stage1 integration lane",
            }
        },
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility change, edge-role change, or terminal-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "candidate_machine_classification": "M1",
            "candidate_evidence_level": "E2_nonrelease_worker_probe",
            "candidate_terminal_obligations": [oid("T-SUFFICIENCY"), oid("T-NECESSITY")],
            "candidate_closure_credit": False,
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope, eligibility, and denominators only. Exact terminals remain candidate-only; the recorded provisional H1/M3/R4 vector, AUDIT-Z, and theorem completion do not change.",
    }

    nodes: list[dict] = []
    for row, source_row in zip(obligations, ROWS):
        short, kind, risk, claim, target, output, _, _ = source_row
        identifier = row["obligation_id"]
        candidate = identifier in {oid("T-SUFFICIENCY"), oid("T-NECESSITY")}
        checked = identifier in CHECKED_INTERFACES
        machine_debt = "M3" if row["machine_eligibility"] == "required" else "M4"
        source_crosswalk = (
            "not-applicable"
            if row["human_source_eligibility"] == "not_applicable"
            else "source-map:v1:pending-pinpoint-and-independent-review"
        )
        provenance_id = (
            f"pinned-mathlib:{MATHLIB_REVISION}:{MATHLIB_BLOB}:{row['terminal_proof_body_id']}"
            if candidate
            else "conditional-local-composition:v1"
            if checked
            else "none"
        )
        owned_sources: list[str] = []
        if checked:
            owned_sources.append("Stage1_Instances/THM-M-0484/ObligationTree.lean")
        if identifier in {oid("S-TARGET"), oid("S-TRANSPORT"), oid("S-BOUNDARY")}:
            owned_sources.append("Stage1_Instances/THM-M-0484/Statement.lean")
        if candidate:
            owned_sources.append("Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/LucasLehmer.lean")
        nodes.append(
            {
                "node_id": f"{THEOREM}-{short}",
                "obligation_id": identifier,
                "kind": kind,
                "human_statement": claim,
                "formal_target": target,
                "output": output,
                "human_debt": "H1",
                "machine_debt": machine_debt,
                "candidate_machine_classification": "M1" if candidate else None,
                "candidate_evidence_level": "E2_nonrelease_worker_probe" if candidate else None,
                "interface_check_status": (
                    "kernel_checked_conditional_no_closure_credit" if checked else "not_checked_in_this_phase"
                ),
                "closure_credit": False,
                "readability_debt": "R4",
                "evidence_ids": [],
                "source_crosswalk_id": source_crosswalk,
                "provenance_id": provenance_id,
                "foundation_profile": "lean4-dependent-type-theory; allowed candidate axioms propext/Classical.choice/Quot.sound; acceptance pending",
                "tcb_profile": "lean-4.29.0+mathlib-8a178386; complete serialized closure, imported oleans, executables, and independent replay pending",
                "computation_record": "none; no finite computation, native code, solver, oracle, experiment, or unchecked certificate is credited",
                "step_budget": 55 if risk == "critical" else 30,
                "semantic_step_ledger": {
                    "premises": "Only the exact typed proof children and formal context named in the graph; source/trust/documentation/workflow overlays are not premises.",
                    "inference": claim,
                    "output": output,
                    "outgoing_use": "Only the declared proof parent or typed non-proof support edge may consume this output.",
                    "substantive_step_cap": 55 if risk == "critical" else 30,
                    "split_rule": "Split before proof acceptance if implementation exposes more substantive steps or hidden branch, construction, transport, or imported theorem work.",
                },
                "public_readable_target": (
                    f"Stage1_Instances/THM-M-0484/obligation-tree.md#{identifier.lower()}"
                    if identifier
                    in {
                        oid("ROOT"), oid("S-TARGET"), oid("S-ENCODINGS"), oid("S-BOUNDARY"),
                        oid("S-TRANSPORT"), oid("S-FOUNDATION"), oid("N-INDEX"),
                        oid("T-ASSEMBLE"), oid("T-SUFFICIENCY"), oid("B-SUFF-CONTRA"),
                        oid("T-NECESSITY"), oid("B-NEC-TRACE"), oid("X-SOURCE"),
                        oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
                    }
                    else "Stage1_Instances/THM-M-0484/obligation-tree.md#visible-source-expansion"
                ),
                "validation_spec_id": LEAN_RECIPE if checked else CHECKER_RECIPE,
                "status_boundary": (
                    "Exact pinned terminal candidate only; no proof-phase installation, accepted M0, or root closure."
                    if candidate
                    else "Frozen architecture or conditional interface only; no accepted proof, H0, R0, AUDIT-Z, or theorem completion."
                ),
                "task_ids": [ITEM, "S56-M-0484-PROOF", "S56-M-0484-VALIDATION"],
                "owned_sources": owned_sources,
                "owner": "THM-M-0484 proof lane",
                "reviewer": "independent Stage1 integration lane",
                "validity": {
                    "validated_at": "2026-07-13" if checked else None,
                    "review_due": "before proof acceptance and whenever an invalidation input changes",
                    "invalidation_inputs": [
                        "Statement.lean or canonical expression",
                        "anchor-audit.json or terminal body identity",
                        "obligation registry, graph, composition harness, or recipe",
                        "Lean toolchain, dependency lock, mathlib pin, or source blob",
                        "source/readability review or assurance standard",
                    ],
                    "revocation_state": "provisional" if checked else "open",
                },
            }
        )

    def edge(edge_id: str, source: str, edge_type: str, target: str, **extra: object) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        value.update(extra)
        return value

    # Every proof pair below has an actual named Lean certificate. The graph deliberately does not
    # pretend that the rest of the upstream source expansion has checked child-to-parent composition.
    checked_pairs = (
        (oid("ROOT"), oid("T-ASSEMBLE"), "root_of_terminal"),
        (oid("T-ASSEMBLE"), oid("T-SUFFICIENCY"), "root_of_directions"),
        (oid("T-ASSEMBLE"), oid("T-NECESSITY"), "root_of_directions"),
        (oid("T-SUFFICIENCY"), oid("B-SUFF-CONTRA"), "sufficiency_of_branch"),
        (oid("B-SUFF-CONTRA"), oid("L-ORDER-INEQ"), "sufficiency_of_order_and_minFac"),
        (oid("B-SUFF-CONTRA"), oid("L-MINFAC-SQUARE"), "sufficiency_of_order_and_minFac"),
        (oid("L-ORDER-INEQ"), oid("L-ORDER-OMEGA"), "orderInequality_of_order_and_card"),
        (oid("L-ORDER-INEQ"), oid("L-X-CARD-UNITS"), "orderInequality_of_order_and_card"),
        (oid("L-ORDER-OMEGA"), oid("L-OMEGA-NEGONE"), "omegaOrder_of_power_boundaries"),
        (oid("L-ORDER-OMEGA"), oid("L-OMEGA-ONE"), "omegaOrder_of_power_boundaries"),
        (oid("L-ORDER-OMEGA"), oid("L-TWO-LT-Q"), "omegaOrder_of_power_boundaries"),
        (oid("L-OMEGA-ONE"), oid("L-OMEGA-NEGONE"), "omegaPowOne_of_negOne"),
        (oid("L-OMEGA-NEGONE"), oid("L-OMEGA-FORMULA"), "omegaPowNegOne_of_formula_and_vanishing"),
        (oid("L-OMEGA-NEGONE"), oid("L-MERSENNE-VANISH"), "omegaPowNegOne_of_formula_and_vanishing"),
        (oid("T-NECESSITY"), oid("B-NEC-TRACE"), "necessity_of_branch"),
        (oid("B-NEC-TRACE"), oid("N-RECURRENCE-X"), "necessity_of_recurrence_closedForm_trace"),
        (oid("B-NEC-TRACE"), oid("L-CLOSED-FORM"), "necessity_of_recurrence_closedForm_trace"),
        (oid("B-NEC-TRACE"), oid("L-OMEGA-TRACE"), "necessity_of_recurrence_closedForm_trace"),
    )
    proof: list[dict] = []
    for index, (parent, child, certificate) in enumerate(checked_pairs, start=1):
        req = f"PROOF-REQ-{index:02d}"
        comp = f"PROOF-COMP-{index:02d}"
        declaration = f"Stage1Instances.THM_M_0484.ObligationTree.{certificate}"
        proof.extend(
            [
                edge(req, parent, "proof_requires", child, reciprocal_edge_id=comp, composition_declaration=declaration),
                edge(comp, child, "composes", parent, reciprocal_edge_id=req, composition_declaration=declaration),
            ]
        )

    decomposition_pairs = (
        (oid("L-ORDER-OMEGA"), oid("C-OMEGA-UNIT")),
        (oid("L-OMEGA-FORMULA"), oid("L-CLOSED-FORM")),
        (oid("L-OMEGA-FORMULA"), oid("N-RECURRENCE-X")),
        (oid("L-OMEGA-FORMULA"), oid("C-X-RING")),
        (oid("L-MERSENNE-VANISH"), oid("C-MINFAC")),
        (oid("L-X-CARD-UNITS"), oid("C-X-RING")),
        (oid("L-X-CARD-UNITS"), oid("C-MINFAC")),
        (oid("L-X-CARD-UNITS"), oid("L-TWO-LT-Q")),
        (oid("L-MINFAC-SQUARE"), oid("C-MINFAC")),
        (oid("L-TWO-LT-Q"), oid("C-MINFAC")),
        (oid("L-OMEGA-TRACE"), oid("L-LEGENDRE-TWO")),
        (oid("L-OMEGA-TRACE"), oid("L-LEGENDRE-THREE")),
        (oid("L-OMEGA-TRACE"), oid("C-X-FROBENIUS")),
        (oid("L-OMEGA-TRACE"), oid("C-X-RING")),
        (oid("L-LEGENDRE-THREE"), oid("N-PRIME-EXPONENT")),
        (oid("B-SUFF-CONTRA"), oid("N-INDEX")),
        (oid("B-NEC-TRACE"), oid("N-INDEX")),
    )
    refinement = [
        edge("REF-ROOT-TARGET", oid("ROOT"), "logical_decomposition", oid("S-TARGET"), closure_role="root_required_refinement"),
        edge("REF-ROOT-ENC", oid("ROOT"), "logical_decomposition", oid("S-ENCODINGS"), closure_role="root_required_refinement"),
        edge("REF-ROOT-BOUND", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY"), closure_role="root_required_refinement"),
        edge("REF-ROOT-TRANSPORT", oid("ROOT"), "logical_decomposition", oid("S-TRANSPORT"), closure_role="root_required_refinement"),
    ]
    refinement.extend(
        edge(
            f"REF-SOURCE-BODY-{index:02d}",
            parent,
            "source_body_decomposition",
            child,
            closure_role="unverified_as_child_to_parent_composition",
            future_certificate_required=True,
        )
        for index, (parent, child) in enumerate(decomposition_pairs, start=1)
    )

    semantic_ids = [
        identifier
        for identifier in ids
        if identifier not in {oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")}
    ]
    provenance = [
        edge(f"SRC-MAP-{index:02d}", oid("X-SOURCE"), "source_map", identifier)
        for index, identifier in enumerate(semantic_ids, start=1)
    ] + [
        edge("PROV-SUFF-BODY", oid("X-PROVENANCE"), "provenance_of", oid("T-SUFFICIENCY")),
        edge("PROV-NEC-BODY", oid("X-PROVENANCE"), "provenance_of", oid("T-NECESSITY")),
        edge("PROV-LOCAL-COMP", oid("X-PROVENANCE"), "provenance_of", oid("T-ASSEMBLE")),
    ]
    evidence = [
        edge("EVID-ANCHOR-SUFF", oid("X-PROVENANCE"), "evidence_for", oid("T-SUFFICIENCY"), evidence_id="S56-M-0484-ANCHOR-AUDIT-WORKER-20260713", accepted=False),
        edge("EVID-ANCHOR-NEC", oid("X-PROVENANCE"), "evidence_for", oid("T-NECESSITY"), evidence_id="S56-M-0484-ANCHOR-AUDIT-WORKER-20260713", accepted=False),
        edge("EVID-COMPOSITION", oid("X-WORKFLOW"), "evidence_for", oid("T-ASSEMBLE"), evidence_id="S56-M-0484-OBLIGATION-TREE-WORKER-20260713", accepted=False),
    ]
    trust = [
        edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
        edge("TRUST-ROOT-PROVENANCE", oid("ROOT"), "trusts", oid("X-PROVENANCE")),
        edge("TRUST-ROOT-TCB", oid("ROOT"), "trusts", oid("X-TRUST")),
        edge("TRUST-SUFF-TCB", oid("T-SUFFICIENCY"), "trusts", oid("X-TRUST")),
        edge("TRUST-NEC-TCB", oid("T-NECESSITY"), "trusts", oid("X-TRUST")),
    ]
    documentation = [
        edge(f"DOC-READABLE-{index:02d}", oid("X-READABLE"), "documents", identifier)
        for index, identifier in enumerate(semantic_ids, start=1)
    ] + [
        edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        edge("DOC-PROVENANCE-TERMINALS", oid("X-PROVENANCE"), "documents", oid("T-ASSEMBLE")),
    ]
    workflow = [
        edge("FLOW-WORKFLOW-PROOF", oid("X-WORKFLOW"), "workflow_depends_on", oid("T-ASSEMBLE")),
        edge("FLOW-WORKFLOW-SOURCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
        edge("FLOW-WORKFLOW-PROVENANCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
        edge("FLOW-WORKFLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
        edge("FLOW-WORKFLOW-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
    ]
    graph_edges = {
        "proof": proof,
        "refinement": refinement,
        "provenance": provenance,
        "evidence": evidence,
        "trust": trust,
        "documentation": documentation,
        "workflow": workflow,
    }
    graphs = {}
    for name in GRAPH_NAMES:
        outgoing = {identifier: [] for identifier in ids}
        incoming = {identifier: [] for identifier in ids}
        for record in graph_edges[name]:
            outgoing[record["from"]].append(record["edge_id"])
            incoming[record["to"]].append(record["edge_id"])
        graphs[name] = {"edges": graph_edges[name], "out": outgoing, "in": incoming}

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child and reciprocal composes is child-to-parent; source_body_decomposition is never machine closure",
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": [
            {
                "certificate_id": f"COMP-M0484-{name}",
                "parent_obligation_ids": sorted(
                    {
                        parent
                        for parent, _child, certificate in checked_pairs
                        if certificate == name
                    }
                ),
                "required_child_ids_by_parent": {
                    parent: [
                        child
                        for candidate_parent, child, certificate in checked_pairs
                        if candidate_parent == parent and certificate == name
                    ]
                    for parent in sorted(
                        {
                            parent
                            for parent, _child, certificate in checked_pairs
                            if certificate == name
                        }
                    )
                },
                "required_child_statement_fingerprints": {
                    child: next(
                        row["statement_fingerprint"]
                        for row in obligations
                        if row["obligation_id"] == child
                    )
                    for parent, child, certificate in checked_pairs
                    if certificate == name
                },
                "declaration": f"Stage1Instances.THM_M_0484.ObligationTree.{name}",
                "certificate_kind": "lean_abstract_child_harness",
                "status": "provisionally_elaborated_not_accepted",
                "introduces_undeclared_premises": False,
                "accepted": False,
            }
            for name in (
                "root_of_directions",
                "root_of_terminal",
                "sufficiency_of_branch",
                "sufficiency_of_order_and_minFac",
                "necessity_of_branch",
                "orderInequality_of_order_and_card",
                "omegaOrder_of_power_boundaries",
                "omegaPowOne_of_negOne",
                "omegaPowNegOne_of_formula_and_vanishing",
                "necessity_of_recurrence_closedForm_trace",
            )
        ],
        "unverified_decomposition_plans": [
            {
                "plan_id": f"DECOMP-{parent}-{child}",
                "parent": parent,
                "child": child,
                "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
                "required_before_parent_machine_acceptance": True,
                "required_future_certificate": "An exact abstract-child harness must bind the parent and child fingerprints and consume the child before parent closure.",
            }
            for parent, child in decomposition_pairs
        ],
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "candidate_terminal_obligations": [oid("T-SUFFICIENCY"), oid("T-NECESSITY")],
            "candidate_classification": "M1",
            "candidate_closure_credit": False,
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_machine_root_cut_set": [oid("T-SUFFICIENCY"), oid("T-NECESSITY")],
            "remaining_release_cut_set": [oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "reason": "The two exact terminals are pinned E2/M1 candidates. E1 release evidence required for M0-W, proof-phase installation, internal source-decomposition certificates, accepted provenance/trust, source/readability reviews, and master acceptance remain open.",
        },
    }

    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [
            {
                "recipe_id": CHECKER_RECIPE,
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0484/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 120,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0484 obligation tree"}],
                "covered_obligation_ids": ids,
                "covered_declarations": [],
                "coverage_boundary": "Schema, hashes, graph semantics, source markers, receipt, and open-state consistency only; this recipe supplies no kernel closure for any declaration.",
            },
            {
                "recipe_id": LEAN_RECIPE,
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0484/check_obligation_tree.py", "--run-lean"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains Lean composition: pass and no sorryAx"}],
                "covered_obligation_ids": sorted(CHECKED_INTERFACES),
                "covered_declarations": [
                    "Stage1Instances.THM_M_0484.ObligationTree.root_of_directions",
                    "Stage1Instances.THM_M_0484.ObligationTree.root_of_terminal",
                    "Stage1Instances.THM_M_0484.ObligationTree.sufficiency_of_branch",
                    "Stage1Instances.THM_M_0484.ObligationTree.sufficiency_of_order_and_minFac",
                    "Stage1Instances.THM_M_0484.ObligationTree.necessity_of_branch",
                    "Stage1Instances.THM_M_0484.ObligationTree.orderInequality_of_order_and_card",
                    "Stage1Instances.THM_M_0484.ObligationTree.omegaOrder_of_power_boundaries",
                    "Stage1Instances.THM_M_0484.ObligationTree.omegaPowOne_of_negOne",
                    "Stage1Instances.THM_M_0484.ObligationTree.omegaPowNegOne_of_formula_and_vanishing",
                    "Stage1Instances.THM_M_0484.ObligationTree.necessity_of_recurrence_closedForm_trace",
                    "lucas_lehmer_sufficiency",
                    "lucas_lehmer_necessity",
                ],
                "coverage_boundary": "Kernel-checks conditional composition interfaces and inspects pinned terminal types only. It does not install terminal proofs or validate planned internal source-body decompositions.",
            },
        ],
    }
    return registry, bundle, specs


def main() -> None:
    values = build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), values
    ):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    edge_count = sum(len(graph["edges"]) for graph in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {values[0]['denominator_sha256']}")


if __name__ == "__main__":
    main()
