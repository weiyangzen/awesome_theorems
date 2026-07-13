#!/usr/bin/env python3
"""Build the frozen THM-M-0626 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0626-OBLIGATION_TREE"
THEOREM = "THM-M-0626"
PREFIX = "M0626-"
ROOT_EXPRESSION = "5c32b45abf131975cd4673ca095ca1a8e0122e4104bf616a4afab09a03289231"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
GRAPH_NAMES = (
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
)
TASK_IDS = (
    "S56-M-0626-INTAKE",
    "S56-M-0626-STATEMENT",
    "S56-M-0626-ANCHOR_AUDIT",
    "S56-M-0626-OBLIGATION_TREE",
    "S56-M-0626-PROOF",
    "S56-M-0626-VALIDATION",
    "S56-M-0626-RELEASE",
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def step(
    identifier: str,
    number: int,
    premise_ids: list[str],
    inference: str,
    source_locator: str,
    output: str,
    outgoing_use: str,
) -> dict:
    return {
        "step_id": f"{identifier}-STEP-{number:02d}",
        "premise_ids": premise_ids,
        "inference": inference,
        "source_locator": source_locator,
        "output": output,
        "outgoing_use": outgoing_use,
    }


def stable_premise_id(identifier: str, number: int, premise: str) -> str:
    if premise.startswith(PREFIX):
        return "OUT-" + premise
    if premise.startswith("OUT-") or premise.startswith("P-"):
        return premise
    return f"P-{identifier}-{number:02d}-{digest(premise)[:12]}"


# short id, kind, risk, human statement, formal target, output, machine eligibility,
# human-source eligibility, terminal proof-body identity, semantic step budget
ROWS = (
    (
        "ROOT", "root", "critical",
        "Every globally continuous map sends every nonempty connected subset of an arbitrary topological space to a nonempty connected direct image.",
        "Stage1Instances.THM_M_0626.ConnectedImageTarget",
        "The exact universe-polymorphic canonical proposition.",
        "required", "required", None, 8,
    ),
    (
        "S-INTERFACE", "definition", "high",
        "Freeze both universes, arbitrary topological-space instances, the subset, IsConnected hypothesis, total map, global Continuous hypothesis, and direct-image conclusion.",
        "Stage1Instances.THM_M_0626.ConnectedImageTarget",
        "The exact ordered binder and conclusion interface.",
        "required", "not_applicable", None, 14,
    ),
    (
        "S-CONNECTEDNESS", "definition", "high",
        "Expose IsConnected s as the conjunction of s.Nonempty and IsPreconnected s, on both source and image.",
        "IsConnected; Stage1Instances.THM_M_0626.connectedImageTarget_iff_expanded",
        "Two typed components for image connectedness without changing the empty-set convention.",
        "required", "not_applicable",
        "repo:Stage1Instances.THM_M_0626.connectedImageTarget_iff_expanded", 12,
    ),
    (
        "S-BOUNDARY", "definition", "high",
        "Exclude the empty source while retaining singleton sources, constant maps, noninjective maps, and arbitrary non-Hausdorff spaces.",
        "empty_source_not_connected; singleton_image_connected; constant_image_connected",
        "The exact degenerate-case boundary of the canonical claim.",
        "required", "not_applicable", None, 16,
    ),
    (
        "S-GLOBAL-LOCAL", "transport", "high",
        "Transport each global Continuous f premise to ContinuousOn f s in the direction needed by the sharper local theorem.",
        "Stage1Instances.THM_M_0626.ObligationTree.GlobalToLocalContinuityPackage",
        "ContinuousOn f s, with no unclaimed converse.",
        "required", "not_applicable",
        "repo:Stage1Instances.THM_M_0626.ObligationTree.globalToLocalContinuity", 10,
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Fix Lean dependent type theory, classical/extensional/quotient axioms, direct imports, computation policy, and the transitive TCB boundary.",
        "Lean 4.29.0 foundation and transitive axiom/trust report",
        "A provisional inventory of foundation, computation, and TCB acceptance requirements.",
        "required", "not_applicable", None, 32,
    ),
    (
        "N-IMAGE-COVER-TO-SOURCE", "normalization", "high",
        "Rewrite the image cover f '' s subset u union v as a cover s subset u' union v' using the relative-preimage identities.",
        "Set.image_subset_iff; Set.preimage_union; union/intersection identities",
        "The source cover s subset u' union v'.",
        "required", "required", None, 22,
    ),
    (
        "N-SEPARATION-GOAL", "reduction", "critical",
        "Reduce image preconnectedness to arbitrary open u and v, an image cover, and witnesses that the image meets each.",
        "IsPreconnected definition for f '' s",
        "A witness that f '' s meets u intersection v.",
        "required", "required", None, 20,
    ),
    (
        "C-RELATIVE-PREIMAGES", "construction", "high",
        "Construct source-open representatives u' and v' for the relative preimages of u and v.",
        "continuousOn_iff'",
        "Open u', v' and their relative-preimage identities.",
        "required", "required", None, 30,
    ),
    (
        "N-WITNESS-PULLBACK", "normalization", "high",
        "Pull the two image-intersection witnesses back to source witnesses in s intersection u' and s intersection v'.",
        "Set.mem_image; relative-preimage identities",
        "Nonempty source intersections s with u' and s with v'.",
        "required", "required", None, 18,
    ),
    (
        "L-SOURCE-INTERSECTION", "core_lemma", "critical",
        "Apply source IsPreconnected to u' and v' and the pulled-back endpoint witnesses.",
        "IsPreconnected s",
        "A source witness z in s intersection u' intersection v'.",
        "required", "required", None, 24,
    ),
    (
        "T-INTERSECTION-PUSHFORWARD", "transport", "critical",
        "Rewrite the source overlap witness with the relative-preimage identities and map it through f into the image overlap.",
        "Set.mem_image; relative-preimage identities",
        "A witness in f '' s intersection (u intersection v).",
        "required", "required", None, 20,
    ),
    (
        "L-IMAGE-PRECONNECTED", "core_lemma", "critical",
        "Push the source intersection witness through f and discharge the complete arbitrary-open-set definition of image preconnectedness.",
        "IsPreconnected.image",
        "IsPreconnected (f '' s).",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:IsPreconnected.image", 22,
    ),
    (
        "L-IMAGE-NONEMPTY", "core_lemma", "normal",
        "Map a source nonempty witness through f to prove the direct image is nonempty.",
        "Set.image_nonempty.mpr",
        "(f '' s).Nonempty.",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:Set.image_nonempty.mpr+IsConnected.nonempty", 6,
    ),
    (
        "A-ISCONNECTED-IMAGE", "bridge", "critical",
        "Pair image nonemptiness with image preconnectedness to obtain the exact local-continuity connected-image theorem.",
        "IsConnected.image",
        "Stage1Instances.THM_M_0626.ObligationTree.LocalConnectedImagePackage",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:IsConnected.image", 8,
    ),
    (
        "T-LOCAL-COMPOSE", "terminal", "high",
        "Consume the explicit nonempty-image and preconnected-image packages to recompose the complete local IsConnected image conclusion.",
        "Stage1Instances.THM_M_0626.ObligationTree.localConnectedImage_of_components",
        "The exact local-continuity package, conditional on both components.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0626.ObligationTree.localConnectedImage_of_components", 10,
    ),
    (
        "T-ASSEMBLE", "terminal", "critical",
        "Consume the local connected-image package and global-to-local continuity transport to yield the exact canonical root.",
        "Stage1Instances.THM_M_0626.ObligationTree.root_of_localConnectedImage",
        "Stage1Instances.THM_M_0626.ConnectedImageTarget",
        "required", "required",
        "repo:Stage1Instances.THM_M_0626.ObligationTree.root_of_localConnectedImage", 10,
    ),
    (
        "X-SOURCE", "terminal", "high",
        "Map the root and each substantive topological step to a pinpoint primary proof source, assumptions, errata, and independent review.",
        "node-specific primary-source crosswalk pending",
        "Human-source coverage without machine proof credit.",
        "not_applicable", "required", None, 48,
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Bind wrappers, terminal bodies, source slices, direct and transitive declarations, revisions, licenses, and duplicate-body identities.",
        "pinned mathlib body and declaration provenance closure pending",
        "Formal provenance without mathematical proof credit.",
        "informational", "not_applicable", None, 48,
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit Lean, mathlib, compiled artifacts, axioms, unsafe/oracle boundaries, replay, and supply-chain trust transitively.",
        "Lean 4.29.0 and mathlib 8a178386 transitive trust closure pending",
        "Release-grade trust inventory without mathematical proof credit.",
        "informational", "not_applicable", None, 48,
    ),
    (
        "X-READABLE", "terminal", "high",
        "Provide and independently review a node-specific readable reconstruction of the open-set pullback proof.",
        "reviewed readable reconstruction pending",
        "Readable coverage without machine proof credit.",
        "not_applicable", "required", None, 64,
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind proof installation, validation, release, freshness, revocation, and independent-verification acceptance.",
        "Stage1 proof to validation to release workflow receipts pending",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", None, 24,
    ),
)


CHECKED_INTERFACES = {
    oid("S-INTERFACE"),
    oid("S-CONNECTEDNESS"),
    oid("S-BOUNDARY"),
    oid("S-GLOBAL-LOCAL"),
    oid("T-LOCAL-COMPOSE"),
    oid("T-ASSEMBLE"),
}
SOURCE_NA = {
    oid("S-INTERFACE"), oid("S-CONNECTEDNESS"), oid("S-BOUNDARY"),
    oid("S-GLOBAL-LOCAL"), oid("S-FOUNDATION"), oid("X-PROVENANCE"),
    oid("X-TRUST"), oid("X-WORKFLOW"),
}

LEDGERS = {
    oid("ROOT"): [
        step(oid("ROOT"), 1, [oid("T-ASSEMBLE")],
             "Stage1Instances.THM_M_0626.ObligationTree.root_of_exactAssembly",
             "ObligationTree.lean:145-149",
             "Stage1Instances.THM_M_0626.ConnectedImageTarget",
             "canonical theorem and release decision"),
    ],
    oid("S-INTERFACE"): [
        step(oid("S-INTERFACE"), 1, ["statement-expression-sha256:" + ROOT_EXPRESSION],
             "Read the fixed universes, topology instances, subset, map, hypotheses, and direct-image conclusion without alteration.",
             "Statement.lean:13-22",
             "the exact ordered binder and conclusion interface",
             oid("ROOT")),
    ],
    oid("S-CONNECTEDNESS"): [
        step(oid("S-CONNECTEDNESS"), 1, ["Mathlib.IsConnected-definition"],
             "Stage1Instances.THM_M_0626.connectedImageTarget_iff_expanded",
             "Statement.lean:24-34; Mathlib/Topology/Connected/Basic.lean:50-56",
             "source and image connectedness exposed as Nonempty and IsPreconnected",
             oid("T-LOCAL-COMPOSE")),
    ],
    oid("S-BOUNDARY"): [
        step(oid("S-BOUNDARY"), 1, ["Mathlib.IsConnected-definition"],
             "empty_source_not_connected fixes the nonempty convention; singleton_image_connected and constant_image_connected retain included edge cases.",
             "Statement.lean:76-102",
             "empty source excluded while singleton and constant-map cases remain included",
             oid("ROOT")),
    ],
    oid("S-GLOBAL-LOCAL"): [
        step(oid("S-GLOBAL-LOCAL"), 1, ["Continuous f"],
             "Continuous.continuousOn",
             "ObligationTree.lean:79-87",
             "ContinuousOn f s",
             oid("T-ASSEMBLE")),
    ],
    oid("S-FOUNDATION"): [
        step(oid("S-FOUNDATION"), 1,
             ["terminal-declaration-closure", "lean-toolchain-pin", "mathlib-pin"],
             "Future validation compares machine-derived axioms, compiled imports, and TCB elements with the selected profiles.",
             "instance.json foundation_profile/tcb_profile/computation_profile",
             "provisional foundation, axiom, computation, and TCB acceptance requirements",
             "release gate for " + oid("ROOT")),
    ],
    oid("N-IMAGE-COVER-TO-SOURCE"): [
        step(oid("N-IMAGE-COVER-TO-SOURCE"), 1,
             [oid("C-RELATIVE-PREIMAGES"), "image-cover:f''s-subset-u-union-v"],
             "Rewrite by Set.image_subset_iff and Set.preimage_union, intersect with s, and substitute both relative-preimage identities.",
             "Mathlib/Topology/Connected/Basic.lean:280-284; ObligationTree.lean:35-40",
             "s subset u' union v'",
             oid("N-SEPARATION-GOAL")),
    ],
    oid("N-SEPARATION-GOAL"): [
        step(oid("N-SEPARATION-GOAL"), 1,
             [oid("C-RELATIVE-PREIMAGES"), oid("N-IMAGE-COVER-TO-SOURCE"),
              oid("N-WITNESS-PULLBACK"), oid("L-SOURCE-INTERSECTION"),
              oid("T-INTERSECTION-PUSHFORWARD")],
             "Stage1Instances.THM_M_0626.ObligationTree.separationEngine_of_components",
             "ObligationTree.lean:89-103",
             "the arbitrary-open SeparationEngine",
             oid("L-IMAGE-PRECONNECTED")),
    ],
    oid("C-RELATIVE-PREIMAGES"): [
        step(oid("C-RELATIVE-PREIMAGES"), 1,
             ["ContinuousOn f s", "IsOpen u", "IsOpen v"],
             "Apply continuousOn_iff' independently to u and v.",
             "Mathlib/Topology/ContinuousOn.lean:116-125; ObligationTree.lean:26-33",
             "open u', v' with f preimage u intersect s = u' intersect s and the analogous v identity",
             oid("N-SEPARATION-GOAL")),
    ],
    oid("N-WITNESS-PULLBACK"): [
        step(oid("N-WITNESS-PULLBACK"), 1,
             [oid("C-RELATIVE-PREIMAGES"), "image-hit-u", "image-hit-v"],
             "Destructure each Set.mem_image witness and rewrite membership through its relative-preimage identity.",
             "Mathlib/Topology/Connected/Basic.lean:276-289; ObligationTree.lean:42-48",
             "(s intersect u').Nonempty and (s intersect v').Nonempty",
             oid("N-SEPARATION-GOAL")),
    ],
    oid("L-SOURCE-INTERSECTION"): [
        step(oid("L-SOURCE-INTERSECTION"), 1,
             ["IsPreconnected s", oid("N-IMAGE-COVER-TO-SOURCE"), oid("N-WITNESS-PULLBACK")],
             "Apply the defining arbitrary-open eliminator of IsPreconnected s to u' and v'.",
             "Mathlib/Topology/Connected/Basic.lean:50-52,285-288; ObligationTree.lean:50-55",
             "(s intersect (u' intersect v')).Nonempty",
             oid("N-SEPARATION-GOAL")),
    ],
    oid("T-INTERSECTION-PUSHFORWARD"): [
        step(oid("T-INTERSECTION-PUSHFORWARD"), 1,
             [oid("C-RELATIVE-PREIMAGES"), oid("L-SOURCE-INTERSECTION")],
             "Rewrite the source overlap with both relative-preimage identities and map its witness through f.",
             "Mathlib/Topology/Connected/Basic.lean:289-292; ObligationTree.lean:57-62",
             "(f '' s intersect (u intersect v)).Nonempty",
             oid("N-SEPARATION-GOAL")),
    ],
    oid("L-IMAGE-PRECONNECTED"): [
        step(oid("L-IMAGE-PRECONNECTED"), 1, [oid("N-SEPARATION-GOAL")],
             "Stage1Instances.THM_M_0626.ObligationTree.imagePreconnected_of_separationEngine",
             "ObligationTree.lean:105-110",
             "ImagePreconnectedPackage, hence IsPreconnected (f '' s)",
             oid("T-LOCAL-COMPOSE")),
    ],
    oid("L-IMAGE-NONEMPTY"): [
        step(oid("L-IMAGE-NONEMPTY"), 1, ["IsConnected.nonempty"],
             "Set.image_nonempty.mpr maps a source witness through f.",
             "Mathlib/Topology/Connected/Basic.lean:295-297; ObligationTree.lean:15-18",
             "(f '' s).Nonempty",
             oid("T-LOCAL-COMPOSE")),
    ],
    oid("A-ISCONNECTED-IMAGE"): [
        step(oid("A-ISCONNECTED-IMAGE"), 1, ["anchor-audit:M0626-C01-MATHLIB-DIRECT"],
             "Treat pinned IsConnected.image as the audited exact candidate interface; record the local body reconstruction only as a deduplicated refinement route.",
             "anchor-audit.json M0626-C01; pinned Basic.lean:295-297",
             "candidate exact ContinuousOn connected-image interface",
             oid("T-ASSEMBLE")),
    ],
    oid("T-LOCAL-COMPOSE"): [
        step(oid("T-LOCAL-COMPOSE"), 1,
             [oid("L-IMAGE-NONEMPTY"), oid("L-IMAGE-PRECONNECTED")],
             "Stage1Instances.THM_M_0626.ObligationTree.localConnectedImage_of_components",
             "ObligationTree.lean:112-118",
             "LocalConnectedImagePackage",
             "deduplicated local reconstruction of " + oid("A-ISCONNECTED-IMAGE")),
    ],
    oid("T-ASSEMBLE"): [
        step(oid("T-ASSEMBLE"), 1,
             [oid("S-GLOBAL-LOCAL"), oid("A-ISCONNECTED-IMAGE")],
             "Stage1Instances.THM_M_0626.ObligationTree.exactAssembly_of_packages",
             "ObligationTree.lean:126-143",
             "ExactAssembly, definitionally the canonical target",
             oid("ROOT")),
    ],
    oid("X-SOURCE"): [
        step(oid("X-SOURCE"), 1,
             ["Stacks-tag-0376-source-lead", "primary-source-review-pending"],
             "Future independent review maps exact assumptions, transitions, conclusion, and errata to every required human-source node.",
             "source-statement-crosswalk.md; anchor-audit.json",
             "provisional source crosswalk with H0 acceptance still open",
             "AUDIT-Z and theorem release gate"),
    ],
    oid("X-PROVENANCE"): [
        step(oid("X-PROVENANCE"), 1,
             ["anchor-audit:M0626-C01-MATHLIB-DIRECT", "anchor-audit:M0626-C02-MATHLIB-SUBSTRATE"],
             "Future audit resolves wrapper, terminal body, declarations, revisions, source hashes, licenses, and aliases transitively.",
             "anchor-audit.json; pinned Basic.lean:274-297",
             "transitive provenance closure without duplicate proof credit",
             "validation and release gates"),
    ],
    oid("X-TRUST"): [
        step(oid("X-TRUST"), 1,
             [oid("S-FOUNDATION"), oid("X-PROVENANCE"), "machine-derived-axiom-report"],
             "Future validation checks compiled artifacts, axioms, unsafe/oracle boundaries, supply chain, and replay.",
             "obligation-tree-receipt.json axiom_and_placeholder_result; instance.json tcb_profile",
             "provisional trust inventory with transitive acceptance still open",
             "validation and release gates"),
    ],
    oid("X-READABLE"): [
        step(oid("X-READABLE"), 1,
             [oid("X-SOURCE"), "all-root-proof-obligations"],
             "Future independent review checks the node-anchored mathematical reconstruction and leaf ledgers.",
             "obligation-tree.md",
             "provisional readable route with independent R0 acceptance still open",
             "AUDIT-Z and theorem release gate"),
    ],
    oid("X-WORKFLOW"): [
        step(oid("X-WORKFLOW"), 1,
             ["accepted-task-receipts", oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE")],
             "Apply the typed task DAG, freshness, revocation, independent-verification, and release policies.",
             "Docs/Stage1_Execution_DAG_rev-5.6.json; task-dag.json",
             "dependency-legal acceptance and release inputs",
             "master acceptance decision"),
    ],
}

PREMISE_CLAIMS = {}
for _identifier, _entries in LEDGERS.items():
    for _entry in _entries:
        _premise_ids = []
        for _index, _premise in enumerate(_entry["premise_ids"], 1):
            _premise_id = stable_premise_id(_identifier, _index, _premise)
            _premise_ids.append(_premise_id)
            if _premise_id.startswith("P-"):
                PREMISE_CLAIMS[_premise_id] = _premise
        _entry["premise_ids"] = _premise_ids

PROOF_TASK_OBLIGATIONS = {
    oid(short) for short in (
        "ROOT", "T-ASSEMBLE", "S-GLOBAL-LOCAL", "A-ISCONNECTED-IMAGE",
        "T-LOCAL-COMPOSE", "L-IMAGE-NONEMPTY", "L-IMAGE-PRECONNECTED",
        "N-SEPARATION-GOAL", "C-RELATIVE-PREIMAGES", "N-IMAGE-COVER-TO-SOURCE",
        "N-WITNESS-PULLBACK", "L-SOURCE-INTERSECTION", "T-INTERSECTION-PUSHFORWARD",
    )
}
INTAKE_TASK_OBLIGATIONS = {oid("ROOT"), oid("S-INTERFACE"), oid("X-SOURCE")}
STATEMENT_TASK_OBLIGATIONS = {
    oid("ROOT"), oid("S-INTERFACE"), oid("S-CONNECTEDNESS"),
    oid("S-BOUNDARY"), oid("S-GLOBAL-LOCAL"),
}
ANCHOR_TASK_OBLIGATIONS = {
    oid("A-ISCONNECTED-IMAGE"), oid("L-IMAGE-PRECONNECTED"),
    oid("L-IMAGE-NONEMPTY"), oid("X-PROVENANCE"), oid("X-TRUST"),
}


def task_roles(identifier: str) -> list[dict]:
    result = [
        {"task_id": TASK_IDS[3], "role": "freezes"},
        {"task_id": TASK_IDS[5], "role": "validates"},
        {"task_id": TASK_IDS[6], "role": "accepts_or_rejects"},
    ]
    for obligations, task_id, role in (
        (INTAKE_TASK_OBLIGATIONS, TASK_IDS[0], "scopes"),
        (STATEMENT_TASK_OBLIGATIONS, TASK_IDS[1], "defines_or_checks"),
        (ANCHOR_TASK_OBLIGATIONS, TASK_IDS[2], "audits_candidate"),
        (PROOF_TASK_OBLIGATIONS, TASK_IDS[4], "implements_or_installs"),
        ({oid("X-READABLE")}, TASK_IDS[4], "reconstructs"),
    ):
        if identifier in obligations:
            result.append({"task_id": task_id, "role": role})
    return sorted(result, key=lambda value: TASK_IDS.index(value["task_id"]))


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []

    exclusion_reasons = {
        oid("S-INTERFACE"): "formal_statement_interface_human_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-CONNECTEDNESS"): "formal_definition_overlay_human_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-BOUNDARY"): "formal_boundary_fixture_human_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-GLOBAL-LOCAL"): "formal_transport_human_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_mathematical_claim_pending_reviewer_acceptance",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-PROVENANCE"): "release_provenance_overlay_no_proof_credit_pending_integration_review",
        oid("X-TRUST"): "release_trust_overlay_no_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
    }

    for short, kind, risk, claim, target, output, machine, human_source, body, budget in ROWS:
        identifier = oid(short)
        if identifier in {oid("ROOT"), oid("S-INTERFACE")}:
            fingerprint = f"lean-expression-sha256:{ROOT_EXPRESSION}"
        else:
            fingerprint = "planned:v1:sha256:" + digest(
                [identifier, kind, claim, target, output]
            )
        root_relevant = True
        obligations.append(
            {
                "obligation_id": identifier,
                "statement_fingerprint": fingerprint,
                "kind": kind,
                "root_relevant": root_relevant,
                "machine_eligibility": machine,
                "human_source_eligibility": human_source,
                "readable_eligibility": "required",
                "risk_class": risk,
                "exclusion_reason": exclusion_reasons.get(identifier),
                "terminal_proof_body_id": body,
            }
        )

        if identifier == oid("ROOT") or identifier in CHECKED_INTERFACES or body is not None:
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        if identifier == oid("A-ISCONNECTED-IMAGE"):
            candidate_status = "M0-W_candidate_pending_proof_phase_and_master_acceptance"
        elif identifier in CHECKED_INTERFACES:
            candidate_status = "M0-L_worker_checked_interface_pending_master_acceptance"
        elif body and body.startswith("mathlib:"):
            candidate_status = "pinned_mathlib_support_candidate_pending_proof_and_master_acceptance"
        else:
            candidate_status = None
        if identifier == oid("A-ISCONNECTED-IMAGE"):
            provenance = "anchor-audit:M0626-C01-MATHLIB-DIRECT"
        elif identifier == oid("L-IMAGE-PRECONNECTED"):
            provenance = "anchor-audit:M0626-C02-MATHLIB-SUBSTRATE"
        elif identifier in {oid("T-LOCAL-COMPOSE"), oid("T-ASSEMBLE")}:
            provenance = "local-conditional-composition"
        elif body and body.startswith("mathlib:"):
            provenance = "pinned-visible-terminal-chain"
        else:
            provenance = "none"
        statement_owned = {
            oid("ROOT"), oid("S-INTERFACE"), oid("S-CONNECTEDNESS"), oid("S-BOUNDARY")
        }
        obligation_owned = {
            oid("S-GLOBAL-LOCAL"), oid("N-IMAGE-COVER-TO-SOURCE"),
            oid("N-SEPARATION-GOAL"), oid("C-RELATIVE-PREIMAGES"),
            oid("N-WITNESS-PULLBACK"), oid("L-SOURCE-INTERSECTION"),
            oid("T-INTERSECTION-PUSHFORWARD"), oid("L-IMAGE-PRECONNECTED"),
            oid("L-IMAGE-NONEMPTY"), oid("A-ISCONNECTED-IMAGE"),
            oid("T-LOCAL-COMPOSE"), oid("T-ASSEMBLE"),
        }
        owned_sources = []
        if identifier in obligation_owned:
            owned_sources = ["Stage1_Instances/THM-M-0626/ObligationTree.lean"]
        elif identifier in statement_owned:
            owned_sources = ["Stage1_Instances/THM-M-0626/Statement.lean"]

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
                "machine_candidate_status": candidate_status,
                "readability_debt": "R4",
                "evidence_ids": [],
                "source_crosswalk_id": (
                    "not-applicable-pending-review"
                    if identifier in SOURCE_NA else "primary-source-node-map-pending"
                ),
                "provenance_id": provenance,
                "foundation_profile": "lean4-dependent-type-theory; accepted axiom policy and transitive review pending",
                "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive declaration and replay closure pending",
                "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
                "step_budget": len(LEDGERS[identifier]),
                "semantic_step_ledger": LEDGERS[identifier],
                "public_readable_target": f"Stage1_Instances/THM-M-0626/obligation-tree.md#{identifier.lower()}",
                "validation_spec_id": f"VAL-{identifier}",
                "status_boundary": "Frozen architecture, audited candidate, or conditional interface only; no accepted root proof or theorem completion.",
                "task_ids": [entry["task_id"] for entry in task_roles(identifier)],
                "owned_sources": owned_sources,
                "owner": "THM-M-0626 proof lane",
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
            }
        )

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
        "registry_id": "THM-M-0626-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T21:48:24+08:00",
        "freeze_basis": "The exact frozen statement and the visible open-set-pullback architecture disclosed by the prerequisite anchor audit. The registry was frozen before proof-phase installation or accepted closure metrics; candidate availability is not used to change eligibility, risks, or denominators.",
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
        "layer_applicability": {
            "S_statement_foundation": {
                "status": "required",
                "obligation_ids": [oid(short) for short in ("S-INTERFACE", "S-CONNECTEDNESS", "S-BOUNDARY", "S-GLOBAL-LOCAL", "S-FOUNDATION")],
            },
            "N_normalization_and_reduction": {"status": "required", "obligation_ids": [oid("N-IMAGE-COVER-TO-SOURCE"), oid("N-WITNESS-PULLBACK"), oid("N-SEPARATION-GOAL")]},
            "B_branch": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The proof introduces arbitrary opens but contains no mathematical case split; N-SEPARATION-GOAL is a reduction node, not a branch.",
                "obligation_ids": [],
            },
            "C_construction": {"status": "required", "obligation_ids": [oid("C-RELATIVE-PREIMAGES")]},
            "L_core_lemma": {"status": "required", "obligation_ids": [oid(short) for short in ("L-SOURCE-INTERSECTION", "L-IMAGE-PRECONNECTED", "L-IMAGE-NONEMPTY")]},
            "X_external_computation": {
                "status": "required_external_boundary_and_not_applicable_computation_pending_independent_approval",
                "reason": "Pinned bodies, provenance, and TCB are material; no computation, solver, oracle, or unchecked certificate is credited.",
                "obligation_ids": [oid(short) for short in ("A-ISCONNECTED-IMAGE", "X-SOURCE", "X-PROVENANCE", "X-TRUST", "X-READABLE", "X-WORKFLOW")],
            },
            "T_terminal_and_transport": {"status": "required", "obligation_ids": [oid("T-INTERSECTION-PUSHFORWARD"), oid("T-LOCAL-COMPOSE"), oid("T-ASSEMBLE")]},
            "ROOT_exact_theorem": {"status": "required", "obligation_ids": [oid("ROOT")]},
        },
        "layer_exclusions": {
            "representative_symmetry_and_order_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The set-image theorem has no representative, sign, order, finite/infinite, induction, descent, or symmetry normalization beyond the explicit global-to-local continuity transport and relative-open normalization.",
            },
            "additional_case_splits": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The visible terminal body has one universal arbitrary-open separation argument; empty, singleton, and constant-map cases are statement boundaries rather than hidden proof branches.",
            },
            "computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, solver, numerical computation, native code, oracle, experiment, or certificate participates in the visible route.",
            },
        },
        "proof_body_aliases": {
            "google-deepmind/formal-conjectures:Mathoverflow235893.Continuous.isConnectedMap": "deduplicated_to:IsConnected.image",
            "Stage1Instances.THM_M_0626_AnchorAudit.exactTarget_mathlib_candidate": "wrapper_only_deduplicated_to:IsConnected.image",
            "IsConnected.image.preconnected_component": "deduplicated_to:IsPreconnected.image",
            "Stage1Instances.THM_M_0626.ObligationTree.localConnectedImage_of_components": "conditional_reconstruction_of:IsConnected.image; no duplicate semantic or proof-body credit",
        },
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "audited_candidate_obligation": oid("A-ISCONNECTED-IMAGE"),
            "audited_candidate_classification": "M0-W_candidate_pending_proof_phase_and_master_acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. The exact pinned candidate is not installed or accepted; H0, R0, audit completion, validation, release, and theorem completion remain open.",
    }

    premise_registry = {}
    for node in nodes:
        for entry in node["semantic_step_ledger"]:
            for premise_id in entry["premise_ids"]:
                if premise_id.startswith("P-"):
                    premise_registry[premise_id] = {
                        "owning_obligation_id": node["obligation_id"],
                        "claim_or_context": PREMISE_CLAIMS[premise_id],
                        "source_locator": entry["source_locator"],
                    }

    def edge(edge_id: str, source: str, edge_type: str, target: str, reciprocal: str | None = None) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        return value

    requires = {
        oid("ROOT"): [oid("T-ASSEMBLE")],
        oid("T-ASSEMBLE"): [oid("S-GLOBAL-LOCAL"), oid("A-ISCONNECTED-IMAGE")],
        oid("T-LOCAL-COMPOSE"): [oid("L-IMAGE-NONEMPTY"), oid("L-IMAGE-PRECONNECTED")],
        oid("L-IMAGE-PRECONNECTED"): [oid("N-SEPARATION-GOAL")],
        oid("N-SEPARATION-GOAL"): [
            oid("C-RELATIVE-PREIMAGES"), oid("N-IMAGE-COVER-TO-SOURCE"),
            oid("N-WITNESS-PULLBACK"), oid("L-SOURCE-INTERSECTION"),
            oid("T-INTERSECTION-PUSHFORWARD"),
        ],
    }
    proof: list[dict] = []
    for parent, children in requires.items():
        for child in children:
            requirement = f"REQ-{parent}-{child}"
            composition = f"CMP-{child}-{parent}"
            proof.extend(
                [
                    edge(requirement, parent, "proof_requires", child, composition),
                    edge(composition, child, "composes", parent, requirement),
                ]
            )

    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "equivalent_to", oid("S-INTERFACE")),
            edge("REF-ROOT-CONNECTEDNESS", oid("ROOT"), "equivalent_to", oid("S-CONNECTEDNESS")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
            edge("REF-ASSEMBLY-TO-ROOT", oid("T-ASSEMBLE"), "transports", oid("ROOT")),
            edge("REF-ANCHOR-LOCAL-RECONSTRUCTION", oid("A-ISCONNECTED-IMAGE"), "expository_decomposition", oid("T-LOCAL-COMPOSE")),
            edge("REF-PRECONNECTED-PULLBACK", oid("L-IMAGE-PRECONNECTED"), "expository_decomposition", oid("C-RELATIVE-PREIMAGES")),
            edge("REF-PRECONNECTED-INTERSECTION", oid("L-IMAGE-PRECONNECTED"), "expository_decomposition", oid("L-SOURCE-INTERSECTION")),
            edge("REF-COVER-USES-PREIMAGES", oid("N-IMAGE-COVER-TO-SOURCE"), "expository_decomposition", oid("C-RELATIVE-PREIMAGES")),
            edge("REF-HITS-USE-PREIMAGES", oid("N-WITNESS-PULLBACK"), "expository_decomposition", oid("C-RELATIVE-PREIMAGES")),
            edge("REF-PUSH-USES-PREIMAGES", oid("T-INTERSECTION-PUSHFORWARD"), "expository_decomposition", oid("C-RELATIVE-PREIMAGES")),
        ],
        "provenance": [
            edge("PROV-ANCHOR", oid("X-PROVENANCE"), "provenance_of", oid("A-ISCONNECTED-IMAGE")),
            edge("PROV-PRECONNECTED", oid("X-PROVENANCE"), "provenance_of", oid("L-IMAGE-PRECONNECTED")),
            edge("PROV-NONEMPTY", oid("X-PROVENANCE"), "provenance_of", oid("L-IMAGE-NONEMPTY")),
            edge("SRC-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-PRECONNECTED", oid("X-SOURCE"), "source_map", oid("L-IMAGE-PRECONNECTED")),
        ],
        "evidence": [
            edge("EVID-PROVENANCE-ANCHOR", oid("X-PROVENANCE"), "evidence_for", oid("A-ISCONNECTED-IMAGE")),
            edge("EVID-WORKFLOW-ROOT", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-ANCHOR-CLOSURE", oid("A-ISCONNECTED-IMAGE"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-PRECONNECTED", oid("X-READABLE"), "documents", oid("L-IMAGE-PRECONNECTED")),
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge("TASK-STATEMENT-INTAKE", TASK_IDS[1], "workflow_depends_on", TASK_IDS[0]),
            edge("TASK-ANCHOR-STATEMENT", TASK_IDS[2], "workflow_depends_on", TASK_IDS[1]),
            edge("TASK-TREE-ANCHOR", TASK_IDS[3], "workflow_depends_on", TASK_IDS[2]),
            edge("TASK-PROOF-TREE", TASK_IDS[4], "workflow_depends_on", TASK_IDS[3]),
            edge("TASK-VALIDATION-PROOF", TASK_IDS[5], "workflow_depends_on", TASK_IDS[4]),
            edge("TASK-RELEASE-VALIDATION", TASK_IDS[6], "workflow_depends_on", TASK_IDS[5]),
        ],
    }
    graphs = {}
    for name in GRAPH_NAMES:
        endpoints = TASK_IDS if name == "workflow" else ids
        outgoing = {identifier: [] for identifier in endpoints}
        incoming = {identifier: [] for identifier in endpoints}
        for row in graph_edges[name]:
            outgoing[row["from"]].append(row["edge_id"])
            incoming[row["to"]].append(row["edge_id"])
        graphs[name] = {"edges": graph_edges[name], "out": outgoing, "in": incoming}

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0626-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id except workflow, which uses authoritative task IDs",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent; workflow_depends_on is task-to-prerequisite",
        "workflow_task_nodes": [
            {
                "task_id": task_id,
                "phase": phase,
                "layer": layer,
                "state_at_freeze": state,
                "depends_on": ([] if layer == 0 else [TASK_IDS[layer - 1]]),
            }
            for task_id, phase, layer, state in zip(
                TASK_IDS,
                ("intake", "statement", "anchor_audit", "obligation_tree", "proof", "validation", "release"),
                range(7),
                ("[_]", "[_]", "[_]", "[ ]", "[ ]", "[ ]", "[ ]"),
            )
        ],
        "task_obligation_links": [
            {
                "task_id": entry["task_id"],
                "obligation_id": node["obligation_id"],
                "role": entry["role"],
            }
            for node in nodes for entry in task_roles(node["obligation_id"])
        ],
        "premise_registry": premise_registry,
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "candidate_only_obligations": [oid("A-ISCONNECTED-IMAGE")],
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [
                oid("A-ISCONNECTED-IMAGE"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "composition_certificates": [
                "Stage1Instances.THM_M_0626.ObligationTree.separationEngine_of_components",
                "Stage1Instances.THM_M_0626.ObligationTree.imagePreconnected_of_separationEngine",
                "Stage1Instances.THM_M_0626.ObligationTree.localConnectedImage_of_components",
                "Stage1Instances.THM_M_0626.ObligationTree.exactAssembly_of_packages",
                "Stage1Instances.THM_M_0626.ObligationTree.root_of_exactAssembly",
            ],
            "checked_composition_parents": [
                oid("ROOT"), oid("T-ASSEMBLE"),
                oid("T-LOCAL-COMPOSE"), oid("L-IMAGE-PRECONNECTED"), oid("N-SEPARATION-GOAL"),
            ],
            "unchecked_composition_parents": [],
            "minimal_open_root_cut_set": [oid("A-ISCONNECTED-IMAGE")],
            "cut_set_semantics": {
                "minimal_open_machine_proof_cut_set": [oid("A-ISCONNECTED-IMAGE")],
                "remaining_theorem_completion_cut_set": [
                    oid("A-ISCONNECTED-IMAGE"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                    oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"),
                    oid("X-WORKFLOW"),
                ],
                "root_relevance_semantics": "root_relevant includes mathematical proof and theorem-completion/release relevance; only proof graph reachability contributes to the machine proof cut.",
                "boundary": "The mathematical proof cut and the theorem-completion/release cut are distinct; neither is accepted closed.",
            },
            "open_internal_body_leaf_ids": [
                oid("C-RELATIVE-PREIMAGES"), oid("N-IMAGE-COVER-TO-SOURCE"),
                oid("N-WITNESS-PULLBACK"), oid("L-SOURCE-INTERSECTION"),
                oid("T-INTERSECTION-PUSHFORWARD"), oid("L-IMAGE-NONEMPTY"),
            ],
            "reason": "All composition certificates are conditional; the exact pinned anchor remains uninstalled and unaccepted until proof-phase and master validation.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [],
    }
    for identifier in ids:
        recipes["recipes"].append(
            {
                "recipe_id": f"VAL-{identifier}",
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0626/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [
                    {
                        "path_or_stream": "stdout",
                        "semantic_hash_policy": "contains PASS THM-M-0626 obligation tree",
                    }
                ],
                "covered_obligation_ids": [identifier],
                "covered_declarations": [],
            }
        )
    return registry, bundle, recipes


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
