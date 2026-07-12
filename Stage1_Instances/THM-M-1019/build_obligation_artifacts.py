#!/usr/bin/env python3
"""Generate the frozen THM-M-1019 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1019-OBLIGATION_TREE"
THEOREM = "THM-M-1019"
ROOT_EXPRESSION = "9e3e6807774912fde69809f88fb4928406a4241c5c3df6ff4bbacfe0c92e3d69"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def spec(oid, kind, statement, target, output, ledger, *, risk="normal", body=None):
    return {
        "obligation_id": oid,
        "kind": kind,
        "human_statement": statement,
        "formal_target": target,
        "output": output,
        "ledger": ledger,
        "risk": risk,
        "body": body,
    }


specs = [
    spec("M1019-ROOT", "root", "Two real probability measures with equal characteristic functions are equal.",
         "Stage1Instances.THM_M_1019.Statement", "The exact frozen uniqueness theorem.",
         "Consume the exact terminal wrapper; preserve both probability hypotheses and full function equality; return measure equality.", risk="critical"),
    spec("M1019-S", "definition", "Freeze the statement, foundations, domains, boundary cases, transports, and axiom policy.",
         "Statement/foundation record for Stage1Instances.THM_M_1019.Statement", "An unambiguous formal root and declared policy.",
         "Jointly consume S1-S5; confirm that each statement dimension agrees with the frozen root."),
    spec("M1019-S1", "definition", "Characteristic functions use MeasureTheory.charFun on real Borel measures.",
         "MeasureTheory.charFun : Measure Real -> Real -> Complex", "The notation and definition used by the root.",
         "Read charFun from the pinned import; specialize its domain to Real; bind that definition to the root occurrence.",
         body="mathlib:MeasureTheory.charFun"),
    spec("M1019-S2", "definition", "The quantified objects are measures on Real carrying explicit probability-measure hypotheses.",
         "forall (mu nu : Measure Real), IsProbabilityMeasure mu -> IsProbabilityMeasure nu -> Prop", "The exact domains and typeclass inputs.",
         "Introduce mu and nu as Measure Real; retain each explicit probability hypothesis; derive only the finite-measure instances needed downstream."),
    spec("M1019-S3", "branch", "Atomic and degenerate probability laws, including dirac 0, remain in scope.",
         "No nondegeneracy premise occurs in Stage1Instances.THM_M_1019.Statement", "Boundary coverage without an excluded-law branch.",
         "Inspect the binder list; verify there is no density, moment, support, or non-Dirac premise; pass all probability measures onward."),
    spec("M1019-S4", "transport", "Function equality of charFun is equivalent to equality of all expanded real characteristic integrals.",
         "Stage1Instances.THM_M_1019.statement_iff_integralForm", "Both checked directions between API and integral forms.",
         "Expand charFun_apply_real; convert function equality with funext; preserve frequency quantification over every real t.",
         body="local:Stage1Instances.THM_M_1019.statement_iff_integralForm"),
    spec("M1019-S5", "definition", "The admitted foundation boundary is Lean equality plus the audited classical, quotient, and extensionality principles.",
         "#print axioms MeasureTheory.Measure.ext_of_charFun", "A declared axiom and foundation policy for later trust validation.",
         "Record the reported constants propext, Classical.choice, and Quot.sound; require later transitive trust replay; admit no additional constant."),
    spec("M1019-N", "normalization", "Normalize characteristic-function equality to the integral inner-product character form expected by Fourier uniqueness.",
         "charFun mu = charFun nu -> forall w, integral (innerProbChar w) dmu = integral (innerProbChar w) dnu", "The normalized integral equality.",
         "Consume N1 and N2 in order; output pointwise equality in the upstream integral-character interface.", risk="high"),
    spec("M1019-N1", "normalization", "Turn equality of characteristic functions into pointwise equality at each frequency.",
         "charFun mu = charFun nu -> forall w, charFun mu w = charFun nu w", "Pointwise characteristic-function equality.",
         "Apply function extensional equality in the forward observation direction; retain every real frequency."),
    spec("M1019-N2", "normalization", "Rewrite each real characteristic-function value as an integral of innerProbChar.",
         "MeasureTheory.charFun_eq_integral_innerProbChar", "Equality of the normalized character integrals.",
         "Rewrite both sides with the pinned identity; preserve measure and frequency arguments; hand the equality to L.",
         body="mathlib:MeasureTheory.charFun_eq_integral_innerProbChar"),
    spec("M1019-B", "branch", "The proof route is uniform over all probability measures and introduces no mathematical case split.",
         "Branch analysis for Stage1Instances.THM_M_1019.Statement", "An exhaustive one-route branch classification.",
         "Check the upstream body and local wrapper for match, by_cases, induction, or support splits; classify the sole route as all inputs; retain boundary obligation S3."),
    spec("M1019-C", "construction", "Construct only the finite-measure instances and the real inner-product separation data required by the bridge.",
         "Construction package for Measure.ext_of_charFun specialized to Real", "Well-typed bridge inputs with no new theorem premise.",
         "Consume C1 and C2; expose the derived instances and separation maps to X; introduce no density or moment construction."),
    spec("M1019-C1", "construction", "Each explicit probability-measure hypothesis supplies the corresponding local probability and finite-measure instances.",
         "IsProbabilityMeasure mu -> IsFiniteMeasure mu", "Finite-measure instances for mu and nu.",
         "Install each explicit hypothesis as a local instance; use the pinned instance chain to obtain finiteness; keep the original hypotheses in scope."),
    spec("M1019-C2", "construction", "The real inner-product linear map separates nonzero vectors and has continuous evaluation.",
         "Separation and continuity premises used by ext_of_integral_char_eq with L := inner_l Real", "The two structural premises for Fourier uniqueness.",
         "For nonzero v use inner_self_ne_zero; identify the witness v; use continuous_inner for joint continuity.",
         body="mathlib:RealInnerProductSpace.inner_l+MeasureTheory.continuous_inner"),
    spec("M1019-L", "core_lemma", "Equality of all normalized character integrals determines a finite measure.",
         "MeasureTheory.ext_of_integral_char_eq", "Equality of the two finite measures.",
         "Consume L1-L3 and the normalized equality; apply the subalgebra integral extensionality engine; return exact measure equality.", risk="critical",
         body="mathlib:MeasureTheory.ext_of_integral_char_eq"),
    spec("M1019-L1", "core_lemma", "Finite character polynomials form a point-separating subalgebra.",
         "MeasureTheory.separatesPoints_charPoly", "The separating algebra supplied to measure extensionality.",
         "Use character continuity, nontriviality, and linear-map separation; obtain the point-separating subalgebra premise.", risk="high",
         body="mathlib:MeasureTheory.separatesPoints_charPoly"),
    spec("M1019-L2", "core_lemma", "Integrals of finite character-polynomial sums distribute over the finite support.",
         "MeasureTheory.integral_finset_sum", "A sum of scalar character integrals for each measure.",
         "Represent an algebra element by finite support; prove integrability of every character term; distribute each finite sum under both measures.",
         body="mathlib:MeasureTheory.integral_finset_sum"),
    spec("M1019-L3", "core_lemma", "The normalized equality identifies every term in the two finite sums and hence every algebra integral.",
         "Termwise use of the normalized integral equality", "Equal integrals for every member of charPoly.",
         "Apply finite-sum congruence; factor each scalar coefficient; use the normalized hypothesis at that frequency; return subalgebra integral equality."),
    spec("M1019-X", "bridge", "The pinned mathlib declaration packages normalization, separation, and Fourier uniqueness for characteristic functions.",
         "MeasureTheory.Measure.ext_of_charFun", "The imported equality-of-measures conclusion.",
         "Consume N, C, and L; replay the pinned theorem body boundary; expose its exact conclusion to the terminal wrapper.", risk="critical",
         body="mathlib:MeasureTheory.Measure.ext_of_charFun"),
    spec("M1019-X1", "terminal", "The immutable upstream source and declaration identity match the audited mathlib revision.",
         "mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95, Basic.lean:251-260", "A pinned body-provenance boundary.",
         "Verify revision, tree, source object, file digest, declaration spelling, and body reference against anchor-audit.json."),
    spec("M1019-X2", "terminal", "Transitive declaration, axiom, toolchain, and kernel trust closure remains a later validation obligation.",
         "Trust closure for MeasureTheory.Measure.ext_of_charFun", "An explicit open trust boundary that cannot create proof credit.",
         "Record direct constants and printed axioms; defer transitive environment, kernel, bootstrap, and independent replay checks to validation."),
    spec("M1019-T", "terminal", "Install explicit probability hypotheses as instances and invoke the imported bridge at the exact frozen target.",
         "Stage1Instances.THM_M_1019.AnchorAudit.pinned_mathlib_candidate", "Stage1Instances.THM_M_1019.Statement.",
         "Introduce mu, nu, and three hypotheses; install both probability instances; apply X to the unchanged charFun equality; return mu = nu.", risk="critical",
         body="local:Stage1Instances.THM_M_1019.AnchorAudit.pinned_mathlib_candidate"),
]

ids = [row["obligation_id"] for row in specs]
assert len(ids) == len(set(ids))

obligations = []
nodes = []
for row in specs:
    oid = row["obligation_id"]
    fingerprint = ("lean-expression-sha256:" + ROOT_EXPRESSION) if oid == "M1019-ROOT" else (
        "planned:v1:sha256:" + digest({key: row[key] for key in ("obligation_id", "kind", "human_statement", "formal_target", "output")})
    )
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": row["kind"],
        "root_relevant": True,
        "machine_eligibility": "required",
        "human_source_eligibility": "required",
        "readable_eligibility": "required",
        "risk_class": row["risk"],
        "exclusion_reason": None,
        "terminal_proof_body_id": row["body"],
    })
    anchor = oid.lower().replace("-", "")
    nodes.append({
        "node_id": "THM-M-1019-" + oid.removeprefix("M1019-"),
        "obligation_id": oid,
        "kind": row["kind"],
        "human_statement": row["human_statement"],
        "formal_target": row["formal_target"],
        "output": row["output"],
        "human_debt": "H1",
        "machine_debt": "M3" if oid in {"M1019-X2"} else "M1",
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk" if oid.startswith("M1019-S") else "anchor-audit-source-boundary",
        "provenance_id": row["body"] or "none",
        "foundation_profile": "lean4-dependent-type-theory/policy-audit-pending",
        "tcb_profile": "lean-4.29.0/transitive-closure-pending",
        "computation_record": "none",
        "step_budget": len([part for part in row["ledger"].split(";") if part.strip()]),
        "semantic_step_ledger": row["ledger"],
        "public_readable_target": f"Stage1_Instances/THM-M-1019/obligation-tree.md#{anchor}",
        "validation_spec_id": "VAL-" + oid + "-PENDING",
        "status_boundary": "Architecture only; this freeze assigns no machine closure, source acceptance, readable acceptance, or theorem completion.",
        "task_ids": [ITEM, "S56-M-1019-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1019/obligation-tree.md"],
        "owner": "THM-M-1019 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-body change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "freeze_basis": "Exact elaborated statement and immutable anchor audit, with eligibility assigned independently of candidate closure.",
    "root_obligation_id": "M1019-ROOT",
    "frozen_denominators": {"inventory": ids, "required_machine": ids, "required_human_source": ids, "required_readable": ids, "informational_overlays": []},
    "denominator_sha256": digest(projection),
    "delta_policy": "Any split, merge, target change, or eligibility change requires version 2 and an append-only old/new ID delta.",
    "obligations": obligations,
}

edges = {name: [] for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
def add(graph, eid, source, kind, target):
    edges[graph].append({"edge_id": eid, "from": source, "type": kind, "to": target})

for parent, children in {
    "M1019-ROOT": ["M1019-T"], "M1019-T": ["M1019-X", "M1019-C1"],
    "M1019-X": ["M1019-N", "M1019-C", "M1019-L"],
    "M1019-L": ["M1019-L1", "M1019-L2", "M1019-L3"],
}.items():
    for child in children: add("proof", f"PROOF-{parent}-{child}", parent, "proof_requires", child)
for parent, children in {
    "M1019-ROOT": ["M1019-S", "M1019-B"], "M1019-S": ["M1019-S1", "M1019-S2", "M1019-S3", "M1019-S4", "M1019-S5"],
    "M1019-N": ["M1019-N1", "M1019-N2"], "M1019-C": ["M1019-C1", "M1019-C2"], "M1019-X": ["M1019-X1", "M1019-X2"],
}.items():
    for child in children: add("refinement", f"REF-{parent}-{child}", parent, "logical_decomposition", child)
add("provenance", "PROV-X-X1", "M1019-X", "provenance_of", "M1019-X1")
add("provenance", "PROV-L-X1", "M1019-L", "provenance_of", "M1019-X1")
add("evidence", "EVID-X-X1", "M1019-X1", "evidence_for", "M1019-X")
add("trust", "TRUST-X-X2", "M1019-X", "trusts", "M1019-X2")
add("documentation", "DOC-ROOT-S", "M1019-ROOT", "documents", "M1019-S")
add("workflow", "FLOW-X-T", "M1019-X", "workflow_depends_on", "M1019-T")

graphs = {}
for name, rows in edges.items():
    outgoing, incoming = {}, {}
    for row in rows:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": rows, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_machine_debt": "M1", "remaining_root_cut_set": ["M1019-X2"],
                         "composition_certificates_checked": [], "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(ids)} obligations and {sum(len(rows) for rows in edges.values())} typed edges")
