#!/usr/bin/env python3
"""Build the deterministic THM-M-0554 rev-5.6 architecture freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0554-OBLIGATION_TREE"
THEOREM = "THM-M-0554"
PREFIX = "M0554-"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def planned(oid, kind, statement, target, output):
    return "planned:v1:sha256:" + digest({
        "obligation_id": oid,
        "kind": kind,
        "human_statement": statement,
        "formal_target": target,
        "output": output,
    })


# id, kind, human statement, formal target, output, risk, source eligibility,
# terminal body candidate, leaf ledger
RAW = [
    ("ROOT", "root", "Every frozen generalized cohomology theory and finite CW input admits the specified cohomological Atiyah-Hirzebruch data.", "Stage1.THM_M_0554.Statement", "The exact closed AHSS proposition.", "critical", "required", None, None),
    ("S-EXACT", "definition", "The root is exactly the explicit Nonempty AtiyahHirzebruchData quantification.", "Stage1.THM_M_0554.statement_iff", "A checked expansion of the canonical target.", "critical", "not_applicable", "local:Stage1.THM_M_0554.statement_iff", ["Use the elaborated Statement definition.", "Unfold StatementShape.", "Return the explicit quantified Nonempty target."]),
    ("S-THEORY", "definition", "Freeze the generalized-cohomology operations, coefficients, suspension, homotopy invariance, exactness, and wedge/representability assumptions.", "Stage1.THM_M_0554.GeneralizedCohomologyTheory", "The complete theory input used by all later constructions.", "high", "required", None, ["Fix C and its category and abelian instances.", "Fix the contravariant graded functors and coefficient objects.", "Record coefficient and suspension isomorphisms.", "Record homotopy, exactness, and wedge/representability hypotheses."]),
    ("S-CW", "definition", "Freeze a finite CW skeletal filtration, its inclusions, total maps, functorial laws, and cell-attachment hypotheses.", "Stage1.THM_M_0554.FiniteCWInput", "The filtered space input with explicit finite/exhaustive/cellular conditions.", "high", "required", None, ["Fix every skeleton and inclusion.", "Check identity and composition laws.", "Check compatibility with the total space.", "Record finite, exhaustive, and attachment hypotheses."]),
    ("S-DATA", "definition", "Freeze every field of the AHSS output record without treating the record as inhabited.", "Stage1.THM_M_0554.AtiyahHirzebruchData", "The exact output interface later constructed.", "critical", "required", None, ["Fix the spectral-sequence and E2 fields.", "Fix generalized cohomology and filtration fields.", "Fix convergence and naturality fields.", "Return only the record type, not an inhabitant."]),
    ("S-FOUNDATION", "certificate", "Audit the logical principles, universes, typeclass instances, and noncomputable boundary used by the construction.", "planned: foundation profile for Stage1.THM_M_0554.Statement", "An accepted foundation profile for every terminal body.", "high", "not_applicable", None, ["Inventory universes and category instances.", "Derive the axiom set from admitted terminal declarations.", "Compare it with the accepted foundation policy.", "Reject undeclared principles."]),
    ("N-SKELETON", "normalization", "Normalize the natural-number skeletal filtration into the integer total-degree indexing used by the spectral sequence.", "planned: Nat skeletal index to Int bidegree normalization", "A coherent filtration indexed for p+q abutment statements.", "high", "required", None, ["Embed skeletal degrees into integers.", "Relate inclusions to the chosen filtration direction.", "Prove compatibility with total degree p+q.", "Expose boundary stages explicitly."]),
    ("N-BIGRADE", "normalization", "Normalize page and bidegree conventions to cohomological differentials of degree (r,1-r).", "planned: cohomological page/bidegree convention", "One convention shared by pages, differentials, E2, and convergence.", "high", "required", None, ["Fix page numbering at r=2.", "Fix source bidegree (p,q).", "Compute target bidegree (p+r,q+1-r).", "Prove compatibility with ComplexShape.up'."]),
    ("N-COEFFICIENT", "normalization", "Normalize E^q(point) and the ordinary/cellular cohomology coefficient convention.", "planned: coefficient q isomorphic to cohomology q at point", "The coefficient object used by the E2 identification.", "high", "required", None, ["Select the recorded point model.", "Apply coefficientIso at q.", "Transport the coefficient system along that isomorphism.", "Record the convention in the E2 target."]),
    ("B-E2", "branch", "Establish the E2-page identification for every integer bidegree.", "forall p q, (spectralSequence.page 2).X (p,q) ≅ ordinaryCohomology p q", "The E2 coefficient-model field.", "critical", "required", None, None),
    ("B-DIFFERENTIAL", "branch", "Establish the cohomological differential bidegree on every page r at least two.", "forall r p q, 2 <= r -> ComplexShape.up' (r,1-r) relates (p,q) and (p+r,q+1-r)", "The pageDifferentialBidegree field.", "high", "required", None, ["Fix r,p,q and the lower-page bound.", "Unfold the up-shape relation.", "Verify both integer coordinates.", "Return the required relation."]),
    ("B-CONVERGENCE", "branch", "Construct the skeletal filtration and identify the stable page with its associated graded objects in total degree p+q.", "forall p q, stablePage p q ≅ associatedGraded p (p+q)", "The abutment and strong-convergence fields.", "critical", "required", None, None),
    ("B-NATURALITY", "branch", "Prove naturality of the construction in maps of spaces compatible with the frozen data.", "planned: naturalityInSpace", "The naturalityInSpace field with its hidden map laws expanded.", "high", "required", None, ["Fix a compatible map of filtered spaces.", "Construct its map on exact couples and pages.", "Prove compatibility with E2 identification.", "Prove compatibility with abutment filtrations."]),
    ("B-RECOMPOSE", "branch", "Recompose the E2, differential, convergence, and naturality branches without dropping any field.", "planned: complete AtiyahHirzebruchData branch recomposition", "All mathematical fields needed by the output record.", "critical", "required", None, None),
    ("C-EXACT-COUPLE", "construction", "Construct the exact couple from cohomology of skeleta and successive filtration pairs.", "planned: skeletal generalized-cohomology exact couple", "An exact couple generating the AHSS.", "critical", "required", "missing:lean4-generalized-cohomology-exact-couple-v1", None),
    ("C-SPECTRAL", "construction", "Derive an E2 cohomological spectral sequence from the skeletal exact couple.", "CategoryTheory.E2CohomologicalSpectralSequence C", "The spectralSequence field with the required page convention.", "critical", "required", "missing:lean4-exact-couple-to-spectral-sequence-v1", None),
    ("C-E2-MODEL", "construction", "Identify the first relevant exact-couple page with cellular cochains and their cohomology.", "planned: page 2 component isomorphic to cellular cohomology with E^q(point)", "The family of e2PageIso witnesses.", "critical", "required", "missing:lean4-ahss-e2-identification-v1", None),
    ("C-FILTRATION", "construction", "Construct the finite skeletal filtration on generalized cohomology of X and its associated graded objects.", "planned: skeletal filtration on (E.cohomology n).obj (op X)", "filtrationStage, associatedGraded, and filtration provenance.", "critical", "required", "missing:lean4-generalized-cohomology-skeletal-filtration-v1", None),
    ("L-CELLULAR", "core_lemma", "Compute relative generalized cohomology of each cell-attachment layer as cellular cochains with coefficient E^q(point).", "planned: relative-cell generalized-cohomology calculation", "The local calculation consumed by the E2 model.", "critical", "required", "missing:lean4-generalized-cohomology-cell-calculation-v1", None),
    ("L-STABILIZATION", "core_lemma", "Use finiteness of the CW filtration to prove pagewise stabilization in every bidegree.", "planned: finite filtration implies spectral-sequence stabilization", "The stablePage objects and stabilization bounds.", "high", "required", "missing:lean4-finite-filtration-stabilization-v1", ["Use finiteCW to obtain a terminal skeletal dimension.", "Show filtration terms outside the finite range vanish or stabilize.", "Bound incoming and outgoing differentials for fixed (p,q).", "Define the stable page at the resulting bound."]),
    ("L-STRONG", "core_lemma", "Prove strong convergence of the bounded skeletal spectral sequence to generalized cohomology of X.", "planned: bounded exhaustive skeletal filtration gives strong convergence", "The strongConvergence and stable-page/graded isomorphism fields.", "critical", "required", "missing:lean4-ahss-strong-convergence-v1", None),
    ("X-SPECTRAL", "bridge", "Cross the pinned mathlib generic spectral-sequence API without mistaking it for an AHSS construction.", "CategoryTheory.E2CohomologicalSpectralSequence C", "Generic page data and bidegree substrate only.", "high", "not_applicable", "mathlib:8a178386:CategoryTheory.E2CohomologicalSpectralSequence", ["Import the pinned spectral-sequence module.", "Check the exact declaration and page field.", "Use it only as the output container.", "Do not credit an AHSS constructor."]),
    ("X-CW", "bridge", "Cross the pinned finite-CW substrate and relate it to the repo-local FiniteCWInput interface.", "planned: RelCWComplex.Finite/skeleton to FiniteCWInput bridge", "A checked bridge from genuine CW data to the frozen skeletal input.", "high", "required", "missing:lean4-cw-to-finitecwinput-bridge-v1", ["Select the pinned CW structure.", "Extract its skeleta and monotone inclusions.", "Prove the FiniteCWInput laws.", "Transport finiteness and attachment facts."]),
    ("X-GENCOH", "bridge", "Supply the missing Lean 4 generalized-cohomology exactness, relative theory, and suspension infrastructure.", "planned: generalized cohomology pair/excision/long-exact-sequence API", "The formal substrate required by the exact-couple and cell calculations.", "critical", "required", "missing:lean4-generalized-cohomology-infrastructure-v1", None),
    ("X-GENCOH-PAIR", "bridge", "Formalize generalized cohomology of pairs and the functorial long exact sequence required by skeletal inclusions.", "planned: generalized cohomology of a TopCat pair with natural long exact sequence", "The exactness maps used to form the skeletal exact couple.", "critical", "required", "missing:lean4-generalized-cohomology-pairs-v1", ["Define the cohomology object of a space pair.", "Construct boundary and inclusion-induced maps.", "Prove consecutive composites vanish.", "Prove exactness at every graded term."]),
    ("X-GENCOH-EXCISION", "bridge", "Formalize excision for the successive CW skeletal pairs.", "planned: generalized-cohomology excision equivalence for cell attachments", "The reduction of relative skeletal terms to wedges of cell pairs.", "critical", "required", "missing:lean4-generalized-cohomology-excision-v1", ["State the admissible subspace and pair hypotheses.", "Construct the excision comparison map.", "Prove it induces an isomorphism in every degree.", "Specialize it to each CW attachment layer."]),
    ("X-GENCOH-WEDGE", "bridge", "Formalize suspension and finite-wedge decomposition for cell pairs with coefficient object E^q(point).", "planned: generalized-cohomology suspension and finite wedge theorem", "The coefficient calculation for a finite wedge of attached cells.", "critical", "required", "missing:lean4-generalized-cohomology-wedge-suspension-v1", ["Identify a cell quotient with a sphere suspension.", "Iterate the suspension isomorphism.", "Apply the finite-wedge axiom or representability consequence.", "Identify the result with copies of E^q(point)."]),
    ("X-SOURCE", "terminal", "Pin primary-source theorem, page, assumptions, coefficient convention, convergence convention, and errata records.", "policy: AHSS primary-source crosswalk", "Reviewed human-source provenance for every material branch.", "high", "required", None, ["Identify an exact primary-source edition and locator.", "Map its hypotheses to the frozen interfaces.", "Map E2, differential, and convergence conventions.", "Record errata and independent review."]),
    ("X-TCB", "terminal", "Inventory terminal bodies, transitive dependencies, axioms, compiled artifacts, and replay tools.", "policy: Lean terminal provenance and TCB closure", "A release-grade trust record for admitted bodies.", "high", "not_applicable", None, ["Resolve each wrapper to its terminal body.", "Hash the transitive declaration closure.", "Record the exact axiom and computation profile.", "Bind all executables and artifacts to the TCB record."]),
    ("T-DATA", "terminal", "Assemble every checked field into an AtiyahHirzebruchData value.", "planned: AtiyahHirzebruchData C E X K", "One complete data record for fixed C,E,X,K.", "critical", "required", None, None),
    ("T-INHABIT", "terminal", "Package the complete data record as the required Nonempty witness.", "Stage1.THM_M_0554.StatementShape C E X K", "Nonempty (AtiyahHirzebruchData C E X K).", "critical", "required", None, ["Fix C,E,X,K from the root binders.", "Consume the assembled data value.", "Apply Nonempty.intro.", "Return the exact StatementShape target."]),
    ("T-ROOT", "terminal", "Abstract over all frozen binders and transport the StatementShape witness through statement_iff.", "Stage1.THM_M_0554.Statement", "The exact canonical root, with no broadened or substituted theorem.", "critical", "required", None, ["Introduce C and its typeclass instances.", "Introduce E,X,K.", "Apply the StatementShape inhabitance result.", "Close the exact quantified root."]),
]


CHILDREN = {
    "ROOT": ["S-EXACT", "S-FOUNDATION", "T-ROOT"],
    "S-EXACT": ["S-THEORY", "S-CW", "S-DATA", "N-SKELETON", "N-BIGRADE", "N-COEFFICIENT"],
    "T-ROOT": ["T-INHABIT"],
    "T-INHABIT": ["T-DATA"],
    "T-DATA": ["B-RECOMPOSE"],
    "B-RECOMPOSE": ["B-E2", "B-DIFFERENTIAL", "B-CONVERGENCE", "B-NATURALITY"],
    "B-E2": ["C-E2-MODEL"],
    "B-DIFFERENTIAL": ["C-SPECTRAL"],
    "B-CONVERGENCE": ["C-FILTRATION", "L-STABILIZATION", "L-STRONG"],
    "B-NATURALITY": ["C-EXACT-COUPLE", "C-FILTRATION"],
    "C-E2-MODEL": ["C-SPECTRAL", "L-CELLULAR", "N-COEFFICIENT"],
    "C-SPECTRAL": ["C-EXACT-COUPLE", "X-SPECTRAL"],
    "C-EXACT-COUPLE": ["X-GENCOH", "X-CW", "N-SKELETON"],
    "C-FILTRATION": ["X-GENCOH", "X-CW", "N-SKELETON"],
    "L-CELLULAR": ["X-GENCOH", "X-CW"],
    "L-STRONG": ["L-STABILIZATION", "C-FILTRATION"],
    "X-GENCOH": ["X-GENCOH-PAIR", "X-GENCOH-EXCISION", "X-GENCOH-WEDGE"],
}


rows = []
nodes = []
for short, kind, statement, target, output, risk, human_eligibility, body, ledger in RAW:
    oid = PREFIX + short
    machine = "informational" if short in {"X-SOURCE", "X-TCB"} else "required"
    root_relevant = machine == "required"
    fp = (
        "lean-source-sha256:8bd29893b87ad6991854c311ef1e80cab11f1fc0d6b63ab82e3bfeb1c5f89970"
        if short in {"ROOT", "S-EXACT"} else planned(oid, kind, statement, target, output)
    )
    rows.append({
        "obligation_id": oid,
        "statement_fingerprint": fp,
        "kind": kind,
        "root_relevant": root_relevant,
        "machine_eligibility": machine,
        "human_source_eligibility": human_eligibility,
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "typed_source_or_trust_overlay" if not root_relevant else None,
        "terminal_proof_body_id": body,
    })
    nonleaf = short in CHILDREN
    nodes.append({
        "node_id": THEOREM + "-" + short,
        "obligation_id": oid,
        "kind": kind,
        "human_statement": statement,
        "formal_target": target,
        "output": output,
        "human_debt": "H3",
        "machine_debt": "M4",
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md" if human_eligibility == "required" else "not-applicable",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-mathlib/noncomputable-policy-pending-v1",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending-v1",
        "computation_record": "none",
        "step_budget": "split-required" if nonleaf else len(ledger or []),
        "semantic_step_ledger": ({"children": [PREFIX + child for child in CHILDREN[short]], "output": output} if nonleaf else {"steps": ledger}),
        "public_readable_target": f"Stage1_Instances/THM-M-0554/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture only; this node has no accepted proof, source review, composition certificate, or closure credit.",
        "task_ids": [ITEM, "S56-M-0554-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0554/Statement.lean"] if short in {"ROOT", "S-EXACT", "S-THEORY", "S-CW", "S-DATA"} else [],
        "owner": "THM-M-0554 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen=2026-07-12; review_due=before-proof-acceptance; invalidated_by=statement,registry,source,toolchain,dependency change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{field: row[field] for field in fields} for row in rows]
denominator = digest(projection)
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated exact target and immutable anchor audit determine the mandatory S/N/B/C/L/X/T layers; eligibility was assigned by semantic role without proof-status credit.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": PREFIX + "ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [row["obligation_id"] for row in rows],
        "required_machine": [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"],
        "required_readable": [row["obligation_id"] for row in rows if row["readable_eligibility"] == "required"],
        "informational_overlays": [row["obligation_id"] for row in rows if row["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any target correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows,
}


def indexed(edges):
    outgoing, incoming = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


proof = []
for parent, children in CHILDREN.items():
    for child in children:
        p, c = PREFIX + parent, PREFIX + child
        req = f"PROOF-{parent}-{child}-REQ"
        comp = f"PROOF-{child}-{parent}-COMP"
        proof.extend([
            {"edge_id": req, "from": p, "type": "proof_requires", "to": c, "reciprocal_edge_id": comp},
            {"edge_id": comp, "from": c, "type": "composes", "to": p, "reciprocal_edge_id": req},
        ])

graph_edges = {
    "proof": proof,
    "refinement": [
        {"edge_id": "REF-ROOT-S-EXACT", "from": PREFIX + "ROOT", "type": "logical_decomposition", "to": PREFIX + "S-EXACT"},
        {"edge_id": "REF-DATA-BRANCHES", "from": PREFIX + "S-DATA", "type": "logical_decomposition", "to": PREFIX + "B-RECOMPOSE"},
    ],
    "provenance": [
        {"edge_id": "PROV-SPECTRAL-MATHLIB", "from": PREFIX + "C-SPECTRAL", "type": "provenance_of", "to": PREFIX + "X-SPECTRAL"},
        {"edge_id": "PROV-ROOT-SOURCE", "from": PREFIX + "ROOT", "type": "source_map", "to": PREFIX + "X-SOURCE"},
    ],
    "evidence": [{"edge_id": "EVID-ROOT-TCB", "from": PREFIX + "X-TCB", "type": "evidence_for", "to": PREFIX + "ROOT"}],
    "trust": [{"edge_id": "TRUST-ROOT-TCB", "from": PREFIX + "ROOT", "type": "trusts", "to": PREFIX + "X-TCB"}],
    "documentation": [{"edge_id": "DOC-ROOT-SOURCE", "from": PREFIX + "ROOT", "type": "documents", "to": PREFIX + "X-SOURCE"}],
    "workflow": [
        {"edge_id": "FLOW-SOURCE-TREE", "from": PREFIX + "X-SOURCE", "type": "workflow_depends_on", "to": PREFIX + "ROOT"},
        {"edge_id": "FLOW-TREE-TERMINAL", "from": PREFIX + "ROOT", "type": "workflow_depends_on", "to": PREFIX + "T-ROOT"},
    ],
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_denominator_sha256": denominator,
    "nodes": nodes,
    "graphs": {name: indexed(edges) for name, edges in graph_edges.items()},
    "closure_boundary": {
        "closed_obligations": [],
        "root_machine_debt": "M4",
        "root_closed": False,
        "remaining_root_cut_set": [PREFIX + "X-GENCOH", PREFIX + "C-EXACT-COUPLE", PREFIX + "C-E2-MODEL", PREFIX + "L-STRONG"],
        "composition_certificates_checked": [],
        "audit_complete": False,
        "theorem_complete": False,
    },
}
specs = {
    "schema_version": "stage1-validation-specs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "recipes": [{
        "recipe_id": "VAL-" + row["obligation_id"],
        "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-0554/check_obligation_tree.py"],
        "env": {},
        "timeout_seconds": 30,
        "network": "forbidden",
        "covered_ids": [row["obligation_id"]],
    } for row in rows],
}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(f"wrote {len(rows)} obligations and {sum(len(x) for x in graph_edges.values())} typed edges")
