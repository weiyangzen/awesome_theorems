# Scope map

## Included claim

- A Banach space over the real or complex scalar field fixed by the selected source.
- A linear operator with explicitly represented domain, closed graph, and dense domain.
- A strongly continuous (`C0`) one-parameter semigroup of bounded linear operators on nonnegative
  time, its infinitesimal generator, and any uniqueness conclusion in the selected formulation.
- The appropriate real half-line in the resolvent set of the operator.
- The complete family of resolvent-power bounds, with every quantified parameter, exponent,
  constant, and strict inequality preserved.
- Both directions of the generator characterization for one single, source-backed variant.

## Statement decisions still open

The statement phase must select either the contraction form or the general exponentially bounded
form with constants such as `M` and `omega`. It must fix real versus complex scalars, the sign of the
generator, whether the resolvent is written using `lambda I - A`, the range and strictness of
`lambda`, the positive-power indexing convention, the topology used for strong continuity, and
whether uniqueness and the growth estimate are inside the equivalence or separate consequences.
The zero space and all domain/coercion conventions must also be handled explicitly.

## Explicit exclusions

- A bounded-operator exponential result in place of the unbounded-generator theorem.
- The Lumer-Phillips dissipativity theorem, Stone's theorem, or a finite-dimensional matrix theorem.
- A one-way necessary condition presented as the generation equivalence.
- A structure that assumes the generator identification, resolvent estimates, or uniqueness as
  opaque proposition fields.
- Reuse of `THM-M-1041`, `S1_M_234.lean`, or their wrappers as proof or statement-identity credit.

The later statement phase owns the concrete Lean APIs and elaborated expression. This intake freezes
the mathematical family and its exclusions without inventing those missing implementation choices.
