# Scope map

## Preserved theorem family

The repository identifies the classical completeness property of the ordered real numbers, but its
one-line gloss does not choose an exact member of that family. The intake preserves that ambiguity
rather than replacing it with the most convenient mathlib declaration.

## Candidate formulations

1. **Least-upper-bound completeness:** every nonempty subset `s : Set Real` that is bounded above
   has an element `x` with `IsLUB s x`.
2. **Greatest-lower-bound completeness:** the order-dual statement for nonempty bounded-below sets.
3. **Dedekind-cut continuity:** every separation of all reals into a lower and upper class, with
   every lower element below every upper element, is produced by a unique boundary real.
4. **Metric/Cauchy completeness:** every Cauchy sequence or Cauchy filter of real numbers converges.
5. **Equivalent analysis forms:** convergence of bounded monotone sequences, the nested-interval
   property, and related convergence principles under their precise hypotheses.

These formulations are mathematically related, but their equivalence is neither definitional nor
part of the catalog record. A future source-reviewed statement may select one and credit another
only through an explicit checked transport in the required direction.

## Decisions required at statement freeze

1. Select and independently review an immutable source edition and exact theorem/page or archival
   passage, including incorporated definitions, assumptions, proof boundary, corrections, and the
   relationship to both named attributions.
2. Fix order completeness, cut continuity, metric completeness, or another exact formulation as the
   root; do not conflate the real-number construction with a derived completeness theorem.
3. For the least-upper-bound form, fix the subset carrier, nonemptiness, boundedness, `IsLUB` versus
   chosen `sSup` conclusion, quantifier order, and whether the lower-bound dual is part of the root.
4. For the cut form, fix that the two classes cover all reals, their overlap/disjointness and
   emptiness conditions, strict separation, endpoint ownership, and the exact meaning and uniqueness
   of a boundary producing the cut.
5. For the metric form, fix sequences versus filters or nets, the Cauchy predicate, index order,
   topology/metric, explicit existential limit versus a `CompleteSpace` instance, and convergence
   mode.
6. Fix domains, ordered binders, hypotheses, conclusion, universes, alternate encodings and
   transport directions, foundation policy, trusted base, and noncomputable choice boundary.
7. Resolve empty and unbounded sets, singleton and finite sets, constant sequences, empty classes,
   endpoints belonging to either class, uniqueness, and any reliance on the Archimedean property.

## Non-substitution boundary

- Completeness of `Rat`, an irrationality example, density of rationals, or the Archimedean
  property is not real completeness.
- A greatest-lower-bound, monotone-convergence, nested-interval, or Cauchy statement cannot replace
  a selected least-upper-bound root without a checked relationship.
- A theorem assuming `[ConditionallyCompleteLinearOrder Real]` or `[CompleteSpace Real]` cannot
  establish the corresponding instance when that instance is the intended conclusion.
- The existence of `sSup s` as a totalized operation does not by itself prove that it is a least
  upper bound; empty or unbounded-set conventions must not broaden the root.
- The catalog's `已验证` label, a theorem-name match, the inspected translation, and a successful API
  probe supply no H0 or M0 credit.

## Pinned formal boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Data.Real.Archimedean` proves `Real.exists_isLUB` and builds
`Real.instConditionallyCompleteLinearOrder`; module `Mathlib.Topology.UniformSpace.Real` builds
`Real.instCompleteSpace`, after which `cauchySeq_tendsto_of_complete` provides sequence convergence.
These are high-quality formal leads only. Exact statement selection, minimal imports, expression and
environment fingerprints, checked transports, mutation tests, proof-body provenance, and trust
acceptance belong to downstream phases.
