#!/usr/bin/env python3
"""Build the canonical THM-M-1566 obligation freeze deterministically."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1566-OBLIGATION_TREE"

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def planned(text: str) -> str:
    return "planned:v1:sha256:" + sha(text.encode())

# id, kind, statement, formal target, output, H, M, risk, source eligibility
ROWS = [
 ("M1566-ROOT", "root", "Exact GIP Corollary 5.9 target frozen in Statement.lean.", "Stage1Instances.THMM1566.GIPCorollary59Target", "Unique local solution with the stated renormalized approximation characterization.", "H1", "M4", "critical", "required"),
 ("M1566-S-INTERFACE", "definition", "Interpret every analytic object in the abstract API by concrete parabolic Holder-Besov, distribution, solution, and equation objects.", "planned concrete implementation and adequacy theorems for GIPCorollary59API", "A concrete API whose predicates have the source meanings.", "H1", "M4", "critical", "required"),
 ("M1566-S-PARAMETERS", "terminal", "Preserve alpha in (2/3,1), beta in (2-2 alpha,alpha], white noise on T2, normalized mollifiers, and almost-sure strict positivity.", "Stage1Instances.THMM1566.{GIPCorollary59Data,alpha_boundary_excluded}", "Checked parameter and endpoint boundary.", "H1", "M0-L", "high", "required"),
 ("M1566-S-FOUNDATION", "certificate", "Fix the classical measure-theoretic foundation, transitive axiom set, TCB, and no-oracle policy.", "planned transitive axiom and TCB certificate", "Accepted trust boundary for terminal bodies.", "H2", "M4", "critical", "not_applicable"),
 ("M1566-N-SPACES", "normalization", "Construct the anisotropic parabolic Holder-Besov scale on the two-dimensional torus and prove embeddings and time-localized norm equivalences used by the argument.", "planned parabolic Holder-Besov space declarations and equivalences", "Concrete spaces and norms matching the paper's notation.", "H1", "M4", "critical", "required"),
 ("M1566-C-NOISE", "construction", "Lift spatial white noise to the enhanced noise carrying the resonant products and prove mollified enhanced-noise convergence.", "planned enhanced-white-noise construction and convergence theorem", "A data-measurable enhanced noise and convergent approximations.", "H1", "M4", "critical", "required"),
 ("M1566-L-PARAPRODUCT", "core_lemma", "Formalize paraproduct, resonant product, commutator, and their Holder-Besov continuity estimates at the required exponents.", "planned paraproduct and commutator estimate package", "The analytic multiplication and commutator bounds.", "H1", "M4", "critical", "required"),
 ("M1566-L-SCHAUDER", "core_lemma", "Prove the localized parabolic Schauder estimates and time-smallness factors used by the solution map.", "planned parabolic Schauder estimate package", "Regularity gain and contraction time factors.", "H1", "M4", "critical", "required"),
 ("M1566-C-RENORMALIZATION", "construction", "Define the mollified resonant products and Lemma 5.8 counterterms, prove well-definedness, and identify their renormalized limit.", "planned Lemma 5.8 renormalization construction and convergence", "Renormalized models and convergent counterterm-corrected products.", "H1", "M4", "critical", "required"),
 ("M1566-L-FIXEDPOINT", "core_lemma", "Build the paracontrolled solution space and prove local contraction, stability, continuation to a positive data-measurable stopping time, and uniqueness.", "planned Theorem 5.4 fixed-point and stability package", "Local solution, stability, stopping time, and uniqueness estimates.", "H1", "M4", "critical", "required"),
 ("M1566-T-EXISTENCE", "terminal", "Combine the enhanced-noise, renormalization, Schauder, and fixed-point packages to construct a limit solution and every required mollified family with convergence in probability.", "Stage1Instances.THMM1566.Corollary59ExistencePackage", "Existence half of IsCorollary59Solution for all canonical inputs.", "H1", "M4", "critical", "required"),
 ("M1566-T-UNIQUENESS", "terminal", "Use fixed-point stability to show any two solutions satisfying the full Corollary 5.9 characterization coincide.", "Stage1Instances.THMM1566.Corollary59UniquenessPackage", "Uniqueness for the exact solution predicate.", "H1", "M4", "critical", "required"),
 ("M1566-T-ASSEMBLE", "transport", "Compose exact existence and uniqueness packages into the unique-existence root without adding assumptions.", "Stage1Instances.THMM1566.root_of_existence_and_uniqueness", "The exact canonical target, conditionally on both packages.", "H1", "M0-L", "high", "required"),
 ("M1566-X-SOURCE", "terminal", "Map every analytic transition to Corollary 5.9, Lemma 5.8, Theorem 5.4, and their upstream results with assumption and errata review.", "human-source ledger and independent review", "Pinpoint human-source coverage.", "H1", "M5", "high", "required"),
 ("M1566-X-PROVENANCE", "certificate", "Inventory every terminal body, wrapper, import, axiom, tool, and replay boundary.", "planned proof-body provenance and trust closure", "Release provenance coverage without proof credit.", "H2", "M4", "critical", "not_applicable"),
]

statement_hash = sha((HERE / "Statement.lean").read_bytes())
audit_hash = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, claim, target, output, h, m, risk, source in ROWS:
    fingerprint = ("lean-expression-sha256:70ee4869b479335e8f13e902d68b13f73828f675124603909189fec1ccee473a"
                   if oid == "M1566-ROOT" else planned(target + "\n" + claim))
    obligations.append({
      "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
      "root_relevant": True,
      "machine_eligibility": "not_applicable" if oid == "M1566-X-SOURCE" else ("informational" if oid == "M1566-X-PROVENANCE" else "required"),
      "human_source_eligibility": source, "readable_eligibility": "required",
      "risk_class": risk,
      "exclusion_reason": ({"M1566-X-SOURCE": "human_source_boundary_only", "M1566-X-PROVENANCE": "release_overlay_no_proof_credit"}.get(oid)),
      "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1566/ObligationTree.lean#root_of_existence_and_uniqueness" if oid == "M1566-T-ASSEMBLE" else None,
    })
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode())
ids = [r[0] for r in ROWS]
registry = {
 "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-1566", "registry_version": 1,
 "frozen_at": "2026-07-12T00:00:00+08:00",
 "freeze_basis": "Exact Corollary 5.9 statement and bounded anchor audit; architecture follows the source dependency chain through Lemma 5.8 and Theorem 5.4; eligibility was assigned without regard to closure.",
 "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": audit_hash,
 "root_obligation_id": "M1566-ROOT", "denominator_sha256": denominator,
 "frozen_denominators": {
   "inventory": ids,
   "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
   "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
   "required_readable": ids, "informational_overlays": ["M1566-X-PROVENANCE"]},
 "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and an append-only old/new ID delta.",
 "obligations": obligations, "append_only_delta": [],
 "status_observed_after_freeze": {"closed_obligations": ["M1566-S-PARAMETERS", "M1566-T-ASSEMBLE"], "root_machine_debt": "M4"},
 "status_boundary": "The registry freezes scope only. The conditional composition theorem is not a proof of either analytic package or the root."
}

nodes = []
for oid, kind, claim, target, output, h, m, risk, source in ROWS:
    nodes.append({
      "node_id": "THM-M-1566-" + oid.removeprefix("M1566-"), "obligation_id": oid, "kind": kind,
      "human_statement": claim, "formal_target": target, "output": output,
      "human_debt": h, "machine_debt": m, "readability_debt": "R3", "evidence_ids": [],
      "source_crosswalk_id": "gip-v4-node-map-review-pending" if source == "required" else "not-applicable",
      "provenance_id": "local-conditional-composition" if oid == "M1566-T-ASSEMBLE" else "none",
      "foundation_profile": "lean4-mathlib-classical-measure/policy-review-pending",
      "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
      "computation_record": "none; no numerical experiment or oracle may close this obligation",
      "step_budget": 100 if risk == "critical" else 60,
      "semantic_step_ledger": {"premises": "The exact typed proof children listed in the proof graph and no implicit theorem package.", "inference": claim, "output": output, "outgoing_use": "Consumed only by the reciprocal parent composition edge or a declared non-proof edge."},
      "public_readable_target": f"Stage1_Instances/THM-M-1566/obligation-tree.md#{oid.lower()}",
      "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture and planned signature only unless machine debt is M0-L; no open analytic premise is discharged.",
      "task_ids": [ITEM, "S56-M-1566-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1566/ObligationTree.lean"] if oid == "M1566-T-ASSEMBLE" else [],
      "owner": "THM-M-1566 proof lane", "reviewer": "independent Stage1 integration lane",
      "validity": {"validated_at": "2026-07-12" if m == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation registry", "toolchain"], "revocation_state": "provisional" if m == "M0-L" else "open"}
    })

requirements = [
 ("M1566-ROOT", "M1566-T-ASSEMBLE"),
 ("M1566-T-ASSEMBLE", "M1566-T-EXISTENCE"), ("M1566-T-ASSEMBLE", "M1566-T-UNIQUENESS"),
 ("M1566-T-EXISTENCE", "M1566-C-RENORMALIZATION"), ("M1566-T-EXISTENCE", "M1566-L-FIXEDPOINT"),
 ("M1566-T-UNIQUENESS", "M1566-L-FIXEDPOINT"),
 ("M1566-C-RENORMALIZATION", "M1566-C-NOISE"), ("M1566-C-RENORMALIZATION", "M1566-L-PARAPRODUCT"),
 ("M1566-L-FIXEDPOINT", "M1566-N-SPACES"), ("M1566-L-FIXEDPOINT", "M1566-L-PARAPRODUCT"), ("M1566-L-FIXEDPOINT", "M1566-L-SCHAUDER"),
]
proof_edges = []
for parent, child in requirements:
    req, cmp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof_edges += [{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": cmp}, {"edge_id": cmp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}]

graph_edges = {
 "proof": proof_edges,
 "refinement": [
   {"edge_id":"REF-ROOT-INTERFACE","from":"M1566-ROOT","type":"logical_decomposition","to":"M1566-S-INTERFACE"},
   {"edge_id":"REF-ROOT-PARAMETERS","from":"M1566-ROOT","type":"logical_decomposition","to":"M1566-S-PARAMETERS"}],
 "provenance": [
   {"edge_id":"SRC-ROOT","from":"M1566-ROOT","type":"source_map","to":"M1566-X-SOURCE"},
   {"edge_id":"PROV-ROOT","from":"M1566-X-PROVENANCE","type":"provenance_of","to":"M1566-ROOT"}],
 "evidence": [],
 "trust": [{"edge_id":"TRUST-FOUND","from":"M1566-ROOT","type":"trusts","to":"M1566-S-FOUNDATION"},{"edge_id":"TRUST-PROV","from":"M1566-ROOT","type":"trusts","to":"M1566-X-PROVENANCE"}],
 "documentation": [{"edge_id":"DOC-SOURCE","from":"M1566-X-SOURCE","type":"documents","to":"M1566-ROOT"}],
 "workflow": [{"edge_id":f"FLOW-{p}-{c}","from":p,"type":"workflow_depends_on","to":c} for p,c in requirements]
}
graphs = {}
for name, edges in graph_edges.items():
    out, incoming = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": out, "in": incoming}
bundle = {
 "schema_version":"stage1-typed-graphs/1.0", "item_id":ITEM, "theorem_id":"THM-M-1566", "registry_id":"THM-M-1566-OBLIGATIONS-v1", "registry_denominator_sha256":denominator,
 "root_node_id":"M1566-ROOT", "edge_direction":"Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes":nodes, "graphs":graphs,
 "closure_boundary":{"closed_obligations":["M1566-S-PARAMETERS","M1566-T-ASSEMBLE"],"root_closed":False,"audit_complete":False,"theorem_complete":False,"remaining_root_cut_set":["M1566-T-EXISTENCE","M1566-T-UNIQUENESS"],"composition_certificates":["Stage1Instances.THMM1566.root_of_existence_and_uniqueness"],"reason":"The composition is conditional; both root-critical analytic packages remain M4."}
}
recipes = []
for n in nodes:
    recipes.append({"recipe_id":n["validation_spec_id"],"cwd":"repository root","argv":["python3","Stage1_Instances/THM-M-1566/validate_obligation_tree.py"],"env_allowlist":{"LANG":"C.UTF-8","TZ":"Asia/Shanghai"},"timeout_seconds":120,"network_policy":"denied","expected_exit":0,"expected_outputs":[{"path_or_stream":"stdout","semantic_hash_policy":"capture exact output; release receipt pending"}],"covered_obligation_ids":[n["obligation_id"]],"covered_declarations":[n["formal_target"]] if n["machine_debt"] == "M0-L" else []})
specs = {"schema_version":"stage1-validation-specs/1.0","item_id":ITEM,"theorem_id":"THM-M-1566","recipes":recipes,"status_boundary":"Recipes are specifications only; this phase records warm local execution, not release receipts."}

for name, obj in (("obligation-registry.json",registry),("typed-graphs.json",bundle),("validation-specs.json",specs)):
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=True)+"\n")

lines = ["# THM-M-1566 frozen obligation tree", "", "This is the reader projection of registry v1. Open debt is intentional and is not theorem completion.", ""]
for row, node in zip(ROWS, nodes):
    oid = row[0]
    lines += [f"## {oid}", "", f"**Claim:** {node['human_statement']}", "", f"**Output:** {node['output']}", "", f"**Formal target:** `{node['formal_target']}`", "", f"**Status:** `[{node['human_debt']}, {node['machine_debt']}, {node['readability_debt']}]`. {node['status_boundary']}", ""]
(HERE/"obligation-tree.md").write_text("\n".join(lines))
print(f"wrote 15 obligations, {sum(len(v['edges']) for v in graphs.values())} typed edges; denominator {denominator}")
