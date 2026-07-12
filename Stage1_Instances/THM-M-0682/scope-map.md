# Scope map

## Repository claim

The complete repository record is the title `微分伽罗瓦理论`, Ellis Kolchin, 1973, and the gloss
`微分方程的伽罗瓦理论` ("the Galois theory of differential equations"). This identifies a field
of mathematics, not a proposition: it supplies no differential equation, base differential field,
constant-field hypothesis, extension, group, quantifier order, or conclusion. Intake freezes that
ambiguity rather than inventing a convenient theorem.

## Candidate theorem families

- Picard-Vessiot existence and uniqueness for a linear differential equation or differential
  module, commonly under characteristic-zero and algebraically closed constants hypotheses.
- The fundamental correspondence between suitable intermediate differential fields of a
  Picard-Vessiot extension and closed subgroups of its differential Galois group.
- Fixed-field conclusions identifying elements fixed by all differential automorphisms.
- Criteria relating solvability of a linear differential equation in Liouvillian extensions to a
  solvability property of the differential Galois group.

These families have different data, assumptions, and conclusions. They are discovery choices, not
accepted alternate encodings.

## Decisions required before statement freeze

- Inspect and pin a primary edition, exact theorem/page, wording, definitions, and errata status.
- Choose ordinary differential fields versus several commuting derivations, and fix characteristic.
- Fix the equation encoding: scalar linear ODE, matrix system, differential operator, or
  differential module.
- Fix the constants hypothesis and whether the conclusion is existence, uniqueness up to
  differential isomorphism, a correspondence, fixed-field equality, or Liouvillian solvability.
- Specify the Picard-Vessiot extension definition, including generation by a fundamental solution
  matrix, determinant inverse, and the no-new-constants condition where applicable.
- Specify the differential Galois group and the topology/algebraic-group notion of closed subgroup,
  all binder orders, universes, classical principles, and boundary cases.

## Explicit exclusions

- Ordinary finite-dimensional Galois theory with no compatible derivation.
- The existence or uniqueness of an extension of a derivation to a finite algebraic field extension.
- Liouville's theorem on elementary antiderivatives or mathlib's `IsLiouville` extension predicate
  as a substitute for a selected differential-Galois theorem.
- Differential closed fields, model-theoretic quantifier elimination, or differential algebra in
  general as substitute roots.
- A structure that assumes the desired correspondence or fixed-field conclusion as a field.
- The untrusted repository label `已验证`, a text-search hit, or an elaborating nearby declaration
  as source or proof acceptance.

## Degenerate cases

The statement phase must explicitly test the identity extension, zero-dimensional system, trivial
differential Galois group, and equations already split over the base. It must decide rather than
silently exclude non-algebraically-closed constants, positive characteristic, nontrivial constants,
and partial differential fields. Until then, no narrower root is authorized.
