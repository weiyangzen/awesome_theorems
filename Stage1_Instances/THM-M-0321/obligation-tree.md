# Frozen obligation architecture

This is an architecture freeze, not a proof or closure report. Every node remains open.

## Proof flow

The checked root composition consumes `FiniteFamilyStep` and `CompactnessUpgrade`. The former is expanded through finite induction and the one-map fixed-point engine; the latter is expanded through closed fixed sets and compact finite-intersection reasoning.

## ROOT

**Claim:** The exact Markov-Kakutani common-fixed-point theorem for an arbitrary commuting family.

**Formal target:** `Stage1Instances.THM_M_0321.MarkovKakutaniTarget`

**Output:** The canonical theorem.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## S-EXACT

**Claim:** Freeze the exact ambient-map statement and every hypothesis.

**Formal target:** `Stage1Instances.THM_M_0321.MarkovKakutaniTarget`

**Output:** The exact root interface.

**Step budget:** `8`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## S-DEFS

**Claim:** Fix affinity on K, invariance, and common fixed point definitions.

**Formal target:** `IsAffineOn; MapsTo; HasCommonFixedPoint`

**Output:** Definitions with no hidden subtype affine structure.

**Step budget:** `8`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## S-CONTEXT

**Claim:** Fix universes and the Hausdorff locally convex real topological-module context.

**Formal target:** `Statement.lean ordered binders`

**Output:** The context inherited by every mathematical child.

**Step budget:** `7`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## S-BOUNDARY

**Claim:** Retain empty index types and all nonempty compact convex K, including singleton K.

**Formal target:** `emptyFamily_boundary`

**Output:** Boundary-complete scope.

**Step budget:** `6`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## S-TRANSPORT

**Claim:** Transport only through the checked EqOn commutation equivalence.

**Formal target:** `markovKakutaniTarget_iff_eqOnCommutationTarget`

**Output:** A bidirectional exact statement transport.

**Step budget:** `4`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## S-FOUNDATION

**Claim:** Audit classical choice, compactness, topology, and the complete kernel/dependency trust boundary.

**Formal target:** `#print axioms of terminal declarations`

**Output:** A versioned foundation and TCB report.

**Step budget:** `10`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## N-FINITE

**Claim:** Reduce the mathematical core to common fixed points for every finite subfamily.

**Formal target:** `FiniteFamilyStep`

**Output:** Finite-subfamily nonemptiness.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## N-INFINITE

**Claim:** Upgrade finite-subfamily fixed points to the full arbitrary family by compactness.

**Formal target:** `CompactnessUpgrade`

**Output:** A common fixed point for all indices.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## B-FINITE-EMPTY

**Claim:** Establish the finite-family base case from K.Nonempty.

**Formal target:** `planned: Finset.empty fixed-point base`

**Output:** The empty finite subfamily has a common fixed point.

**Step budget:** `8`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## B-FINITE-INSERT

**Claim:** For insert i s, restrict f i to the common fixed set of s and obtain a fixed point there.

**Formal target:** `planned: Finset.induction insert branch`

**Output:** A point fixed by every member of insert i s.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## B-RECOMPOSE

**Claim:** Prove the empty and insert branches exhaust all finite subfamilies.

**Formal target:** `planned: Finset.induction recomposition`

**Output:** FiniteFamilyStep.

**Step budget:** `8`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## C-FIXSET

**Claim:** Construct K intersected with the equalizer f i x = x for a selected map.

**Formal target:** `planned: fixedSetWithin K (f i)`

**Output:** The restricted fixed-point carrier.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## C-RESTRICT

**Claim:** Restrict every commuting map to each earlier common fixed set.

**Formal target:** `planned: restricted ambient self-map`

**Output:** A well-defined continuous affine self-map on the invariant carrier.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## C-AVERAGE

**Claim:** Construct Cesaro averages for one affine self-map and keep them inside K.

**Formal target:** `planned: (n+1)^-1 • ∑ k in range (n+1), f^[k] x`

**Output:** A net/sequence of approximate fixed points in K.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## C-FIP

**Claim:** Construct the closed fixed subsets of K and their finite intersections.

**Formal target:** `planned: {x ∈ K | f i x = x}`

**Output:** A closed family with the finite-intersection property.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## L-SINGLE

**Claim:** A continuous affine self-map of nonempty compact convex K has a fixed point.

**Formal target:** `planned: singleMap_fixedPoint`

**Output:** One-map fixed-point existence.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## L-AVERAGE-IN-K

**Claim:** Every Cesaro average lies in K by convexity and invariance.

**Formal target:** `planned: cesaroAverage_mem`

**Output:** Membership of all averages in K.

**Step budget:** `20`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## L-AVERAGE-DEFECT

**Claim:** The displacement of Cesaro averages tends to zero by telescoping and boundedness.

**Formal target:** `planned: tendsto_cesaro_displacement_zero`

**Output:** Approximate fixed-point convergence.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## L-CLUSTER

**Claim:** Compactness supplies a cluster point and continuity makes it a genuine fixed point.

**Formal target:** `planned: clusterPoint_isFixedPt`

**Output:** A fixed point of the selected map in K.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## L-FIXSET-COMPACT

**Claim:** The fixed-point subset inside K is compact.

**Formal target:** `planned: isCompact_fixedSetWithin`

**Output:** Compactness of the induction carrier.

**Step budget:** `15`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## L-FIXSET-CONVEX

**Claim:** Affinity makes the fixed-point subset inside K convex.

**Formal target:** `planned: convex_fixedSetWithin`

**Output:** Convexity of the induction carrier.

**Step budget:** `15`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## L-COMMUTE-INVARIANT

**Claim:** Pairwise commutation makes each remaining map preserve prior common fixed points.

**Formal target:** `planned: MapsTo on common fixed set`

**Output:** Invariance required for restriction.

**Step budget:** `18`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## L-FIP-COMPACT

**Claim:** A compact space's closed subsets with the finite-intersection property have nonempty total intersection.

**Formal target:** `planned: IsCompact nonempty_iInter_of_directed`

**Output:** A point in every fixed subset.

**Step budget:** `split-required`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## X-SOURCE

**Claim:** Pinpoint each proof package to primary Markov/Kakutani theorem text and errata.

**Formal target:** `source-statement-crosswalk.md; primary pages pending`

**Output:** Human-source boundary.

**Step budget:** `20`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## X-LEAN

**Claim:** Resolve every imported Lean theorem and terminal proof body used by proof execution.

**Formal target:** `anchor-audit.json; exact candidate absent`

**Output:** Formal provenance boundary.

**Step budget:** `15`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## X-TCB

**Claim:** Record transitive declarations, axioms, toolchain, dependencies, and replay boundary.

**Formal target:** `Lean 4.29.0; mathlib 8a178386; closure pending`

**Output:** Trusted-computing-base boundary.

**Step budget:** `15`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## T-FINITE

**Claim:** Assemble the finite induction into FiniteFamilyStep.

**Formal target:** `FiniteFamilyStep`

**Output:** The first premise of root_compose.

**Step budget:** `12`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## T-UPGRADE

**Claim:** Assemble closed fixed sets and compact FIP into CompactnessUpgrade.

**Formal target:** `CompactnessUpgrade`

**Output:** The second premise of root_compose.

**Step budget:** `12`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.

## T-ASSEMBLE

**Claim:** Consume both exact child propositions and return the canonical target.

**Formal target:** `Stage1Instances.THM_M_0321.ObligationTree.root_compose`

**Output:** MarkovKakutaniTarget.

**Step budget:** `6`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.
