#!/usr/bin/env python3
"""Deterministically build the THM-M-0115 obligation registry and typed graphs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0115-OBLIGATION_TREE"
THEOREM = "THM-M-0115"
REGISTRY_ID = "THM-M-0115-OBLIGATIONS-v1"
STATEMENT_EXPRESSION_SHA256 = (
    "eada246ab2968c378c5b6c31c2ffd84c10873d9206b499457c451ae3848c160e"
)
FOUNDATION = "lean4-mathlib-classical/policy-audit-pending"
TCB = "lean-4.29.0+mathlib-8a178386/transitive-closure-pending"
OWNER = "THM-M-0115 proof lane"
REVIEWER = "independent Stage1 integration lane"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(identifier: str, statement: str) -> str:
    if identifier in {"M0115-ROOT", "M0115-S-TARGET"}:
        return f"lean-expression-sha256:{STATEMENT_EXPRESSION_SHA256}"
    payload = {
        "context": STATEMENT_EXPRESSION_SHA256,
        "obligation_id": identifier,
        "statement": statement,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return f"planned-context-sha256:{digest}"


def obligation(
    identifier: str,
    kind: str,
    statement: str,
    *,
    machine: str = "required",
    human: str = "required",
    readable_: str = "required",
    risk: str = "high",
    exclusion: dict | None = None,
) -> dict:
    return {
        "obligation_id": identifier,
        "statement_fingerprint": fingerprint(identifier, statement),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human,
        "readable_eligibility": readable_,
        "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": None,
        "human_statement": statement,
    }


ROWS = [
    obligation("M0115-ROOT", "root", "The exact frozen Grothendieck-Riemann-Roch target for every proper morphism of nonsingular quasi-projective varieties over a field and every K_0 class.", risk="critical"),
    obligation("M0115-S-TARGET", "definition", "Freeze the elaborated public target, expanded target, ordered binders, and exact formula without proof credit.", risk="critical"),
    obligation("M0115-S-DOMAIN", "definition", "Verify that X and Y are varieties over one field, their structure maps are smooth and quasi-projective, f is over the base, and f is proper.", risk="critical"),
    obligation("M0115-S-KZERO", "definition", "Construct or integrate the selected scheme K_0 family and prove that it models the Grothendieck group with the relations required by GRR.", risk="critical"),
    obligation("M0115-S-CHOW", "definition", "Construct or integrate rational Chow homology with its grading, coefficient, and cap-product conventions.", risk="critical"),
    obligation("M0115-S-OPERATIONS", "definition", "Construct both proper pushforwards, Chern characters, tangent classes, Todd classes, and cap actions with their exact semantic compatibility.", risk="critical"),
    obligation("M0115-S-BOUNDARY", "branch", "Cover empty varieties and alpha = 0 while excluding singular, non-quasi-projective, nonproper, and non-base-compatible inputs only through the frozen hypotheses."),
    obligation("M0115-S-TRANSPORT", "transport", "Check the public alias, expanded target, source cap notation, and any relative or multiplication form in each claimed direction.", risk="critical"),
    obligation("M0115-S-FOUNDATION", "certificate", "Audit the logic, quotient/extensionality principles, imported axioms, computation policy, and complete TCB boundary.", human="not_applicable", risk="critical", exclusion={"code": "non_human_source_trust_axis", "justification": "Foundation and TCB acceptance is governed by trust evidence rather than a mathematical source proof.", "review": "pending independent integration review"}),
    obligation("M0115-N-PERFECT", "normalization", "Normalize alpha to the chosen perfect-complex or vector-bundle representative model and prove independence of that choice.", risk="critical"),
    obligation("M0115-N-FACTORIZATION", "normalization", "Reduce an arbitrary proper morphism in the frozen scope to the factorization or deformation setting used by the selected human proof.", risk="critical"),
    obligation("M0115-B-FACTOR", "branch", "Split the normalized morphism into the source-proof cases, prove the cases exhaustive, and expose the recomposition theorem.", risk="critical"),
    obligation("M0115-C-DEFORMATION", "construction", "Construct the deformation or graph-factorization space, its closed/open pieces, and all maps used by the proof.", risk="critical"),
    obligation("M0115-C-NORMAL", "construction", "Prove well-definedness, flatness or regularity conditions, choice independence, and compatibility of the constructed deformation data.", risk="critical"),
    obligation("M0115-L-CHERN", "core_lemma", "Establish additivity and functoriality of the Chern character for the exact K_0 and Chow models."),
    obligation("M0115-L-TODD", "core_lemma", "Establish the tangent-bundle and Todd-class identities needed for the source and target varieties."),
    obligation("M0115-L-PROJECTION", "core_lemma", "Prove the Chow projection formula and compatibility of cap product with proper pushforward."),
    obligation("M0115-L-IMMERSION", "core_lemma", "Prove the GRR comparison for the regular closed-immersion case, including the normal-bundle correction.", risk="critical"),
    obligation("M0115-L-PROJECTION_CASE", "core_lemma", "Prove the GRR comparison for the smooth/projective-bundle projection case selected by the factorization route.", risk="critical"),
    obligation("M0115-L-COMPOSE", "core_lemma", "Prove that the GRR comparison is stable under composition of the factored morphisms.", risk="critical"),
    obligation("M0115-X-MATHLIB", "bridge", "Bind and audit all pinned mathlib geometry, sheaf, derived, and group-completion substrate actually consumed by later proof work.", human="not_applicable", risk="high", exclusion={"code": "formal_import_boundary", "justification": "This records formal substrate provenance, not a separately sourced mathematical claim.", "review": "pending independent integration review"}),
    obligation("M0115-X-EXTERNAL", "bridge", "Integrate any future external Lean GRR body only after exact-statement transport, placeholder, trust, license, and content-binding checks.", risk="critical"),
    obligation("M0115-X-SOURCE", "terminal", "Map every material definition, reduction, construction, and lemma to pinpoint primary-source records, assumptions, corrections, and independent review.", machine="informational", readable_="not_applicable", risk="critical", exclusion={"code": "human_source_overlay", "justification": "This is the H-axis acceptance boundary and is not an independent machine proof premise.", "review": "pending independent source review"}),
    obligation("M0115-X-PROVENANCE", "terminal", "Resolve every wrapper, terminal declaration, proof-body origin, direct dependency, and transitive trust closure.", machine="informational", human="not_applicable", readable_="not_applicable", risk="critical", exclusion={"code": "provenance_overlay", "justification": "Provenance governs evidence admissibility and does not itself imply GRR.", "review": "pending independent integration review"}),
    obligation("M0115-X-EVIDENCE", "certificate", "Bind exact validation specifications, receipts, expression hashes, source hashes, logs, and invalidation inputs.", machine="informational", human="not_applicable", readable_="not_applicable", risk="critical", exclusion={"code": "evidence_overlay", "justification": "Evidence records validate proof claims but are not mathematical premises.", "review": "pending independent integration review"}),
    obligation("M0115-X-TRUST", "certificate", "Close the foundation, axiom, TCB, computation, offline replay, and reproducibility audits.", machine="informational", human="not_applicable", readable_="not_applicable", risk="critical", exclusion={"code": "release_trust_overlay", "justification": "Trust closure is a release gate and does not replace a proof premise.", "review": "pending independent trust review"}),
    obligation("M0115-X-READABLE", "terminal", "Produce unique anchored short and long reconstructions and obtain independent R0 review.", machine="informational", human="not_applicable", risk="high", exclusion={"code": "documentation_overlay", "justification": "Readable reconstruction is independently accepted and cannot close machine proof nodes.", "review": "pending independent reader review"}),
    obligation("M0115-X-WORKFLOW", "terminal", "Execute dependency-ordered proof, validation, release, freshness, revocation, and master-acceptance tasks.", machine="informational", human="not_applicable", readable_="not_applicable", risk="high", exclusion={"code": "workflow_overlay", "justification": "Workflow state orders acceptance but is not a theorem premise.", "review": "pending independent integration review"}),
    obligation("M0115-T-RELATIVE", "terminal", "Derive the relative Chern-character and proper-pushforward comparison from the factored source proof.", risk="critical"),
    obligation("M0115-T-TODD_ACTION", "terminal", "Transport the relative comparison through the target Todd factor to the exact frozen absolute formula.", risk="critical"),
    obligation("M0115-T-FORMULA", "terminal", "Deliver D.Formula alpha for every frozen datum, hypothesis package, and K_0 class.", risk="critical"),
    obligation("M0115-T-ASSEMBLE", "terminal", "Kernel-check the exact child-to-root composition, statement fingerprints, and axiom report without inhabiting open premises.", risk="critical"),
]

PROJECTION_FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)


def projection(rows: list[dict]) -> list[dict]:
    return [{field: row[field] for field in PROJECTION_FIELDS} for row in rows]


def denominator(rows: list[dict]) -> str:
    return hashlib.sha256(
        json.dumps(projection(rows), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


PROOF_CHILDREN = {
    "M0115-ROOT": ["M0115-T-ASSEMBLE"],
    "M0115-T-ASSEMBLE": ["M0115-T-FORMULA"],
    "M0115-T-FORMULA": ["M0115-T-RELATIVE", "M0115-T-TODD_ACTION"],
    "M0115-T-RELATIVE": ["M0115-B-FACTOR", "M0115-L-CHERN", "M0115-L-PROJECTION", "M0115-L-COMPOSE"],
    "M0115-T-TODD_ACTION": ["M0115-L-TODD", "M0115-L-PROJECTION"],
    "M0115-B-FACTOR": ["M0115-N-PERFECT", "M0115-N-FACTORIZATION", "M0115-L-IMMERSION", "M0115-L-PROJECTION_CASE"],
    "M0115-N-PERFECT": ["M0115-S-KZERO", "M0115-S-OPERATIONS"],
    "M0115-N-FACTORIZATION": ["M0115-S-DOMAIN", "M0115-C-DEFORMATION", "M0115-C-NORMAL"],
    "M0115-L-CHERN": ["M0115-S-KZERO", "M0115-S-CHOW", "M0115-S-OPERATIONS"],
    "M0115-L-TODD": ["M0115-S-DOMAIN", "M0115-S-CHOW", "M0115-S-OPERATIONS"],
    "M0115-L-PROJECTION": ["M0115-S-CHOW", "M0115-S-OPERATIONS"],
    "M0115-L-IMMERSION": ["M0115-C-DEFORMATION", "M0115-C-NORMAL", "M0115-L-CHERN", "M0115-L-TODD"],
    "M0115-L-PROJECTION_CASE": ["M0115-C-DEFORMATION", "M0115-L-CHERN", "M0115-L-TODD", "M0115-L-PROJECTION"],
    "M0115-L-COMPOSE": ["M0115-S-OPERATIONS", "M0115-L-PROJECTION"],
}

CHECKED_COMPOSITIONS = {
    "M0115-ROOT": "Stage1Instances.THMM0115.ObligationTree.root_of_assembled_root_package",
    "M0115-T-ASSEMBLE": "Stage1Instances.THMM0115.ObligationTree.assembled_root_package_of_formula_package",
    "M0115-T-FORMULA": "Stage1Instances.THMM0115.ObligationTree.formula_package_of_relative_and_todd",
}


def node(row: dict) -> dict:
    identifier = row["obligation_id"]
    proof_children = PROOF_CHILDREN.get(identifier, [])
    ledger_steps = [
        {
            "step_id": f"{identifier}-STEP-{index:02d}",
            "premise_ids": children if index == 1 else [f"{identifier}-STEP-{index - 1:02d}"],
            "inference": inference,
            "output": output,
            "outgoing_use": use,
        }
        for index, (children, inference, output, use) in enumerate((
            (proof_children or ["frozen formal context"], "unpack the exact node context and declared inputs", f"the binders and hypotheses of {identifier}", f"{identifier}-STEP-02"),
            ([], "apply only the named mathematical or formal interface of this obligation", row["human_statement"], f"{identifier}-STEP-03"),
            ([], "package the exact output under the frozen statement fingerprint", f"the declared output of {identifier}", "the declared typed parent edge or release overlay"),
        ), start=1)
    ]
    source_map = "M0115-X-SOURCE" if row["human_source_eligibility"] == "required" and identifier != "M0115-X-SOURCE" else "not-applicable"
    return {
        "node_id": f"THM-M-0115-{identifier.removeprefix('M0115-')}",
        "obligation_id": identifier,
        "kind": row["kind"],
        "human_statement": row["human_statement"],
        "formal_target": {
            "M0115-ROOT": "Stage1Instances.THMM0115.GrothendieckRiemannRochTarget",
            "M0115-S-TARGET": "Stage1Instances.THMM0115.GrothendieckRiemannRochExpandedTarget",
            "M0115-T-RELATIVE": "Stage1Instances.THMM0115.ObligationTree.RelativeComparisonPackage",
            "M0115-T-TODD_ACTION": "Stage1Instances.THMM0115.ObligationTree.TargetToddActionPackage",
            "M0115-T-FORMULA": "Stage1Instances.THMM0115.ObligationTree.FormulaPackage",
            "M0115-T-ASSEMBLE": "Stage1Instances.THMM0115.ObligationTree.AssembledRootPackage",
        }.get(identifier, f"planned exact signature bound by {row['statement_fingerprint']}"),
        "output": row["human_statement"],
        "human_debt": "H4",
        "machine_debt": "M3" if identifier in {"M0115-ROOT", "M0115-S-TARGET", "M0115-T-ASSEMBLE"} else "M4",
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": source_map,
        "provenance_id": "none; no accepted terminal proof body",
        "foundation_profile": FOUNDATION,
        "tcb_profile": TCB,
        "computation_record": "none; the selected architecture is symbolic and no oracle, experiment, or unchecked certificate is credited",
        "step_budget": 12 if not proof_children else 30,
        "semantic_step_ledger": ledger_steps,
        "public_readable_target": f"Stage1_Instances/THM-M-0115/obligation-tree.md#{identifier.lower()}",
        "validation_spec_id": f"VAL-{identifier}",
        "status_boundary": "Architecture or conditional interface only. No open mathematical premise is inhabited and no obligation receives closure credit.",
        "task_ids": [ITEM, "S56-M-0115-PROOF", "S56-M-0115-VALIDATION"],
        "owned_sources": ["Stage1_Instances/THM-M-0115/ObligationTree.lean"] if identifier in CHECKED_COMPOSITIONS else [],
        "owner": OWNER,
        "reviewer": REVIEWER,
        "validity": {
            "validated_at": None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["Statement.lean", "statement.json", "anchor-audit.json", "obligation registry", "typed graphs", "toolchain"],
            "revocation_state": "open",
        },
    }


def empty_graph(name: str) -> dict:
    ids = [row["obligation_id"] for row in ROWS]
    return {"graph_type": name, "edges": [], "out": {identifier: [] for identifier in ids}, "in": {identifier: [] for identifier in ids}}


def add_edge(graph: dict, edge: dict) -> None:
    graph["edges"].append(edge)
    graph["out"][edge["from"]].append(edge["edge_id"])
    graph["in"][edge["to"]].append(edge["edge_id"])


def build_graphs(rows: list[dict], digest: str) -> dict:
    graphs = {name: empty_graph(name) for name in GRAPH_NAMES}
    row_by_id = {row["obligation_id"]: row for row in rows}
    pair_index = 0
    for parent, children in PROOF_CHILDREN.items():
        for child in children:
            pair_index += 1
            forward_id = f"M0115-PROOF-{pair_index:03d}-REQUIRES"
            reverse_id = f"M0115-PROOF-{pair_index:03d}-COMPOSES"
            reverse_type = "composes" if parent in CHECKED_COMPOSITIONS else "logical_decomposition"
            add_edge(graphs["proof"], {
                "edge_id": forward_id,
                "type": "proof_requires",
                "from": parent,
                "to": child,
                "reciprocal_edge_id": reverse_id,
                "affects_machine_closure": True,
            })
            add_edge(graphs["proof"], {
                "edge_id": reverse_id,
                "type": reverse_type,
                "from": child,
                "to": parent,
                "reciprocal_edge_id": forward_id,
                "affects_machine_closure": True,
            })

    refinement_index = 0
    for parent, children in PROOF_CHILDREN.items():
        for child in children:
            refinement_index += 1
            add_edge(graphs["refinement"], {
                "edge_id": f"M0115-REFINE-{refinement_index:03d}",
                "type": "logical_decomposition",
                "from": parent,
                "to": child,
                "affects_machine_closure": True,
            })

    provenance_index = 0
    for row in rows:
        identifier = row["obligation_id"]
        if row["human_source_eligibility"] == "required" and identifier != "M0115-X-SOURCE":
            provenance_index += 1
            add_edge(graphs["provenance"], {
                "edge_id": f"M0115-SOURCE-{provenance_index:03d}",
                "type": "source_map",
                "from": identifier,
                "to": "M0115-X-SOURCE",
                "affects_machine_closure": False,
            })
    for source, destination in (("M0115-X-MATHLIB", "M0115-X-PROVENANCE"), ("M0115-X-EXTERNAL", "M0115-X-PROVENANCE")):
        provenance_index += 1
        add_edge(graphs["provenance"], {
            "edge_id": f"M0115-PROVENANCE-{provenance_index:03d}",
            "type": "provenance_of",
            "from": source,
            "to": destination,
            "affects_machine_closure": False,
        })

    for index, source in enumerate(("M0115-S-FOUNDATION", "M0115-X-MATHLIB", "M0115-X-EXTERNAL"), start=1):
        add_edge(graphs["trust"], {
            "edge_id": f"M0115-TRUST-{index:03d}",
            "type": "trusts",
            "from": "M0115-ROOT",
            "to": source,
            "affects_machine_closure": False,
        })
    add_edge(graphs["trust"], {
        "edge_id": "M0115-TRUST-004",
        "type": "trusts",
        "from": "M0115-X-TRUST",
        "to": "M0115-X-EVIDENCE",
        "affects_machine_closure": False,
    })

    for index, row in enumerate(rows, start=1):
        identifier = row["obligation_id"]
        if row["readable_eligibility"] == "required" and identifier != "M0115-X-READABLE":
            add_edge(graphs["documentation"], {
                "edge_id": f"M0115-DOC-{index:03d}",
                "type": "documents",
                "from": "M0115-X-READABLE",
                "to": identifier,
                "affects_machine_closure": False,
            })

    workflow_order = [
        "M0115-S-TARGET", "M0115-X-SOURCE", "M0115-S-DOMAIN", "M0115-S-KZERO",
        "M0115-S-CHOW", "M0115-S-OPERATIONS", "M0115-N-PERFECT",
        "M0115-N-FACTORIZATION", "M0115-C-DEFORMATION", "M0115-C-NORMAL",
        "M0115-L-CHERN", "M0115-L-TODD", "M0115-L-PROJECTION",
        "M0115-L-IMMERSION", "M0115-L-PROJECTION_CASE", "M0115-L-COMPOSE",
        "M0115-T-RELATIVE", "M0115-T-TODD_ACTION", "M0115-T-FORMULA",
        "M0115-T-ASSEMBLE", "M0115-X-PROVENANCE", "M0115-X-EVIDENCE",
        "M0115-X-TRUST", "M0115-X-READABLE", "M0115-ROOT", "M0115-X-WORKFLOW",
    ]
    for index, (dependency, task) in enumerate(zip(workflow_order, workflow_order[1:]), start=1):
        add_edge(graphs["workflow"], {
            "edge_id": f"M0115-WORK-{index:03d}",
            "type": "workflow_depends_on",
            "from": task,
            "to": dependency,
            "affects_machine_closure": False,
        })

    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in rows}
    certificates = []
    for parent, declaration in CHECKED_COMPOSITIONS.items():
        children = PROOF_CHILDREN[parent]
        certificates.append({
            "certificate_id": f"M0115-COMP-{parent.removeprefix('M0115-')}",
            "parent_obligation_id": parent,
            "parent_statement_fingerprint": fingerprints[parent],
            "required_child_ids": children,
            "required_child_statement_fingerprints": {child: fingerprints[child] for child in children},
            "certificate_kind": "lean_abstract_child_harness",
            "checked_declaration": declaration,
            "status": "provisionally_elaborated_not_accepted",
            "consumes_all_required_children": True,
            "yields_exact_parent": True,
            "introduces_undeclared_premises": False,
        })
    plans = [
        {
            "parent_obligation_id": parent,
            "planned_child_ids": children,
            "status": "source_architecture_decomposition_unverified_as_child_to_parent_composition",
            "boundary": "The later proof phase must add an exact checked composition certificate before this parent can receive machine closure.",
        }
        for parent, children in PROOF_CHILDREN.items()
        if parent not in CHECKED_COMPOSITIONS
    ]
    edge_count = sum(len(graph["edges"]) for graph in graphs.values())
    return {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": REGISTRY_ID,
        "registry_denominator_sha256": digest,
        "root_node_id": "M0115-ROOT",
        "edge_direction": "proof_requires runs parent to required child; reciprocal composes or logical_decomposition runs child to parent; overlay graphs declare their direction per edge type.",
        "nodes": [node(row) for row in rows],
        "graphs": graphs,
        "composition_certificates": certificates,
        "unverified_decomposition_plans": plans,
        "edge_count": edge_count,
        "closure_boundary": {
            "closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "remaining_machine_root_cut_set": ["M0115-T-RELATIVE", "M0115-T-TODD_ACTION"],
            "audit_complete": False,
            "theorem_complete": False,
            "status_boundary": "Typed architecture and three conditional Lean compositions only; no proof premise is inhabited and no closure is accepted.",
        },
    }


def registry(rows: list[dict], digest: str) -> dict:
    ids = [row["obligation_id"] for row in rows]
    mandatory = {
        "S": [identifier for identifier in ids if "-S-" in identifier],
        "N": [identifier for identifier in ids if "-N-" in identifier],
        "B": [identifier for identifier in ids if "-B-" in identifier],
        "C": [identifier for identifier in ids if "-C-" in identifier],
        "L": [identifier for identifier in ids if "-L-" in identifier],
        "X": [identifier for identifier in ids if "-X-" in identifier],
        "T": [identifier for identifier in ids if "-T-" in identifier] + ["M0115-ROOT"],
    }
    return {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "registry_id": REGISTRY_ID,
        "registry_version": 1,
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "root_obligation_id": "M0115-ROOT",
        "frozen_at": "2026-07-17T00:00:00+08:00",
        "freeze_basis": "The exact elaborated target, the bounded formal-anchor audit, and the classical source architecture for the frozen nonsingular quasi-projective variety formula. Eligibility is fixed by semantic role before machine status is attached.",
        "freeze_order_boundary": "The canonical ten-field projection below contains no proof status. Its digest is computed before status_observed_after_freeze is attached.",
        "frozen_against_statement_sha256": sha256(HERE / "Statement.lean"),
        "frozen_against_statement_record_sha256": sha256(HERE / "statement.json"),
        "frozen_against_anchor_audit_sha256": sha256(HERE / "anchor-audit.json"),
        "canonical_projection_fields": list(PROJECTION_FIELDS),
        "denominator_sha256": digest,
        "obligations": projection(rows),
        "obligation_statements": {row["obligation_id"]: row["human_statement"] for row in rows},
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in rows if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in rows if row["machine_eligibility"] == "informational"],
        },
        "mandatory_layer_analysis": {**mandatory, "not_applicable_layers": []},
        "layer_exclusions": {
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The selected proof architecture is symbolic. No solver, native evaluator, numerical experiment, external oracle, or unchecked certificate is part of the route.",
                "reviewer": REVIEWER,
            },
            "extra_boundary_branches": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The exact target already quantifies over empty objects and alpha = 0; all out-of-scope cases are excluded by explicit frozen hypotheses rather than hidden case splits.",
                "reviewer": REVIEWER,
            },
        },
        "append_only_delta": [],
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility, edge-role, risk, or terminal-body change requires registry version 2 and an append-only old/new ID delta.",
        "status_observed_after_freeze": {
            "canonical_statement": "M3_exact_statement_interface_only",
            "bounded_anchor_inventory": "no_valid_exact_proof_anchor",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
            "root_human_debt": "H4",
            "root_readability_debt": "R4",
        },
        "status_boundary": "Registry scope, eligibility, and denominators only. Conditional interface checks close no mathematical obligation; AUDIT-Z and theorem completion remain false.",
    }


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> None:
    digest = denominator(ROWS)
    write_json(HERE / "obligation-registry.json", registry(ROWS, digest))
    bundle = build_graphs(ROWS, digest)
    write_json(HERE / "typed-graphs.json", bundle)
    print(json.dumps({
        "theorem_id": THEOREM,
        "obligation_count": len(ROWS),
        "typed_edge_count": bundle["edge_count"],
        "registry_denominator_sha256": digest,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
