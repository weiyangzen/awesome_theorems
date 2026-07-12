#!/usr/bin/env python3
"""Build the frozen THM-M-0541 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0541-OBLIGATION_TREE"
PREFIX = "M0541-"


def fp(formal_target: str) -> str:
    context = (
        "Lean 4.29.0; mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95; "
        "V:Type u; LinearOrder V; K:AbstractSimplicialComplex V"
    )
    return "planned-sha256:" + hashlib.sha256(f"{context}\n{formal_target}".encode()).hexdigest()


# id, kind, risk, human statement, planned formal target, output, budget
SPECS = [
    ("ROOT", "root", "critical", "The frozen alternating simplicial boundary exists and squares to zero.", "Stage1Instances.THM_M_0541.StatementShape", "The exact canonical target.", None),
    ("S", "definition", "high", "Freeze the exact statement, representations, and foundation boundary.", "Statement layer for StatementShape", "An exact, stable proof interface.", None),
    ("S1", "definition", "normal", "Ordered n-simplices and integral finite chains have the definitions in Statement.lean.", "Simplex K n := {s // s in K and s.card = n+1}; Chains K n := Simplex K n ->0 Z", "The generator and chain types used by every child.", 7),
    ("S2", "definition", "normal", "The universe, linear order, coefficient ring, and typeclass assumptions are fixed.", "V : Type u; [LinearOrder V]; K : AbstractSimplicialComplex V; coefficients Z", "No implicit domain or coefficient changes.", 5),
    ("S3", "branch", "high", "Degree zero, the empty complex, infinite complexes, and finite-support chains obey the frozen conventions.", "No degree -1; d 0 : Chains K 1 ->+ Chains K 0; every chain has finite support", "Boundary cases compatible with the root.", 9),
    ("S4", "transport", "high", "The explicit double-sum proof and the alternating-face-map anchor must be kept distinct unless a checked bridge is built.", "Direct Finsupp construction -> CanonicalTarget K; categorical bridge is uncredited", "A declared one-way direct route with no anchor substitution.", 8),
    ("S5", "certificate", "high", "Only audited Lean and mathlib foundation primitives may enter an eventual proof closure.", "Axiom and terminal-declaration policy certificate for StatementShape", "A fail-closed foundation boundary.", 8),
    ("N", "normalization", "high", "Normalize boundary-square evaluation to paired ordered vertex deletions.", "forall n c, d n (d (n+1) c) = 0 reduced to basis generators and normalized deletion pairs", "A finite cancellation problem.", None),
    ("N1", "normalization", "high", "Deleting an ordered vertex gives the expected order enumeration of the erased simplex.", "Planned lemma relating orderEmbOfFin (erase v) to orderEmbOfFin before erasure", "Index control for iterated faces.", 18),
    ("N2", "normalization", "critical", "Each iterated deletion is normalized to an unordered pair of distinct original indices.", "Planned equivalence between Sigma (fun i : Fin (n+3) => Fin (n+2)) and ordered distinct-index deletion data", "A canonical index for each double-boundary term.", 22),
    ("N3", "normalization", "normal", "Equality of Finsupp chains is reduced extensionally to coefficients.", "Finsupp.ext plus coefficient evaluation of finite sums of singletons", "Coefficientwise equality goal.", 10),
    ("N4", "reduction", "high", "An additive-map equality on finite chains is reduced to basis simplices.", "forall c : Chains K (n+2), P c, reduced using Finsupp.induction or AddMonoidHom ext", "Basis-level square-zero obligations.", 14),
    ("B", "branch", "critical", "Split every ordered pair of deletions by the relative order of its original vertices.", "Complete split a < b or b < a for distinct a b", "Two exhaustive cancellation branches.", None),
    ("B1", "branch", "high", "Handle the branch in which the first original deleted index is smaller.", "a < b branch: face (face sigma b) a = face (face sigma a) (b-1)", "One representative of each cancellation pair.", 16),
    ("B2", "branch", "high", "Handle the branch in which the second original deleted index is smaller.", "b < a branch, symmetric normalization to the B1 representative", "The partner term for each cancellation pair.", 14),
    ("B3", "core_lemma", "critical", "The two branch coefficients have opposite signs.", "(-1:Z)^a * (-1)^(b-1) + (-1)^b * (-1)^a = 0 for a < b", "Coefficient cancellation for a deletion pair.", 15),
    ("B4", "bridge", "critical", "The relative-order split is exhaustive and recomposes the full double sum without duplication.", "Finite-sum partition/bijection certificate covering every iterated-face index exactly once", "The complete double sum partition.", 20),
    ("C", "construction", "critical", "Construct the degreewise additive boundary maps with the required basis formula.", "exists d : (n:Nat) -> Chains K (n+1) ->+ Chains K n, HasAlternatingBoundary K d", "The boundary-map family.", None),
    ("C1", "construction", "high", "Vertex deletion is a well-defined simplex of the preceding degree.", "face : Simplex K (n+1) -> Fin (n+2) -> Simplex K n", "Typed codimension-one faces.", 12),
    ("C2", "construction", "normal", "Define the alternating boundary of one basis simplex as a finite sum.", "boundaryBasis n sigma := sum i, single (face sigma i) ((-1:Z)^(i:Nat))", "A chain in degree n.", 8),
    ("C3", "construction", "high", "Extend the basis assignment uniquely to an additive map on Finsupp chains.", "boundary n : Chains K (n+1) ->+ Chains K n via Finsupp.liftAddHom", "The additive boundary map d n.", 18),
    ("C4", "certificate", "normal", "The constructed map evaluates on each basis chain by the frozen alternating formula.", "forall n sigma, boundary n (single sigma 1) = boundaryBasis n sigma", "HasAlternatingBoundary K boundary.", 10),
    ("L", "core_lemma", "critical", "Prove the combinatorial cancellation engine for two consecutive boundaries.", "forall n sigma, boundary n (boundary (n+1) (single sigma 1)) = 0", "Basis-level boundary-square theorem.", None),
    ("L1", "core_lemma", "critical", "Deleting distinct vertices in either order produces the same subtype simplex.", "planned face-face identity with shifted Fin indices for i < j", "Equality of the paired basis keys.", 24),
    ("L2", "core_lemma", "high", "The signs attached to the paired deletion orders are negatives.", "planned integer parity/sign identity for shifted indices", "Opposite integer coefficients.", 15),
    ("L3", "core_lemma", "high", "Each normalized pair contributes zero to the Finsupp coefficient.", "paired singleton terms with equal keys and opposite coefficients sum to zero", "Local cancellation.", 14),
    ("L4", "core_lemma", "critical", "Finite reindexing by the cancellation pairing makes the entire expanded double sum zero.", "planned Finset sum_bij/involution cancellation theorem specialized to iterated faces", "Double-boundary basis sum equals zero.", 25),
    ("L5", "bridge", "critical", "The expanded double-boundary expression agrees with the normalized double sum.", "map_sum and boundary-on-single expansion certificate", "Boundary square on each basis simplex.", 18),
    ("X", "bridge", "high", "Audit external APIs and the trust boundary used by the direct proof route.", "Imported theorem and foundation boundary", "No imported infrastructure is mistaken for root closure.", None),
    ("X1", "bridge", "high", "The Finsupp additive-lift, induction, extensionality, and single evaluation APIs have exact pinned signatures.", "Pinned Finsupp APIs needed by C3, N3, and N4", "Checked free-additive-group infrastructure.", 16),
    ("X2", "bridge", "high", "The finite-sum reindexing or involution API used by L4 has an exact pinned signature.", "Pinned Fin/Finset sum cancellation APIs needed by B4 and L4", "Checked finite cancellation infrastructure.", 16),
    ("X3", "certificate", "high", "Record the transitive Lean kernel, axiom, quotient, choice, and computation boundary.", "Trust/TCB certificate for eventual terminal declarations", "Release-gating trust overlay only.", 12),
    ("T", "terminal", "critical", "Compose construction and cancellation into the exact existential root.", "CanonicalTarget K and universal closure StatementShape", "Exact-root assembly.", None),
    ("T1", "terminal", "high", "Package the construction formula as HasAlternatingBoundary.", "HasAlternatingBoundary K boundary", "First conjunct of CanonicalTarget.", 7),
    ("T2", "terminal", "critical", "Extend basis cancellation to every finite chain.", "forall n c, boundary n (boundary (n+1) c) = 0", "Second conjunct of CanonicalTarget.", 14),
    ("T3", "terminal", "critical", "Introduce the boundary witness and universally close all frozen binders.", "forall V [LinearOrder V] K, CanonicalTarget K", "Stage1Instances.THM_M_0541.StatementShape.", 8),
]

CHILDREN = {
    "ROOT": ["S", "N", "B", "C", "L", "X", "T"],
    "S": ["S1", "S2", "S3", "S4", "S5"],
    "N": ["N1", "N2", "N3", "N4"],
    "B": ["B1", "B2", "B3", "B4"],
    "C": ["C1", "C2", "C3", "C4"],
    "L": ["L1", "L2", "L3", "L4", "L5"],
    "X": ["X1", "X2", "X3"],
    "T": ["T1", "T2", "T3"],
}


def oid(short: str) -> str:
    return PREFIX + short


def edges(name: str, pairs: list[tuple[str, str]], relation: str) -> dict:
    rows = []
    incoming, outgoing = {}, {}
    for number, (source, target) in enumerate(pairs, 1):
        edge_id = f"M0541-{name.upper()}-{number:03d}"
        row = {"edge_id": edge_id, "type": relation, "from": oid(source), "to": oid(target)}
        rows.append(row)
        outgoing.setdefault(oid(source), []).append(edge_id)
        incoming.setdefault(oid(target), []).append(edge_id)
    return {"edges": rows, "out": outgoing, "in": incoming}


def main() -> None:
    obligations = []
    nodes = []
    for short, kind, risk, human, formal, output, budget in SPECS:
        informational = short == "X3"
        obligation = {
            "obligation_id": oid(short),
            "statement_fingerprint": fp(formal),
            "kind": kind,
            "root_relevant": True,
            "machine_eligibility": "informational" if informational else "required",
            "human_source_eligibility": "not_applicable" if informational else "required",
            "readable_eligibility": "not_applicable" if informational else "required",
            "risk_class": risk,
            "exclusion_reason": "trust-overlay-not-a-mathematical-conclusion" if informational else "none",
            "terminal_proof_body_id": "none-until-proof-phase",
        }
        obligations.append(obligation)
        ledger = (
            f"Premises: exact frozen context and the typed children recorded for {oid(short)}. "
            f"Inference target: {formal}. Output: {output} "
            "No proof, source, composition, or closure credit is attached by this architecture record."
        )
        nodes.append({
            "node_id": f"THM-M-0541-{short}", "obligation_id": oid(short), "kind": kind,
            "human_statement": human, "formal_target": formal, "output": output,
            "human_debt": "H2", "machine_debt": "M3", "readability_debt": "R4",
            "evidence_ids": [], "source_crosswalk_id": "source-statement-crosswalk.md (pinpoint review open)",
            "provenance_id": "MATHLIB-AFMC-anchor-only" if short in {"S4", "X", "X2"} else "none",
            "foundation_profile": "lean4-4.29.0/policy-audit-pending",
            "tcb_profile": "mathlib-8a178386/transitive-closure-pending",
            "computation_record": "none", "step_budget": "split-required" if budget is None else budget,
            "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/THM-M-0541/obligation-tree.md#m0541-{short.lower()}",
            "validation_spec_id": f"VAL-M0541-{short}-PENDING", "status_boundary": "Architecture only; this node is open and has no admitted proof body or composition certificate.",
            "task_ids": [ITEM, "S56-M-0541-PROOF"], "owned_sources": [],
            "owner": "THM-M-0541 proof implementer", "reviewer": "independent Stage1 integration reviewer",
            "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
        })

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    projection = [{key: row[key] for key in fields} for row in obligations]
    digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
        "theorem_id": "THM-M-0541", "registry_version": 1,
        "freeze_basis": "Exact StatementShape plus the audited direct combinatorial and anchor-only routes; closure state was not used to choose eligibility.",
        "root_obligation_id": oid("ROOT"), "denominator_sha256": digest,
        "frozen_denominators": {
            "inventory": [row["obligation_id"] for row in obligations],
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
        },
        "obligations": obligations,
        "status_boundary": "Registry freeze only. All mathematical obligations remain open; X3 is an informational trust overlay and cannot earn proof credit.",
    }

    proof_pairs = []
    refinement_pairs = []
    for parent, children in CHILDREN.items():
        target = refinement_pairs if parent == "S" else proof_pairs
        target.extend((parent, child) for child in children)
    graphs = {
        "proof": edges("proof", proof_pairs, "proof_requires"),
        "refinement": edges("refinement", refinement_pairs, "logical_decomposition"),
        "provenance": edges("provenance", [("S4", "X2"), ("X", "X1"), ("X", "X2")], "provenance_of"),
        "evidence": edges("evidence", [("ROOT", "S5"), ("L", "X2")], "evidence_for"),
        "trust": edges("trust", [("ROOT", "X3"), ("C3", "X3"), ("L4", "X3")], "trusts"),
        "documentation": edges("documentation", [("ROOT", "S"), ("ROOT", "N"), ("ROOT", "B"), ("ROOT", "C"), ("ROOT", "L"), ("ROOT", "T")], "documents"),
        "workflow": edges("workflow", [("S", "C"), ("C", "N"), ("N", "B"), ("B", "L"), ("L", "T")], "workflow_depends_on"),
    }
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0541",
        "registry_version": 1, "registry_denominator_sha256": digest, "nodes": nodes, "graphs": graphs,
        "closure_boundary": {"closed_obligations": [], "root_machine_debt": "M3", "theorem_complete": False,
                             "remaining_root_cut_set": [oid("C3"), oid("L1"), oid("L4"), oid("T2")]},
    }
    (HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
    (HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")
    print(f"built {len(obligations)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges; denominator {digest}")


if __name__ == "__main__":
    main()
