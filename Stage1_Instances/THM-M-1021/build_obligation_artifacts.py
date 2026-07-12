#!/usr/bin/env python3
"""Build the frozen rev-5.6 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1021-OBLIGATION_TREE"
THEOREM = "THM-M-1021"
ROOT_HASH = "5b397ee9de0936db2c62ba953794ee0c2b9dc3192370aa06825fdf4aafc8322b"


def spec(identifier, kind, title, target, output, risk="normal", children=(), body=None,
         root_relevant=True, machine="required", human="required"):
    return {
        "id": identifier, "kind": kind, "title": title, "target": target,
        "output": output, "risk": risk, "children": list(children), "body": body,
        "root_relevant": root_relevant, "machine": machine, "human": human,
    }


# This is a proof architecture, not a claim that any listed implication is closed.
SPECS = [
    spec("M1021-ROOT", "root", "Exact Bochner characteristic-function equivalence on Real",
         "AwesomeTheorems.Stage1.THM_M_1021.BochnerTarget phi",
         "The frozen biconditional for every phi : Real -> Complex.", "critical",
         ("M1021-S", "M1021-N", "M1021-B", "M1021-C", "M1021-L", "M1021-T")),
    spec("M1021-S", "definition", "Statement and foundation package",
         "Exact definitions, domains, boundaries, transports, and logical policy",
         "An unambiguous proposition and admissible foundation context.", "high",
         ("M1021-S1", "M1021-S2", "M1021-S3", "M1021-S4", "M1021-S5")),
    spec("M1021-S1", "definition", "Positive-definite quadratic-form predicate",
         "IsPositiveDefinite phi",
         "Reality and nonnegativity of every finite Hermitian quadratic sum.", body="BochnerStatement.lean:IsPositiveDefinite"),
    spec("M1021-S2", "definition", "Characteristic-function representation predicate",
         "IsCharacteristicFunction phi",
         "Existence of a Borel probability measure with the fixed positive-sign exponential transform.", body="BochnerStatement.lean:IsCharacteristicFunction"),
    spec("M1021-S3", "branch", "Boundary and degenerate inputs",
         "Fin 0, Fin 1, s = 0, zero coefficients, and probability mass boundaries",
         "All vacuous and normalization cases are explicitly accounted for.", "high",
         ("M1021-S3.1", "M1021-S3.2", "M1021-S3.3")),
    spec("M1021-S3.1", "terminal", "Empty and zero coefficient families",
         "The n = 0 and c = 0 instances of IsPositiveDefinite",
         "The quadratic sum is zero and has nonnegative real witness zero."),
    spec("M1021-S3.2", "terminal", "Singleton diagonal family",
         "The n = 1 instance together with phi 0 = 1",
         "The normalized diagonal quadratic form is |c 0|^2."),
    spec("M1021-S3.3", "terminal", "Zero-frequency transform and total mass",
         "integral mu (fun _ => exp (I * 0 * x)) = 1",
         "Probability normalization yields the value at zero."),
    spec("M1021-S4", "transport", "Mathlib characteristic-function convention transport",
         "Explicit integral encoding compared with MeasureTheory.charFun mu",
         "Checked equality after scalar multiplication and inner-product normalization.", "high"),
    spec("M1021-S5", "definition", "Foundation and trust policy",
         "Classical Lean logic, measure extensionality, Bochner integration, and no computational oracle",
         "A versioned admissible-principle boundary for later axiom inspection.", "high"),
    spec("M1021-N", "normalization", "Analytic normalization package",
         "Normalize quadratic sums, transform convention, and finite-family presentations",
         "Canonical forms usable by both theorem directions.", "high",
         ("M1021-N1", "M1021-N2", "M1021-N3", "M1021-N4")),
    spec("M1021-N1", "normalization", "Hermitian symmetry and real-valued quadratic sums",
         "phi (-t) = conj (phi t) and star symmetry of the finite sum",
         "The complex quadratic form is identified with a real scalar.", "high",
         ("M1021-N1.1", "M1021-N1.2")),
    spec("M1021-N1.1", "core_lemma", "Conjugate symmetry from positive definiteness",
         "IsPositiveDefinite phi -> forall t, phi (-t) = star (phi t)",
         "Hermitian symmetry of phi."),
    spec("M1021-N1.2", "core_lemma", "Quadratic-form reality",
         "Hermitian symmetry -> star Q = Q for the finite quadratic form Q",
         "A real witness can be recovered from the complex sum."),
    spec("M1021-N2", "transport", "Fourier sign and factor ordering",
         "exp (I*s*x), exp (x*s*I), and the negative-sign convention",
         "Directional checked transports without silently changing the root.", "high"),
    spec("M1021-N3", "transport", "Finite-index and finitely-supported encodings",
         "Fin n families compared with finitely supported functions and finite measures",
         "Equivalent positive-definiteness test families.", "high"),
    spec("M1021-N4", "normalization", "Continuity regularity package",
         "Continuous phi compared with continuity at zero under positive definiteness",
         "The canonical global-continuity premise, with any weaker encoding used only through a proved transport.", "high"),
    spec("M1021-B", "branch", "Two-direction split and exhaustive merge",
         "IsCharacteristicFunction phi <-> Continuous phi /\\ phi 0 = 1 /\\ IsPositiveDefinite phi",
         "Forward and reverse implications with no omitted direction.", "critical",
         ("M1021-BF", "M1021-BR", "M1021-BM")),
    spec("M1021-BF", "branch", "Forward representation direction",
         "IsCharacteristicFunction phi -> Continuous phi /\\ phi 0 = 1 /\\ IsPositiveDefinite phi",
         "All three analytic properties of a probability characteristic function.", "high"),
    spec("M1021-BR", "branch", "Reverse Bochner direction",
         "Continuous phi -> phi 0 = 1 -> IsPositiveDefinite phi -> IsCharacteristicFunction phi",
         "Existence of the representing probability measure.", "critical"),
    spec("M1021-BM", "terminal", "Directional recomposition",
         "Forward implication -> reverse implication -> BochnerTarget phi",
         "The exact canonical biconditional.", "high"),
    spec("M1021-C", "construction", "Representing-measure construction package",
         "Construct a positive Radon measure from the normalized positive-definite function",
         "A Borel probability measure whose transform is phi.", "critical",
         ("M1021-C1", "M1021-C2", "M1021-C3", "M1021-C4", "M1021-C5")),
    spec("M1021-C1", "construction", "Dense test-function transform algebra",
         "A Fourier-transform test algebra on Real suitable for defining a functional from phi",
         "A well-defined linear test space and transform map.", "high",
         ("M1021-C1.1", "M1021-C1.2")),
    spec("M1021-C1.1", "definition", "Test algebra operations",
         "Addition, scalar multiplication, conjugation, translation, and convolution on the selected test class",
         "An algebra closed under the operations used in positivity."),
    spec("M1021-C1.2", "transport", "Fourier transform compatibility",
         "Transform laws for convolution, involution, and translation",
         "Algebra operations correspond to pointwise operations required by phi."),
    spec("M1021-C2", "construction", "Positive linear functional induced by phi",
         "Define Lambda_phi on the test algebra and prove positivity",
         "A well-defined positive linear functional.", "critical",
         ("M1021-C2.1", "M1021-C2.2")),
    spec("M1021-C2.1", "core_lemma", "Well-definedness of Lambda_phi",
         "Equal test-function representations give equal functional values",
         "The functional is independent of representation choices.", "high"),
    spec("M1021-C2.2", "core_lemma", "Functional positivity",
         "0 <= Lambda_phi (star f * f)",
         "Positive definiteness transfers from finite sums to the test algebra.", "critical"),
    spec("M1021-C3", "construction", "Riesz-Markov representation boundary",
         "A positive functional on the selected test space is integration against a Radon measure",
         "Existence of a Borel measure mu representing Lambda_phi.", "critical",
         ("M1021-C3.1", "M1021-C3.2")),
    spec("M1021-C3.1", "bridge", "Functional continuity and boundedness",
         "Lambda_phi satisfies the boundedness hypothesis of the representation theorem",
         "The precise continuity premise required by Riesz-Markov.", "high"),
    spec("M1021-C3.2", "bridge", "Riesz-Markov theorem application",
         "Apply a pinned exact representation theorem to Lambda_phi",
         "A regular Borel measure and equality on the full selected test class.", "critical"),
    spec("M1021-C4", "core_lemma", "Mass normalization of the constructed measure",
         "phi 0 = 1 -> IsProbabilityMeasure mu",
         "The representing measure has total mass one.", "high"),
    spec("M1021-C5", "core_lemma", "Pointwise transform recovery",
         "forall s, phi s = integral mu (fun x => exp (I*s*x))",
         "The constructed measure represents phi at every frequency.", "critical",
         ("M1021-C5.1", "M1021-C5.2")),
    spec("M1021-C5.1", "core_lemma", "Approximation of exponential characters",
         "Approximate each character x |-> exp (I*s*x) by the selected test class",
         "A convergence family compatible with Lambda_phi and integration.", "high"),
    spec("M1021-C5.2", "core_lemma", "Passage to the character limit",
         "Continuity of phi and measure convergence identify the limiting values",
         "Exact pointwise transform identity.", "critical"),
    spec("M1021-L", "core_lemma", "Forward analytic engine",
         "Derive continuity, normalization, and positive definiteness from a probability measure",
         "The complete forward implication.", "high",
         ("M1021-L1", "M1021-L2", "M1021-L3")),
    spec("M1021-L1", "bridge", "Continuity of the characteristic function",
         "IsProbabilityMeasure mu -> Continuous (explicitCharFun mu)",
         "Continuity by dominated convergence or the audited mathlib declaration.", "high", body="mathlib:MeasureTheory.continuous_charFun"),
    spec("M1021-L2", "core_lemma", "Characteristic function at zero",
         "IsProbabilityMeasure mu -> explicitCharFun mu 0 = 1",
         "Normalization of the transform.", body="mathlib:MeasureTheory.charFun_zero"),
    spec("M1021-L3", "core_lemma", "Integral square-norm positivity",
         "The finite quadratic sum equals integral mu (fun x => normSq (sum j, c j * exp (I*t j*x)))",
         "Positive definiteness of every probability characteristic function.", "high",
         ("M1021-L3.1", "M1021-L3.2")),
    spec("M1021-L3.1", "core_lemma", "Expand the finite squared modulus",
         "Expand star(sum_j ...) * sum_k ... and interchange finite sums with the integral",
         "Equality between the quadratic sum and an integral of a pointwise square."),
    spec("M1021-L3.2", "terminal", "Nonnegativity of the square integral",
         "0 <= integral mu (fun x => normSq (...))",
         "A nonnegative real witness for IsPositiveDefinite."),
    spec("M1021-T", "terminal", "Terminal composition and trust report",
         "Compose both directions, transport to the frozen target, and inspect trust closure",
         "The exact root only after all child certificates and trust gates close.", "critical",
         ("M1021-T1", "M1021-T2", "M1021-T3", "M1021-T4")),
    spec("M1021-T1", "terminal", "Forward composition certificate",
         "Consume S4, L1, L2, and L3 to yield M1021-BF",
         "Checked exact forward implication.", "high"),
    spec("M1021-T2", "terminal", "Reverse composition certificate",
         "Consume normalization and C1-C5 to yield M1021-BR",
         "Checked exact reverse implication.", "critical"),
    spec("M1021-T3", "terminal", "Root biconditional certificate",
         "Consume M1021-BF and M1021-BR to yield BochnerTarget phi",
         "Checked exact canonical root.", "critical"),
    spec("M1021-T4", "terminal", "Root axiom and terminal-body report",
         "Machine-derived axiom, declaration dependency, and proof-body provenance closure",
         "Accepted foundation/TCB report for the exact terminal declaration.", "critical"),
    # Informational overlays are deliberately outside mathematical denominators.
    spec("M1021-X", "bridge", "External and trusted boundary inventory",
         "Pinned mathlib candidates, kernel, imports, and future representation-theorem body",
         "Separated provenance and trust records that cannot discharge a proof premise.", "critical",
         ("M1021-X1", "M1021-X2", "M1021-X3"), root_relevant=False, machine="informational", human="not_applicable"),
    spec("M1021-X1", "bridge", "Pinned characteristic-function API provenance",
         "mathlib 8a178386: charFun, charFun_zero, continuous_charFun, ext_of_charFun",
         "Supporting API boundary only; no reverse theorem body.", root_relevant=False, machine="informational", human="not_applicable"),
    spec("M1021-X2", "bridge", "Representation-theorem body provenance",
         "Terminal body and immutable origin for the reverse existence engine",
         "Currently absent; must be local or pinned and trust-audited before credit.", "critical", root_relevant=False, machine="informational", human="not_applicable"),
    spec("M1021-X3", "certificate", "Lean and dependency trust boundary",
         "Lean kernel, compiled mathlib artifacts, imported declarations, axioms, and executable recipes",
         "A content-addressed TCB closure for later release validation.", "high", root_relevant=False, machine="informational", human="not_applicable"),
]


def planned_hash(row):
    if row["id"] == "M1021-ROOT":
        return "lean-expression-sha256:" + ROOT_HASH
    payload = "v1\0" + row["id"] + "\0" + row["target"] + "\0" + row["output"]
    return "planned:v1:sha256:" + hashlib.sha256(payload.encode()).hexdigest()


def graph(edges):
    incoming, outgoing = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


ids = [row["id"] for row in SPECS]
rows = []
nodes = []
for row in SPECS:
    informational = row["machine"] == "informational"
    rows.append({
        "obligation_id": row["id"], "statement_fingerprint": planned_hash(row),
        "kind": row["kind"], "root_relevant": row["root_relevant"],
        "machine_eligibility": row["machine"], "human_source_eligibility": row["human"],
        "readable_eligibility": "required", "risk_class": row["risk"],
        "exclusion_reason": "typed_trust_or_provenance_overlay" if informational else None,
        "terminal_proof_body_id": row["body"],
    })
    leaf = not row["children"]
    ledger = (
        "Premises: exact child outputs listed by typed refinement edges. "
        f"Inference package: {row['title']}. Output: {row['output']}"
        if not leaf else
        f"Premises: the exact context in `{row['target']}`. Inference to implement: {row['title']}. "
        f"Output delivered to the parent: {row['output']} No stronger result is credited."
    )
    nodes.append({
        "node_id": THEOREM + "-" + row["id"].split("-", 1)[1],
        "obligation_id": row["id"], "kind": row["kind"],
        "human_statement": row["title"], "formal_target": row["target"], "output": row["output"],
        "human_debt": "H1", "machine_debt": "M3" if row["id"] == "M1021-ROOT" else "M4",
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-source-boundary" if row["id"] in {"M1021-ROOT", "M1021-X1"} else "pinpoint-map-pending",
        "provenance_id": row["body"] or "none",
        "foundation_profile": "lean4-classical-measure-theory/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none", "step_budget": 6 if leaf else "split-required",
        "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1021/obligation-tree.md#{row['id'].lower().replace('.', '')}",
        "validation_spec_id": "VAL-" + row["id"] + "-PENDING",
        "status_boundary": "Architecture only: no proof body or child-to-parent composition certificate is credited by this freeze.",
        "task_ids": [ITEM, "S56-M-1021-PROOF"],
        "owned_sources": (["Stage1_Instances/THM-M-1021/" + row["body"].split(":")[0]] if row["body"] and not row["body"].startswith("mathlib:") else []),
        "owner": "THM-M-1021 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
    })

projection_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
                     "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                     "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in projection_fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
denoms = {
    "inventory": ids,
    "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
    "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
    "required_readable": ids,
}
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1,
    "freeze_basis": "Mandatory rev-5.6 layers expanded from the exact elaborated target and bounded anchor audit before proof status inspection; eligibility does not depend on candidate availability.",
    "root_obligation_id": "M1021-ROOT", "frozen_denominators": denoms,
    "denominator_sha256": digest, "obligations": rows,
}

proof_edges = []
refinement_edges = []
for row in SPECS:
    for child in row["children"]:
        edge = {"edge_id": f"REF-{row['id']}-{child}", "from": row["id"], "type": "logical_decomposition", "to": child}
        refinement_edges.append(edge)
for child in ("M1021-S", "M1021-N", "M1021-B", "M1021-C", "M1021-L", "M1021-T"):
    proof_edges.append({"edge_id": f"PROOF-M1021-ROOT-{child}", "from": "M1021-ROOT", "type": "proof_requires", "to": child})

graphs = {
    "proof": graph(proof_edges), "refinement": graph(refinement_edges),
    "provenance": graph([
        {"edge_id": "PROV-L1-X1", "from": "M1021-L1", "type": "provenance_of", "to": "M1021-X1"},
        {"edge_id": "PROV-C3-X2", "from": "M1021-C3", "type": "provenance_of", "to": "M1021-X2"},
    ]),
    "evidence": graph([
        {"edge_id": "EVID-ROOT-X1", "from": "M1021-ROOT", "type": "evidence_for", "to": "M1021-X1"},
    ]),
    "trust": graph([
        {"edge_id": "TRUST-ROOT-X", "from": "M1021-ROOT", "type": "trusts", "to": "M1021-X"},
        {"edge_id": "TRUST-X-X1", "from": "M1021-X", "type": "trusts", "to": "M1021-X1"},
        {"edge_id": "TRUST-X-X2", "from": "M1021-X", "type": "trusts", "to": "M1021-X2"},
        {"edge_id": "TRUST-X-X3", "from": "M1021-X", "type": "trusts", "to": "M1021-X3"},
    ]),
    "documentation": graph([
        {"edge_id": "DOC-ROOT-T", "from": "M1021-ROOT", "type": "documents", "to": "M1021-T"},
        {"edge_id": "DOC-C-T", "from": "M1021-C", "type": "documents", "to": "M1021-T"},
    ]),
    "workflow": graph([
        {"edge_id": "FLOW-X-ROOT", "from": "M1021-X", "type": "workflow_depends_on", "to": "M1021-ROOT"},
        {"edge_id": "FLOW-ROOT-T", "from": "M1021-ROOT", "type": "workflow_depends_on", "to": "M1021-T"},
    ]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_sha256": digest, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_machine_debt": "M3",
                         "remaining_root_cut_set": ["M1021-BR", "M1021-C"],
                         "proof_claimed": False, "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"built {len(rows)} obligations; denominator sha256 {digest}")
