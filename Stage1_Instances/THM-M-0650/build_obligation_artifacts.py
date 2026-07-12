#!/usr/bin/env python3
"""Build the frozen THM-M-0650 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0650-OBLIGATION_TREE"
THEOREM = "THM-M-0650"


def canonical_hash(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M0650-ROOT", "root", "critical",
     "The exact witness-condition-implies-elementarity target frozen in Statement.lean.",
     "Stage1Instances.THM_M_0650.TarskiVaughtTarget",
     "S.IsElementary for every substructure satisfying the frozen witness condition."),
    ("M0650-S-DEFINITIONS", "definition", "high",
     "Freeze bounded formulas, realization, the last-variable witness convention, and substructure elementarity.",
     "Stage1Instances.THM_M_0650.{TarskiVaughtWitnessCondition,TarskiVaughtTarget}",
     "The exact canonical interface and witness-variable convention."),
    ("M0650-S-DOMAINS", "normalization", "high",
     "Fix universes, language signatures, structure instances, substructure coercions, and tuple domains.",
     "universes u v w; L : FirstOrder.Language.{v,w}; M : Type u; S : L.Substructure M",
     "A type-correct substructure inclusion and parameter tuple in the ambient model."),
    ("M0650-S-BOUNDARY", "terminal", "high",
     "Retain the nullary parameter case n = 0 and all language-symbol degeneracies admitted by the canonical statement.",
     "Stage1Instances.THM_M_0650.nullaryParameterBoundary",
     "The witness premise applies without a positive-arity side condition."),
    ("M0650-S-TRANSPORT", "transport", "high",
     "Relate the named canonical target definition to the direct pinned mathlib binder shape.",
     "Stage1Instances.THM_M_0650.tarskiVaughtTarget_iff_pinnedMathlibStatementShape",
     "A checked definitional equivalence with no change of theorem direction."),
    ("M0650-S-FOUNDATION", "certificate", "critical",
     "Fix the accepted propext, classical-choice, quotient, kernel, and no-placeholder boundary for the terminal body.",
     "planned transitive axiom, declaration-dependency, and TCB report",
     "An accepted foundation and trust boundary for every credited declaration."),
    ("M0650-N-SUBTYPE", "normalization", "high",
     "Normalize the substructure inclusion to its bundled language embedding S.subtype.",
     "FirstOrder.Language.Substructure.subtype",
     "An embedding S -> M whose function is the substructure coercion."),
    ("M0650-N-WITNESS", "transport", "critical",
     "Show that the substructure witness premise is exactly the embedding witness premise for S.subtype.",
     "checked by Stage1Instances.THM_M_0650.root_of_embeddingTarskiVaughtPackage",
     "The premise needed by the embedding-level Tarski-Vaught theorem."),
    ("M0650-B-FORMULA", "branch", "critical",
     "Perform structural recursion over bounded formulas, separating falsum, equality, relation, implication, and universal quantification.",
     "FirstOrder.Language.Embedding.isElementary_of_exists structural recursion",
     "Realization preservation for every bounded formula constructor."),
    ("M0650-B-ATOMIC", "branch", "high",
     "Close falsum, equality, and relation cases using term realization and embedding preservation.",
     "terminal cases of FirstOrder.Language.Embedding.isElementary_of_exists",
     "Realization equivalence for atomic bounded formulas."),
    ("M0650-B-IMPLIES", "branch", "high",
     "Compose induction hypotheses through the implication constructor.",
     "implication case of FirstOrder.Language.Embedding.isElementary_of_exists",
     "Realization equivalence for implications."),
    ("M0650-B-FORALL", "branch", "critical",
     "Prove the universal case in both directions, using the witness criterion on the negated body for the nontrivial direction.",
     "universal case of FirstOrder.Language.Embedding.isElementary_of_exists",
     "Realization equivalence under one more bound variable."),
    ("M0650-L-WITNESS-NOT", "core_lemma", "critical",
     "From failure of the ambient universal, apply the frozen witness condition to the negated body and obtain a counterexample in the source.",
     "htv n phi.not xs a inside FirstOrder.Language.Embedding.isElementary_of_exists",
     "A source element witnessing failure of the source universal."),
    ("M0650-L-REINDEX", "core_lemma", "high",
     "Reconcile default assignments, Fin.snoc composition, and formula relabeling at the induction and final-formula boundaries.",
     "Finite-variable relabeling and Fin.comp_snoc steps in the pinned terminal body",
     "The exact tuple shapes required by Formula.Realize."),
    ("M0650-T-EMBEDDING", "terminal", "critical",
     "Assemble structural recursion into the exact embedding-level Tarski-Vaught theorem.",
     "FirstOrder.Language.Embedding.isElementary_of_exists",
     "Stage1Instances.THM_M_0650.EmbeddingTarskiVaughtPackage."),
    ("M0650-T-SUBSTRUCTURE", "transport", "high",
     "Specialize the embedding theorem to S.subtype and package formula preservation as S.IsElementary.",
     "Stage1Instances.THM_M_0650.root_of_embeddingTarskiVaughtPackage",
     "The exact canonical TarskiVaughtTarget."),
    ("M0650-X-MATHLIB", "bridge", "critical",
     "Pin the imported substructure wrapper and terminal embedding proof body to mathlib revision 8a178386.",
     "FirstOrder.Language.Substructure.isElementary_of_exists -> FirstOrder.Language.Embedding.isElementary_of_exists",
     "A unique immutable terminal proof-body identity and wrapper relationship."),
    ("M0650-X-SOURCE", "terminal", "high",
     "Map the canonical implication and every material proof node to a reviewed primary-source passage and convention.",
     "non-machine node-specific primary-source crosswalk",
     "Human-source coverage without machine proof credit."),
    ("M0650-X-PROVENANCE", "certificate", "critical",
     "Inventory wrapper/body declarations, imports, axioms, TCB, placeholders, licenses, and replay evidence.",
     "planned machine-derived provenance closure",
     "Release provenance without independent mathematical proof credit."),
]

local_checked = {
    "M0650-S-DEFINITIONS", "M0650-S-DOMAINS", "M0650-S-BOUNDARY",
    "M0650-S-TRANSPORT", "M0650-N-SUBTYPE", "M0650-N-WITNESS",
    "M0650-T-SUBSTRUCTURE",
}
source_na = {
    "M0650-S-DEFINITIONS", "M0650-S-DOMAINS", "M0650-S-BOUNDARY",
    "M0650-S-TRANSPORT", "M0650-S-FOUNDATION", "M0650-N-SUBTYPE",
    "M0650-N-WITNESS", "M0650-T-SUBSTRUCTURE", "M0650-X-PROVENANCE",
}
machine_special = {
    "M0650-X-SOURCE": "not_applicable",
    "M0650-X-PROVENANCE": "informational",
}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    if oid in {"M0650-ROOT", "M0650-S-DEFINITIONS", "M0650-S-DOMAINS", "M0650-S-BOUNDARY", "M0650-S-TRANSPORT"}:
        fingerprint = "lean-source:v1:sha256:" + statement_hash
    else:
        fingerprint = "planned:v1:sha256:" + canonical_hash([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {
        "not_applicable": "human_source_boundary_only",
        "informational": "release_provenance_overlay_no_proof_credit",
    }.get(machine)
    body = None
    if oid == "M0650-T-EMBEDDING":
        body = "mathlib:8a178386:FirstOrder.Language.Embedding.isElementary_of_exists"
    elif oid == "M0650-T-SUBSTRUCTURE":
        body = "local:Stage1_Instances/THM-M-0650/ObligationTree.lean#root_of_embeddingTarskiVaughtPackage"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0650-" + oid.removeprefix("M0650-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": claim,
        "formal_target": target,
        "output": output,
        "human_debt": "H1",
        "machine_debt": "M0-L" if oid in local_checked else ("M3" if oid == "M0650-ROOT" else "M4"),
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "pinned-anchor-audit-candidate" if oid in {"M0650-T-EMBEDDING", "M0650-X-MATHLIB"} else ("local-conditional-composition" if body else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; this is a logical proof with no oracle or experimental computation",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {
            "premises": "Only exact proof_requires child conclusions and the formal context named by this node.",
            "inference": claim,
            "output": output,
            "source_anchors": "Pinned mathlib body where named; reviewed primary-source mapping remains open.",
            "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0650/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; proof-phase integration, full provenance, H0/R0, and release remain open.",
        "task_ids": [ITEM, "S56-M-0650-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0650/ObligationTree.lean"] if oid in local_checked else [],
        "owner": "THM-M-0650 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if oid in local_checked else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"],
            "revocation_state": "provisional" if oid in local_checked else "open",
        },
    })

fields = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)
denominator = canonical_hash([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and immutable anchor audit; the short substructure wrapper and central embedding structural induction were expanded before proof-phase closure was credited.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0650-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0650-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {
        "closed_obligations": sorted(local_checked),
        "anchor_candidates_not_credited_as_closed": ["M0650-T-EMBEDDING", "M0650-X-MATHLIB"],
        "root_machine_debt": "M3",
    },
    "status_boundary": "Scope and denominators only. The anchor remains candidate evidence until the proof phase; no H0, root closure, audit completion, or theorem completion is claimed.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0650-ROOT": ["M0650-T-SUBSTRUCTURE"],
    "M0650-T-SUBSTRUCTURE": ["M0650-N-SUBTYPE", "M0650-N-WITNESS", "M0650-T-EMBEDDING"],
    "M0650-T-EMBEDDING": ["M0650-B-FORMULA", "M0650-L-REINDEX"],
    "M0650-B-FORMULA": ["M0650-B-ATOMIC", "M0650-B-IMPLIES", "M0650-B-FORALL"],
    "M0650-B-FORALL": ["M0650-L-WITNESS-NOT", "M0650-L-REINDEX"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof += [
            edge(req, parent, "proof_requires", child, comp),
            edge(comp, child, "composes", parent, req),
        ]

graph_edges = {
    "proof": proof,
    "refinement": [
        edge("REF-ROOT-DEFS", "M0650-ROOT", "logical_decomposition", "M0650-S-DEFINITIONS"),
        edge("REF-ROOT-DOMAINS", "M0650-ROOT", "logical_decomposition", "M0650-S-DOMAINS"),
        edge("REF-ROOT-BOUNDARY", "M0650-ROOT", "logical_decomposition", "M0650-S-BOUNDARY"),
        edge("REF-ROOT-TRANSPORT", "M0650-ROOT", "logical_decomposition", "M0650-S-TRANSPORT"),
        edge("REF-ROOT-FOUNDATION", "M0650-ROOT", "logical_decomposition", "M0650-S-FOUNDATION"),
    ],
    "provenance": [
        edge("PROV-BODY-BRIDGE", "M0650-T-EMBEDDING", "provenance_of", "M0650-X-MATHLIB"),
        edge("PROV-BRIDGE-ROOT", "M0650-X-MATHLIB", "provenance_of", "M0650-ROOT"),
        edge("SRC-EMBEDDING", "M0650-T-EMBEDDING", "source_map", "M0650-X-SOURCE"),
    ],
    "evidence": [],
    "trust": [
        edge("TRUST-FOUNDATION", "M0650-ROOT", "trusts", "M0650-S-FOUNDATION"),
        edge("TRUST-PROVENANCE", "M0650-ROOT", "trusts", "M0650-X-PROVENANCE"),
    ],
    "documentation": [
        edge("DOC-DEFINITIONS", "M0650-S-DEFINITIONS", "documents", "M0650-ROOT"),
        edge("DOC-SOURCE", "M0650-X-SOURCE", "documents", "M0650-T-EMBEDDING"),
        edge("DOC-BRANCH", "M0650-B-FORMULA", "documents", "M0650-T-EMBEDDING"),
    ],
    "workflow": [
        edge("FLOW-PROOF-TREE", "M0650-T-SUBSTRUCTURE", "workflow_depends_on", "M0650-T-EMBEDDING"),
        edge("FLOW-PROVENANCE-BODY", "M0650-X-PROVENANCE", "workflow_depends_on", "M0650-T-EMBEDDING"),
        edge("FLOW-SOURCE-BODY", "M0650-X-SOURCE", "workflow_depends_on", "M0650-T-EMBEDDING"),
    ],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": "THM-M-0650-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": "M0650-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": sorted(local_checked),
        "root_closed": False,
        "root_machine_debt": "M3",
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M0650-T-EMBEDDING"],
        "composition_certificates": ["Stage1Instances.THM_M_0650.root_of_embeddingTarskiVaughtPackage"],
        "reason": "The final local composition is conditional. The pinned embedding theorem is inventoried as an M0-W candidate, but proof-phase integration and provenance/trust acceptance remain downstream.",
    },
}

recipes = {
    "schema_version": "stage1-validation-specs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "recipes": [],
}
for oid, *_ in rows:
    recipes["recipes"].append({
        "recipe_id": "VAL-" + oid,
        "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-0650/check_obligation_tree.py"],
        "env_allowlist": {},
        "timeout_seconds": 30,
        "network_policy": "denied",
        "expected_exit": 0,
        "expected_outputs": [{
            "path_or_stream": "stdout",
            "semantic_hash_policy": "contains PASS THM-M-0650 obligation tree",
        }],
        "covered_obligation_ids": [oid],
        "covered_declarations": [],
    })

for name, value in (
    ("obligation-registry.json", registry),
    ("typed-graphs.json", bundle),
    ("validation-specs.json", recipes),
):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
