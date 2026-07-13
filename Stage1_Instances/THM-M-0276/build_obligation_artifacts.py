#!/usr/bin/env python3
"""Build the frozen THM-M-0276 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0276-OBLIGATION_TREE"
THEOREM = "THM-M-0276"
PREFIX = "M0276"
ROOT_EXPRESSION = "0cfb9796471903d081ad67551a3f9c2c3414cce1f7adbf79394d364a467c82fa"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_BODY = (
    "mathlib@8a178386:Mathlib/Analysis/Normed/Operator/Banach.lean:227-248"
)
GRAPH_NAMES = (
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
)
RECIPE = "VAL-M0276-OBLIGATION-BUNDLE"


def digest(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


def spec(
    short: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    output: str,
    source: str,
    budget: int,
) -> dict[str, object]:
    return {
        "id": oid(short),
        "kind": kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "output": output,
        "source": source,
        "budget": budget,
    }


# No row carries candidate status. The denominator is computed from these architecture-only rows
# before the scheduler-visible anchor result is attached under status_observed_after_freeze.
SPECS = (
    spec("ROOT", "root", "critical", "For real and complex Banach spaces, every surjective bounded linear operator is open.", "Stage1Instances.THM_M_0276.BanachOpenMappingTarget", "The exact frozen real-and-complex conjunction.", "Statement.lean:32-34; expression sha256 0cfb9796...82fa", 12),
    spec("S-TARGET", "definition", "high", "Preserve both scalar branches, independent universes, complete normed-space instances, ordinary continuous linear maps, surjectivity, and IsOpenMap.", "Stage1Instances.THM_M_0276.{RealOpenMappingTarget,ComplexOpenMappingTarget,BanachOpenMappingTarget}", "The exact ordered root interface.", "Statement.lean:20-34", 20),
    spec("S-BOUNDARY", "definition", "high", "Retain trivial spaces, the zero map onto a trivial codomain, and noninjective surjections while excluding incomplete spaces and nonsurjective maps.", "the ordered binders and hypotheses of BanachOpenMappingTarget", "No strengthened or omitted boundary premise.", "Statement.lean:18-34; statement.json degenerate_cases", 18),
    spec("S-OPEN-EXPANSION", "transport", "high", "Expand IsOpenMap to openness of every image without changing scalar, operator, completeness, or surjectivity scope.", "Stage1Instances.THM_M_0276.banachOpenMappingTarget_iff_expandedOpenMappingTarget", "The checked open-image formulation.", "Statement.lean:36-57", 12),
    spec("S-FOUNDATION", "certificate", "critical", "Account for propositional extensionality, classical choice, quotient soundness, Lean, mathlib, imports, and the no-oracle policy.", "planned transitive foundation and TCB report", "An accepted logical-foundation boundary.", "AnchorAudit.lean axiom and closure probes", 24),
    spec("N-SAME-FIELD", "normalization", "high", "Specialize the pinned semilinear theorem to the identity scalar homomorphism for ordinary same-field Real and Complex maps.", "identity RingHomInvPair and RingHomIsometric specialization of ContinuousLinearMap.isOpenMap", "The exact same-field terminal interface.", "AnchorAudit.lean:49-56; Banach.lean:227-248", 22),
    spec("T-ASSEMBLE", "terminal", "critical", "Assemble the exact real and complex branch conclusions into the frozen conjunction.", "conjunction introduction inside Stage1Instances.THM_M_0276_Obligations.terminal_adapter", "The exact canonical conjunction.", "ObligationTree.lean#terminal_adapter", 10),
    spec("T-ADAPTER", "transport", "high", "Specialize the literal pinned semilinear terminal to identity scalar homomorphisms and assemble the exact Real-and-Complex root.", "Stage1Instances.THM_M_0276_Obligations.terminal_adapter", "The exact frozen root from the upstream terminal interface.", "ObligationTree.lean#terminal_adapter", 18),
    spec("T-UPSTREAM", "terminal", "critical", "Expose the literal polymorphic semilinear proposition proved by ContinuousLinearMap.isOpenMap without relocating its body.", "Stage1Instances.THM_M_0276_Obligations.MathlibTerminal", "The pinned semilinear open mapping proposition.", "ObligationTree.lean#pinned_mathlib_terminal; Banach.lean:227-248", 14),
    spec("B-REAL", "branch", "high", "Prove the real scalar branch at its exact binders.", "Stage1Instances.THM_M_0276.RealOpenMappingTarget", "The real Banach open mapping proposition.", "Statement.lean:20-25; Banach.lean:227-248", 18),
    spec("B-COMPLEX", "branch", "high", "Prove the complex scalar branch at its exact binders.", "Stage1Instances.THM_M_0276.ComplexOpenMappingTarget", "The complex Banach open mapping proposition.", "Statement.lean:27-31; Banach.lean:227-248", 18),
    spec("T-ISOPENMAP", "terminal", "critical", "Turn a positive controlled-preimage constant into a neighborhood of every image point and hence an open image.", "ContinuousLinearMap.isOpenMap", "IsOpenMap f for a surjective continuous linear map.", "Banach.lean:227-248", 30),
    spec("L-LOCAL-OPEN-BALL", "core_lemma", "high", "For y=f x in an open source image, choose an epsilon-ball around x and lift every nearby z through a controlled preimage of z-y.", "Metric.isOpen_iff; ContinuousLinearMap.map_add; Set.mem_image_of_mem", "The ball of radius epsilon/C around y lies in the image.", "Banach.lean:230-248", 24),
    spec("L-EXACT-PREIMAGE", "core_lemma", "critical", "Produce an exact preimage of every y with a uniform positive norm bound from half-error approximate preimages.", "ContinuousLinearMap.exists_preimage_norm_le", "There is C>0 with f x=y and norm x <= C*norm y.", "Banach.lean:160-225", 46),
    spec("C-APPROX-SELECTION", "construction", "high", "Choose an approximate-preimage function g and residual map h(y)=y-f(g y), preserving the half-error and norm bounds.", "Classical choice package immediately after exists_approx_preimage_norm_le", "Functions g and h with geometric residual contraction.", "Banach.lean:164-175", 24),
    spec("L-RESIDUAL-GEOMETRIC", "core_lemma", "high", "Inductively bound the nth residual and the nth approximate preimage by powers of one half.", "local hle, hnle, and ule estimates", "Geometric norm bounds for h^[n] y and u n.", "Banach.lean:171-188", 30),
    spec("L-SUMMABLE-SERIES", "core_lemma", "critical", "Use the geometric majorant and completeness of the domain to sum the approximate preimage series.", "Summable.of_nonneg_of_le; Summable.of_norm; tsum", "A limit x = sum' u with a controlled norm.", "Banach.lean:189-207", 36),
    spec("L-TELESCOPE", "core_lemma", "high", "Show that applying f to every finite partial sum telescopes to y minus the nth residual.", "local fsumeq induction", "f(sum i<n, u i)=y-h^[n] y.", "Banach.lean:208-213", 22),
    spec("L-LIMIT-IMAGE", "core_lemma", "critical", "Pass the partial-sum identity to the limit using continuity of f, residual convergence, and uniqueness of limits.", "HasSum.tendsto_sum_nat; Continuous.tendsto; tendsto_nhds_unique", "The series sum x satisfies f x=y.", "Banach.lean:214-225", 30),
    spec("L-APPROX-PREIMAGE", "core_lemma", "critical", "Use Baire category, rescaling, and two closure witnesses to approximate every y within half its norm while controlling the preimage norm.", "ContinuousLinearMap.exists_approx_preimage_norm_le", "There is C>=0 and an approximate controlled preimage for every y.", "Banach.lean:85-153", 48),
    spec("C-BAIRE-COVER", "construction", "critical", "Cover the codomain by the countable union of closures of images of radius-n balls using surjectivity.", "union n, closure (f '' Metric.ball 0 n) = Set.univ", "A countable closed cover of the complete codomain.", "Banach.lean:94-101", 24),
    spec("L-BAIRE-INTERIOR", "bridge", "critical", "Apply Baire category to the closed cover and extract a ball inside one closure.", "nonempty_interior_of_iUnion_of_closed", "Some closure(f '' ball 0 n) contains a nonempty open ball.", "Banach.lean:102-105; Topology/Baire/Lemmas.lean:243-248", 28),
    spec("L-RESCALE-SHELL", "bridge", "critical", "Rescale a nonzero y by a scalar whose norm lies in a controlled shell and retain inverse-norm control.", "rescale_to_shell", "A scalar d placing d*y inside the Baire ball with bounded inverse norm.", "Banach.lean:106-113; Analysis/Seminorm.lean:1379-1382", 30),
    spec("C-CLOSURE-PAIR", "construction", "critical", "Choose two nearby points in the image closure, subtract their preimages, and rescale the difference.", "Metric.mem_closure_iff; Set.mem_image; norm_sub_le", "The half-error approximate preimage and its norm estimate.", "Banach.lean:114-153", 54),
    spec("X-SOURCE", "terminal", "high", "Map every material analytic node to an approved proof source with exact assumptions, correction, errata, and independent review.", "node-specific primary-source crosswalk remains open", "Human-source evidence without machine proof credit.", "source-statement-crosswalk.md; known printed Baire-cover gap", 32),
    spec("X-PROVENANCE", "certificate", "critical", "Bind the adapter, terminal body, helper bodies, immutable source hashes, licenses, declaration closure, and replay evidence without duplicate credit.", "anchor-audit.json plus a future release provenance packet", "Proof-body provenance without mathematical proof credit.", "anchor-audit.json; anchor-audit-receipt.json", 36),
    spec("X-TRUST", "certificate", "critical", "Audit imported compiled artifacts, executables, transitive declarations, unsafe/oracle boundaries, and independent replay.", "Lean 4.29.0 and mathlib 8a178386 release trust closure", "Release-grade trust evidence without proof credit.", "anchor-audit.json immutable_environment; release gate pending", 38),
    spec("X-READABLE", "terminal", "high", "Provide a complete node-anchored reconstruction and independent functional-analysis review.", "planned readable reconstruction", "Readable coverage without machine proof credit.", "future readable proof surface", 40),
    spec("X-WORKFLOW", "certificate", "high", "Bind proof, validation, release, freshness, revocation, and independent verification tasks.", "planned Stage1 workflow receipts", "Dependency-legal workflow evidence without proof credit.", "task-dag.json and future accepted receipts", 24),
)


REQUIRES = {
    oid("ROOT"): [oid("T-ADAPTER"), oid("T-UPSTREAM")],
    oid("T-ADAPTER"): [oid("N-SAME-FIELD"), oid("T-ASSEMBLE")],
    oid("T-ASSEMBLE"): [oid("B-REAL"), oid("B-COMPLEX")],
    oid("T-UPSTREAM"): [oid("T-ISOPENMAP")],
    oid("T-ISOPENMAP"): [oid("L-LOCAL-OPEN-BALL"), oid("L-EXACT-PREIMAGE")],
    oid("L-LOCAL-OPEN-BALL"): [oid("L-EXACT-PREIMAGE")],
    oid("L-EXACT-PREIMAGE"): [
        oid("C-APPROX-SELECTION"),
        oid("L-RESIDUAL-GEOMETRIC"),
        oid("L-SUMMABLE-SERIES"),
        oid("L-TELESCOPE"),
        oid("L-LIMIT-IMAGE"),
    ],
    oid("C-APPROX-SELECTION"): [oid("L-APPROX-PREIMAGE")],
    oid("L-RESIDUAL-GEOMETRIC"): [oid("C-APPROX-SELECTION")],
    oid("L-SUMMABLE-SERIES"): [oid("L-RESIDUAL-GEOMETRIC")],
    oid("L-TELESCOPE"): [oid("C-APPROX-SELECTION")],
    oid("L-LIMIT-IMAGE"): [
        oid("L-SUMMABLE-SERIES"),
        oid("L-TELESCOPE"),
        oid("L-RESIDUAL-GEOMETRIC"),
    ],
    oid("L-APPROX-PREIMAGE"): [
        oid("C-BAIRE-COVER"),
        oid("L-BAIRE-INTERIOR"),
        oid("L-RESCALE-SHELL"),
        oid("C-CLOSURE-PAIR"),
    ],
    oid("L-BAIRE-INTERIOR"): [oid("C-BAIRE-COVER")],
    oid("C-CLOSURE-PAIR"): [oid("L-BAIRE-INTERIOR"), oid("L-RESCALE-SHELL")],
}

SOURCE_NA = {
    oid("S-OPEN-EXPANSION"),
    oid("S-FOUNDATION"),
    oid("N-SAME-FIELD"),
    oid("X-PROVENANCE"),
    oid("X-TRUST"),
    oid("X-READABLE"),
    oid("X-WORKFLOW"),
}
MACHINE_SPECIAL = {
    oid("X-SOURCE"): "not_applicable",
    oid("X-PROVENANCE"): "informational",
    oid("X-TRUST"): "informational",
    oid("X-READABLE"): "not_applicable",
    oid("X-WORKFLOW"): "informational",
}
READABLE_NA = {oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW")}
BODY_IDS = {
    oid("B-REAL"): MATHLIB_BODY,
    oid("B-COMPLEX"): MATHLIB_BODY,
    oid("T-ISOPENMAP"): MATHLIB_BODY,
    oid("T-UPSTREAM"): MATHLIB_BODY,
    oid("L-EXACT-PREIMAGE"): (
        "mathlib@8a178386:Mathlib/Analysis/Normed/Operator/Banach.lean:160-225"
    ),
    oid("L-APPROX-PREIMAGE"): (
        "mathlib@8a178386:Mathlib/Analysis/Normed/Operator/Banach.lean:85-153"
    ),
}


def exclusion(identifier: str, machine: str, source: str, readable: str) -> dict | None:
    if machine == source == readable == "required":
        return None
    if identifier == oid("X-SOURCE"):
        code = "human_source_boundary_only"
        reason = "This node carries human-source review and cannot receive machine proof credit."
    elif identifier == oid("X-READABLE"):
        code = "readability_boundary_only"
        reason = "This node carries readable reconstruction and cannot receive proof credit."
    elif machine == "required":
        code = "formal_interface_or_trust_only"
        reason = "This formal interface is not a separate human mathematical claim."
    else:
        code = "assurance_overlay_no_proof_credit"
        reason = "This assurance overlay is informational for proof coverage."
    return {
        "code": code,
        "justification": reason,
        "approval": "pending independent Stage1 integration review",
    }


def build() -> tuple[dict, dict, dict, str]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = []
    for row in SPECS:
        identifier = row["id"]
        machine = MACHINE_SPECIAL.get(identifier, "required")
        source = "not_applicable" if identifier in SOURCE_NA else "required"
        readable = "not_applicable" if identifier in READABLE_NA else "required"
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-TARGET")}
            else "planned:v1:sha256:"
            + digest(
                [
                    identifier,
                    row["kind"],
                    row["claim"],
                    row["formal"],
                    row["output"],
                ]
            )
        )
        obligations.append(
            {
                "obligation_id": identifier,
                "statement_fingerprint": fingerprint,
                "kind": row["kind"],
                "root_relevant": True,
                "machine_eligibility": machine,
                "human_source_eligibility": source,
                "readable_eligibility": readable,
                "risk_class": row["risk"],
                "exclusion_reason": exclusion(identifier, machine, source, readable),
                "terminal_proof_body_id": BODY_IDS.get(identifier),
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
    denominator = digest([{key: row[key] for key in fields} for row in obligations])
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "registry_id": "THM-M-0276-OBLIGATIONS-v1",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "frozen_at": "2026-07-13T23:40:00+08:00",
        "freeze_basis": "The exact elaborated statement and visible semantic architecture of the immutable pinned Banach source determine the registry. Eligibility and body deduplication do not depend on candidate acceptance status.",
        "freeze_order_boundary": "The scheduler exposes the predecessor anchor audit first. SPECS carries no observed status, its canonical projection is hashed first, and candidate observations are isolated below.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "canonical_projection_fields": list(fields),
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [
                row["obligation_id"]
                for row in obligations
                if row["machine_eligibility"] == "required"
            ],
            "required_human_source": [
                row["obligation_id"]
                for row in obligations
                if row["human_source_eligibility"] == "required"
            ],
            "required_readable": [
                row["obligation_id"]
                for row in obligations
                if row["readable_eligibility"] == "required"
            ],
            "informational_overlays": [
                row["obligation_id"]
                for row in obligations
                if row["machine_eligibility"] == "informational"
            ],
        },
        "distinct_terminal_proof_body_ids": sorted(set(BODY_IDS.values())),
        "deduplication_policy": "Real and Complex are distinct semantic branch obligations but share the same pinned generic terminal-body identity; wrappers, transports, and adapters receive no duplicate terminal-body credit.",
        "layer_exclusions": {
            "finite_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The analytic proof uses no finite certificate, native computation, solver, numerical experiment, or oracle.",
                "reviewer": "independent Stage1 integration lane",
            },
            "case_split": {
                "status": "represented",
                "reason": "The Real and Complex scalar branches are explicit and recombined at T-ASSEMBLE.",
                "reviewer": "independent Stage1 integration lane",
            },
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility, risk, edge-role, fingerprint, or proof-body identity change requires version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "closed_obligations": [],
            "accepted_root_machine_debt": "M3",
            "candidate_route": "M0276-C01 is an exact pinned M1/E2 candidate; it is not accepted closure and supplies no obligation credit in this phase.",
            "candidate_terminal_obligations": [oid("B-REAL"), oid("B-COMPLEX")],
            "candidate_closure_credit": False,
            "human_source_debt": "H2",
            "readability_debt": "R4",
        },
        "status_boundary": "Frozen architecture only. No obligation receives closure credit; the accepted root remains H2/M3/R4, and neither AUDIT-Z nor theorem completion is claimed.",
    }

    row_by_id = {row["id"]: row for row in SPECS}

    def ledger(row: dict[str, object]) -> list[dict[str, object]]:
        identifier = str(row["id"])
        children = REQUIRES.get(identifier, [])
        steps = []
        for index, child in enumerate(children, 1):
            steps.append(
                {
                    "step_id": f"{identifier}-STEP-{index:02d}",
                    "premise_ids": [child],
                    "inference": "consume the exact typed child output",
                    "source_locator": row_by_id[child]["source"],
                    "output": row_by_id[child]["output"],
                    "outgoing_use": f"composition of {identifier}",
                }
            )
        steps.append(
            {
                "step_id": f"{identifier}-STEP-{len(steps) + 1:02d}",
                "premise_ids": children if children else ["frozen-formal-context"],
                "inference": row["formal"],
                "source_locator": row["source"],
                "output": row["output"],
                "outgoing_use": "declared proof parent or typed non-proof support edge only",
            }
        )
        return steps

    nodes = []
    for row, obligation in zip(SPECS, obligations):
        identifier = str(row["id"])
        source_crosswalk = (
            "SRC-M0276-ROTEM-TZORANI-H2-GAP"
            if obligation["human_source_eligibility"] == "required"
            else "not-applicable"
        )
        provenance = (
            "PROV-M0276-C01-PARTIAL"
            if identifier in REQUIRES or identifier in BODY_IDS
            else "none"
        )
        owned = []
        if identifier in {
            oid("ROOT"),
            oid("T-ASSEMBLE"),
            oid("T-ADAPTER"),
            oid("T-UPSTREAM"),
            oid("S-TARGET"),
        }:
            owned.append("Stage1_Instances/THM-M-0276/ObligationTree.lean")
        if identifier in {oid("S-TARGET"), oid("S-BOUNDARY"), oid("S-OPEN-EXPANSION")}:
            owned.append("Stage1_Instances/THM-M-0276/Statement.lean")
        nodes.append(
            {
                "node_id": f"{THEOREM}-{identifier.removeprefix(PREFIX + '-')}",
                "obligation_id": identifier,
                "kind": row["kind"],
                "human_statement": row["claim"],
                "formal_target": row["formal"],
                "output": row["output"],
                "human_debt": "H2",
                "machine_debt": (
                    "M5"
                    if obligation["machine_eligibility"] == "not_applicable"
                    else "M3"
                ),
                "readability_debt": "R4",
                "evidence_ids": ["M0276-C01-E2-UNACCEPTED"]
                if identifier in REQUIRES or identifier in BODY_IDS
                else [],
                "source_crosswalk_id": source_crosswalk,
                "provenance_id": provenance,
                "foundation_profile": "Lean4-mathlib-classical candidate permits propext, Classical.choice, and Quot.sound; acceptance remains open",
                "tcb_profile": "Lean-4.29.0+mathlib-8a178386; compiled-artifact, executable, transitive, and independent release closure remains open",
                "computation_record": "none; no native evaluation, solver, numerical experiment, certificate, or oracle closes this node",
                "step_budget": row["budget"],
                "semantic_step_ledger": ledger(row),
                "public_readable_target": f"Stage1_Instances/THM-M-0276/obligation-tree.md#{identifier.lower()}",
                "validation_spec_id": RECIPE,
                "status_boundary": "Frozen architecture and unaccepted M1/E2 candidate mapping only; no M0, H0, R0, accepted proof, AUDIT-Z, or theorem completion is credited.",
                "task_ids": [ITEM],
                "owned_sources": owned,
                "owner": "THM-M-0276 execution lane",
                "reviewer": "independent Stage1 integration lane",
                "validity": {
                    "validated_at": "2026-07-13",
                    "review_due": "before proof acceptance and whenever an invalidation input changes",
                    "invalidation_inputs": [
                        "statement hash or expression",
                        "anchor hash or terminal-body identity",
                        "registry, graph, ledger, adapter, or recipe",
                        "Lean toolchain, dependency lock, mathlib pin, or source blob",
                        "source/readability review or assurance standard",
                    ],
                    "revocation_state": "not-accepted",
                },
            }
        )

    def edge(
        edge_id: str,
        source: str,
        edge_type: str,
        target: str,
        reciprocal: str | None = None,
        **extra: object,
    ) -> dict[str, object]:
        value: dict[str, object] = {
            "edge_id": edge_id,
            "from": source,
            "type": edge_type,
            "to": target,
        }
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        value.update(extra)
        return value

    proof = []
    for parent, children in REQUIRES.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            reverse = f"REV-{child}-{parent}"
            reverse_type = "composes" if parent == oid("ROOT") else "logical_decomposition"
            proof.extend(
                [
                    edge(req, parent, "proof_requires", child, reverse),
                    edge(reverse, child, reverse_type, parent, req),
                ]
            )

    refinement = [
        edge("REF-ROOT-TARGET", oid("ROOT"), "logical_decomposition", oid("S-TARGET")),
        edge("REF-ROOT-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY")),
        edge("REF-ROOT-EXPANSION", oid("ROOT"), "equivalent_to", oid("S-OPEN-EXPANSION")),
    ]
    for index, (parent, children) in enumerate(REQUIRES.items(), 1):
        if parent != oid("ROOT"):
            refinement.append(
                edge(
                    f"REF-SOURCE-BODY-{index:02d}",
                    parent,
                    "logical_decomposition",
                    children[0],
                    closure_role="unverified_source_body_decomposition",
                )
            )

    provenance = []
    evidence = []
    documentation = []
    for obligation in obligations:
        identifier = obligation["obligation_id"]
        if (
            identifier != oid("X-SOURCE")
            and obligation["human_source_eligibility"] == "required"
        ):
            provenance.append(
                edge(f"SOURCE-{identifier}", identifier, "source_map", oid("X-SOURCE"))
            )
        if identifier not in {
            oid("X-SOURCE"),
            oid("X-PROVENANCE"),
            oid("X-TRUST"),
            oid("X-READABLE"),
            oid("X-WORKFLOW"),
        }:
            provenance.append(
                edge(
                    f"PROVENANCE-{identifier}",
                    oid("X-PROVENANCE"),
                    "provenance_of",
                    identifier,
                )
            )
            evidence.append(
                edge(
                    f"EVIDENCE-{identifier}",
                    oid("X-PROVENANCE"),
                    "evidence_for",
                    identifier,
                    evidence_id="S56-M-0276-ANCHOR-AUDIT-WORKER-20260713",
                    accepted=False,
                )
            )
        if identifier != oid("X-READABLE"):
            documentation.append(
                edge(
                    f"DOCUMENT-{identifier}",
                    oid("X-READABLE"),
                    "documents",
                    identifier,
                )
            )

    trust = [
        edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
        edge("TRUST-ROOT-PROVENANCE", oid("ROOT"), "trusts", oid("X-PROVENANCE")),
        edge("TRUST-ROOT-TCB", oid("ROOT"), "trusts", oid("X-TRUST")),
        edge("TRUST-TERMINAL-TCB", oid("T-ISOPENMAP"), "trusts", oid("X-TRUST")),
    ]
    workflow_tasks = [
        "S56-M-0276-ANCHOR_AUDIT",
        ITEM,
        "S56-M-0276-PROOF",
        "S56-M-0276-VALIDATION",
        "S56-M-0276-RELEASE",
    ]
    workflow = [
        edge("FLOW-TREE-ANCHOR", ITEM, "workflow_depends_on", "S56-M-0276-ANCHOR_AUDIT"),
        edge("FLOW-PROOF-TREE", "S56-M-0276-PROOF", "workflow_depends_on", ITEM),
        edge("FLOW-VALIDATION-PROOF", "S56-M-0276-VALIDATION", "workflow_depends_on", "S56-M-0276-PROOF"),
        edge("FLOW-RELEASE-VALIDATION", "S56-M-0276-RELEASE", "workflow_depends_on", "S56-M-0276-VALIDATION"),
    ]
    edge_sets = {
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
        endpoints = workflow_tasks if name == "workflow" else ids
        incoming = {identifier: [] for identifier in endpoints}
        outgoing = {identifier: [] for identifier in endpoints}
        for record in edge_sets[name]:
            outgoing[str(record["from"])].append(str(record["edge_id"]))
            incoming[str(record["to"])].append(str(record["edge_id"]))
        graphs[name] = {"edges": edge_sets[name], "out": outgoing, "in": incoming}

    root_fingerprint = next(
        row["statement_fingerprint"]
        for row in obligations
        if row["obligation_id"] == oid("ROOT")
    )
    root_children = [oid("T-ADAPTER"), oid("T-UPSTREAM")]
    root_child_fingerprints = {
        child: next(
            row["statement_fingerprint"]
            for row in obligations
            if row["obligation_id"] == child
        )
        for child in root_children
    }
    plans = []
    for parent, children in REQUIRES.items():
        if parent == oid("ROOT"):
            continue
        plans.append(
            {
                "plan_id": f"DECOMP-{parent}",
                "parent_obligation_id": parent,
                "planned_child_ids": children,
                "source_declaration": (
                    "ContinuousLinearMap.isOpenMap"
                    if parent
                    in {
                        oid("T-ADAPTER"),
                        oid("T-ASSEMBLE"),
                        oid("T-UPSTREAM"),
                        oid("B-REAL"),
                        oid("B-COMPLEX"),
                        oid("T-ISOPENMAP"),
                    }
                    else "ContinuousLinearMap.exists_preimage_norm_le"
                    if parent in {
                        oid("L-LOCAL-OPEN-BALL"),
                        oid("L-EXACT-PREIMAGE"),
                        oid("C-APPROX-SELECTION"),
                        oid("L-RESIDUAL-GEOMETRIC"),
                        oid("L-SUMMABLE-SERIES"),
                        oid("L-TELESCOPE"),
                        oid("L-LIMIT-IMAGE"),
                    }
                    else "ContinuousLinearMap.exists_approx_preimage_norm_le"
                ),
                "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
                "required_future_certificate": "An exact abstract-child harness must bind these fingerprints and consume every child before parent closure.",
            }
        )

    proof_children = {child for children in REQUIRES.values() for child in children}
    proof_parents = set(REQUIRES)
    proof_leaf_cut_set = sorted(proof_children - proof_parents)
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id except workflow task IDs",
        "edge_direction": "proof_requires is parent-to-child; only the checked root reverse is composes; internal reverses remain logical_decomposition; workflow dependencies run task to prerequisite",
        "workflow_task_nodes": workflow_tasks,
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": [
            {
                "certificate_id": "COMP-M0276-ROOT",
                "parent_obligation_id": oid("ROOT"),
                "parent_statement_fingerprint": root_fingerprint,
                "required_child_ids": root_children,
                "required_child_statement_fingerprints": root_child_fingerprints,
                "fingerprint_binding_boundary": "The canonical parent fingerprint is the elaborated statement hash. Child fingerprints are frozen planned signatures and remain pending declaration-type fingerprint extraction before proof acceptance.",
                "checked_declarations": [
                    "Stage1Instances.THM_M_0276_Obligations.terminal_adapter",
                    "Stage1Instances.THM_M_0276_Obligations.pinned_mathlib_terminal",
                    "Stage1Instances.THM_M_0276_Obligations.compose_root",
                ],
                "certificate_kind": "lean_abstract_child_harness",
                "status": "provisionally_elaborated_not_accepted",
                "introduces_undeclared_premises": False,
                "accepted": False,
            }
        ],
        "unverified_decomposition_plans": plans,
        "closure_boundary": {
            "closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "proof_leaf_cut_set": proof_leaf_cut_set,
            "remaining_machine_root_cut_set": [oid("B-REAL"), oid("B-COMPLEX")],
            "remaining_release_cut_set": [
                oid("X-SOURCE"),
                oid("S-FOUNDATION"),
                oid("X-PROVENANCE"),
                oid("X-TRUST"),
                oid("X-READABLE"),
                oid("X-WORKFLOW"),
            ],
            "distinct_known_terminal_body_ids": sorted(set(BODY_IDS.values())),
            "candidate_evidence": "M0276-C01/E2/M1 is exact and locally checked but is not an accepted proof receipt.",
            "reason": "This phase freezes and structurally checks the architecture. Only the root adapter/composition is checked; internal source decompositions require future exact composition certificates and the proof phase must install accepted terminal closure.",
        },
    }

    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [
            {
                "recipe_id": RECIPE,
                "cwd": ".",
                "argv": [
                    "python3",
                    "-B",
                    "Stage1_Instances/THM-M-0276/check_obligation_tree.py",
                ],
                "env_allowlist": {
                    "LC_ALL": "C",
                    "TZ": "UTC",
                    "PATH": "runner-provided tool path",
                    "HOME": "runner-provided toolchain home",
                    "TMPDIR": "runner-provided temporary directory",
                    "PYTHONDONTWRITEBYTECODE": "1",
                },
                "timeout_seconds": 240,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [
                    {
                        "path_or_stream": "stdout",
                        "semantic_hash_policy": "contains PASS THM-M-0276 obligation tree with generated obligation, edge, and ledger counts",
                    },
                    {
                        "path_or_stream": "stdout",
                        "semantic_hash_policy": "contains accepted root H2/M3/R4, zero closed obligations, and theorem_complete=false",
                    },
                ],
                "covered_obligation_ids": ids,
                "covered_declarations": [
                    "Stage1Instances.THM_M_0276.BanachOpenMappingTarget",
                    "Stage1Instances.THM_M_0276_Obligations.ExactRoot",
                    "Stage1Instances.THM_M_0276_Obligations.exactRoot_iff_canonicalStatementCopy",
                    "Stage1Instances.THM_M_0276_Obligations.terminal_adapter",
                    "Stage1Instances.THM_M_0276_Obligations.pinned_mathlib_terminal",
                    "Stage1Instances.THM_M_0276_Obligations.compose_root",
                    "ContinuousLinearMap.exists_approx_preimage_norm_le",
                    "ContinuousLinearMap.exists_preimage_norm_le",
                    "ContinuousLinearMap.isOpenMap",
                ],
                "coverage_boundary": "The recipe structurally covers every registry node, while kernel coverage is limited to the named statement, adapter, composition, and audited candidate declarations. Internal source-body compositions remain open.",
            }
        ],
    }

    markdown = [
        "# THM-M-0276 frozen obligation architecture",
        "",
        f"Item: `{ITEM}`.",
        "",
        f"Registry version 1 freezes {len(ids)} canonical obligations before proof-phase closure",
        "credit. The architecture follows the visible pinned `Banach.lean` proof through the real",
        "and complex branches, controlled exact preimages, residual series, Baire cover, rescaling,",
        "closure witnesses, and the final open-image neighborhood argument. Provenance, evidence,",
        "trust, documentation, and workflow relations remain separate from proof premises.",
        "",
        "## Proof route",
        "",
        "```text",
        "ROOT -> exact adapter + literal pinned semilinear terminal",
        "  adapter -> Real and Complex branches + same-field normalization",
        "  upstream terminal -> IsOpenMap terminal",
        "    -> local open-ball image argument -> exact controlled preimages",
        "      -> approximate selection + residual contraction + geometric series",
        "        -> summability + telescoping + continuity/limit uniqueness",
        "      -> approximate controlled preimages",
        "        -> surjective Baire cover -> nonempty interior",
        "        -> scalar shell rescaling -> paired closure witnesses",
        "```",
        "",
        "Only the exact root adapter/composition is checked in this phase. Every internal relation",
        "is frozen as a source-body decomposition and remains unverified as child-to-parent",
        "composition until a later proof task supplies an exact abstract-child harness.",
        "",
        "## Node ledger",
        "",
    ]
    for row in SPECS:
        identifier = str(row["id"])
        markdown.extend(
            [
                f"### {identifier.lower()}",
                "",
                str(row["claim"]),
                "",
                f"Formal target: `{row['formal']}`. Output: {row['output']} Source boundary: {row['source']}.",
                f"Budget: {row['budget']} substantive steps maximum; structured ledger: {len(ledger(row))} recorded step(s).",
                "",
            ]
        )
    markdown.extend(
        [
            "## Freeze boundary",
            "",
            "All accepted machine obligations remain open at `M3`. Candidate `M0276-C01` is exact,",
            "pinned, sorry-free, and locally checked at `M1/E2`, but it is not installed by this",
            "obligation phase and has no accepted closure credit. The real and complex branches share",
            "one generic terminal-body identity and cannot inflate distinct-body coverage. The printed",
            "human-source Baire-cover gap, H0 and R0 independent reviews, complete provenance/TCB,",
            "hermetic replay, independent verification, AUDIT-Z, and theorem completion remain open.",
            "Any architectural or eligibility change requires a successor registry and append-only",
            "delta.",
            "",
        ]
    )
    return registry, bundle, specs, "\n".join(markdown)


def main() -> None:
    registry, bundle, specs, markdown = build()
    outputs = {
        "obligation-registry.json": json.dumps(registry, indent=2, ensure_ascii=True) + "\n",
        "typed-graphs.json": json.dumps(bundle, indent=2, ensure_ascii=True) + "\n",
        "validation-specs.json": json.dumps(specs, indent=2, ensure_ascii=True) + "\n",
        "obligation-tree.md": markdown,
    }
    for name, content in outputs.items():
        (HERE / name).write_text(content, encoding="utf-8")
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    ledger_count = sum(len(node["semantic_step_ledger"]) for node in bundle["nodes"])
    print(
        f"wrote {len(registry['obligations'])} obligations, {edge_count} typed edges, "
        f"and {ledger_count} substantive ledger steps"
    )
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
