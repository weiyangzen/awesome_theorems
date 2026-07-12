#!/usr/bin/env python3
"""Generate the frozen THM-M-0464 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "345fe5a69ba9559544340ea64c754f3fb53f2fcf"
ITEM = "S56-M-0464-OBLIGATION_TREE"

# id, kind, statement, formal target, output, risk, H eligibility, budget, machine debt
ROWS = [
 ("M0464-ROOT", "root", "Pila-Wilkie Theorem 1.8, first version, with the frozen binder order and definitions.", "AwesomeTheorems.THM_M_0464.PilaWilkieStatement", "The exact canonical proposition.", "critical", "required", 20, "M3"),
 ("M0464-S-DEFINITIONS", "definition", "Validate the source-faithful encodings of semialgebraicity, o-minimal definability, affine height, rational points, and the algebraic part.", "planned equivalence lemmas for definitions in Statement.lean", "Source definitions transported to the Lean encodings.", "critical", "required", 100, "M3"),
 ("M0464-S-DOMAINS", "transport", "Preserve n >= 1, definability in one fixed o-minimal expansion of the real field, epsilon > 0, and T >= 1.", "planned binder/domain mutation and transport suite", "Checked source-to-formal domain identity.", "high", "required", 60, "M3"),
 ("M0464-S-BOUNDARY", "branch", "Cover empty and zero-dimensional X, and ensure finite/ncard and height boundary conventions do not weaken the claim.", "planned degenerate-case lemmas for rationalPoints and algebraicPart", "All degenerate cases feed the same root without changing it.", "high", "required", 80, "M4"),
 ("M0464-S-FOUNDATION", "certificate", "Freeze classical logic, choice, quotient, real-analysis, axiom, computation, and TCB policy.", "planned transitive axiom and trust report", "Accepted foundation boundary.", "high", "not_applicable", 50, "M4"),
 ("M0464-N-CELL", "reduction", "Reduce definable sets to the source's finite cell/decomposition and regularity data without changing the exceptional locus.", "planned o-minimal cell decomposition and regularity package", "Finite regular pieces suitable for parameterization.", "critical", "required", 100, "M4"),
 ("M0464-C-PARAM", "construction", "Construct the smooth parameterizations with uniform derivative control required by the counting argument.", "planned parameterization theorem in the frozen OMinimalStructure model", "Controlled parameter charts covering the relevant rational points.", "critical", "required", 100, "M4"),
 ("M0464-L-DETERMINANT", "core_lemma", "Prove the determinant/interpolation estimate placing sufficiently dense bounded-height rational points on controlled algebraic hypersurfaces.", "planned determinant-method estimate", "Algebraic hypersurface covers with quantitative bounds.", "critical", "required", 100, "M4"),
 ("M0464-B-ALGEBRAIC", "branch", "Separate positive-dimensional semialgebraic pieces exactly into algebraicPart X and control the residual intersections.", "planned algebraic-part extraction and intersection induction", "Only transcendental residual points remain countable by the exponent bound.", "critical", "required", 100, "M4"),
 ("M0464-L-INDUCTION", "core_lemma", "Run the source dimension/complexity induction over hypersurface intersections and parameterized pieces.", "planned dimension-induction theorem", "A finite residual cover with strictly reduced geometric complexity.", "critical", "required", 100, "M4"),
 ("M0464-L-COUNT", "core_lemma", "Combine parameterization, determinant bounds, and induction into the T^epsilon estimate for the transcendental part.", "planned quantitative rational-point counting theorem", "CountingConclusion n X epsilon for fixed S, X, and epsilon.", "critical", "required", 100, "M4"),
 ("M0464-X-TRANSPORT", "transport", "Check every representation change between source Euclidean tuples, rational heights, positive dimension, charts, and the canonical Lean target.", "planned checked equivalence and directed implication declarations", "No unproved representation gap at the root.", "critical", "required", 100, "M4"),
 ("M0464-X-SOURCE", "terminal", "Map every proof node to primary-source statements, assumptions, locators, and errata disposition.", "non-kernel primary-source crosswalk", "Reviewed human-source genealogy.", "high", "required", 100, "M4"),
 ("M0464-X-PROVENANCE", "terminal", "Identify each terminal proof body, immutable revision, wrapper, license, and dependency boundary.", "planned transitive provenance inventory", "Complete terminal-body provenance.", "high", "not_applicable", 70, "M4"),
 ("M0464-X-TRUST", "terminal", "Audit axioms, placeholders, unsafe/oracle paths, pins, replay, freshness, and independent verification.", "planned release trust certificate", "Accepted trust closure.", "critical", "not_applicable", 70, "M4"),
 ("M0464-T-ASSEMBLE", "terminal", "Compose all mathematical packages and checked transports into the exact canonical root.", "AwesomeTheorems.THM_M_0464.ObligationTree.root_from_terminal_counting", "PilaWilkieStatement, conditional on the full terminal counting premise.", "critical", "not_applicable", 20, "M3"),
]

def sha(path): return hashlib.sha256((HERE / path).read_bytes()).hexdigest()
def fingerprint(oid, target):
    if oid == "M0464-ROOT": return "lean:AwesomeTheorems.THM_M_0464.PilaWilkieStatement@" + sha("Statement.lean")
    if oid == "M0464-T-ASSEMBLE": return "lean:AwesomeTheorems.THM_M_0464.ObligationTree.root_from_terminal_counting"
    return "planned-sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

obligations = []
for oid, kind, statement, target, output, risk, human, budget, debt in ROWS:
    obligations.append({
      "obligation_id": oid, "statement_fingerprint": fingerprint(oid, target), "kind": kind,
      "formal_target": target, "root_relevant": True, "machine_eligibility": "required",
      "human_source_eligibility": human, "readable_eligibility": "required", "risk_class": risk,
      "exclusion_reason": None if human == "required" else "Formal/trust boundary; human proof-source credit belongs to its mathematical premises.",
      "terminal_proof_body_id": "local:ObligationTree.lean:root_from_terminal_counting" if oid == "M0464-T-ASSEMBLE" else None,
      "step_budget": budget})

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in obligations]
registry = {
 "schema_version": "stage1-obligation-registry/5.6.0", "item_id": ITEM, "depends_on": ["S56-M-0464-ANCHOR_AUDIT"],
 "theorem_id": "THM-M-0464", "registry_version": 1, "base_revision": BASE,
 "frozen_against_statement_sha256": sha("Statement.lean"), "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
 "root_obligation_id": "M0464-ROOT",
 "freeze_basis": "The exact elaborated first-version Pila-Wilkie statement and the immutable negative anchor audit were frozen before proof execution. The architecture follows the source's geometric parameterization and determinant-counting route; no closure status affected eligibility.",
 "denominator_sha256": denominator,
 "frozen_denominators": {"inventory": ids, "required_machine": ids,
   "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
   "required_readable": ids},
 "append_only_deltas": [], "obligations": obligations,
 "closure_boundary": {"root_machine_debt": "M3", "root_closed": False, "audit_complete": False, "theorem_complete": False,
   "immediate_root_cut_set": ["M0464-S-DEFINITIONS", "M0464-N-CELL", "M0464-C-PARAM", "M0464-L-DETERMINANT", "M0464-B-ALGEBRAIC", "M0464-L-INDUCTION", "M0464-L-COUNT", "M0464-X-TRANSPORT"]},
}

nodes = []
for row, data in zip(obligations, ROWS):
    oid, kind, statement, target, output, risk, human, budget, debt = data
    nodes.append({
      "node_id": "THM-" + oid, "obligation_id": oid, "kind": kind, "human_statement": statement,
      "formal_target": target, "output": output, "human_debt": "H1", "machine_debt": debt,
      "readability_debt": "R3", "evidence_ids": [],
      "source_crosswalk_id": "PW2006-node-map-pending" if human == "required" else "not-applicable",
      "provenance_id": "anchor-audit:f1ba60e8ff4ee2085e42f27a7bfda831034fabebb7e5b207fd624f4740d31045",
      "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
      "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
      "computation_record": "none; no computation or oracle is credited", "step_budget": budget,
      "semantic_step_ledger": {"premises": "Exactly the incoming proof_requires premises and the frozen formal context.",
        "inference": statement, "output": output, "outgoing_use": "Only typed outgoing edges may consume this output."},
      "public_readable_target": "Stage1_Instances/THM-M-0464/obligation-tree.md#" + oid.lower(),
      "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture/interface only; open premises remain open and no root closure is claimed.",
      "task_ids": [ITEM, "S56-M-0464-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0464/ObligationTree.lean"] if oid == "M0464-T-ASSEMBLE" else [],
      "owner": "THM-M-0464 proof lane", "reviewer": "independent Stage1 integration lane",
      "validity": {"validated_at": "2026-07-12" if debt == "M3" else None, "review_due": "before proof acceptance",
        "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if debt == "M3" else "open"}})

proof_pairs = [
 ("M0464-ROOT","M0464-T-ASSEMBLE"), ("M0464-T-ASSEMBLE","M0464-S-DEFINITIONS"),
 ("M0464-T-ASSEMBLE","M0464-S-DOMAINS"), ("M0464-T-ASSEMBLE","M0464-S-BOUNDARY"),
 ("M0464-T-ASSEMBLE","M0464-L-COUNT"), ("M0464-T-ASSEMBLE","M0464-X-TRANSPORT"),
 ("M0464-L-COUNT","M0464-N-CELL"), ("M0464-L-COUNT","M0464-C-PARAM"),
 ("M0464-L-COUNT","M0464-L-DETERMINANT"), ("M0464-L-COUNT","M0464-B-ALGEBRAIC"),
 ("M0464-L-COUNT","M0464-L-INDUCTION"), ("M0464-C-PARAM","M0464-N-CELL"),
 ("M0464-B-ALGEBRAIC","M0464-L-DETERMINANT"), ("M0464-L-INDUCTION","M0464-B-ALGEBRAIC")]

def graph(name, edge_type, pairs):
    edges=[]; incoming={x:[] for x in ids}; outgoing={x:[] for x in ids}
    for i,(a,b) in enumerate(pairs,1):
        eid=f"E-{name.upper()}-{i:02d}"; e={"edge_id":eid,"type":edge_type,"from":a,"to":b}
        edges.append(e); outgoing[a].append(eid); incoming[b].append(eid)
    return {"edges":edges,"out":outgoing,"in":incoming}

graphs = {
 "proof": graph("proof", "proof_requires", proof_pairs),
 "refinement": graph("refine", "refines", [("M0464-ROOT","M0464-S-DEFINITIONS"),("M0464-ROOT","M0464-S-DOMAINS"),("M0464-ROOT","M0464-S-BOUNDARY")]),
 "provenance": graph("provenance", "provenance_of", [("M0464-X-PROVENANCE",x) for x in ids if x not in ("M0464-X-PROVENANCE",)]),
 "evidence": graph("evidence", "evidence_for", []),
 "trust": graph("trust", "trusts", [(x,"M0464-X-TRUST") for x in ids if x != "M0464-X-TRUST"]),
 "documentation": graph("docs", "documents", [("M0464-X-SOURCE",x) for x in ids if x not in ("M0464-X-SOURCE","M0464-X-PROVENANCE","M0464-X-TRUST")]),
 "workflow": graph("workflow", "workflow_depends_on", [("M0464-ROOT",x) for x in ids if x != "M0464-ROOT"]),
}
bundle = {"schema_version":"stage1-typed-graphs/5.6.0", "item_id":ITEM, "theorem_id":"THM-M-0464",
 "root_obligation_id":"M0464-ROOT", "registry_denominator_sha256":denominator, "nodes":nodes, "graphs":graphs,
 "closure_boundary":registry["closure_boundary"]}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(ids)} obligations; denominator {denominator}")
