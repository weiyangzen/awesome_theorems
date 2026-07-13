#!/usr/bin/env python3
"""Build or verify the frozen THM-M-0856 obligation architecture."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM_ID = "S56-M-0856-OBLIGATION_TREE"
THEOREM_ID = "THM-M-0856"
PREFIX = "M0856"
FROZEN_AT = "2026-07-14T02:04:55+08:00"
ROOT_EXPRESSION = "5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
TUTTE_BLOB = "4b7931e61e4dd6a3aae37fcecf698ddc238fbc4e"
MATCHING_BLOB = "1c4940a10d3d4c6fc6462bd43ffa2e70ced8dacf"
METRIC_BLOB = "9599bd6984b87caedfbf6a87c15a704b09339480"
UNIVERSAL_VERTS_BLOB = "9ac099fcadc6d87bd9d1b3fd7a07bbe11c6af38f"
TUTTE_BODY = f"mathlib4@{MATHLIB_REVISION}:{TUTTE_BLOB}#SimpleGraph.tutte"

EXACT_TYPES = {
    "M0856-ROOT": "forall {V : Type u} (G : SimpleGraph V), [Finite V] -> ((Exists fun M : G.Subgraph => M.IsPerfectMatching) <-> Stage1Instances.THM_M_0856.OddComponentCondition G)",
    "M0856-S-TARGET": "forall {V : Type u} (G : SimpleGraph V), [Finite V] -> ((Exists fun M : G.Subgraph => M.IsPerfectMatching) <-> Stage1Instances.THM_M_0856.OddComponentCondition G)",
    "M0856-S-ODD-CONDITION": "forall {V : Type u} (G : SimpleGraph V), Prop",
    "M0856-S-TRANSPORT": "Stage1Instances.THM_M_0856.TutteOneFactorTarget <-> Stage1Instances.THM_M_0856.NoTutteViolatorTarget",
    "M0856-T-ADAPTER": "Stage1Instances.THM_M_0856.ObligationTree.MathlibTerminal -> Stage1Instances.THM_M_0856.TutteOneFactorTarget",
    "M0856-T-UPSTREAM": "forall {V : Type u} {G : SimpleGraph V} [Finite V], (Exists fun M : G.Subgraph => M.IsPerfectMatching) <-> forall U : Set V, Not (G.IsTutteViolator U)",
    "M0856-T-NECESSITY": "forall {V : Type u} {G : SimpleGraph V} [Finite V] {M : G.Subgraph}, M.IsPerfectMatching -> forall U : Set V, Not (G.IsTutteViolator U)",
    "M0856-L-ODD-MATCHES-OUTSIDE": "forall {V : Type u} {G : SimpleGraph V} {M : G.Subgraph} [Finite V] {U : Set V}, M.IsPerfectMatching -> forall c : ((\u22a4 : G.Subgraph).deleteVerts U).coe.oddComponents, exists w, w \u2208 U /\\ exists v : ((\u22a4 : G.Subgraph).deleteVerts U).verts, M.Adj v w /\\ v \u2208 c.val.supp",
    "M0856-L-EMPTY-VIOLATOR": "forall {V : Type u} {G : SimpleGraph V} [Finite V], Odd (Nat.card V) -> G.IsTutteViolator (\u2205 : Set V)",
    "M0856-L-EXISTS-VIOLATOR": "forall {V : Type u} {G : SimpleGraph V} [Finite V], (forall M : G.Subgraph, Not M.IsPerfectMatching) -> Even (Nat.card V) -> exists U, G.IsTutteViolator U",
    "M0856-C-MAXIMAL-MATCHING-FREE": "forall {V : Type u} {G : SimpleGraph V} [Finite V], G.IsMatchingFree -> exists Gmax, G <= Gmax /\\ Gmax.IsMatchingFree /\\ forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching",
    "M0856-L-VIOLATOR-MONO": "forall {V : Type u} {G G' : SimpleGraph V} [Finite V] {U : Set V}, G <= G' -> G'.IsTutteViolator U -> G.IsTutteViolator U",
    "M0856-T-CLIQUE-PERFECT": "forall {V : Type u} {G : SimpleGraph V} [Finite V], Even (Nat.card V) -> Not (G.IsTutteViolator G.universalVerts) -> (forall K : G.deleteUniversalVerts.coe.ConnectedComponent, G.deleteUniversalVerts.coe.IsClique K.supp) -> exists M : G.Subgraph, M.IsPerfectMatching",
}

EXACT_DECLARATIONS = {
    "M0856-ROOT": "Stage1Instances.THM_M_0856.TutteOneFactorTarget",
    "M0856-S-TARGET": "Stage1Instances.THM_M_0856.TutteOneFactorTarget",
    "M0856-S-ODD-CONDITION": "Stage1Instances.THM_M_0856.OddComponentCondition",
    "M0856-S-TRANSPORT": "Stage1Instances.THM_M_0856.tutteOneFactorTarget_iff_noTutteViolatorTarget",
    "M0856-T-ADAPTER": "Stage1Instances.THM_M_0856.ObligationTree.terminal_adapter",
    "M0856-T-UPSTREAM": "SimpleGraph.tutte",
    "M0856-T-NECESSITY": "SimpleGraph.not_isTutteViolator_of_isPerfectMatching",
    "M0856-L-ODD-MATCHES-OUTSIDE": "SimpleGraph.ConnectedComponent.odd_matches_node_outside",
    "M0856-L-EMPTY-VIOLATOR": "SimpleGraph.IsTutteViolator.empty",
    "M0856-L-EXISTS-VIOLATOR": "SimpleGraph.exists_isTutteViolator",
    "M0856-C-MAXIMAL-MATCHING-FREE": "SimpleGraph.exists_maximal_isMatchingFree",
    "M0856-L-VIOLATOR-MONO": "SimpleGraph.IsTutteViolator.mono",
    "M0856-T-CLIQUE-PERFECT": "SimpleGraph.Subgraph.IsPerfectMatching.exists_of_isClique_supp",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def spec(
    suffix: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    output: str,
    source: str,
    method: str,
    budget: int,
    *,
    machine_eligibility: str = "required",
    human_source_eligibility: str = "required",
    terminal_body: str | None = None,
    formal_kind: str = "exact_lean_type",
    formal_declaration: str | None = None,
) -> dict:
    return {
        "id": f"{PREFIX}-{suffix}",
        "kind": kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "formal_kind": formal_kind,
        "formal_declaration": formal_declaration,
        "output": output,
        "source": source,
        "method": method,
        "budget": budget,
        "machine_eligibility": machine_eligibility,
        "human_source_eligibility": human_source_eligibility,
        "terminal_body": terminal_body,
    }


SPECS = [
    spec("ROOT", "root", "critical", "Every finite simple graph has a perfect matching exactly when every vertex deletion leaves at most as many odd components as deleted vertices.", "Stage1Instances.THM_M_0856.TutteOneFactorTarget", "The exact canonical universe-polymorphic proposition.", "Statement.lean; expression sha256 " + ROOT_EXPRESSION, "Apply the checked terminal adapter to the pinned no-violator terminal without changing any binder, domain, or boundary case.", 8),
    spec("S-TARGET", "definition", "critical", "Freeze the exact finite-simple-graph target and its expression fingerprint.", "Stage1Instances.THM_M_0856.TutteOneFactorTarget", "The canonical target interface, counted only once at the root.", "Statement.lean:27-31; statement.json canonical_formal_target", "Read the elaborated proposition and preserve its universe, graph, finiteness, existential matching, and universal deletion binders.", 8, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("S-DOMAIN", "definition", "high", "Fix V : Type u, G : SimpleGraph V, and [Finite V] with no connectedness, decidability, Fintype, or nonemptiness premise.", "forall {V : Type u} (G : SimpleGraph V), [Finite V] -> True", "The exact domain and typeclass context used by every proof node.", "Statement.lean:28-31; statement.json ordered_binders", "Propagate the original binder order and infer only local instances derivable from [Finite V].", 10, machine_eligibility="informational", human_source_eligibility="not_applicable", formal_kind="planned_lean_signature"),
    spec("S-MATCHING", "definition", "high", "Use a spanning matching subgraph as the perfect-matching witness.", "forall {V : Type u} (G : SimpleGraph V), (Exists fun M : G.Subgraph => M.IsPerfectMatching) <-> (Exists fun M : G.Subgraph => M.IsPerfectMatching)", "A non-claiming interface identity that freezes the left side as `Exists fun M : G.Subgraph => M.IsPerfectMatching`.", "Statement.lean:31; Mathlib/Combinatorics/SimpleGraph/Matching.lean", "Freeze the existential subgraph representation and its spanning and matching fields without asserting that every graph has such a witness; do not substitute an edge set or involution.", 12, machine_eligibility="informational", human_source_eligibility="not_applicable", formal_kind="planned_lean_signature"),
    spec("S-ODD-CONDITION", "definition", "high", "Count odd connected components of the induced graph after deleting an arbitrary vertex set U.", "Stage1Instances.THM_M_0856.OddComponentCondition", "The right side of the canonical equivalence.", "Statement.lean:18-25", "Expand deleteVerts, oddComponents, and ncard only through the frozen definitions, retaining every U : Set V.", 12, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("S-BOUNDARY", "branch", "high", "Retain empty carriers, odd carriers, isolated vertices, disconnected graphs, and empty or full deletion sets.", "statement.json#/degenerate_cases", "No strengthened premise or omitted degenerate case.", "statement.json degenerate_cases", "Check that each listed case remains admitted by the same target rather than being discharged by an added premise.", 14, machine_eligibility="informational", human_source_eligibility="not_applicable", formal_kind="nonformal_record"),
    spec("S-TRANSPORT", "transport", "critical", "Transport the deletion inequality to the absence of a strict IsTutteViolator in the direction used by mathlib.", "Stage1Instances.THM_M_0856.tutteOneFactorTarget_iff_noTutteViolatorTarget", "An exact checked bridge between canonical and pinned terminal interfaces.", "Statement.lean:46-57", "Unfold both violator predicates and use not_lt, preserving the complete Iff and all quantifiers.", 10, machine_eligibility="informational", human_source_eligibility="not_applicable", terminal_body="repo:Statement.lean#tutteOneFactorTarget_iff_noTutteViolatorTarget"),
    spec("S-FOUNDATION", "certificate", "critical", "Account for propositional extensionality, classical choice, quotient soundness, Lean, mathlib, and the no-oracle computation policy.", "stage1-foundation-profile/1.0", "A reviewed release-grade foundation and trust decision, not a theorem premise.", "anchor-audit.json immutable_environment and provenance_packet", "Compare machine-derived transitive dependencies with the selected foundation profile and reject any unknown trust path.", 35, machine_eligibility="informational", human_source_eligibility="not_applicable", formal_kind="nonformal_record"),
    spec("N-FINITE-INTERFACES", "normalization", "high", "Derive local Fintype and decidability interfaces from [Finite V] without adding a Nonempty V premise.", "forall {V : Type u}, [Finite V] -> Nonempty (Fintype V)", "Finite-cardinality APIs usable in the clique and maximal-graph branches.", "Tutte.lean:126,272", "Obtain a local Fintype witness by classical choice and keep the empty carrier within the original [Finite V] context.", 18, formal_kind="planned_lean_signature"),
    spec("T-ADAPTER", "transport", "critical", "Convert the literal pinned no-violator theorem to the exact frozen inequality target.", "Stage1Instances.THM_M_0856.ObligationTree.terminal_adapter", "MathlibTerminal implies TutteOneFactorTarget.", "ObligationTree.lean#terminal_adapter", "Simplify only the frozen target, odd-component condition, pinned violator predicate, and not_lt.", 10, human_source_eligibility="not_applicable", terminal_body="repo:ObligationTree.lean#terminal_adapter"),
    spec("T-UPSTREAM", "terminal", "critical", "Compose necessity and contraposed sufficiency into the pinned no-violator Iff.", "SimpleGraph.tutte", "The literal MathlibTerminal proposition.", "Tutte.lean:310-322", "Use the necessity declaration for the forward direction, then contrapose the reverse direction and split the finite carrier by parity.", 14, terminal_body=TUTTE_BODY),
    spec("T-NECESSITY", "terminal", "critical", "A perfect matching prevents every vertex set from being a Tutte violator.", "SimpleGraph.not_isTutteViolator_of_isPerfectMatching", "For all U, not G.IsTutteViolator U.", "Tutte.lean:140-149", "Choose a matched exit from every odd component, prove the exit map injective, and compare finite cardinalities.", 18, terminal_body=f"mathlib4@{MATHLIB_REVISION}:{TUTTE_BLOB}#SimpleGraph.not_isTutteViolator_of_isPerfectMatching"),
    spec("L-ODD-MATCHES-OUTSIDE", "core_lemma", "critical", "Every odd component after deleting U has a matching edge to a vertex of U.", "ConnectedComponent.odd_matches_node_outside", "For each odd component, an incident matched vertex outside the deleted graph.", "Matching.lean:293-314", "Assume no matched exit, restrict the perfect matching to the component, derive even component cardinality, and contradict oddness.", 55, terminal_body=f"mathlib4@{MATHLIB_REVISION}:{MATCHING_BLOB}#ConnectedComponent.odd_matches_node_outside"),
    spec("C-ODD-TO-U-INJECTION", "construction", "critical", "Choose one supplied deleted endpoint for each odd component and construct an injection into U.", "forall {V : Type u} {G : SimpleGraph V} [Finite V] {M : G.Subgraph} (hM : M.IsPerfectMatching) (U : Set V), (forall c : ((\u22a4 : G.Subgraph).deleteVerts U).coe.oddComponents, exists w, w \u2208 U /\\ exists v : ((\u22a4 : G.Subgraph).deleteVerts U).verts, M.Adj v w /\\ v \u2208 c.val.supp) -> exists f : ((\u22a4 : G.Subgraph).deleteVerts U).coe.oddComponents -> U, Function.Injective f", "An injective map from odd components to U, conditional on the exact odd-component exit family.", "Tutte.lean:144-147", "Consume the odd-exit family supplied by L-ODD-MATCHES-OUTSIDE, choose endpoints, then use matching uniqueness and common-component membership to show equal images force equal components.", 24, formal_kind="planned_lean_signature"),
    spec("L-NCARD-INJECTION", "core_lemma", "high", "Convert the component injection into the canonical odd-component ncard inequality.", "forall {V : Type u} {G : SimpleGraph V} [Finite V] (U : Set V), (exists f : ((\u22a4 : G.Subgraph).deleteVerts U).coe.oddComponents -> U, Function.Injective f) -> ((\u22a4 : G.Subgraph).deleteVerts U).coe.oddComponents.ncard <= U.ncard", "oddComponents.ncard <= U.ncard.", "Tutte.lean:148-149", "Apply cardinal monotonicity to the subtype injection and normalize subtype cardinalities to Set.ncard.", 16, formal_kind="planned_lean_signature"),
    spec("T-SUFFICIENCY", "terminal", "critical", "If no vertex set violates Tutte's condition, a perfect matching exists.", "forall {V : Type u} (G : SimpleGraph V) [Finite V], (forall U : Set V, Not (G.IsTutteViolator U)) -> Exists fun M : G.Subgraph => M.IsPerfectMatching", "The reverse implication of the pinned terminal Iff.", "Tutte.lean:317-322", "Contrapose perfect-matching existence, then construct a violator in the odd-cardinality or even-cardinality branch.", 14, formal_kind="planned_lean_signature"),
    spec("B-PARITY-SPLIT", "branch", "critical", "Split Nat.card V into odd and not-odd cases and recompose exhaustively.", "forall {V : Type u} (G : SimpleGraph V) [Finite V], (forall M : G.Subgraph, Not M.IsPerfectMatching) -> (Odd (Nat.card V) -> Exists fun U : Set V => G.IsTutteViolator U) -> (Even (Nat.card V) -> Exists fun U : Set V => G.IsTutteViolator U) -> Exists fun U : Set V => G.IsTutteViolator U", "A Tutte violator under the assumption that every subgraph matching is imperfect.", "Tutte.lean:320-322", "Use the odd branch directly; in the complement convert not-odd to even before invoking the even-order theorem.", 10, formal_kind="planned_lean_signature"),
    spec("B-ODD-CARD", "branch", "high", "On an odd-order carrier, the empty deletion set is a Tutte violator.", "forall {V : Type u} {G : SimpleGraph V} [Finite V], Odd (Nat.card V) -> exists U : Set V, U = \u2205 /\\ G.IsTutteViolator U", "Exists U, G.IsTutteViolator U with U = empty.", "Tutte.lean:136-138,320-321", "Relate odd total vertex count to a positive odd-component count after deleting no vertices.", 12, formal_kind="planned_lean_signature"),
    spec("L-EMPTY-VIOLATOR", "core_lemma", "high", "Odd total order implies strictly more than zero odd components after empty deletion.", "SimpleGraph.IsTutteViolator.empty", "G.IsTutteViolator empty.", "Tutte.lean:136-138", "Rewrite the empty-set cardinality and use odd_ncard_oddComponents to obtain positivity.", 12, terminal_body=f"mathlib4@{MATHLIB_REVISION}:{TUTTE_BLOB}#SimpleGraph.IsTutteViolator.empty"),
    spec("B-EVEN-CARD", "branch", "critical", "On an even-order matching-free graph, construct a Tutte violator.", "forall {V : Type u} {G : SimpleGraph V} [Finite V], Even (Nat.card V) -> (forall M : G.Subgraph, Not M.IsPerfectMatching) -> exists U : Set V, G.IsTutteViolator U", "Exists U, G.IsTutteViolator U.", "Tutte.lean:264-308,322", "Invoke the maximal matching-free supergraph argument with the derived even cardinality witness.", 12, formal_kind="planned_lean_signature"),
    spec("L-EXISTS-VIOLATOR", "core_lemma", "critical", "Every finite even-order matching-free graph has a Tutte violator.", "SimpleGraph.exists_isTutteViolator", "A vertex set whose deletion leaves too many odd components.", "Tutte.lean:264-308", "Pass to an edge-maximal matching-free supergraph, delete its universal vertices, and split on whether all remaining components are cliques.", 22, terminal_body=f"mathlib4@{MATHLIB_REVISION}:{TUTTE_BLOB}#SimpleGraph.exists_isTutteViolator"),
    spec("C-MAXIMAL-MATCHING-FREE", "construction", "critical", "Extend G to an edge-maximal matching-free supergraph Gmax.", "SimpleGraph.exists_maximal_isMatchingFree", "G <= Gmax, Gmax matching-free, and every strict supergraph has a perfect matching.", "Matching.lean:335-340; Tutte.lean:274", "Apply finite maximality to the matching-free property and retain both inclusion and strict-extension witnesses.", 30, terminal_body=f"mathlib4@{MATHLIB_REVISION}:{MATCHING_BLOB}#SimpleGraph.exists_maximal_isMatchingFree"),
    spec("L-VIOLATOR-MONO", "core_lemma", "high", "A violator for a supergraph remains a violator for a subgraph on the same vertices.", "SimpleGraph.IsTutteViolator.mono", "Gmax violator U implies G violator U when G <= Gmax.", "Tutte.lean:60-65", "Use monotonicity of odd-component counts under edge deletion and discharge the strict cardinal inequality.", 18, terminal_body=f"mathlib4@{MATHLIB_REVISION}:{TUTTE_BLOB}#SimpleGraph.IsTutteViolator.mono"),
    spec("C-UNIVERSAL-DELETION", "construction", "high", "Choose Gmax.universalVerts as the candidate deletion set and expose the remaining connected components.", "forall {V : Type u} (Gmax : SimpleGraph V), Gmax.deleteUniversalVerts = (\u22a4 : Gmax.Subgraph).deleteVerts Gmax.universalVerts", "The candidate deletion subgraph is definitionally the top subgraph with universal vertices removed.", "Tutte.lean:275-278; UniversalVerts.lean:20-45", "Use the exact deleteUniversalVerts definition, then expose its connected-component type without assuming that a component exists.", 20, formal_kind="planned_lean_signature"),
    spec("B-CLIQUE-SPLIT", "branch", "critical", "Split whether every component after deleting universal vertices is a clique and recompose the two contradiction handlers.", "forall {V : Type u} (Gmax : SimpleGraph V) [Finite V], Gmax.IsMatchingFree -> Even (Nat.card V) -> (forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching) -> Not (Gmax.IsTutteViolator Gmax.universalVerts) -> ((forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False) -> (Not (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False) -> False", "A contradiction from either exhaustive clique-status branch, with the maximal-graph context retained.", "Tutte.lean:278-308", "Use classical case analysis on the componentwise clique predicate and invoke exactly the matching branch handler; neither child may be ignored.", 14, formal_kind="planned_lean_signature"),
    spec("B-ALL-CLIQUES", "branch", "critical", "If all deleted components are cliques and universalVerts is not a violator, derive a perfect matching of Gmax.", "forall {V : Type u} {Gmax : SimpleGraph V} [Finite V], Gmax.IsMatchingFree -> Even (Nat.card V) -> Not (Gmax.IsTutteViolator Gmax.universalVerts) -> (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False", "A contradiction to Gmax being matching-free.", "Tutte.lean:280-286", "Normalize the nonviolator cardinal bound and invoke the clique-support perfect-matching construction.", 16, formal_kind="planned_lean_signature"),
    spec("T-CLIQUE-PERFECT", "terminal", "critical", "Build a perfect matching when universal-vertex deletion decomposes into cliques and the count bound holds.", "SimpleGraph.Subgraph.IsPerfectMatching.exists_of_isClique_supp", "Exists M : Subgraph Gmax, M.IsPerfectMatching.", "Tutte.lean:118-134", "Combine a near-covering matching with a matching on its uncovered universal-vertex complement.", 22, terminal_body=f"mathlib4@{MATHLIB_REVISION}:{TUTTE_BLOB}#SimpleGraph.Subgraph.IsPerfectMatching.exists_of_isClique_supp"),
    spec("C-NEAR-COVER-MATCHING", "construction", "critical", "Construct a matching covering every non-universal vertex and possibly leaving universal vertices uncovered.", "forall {V : Type u} (G : SimpleGraph V) [Finite V], Not (G.IsTutteViolator G.universalVerts) -> (forall K : G.deleteUniversalVerts.coe.ConnectedComponent, G.deleteUniversalVerts.coe.IsClique K.supp) -> exists M : G.Subgraph, M.IsMatching /\\ M.vertsᶜ \u2286 G.universalVerts", "M.IsMatching and M.verts complement subset universalVerts.", "Tutte.lean:67-116", "Match odd-component representatives to universal vertices, match remaining component vertices internally, and take the disjoint supremum.", 26, formal_kind="planned_lean_signature"),
    spec("C-ODD-REPRESENTATIVES", "construction", "high", "Choose one representative in each odd component and derive the disjointness and cardinal bound needed to match them to universal vertices.", "forall {V : Type u} (G : SimpleGraph V) [Finite V], Not (G.IsTutteViolator G.universalVerts) -> let reps : Set G.deleteUniversalVerts.verts := Quot.out '' G.deleteUniversalVerts.coe.oddComponents; ConnectedComponent.Represents reps G.deleteUniversalVerts.coe.oddComponents /\\ reps.ncard = G.deleteUniversalVerts.coe.oddComponents.ncard /\\ Disjoint G.universalVerts (Subtype.val '' reps) /\\ (Subtype.val '' reps).ncard <= G.universalVerts.ncard", "A representative set with exact count, disjointness from universal vertices, and the nonviolator cardinal bound.", "Tutte.lean:79-84; Connectivity/Represents.lean:39-44,67-68; UniversalVerts.lean:59-62", "Use image_out and ncard_eq, lift representatives through Subtype.val, prove universal-vertex disjointness, and normalize the nonviolator inequality to the image ncard bound.", 28, formal_kind="planned_lean_signature"),
    spec("C-MATCH-REPS-UNIVERSALS", "construction", "critical", "Match odd-component representatives injectively to universal vertices using the derived nonviolator bound.", "forall {V : Type u} {G : SimpleGraph V} [Finite V] {reps : Set G.deleteUniversalVerts.verts}, ConnectedComponent.Represents reps G.deleteUniversalVerts.coe.oddComponents -> Disjoint G.universalVerts (Subtype.val '' reps) -> (Subtype.val '' reps).ncard <= G.universalVerts.ncard -> exists t : Set V, t \u2286 G.universalVerts /\\ exists M1 : G.Subgraph, M1.verts = Subtype.val '' reps \u222a t /\\ M1.IsMatching", "A selected universal set t and matching M1 whose vertices are exactly the representatives and t.", "Tutte.lean:81-84; UniversalVerts.lean:48-58", "Apply exists_of_universalVerts to the derived disjointness and ncard bound, retaining t, its subset proof, the exact vertex equation, and matching property for downstream parity.", 28, formal_kind="planned_lean_signature"),
    spec("C-INTERNAL-COMPONENT-MATCHINGS", "construction", "critical", "For each deleted component, derive evenness of the unused vertices and match them inside its clique.", "forall {V : Type u} {G : SimpleGraph V} [Finite V] {reps : Set G.deleteUniversalVerts.verts} {t : Set V} {M1 : G.Subgraph}, (forall K : G.deleteUniversalVerts.coe.ConnectedComponent, G.deleteUniversalVerts.coe.IsClique K.supp) -> ConnectedComponent.Represents reps G.deleteUniversalVerts.coe.oddComponents -> t \u2286 G.universalVerts -> M1.verts = Subtype.val '' reps \u222a t -> M1.IsMatching -> exists complMatch : G.deleteUniversalVerts.coe.ConnectedComponent -> G.Subgraph, forall K, (complMatch K).verts = Subtype.val '' K.supp \\ M1.verts /\\ (complMatch K).IsMatching", "A component-indexed family of matchings covering exactly the vertices not used by M1.", "Tutte.lean:85-92; UniversalVerts.lean:69-77; Matching.lean:260-275", "Use the representative parity lemma to prove each residual set even, inherit the clique property, and apply the finite clique matching equivalence before choosing the family.", 42, formal_kind="planned_lean_signature"),
    spec("C-ISUP-DISJOINT-MATCHING", "construction", "critical", "Take the supremum of the component-local matchings and derive both matching and M1-disjointness invariants.", "forall {V : Type u} {G : SimpleGraph V} {M1 : G.Subgraph} (complMatch : G.deleteUniversalVerts.coe.ConnectedComponent -> G.Subgraph), M1.IsMatching -> (forall K, (complMatch K).verts = Subtype.val '' K.supp \\ M1.verts /\\ (complMatch K).IsMatching) -> let M2 := iSup complMatch; M2.IsMatching /\\ Disjoint M1.support M2.support", "A global matching M2 together with the required disjointness from M1.", "Tutte.lean:93-104; Matching.lean:128-142", "Derive pairwise support disjointness from distinct connected-component supports, apply matching closure under iSup, and lift the exact residual-vertex equations to M1 support disjointness.", 38, formal_kind="planned_lean_signature"),
    spec("L-UNCOVERED-SUBSET", "core_lemma", "high", "Show every vertex left uncovered by M1 and the component-local supremum is universal.", "forall {V : Type u} {G : SimpleGraph V} (M1 : G.Subgraph) (complMatch : G.deleteUniversalVerts.coe.ConnectedComponent -> G.Subgraph), (forall K, (complMatch K).verts = Subtype.val '' K.supp \\ M1.verts) -> let M2 := iSup complMatch; (M1.verts \u222a M2.verts)ᶜ \u2286 G.universalVerts", "The exact near-cover property needed for the supremum matching.", "Tutte.lean:105-116", "For a non-universal vertex, choose its component in deleteUniversalVerts; if it is not in M1, the exact component-local vertex equation places it in the supremum.", 24, formal_kind="planned_lean_signature"),
    spec("C-COMPLEMENT-MATCHING", "construction", "critical", "Derive evenness of the uncovered universal vertices and match them.", "forall {V : Type u} {G : SimpleGraph V} [Finite V] (M : G.Subgraph), Even (Nat.card V) -> M.IsMatching -> M.vertsᶜ \u2286 G.universalVerts -> exists M' : G.Subgraph, M'.verts = M.vertsᶜ /\\ M'.IsMatching", "A matching M' with vertices exactly M.verts complement, with complement parity derived rather than assumed.", "Tutte.lean:126-130", "Combine even total order with the matching's even vertex count to derive complement parity, inherit the universal-vertex clique, and apply the finite clique matching equivalence.", 30, formal_kind="planned_lean_signature"),
    spec("C-SUP-PERFECT", "construction", "high", "Take the disjoint supremum of the near-covering and complement matchings.", "forall {V : Type u} {G : SimpleGraph V} {M M' : G.Subgraph}, M.IsMatching -> M'.IsMatching -> M'.verts = M.vertsᶜ -> (M \u2294 M').IsPerfectMatching", "A spanning matching, hence a perfect matching.", "Tutte.lean:131-134", "Prove support disjointness from complementary vertex sets and prove the supremum vertices equal the universe.", 18, formal_kind="planned_lean_signature"),
    spec("B-NONCLIQUE", "branch", "critical", "If one deleted component is not a clique, use maximality to obtain two near-perfect matchings and combine them.", "forall {V : Type u} (Gmax : SimpleGraph V) [Finite V], Gmax.IsMatchingFree -> (forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching) -> Not (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> False", "A perfect matching of Gmax, contradicting matching-freedom.", "Tutte.lean:287-308", "Extract a shortest-path three-vertex pattern, add two missing edges separately, and invoke the near-matching composition.", 18, formal_kind="planned_lean_signature"),
    spec("C-NONCLIQUE-WITNESS", "construction", "high", "Choose a nonclique component, two nonadjacent vertices, and a shortest path between them inside that component.", "forall {V : Type u} (Gmax : SimpleGraph V), Not (forall K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, Gmax.deleteUniversalVerts.coe.IsClique K.supp) -> exists K : Gmax.deleteUniversalVerts.coe.ConnectedComponent, exists x y : K, x ≠ y /\\ Not (K.toSimpleGraph.Adj x y) /\\ exists p : K.toSimpleGraph.Walk x y, p.IsPath /\\ p.length = K.toSimpleGraph.dist x y /\\ 1 < K.toSimpleGraph.dist x y", "A chosen nonclique component, nonadjacent distinct pair, and distance-realizing path of length greater than one.", "Tutte.lean:288-292; Metric.lean:242-247,337-340", "Negate the componentwise clique condition to choose K and its nonadjacent supported vertices, then use connectedness of K.toSimpleGraph to obtain a distance-realizing path and strict distance bound.", 26, formal_kind="planned_lean_signature"),
    spec("L-SHORTEST-PATH-TRIPLE", "core_lemma", "critical", "Extract adjacent x-a-b along the component shortest path and normalize them to ambient vertices.", "forall {V : Type u} (Gmax : SimpleGraph V) {K : Gmax.deleteUniversalVerts.coe.ConnectedComponent} {v w : K} {p : K.toSimpleGraph.Walk v w}, p.length = K.toSimpleGraph.dist v w -> 1 < K.toSimpleGraph.dist v w -> exists x a b : V, Gmax.Adj x a /\\ Gmax.Adj a b /\\ Not (Gmax.Adj x b) /\\ x ≠ b /\\ a \u2209 Gmax.universalVerts", "Ambient vertices x, a, b with two path edges, a missing chord, x distinct from b, and a non-universal.", "Metric.lean:378-389; Tutte.lean:290-298", "Apply exists_adj_adj_not_adj_ne in K.toSimpleGraph, then unfold the induced deleted-component graph and subtype coercions to preserve adjacency, nonadjacency, distinctness, and membership outside universalVerts.", 34, formal_kind="planned_lean_signature"),
    spec("C-EDGE-AUGMENTATIONS", "construction", "critical", "Choose c nonadjacent to a and form the two strict supergraphs adding x-b and a-c.", "forall {V : Type u} (Gmax : SimpleGraph V) (x a b : V), Gmax.Adj x a -> Gmax.Adj a b -> x ≠ b -> Not (Gmax.Adj x b) -> a \u2209 Gmax.universalVerts -> exists c : V, a ≠ c /\\ x ≠ c /\\ b ≠ c /\\ Not (Gmax.Adj c a) /\\ Gmax < Gmax \u2294 SimpleGraph.edge x b /\\ Gmax < Gmax \u2294 SimpleGraph.edge a c", "Two strict edge extensions of Gmax plus every distinctness fact required by the near-matching theorem.", "Tutte.lean:297-305", "Use non-universality of a for c; derive b != c and x != c from the two retained Gmax adjacencies and a-c nonadjacency; then prove both missing-edge strictness conditions.", 28, formal_kind="planned_lean_signature"),
    spec("C-NEAR-MATCHINGS", "construction", "critical", "Use edge-maximal matching-freedom to obtain perfect matchings in both one-edge extensions.", "forall {V : Type u} (Gmax : SimpleGraph V) (x a b c : V), (forall G', G' > Gmax -> exists M : G'.Subgraph, M.IsPerfectMatching) -> Gmax < Gmax \u2294 SimpleGraph.edge x b -> Gmax < Gmax \u2294 SimpleGraph.edge a c -> (exists M1 : (Gmax \u2294 SimpleGraph.edge x b).Subgraph, M1.IsPerfectMatching) /\\ (exists M2 : (Gmax \u2294 SimpleGraph.edge a c).Subgraph, M2.IsPerfectMatching)", "Perfect matchings M1 and M2 on the two augmented graphs.", "Tutte.lean:300-306", "Apply the maximality certificate to each strict supergraph and preserve which artificial edge belongs to which graph.", 16, formal_kind="planned_lean_signature"),
    spec("T-NEAR-TO-PERFECT", "terminal", "critical", "Combine perfect matchings from the two one-edge extensions into a perfect matching of the original graph.", "forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G \u2294 SimpleGraph.edge x b).Subgraph} {M2 : (G \u2294 SimpleGraph.edge a c).Subgraph}, G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> exists M : G.Subgraph, M.IsPerfectMatching", "Exists M : Subgraph Gmax, M.IsPerfectMatching.", "Tutte.lean:153-262", "Return an extension matching directly when it omits its added edge; otherwise use an alternating cycle in the symmetric difference and toggle it.", 30, formal_kind="planned_lean_signature"),
    spec("B-FIRST-EXTRA-ABSENT", "branch", "high", "If M1 omits the artificial edge x-b, restrict M1 to Gmax.", "forall {V : Type u} {G : SimpleGraph V} {x b : V} {M1 : (G \u2294 SimpleGraph.edge x b).Subgraph}, M1.IsPerfectMatching -> Not (M1.Adj x b) -> exists M : G.Subgraph, M.IsPerfectMatching", "A perfect matching of the original graph.", "Tutte.lean:160-163", "Use toSubgraph with the spanning-coefficient inclusion and transport perfect matching across the restriction.", 14, formal_kind="planned_lean_signature"),
    spec("B-SECOND-EXTRA-ABSENT", "branch", "high", "If M2 omits the artificial edge a-c, restrict M2 to Gmax.", "forall {V : Type u} {G : SimpleGraph V} {a c : V} {M2 : (G \u2294 SimpleGraph.edge a c).Subgraph}, M2.IsPerfectMatching -> Not (M2.Adj a c) -> exists M : G.Subgraph, M.IsPerfectMatching", "A perfect matching of the original graph.", "Tutte.lean:164-166", "Use the symmetric restriction argument for the second augmented graph.", 12, formal_kind="planned_lean_signature"),
    spec("B-BOTH-EXTRA-PRESENT", "branch", "critical", "When both augmented perfect matchings contain their artificial edges, splice them with an alternating symmetric-difference cycle.", "forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G \u2294 SimpleGraph.edge x b).Subgraph} {M2 : (G \u2294 SimpleGraph.edge a c).Subgraph}, G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x ≠ b -> x ≠ c -> a ≠ c -> b ≠ c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> exists M : G.Subgraph, M.IsPerfectMatching", "A perfect matching of the original graph after the cycle-support subcase.", "Tutte.lean:167-262", "Establish the symmetric-difference invariants, split whether its c-component contains x, and toggle M2 along the resulting alternating cycle.", 18, formal_kind="planned_lean_signature"),
    spec("C-SYMDIFF-CYCLES", "construction", "critical", "When both artificial edges occur, form the symmetric difference of the two perfect matchings as alternating cycles.", "forall {V : Type u} {G : SimpleGraph V} {x a b c : V} {M1 : (G \u2294 SimpleGraph.edge x b).Subgraph} {M2 : (G \u2294 SimpleGraph.edge a c).Subgraph}, G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x \u2260 b -> x \u2260 c -> a \u2260 c -> b \u2260 c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> let cycles := M1.spanningCoe \u2206 M2.spanningCoe; cycles.IsAlternating M2.spanningCoe /\\ cycles.IsCycles /\\ cycles.Adj a c /\\ ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe \u2264 (G \u2294 SimpleGraph.edge a c) \u2294 SimpleGraph.edge x b", "The symmetric-difference cycles are alternating with respect to M2, contain a-c, and place c's component inside the two-edge ambient graph.", "Tutte.lean:167-194; Matching.lean:413-429 and isAlternating_symmDiff_right", "Derive that M1 omits a-c, prove alternation and the cycles property, expose a-c in the symmetric difference, and retain the component inclusion used by both support branches.", 38, formal_kind="planned_lean_signature"),
    spec("B-CYCLE-SUPPORT-SPLIT", "branch", "critical", "Split whether x lies in the support of the symmetric-difference component containing c and recompose the common alternating-cycle contract.", "forall {V : Type u} {G cycles : SimpleGraph V} {x b a c : V} {M2 : (G \u2294 SimpleGraph.edge a c).Subgraph}, (x \u2209 (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\\ G'.IsCycles /\\ Not (G'.Adj x b) /\\ G'.Adj a c /\\ G' \u2264 G \u2294 SimpleGraph.edge a c) -> (x \u2208 (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\\ G'.IsCycles /\\ Not (G'.Adj x b) /\\ G'.Adj a c /\\ G' \u2264 G \u2294 SimpleGraph.edge a c) -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\\ G'.IsCycles /\\ Not (G'.Adj x b) /\\ G'.Adj a c /\\ G' \u2264 G \u2294 SimpleGraph.edge a c", "An alternating cycles graph satisfying the identical inclusion and edge-incidence contract in either exhaustive support subcase.", "Tutte.lean:195-262", "Use classical case analysis on support membership, invoke exactly one child branch, and return its full common contract rather than only the excluded-middle proposition.", 12, formal_kind="planned_lean_signature"),
    spec("B-CYCLE-AVOIDS-X", "branch", "high", "If the symmetric-difference component containing c avoids x, use that component cycle directly.", "forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G \u2294 SimpleGraph.edge x b).Subgraph} {M2 : (G \u2294 SimpleGraph.edge a c).Subgraph} (cycles : SimpleGraph V), cycles = M1.spanningCoe \u2206 M2.spanningCoe -> G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x \u2260 b -> x \u2260 c -> a \u2260 c -> b \u2260 c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> cycles.IsAlternating M2.spanningCoe -> cycles.IsCycles -> cycles.Adj a c -> ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe \u2264 (G \u2294 SimpleGraph.edge a c) \u2294 SimpleGraph.edge x b -> x \u2209 (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\\ G'.IsCycles /\\ Not (G'.Adj x b) /\\ G'.Adj a c /\\ G' \u2264 G \u2294 SimpleGraph.edge a c", "The c-component yields an alternating cycles graph containing a-c, avoiding x-b, and lying in G sup edge a c.", "Tutte.lean:195-206", "Restrict to the connected component, inherit alternation and the cycles property, use a-c to retain the component, and remove the only extra x-b edge using x's absence from the support.", 24, formal_kind="planned_lean_signature"),
    spec("B-CYCLE-CONTAINS-X", "branch", "critical", "If that component contains x, cut a cycle path before an occurrence of x or b and close it with x-a.", "forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G \u2294 SimpleGraph.edge x b).Subgraph} {M2 : (G \u2294 SimpleGraph.edge a c).Subgraph} (cycles : SimpleGraph V), cycles = M1.spanningCoe \u2206 M2.spanningCoe -> G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x \u2260 b -> x \u2260 c -> a \u2260 c -> b \u2260 c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> cycles.IsAlternating M2.spanningCoe -> cycles.IsCycles -> cycles.Adj a c -> ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe \u2264 (G \u2294 SimpleGraph.edge a c) \u2294 SimpleGraph.edge x b -> x \u2208 (cycles.connectedComponentMk c).supp -> exists G' : SimpleGraph V, G'.IsAlternating M2.spanningCoe /\\ G'.IsCycles /\\ Not (G'.Adj x b) /\\ G'.Adj a c /\\ G' \u2264 G \u2294 SimpleGraph.edge a c", "The truncated-path construction yields the same full alternating cycles contract as the avoid-x branch.", "Tutte.lean:207-262", "Use finite local finiteness, extract and truncate the component cycle, prove the terminal matching edge, then invoke the alternating-cycle augmentation in the x or b endpoint subcase.", 34, formal_kind="planned_lean_signature"),
    spec("C-TRUNCATED-PATH", "construction", "critical", "Construct a path from a to x or b that contains a-c, omits x-b, lies in the second augmentation, and ends with the required M2 edge.", "forall {V : Type u} [Finite V] {G : SimpleGraph V} {x a b c : V} {M1 : (G \u2294 SimpleGraph.edge x b).Subgraph} {M2 : (G \u2294 SimpleGraph.edge a c).Subgraph} (cycles : SimpleGraph V), cycles = M1.spanningCoe \u2206 M2.spanningCoe -> G.Adj x a -> G.Adj a b -> Not (G.Adj x b) -> Not (G.Adj a c) -> x \u2260 b -> x \u2260 c -> a \u2260 c -> b \u2260 c -> M1.IsPerfectMatching -> M2.IsPerfectMatching -> M1.Adj x b -> M2.Adj a c -> cycles.IsAlternating M2.spanningCoe -> cycles.IsCycles -> cycles.Adj a c -> ((cycles.connectedComponentMk c).toSimpleGraph).spanningCoe \u2264 (G \u2294 SimpleGraph.edge a c) \u2294 SimpleGraph.edge x b -> x \u2208 (cycles.connectedComponentMk c).supp -> exists x' : V, (x' = x \\/ x' = b) /\\ exists p : cycles.Walk a x', p.IsPath /\\ p.toSubgraph.Adj a c /\\ Not (p.toSubgraph.Adj x b) /\\ p.toSubgraph.spanningCoe \u2264 G \u2294 SimpleGraph.edge a c /\\ forall c' : V, c' \u2260 a -> p.toSubgraph.Adj c' x' -> M2.Adj c' x'", "A simple path whose endpoint, a-c edge, x-b exclusion, ambient inclusion, and terminal M2-edge contract are all explicit.", "Tutte.lean:207-253", "Select and truncate the component cycle, prove the path inclusion after deleting x-b, and use matching uniqueness at x or b to derive the terminal M2 edge needed by the augmentation lemma.", 52, formal_kind="planned_lean_signature"),
    spec("L-ALTERNATING-CYCLE-AUGMENT", "core_lemma", "critical", "Close the truncated alternating path with edge x-a while preserving cycle and edge-exclusion invariants.", "forall {V : Type u} {G G' : SimpleGraph V} {x b a c : V} {M : (G \u2294 SimpleGraph.edge a c).Subgraph} (p : G'.Walk a x), p.IsPath -> G'.IsAlternating M.spanningCoe -> Not (M.Adj x a) -> p.toSubgraph.Adj a c -> Not (p.toSubgraph.Adj x b) -> M.Adj a c -> G.Adj x a -> x ≠ c -> a ≠ b -> p.toSubgraph.spanningCoe \u2264 G \u2294 SimpleGraph.edge a c -> ((c' : V) -> c' ≠ a -> p.toSubgraph.Adj c' x -> M.Adj c' x) -> exists G'', G''.IsAlternating M.spanningCoe /\\ G''.IsCycles /\\ Not (G''.Adj x b) /\\ G''.Adj a c /\\ G'' \u2264 G \u2294 SimpleGraph.edge a c", "An alternating cycles graph containing a-c, excluding x-b, and lying in G sup edge a c.", "Tutte.lean:39-56,254-262", "Take the path spanning graph sup the closing edge, prove degree two, alternating parity, and the required graph inclusion.", 32, formal_kind="planned_lean_signature"),
    spec("L-SYMDIFF-PRESERVES-PERFECT", "core_lemma", "critical", "Derive that toggling the second augmented matching along the selected alternating cycles graph lies in G, then transport perfectness.", "forall {V : Type u} {G G' : SimpleGraph V} {a c : V} {M : (G \u2294 SimpleGraph.edge a c).Subgraph}, M.IsPerfectMatching -> G'.IsAlternating M.spanningCoe -> G'.IsCycles -> G'.Adj a c -> M.Adj a c -> G' \u2264 G \u2294 SimpleGraph.edge a c -> exists hle : M.spanningCoe \u2206 G' \u2264 G, (G.toSubgraph (M.spanningCoe \u2206 G') hle).IsPerfectMatching", "A derived inclusion and the corresponding explicit symmetric-difference perfect matching in G.", "Matching.lean:576-604; Tutte.lean:173-181", "Derive the inclusion from the augmented-graph bounds and cancellation of the artificial a-c edge present in both M and G'; then apply symmetric-difference preservation and transport the exact graph through G.toSubgraph.", 46, formal_kind="planned_lean_signature"),
    spec("X-SOURCE", "terminal", "high", "Map every material mathematical node to a pinpoint primary proof source, incorporated definitions, assumptions, and corrections.", "stage1-source-crosswalk-record/1.0", "An independently reviewed H0 crosswalk for the complete route.", "source-statement-crosswalk.md; primary 1947 article lead", "Preserve an admitted edition and map each source transition to the frozen nodes; a bibliographic identity alone does not close this obligation.", 90, machine_eligibility="not_applicable", formal_kind="nonformal_record"),
    spec("X-PROVENANCE", "certificate", "critical", "Bind local wrappers, the single exact terminal body, support declarations, private source segments, hashes, origin, license, and transitive dependencies.", "stage1-provenance-closure-record/1.0", "Release-grade proof-body provenance without duplicate root credit.", "anchor-audit.json provenance_packet", "Traverse actual declaration bodies and deduplicate the local adapter and Atlas wrapper from the sole SimpleGraph.tutte terminal body.", 90, machine_eligibility="informational", human_source_eligibility="not_applicable", formal_kind="nonformal_record"),
    spec("X-TRUST", "certificate", "critical", "Close the transitive axiom, unsafe-code, compiled-artifact, executable, dependency, and TCB inventory.", "stage1-trust-closure-record/1.0", "Accepted trust closure under the selected foundation policy.", "anchor-audit.json trust_boundary", "Hash and classify every trusted element, then perform cold offline and independent replay; unknown trust fails closed.", 90, machine_eligibility="informational", human_source_eligibility="not_applicable", formal_kind="nonformal_record"),
    spec("X-DOCUMENTATION", "terminal", "high", "Provide a stable reader-facing entry and exact formal/source boundary for every readable obligation.", "stage1-readable-crosswalk-record/1.0", "Node-specific readable records and independent R0 review receipts.", "obligation-tree.md", "Reconstruct the accepted proof route in graph-theory language while keeping architecture plans distinct from completed proof claims.", 90, machine_eligibility="informational", human_source_eligibility="not_applicable", formal_kind="nonformal_record"),
    spec("X-WORKFLOW", "terminal", "critical", "Enforce dependency legality from anchor acceptance through proof, validation, release, invalidation, and revocation.", "stage1-workflow-state-record/1.0", "Only dependency-legal provisional or accepted execution states.", "Docs/Stage1_Execution_DAG_rev-5.6.json; task-dag.json", "Bind task-to-obligation links and reject any downstream acceptance before its prerequisites and receipts are accepted.", 30, machine_eligibility="informational", human_source_eligibility="not_applicable", formal_kind="nonformal_record"),
]


REQUIRES = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ADAPTER", f"{PREFIX}-T-UPSTREAM"],
    f"{PREFIX}-T-UPSTREAM": [f"{PREFIX}-T-NECESSITY", f"{PREFIX}-T-SUFFICIENCY"],
    f"{PREFIX}-T-NECESSITY": [f"{PREFIX}-L-ODD-MATCHES-OUTSIDE", f"{PREFIX}-C-ODD-TO-U-INJECTION", f"{PREFIX}-L-NCARD-INJECTION"],
    f"{PREFIX}-T-SUFFICIENCY": [f"{PREFIX}-B-PARITY-SPLIT"],
    f"{PREFIX}-B-PARITY-SPLIT": [f"{PREFIX}-B-ODD-CARD", f"{PREFIX}-B-EVEN-CARD"],
    f"{PREFIX}-B-ODD-CARD": [f"{PREFIX}-L-EMPTY-VIOLATOR"],
    f"{PREFIX}-B-EVEN-CARD": [f"{PREFIX}-L-EXISTS-VIOLATOR"],
    f"{PREFIX}-L-EXISTS-VIOLATOR": [f"{PREFIX}-N-FINITE-INTERFACES", f"{PREFIX}-C-MAXIMAL-MATCHING-FREE", f"{PREFIX}-L-VIOLATOR-MONO", f"{PREFIX}-C-UNIVERSAL-DELETION", f"{PREFIX}-B-CLIQUE-SPLIT"],
    f"{PREFIX}-B-CLIQUE-SPLIT": [f"{PREFIX}-B-ALL-CLIQUES", f"{PREFIX}-B-NONCLIQUE"],
    f"{PREFIX}-B-ALL-CLIQUES": [f"{PREFIX}-T-CLIQUE-PERFECT"],
    f"{PREFIX}-T-CLIQUE-PERFECT": [f"{PREFIX}-N-FINITE-INTERFACES", f"{PREFIX}-C-NEAR-COVER-MATCHING", f"{PREFIX}-C-COMPLEMENT-MATCHING", f"{PREFIX}-C-SUP-PERFECT"],
    f"{PREFIX}-C-NEAR-COVER-MATCHING": [f"{PREFIX}-C-ODD-REPRESENTATIVES", f"{PREFIX}-C-MATCH-REPS-UNIVERSALS", f"{PREFIX}-C-INTERNAL-COMPONENT-MATCHINGS", f"{PREFIX}-C-ISUP-DISJOINT-MATCHING", f"{PREFIX}-L-UNCOVERED-SUBSET"],
    f"{PREFIX}-B-NONCLIQUE": [f"{PREFIX}-C-NONCLIQUE-WITNESS", f"{PREFIX}-L-SHORTEST-PATH-TRIPLE", f"{PREFIX}-C-EDGE-AUGMENTATIONS", f"{PREFIX}-C-NEAR-MATCHINGS", f"{PREFIX}-T-NEAR-TO-PERFECT"],
    f"{PREFIX}-T-NEAR-TO-PERFECT": [f"{PREFIX}-B-FIRST-EXTRA-ABSENT", f"{PREFIX}-B-SECOND-EXTRA-ABSENT", f"{PREFIX}-B-BOTH-EXTRA-PRESENT"],
    f"{PREFIX}-B-BOTH-EXTRA-PRESENT": [f"{PREFIX}-C-SYMDIFF-CYCLES", f"{PREFIX}-B-CYCLE-SUPPORT-SPLIT", f"{PREFIX}-L-SYMDIFF-PRESERVES-PERFECT"],
    f"{PREFIX}-B-CYCLE-SUPPORT-SPLIT": [f"{PREFIX}-B-CYCLE-AVOIDS-X", f"{PREFIX}-B-CYCLE-CONTAINS-X"],
    f"{PREFIX}-B-CYCLE-CONTAINS-X": [f"{PREFIX}-C-TRUNCATED-PATH", f"{PREFIX}-L-ALTERNATING-CYCLE-AUGMENT"],
}


REGISTRY_FIELDS = (
    "obligation_id",
    "statement_fingerprint",
    "kind",
    "root_relevant",
    "machine_eligibility",
    "human_source_eligibility",
    "readable_eligibility",
    "risk_class",
    "exclusion_reason",
    "terminal_proof_body_id",
)


def canonical_digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def planned_declaration(oid: str) -> str:
    return "Stage1Instances.THM_M_0856.ObligationSignatures." + oid.replace("-", "_")


def formal_target_record(row: dict) -> dict:
    kind = row["formal_kind"]
    target = EXACT_TYPES.get(row["id"], row["formal"])
    declaration = row["formal_declaration"]
    if kind == "exact_lean_type":
        declaration = declaration or EXACT_DECLARATIONS[row["id"]]
        fingerprint_basis = {
            "kind": kind,
            "declaration": declaration,
            "type_interface": target,
            "environment": f"lean4.29.0-mathlib-{MATHLIB_REVISION}",
        }
    elif kind == "planned_lean_signature":
        declaration = planned_declaration(row["id"])
        fingerprint_basis = {
            "kind": kind,
            "declaration": declaration,
            "signature": target,
            "syntax": "Lean 4 surface syntax elaborated by generated ObligationSignatures.lean",
        }
    elif kind == "nonformal_record":
        fingerprint_basis = {"kind": kind, "record_schema_or_pointer": target}
    else:
        raise ValueError(f"unknown formal target kind: {kind}")
    return {
        "kind": kind,
        "declaration": declaration,
        "type_or_record": target,
        "fingerprint": "sha256:" + canonical_digest(fingerprint_basis),
        "fingerprint_basis": fingerprint_basis,
    }


def build_signature_source() -> str:
    lines = [
        "import ObligationTree",
        "",
        "set_option autoImplicit false",
        "",
        "/-! Generated exact-declaration probes and planned proposition signatures for THM-M-0856. -/",
        "",
        "namespace Stage1Instances.THM_M_0856.ObligationSignatures",
        "",
        "universe u v",
        "",
        "open SimpleGraph",
        "open scoped symmDiff",
        "",
    ]
    seen_exact = set()
    for row in SPECS:
        target = formal_target_record(row)
        if target["kind"] == "planned_lean_signature":
            name = target["declaration"].rsplit(".", 1)[1]
            lines.extend(
                [
                    f"/-- Frozen planned interface for `{row['id']}`; this definition grants no proof closure. -/",
                    f"def {name} : Prop := {target['type_or_record']}",
                    "",
                ]
            )
        elif target["kind"] == "exact_lean_type" and target["declaration"] not in seen_exact:
            if row["id"] in {"M0856-ROOT", "M0856-S-TARGET"}:
                lines.append(
                    f"#check (rfl : @{target['declaration']}.{{u}} = ({target['type_or_record']}))"
                )
            else:
                lines.append(
                    f"#check (@{target['declaration']} : {target['type_or_record']})"
                )
            seen_exact.add(target["declaration"])
    lines.extend(["", "end Stage1Instances.THM_M_0856.ObligationSignatures", ""])
    return "\n".join(lines)


def build() -> tuple[dict, dict, dict, str, str]:
    execution_path = ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    execution = json.loads(execution_path.read_text())
    authoritative_tasks = [
        item for item in execution["items"] if item["theorem_id"] == THEOREM_ID
    ]
    if len(authoritative_tasks) != 7:
        raise SystemExit("expected exactly seven authoritative THM-M-0856 tasks")

    obligations = []
    nodes = []
    for row in SPECS:
        oid = row["id"]
        formal_target = formal_target_record(row)
        if oid in {f"{PREFIX}-ROOT", f"{PREFIX}-S-TARGET"}:
            fingerprint = "lean-expression-sha256:" + ROOT_EXPRESSION
        else:
            payload = "\0".join(
                (oid, row["claim"], formal_target["fingerprint"], row["output"])
            ).encode()
            fingerprint = "architecture:v1:sha256:" + hashlib.sha256(payload).hexdigest()
        exclusion = None
        if row["machine_eligibility"] != "required":
            exclusion = (
                "human_source_boundary_no_machine_proof_credit"
                if row["machine_eligibility"] == "not_applicable"
                else "typed_overlay_or_statement_interface_no_duplicate_machine_proof_credit"
            )
        obligations.append(
            {
                "obligation_id": oid,
                "statement_fingerprint": fingerprint,
                "kind": row["kind"],
                "root_relevant": True,
                "machine_eligibility": row["machine_eligibility"],
                "human_source_eligibility": row["human_source_eligibility"],
                "readable_eligibility": "required",
                "risk_class": row["risk"],
                "exclusion_reason": exclusion,
                "terminal_proof_body_id": row["terminal_body"],
            }
        )
        child_ids = REQUIRES.get(oid, [])
        step = {
            "step_id": f"{oid}-STEP-01",
            "premise_ids": child_ids or ["frozen-formal-context"],
            "inference": row["method"],
            "source_locator": row["source"],
            "output": row["output"],
            "outgoing_use": (
                "Supplies this exact output only to the declared parent relations; it grants no accepted closure in this phase."
            ),
        }
        nodes.append(
            {
                "node_id": f"{THEOREM_ID}-{oid.removeprefix(PREFIX + '-')}",
                "obligation_id": oid,
                "kind": row["kind"],
                "human_statement": row["claim"],
                "formal_target": formal_target,
                "output": row["output"],
                "human_debt": "H1",
                "machine_debt": "M3",
                "readability_debt": "R4",
                "evidence_ids": [],
                "source_crosswalk_id": (
                    "source-statement-crosswalk.md; node pinpoint review pending"
                    if row["human_source_eligibility"] == "required"
                    else "not_applicable"
                ),
                "provenance_id": (
                    "anchor-audit.json#provenance_packet; proof-phase acceptance pending"
                    if row["terminal_body"]
                    else "none"
                ),
                "foundation_profile": "lean4-foundation-planned/1.0; accepted transitive axiom policy remains open",
                "tcb_profile": "lean4-mathlib-tcb-planned/1.0; Lean 4.29.0 plus mathlib 8a178386; full closure remains open",
                "computation_record": "not_applicable_pending_independent_approval; no solver, native computation, oracle, randomized search, or unchecked certificate is credited",
                "step_budget": row["budget"],
                "semantic_step_ledger": {
                    "premises": child_ids or ["frozen-formal-context"],
                    "inference": row["method"],
                    "source_anchors": [row["source"]],
                    "output": row["output"],
                    "outgoing_use": step["outgoing_use"],
                    "steps": [step],
                },
                "public_readable_target": f"Stage1_Instances/THM-M-0856/obligation-tree.md#{oid.lower()}",
                "validation_spec_id": "VAL-M0856-OBLIGATION-BUNDLE",
                "status_boundary": "Frozen architecture and source-body mapping only; no M0, H0, R0, accepted node closure, AUDIT-Z, or theorem completion is claimed.",
                "task_ids": [ITEM_ID, "S56-M-0856-PROOF"],
                "owned_sources": [
                    "Stage1_Instances/THM-M-0856/obligation-registry.json",
                    "Stage1_Instances/THM-M-0856/typed-graphs.json",
                    f"Stage1_Instances/THM-M-0856/obligation-tree.md#{oid.lower()}",
                ],
                "owner": "THM-M-0856 proof lane",
                "reviewer": "unassigned independent Stage1 graph-theory and Lean reviewer",
                "validity": {
                    "validated_at": None,
                    "review_due": "before master acceptance of this obligation-tree node",
                    "invalidation_inputs": [
                        "Statement.lean or statement fingerprint",
                        "anchor-audit.json or candidate inventory",
                        "obligation registry or typed graphs",
                        "Tutte source or terminal body identity",
                        "toolchain, dependency pin, or assurance profile",
                    ],
                    "revocation_state": "open_not_accepted",
                },
            }
        )

    projection = [{key: item[key] for key in REGISTRY_FIELDS} for item in obligations]
    denominator = canonical_digest(projection)
    ids = [row["id"] for row in SPECS]
    proof_children = {child for children in REQUIRES.values() for child in children}
    proof_leaves = sorted(proof_children - set(REQUIRES))
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "registry_id": "THM-M-0856-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": FROZEN_AT,
        "freeze_basis": "The exact elaborated target and immutable anchor inventory fix the necessity, parity, maximal matching-free, universal-clique, nonclique near-matching, source, provenance, trust, documentation, and workflow architecture. Eligibility was fixed before any proof-phase closure credit.",
        "frozen_against_statement_sha256": sha256(HERE / "Statement.lean"),
        "frozen_against_anchor_audit_sha256": sha256(HERE / "anchor-audit.json"),
        "root_obligation_id": f"{PREFIX}-ROOT",
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [item["obligation_id"] for item in obligations if item["machine_eligibility"] == "required"],
            "required_human_source": [item["obligation_id"] for item in obligations if item["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [item["obligation_id"] for item in obligations if item["machine_eligibility"] != "required"],
            "required_unique_logical_leaves": proof_leaves,
        },
        "layer_applicability": {
            "S_statement_foundation": {"state": "required", "obligation_ids": [f"{PREFIX}-S-TARGET", f"{PREFIX}-S-DOMAIN", f"{PREFIX}-S-MATCHING", f"{PREFIX}-S-ODD-CONDITION", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-S-FOUNDATION"]},
            "N_normalization": {"state": "required", "obligation_ids": [f"{PREFIX}-N-FINITE-INTERFACES"]},
            "B_branch": {"state": "required", "obligation_ids": [oid for oid in ids if "-B-" in oid]},
            "C_construction": {"state": "required", "obligation_ids": [oid for oid in ids if "-C-" in oid]},
            "L_core_lemma": {"state": "required", "obligation_ids": [oid for oid in ids if "-L-" in oid]},
            "X_external_computation": {
                "state": "required_external_boundary_and_not_applicable_computation_pending_independent_approval",
                "reason": "Pinned theorem bodies, source, provenance, trust, documentation, and workflow are material. The proof is symbolic and uses no solver, experiment, finite search, oracle, native evaluation, or certificate.",
                "obligation_ids": [f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-DOCUMENTATION", f"{PREFIX}-X-WORKFLOW"],
                "reviewer": "unassigned independent Lean and TCB reviewer",
            },
            "T_terminal": {"state": "required", "obligation_ids": [f"{PREFIX}-ROOT", f"{PREFIX}-T-ADAPTER", f"{PREFIX}-T-UPSTREAM", f"{PREFIX}-T-NECESSITY", f"{PREFIX}-T-SUFFICIENCY", f"{PREFIX}-T-CLIQUE-PERFECT", f"{PREFIX}-T-NEAR-TO-PERFECT"]},
        },
        "deduplication_policy": "SimpleGraph.tutte owns the sole exact root terminal body. The local adapter, pinned wrapper, direction declarations, Atlas wrapper, statement transports, and private source segments cannot create duplicate root or body credit.",
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility, risk, source-body, or terminal-body identity change requires registry v2 with an append-only old/new ID delta; v1 denominators remain reportable.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "checked_root_composition": f"{PREFIX}-ROOT",
            "checked_candidate_interfaces": [f"{PREFIX}-T-ADAPTER", f"{PREFIX}-T-UPSTREAM"],
            "unverified_internal_decomposition_parents": [oid for oid in REQUIRES if oid != f"{PREFIX}-ROOT"],
            "candidate_classification": "M3_node_local_below_E1",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. The exact pinned route is not proof-phase accepted; H0, M0, R0, audit completion, release validation, and theorem completion remain open.",
    }

    graph_names = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
    graphs = {name: {"edges": [], "out": {}, "in": {}} for name in graph_names}

    def add_edge(graph: str, edge: dict) -> None:
        graphs[graph]["edges"].append(edge)
        graphs[graph]["out"].setdefault(edge["from"], []).append(edge["edge_id"])
        graphs[graph]["in"].setdefault(edge["to"], []).append(edge["edge_id"])

    pair_index = 0
    for parent, children in REQUIRES.items():
        for child in children:
            pair_index += 1
            req = f"P{pair_index:03d}-REQ"
            reverse = f"P{pair_index:03d}-REV"
            reverse_type = "composes" if parent == f"{PREFIX}-ROOT" else "logical_decomposition"
            add_edge("proof", {"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": reverse})
            add_edge("proof", {"edge_id": reverse, "from": child, "type": reverse_type, "to": parent, "reciprocal_edge_id": req})

    for index, child in enumerate(
        [f"{PREFIX}-S-TARGET", f"{PREFIX}-S-DOMAIN", f"{PREFIX}-S-MATCHING", f"{PREFIX}-S-ODD-CONDITION", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-S-FOUNDATION"], 1
    ):
        add_edge("refinement", {"edge_id": f"R{index:02d}", "from": f"{PREFIX}-ROOT", "type": "expository_decomposition", "to": child})

    source_required_ids = registry["frozen_denominators"]["required_human_source"]
    formal_ids = [oid for oid in ids if not oid.startswith(f"{PREFIX}-X-")]
    for index, oid in enumerate(
        (oid for oid in source_required_ids if oid != f"{PREFIX}-X-SOURCE"), 1
    ):
        add_edge("provenance", {"edge_id": f"SRC{index:03d}", "from": oid, "type": "source_map", "to": f"{PREFIX}-X-SOURCE"})
    for index, oid in enumerate(formal_ids, 1):
        add_edge("provenance", {"edge_id": f"PROV{index:03d}", "from": f"{PREFIX}-X-PROVENANCE", "type": "provenance_of", "to": oid})
        if oid != f"{PREFIX}-S-FOUNDATION":
            add_edge("trust", {"edge_id": f"TRUST{index:03d}", "from": oid, "type": "trusts", "to": f"{PREFIX}-X-TRUST"})
    add_edge("trust", {"edge_id": "TRUST-POLICY", "from": f"{PREFIX}-X-TRUST", "type": "trusts", "to": f"{PREFIX}-S-FOUNDATION"})
    for index, oid in enumerate(ids, 1):
        if oid != f"{PREFIX}-X-DOCUMENTATION":
            add_edge("documentation", {"edge_id": f"DOC{index:03d}", "from": f"{PREFIX}-X-DOCUMENTATION", "type": "documents", "to": oid})
    for index, dependency in enumerate([f"{PREFIX}-T-UPSTREAM", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-DOCUMENTATION"], 1):
        add_edge("workflow", {"edge_id": f"FLOW{index:02d}", "from": f"{PREFIX}-X-WORKFLOW", "type": "workflow_depends_on", "to": dependency})

    by_obligation = {item["obligation_id"]: item for item in obligations}
    composition_certificates = [
        {
            "certificate_id": "COMP-M0856-ROOT",
            "parent_obligation_id": f"{PREFIX}-ROOT",
            "parent_statement_fingerprint": by_obligation[f"{PREFIX}-ROOT"]["statement_fingerprint"],
            "required_child_ids": REQUIRES[f"{PREFIX}-ROOT"],
            "required_child_statement_fingerprints": {child: by_obligation[child]["statement_fingerprint"] for child in REQUIRES[f"{PREFIX}-ROOT"]},
            "checked_declaration": "Stage1Instances.THM_M_0856.ObligationTree.compose_root",
            "certificate_kind": "lean_abstract_child_harness",
            "status": "provisionally_elaborated_not_accepted",
            "introduces_undeclared_premises": False,
        }
    ]
    decomposition_plans = [
        {
            "plan_id": "DECOMP-" + parent,
            "parent_obligation_id": parent,
            "parent_statement_fingerprint": by_obligation[parent]["statement_fingerprint"],
            "planned_child_ids": children,
            "planned_child_statement_fingerprints": {child: by_obligation[child]["statement_fingerprint"] for child in children},
            "source_locator": next(row["source"] for row in SPECS if row["id"] == parent),
            "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
            "required_future_certificate": "An exact child-fingerprint harness must consume every listed child and yield the parent before any parent closure credit.",
        }
        for parent, children in REQUIRES.items()
        if parent != f"{PREFIX}-ROOT"
    ]
    task_nodes = [
        {"task_id": item["id"], "phase": item["phase"], "layer": item["layer"]}
        for item in authoritative_tasks
    ]
    task_edges = [
        {"edge_id": f"TASK-{index:02d}", "type": "workflow_depends_on", "from": item["id"], "to": dependency}
        for index, (item, dependency) in enumerate(
            ((item, dependency) for item in authoritative_tasks for dependency in item["depends_on"]), 1
        )
    ]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "frozen_against_execution_dag_sha256": sha256(execution_path),
        "local_task_dag_projection_sha256": sha256(HERE / "task-dag.json"),
        "root_node_id": f"{PREFIX}-ROOT",
        "edge_direction": "proof_requires runs parent to child; checked composes and planned logical_decomposition run child to parent. Non-proof edges never grant proof closure.",
        "evidence_endpoint_policy": "Evidence objects are external content-addressed packets, never semantic obligations or provenance nodes. All current worker receipts are mutable, unaccepted, and content_addressed=false, so the frozen evidence-object registry and evidence graph are empty.",
        "evidence_objects": [],
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": composition_certificates,
        "unverified_decomposition_plans": decomposition_plans,
        "workflow_task_graph": {
            "authority": "Docs/Stage1_Execution_DAG_rev-5.6.json",
            "authority_sha256": sha256(execution_path),
            "nodes": task_nodes,
            "edges": task_edges,
            "task_obligation_links": (
                [{"task_id": ITEM_ID, "obligation_id": oid} for oid in ids]
                + [{"task_id": "S56-M-0856-PROOF", "obligation_id": oid} for oid in registry["frozen_denominators"]["required_machine"]]
                + [{"task_id": task, "obligation_id": oid} for task in ("S56-M-0856-VALIDATION", "S56-M-0856-RELEASE") for oid in (f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-DOCUMENTATION", f"{PREFIX}-X-WORKFLOW")]
            ),
        },
        "closure_boundary": {
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "accepted_closed_obligations": [],
            "checked_conditional_interfaces": [f"{PREFIX}-T-ADAPTER", f"{PREFIX}-T-UPSTREAM", f"{PREFIX}-ROOT"],
            "unverified_internal_decomposition_count": len(decomposition_plans),
            "proof_leaf_cut_set": proof_leaves,
            "remaining_root_cut_set": ["accepted proof-phase receipt for the exact pinned route", "exact composition certificates for all internal source decompositions", "release-grade E1 provenance and trust closure", "primary-source H0 and independent review", "readable R0 and independent review", "hermetic and independent validation", "master acceptance"],
            "distinct_exact_root_terminal_body_ids": [TUTTE_BODY],
            "audit_complete": False,
            "theorem_complete": False,
            "reason": "This phase freezes and checks architecture only. The exact pinned route is below E1 and internal source decompositions are not checked child-to-parent certificates.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "recipes": [
            {
                "recipe_id": "VAL-M0856-OBLIGATION-BUNDLE",
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0856/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS with obligation, typed-edge, and denominator counts plus open H1/M3/R4 root"}],
                "covered_obligation_ids": ids,
                "covered_declarations": ["Stage1Instances.THM_M_0856.TutteOneFactorTarget", "SimpleGraph.tutte", "Stage1Instances.THM_M_0856.ObligationTree.terminal_adapter", "Stage1Instances.THM_M_0856.ObligationTree.pinned_mathlib_terminal", "Stage1Instances.THM_M_0856.ObligationTree.compose_root"],
                "coverage_boundary": "Structural coverage includes every registry node. Lean elaborates every planned signature and checks every named imported declaration, but proof closure remains limited to the root terminal, adapter, wrapper, and conditional composition; internal source decompositions remain open.",
                "closure_credit": False,
            },
            {
                "recipe_id": "VAL-M0856-OBLIGATION-GENERATOR",
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0856/build_obligation_artifacts.py", "--check"],
                "env_allowlist": {},
                "timeout_seconds": 60,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "reports deterministic byte equality for registry, graph, validation-spec, and readable-tree artifacts"}],
                "covered_obligation_ids": ids,
                "covered_declarations": [],
                "coverage_boundary": "Generator drift check only; no proof closure credit.",
                "closure_credit": False,
            },
        ],
    }

    markdown = [
        "# THM-M-0856 frozen obligation architecture",
        "",
        f"Item: `{ITEM_ID}`.",
        "",
        f"Registry version 1 freezes {len(ids)} canonical obligations before proof-phase closure credit.",
        "The proof route follows the actual pinned `SimpleGraph.tutte` body through necessity, parity,",
        "the maximal matching-free supergraph, universal-vertex clique and nonclique branches, the",
        "near-matching symmetric-difference construction, and the exact local adapter. Source,",
        "provenance, evidence, trust, documentation, and workflow edges are separately typed.",
        "",
        "## Composition boundary",
        "",
        "`ObligationTree.lean` checks only the root composition from the exact terminal adapter and",
        "literal pinned terminal. Every internal source-body relation is recorded as an unverified",
        "decomposition plan until an exact child-fingerprint composition harness is accepted. The",
        "pinned candidate therefore remains M3/below E1 here, and no obligation is accepted closed.",
        "",
        "## Proof route",
        "",
        "```text",
        "ROOT -> exact adapter + SimpleGraph.tutte",
        "  necessity -> odd-component matched exits -> injection -> cardinal bound",
        "  sufficiency by contraposition -> parity split",
        "    odd order -> empty-set violator",
        "    even order -> maximal matching-free supergraph -> universal-vertex deletion",
        "      all residual components cliques -> representative/universal/internal matchings",
        "      a residual component nonclique -> two near-matchings",
        "        symmetric-difference cycles -> avoid/contain x branches -> alternating toggle",
        "```",
        "",
        "## Node ledger",
        "",
    ]
    for row, node in zip(SPECS, nodes, strict=True):
        step = node["semantic_step_ledger"]["steps"][0]
        markdown.extend(
            [
                f"### {row['id'].lower()}",
                "",
                row["claim"],
                "",
                f"Formal target kind: `{row['formal_kind']}`.",
                "",
                f"Formal target/type/record: `{row['formal']}`.",
                "",
                f"Formal target fingerprint: `{node['formal_target']['fingerprint']}`.",
                "",
                f"Source locator: `{row['source']}`.",
                "",
                f"Required premises: `{', '.join(step['premise_ids'])}`.",
                "",
                f"Inference: {step['inference']}",
                "",
                f"Output: {row['output']}",
                "",
                "Boundary: frozen architecture only; accepted proof, H0, R0, trust closure, audit",
                "completion, and theorem completion remain open.",
                "",
            ]
        )
    return registry, bundle, recipes, "\n".join(markdown), build_signature_source()


def serialized_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry, bundle, specs, markdown, signatures = build()
    artifacts = {
        "obligation-registry.json": serialized_json(registry),
        "typed-graphs.json": serialized_json(bundle),
        "validation-specs.json": serialized_json(specs),
        "obligation-tree.md": markdown,
        "ObligationSignatures.lean": signatures,
    }
    if args.write:
        for name, content in artifacts.items():
            (HERE / name).write_text(content)
        edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
        print(f"wrote {len(registry['obligations'])} obligations and {edge_count} typed edges")
        print(registry["denominator_sha256"])
        return
    for name, content in artifacts.items():
        if (HERE / name).read_text() != content:
            raise SystemExit(f"generated artifact drift: {name}")
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    print(f"PASS deterministic artifacts: {len(registry['obligations'])} obligations, {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
