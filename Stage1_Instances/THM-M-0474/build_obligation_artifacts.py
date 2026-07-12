#!/usr/bin/env python3
"""Build the frozen THM-M-0474 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0474-OBLIGATION_TREE"
THEOREM = "THM-M-0474"
PREFIX = "M0474"
ROOT_EXPRESSION = "5475969fd23513d3b98134a6aaa747675a32a899f38be773a23cb330f2f590e8"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_BLOB = "fb3668d594f865e52f20c8af45e91e7e3b1eebd8"
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


# Architecture is derived from the exact target and the visible terminal source chain. Status is
# deliberately absent from this table and is attached only after the denominator is frozen.
ROWS = (
    (
        "ROOT",
        "root",
        "critical",
        "Prove the exact natural-number Fermat little theorem target frozen in Statement.lean.",
        "Stage1Instances.THM_M_0474.FermatLittleTheoremTarget",
        "For every prime p and a coprime to p, a^(p-1) is congruent to 1 modulo p.",
        "required",
        "required",
        None,
    ),
    (
        "S-INTERFACE",
        "definition",
        "high",
        "Preserve the ordered natural binders, prime and coprime hypotheses, Nat.ModEq modulus, exponent, and conclusion.",
        "Stage1Instances.THM_M_0474.FermatLittleTheoremTarget",
        "The exact root interface without an added or removed hypothesis.",
        "required",
        "required",
        None,
    ),
    (
        "S-BOUNDARY",
        "branch",
        "high",
        "Retain p = 2, exclude composite or zero moduli by primality, and exclude a divisible by p only through coprimality.",
        "the boundary and degenerate cases of FermatLittleTheoremTarget",
        "An exhaustive boundary policy for the canonical quantifiers.",
        "required",
        "required",
        None,
    ),
    (
        "S-TRANSPORT",
        "transport",
        "high",
        "Relate the canonical coprime premise to the checked nondivisibility premise without changing the target domain.",
        "Stage1Instances.THM_M_0474.fermatLittleTheoremTarget_iff_notDvd",
        "The checked iff between the coprime and not-divides target encodings.",
        "required",
        "not_applicable",
        "formal_encoding_transport_human_source_coverage_inherited_from_root_pending_reviewer_acceptance",
    ),
    (
        "S-FOUNDATION",
        "certificate",
        "critical",
        "Audit logic, classical choice, quotient soundness, kernel, imports, and the no-oracle computation policy.",
        "planned transitive foundation and TCB report",
        "An accepted foundation, trust, and computation boundary.",
        "required",
        "not_applicable",
        "formal_trust_boundary_not_a_human_mathematical_claim_pending_reviewer_acceptance",
    ),
    (
        "T-COMPOSE",
        "terminal",
        "high",
        "Consume the exact Nat.ModEq child conclusion and return the canonical target without adding a premise.",
        "Stage1Instances.THM_M_0474.ObligationTree.root_of_exactNatAnchor",
        "Stage1Instances.THM_M_0474.FermatLittleTheoremTarget.",
        "required",
        "required",
        "local:Stage1_Instances/THM-M-0474/ObligationTree.lean#root_of_exactNatAnchor",
    ),
    (
        "L-NAT",
        "bridge",
        "critical",
        "Instantiate the exact pinned Nat.ModEq theorem at the canonical p and a binders.",
        "Nat.ModEq.pow_card_sub_one_eq_one",
        "The exact proposition consumed by T-COMPOSE.",
        "required",
        "required",
        f"git-blob:{MATHLIB_BLOB}:Nat.ModEq.pow_card_sub_one_eq_one",
    ),
    (
        "N-NAT-INT",
        "normalization",
        "high",
        "Rewrite natural modular congruence and casts of powers and one into the integer ModEq representation.",
        "Int.natCast_modEq_iff together with Nat.cast_pow and Nat.cast_one",
        "The integer congruence target for the same natural p and a.",
        "required",
        "required",
        None,
    ),
    (
        "N-COPRIME",
        "normalization",
        "high",
        "Transport Nat.Coprime a p to IsCoprime (a : Int) p for the integer theorem.",
        "Nat.isCoprime_iff_coprime",
        "IsCoprime (a : Int) p.",
        "required",
        "required",
        None,
    ),
    (
        "L-INT",
        "bridge",
        "critical",
        "Apply the pinned integer Fermat theorem after the natural-to-integer conversions.",
        "Int.ModEq.pow_card_sub_one_eq_one",
        "(a : Int)^(p-1) is congruent to 1 modulo p.",
        "required",
        "required",
        f"pinned-mathlib:{MATHLIB_REVISION}#Int.ModEq.pow_card_sub_one_eq_one",
    ),
    (
        "C-ZMOD-NONZERO",
        "construction",
        "critical",
        "Install Fact p.Prime and turn integer coprimality into nonvanishing of the residue of a in ZMod p.",
        "CharP.intCast_eq_zero_iff and Nat.prime_iff_prime_int.coprime_iff_not_dvd",
        "Fact p.Prime and ((a : Int) : ZMod p) != 0.",
        "required",
        "required",
        None,
    ),
    (
        "T-INT-ZMOD",
        "transport",
        "high",
        "Transport equality in ZMod p back to the integer ModEq conclusion.",
        "ZMod.intCast_eq_intCast_iff",
        "The exact Int.ModEq conclusion expected by L-INT.",
        "required",
        "required",
        None,
    ),
    (
        "L-ZMOD",
        "bridge",
        "critical",
        "Specialize the finite-field power theorem to the nonzero element of ZMod p.",
        "ZMod.pow_card_sub_one_eq_one",
        "The residue of a raised to p-1 equals one in ZMod p.",
        "required",
        "required",
        f"pinned-mathlib:{MATHLIB_REVISION}#ZMod.pow_card_sub_one_eq_one",
    ),
    (
        "T-ZMOD-CARD",
        "transport",
        "high",
        "Rewrite Fintype.card (ZMod p) to p so the finite-field exponent is exactly p-1.",
        "ZMod.card",
        "The ZMod p statement with canonical exponent p-1.",
        "required",
        "required",
        None,
    ),
    (
        "L-FINITE-FIELD",
        "bridge",
        "critical",
        "For a nonzero element of a finite group-with-zero, reduce the card-minus-one power to the unit group.",
        "FiniteField.pow_card_sub_one_eq_one",
        "a^(card K-1) = 1 for nonzero a.",
        "required",
        "required",
        f"pinned-mathlib:{MATHLIB_REVISION}#FiniteField.pow_card_sub_one_eq_one",
    ),
    (
        "C-UNIT",
        "construction",
        "high",
        "Construct Units.mk0 a ha and identify its underlying power with the original nonzero element's power.",
        "Units.mk0 and Units.val_pow_eq_pow_val",
        "A unit carrying the finite-field element and its exponent equality.",
        "required",
        "required",
        None,
    ),
    (
        "L-GROUP-CARD",
        "core_lemma",
        "critical",
        "Use element order dividing the finite group cardinality to prove every unit raised to group cardinality is one.",
        "pow_card_eq_one via pow_card_eq_one', orderOf_dvd_natCard, and orderOf_dvd_card",
        "x^(Fintype.card G) = 1 for every element x of a finite group.",
        "required",
        "required",
        f"pinned-mathlib:{MATHLIB_REVISION}#pow_card_eq_one",
    ),
    (
        "X-SOURCE",
        "terminal",
        "critical",
        "Map every material premise and transition to a pinpoint reviewed primary source, including assumptions and errata.",
        "non-machine primary-source crosswalk",
        "Human-source evidence without machine proof credit.",
        "not_applicable",
        "required",
        None,
    ),
    (
        "X-PROVENANCE",
        "certificate",
        "critical",
        "Resolve terminal bodies, transitive declarations, source hashes, pins, axioms, license, and replay evidence.",
        "planned machine-derived provenance closure",
        "Release provenance without mathematical proof credit.",
        "informational",
        "not_applicable",
        None,
    ),
    (
        "X-READABLE",
        "terminal",
        "high",
        "Provide and independently review a complete readable reconstruction of the Nat-to-group proof route.",
        "planned node-specific readable reconstruction",
        "Readable coverage and reviewer decision without machine proof credit.",
        "not_applicable",
        "required",
        None,
    ),
    (
        "X-WORKFLOW",
        "certificate",
        "high",
        "Bind proof, validation, release, freshness, revocation, and independent-verification task acceptance.",
        "planned Stage1 workflow receipts",
        "Workflow acceptance without mathematical proof credit.",
        "informational",
        "not_applicable",
        None,
    ),
)


CHECKED_INTERFACES = {oid("S-INTERFACE"), oid("S-TRANSPORT"), oid("T-COMPOSE")}
SOURCE_NA = {oid("S-TRANSPORT"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-WORKFLOW")}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []

    for short, kind, risk, claim, target, output, machine, human_source, body in ROWS:
        identifier = oid(short)
        if identifier in {oid("ROOT"), oid("S-INTERFACE")}:
            fingerprint = f"lean-expression-sha256:{ROOT_EXPRESSION}"
        else:
            fingerprint = "planned:v1:sha256:" + digest(
                [identifier, kind, claim, target, output]
            )
        exclusion = None
        if machine != "required" or human_source != "required":
            exclusion = {
                oid("S-TRANSPORT"): "formal_encoding_transport_human_source_coverage_inherited_from_root_pending_reviewer_acceptance",
                oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_mathematical_claim_pending_reviewer_acceptance",
                oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
                oid("X-PROVENANCE"): "release_provenance_overlay_no_proof_credit_pending_integration_review",
                oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
                oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
            }.get(identifier)
        obligations.append(
            {
                "obligation_id": identifier,
                "statement_fingerprint": fingerprint,
                "kind": kind,
                "root_relevant": identifier not in {oid("X-PROVENANCE"), oid("X-WORKFLOW")},
                "machine_eligibility": machine,
                "human_source_eligibility": human_source,
                "readable_eligibility": "required",
                "risk_class": risk,
                "exclusion_reason": exclusion,
                "terminal_proof_body_id": body if body and not body.startswith(("human_", "release_", "readability_", "workflow_", "formal_")) else None,
            }
        )

        if identifier in CHECKED_INTERFACES:
            machine_debt = "M0-L"
        elif identifier == oid("ROOT"):
            machine_debt = "M3"
        elif identifier == oid("L-NAT"):
            machine_debt = "M0-W"
        else:
            machine_debt = "M4"
        source_crosswalk = (
            "not-applicable-pending-review" if identifier in SOURCE_NA else "primary-source-node-map-pending"
        )
        if identifier == oid("L-NAT"):
            provenance = "anchor-audit:M0474-C01-MATHLIB-NAT-EXACT"
        elif identifier == oid("T-COMPOSE"):
            provenance = "local-conditional-composition"
        elif short.startswith(("N-", "L-", "C-", "T-")):
            provenance = "pinned-visible-terminal-chain"
        else:
            provenance = "none"
        owned_sources = []
        if identifier == oid("T-COMPOSE"):
            owned_sources = ["Stage1_Instances/THM-M-0474/ObligationTree.lean"]
        elif identifier == oid("S-TRANSPORT"):
            owned_sources = ["Stage1_Instances/THM-M-0474/Statement.lean"]

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
                "readability_debt": "R4",
                "evidence_ids": [],
                "source_crosswalk_id": source_crosswalk,
                "provenance_id": provenance,
                "foundation_profile": "lean4-dependent-type-theory; accepted axiom policy and transitive review pending",
                "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
                "computation_record": "none; no native computation, solver, oracle, or unchecked certificate is credited",
                "step_budget": 60 if risk == "critical" else 30,
                "semantic_step_ledger": {
                    "premises": "The exact formal context and only the conclusions named by incoming proof_requires edges.",
                    "inference": claim,
                    "output": output,
                    "outgoing_use": "Only the declared proof parent or a typed non-proof support edge may consume this output.",
                },
                "public_readable_target": f"Stage1_Instances/THM-M-0474/obligation-tree.md#{identifier.lower()}",
                "validation_spec_id": f"VAL-{identifier}",
                "status_boundary": "Frozen architecture, audited candidate, or conditional interface only; no accepted root proof or theorem completion.",
                "task_ids": [ITEM, "S56-M-0474-PROOF"],
                "owned_sources": owned_sources,
                "owner": "THM-M-0474 proof lane",
                "reviewer": "independent Stage1 integration lane",
                "validity": {
                    "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                    "review_due": "before proof acceptance",
                    "invalidation_inputs": [
                        "Statement.lean",
                        "anchor-audit.json",
                        "obligation-registry.json",
                        "typed-graphs.json",
                        "toolchain and dependency pins",
                    ],
                    "revocation_state": "provisional" if identifier in CHECKED_INTERFACES else "open",
                },
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
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "Exact statement and the visible semantic architecture of the pinned terminal sources. Eligibility and the denominator are derived without using candidate closure status, although scheduler order exposed the prior anchor audit.",
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
            "branching": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The source proof is uniform in p and a; p=2 and other boundary behavior are retained explicitly in M0474-S-BOUNDARY rather than split into proof branches.",
            },
            "computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No finite calculation, reflection, solver, native code, oracle, experiment, or certificate participates in the visible terminal proof chain.",
            },
        },
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "audited_candidate_obligation": oid("L-NAT"),
            "audited_candidate_classification": "M0-W_candidate_pending_proof_phase_and_master_acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. The exact candidate is not installed or accepted; H0, R0, audit completion, validation, release, and theorem completion remain open.",
    }

    def edge(edge_id: str, source: str, edge_type: str, target: str, reciprocal: str | None = None) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        return value

    requires = {
        oid("ROOT"): [oid("T-COMPOSE")],
        oid("T-COMPOSE"): [oid("L-NAT")],
        oid("L-NAT"): [oid("N-NAT-INT"), oid("N-COPRIME"), oid("L-INT")],
        oid("L-INT"): [oid("C-ZMOD-NONZERO"), oid("T-INT-ZMOD"), oid("L-ZMOD")],
        oid("L-ZMOD"): [oid("T-ZMOD-CARD"), oid("L-FINITE-FIELD")],
        oid("L-FINITE-FIELD"): [oid("C-UNIT"), oid("L-GROUP-CARD")],
    }
    proof: list[dict] = []
    for parent, children in requires.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            comp = f"CMP-{child}-{parent}"
            proof.extend(
                [
                    edge(req, parent, "proof_requires", child, comp),
                    edge(comp, child, "composes", parent, req),
                ]
            )

    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "logical_decomposition", oid("S-INTERFACE")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY")),
            edge("REF-ROOT-TRANSPORT", oid("ROOT"), "logical_decomposition", oid("S-TRANSPORT")),
        ],
        "provenance": [
            edge("PROV-NAT-BODY", oid("X-PROVENANCE"), "provenance_of", oid("L-NAT")),
            edge("PROV-GROUP-BODY", oid("X-PROVENANCE"), "provenance_of", oid("L-GROUP-CARD")),
            edge("SRC-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-CHAIN", oid("X-SOURCE"), "source_map", oid("L-FINITE-FIELD")),
        ],
        "evidence": [
            edge("EVID-NAT-PROVENANCE", oid("X-PROVENANCE"), "evidence_for", oid("L-NAT")),
            edge("EVID-WORKFLOW-ROOT", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-PROVENANCE", oid("ROOT"), "trusts", oid("X-PROVENANCE")),
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-CHAIN", oid("X-READABLE"), "documents", oid("L-INT")),
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge("FLOW-ROOT-PROOF", oid("ROOT"), "workflow_depends_on", oid("L-NAT")),
            edge("FLOW-PROV-PROOF", oid("X-PROVENANCE"), "workflow_depends_on", oid("L-NAT")),
            edge("FLOW-WORKFLOW-PROV", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
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
        "registry_id": "THM-M-0474-OBLIGATIONS-v1",
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
                oid("L-NAT"),
                oid("X-SOURCE"),
                oid("S-FOUNDATION"),
                oid("X-PROVENANCE"),
                oid("X-READABLE"),
                oid("X-WORKFLOW"),
            ],
            "composition_certificates": [
                "Stage1Instances.THM_M_0474.ObligationTree.root_of_exactNatAnchor"
            ],
            "reason": "The composition is conditional and the exact pinned anchor remains uninstalled and unaccepted until the proof phase and master validation.",
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
                "argv": ["python3", "Stage1_Instances/THM-M-0474/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 60,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [
                    {
                        "path_or_stream": "stdout",
                        "semantic_hash_policy": "contains PASS THM-M-0474 obligation tree",
                    }
                ],
                "covered_obligation_ids": [identifier],
                "covered_declarations": (
                    ["Stage1Instances.THM_M_0474.ObligationTree.root_of_exactNatAnchor"]
                    if identifier == oid("T-COMPOSE")
                    else ["Nat.ModEq.pow_card_sub_one_eq_one"]
                    if identifier == oid("L-NAT")
                    else []
                ),
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
    print(values[0]["denominator_sha256"])


if __name__ == "__main__":
    main()
