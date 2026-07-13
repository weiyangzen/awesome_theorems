# Scope map

## Received claim

The repository supplies the name "Maschke's theorem" and the gloss "a finite-group representation
is completely reducible when the characteristic does not divide the group order." This identifies
the classical theorem family, but it is not yet a fully bound mathematical proposition.

## Candidate representation boundary

A common reading contains all of the following, each of which still needs a pinpoint source and a
checked formal choice:

- a finite group `G`;
- a scalar field `k` whose characteristic does not divide the order of `G`;
- a `k`-linear representation `rho` of `G` on a vector space `V`;
- a complete-reducibility conclusion, expressed either by invariant complements or by a direct-sum
  decomposition into irreducible representations.

Pinned mathlib's direct formulation uses `[Group G] [Finite G]`, `[Field k]`,
`[NeZero (Nat.card G : k)]`, and `rho : Representation k G V`. Its conclusion
`Representation.IsSemisimpleRepresentation rho` abbreviates
`ComplementedLattice (Subrepresentation rho)`: every invariant subspace has an invariant
complement. It does not assume finite-dimensionality. The module documentation identifies its
nonzero-cardinality premise with the usual characteristic condition, but explicitly lists the
finite-dimensional direct-sum-of-irreducibles formulation as future work.

## Decisions required at statement freeze

1. Identify and independently review the intended source edition, theorem/page, incorporated
   definitions, assumptions, proof boundary, translation, and errata.
2. Fix the scalar domain: field, division ring, or a more general ring, and its nontriviality
   conventions.
3. Fix whether the representation space is required to be finite-dimensional.
4. Fix the finiteness encoding for `G` and the exact order used in the characteristic premise.
5. Fix whether `characteristic does not divide the group order` is encoded as nonzero natural-card
   coercion, invertibility, an explicit `ringChar` nondivisibility proposition, or a checked
   equivalent form.
6. Fix complete reducibility as complemented subrepresentations, a direct sum of irreducibles, a
   semisimple group-algebra module, or another source-defined convention, and provide checked
   transports for every credited alternate form.
7. Fix binder order, universe levels, and boundary behavior for the trivial group, the zero
   representation space, characteristic zero, positive characteristic, and infinite-dimensional
   spaces.

## Related but nonidentical forms

- Every `k[G]`-submodule has a complement is the module-theoretic form implemented by the direct
  mathlib candidate; a representation/module bridge is available but not yet credited to the root.
- A finite-dimensional representation is a direct sum of irreducibles is a familiar formulation,
  but pinned mathlib's Maschke module does not claim this form.
- Semisimplicity of the regular module or group algebra can imply statements for all modules, but it
  is not definitionally the catalog's representation wording.
- Characteristic-zero variants are special cases and do not cover the received positive-
  characteristic nondivisibility condition.

## Explicit exclusions

- Characteristic-zero-only, complex-only, or algebraically-closed-field specializations used as the
  complete theorem.
- A result for only the regular representation, only the group algebra, or one fixed representation
  substituted for the universal representation claim.
- Existence of a complement for one selected invariant subspace used instead of complete
  reducibility.
- Irreducibility, Schur's lemma, or character orthogonality substituted for semisimplicity.
- Direct-sum-of-irreducibles and complemented-subrepresentation formulations treated as identical
  without source fidelity and a checked transport.
- The characteristic premise removed, reversed, or replaced by a stronger special case.
- A premise or bundled structure that already assumes semisimplicity.
- The catalog's `已验证` label, a matching theorem name, or a successful API probe used as proof
  credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion encoding, alternate
transport, or degenerate-case exclusion is frozen during intake.
