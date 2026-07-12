#!/usr/bin/env python3
"""Build the frozen THM-M-1083 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1083-OBLIGATION_TREE"
THEOREM = "THM-M-1083"
ROOT_FP = "lean-expression-sha256:fb7209158513f98f9692a12449560573c5009e1a2366ed34eb8e61f9cae7c58a"


def sha(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


# This route is frozen from the mathematical architecture, before inspecting closure status.
SPECS = [
    ("M1083-ROOT", "root", "critical", "The exact compact-interval real-valued Kolmogorov-Chentsov statement.", "Stage1Instances.THM_M_1083.Statement", "The canonical proposition.", "H1"),
    ("M1083-S-DEFINITIONS", "definition", "high", "Freeze the intrinsic interval, process, fixed-time modification, and HolderWith path interfaces.", "Stage1Instances.THM_M_1083.{TimeInterval,RealProcess,IsModification,HasHolderPath}", "The exact statement vocabulary and coercions.", "not_applicable"),
    ("M1083-S-BOUNDARY", "normalization", "high", "Preserve T>0, alpha>0, beta>0, gamma>0, the strict gamma<beta/alpha endpoint, fixed-time modification, and gamma-dependent path null sets.", "Boundary package for Stage1Instances.THM_M_1083.Statement", "No critical-exponent, continuity-only, simultaneous-modification, or beta-power substitution.", "H1"),
    ("M1083-S-FOUNDATION", "certificate", "critical", "Freeze classical noncomputable measure theory, quotient/extensionality, probability, and no-oracle policy.", "Planned foundation and transitive axiom certificate", "An accepted trust boundary for every terminal body.", "not_applicable"),
    ("M1083-N-KOLMOGOROV", "transport", "critical", "Translate the frozen increment integral into mathlib's Kolmogorov-process condition with p=alpha and q=1+beta.", "Planned checked bridge to ProbabilityTheory.IsKolmogorovProcess", "The exact measurable-pair moment interface without a continuity conclusion.", "H1"),
    ("M1083-N-COVERING", "reduction", "critical", "Prove the intrinsic compact interval has the dimension-one bounded-covering-number estimate required by the continuity engine.", "Planned CoveringNumberBound (Set.univ : Set (TimeInterval T)) 1", "A checked metric entropy witness with dimension d=1.", "H1"),
    ("M1083-B-SCALES", "branch", "high", "Choose a countable geometric scale and prove every sufficiently close pair is controlled by adjacent grid points; include endpoints and exhaust all distances.", "Planned scale partition and recomposition theorem", "An exhaustive multiscale reduction on the compact interval.", "H1"),
    ("M1083-C-NETS", "construction", "high", "Construct finite nets and measurable representative maps at every scale, with cardinality and approximation invariants.", "Planned finite-net construction on TimeInterval T", "Finite measurable approximants compatible across scales.", "H1"),
    ("M1083-L-MARKOV", "core_lemma", "critical", "Convert the increment moment bound into tail estimates on all net edges using Markov's inequality.", "Planned increment tail bound at each finite scale", "Summable probability bounds after the gamma<beta/alpha choice.", "H1"),
    ("M1083-L-BOREL-CANTELLI", "core_lemma", "critical", "Sum the scale-wise bad-event estimates and apply Borel-Cantelli to obtain eventual increment control almost surely.", "Planned first Borel-Cantelli application to multiscale bad events", "Almost-sure eventual control on every registered net edge.", "H1"),
    ("M1083-L-CAUCHY", "core_lemma", "critical", "Show the approximating process values form pointwise Cauchy sequences on a common full-measure set and define their limits.", "Planned Cauchy convergence theorem for net approximants", "A pathwise limit process on the dense net and then all times.", "H1"),
    ("M1083-C-MODIFICATION", "construction", "critical", "Construct one process Y from the multiscale limits and prove X t = Y t almost everywhere for every fixed t.", "Planned Y : RealProcess T Omega with IsModification P X Y", "One fixed-time modification independent of the requested Holder exponent.", "H1"),
    ("M1083-L-HOLDER-NET", "core_lemma", "critical", "Derive the gamma-Holder estimate on the dense net from eventual multiscale increment control.", "Planned Holder estimate on the selected dense net", "A finite random Holder constant for each admissible gamma.", "H1"),
    ("M1083-L-HOLDER-EXTEND", "bridge", "critical", "Extend the dense-net estimate to the complete real-valued path and transport HolderOnWith univ to HolderWith.", "Planned checked dense-extension and Holder transport", "HasHolderPath Y gamma omega on the intrinsic interval.", "H1"),
    ("M1083-T-ONE-GAMMA", "terminal", "critical", "For each fixed 0<gamma<beta/alpha, prove almost every path of the already constructed Y is gamma-Holder.", "forall gamma, 0<gamma -> gamma<beta/alpha -> almost_everywhere HasHolderPath Y gamma", "The per-exponent almost-sure Holder conclusion for one common Y.", "H1"),
    ("M1083-T-MODIFICATION", "terminal", "critical", "Package the fixed-time modification and all admissible Holder conclusions for the same Y.", "exists Y, IsModification P X Y and forall admissible gamma, AE HasHolderPath Y gamma", "The exact existential conclusion of the canonical theorem.", "H1"),
    ("M1083-T-COMPOSE", "terminal", "critical", "Consume the exact hypotheses and the modification package to produce the canonical universally quantified statement.", "Stage1Instances.THM_M_1083.ObligationTree.kolmogorovContinuity_of_engine", "The exact canonical root conditional only on registered children.", "H1"),
    ("M1083-X-EXTERNAL", "bridge", "critical", "Integrate or reconstruct the external exists_modification_holder engine, including version transport and exact specialization.", "ProbabilityTheory.exists_modification_holder at audited immutable provenance", "A repo-local kernel-checked terminal engine, or an explicit blocker.", "H1"),
    ("M1083-X-SOURCE", "terminal", "high", "Map every material node to immutable primary-source pinpoints, assumptions, conventions, and errata review.", "Node-specific human-source crosswalk overlay", "Human-source coverage only; no machine proof credit.", "H1"),
    ("M1083-X-PROVENANCE", "certificate", "critical", "Record proof bodies, wrappers, dependency revisions, imports, axioms, unsafe/oracle checks, and replay receipts.", "Machine-derived provenance and trust overlay", "Release provenance only; no mathematical proof credit.", "not_applicable"),
]

ids = [row[0] for row in SPECS]
machine_overlays = {"M1083-X-EXTERNAL": "informational", "M1083-X-SOURCE": "not_applicable", "M1083-X-PROVENANCE": "informational"}
source_na = {"M1083-S-DEFINITIONS", "M1083-S-FOUNDATION", "M1083-X-PROVENANCE"}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output, hdebt in SPECS:
    machine = machine_overlays.get(oid, "required")
    fingerprint = ROOT_FP if oid == "M1083-ROOT" else "planned:v1:sha256:" + sha([THEOREM, oid, claim, target, output])
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": ({"M1083-X-EXTERNAL": "optional_external_candidate_overlay_no_duplicate_proof_credit", "M1083-X-PROVENANCE": "release_provenance_overlay_no_proof_credit"}.get(oid)
                             if machine == "informational" else ("human_source_overlay_no_machine_credit" if machine == "not_applicable" else None)),
        "terminal_proof_body_id": None,
    })
    ledger = {
        "premises": "Only the exact formal context and incoming proof_requires conclusions.",
        "inference": claim,
        "output": output,
        "outgoing_use": "Only registered typed edges may consume this output; no hidden theorem package is allowed.",
    }
    nodes.append({
        "node_id": "THM-M-1083-" + oid.removeprefix("M1083-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": claim,
        "formal_target": target,
        "output": output,
        "human_debt": hdebt,
        "machine_debt": "M3" if oid in {"M1083-ROOT", "M1083-S-DEFINITIONS", "M1083-T-COMPOSE", "M1083-X-EXTERNAL"} else "M4",
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "node-pinpoint-review-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "external-candidate-unintegrated" if oid == "M1083-X-EXTERNAL" else "none",
        "foundation_profile": "lean4-dependent-type-theory/classical-measure-theory-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or unchecked computation may close this node",
        "step_budget": 100 if risk == "critical" and kind in {"core_lemma", "bridge", "construction"} else 40,
        "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1083/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; this node supplies no accepted root proof.",
        "task_ids": [ITEM, "S56-M-1083-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1083/ObligationTree.lean"] if oid == "M1083-T-COMPOSE" else [],
        "owner": "THM-M-1083 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid == "M1083-T-COMPOSE" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry", "toolchain", "source map"], "revocation_state": "provisional" if oid == "M1083-T-COMPOSE" else "open"},
    })

required_machine = [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"]
denominators = {
    "inventory": ids,
    "required_machine": required_machine,
    "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
    "required_readable": ids,
    "informational_overlays": ["M1083-X-PROVENANCE"],
}
denominator_digest = sha(denominators)
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement, structural mutations, and bounded anchor audit; the multiscale Kolmogorov-Chentsov architecture and eligibility were selected without observing proof closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1083-ROOT",
    "denominator_sha256": denominator_digest,
    "frozen_denominators": denominators,
    "eligibility_policy": "Every semantic node required by the multiscale modification proof is counted regardless of present library availability. Source and provenance overlays cannot earn proof credit.",
    "delta_policy": "Any split, merge, exclusion, statement change, or eligibility change requires a new registry version and append-only old/new ID delta.",
    "exclusions": [
        "Continuity without the strict family of Holder exponents is not the root.",
        "A separately chosen modification for each gamma is not the root.",
        "The optional external theorem overlay is not a second required proof route or proof credit; adopting it requires a new registry delta plus exact specialization, import, and trust closure.",
        "Wrappers, transports, source rows, and presentation splits do not add semantic coverage."
    ],
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": [], "root_machine_debt": "M3"},
    "status_boundary": "The registry freezes scope and denominators only; no obligation or theorem completion is accepted."
}


def graph(name, pairs):
    edges, outgoing, incoming = [], {}, {}
    for i, (src, typ, dst) in enumerate(pairs, 1):
        eid = f"{name.upper()}-{i:03d}"
        edge = {"edge_id": eid, "from": src, "type": typ, "to": dst}
        edges.append(edge)
        outgoing.setdefault(src, []).append(eid)
        incoming.setdefault(dst, []).append(eid)
    return {"edges": edges, "out": outgoing, "in": incoming}


# Direction is prerequisite/child -> consumer/parent in every graph.
proof_pairs = [
    ("M1083-S-DEFINITIONS", "proof_requires", "M1083-T-COMPOSE"),
    ("M1083-S-BOUNDARY", "proof_requires", "M1083-T-COMPOSE"),
    ("M1083-S-FOUNDATION", "proof_requires", "M1083-T-COMPOSE"),
    ("M1083-N-KOLMOGOROV", "proof_requires", "M1083-L-MARKOV"),
    ("M1083-N-COVERING", "proof_requires", "M1083-C-NETS"),
    ("M1083-B-SCALES", "proof_requires", "M1083-C-NETS"),
    ("M1083-C-NETS", "proof_requires", "M1083-L-MARKOV"),
    ("M1083-L-MARKOV", "proof_requires", "M1083-L-BOREL-CANTELLI"),
    ("M1083-L-BOREL-CANTELLI", "proof_requires", "M1083-L-CAUCHY"),
    ("M1083-L-CAUCHY", "proof_requires", "M1083-C-MODIFICATION"),
    ("M1083-C-MODIFICATION", "proof_requires", "M1083-L-HOLDER-NET"),
    ("M1083-L-BOREL-CANTELLI", "proof_requires", "M1083-L-HOLDER-NET"),
    ("M1083-L-HOLDER-NET", "proof_requires", "M1083-L-HOLDER-EXTEND"),
    ("M1083-L-HOLDER-EXTEND", "composes", "M1083-T-ONE-GAMMA"),
    ("M1083-C-MODIFICATION", "proof_requires", "M1083-T-MODIFICATION"),
    ("M1083-T-ONE-GAMMA", "composes", "M1083-T-MODIFICATION"),
    ("M1083-T-MODIFICATION", "composes", "M1083-T-COMPOSE"),
    ("M1083-T-COMPOSE", "composes", "M1083-ROOT"),
]
refinement_pairs = [
    ("M1083-S-DEFINITIONS", "logical_decomposition", "M1083-ROOT"),
    ("M1083-S-BOUNDARY", "logical_decomposition", "M1083-ROOT"),
    ("M1083-S-FOUNDATION", "logical_decomposition", "M1083-ROOT"),
    ("M1083-N-KOLMOGOROV", "logical_decomposition", "M1083-T-MODIFICATION"),
    ("M1083-N-COVERING", "logical_decomposition", "M1083-T-MODIFICATION"),
]
graphs = {
    "proof": graph("proof", proof_pairs),
    "refinement": graph("refinement", refinement_pairs),
    "provenance": graph("provenance", [("M1083-X-PROVENANCE", "provenance_of", x) for x in required_machine] + [("M1083-X-EXTERNAL", "source_map", "M1083-T-MODIFICATION")]),
    "evidence": graph("evidence", []),
    "trust": graph("trust", [("M1083-S-FOUNDATION", "trusts", x) for x in required_machine if x != "M1083-S-FOUNDATION"]),
    "documentation": graph("documentation", [("M1083-X-SOURCE", "documents", x) for x in denominators["required_human_source"]]),
    "workflow": graph("workflow", [("M1083-X-SOURCE", "workflow_depends_on", "M1083-X-PROVENANCE"), ("M1083-X-PROVENANCE", "workflow_depends_on", "M1083-ROOT")]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": "THM-M-1083/obligations-v1",
    "registry_denominator_sha256": denominator_digest,
    "statement_source_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_node_id": "M1083-ROOT",
    "edge_direction": "prerequisite_or_child -> consumer_or_parent",
    "nodes": nodes,
    "graphs": graphs,
    "composition_certificates": [{
        "certificate_id": "COMP-M1083-ROOT-V1",
        "parent": "M1083-ROOT",
        "required_children": ["M1083-T-COMPOSE"],
        "checked_declaration": "Stage1Instances.THM_M_1083.ObligationTree.kolmogorovContinuity_of_engine",
        "status": "conditional-interface-kernel-checked; all mathematical children open"
    }],
    "closure_boundary": {
        "closed_obligations": [],
        "root_closed": False,
        "root_machine_debt": "M3",
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1083-N-COVERING", "M1083-L-MARKOV", "M1083-L-BOREL-CANTELLI", "M1083-L-CAUCHY", "M1083-L-HOLDER-EXTEND"],
        "first_blocker": "No repo-local kernel-checked continuity engine; the known external body uses an unpinned incompatible closure."
    }
}
recipes = {
    "schema_version": "stage1-validation-specs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1083/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]
}

for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / filename).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

lines = ["# THM-M-1083 obligation tree", "", "Registry version 1 freezes the multiscale Kolmogorov-Chentsov route. Every mathematical node remains open; checked composition is conditional only.", ""]
for node in nodes:
    lines += [f"## {node['obligation_id']}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:"]
    lines += [f"- {key}: {value}" for key, value in node["semantic_step_ledger"].items()]
    lines += ["", f"Boundary: {node['status_boundary']}", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines) + "\n")
print(f"built {len(ids)} obligations; denominator sha256 {denominator_digest}")
