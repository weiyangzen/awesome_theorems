# THM-M-0821 frozen obligation architecture

Item: `S56-M-0821-OBLIGATION_TREE`.

Registry version 2 freezes 36 canonical obligations before proof-phase closure credit.
The proof graph follows the pinned `IsAntichain.sperner` body through inverse-sum LYM,
layer-density LYM, falling-family induction, shadow incidence counting, and the separate
middle-layer attainment route. Provenance, evidence, trust, documentation, and workflow
edges remain non-proof overlays.

## Proof route

```text
ROOT -> exact root composition -> maximum conjunction split
  attainment -> middleLayer construction -> sized -> antichain + binomial cardinality
  upper bound -> IsAntichain.sperner -> choose-middle comparison + inverse-sum LYM
    fiberwise slices + layer-density LYM -> falling top-part induction
      slice/shadow identity + disjointness + local LYM
        shadow incidence construction + bipartite double counting
```

Only the exact package boundaries listed in `composition_certificates` have checked
abstract-child harnesses. Every internal relation is an explicit unverified source-body
decomposition plan until a future proof-phase certificate consumes all child outputs.

## Node ledger

### m0821-root

Every finite Boolean lattice has maximum antichain cardinality choose(n, floor(n/2)): the value is attained and bounds every antichain.

Formal target: `Stage1Instances.THM_M_0821.SpernerMaximumTarget`.

Output: The exact frozen root proposition at arbitrary universe u.

Source boundary: Statement.lean:30-37; expression sha256 8f5d05428a35e3b6f13947097ac52417ba900b3cf9b1b45c0bb173766c914d7c.

Budget: 12 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0821-s-interface

Preserve the arbitrary finite ground type, finite family of finite subsets, strict distinct-member antichain relation, existential witness, and universal bound.

Formal target: `Stage1Instances.THM_M_0821.SpernerMaximumTarget`.

Output: The exact binder and conclusion interface.

Source boundary: Statement.lean:16-37; statement.json.

Budget: 22 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0821-s-boundary

Include empty and singleton ground types and families, both parities, natural floor division, and no equality-classification claim.

Formal target: `(Stage1Instances.THM_M_0821.middleLayer (Fin 0) = {∅}) /\ (Stage1Instances.THM_M_0821.middleLayer (Fin 1) = {∅})`.

Output: No strengthened premise, omitted degenerate case, or stronger equality conclusion.

Source boundary: Statement.lean:30-37,64-70; statement.json encoding_decisions.

Budget: 18 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-s-transport

Relate the existential maximum target to the concrete lower-middle-layer form without using the Sperner upper-bound proof.

Formal target: `Stage1Instances.THM_M_0821.spernerMaximumTarget_iff_middleLayerMaximumTarget`.

Output: A checked iff with the universal-bound conjunct unchanged.

Source boundary: Statement.lean:39-62.

Budget: 18 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-s-foundation

Account for propext, Classical.choice, Quot.sound, the Lean/mathlib pins, imports, and the no-oracle policy.

Formal target: `planned signature: every checked declaration in validation-specs.json has a machine-derived axiom set contained in {propext, Classical.choice, Quot.sound} and no prohibited proof boundary`.

Output: A versioned foundation, TCB, and computation boundary.

Source boundary: ObligationTree.lean axiom probes; anchor-audit.json immutable_environment.

Budget: 24 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-n-lower-middle

Select floor(n/2) as the canonical lower middle rank; for odd n the adjacent upper rank has equal size but is unnecessary for the maximum value.

Formal target: `forall r n : Nat, Nat.choose n r <= Nat.choose n (n / 2)`.

Output: The canonical rank and maximal binomial coefficient used by both branches.

Source boundary: Statement.lean:21-23; LYM.lean:236-243; Nat.choose_le_middle.

Budget: 20 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-n-no-other

Record that the chosen mathlib route needs no further symmetry, representation, finite/infinite, or local/global normalization.

Formal target: `planned review proposition: the proof graph is total on the frozen finite Boolean-lattice encoding without another normalization node`.

Output: A reviewed layer-exclusion decision only; no proof premise.

Source boundary: Blueprint section 6.4; target finite Boolean-lattice encoding.

Budget: 8 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0821-b-maximum

Split the exact maximum claim into attainment and universal upper-bound branches and recombine both exhaustively.

Formal target: `Stage1Instances.THM_M_0821_Obligations.AttainmentPackage -> Stage1Instances.THM_M_0821_Obligations.UpperBoundPackage -> Stage1Instances.THM_M_0821_Obligations.MaximumSplit`.

Output: Both conjuncts required by the root.

Source boundary: ObligationTree.lean:91-95.

Budget: 12 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0821-b-no-cases

Record that the pinned proof is uniform over ground-set cardinality and parity after the maximum-conjunction split.

Formal target: `planned review proposition: IsAntichain.sperner has no parity or cardinality case split outside its internal uniform inequalities`.

Output: A reviewed no-additional-case-split decision only.

Source boundary: LYM.lean:232-245; Statement.lean boundary probes.

Budget: 8 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0821-c-middle-layer

Construct the lower-middle layer as powersetCard floor(n/2) univ.

Formal target: `Stage1Instances.THM_M_0821_Obligations.MiddleLayerDefinitionPackage`.

Output: The explicit finite family used as an extremizer.

Source boundary: Statement.lean:21-23; ObligationTree.lean:30-34,119-122.

Budget: 14 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-c-middle-sized

Show that every subset in the raw lower-middle powerset slice has cardinality floor(n/2).

Formal target: `Stage1Instances.THM_M_0821_Obligations.MiddleLayerSizedPackage`.

Output: The fixed-rank invariant consumed by antichain construction.

Source boundary: Mathlib/Data/Finset/Slice.lean:86-88; ObligationTree.lean:36-42,124-129.

Budget: 12 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-l-middle-antichain

A fixed-rank family is an antichain under inclusion, hence the selected middle layer is a Sperner family.

Formal target: `Stage1Instances.THM_M_0821_Obligations.MiddleLayerSizedPackage -> Stage1Instances.THM_M_0821_Obligations.MiddleLayerAntichainPackage`.

Output: The antichain half of the attaining witness.

Source boundary: Mathlib/Data/Finset/Slice.lean:44-47; ObligationTree.lean:67-72.

Budget: 18 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-l-middle-card

Count the lower-middle powerset slice by the binomial coefficient.

Formal target: `Stage1Instances.THM_M_0821_Obligations.MiddleLayerCardinalityPackage`.

Output: The exact cardinality half of the attaining witness.

Source boundary: Mathlib/Data/Finset/Powerset.lean:198-202; ObligationTree.lean:51-57,131-135.

Budget: 14 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-l-sperner-upper

Bound every finite antichain by the middle binomial coefficient using the pinned terminal theorem.

Formal target: `Stage1Instances.THM_M_0821_Obligations.UpperBoundPackage`.

Output: The complete universal upper-bound package.

Source boundary: Mathlib/Combinatorics/SetFamily/LYM.lean:232-245; IsAntichain.sperner.

Budget: 20 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0821-l-choose-middle

Bound each rank binomial coefficient by the lower-middle coefficient and prove positivity of both denominators used in Sperner's argument.

Formal target: `planned signature: forall (alpha : Type*) [Fintype alpha] (s : Finset alpha), 0 < Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2) /\ 0 < Nat.choose (Fintype.card alpha) s.card /\ ((Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2) : ℚ≥0)^-1 <= (Nat.choose (Fintype.card alpha) s.card : ℚ≥0)^-1)`.

Output: The denominator positivity and inverse coefficient comparison used in the Sperner corollary.

Source boundary: LYM.lean:236-243; Nat.choose_le_middle; Nat.choose_pos.

Budget: 18 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0821-l-lym-inv

Bound the sum over family members of inverse rank-binomial coefficients by one.

Formal target: `planned specialization: forall (alpha : Type*) [Fintype alpha] (A : Finset (Finset alpha)), IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> (sum s in A, (Nat.choose (Fintype.card alpha) s.card : ℚ≥0)^-1) <= 1`.

Output: The inverse-sum LYM inequality consumed by Sperner's bound.

Source boundary: LYM.lean:216-228; Finset.lubell_yamamoto_meshalkin_inequality_sum_inv_choose.

Budget: 30 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-n-fiberwise-slices

Regroup the member-wise inverse-binomial sum by subset cardinality and identify each fiber with a family slice.

Formal target: `planned signature: forall (alpha : Type*) [Fintype alpha] (A : Finset (Finset alpha)), (sum s in A, (Nat.choose (Fintype.card alpha) s.card : ℚ≥0)^-1) = sum r in Finset.range (Fintype.card alpha + 1), ((A.slice r).card : ℚ≥0) / Nat.choose (Fintype.card alpha) r`.

Output: Equality between the inverse-member sum and the layer-density sum.

Source boundary: LYM.lean:219-227; Slice.lean:117-139; Algebra/BigOperators/Group/Finset/Basic.lean:263-269; Finset.sum_fiberwise_of_maps_to'.

Budget: 28 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0821-l-lym-card

Bound the sum of the family densities in every Boolean-lattice rank by one.

Formal target: `planned specialization: forall (alpha : Type*) [Fintype alpha] (A : Finset (Finset alpha)), IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> (sum r in Finset.range (Fintype.card alpha + 1), ((A.slice r).card : ℚ≥0) / Nat.choose (Fintype.card alpha) r) <= 1`.

Output: The cardinality-slice LYM inequality.

Source boundary: LYM.lean:197-211; Finset.lubell_yamamoto_meshalkin_inequality_sum_card_div_choose.

Budget: 26 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-l-falling-zero

At k = card alpha, bound falling 0 A by the zero layer and normalize choose(n, 0) to one.

Formal target: `planned signature: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)), ((Finset.falling 0 A).card : ℚ≥0) / (Nat.choose (Fintype.card alpha) 0 : ℚ≥0) <= 1`.

Output: The normalized zero-rank falling-family density is at most one.

Source boundary: LYM.lean:205-211; Set.Sized.card_le (Finset.sized_falling 0 A).

Budget: 18 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-c-falling

Construct falling k A, characterize its members, and establish its size and slice-containment invariants.

Formal target: `planned package signature: forall (alpha : Type*) [DecidableEq alpha] (k : Nat) (A : Finset (Finset alpha)), (forall s, s in Finset.falling k A <-> (exists t in A, s ⊆ t) /\ s.card = k) /\ Set.Sized k (Finset.falling k A : Set (Finset alpha)) /\ A.slice k ⊆ Finset.falling k A`.

Output: The rank-normalized down-family and the exact invariants used by the LYM induction.

Source boundary: LYM.lean:123-142; Finset.falling, Finset.mem_falling, Finset.sized_falling, Finset.slice_subset_falling.

Budget: 30 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0821-l-falling-top

Induct on the top k+1 layers to bound their density sum by the normalized size of the corresponding falling family.

Formal target: `planned ℚ≥0 specialization: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)) (k : Nat), k <= Fintype.card alpha -> IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> (sum r in Finset.range (k + 1), ((A.slice (Fintype.card alpha - r)).card : ℚ≥0) / Nat.choose (Fintype.card alpha) (Fintype.card alpha - r)) <= ((Finset.falling (Fintype.card alpha - k) A).card : ℚ≥0) / Nat.choose (Fintype.card alpha) (Fintype.card alpha - k)`.

Output: The top-part inequality specialized to NNRat for every legal top-layer index.

Source boundary: LYM.lean:169-191; Finset.le_card_falling_div_choose.

Budget: 42 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-b-falling-induction

Handle the zero and successor induction branches and recombine them into the falling top-part inequality.

Formal target: `planned package signature: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)), IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> forall k, k <= Fintype.card alpha -> (sum r in Finset.range (k + 1), ((A.slice (Fintype.card alpha - r)).card : ℚ≥0) / Nat.choose (Fintype.card alpha) (Fintype.card alpha - r)) <= ((Finset.falling (Fintype.card alpha - k) A).card : ℚ≥0) / Nat.choose (Fintype.card alpha) (Fintype.card alpha - k)`.

Output: The complete top-layer falling-family inequality for every legal induction index.

Source boundary: LYM.lean:173-191; Finset.le_card_falling_div_choose.

Budget: 24 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0821-l-slice-shadow

Decompose falling k A as the current k-slice union the shadow of falling(k+1) A.

Formal target: `forall (alpha : Type*) [DecidableEq alpha] (A : Finset (Finset alpha)) (k : Nat), A.slice k ∪ (Finset.falling (k + 1) A).shadow = Finset.falling k A`.

Output: The exact set-family identity used in the successor step.

Source boundary: LYM.lean:141-159; Finset.slice_union_shadow_falling_succ.

Budget: 24 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0821-l-disjoint-shadow

Use the antichain premise to make the current slice disjoint from the next falling shadow.

Formal target: `forall (alpha : Type*) [DecidableEq alpha] {A : Finset (Finset alpha)} {m n : Nat}, IsAntichain ((.) ⊆ (.)) (A : Set (Finset alpha)) -> Disjoint (A.slice m) (Finset.falling n A).shadow`.

Output: The disjointness needed for cardinality addition.

Source boundary: LYM.lean:162-171; Finset.IsAntichain.disjoint_slice_shadow_falling.

Budget: 20 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0821-l-local-lym

Compare a fixed-rank family density with its downward shadow density, including the nonzero-rank and denominator conditions.

Formal target: `planned ℚ≥0 specialization: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)) (r : Nat), Not (r = 0) -> Set.Sized r (A : Set (Finset alpha)) -> (A.card : ℚ≥0) / Nat.choose (Fintype.card alpha) r <= (A.shadow.card : ℚ≥0) / Nat.choose (Fintype.card alpha) (r - 1)`.

Output: The local LYM inequality used in the successor induction step.

Source boundary: LYM.lean:91-113; Finset.local_lubell_yamamoto_meshalkin_inequality_div.

Budget: 38 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-l-local-lym-mul

Double count deletion/insertion incidences to obtain the denominator-cleared local LYM inequality.

Formal target: `forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)) (r : Nat), Set.Sized r (A : Set (Finset alpha)) -> A.card * r <= A.shadow.card * (Fintype.card alpha - r + 1)`.

Output: A.card * r <= A.shadow.card * (Fintype.card alpha - r + 1).

Source boundary: LYM.lean:64-86; Finset.local_lubell_yamamoto_meshalkin_inequality_mul.

Budget: 44 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0821-c-shadow

Construct the downward shadow, identify deletion/insertion witnesses, and derive the two incidence-degree bounds used by local LYM.

Formal target: `planned package signature: forall (alpha : Type*) [DecidableEq alpha] [Fintype alpha] (A : Finset (Finset alpha)) (r : Nat), Set.Sized r (A : Set (Finset alpha)) -> (forall b in A, r <= #(A.shadow.bipartiteBelow ((.) ⊆ (.)) b)) /\ (forall a in A.shadow, #(A.bipartiteAbove ((.) ⊆ (.)) a) <= Fintype.card alpha - r + 1)`.

Output: The shadow family and the exact lower/upper incidence-degree bounds.

Source boundary: Mathlib/Combinatorics/SetFamily/Shadow.lean:62-115,165-171; LYM.lean:68-85.

Budget: 34 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0821-l-double-count

Apply the bipartite card-product inequality to the deletion/insertion incidence relation.

Formal target: `forall finite s t and decidable relation R, (forall b in t, n <= #(s.bipartiteBelow R b)) -> (forall a in s, #(t.bipartiteAbove R a) <= m) -> #t * n <= #s * m`.

Output: The incidence-cardinality comparison underlying local LYM.

Source boundary: LYM.lean:68-75; DoubleCounting.lean:170-182; Finset.card_mul_le_card_mul'.

Budget: 26 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0821-t-attain

Assemble the explicit middle layer, its fixed-rank antichain property, and its cardinality into the attaining package.

Formal target: `Stage1Instances.THM_M_0821_Obligations.attainment_of_middleLayer`.

Output: AttainmentPackage for every finite ground type.

Source boundary: ObligationTree.lean.

Budget: 18 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0821-t-upper

Package the exact imported Sperner conclusion as the universal upper-bound branch.

Formal target: `Stage1Instances.THM_M_0821_Obligations.upperBound_of_sperner`.

Output: UpperBoundPackage for every finite ground type and antichain.

Source boundary: ObligationTree.lean.

Budget: 12 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-t-root-compose

Transport the exact recombined maximum conjunction to the frozen target.

Formal target: `Stage1Instances.THM_M_0821_Obligations.MaximumSplit -> Stage1Instances.THM_M_0821.SpernerMaximumTarget`.

Output: Stage1Instances.THM_M_0821.SpernerMaximumTarget.

Source boundary: ObligationTree.lean:97-101.

Budget: 16 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0821-x-source

Map every mathematical node to the 1928 source and modern support sources with exact locators, assumptions, translations, proof steps, errata, and independent review.

Formal target: `planned record predicate: each required_human_source ID has a pinpoint primary-source crosswalk and independent source-review receipt`.

Output: Human-source evidence without machine-proof credit.

Source boundary: source-statement-crosswalk.md; printed pages 544-548.

Budget: 48 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0821-x-provenance

Bind wrapper, terminal, support body, source hashes, licenses, direct and transitive declarations, and receipts without duplicate proof-body credit.

Formal target: `planned record predicate: every formal body ID has an immutable origin, source hash, direct dependencies, and transitive trust-closure hash`.

Output: Proof-body provenance without mathematical proof credit.

Source boundary: anchor-audit.json; anchor-audit-receipt.json.

Budget: 42 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0821-x-trust

Audit the transitive Lean/mathlib declaration closure, compiled artifacts, executables, axioms, unsafe/oracle boundaries, and independent replay.

Formal target: `planned record predicate: all root-relevant declarations, imported artifacts, executables, axioms, and oracle boundaries are inside an accepted TCB profile`.

Output: Release-grade trust inventory without proof credit.

Source boundary: anchor-audit.json immutable_environment; ObligationTree.lean axiom probes.

Budget: 42 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0821-x-readable

Produce an independently reviewed readable reconstruction with one stable section per required node and every source/formal anchor.

Formal target: `planned record predicate: each required_readable ID has the ten ordered section-8 fields and an independent reader receipt`.

Output: Reader-facing coverage without machine-proof credit.

Source boundary: obligation-tree.md is architecture only.

Budget: 60 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0821-x-workflow

Require dependency-legal proof, validation, release, freshness, revocation, and independent-verification receipts before root promotion.

Formal target: `planned record predicate: task acceptance is topologically legal and all freshness, revocation, validation, and release gates are accepted`.

Output: Workflow acceptance boundary without proof credit.

Source boundary: Docs/Stage1_Execution_DAG_rev-5.6.json.

Budget: 20 substantive steps maximum; structured ledger: 1 recorded step(s).

## Freeze boundary

All accepted machine obligations remain open and the root stays `[H1, M3, R4]`.
Candidate `M0821-C01` is exact, pinned, sorry-free, and locally elaborated at `E2`, but
the proof node, complete provenance/trust acceptance, primary-source `H0`, readable `R0`,
hermetic replay, independent verification, audit completion, theorem completion, and master
acceptance remain open. Any architecture or eligibility change requires a new registry
version and append-only delta.
