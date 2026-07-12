# Scope map

## Included topic boundary

- A source-specified Fourier multiplier theorem on a specified Euclidean space or locally compact
  abelian group.
- A symbol `m` defined away from frequency zero, with the source's exact differentiability and
  scale-invariant derivative estimates.
- An initial multiplier operator on a dense test-function class and its asserted bounded extension
  to `L^p`, including the exact exponent range and norm estimate.
- All Fourier-transform, measure, multi-index, scalar-field, and almost-everywhere conventions.

## Ambiguities to resolve at statement freeze

The familiar Euclidean formulation assumes bounds of the shape
`|x|^|alpha| * |D^alpha m(x)| <= C` for finitely many multi-indices and concludes `L^p`
boundedness for `1 < p < infinity`. That description is only a theorem family. Sources differ on:

1. the required derivative cutoff (`floor (n / 2) + 1`, all orders through another integer, or a
   Sobolev/annular condition);
2. pointwise derivatives versus weak derivatives and uniform pointwise versus annular integral
   bounds;
3. scalar complex symbols versus operator-valued or vector-valued generalizations;
4. whether the result states bounded extension, a quantitative operator-norm estimate, weak type,
   or an endpoint conclusion;
5. treatment of the origin, representatives of `m`, the initial Schwartz-class definition, and
   uniqueness of the `L^p` extension.

The statement phase must inspect an immutable source and freeze each choice, all ordered binders,
the dimension and exponent inequalities, derivative convention, constants, and boundary cases.

## Explicit exclusions

- Plancherel's `L^2` multiplier bound as a substitute for the general `1 < p < infinity` theorem.
- A Fourier multiplier merely defined on Schwartz functions or tempered distributions without an
  `L^p` bounded-extension conclusion.
- The Marcinkiewicz, Hormander, or Hörmander-Mikhlin multiplier theorem under a different regularity
  criterion unless a checked source transport establishes the selected equivalence.
- A bounded symbol with the desired `L^p` operator bound assumed as a hypothesis.
- Torus, compact-group, bilinear, pseudodifferential, or endpoint variants as silent replacements.
- The repository label `已验证` or its Helgason attribution as proof or source-fidelity evidence.

No canonical Lean target is frozen at intake because the repository record does not uniquely state
one.

