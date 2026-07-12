# THM-M-0843 frozen obligation architecture

Item: `S56-M-0843-OBLIGATION_TREE`.

Registry version 1 freezes 44 canonical obligations before proof-phase closure credit.
The proof graph follows the actual pinned `szemeredi_regularity` body through its cardinality
and tolerance splits, energy induction, increment construction, chunk-density engine, terminal
body, and exact adapter. Typed provenance, evidence, trust, documentation, and workflow edges
are separate and cannot act as proof premises.

## Proof route

The full planned reciprocal edge set is in `typed-graphs.json`. Only the root's exact abstract-
child composition is checked in this phase; every internal relation remains an explicitly
unverified source-body decomposition until an exact child-to-parent harness is accepted. The
main route is:

```text
ROOT -> exact adapter -> pinned upstream body -> cardinality split
  small graph -> bottom singleton equipartition
  large graph -> bounds -> tolerance split
    epsilon >= 1 -> initial equipartition is uniform
    epsilon <= 1 -> energy invariant -> zero/successor branches
      nonuniform successor -> iteration bounds -> increment
        equipartition + cardinality + energy increment
          chunk refinement + distinct pairs + density + count + sum recomposition
    terminal floor-plus-one energy contradiction
```

## Node ledger

### m0843-root

Every admissible finite simple graph has the exact frozen bounded epsilon-uniform equipartition.

Formal target: `Stage1Instances.THM_M_0843.SzemerediRegularityTarget`. Output: The canonical proposition at arbitrary universe u. Source boundary: Statement.lean; expression sha256 3fe13f3562cb642e45e467687508ac44f945e9848ff53d22b9cf068d7ec11219.
Budget: 12 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-s-target

Freeze graph, decidability, tolerance, lower bound, full-vertex finpartition, equitability, explicit bound, and uniformity interfaces.

Formal target: `Stage1Instances.THM_M_0843.SzemerediRegularityTarget`. Output: The exact elaborated root interface. Source boundary: Statement.lean:20-36.
Budget: 22 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-s-boundary

Retain epsilon positivity and l <= card alpha exactly, including l = 0 and empty or singleton types when the premise permits them.

Formal target: `the ordered binders and hypotheses of SzemerediRegularityTarget`. Output: No strengthened or omitted boundary premise. Source boundary: Statement.lean:24-36; statement.json encoding_decisions.boundaries.
Budget: 18 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-s-foundation

Account for classical choice, quotient soundness, propositional extensionality, Lean, mathlib, imports, and the no-oracle policy.

Formal target: `#print axioms szemeredi_regularity and the exact local adapters`. Output: A versioned foundation and TCB boundary. Source boundary: ObligationTree.lean axiom probes; anchor-audit.json immutable_environment.
Budget: 24 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-n-bounds

Relate l, initialBound epsilon l, iterated stepBound, and bound epsilon l with positivity and monotonicity.

Formal target: `planned signature: l <= initialBound epsilon l /\ 7 <= initialBound epsilon l /\ 0 < initialBound epsilon l /\ initialBound epsilon l <= bound epsilon l /\ (forall n, n <= stepBound n) /\ Monotone stepBound`. Output: All cardinal bounds used by the large-graph construction. Source boundary: Regularity/Bound.lean:167-200; Regularity/Lemma.lean:85-87,105-109,135-146.
Budget: 42 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-b-card-split

Split card alpha <= bound epsilon l from bound epsilon l <= card alpha and recombine exhaustively.

Formal target: `le_total (Fintype.card alpha) (SzemerediRegularity.bound epsilon l)`. Output: Either the singleton partition route or the iterative route. Source boundary: Regularity/Lemma.lean:79-84.
Budget: 12 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-b-small

For card alpha <= bound epsilon l, use the bottom singleton partition and prove all four conclusions.

Formal target: `Finpartition.bot_isEquipartition; card_bot; card_univ; Finpartition.bot_isUniform`. Output: An admissible partition in the small-cardinality branch. Source boundary: Regularity/Lemma.lean:80-83.
Budget: 18 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-b-large

For bound epsilon l <= card alpha, construct the initial partition and run the tolerance split.

Formal target: `planned signature: bound epsilon l <= Fintype.card alpha -> exists P : Finpartition univ, P.IsEquipartition /\ l <= P.parts.card /\ P.parts.card <= bound epsilon l /\ P.IsUniform G epsilon`. Output: An admissible partition in the large-cardinality branch. Source boundary: Regularity/Lemma.lean:84-155.
Budget: 16 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-c-initial

Construct an equipartition of univ with exactly initialBound epsilon l parts.

Formal target: `Finpartition.exists_equipartition_card_eq`. Output: dum with IsEquipartition and exact part cardinality. Source boundary: Regularity/Equitabilise.lean:195; Regularity/Lemma.lean:85-89.
Budget: 26 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-b-eps-split

Split 1 <= epsilon from epsilon <= 1 and recombine the easy and energy routes.

Formal target: `le_total 1 epsilon`. Output: An epsilon-uniform bounded equipartition in either tolerance branch. Source boundary: Regularity/Lemma.lean:90-155.
Budget: 12 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0843-b-eps-ge-one

When 1 <= epsilon, enlarge one-uniformity of the initial equipartition by monotonicity.

Formal target: `Finpartition.isUniform_one; Finpartition.IsUniform.mono`. Output: The initial equipartition is epsilon-uniform. Source boundary: Regularity/Lemma.lean:91-93.
Budget: 18 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-c-energy-invariant

For every i construct an equipartition between t and stepBound^[i] t that is uniform or has energy at least epsilon^5/4*i.

Formal target: `the local suffices h invariant in szemeredi_regularity`. Output: The induction invariant consumed by the terminal energy contradiction. Source boundary: Regularity/Lemma.lean:94-101,116-155.
Budget: 30 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-b-induct-zero

Establish the energy invariant at i = 0 from the initial partition and energy nonnegativity.

Formal target: `Finpartition.energy_nonneg`. Output: The i = 0 invariant instance. Source boundary: Regularity/Lemma.lean:119-123.
Budget: 16 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-b-induct-succ

At i+1 split whether the current partition is already uniform, preserving it or incrementing it.

Formal target: `by_cases huniform : P.IsUniform G epsilon`. Output: The successor invariant instance. Source boundary: Regularity/Lemma.lean:124-155.
Budget: 18 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-b-already-uniform

If P is uniform, reuse P and enlarge its iterate bound by le_stepBound.

Formal target: `Function.iterate_succ_apply'; SzemerediRegularity.le_stepBound`. Output: The successor invariant with its uniform disjunct. Source boundary: Regularity/Lemma.lean:127-131.
Budget: 14 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-b-nonuniform

If P is nonuniform, derive the numerical side conditions and use its increment to raise energy.

Formal target: `planned signature: not (P.IsUniform G epsilon) -> epsilon^5 / 4 * i <= P.energy G -> exists Q, Q.IsEquipartition /\ t <= Q.parts.card /\ Q.parts.card <= (stepBound^[i+1]) t /\ epsilon^5 / 4 * (i+1) <= Q.energy G`. Output: The successor invariant with its energy disjunct. Source boundary: Regularity/Lemma.lean:132-155.
Budget: 24 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-n-iteration

Derive 100 <= 4^card(P.parts)*epsilon^5, i <= 4/epsilon^5, the terminal iterate bound, and the graph-cardinality side condition.

Formal target: `planned signature: 100 <= 4^P.parts.card * epsilon^5 /\ (i : Real) <= 4 / epsilon^5 /\ P.parts.card <= (stepBound^[floor(4/epsilon^5)]) t /\ P.parts.card * 16^P.parts.card <= Fintype.card alpha`. Output: All hypotheses needed by card_increment and energy_increment. Source boundary: Regularity/Lemma.lean:134-146.
Budget: 48 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0843-c-increment

Construct the refinement P.increment and assemble its equitability, cardinal bounds, and raised-energy result.

Formal target: `SzemerediRegularity.increment`. Output: A successor-stage equipartition satisfying the invariant. Source boundary: Regularity/Increment.lean:52-59; Regularity/Lemma.lean:147-155.
Budget: 22 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0843-l-increment-equip

Show that gluing the equitable chunks produces an equipartition.

Formal target: `SzemerediRegularity.increment_isEquipartition`. Output: (increment hP G epsilon).IsEquipartition. Source boundary: Regularity/Increment.lean:79-86.
Budget: 18 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-l-increment-card

Compute the increment partition cardinality as stepBound of the old part count.

Formal target: `SzemerediRegularity.card_increment`. Output: card(increment.parts) = stepBound card(P.parts). Source boundary: Regularity/Increment.lean:65-77.
Budget: 32 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-l-energy-increment

Raise energy by epsilon^5/4 for a large enough nonuniform equitable partition.

Formal target: `SzemerediRegularity.energy_increment`. Output: energy(P)+epsilon^5/4 <= energy(increment P). Source boundary: Regularity/Increment.lean:138-182.
Budget: 28 substantive steps maximum; structured ledger: 6 recorded step(s).

### m0843-c-chunk-refinement

Break each old part along nonuniform witnesses, equitabilise it, and bind all chunks into increment.

Formal target: `SzemerediRegularity.chunk; Finpartition.equitabilise; SzemerediRegularity.increment`. Output: A controlled refinement whose pieces have size m or m+1. Source boundary: Regularity/Chunk.lean:62-71,172-187; Regularity/Equitabilise.lean:149-195; Regularity/Increment.lean:52-86.
Budget: 88 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0843-c-equitabilise

Equitabilise a finite partition using the quotient/remainder cardinal decomposition and retain exact small/big part counts.

Formal target: `Finpartition.equitabilise; Finpartition.equitabilise_isEquipartition; Finpartition.card_parts_equitabilise`. Output: An equipartition with controlled part count and sizes. Source boundary: Regularity/Equitabilise.lean:45-195.
Budget: 72 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0843-c-chunk-witnesses

Form the star families from nonuniformity witnesses and show they lie in the chunk partition.

Formal target: `SzemerediRegularity.star; SzemerediRegularity.biUnion_star_subset_nonuniformWitness; SzemerediRegularity.star_subset_chunk`. Output: Witness-aligned subfamilies of every chunk. Source boundary: Regularity/Chunk.lean:62-120.
Budget: 70 substantive steps maximum; structured ledger: 5 recorded step(s).

### m0843-l-chunk-card

Prove exact chunk part count and the m to m+1 cardinal bounds for every member.

Formal target: `SzemerediRegularity.card_chunk; SzemerediRegularity.card_eq_of_mem_parts_chunk; SzemerediRegularity.m_le_card_of_mem_chunk_parts; SzemerediRegularity.card_le_m_add_one_of_mem_chunk_parts`. Output: Controlled chunk cardinality and member sizes. Source boundary: Regularity/Chunk.lean:172-187.
Budget: 36 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-c-distinct-pairs

Index chunk pairs over old off-diagonal pairs, prove containment in the new off-diagonal set, and prove pairwise disjointness.

Formal target: `SzemerediRegularity.distinctPairs and its two private support theorems`. Output: A disjoint reindexing domain for the energy sum. Source boundary: Regularity/Increment.lean:88-121.
Budget: 44 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-c-distinct-contain

Show the union of chunk-pair families is contained in the increment partition's off-diagonal pair set.

Formal target: `SzemerediRegularity.distinctPairs_increment (private theorem)`. Output: Containment needed for monotonicity of the nonnegative energy sum. Source boundary: Regularity/Increment.lean:96-106.
Budget: 28 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-c-distinct-disjoint

Show chunk-pair families indexed by different old off-diagonal pairs are pairwise disjoint.

Formal target: `SzemerediRegularity.pairwiseDisjoint_distinctPairs (private lemma)`. Output: Disjointness needed by sum_biUnion. Source boundary: Regularity/Increment.lean:108-121.
Budget: 32 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-l-chunk-density

For uniform and nonuniform old pairs, bound the normalized sum of squared chunk densities with the required epsilon gain or loss.

Formal target: `le_sum_distinctPairs_edgeDensity_sq using edgeDensity_chunk_uniform and edgeDensity_chunk_not_uniform`. Output: The pointwise squared-density inequality for each old pair. Source boundary: Regularity/Increment.lean:125-136; Regularity/Chunk.lean:335-509.
Budget: 96 substantive steps maximum; structured ledger: 5 recorded step(s).

### m0843-l-chunk-average

Bound the weighted average density of chunk pairs near the old total density using size control.

Formal target: `SzemerediRegularity.average_density_near_total_density (private theorem)`. Output: The average-density approximation used in both pair cases. Source boundary: Regularity/Chunk.lean:190-357.
Budget: 86 substantive steps maximum; structured ledger: 5 recorded step(s).

### m0843-l-chunk-aux

Bound the square of the old pair density by the square of the average chunk density, up to epsilon^5/25.

Formal target: `SzemerediRegularity.edgeDensity_chunk_aux (private theorem)`. Output: The common squared-average lower bound used by both chunk density branches. Source boundary: Regularity/Chunk.lean:335-360.
Budget: 48 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0843-l-density-star

Control star-family density and prove its witness subsets are large enough for nonuniformity.

Formal target: `SzemerediRegularity.abs_density_star_sub_density_le_eps; SzemerediRegularity.eps_le_card_star_div; SzemerediRegularity.edgeDensity_star_not_uniform`. Output: A density-separated star subfamily for every nonuniform pair. Source boundary: Regularity/Chunk.lean:362-452.
Budget: 90 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-l-density-nonuniform

Convert the star density separation into a squared-density gain for a nonuniform old pair.

Formal target: `SzemerediRegularity.edgeDensity_chunk_not_uniform`. Output: The nonuniform-pair chunk inequality. Source boundary: Regularity/Chunk.lean:454-503.
Budget: 78 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-l-density-uniform

Use convexity of squares and the average-density approximation to prevent excessive energy loss for a uniform old pair.

Formal target: `SzemerediRegularity.edgeDensity_chunk_uniform`. Output: The uniform-pair chunk inequality. Source boundary: Regularity/Chunk.lean:505-522.
Budget: 42 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-l-nonuniform-count

Convert failure of partition uniformity and the seven-part lower bound into the cardinal inequality that pays for the epsilon^5/4 gain.

Formal target: `Finpartition.IsUniform definition; offDiag_card; the arithmetic tail of energy_increment`. Output: A lower bound on the contribution of nonuniform pairs. Source boundary: Regularity/Uniform.lean:196-235; Regularity/Increment.lean:159-182.
Budget: 58 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0843-l-energy-recompose

Rewrite old and new energies as squared-density sums, reindex the disjoint chunk pairs, and compare to the full new off-diagonal sum.

Formal target: `Finpartition.coe_energy; sum_biUnion; sum_le_sum_of_subset_of_nonneg`. Output: The global energy inequality from the pointwise chunk bounds. Source boundary: Regularity/Energy.lean:38-63; Regularity/Increment.lean:143-169.
Budget: 70 substantive steps maximum; structured ledger: 5 recorded step(s).

### m0843-l-energy-coe

Rewrite rational partition energy as a real normalized off-diagonal squared-density sum.

Formal target: `Finpartition.coe_energy`. Output: A real-valued sum representation of energy. Source boundary: Regularity/Energy.lean:38-63.
Budget: 28 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0843-l-energy-sum

Reindex the sum over pairwise-disjoint distinctPairs families and compare the contained subfamily to the full increment off-diagonal sum.

Formal target: `Finset.sum_biUnion; Finset.sum_le_sum_of_subset_of_nonneg`. Output: The global new-partition sum bound. Source boundary: Regularity/Increment.lean:147-157.
Budget: 38 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0843-b-energy-contradiction

Choose floor(4/epsilon^5)+1, rule out its energy alternative using strict growth and energy <= 1, and discharge the final bound.

Formal target: `Nat.lt_floor_add_one; Finpartition.energy_le_one; SzemerediRegularity.bound`. Output: The uniform partition returned by the energy route. Source boundary: Regularity/Lemma.lean:100-115.
Budget: 42 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0843-t-upstream

Compose the cardinal split, initial construction, tolerance split, energy induction, increment engine, and contradiction.

Formal target: `szemeredi_regularity`. Output: The literal pinned mathlib proposition. Source boundary: Regularity/Lemma.lean:74-155.
Budget: 34 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0843-t-adapter

Apply the literal pinned terminal proposition at the exact canonical binders.

Formal target: `Stage1Instances.THM_M_0843_Obligations.terminal_adapter`. Output: The exact frozen root proposition. Source boundary: ObligationTree.lean: terminal_adapter and compose_root.
Budget: 12 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-x-source

Map every material node to reviewed human sources with edition, page, assumptions, proof steps, and errata.

Formal target: `node-specific primary-source crosswalk remains open`. Output: Human-source coverage without machine proof credit. Source boundary: source-statement-crosswalk.md; anchor-audit.json source_leads.
Budget: 36 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-x-provenance

Bind wrapper, terminal and support bodies, immutable source hashes, licenses, direct dependencies, and replay evidence without duplicate credit.

Formal target: `anchor-audit.json candidate M0843-C01 plus a future transitive closure packet`. Output: Proof-body provenance without mathematical proof credit. Source boundary: anchor-audit.json; anchor-audit-receipt.json.
Budget: 38 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0843-x-trust

Audit the transitive Lean/mathlib declaration closure, compiled artifacts, executables, unsafe/oracle boundaries, and independent replay.

Formal target: `Lean 4.29.0; mathlib 8a178386; release trust closure pending`. Output: Release-grade trust inventory without mathematical proof credit. Source boundary: anchor-audit.json immutable_environment and foundation_assessment.
Budget: 40 substantive steps maximum; structured ledger: 1 recorded step(s).

## Freeze boundary

All machine obligations remain open at accepted `M3`. Candidate `M0843-C01` is exact, pinned,
sorry-free, and locally elaborated at `E2`, but rev-5.6 requires an accepted `E1` receipt before
`M0-W`; the downstream proof task and master acceptance are therefore not preempted. Primary-source
`H0`, readable `R0`, transitive provenance/TCB, hermetic replay, independent verification, audit
completion, and theorem completion remain open. Any architectural or eligibility change requires
a new registry version and append-only delta.
