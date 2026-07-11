#!/usr/bin/env python3
"""Generate the frozen THM-M-0120 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0120-OBLIGATION_TREE"

# id, kind, human statement, formal target, output, risk, machine debt, budget
SPECS = [
    ("M0120-ROOT", "root", "Prove the exact frozen relative Mori cone and contraction target.", "Stage1Instances.THMM0120.MoriConeTheoremTarget", "the exact canonical theorem", "critical", "M3", 8),
    ("M0120-T", "terminal", "Assemble one indexed ray family and all four conclusion branches into the canonical root.", "MoriConeTheoremTarget from M0120-S, M0120-D, M0120-F, and M0120-C", "the canonical target", "critical", "M3", 12),
    ("M0120-S", "definition", "Preserve every universe, typeclass, geometric hypothesis, and conclusion from the frozen statement.", "MoriConeTheoremTarget and moriConeTheoremTarget_iff_expanded", "an exact statement boundary", "high", "M3", 10),
    ("M0120-S-DATA", "definition", "Realize klt pairs, numerical curve classes, the Mori cone, canonical pairing, and contracted curves without assuming an output.", "ConeTheoremData", "typed input geometry", "critical", "M3", 18),
    ("M0120-S-DEFS", "definition", "Validate generated rays, extremality, the nonnegative part, finite-support sums, and universal contraction definitions.", "ConeTheoremData.IsGeneratedRay; IsExtremalRay; NonnegativePart; InRayDecomposition; IsContractionOf", "typed conclusion vocabulary", "high", "M3", 16),
    ("M0120-S-BOUNDARY", "branch", "Cover empty ray families, dimension zero, and numerically trivial canonical pairing while excluding inputs outside the frozen hypotheses.", "planned boundary lemmas for ConeTheoremData.Conclusion", "complete boundary semantics", "high", "M4", 20),
    ("M0120-S-TRANSPORT", "transport", "Check the compact target against its fully expanded binder form.", "moriConeTheoremTarget_iff_expanded", "checked exact transport", "normal", "M3", 4),
    ("M0120-X", "bridge", "Build the missing characteristic-zero relative birational-geometry infrastructure.", "planned Lean package: relative klt intersection theory", "usable MMP foundations", "critical", "M4", 20),
    ("M0120-X-KLT", "definition", "Define Q-divisors, discrepancies, Q-factoriality, and klt singularities and connect them to the frozen predicates.", "planned Lean signature: RelativeKltPair", "typed klt pair", "critical", "M4", 30),
    ("M0120-X-N1", "construction", "Construct the finite-dimensional relative numerical curve-class space and closed effective cone.", "planned Lean signature: NumericalCurveSpace", "N_1(X/S)_R and NEbar(X/S)", "critical", "M4", 35),
    ("M0120-X-INT", "construction", "Construct the canonical divisor pairing on numerical curve classes and prove numerical invariance.", "planned Lean signature: canonicalPairing", "K_X+Delta intersection functional", "critical", "M4", 30),
    ("M0120-D", "core_lemma", "Produce a countable family of negative extremal rays together with rational generators and the finite-support cone decomposition.", "first two conjuncts of ConeTheoremData.Conclusion", "ray family and cone decomposition", "critical", "M4", 18),
    ("M0120-D-RAYS", "core_lemma", "Prove existence and countability of all relevant canonical-negative extremal rays.", "exists (iota) [Countable iota] (ray : iota -> Set D.N1), forall i, D.IsExtremalRay (ray i)", "indexed extremal rays", "critical", "M4", 35),
    ("M0120-D-NEG", "core_lemma", "Prove strict canonical negativity for every nonzero class on each selected ray.", "forall i z, z in ray i -> z != 0 -> D.canonicalPairing z < 0", "negative rays", "high", "M4", 24),
    ("M0120-D-RAT", "core_lemma", "Produce a rational curve generator on every ray with positive anticanonical degree bounded by twice the relative dimension.", "forall i, exists C, curveClass C in ray i and curveClass C != 0 and 0 < antiCanonicalDegree C and antiCanonicalDegree C <= 2 * relativeDimension", "bounded rational generators", "critical", "M4", 40),
    ("M0120-D-SUM", "core_lemma", "Prove both directions of membership in the nonnegative-part plus finite ray-sum decomposition.", "forall z, z in D.moriCone iff D.InRayDecomposition ray z", "exact cone decomposition", "critical", "M4", 45),
    ("M0120-F", "core_lemma", "Prove local finiteness of negative rays uniformly away from the nonnegative wall.", "forall epsilon > 0, {i | exists z in ray i, norm z = 1 and canonicalPairing z <= -epsilon}.Finite", "epsilon-local finiteness", "critical", "M4", 45),
    ("M0120-F-COMPACT", "bridge", "Reduce local finiteness to a compact normalized slice and the rationality/length estimates.", "planned Lean signature: negativeSlice_finite", "finite normalized ray indices", "critical", "M4", 50),
    ("M0120-C", "construction", "Construct a contraction for every selected negative extremal ray and prove its exact universal property.", "forall i, exists Y g, D.IsContractionOf (ray i) Y g", "ray contractions", "critical", "M4", 24),
    ("M0120-C-EXIST", "construction", "Construct the target scheme and contraction morphism for a fixed negative extremal ray.", "planned Lean signature: contraction_exists", "Y and g : X -> Y", "critical", "M4", 45),
    ("M0120-C-CURVES", "core_lemma", "Prove that the contraction contracts exactly the rational curves whose classes lie on the ray.", "forall C, D.isContracted g C iff D.curveClass C in R", "exact contracted-curve locus", "critical", "M4", 35),
    ("M0120-C-UNIV", "core_lemma", "Prove existence and uniqueness of factorization through the contraction.", "forall Z h, (...) -> exists! q, g >> q = h", "universal factorization", "critical", "M4", 40),
    ("M0120-P", "provenance", "Resolve wrapper, conclusion, imported declaration, and terminal proof-body provenance without duplicate credit.", "planned provenance certificate", "deduplicated proof provenance", "high", "M4", 20),
    ("M0120-V", "certificate", "Audit placeholders, axioms, imports, TCB, computations, node recipes, and child-to-parent composition.", "planned trust and evidence certificate", "accepted validation evidence", "high", "M4", 24),
    ("M0120-R", "documentation", "Pin primary theorem sources and give a reviewed node-by-node readable reconstruction.", "planned source crosswalk and readable proof", "H/R acceptance evidence", "critical", "M4", 30),
]

PROOF = {
    "M0120-ROOT": ["M0120-T"],
    "M0120-T": ["M0120-S", "M0120-D", "M0120-F", "M0120-C", "M0120-P", "M0120-V", "M0120-R"],
    "M0120-S": ["M0120-S-DATA", "M0120-S-DEFS", "M0120-S-BOUNDARY", "M0120-S-TRANSPORT"],
    "M0120-X": ["M0120-X-KLT", "M0120-X-N1", "M0120-X-INT"],
    "M0120-D": ["M0120-X", "M0120-D-RAYS", "M0120-D-NEG", "M0120-D-RAT", "M0120-D-SUM"],
    "M0120-F": ["M0120-F-COMPACT"],
    "M0120-C": ["M0120-C-EXIST", "M0120-C-CURVES", "M0120-C-UNIV"],
}
REFINEMENT = {
    "M0120-D-RAYS": ["M0120-X-KLT", "M0120-X-N1", "M0120-X-INT"],
    "M0120-D-RAT": ["M0120-D-RAYS", "M0120-X-INT"],
    "M0120-D-SUM": ["M0120-D-RAYS", "M0120-D-NEG"],
    "M0120-F-COMPACT": ["M0120-D-RAT", "M0120-D-SUM"],
    "M0120-C-EXIST": ["M0120-X-KLT", "M0120-D-RAYS"],
    "M0120-C-CURVES": ["M0120-C-EXIST"],
    "M0120-C-UNIV": ["M0120-C-EXIST", "M0120-C-CURVES"],
}


def fingerprint(oid, human):
    if oid == "M0120-ROOT":
        statement = json.loads((HERE / "statement.json").read_text())
        return "lean-expression-sha256:" + statement["canonical_formal_target"]["elaborated_expression_sha256"]
    return "planned:v1:sha256:" + hashlib.sha256(human.encode()).hexdigest()


rows, nodes = [], []
for oid, kind, human, formal, output, risk, machine, budget in SPECS:
    rows.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, human), "kind": kind,
        "root_relevant": True, "machine_eligibility": "required", "human_source_eligibility": "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": None,
    })
    nodes.append({
        "node_id": "THM-M-0120-" + oid.removeprefix("M0120-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H2", "machine_debt": machine, "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md; pinpoint mapping pending",
        "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/classical-policy-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-audit-pending", "computation_record": "none",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "the typed children and inputs named by this node",
            "inference": human, "output": output, "outgoing_use": "conditional composition only; no closure credited"},
        "public_readable_target": "Stage1_Instances/THM-M-0120/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture and signature only; no substantive proof body is credited.",
        "task_ids": [ITEM, "S56-M-0120-PROOF"], "owned_sources": [],
        "owner": "THM-M-0120 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,edge,source,toolchain change; revocation=none",
    })

ids = [r["obligation_id"] for r in rows]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-0120",
    "registry_version": 1, "freeze_basis": "Exact statement and bounded immutable anchor audit precede this status-blind eligibility freeze.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0120-ROOT", "frozen_denominators": {"inventory": ids, "required_machine": ids,
        "required_human_source": ids, "required_readable": ids, "informational_overlays": []},
    "denominator_sha256": digest,
    "delta_policy": "Any target, split, merge, eligibility, exclusion, or weight change requires a new version and append-only ID delta.",
    "obligations": rows,
}

graph_specs = {
    "proof": (PROOF, "proof_requires"), "refinement": (REFINEMENT, "logical_decomposition"),
    "provenance": ({"M0120-T": ["M0120-P"], "M0120-P": ["M0120-D", "M0120-F", "M0120-C"]}, "provenance_of"),
    "evidence": ({"M0120-T": ["M0120-V"], "M0120-V": ["M0120-S-TRANSPORT", "M0120-D", "M0120-F", "M0120-C"]}, "evidence_for"),
    "trust": ({"M0120-ROOT": ["M0120-V"], "M0120-V": ["M0120-X", "M0120-P"]}, "trusts"),
    "documentation": ({"M0120-ROOT": ["M0120-R"], "M0120-R": ["M0120-S", "M0120-D", "M0120-F", "M0120-C"]}, "documents"),
    "workflow": ({"M0120-ROOT": ["M0120-T"], "M0120-T": ["M0120-D", "M0120-F", "M0120-C", "M0120-P", "M0120-V", "M0120-R"]}, "workflow_depends_on"),
}
graphs = {}
for name, (adj, typ) in graph_specs.items():
    edges, out, incoming = [], {x: [] for x in ids}, {x: [] for x in ids}
    for parent, children in adj.items():
        for index, child in enumerate(children, 1):
            eid = f"{name.upper()}-{parent}-{index:02d}"
            edge = {"edge_id": eid, "type": typ, "from": parent, "to": child}
            edges.append(edge); out[parent].append(eid); incoming[child].append(eid)
    graphs[name] = {"edges": edges, "out": out, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0120",
    "registry_denominator_sha256": digest, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M0120-X-KLT", "M0120-X-N1", "M0120-X-INT", "M0120-D-RAYS", "M0120-D-RAT", "M0120-D-SUM", "M0120-F-COMPACT", "M0120-C-EXIST", "M0120-C-UNIV"],
        "reason": "The pinned closure contains the statement interface but no klt/numerical-intersection stack or proof bodies for decomposition, local finiteness, or contraction."},
}

recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "planned",
            "command": "node-scoped exact-type, axiom, placeholder, provenance, and composition checks after implementation"}
           for oid in ids]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM,
              "theorem_id": "THM-M-0120", "recipes": recipes}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
(HERE / "validation-specs.json").write_text(json.dumps(validation, indent=2) + "\n")
print(f"wrote {len(rows)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {digest}")
