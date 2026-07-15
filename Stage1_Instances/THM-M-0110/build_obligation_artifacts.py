#!/usr/bin/env python3
"""Build THM-M-0110's frozen obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0110-OBLIGATION_TREE"
THEOREM = "THM-M-0110"
PREFIX = "M0110-"
ROOT_EXPRESSION = "d0a9a0e873dd388aa37c0bcc77fce1fc38bae5911851a87570b94f50c80eecc6"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
)
REGISTRY_FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)


def sha(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def oid(short: str) -> str:
    return PREFIX + short


def planned(short: str, formal_target: str) -> str:
    return "planned-v1-sha256:" + digest(
        {"obligation_id": oid(short), "formal_target": formal_target}
    )


# short id, registry kind, node kind, risk, human claim, formal target, output,
# M eligibility, H eligibility, R eligibility, terminal body, budget, M debt.
ROWS = (
    (
        "ROOT", "root", "root", "critical",
        "For every frozen smooth projective characteristic-zero datum and every positive degree, the concrete cohomology type of KTensorL is subsingleton.",
        "Stage1Instances.THMM0110.KodairaVanishingTarget",
        "The exact frozen KodairaVanishingTarget proposition.",
        "required", "required", "required", None, 8, "M3",
    ),
    (
        "S-TARGET", "definition", "definition", "critical",
        "Freeze the universe, characteristic-zero field, data package, ordered hypotheses, positive degree, and concrete Sheaf.H conclusion.",
        "Stage1Instances.THMM0110.KodairaVanishingTarget and kodairaVanishingTarget_iff_expanded",
        "The expression-fingerprinted root interface.",
        "required", "not_applicable", "required", None, 7, "M0-L",
    ),
    (
        "S-BOUNDARY", "branch", "branch", "high",
        "Exclude positive characteristic, degree zero, nonintegral, singular, nonprojective, noninvertible, nonample, and unidentified tensor cases without silently strengthening the target.",
        "Statement.lean mutation declarations and statement.json boundary record",
        "The exact degenerate-case and hypothesis boundary.",
        "required", "required", "required", None, 8, "M0-L",
    ),
    (
        "S-SEMANTIC", "transport", "transport", "critical",
        "Connect the independent projective, canonical, dualizing, invertible, rank-one, ample, and tensor proposition fields to native mathematical structures.",
        "Stage1Instances.THMM0110.ObligationTree.NativeSemanticTransportPackage",
        "An open signature slot for a future native interpretation of every semantic field.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "S-COHOMOLOGY", "transport", "transport", "critical",
        "Identify the frozen Sheaf.H carrier with the cohomology object used by the substantive Kodaira proof route.",
        "planned: concrete Sheaf.H comparison transport preserving every degree",
        "An exact cohomology comparison with no carrier substitution.",
        "required", "required", "required", None, 9, "M4",
    ),
    (
        "S-FOUNDATION", "certificate", "certificate", "critical",
        "Account for kernel, axioms, imports, compiled artifacts, TCB, and the no-oracle boundary of every eventual terminal declaration.",
        "planned theorem-specific foundation and TCB certificate",
        "An accepted foundation and trust profile.",
        "required", "not_applicable", "required", None, 8, "M3",
    ),
    (
        "N-ALGEBRAIC", "normalization", "normalization", "critical",
        "Normalize the scheme-level canonical sheaf, ample invertible sheaf, tensor product, and projective morphism interfaces without changing the frozen claim.",
        "planned: native algebraic-geometry normalization package",
        "A native algebraic datum matching KodairaVanishingData exactly.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "N-ANALYTIC", "normalization", "normalization", "critical",
        "For an analytic route, descend to finite-type characteristic-zero data, embed the field into C, apply GAGA, and transport the result back by checked base change.",
        "planned: noetherian descent, embedding into C, GAGA, and return base-change package",
        "An analytic datum with a checked return map to algebraic cohomology.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "B-ROUTE", "branch", "branch", "critical",
        "Select one complete proof route through a future versioned registry delta; neither current candidate branch receives closure credit.",
        "planned: route-selection decision with checked exact return transport",
        "A substantive KodairaVanishingArgumentPackage.",
        "required", "required", "required", None, 8, "M4",
    ),
    (
        "L-SERRE-DUALITY", "lemma", "core_lemma", "critical",
        "Prove the Serre-duality comparison, including dualizing/canonical identification and exact cohomological indexing.",
        "planned: Serre duality for the frozen Scheme.Modules carrier",
        "A checked duality equivalence for K tensor L.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "L-SERRE-VANISHING", "lemma", "core_lemma", "critical",
        "Supply a genuine algebraic Kodaira engine; ordinary eventual Serre vanishing is only a nearby technique and cannot discharge this node.",
        "planned: algebraic Kodaira engine, explicitly not ordinary eventual Serre vanishing",
        "Positive-degree vanishing on the algebraic branch.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "L-DOLBEAULT", "lemma", "core_lemma", "critical",
        "Identify algebraic sheaf cohomology with bundle-valued Dolbeault cohomology in the chosen analytic comparison.",
        "planned: GAGA and Dolbeault cohomology comparison",
        "A checked cohomology equivalence in every positive degree.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "L-BOCHNER", "lemma", "core_lemma", "critical",
        "Prove the Bochner-Kodaira identity and the strict positivity estimate for the canonical bundle tensored with the positive line bundle.",
        "planned: Bochner-Kodaira positivity package",
        "Every relevant harmonic representative is zero.",
        "required", "required", "required", None, 10, "M4",
    ),
    (
        "C-ALGEBRAIC", "construction", "construction", "critical",
        "Compose native algebraic interfaces, duality, and the algebraic vanishing input while preserving the exact Sheaf.H carrier.",
        "planned: algebraic Kodaira argument constructor",
        "KodairaVanishingArgumentPackage via the algebraic route.",
        "required", "required", "required", None, 9, "M4",
    ),
    (
        "C-ANALYTIC", "construction", "construction", "critical",
        "Compose GAGA, Dolbeault-Hodge theory, Bochner-Kodaira positivity, and the return transport to the exact algebraic cohomology type.",
        "planned: analytic Kodaira argument constructor",
        "KodairaVanishingArgumentPackage via the analytic route.",
        "required", "required", "required", None, 9, "M4",
    ),
    (
        "T-VANISHING", "terminal", "terminal", "critical",
        "Deliver the substantive positive-degree vanishing conclusion for every frozen datum.",
        "Stage1Instances.THMM0110.ObligationTree.KodairaVanishingArgumentPackage",
        "D.VanishingConclusion for every D satisfying D.Hypotheses.",
        "required", "required", "required", None, 7, "M4",
    ),
    (
        "T-ASSEMBLE", "terminal", "terminal", "critical",
        "Consume the semantic transport and substantive vanishing packages and bind them to the exact root.",
        "Stage1Instances.THMM0110.ObligationTree.checkedRootAssembly",
        "Stage1Instances.THMM0110.KodairaVanishingTarget.",
        "required", "required", "required",
        "local:ObligationTree.lean#checkedRootAssembly", 5, "M0-L",
    ),
    (
        "X-SOURCE", "terminal", "terminal", "critical",
        "Pinpoint and independently review the primary Kodaira theorem, assumptions, proof, errata, algebraic reformulation, and node crosswalk.",
        "Kodaira 1953 and exact algebraic comparison source ledger pending",
        "H0-eligible source coverage without machine-proof credit.",
        "not_applicable", "required", "required", None, 9, "M4",
    ),
    (
        "X-ANCHORS", "certificate", "certificate", "high",
        "Retain concrete Sheaf.H, zero-sheaf, injective-Ext, and projective-spectrum anchors only within their audited stronger-premise or substrate boundaries.",
        "anchor-audit.json candidates M0110-C02 through M0110-C05",
        "A zero-root-credit candidate provenance boundary.",
        "informational", "not_applicable", "required", None, 8, "M3",
    ),
    (
        "X-PROVENANCE", "certificate", "certificate", "critical",
        "Resolve every wrapper, terminal body, source blob, revision, import, license, and shared body identity before proof credit.",
        "planned transitive declaration and terminal-body provenance inventory",
        "Unique body-level provenance without duplicate credit.",
        "informational", "not_applicable", "required", None, 8, "M3",
    ),
    (
        "X-TRUST", "certificate", "certificate", "critical",
        "Audit axioms, unsafe and oracle boundaries, executable identities, supply chain, hermetic replay, and independent verification.",
        "Lean 4.29.0 plus mathlib 8a178386 transitive trust closure pending",
        "Release trust coverage without mathematical proof credit.",
        "informational", "not_applicable", "required", None, 9, "M3",
    ),
    (
        "X-READABLE", "terminal", "terminal", "high",
        "Produce an independently reviewed node reconstruction of the chosen proof route and every comparison boundary.",
        "planned independently reviewed readable reconstruction",
        "Readable coverage without machine-proof credit.",
        "not_applicable", "required", "required", None, 8, "M4",
    ),
    (
        "X-WORKFLOW", "certificate", "certificate", "high",
        "Bind proof, source/readable review, validation, freshness, revocation, release, and independent-verification receipts.",
        "Stage1 task and receipt workflow",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", "required", None, 7, "M3",
    ),
)


LEDGER_DETAILS = {
    oid("ROOT"): ([oid("T-ASSEMBLE")], "Apply the checked exact-root assembly in the frozen universe and binder context.", ["theorem root", "release decision"]),
    oid("S-TARGET"): (["Statement.lean", "statement.json expression fingerprint"], "Elaborate the exact target, expansion, and mutations with fixed imports.", [oid("ROOT"), oid("T-ASSEMBLE")]),
    oid("S-BOUNDARY"): (["four statement mutations", "statement.json boundary policy"], "Preserve every hypothesis and the positive-degree boundary.", [oid("ROOT"), oid("B-ROUTE")]),
    oid("S-SEMANTIC"): (["all nine D.Hypotheses fields", "native mathlib structures"], "Fill the conditional interface with checked relations from semantic labels to their actual objects.", [oid("N-ALGEBRAIC"), oid("T-ASSEMBLE")]),
    oid("S-COHOMOLOGY"): (["concrete Sheaf.H", "proof-route cohomology object"], "Construct a degree-preserving checked equivalence and transport Subsingleton.", [oid("C-ALGEBRAIC"), oid("C-ANALYTIC"), oid("T-VANISHING")]),
    oid("S-FOUNDATION"): (["eventual terminal declarations", "pinned toolchain and dependency closure"], "Compare machine-derived axioms and TCB elements with accepted profiles.", [oid("ROOT"), oid("X-TRUST")]),
    oid("N-ALGEBRAIC"): ([oid("S-SEMANTIC"), "native scheme and sheaf APIs"], "Normalize projectivity, canonical/dualizing sheaves, ampleness, and tensor product.", [oid("C-ALGEBRAIC")]),
    oid("N-ANALYTIC"): ([oid("N-ALGEBRAIC"), "noetherian descent", "embedding into C", "GAGA", "base-change return"], "Construct analytic data only after checked descent and return transports.", [oid("C-ANALYTIC")]),
    oid("B-ROUTE"): (["one selected complete route: M0110-C-ALGEBRAIC or M0110-C-ANALYTIC", "checked exact return transport"], "Accept only one complete branch whose output has the exact argument-package type.", [oid("T-VANISHING")]),
    oid("L-SERRE-DUALITY"): ([oid("N-ALGEBRAIC"), "dualizing/canonical identification"], "Prove duality with exact degree and tensor conventions.", [oid("C-ALGEBRAIC")]),
    oid("L-SERRE-VANISHING"): (["ample invertible sheaf", "all required positive degrees"], "Prove a Kodaira-specific algebraic engine; reject ordinary eventual Serre vanishing as insufficient.", [oid("C-ALGEBRAIC")]),
    oid("L-DOLBEAULT"): ([oid("N-ANALYTIC"), oid("S-COHOMOLOGY")], "Compose GAGA and Dolbeault comparison without changing cohomology degree.", [oid("C-ANALYTIC")]),
    oid("L-BOCHNER"): ([oid("N-ANALYTIC"), "positive Hermitian curvature"], "Apply the Bochner-Kodaira identity and strict positivity to harmonic forms.", [oid("C-ANALYTIC")]),
    oid("C-ALGEBRAIC"): ([oid("N-ALGEBRAIC"), oid("L-SERRE-DUALITY"), oid("L-SERRE-VANISHING"), oid("S-COHOMOLOGY")], "Compose the exact algebraic proof route.", [oid("B-ROUTE"), oid("T-VANISHING")]),
    oid("C-ANALYTIC"): ([oid("N-ANALYTIC"), oid("L-DOLBEAULT"), oid("L-BOCHNER"), oid("S-COHOMOLOGY")], "Compose the exact analytic proof route and return transport.", [oid("B-ROUTE"), oid("T-VANISHING")]),
    oid("T-VANISHING"): ([oid("B-ROUTE"), "every positive i"], "Deliver D.VanishingConclusion for arbitrary frozen data.", [oid("T-ASSEMBLE")]),
    oid("T-ASSEMBLE"): ([oid("S-SEMANTIC"), oid("T-VANISHING")], "Use checkedRootAssembly and bind the result to the exact declaration.", [oid("ROOT")]),
    oid("X-SOURCE"): (["immutable primary edition", "pinpoint theorem/proof", "errata", "independent review"], "Map all mathematical nodes and analytic/algebraic comparisons to exact source passages.", [oid("ROOT"), oid("X-READABLE")]),
    oid("X-ANCHORS"): (["anchor-audit.json", "pinned mathlib source hashes"], "Preserve stronger-premise and substrate-only classifications with zero root credit.", [oid("X-PROVENANCE")]),
    oid("X-PROVENANCE"): (["repo-local declarations", "pinned mathlib", oid("X-ANCHORS")], "Resolve conclusion, wrapper, terminal body, transitive dependencies, revisions, and licenses.", [oid("ROOT"), oid("X-TRUST")]),
    oid("X-TRUST"): ([oid("S-FOUNDATION"), oid("X-PROVENANCE"), "actual proof bodies"], "Recompute axioms, TCB, unsafe/oracle boundaries, and replay evidence.", [oid("ROOT"), oid("X-WORKFLOW")]),
    oid("X-READABLE"): ([oid("X-SOURCE"), "all readable-required obligations", "independent reviewer"], "Publish exact inputs, route, formal map, ledger, and status per node.", [oid("ROOT"), oid("X-WORKFLOW")]),
    oid("X-WORKFLOW"): (["accepted proof/source/readable/trust receipts", "freshness and revocation state"], "Enforce dependency order through proof, validation, release, and independent verification.", ["AUDIT-Z", "THEOREM-Z"]),
}


def substantive_steps(identifier: str, count: int, output: str) -> list[dict]:
    premises, inference, outgoing = LEDGER_DETAILS[identifier]
    stages = (
        (premises, "Fix the exact inputs and context for this obligation.", "The obligation context is fixed."),
        ([identifier], inference, output),
        ([identifier], "Check that no stronger premise, hidden branch, or support edge is introduced.", "The output retains the registered boundary."),
        ([identifier], "Bind the output only to its declared consumers.", "Only recorded outgoing uses may consume the result."),
        ([identifier], "Retain the stated debt until accepted content-bound evidence exists.", "The node remains truthfully classified."),
        ([identifier], "Keep aliases, wrappers, transports, and presentation forms on one canonical identity.", "No duplicate coverage is created."),
        ([identifier], "Require the node-specific structured validation recipe.", "The validation boundary is explicit."),
        ([identifier], "Require independent master review before acceptance.", "Worker evidence remains provisional."),
        ([identifier], "Record the next open proof or assurance dependency.", "The remaining debt is explicit."),
        ([identifier], "Publish the precise status boundary in the readable architecture.", "Readable prose cannot imply theorem completion."),
    )
    result = []
    for index, (step_premises, step_inference, exact_output) in enumerate(stages[:count], 1):
        result.append({
            "step_id": f"STEP-{identifier}-{index:02d}",
            "premise_ids": step_premises,
            "inference_or_source": step_inference,
            "exact_output": exact_output,
            "outgoing_use_ids": outgoing,
        })
    return result


def graph(ids: list[str], edges: list[dict]) -> dict:
    result = {"edges": edges, "out": {identifier: [] for identifier in ids}, "in": {identifier: [] for identifier in ids}}
    for edge in edges:
        result["out"][edge["from"]].append(edge["edge_id"])
        result["in"][edge["to"]].append(edge["edge_id"])
    return result


def support_edges(prefix: str, kind: str, pairs: list[tuple[str, str]]) -> list[dict]:
    return [
        {"edge_id": f"{prefix}{index:02d}", "type": kind, "from": source, "to": target}
        for index, (source, target) in enumerate(pairs, 1)
    ]


def build() -> tuple[dict, dict, dict]:
    obligations = []
    for row in ROWS:
        short, registry_kind, _node_kind, risk, _human, formal, _output, machine, human, readable, body, _budget, _debt = row
        identifier = oid(short)
        fingerprint = (
            "lean-expression-sha256:" + ROOT_EXPRESSION
            if short in {"ROOT", "S-TARGET"}
            else planned(short, formal)
        )
        exclusions = []
        if machine != "required":
            exclusions.append("machine_" + machine)
        if human != "required":
            exclusions.append("human_source_" + human)
        if readable != "required":
            exclusions.append("readable_" + readable)
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": registry_kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": readable,
            "risk_class": risk,
            "exclusion_reason": "+".join(exclusions) + ":pending_independent_approval" if exclusions else None,
            "terminal_proof_body_id": body,
        })

    ids = [row["obligation_id"] for row in obligations]
    projection = [{field: row[field] for field in REGISTRY_FIELDS} for row in obligations]
    denominator = digest(projection)
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "registry_id": "THM-M-0110-OBLIGATIONS-v1",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "frozen_at": "2026-07-16T05:00:00+08:00",
        "freeze_basis": "The exact elaborated statement and bounded immutable anchor audit determine the algebraic-or-analytic Kodaira architecture. Eligibility follows semantic root relevance rather than current Lean availability.",
        "freeze_timing_boundary": "The workflow places anchor audit before this freeze. Candidate status was observable, but all source, semantic bridge, construction, lemma, transport, trust, readable, and workflow obligations remain in the denominator independently of proof convenience.",
        "frozen_against_statement_sha256": sha("Statement.lean"),
        "frozen_against_statement_record_sha256": sha("statement.json"),
        "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "mandatory_layer_analysis": {
            "S": [oid("S-TARGET"), oid("S-BOUNDARY"), oid("S-SEMANTIC"), oid("S-COHOMOLOGY"), oid("S-FOUNDATION")],
            "N": [oid("N-ALGEBRAIC"), oid("N-ANALYTIC")],
            "B": [oid("B-ROUTE")],
            "C": [oid("C-ALGEBRAIC"), oid("C-ANALYTIC")],
            "L": [oid("L-SERRE-DUALITY"), oid("L-SERRE-VANISHING"), oid("L-DOLBEAULT"), oid("L-BOCHNER")],
            "X": [oid("X-SOURCE"), oid("X-ANCHORS"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "T": [oid("T-VANISHING"), oid("T-ASSEMBLE")],
            "not_applicable_layers": [],
        },
        "delta_policy": "Any correction, split, merge, target change, eligibility change, exclusion, or weight change requires registry version 2 and an append-only old/new ID delta; v1 remains reportable.",
        "obligations": obligations,
        "append_only_delta": [],
        "deduplication": {
            "conditional_declarations": "The local assembly declarations are interface certificates and receive no substantive theorem-body credit.",
            "shared_module_group": "The THM-M-0118 co-mention is not a lemma or body identity and receives no reuse credit.",
            "near_anchors": "Sheaf.subsingleton_H_of_isZero and Ext.subsingleton_of_injective retain distinct stronger premises and cannot duplicate or close the Kodaira root.",
        },
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "provisionally_checked_interfaces": [oid("T-ASSEMBLE")],
            "authoritative_root_vector": {"H": "H1", "M": "M3", "R": "R3"},
        },
        "status_boundary": "This freeze supplies architecture and conditional composition only. It accepts no proof, source, readable, trust, validation, audit, or theorem-completion state.",
    }

    nodes = []
    for row in ROWS:
        short, _registry_kind, node_kind, _risk, human, formal, output, _machine, human_eligibility, _readable, body, budget, machine_debt = row
        identifier = oid(short)
        owned = []
        if short in {"S-TARGET", "S-BOUNDARY"}:
            owned.append("Stage1_Instances/THM-M-0110/Statement.lean")
        if body and body.startswith("local:"):
            owned.append("Stage1_Instances/THM-M-0110/ObligationTree.lean")
        steps = substantive_steps(identifier, budget, output)
        nodes.append({
            "node_id": identifier,
            "obligation_id": identifier,
            "kind": node_kind,
            "human_statement": human,
            "formal_target": formal,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R3",
            "evidence_ids": [],
            "source_crosswalk_id": "not-applicable" if human_eligibility == "not_applicable" else "source_statement_crosswalk.md:pinpoint-node-review-pending",
            "provenance_id": "anchor-audit:stronger-premise-zero-credit" if short == "X-ANCHORS" else "local:ObligationTree.lean" if body and body.startswith("local:") else "pending",
            "foundation_profile": "lean4-mathlib-classical/propext+Classical.choice+Quot.sound-observed-acceptance-pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-and-independent-replay-pending",
            "computation_record": "none; no computation, oracle, native evaluator, or external solver receives proof credit",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": LEDGER_DETAILS[identifier][0],
                "inference": LEDGER_DETAILS[identifier][1],
                "output": output,
                "outgoing_use": LEDGER_DETAILS[identifier][2],
                "steps": steps,
            },
            "public_readable_target": f"Stage1_Instances/THM-M-0110/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": "VAL-" + identifier,
            "status_boundary": "Provisional obligation architecture only; conditional interface checks supply no accepted substantive premise or theorem closure.",
            "task_ids": [ITEM, "S56-M-0110-PROOF", "S56-M-0110-VALIDATION"],
            "owned_sources": owned,
            "owner": "THM-M-0110 execution lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-16" if owned else None,
                "review_due": "before master acceptance and on every invalidation input change",
                "invalidation_inputs": ["Statement.lean", "statement.json", "anchor-audit.json", "obligation-registry.json", "ObligationTree.lean", "dependency-reuse-ledger.json", "toolchain"],
                "revocation_state": "provisional" if owned else "open",
            },
        })

    proof_pairs = [
        (oid("ROOT"), oid("T-ASSEMBLE")),
        (oid("T-ASSEMBLE"), oid("S-SEMANTIC")),
        (oid("T-ASSEMBLE"), oid("T-VANISHING")),
    ]
    proof_edges = []
    for index, (parent, child) in enumerate(proof_pairs, 1):
        requirement = f"P{index:02d}-REQ"
        reciprocal = f"P{index:02d}-COMP"
        proof_edges.extend([
            {"edge_id": requirement, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": reciprocal},
            {"edge_id": reciprocal, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": requirement},
        ])

    refinement_pairs = [
        (oid("ROOT"), oid("S-TARGET")), (oid("S-TARGET"), oid("S-BOUNDARY")),
        (oid("S-SEMANTIC"), oid("N-ALGEBRAIC")), (oid("S-COHOMOLOGY"), oid("N-ALGEBRAIC")),
        (oid("T-VANISHING"), oid("B-ROUTE")), (oid("C-ALGEBRAIC"), oid("L-SERRE-DUALITY")),
        (oid("C-ALGEBRAIC"), oid("L-SERRE-VANISHING")), (oid("C-ANALYTIC"), oid("N-ANALYTIC")),
        (oid("C-ANALYTIC"), oid("L-DOLBEAULT")), (oid("C-ANALYTIC"), oid("L-BOCHNER")),
    ]
    # The two candidate routes are alternatives. Expository edges record them
    # without making both branches joint machine-closure requirements.
    alternative_pairs = [(oid("B-ROUTE"), oid("C-ALGEBRAIC")), (oid("B-ROUTE"), oid("C-ANALYTIC"))]
    provenance_pairs = [
        (oid("X-ANCHORS"), oid("S-COHOMOLOGY")), (oid("X-ANCHORS"), oid("T-VANISHING")),
        (oid("X-PROVENANCE"), oid("ROOT")), (oid("X-PROVENANCE"), oid("T-ASSEMBLE")),
    ]
    evidence_pairs = [(oid("X-SOURCE"), oid("L-SERRE-DUALITY")), (oid("X-SOURCE"), oid("L-SERRE-VANISHING")), (oid("X-SOURCE"), oid("L-DOLBEAULT")), (oid("X-SOURCE"), oid("L-BOCHNER"))]
    trust_pairs = [(oid("ROOT"), oid("S-FOUNDATION")), (oid("ROOT"), oid("X-TRUST")), (oid("X-PROVENANCE"), oid("X-TRUST"))]
    documentation_pairs = [(oid("X-READABLE"), identifier) for identifier in ids if identifier != oid("X-READABLE")]
    workflow_pairs = [(oid("ROOT"), oid("X-SOURCE")), (oid("ROOT"), oid("X-PROVENANCE")), (oid("ROOT"), oid("X-TRUST")), (oid("ROOT"), oid("X-READABLE")), (oid("ROOT"), oid("X-WORKFLOW"))]
    graphs = {
        "proof": graph(ids, proof_edges),
        "refinement": graph(ids, support_edges("R", "logical_decomposition", refinement_pairs) + support_edges("RA", "expository_decomposition", alternative_pairs)),
        "provenance": graph(ids, support_edges("V", "provenance_of", provenance_pairs)),
        "evidence": graph(ids, support_edges("E", "source_map", evidence_pairs)),
        "trust": graph(ids, support_edges("TR", "trusts", trust_pairs)),
        "documentation": graph(ids, support_edges("D", "documents", documentation_pairs)),
        "workflow": graph(ids, support_edges("W", "workflow_depends_on", workflow_pairs)),
    }

    task_nodes = [("INTAKE", "intake", 0), ("STATEMENT", "statement", 1), ("ANCHOR_AUDIT", "anchor_audit", 2), ("OBLIGATION_TREE", "obligation_tree", 3), ("PROOF", "proof", 4), ("VALIDATION", "validation", 5), ("RELEASE", "release", 6)]
    task_ids = {name: f"S56-M-0110-{name}" for name, _phase, _layer in task_nodes}
    dependency_order = (("STATEMENT", "INTAKE"), ("ANCHOR_AUDIT", "STATEMENT"), ("OBLIGATION_TREE", "ANCHOR_AUDIT"), ("PROOF", "OBLIGATION_TREE"), ("VALIDATION", "PROOF"), ("RELEASE", "VALIDATION"))
    task_edges = [{"edge_id": f"TASK-{index:02d}", "type": "workflow_depends_on", "from": task_ids[source], "to": task_ids[target]} for index, (source, target) in enumerate(dependency_order, 1)]
    task_links = []
    assurance_only = {oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")}
    for identifier in ids:
        task_links.append({"task_id": ITEM, "obligation_id": identifier})
        if identifier not in assurance_only:
            task_links.append({"task_id": task_ids["PROOF"], "obligation_id": identifier})
        task_links.append({"task_id": task_ids["VALIDATION"], "obligation_id": identifier})

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_direction": "proof_requires runs parent to child; its reciprocal composes edge runs child to parent. Support graphs never confer machine closure.",
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": [
            {"certificate_id": "COMP-M0110-ROOT", "declaration": "Stage1Instances.THMM0110.ObligationTree.checkedRootAssembly", "parent_obligation_id": oid("T-ASSEMBLE"), "consumes": [oid("S-SEMANTIC"), oid("T-VANISHING")], "state": "kernel_checked_conditional_provisional"},
            {"certificate_id": "COMP-M0110-ROOT-BIND", "declaration": "Stage1Instances.THMM0110.ObligationTree.root_of_packages", "parent_obligation_id": oid("ROOT"), "consumes": [oid("T-ASSEMBLE")], "state": "kernel_checked_conditional_provisional"},
        ],
        "unverified_decomposition_plans": [{"parent": parent, "child": child, "state": "planned_no_composition_credit"} for parent, child in refinement_pairs] + [{"parent": parent, "child": child, "state": "alternative_candidate_no_machine_closure"} for parent, child in alternative_pairs],
        "workflow_task_graph": {
            "nodes": [{"task_id": task_ids[name], "phase": phase, "layer": layer} for name, phase, layer in task_nodes],
            "edges": task_edges,
            "task_obligation_links": task_links,
        },
        "evidence_endpoint_policy": "The source-map graph records unaccepted source requirements only. It supplies no receipt or machine closure credit.",
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "provisionally_checked_interfaces": [oid("T-ASSEMBLE")],
            "root_closed": False,
            "audit_complete": False,
            "theorem_complete": False,
            "authoritative_root_vector": {"H": "H1", "M": "M3", "R": "R3"},
            "minimal_open_proof_cut_set": [oid("S-SEMANTIC"), oid("T-VANISHING")],
            "remaining_root_assurance_cut_set": [oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "reason": "Only conditional root composition is checked. Native semantic relations, the substantive Kodaira vanishing argument, source, provenance, trust, readable review, and workflow acceptance remain open.",
        },
        "status_boundary": "No support edge, conditional theorem, source mapping, weak shared-module group, or worker receipt closes a mathematical obligation or the canonical root.",
    }

    covered_declarations = {
        oid("T-ASSEMBLE"): ["Stage1Instances.THMM0110.ObligationTree.checkedRootAssembly"],
        oid("ROOT"): ["Stage1Instances.THMM0110.ObligationTree.root_of_packages"],
    }
    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_denominator_sha256": denominator,
        "recipes": [
            {
                "recipe_id": "VAL-" + identifier,
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0110/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0110 obligation tree"}],
                "covered_obligation_ids": [identifier],
                "covered_declarations": covered_declarations.get(identifier, []),
                "coverage_semantics": "provisional_conditional_interface_validation" if identifier in covered_declarations else "open_state_architecture_classification_only",
                "closure_credit": False,
            }
            for identifier in ids
        ],
        "status_boundary": "Every recipe validates architecture or an explicitly conditional interface. No recipe supplies substantive proof or accepted closure credit.",
    }
    return registry, bundle, recipes


def render(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=True) + "\n"


def main() -> None:
    registry, bundle, recipes = build()
    for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
        (HERE / name).write_text(render(value), encoding="utf-8")
    edge_count = sum(len(value["edges"]) for value in bundle["graphs"].values())
    print(f"generated {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
