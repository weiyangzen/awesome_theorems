#!/usr/bin/env python3
"""Build the frozen THM-M-0028 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0028-OBLIGATION_TREE"
THEOREM = "THM-M-0028"
PREFIX = "M0028"
ROOT_EXPRESSION = "89e7e911ed4a5b75c153d824133091ad74ba20a0ecab19bd609b23a54badbee4"
FOUNDATION = (
    "lean4-foundation-planned/1.0: propext, Classical.choice, and Quot.sound observed; "
    "accepted transitive axiom review pending"
)
TCB = (
    "lean4-mathlib-tcb-planned/1.0: Lean 4.29.0 and mathlib 8a178386; "
    "complete transitive closure and independent replay pending"
)
COMPUTATION = (
    "none: no solver, reflection, native evaluator, oracle, experiment, generated certificate, "
    "or unchecked computation is credited"
)

# Architecture and eligibility are declared here before the status fields are attached below.
# Tuple fields: id, kind, human statement, formal target, output, risk, M/H/R eligibility, budget,
# body identity, source crosswalk, provenance id, owned sources.
SPECS = [
    ("ROOT", "root", "Prove the exact modern-unital ideal ascending-chain target frozen in Statement.lean.", "Stage1Instances.THM_M_0028.IdealAscendingChainTarget", "Every Nat-indexed ascending ideal chain stabilizes when every ideal is finitely generated.", "critical", "required", "required", "required", 20, None, "source-statement-crosswalk:canonical-claim", "none", []),
    ("S-INTERFACE", "definition", "Preserve the universe, implicit CommRing binder, explicit every-ideal-FG premise, Nat OrderHom chain, and eventual equality conclusion.", "Stage1Instances.THM_M_0028.IdealAscendingChainTarget", "The canonical interface without Nontrivial, domain, field, characteristic, carrier-finiteness, or countability assumptions.", "critical", "required", "required", "required", 30, None, "source-statement-crosswalk:scope-boundary", "none", ["Stage1_Instances/THM-M-0028/Statement.lean"]),
    ("S-REGULAR-TRANSPORT", "transport", "Relate ideal chains to regular-submodule chains by definitional equality.", "Stage1Instances.THM_M_0028.idealAscendingChainTarget_iff_regularSubmoduleAscendingChainTarget", "A checked iff between ideal and regular-submodule chain targets.", "high", "required", "not_applicable", "required", 15, "repo:Statement.lean#idealAscendingChainTarget_iff_regularSubmoduleAscendingChainTarget", "formal_transport_not_a_separate_human_claim_pending_review", "repo-statement-regular-transport", ["Stage1_Instances/THM-M-0028/Statement.lean"]),
    ("S-MONOTONE-TRANSPORT", "transport", "Relate OrderHom ideal chains to functions carrying an explicit Monotone hypothesis.", "Stage1Instances.THM_M_0028.idealAscendingChainTarget_iff_monotoneIdealSequenceTarget", "A checked iff between OrderHom and function-plus-monotonicity targets.", "high", "required", "not_applicable", "required", 25, "repo:Statement.lean#idealAscendingChainTarget_iff_monotoneIdealSequenceTarget", "formal_transport_not_a_separate_human_claim_pending_review", "repo-statement-monotone-transport", ["Stage1_Instances/THM-M-0028/Statement.lean"]),
    ("S-ZERO-RING", "branch", "Keep subsingleton commutative rings in scope and forbid insertion of a Nontrivial premise.", "Stage1Instances.THM_M_0028.subsingleton_boundary_has_no_nontrivial plus BoundaryProbe.lean", "The zero-ring boundary remains part of the exact quantifier domain.", "high", "required", "required", "required", 20, "repo:Statement.lean#subsingleton_boundary_has_no_nontrivial", "source-statement-crosswalk:unital-boundary", "repo-boundary-witness", ["Stage1_Instances/THM-M-0028/Statement.lean", "Stage1_Instances/THM-M-0028/BoundaryProbe.lean"]),
    ("S-FOUNDATION", "certificate", "Audit the classical principles, quotient soundness, kernel, imports, and no-oracle computation policy of the exact route.", "planned transitive foundation, computation, and TCB report", "An accepted foundation and trust boundary for both terminal proof bodies.", "critical", "required", "not_applicable", "required", 45, None, "formal_trust_boundary_not_a_human_claim_pending_review", "anchor-audit:C01-axiom-probe", []),
    ("T-ROOT-COMPOSE", "terminal", "Package both exact bridge conclusions for the root composition.", "Stage1Instances.THM_M_0028.ObligationTree.BridgePackage", "A conjunction of the two bridge interfaces consumed by root_of_bridgePackage.", "critical", "required", "required", "required", 15, "local:ObligationTree.lean#bridgePackage_of_bridges", "source-statement-crosswalk:direction", "local-conditional-composition", ["Stage1_Instances/THM-M-0028/ObligationTree.lean"]),
    ("B-FG-NOETHERIAN", "bridge", "Convert finite generation of every ideal of R into IsNoetherianRing R.", "Stage1Instances.THM_M_0028.ObligationTree.FiniteGenerationToNoetherian", "IsNoetherianRing R from the exact target premise.", "critical", "required", "required", "required", 25, None, "source-statement-crosswalk:finite-basis-premise", "anchor-audit:M0028-C01-MATHLIB-COMPOSITION", []),
    ("B-NOETHERIAN-CHAIN", "bridge", "Convert IsNoetherianRing R into stabilization of every Nat-indexed ascending ideal chain.", "Stage1Instances.THM_M_0028.ObligationTree.NoetherianToChainStabilization", "The exact eventual-equality conclusion for every ideal OrderHom chain.", "critical", "required", "required", "required", 25, None, "source-statement-crosswalk:chain-conclusion", "anchor-audit:M0028-C01-MATHLIB-COMPOSITION", []),
    ("X-FG-BODY", "bridge", "Expose the pinned terminal body converting finite generation of every ideal to IsNoetherianRing.", "isNoetherianRing_iff_ideal_fg at pinned mathlib", "The exact forward finite-generation bridge.", "critical", "required", "required", "required", 15, "git-blob:66ddf1f73601e7dbeb04e37b95fcc61e34ee3c14:isNoetherianRing_iff_ideal_fg", "source-statement-crosswalk:finite-basis-premise", "anchor-audit:M0028-C01-MATHLIB-COMPOSITION", []),
    ("X-CHAIN-BODY", "bridge", "Expose the pinned terminal body converting module Noetherianity to monotone-chain stabilization.", "monotone_stabilizes_iff_noetherian at pinned mathlib", "The exact forward ascending-chain bridge after regular-module specialization.", "critical", "required", "required", "required", 15, "git-blob:66ddf1f73601e7dbeb04e37b95fcc61e34ee3c14:monotone_stabilizes_iff_noetherian", "source-statement-crosswalk:chain-conclusion", "anchor-audit:M0028-C01-MATHLIB-COMPOSITION", []),
    ("N-RING-REGULAR", "normalization", "Unfold IsNoetherianRing R to Noetherianity of the regular R-module.", "isNoetherianRing_iff", "IsNoetherian R R in the regular-module carrier used by ideals.", "high", "required", "not_applicable", "required", 10, "git-blob:66ddf1f73601e7dbeb04e37b95fcc61e34ee3c14:isNoetherianRing_iff", "formal_abbreviation_not_a_separate_human_claim_pending_review", "pinned-mathlib-noetherian-defs", []),
    ("D-NOETHERIAN-CLASS", "definition", "Package or project the IsNoetherian class field asserting finite generation of every submodule.", "isNoetherian_def and IsNoetherian.mk/noetherian", "The exact equivalence between a Noetherian module instance and finite generation of all submodules.", "high", "required", "required", "required", 20, "git-blob:66ddf1f73601e7dbeb04e37b95fcc61e34ee3c14:isNoetherian_def", "source-statement-crosswalk:finite-basis-premise", "pinned-mathlib-noetherian-defs", []),
    ("N-CHAIN-IFF", "reduction", "Reduce the ascending-chain bridge to the generic module theorem specialized to the regular module R over itself.", "monotone_stabilizes_iff_noetherian specialized to M := R", "Chain stabilization for Ideal R, definitionally Submodule R R.", "critical", "required", "required", "required", 20, None, "source-statement-crosswalk:chain-conclusion", "pinned-mathlib-noetherian-defs", []),
    ("N-NOETHERIAN-WF", "reduction", "Identify module Noetherianity with well-founded strict descent in its complete lattice of submodules.", "isNoetherian_iff'", "WellFoundedGT (Submodule R M) from IsNoetherian R M and conversely.", "critical", "required", "required", "required", 35, "git-blob:66ddf1f73601e7dbeb04e37b95fcc61e34ee3c14:isNoetherian_iff'", "source-statement-crosswalk:finite-basis-to-acc", "pinned-mathlib-noetherian-defs", []),
    ("L-FG-COMPACT", "core_lemma", "Relate finite generation of a submodule to compactness in the complete submodule lattice.", "fg_iff_compact", "s.FG iff IsCompactElement s for each submodule s.", "critical", "required", "required", "required", 70, "git-blob:5e83d4d993577f239286960f38eba10b4628d56e:fg_iff_compact", "source-proof-crosswalk_pending", "pinned-mathlib-finiteness-basic", []),
    ("C-LATTICE-WF", "construction", "Use the complete-lattice equivalence between compact generation of every element and WellFoundedGT.", "CompleteLattice.wellFoundedGT_characterisations", "WellFoundedGT for the submodule lattice exactly when every element is compact.", "critical", "required", "required", "required", 65, "git-blob:fd66d4dbebe5b64b7118a0a76dce9575cdec9507:wellFoundedGT_characterisations", "source-proof-crosswalk_pending", "pinned-mathlib-compactly-generated-basic", []),
    ("L-WF-CHAIN", "core_lemma", "Relate WellFoundedGT in a partial order to eventual equality of every monotone Nat sequence.", "wellFoundedGT_iff_monotone_chain_condition", "The generic well-founded partial-order chain condition.", "critical", "required", "required", "required", 25, "git-blob:531f93b96fe0fe5ef91fc07a8bff0a5cfbfe163f:wellFoundedGT_iff_monotone_chain_condition", "source-statement-crosswalk:chain-conclusion", "pinned-mathlib-order-iso-nat", []),
    ("L-PREORDER-CHAIN", "core_lemma", "For preorders, derive an index after which no later chain value is strictly greater, and reconstruct well-foundedness from that condition.", "wellFoundedGT_iff_monotone_chain_condition'", "The no-strict-growth monotone-chain condition equivalent to WellFoundedGT.", "high", "required", "required", "required", 75, "git-blob:531f93b96fe0fe5ef91fc07a8bff0a5cfbfe163f:wellFoundedGT_iff_monotone_chain_condition'", "source-proof-crosswalk_pending", "pinned-mathlib-order-iso-nat", []),
    ("L-PARTIAL-EQUALITY", "core_lemma", "In a partial order, combine chain monotonicity with absence of strict growth to obtain equality at every later index.", "lt_iff_le_and_ne plus OrderHom.mono inside wellFoundedGT_iff_monotone_chain_condition", "a n = a m whenever n <= m after the selected index.", "high", "required", "required", "required", 25, "git-blob:531f93b96fe0fe5ef91fc07a8bff0a5cfbfe163f:lines-216-219", "source-proof-crosswalk_pending", "pinned-mathlib-order-iso-nat", []),
    ("X-SOURCE", "certificate", "Map every material premise, transition, and conclusion to pinpoint primary-source records and independent review.", "planned H0 source packet", "Accepted node-level historical and modern-unital source fidelity.", "critical", "informational", "required", "required", 60, None, "source-statement-crosswalk:open-H0-work", "none", ["Stage1_Instances/THM-M-0028/source-statement-crosswalk.md"]),
    ("X-PROVENANCE", "certificate", "Resolve local wrapper, terminal bodies, immutable origins, direct dependencies, and transitive declaration provenance.", "planned complete provenance packet", "Accepted provenance closure for both bridge bodies.", "critical", "informational", "not_applicable", "required", 60, None, "formal_provenance_not_a_human_claim_pending_review", "anchor-audit:C01-provenance", ["Stage1_Instances/THM-M-0028/anchor-audit.json"]),
    ("X-TRUST", "certificate", "Close transitive axioms, TCB artifacts, supply-chain identity, computation policy, and independent replay.", "planned trust and TCB packet", "Release-grade trust closure for the exact root.", "critical", "informational", "not_applicable", "required", 70, None, "formal_trust_boundary_not_a_human_claim_pending_review", "anchor-audit:C01-foundation-assessment", []),
    ("X-READABLE", "terminal", "Produce short and long node-specific proof reconstructions and obtain independent domain review.", "Stage1_Instances/THM-M-0028/obligation-tree.md plus downstream proof process", "Reviewed readable coverage of every root-critical obligation.", "high", "informational", "required", "required", 70, None, "source-statement-crosswalk:reader-route", "none", ["Stage1_Instances/THM-M-0028/obligation-tree.md"]),
    ("X-WORKFLOW", "certificate", "Run proof installation, composition, hermetic validation, deterministic evidence, independent verification, and release in dependency order.", "S56-M-0028-PROOF through S56-M-0028-RELEASE", "Accepted workflow receipts without deriving proof credit from task order.", "critical", "informational", "not_applicable", "required", 50, None, "workflow_not_a_human_claim_pending_review", "none", ["Stage1_Instances/THM-M-0028/task-dag.json"]),
]

PROOF_REQUIRES = {
    "ROOT": ["T-ROOT-COMPOSE"],
    "T-ROOT-COMPOSE": ["B-FG-NOETHERIAN", "B-NOETHERIAN-CHAIN"],
}

REFINEMENT_EDGES = [
    ("ROOT", "S-INTERFACE"), ("ROOT", "S-REGULAR-TRANSPORT"),
    ("ROOT", "S-MONOTONE-TRANSPORT"), ("ROOT", "S-ZERO-RING"),
    ("B-FG-NOETHERIAN", "X-FG-BODY"), ("X-FG-BODY", "N-RING-REGULAR"),
    ("X-FG-BODY", "D-NOETHERIAN-CLASS"),
    ("B-NOETHERIAN-CHAIN", "N-CHAIN-IFF"), ("N-CHAIN-IFF", "X-CHAIN-BODY"),
    ("X-CHAIN-BODY", "N-NOETHERIAN-WF"), ("X-CHAIN-BODY", "L-WF-CHAIN"),
    ("N-NOETHERIAN-WF", "L-FG-COMPACT"), ("N-NOETHERIAN-WF", "C-LATTICE-WF"),
    ("L-WF-CHAIN", "L-PREORDER-CHAIN"), ("L-WF-CHAIN", "L-PARTIAL-EQUALITY"),
]


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


def planned_fingerprint(formal_target: str, output: str) -> str:
    payload = f"{THEOREM}\0{formal_target}\0{output}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(payload).hexdigest()


def exclusion_reason(machine: str, human: str, readable: str, source_id: str) -> str | None:
    if (machine, human, readable) == ("required", "required", "required"):
        return None
    if "pending_review" in source_id:
        return source_id
    return "eligibility_exclusion_pending_independent_approval"


def edge(edge_id: str, source: str, edge_type: str, target: str, **extra: str) -> dict:
    return {"edge_id": edge_id, "from": oid(source), "type": edge_type, "to": oid(target), **extra}


def graph(all_ids: list[str], edges: list[dict]) -> dict:
    outgoing = {key: [] for key in all_ids}
    incoming = {key: [] for key in all_ids}
    for item in edges:
        outgoing[item["from"]].append(item["edge_id"])
        incoming[item["to"]].append(item["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict]:
    obligations = []
    nodes = []
    architecture_children: dict[str, list[str]] = {
        parent: list(children) for parent, children in PROOF_REQUIRES.items()
    }
    for parent, child in REFINEMENT_EDGES:
        architecture_children.setdefault(parent, []).append(child)
    architecture_parents: dict[str, list[str]] = {}
    for parent, children in architecture_children.items():
        for child in children:
            architecture_parents.setdefault(child, []).append(parent)
    for short, kind, human, formal, output, risk, machine, source, readable, budget, body, crosswalk, provenance, owned in SPECS:
        obligation_id = oid(short)
        registry_kind = {
            "bridge": "reduction",
            "normalization": "reduction",
            "core_lemma": "lemma",
            "certificate": "terminal",
        }.get(kind, kind)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if short in {"ROOT", "S-INTERFACE"}
            else planned_fingerprint(formal, output)
        )
        obligations.append({
            "obligation_id": obligation_id,
            "statement_fingerprint": fingerprint,
            "kind": registry_kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": source,
            "readable_eligibility": readable,
            "risk_class": risk,
            "exclusion_reason": exclusion_reason(machine, source, readable, crosswalk),
            "terminal_proof_body_id": body,
        })
        machine_debt = "M3" if short == "ROOT" else ("M0-L" if short in {"S-INTERFACE", "S-REGULAR-TRANSPORT", "S-MONOTONE-TRANSPORT", "S-ZERO-RING", "T-ROOT-COMPOSE"} else "M4")
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": obligation_id,
            "kind": kind,
            "human_statement": human,
            "formal_target": formal,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R3",
            "evidence_ids": [],
            "source_crosswalk_id": crosswalk,
            "provenance_id": provenance,
            "foundation_profile": FOUNDATION,
            "tcb_profile": TCB,
            "computation_record": COMPUTATION,
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": [oid(child) for child in architecture_children.get(short, [])] or ["exact frozen context; no undeclared premise"],
                "inference": human,
                "output": output,
                "outgoing_use": [oid(parent) for parent in architecture_parents.get(short, [])] or ["typed support edge or canonical terminal output only"],
            },
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{obligation_id.lower()}",
            "validation_spec_id": f"VAL-{obligation_id}",
            "status_boundary": "Architecture, interface, or audited-candidate record only; no accepted proof, source, trust, readability, audit-completion, or theorem-completion credit.",
            "task_ids": [ITEM, "S56-M-0028-PROOF"],
            "owned_sources": owned,
            "owner": "THM-M-0028 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": None,
                "review_due": "at master acceptance and after every invalidation input change",
                "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "typed-graphs.json", "toolchain and dependency pins"],
                "revocation_state": "provisional" if machine_debt == "M0-L" else "open",
            },
        })

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    projection = [{key: row[key] for key in fields} for row in obligations]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0028-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T08:02:57+08:00",
        "freeze_basis": "Exact statement plus the visible semantic architecture of the two pinned terminal bodies. Eligibility and denominators are architecture-derived and do not use candidate closure status.",
        "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
        "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "representative_symmetry_sign_order_normalization": {"status": "not_applicable_pending_independent_approval", "reason": "No representative, quotient choice, symmetry, or sign normalization occurs; the required order conversion is explicit in M0028-L-PARTIAL-EQUALITY."},
            "finite_infinite_or_local_global_reduction": {"status": "not_applicable_pending_independent_approval", "reason": "The target and pinned route are uniform over one ring and one Nat-indexed chain; there is no finite/infinite or local/global split."},
            "constructed_mathematical_objects": {"status": "not_applicable_pending_independent_approval", "reason": "The route packages a class witness and invokes complete-lattice equivalences but constructs no new ideal or ring; the class and lattice packages are explicit obligations."},
            "computation": {"status": "not_applicable_pending_independent_approval", "reason": "No reflection, decision procedure, solver, oracle, experiment, finite computation, or certificate is present in the audited route."},
        },
        "proof_body_aliases": {
            "Stage1Instances.THM_M_0028_AnchorAudit.exactTarget_mathlib_candidate": ["M0028-X-FG-BODY", "M0028-X-CHAIN-BODY"],
            "facebookresearch/atlas-lean:noetherian_fg_iff_acc": ["M0028-X-FG-BODY", "M0028-X-CHAIN-BODY"],
            "NoetherianModules.noetherian_ring_iff_acc": ["M0028-X-CHAIN-BODY"],
        },
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {"accepted_closed_obligations": [], "root_machine_debt": "M3", "candidate_only": [oid("B-FG-NOETHERIAN"), oid("B-NOETHERIAN-CHAIN"), oid("X-FG-BODY"), oid("X-CHAIN-BODY")]},
        "status_boundary": "The architecture is frozen before crediting the candidate. Accepted root state remains H1/M3/R3; proof integration and all terminal gates remain open.",
    }

    proof_edges = []
    for parent, children in PROOF_REQUIRES.items():
        for child in children:
            request_id = f"REQ-{parent}-{child}"
            compose_id = f"CMP-{child}-{parent}"
            proof_edges.extend([
                edge(request_id, parent, "proof_requires", child, reciprocal_edge_id=compose_id),
                edge(compose_id, child, "composes", parent, reciprocal_edge_id=request_id),
            ])
    refinement = [edge(f"REF-{parent}-{child}", parent, "logical_decomposition", child) for parent, child in REFINEMENT_EDGES]
    provenance = [
        edge("PROV-FG-BODY", "X-PROVENANCE", "provenance_of", "X-FG-BODY"),
        edge("PROV-CHAIN-BODY", "X-PROVENANCE", "provenance_of", "X-CHAIN-BODY"),
        edge("SRC-ROOT", "X-SOURCE", "source_map", "ROOT"),
        edge("SRC-FG", "X-SOURCE", "source_map", "B-FG-NOETHERIAN"),
        edge("SRC-CHAIN", "X-SOURCE", "source_map", "B-NOETHERIAN-CHAIN"),
    ]
    evidence = [
        edge("EVIDENCE-STATEMENT", "S-INTERFACE", "evidence_for", "ROOT"),
        edge("EVIDENCE-COMPOSITION", "T-ROOT-COMPOSE", "evidence_for", "ROOT"),
    ]
    trust = [
        edge("TRUST-FOUNDATION", "ROOT", "trusts", "S-FOUNDATION"),
        edge("TRUST-ROOT", "ROOT", "trusts", "X-TRUST"),
        edge("TRUST-FG-BODY", "X-FG-BODY", "trusts", "X-TRUST"),
        edge("TRUST-CHAIN-BODY", "X-CHAIN-BODY", "trusts", "X-TRUST"),
    ]
    documentation = [
        edge("DOC-ROOT", "X-READABLE", "documents", "ROOT"),
        edge("DOC-SOURCE", "X-READABLE", "documents", "X-SOURCE"),
        edge("DOC-FG-BODY", "X-READABLE", "documents", "X-FG-BODY"),
        edge("DOC-CHAIN-BODY", "X-READABLE", "documents", "X-CHAIN-BODY"),
    ]
    workflow = [
        edge("FLOW-PROOF", "X-WORKFLOW", "workflow_depends_on", "T-ROOT-COMPOSE"),
        edge("FLOW-PROVENANCE", "X-WORKFLOW", "workflow_depends_on", "X-PROVENANCE"),
        edge("FLOW-TRUST", "X-WORKFLOW", "workflow_depends_on", "X-TRUST"),
        edge("FLOW-READABLE", "X-WORKFLOW", "workflow_depends_on", "X-READABLE"),
    ]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent; support relations use their declared semantic direction",
        "nodes": nodes,
        "graphs": {
            "proof": graph(ids, proof_edges),
            "refinement": graph(ids, refinement),
            "provenance": graph(ids, provenance),
            "evidence": graph(ids, evidence),
            "trust": graph(ids, trust),
            "documentation": graph(ids, documentation),
            "workflow": graph(ids, workflow),
        },
        "composition_certificates": [
            {
                "certificate_id": "M0028-COMP-BRIDGE-PACKAGE-v1",
                "declaration": "Stage1Instances.THM_M_0028.ObligationTree.bridgePackage_of_bridges",
                "parent_obligation_id": oid("T-ROOT-COMPOSE"),
                "required_child_obligation_ids": [oid("B-FG-NOETHERIAN"), oid("B-NOETHERIAN-CHAIN")],
                "binding": "The Lean declaration consumes both exact bridge propositions and returns their conjunction package.",
                "status": "provisional_conditional_composition_checked",
                "closure_credit": False,
            },
            {
                "certificate_id": "M0028-COMP-ROOT-PACKAGE-v1",
                "declaration": "Stage1Instances.THM_M_0028.ObligationTree.root_of_bridgePackage",
                "parent_obligation_id": oid("ROOT"),
                "required_child_obligation_ids": [oid("T-ROOT-COMPOSE")],
                "binding": "The Lean declaration consumes the exact bridge package and returns the canonical Statement.lean target.",
                "status": "provisional_conditional_composition_checked",
                "closure_credit": False,
            },
        ],
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "root_closed": False,
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set_semantics": "minimal open proof-interface cut plus every independent root-critical release overlay",
            "remaining_root_cut_set": [oid("B-FG-NOETHERIAN"), oid("B-NOETHERIAN-CHAIN"), oid("S-FOUNDATION"), oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "reason": "The exact bridge interfaces compose conditionally, but neither pinned bridge is installed or master-accepted and all source/readability/release overlays remain open.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [{
            "recipe_id": f"VAL-{row['obligation_id']}",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0028/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 120,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "must include PASS THM-M-0028 obligation tree"}],
            "covered_obligation_ids": [row["obligation_id"]],
            "covered_declarations": [node["formal_target"] for node in nodes if node["obligation_id"] == row["obligation_id"]],
            "coverage_semantics": "architecture_validation_only",
            "closure_credit": False,
        } for row in obligations],
    }
    return registry, bundle, recipes


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=True) + "\n"


def main() -> None:
    for name, value in zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), build()):
        (HERE / name).write_text(canonical(value), encoding="utf-8")
    registry, bundle, _ = build()
    count = sum(len(graph_data["edges"]) for graph_data in bundle["graphs"].values())
    print(f"generated {len(registry['obligations'])} obligations and {count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
