# Scope map

## Preserved repository boundary

- Catalog title: `Markov分割` (`Markov partition`).
- Attribution and date: Yakov Sinai and Rufus Bowen, 1970.
- Literal gloss: `双曲系统的符号化` (`symbolization of hyperbolic systems`).
- Intended subject: a source-selected theorem connecting Markov partitions with hyperbolic
  dynamics and symbolic dynamics.
- Assurance boundary: the catalog's `已验证` field is discovery metadata and supplies no human
  source, exact statement, or kernel-proof credit.

The Bowen and Sinai papers listed in the source crosswalk make a classical theorem family highly
plausible. They do not make any one formulation canonical without inspection of the actual theorem
text and definitions.

## Decisions required at statement freeze

The dependent statement phase must approve an immutable source passage and freeze all of the
following before writing a canonical proposition:

1. Whether the root asserts existence of a Markov partition, existence at every sufficiently small
   scale, construction of a symbolic coding, or a bundle of existence and coding conclusions.
2. Whether the system is an Axiom A diffeomorphism, an Anosov diffeomorphism, Sinai's
   `C`-diffeomorphism, a hyperbolic homeomorphism, or another exact source class, including smoothness
   and invertibility hypotheses.
3. Whether the domain is the full compact manifold, the nonwandering set, one basic set, a locally
   maximal hyperbolic set, or another invariant subset.
4. The exact definition of a rectangle: product-bracket closure, stable/unstable plaques, closure of
   interior, diameter bound, and treatment relative to the invariant set.
5. The exact partition conditions: finite cover versus literal partition, disjoint interiors,
   overlaps on boundaries, and the forward/backward stable and unstable Markov inclusions.
6. How the transition relation or matrix is defined, and whether the symbolic system is a one-sided
   or two-sided full shift, subshift, or subshift of finite type.
7. The direction of the itinerary/coding map and the exact intertwining law with the shift.
8. Whether the coding is continuous, surjective, injective, finite-to-one, one-to-one off a boundary
   orbit set, a semiconjugacy, or a conjugacy; each additional conclusion must be source-mapped.
9. Boundary and degenerate behavior: empty/singleton invariant sets, empty rectangles, multiple
   names, periodic boundary orbits, zero transition matrices, nontransitive components, and scale
   parameters at or beyond the expansivity bound.
10. Lean universes and representations for manifolds, differentiability, hyperbolicity, local
    product structure, partitions, symbolic paths, and any alternate encoding with checked
    transports.

## Explicit exclusions

- The generic definition of a set partition, stream shift, or function semiconjugacy as the target.
- A theorem about arbitrary finite covers without stable/unstable rectangle and Markov conditions.
- A statement that assumes the desired Markov partition or coding as an input field and merely
  projects it.
- A shift-map theorem (`THM-M-1402`), symbolic-dynamics topic theorem (`THM-M-1401`), entropy result
  (`THM-M-1403` through `THM-M-1406`), spectral decomposition (`THM-M-1414`), or another neighboring
  target substituted for this one.
- A special horseshoe, toral automorphism, or geodesic-flow construction unless the approved source
  selects exactly that scope.
- Measure-theoretic Markov chains, Markov kernels/categories, probability inequalities, interval
  Markov partitions, or graph partitions merely because they share the name `Markov`.
- Conjugacy silently substituted for a finite-to-one semiconjugacy, or a one-sided coding silently
  substituted for an invertible two-sided system.
- The catalog label `已验证`, a paper title, bibliographic metadata, or an API probe as proof.

No canonical mathematical claim, Lean expression, discovery protocol, or obligation registry is
frozen in this intake. Those remain blocked on exact source and statement selection.
