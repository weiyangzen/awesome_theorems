#!/usr/bin/env python3
"""Build the frozen THM-M-1277 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1277-OBLIGATION_TREE"
THEOREM = "THM-M-1277"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M1277-ROOT", "root", "critical", "The exact endpoint-and-sharpness Statement frozen in Statement.lean.", "Stage1Rev56.THMM1277.Statement", "The selected sharp two-dimensional Moser-Trudinger theorem."),
    ("M1277-S-DEFINITIONS", "definition", "high", "Freeze the plane, selected weak gradient, W_0^{1,2} completion predicate, energy, and exponential integral.", "Stage1Rev56.THMM1277.{Plane,ZeroBoundarySobolev,GradientEnergy,ExponentialIntegral,Admissible}", "The exact canonical interface."),
    ("M1277-S-DOMAIN", "normalization", "high", "Track openness, boundedness, nonemptiness, volume conventions, extended-real integrals, and the selected weak gradient.", "planned exact domain and coercion package", "All analytic lemmas use the canonical domain and measure."),
    ("M1277-S-BOUNDARY", "branch", "high", "Account for the zero function, energy equality, the exact exponent 4*pi, strictly larger exponents, and exclusion of the empty domain.", "planned boundary-case lemmas for Statement", "Every boundary case agrees with the frozen quantifiers."),
    ("M1277-S-FOUNDATION", "certificate", "critical", "Fix classical choice, quotient, measure-theory, TCB, and no-oracle policy for admitted terminal bodies.", "planned transitive axiom and trust report", "An accepted foundation boundary."),
    ("M1277-N-DENSITY", "transport", "critical", "Convert the sequence-based ZeroBoundarySobolev witness into controlled smooth compactly supported approximants and pass estimates to the limit.", "planned checked completion/density transport", "Endpoint estimates for smooth approximants transfer to every Admissible function."),
    ("M1277-N-ZEROEXT", "transport", "critical", "Extend compactly supported functions by zero and identify their gradient energy without boundary terms.", "planned zero-extension theorem", "A whole-plane function with unchanged L2 gradient bound."),
    ("M1277-C-REARRANGE", "construction", "critical", "Construct the symmetric decreasing rearrangement on a disk with the same measure as the bounded domain.", "planned Schwarz rearrangement construction", "A radial decreasing equimeasurable representative."),
    ("M1277-L-EQUIMEAS", "core_lemma", "critical", "Prove equimeasurability preserves the exponential integral, including ENNReal measurability and endpoint exponent.", "planned layer-cake/equimeasurability theorem", "Equality of original and rearranged exponential integrals."),
    ("M1277-L-POLYASZEGO", "core_lemma", "critical", "Prove the Polya-Szego inequality for smooth zero-extended functions in the selected normalization.", "planned Polya-Szego theorem", "Rearrangement does not increase gradient energy."),
    ("M1277-N-RADIAL", "normalization", "high", "Express the radial rearrangement in logarithmic polar coordinates and normalize its energy to at most one.", "planned radial/logarithmic-coordinate transport", "A one-dimensional profile with the correct weighted integral."),
    ("M1277-L-RADIALBOUND", "core_lemma", "critical", "Derive the radial pointwise/control estimate from the one-dimensional derivative energy.", "planned radial lemma at dimension two", "Control of the profile needed at the critical exponent."),
    ("M1277-L-ENDPOINT1D", "core_lemma", "critical", "Prove the critical one-dimensional exponential integral estimate at coefficient 4*pi.", "planned critical one-dimensional Moser estimate", "A finite uniform endpoint constant depending only on the domain measure."),
    ("M1277-T-ENDPOINT-SMOOTH", "terminal", "critical", "Combine rearrangement, Polya-Szego, radial reduction, and the critical estimate for smooth compactly supported functions.", "planned smooth endpoint theorem", "The endpoint bound on the dense smooth class."),
    ("M1277-T-ENDPOINT-COMPLETE", "terminal", "critical", "Pass the smooth endpoint inequality through the frozen W_0^{1,2} completion predicate.", "Stage1Rev56.THMM1277.EndpointBranch", "The endpoint conjunct for every admissible function."),
    ("M1277-C-INBALL", "construction", "high", "Choose a closed positive-radius ball contained in every nonempty open domain.", "planned interior-ball construction", "A region on which a concentrating sequence may be supported."),
    ("M1277-C-MOSERSEQ", "construction", "critical", "Define a logarithmic Moser concentrating sequence supported in the interior ball, with a checked smoothing or completion witness.", "planned explicit Moser sequence", "Admissible candidates indexed by concentration scale."),
    ("M1277-L-MOSERSOBOLEV", "core_lemma", "critical", "Show each concentrating function satisfies the exact ZeroBoundarySobolev predicate.", "planned W_0^{1,2} membership proof", "A valid completion witness and selected weak gradient."),
    ("M1277-L-MOSERENERGY", "computation", "critical", "Compute and normalize the weak-gradient energy of the Moser sequence to at most one.", "planned exact gradient-energy computation", "Admissibility of every sequence member."),
    ("M1277-L-MOSERINTEGRAL", "computation", "critical", "Lower-bound the core exponential integral and prove divergence whenever alpha is strictly greater than 4*pi.", "planned supercritical integral divergence proof", "For every finite C, a sequence member whose integral exceeds C."),
    ("M1277-T-SHARP", "terminal", "critical", "Assemble the interior-ball Moser sequence, membership, energy, and divergence results.", "Stage1Rev56.THMM1277.SharpnessBranch", "The full supercritical-unboundedness conjunct."),
    ("M1277-T-ASSEMBLE", "transport", "high", "Consume the exact endpoint and sharpness conjuncts and recompose Statement.", "Stage1Rev56.THMM1277.statement_of_branches", "The exact frozen root conditional on both analytic branches."),
    ("M1277-X-SOURCE", "terminal", "high", "Map each rearrangement, endpoint, density, and sharpness lemma to a pinpoint reviewed primary-source passage.", "non-machine primary-source crosswalk", "Human-source coverage without proof credit."),
    ("M1277-X-PROVENANCE", "certificate", "critical", "Inventory imports, terminal bodies, axioms, placeholders, TCB, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
checked = {"M1277-S-DEFINITIONS", "M1277-T-ASSEMBLE"}
source_na = {"M1277-S-DEFINITIONS", "M1277-S-DOMAIN", "M1277-S-BOUNDARY", "M1277-S-FOUNDATION", "M1277-X-PROVENANCE"}
machine_special = {"M1277-X-SOURCE": "not_applicable", "M1277-X-PROVENANCE": "informational"}
obligations, nodes = [], []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = ("lean-source:v1:sha256:" + statement_hash) if oid in {"M1277-ROOT", "M1277-S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    body = "local:Stage1_Instances/THM-M-1277/ObligationTree.lean#statement_of_branches" if oid == "M1277-T-ASSEMBLE" else None
    obligations.append({"obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required", "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": body})
    nodes.append({"node_id": "THM-M-1277-" + oid.removeprefix("M1277-"), "obligation_id": oid, "kind": kind, "human_statement": claim, "formal_target": target, "output": output, "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1277-ROOT" else "M4"), "readability_debt": "R3", "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable", "provenance_id": "local-conditional-composition" if body else "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; no numerical experiment or oracle may close this node", "step_budget": 100 if risk == "critical" else 40, "semantic_step_ledger": {"premises": "Only exact incoming proof_requires conclusions and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."}, "public_readable_target": "Stage1_Instances/THM-M-1277/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted analytic premise and no root closure is supplied.", "task_ids": [ITEM, "S56-M-1277-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1277/ObligationTree.lean"] if body else [], "owner": "THM-M-1277 proof lane", "reviewer": "independent Stage1 integration lane", "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"}})

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "The exact statement and negative anchor audit; the classical rearrangement endpoint route and explicit Moser-sequence sharpness route were expanded before closure status was credited.", "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash, "root_obligation_id": "M1277-ROOT", "denominator_sha256": denominator, "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1277-X-PROVENANCE"]}, "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.", "obligations": obligations, "append_only_delta": [], "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"}, "status_boundary": "Scope and denominators only; no endpoint or sharpness proof, source acceptance, audit completion, or theorem completion."}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1277-ROOT": ["M1277-T-ASSEMBLE"],
    "M1277-T-ASSEMBLE": ["M1277-T-ENDPOINT-COMPLETE", "M1277-T-SHARP"],
    "M1277-T-ENDPOINT-COMPLETE": ["M1277-N-DENSITY", "M1277-T-ENDPOINT-SMOOTH"],
    "M1277-T-ENDPOINT-SMOOTH": ["M1277-N-ZEROEXT", "M1277-C-REARRANGE", "M1277-L-EQUIMEAS", "M1277-L-POLYASZEGO", "M1277-N-RADIAL", "M1277-L-RADIALBOUND", "M1277-L-ENDPOINT1D"],
    "M1277-T-SHARP": ["M1277-C-INBALL", "M1277-C-MOSERSEQ", "M1277-L-MOSERSOBOLEV", "M1277-L-MOSERENERGY", "M1277-L-MOSERINTEGRAL"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]
refinement = [edge("REF-ROOT-DEFS", "M1277-ROOT", "logical_decomposition", "M1277-S-DEFINITIONS"), edge("REF-ROOT-DOMAIN", "M1277-ROOT", "logical_decomposition", "M1277-S-DOMAIN"), edge("REF-ROOT-BOUNDARY", "M1277-ROOT", "logical_decomposition", "M1277-S-BOUNDARY"), edge("REF-ROOT-FOUNDATION", "M1277-ROOT", "logical_decomposition", "M1277-S-FOUNDATION")]
graph_edges = {"proof": proof, "refinement": refinement, "provenance": [edge("SRC-ENDPOINT", "M1277-L-ENDPOINT1D", "source_map", "M1277-X-SOURCE"), edge("SRC-SHARP", "M1277-L-MOSERINTEGRAL", "source_map", "M1277-X-SOURCE"), edge("PROV-ROOT", "M1277-X-PROVENANCE", "provenance_of", "M1277-ROOT")], "evidence": [], "trust": [edge("TRUST-FOUND", "M1277-ROOT", "trusts", "M1277-S-FOUNDATION"), edge("TRUST-PROV", "M1277-ROOT", "trusts", "M1277-X-PROVENANCE")], "documentation": [edge("DOC-DEFS", "M1277-S-DEFINITIONS", "documents", "M1277-ROOT"), edge("DOC-SOURCE", "M1277-X-SOURCE", "documents", "M1277-T-ASSEMBLE")], "workflow": [edge("FLOW-ASSEMBLE-END", "M1277-T-ASSEMBLE", "workflow_depends_on", "M1277-T-ENDPOINT-COMPLETE"), edge("FLOW-ASSEMBLE-SHARP", "M1277-T-ASSEMBLE", "workflow_depends_on", "M1277-T-SHARP"), edge("FLOW-PROV-ASSEMBLE", "M1277-X-PROVENANCE", "workflow_depends_on", "M1277-T-ASSEMBLE")]}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-1277-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": "M1277-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1277-T-ENDPOINT-COMPLETE", "M1277-T-SHARP"], "composition_certificates": ["Stage1Rev56.THMM1277.statement_of_branches"], "reason": "Final composition is conditional; neither analytic branch has a proof body."}}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1277/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1277 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
