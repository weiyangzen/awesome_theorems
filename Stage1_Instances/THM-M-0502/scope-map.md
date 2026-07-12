# Scope map

## Included theorem family

- A finite family of primitive Dirichlet characters with conductor bounded by a common parameter
  `Q`.
- Real characters and real zeros of their complex Dirichlet L-functions near `s = 1`.
- The Page/Landau-Page conclusion that at most one exceptional member occurs in a uniform
  source-specified zero region.
- The source-level constants, threshold, interval endpoints, and uniqueness unit (character,
  primitive character, or character-zero pair) once pinned during the statement phase.

The intended root is a uniform uniqueness theorem, not the bare proposition that some L-function
has some real zero. That repository phrase is retained as provenance but cannot determine the
formal target.

## Statement decisions still open

The next phase must select one pinpoint theorem and freeze:

1. whether the conductor family is `q <= Q`, `q q' <= Q`, or another historically equivalent
   parameterization;
2. the exact near-one region and the dependence of its absolute constant;
3. whether zeros are quantified only on the real axis or inside a complex rectangle;
4. whether the conclusion says at most one exceptional character, one exceptional zero, or both;
5. whether simplicity, reality, primitiveness, quadraticity, or a lower bound for `1 - beta` is
   part of the root or a corollary;
6. how the principal character, modulus one, induced characters, and duplicate primitive
   representatives are treated.

## Formal object boundary

The pinned mathlib environment has `DirichletCharacter.LFunction` and basic analytic results for
complex-valued Dirichlet characters. Intake does not establish APIs for conductor-minimal primitive
representatives, a finite sigma type ranging over all moduli up to `Q`, real-character predicates,
zero counting, or the Page zero-free constant. Those are statement and anchor-audit obligations.

## Explicit exclusions

- Existence of an exceptional zero; Page's theorem permits there to be none.
- Nonvanishing only on `re s >= 1`, which is adjacent but does not give the uniform near-one region.
- Siegel's theorem, the Deuring-Heilbronn repulsion phenomenon, a prime number theorem in arithmetic
  progressions, or a zero-density estimate as a substitute for the Page conclusion.
- The generalized Riemann hypothesis or a claim about arbitrary L-functions.
- A finite computational search for zeros or an abstract structure carrying the desired result as
  assumed data.
