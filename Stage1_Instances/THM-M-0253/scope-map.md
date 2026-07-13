# Scope map

## Preserved theorem family

The intake preserves the Carleson 1958 bounded-analytic interpolation family suggested jointly by
the catalog title, attribution, date, and Hardy-space gloss. A candidate reading concerns when a
sequence of points in the complex unit disc permits bounded scalar data to be interpolated by a
bounded analytic function. That sentence is a scope description, not the frozen canonical claim.

The repository does not authorize silently replacing "Hardy spaces" by `H^infinity`, selecting a
geometric characterization, or treating several equivalent classical formulations as
definitionally identical. Every credited root and alternate encoding needs a pinpoint source
crosswalk and a checked transport.

## Proposition-changing decisions

An approved exact source statement must freeze all of the following:

1. The domain: unit disc, upper half-plane, or another conformally equivalent model, including the
   chosen transport and boundary conventions.
2. The function space: `H^infinity`, one fixed `H^p`, every `H^p`, a multiplier algebra, or another
   Hardy-type space; also scalar or vector values and the exact norm model.
3. The sequence representation and index type, countability, injectivity/distinctness, repetitions,
   interior membership, finite versus infinite sequences, and accumulation behavior.
4. The interpolation predicate: which data space is quantified over, whether every bounded scalar
   sequence must be realized exactly, and whether a uniform norm bound or optimal interpolation
   constant is part of the claim.
5. The characterization selected as the conclusion: uniform pseudohyperbolic separation, a lower
   bound involving a Blaschke product or product of pairwise factors, a Carleson measure condition,
   bounded evaluation-map surjectivity, or a source-selected conjunction/equivalence.
6. Every normalization for pseudohyperbolic distance, Blaschke factors/products, boundary measure,
   Carleson boxes, evaluation operators, and constants.
7. The ordered binders, quantifier dependencies, hypotheses, conclusion, universes, typeclass
   context, foundation profile, and every alternate encoding with its checked relationship.

These choices change the proposition or its proof boundary. The intake records them without
selecting among them.

## Degenerate and boundary cases

Source review must explicitly dispose of the empty and singleton sequences; finite sequences;
repeated points; a point at zero; sequences approaching the unit circle; interior accumulation;
noninjective enumerations of the same set; permutations and subsequences; zero and constant data;
real versus complex data; nonpositive or unattained separation constants; divergent infinite
products; and any boundary point or upper-half-plane point at infinity. No case is silently
excluded while the root is unfrozen.

## Excluded substitutions

- Nevanlinna-Pick interpolation for finitely many prescribed values is not by itself the requested
  characterization of universal interpolating sequences.
- Lagrange, polynomial, Fourier, spline, Sobolev, real-method, complex-method, or model-theoretic
  interpolation theorems are different targets.
- Interpolation in Bergman, Dirichlet, Bloch, Nevanlinna, Smirnov, Fock, de Branges, several-variable,
  weighted, or vector-valued spaces cannot replace the selected Hardy-space result.
- The Carleson measure theorem and Corona theorem are related but distinct results; neither grants
  the root statement or proof by name or shared author.
- A one-way necessary condition, sufficient condition, finite special case, or pre-assumed
  separation/interpolation structure cannot substitute for a source-selected equivalence.
- A structure field, axiom, oracle, numeric experiment, theorem name, API probe, or the catalog's
  untrusted `已验证` label supplies no proof credit.

## Neighbor boundaries

`THM-M-0250` separately owns the broad Hardy-space-theory topic, and `THM-M-0252` the Corona
problem. `THM-M-0372` owns a Carleson-measure characterization family, `THM-M-0373` another Corona
entry, and `THM-M-0374` a generic harmonic-analysis interpolation label. These may eventually
provide explicit checked dependencies or require duplicate reconciliation, but no dossier shares
statement identity or proof status automatically.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks the unit-disc carrier,
analyticity, bounded ranges, sequences, injectivity, and a canonical factor. A bounded search of
repo-local Lean and pinned mathlib found no exact interpolating-sequence, Hardy-space, Carleson-
sequence, or pseudohyperbolic declaration. Mathlib's canonical factor has a pole at its parameter
and is not directly the usual zero-at-the-point factor used in pseudohyperbolic products; a checked
orientation/reciprocal transport would be required. The file also explicitly leaves the full
Blaschke-product decomposition as a TODO. This is scoped intake evidence, not a global
absence theorem or the downstream immutable anchor audit.
