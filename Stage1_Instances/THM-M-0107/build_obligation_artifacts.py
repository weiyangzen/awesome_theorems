#!/usr/bin/env python3
"""Build the deterministic THM-M-0107 obligation registry and graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TID = "THM-M-0107"
ITEM = "S56-M-0107-OBLIGATION_TREE"
PREFIX = "M0107"
ROOT_FP = "sha256:1432cea76d1fbb8b70f03874753d551bc28ee05c4b86c738e4085cd6f8923f27"

# This architecture was fixed from the statement and mathematical factorization
# route. Candidate closure is deliberately not an input to this table.
SPECS = [
    ("ROOT", "root", None, "Every locally quasi-finite, locally finite-type, separated, quasi-compact scheme morphism factors as an open immersion followed by a finite morphism.", "Stage1Instances.THM_M_0107.ZariskiMainFactorizationTarget", "The exact frozen existential factorization target.", "critical"),
    ("S", "definition", "ROOT", "Fix the exact statement, contexts, boundary cases, transport direction, and foundation policy.", "Statement.lean statement package", "An immutable, unambiguous root interface.", "critical"),
    ("S-DEFS", "definition", "S", "Fix schemes, morphism composition, and the four morphism-property predicates.", "Scheme; CategoryStruct.Hom; LocallyQuasiFinite; LocallyOfFiniteType; IsSeparated; QuasiCompact; IsOpenImmersion; IsFinite", "Definitions used without changing mathematical meaning.", "high"),
    ("S-CONTEXT", "definition", "S", "Fix universe u, ordered binders, typeclass instances, and composition orientation.", "Statement.lean ordered binders", "The exact Lean context for every later node.", "high"),
    ("S-BOUNDARY", "branch", "S", "Retain empty schemes, isomorphisms, and all degenerate cases admitted by the four stated hypotheses.", "No additional nonempty, reduced, irreducible, normal, or noetherian assumptions", "Boundary-complete theorem scope.", "normal"),
    ("S-TRANSPORT", "transport", "S", "Use the relative-normalization factorization only in the checked direction toward the existential root.", "relativeNormalization_implies_factorization", "A type-correct route that cannot substitute a stronger target silently.", "high"),
    ("S-FOUNDATION", "certificate", "S", "Audit dependent type theory, classical choice, quotient, extensionality, and the pinned TCB policy.", "Lean 4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95", "Declared foundation and trust boundary.", "critical"),
    ("N", "normalization", "ROOT", "Reduce the existential factorization goal to the canonical relative normalization of f.", "Scheme.Hom.normalization, toNormalization, fromNormalization", "A canonical intermediate scheme and two composable maps.", "critical"),
    ("N-OBJECT", "normalization", "N", "Construct f.normalization over Y from the relative spectrum of the integral closure.", "f.normalization", "The selected intermediate scheme Xbar.", "high"),
    ("N-MAPS", "normalization", "N", "Construct the comparison map to normalization and the structural map back to Y.", "f.toNormalization; f.fromNormalization", "Maps j and g with the required types.", "high"),
    ("N-REDUCE", "reduction", "N", "Show open immersion, finiteness, and the composition equation for the normalization maps imply the existential root.", "ObligationTree.root_compose", "A checked exact child-to-root composition.", "critical"),
    ("B", "branch", "ROOT", "Expose the local-to-global proof boundary for the finite-envelope construction rather than hiding it in normalization terminology.", "Planned affine-local cover and global morphism-property recomposition", "An exhaustive local/global route for the finite factor.", "critical"),
    ("B-AFFINE", "branch", "B", "On affine opens of Y, identify the normalization algebra and prove the required finite algebra statement.", "Planned affine localization signature", "Local finiteness of the envelope map.", "critical"),
    ("B-OVERLAP", "core_lemma", "B", "Prove compatibility of the affine constructions and their integral closures on overlaps.", "Planned localization/base-change compatibility signature", "Descent-compatible local finite envelopes.", "critical"),
    ("B-GLOBAL", "terminal", "B", "Recompose the affine-local finite statements into global IsFinite for the envelope map.", "Planned locality-of-IsFinite composition signature", "IsFinite f.fromNormalization or an equivalent finite envelope.", "critical"),
    ("C", "construction", "ROOT", "Construct a finite Y-scheme envelope containing X as an open subscheme.", "Planned finite-envelope construction package", "Witnesses Xbar, j, and g for the root.", "critical"),
    ("C-WELLDEF", "construction", "C", "Prove the relative integral-closure algebra and relative spectrum are well-defined and functorially attached to f.", "Planned relative integral-closure well-definedness signature", "A canonical envelope independent of local presentation choices.", "critical"),
    ("C-COMPARE", "construction", "C", "Define the comparison morphism from X into the envelope and verify compatibility over Y.", "f.toNormalization and its structural compatibility", "The first factor j over Y.", "high"),
    ("C-OPEN", "core_lemma", "C", "Prove the comparison morphism is an open immersion under local quasi-finiteness and separatedness.", "IsOpenImmersion f.toNormalization", "The open-immersion conjunct of the root.", "critical"),
    ("L", "core_lemma", "ROOT", "Establish the two property theorems and the equality that make the constructed factorization valid.", "Planned normalization property package", "All three conjuncts consumed by root composition.", "critical"),
    ("L-OPEN", "core_lemma", "L", "Derive the global open-immersion property from the quasi-finite locus theorem.", "Scheme.Hom.exists_isIso_morphismRestrict_toNormalization plus pinned instance", "IsOpenImmersion f.toNormalization.", "high"),
    ("L-FINITE", "core_lemma", "L", "Prove that the selected envelope map is finite, not merely integral.", "Planned IsFinite envelope theorem", "IsFinite g for the second factor.", "critical"),
    ("L-INTEGRAL-TO-FINITE", "bridge", "L-FINITE", "Bridge the audited integral normalization map to a finite morphism using the required compactness or finite-generation argument.", "Planned integral plus finite-type/quasi-compact to finite bridge", "The missing finiteness result for the normalization candidate.", "critical"),
    ("L-EQUATION", "core_lemma", "L", "Verify that the comparison map followed by the envelope map is exactly f.", "Scheme.Hom.toNormalization_fromNormalization", "j ≫ g = f.", "high"),
    ("X", "bridge", None, "Inventory imported declarations, terminal bodies, automation, and TCB dependencies separately from proof obligations.", "anchor-audit.json", "Auditable external boundaries without semantic coverage inflation.", "high"),
    ("X-ZMT", "bridge", None, "Pin the mathlib quasi-finite-locus theorem and derived open-immersion instance.", "mathlib@8a178386:Scheme.Hom.exists_isIso_morphismRestrict_toNormalization", "Provenance for the open-factor candidate.", "high"),
    ("X-EQUATION", "bridge", None, "Pin the mathlib normalization composition theorem.", "mathlib@8a178386:Scheme.Hom.toNormalization_fromNormalization", "Provenance for the equation candidate.", "normal"),
    ("X-TCB", "certificate", None, "Track kernel, elaborator, dependency pins, axioms, and reproducibility inputs.", "Lean 4.29.0 transitive trust closure", "The later release trust record.", "critical"),
    ("T", "terminal", "ROOT", "Assemble Xbar, j, g and the open, finite, and equation proofs into the exact existential target.", "ObligationTree.root_compose", "The exact canonical root, conditional on every declared premise.", "critical"),
]


def oid(short):
    return f"{PREFIX}-{short}"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


children = {short: [] for short, *_ in SPECS}
for short, _kind, parent, *_rest in SPECS:
    if parent:
        children[parent].append(short)

obligations = []
nodes = []
for short, kind, parent, statement, formal, output, risk in SPECS:
    overlay = short.startswith("X")
    fp = ROOT_FP if short == "ROOT" else "planned:v1:sha256:" + digest({
        "id": oid(short), "kind": kind, "statement": statement,
        "formal_target": formal, "context_parent": oid(parent) if parent else None,
        "output": output,
    })
    body = {
        "X-ZMT": "mathlib@8a178386:Scheme.Hom.exists_isIso_morphismRestrict_toNormalization",
        "X-EQUATION": "mathlib@8a178386:Scheme.Hom.toNormalization_fromNormalization",
    }.get(short)
    obligations.append({
        "obligation_id": oid(short),
        "statement_fingerprint": fp,
        "kind": kind,
        "root_relevant": not overlay,
        "machine_eligibility": "informational" if overlay else "required",
        "human_source_eligibility": "not_applicable" if overlay else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "typed_provenance_or_trust_overlay" if overlay else None,
        "terminal_proof_body_id": body,
    })
    leaf = not children[short]
    ledger = [
        {"premise_ids": [oid(parent)] if parent else [], "inference": "establish the precise named transition", "output": output, "outgoing_use": oid(parent) if parent else "theorem audit or release gate"},
        {"premise_ids": [oid(short)], "inference": "validate the exact typed handoff without strengthening or hidden hypotheses", "output": f"validated handoff of {oid(short)}", "outgoing_use": oid(parent) if parent else "typed provenance/trust boundary"},
    ]
    nodes.append({
        "node_id": f"{TID}-{short}", "obligation_id": oid(short), "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": output,
        "human_debt": "H2" if not overlay else "H1", "machine_debt": "M3",
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source_statement_crosswalk.md" if not overlay else "not-applicable",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-dependent-type-theory/profile-review-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none",
        "step_budget": len(ledger) if leaf else "split-required",
        "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-0107/obligation-tree.md#{oid(short).lower()}",
        "validation_spec_id": f"VAL-{oid(short)}-PENDING",
        "status_boundary": "Architecture and typed interface only; no proof, source, readability, or release acceptance is credited.",
        "task_ids": [ITEM, "S56-M-0107-PROOF"],
        "owned_sources": [], "owner": "THM-M-0107 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,edge,source,toolchain change; revocation=none",
    })

registry_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
                   "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                   "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in registry_fields} for row in obligations]
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": TID, "registry_version": 1,
    "freeze_basis": "The exact statement and its mathematical normalization/finite-envelope architecture. Eligibility is fixed independently of candidate availability or closure status.",
    "root_obligation_id": oid("ROOT"),
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "denominator_sha256": digest(projection),
    "delta_policy": "Any target, split, merge, exclusion, eligibility, or weight change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations,
}

edges = {name: [] for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
for short, _kind, parent, *_rest in SPECS:
    if not parent:
        continue
    graph = "refinement" if parent == "S" else "proof"
    edge_type = "logical_decomposition" if graph == "refinement" else "proof_requires"
    edges[graph].append({"edge_id": f"{graph.upper()}-{parent}-{short}", "from": oid(parent), "type": edge_type, "to": oid(short)})
edges["provenance"] = [
    {"edge_id": "PROV-L-OPEN-ZMT", "from": oid("L-OPEN"), "type": "provenance_of", "to": oid("X-ZMT")},
    {"edge_id": "PROV-L-EQUATION", "from": oid("L-EQUATION"), "type": "provenance_of", "to": oid("X-EQUATION")},
]
edges["evidence"] = [
    {"edge_id": "EVID-ROOT-X", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X")},
]
edges["trust"] = [
    {"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")},
]
edges["documentation"] = [
    {"edge_id": "DOC-ROOT-T", "from": oid("ROOT"), "type": "documents", "to": oid("T")},
]
edges["workflow"] = [
    {"edge_id": "FLOW-TREE-PROOF", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T")},
]

graphs = {}
for name, rows in edges.items():
    outgoing, incoming = {}, {}
    for row in rows:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": rows, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM,
    "theorem_id": TID, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [], "root_machine_debt": "M3",
        "remaining_root_cut_set": [oid("L-FINITE"), oid("L-INTEGRAL-TO-FINITE")],
        "composition_certificates_checked": ["Stage1Instances.THM_M_0107.ObligationTree.root_compose"],
        "theorem_complete": False,
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(v) for v in edges.values())} typed edges")
