#!/usr/bin/env python3
"""Build the frozen THM-M-0821 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0821-OBLIGATION_TREE"
THEOREM = "THM-M-0821"
PREFIX = "M0821-"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
ROOT_EXPRESSION = "8f5d05428a35e3b6f13947097ac52417ba900b3cf9b1b45c0bb173766c914d7c"
INTERFACE_EXPRESSION_FINGERPRINTS = {
    "M0821-ROOT": "lean-expression-sha256:" + ROOT_EXPRESSION,
    "M0821-T-ROOT-COMPOSE": "lean-expression-sha256:" + ROOT_EXPRESSION,
    "M0821-B-MAXIMUM": "lean-expression-sha256:8e02cc3ca1f096aa098134c5c7e84d1b891ba45cf8a24f4f2244e98e14c9f4c9",
    "M0821-T-ATTAIN": "lean-expression-sha256:4d358b258c3e461e3187bb2534edaa2369ba757f4ec1a6fb1dd76e3167f8f0f3",
    "M0821-C-MIDDLE-LAYER": "lean-expression-sha256:3191f7b92bd4ed8d33dc291dfa915cbf80007810cae4bb2221be6990520337b9",
    "M0821-L-MIDDLE-ANTICHAIN": "lean-expression-sha256:3158151734078aac1a57163a39bb3d968735663302a1f5543a5a4d91b2fdd6c7",
    "M0821-C-MIDDLE-SIZED": "lean-expression-sha256:d153343a507b15afe161bae19d47988477c8c2bc099f683c78a0fefe08438e5b",
    "M0821-L-MIDDLE-CARD": "lean-expression-sha256:fa139945a23e43d575b11699af1ef69fd00e686c35ddbec4fe9489fb9ac2fa84",
    "M0821-T-UPPER": "lean-expression-sha256:5a72e63d35d8d9fe0f1c7ff656c91b9604f0ded4810b6ce0dc224d8af0d94116",
    "M0821-L-SPERNER-UPPER": "lean-expression-sha256:5a72e63d35d8d9fe0f1c7ff656c91b9604f0ded4810b6ce0dc224d8af0d94116",
}


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def source_hash(path: str) -> str:
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()


def spec(
    oid: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    output: str,
    locator: str,
    budget: int,
) -> dict:
    return {
        "id": oid,
        "kind": kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "output": output,
        "locator": locator,
        "budget": budget,
    }


SPECS = [
    spec("M0821-ROOT", "root", "critical", "Every finite Boolean lattice has maximum antichain cardinality choose(n, floor(n/2)): the value is attained and bounds every antichain.", "Stage1Instances.THM_M_0821.SpernerMaximumTarget", "The exact frozen root proposition at arbitrary universe u.", "Statement.lean:30-37; expression sha256 8f5d05428a35e3b6f13947097ac52417ba900b3cf9b1b45c0bb173766c914d7c", 12),
    spec("M0821-S-INTERFACE", "definition", "high", "Preserve the arbitrary finite ground type, finite family of finite subsets, strict distinct-member antichain relation, existential witness, and universal bound.", "Stage1Instances.THM_M_0821.SpernerMaximumTarget", "The exact binder and conclusion interface.", "Statement.lean:16-37; statement.json", 22),
    spec("M0821-S-BOUNDARY", "definition", "high", "Include empty and singleton ground types and families, both parities, natural floor division, and no equality-classification claim.", "(Stage1Instances.THM_M_0821.middleLayer (Fin 0) = {∅}) /\\ (Stage1Instances.THM_M_0821.middleLayer (Fin 1) = {∅})", "No strengthened premise, omitted degenerate case, or stronger equality conclusion.", "Statement.lean:30-37,64-70; statement.json encoding_decisions", 18),
    spec("M0821-S-TRANSPORT", "transport", "high", "Relate the existential maximum target to the concrete lower-middle-layer form without using the Sperner upper-bound proof.", "Stage1Instances.THM_M_0821.spernerMaximumTarget_iff_middleLayerMaximumTarget", "A checked iff with the universal-bound conjunct unchanged.", "Statement.lean:39-62", 18),
    spec("M0821-S-FOUNDATION", "certificate", "critical", "Account for propext, Classical.choice, Quot.sound, the Lean/mathlib pins, imports, and the no-oracle policy.", "planned signature: every checked declaration in validation-specs.json has a machine-derived axiom set contained in {propext, Classical.choice, Quot.sound} and no prohibited proof boundary", "A versioned foundation, TCB, and computation boundary.", "ObligationTree.lean axiom probes; anchor-audit.json immutable_environment", 24),
    spec("M0821-N-LOWER-MIDDLE", "normalization", "normal", "Select floor(n/2) as the canonical lower middle rank; for odd n the adjacent upper rank has equal size but is unnecessary for the maximum value.", "forall r n : Nat, Nat.choose n r <= Nat.choose n (n / 2)", "The canonical rank and maximal binomial coefficient used by both branches.", "Statement.lean:21-23; LYM.lean:236-243; Nat.choose_le_middle", 20),
    spec("M0821-N-NO-OTHER", "normalization", "low", "Record that the chosen mathlib route needs no further symmetry, representation, finite/infinite, or local/global normalization.", "planned review proposition: the proof graph is total on the frozen finite Boolean-lattice encoding without another normalization node", "A reviewed layer-exclusion decision only; no proof premise.", "Blueprint section 6.4; target finite Boolean-lattice encoding", 8),
    spec("M0821-B-MAXIMUM", "branch", "high", "Split the exact maximum claim into attainment and universal upper-bound branches and recombine both exhaustively.", "Stage1Instances.THM_M_0821_Obligations.AttainmentPackage -> Stage1Instances.THM_M_0821_Obligations.UpperBoundPackage -> Stage1Instances.THM_M_0821_Obligations.MaximumSplit", "Both conjuncts required by the root.", "ObligationTree.lean:91-95", 12),
    spec("M0821-B-NO-CASES", "branch", "low", "Record that the pinned proof is uniform over ground-set cardinality and parity after the maximum-conjunction split.", "planned review proposition: IsAntichain.sperner has no parity or cardinality case split outside its internal uniform inequalities", "A reviewed no-additional-case-split decision only.", "LYM.lean:232-245; Statement.lean boundary probes", 8),
    spec("M0821-C-MIDDLE-LAYER", "construction", "normal", "Construct the lower-middle layer as powersetCard floor(n/2) univ.", "Stage1Instances.THM_M_0821_Obligations.MiddleLayerDefinitionPackage", "The explicit finite family used as an extremizer.", "Statement.lean:21-23; ObligationTree.lean:30-34,119-122", 14),
    spec("M0821-C-MIDDLE-SIZED", "construction", "normal", "Show that every subset in the raw lower-middle powerset slice has cardinality floor(n/2).", "Stage1Instances.THM_M_0821_Obligations.MiddleLayerSizedPackage", "The fixed-rank invariant consumed by antichain construction.", "Mathlib/Data/Finset/Slice.lean:86-88; ObligationTree.lean:36-42,124-129", 12),
    spec("M0821-L-MIDDLE-ANTICHAIN", "core_lemma", "high", "A fixed-rank family is an antichain under inclusion, hence the selected middle layer is a Sperner family.", "Stage1Instances.THM_M_0821_Obligations.MiddleLayerSizedPackage -> Stage1Instances.THM_M_0821_Obligations.MiddleLayerAntichainPackage", "The antichain half of the attaining witness.", "Mathlib/Data/Finset/Slice.lean:44-47; ObligationTree.lean:67-72", 18),
    spec("M0821-L-MIDDLE-CARD", "core_lemma", "normal", "Count the lower-middle powerset slice by the binomial coefficient.", "Stage1Instances.THM_M_0821_Obligations.MiddleLayerCardinalityPackage", "The exact cardinality half of the attaining witness.", "Mathlib/Data/Finset/Powerset.lean:198-202; ObligationTree.lean:51-57,131-135", 14),
    spec("M0821-L-SPERNER-UPPER", "bridge", "critical", "Bound every finite antichain by the middle binomial coefficient using the pinned terminal theorem.", "Stage1Instances.THM_M_0821_Obligations.UpperBoundPackage", "The complete universal upper-bound package.", "Mathlib/Combinatorics/SetFamily/LYM.lean:232-245; IsAntichain.sperner", 20),
    spec("M0821-L-CHOOSE-MIDDLE", "normalization", "high", "Bound each rank binomial coefficient by the lower-middle coefficient and prove positivity of both denominators used in Sperner's argument.", "planned signature: forall (alpha : Type*) [Fintype alpha] (s : Finset alpha), 0 < Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2) /\\ 0 < Nat.choose (Fintype.card alpha) s.card /\\ ((Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2) : ℚ≥0)^-1 <= (Nat.choose (Fintype.card alpha) s.card : ℚ≥0)^-1)", "The denominator positivity and inverse coefficient comparison used in the Sperner corollary.", "LYM.lean:236-243; Nat.choose_le_middle; Nat.choose_pos", 18),
    spec("M0821-L-LYM-INV", "bridge", "critical", "Bound the sum over family members of inverse rank-binomial coefficients by one.", "planned specialization: forall (alpha : Type*) [Fintype alpha] (A : Finset (Finset alpha)), IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> (sum s in A, (Nat.choose (Fintype.card alpha) s.card : ℚ≥0)^-1) <= 1", "The inverse-sum LYM inequality consumed by Sperner's bound.", "LYM.lean:216-228; Finset.lubell_yamamoto_meshalkin_inequality_sum_inv_choose", 30),
    spec("M0821-N-FIBERWISE-SLICES", "normalization", "high", "Regroup the member-wise inverse-binomial sum by subset cardinality and identify each fiber with a family slice.", "planned signature: forall (alpha : Type*) [Fintype alpha] (A : Finset (Finset alpha)), (sum s in A, (Nat.choose (Fintype.card alpha) s.card : ℚ≥0)^-1) = sum r in Finset.range (Fintype.card alpha + 1), ((A.slice r).card : ℚ≥0) / Nat.choose (Fintype.card alpha) r", "Equality between the inverse-member sum and the layer-density sum.", "LYM.lean:219-227; Slice.lean:117-139; Algebra/BigOperators/Group/Finset/Basic.lean:263-269; Finset.sum_fiberwise_of_maps_to'", 28),
    spec("M0821-L-LYM-CARD", "bridge", "critical", "Bound the sum of the family densities in every Boolean-lattice rank by one.", "planned specialization: forall (alpha : Type*) [Fintype alpha] (A : Finset (Finset alpha)), IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> (sum r in Finset.range (Fintype.card alpha + 1), ((A.slice r).card : ℚ≥0) / Nat.choose (Fintype.card alpha) r) <= 1", "The cardinality-slice LYM inequality.", "LYM.lean:197-211; Finset.lubell_yamamoto_meshalkin_inequality_sum_card_div_choose", 26),
    spec("M0821-L-FALLING-ZERO", "core_lemma", "high", "At k = card alpha, bound falling 0 A by the zero layer and normalize choose(n, 0) to one.", "planned signature: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)), ((Finset.falling 0 A).card : ℚ≥0) / (Nat.choose (Fintype.card alpha) 0 : ℚ≥0) <= 1", "The normalized zero-rank falling-family density is at most one.", "LYM.lean:205-211; Set.Sized.card_le (Finset.sized_falling 0 A)", 18),
    spec("M0821-C-FALLING", "construction", "high", "Construct falling k A, characterize its members, and establish its size and slice-containment invariants.", "planned package signature: forall (alpha : Type*) [DecidableEq alpha] (k : Nat) (A : Finset (Finset alpha)), (forall s, s in Finset.falling k A <-> (exists t in A, s ⊆ t) /\\ s.card = k) /\\ Set.Sized k (Finset.falling k A : Set (Finset alpha)) /\\ A.slice k ⊆ Finset.falling k A", "The rank-normalized down-family and the exact invariants used by the LYM induction.", "LYM.lean:123-142; Finset.falling, Finset.mem_falling, Finset.sized_falling, Finset.slice_subset_falling", 30),
    spec("M0821-L-FALLING-TOP", "core_lemma", "critical", "Induct on the top k+1 layers to bound their density sum by the normalized size of the corresponding falling family.", "planned ℚ≥0 specialization: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)) (k : Nat), k <= Fintype.card alpha -> IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> (sum r in Finset.range (k + 1), ((A.slice (Fintype.card alpha - r)).card : ℚ≥0) / Nat.choose (Fintype.card alpha) (Fintype.card alpha - r)) <= ((Finset.falling (Fintype.card alpha - k) A).card : ℚ≥0) / Nat.choose (Fintype.card alpha) (Fintype.card alpha - k)", "The top-part inequality specialized to NNRat for every legal top-layer index.", "LYM.lean:169-191; Finset.le_card_falling_div_choose", 42),
    spec("M0821-B-FALLING-INDUCTION", "branch", "high", "Handle the zero and successor induction branches and recombine them into the falling top-part inequality.", "planned package signature: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)), IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> forall k, k <= Fintype.card alpha -> (sum r in Finset.range (k + 1), ((A.slice (Fintype.card alpha - r)).card : ℚ≥0) / Nat.choose (Fintype.card alpha) (Fintype.card alpha - r)) <= ((Finset.falling (Fintype.card alpha - k) A).card : ℚ≥0) / Nat.choose (Fintype.card alpha) (Fintype.card alpha - k)", "The complete top-layer falling-family inequality for every legal induction index.", "LYM.lean:173-191; Finset.le_card_falling_div_choose", 24),
    spec("M0821-L-SLICE-SHADOW", "core_lemma", "high", "Decompose falling k A as the current k-slice union the shadow of falling(k+1) A.", "forall (alpha : Type*) [DecidableEq alpha] (A : Finset (Finset alpha)) (k : Nat), A.slice k ∪ (Finset.falling (k + 1) A).shadow = Finset.falling k A", "The exact set-family identity used in the successor step.", "LYM.lean:141-159; Finset.slice_union_shadow_falling_succ", 24),
    spec("M0821-L-DISJOINT-SHADOW", "core_lemma", "high", "Use the antichain premise to make the current slice disjoint from the next falling shadow.", "forall (alpha : Type*) [DecidableEq alpha] {A : Finset (Finset alpha)} {m n : Nat}, IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> Disjoint (A.slice m) (Finset.falling n A).shadow", "The disjointness needed for cardinality addition.", "LYM.lean:162-171; Finset.IsAntichain.disjoint_slice_shadow_falling", 20),
    spec("M0821-L-LOCAL-LYM", "bridge", "critical", "Compare a fixed-rank family density with its downward shadow density, including the nonzero-rank and denominator conditions.", "planned ℚ≥0 specialization: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)) (r : Nat), Not (r = 0) -> Set.Sized r (A : Set (Finset alpha)) -> (A.card : ℚ≥0) / Nat.choose (Fintype.card alpha) r <= (A.shadow.card : ℚ≥0) / Nat.choose (Fintype.card alpha) (r - 1)", "The local LYM inequality used in the successor induction step.", "LYM.lean:91-113; Finset.local_lubell_yamamoto_meshalkin_inequality_div", 38),
    spec("M0821-L-LOCAL-LYM-MUL", "core_lemma", "critical", "Double count deletion/insertion incidences to obtain the denominator-cleared local LYM inequality.", "forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)) (r : Nat), Set.Sized r (A : Set (Finset alpha)) -> A.card * r <= A.shadow.card * (Fintype.card alpha - r + 1)", "A.card * r <= A.shadow.card * (Fintype.card alpha - r + 1).", "LYM.lean:64-86; Finset.local_lubell_yamamoto_meshalkin_inequality_mul", 44),
    spec("M0821-C-SHADOW", "construction", "high", "Construct the downward shadow, identify deletion/insertion witnesses, and derive the two incidence-degree bounds used by local LYM.", "planned package signature: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)) (r : Nat), Set.Sized r (A : Set (Finset alpha)) -> (forall b in A, r <= #(A.shadow.bipartiteBelow ((.) ⊆ (.)) b)) /\\ (forall a in A.shadow, #(A.bipartiteAbove ((.) ⊆ (.)) a) <= Fintype.card alpha - r + 1)", "The shadow family and the exact lower/upper incidence-degree bounds.", "Mathlib/Combinatorics/SetFamily/Shadow.lean:62-115,165-171; LYM.lean:68-85", 34),
    spec("M0821-L-DOUBLE-COUNT", "bridge", "high", "Apply the bipartite card-product inequality to the deletion/insertion incidence relation.", "forall finite s t and decidable relation R, (forall b in t, n <= #(s.bipartiteBelow R b)) -> (forall a in s, #(t.bipartiteAbove R a) <= m) -> #t * n <= #s * m", "The incidence-cardinality comparison underlying local LYM.", "LYM.lean:68-75; DoubleCounting.lean:170-182; Finset.card_mul_le_card_mul'", 26),
    spec("M0821-T-ATTAIN", "terminal", "critical", "Assemble the explicit middle layer, its fixed-rank antichain property, and its cardinality into the attaining package.", "Stage1Instances.THM_M_0821_Obligations.attainment_of_middleLayer", "AttainmentPackage for every finite ground type.", "ObligationTree.lean", 18),
    spec("M0821-T-UPPER", "terminal", "critical", "Package the exact imported Sperner conclusion as the universal upper-bound branch.", "Stage1Instances.THM_M_0821_Obligations.upperBound_of_sperner", "UpperBoundPackage for every finite ground type and antichain.", "ObligationTree.lean", 12),
    spec("M0821-T-ROOT-COMPOSE", "terminal", "critical", "Transport the exact recombined maximum conjunction to the frozen target.", "Stage1Instances.THM_M_0821_Obligations.MaximumSplit -> Stage1Instances.THM_M_0821.SpernerMaximumTarget", "Stage1Instances.THM_M_0821.SpernerMaximumTarget.", "ObligationTree.lean:97-101", 16),
    spec("M0821-X-SOURCE", "terminal", "critical", "Map every mathematical node to the 1928 source and modern support sources with exact locators, assumptions, translations, proof steps, errata, and independent review.", "planned record predicate: each required_human_source ID has a pinpoint primary-source crosswalk and independent source-review receipt", "Human-source evidence without machine-proof credit.", "source-statement-crosswalk.md; printed pages 544-548", 48),
    spec("M0821-X-PROVENANCE", "certificate", "critical", "Bind wrapper, terminal, support body, source hashes, licenses, direct and transitive declarations, and receipts without duplicate proof-body credit.", "planned record predicate: every formal body ID has an immutable origin, source hash, direct dependencies, and transitive trust-closure hash", "Proof-body provenance without mathematical proof credit.", "anchor-audit.json; anchor-audit-receipt.json", 42),
    spec("M0821-X-TRUST", "certificate", "critical", "Audit the transitive Lean/mathlib declaration closure, compiled artifacts, executables, axioms, unsafe/oracle boundaries, and independent replay.", "planned record predicate: all root-relevant declarations, imported artifacts, executables, axioms, and oracle boundaries are inside an accepted TCB profile", "Release-grade trust inventory without proof credit.", "anchor-audit.json immutable_environment; ObligationTree.lean axiom probes", 42),
    spec("M0821-X-READABLE", "terminal", "high", "Produce an independently reviewed readable reconstruction with one stable section per required node and every source/formal anchor.", "planned record predicate: each required_readable ID has the ten ordered section-8 fields and an independent reader receipt", "Reader-facing coverage without machine-proof credit.", "obligation-tree.md is architecture only", 60),
    spec("M0821-X-WORKFLOW", "certificate", "high", "Require dependency-legal proof, validation, release, freshness, revocation, and independent-verification receipts before root promotion.", "planned record predicate: task acceptance is topologically legal and all freshness, revocation, validation, and release gates are accepted", "Workflow acceptance boundary without proof credit.", "Docs/Stage1_Execution_DAG_rev-5.6.json", 20),
]


REQUIRES = {
    "M0821-ROOT": ["M0821-T-ROOT-COMPOSE"],
    "M0821-T-ROOT-COMPOSE": ["M0821-B-MAXIMUM"],
    "M0821-B-MAXIMUM": ["M0821-T-ATTAIN", "M0821-T-UPPER"],
    "M0821-T-ATTAIN": ["M0821-C-MIDDLE-LAYER", "M0821-L-MIDDLE-ANTICHAIN", "M0821-L-MIDDLE-CARD"],
    "M0821-L-MIDDLE-ANTICHAIN": ["M0821-C-MIDDLE-SIZED"],
    "M0821-T-UPPER": ["M0821-L-SPERNER-UPPER"],
    "M0821-L-SPERNER-UPPER": ["M0821-L-CHOOSE-MIDDLE", "M0821-L-LYM-INV"],
    "M0821-L-LYM-INV": ["M0821-N-FIBERWISE-SLICES", "M0821-L-LYM-CARD"],
    "M0821-L-LYM-CARD": ["M0821-L-FALLING-TOP", "M0821-L-FALLING-ZERO"],
    "M0821-L-FALLING-ZERO": ["M0821-C-FALLING"],
    "M0821-L-FALLING-TOP": ["M0821-C-FALLING", "M0821-B-FALLING-INDUCTION"],
    "M0821-B-FALLING-INDUCTION": ["M0821-C-FALLING", "M0821-L-SLICE-SHADOW", "M0821-L-DISJOINT-SHADOW", "M0821-L-LOCAL-LYM"],
    "M0821-L-LOCAL-LYM": ["M0821-L-LOCAL-LYM-MUL"],
    "M0821-L-LOCAL-LYM-MUL": ["M0821-C-SHADOW", "M0821-L-DOUBLE-COUNT"],
}


CHECKED_PARENTS = {
    "M0821-ROOT": ("Stage1Instances.THM_M_0821_Obligations.root_of_terminal", "lean_abstract_child_harness"),
    "M0821-T-ROOT-COMPOSE": ("Stage1Instances.THM_M_0821_Obligations.compose_root", "lean_abstract_child_harness"),
    "M0821-B-MAXIMUM": ("Stage1Instances.THM_M_0821_Obligations.maximumSplit_of_packages", "lean_abstract_child_harness"),
    "M0821-T-ATTAIN": ("Stage1Instances.THM_M_0821_Obligations.attainment_of_middleLayer", "lean_abstract_child_harness"),
    "M0821-L-MIDDLE-ANTICHAIN": ("Stage1Instances.THM_M_0821_Obligations.middleLayerAntichain_of_sized", "lean_abstract_child_harness"),
    "M0821-T-UPPER": ("Stage1Instances.THM_M_0821_Obligations.upperBound_of_sperner", "lean_abstract_child_harness"),
}


MACHINE_SPECIAL = {
    "M0821-N-NO-OTHER": "informational",
    "M0821-B-NO-CASES": "informational",
    "M0821-X-SOURCE": "not_applicable",
    "M0821-X-PROVENANCE": "informational",
    "M0821-X-TRUST": "informational",
    "M0821-X-READABLE": "not_applicable",
    "M0821-X-WORKFLOW": "informational",
}
SOURCE_NA = {
    "M0821-S-INTERFACE", "M0821-S-BOUNDARY", "M0821-S-TRANSPORT",
    "M0821-S-FOUNDATION", "M0821-N-NO-OTHER", "M0821-B-NO-CASES",
    "M0821-X-PROVENANCE", "M0821-X-TRUST", "M0821-X-READABLE",
    "M0821-X-WORKFLOW",
}
READABLE_NA = {"M0821-X-WORKFLOW"}


def body_id(module: str, declaration: str) -> str:
    return f"mathlib:{MATHLIB_REVISION}:{module}#{declaration}"


BODY_IDS = {
    "M0821-S-TRANSPORT": "local:Statement.lean#spernerMaximumTarget_iff_middleLayerMaximumTarget",
    "M0821-C-MIDDLE-LAYER": "local:ObligationTree.lean#pinned_middleLayerDefinition",
    "M0821-C-MIDDLE-SIZED": "local:ObligationTree.lean#pinned_middleLayerSized",
    "M0821-L-MIDDLE-ANTICHAIN": "local:ObligationTree.lean#middleLayerAntichain_of_sized",
    "M0821-L-MIDDLE-CARD": "local:ObligationTree.lean#pinned_middleLayerCardinality",
    "M0821-L-SPERNER-UPPER": "local:ObligationTree.lean#pinned_upperBound",
    "M0821-L-LYM-INV": body_id("Mathlib.Combinatorics.SetFamily.LYM", "Finset.lubell_yamamoto_meshalkin_inequality_sum_inv_choose"),
    "M0821-L-LYM-CARD": body_id("Mathlib.Combinatorics.SetFamily.LYM", "Finset.lubell_yamamoto_meshalkin_inequality_sum_card_div_choose"),
    "M0821-L-FALLING-TOP": body_id("Mathlib.Combinatorics.SetFamily.LYM", "Finset.le_card_falling_div_choose"),
    "M0821-L-SLICE-SHADOW": body_id("Mathlib.Combinatorics.SetFamily.LYM", "Finset.slice_union_shadow_falling_succ"),
    "M0821-L-DISJOINT-SHADOW": body_id("Mathlib.Combinatorics.SetFamily.LYM", "Finset.IsAntichain.disjoint_slice_shadow_falling"),
    "M0821-L-LOCAL-LYM": body_id("Mathlib.Combinatorics.SetFamily.LYM", "Finset.local_lubell_yamamoto_meshalkin_inequality_div"),
    "M0821-L-LOCAL-LYM-MUL": body_id("Mathlib.Combinatorics.SetFamily.LYM", "Finset.local_lubell_yamamoto_meshalkin_inequality_mul"),
    "M0821-L-DOUBLE-COUNT": body_id("Mathlib.Combinatorics.Enumerative.DoubleCounting", "Finset.card_mul_le_card_mul'"),
    "M0821-T-ATTAIN": "local:ObligationTree.lean#attainment_of_middleLayer",
    "M0821-T-UPPER": "local:ObligationTree.lean#upperBound_of_sperner",
    "M0821-T-ROOT-COMPOSE": "local:ObligationTree.lean#compose_root",
}

# Only declarations explicitly bound by the anchor candidate receive its E2 tag.
ANCHOR_EVIDENCE_OBLIGATIONS = {
    "M0821-C-MIDDLE-SIZED",
    "M0821-L-MIDDLE-ANTICHAIN",
    "M0821-L-MIDDLE-CARD",
    "M0821-L-SPERNER-UPPER",
}


LEAF_LEDGERS = {
    "M0821-ROOT": [
        (["M0821-T-ROOT-COMPOSE"], "Consume the exact terminal proposition with the checked root_of_terminal identity harness.", "ObligationTree.lean:103-107", "The exact frozen SpernerMaximumTarget."),
    ],
    "M0821-S-INTERFACE": [
        (["frozen-formal-context"], "Serialize the elaborated canonical Prop with explicit universes, binders, typeclass arguments, conjunction, existential, and universal family.", "Statement.lean:30-37; check_statement.py expression serialization", "The exact root expression with SHA-256 8f5d05428a35e3b6f13947097ac52417ba900b3cf9b1b45c0bb173766c914d7c."),
    ],
    "M0821-S-BOUNDARY": [
        (["frozen-formal-context"], "Check the two concrete middle-layer equalities at Fin 0 and Fin 1.", "Statement.lean:64-70", "Empty and singleton ground types remain included."),
        (["M0821-S-BOUNDARY-STEP-01"], "Inspect the exact target binders: keep natural division n/2, all finite types, and no equality-family classification.", "Statement.lean:30-37; statement.json encoding_decisions", "The exact maximum-value, not equality-classification, boundary."),
    ],
    "M0821-S-TRANSPORT": [
        (["frozen-formal-context"], "Forward: retain the root's universal bound and derive the concrete lower-middle witness facts independently.", "Statement.lean:51-60", "MiddleLayerMaximumTarget."),
        (["M0821-S-TRANSPORT-STEP-01"], "Backward: package the concrete middle layer as the root existential witness and retain the same universal bound.", "Statement.lean:61-62", "SpernerMaximumTarget."),
    ],
    "M0821-S-FOUNDATION": [
        (["frozen-formal-context"], "Run machine axiom reports on the pinned terminal, candidate interfaces, and every checked composition declaration.", "ObligationTree.lean #print axioms", "Observed axiom sets are subsets of propext, Classical.choice, Quot.sound."),
        (["M0821-S-FOUNDATION-STEP-01"], "Reject placeholders, unsafe injection, native/external evaluation, solver, certificate, or oracle proof credit.", "check_obligation_tree.py Lean source and output gates", "The provisional foundation/computation boundary."),
    ],
    "M0821-N-LOWER-MIDDLE": [
        (["frozen-formal-context"], "Use Nat division to select floor(n/2) in the formal target and witness definition.", "Statement.lean:21-23,30-37", "The lower-middle rank n/2."),
        (["M0821-N-LOWER-MIDDLE-STEP-01"], "Use choose_le_middle to show every rank coefficient is at most the selected coefficient.", "LYM.lean:236-243", "choose(n,r) <= choose(n,n/2)."),
    ],
    "M0821-N-NO-OTHER": [
        (["frozen-formal-context"], "Check every normalization trigger in blueprint section 6.5 against the finite Boolean-lattice encoding and pinned proof body.", "Blueprint sections 6.4-6.5; LYM.lean:232-245", "A pending-review decision that no additional normalization node is required."),
    ],
    "M0821-B-MAXIMUM": [
        (["M0821-T-ATTAIN"], "Obtain the exact AttainmentPackage.", "ObligationTree.lean:91-95", "AttainmentPackage."),
        (["M0821-T-UPPER"], "Obtain the exact UpperBoundPackage.", "ObligationTree.lean:91-95", "UpperBoundPackage."),
        (["M0821-T-ATTAIN", "M0821-T-UPPER"], "Apply maximumSplit_of_packages and consume both conjunct packages.", "ObligationTree.lean:91-95", "MaximumSplit."),
    ],
    "M0821-B-NO-CASES": [
        (["frozen-formal-context"], "Check every branch trigger in blueprint section 6.5 against the uniform pinned Sperner proof.", "Blueprint sections 6.4-6.5; LYM.lean:232-245", "A pending-review decision that no additional parity/cardinality branch node is required."),
    ],
    "M0821-C-MIDDLE-LAYER": [
        (["frozen-formal-context"], "Unfold the repo-local definition of middleLayer.", "Statement.lean:21-23; ObligationTree.lean:119-122", "middleLayer alpha is powersetCard (card alpha / 2) univ."),
        (["M0821-C-MIDDLE-LAYER-STEP-01"], "Generalize the definitional equality over every finite ground type.", "ObligationTree.lean:119-122", "MiddleLayerDefinitionPackage."),
    ],
    "M0821-C-MIDDLE-SIZED": [
        (["frozen-formal-context"], "Instantiate Set.sized_powersetCard at univ and the selected rank card alpha / 2.", "Slice.lean:86-88; ObligationTree.lean:124-129", "Every member of the raw middle slice has the selected cardinality."),
        (["M0821-C-MIDDLE-SIZED-STEP-01"], "Generalize over alpha and its Fintype instance.", "ObligationTree.lean:124-129", "MiddleLayerSizedPackage."),
    ],
    "M0821-L-MIDDLE-ANTICHAIN": [
        (["M0821-C-MIDDLE-SIZED"], "Use equality of member cardinalities to turn either inclusion between distinct slice members into equality.", "Slice.lean:44-47", "The raw fixed-rank slice is an antichain."),
        (["M0821-L-MIDDLE-ANTICHAIN-STEP-01"], "Package the relation as IsSpernerFamily through the checked conditional harness.", "ObligationTree.lean: middleLayerAntichain_of_sized", "MiddleLayerAntichainPackage."),
    ],
    "M0821-L-MIDDLE-CARD": [
        (["frozen-formal-context"], "Instantiate Finset.card_powersetCard at the selected rank and univ.", "Powerset.lean:198-202", "The middle slice has cardinality choose(card univ, card alpha / 2)."),
        (["M0821-L-MIDDLE-CARD-STEP-01"], "Rewrite card univ as Fintype.card alpha and generalize over alpha.", "ObligationTree.lean:131-135", "MiddleLayerCardinalityPackage."),
    ],
    "M0821-L-SPERNER-UPPER": [
        (["M0821-L-CHOOSE-MIDDLE"], "Replace every inverse rank coefficient by the inverse middle coefficient using positivity and choose_le_middle.", "LYM.lean:236-243", "A constant inverse-middle sum bounded by the member-wise LYM sum."),
        (["M0821-L-LYM-INV"], "Apply the inverse-sum LYM bound to the antichain family.", "LYM.lean:244", "The constant inverse-middle sum is at most one."),
        (["M0821-L-SPERNER-UPPER-STEP-01", "M0821-L-SPERNER-UPPER-STEP-02"], "Clear the positive middle-binomial denominator.", "LYM.lean:245", "A.card <= choose(card alpha, card alpha / 2)."),
    ],
    "M0821-L-CHOOSE-MIDDLE": [
        (["frozen-formal-context"], "Apply Nat.choose_pos to Nat.div_le_self to prove positivity of the middle coefficient.", "LYM.lean:236-237", "0 < choose(n,n/2)."),
        (["frozen-formal-context"], "Use s.card_le_univ and Nat.choose_pos for the member-rank coefficient.", "LYM.lean:241-242", "0 < choose(n,card s)."),
        (["M0821-L-CHOOSE-MIDDLE-STEP-01", "M0821-L-CHOOSE-MIDDLE-STEP-02"], "Apply Nat.choose_le_middle and antitonicity of inversion in NNRat.", "LYM.lean:239-243", "The inverse middle coefficient is at most the inverse member-rank coefficient."),
        (["M0821-L-CHOOSE-MIDDLE-STEP-01", "M0821-L-CHOOSE-MIDDLE-STEP-02", "M0821-L-CHOOSE-MIDDLE-STEP-03"], "Package both positivity facts and the inverse comparison without dropping a conjunct.", "planned exact package boundary; LYM.lean:236-243", "For every member rank, choose(n,n/2) is positive, choose(n,card s) is positive, and the inverse middle coefficient is at most the inverse member-rank coefficient."),
    ],
    "M0821-L-LYM-INV": [
        (["M0821-N-FIBERWISE-SLICES"], "Group the member sum by cardinality and identify each filtered family with a slice.", "LYM.lean:219-227", "The inverse-member sum equals the layer-density sum."),
        (["M0821-L-LYM-CARD"], "Apply the layer-density LYM inequality.", "LYM.lean:228", "The inverse-member sum is at most one."),
    ],
    "M0821-N-FIBERWISE-SLICES": [
        (["frozen-formal-context"], "Regroup the member sum by the cardinality map into range(card alpha + 1), using card_le_univ for maps-to.", "LYM.lean:223-225; Algebra/BigOperators/Group/Finset/Basic.lean:263-269; Finset.sum_fiberwise_of_maps_to'", "A sum over rank fibers."),
        (["M0821-N-FIBERWISE-SLICES-STEP-01"], "Identify each filtered fiber with A.slice r through Finset.mem_slice.", "Slice.lean:117-139; LYM.lean:226-227", "The rank-r fiber cardinality times the inverse rank coefficient."),
        (["M0821-N-FIBERWISE-SLICES-STEP-02"], "Rewrite the constant fiber sum with div_eq_mul_inv.", "LYM.lean:226-227", "Equality between the inverse-member sum and layer-density sum."),
    ],
    "M0821-L-LYM-CARD": [
        (["M0821-L-FALLING-TOP"], "Specialize the top-part bound at k = card alpha and normalize the reversed rank indexing.", "LYM.lean:201-206", "The full layer-density sum is bounded by the normalized size of falling 0 A."),
        (["M0821-L-FALLING-ZERO"], "Bound the zero-rank falling family by choose(n,0)=1 and clear the unit denominator.", "LYM.lean:206-211", "The layer-density sum is at most one."),
    ],
    "M0821-L-FALLING-ZERO": [
        (["M0821-C-FALLING"], "Use sized_falling 0 A and Set.Sized.card_le to bound the zero-rank falling family by choose(n,0).", "LYM.lean:208-210", "card(falling 0 A) <= choose(n,0)."),
        (["M0821-L-FALLING-ZERO-STEP-01"], "Rewrite choose(n,0), casts, and division by one.", "LYM.lean:207-211", "card(falling 0 A) / choose(n,0) <= 1."),
    ],
    "M0821-C-FALLING": [
        (["frozen-formal-context"], "Define falling k A as the supremum of powersetCard k over A.", "LYM.lean:123-127", "A finite family of k-subsets lying below A."),
        (["M0821-C-FALLING-STEP-01"], "Characterize membership by an upper family member and exact cardinality k.", "LYM.lean:129-136", "mem_falling and sized_falling."),
        (["M0821-C-FALLING-STEP-02"], "Embed the k-slice of A into falling k A.", "LYM.lean:138-139", "slice_subset_falling."),
        (["M0821-C-FALLING-STEP-02", "M0821-C-FALLING-STEP-03"], "Package the membership characterization, fixed-rank invariant, and slice containment without dropping an invariant.", "planned exact package boundary; LYM.lean:123-139", "For every k and A, membership in falling k A is characterized by a containing member of A and card k, falling k A is Sized k, and A.slice k is contained in falling k A."),
    ],
    "M0821-L-FALLING-TOP": [
        (["M0821-C-FALLING"], "Initialize the normalized top-layer family and its fixed-rank invariant.", "LYM.lean:173-178", "The right-hand falling-family density is well-formed."),
        (["M0821-B-FALLING-INDUCTION"], "Induct over the number of included top layers.", "LYM.lean:179-191", "The top-layer density sum is bounded by the falling-family density."),
    ],
    "M0821-B-FALLING-INDUCTION": [
        (["M0821-C-FALLING"], "In the zero branch, use slice_subset_falling and cardinal monotonicity.", "LYM.lean:179-184", "The one-term top sum is bounded."),
        (["M0821-L-SLICE-SHADOW", "M0821-L-DISJOINT-SHADOW"], "In the successor branch, rewrite falling as a disjoint union and add cardinalities.", "LYM.lean:185-189", "The successor right side splits into the current slice and a shadow term."),
        (["M0821-L-LOCAL-LYM", "M0821-B-FALLING-INDUCTION-STEP-02"], "Apply the induction hypothesis and local LYM to the shadow term.", "LYM.lean:189-191", "The successor top-layer inequality."),
    ],
    "M0821-L-SLICE-SHADOW": [
        (["frozen-formal-context"], "Expand membership in slice, shadow, and falling on both sides.", "LYM.lean:144-147", "The desired family equality reduced to elementwise implications."),
        (["M0821-L-SLICE-SHADOW-STEP-01"], "Map a slice member directly into falling, and a shadow witness by erasing its added element.", "LYM.lean:148-152", "The union is contained in falling k A."),
        (["M0821-L-SLICE-SHADOW-STEP-01"], "For a falling member, split on membership in A; otherwise obtain a strict-superset insertion witness.", "LYM.lean:153-158", "falling k A is contained in the slice-shadow union."),
        (["M0821-L-SLICE-SHADOW-STEP-02", "M0821-L-SLICE-SHADOW-STEP-03"], "Apply extensionality to the two containments.", "LYM.lean:144-159", "A.slice k union shadow(falling(k+1) A) = falling k A."),
    ],
    "M0821-L-DISJOINT-SHADOW": [
        (["frozen-formal-context"], "Assume a member lies in both the current slice and the shadow of a falling family and expand both witnesses.", "LYM.lean:164-168", "Two members of A related by inclusion through an erased set."),
        (["M0821-L-DISJOINT-SHADOW-STEP-01"], "Invoke the antichain property on those two A-members.", "LYM.lean:168-170", "They would have to be unequal while inclusion holds."),
        (["M0821-L-DISJOINT-SHADOW-STEP-02"], "Rule out equality because the erased element cannot belong to the erase result.", "LYM.lean:170-171", "Disjoint (A.slice m) (shadow (falling n A))."),
    ],
    "M0821-L-LOCAL-LYM": [
        (["M0821-L-LOCAL-LYM-MUL"], "Start from the denominator-cleared incidence inequality.", "LYM.lean:99", "card(A)*r <= card(shadow A)*(n-r+1)."),
        (["M0821-L-LOCAL-LYM-STEP-01"], "Use choose_succ_right_eq, positivity, and the rank bounds to divide by both binomial coefficients.", "LYM.lean:96-110", "The local density comparison."),
    ],
    "M0821-L-LOCAL-LYM-MUL": [
        (["M0821-C-SHADOW"], "Identify each deletion fiber below a family member with its r possible erased elements.", "LYM.lean:68-73", "A lower incidence degree r on the family side."),
        (["M0821-C-SHADOW"], "Identify insertion fibers above a shadow member and bound them by n-r+1.", "LYM.lean:74-85", "An upper incidence degree n-r+1 on the shadow side."),
        (["M0821-L-DOUBLE-COUNT", "M0821-L-LOCAL-LYM-MUL-STEP-01", "M0821-L-LOCAL-LYM-MUL-STEP-02"], "Apply bipartite double counting to both degree bounds.", "LYM.lean:69; DoubleCounting.lean:179-182", "The denominator-cleared local LYM inequality."),
    ],
    "M0821-C-SHADOW": [
        (["frozen-formal-context"], "Construct the downward shadow as all one-element deletions of members of the fixed-rank family.", "Mathlib/Combinatorics/SetFamily/Shadow.lean; LYM.lean:71-73", "The shadow family and erase membership witnesses."),
        (["M0821-C-SHADOW-STEP-01"], "Use the sized invariant to count exactly r deletions below each original member.", "LYM.lean:70-73", "Lower incidence degree r."),
        (["M0821-C-SHADOW-STEP-01"], "Use complement insertion and sized_shadow_iff to bound supersets of a shadow member by n-r+1.", "LYM.lean:74-85", "Upper incidence degree n-r+1."),
        (["M0821-C-SHADOW-STEP-02", "M0821-C-SHADOW-STEP-03"], "Package both incidence-degree estimates for the same shadow construction and sized premise.", "planned exact package boundary; LYM.lean:68-85", "Every original member has at least r lower incidences, and every shadow member has at most Fintype.card alpha - r + 1 upper incidences."),
    ],
    "M0821-L-DOUBLE-COUNT": [
        (["frozen-formal-context"], "Fix the decidable bipartite incidence relation and its two finite vertex families.", "DoubleCounting.lean:170-182", "Finite bipartiteAbove and bipartiteBelow neighborhoods."),
        (["M0821-L-DOUBLE-COUNT-STEP-01"], "Supply the lower degree bound for every right-side vertex and the upper degree bound for every left-side vertex.", "DoubleCounting.lean:179-182", "The two hypotheses of card_mul_le_card_mul'."),
        (["M0821-L-DOUBLE-COUNT-STEP-02"], "Apply Finset.card_mul_le_card_mul'.", "DoubleCounting.lean:179-182", "#t * n <= #s * m."),
    ],
    "M0821-T-ATTAIN": [
        (["M0821-C-MIDDLE-LAYER"], "Rewrite the repo-local witness as the raw lower-middle powerset slice.", "ObligationTree.lean:59-65", "The selected explicit witness."),
        (["M0821-L-MIDDLE-ANTICHAIN"], "Apply the exact antichain package to the rewritten witness.", "ObligationTree.lean:59-65", "The witness is a Sperner family."),
        (["M0821-L-MIDDLE-CARD"], "Apply the exact cardinality package to the rewritten witness.", "ObligationTree.lean:59-65", "The witness has the middle binomial cardinality."),
        (["M0821-C-MIDDLE-LAYER", "M0821-L-MIDDLE-ANTICHAIN", "M0821-L-MIDDLE-CARD"], "Construct the existential witness and both required conjuncts.", "ObligationTree.lean:59-65", "AttainmentPackage."),
    ],
    "M0821-T-UPPER": [
        (["M0821-L-SPERNER-UPPER"], "Introduce alpha, A, and its exact IsSpernerFamily hypothesis, then apply the imported Sperner conclusion.", "ObligationTree.lean:74-82,137-140", "The universal middle-binomial upper bound."),
        (["M0821-T-UPPER-STEP-01"], "Generalize over all finite ground types and families.", "ObligationTree.lean:74-82", "UpperBoundPackage."),
    ],
    "M0821-T-ROOT-COMPOSE": [
        (["M0821-B-MAXIMUM"], "Consume MaximumSplit, introduce the finite ground type, and project its attainment and upper-bound conjuncts.", "ObligationTree.lean:97-101", "The conjunction required by SpernerMaximumTarget at alpha."),
        (["M0821-T-ROOT-COMPOSE-STEP-01"], "Generalize the conjunction over every finite ground type.", "ObligationTree.lean:97-101", "SpernerMaximumTarget."),
    ],
    "M0821-X-SOURCE": [
        (["frozen-formal-context"], "Enumerate every required_human_source ID and require a pinpoint primary-source record, premise mapping, errata state, and reviewer.", "Blueprint sections 8.1 and 9.1; source-statement-crosswalk.md", "An explicitly open source-crosswalk coverage record."),
    ],
    "M0821-X-PROVENANCE": [
        (["frozen-formal-context"], "Bind each terminal body to immutable project, revision, source hash, license, declaration dependencies, and trust-closure hash.", "Blueprint section 7.3; anchor-audit.json", "An explicitly partial provenance record with no proof credit."),
    ],
    "M0821-X-TRUST": [
        (["frozen-formal-context"], "Inventory the transitive declarations, imported artifacts, executables, axioms, unsafe/oracle boundaries, and replay environment.", "Blueprint sections 7.4 and 10.6; anchor-audit.json", "An explicitly open trust/TCB record."),
    ],
    "M0821-X-READABLE": [
        (["frozen-formal-context"], "Require the ten ordered readable fields and an independent reader receipt for every required_readable ID.", "Blueprint section 8; obligation-tree.md", "An explicitly open readable-coverage record."),
    ],
    "M0821-X-WORKFLOW": [
        (["frozen-formal-context"], "Topologically check prerequisite acceptance, freshness, revocation, validation, and release gates before any root promotion.", "Blueprint sections 10.1-10.4; task-dag.json", "An explicitly open workflow record."),
    ],
}


def semantic_ledger(row: dict) -> list[dict]:
    oid = row["id"]
    if oid in LEAF_LEDGERS:
        raw = LEAF_LEDGERS[oid]
    else:
        raise ValueError(f"missing substantive semantic ledger for {oid}")
    result = []
    for index, (premises, inference, locator, output) in enumerate(raw, 1):
        result.append({
            "step_id": f"{oid}-STEP-{index:02d}",
            "premise_ids": premises,
            "inference": inference,
            "source_locator": locator,
            "output": output,
            "outgoing_use": row["output"] if index == len(raw) else f"{oid}-STEP-{index + 1:02d}",
        })
    return result


def edge(eid: str, source: str, typ: str, target: str, reciprocal: str | None = None) -> dict:
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal is not None:
        value["reciprocal_edge_id"] = reciprocal
    return value


def build() -> tuple[dict, dict, dict, str]:
    statement_sha = source_hash("Statement.lean")
    anchor_sha = source_hash("anchor-audit.json")
    obligations = []
    for row in SPECS:
        oid = row["id"]
        machine = MACHINE_SPECIAL.get(oid, "required")
        human = "not_applicable" if oid in SOURCE_NA else "required"
        readable = "not_applicable" if oid in READABLE_NA else "required"
        excluded = machine != "required" or human != "required" or readable != "required"
        if oid == "M0821-ROOT" or oid == "M0821-S-INTERFACE":
            fingerprint = "lean-expression-sha256:" + ROOT_EXPRESSION
        else:
            fingerprint = "planned:v2:sha256:" + digest({
                "obligation_id": oid,
                "formal_target": row["formal"],
                "output": row["output"],
            })
        obligations.append({
            "obligation_id": oid,
            "statement_fingerprint": fingerprint,
            "kind": row["kind"],
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": readable,
            "risk_class": row["risk"],
            "exclusion_reason": "support_or_layer_overlay_pending_independent_approval_no_proof_credit" if excluded else None,
            "terminal_proof_body_id": BODY_IDS.get(oid),
        })
    ids = [row["obligation_id"] for row in obligations]
    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in fields} for row in obligations]
    denominator = digest(projection)
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "registry_id": "THM-M-0821-OBLIGATIONS-v2",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 2,
        "frozen_at": "2026-07-13T23:00:36+08:00",
        "freeze_basis": "The exact maximum-value statement and bounded immutable anchor inventory select the concrete middle-layer attainment plus pinned LYM upper-bound architecture before proof-phase closure credit.",
        "frozen_against_statement_sha256": statement_sha,
        "frozen_against_anchor_audit_sha256": anchor_sha,
        "root_obligation_id": "M0821-ROOT",
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": [row["obligation_id"] for row in obligations if row["readable_eligibility"] == "required"],
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "additional_normalization": {"obligation_id": "M0821-N-NO-OTHER", "status": "not_applicable_pending_independent_approval"},
            "additional_case_splits": {"obligation_id": "M0821-B-NO-CASES", "status": "not_applicable_pending_independent_approval"},
        },
        "proof_body_aliases": {
            "Finset.card_div_choose_le_card_shadow_div_choose": "deduplicated_to:Finset.local_lubell_yamamoto_meshalkin_inequality_div",
            "Finset.card_mul_le_card_shadow_mul": "deduplicated_to:Finset.local_lubell_yamamoto_meshalkin_inequality_mul",
            "Finset.sum_card_slice_div_choose_le_one": "deduplicated_to:Finset.lubell_yamamoto_meshalkin_inequality_sum_card_div_choose",
        },
        "delta_policy": "Any later semantic correction, split, merge, exclusion, eligibility, risk, fingerprint, or proof-body identity change requires registry version 3 and an append-only old/new ID delta.",
        "append_only_delta": [{
            "from_registry_id": "THM-M-0821-OBLIGATIONS-v1",
            "from_denominator_sha256": "5c2062c82371b379919339f413619d88b6c4c1e08c79acf4f3c89022f2adafaf",
            "from_inventory_count": 35,
            "to_registry_id": "THM-M-0821-OBLIGATIONS-v2",
            "to_denominator_sha256": denominator,
            "to_inventory_count": len(ids),
            "added_obligation_ids": ["M0821-L-FALLING-ZERO"],
            "removed_obligation_ids": [],
            "changed_existing_obligation_ids": [
                row["obligation_id"] for row in obligations
                if row["obligation_id"] != "M0821-L-FALLING-ZERO"
                and row["statement_fingerprint"].startswith("planned:v2:")
            ],
            "reason": "Add the previously hidden falling-zero estimate and re-fingerprint every planned signature after exact formal-target and ledger correction; the root expression is unchanged.",
            "status_effect": "No obligation closes and accepted H1/M3/R4 remains unchanged.",
        }],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "closed_obligations": [],
            "accepted_root_machine_debt": "M3",
            "candidate_route": "M0821-C01 is an exact potential M0-W route, but current E2 worker evidence supports only M1 candidate status; it is not accepted closure and proof-phase E1 installation remains open.",
            "human_source_debt": "H1",
            "readability_debt": "R4",
        },
    }

    nodes = []
    for row, obligation in zip(SPECS, obligations):
        oid = row["id"]
        candidate = oid in ANCHOR_EVIDENCE_OBLIGATIONS
        nodes.append({
            "node_id": THEOREM + "-" + oid.removeprefix(PREFIX),
            "obligation_id": oid,
            "kind": row["kind"],
            "human_statement": row["claim"],
            "formal_target": row["formal"],
            "output": row["output"],
            "human_debt": "H1" if obligation["human_source_eligibility"] == "required" else "H2",
            "machine_debt": "M3" if obligation["machine_eligibility"] == "required" else "M4",
            "readability_debt": "R4",
            "evidence_ids": ["M0821-C01-E2-UNACCEPTED"] if candidate else [],
            "source_crosswalk_id": "SRC-M0821-SPERNER1928-PARTIAL" if obligation["human_source_eligibility"] == "required" else "not-applicable",
            "provenance_id": "PROV-M0821-C01-PARTIAL" if candidate else "none",
            "foundation_profile": "Lean4-mathlib-classical candidate: propext, Classical.choice, Quot.sound; acceptance open",
            "tcb_profile": "Lean-4.29.0+mathlib-8a178386; transitive declaration and release closure open",
            "computation_record": "none; no external computation, native evaluation, certificate, solver, or oracle closes this node",
            "step_budget": row["budget"],
            "semantic_step_ledger": semantic_ledger(row),
            "public_readable_target": f"Stage1_Instances/THM-M-0821/obligation-tree.md#{oid.lower()}",
            "validation_spec_id": "VAL-M0821-OBLIGATION-BUNDLE",
            "status_boundary": "Frozen architecture and unaccepted candidate or interface mapping only; no M0, E1, H0, R0, proof acceptance, audit completion, or theorem completion is credited.",
            "task_ids": [ITEM],
            "owned_sources": ["Stage1_Instances/THM-M-0821/ObligationTree.lean"] if oid in CHECKED_PARENTS or oid in {"M0821-C-MIDDLE-LAYER", "M0821-C-MIDDLE-SIZED", "M0821-L-MIDDLE-CARD"} else [],
            "owner": "THM-M-0821 execution lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13",
                "review_due": "before proof acceptance",
                "invalidation_inputs": ["statement hash", "anchor hash", "registry hash", "mathlib revision", "terminal bodies", "toolchain"],
                "revocation_state": "not-accepted",
            },
        })

    proof_edges = []
    for parent, children in REQUIRES.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            reverse = f"REV-{child}-{parent}"
            reverse_type = "composes" if parent in CHECKED_PARENTS else "logical_decomposition"
            proof_edges.extend([
                edge(req, parent, "proof_requires", child, reverse),
                edge(reverse, child, reverse_type, parent, req),
            ])
    workflow_tasks = [
        "S56-M-0821-ANCHOR_AUDIT", ITEM, "S56-M-0821-PROOF",
        "S56-M-0821-VALIDATION", "S56-M-0821-RELEASE",
    ]
    graph_edges = {
        "proof": proof_edges,
        "refinement": [
            edge("REF-ROOT-INTERFACE", "M0821-ROOT", "logical_decomposition", "M0821-S-INTERFACE", "REF-INTERFACE-OF-ROOT"),
            edge("REF-INTERFACE-OF-ROOT", "M0821-S-INTERFACE", "refines", "M0821-ROOT", "REF-ROOT-INTERFACE"),
            edge("REF-ROOT-BOUNDARY", "M0821-ROOT", "logical_decomposition", "M0821-S-BOUNDARY", "REF-BOUNDARY-OF-ROOT"),
            edge("REF-BOUNDARY-OF-ROOT", "M0821-S-BOUNDARY", "refines", "M0821-ROOT", "REF-ROOT-BOUNDARY"),
            edge("REF-ROOT-TRANSPORT", "M0821-ROOT", "equivalent_to", "M0821-S-TRANSPORT", "REF-TRANSPORT-ROOT"),
            edge("REF-TRANSPORT-ROOT", "M0821-S-TRANSPORT", "equivalent_to", "M0821-ROOT", "REF-ROOT-TRANSPORT"),
            edge("REF-ROOT-MIDDLE", "M0821-ROOT", "logical_decomposition", "M0821-N-LOWER-MIDDLE", "REF-MIDDLE-OF-ROOT"),
            edge("REF-MIDDLE-OF-ROOT", "M0821-N-LOWER-MIDDLE", "refines", "M0821-ROOT", "REF-ROOT-MIDDLE"),
            edge("REF-ROOT-NORM-NA", "M0821-ROOT", "expository_decomposition", "M0821-N-NO-OTHER", "REF-NORM-NA-DOCUMENTS-ROOT"),
            edge("REF-NORM-NA-DOCUMENTS-ROOT", "M0821-N-NO-OTHER", "documents", "M0821-ROOT", "REF-ROOT-NORM-NA"),
            edge("REF-ROOT-BRANCH-NA", "M0821-ROOT", "expository_decomposition", "M0821-B-NO-CASES", "REF-BRANCH-NA-DOCUMENTS-ROOT"),
            edge("REF-BRANCH-NA-DOCUMENTS-ROOT", "M0821-B-NO-CASES", "documents", "M0821-ROOT", "REF-ROOT-BRANCH-NA"),
        ],
        "provenance": [],
        "evidence": [],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", "M0821-ROOT", "trusts", "M0821-S-FOUNDATION", "TRUST-FOUNDATION-SUPPORTS-ROOT"),
            edge("TRUST-FOUNDATION-SUPPORTS-ROOT", "M0821-S-FOUNDATION", "trusted_by", "M0821-ROOT", "TRUST-ROOT-FOUNDATION"),
            edge("TRUST-ROOT-RELEASE", "M0821-ROOT", "trusts", "M0821-X-TRUST", "TRUST-RELEASE-SUPPORTS-ROOT"),
            edge("TRUST-RELEASE-SUPPORTS-ROOT", "M0821-X-TRUST", "trusted_by", "M0821-ROOT", "TRUST-ROOT-RELEASE"),
        ],
        "documentation": [],
        "workflow": [
            edge("FLOW-TREE-ANCHOR", ITEM, "workflow_depends_on", "S56-M-0821-ANCHOR_AUDIT"),
            edge("FLOW-PROOF-TREE", "S56-M-0821-PROOF", "workflow_depends_on", ITEM),
            edge("FLOW-VALIDATION-PROOF", "S56-M-0821-VALIDATION", "workflow_depends_on", "S56-M-0821-PROOF"),
            edge("FLOW-RELEASE-VALIDATION", "S56-M-0821-RELEASE", "workflow_depends_on", "S56-M-0821-VALIDATION"),
        ],
    }
    for obligation in obligations:
        oid = obligation["obligation_id"]
        if oid != "M0821-X-SOURCE" and obligation["human_source_eligibility"] == "required":
            graph_edges["provenance"].append(edge("SOURCE-MAP-" + oid, oid, "source_map", "M0821-X-SOURCE"))
        if oid not in {"M0821-X-SOURCE", "M0821-X-PROVENANCE", "M0821-X-TRUST", "M0821-X-READABLE", "M0821-X-WORKFLOW"}:
            graph_edges["provenance"].append(edge("PROVENANCE-" + oid, "M0821-X-PROVENANCE", "provenance_of", oid))
            graph_edges["evidence"].append(edge("EVIDENCE-" + oid, "M0821-X-PROVENANCE", "evidence_for", oid))
        if oid not in {"M0821-X-READABLE", "M0821-X-WORKFLOW"}:
            graph_edges["documentation"].append(edge("DOCUMENT-" + oid, "M0821-X-READABLE", "documents", oid))
    graphs = {}
    for name, edges in graph_edges.items():
        incoming: dict[str, list[str]] = {}
        outgoing: dict[str, list[str]] = {}
        for item in edges:
            outgoing.setdefault(item["from"], []).append(item["edge_id"])
            incoming.setdefault(item["to"], []).append(item["edge_id"])
        graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

    certificates = []
    plans = []
    obligation_by_id = {row["obligation_id"]: row for row in obligations}
    for parent, children in REQUIRES.items():
        if parent in CHECKED_PARENTS:
            declaration, kind = CHECKED_PARENTS[parent]
            certificates.append({
                "certificate_id": "COMP-" + parent,
                "parent_obligation_id": parent,
                "parent_statement_fingerprint": obligation_by_id[parent]["statement_fingerprint"],
                "required_child_ids": children,
                "required_child_statement_fingerprints": {child: obligation_by_id[child]["statement_fingerprint"] for child in children},
                "parent_interface_expression_fingerprint": INTERFACE_EXPRESSION_FINGERPRINTS[parent],
                "required_child_interface_expression_fingerprints": {child: INTERFACE_EXPRESSION_FINGERPRINTS[child] for child in children},
                "checked_declaration": declaration,
                "certificate_kind": kind,
                "status": "provisionally_elaborated_not_accepted",
                "introduces_undeclared_premises": False,
            })
        else:
            plans.append({
                "plan_id": "DECOMP-" + parent,
                "parent_obligation_id": parent,
                "planned_child_ids": children,
                "source_declaration": next(row["formal"] for row in SPECS if row["id"] == parent),
                "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
                "required_future_certificate": "An exact abstract-child harness must bind these fingerprints and consume every child before parent closure.",
            })
    proof_children = {child for values in REQUIRES.values() for child in values}
    proof_leaves = sorted(proof_children - set(REQUIRES))
    mandatory_root_overlays = [
        "M0821-S-INTERFACE", "M0821-S-BOUNDARY", "M0821-S-TRANSPORT",
        "M0821-S-FOUNDATION", "M0821-N-LOWER-MIDDLE",
    ]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": "THM-M-0821-ROOT",
        "edge_direction": "Proof requirements run parent to child; reciprocal checked composes or unverified logical-decomposition edges run child to parent. Workflow dependencies run task to prerequisite.",
        "workflow_task_nodes": workflow_tasks,
        "interface_expression_fingerprints": INTERFACE_EXPRESSION_FINGERPRINTS,
        "reciprocal_edge_type_contract": {
            "proof": {
                "proof_requires": ["composes", "logical_decomposition"],
                "composes": ["proof_requires"],
                "logical_decomposition": ["proof_requires"],
            },
            "refinement": {
                "logical_decomposition": ["refines"],
                "refines": ["logical_decomposition"],
                "expository_decomposition": ["documents"],
                "documents": ["expository_decomposition"],
                "equivalent_to": ["equivalent_to"],
            },
            "trust": {"trusts": ["trusted_by"], "trusted_by": ["trusts"]},
        },
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": certificates,
        "unverified_decomposition_plans": plans,
        "closure_boundary": {
            "closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "proof_leaf_cut_set": proof_leaves,
            "mandatory_root_overlay_cut_set": mandatory_root_overlays,
            "remaining_root_cut_set": mandatory_root_overlays + ["M0821-X-SOURCE", "M0821-X-PROVENANCE", "M0821-X-TRUST", "M0821-X-READABLE", "M0821-X-WORKFLOW", "proof-phase node receipts", "master acceptance"],
            "distinct_known_terminal_body_ids": sorted({row["terminal_proof_body_id"] for row in obligations if row["terminal_proof_body_id"]}),
            "candidate_evidence": "M0821-C01/E2 is exact and locally checked; current candidate status is M1, while M0-W remains a potential classification requiring an accepted E1 receipt.",
            "reason": "This phase freezes the architecture and checks only named package compositions and candidate interfaces. Internal LYM source decompositions require future exact composition certificates, and the downstream proof phase must install and validate the candidate.",
        },
    }
    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [{
            "recipe_id": "VAL-M0821-OBLIGATION-BUNDLE",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0821/check_obligation_tree.py"],
            "env_allowlist": {
                "PATH": "runner-provided tool path",
                "HOME": "runner-provided toolchain home",
                "TMPDIR": "runner-provided temporary directory",
                "PYTHONDONTWRITEBYTECODE": "1",
            },
            "timeout_seconds": 240,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [
                {"path_or_stream": "stdout", "semantic_hash_policy": "contains structural PASS line with obligation, edge, ledger, certificate, and plan counts"},
                {"path_or_stream": "stdout", "semantic_hash_policy": "contains accepted root H1/M3/R4, zero closed obligations, theorem_complete=false"},
            ],
            "covered_obligation_ids": ids,
            "covered_declarations": [
                "Stage1Instances.THM_M_0821.SpernerMaximumTarget",
                "IsAntichain.sperner",
                "Stage1Instances.THM_M_0821_Obligations.middleLayerAntichain_of_sized",
                "Stage1Instances.THM_M_0821_Obligations.attainment_of_middleLayer",
                "Stage1Instances.THM_M_0821_Obligations.upperBound_of_sperner",
                "Stage1Instances.THM_M_0821_Obligations.maximumSplit_of_packages",
                "Stage1Instances.THM_M_0821_Obligations.compose_root",
                "Stage1Instances.THM_M_0821_Obligations.root_of_terminal",
            ],
            "coverage_boundary": "The recipe structurally covers every registry node, but kernel declaration coverage is limited to the named target, terminal, candidate interfaces, and exact package compositions. Internal source-body child-to-parent compositions remain open.",
        }],
    }

    lines = [
        "# THM-M-0821 frozen obligation architecture", "", f"Item: `{ITEM}`.", "",
        f"Registry version 2 freezes {len(ids)} canonical obligations before proof-phase closure credit.",
        "The proof graph follows the pinned `IsAntichain.sperner` body through inverse-sum LYM,",
        "layer-density LYM, falling-family induction, shadow incidence counting, and the separate",
        "middle-layer attainment route. Provenance, evidence, trust, documentation, and workflow",
        "edges remain non-proof overlays.", "", "## Proof route", "", "```text",
        "ROOT -> exact root composition -> maximum conjunction split",
        "  attainment -> middleLayer construction -> sized -> antichain + binomial cardinality",
        "  upper bound -> IsAntichain.sperner -> choose-middle comparison + inverse-sum LYM",
        "    fiberwise slices + layer-density LYM -> falling top-part induction",
        "      slice/shadow identity + disjointness + local LYM",
        "        shadow incidence construction + bipartite double counting",
        "```", "",
        "Only the exact package boundaries listed in `composition_certificates` have checked",
        "abstract-child harnesses. Every internal relation is an explicit unverified source-body",
        "decomposition plan until a future proof-phase certificate consumes all child outputs.", "",
        "## Node ledger", "",
    ]
    for row in SPECS:
        lines.extend([
            f"### {row['id'].lower()}", "", row["claim"], "",
            f"Formal target: `{row['formal']}`.", "",
            f"Output: {row['output']}", "",
            f"Source boundary: {row['locator']}.", "",
            f"Budget: {row['budget']} substantive steps maximum; structured ledger: {len(semantic_ledger(row))} recorded step(s).", "",
        ])
    lines.extend([
        "## Freeze boundary", "",
        "All accepted machine obligations remain open and the root stays `[H1, M3, R4]`.",
        "Candidate `M0821-C01` is exact, pinned, sorry-free, and locally elaborated at `E2`, but",
        "the proof node, complete provenance/trust acceptance, primary-source `H0`, readable `R0`,",
        "hermetic replay, independent verification, audit completion, theorem completion, and master",
        "acceptance remain open. Any architecture or eligibility change requires a new registry",
        "version and append-only delta.", "",
    ])
    markdown = "\n".join(lines)
    return registry, bundle, recipes, markdown


def main() -> None:
    registry, bundle, recipes, markdown = build()
    for name, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", recipes),
    ):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    (HERE / "obligation-tree.md").write_text(markdown, encoding="utf-8")
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    print(f"wrote {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
