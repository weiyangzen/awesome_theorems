# Scope map

## Included claim

- A real Banach space; the selected contraction variant fixes the scalar field to `Real`.
- A linear operator with explicitly represented domain, closed graph, and dense domain.
- A strongly continuous (`C0`) one-parameter semigroup of bounded linear operators on nonnegative
  time, its infinitesimal generator, and any uniqueness conclusion in the selected formulation.
- The appropriate real half-line in the resolvent set of the operator.
- For every real `a > 0`, a bounded two-sided inverse of `a I - A` with the contraction resolvent
  estimate `||R y|| <= a^-1 ||y||`.
- Both directions of the generator characterization for one single, source-backed variant.

## Frozen statement decisions

The statement selects the contraction form over a real Banach space, with nonnegative time,
pointwise orbit continuity, and `||T(t)x|| <= ||x||`. The generator graph is equality with the
strong right derivative at zero. The zero space is included; `a = 0`, the general `M, omega` form,
complex scalars, and a separate uniqueness clause are excluded from this variant.

## Explicit exclusions

- A bounded-operator exponential result in place of the unbounded-generator theorem.
- The Lumer-Phillips dissipativity theorem, Stone's theorem, or a finite-dimensional matrix theorem.
- A one-way necessary condition presented as the generation equivalence.
- A structure that assumes the generator identification, resolvent estimates, or uniqueness as
  opaque proposition fields.
- Reuse of `THM-M-1041`, `S1_M_234.lean`, or their wrappers as proof or statement-identity credit.

`Statement.lean` owns the concrete Lean APIs and elaborated expression. Source-fidelity review and
all proof obligations remain downstream.
