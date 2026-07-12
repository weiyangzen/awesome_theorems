#!/usr/bin/env python3
"""Build the frozen THM-M-1080 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1080-OBLIGATION_TREE"
THEOREM = "THM-M-1080"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


# This architecture is selected from the bounded-increment exponential-moment proof,
# before any later proof phase is allowed to assign closure.
SPECS = [
    ("M1080-ROOT", "root", "critical", "The exact arbitrary-measurable-space upper-tail proposition in Statement.lean.", "Stage1Instances.THM_M_1080.Statement", "The canonical Azuma upper-tail inequality."),
    ("M1080-S-DEFINITIONS", "definition", "high", "Freeze squaredBoundSum, event probability via Measure.real, martingale, filtration, and a.e. increment bounds.", "Stage1Instances.THM_M_1080.{squaredBoundSum,Statement}", "The exact objects and coercions used by every proof node."),
    ("M1080-S-SCOPE", "normalization", "critical", "Preserve the ordered universe, probability, filtration, process, varying NNReal bounds, horizon, and nonnegative-threshold binders.", "binder package of Stage1Instances.THM_M_1080.Statement", "No StandardBorelSpace or stronger conditional-sub-Gaussian premise is inserted."),
    ("M1080-S-BOUNDARY", "branch", "high", "Account for n=0, t=0, and squaredBoundSum=0 under Lean total division.", "planned boundary lemmas for the frozen expression", "All degenerate inputs remain inside the root theorem."),
    ("M1080-S-FOUNDATION", "certificate", "critical", "Fix classical measure theory, Lean/mathlib trust, axiom inspection, and no-oracle policy.", "planned transitive trust and axiom report", "An explicit foundation boundary for eventual terminal bodies."),
    ("M1080-N-INCREMENTS", "construction", "high", "Define Y k = X (k+1)-X k and establish measurability, integrability, adaptation, and conditional mean zero from Martingale X G mu.", "planned martingale-difference interface", "A bounded centered increment family without strengthening the space."),
    ("M1080-N-TELESCOPE", "normalization", "high", "Prove the finite telescoping identity sum_{k<n} Y k = X n-X 0 and align c(k+1) indexing.", "planned finite-sum telescoping transport", "The sum-tail event is exactly the canonical event."),
    ("M1080-C-EXPONENTIAL", "construction", "critical", "Construct the exponential process from partial sums and deterministic squared-bound sums and prove measurability/integrability needed for iteration.", "planned exponential-supermartingale package", "A valid exponential-moment object for every lambda >= 0."),
    ("M1080-L-COND-HOEFFDING", "core_lemma", "critical", "Derive the conditional Hoeffding bound for each a.e. centered increment in [-c(k+1),c(k+1)] on the frozen arbitrary measurable space.", "planned conditional exponential-moment inequality", "The one-step factor exp(lambda^2*c(k+1)^2/2)."),
    ("M1080-L-MGF-ITERATE", "core_lemma", "critical", "Iterate the one-step conditional bound through the filtration.", "planned finite-horizon MGF induction", "E exp(lambda*(X n-X 0)) <= exp(lambda^2*squaredBoundSum c n/2)."),
    ("M1080-L-MARKOV", "core_lemma", "high", "Apply exponential Markov to the canonical upper-tail event.", "planned exponential Markov inequality", "For lambda >= 0, probability is bounded by exp(-lambda*t+lambda^2*S/2)."),
    ("M1080-L-OPTIMIZE", "core_lemma", "critical", "Choose and normalize the exponential parameter, with an explicit zero-sum branch, to obtain the frozen total-division exponent.", "planned real arithmetic optimization", "The exact exp(-t^2/(2*S)) bound for positive thresholds."),
    ("M1080-T-POSITIVE", "terminal", "critical", "Compose increments, telescoping, conditional Hoeffding, MGF iteration, Markov, and optimization for t>0.", "Stage1Instances.THM_M_1080.ObligationTree.PositiveThresholdPackage", "The canonical conclusion restricted only to the positive-threshold branch."),
    ("M1080-T-ZERO", "terminal", "high", "Prove the t=0 conclusion from probability <= 1 and simplification of the frozen exponent.", "Stage1Instances.THM_M_1080.ObligationTree.ZeroThresholdPackage", "The canonical conclusion at the included threshold boundary."),
    ("M1080-T-ASSEMBLE", "transport", "high", "Recombine t=0 and t>0 without changing any other binder or conclusion.", "Stage1Instances.THM_M_1080.ObligationTree.azumaUpperTail_of_threshold_packages", "The exact canonical root conditional on both open terminal packages."),
    ("M1080-X-MATHLIB", "bridge", "critical", "Audit the pinned conditional-sub-Gaussian sum theorem as a semantic anchor only, including its StandardBorelSpace and hypothesis mismatches.", "ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF", "A provenance-aware optional bridge that earns no direct root credit."),
    ("M1080-X-SOURCE", "terminal", "high", "Map every root-relevant mathematical node to fixed primary/modern source pinpoints and normalization review.", "node-specific human-source crosswalk", "Human-source coverage only; no machine proof credit."),
    ("M1080-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, axioms, placeholders, unsafe/oracle boundaries, and replay receipts.", "planned machine-derived provenance closure", "Release provenance only; no mathematical proof credit."),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
checked = {"M1080-T-ASSEMBLE"}
machine_overlay = {"M1080-X-MATHLIB": "informational", "M1080-X-SOURCE": "not_applicable", "M1080-X-PROVENANCE": "informational"}
source_na = {"M1080-S-DEFINITIONS", "M1080-S-SCOPE", "M1080-S-FOUNDATION", "M1080-X-PROVENANCE"}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in SPECS:
    fp = ("lean-source:v1:sha256:" + statement_hash if oid == "M1080-ROOT" else
          "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    eligibility = machine_overlay.get(oid, "required")
    exclusion = {"not_applicable": "human_source_overlay_no_machine_credit", "informational": "release_provenance_overlay_no_proof_credit"}.get(eligibility)
    body = "local:Stage1_Instances/THM-M-1080/ObligationTree.lean#azumaUpperTail_of_threshold_packages" if oid in checked else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": eligibility,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body,
    })
    ledger = {
        "premises": "Only the exact incoming proof_requires conclusions and the frozen formal context.",
        "inference": claim,
        "output": output,
        "outgoing_use": "Only declared typed proof, support, or workflow edges may consume this output.",
    }
    nodes.append({
        "node_id": oid, "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "not_applicable" if oid in source_na else "H2",
        "machine_debt": "M0-L" if oid in checked else ("M3" if oid in {"M1080-ROOT", "M1080-X-MATHLIB"} else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if body else ("anchor-audit-mathlib" if oid == "M1080-X-MATHLIB" else "none"),
        "foundation_profile": "lean4-dependent-type-theory/classical-measure-theory-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical experiment, native oracle, or external result closes this node",
        "step_budget": 4, "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1080/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or checked conditional composition only; no open premise is treated as a proof body.",
        "task_ids": [ITEM, "S56-M-1080-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1080/ObligationTree.lean"] if body else [],
        "owner": "THM-M-1080 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if body else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain", "source map"], "revocation_state": "provisional" if body else "open"},
    })

ids = [row["obligation_id"] for row in obligations]
denominators = {
    "inventory": ids,
    "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
    "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
    "required_readable": ids,
    "informational_overlays": ["M1080-X-MATHLIB", "M1080-X-SOURCE", "M1080-X-PROVENANCE"],
}
denominator_hash = digest(denominators)
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; direct exponential-moment architecture and eligibility were selected before proof closure inspection.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1080-ROOT", "denominator_sha256": denominator_hash,
    "frozen_denominators": denominators,
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry v2 plus an append-only old/new ID delta.",
    "eligibility_policy": "The arbitrary-space direct proof obligations remain required regardless of anchor availability; source and provenance overlays cannot earn proof credit.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Architecture only; no Azuma terminal package, root closure, H0, R0, audit completion, or theorem completion is claimed.",
}


def edge(eid, source, typ, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    "M1080-ROOT": ["M1080-T-ASSEMBLE"],
    "M1080-T-ASSEMBLE": ["M1080-T-POSITIVE", "M1080-T-ZERO"],
    "M1080-T-POSITIVE": ["M1080-S-DEFINITIONS", "M1080-S-SCOPE", "M1080-S-BOUNDARY", "M1080-S-FOUNDATION", "M1080-N-TELESCOPE", "M1080-L-MGF-ITERATE", "M1080-L-MARKOV", "M1080-L-OPTIMIZE"],
    "M1080-N-TELESCOPE": ["M1080-N-INCREMENTS"],
    "M1080-C-EXPONENTIAL": ["M1080-N-INCREMENTS"],
    "M1080-L-MGF-ITERATE": ["M1080-C-EXPONENTIAL", "M1080-L-COND-HOEFFDING"],
    "M1080-T-ZERO": ["M1080-S-BOUNDARY"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = f"REQ-{parent}-{child}"
        comp = f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-SCOPE", "M1080-ROOT", "logical_decomposition", "M1080-S-SCOPE"), edge("REF-POS-ZERO", "M1080-ROOT", "logical_decomposition", "M1080-S-BOUNDARY")],
    "provenance": [edge("SRC-ANCHOR", "M1080-X-MATHLIB", "source_map", "M1080-L-COND-HOEFFDING"), edge("PROV-ROOT", "M1080-X-PROVENANCE", "provenance_of", "M1080-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1080-ROOT", "trusts", "M1080-S-FOUNDATION"), edge("TRUST-PROV", "M1080-ROOT", "trusts", "M1080-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE", "M1080-X-SOURCE", "documents", "M1080-ROOT"), edge("DOC-ANCHOR", "M1080-X-SOURCE", "documents", "M1080-X-MATHLIB")],
    "workflow": [edge("FLOW-PROOF-TREE", "M1080-T-ASSEMBLE", "workflow_depends_on", "M1080-T-POSITIVE"), edge("FLOW-PROV", "M1080-X-PROVENANCE", "workflow_depends_on", "M1080-T-ASSEMBLE")],
}
graphs = {}
for name, rows in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in rows:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": rows, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1080/registry-v1", "registry_denominator_sha256": denominator_hash,
    "statement_source_sha256": statement_hash, "anchor_audit_sha256": anchor_hash,
    "root_node_id": "M1080-ROOT",
    "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent; non-proof graphs retain their declared semantics",
    "nodes": nodes, "graphs": graphs,
    "composition_certificates": [{
        "certificate_id": "COMP-M1080-THRESHOLD-V1", "parent": "M1080-T-ASSEMBLE",
        "required_children": ["M1080-T-POSITIVE", "M1080-T-ZERO"],
        "checked_declaration": "Stage1Instances.THM_M_1080.ObligationTree.azumaUpperTail_of_threshold_packages",
        "status": "interface-composition-kernel-checked; both children open",
    }],
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1080-T-POSITIVE", "M1080-T-ZERO"], "reason": "Only conditional threshold recomposition is checked; neither threshold package has a terminal proof body."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({"recipe_id": f"VAL-{oid}", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1080/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1080 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

lines = ["# THM-M-1080 obligation tree", "", "Registry v1 freezes the direct exponential-moment route for the exact arbitrary-space statement. Every mathematical proof leaf remains open; only final conditional recomposition is kernel checked.", ""]
for node in nodes:
    lines.extend([f"## {node['node_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:", f"1. Premises: {node['semantic_step_ledger']['premises']}", f"2. Inference: {node['semantic_step_ledger']['inference']}", f"3. Output: {node['semantic_step_ledger']['output']}", f"4. Outgoing use: {node['semantic_step_ledger']['outgoing_use']}", "", f"Boundary: {node['status_boundary']}", ""])
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"built {len(ids)} obligations and {sum(len(x) for x in graph_edges.values())} typed edges")
print(f"registry denominator sha256: {denominator_hash}")
