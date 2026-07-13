# Scope map

## Preserved theorem family

The intake preserves the literal catalog claim: every group is isomorphic to some permutation
group. In the standard modern reading, an arbitrary group `G` maps each `g` to the permutation
`x |-> g * x` of its underlying set. This left-regular representation is injective, so `G` is
isomorphic to its image, a subgroup of `Equiv.Perm G`.

The statement phase freezes that conventional repository scope as
`Stage1Instances.THM_M_0063.CayleyTheoremTarget`. It is not an H0 claim about an independently
reviewed historical passage.

## Decisions required at statement freeze

The following choices are now fixed by `Statement.lean`:

1. The carrier is `G : Type u`, universally quantified before the implicit `[Group G]` binder.
2. "Permutation group" is the range subgroup of `Equiv.Perm G`; a checked implication connects it
   to an existential subgroup formulation on the same carrier.
3. The regular-action orientation is left multiplication. The map `g |-> (x |-> g * x)` is a homomorphism under
   mathlib's permutation multiplication; right multiplication may require inversion or an
   opposite-group transport.
4. The conclusion is `Nonempty` of a `MulEquiv` to the regular image range, not merely an injective
   homomorphism. The reverse direction from the existential subgroup form is not credited.
5. The exact explicit expression fingerprint is
   `sha256:40929846f1d1d1ff4479e5be6a989358a65ecebec5a2646f6e2dab508c641a1a`.
6. The statement vocabulary uses the minimal tested pair `Mathlib.Algebra.Group.Action.End` and
   `Mathlib.Algebra.Group.Subgroup.Ker`; the proof-bearing anchor remains outside the import closure.
7. The checked transport reports `propext`, `Classical.choice`, and `Quot.sound`. Full transitive
   trust closure remains downstream.

Exact primary-source passage review, correction history, independent source review, anchor
provenance, and proof closure remain open.

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

The exact Lean expression, one directional alternate-encoding transport, mutation classes, and
environment fingerprint are frozen provisionally by the statement artifacts. No canonical
proof state, accepted receipt, or theorem-completion state is frozen. The separate
`obligation-registry.json` now freezes the provisional semantic denominator for the obligation-tree
phase; it changes no accepted state and grants no proof credit.
