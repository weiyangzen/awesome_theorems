# Scope map

## Preserved theorem family

The intake preserves the catalog's group Jordan-Holder family: two composition series of the same
group have the same finite length and, after permuting indices, isomorphic successive quotient
factors. This is a scope description, not the frozen canonical proposition.

Milne's inspected formulation uses finite subnormal chains from the group to the trivial subgroup,
with each term normal in its predecessor and each quotient nontrivial and simple. The source audit
must decide whether the root is Theorem 6.2 for finite groups or the conditional extension to any
group admitting a finite composition series.

## Decisions required at statement freeze

1. Select an immutable primary or otherwise approved statement and incorporated definitions with
   a complete premise, conclusion, correction, translation, and reviewer crosswalk.
2. Fix whether `G` is finite, of finite length, or arbitrary with two finite composition series
   supplied as hypotheses.
3. Define a composition series, including indexing/order orientation, strictness, endpoints, and
   whether each subgroup is normal only in its successor or normal in the whole group.
4. Fix the simplicity convention for successive quotients, including nontriviality.
5. Fix quotient construction and prove all normality obligations needed for each factor.
6. Define equivalence: equal lengths plus a permutation and group isomorphism of corresponding
   factors, or an exactly source-equivalent bundled relation.
7. Decide whether existence of a composition series belongs to the root or only uniqueness
   conditional on two supplied series.
8. Freeze universes, ordered binders, explicit and typeclass hypotheses, conclusion, logical
   profiles, and any abstract-lattice alternate encoding with a checked group transport.

## Boundary cases

Source and statement review must explicitly address the trivial group; a simple group and its
one-factor series; length-zero series; equal or definitionally identical series; finite groups for
which composition-series existence is derived; infinite groups that admit finite composition
series; repeated isomorphic factors; quotient orientation; and chains with repeated terms or
nonsimple factors, which should not qualify as composition series.

## Excluded substitutions

- Equality of series lengths alone is weaker than matching simple quotient factors.
- Existence of a composition series does not prove uniqueness.
- Schreier refinement alone is an ingredient, not the final composition-factor equivalence.
- Chief, derived, central, normal, or arbitrary subgroup series are different notions unless a
  checked source bridge establishes the exact requested claim.
- Requiring every term to be normal in the whole group may improperly narrow the standard
  subnormal-series theorem.
- A module, category-theoretic, monoid, or abstract-lattice theorem cannot replace the group result
  without a checked group specialization and source mapping.
- A class or structure that stores factor equivalence as input data merely assumes the result.
- The catalog label, a theorem name, `#check`, or the abstract mathlib declaration alone supplies
  no H0 or M0 credit.

## Formal boundary

No canonical Lean expression is frozen at intake. The narrow probe imports
`Mathlib.Order.JordanHolder` and authenticates its generic theorem, equivalence relation, and axiom
report. That module has no checked subgroup instance in the pinned revision. This omission is
substantive: group quotients require proof that each lower subgroup is normal in its immediate
successor, while the abstract class's `Iso` receives only pairs of lattice elements. A faithful
proof-carrying group realization or another checked transport belongs to later work after source
approval; globally normal subgroups must not be chosen merely to simplify quotients.
