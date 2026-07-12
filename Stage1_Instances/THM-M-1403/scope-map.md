# Scope map

## Preserved source scope

- Subject: topological entropy of a dynamical system.
- Historical locator: Adler, Konheim, and McAndrew; 1965.
- Intended role: quantify dynamical complexity rather than measure-theoretic randomness alone.
- Target kind: one source-selected mathematical proposition about topological entropy, not an
  arbitrary nearby entropy fact.

This boundary does not yet select a proposition. The title can denote the invariant's definition,
its existence or limiting construction, invariance under conjugacy, monotonicity under factor
maps, equivalence of definitions, or a property or computation for a particular system.

## Decisions required at statement freeze

The next phase must freeze all of the following from an inspected source passage:

1. A discrete-time self-map versus a flow or group action.
2. Compact Hausdorff, general topological, uniform, or metric phase space, including separation and
   compactness assumptions and the exact continuity condition on the dynamics.
3. Entropy of the whole space versus a specified invariant or arbitrary subset.
4. The AKM finite-open-cover construction, a Bowen-Dinaburg entourage-cover construction, a
   separated/spanning-set construction, or a checked relationship between them.
5. Cover refinement and join conventions, cardinality, logarithm base, limit versus limsup/liminf,
   supremum, and the real or extended-real codomain.
6. The exact conclusion: definition well-posedness, equality of variants, conjugacy invariance,
   factor monotonicity, restriction coherence, or another named property.
7. Empty-space/subset behavior, singleton systems, infinite entropy, non-invariant subsets,
   noncompact spaces, and discontinuous maps.

## Explicit exclusions

- Measure-theoretic or Kolmogorov-Sinai entropy as a substitute; those have separate repository
  targets `THM-M-1404` and `THM-M-1406`.
- A shift-specific entropy result or the shift map itself as the root; `THM-M-1402` is separate.
- Shannon, binary, thermodynamic, differential, or algebraic entropy without a source transport.
- A definition packaged as data followed by a tautological projection.
- `Dynamics.coverEntropy_nonneg`, the liminf/limsup equality, cover/net equality, semiconjugacy
  inequality, restriction theorem, subset monotonicity, closure, or union law merely because pinned
  mathlib provides it.
- Silent replacement of the historical AKM open-cover formulation by mathlib's documented
  Bowen-Dinaburg uniform-space/subset formulation.
- The repository label `verified` as human-source or Lean proof evidence.

No canonical Lean proposition is frozen at intake. Candidate APIs remain discovery-only until a
pinpoint source and a reviewed source-to-expression crosswalk select one claim.
