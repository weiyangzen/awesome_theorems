# Scope map

## Included claim

- A Banach space `X` over a scalar field fixed by the chosen source.
- A densely defined linear operator `A` with closed graph.
- A strongly continuous (`C0`) semigroup of bounded linear operators and its infinitesimal
  generator.
- Membership of an appropriate real half-line in the resolvent set of `A` and the corresponding
  resolvent-power estimates.
- Both directions of the generation characterization, with uniqueness where the source includes it.

## Decisions deferred to statement freeze

Source inspection must choose between the contraction form and the exponentially bounded form
with constants `M` and `omega`. It must also fix real versus complex scalars, sign conventions for
the generator and resolvent, whether all powers `n >= 1` are quantified, the precise strictness of
`lambda > omega`, and whether uniqueness and the semigroup growth estimate are conclusions or part
of an equivalence. Degenerate spaces and domain coercions must be made explicit.

## Explicit exclusions

- The bounded-operator exponential theorem as a substitute for unbounded generators.
- The Lumer-Phillips dissipativity characterization or the Stone theorem as the target theorem.
- A finite-dimensional matrix-only specialization.
- Any structure that assumes resolvent conditions or generator identification as opaque fields.
- Treating the legacy `StatementShape` or projection lemmas as terminal proof evidence.

The statement phase must define or select concrete APIs for closed densely defined operators,
resolvents and their powers, `C0` semigroups, growth bounds, and infinitesimal generators.
