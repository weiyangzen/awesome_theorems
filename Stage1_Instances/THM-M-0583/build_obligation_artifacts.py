#!/usr/bin/env python3
"""Reproducibly build the frozen THM-M-0583 obligation and graph artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATEMENT = HERE / "Statement.lean"
REGISTRY_ID = "THM-M-0583-OBLIGATIONS-v1"

# id, kind, risk, H eligibility, formal target, output, budget, semantic ledger
SPECS = [
    ("M0583-ROOT", "root", "critical", "required",
     "Stage1Instances.THM_M_0583.FourDimensionalTopologicalPoincareTarget",
     "The exact frozen canonical proposition.", 8,
     ["Obtain the terminal topological result.", "Apply the checked exact adapter.", "Return the canonical homeomorphism existence claim."]),
    ("M0583-S-ENCODING", "definition", "high", "not_applicable",
     "Stage1Instances.THM_M_0583.{FourModel,FourSphere,FourDimensionalTopologicalPoincareTarget}",
     "An audited match between closed topological four-manifolds and the Lean object model.", 35,
     ["Check the Euclidean chart model fixes dimension four.", "Check CompactSpace and T2Space express closedness.", "Check the metric sphere model and unpointed homotopy equivalence.", "Exclude smooth and boundary-bearing variants."]),
    ("M0583-H-SOURCE-CROSSWALK", "source_boundary", "critical", "required",
     "planned primary-source theorem and definition crosswalk",
     "Pinpoint source assumptions and conclusions for every mathematical child.", 70,
     ["Acquire a stable primary text.", "Locate the exact theorem, page, and surrounding definitions.", "Map closedness, category, dimension, and homotopy assumptions.", "Audit errata and later corrections.", "Obtain independent source review."]),
    ("M0583-R-HOMOTOPY-DATA", "reduction", "high", "required",
     "planned Lean homotopy-sphere invariant package",
     "Simply-connected homology four-sphere data derived from the supplied homotopy equivalence.", 75,
     ["Transport connectedness from the four-sphere.", "Transport fundamental-group triviality.", "Transport integral homology and orientation data.", "Package the invariants required by the topological classification argument."]),
    ("M0583-C-TOPOLOGICAL-MODEL", "construction", "critical", "required",
     "planned Lean handle/Poincare-complex model",
     "A finite topological model on which the four-dimensional surgery argument applies.", 95,
     ["Choose the source-compatible topological model.", "Relate manifold data to its Poincare complex.", "Track local flatness and boundary conventions.", "Preserve the homotopy-sphere invariants.", "Expose the exact surgery inputs."]),
    ("M0583-L-DISK-EMBEDDING", "theorem_bridge", "critical", "required",
     "planned Lean Freedman disk-embedding theorem",
     "Embedded topological disks replacing the required immersed disks under the valid good-group hypotheses.", 100,
     ["State capped-grope and Whitney-disk input data.", "Verify the trivial fundamental group is in the admissible class.", "Construct controlled immersed disks.", "Apply Casson-handle limiting topology.", "Prove local flatness and disjointness.", "Return embedded disks with the prescribed boundary and framing."]),
    ("M0583-L-SURGERY", "theorem_bridge", "critical", "required",
     "planned Lean simply-connected four-dimensional topological surgery theorem",
     "A surgery solution and normal cobordism for the homotopy four-sphere.", 100,
     ["Construct the degree-one normal map.", "Identify the dimension-four surgery obstruction.", "Show the obstruction vanishes for the sphere data.", "Use disk embedding to perform middle-dimensional surgery.", "Track the normal invariant and boundary.", "Produce the required topological cobordism."]),
    ("M0583-L-S-COBORDISM", "theorem_bridge", "critical", "required",
     "planned Lean four-dimensional topological s-cobordism theorem for the trivial group",
     "A product structure on the resulting topological h-cobordism.", 100,
     ["Verify both inclusions are homotopy equivalences.", "Compute the trivial Whitehead torsion.", "Check the fundamental group is good and trivial.", "Apply four-dimensional topological s-cobordism.", "Obtain a boundary-compatible product homeomorphism."]),
    ("M0583-C-HOMEOMORPHISM", "composition", "critical", "required",
     "planned Lean classification-to-homeomorphism composition",
     "A homeomorphism from the arbitrary manifold to the standard four-sphere.", 60,
     ["Compose the surgery cobordism with its product structure.", "Restrict the product homeomorphism to the boundary ends.", "Identify the standard end with the encoded four-sphere.", "Package the map and inverse as a Homeomorph."]),
    ("M0583-X-FREEDMAN-CORE", "terminal", "critical", "required",
     "Stage1Instances.THM_M_0583.ObligationTree.FreedmanTopologicalCore",
     "The placeholder-free terminal theorem body for the complete topological classification argument.", 90,
     ["Introduce the arbitrary encoded closed four-manifold.", "Apply the homotopy-data reduction.", "Build the topological surgery model.", "Invoke disk embedding and topological surgery.", "Apply topological s-cobordism.", "Construct and return the homeomorphism."]),
    ("M0583-T-EXACT-ADAPTER", "transport", "high", "not_applicable",
     "Stage1Instances.THM_M_0583.ObligationTree.canonicalRoot_of_freedmanTopologicalCore",
     "A kernel-checked identity-preserving transport to the canonical root.", 12,
     ["Unfold the core proposition.", "Unfold the repeated canonical root.", "Check definitional identity.", "Apply the core proof without changing binders."]),
    ("M0583-C-ROOT-COMPOSITION", "composition", "high", "not_applicable",
     "planned import-level composition certificate",
     "A checked certificate consuming the exact terminal core and adapter.", 20,
     ["Resolve the terminal declaration.", "Resolve the exact adapter.", "Check both expression fingerprints.", "Produce the canonical declaration."]),
    ("M0583-X-PROVENANCE", "provenance", "critical", "not_applicable",
     "planned terminal-object provenance report",
     "Content-addressed wrapper, body, project, revision, and source identities.", 55,
     ["Resolve the root wrapper and terminal constant.", "Separate aliases from unique proof bodies.", "Hash every owned and imported source.", "Record project and immutable revision origins.", "Reject placeholder, unsafe, oracle, and unpinned boundaries."]),
    ("M0583-S-FOUNDATION", "trust", "critical", "not_applicable",
     "planned transitive axiom/dependency/TCB report",
     "An accepted trust closure for the actual terminal proof object.", 55,
     ["Extract transitive declaration dependencies.", "Extract axioms from the terminal object.", "Classify native code and external computation.", "Compare all results to the pinned foundation and TCB profiles.", "Record an independently checked trust receipt."]),
    ("M0583-D-READABLE", "documentation", "high", "required",
     "planned source-linked readable reconstruction",
     "A complete readable proof aligned with graph nodes and machine declarations.", 80,
     ["Explain every mathematical reduction and construction.", "Cross-link each section to a stable obligation ID.", "Distinguish source theorem use from local derivation.", "Expose every machine-open node as a blocker.", "Obtain independent mathematical review."]),
    ("M0583-E-VALIDATION", "evidence", "critical", "not_applicable",
     "planned exact validation and independent replay receipts",
     "Fresh kernel, graph, provenance, hermetic, and independent evidence for the immutable root.", 70,
     ["Run exact-type elaboration and kernel checks.", "Run graph composition and denominator checks.", "Run placeholder, axiom, provenance, and dependency checks.", "Replay from a cold cache with the network denied.", "Require two independent verifiers and deterministic bundle agreement."]),
]

PROOF_EDGES = [
    ("M0583-ROOT", "M0583-C-ROOT-COMPOSITION", "requires_composition"),
    ("M0583-C-ROOT-COMPOSITION", "M0583-T-EXACT-ADAPTER", "uses_transport"),
    ("M0583-C-ROOT-COMPOSITION", "M0583-X-FREEDMAN-CORE", "uses_terminal"),
    ("M0583-X-FREEDMAN-CORE", "M0583-S-ENCODING", "uses_encoding"),
    ("M0583-X-FREEDMAN-CORE", "M0583-R-HOMOTOPY-DATA", "requires_reduction"),
    ("M0583-X-FREEDMAN-CORE", "M0583-C-TOPOLOGICAL-MODEL", "requires_model"),
    ("M0583-X-FREEDMAN-CORE", "M0583-L-DISK-EMBEDDING", "requires_bridge"),
    ("M0583-X-FREEDMAN-CORE", "M0583-L-SURGERY", "requires_bridge"),
    ("M0583-X-FREEDMAN-CORE", "M0583-L-S-COBORDISM", "requires_bridge"),
    ("M0583-X-FREEDMAN-CORE", "M0583-C-HOMEOMORPHISM", "requires_construction"),
    ("M0583-C-TOPOLOGICAL-MODEL", "M0583-R-HOMOTOPY-DATA", "consumes"),
    ("M0583-L-SURGERY", "M0583-C-TOPOLOGICAL-MODEL", "consumes"),
    ("M0583-L-SURGERY", "M0583-L-DISK-EMBEDDING", "consumes"),
    ("M0583-L-S-COBORDISM", "M0583-L-SURGERY", "consumes"),
    ("M0583-C-HOMEOMORPHISM", "M0583-L-S-COBORDISM", "consumes"),
]

GRAPH_EDGES = {
    "proof": PROOF_EDGES,
    "refinement": [("M0583-ROOT", "M0583-X-FREEDMAN-CORE", "refined_by"), ("M0583-X-FREEDMAN-CORE", "M0583-R-HOMOTOPY-DATA", "refined_by"), ("M0583-X-FREEDMAN-CORE", "M0583-C-TOPOLOGICAL-MODEL", "refined_by"), ("M0583-X-FREEDMAN-CORE", "M0583-C-HOMEOMORPHISM", "refined_by")],
    "provenance": [("M0583-ROOT", "M0583-X-PROVENANCE", "attested_by"), ("M0583-X-FREEDMAN-CORE", "M0583-X-PROVENANCE", "resolved_by")],
    "evidence": [("M0583-ROOT", "M0583-E-VALIDATION", "validated_by"), ("M0583-C-ROOT-COMPOSITION", "M0583-E-VALIDATION", "validated_by")],
    "trust": [("M0583-ROOT", "M0583-S-FOUNDATION", "trusted_by"), ("M0583-X-FREEDMAN-CORE", "M0583-S-FOUNDATION", "audited_by")],
    "documentation": [("M0583-ROOT", "M0583-D-READABLE", "explained_by"), ("M0583-D-READABLE", "M0583-H-SOURCE-CROSSWALK", "sourced_by")],
    "workflow": [("M0583-ROOT", "M0583-H-SOURCE-CROSSWALK", "source_gate"), ("M0583-ROOT", "M0583-X-PROVENANCE", "provenance_gate"), ("M0583-ROOT", "M0583-S-FOUNDATION", "trust_gate"), ("M0583-ROOT", "M0583-D-READABLE", "readability_gate"), ("M0583-ROOT", "M0583-E-VALIDATION", "validation_gate")],
}


def main() -> None:
    statement_hash = hashlib.sha256(STATEMENT.read_bytes()).hexdigest()
    obligations = []
    for oid, kind, risk, human, *_ in SPECS:
        obligations.append({
            "obligation_id": oid,
            "statement_fingerprint": f"lean-file-sha256:{statement_hash}" if oid == "M0583-ROOT" else f"planned-id:{oid}:v1",
            "kind": kind, "root_relevant": True, "machine_eligibility": "required",
            "human_source_eligibility": human, "readable_eligibility": "required",
            "risk_class": risk, "exclusion_reason": None, "terminal_proof_body_id": None,
        })
    keys = ["obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason"]
    projection = [{k: o[k] for k in keys} for o in obligations]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "registry_id": REGISTRY_ID,
        "theorem_id": "THM-M-0583", "item_id": "S56-M-0583-OBLIGATION_TREE",
        "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": {"canonical_declaration": "Stage1Instances.THM_M_0583.FourDimensionalTopologicalPoincareTarget", "statement_source_sha256": statement_hash, "source_inventory": "anchor-audit.json", "architecture_rule": "Conservatively expose every known four-dimensional topology boundary; source review may invalidate this registry but no node receives closure before review."},
        "denominator_projection": "Registry order, nine eligibility keys, sorted-key compact JSON.",
        "denominator_sha256": denominator, "obligations": obligations,
        "eligibility_counts": {"total": len(obligations), "root_relevant": len(obligations), "machine_required": len(obligations), "human_source_required": sum(o[3] == "required" for o in SPECS), "readable_required": len(obligations), "informational": 0},
        "status_observed_after_freeze": {"closed_obligations": [], "root_machine_debt": "M2"},
        "append_only_delta": [],
        "invalidation_rule": "A source finding that changes the proof architecture invalidates v1 and requires a new registry version; it may not silently edit the frozen denominator.",
        "status_boundary": "Scope and denominators only. No Freedman proof, source H0, machine closure, or theorem completion is credited."
    }
    nodes = []
    for oid, kind, _, human_elig, formal, output, budget, ledger in SPECS:
        nodes.append({
            "node_id": oid, "obligation_id": oid, "kind": kind,
            "human_statement": output, "formal_target": formal, "output": output,
            "human_debt": "H2", "machine_debt": "M2", "readability_debt": "R4",
            "evidence_ids": [], "source_crosswalk_id": "source-statement-crosswalk.md" if human_elig == "required" else "not_applicable",
            "provenance_id": "none", "foundation_profile": "LEAN4-MATHLIB-PINNED-v1",
            "tcb_profile": "LEAN4-4.29.0-MATHLIB-8a178386-v1", "computation_record": "none",
            "step_budget": budget, "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/THM-M-0583/obligation-tree.md#{oid.lower()}",
            "validation_spec_id": "VAL-M0583-OBLIGATION-TREE", "status_boundary": "Open architecture node; no proof-body closure is credited.",
            "task_ids": ["S56-M-0583-OBLIGATION_TREE", "S56-M-0583-PROOF"],
            "owned_sources": ["Stage1_Instances/THM-M-0583/typed-graphs.json"],
            "owner": "S56-M-0583 execution lane", "reviewer": "independent integration lane",
            "validity": {"validated_at": None, "review_due": "on source or implementation change", "invalidation_inputs": ["statement hash", "registry hash", "primary-source crosswalk", "proof implementation"], "revocation_state": "open"},
        })
    graphs = {}
    edge_number = 0
    for name, triples in GRAPH_EDGES.items():
        edges, outgoing, incoming = [], {o[0]: [] for o in SPECS}, {o[0]: [] for o in SPECS}
        for source, target, relation in triples:
            edge_number += 1
            eid = f"M0583-E{edge_number:03d}"
            edge = {"edge_id": eid, "from": source, "to": target, "relation": relation, "typing": f"{source} consumes/supports {target} via {relation}", "composition_status": "open"}
            edges.append(edge); outgoing[source].append(eid); incoming[target].append(eid)
        graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}
    typed = {
        "schema_version": "stage1-typed-graphs/1.0", "theorem_id": "THM-M-0583", "registry_id": REGISTRY_ID,
        "edge_direction": "consumer/parent to required child/support; reciprocal adjacency is explicit.",
        "nodes": nodes, "graphs": graphs,
        "closure_boundary": {"closed_obligations": [], "root_machine_debt": "M2", "root_cut_set": ["M0583-H-SOURCE-CROSSWALK", "M0583-X-FREEDMAN-CORE", "M0583-X-PROVENANCE", "M0583-S-FOUNDATION", "M0583-D-READABLE", "M0583-E-VALIDATION"], "audit_complete": False, "theorem_complete": False, "reason": "No audited placeholder-free formalization of Freedman's theorem exists in the pinned closure."}
    }
    (HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
    (HERE / "typed-graphs.json").write_text(json.dumps(typed, indent=2) + "\n")
    sections = ["# THM-M-0583 frozen obligation architecture", "", "All nodes below are open. The ledgers describe required work, not completed proof steps.", ""]
    for oid, _, _, _, _, output, budget, ledger in SPECS:
        sections.extend([f"## {oid}", "", output, "", f"Step budget: {budget}.", ""] + [f"- {step}" for step in ledger] + [""])
    sections.extend(["## Status boundary", "", "This architecture freezes a conservative denominator and checks only an exact logical adapter. It does not formalize or prove Freedman's theorem. The root remains M2 and theorem completion is false.", ""])
    (HERE / "obligation-tree.md").write_text("\n".join(sections))
    print(f"wrote {len(obligations)} obligations, {edge_number} typed edges, denominator {denominator}")


if __name__ == "__main__":
    main()
