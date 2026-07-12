# Scope map

## Included theorem family

- A source-selected probability-preserving discrete dynamical system.
- A source-selected measurable partition and its iterated pullbacks or translates.
- The sigma-algebra generation condition, with the source's exact completion and almost-everywhere
  convention.
- The entropy of a partition, entropy relative to the transformation, and system entropy under one
  consistent normalization.
- A source-selected conclusion connecting a generating partition to the system entropy. The
  leading candidate is the equality `h_mu(T) = h_mu(T, xi)`, but intake does not freeze it.

## Statement-phase decisions

The repository wording does not determine:

1. Whether the space is a standard/Lebesgue probability space or an arbitrary probability space.
2. Whether `T` is an invertible bimeasurable automorphism or a noninvertible endomorphism, and
   whether partition iterates are indexed by `Z` or `N`.
3. Whether `xi` is finite or countable and, for a countable partition, which finite-entropy
   hypothesis is required.
4. Whether generating means literal sigma-algebra equality or equality after completion modulo
   null sets.
5. The definitions of partition join, Shannon entropy, relative dynamical entropy, system entropy,
   logarithm base, and extended-real values.
6. Whether ergodicity is assumed. The author-written candidate statement does not display such an
   assumption, so intake does not add it.
7. How null atoms, the one-atom partition, zero entropy, infinite entropy, and completed measurable
   spaces are handled.

These choices must come from an immutable source statement and definitions, not from a convenient
Lean encoding. The statement phase must freeze ordered binders, all hypotheses, every boundary
case, an elaborated expression fingerprint, and non-equivalent mutations before any proof search.

## Explicit exclusions

- Sinai's Bernoulli factor theorem or an existence theorem for Bernoulli factors.
- Krieger's finite generator theorem, Rokhlin's countable generator results, or any theorem that
  constructs a generator from an entropy bound.
- The definition, existence, or isomorphism invariance of Kolmogorov-Sinai entropy by itself.
- Topological entropy, Bernoulli-shift entropy computations, or symbolic coding alone.
- A theorem that assumes the desired entropy equality, or hides measure entropy and generation in
  unconstrained proposition-valued inputs.
- The neighboring `THM-M-1406` Kolmogorov-Sinai entropy record as a substitute for this target.
- The catalogue label `已验证` as evidence of a human proof or Lean kernel closure.

No canonical Lean target is frozen at intake. The scope records what must be decided without
silently selecting a nearby theorem.
