#!/usr/bin/env python3
"""Build the frozen THM-M-0112 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0112-OBLIGATION_TREE"
THEOREM = "THM-M-0112"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


# Eligibility is architectural, not inferred from the currently open machine state.
ROWS = [
    ("M0112-ROOT", "root", "critical", "The exact frozen weak topological Lefschetz target.", "Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget", "The canonical proposition."),
    ("M0112-S-INTERFACE", "definition", "critical", "Relate every opaque field of LefschetzHyperplaneData to a native complex-algebraic/analytic realization without assuming the conclusion.", "planned native-realization bridge into LefschetzHyperplaneData", "A faithful instance of the frozen interface."),
    ("M0112-S-BOUNDARY", "branch", "high", "Account explicitly for dimensions zero and one and for Pi 0 conventions under truncated natural subtraction.", "planned low-dimensional branch theorem for complexDimension <= 1", "The exact low-dimensional cases or a source-supported restriction/transport."),
    ("M0112-S-FOUNDATION", "certificate", "critical", "Fix the classical-choice, quotient, extensionality, axiom, TCB, and no-oracle policy for all terminal bodies.", "planned transitive axiom and trust report", "An accepted foundation and TCB profile."),
    ("M0112-N-RELATIVE", "transport", "critical", "State and check the equivalence direction from relative homotopy vanishing through degree n-1 to the map formulation, including basepoints.", "planned relative-homotopy long-exact-sequence transport", "Bijectivity below n-1 and surjectivity at n-1."),
    ("M0112-C-MORSE-DATA", "construction", "critical", "Construct the affine complement, exhaustion/Lefschetz-pencil data, critical strata, and compatibility with the hyperplane inclusion.", "planned complex Morse/Lefschetz-pencil construction", "Geometric data suitable for the index estimate."),
    ("M0112-L-INDEX", "core_lemma", "critical", "Prove the complex Morse index bound forcing all relative handles/cells to have real index at least the complex dimension n.", "planned affine complex Morse index theorem", "No relative cell below dimension n."),
    ("M0112-L-CELLULAR", "core_lemma", "critical", "Convert the handle-index bound into vanishing of relative homotopy groups pi_k(X,Y) for every k < n.", "planned relative CW/handle connectivity theorem", "Relative (n-1)-connectivity of (X,Y)."),
    ("M0112-B-BELOW", "branch", "critical", "For each k < n-1, use adjacent relative vanishing terms in the long exact sequence to prove bijectivity of pi_k(Y) to pi_k(X).", "Stage1Instances.THMM0112.BelowBoundaryPackage", "The complete below-boundary package."),
    ("M0112-B-EDGE", "branch", "critical", "At k = n-1, use the relative vanishing term to prove surjectivity, without strengthening it to injectivity.", "Stage1Instances.THMM0112.BoundaryPackage", "The exact boundary package."),
    ("M0112-T-ASSEMBLE", "terminal", "high", "Conjoin the lower-degree and boundary packages under the identical geometric hypotheses.", "Stage1Instances.THMM0112.weakTopologicalLefschetz_of_packages", "The exact canonical root, conditional on both packages."),
    ("M0112-X-SOURCE", "terminal", "high", "Map the relative-connectivity, Morse-index, low-dimensional, and long-exact-sequence nodes to pinpoint reviewed primary-source passages.", "non-machine node-specific source crosswalk", "Human-source coverage only."),
    ("M0112-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, declaration closure, axioms, TCB, replay evidence, and unique proof-body identities.", "planned machine-derived provenance closure", "Release provenance without proof credit."),
]

statement = json.loads((HERE / "statement.json").read_text())
statement_fp = statement["canonical_formal_target"]["elaborated_expression_sha256"]
statement_file_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
checked = {"M0112-T-ASSEMBLE"}
source_na = {"M0112-S-INTERFACE", "M0112-S-BOUNDARY", "M0112-S-FOUNDATION", "M0112-X-PROVENANCE"}
machine_special = {"M0112-X-SOURCE": "not_applicable", "M0112-X-PROVENANCE": "informational"}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in ROWS:
    fp = ("lean-expression-sha256:" + statement_fp if oid == "M0112-ROOT"
          else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only",
                              "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0112/ObligationTree.lean#weakTopologicalLefschetz_of_packages" if oid == "M0112-T-ASSEMBLE" else None),
    })
    nodes.append({
        "node_id": "THM-M-0112-" + oid.removeprefix("M0112-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0112-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid in checked else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if oid in {"M0112-C-MORSE-DATA", "M0112-L-INDEX", "M0112-L-CELLULAR"} else 40,
        "semantic_step_ledger": {
            "premises": "Only the exact typed proof children and the frozen formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed parent or a non-proof support edge may consume this output."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0112/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; no unlisted premise or root proof is supplied.",
        "task_ids": [ITEM, "S56-M-0112-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0112/ObligationTree.lean"] if oid == "M0112-T-ASSEMBLE" else [],
        "owner": "THM-M-0112 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None,
                     "review_due": "before proof acceptance",
                     "invalidation_inputs": ["statement", "registry", "source map", "toolchain"],
                     "revocation_state": "provisional" if oid in checked else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Frozen exact statement plus bounded anchor audit; classical relative-homotopy/Morse architecture; eligibility assigned before closure observation.",
    "frozen_against_statement_sha256": statement_file_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0112-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0112-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and conditional recomposition only; the geometric packages and root remain open."
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0112-ROOT": ["M0112-T-ASSEMBLE"],
    "M0112-T-ASSEMBLE": ["M0112-B-BELOW", "M0112-B-EDGE"],
    "M0112-B-BELOW": ["M0112-N-RELATIVE", "M0112-L-CELLULAR"],
    "M0112-B-EDGE": ["M0112-N-RELATIVE", "M0112-L-CELLULAR"],
    "M0112-L-CELLULAR": ["M0112-C-MORSE-DATA", "M0112-L-INDEX"],
    "M0112-C-MORSE-DATA": ["M0112-S-INTERFACE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp),
                      edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-BOUNDARY", "M0112-ROOT", "logical_decomposition", "M0112-S-BOUNDARY")],
    "provenance": [edge("SRC-RELATIVE", "M0112-N-RELATIVE", "source_map", "M0112-X-SOURCE"),
                   edge("SRC-INDEX", "M0112-L-INDEX", "source_map", "M0112-X-SOURCE"),
                   edge("PROV-ROOT", "M0112-X-PROVENANCE", "provenance_of", "M0112-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M0112-ROOT", "trusts", "M0112-S-FOUNDATION"),
              edge("TRUST-PROVENANCE", "M0112-ROOT", "trusts", "M0112-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE-ROOT", "M0112-X-SOURCE", "documents", "M0112-ROOT"),
                      edge("DOC-BOUNDARY", "M0112-S-BOUNDARY", "documents", "M0112-B-EDGE")],
    "workflow": [edge("FLOW-PROOF-TREE", "M0112-T-ASSEMBLE", "workflow_depends_on", "M0112-B-BELOW"),
                 edge("FLOW-PROOF-EDGE", "M0112-T-ASSEMBLE", "workflow_depends_on", "M0112-B-EDGE"),
                 edge("FLOW-PROV-ASSEMBLE", "M0112-X-PROVENANCE", "workflow_depends_on", "M0112-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0112-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0112-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False,
                         "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": ["M0112-B-BELOW", "M0112-B-EDGE"],
                         "composition_certificates": ["Stage1Instances.THMM0112.weakTopologicalLefschetz_of_packages"],
                         "reason": "The exact final recomposition is checked, but both mathematical package premises remain open."}
}

recipes = []
for oid, *_ in ROWS:
    recipes.append({
        "recipe_id": "VAL-" + oid, "obligation_id": oid,
        "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0112/check_obligation_tree.py"],
        "env_allowlist": {"PATH": "runner-provided-pinned-toolchain"}, "timeout_seconds": 120,
        "network_policy": "denied", "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS and denominator digest"}],
        "covered_obligation_ids": [oid],
        "covered_declarations": (["Stage1Instances.THMM0112.weakTopologicalLefschetz_of_packages"] if oid == "M0112-T-ASSEMBLE" else [])
    })
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM,
         "theorem_id": THEOREM, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle),
                    ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
