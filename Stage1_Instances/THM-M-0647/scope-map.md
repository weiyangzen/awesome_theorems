# Scope map

## Included claim

- A first-order language `L` and an infinite `L`-structure `M`.
- An infinite cardinal `kappa` large enough for the language symbols.
- Existence of an `L`-structure `N` with cardinality `kappa`.
- Elementary equivalence of `M` and `N`, meaning agreement on every `L`-sentence.
- Both smaller and larger cardinalities when their respective cardinal inequalities permit them;
  this explains the conventional Lowenheim-Skolem-Tarski family behind the short source gloss.

## Decisions reserved for the statement phase

Primary-source review must decide whether the root quantifies over every admissible `kappa`, merely
asserts one model of a different cardinality, or separately conjoins upward and downward forms. It
must also fix the nonempty-structure convention, exact lower bound (`aleph_0`, `#L`, or their max),
cardinal and universe lifts, and whether the conclusion asks only for elementary equivalence or an
elementary embedding in the size-dependent direction.

## Boundaries and exclusions

- `THM-M-0646` (plain Lowenheim-Skolem) and `THM-M-0648` (explicit upward/downward theorem) are
  adjacent records, not interchangeable proof credit. The statement audit must document any
  semantic overlap without changing this target's source phrase.
- The downward theorem alone, the upward theorem alone, compactness alone, or Skolemization alone
  is not substituted for the combined/different-cardinality claim.
- Isomorphism is not substituted for elementary equivalence; an abstract structure containing the
  requested model as data is not a proof.
- Finite models and cardinals below the required language-size bound are outside the intended root.

## Formal surface map

The candidate mathlib API uses `FirstOrder.Language`, an instance `[L.Structure M]`, `[Infinite M]`,
`Cardinal`, `CategoryTheory.Bundled L.Structure`, and `M ≅[L] N`. The exact wrapper and minimal import
are deliberately not frozen during intake. `Mathlib.ModelTheory.Satisfiability` is a candidate
import, not yet an accepted canonical module.
