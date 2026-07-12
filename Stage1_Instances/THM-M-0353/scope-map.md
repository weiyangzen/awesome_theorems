# Scope map

## Included theorem family

- A sequence indexed by `n : Nat` of explicitly normalized Hermite functions on `Real`.
- The `L^2` space for Lebesgue measure, over the real or complex scalars selected by the source.
- Pairwise orthonormality of the represented `L^2` vectors.
- Completeness: their linear span is dense in the whole `L^2` space, packaged equivalently as a
  `HilbertBasis` only after checked transport.

## Decisions required at statement freeze

The repository gloss does not say whether it uses the physicists' polynomials
`H_n(x)` with a Gaussian factor `exp (-x^2 / 2)` or the probabilists' polynomials
`He_n(x)` with the corresponding rescaling. The statement phase must select a stable source and
freeze the polynomial convention, all normalization constants, the real-versus-complex codomain,
Lebesgue measure, equality almost everywhere, the concrete `L^2` representation, binder order, and
whether "basis" is expressed as dense span, trivial orthogonal complement, or `HilbertBasis`.

Boundary checks must include index zero, positivity/nonvanishing of normalization constants,
measurability and square-integrability of every function, and the transport between any weighted
polynomial theorem and the unweighted Hermite-function theorem.

## Explicit exclusions

- Orthogonality or degree facts for Hermite polynomials without completeness of the functions.
- A finite Hermite expansion or density of arbitrary polynomials as the terminal claim.
- An arbitrary `HilbertBasis` whose vectors are not definitionally or propositionally identified
  with the selected Hermite functions.
- Completeness of harmonic-oscillator eigenvectors without a checked identification with the
  selected functions in the selected `L^2` space.
- Weighted Gaussian `L^2`, complex Hermite functions, or a rescaled convention as a substitute
  unless an exact checked isometric transport is supplied.
- Higher-dimensional tensor-product Hermite bases and distributional expansions.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean proposition is frozen during intake because the constants and representation
needed to make the functions literal have not been sourced.

