#!/usr/bin/env python3
"""Build the frozen THM-M-0373 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

rows = [
    ("ROOT", "root", "Exact finite-generator bounded analytic Bezout target", "CoronaTheoremTarget", 8, "critical", "M4"),
    ("S-DOMAIN", "definition", "Open unit disc and ambient-function H-infinity encoding", "unitDisc; InHInfinity", 20, "high", "M1"),
    ("S-TRANSPORT", "transport", "Canonical-to-expanded statement transport", "coronaTheoremTarget_iff_expanded", 12, "normal", "M1"),
    ("N-L2", "reduction", "Convert the sum-of-norms lower bound to a finite Euclidean lower bound", "planned exact Lean signature", 45, "high", "M4"),
    ("N-SCALE", "reduction", "Normalize generator bounds and the positive corona constant", "planned exact Lean signature", 45, "high", "M4"),
    ("K-COMPLEX", "construction", "Build the finite Koszul complex and contraction by the generators", "planned exact Lean signature", 80, "critical", "M4"),
    ("K-ALGEBRA", "core_lemma", "Prove the Koszul contraction identities and pointwise algebraic Bezout seed", "planned exact Lean signature", 90, "critical", "M4"),
    ("D-DATA", "construction", "Construct smooth preliminary coefficients and their dbar defect", "planned exact Lean signature", 80, "critical", "M4"),
    ("D-CLOSED", "core_lemma", "Show the defect is dbar-closed with the required Koszul compatibility", "planned exact Lean signature", 85, "critical", "M4"),
    ("E-CARLESON", "estimate", "Establish the Carleson-measure estimates for generator derivatives", "planned exact Lean signature", 100, "critical", "M4"),
    ("E-DBAR", "bridge", "Solve the relevant dbar equation with an H-infinity bound", "planned exact Lean signature", 100, "critical", "M4"),
    ("E-BOUND", "estimate", "Propagate quantitative estimates to bounded correction coefficients", "planned exact Lean signature", 75, "critical", "M4"),
    ("A-CORRECT", "construction", "Correct the preliminary coefficients to analytic coefficients", "planned exact Lean signature", 85, "critical", "M4"),
    ("A-ANALYTIC", "core_lemma", "Prove every corrected coefficient is analytic on the disc", "planned exact Lean signature", 60, "critical", "M4"),
    ("A-BOUNDED", "core_lemma", "Prove every corrected coefficient has bounded disc image", "planned exact Lean signature", 60, "critical", "M4"),
    ("A-BEZOUT", "core_lemma", "Prove the corrected pointwise Bezout identity", "planned exact Lean signature", 55, "critical", "M4"),
    ("T-ASSEMBLE", "terminal", "Assemble boundedness, analyticity, and Bezout into the exact existential", "BoundedAnalyticBezout", 30, "critical", "M4"),
    ("X-SOURCE", "source_boundary", "Primary theorem and analytic proof source crosswalk", "primary source review open", 40, "critical", "M5"),
    ("X-TCB", "trust_boundary", "Transitive axioms, imports, artifacts, and TCB acceptance", "planned trust report", 30, "critical", "M3"),
    ("X-WORKFLOW", "workflow", "Node receipts, independent review, freshness, and revocation", "planned receipt chain", 20, "high", "M3"),
]

ids = [f"M0373-{suffix}" for suffix, *_ in rows]
statement_hash = hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
obligations = []
nodes = []
for suffix, kind, human, formal, budget, risk, machine in rows:
    oid = f"M0373-{suffix}"
    source = "required" if suffix not in {"S-DOMAIN", "S-TRANSPORT", "X-TCB", "X-WORKFLOW"} else "not_applicable"
    terminal = "repo:Stage1Instances.THM_M_0373.coronaTheoremTarget_iff_expanded" if suffix == "S-TRANSPORT" else None
    fingerprint = "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + human + "\0" + formal).encode()).hexdigest()
    obligations.append({"obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": suffix not in {"X-SOURCE", "X-TCB", "X-WORKFLOW"}, "machine_eligibility": "required" if not suffix.startswith("X-") else "informational",
        "human_source_eligibility": source, "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "typed overlay; excluded from the mathematical machine denominator" if suffix.startswith("X-") else None,
        "terminal_proof_body_id": terminal})
    nodes.append({"node_id": "THM-M-0373-" + suffix, "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "human_debt": "H1" if suffix != "X-SOURCE" else "H2",
        "machine_debt": machine, "readability_debt": "R4", "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the typed proof children listed in the proof graph.", "inference": formal,
          "output": human, "outgoing_use": "Only the declared parent edge may consume this output."},
        "provenance_id": "none", "evidence_ids": [], "source_crosswalk_id": "SRC-M0373-PRIMARY-OPEN" if source == "required" else "not-applicable",
        "foundation_profile": "Lean 4 kernel and pinned mathlib; final proof axiom profile open",
        "tcb_profile": "Lean 4.29.0 and mathlib 8a178386; transitive closure open",
        "computation_record": "none credited", "status_boundary": "Architecture only; no closure credited.",
        "owner": "THM-M-0373 proof lane", "reviewer": "independent Stage1 integration lane"})

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0373-OBLIGATION_TREE", "theorem_id": "THM-M-0373",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus the bounded immutable no-anchor result; architecture frozen before proof closure metrics.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0373-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids,
      "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
      "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
      "required_readable": ids, "informational_overlays": ["M0373-X-SOURCE", "M0373-X-TCB", "M0373-X-WORKFLOW"]},
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires version 2 and an append-only ID delta.",
    "append_only_delta": [], "obligations": obligations}

proof_pairs = [
 ("ROOT","S-DOMAIN"),("ROOT","S-TRANSPORT"),("ROOT","N-L2"),("ROOT","N-SCALE"),("ROOT","T-ASSEMBLE"),
 ("T-ASSEMBLE","A-ANALYTIC"),("T-ASSEMBLE","A-BOUNDED"),("T-ASSEMBLE","A-BEZOUT"),
 ("A-ANALYTIC","A-CORRECT"),("A-BOUNDED","A-CORRECT"),("A-BOUNDED","E-BOUND"),("A-BEZOUT","A-CORRECT"),
 ("A-CORRECT","D-DATA"),("A-CORRECT","D-CLOSED"),("A-CORRECT","E-DBAR"),
 ("D-DATA","K-COMPLEX"),("D-DATA","K-ALGEBRA"),("D-CLOSED","K-COMPLEX"),("D-CLOSED","K-ALGEBRA"),
 ("E-DBAR","E-CARLESON"),("E-DBAR","D-CLOSED"),("E-BOUND","E-DBAR"),("E-BOUND","E-CARLESON"),
 ("K-COMPLEX","N-L2"),("K-COMPLEX","N-SCALE"),("K-ALGEBRA","K-COMPLEX")]

def graph(edges):
    out, inn = {i: [] for i in ids}, {i: [] for i in ids}
    for e in edges: out[e["from"]].append(e["edge_id"]); inn[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": out, "in": inn}

proof_edges=[]
for n,(a,b) in enumerate(proof_pairs,1):
    req=f"P{n:02d}R"; comp=f"P{n:02d}C"; aa=f"M0373-{a}"; bb=f"M0373-{b}"
    proof_edges += [{"edge_id":req,"type":"proof_requires","from":aa,"to":bb,"reciprocal_edge_id":comp},
                    {"edge_id":comp,"type":"composes","from":bb,"to":aa,"reciprocal_edge_id":req}]
support = {
 "refinement": [("R01","logical_decomposition","M0373-ROOT","M0373-N-L2"),("R02","logical_decomposition","M0373-ROOT","M0373-N-SCALE")],
 "provenance": [("V01","provenance_of","M0373-X-SOURCE","M0373-ROOT")],
 "evidence": [("E01","evidence_for","M0373-X-WORKFLOW","M0373-ROOT")],
 "trust": [("T01","trusts","M0373-ROOT","M0373-X-TCB")],
 "documentation": [("D01","documents","M0373-X-SOURCE","M0373-T-ASSEMBLE")],
 "workflow": [("W01","workflow_depends_on","M0373-X-WORKFLOW","M0373-X-TCB")],
}
graphs={"proof":graph(proof_edges)}
for name, triples in support.items(): graphs[name]=graph([{"edge_id":e,"type":t,"from":a,"to":b} for e,t,a,b in triples])
bundle={"schema_version":"stage1-typed-graphs/1.0","item_id":"S56-M-0373-OBLIGATION_TREE","theorem_id":"THM-M-0373",
 "registry_id":"THM-M-0373-OBLIGATIONS-v1","registry_denominator_sha256":denominator,"root_node_id":"M0373-ROOT",
 "edge_direction":"Proof requirements run parent to child; reciprocal composes edges run child to parent.","nodes":nodes,"graphs":graphs,
 "closure_boundary":{"closed_obligations":[],"root_closed":False,"audit_complete":False,"theorem_complete":False,
   "remaining_root_cut_set":["M0373-N-L2","M0373-N-SCALE","M0373-K-COMPLEX","M0373-K-ALGEBRA","M0373-D-DATA","M0373-D-CLOSED","M0373-E-CARLESON","M0373-E-DBAR","M0373-E-BOUND","M0373-A-CORRECT","M0373-A-ANALYTIC","M0373-A-BOUNDED","M0373-A-BEZOUT","M0373-T-ASSEMBLE"]}}
for name, data in (("obligation-registry.json",registry),("typed-graphs.json",bundle)):
    (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=True)+"\n")
print(f"wrote {len(ids)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
