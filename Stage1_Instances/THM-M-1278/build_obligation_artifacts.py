#!/usr/bin/env python3
"""Build the frozen THM-M-1278 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1278-OBLIGATION_TREE"
THEOREM = "THM-M-1278"
PREFIX = "M1278"
ROOT_HASH = "a267837ccca68a9ad86620bd4ce7c26c8d56861b57d76d6198ddce94ae671fdb"

specs = [
    ("ROOT", "root", "critical", "The exact normalized Onofri inequality on the encoded unit two-sphere.", "Stage1Instances.THM_M_1278.OnofriInequality", "The exact canonical target."),
    ("S-DEFINITIONS", "definition", "high", "Freeze the sphere, Hausdorff area, smooth ambient representative, tangential gradient, mean, and Dirichlet energy.", "Definitions in Statement.lean and ObligationTree.lean", "The objects occurring in the root have one fixed Lean meaning."),
    ("S-AREA", "lemma", "critical", "Prove that the chosen two-dimensional Hausdorff measure of the unit sphere has total mass 4*pi.", "sphereArea Set.univ = 4 * Real.pi", "The normalization constants describe probability-normalized spherical area."),
    ("S-FINITE", "lemma", "high", "Establish measurability, integrability, finiteness, and positivity needed for all root integrals and logarithms.", "Integrable u sphereArea ∧ Integrable (fun x => Real.exp (u x)) sphereArea ∧ 0 < normalizedExpIntegral u", "Every analytic expression used by the proof obeys its side conditions."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, quotient, extensionality, imported axioms, and the transitive Lean trust boundary.", "Foundation and axiom-report certificate for the terminal declaration", "A checked foundation and TCB profile for every proof body."),
    ("N-SUBTRACT-MEAN", "construction", "high", "Construct the smooth representative v = u - mean(u) without changing the represented tangential derivatives.", "forall u, exists v, forall x, v x = u x - mean u", "A smooth mean-shifted representative."),
    ("N-ZERO-MEAN", "normalization", "critical", "Using the area formula, prove that subtracting mean(u) produces spherical mean zero.", "mean v = 0", "The normalized function satisfies the sharp estimate's hypothesis."),
    ("N-ENERGY", "lemma", "high", "Prove tangential gradients and Dirichlet energy are invariant under the constant mean shift.", "dirichletEnergy v = dirichletEnergy u", "The normalization introduces no energy error."),
    ("N-EXP-SHIFT", "lemma", "critical", "Factor exp(mean u) from the integral and transport through log, discharging positivity and finiteness.", "Real.log (normalizedExpIntegral u) = mean u + Real.log (normalizedExpIntegral v)", "The left side decomposes into the mean plus the zero-mean left side."),
    ("T-SHIFT", "transport", "critical", "Compose construction, zero-mean, energy, and exponential-shift facts into the exact mean-shift transport interface.", "Stage1Instances.THM_M_1278_Obligations.MeanShiftTransport", "A checked transport from arbitrary smooth input to normalized input."),
    ("L-SHARP-ONOFRI", "core_lemma", "critical", "Prove the sharp zero-mean Onofri estimate with coefficient 1/(16*pi) for every encoded smooth sphere function.", "Stage1Instances.THM_M_1278_Obligations.SharpZeroMeanEstimate", "The central sharp analytic inequality."),
    ("L-SOURCE-ROUTE", "bridge", "critical", "Expand the selected primary-source analytic route for the sharp estimate into independently checkable lemmas before proof credit.", "A source-pinpointed derivation of SharpZeroMeanEstimate", "A non-circular proof route for the central analytic inequality."),
    ("T-COMPOSE", "terminal", "critical", "Apply the sharp estimate to the shifted function and rewrite the energy and logarithmic integral.", "Stage1Instances.THM_M_1278_Obligations.compose_root", "The exact root proposition from both required semantic children."),
    ("X-SOURCE", "terminal", "high", "Pinpoint and independently review the human source for every root-relevant analytic step.", "Human-source crosswalk ledger", "H-status evidence only; no machine proof credit."),
    ("X-PROVENANCE", "terminal", "high", "Trace every eventual wrapper to its terminal proof body, imports, revision, license, and axiom report.", "Machine provenance ledger", "Provenance evidence only; no duplicate semantic credit."),
]

ids = [f"{PREFIX}-{suffix}" for suffix, *_ in specs]

def fingerprint(oid, human, formal, output):
    if oid == f"{PREFIX}-ROOT":
        return f"lean-expression-sha256:{ROOT_HASH}"
    body = json.dumps([oid, human, formal, output], ensure_ascii=True, separators=(",", ":"))
    return "planned:v1:sha256:" + hashlib.sha256(body.encode()).hexdigest()

obligations = []
nodes = []
for suffix, kind, risk, human, formal, output in specs:
    oid = f"{PREFIX}-{suffix}"
    overlay = suffix in {"X-SOURCE", "X-PROVENANCE"}
    human_required = suffix not in {"S-DEFINITIONS", "S-FOUNDATION", "X-PROVENANCE"}
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint(oid, human, formal, output),
        "kind": kind,
        "root_relevant": not overlay,
        "machine_eligibility": "informational" if overlay else "required",
        "human_source_eligibility": "required" if human_required else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "SOURCE_OR_PROVENANCE_OVERLAY_NO_PROOF_CREDIT" if overlay else None,
        "terminal_proof_body_id": None,
    })
    composition = suffix in {"ROOT", "T-SHIFT", "T-COMPOSE"}
    ledger = (["Consume every required incoming proof premise.", f"Derive exactly: {output}", "Validate the child-to-parent composition term and its target fingerprint."] if composition else
              ["Freeze the exact context and input interfaces.", f"Establish: {human}", f"Derive exactly: {output}", "Pass the output along the declared typed edge without strengthening the target."])
    nodes.append({
        "node_id": oid, "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H2", "machine_debt": "M3" if suffix in {"S-DEFINITIONS", "T-COMPOSE"} else "M4",
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if not human_required else "pending-pinpoint-primary-source-review",
        "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/policy-audit-open",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-open", "computation_record": "none",
        "step_budget": len(ledger), "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1278/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-OPEN", "status_boundary": "Architecture interface only; no analytic proof body or closure is claimed.",
        "task_ids": [ITEM, "S56-M-1278-PROOF"], "owned_sources": [],
        "owner": "THM-M-1278 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
    })

denominators = {
    "inventory": ids,
    "required_machine": [x["obligation_id"] for x in obligations if x["machine_eligibility"] == "required"],
    "required_human_source": [x["obligation_id"] for x in obligations if x["human_source_eligibility"] == "required"],
    "required_readable": ids,
    "informational_overlays": [f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE"],
}

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1,
    "freeze_basis": "Exact elaborated statement and completed bounded anchor audit; proof availability and closure metrics were ignored while selecting the architecture.",
    "root_obligation_id": f"{PREFIX}-ROOT", "frozen_denominators": denominators,
    "eligibility_policy": "All semantic nodes are required regardless of proof availability. Source and provenance overlays receive no machine proof credit.",
    "mandatory_layer_dispositions": {
        "statement": "represented", "normalization": "represented", "branch": "not_applicable_no_case_split_in_selected_route",
        "construction": "represented", "core_lemma": "represented", "external_and_computational": "represented_as_source_and_provenance_overlays_no_computation_selected",
        "terminal": "represented", "review_status": "pending_independent_master_acceptance"
    },
    "exclusions": [
        "Moser-Trudinger variants on other manifolds, weak constants, and zero-mean-only statements are not the root.",
        "Aliases, wrappers, definitional expansions, and presentation nodes cannot create additional proof credit.",
        "No external Onofri theorem was found, so supporting mathlib geometry declarations are not terminal proof bodies."
    ], "obligations": obligations,
}

proof_pairs = [
    ("T-COMPOSE", "ROOT"), ("T-SHIFT", "T-COMPOSE"), ("L-SHARP-ONOFRI", "T-COMPOSE"),
    ("S-DEFINITIONS", "T-SHIFT"), ("S-AREA", "N-ZERO-MEAN"), ("S-FINITE", "N-EXP-SHIFT"),
    ("N-SUBTRACT-MEAN", "N-ZERO-MEAN"), ("N-SUBTRACT-MEAN", "N-ENERGY"), ("N-SUBTRACT-MEAN", "N-EXP-SHIFT"),
    ("N-ZERO-MEAN", "T-SHIFT"), ("N-ENERGY", "T-SHIFT"), ("N-EXP-SHIFT", "T-SHIFT"),
    ("L-SOURCE-ROUTE", "L-SHARP-ONOFRI"), ("S-FOUNDATION", "T-COMPOSE")
]
refine_pairs = [("S-DEFINITIONS", "ROOT"), ("S-AREA", "ROOT"), ("S-FINITE", "ROOT")]
prov_pairs = [("X-PROVENANCE", s) for s, *_ in specs if s not in {"X-PROVENANCE"}]
evidence_pairs = [("X-SOURCE", "L-SOURCE-ROUTE"), ("X-PROVENANCE", "ROOT"), ("S-DEFINITIONS", "ROOT")]
trust_pairs = [("S-FOUNDATION", "ROOT"), ("X-PROVENANCE", "S-FOUNDATION")]
doc_pairs = [(s, "ROOT") for s, *_ in specs if s != "ROOT"]
workflow_pairs = [("X-SOURCE", "L-SOURCE-ROUTE"), ("L-SOURCE-ROUTE", "L-SHARP-ONOFRI"), ("T-SHIFT", "T-COMPOSE"), ("T-COMPOSE", "ROOT")]

def graph(name, pairs):
    edges, outgoing, incoming = [], {}, {}
    for i, (a, b) in enumerate(pairs, 1):
        eid = f"{name.upper()}-{i:02d}"
        a, b = f"{PREFIX}-{a}", f"{PREFIX}-{b}"
        edges.append({"edge_id": eid, "from": a, "to": b})
        outgoing.setdefault(a, []).append(eid); incoming.setdefault(b, []).append(eid)
    return {"edge_type": {"proof": "proof_requires", "refinement": "logical_decomposition", "provenance": "provenance_of", "evidence": "evidence_for", "trust": "trusts", "documentation": "documents", "workflow": "workflow_depends_on"}[name], "edges": edges, "out": outgoing, "in": incoming}

graphs = {name: graph(name, pairs) for name, pairs in [("proof", proof_pairs), ("refinement", refine_pairs), ("provenance", prov_pairs), ("evidence", evidence_pairs), ("trust", trust_pairs), ("documentation", doc_pairs), ("workflow", workflow_pairs)]}
denom_digest = hashlib.sha256(json.dumps(denominators, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1278-obligations-v1", "registry_denominator_sha256": denom_digest,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "required child or supporting record -> consumer/parent",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": [f"{PREFIX}-L-SHARP-ONOFRI", f"{PREFIX}-S-AREA", f"{PREFIX}-S-FINITE"], "root_machine_debt": "M3"}
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

lines = ["# THM-M-1278 obligation tree", "", "This registry freezes a direct normalized proof architecture. Every analytic node remains open; only the exact composition harness is kernel-checked.", ""]
for node in nodes:
    lines += [f"## {node['node_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:"]
    lines += [f"{i}. {step}" for i, step in enumerate(node["semantic_step_ledger"], 1)] + ["", f"Boundary: {node['status_boundary']}", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))

print(f"built {len(obligations)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denom_digest}")
