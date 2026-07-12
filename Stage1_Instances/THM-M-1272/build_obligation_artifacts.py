#!/usr/bin/env python3
"""Build deterministic THM-M-1272 obligation and typed-graph artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1272-OBLIGATION_TREE"
TID = "THM-M-1272"

def sha(name): return hashlib.sha256((HERE / name).read_bytes()).hexdigest()
def planned(text): return "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()

# id, kind, exact semantic output, risk, machine eligibility, source eligibility, budget
rows = [
 ("M1272-ROOT", "root", "The exact canonical Hilbert-space Fountain target", "critical", "required", "required", 30),
 ("M1272-S-DEFINITIONS", "definition", "Freeze finite cores, orthogonal tails, criticality, global Palais-Smale, and strict Fountain geometry", "high", "required", "not_applicable", 45),
 ("M1272-S-BOUNDARY", "terminal", "Establish the infinite-dimensional and strict-radius boundary consequences of the total orthonormal family", "high", "required", "not_applicable", 50),
 ("M1272-S-FOUNDATION", "certificate", "Audit classical choice, noncomputability, quotient constructions, transitive axioms, and the no-oracle policy", "critical", "required", "not_applicable", 50),
 ("M1272-N-SYMMETRIC", "normalization", "Normalize the even functional to symmetric admissible classes compatible with the finite-core and tail splitting", "critical", "required", "required", 100),
 ("M1272-C-MINIMAX", "construction", "Construct nonempty symmetric minimax classes and their levels c_k", "critical", "required", "required", 100),
 ("M1272-L-LINKING", "core_lemma", "Prove every kth admissible class meets the kth orthogonal-tail sphere", "critical", "required", "required", 100),
 ("M1272-T-LOWER-BOUND", "terminal", "Derive b_k <= c_k and hence that the minimax levels tend to positive infinity", "critical", "required", "required", 75),
 ("M1272-C-DEFORMATION", "construction", "Use an odd deformation argument to construct a Palais-Smale sequence at every minimax level", "critical", "required", "required", 100),
 ("M1272-L-LEVEL-BOUNDED", "core_lemma", "Turn convergence of each functional-value sequence to c_k into the bounded-range premise required by global Palais-Smale", "high", "required", "required", 60),
 ("M1272-L-PS-SUBSEQUENCE", "core_lemma", "Apply global Palais-Smale at each level and select a convergent subsequence", "critical", "required", "required", 85),
 ("M1272-L-LIMIT-PASSAGE", "core_lemma", "Pass functional values and Frechet derivatives to the subsequential limit", "critical", "required", "required", 100),
 ("M1272-T-CRITICAL-LEVELS", "terminal", "Choose critical representatives u_k satisfying Phi(u_k) = c_k", "critical", "required", "required", 70),
 ("M1272-T-ASSEMBLE", "terminal", "Compose divergent minimax levels and exact critical representatives into the canonical root", "critical", "required", "required", 35),
 ("M1272-X-SOURCE", "terminal", "Pinpoint the primary-source theorem, hypotheses, variant, errata, and proof steps for every mathematical node", "high", "not_applicable", "required", 80),
 ("M1272-X-PROVENANCE", "certificate", "Track terminal bodies, wrappers, imports, axioms, TCB, and unique proof credit", "critical", "informational", "not_applicable", 60),
]

statement_fp = "lean-expression-sha256:529bd5aeec0b1e9e58034f05dc03531a3fd9063547aeb54b68d5c0821d46cd31"
obligations = []
for oid, kind, text, risk, machine, human, _ in rows:
    obligations.append({
      "obligation_id": oid,
      "statement_fingerprint": statement_fp if oid in {"M1272-ROOT", "M1272-S-DEFINITIONS"} else planned(text),
      "kind": kind, "root_relevant": True, "machine_eligibility": machine,
      "human_source_eligibility": human, "readable_eligibility": "required",
      "risk_class": risk,
      "exclusion_reason": {"M1272-X-SOURCE": "human_source_boundary_only", "M1272-X-PROVENANCE": "provenance_overlay_no_proof_credit"}.get(oid),
      "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1272/ObligationTree.lean#root_of_minimax_and_limit_packages" if oid == "M1272-T-ASSEMBLE" else None,
    })
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: o[k] for k in fields} for o in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r[0] for r in rows]
registry = {
 "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": TID,
 "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
 "freeze_basis": "Exact elaborated statement and immutable anchor audit; classical symmetric minimax/deformation/compactness architecture; eligibility fixed independently of proof availability.",
 "frozen_against_statement_sha256": sha("Statement.lean"), "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
 "root_obligation_id": "M1272-ROOT", "denominator_sha256": denominator,
 "frozen_denominators": {
   "inventory": ids,
   "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
   "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
   "required_readable": ids, "informational_overlays": ["M1272-X-PROVENANCE"]},
 "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new registry version with an append-only old/new ID delta.",
 "obligations": obligations}

formal = {
 "M1272-ROOT": "Stage1Instances.THM_M_1272.FountainTheoremTarget",
 "M1272-S-DEFINITIONS": "Stage1Instances.THM_M_1272.{finiteCore,orthogonalTail,IsCriticalPoint,PalaisSmale,HasFountainGeometry}",
 "M1272-T-LOWER-BOUND": "Stage1Instances.THM_M_1272.FountainMinimaxPackage",
 "M1272-T-CRITICAL-LEVELS": "Stage1Instances.THM_M_1272.FountainLimitPackage",
 "M1272-T-ASSEMBLE": "Stage1Instances.THM_M_1272.root_of_minimax_and_limit_packages"}
nodes = []
for oid, kind, text, risk, machine, human, budget in rows:
    checked = oid in {"M1272-S-DEFINITIONS", "M1272-T-ASSEMBLE"}
    mdebt = "M0-L" if oid == "M1272-S-DEFINITIONS" else ("M0-P" if oid == "M1272-T-ASSEMBLE" else ("M3" if oid == "M1272-ROOT" else "M4"))
    nodes.append({
      "node_id": "THM-M-1272-" + oid.removeprefix("M1272-"), "obligation_id": oid, "kind": kind,
      "human_statement": text, "formal_target": formal.get(oid, "planned exact Lean signature: " + text), "output": text,
      "human_debt": "H2", "machine_debt": mdebt, "readability_debt": "R4", "evidence_ids": [],
      "source_crosswalk_id": "primary-source-node-map-pending" if human == "required" else "not-applicable", "provenance_id": "none",
      "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
      "computation_record": "none; no oracle or external computation is eligible", "step_budget": budget,
      "semantic_step_ledger": {"premises": "Only exact typed proof_requires children and the canonical formal context.", "inference": text, "output": text, "outgoing_use": "Consumed only by the declared typed parent or a non-proof support edge."},
      "public_readable_target": "Stage1_Instances/THM-M-1272/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
      "status_boundary": "Frozen architecture or conditional interface only; no open child or package is claimed proved.",
      "task_ids": [ITEM, "S56-M-1272-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1272/ObligationTree.lean"] if oid == "M1272-T-ASSEMBLE" else [],
      "owner": "THM-M-1272 proof lane", "reviewer": "independent Stage1 integration lane",
      "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if checked else "open"}})

proof_pairs = [
 ("M1272-ROOT", "M1272-T-ASSEMBLE"),
 ("M1272-T-ASSEMBLE", "M1272-T-LOWER-BOUND"), ("M1272-T-ASSEMBLE", "M1272-T-CRITICAL-LEVELS"),
 ("M1272-T-LOWER-BOUND", "M1272-N-SYMMETRIC"), ("M1272-T-LOWER-BOUND", "M1272-C-MINIMAX"), ("M1272-T-LOWER-BOUND", "M1272-L-LINKING"),
 ("M1272-T-LOWER-BOUND", "M1272-C-DEFORMATION"),
 ("M1272-T-CRITICAL-LEVELS", "M1272-L-LEVEL-BOUNDED"), ("M1272-T-CRITICAL-LEVELS", "M1272-L-PS-SUBSEQUENCE"),
 ("M1272-T-CRITICAL-LEVELS", "M1272-L-LIMIT-PASSAGE")]
proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req}]
def graph(edges):
    incoming, outgoing = {i: [] for i in ids}, {i: [] for i in ids}
    for e in edges: outgoing[e["from"]].append(e["edge_id"]); incoming[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}
support = {
 "refinement": [("R01", "logical_decomposition", "M1272-T-LOWER-BOUND", "M1272-S-DEFINITIONS"), ("R02", "logical_decomposition", "M1272-T-CRITICAL-LEVELS", "M1272-S-BOUNDARY")],
 "provenance": [("V01", "provenance_of", "M1272-X-PROVENANCE", "M1272-ROOT")], "evidence": [],
 "trust": [("U01", "trusts", "M1272-ROOT", "M1272-S-FOUNDATION")],
 "documentation": [("D01", "source_map", "M1272-ROOT", "M1272-X-SOURCE"), ("D02", "documents", "M1272-X-SOURCE", "M1272-T-LOWER-BOUND"), ("D03", "documents", "M1272-X-SOURCE", "M1272-T-CRITICAL-LEVELS")],
 "workflow": [("W01", "workflow_depends_on", "M1272-T-ASSEMBLE", "M1272-T-LOWER-BOUND"), ("W02", "workflow_depends_on", "M1272-T-ASSEMBLE", "M1272-T-CRITICAL-LEVELS")]}
graphs = {"proof": graph(proof_edges)}
for name, entries in support.items(): graphs[name] = graph([{"edge_id": a, "type": b, "from": c, "to": d} for a,b,c,d in entries])
bundle = {
 "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": TID, "registry_id": "THM-M-1272-OBLIGATIONS-v1",
 "registry_denominator_sha256": denominator, "root_node_id": "M1272-ROOT",
 "edge_direction": "Proof requirements run parent to child; composes edges are reciprocal child-to-parent edges.",
 "nodes": nodes, "graphs": graphs,
 "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "theorem_complete": False,
   "first_open_cut_set": ["M1272-T-LOWER-BOUND", "M1272-T-CRITICAL-LEVELS"],
   "checked_composition": "Stage1Instances.THM_M_1272.root_of_minimax_and_limit_packages"}}
recipes = []
for oid in ids:
    lean = oid in {"M1272-ROOT", "M1272-T-ASSEMBLE"}
    recipes.append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1272/" + ("check_lean_composition.py" if lean else "check_obligation_tree.py")], "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact exit and structural assertions"}], "covered_obligation_ids": [oid], "covered_declarations": [formal[oid]] if oid in formal else []})
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": TID, "recipes": recipes}
for name, obj in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=True) + "\n")
lines = ["# THM-M-1272 frozen obligation architecture", "", f"Frozen denominator: `sha256:{denominator}`.", "", "The root remains `M3`; the Lean artifact checks only conditional composition of two open packages.", ""]
for oid, kind, text, *_ in rows:
    lines += ["## " + oid.lower(), "", f"**{kind}.** {text}.", "", "Boundary: architecture and ledger only; open proof work receives no closure credit.", ""]
lines += ["## Open cut", "", "The first open root cut is `M1272-T-LOWER-BOUND` plus `M1272-T-CRITICAL-LEVELS`. Primary-source pinpointing, terminal provenance, readable review, release replay, and independent acceptance also remain open.", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(obligations)} obligations; denominator sha256: {denominator}")
