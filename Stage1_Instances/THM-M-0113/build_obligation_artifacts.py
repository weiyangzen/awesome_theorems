#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent

SPECS = [
    ("M0113-ROOT", "root", "The exact frozen compact-Kahler Hodge decomposition target.", "Stage1Instances.THMM0113.HodgeDecompositionTarget", "the exact target", "critical"),
    ("M0113-S", "definition", "Preserve the frozen universes, domains, instances, hypothesis, and conclusion.", "HodgeDecompositionTarget and hodgeDecompositionTarget_iff_expanded", "an exact statement boundary", "high"),
    ("M0113-S-DATA", "definition", "Realize de Rham cohomology, Hodge pieces, and conjugation without assuming either conclusion.", "HodgeData", "the theorem's typed objects", "high"),
    ("M0113-S-BOUNDARY", "branch", "Include degree zero and every natural bidegree p+q=n, including vanishing pieces.", "Bidegree; HodgeData.Conclusion", "complete boundary coverage", "normal"),
    ("M0113-S-TRANSPORT", "transport", "Check the compact target against its fully expanded binder form.", "hodgeDecompositionTarget_iff_expanded", "checked exact transport", "normal"),
    ("M0113-A", "construction", "Construct the analytic de Rham and Dolbeault complexes on the compact complex manifold.", "planned Lean signature: analytic complex package", "typed analytic complexes", "critical"),
    ("M0113-A-DR", "construction", "Construct smooth complex differential forms, exterior derivative, and de Rham cohomology.", "planned Lean signature: de Rham cohomology realization", "H^n(X; C)", "critical"),
    ("M0113-A-DOL", "construction", "Split complex forms by type and construct dbar/Dolbeault cohomology.", "planned Lean signature: Dolbeault bicomplex realization", "(p,q)-typed complexes", "critical"),
    ("M0113-A-ELL", "bridge", "Develop the elliptic and formal-adjoint infrastructure for the Hodge Laplacians.", "planned Lean signature: elliptic Hodge operator package", "analytic Fredholm/Hodge input", "critical"),
    ("M0113-H", "theorem", "Prove the Hodge theorem identifying cohomology classes with unique harmonic representatives.", "planned Lean signature: harmonic representative equivalence", "cohomology-harmonic equivalence", "critical"),
    ("M0113-H-EXIST", "theorem", "Prove existence of a harmonic representative for every de Rham class.", "planned Lean signature: harmonic representative existence", "harmonic representatives", "critical"),
    ("M0113-H-UNIQUE", "theorem", "Prove uniqueness of the harmonic representative in a cohomology class.", "planned Lean signature: harmonic representative uniqueness", "injective harmonic-class map", "critical"),
    ("M0113-K", "bridge", "Use the Kahler identities to identify the relevant Laplacians and preserve bidegree.", "planned Lean signature: Kahler identities", "type-preserving harmonic theory", "critical"),
    ("M0113-K-ID", "theorem", "Prove the d, dbar, and partial Laplacian identities with the fixed normalization.", "planned Lean signature: Kahler Laplacian identity", "equality of Laplacians", "critical"),
    ("M0113-K-TYPE", "theorem", "Prove that the harmonic projector decomposes by (p,q)-type.", "planned Lean signature: harmonic type decomposition", "bigraded harmonic forms", "critical"),
    ("M0113-D", "theorem", "Transfer the harmonic type decomposition to the internal direct sum of Hodge submodules.", "HodgeData.IsHodgeDirectSum", "iSupIndep plus spanning", "critical"),
    ("M0113-D-INDEP", "theorem", "Prove independence of distinct bidegree Hodge submodules.", "iSupIndep (fun pq => D.piece n pq)", "the independence conjunct", "high"),
    ("M0113-D-SPAN", "theorem", "Prove that the bidegree pieces span all degree-n cohomology.", "iSup (fun pq => D.piece n pq) = top", "the spanning conjunct", "high"),
    ("M0113-C", "theorem", "Establish conjugation symmetry on Hodge pieces.", "HodgeData.HasConjugationSymmetry", "the conjugation conclusion", "critical"),
    ("M0113-C-CHAIN", "construction", "Construct conjugation on forms and prove compatibility with the differential and harmonicity.", "planned Lean signature: conjugation chain equivalence", "conjugation on harmonic representatives", "critical"),
    ("M0113-C-TYPE", "theorem", "Prove that conjugation exchanges form type (p,q) with (q,p).", "planned Lean signature: conjugation type swap", "the bidegree swap", "critical"),
    ("M0113-C-IFF", "theorem", "Use involutivity to strengthen forward preservation to the required membership iff.", "forall x, x in Hpq iff conjugate x in Hqp", "the exact membership equivalence", "high"),
    ("M0113-T", "composition", "Assemble direct-sum and conjugation results in every degree and discharge the exact root.", "HodgeData.Conclusion -> HodgeDecompositionTarget", "the root theorem", "critical"),
    ("M0113-P", "provenance", "Resolve terminal proof bodies, source boundaries, aliases, and shared bodies for every root dependency.", "planned provenance certificate", "deduplicated terminal provenance", "high"),
    ("M0113-V", "certificate", "Audit axioms, placeholders, transitive imports, TCB, computations, and node-scoped evidence.", "planned trust/evidence certificate", "accepted machine evidence", "high"),
    ("M0113-R", "documentation", "Provide primary-source crosswalks and a unique reviewed readable reconstruction.", "planned H0/R0 package", "human-source and readable evidence", "high"),
]

PROOF = {
    "M0113-ROOT": ["M0113-T"],
    "M0113-T": ["M0113-S", "M0113-D", "M0113-C", "M0113-P", "M0113-V", "M0113-R"],
    "M0113-S": ["M0113-S-DATA", "M0113-S-BOUNDARY", "M0113-S-TRANSPORT"],
    "M0113-D": ["M0113-H", "M0113-K", "M0113-D-INDEP", "M0113-D-SPAN"],
    "M0113-H": ["M0113-A", "M0113-H-EXIST", "M0113-H-UNIQUE"],
    "M0113-A": ["M0113-A-DR", "M0113-A-DOL", "M0113-A-ELL"],
    "M0113-K": ["M0113-K-ID", "M0113-K-TYPE"],
    "M0113-C": ["M0113-C-CHAIN", "M0113-C-TYPE", "M0113-C-IFF"],
}

REFINEMENT = {
    "M0113-D-INDEP": ["M0113-K-TYPE"],
    "M0113-D-SPAN": ["M0113-H-EXIST", "M0113-K-TYPE"],
    "M0113-C-IFF": ["M0113-C-CHAIN", "M0113-C-TYPE"],
}


def fingerprint(oid, statement):
    if oid == "M0113-ROOT":
        return "lean-source-sha256:73010040e7a16c02d00bfa95db270e2370440f433e8c3519e5e2ab429cd236dd"
    return "planned:v1:sha256:" + hashlib.sha256(statement.encode()).hexdigest()


rows = []
nodes = []
for oid, kind, human, formal, output, risk in SPECS:
    rows.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, human),
        "kind": kind, "root_relevant": True, "machine_eligibility": "required",
        "human_source_eligibility": "required", "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": None, "terminal_proof_body_id": None,
    })
    children = PROOF.get(oid, []) + REFINEMENT.get(oid, [])
    nodes.append({
        "node_id": "THM-M-0113-" + oid.removeprefix("M0113-"),
        "obligation_id": oid, "kind": kind, "human_statement": human,
        "formal_target": formal, "output": output, "human_debt": "H4",
        "machine_debt": "M4", "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "pending-primary-source-pinpoint",
        "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/policy-audit-pending",
        "tcb_profile": "lean-4.29.0/transitive-closure-pending", "computation_record": "none",
        "step_budget": "split-required" if children else 8,
        "semantic_step_ledger": [{
            "premises": "the exact inputs named by this obligation",
            "inference": human, "output": output,
            "outgoing_use": "conditional parent composition; no closure credited",
        }],
        "public_readable_target": "Stage1_Instances/THM-M-0113/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid + "-PENDING",
        "status_boundary": "Frozen architecture only; the planned signature and proof body remain open.",
        "task_ids": ["S56-M-0113-OBLIGATION_TREE", "S56-M-0113-PROOF"],
        "owned_sources": [], "owner": "THM-M-0113 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,edge,source,toolchain change; revocation=none",
    })

ids = [row["obligation_id"] for row in rows]
projection = [{k: row[k] for k in ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")} for row in rows]
denominator_hash = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0113-OBLIGATION_TREE",
    "theorem_id": "THM-M-0113", "registry_version": 1,
    "freeze_basis": "The exact statement and bounded immutable anchor audit precede this registry. Eligibility and denominators are frozen without assigning proof closure.",
    "root_obligation_id": "M0113-ROOT",
    "frozen_denominators": {"inventory": ids, "required_machine": ids, "required_human_source": ids, "required_readable": ids, "informational_overlays": []},
    "denominator_sha256": denominator_hash,
    "delta_policy": "Any split, merge, eligibility change, exclusion, or target change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows,
}

graph_specs = {
    "proof": (PROOF, "proof_requires"), "refinement": (REFINEMENT, "logical_decomposition"),
    "provenance": ({"M0113-T": ["M0113-P"], "M0113-P": ["M0113-A-DR", "M0113-A-DOL", "M0113-A-ELL", "M0113-K-ID"]}, "provenance_of"),
    "evidence": ({"M0113-T": ["M0113-V"], "M0113-V": ["M0113-S-TRANSPORT", "M0113-D", "M0113-C"]}, "evidence_for"),
    "trust": ({"M0113-ROOT": ["M0113-V"], "M0113-V": ["M0113-P"]}, "trusts"),
    "documentation": ({"M0113-ROOT": ["M0113-R"], "M0113-R": ["M0113-S", "M0113-D", "M0113-C"]}, "documents"),
    "workflow": ({"M0113-ROOT": ["M0113-T"], "M0113-T": ["M0113-P", "M0113-V", "M0113-R"]}, "workflow_depends_on"),
}
graphs = {}
for name, (adj, typ) in graph_specs.items():
    edges, outs, ins = [], {oid: [] for oid in ids}, {oid: [] for oid in ids}
    for parent, children in adj.items():
        for i, child in enumerate(children, 1):
            eid = f"{name.upper()}-{parent}-{i:02d}"
            edge = {"edge_id": eid, "type": typ, "from": parent, "to": child}
            edges.append(edge); outs[parent].append(eid); ins[child].append(eid)
    graphs[name] = {"edges": edges, "out": outs, "in": ins}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0113-OBLIGATION_TREE",
    "theorem_id": "THM-M-0113", "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [], "theorem_complete": False,
        "remaining_root_cut_set": ["M0113-A-DR", "M0113-A-DOL", "M0113-A-ELL", "M0113-K-ID", "M0113-C-CHAIN"],
        "reason": "The pinned environment lacks the analytic cohomology, elliptic Hodge, Kahler-identity, and conjugation chain-level bodies required by the exact root.",
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(rows)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator_hash}")
