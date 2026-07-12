#!/usr/bin/env python3
"""Build the deterministic THM-M-1014 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1014-OBLIGATION_TREE"
THEOREM = "THM-M-1014"
PREFIX = "M1014-"
PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"

ROWS = [
    ("ROOT", "root", "critical", "The exact frozen filtered continuous mapping theorem for probability measures.", "Stage1Instances.THM_M_1014.StatementShape", "The canonical Tendsto conclusion.", "H1", "M1", "R4", 6, "required", "required", "required"),
    ("S-EXACT", "definition", "high", "Preserve all universes, ordered binders, typeclasses, continuity premise, filter convergence premise, and pushforward conclusion.", "Stage1Instances.THM_M_1014.StatementShape", "The exact elaborated statement boundary.", "H1", "M0-L", "R3", 16, "required", "required", "required"),
    ("S-DOMAIN", "normalization", "high", "Fix ProbabilityMeasure, its weak topology, OpensMeasurableSpace on the source, and BorelSpace on the target.", "checked binder context in Statement.lean", "The domain and instance interface used by every proof node.", "H2", "M0-L", "R4", 12, "required", "not_applicable", "required"),
    ("S-BOUNDARY", "terminal", "normal", "Retain arbitrary filters and all constant, identity, Dirac, and degenerate-carrier cases admitted by the frozen instances.", "planned boundary probes for StatementShape", "No unstated nondegeneracy or sequentiality premise.", "H2", "M4", "R4", 16, "required", "required", "required"),
    ("S-TRANSPORT", "transport", "high", "Relate the human pushforward claim to ProbabilityMeasure.map with continuity-derived AEMeasurable witnesses in the declared direction.", "planned exact representation transport", "A checked route from the source formulation to the frozen Lean representation.", "H1", "M3", "R4", 20, "required", "required", "required"),
    ("S-FOUNDATION", "certificate", "high", "Audit the kernel, imports, classical choice, quotient, extensionality, noncomputability, and absence of computational proof credit.", "planned transitive trust and dependency certificate", "The accepted foundation and TCB boundary.", "H3", "M3", "R4", 18, "required", "not_applicable", "required"),
    ("N-WEAK-TOPOLOGY", "reduction", "high", "Reduce weak convergence to convergence of integrals against bounded continuous nonnegative test functions.", "ProbabilityMeasure.tendsto_iff_forall_lintegral_tendsto", "The integral test interface for source and mapped measures.", "H1", "M0-P", "R4", 30, "required", "required", "required"),
    ("C-COMPOSED-TEST", "construction", "normal", "For each bounded continuous target test function, construct its composition with f and preserve continuity, boundedness, nonnegativity, and measurability.", "pinned mathlib composition and measurability interfaces", "An admissible source-space weak-convergence test function.", "H1", "M0-P", "R4", 24, "required", "required", "required"),
    ("L-MAP-INTEGRAL", "core_lemma", "high", "Identify the integral of a target test function under the pushforward with the integral of its composition under the source measure.", "MeasureTheory.lintegral_map specialized inside the pinned terminal body", "The exact pushforward integral identity.", "H1", "M0-P", "R4", 26, "required", "required", "required"),
    ("L-TEST-LIMIT", "core_lemma", "critical", "Apply source weak convergence to each composed test function and rewrite both sides by the pushforward integral identity.", "terminal body of ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous", "Convergence of every mapped-measure test integral.", "H1", "M0-P", "R4", 30, "required", "required", "required"),
    ("X-PINNED", "bridge", "critical", "Consume the exact pinned mathlib theorem as the unique terminal proof body, without duplicate credit for aliases or wrappers.", "MeasureTheory.ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous", "The exact frozen root proposition.", "H1", "M0-P", "R4", 18, "required", "required", "required"),
    ("T-ASSEMBLE", "terminal", "critical", "Consume the exact pinned bridge conclusion and return the canonical proposition without changing its context.", "Stage1Instances.THM_M_1014.ObligationTree.root_of_continuousMappingTerminal", "The exact public root, conditional on the bridge premise.", "H1", "M0-W", "R3", 4, "required", "required", "required"),
    ("X-SOURCE", "terminal", "high", "Pinpoint-map every material transition to an accepted primary human source, including assumptions and errata.", "non-Lean human-source crosswalk", "Human mathematical provenance coverage.", "H1", "M3", "R4", 24, "informational", "required", "required"),
    ("X-PROVENANCE", "certificate", "high", "Record the unique terminal body, aliases, dependency revision, license, transitive declarations, and trust report.", "anchor-audit.json plus downstream provenance receipt", "Machine provenance and anti-duplication coverage.", "H3", "M3", "R4", 24, "informational", "not_applicable", "required"),
]

PROOF_CHILDREN = {"ROOT": ["T-ASSEMBLE"], "T-ASSEMBLE": ["X-PINNED"]}
REFINEMENTS = {
    "ROOT": ["S-EXACT", "S-DOMAIN", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION"],
    "X-PINNED": ["N-WEAK-TOPOLOGY", "C-COMPOSED-TEST", "L-MAP-INTEGRAL", "L-TEST-LIMIT"],
}


def oid(short):
    return PREFIX + short


def planned(short, human, formal):
    raw = f"v1\n{oid(short)}\n{human}\n{formal}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(raw).hexdigest()


def graph(edges, ids):
    out = {item: [] for item in ids}
    incoming = {item: [] for item in ids}
    for row in edges:
        out[row["from"]].append(row["edge_id"])
        incoming[row["to"]].append(row["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}


def make_edge(family, number, source, target, kind, reciprocal=None):
    row = {"edge_id": f"M1014-{family.upper()}-{number:03d}", "type": kind, "from": oid(source), "to": oid(target)}
    if reciprocal is not None:
        row["reciprocal_edge_id"] = reciprocal
    return row


def main():
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    body_id = f"mathlib:{PIN}:ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous"
    obligations = []
    nodes = []
    for short, kind, risk, human, formal, output, hdebt, mdebt, rdebt, budget, melig, helig, relig in ROWS:
        fingerprint = "lean-file-sha256:" + statement_hash if short in {"ROOT", "S-EXACT"} else planned(short, human, formal)
        terminal_id = body_id if short in {"N-WEAK-TOPOLOGY", "C-COMPOSED-TEST", "L-MAP-INTEGRAL", "L-TEST-LIMIT", "X-PINNED"} else ("local:ObligationTree.lean#root_of_continuousMappingTerminal" if short == "T-ASSEMBLE" else None)
        exclusion = "support_only_source_or_provenance_overlay" if melig == "informational" else None
        obligations.append({"obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind, "root_relevant": True, "machine_eligibility": melig, "human_source_eligibility": helig, "readable_eligibility": relig, "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": terminal_id})
        children = PROOF_CHILDREN.get(short, []) + REFINEMENTS.get(short, [])
        nodes.append({
            "node_id": f"{THEOREM}-{short}", "obligation_id": oid(short), "kind": kind,
            "human_statement": human, "formal_target": formal, "output": output,
            "human_debt": hdebt, "machine_debt": mdebt, "readability_debt": rdebt,
            "evidence_ids": [],
            "source_crosswalk_id": "billingsley-mapping-theorem-pinpoint-pending" if helig == "required" else "not-applicable",
            "provenance_id": "S56-M-1014-ANCHOR-AUDIT" if terminal_id == body_id else ("local-obligation-composition" if short == "T-ASSEMBLE" else "none"),
            "foundation_profile": "Lean4-dependent-type-theory/classical-choice-quotient-policy-pending",
            "tcb_profile": f"Lean-4.29.0+mathlib-{PIN}/transitive-closure-pending",
            "computation_record": "none; no oracle, native computation, or experiment supplies proof credit",
            "step_budget": budget,
            "semantic_step_ledger": {"premises": "Exact frozen context" if not children else ", ".join(oid(child) for child in children), "inference": human, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
            "public_readable_target": f"Stage1_Instances/THM-M-1014/obligation-tree.md#{oid(short).lower()}",
            "validation_spec_id": f"VAL-{oid(short)}",
            "status_boundary": "Architecture, pinned-body mapping, or conditional interface only; no downstream proof acceptance or root closure.",
            "task_ids": [ITEM, "S56-M-1014-PROOF"],
            "owned_sources": ["Stage1_Instances/THM-M-1014/ObligationTree.lean"] if short == "T-ASSEMBLE" else [],
            "owner": "THM-M-1014 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if mdebt in {"M0-L", "M0-W", "M0-P"} else None, "review_due": "before proof-node acceptance", "invalidation_inputs": ["statement", "anchor audit", "registry", "toolchain", "dependency lock"], "revocation_state": "provisional" if mdebt in {"M0-L", "M0-W", "M0-P"} else "open"},
        })

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    payload = json.dumps([{key: row[key] for key in fields} for row in obligations], sort_keys=True, separators=(",", ":")).encode()
    denominator = hashlib.sha256(payload).hexdigest()
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": "The elaborated exact statement and bounded immutable anchor audit determine the weak-topology and pushforward architecture before proof-node acceptance or coverage credit.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "delta_policy": "Any correction, split, merge, exclusion, eligibility, risk, or weight change requires a new registry version and append-only old/new ID delta.",
        "unique_terminal_proof_bodies": [body_id], "obligations": obligations,
    }

    proof_edges = []
    number = 1
    for parent, children in PROOF_CHILDREN.items():
        for child in children:
            request_id = f"M1014-PROOF-{number:03d}R"
            compose_id = f"M1014-PROOF-{number:03d}C"
            request = make_edge("proof", number, parent, child, "proof_requires", compose_id)
            request["edge_id"] = request_id
            compose = make_edge("proof", number, child, parent, "composes", request_id)
            compose["edge_id"] = compose_id
            proof_edges.extend([request, compose])
            number += 1
    refinement_edges = []
    for parent, children in REFINEMENTS.items():
        for child in children:
            refinement_edges.append(make_edge("refine", len(refinement_edges) + 1, parent, child, "logical_decomposition"))
    provenance_edges = [make_edge("prov", 1, "X-PROVENANCE", "X-PINNED", "provenance_of"), make_edge("prov", 2, "X-SOURCE", "ROOT", "source_map")]
    evidence_edges = [make_edge("evidence", 1, "X-PROVENANCE", "X-PINNED", "evidence_for")]
    trust_edges = [make_edge("trust", 1, "ROOT", "S-FOUNDATION", "trusts"), make_edge("trust", 2, "X-PINNED", "S-FOUNDATION", "trusts")]
    documentation_edges = [make_edge("docs", 1, "X-SOURCE", "ROOT", "documents"), make_edge("docs", 2, "X-PROVENANCE", "ROOT", "documents")]
    workflow_edges = [make_edge("workflow", 1, "T-ASSEMBLE", "X-PINNED", "workflow_depends_on"), make_edge("workflow", 2, "ROOT", "T-ASSEMBLE", "workflow_depends_on")]
    graphs = {
        "proof": graph(proof_edges, ids), "refinement": graph(refinement_edges, ids),
        "provenance": graph(provenance_edges, ids), "evidence": graph(evidence_edges, ids),
        "trust": graph(trust_edges, ids), "documentation": graph(documentation_edges, ids),
        "workflow": graph(workflow_edges, ids),
    }
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": "THM-M-1014-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"), "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent.",
        "nodes": nodes, "graphs": graphs,
        "closure_boundary": {"closed_obligations": [oid("S-EXACT"), oid("S-DOMAIN"), oid("T-ASSEMBLE")], "root_closed": False, "root_machine_debt": "M1", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [oid("X-PINNED")], "composition_certificates_checked": ["Stage1Instances.THM_M_1014.ObligationTree.root_of_continuousMappingTerminal"], "proof_body_acceptance_deferred_to": "S56-M-1014-PROOF"},
    }
    recipes = [{
        "recipe_id": f"VAL-{oid(short)}", "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-1014/check_obligation_tree.py"],
        "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1014 obligation tree"}],
        "covered_obligation_ids": [oid(short)], "covered_declarations": [formal] if formal.startswith("Stage1Instances.") else [],
    } for short, _, _, _, formal, *_ in ROWS]
    specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes, "status_boundary": "These recipes validate the frozen architecture and exact conditional composition, not proof-node acceptance or theorem completion."}
    for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    print(denominator)


if __name__ == "__main__":
    main()
