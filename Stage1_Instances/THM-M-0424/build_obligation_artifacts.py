#!/usr/bin/env python3
"""Build the deterministic THM-M-0424 obligation registry and graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

ITEM = "S56-M-0424-OBLIGATION_TREE"
THEOREM = "THM-M-0424"
PREFIX = "M0424"

ROWS = [
    ("ROOT", "root", "Exact BrauerGroupStatement for every field.", "critical", "required", "required"),
    ("S-TARGET", "definition", "Freeze CSA, stable equivalence, quotient, universes, and every LawData field.", "critical", "not_applicable", "required"),
    ("S-BOUNDARY", "terminal", "Retain split algebras, arbitrary fields, and both universe parameters without extra hypotheses.", "high", "required", "required"),
    ("S-FOUNDATION", "certificate", "Audit quotient, classical choice, kernel, and transitive axiom boundaries.", "critical", "not_applicable", "required"),
    ("C-TENSOR-ALG", "construction", "Construct the K-algebra TensorProduct K A B with the required algebra structure.", "critical", "required", "required"),
    ("C-TENSOR-CSA", "construction", "Package the tensor product of two CSAs as a finite-dimensional central simple K-algebra.", "critical", "required", "required"),
    ("C-TENSOR-CONGR", "bridge", "Prove tensoring respects stable matrix equivalence in both arguments.", "critical", "required", "required"),
    ("C-ONE", "construction", "Package K as a CSA and exhibit the required K-algebra equivalence.", "high", "required", "required"),
    ("C-OPPOSITE", "construction", "Package MulOpposite A as a CSA and exhibit the required K-algebra equivalence.", "critical", "required", "required"),
    ("L-DESCENT", "core_lemma", "Descend tensor product to multiplication on the stable-equivalence quotient.", "critical", "required", "required"),
    ("L-ASSOC", "core_lemma", "Prove quotient multiplication is associative.", "critical", "required", "required"),
    ("L-COMM", "core_lemma", "Prove quotient multiplication is commutative.", "critical", "required", "required"),
    ("L-UNIT", "core_lemma", "Prove the class represented by K is a two-sided unit.", "critical", "required", "required"),
    ("L-INVERSE", "core_lemma", "Prove the opposite-algebra class is the inverse.", "critical", "required", "required"),
    ("T-LAWDATA", "terminal", "Assemble all constructions and laws into BrauerGroupLawData for every field.", "critical", "required", "required"),
    ("T-COMPOSE", "transport", "Consume the universal LawData package and return the exact canonical root.", "high", "not_applicable", "required"),
    ("X-SOURCE", "terminal", "Map every mathematical obligation to accepted pinpoint primary sources.", "critical", "required", "required"),
    ("X-PROVENANCE", "terminal", "Record terminal bodies, imports, licenses, hashes, and trust closure without wrapper duplication.", "critical", "not_applicable", "required"),
]


def oid(short):
    return f"{PREFIX}-{short}"


def digest_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}


def main():
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    audit_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = []
    for short, kind, statement, risk, human, readable in ROWS:
        obligations.append({
            "obligation_id": oid(short),
            "statement_fingerprint": ("lean-expression-sha256:62cfee70820b2f8bc4e924505b8984993322f623109868957b726b3446fc3aa8" if short == "ROOT" else f"planned:v1:sha256:{digest_text(statement)}"),
            "kind": kind,
            "root_relevant": True,
            "machine_eligibility": "required" if short not in ("X-SOURCE", "X-PROVENANCE") else "informational",
            "human_source_eligibility": human,
            "readable_eligibility": readable,
            "risk_class": risk,
            "exclusion_reason": None,
            "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0424/ObligationTree.lean#brauerGroupStatement_of_lawData" if short == "T-COMPOSE" else None),
        })
    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    wire = json.dumps([{key: row[key] for key in fields} for row in obligations], sort_keys=True, separators=(",", ":"))
    denominator = digest_text(wire)
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "registry_id": "THM-M-0424-OBLIGATIONS-v1",
        "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
        "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": "Exact statement and pre-closure architecture implied by every BrauerGroupLawData field; eligibility was fixed without treating anchor availability as closure.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": audit_hash,
        "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
            "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
            "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
            "informational_overlays": [oid("X-SOURCE"), oid("X-PROVENANCE")],
        },
        "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new version with an append-only old/new ID delta.",
        "obligations": obligations,
    }

    nodes = []
    for (short, kind, statement, _risk, human, _readable), obligation in zip(ROWS, obligations):
        known = short in ("S-TARGET", "T-COMPOSE")
        nodes.append({
            "node_id": f"{THEOREM}-{short}", "obligation_id": obligation["obligation_id"], "kind": kind,
            "human_statement": statement,
            "formal_target": ({"ROOT": "Stage1Instances.THM_M_0424.BrauerGroupStatement", "S-TARGET": "Stage1Instances.THM_M_0424.BrauerGroupLawData", "T-COMPOSE": "Stage1Instances.THM_M_0424.brauerGroupStatement_of_lawData"}.get(short, "planned exact Lean signature; proof phase must freeze before implementation")),
            "output": statement, "human_debt": "H1" if human == "required" else "H2",
            "machine_debt": "M0-L" if known else ("M3" if short == "ROOT" else "M4"), "readability_debt": "R3",
            "evidence_ids": [], "source_crosswalk_id": "source_statement_crosswalk.md#primary-proof-node-map-pending" if human == "required" else "not-applicable",
            "provenance_id": "anchor-audit:M0424-C01" if short == "S-TARGET" else "none",
            "foundation_profile": "lean4-mathlib-classical/quotient-policy-audit-pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; no computation or oracle is credited",
            "step_budget": 60 if short in ("C-TENSOR-CSA", "L-INVERSE", "L-COMM") else 30,
            "semantic_step_ledger": {"premises": "Only incoming proof_requires conclusions and the stated field/CSA context.", "inference": statement, "output": statement, "outgoing_use": "Only the declared typed proof parent may consume this conclusion."},
            "public_readable_target": f"Stage1_Instances/THM-M-0424/obligation-tree.md#{oid(short).lower()}",
            "validation_spec_id": f"VAL-{oid(short)}", "status_boundary": "Architecture/interface only; this node is not proof-closed unless its machine debt explicitly says M0-L.",
            "task_ids": [ITEM, "S56-M-0424-PROOF"], "owned_sources": (["Stage1_Instances/THM-M-0424/ObligationTree.lean"] if known else []),
            "owner": "THM-M-0424 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if known else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if known else "open"},
        })

    required = {
        "ROOT": ["T-COMPOSE"], "T-COMPOSE": ["T-LAWDATA"],
        "T-LAWDATA": ["C-TENSOR-CSA", "C-TENSOR-CONGR", "C-ONE", "C-OPPOSITE", "L-DESCENT", "L-ASSOC", "L-COMM", "L-UNIT", "L-INVERSE"],
        "C-TENSOR-CSA": ["C-TENSOR-ALG"],
    }
    proof_edges = []
    for parent, children in required.items():
        for child in children:
            base = f"PROOF-{parent}-{child}"
            proof_edges += [
                {"edge_id": base + "-REQ", "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": base + "-COMP"},
                {"edge_id": base + "-COMP", "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": base + "-REQ"},
            ]
    refine_edges = [{"edge_id": f"REFINE-{short}", "from": oid("ROOT"), "type": "logical_decomposition", "to": oid(short)} for short in ("S-TARGET", "S-BOUNDARY")]
    provenance_edges = [{"edge_id": "PROV-DEFS", "from": oid("X-PROVENANCE"), "type": "provenance_of", "to": oid("S-TARGET")}]
    evidence_edges = [{"edge_id": "EVID-COMPOSE", "from": oid("X-PROVENANCE"), "type": "evidence_for", "to": oid("T-COMPOSE")}]
    trust_edges = [{"edge_id": "TRUST-FOUNDATION", "from": oid("ROOT"), "type": "trusts", "to": oid("S-FOUNDATION")}, {"edge_id": "TRUST-PROVENANCE", "from": oid("ROOT"), "type": "trusts", "to": oid("X-PROVENANCE")}]
    document_edges = [{"edge_id": "DOC-TARGET", "from": oid("S-TARGET"), "type": "documents", "to": oid("ROOT")}, {"edge_id": "DOC-SOURCE", "from": oid("X-SOURCE"), "type": "source_map", "to": oid("ROOT")}]
    workflow_edges = [{"edge_id": "FLOW-PROOF", "from": oid("T-LAWDATA"), "type": "workflow_depends_on", "to": oid("C-TENSOR-CSA")}, {"edge_id": "FLOW-VALIDATE", "from": oid("X-PROVENANCE"), "type": "workflow_depends_on", "to": oid("T-COMPOSE")}, {"edge_id": "FLOW-SOURCE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("X-SOURCE")}]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": registry["registry_id"], "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"), "edge_direction": "proof_requires runs parent to child; composes is reciprocal child to parent.",
        "nodes": nodes,
        "graphs": {"proof": graph(proof_edges), "refinement": graph(refine_edges), "provenance": graph(provenance_edges), "evidence": graph(evidence_edges), "trust": graph(trust_edges), "documentation": graph(document_edges), "workflow": graph(workflow_edges)},
        "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False,
            "remaining_root_cut_set": [oid(x) for x in ("C-TENSOR-CSA", "C-TENSOR-CONGR", "C-ONE", "C-OPPOSITE", "L-DESCENT", "L-ASSOC", "L-COMM", "L-UNIT", "L-INVERSE")],
            "remaining_release_cut_set": [oid("S-FOUNDATION"), oid("X-SOURCE"), oid("X-PROVENANCE"), "R0 reconstruction", "hermetic and independent validation"],
            "composition_certificates": ["Stage1Instances.THM_M_0424.brauerGroupStatement_of_lawData"],
            "distinct_terminal_proof_bodies": [],
            "note": "The checked conditional adapter is not a terminal proof body and supplies no root credit."},
    }
    specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
    for row in obligations:
        specs["recipes"].append({"recipe_id": f"VAL-{row['obligation_id']}", "obligation_id": row["obligation_id"], "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0424/check_obligation_tree.py"], "env": {}, "timeout_seconds": 30, "network": "denied", "covered_ids": [row["obligation_id"]], "expected_exit": 0})
    dump("obligation-registry.json", registry)
    dump("typed-graphs.json", bundle)
    dump("validation-specs.json", specs)
    print(f"built {len(obligations)} obligations; denominator {denominator}")


if __name__ == "__main__":
    main()
