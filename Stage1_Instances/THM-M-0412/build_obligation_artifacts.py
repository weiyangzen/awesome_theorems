#!/usr/bin/env python3
"""Build the status-independent THM-M-0412 obligation architecture."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0412-OBLIGATION_TREE"
THEOREM = "THM-M-0412"
STATEMENT_SHA256 = "1c4ca90f92ad2d74e7e6abe4124b57e623a8218312ed88f38626ae0b096edd65"
STATEMENT_RECORD_SHA256 = "f1c06c651eb29495e03b0c833941f55ebe61bbacdf08f93b50d045e50ef28cfd"
ANCHOR_SHA256 = "bac3854ea0523b4b7b977e71a2f81924d69a72e353b0cc8fd6f7f9b2e85f919f"

PROJECTION_FIELDS = (
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

STATEMENTS = {
    "M0412-ROOT-IDENTITY": (
        "Identify, from an immutable independently reviewed source, the one exact mathematical "
        "proposition denoted by the THM-M-0412 catalog entry."
    ),
    "M0412-S-SOURCE": (
        "Bind the primary publication, edition, theorem or page locator, original title, author, "
        "year, corrections, and translation or transliteration crosswalk."
    ),
    "M0412-S-CLAIM": (
        "Transcribe the exact human claim, including the cubic equation or family, domains, ordered "
        "binders, parameters, hypotheses, conclusion, and proof boundary."
    ),
    "M0412-S-DOMAIN": (
        "Fix the number systems, curve and point models, nonsingularity conditions, coercions, and "
        "all universe or typeclass assumptions required by the exact claim."
    ),
    "M0412-S-BOUNDARY": (
        "Classify every degenerate or boundary case named or implied by the source, including singular "
        "curves, zero discriminant, exceptional parameters, and points at infinity where applicable."
    ),
    "M0412-S-TRANSPORT": (
        "Check both required directions between the source formulation and the canonical Lean "
        "encoding without weakening either statement."
    ),
    "M0412-S-FOUNDATION": (
        "Freeze the logic, choice, quotient, extensionality, computation, kernel, dependency, and "
        "axiom policy for the eventual exact target."
    ),
    "M0412-N-CURVE": (
        "Normalize the exact source curve or curve family into a canonical integral or rational "
        "Weierstrass model, proving preservation of every source hypothesis and conclusion."
    ),
    "M0412-N-POINT": (
        "Normalize point coordinates and arithmetic data to the primitive, reduced, or integral "
        "representatives required by the exact claim."
    ),
    "M0412-N-TRANSPORT": (
        "Transport all conclusions from normalized curve and point data back to the original source "
        "objects, with independence of choices."
    ),
    "M0412-B-DEGENERATE": (
        "Discharge every source-authorized degenerate and exceptional case under its exact hypotheses."
    ),
    "M0412-B-GENERIC": (
        "Handle the complementary nonsingular generic case after proving that the branch split is exhaustive."
    ),
    "M0412-B-RECOMPOSE": (
        "Prove exhaustiveness, incompatibility where required, and exact recomposition of all boundary "
        "and generic branches."
    ),
    "M0412-C-MODEL": (
        "Construct the selected curve, discriminant, point, torsion, divisor, or descent objects from "
        "the exact normalized source data."
    ),
    "M0412-C-WELLDEFINED": (
        "Prove that every constructed object is well-defined and satisfies its required curve, field, "
        "integrality, and nonsingularity conditions."
    ),
    "M0412-C-INVARIANTS": (
        "Establish the arithmetic and geometric invariants consumed by the core proof, including all "
        "discriminant or coordinate relations actually required by the resolved theorem."
    ),
    "M0412-C-COMPATIBILITY": (
        "Prove functoriality, representation independence, and compatibility of constructed objects "
        "with normalization and branch transports."
    ),
    "M0412-L-ARITHMETIC": (
        "Prove the central Diophantine arithmetic lemma for the resolved cubic equation or family, "
        "with every descent, divisibility, valuation, and coprimality step exposed."
    ),
    "M0412-L-GEOMETRIC": (
        "Prove the central elliptic-curve or cubic-curve lemma connecting the constructed invariants "
        "to the exact finiteness, integrality, torsion, or classification conclusion."
    ),
    "M0412-L-CLASSIFY": (
        "Complete the source theorem's existence, finiteness, uniqueness, exclusion, or classification "
        "argument and derive the terminal generic-branch conclusion."
    ),
    "M0412-X-IMPORTED": (
        "Inventory every imported Lean theorem, wrapper, terminal proof body, statement fingerprint, "
        "source byte hash, and checked consumer-owned transport used by the proof."
    ),
    "M0412-X-SOURCE": (
        "Map every material premise, transition, and conclusion to pinpoint primary-source records and "
        "an independent human-source review."
    ),
    "M0412-X-PROVENANCE": (
        "Close wrapper, alias, terminal-body, dependency, license, and consumer-owned provenance for "
        "every formal boundary without transferring provider acceptance."
    ),
    "M0412-X-TRUST": (
        "Close the Lean kernel, axiom, foundation, computation, dependency, toolchain, and reproducibility "
        "trust boundary."
    ),
    "M0412-X-READABLE": (
        "Produce and independently review the bidirectionally anchored readable reconstruction for all "
        "root-critical obligations."
    ),
    "M0412-X-WORKFLOW": (
        "Obtain dependency-ordered worker, validation, independent-review, and master receipts without "
        "using checkbox state as proof evidence."
    ),
    "M0412-T-GENERIC": (
        "Derive the exact source conclusion for the generic branch from the completed construction and core lemmas."
    ),
    "M0412-T-TRANSPORT": (
        "Transport the branch conclusions through every checked equivalence back to the exact canonical source statement."
    ),
    "M0412-T-ASSEMBLE": (
        "Consume all exact branch conclusions and boundary results to yield the complete resolved THM-M-0412 root target."
    ),
}

KINDS = {
    "ROOT-IDENTITY": "root",
    "S-SOURCE": "definition",
    "S-CLAIM": "definition",
    "S-DOMAIN": "definition",
    "S-BOUNDARY": "branch",
    "S-TRANSPORT": "transport",
    "S-FOUNDATION": "certificate",
    "N-CURVE": "normalization",
    "N-POINT": "normalization",
    "N-TRANSPORT": "transport",
    "B-DEGENERATE": "branch",
    "B-GENERIC": "branch",
    "B-RECOMPOSE": "branch",
    "C-MODEL": "construction",
    "C-WELLDEFINED": "construction",
    "C-INVARIANTS": "construction",
    "C-COMPATIBILITY": "construction",
    "L-ARITHMETIC": "core_lemma",
    "L-GEOMETRIC": "core_lemma",
    "L-CLASSIFY": "core_lemma",
    "X-IMPORTED": "bridge",
    "X-SOURCE": "terminal",
    "X-PROVENANCE": "terminal",
    "X-TRUST": "certificate",
    "X-READABLE": "terminal",
    "X-WORKFLOW": "terminal",
    "T-GENERIC": "terminal",
    "T-TRANSPORT": "transport",
    "T-ASSEMBLE": "terminal",
}

RISKS = {
    "ROOT-IDENTITY": "critical",
    "S-SOURCE": "critical",
    "S-CLAIM": "critical",
    "S-DOMAIN": "high",
    "S-BOUNDARY": "high",
    "S-TRANSPORT": "critical",
    "S-FOUNDATION": "high",
    "N-CURVE": "critical",
    "N-POINT": "high",
    "N-TRANSPORT": "critical",
    "B-DEGENERATE": "high",
    "B-GENERIC": "critical",
    "B-RECOMPOSE": "critical",
    "C-MODEL": "critical",
    "C-WELLDEFINED": "critical",
    "C-INVARIANTS": "critical",
    "C-COMPATIBILITY": "high",
    "L-ARITHMETIC": "critical",
    "L-GEOMETRIC": "critical",
    "L-CLASSIFY": "critical",
    "X-IMPORTED": "high",
    "X-SOURCE": "critical",
    "X-PROVENANCE": "critical",
    "X-TRUST": "critical",
    "X-READABLE": "high",
    "X-WORKFLOW": "high",
    "T-GENERIC": "critical",
    "T-TRANSPORT": "critical",
    "T-ASSEMBLE": "critical",
}

MACHINE_INFORMATIONAL = {
    "M0412-S-SOURCE",
    "M0412-X-SOURCE",
    "M0412-X-PROVENANCE",
    "M0412-X-TRUST",
    "M0412-X-READABLE",
    "M0412-X-WORKFLOW",
}
HUMAN_NOT_APPLICABLE = {
    "M0412-S-FOUNDATION",
    "M0412-X-IMPORTED",
    "M0412-X-PROVENANCE",
    "M0412-X-TRUST",
    "M0412-X-WORKFLOW",
}
READABLE_NOT_APPLICABLE = {"M0412-X-WORKFLOW"}

EXCLUSIONS = {
    "M0412-S-FOUNDATION": {
        "code": "formal_policy_boundary",
        "justification": "The foundation profile is a formal trust policy rather than a human mathematical premise.",
        "review": "pending independent foundation review",
    },
    "M0412-X-IMPORTED": {
        "code": "formal_import_boundary",
        "justification": "Imported-body provenance is formal evidence and does not require a separate primary mathematical source.",
        "review": "pending independent provenance review",
    },
    "M0412-X-PROVENANCE": {
        "code": "formal_provenance_overlay",
        "justification": "Provenance binds formal artifacts and cannot replace a human proof premise.",
        "review": "pending independent provenance review",
    },
    "M0412-X-TRUST": {
        "code": "release_trust_overlay",
        "justification": "Trust closure is a release gate and is not a human mathematical transition.",
        "review": "pending independent trust review",
    },
    "M0412-X-WORKFLOW": {
        "code": "workflow_overlay",
        "justification": "Workflow ordering is neither a mathematical premise nor a readable proof node.",
        "review": "pending independent integration review",
    },
}


def planned_fingerprint(identifier: str, statement: str) -> str:
    payload = f"THM-M-0412|registry-v1|{identifier}|{statement}".encode()
    return "planned-identity-dependent-sha256:" + hashlib.sha256(payload).hexdigest()


def rows() -> list[dict]:
    result = []
    for identifier, statement in STATEMENTS.items():
        suffix = identifier.removeprefix("M0412-")
        result.append(
            {
                "obligation_id": identifier,
                "statement_fingerprint": planned_fingerprint(identifier, statement),
                "kind": KINDS[suffix],
                "root_relevant": True,
                "machine_eligibility": "informational" if identifier in MACHINE_INFORMATIONAL else "required",
                "human_source_eligibility": "not_applicable" if identifier in HUMAN_NOT_APPLICABLE else "required",
                "readable_eligibility": "not_applicable" if identifier in READABLE_NOT_APPLICABLE else "required",
                "risk_class": RISKS[suffix],
                "exclusion_reason": EXCLUSIONS.get(identifier),
                "terminal_proof_body_id": None,
            }
        )
    return result


ROWS = rows()

PROOF_CHILDREN = {
    "M0412-ROOT-IDENTITY": ["M0412-S-SOURCE", "M0412-S-CLAIM", "M0412-T-ASSEMBLE"],
    "M0412-S-CLAIM": ["M0412-S-DOMAIN", "M0412-S-BOUNDARY", "M0412-S-TRANSPORT", "M0412-S-FOUNDATION"],
    "M0412-N-CURVE": ["M0412-S-CLAIM", "M0412-S-DOMAIN"],
    "M0412-N-POINT": ["M0412-N-CURVE"],
    "M0412-N-TRANSPORT": ["M0412-N-CURVE", "M0412-N-POINT"],
    "M0412-B-DEGENERATE": ["M0412-S-BOUNDARY"],
    "M0412-C-MODEL": ["M0412-N-CURVE", "M0412-N-POINT"],
    "M0412-C-WELLDEFINED": ["M0412-C-MODEL"],
    "M0412-C-INVARIANTS": ["M0412-C-MODEL", "M0412-C-WELLDEFINED"],
    "M0412-C-COMPATIBILITY": ["M0412-C-INVARIANTS", "M0412-N-TRANSPORT"],
    "M0412-L-ARITHMETIC": ["M0412-C-INVARIANTS"],
    "M0412-L-GEOMETRIC": ["M0412-C-INVARIANTS", "M0412-C-COMPATIBILITY"],
    "M0412-L-CLASSIFY": ["M0412-L-ARITHMETIC", "M0412-L-GEOMETRIC"],
    "M0412-B-GENERIC": ["M0412-L-CLASSIFY"],
    "M0412-B-RECOMPOSE": ["M0412-B-DEGENERATE", "M0412-B-GENERIC"],
    "M0412-T-GENERIC": ["M0412-B-GENERIC", "M0412-L-CLASSIFY"],
    "M0412-T-TRANSPORT": ["M0412-T-GENERIC", "M0412-N-TRANSPORT"],
    "M0412-T-ASSEMBLE": ["M0412-B-RECOMPOSE", "M0412-T-TRANSPORT"],
}

REFINEMENT_CHILDREN = {
    "M0412-S-CLAIM": [
        "M0412-S-SOURCE",
        "M0412-S-DOMAIN",
        "M0412-S-BOUNDARY",
        "M0412-S-TRANSPORT",
        "M0412-S-FOUNDATION",
    ],
}

OVERLAYS = {
    "provenance": [
        ("M0412-ROOT-IDENTITY", "source_map", "M0412-S-SOURCE"),
        ("M0412-ROOT-IDENTITY", "source_map", "M0412-X-SOURCE"),
        ("M0412-L-ARITHMETIC", "provenance_of", "M0412-X-IMPORTED"),
        ("M0412-L-GEOMETRIC", "provenance_of", "M0412-X-IMPORTED"),
        ("M0412-T-ASSEMBLE", "provenance_of", "M0412-X-PROVENANCE"),
    ],
    "evidence": [
        ("M0412-S-SOURCE", "evidence_for", "M0412-X-SOURCE"),
        ("M0412-X-IMPORTED", "evidence_for", "M0412-X-PROVENANCE"),
        ("M0412-T-ASSEMBLE", "evidence_for", "M0412-X-PROVENANCE"),
    ],
    "trust": [
        ("M0412-ROOT-IDENTITY", "trusts", "M0412-X-TRUST"),
        ("M0412-S-FOUNDATION", "trusts", "M0412-X-TRUST"),
        ("M0412-X-IMPORTED", "trusts", "M0412-X-TRUST"),
    ],
    "documentation": [
        (identifier, "documents", "M0412-X-READABLE")
        for identifier in STATEMENTS
        if identifier != "M0412-X-READABLE"
    ],
    "workflow": [
        ("M0412-X-WORKFLOW", "workflow_depends_on", "M0412-S-SOURCE"),
        ("M0412-X-WORKFLOW", "workflow_depends_on", "M0412-X-PROVENANCE"),
        ("M0412-X-WORKFLOW", "workflow_depends_on", "M0412-X-TRUST"),
        ("M0412-X-WORKFLOW", "workflow_depends_on", "M0412-X-READABLE"),
        ("M0412-X-WORKFLOW", "workflow_depends_on", "M0412-T-ASSEMBLE"),
    ],
}


def projection(records: list[dict]) -> list[dict]:
    return [{field: row[field] for field in PROJECTION_FIELDS} for row in records]


def canonical_digest(records: list[dict]) -> str:
    raw = json.dumps(projection(records), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def graph(edges: list[dict]) -> dict:
    identifiers = list(STATEMENTS)
    outgoing = {identifier: [] for identifier in identifiers}
    incoming = {identifier: [] for identifier in identifiers}
    for edge in edges:
        outgoing[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build_graphs() -> dict:
    proof_edges = []
    for parent, children in PROOF_CHILDREN.items():
        for child in children:
            stem = f"{parent.removeprefix('M0412-')}--{child.removeprefix('M0412-')}"
            requires = f"PROOF-{stem}"
            composes = f"COMPOSE-{stem}"
            proof_edges.extend(
                [
                    {"edge_id": requires, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": composes},
                    {"edge_id": composes, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": requires},
                ]
            )
    refinement_edges = []
    for parent, children in REFINEMENT_CHILDREN.items():
        for child in children:
            stem = f"{parent.removeprefix('M0412-')}--{child.removeprefix('M0412-')}"
            forward = f"REFINE-{stem}"
            reverse = f"REFINE-BACK-{stem}"
            refinement_edges.extend(
                [
                    {"edge_id": forward, "from": parent, "type": "logical_decomposition", "to": child, "reciprocal_edge_id": reverse},
                    {"edge_id": reverse, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": forward},
                ]
            )
    result = {"proof": graph(proof_edges), "refinement": graph(refinement_edges)}
    for name, triples in OVERLAYS.items():
        edges = []
        for index, (source, edge_type, target) in enumerate(triples, 1):
            edges.append(
                {
                    "edge_id": f"{name.upper()}-{index:02d}-{source.removeprefix('M0412-')}--{target.removeprefix('M0412-')}",
                    "from": source,
                    "type": edge_type,
                    "to": target,
                }
            )
        result[name] = graph(edges)
    return result


def node(row: dict) -> dict:
    identifier = row["obligation_id"]
    children = PROOF_CHILDREN.get(identifier, [])
    first_premises = children or ["frozen exact source identity and formal context"]
    return {
        "node_id": f"THM-M-0412-{identifier.removeprefix('M0412-')}",
        "obligation_id": identifier,
        "kind": row["kind"],
        "human_statement": STATEMENTS[identifier],
        "formal_target": f"planned exact signature bound by {row['statement_fingerprint']}",
        "output": STATEMENTS[identifier],
        "human_debt": "H5",
        "machine_debt": "M4",
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "Stage1_Instances/THM-M-0412/source-statement-crosswalk.md#crosswalk-verdict",
        "provenance_id": "none; source identity and terminal proof body are unresolved",
        "foundation_profile": "lean4-plus-pinned-mathlib/policy-selection-blocked-by-target-identity",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no solver, oracle, experiment, or unchecked certificate is credited",
        "step_budget": 24 if row["risk_class"] == "critical" else 12,
        "semantic_step_ledger": [
            {
                "step_id": f"{identifier}-STEP-01",
                "premise_ids": first_premises,
                "inference": "unpack only the exact source-backed context and declared child conclusions",
                "output": f"the complete input boundary for {identifier}",
                "outgoing_use": f"{identifier}-STEP-02",
            },
            {
                "step_id": f"{identifier}-STEP-02",
                "premise_ids": [f"{identifier}-STEP-01"],
                "inference": "apply the named mathematical interface without substituting a nearby theorem or hiding a branch",
                "output": STATEMENTS[identifier],
                "outgoing_use": f"{identifier}-STEP-03",
            },
            {
                "step_id": f"{identifier}-STEP-03",
                "premise_ids": [f"{identifier}-STEP-02"],
                "inference": "bind the exact output fingerprint and hand it to every typed outgoing edge",
                "output": f"the declared output of {identifier}",
                "outgoing_use": "the declared proof, composition, provenance, documentation, or workflow edge",
            },
        ],
        "public_readable_target": f"Stage1_Instances/THM-M-0412/obligation-tree.md#{identifier.lower()}",
        "validation_spec_id": f"VAL-{identifier}",
        "status_boundary": "Planned identity-dependent architecture only. This node is not an exact source claim, formal theorem, proof body, or accepted obligation.",
        "task_ids": [ITEM, "S56-M-0412-PROOF", "S56-M-0412-VALIDATION"],
        "owned_sources": ["Stage1_Instances/THM-M-0412/ObligationTree.lean"] if identifier == "M0412-T-ASSEMBLE" else [],
        "owner": "THM-M-0412 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": [
                "source identity or primary-source crosswalk",
                "Statement.lean or statement.json",
                "anchor-audit.json",
                "obligation registry or typed graphs",
                "toolchain, dependency context, or acceptance contract",
            ],
            "revocation_state": "open",
        },
    }


def registry() -> dict:
    records = projection(ROWS)
    identifiers = [row["obligation_id"] for row in records]
    layers = {letter: [identifier for identifier in identifiers if identifier.startswith(f"M0412-{letter}-")] for letter in "SNBCLXT"}
    layers["not_applicable_layers"] = []
    return {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "freeze_basis": (
            "The exact source identity is unresolved. Before inspecting proof closure, this registry freezes the complete root-critical identity-resolution and conditional arithmetic-geometry architecture derivable without choosing a nearby theorem. Every planned fingerprint explicitly depends on later source resolution."
        ),
        "freeze_sequence": [
            "read source and statement blocker evidence",
            "derive mandatory S/N/B/C/L/X/T architecture without observing proof availability",
            "assign all eligibility and risk axes",
            "serialize canonical projection and freeze denominator",
            "only then record the all-open H5/M4/R4 status boundary",
        ],
        "frozen_against_statement_sha256": STATEMENT_SHA256,
        "frozen_against_statement_record_sha256": STATEMENT_RECORD_SHA256,
        "frozen_against_anchor_audit_sha256": ANCHOR_SHA256,
        "root_obligation_id": "M0412-ROOT-IDENTITY",
        "canonical_projection_fields": list(PROJECTION_FIELDS),
        "frozen_denominators": {
            "inventory": identifiers,
            "required_machine": [row["obligation_id"] for row in records if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in records if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in records if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in records if row["machine_eligibility"] == "informational"],
        },
        "denominator_sha256": canonical_digest(records),
        "delta_policy": "Any resolved target, split, merge, exclusion, or eligibility change requires registry version 2 with an append-only old/new ID delta; version 1 remains reportable.",
        "append_only_delta": [],
        "mandatory_layer_analysis": layers,
        "risk_review": {
            "status": "worker_classified_pending_independent_review",
            "critical_ids": [row["obligation_id"] for row in records if row["risk_class"] == "critical"],
            "boundary": "Critical status reflects source ambiguity, central arithmetic/geometric work, or terminal composition; it is independent of machine availability.",
        },
        "exclusion_review": {
            "status": "explicit_axis_exclusions_pending_independent_review",
            "records": [
                {"obligation_id": row["obligation_id"], **row["exclusion_reason"]}
                for row in records
                if row["exclusion_reason"] is not None
            ],
            "semantic_obligations_excluded": [],
        },
        "obligation_statements": STATEMENTS,
        "status_observed_after_freeze": {
            "root_vector": {"H": "H5", "M": "M4", "R": "R4"},
            "accepted_closed_obligations": [],
            "exact_formal_targets": [],
            "terminal_proof_body_ids": [],
            "boundary": "The frozen denominator is complete as a conditional architecture; unresolved identity prevents exact formal signatures and every proof-closure claim.",
        },
        "obligations": records,
    }


def bundle(registry_document: dict) -> dict:
    graphs = build_graphs()
    return {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_denominator_sha256": registry_document["denominator_sha256"],
        "nodes": [node(row) for row in registry_document["obligations"]],
        "graphs": graphs,
        "edge_count": sum(len(value["edges"]) for value in graphs.values()),
        "composition_certificates": [],
        "composition_ineligibility": {
            "status": "not_machine_eligible_no_exact_parent_or_child_targets",
            "composition_source": "Stage1_Instances/THM-M-0412/ObligationTree.lean",
            "source_is_declaration_free": True,
            "reason": "No exact human proposition, canonical Lean root, or exact child signatures exist. A Lean harness would necessarily invent or substitute a target, so no machine-eligible nonleaf composition is claimed.",
            "retry_condition": "Resolve and independently approve the exact source claim, elaborate its canonical root and every required child signature, then add checked certificates consuming exactly those children.",
        },
        "closure_boundary": {
            "closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M4",
            "remaining_machine_root_cut_set": ["M0412-ROOT-IDENTITY"],
            "audit_complete": False,
            "theorem_complete": False,
            "status_boundary": "Complete conditional architecture only. No exact formal target, proof body, composition certificate, human-source acceptance, readable acceptance, audit completion, or theorem completion exists.",
        },
    }


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    registry_document = registry()
    bundle_document = bundle(registry_document)
    write_json(HERE / "obligation-registry.json", registry_document)
    write_json(HERE / "typed-graphs.json", bundle_document)
    print(
        f"wrote {len(registry_document['obligations'])} obligations, "
        f"{bundle_document['edge_count']} typed edges, denominator "
        f"{registry_document['denominator_sha256']}"
    )


if __name__ == "__main__":
    main()
