#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

SPECS = [
    ("ROOT", "root", "critical", "Exact bounded-entry Wigner semicircle law", "The exact canonical proposition in Statement.lean."),
    ("S-DEFINITIONS", "definition", "high", "Freeze the random-matrix, eigenvalue, empirical-average, and semicircle-integral objects", "Exact objects used by all analytic nodes."),
    ("S-BOUNDARY", "normalization", "high", "Preserve n+1 dimensions, off-diagonal variance one, diagonal freedom, bounded entries, and one common almost-everywhere set", "No GOE, expected-only, moment-only, or pointwise-null-set substitute."),
    ("S-FOUNDATION", "certificate", "critical", "Freeze the classical measure-theory, Hermitian-spectrum, choice, and kernel trust boundary", "A foundation profile for every eventual body."),
    ("N-TRACE", "bridge", "critical", "Rewrite empirical monomial averages as normalized traces of scaled matrix powers", "An exact trace-moment identity with scaling and eigenvalue multiplicity."),
    ("B-PARITY", "branch", "high", "Split trace moments into odd and even exponents and prove exhaustiveness", "Odd moments vanish asymptotically; even moments enter the pairing count."),
    ("C-WALKS", "construction", "critical", "Expand normalized traces into closed index walks and associate entry products and multigraphs", "A finite walk sum with all multiplicities and normalization factors."),
    ("L-INDEPENDENCE", "core_lemma", "critical", "Use upper-triangular independence and centering to eliminate singly occurring edges", "Only walk patterns with every edge repeated can contribute."),
    ("L-NONPAIR", "core_lemma", "critical", "Bound all surviving non-pairing and diagonal-containing walk patterns using the common entry bound", "Every non-leading pattern is o(1) after normalization."),
    ("L-PAIRING", "core_lemma", "critical", "Identify leading even closed walks with genus-zero pairings", "The leading expectation is the number of noncrossing pairings."),
    ("L-CATALAN", "bridge", "high", "Count noncrossing pairings by Catalan numbers", "The limiting even moment is the corresponding Catalan number."),
    ("L-EXPECTATION", "core_lemma", "critical", "Combine the walk bounds and pairing count to prove convergence of expected trace moments", "Expected odd/even empirical moments converge to semicircle moments."),
    ("L-CONCENTRATION", "core_lemma", "critical", "Prove summable deviation bounds for every fixed normalized trace moment", "Borel-Cantelli applies without independence between matrix sizes."),
    ("T-MOMENTS-AS", "terminal", "critical", "Upgrade expected moment convergence to simultaneous almost-sure convergence for all natural powers", "On one full-measure set, every empirical polynomial moment converges."),
    ("L-SEMICIRCLE-MOMENTS", "core_lemma", "high", "Compute the moments of the stated density and verify it is a probability measure", "Odd moments are zero and even moments are Catalan."),
    ("L-TIGHTNESS", "core_lemma", "critical", "Derive almost-sure tightness of empirical spectral measures from high even moments", "Uniformly small tail mass on the common full-measure set."),
    ("L-POLYNOMIAL", "core_lemma", "high", "Extend monomial convergence to polynomial test functions", "Every real polynomial integral converges on the common set."),
    ("L-BC-APPROX", "core_lemma", "critical", "Approximate bounded continuous tests on compact intervals and control both empirical and semicircle tails", "Convergence holds for every bounded continuous real test function."),
    ("T-WEAK", "terminal", "critical", "Compose moment, determinacy, tightness, and approximation packages", "SampleWeakConvergence for almost every sample."),
    ("T-COMPOSE", "terminal", "critical", "Transport the terminal sample predicate to the exact frozen root", "The complete canonical conclusion, with every root hypothesis preserved."),
    ("X-SOURCE", "terminal", "high", "Map every analytic obligation to pinpoint human sources", "Source overlay only; no machine-proof credit."),
    ("X-PROVENANCE", "terminal", "critical", "Track wrapper/body identities, axioms, and external boundaries", "Provenance overlay only; no machine-proof credit."),
]

def planned(oid, statement, output):
    payload = f"THM-M-1105|v1|{oid}|{statement}|{output}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(payload).hexdigest()

ids = [f"M1105-{x[0]}" for x in SPECS]
machine = [x for x in ids if not x.startswith("M1105-X-")]
human = [x for x in ids if x not in {"M1105-S-DEFINITIONS", "M1105-S-FOUNDATION", "M1105-X-PROVENANCE"}]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-1105-OBLIGATION_TREE",
    "theorem_id": "THM-M-1105", "registry_version": 1,
    "freeze_basis": "Exact elaborated statement plus bounded immutable anchor audit; moment-method architecture selected before proof implementation.",
    "root_obligation_id": "M1105-ROOT",
    "frozen_denominators": {"inventory": ids, "required_machine": machine, "required_human_source": human,
      "required_readable": ids, "informational_overlays": ["M1105-X-SOURCE", "M1105-X-PROVENANCE"]},
    "eligibility_policy": "Every semantic component required by the selected moment method remains required regardless of present library coverage. Overlays earn no proof credit.",
    "exclusions": ["GOE-only, expected-measure, finite-moment, and convergence-in-probability results are not the root.",
      "Aliases, wrappers, transports, source rows, and presentation nodes cannot add semantic or terminal-body credit."],
    "obligations": []
}
for key, kind, risk, statement, output in SPECS:
    oid = f"M1105-{key}"
    registry["obligations"].append({"obligation_id": oid,
      "statement_fingerprint": "lean-output-sha256:1f7809988010cf399cf6cabff27fd5630468e795b282002e6286a7f6a39d6769" if key == "ROOT" else planned(oid, statement, output),
      "kind": kind, "root_relevant": not key.startswith("X-"),
      "machine_eligibility": "informational" if key.startswith("X-") else "required",
      "human_source_eligibility": "required" if oid in human else "not_applicable",
      "readable_eligibility": "required", "risk_class": risk,
      "exclusion_reason": "informational_overlay_no_proof_credit" if key.startswith("X-") else None,
      "terminal_proof_body_id": None})

proof = [
 ("S-DEFINITIONS","N-TRACE"),("S-BOUNDARY","N-TRACE"),("S-FOUNDATION","N-TRACE"),
 ("N-TRACE","B-PARITY"),("B-PARITY","C-WALKS"),("C-WALKS","L-INDEPENDENCE"),
 ("L-INDEPENDENCE","L-NONPAIR"),("L-INDEPENDENCE","L-PAIRING"),("L-PAIRING","L-CATALAN"),
 ("L-NONPAIR","L-EXPECTATION"),("L-CATALAN","L-EXPECTATION"),("B-PARITY","L-EXPECTATION"),
 ("L-EXPECTATION","T-MOMENTS-AS"),("L-CONCENTRATION","T-MOMENTS-AS"),
 ("L-SEMICIRCLE-MOMENTS","T-WEAK"),("T-MOMENTS-AS","T-WEAK"),("L-TIGHTNESS","T-WEAK"),
 ("L-POLYNOMIAL","T-WEAK"),("L-BC-APPROX","T-WEAK"),("T-WEAK","T-COMPOSE"),("T-COMPOSE","ROOT")]
def edge(a,b,t): return {"from": f"M1105-{a}" if not a.startswith("M1105-") else a, "to": f"M1105-{b}" if not b.startswith("M1105-") else b, "type": t}
graphs = {
 "proof": [edge(a,b,"proof_requires") for a,b in proof] + [edge("T-WEAK","T-COMPOSE","composes"), edge("T-COMPOSE","ROOT","composes")],
 "refinement": [edge("ROOT",x,"logical_decomposition") for x in ["S-DEFINITIONS","S-BOUNDARY","S-FOUNDATION","N-TRACE","B-PARITY","C-WALKS","L-INDEPENDENCE","L-NONPAIR","L-PAIRING","L-CATALAN","L-EXPECTATION","L-CONCENTRATION","T-MOMENTS-AS","L-SEMICIRCLE-MOMENTS","L-TIGHTNESS","L-POLYNOMIAL","L-BC-APPROX","T-WEAK","T-COMPOSE"]],
 "provenance": [edge("X-PROVENANCE",x,"provenance_of") for x in ids if not x.endswith("X-PROVENANCE")],
 "evidence": [],
 "trust": [edge(x,"S-FOUNDATION","trusts") for x in ["ROOT","N-TRACE","L-CONCENTRATION","T-WEAK"]],
 "documentation": [edge(x,"X-SOURCE","source_map") for x in human if x != "M1105-X-SOURCE"] + [edge(x,"X-PROVENANCE","documents") for x in machine],
 "workflow": [edge("M1105-WF-ANCHOR","M1105-WF-TREE","workflow_depends_on"), edge("M1105-WF-TREE","M1105-WF-PROOF","workflow_depends_on"), edge("M1105-WF-PROOF","M1105-WF-VALIDATION","workflow_depends_on")]
}
nodes = []
for key, kind, risk, statement, output in SPECS:
    oid=f"M1105-{key}"
    nodes.append({"node_id": f"THM-M-1105-{key}", "obligation_id": oid, "kind": kind,
      "human_statement": statement, "formal_target": "Stage1.THM_M_1105.WignerSemicircleLaw" if key=="ROOT" else f"planned signature v1 for {oid}",
      "output": output, "human_debt": "H2", "machine_debt": "M3", "readability_debt": "R4",
      "evidence_ids": [], "source_crosswalk_id": "anchor-inventory.json" if oid in human else "not-applicable",
      "provenance_id": "none", "foundation_profile": "lean4-mathlib-pinned-v1", "tcb_profile": "lean-kernel-v1",
      "computation_record": "none", "step_budget": 12,
      "semantic_step_ledger": [{"step": 1, "premises": [e["from"] for e in graphs["proof"] if e["to"]==oid and e["type"]=="proof_requires"], "inference": statement, "output": output, "outgoing_use": [e["to"] for e in graphs["proof"] if e["from"]==oid]}],
      "public_readable_target": f"Stage1_Instances/THM-M-1105/obligation-tree.md#{oid.lower()}",
      "validation_spec_id": "S56-M-1105-OBLIGATION-TREE-CHECK-v1",
      "status_boundary": "Architecture only; no accepted proof body, source closure, or root closure.",
      "task_ids": ["S56-M-1105-OBLIGATION_TREE", "S56-M-1105-PROOF"],
      "owned_sources": ["Stage1_Instances/THM-M-1105/obligation-registry.json", "Stage1_Instances/THM-M-1105/typed-graphs.json"],
      "owner": "stage1-worker", "reviewer": "independent-master-required",
      "validity": {"validated_at": None, "review_due": "before-master-acceptance", "invalidation_inputs": ["Statement.lean", "anchor-inventory.json", "obligation-registry.json"], "revocation_state": "open"}})

bundle={"schema_version":"stage1-typed-graphs/1.0","theorem_id":"THM-M-1105","registry_version":1,
 "source_bindings":{"statement_source_sha256":"b7e0e83c6cf2a596e34aa4e8b9b869a05700375a6a4f40b0d4ca3d99a1fdf75b","root_elaboration_output_sha256":"1f7809988010cf399cf6cabff27fd5630468e795b282002e6286a7f6a39d6769"},
 "nodes":nodes,"graphs":graphs,
 "composition_certificates":[{"parent":"M1105-ROOT","children":["M1105-T-COMPOSE"],"lean_declaration":"root_of_sample_weak_convergence","status":"interface_checked_children_open"}],
 "closure_boundary":{"closed_obligations":[],"root_closed":False,"audit_complete":False,"theorem_complete":False,"root_machine_debt":"M3",
   "remaining_root_cut_set":["M1105-L-NONPAIR","M1105-L-PAIRING","M1105-L-CONCENTRATION","M1105-L-TIGHTNESS","M1105-L-BC-APPROX"]}}

(HERE/"obligation-registry.json").write_text(json.dumps(registry,indent=2)+"\n")
(HERE/"typed-graphs.json").write_text(json.dumps(bundle,indent=2)+"\n")
doc=["# THM-M-1105 obligation tree","","Registry version 1 freezes a bounded-entry moment-method route before proof implementation. Every semantic node below is open.",""]
for n in nodes:
    doc += [f"## {n['obligation_id']}","",n["human_statement"],"",f"Formal target: `{n['formal_target']}`","",f"Output: {n['output']}","","Semantic ledger:",f"1. Inputs: {', '.join(n['semantic_step_ledger'][0]['premises']) or 'frozen statement context' }.",f"2. Inference: {n['semantic_step_ledger'][0]['inference']}.",f"3. Output and use: {n['semantic_step_ledger'][0]['output']}","",f"Boundary: {n['status_boundary']}",""]
(HERE/"obligation-tree.md").write_text("\n".join(doc))
den=hashlib.sha256("\n".join(ids).encode()).hexdigest()
print(f"built {len(ids)} obligations; denominator sha256: {den}")
