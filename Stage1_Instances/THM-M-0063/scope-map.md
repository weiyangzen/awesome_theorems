# Scope map

## Preserved theorem family

The intake preserves the literal catalog claim: every group is isomorphic to some permutation
group. In the standard modern reading, an arbitrary group `G` maps each `g` to the permutation
`x |-> g * x` of its underlying set. This left-regular representation is injective, so `G` is
isomorphic to its image, a subgroup of `Equiv.Perm G`.

That paragraph is a scope description, not the frozen canonical proposition. The statement phase
must select an exact, source-reviewed encoding and elaborate it in the pinned environment.

## Decisions required at statement freeze

1. Fix the group carrier universe, the `[Group G]` binder, and whether the theorem is represented as
   a universally quantified declaration or as a construction parameterized by `G`.
2. Define "permutation group" as a subgroup of `Equiv.Perm X` for an explicitly quantified carrier
   `X`; decide whether `X` is existential or fixed to the underlying type `G`.
3. Fix the regular-action orientation. The usual map `g |-> (x |-> g * x)` is a homomorphism under
   mathlib's permutation multiplication; right multiplication may require inversion or an
   opposite-group transport.
4. Decide whether the conclusion exposes an injective `MonoidHom`, an isomorphism to its range, an
   existential subgroup plus `MulEquiv`, or checked equivalent formulations. An injection alone is
   not silently identified with the catalog's isomorphism wording.
5. If `Equiv.Perm.subgroupOfMulAction G G` is selected, fix the action/typeclass synthesis and check
   the exact specialization, expression fingerprint, minimal import, and declaration provenance.
6. Freeze the foundation, choice and quotient policy. The inspected declaration reports `propext`,
   `Classical.choice`, and `Quot.sound`; no smaller trust claim is made at intake.
7. Resolve all ordered binders, implicit typeclasses, conclusion, alternate directions, mutation
   tests, environment fingerprint, source passage, correction history, and independent review.

## Degenerate and boundary cases

The theorem includes the trivial group, finite groups, and infinite groups. It does not require
`Finite`, `Fintype`, `DecidableEq`, or countability. Universe-polymorphic group carriers must not be
silently restricted to a small or finite symmetric group. For the trivial group, the regular image
is the trivial subgroup of the singleton permutation group. For nontrivial groups, injectivity must
come from faithfulness of multiplication rather than from an assumed embedding. The range subtype
must carry the subgroup structure used by the claimed `MulEquiv`.

## Explicit substitutions excluded

- The false stronger claim that every group is isomorphic to the entire `Equiv.Perm G` is excluded.
- The finite-only statement that every finite group embeds into a finite symmetric group does not
  cover arbitrary groups.
- An arbitrary group action is insufficient unless its faithfulness is established; a nonfaithful
  action represents only a quotient.
- An injective function that does not preserve multiplication is not a group representation.
- An injective group homomorphism without a checked isomorphism-to-range bridge does not by itself
  match the literal isomorphism wording.
- The conjugation action is generally nonfaithful because its kernel is the center; it cannot replace
  the regular action without extra hypotheses.
- A right-regular antihomomorphism, an action of `Gᵐᵒᵖ`, or an inversion-adjusted map requires a
  checked directional transport.
- Lagrange's theorem, the regular representation into linear automorphisms, or a result only for a
  particular named group is related but not this target.
- The catalog's `已验证` label, a successful `#check`, or an upstream theorem name is not accepted
  source or proof evidence.

No canonical Lean expression, statement fingerprint, alternate encoding, obligation registry, or
proof state is frozen by this intake.
