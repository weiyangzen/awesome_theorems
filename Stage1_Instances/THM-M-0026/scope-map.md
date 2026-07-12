# Scope map

## Preserved theorem family

The repository wording preserves the following family-level content:

- the coefficient ring is a polynomial ring over an algebraically closed field;
- the relevant ideals are maximal ideals;
- the geometric objects are points interpreted through simultaneous polynomial evaluation; and
- the intended relation is a correspondence between those maximal ideals and points.

A likely finite-variable formulation says that a maximal ideal is exactly the ideal of polynomials
vanishing at one affine point. This is a scope locator, not the canonical claim: the repository has
not supplied the quantifiers, definitions, or source passage needed to distinguish an existential
classification from an `Iff` or a genuine equivalence of bundled spaces.

## Decisions required at statement freeze

The dependent statement phase must select an immutable, independently reviewed source passage and
freeze all proposition-changing choices below.

1. The algebraically closed coefficient field and whether points take values in the same field or
   in a separately quantified algebraically closed extension.
2. A finite natural-number variable set, an arbitrary type with a `Finite` instance, or another
   finite-variable presentation, including the zero-variable case.
3. The precise polynomial representation and the ordered field, variable, ideal, and point binders.
4. Whether a point `x` denotes an element of affine space `sigma -> K`, a point of a selected
   algebraic set, or a maximal-spectrum point.
5. Whether the point ideal is the kernel of evaluation, the vanishing ideal of a singleton, or an
   explicitly generated ideal, and the checked transports among credited encodings.
6. Whether the conclusion is `I.IsMaximal -> exists x, I = I({x})`, an `Iff`, a bijection, or the
   strong identity `I(V(I)) = radical(I)`.
7. Whether equality is literal ideal equality or equality after a polynomial-ring equivalence.
8. The treatment of the top/bottom ideal, empty zero locus, empty variable type, zero ring
   conventions, and uniqueness of the point.
9. The exact foundation, choice, quotient, algebraic-closure, TCB, and computation profiles.

## Explicit exclusions

- The strong radical/zero-locus Nullstellensatz cannot silently replace the catalog's
  maximal-ideal/point correspondence, even though the statements are closely related.
- The weak maximal-ideal existence direction cannot silently replace an `Iff` or a bijection if the
  selected source requires the stronger correspondence.
- A theorem over an algebraically closed extension cannot be substituted for a same-field theorem
  without a checked relationship and an exact source map.
- Prime-spectrum identities valid for arbitrary rings are adjacent algebraic geometry, not by
  themselves the classical affine-point result.
- Alon's combinatorial Nullstellensatz is a distinct theorem and receives no target credit here.
- Hilbert's basis theorem, Zariski's lemma alone, a finite-field analogue, a one-variable special
  case, or a concrete example is not the requested theorem.
- A structure field, premise, or oracle that assumes the desired correspondence is not a proof.
- The catalog label `已验证`, a theorem name, or successful API elaboration is not source or kernel
  evidence for the canonical root.

No canonical Lean target, statement fingerprint, checked alternate encoding, mutation result,
obligation registry, discovery protocol, or proof status is frozen at intake.
