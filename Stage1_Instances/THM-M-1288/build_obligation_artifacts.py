#!/usr/bin/env python3
"""Build the frozen THM-M-1288 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1288-OBLIGATION_TREE"
THEOREM = "THM-M-1288"
PREFIX = "M1288"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# ID, kind, risk, human claim, planned/checked formal surface, output, budget.
ROWS = [
    ("M1288-ROOT", "root", "critical", "The exact frozen Talenti inequality and least-admissible-constant proposition.", "Stage1Instances.THM_M_1288.TalentiSharpSobolevTarget", "The canonical proposition.", 20),
    ("M1288-S-DEFINITIONS", "definition", "high", "Fix Euclidean space, real integral powers, Sobolev conjugate, gradient, admissibility, and the displayed Gamma-function constant exactly as in Statement.lean.", "Stage1Instances.THM_M_1288.{Space,lpNorm,vectorLpNorm,sobolevConjugate,talentiConstant,IsAdmissibleConstant}", "The exact formal vocabulary used by every proof child.", 30),
    ("M1288-S-DOMAIN", "terminal", "high", "Derive n at least two, positivity of p and n-p, finiteness of the displayed expressions, and handle the zero test function without adding endpoint assumptions.", "planned Lean domain-and-boundary package for 1 < p < (n : Real)", "All domain side conditions required by later transports and computations.", 45),
    ("M1288-S-FOUNDATION", "certificate", "critical", "Freeze the classical logic, choice, quotient, extensionality, TCB, and no-oracle policy for all terminal proof bodies.", "planned transitive axiom and trust report", "Accepted foundation boundary.", 20),
    ("M1288-N-ELPNORM", "transport", "critical", "Transport the frozen real integral-power scalar and vector norms to and from mathlib eLpNorm statements under the exact positivity and integrability hypotheses.", "planned checked lpNorm/vectorLpNorm versus eLpNorm equivalences", "Exact norm equalities or directed inequalities usable in the frozen target.", 70),
    ("M1288-N-GRADIENT", "transport", "critical", "Identify the norm of the total gradient of a smooth scalar map with the operator norm of its Frechet derivative in Euclidean space.", "planned checked gradient/fderiv operator-norm bridge", "The derivative expression required by Sobolev infrastructure.", 65),
    ("M1288-N-REARRANGEMENT", "reduction", "critical", "Replace a compactly supported smooth function by its symmetric decreasing rearrangement, preserving its L^q mass and not increasing its gradient L^p mass.", "planned equimeasurability and Polya-Szego reduction", "A radial nonincreasing representative sufficient for the sharp estimate.", 90),
    ("M1288-N-RADIAL", "reduction", "critical", "Convert the radial Euclidean norm integrals to weighted one-dimensional integrals with the correct sphere-area normalization.", "planned polar-coordinate radial integral reduction", "The exact weighted one-dimensional variational inequality.", 80),
    ("M1288-B-BOUNDARY", "branch", "high", "Separate zero and nonzero test functions and prove the split exhaustive; the zero branch closes directly and the nonzero branch supports normalization.", "planned zero/nonzero function split and recomposition", "Exhaustive branches without division by a zero norm.", 35),
    ("M1288-L-WEIGHTED", "core_lemma", "critical", "Prove the sharp weighted one-dimensional Sobolev inequality produced by radial reduction, including all integration and limit boundary terms.", "planned sharp weighted one-dimensional inequality", "The sharp radial inequality with its beta-integral coefficient.", 100),
    ("M1288-L-GAMMA", "computation", "critical", "Evaluate the beta and sphere-volume factors and prove algebraically that their coefficient equals talentiConstant n p in the frozen normalization.", "planned symbolic Beta/Gamma constant identity", "Literal equality with Stage1Instances.THM_M_1288.talentiConstant.", 85),
    ("M1288-T-ADMISSIBILITY", "terminal", "critical", "Compose domain, encoding, rearrangement, radial, weighted-estimate, and constant computations to prove the displayed constant admissible.", "Stage1Instances.THM_M_1288.TalentiAdmissibilityPackage", "Admissibility at exactly talentiConstant n p.", 55),
    ("M1288-C-EXTREMIZERS", "construction", "critical", "Construct smooth compactly supported approximations to the Aubin-Talenti profile and prove support, smoothness, scaling, and convergence invariants.", "planned compactly-supported extremizing sequence", "Admissible test functions whose norm ratios converge to the displayed constant.", 100),
    ("M1288-L-LOWER-BOUND", "core_lemma", "critical", "Apply every admissible constant to the extremizing sequence and pass to the limit to bound it below by talentiConstant.", "planned least-constant lower-bound theorem", "For every admissible C, talentiConstant n p <= C.", 75),
    ("M1288-T-OPTIMALITY", "terminal", "critical", "Package the extremizing-sequence lower bound with the exact ordered binders and admissibility predicate.", "Stage1Instances.THM_M_1288.TalentiOptimalityPackage", "Least-admissible-constant sharpness.", 30),
    ("M1288-T-ASSEMBLE", "transport", "high", "Compose exact admissibility and optimality packages into the conjunction of the frozen root.", "Stage1Instances.THM_M_1288.talentiSharpSobolevTarget_of_packages", "The exact canonical root conditional on both packages.", 12),
    ("M1288-X-MATHLIB", "bridge", "high", "Audit and, where exact, consume pinned mathlib's non-sharp eLpNorm/fderiv Sobolev family without crediting it for the Talenti constant or optimality.", "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq", "Supporting non-sharp infrastructure only.", 40),
    ("M1288-X-SOURCE", "terminal", "high", "Map every material analytic and constant step to pinpoint reviewed primary-source passages, conventions, and errata results.", "non-machine primary-source node crosswalk", "Human-source coverage without machine proof credit.", 40),
    ("M1288-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, licenses, axioms, trust closure, and replay receipts.", "planned machine-derived provenance closure", "Release provenance overlay without mathematical proof credit.", 35),
]

CHECKED = {"M1288-S-DEFINITIONS", "M1288-T-ASSEMBLE"}
SOURCE_NA = {"M1288-S-DEFINITIONS", "M1288-S-DOMAIN", "M1288-S-FOUNDATION", "M1288-N-ELPNORM", "M1288-N-GRADIENT", "M1288-B-BOUNDARY", "M1288-X-PROVENANCE"}
MACHINE_SPECIAL = {"M1288-X-SOURCE": "not_applicable", "M1288-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output, budget in ROWS:
    fingerprint = ("lean-elaborated-print-sha256:399dca9a18e2ab2e7577ab64e41f7bc79a0b3f20cc5c4fcb3f3d7d9593408126"
                   if oid == "M1288-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = MACHINE_SPECIAL.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    body = ("local:Stage1_Instances/THM-M-1288/ObligationTree.lean#talentiSharpSobolevTarget_of_packages"
            if oid == "M1288-T-ASSEMBLE" else None)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in SOURCE_NA else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body,
    })
    is_checked = oid in CHECKED
    nodes.append({
        "node_id": "THM-M-1288-" + oid.removeprefix(PREFIX + "-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1" if oid == "M1288-X-SOURCE" else "H3",
        "machine_debt": "M0-L" if is_checked else ("M3" if oid in {"M1288-ROOT", "M1288-X-MATHLIB"} else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md; pinpoint-node-map-pending" if oid not in SOURCE_NA else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1288-T-ASSEMBLE" else ("anchor-audit:C02" if oid == "M1288-X-MATHLIB" else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "symbolic kernel proof required; no oracle or floating-point result accepted" if kind == "computation" else "none; no oracle or external computation may close this node",
        "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "The exact incoming proof_requires conclusions and the frozen 1 < p < n context only.",
            "inference": claim,
            "output": output,
            "outgoing_use": "Only declared typed parent edges may consume this conclusion; support edges carry no proof credit.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-1288/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional interface only; no undeclared premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-1288-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1288/ObligationTree.lean"] if oid == "M1288-T-ASSEMBLE" else [],
        "owner": "THM-M-1288 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if is_checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "obligation registry", "source crosswalk", "toolchain"], "revocation_state": "provisional" if is_checked else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus bounded immutable anchor audit; classical rearrangement/radial/extremizing-sequence architecture; eligibility fixed independently of proof availability.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1288-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [x["obligation_id"] for x in obligations if x["machine_eligibility"] == "required"],
        "required_human_source": [x["obligation_id"] for x in obligations if x["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M1288-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(CHECKED), "root_machine_debt": "M3"},
    "status_boundary": "Frozen architecture and denominators only; no Talenti analytic package, H0 source audit, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal is not None:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M1288-ROOT": ["M1288-T-ASSEMBLE"],
    "M1288-T-ASSEMBLE": ["M1288-T-ADMISSIBILITY", "M1288-T-OPTIMALITY"],
    "M1288-T-ADMISSIBILITY": ["M1288-S-DOMAIN", "M1288-N-ELPNORM", "M1288-N-GRADIENT", "M1288-N-REARRANGEMENT", "M1288-N-RADIAL", "M1288-B-BOUNDARY", "M1288-L-WEIGHTED", "M1288-L-GAMMA"],
    "M1288-T-OPTIMALITY": ["M1288-S-DOMAIN", "M1288-L-GAMMA", "M1288-L-LOWER-BOUND"],
    "M1288-L-LOWER-BOUND": ["M1288-C-EXTREMIZERS"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1288-ROOT", "logical_decomposition", "M1288-S-DEFINITIONS"), edge("REF-ROOT-FOUND", "M1288-ROOT", "logical_decomposition", "M1288-S-FOUNDATION")],
    "provenance": [edge("SRC-ANALYTIC", "M1288-L-WEIGHTED", "source_map", "M1288-X-SOURCE"), edge("SRC-CONSTANT", "M1288-L-GAMMA", "source_map", "M1288-X-SOURCE"), edge("PROV-MATHLIB", "M1288-X-MATHLIB", "provenance_of", "M1288-N-ELPNORM"), edge("PROV-ROOT", "M1288-X-PROVENANCE", "provenance_of", "M1288-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1288-ROOT", "trusts", "M1288-S-FOUNDATION"), edge("TRUST-PROV", "M1288-ROOT", "trusts", "M1288-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M1288-S-DEFINITIONS", "documents", "M1288-ROOT"), edge("DOC-SOURCE", "M1288-X-SOURCE", "documents", "M1288-L-WEIGHTED")],
    "workflow": [edge("FLOW-ASSEMBLE-ADM", "M1288-T-ASSEMBLE", "workflow_depends_on", "M1288-T-ADMISSIBILITY"), edge("FLOW-ASSEMBLE-OPT", "M1288-T-ASSEMBLE", "workflow_depends_on", "M1288-T-OPTIMALITY"), edge("FLOW-PROV-ASSEMBLE", "M1288-X-PROVENANCE", "workflow_depends_on", "M1288-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1288-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1288-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": sorted(CHECKED), "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M1288-T-ADMISSIBILITY", "M1288-T-OPTIMALITY"],
        "composition_certificates": ["Stage1Instances.THM_M_1288.talentiSharpSobolevTarget_of_packages"],
        "reason": "Final conjunction composition is checked, but both exact analytic package premises remain open.",
    },
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in ROWS:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1288/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"})

lines = ["# THM-M-1288 frozen obligation tree", "", f"Registry version 1 contains {len(ROWS)} canonical obligations. The denominator digest is `{denominator}`.", "", "Proof edges point from a parent to required children and have reciprocal `composes` edges. Source, provenance, trust, documentation, and workflow graphs carry no proof credit. The exact root remains open.", ""]
for oid, kind, _, claim, target, output, budget in ROWS:
    lines.extend([f"## {oid}", "", f"Kind: `{kind}`. Step budget: `{budget}`.", "", claim, "", f"Formal surface: `{target}`. Output: {output}", "", "Boundary: this frozen node supplies no proof unless its machine evidence and incoming composition edges are accepted.", ""])

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(denominator)
