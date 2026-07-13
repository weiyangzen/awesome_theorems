# Scope map

## Received claim

The repository supplies the name "Schur's lemma" and the gloss "a homomorphism between
irreducible representations is either zero or an isomorphism." This identifies the classical
zero-or-isomorphism family, but it is not yet a fully bound mathematical proposition.

## Candidate representation boundary

A common reading contains all of the following, each of which still needs a pinpoint source and a
checked formal choice:

- one acting group `G` and one scalar field `k`;
- two representations `rho : G -> GL(V)` and `sigma : G -> GL(W)` over `k`;
- irreducibility of both representations, including nontriviality and invariant-subspace
  conventions;
- an intertwining `k`-linear map `f : V -> W`;
- a dichotomy: `f = 0`, or `f` is an equivariant linear isomorphism.

Pinned mathlib's direct theorem is more general in one direction: it assumes only `Monoid G`, uses
`Representation k G V`, defines irreducibility via the simple order of subrepresentations, and
concludes `Function.Bijective f ∨ f = 0` for `f : IntertwiningMap rho sigma`. Its
`IntertwiningMap.ofBijective` constructor packages the first branch as a representation
equivalence. A group specialization and that packaging are plausible checked transports, but the
catalog has not selected them.

## Decisions required at statement freeze

1. Identify and independently review the intended source edition, theorem/page, incorporated
   definitions, assumptions, proof boundary, translation, and errata.
2. Fix whether the acting object is a group, finite group, monoid, associative algebra, group
   algebra, or an object in a representation category.
3. Fix the scalar field or division ring, and decide whether any algebraic-closure or characteristic
   condition belongs to this exact form.
4. Fix finite-dimensionality. It is unnecessary for mathlib's zero-or-bijective result, but it is
   often part of surrounding textbook conventions.
5. Fix irreducibility, including exclusion of the zero representation and the exact invariant-
   subspace or simple-module bridge.
6. Fix the homomorphism type and the meaning of isomorphism: underlying bijectivity, a linear
   equivalence with intertwining inverse, or a categorical `IsIso` witness.
7. Fix binder order, disjunction orientation, universe levels, and boundary behavior for trivial
   groups, equal representations, zero maps, and any zero carriers allowed by the definitions.

## Related but nonidentical forms

- `LinearMap.bijective_or_eq_zero` is the simple-module form and forgets the received
  representation language unless the group-algebra equivalence is checked.
- `CategoryTheory.isIso_iff_nonzero` is a categorical generalization for simple objects in a
  preadditive category with kernels.
- The statement that an endomorphism of a finite-dimensional irreducible representation over an
  algebraically closed field is scalar is stronger and adds material assumptions.
- A formula for the dimension of a Hom-space is a consequence or refinement, not the received
  dichotomy itself.

## Explicit exclusions

- Injective-only or surjective-only claims.
- Endomorphisms of a single representation as a substitute for morphisms between possibly
  distinct representations.
- The algebraically-closed scalar-endomorphism version substituted for zero-or-isomorphism.
- A finite-group or characteristic-specific special case silently used as the unrestricted root.
- The monoid, module, or categorical generalization treated as identical without a checked source
  and formal transport.
- A premise or bundled structure that already assumes the desired isomorphism.
- The catalog's `已验证` label, a matching theorem name, or a successful API probe as proof credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion encoding, alternate
transport, or degenerate-case exclusion is frozen during intake.
