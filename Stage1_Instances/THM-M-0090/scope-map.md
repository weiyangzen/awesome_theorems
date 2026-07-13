# Scope map

## Frozen catalog boundary

- Target ID: `THM-M-0090`; execution rank: `1107`; baseline: `L0 / rework_required`.
- Catalog title: `外尔特征标公式` (Weyl character formula).
- Catalog attribution and date: Hermann Weyl, 1925.
- Literal catalog statement: `李群表示的特征标公式` (a character formula for Lie-group
  representations).
- The manifest value `已验证` is untrusted metadata and supplies no source or proof credit.

These facts are frozen as provenance, not as a binder-complete mathematical proposition.

## Standard candidate reading, not yet selected

The inspected modern source lead formulates the theorem using a complex semisimple Lie algebra
`g`, its weight lattice `P`, positive roots, Weyl group `W`, Weyl vector `rho`, and the irreducible
finite-dimensional module `L_lambda` for a dominant integral weight `lambda`. It gives the
character as the alternating Weyl sum at `lambda + rho` divided by the Weyl denominator. This is a
strong disambiguation lead, but it is not the catalog's cited source and has no accepted Lean
transport.

An exact statement must still choose at least:

- a compact connected Lie group, complex semisimple Lie algebra, or algebraic-group domain;
- the relation between group representations and Lie-algebra modules, including integrability and
  any connectedness or simply connectedness requirement;
- finite-dimensionality, irreducibility, coefficient field, highest weight, dominance, and
  integrality hypotheses;
- a maximal torus or Cartan subalgebra, positive-root system, weight lattice, Weyl group, sign, and
  normalization of `rho`;
- formal characters in a group algebra or completion versus pointwise characters on a torus;
- whether division is an algebraic divisibility assertion or evaluation only where the denominator
  is nonzero, plus extension to singular elements;
- the exact numerator and denominator conventions and all ordered binders.

No item in that list is frozen by the catalog gloss alone.

## Boundary cases to resolve

- rank-zero or trivial group/Lie-algebra and the zero highest weight;
- empty positive-root family and the resulting denominator convention;
- reducible or nonsemisimple groups and Lie algebras;
- non-dominant or non-integral weights and representations that do not integrate;
- singular torus elements where a pointwise quotient denominator vanishes;
- reducible, infinite-dimensional, or non-highest-weight representations;
- simply connected covers, central quotients, and which highest weights descend;
- formal equality versus analytic equality and equality on the full group versus a maximal torus.

No case is excluded before an exact proposition is selected.

## Explicit non-substitutions

- the Weyl dimension formula (`THM-M-0091`) or the denominator identity alone;
- Peter-Weyl completeness (`THM-M-0089`) or the highest-weight classification
  (`THM-M-0093`);
- Weyl-Kac, Kac-Peterson, Kazhdan-Lusztig, or special affine character formulas;
- finite-group character orthogonality or basic trace-character identities;
- the root-system or Weyl-group API by itself;
- `LieAlgebra.LieCharacter`, which is a Lie homomorphism to scalars rather than the trace/formal
  character of a representation;
- only `sl2`, only one fixed type/rank, the trivial representation, or another special case;
- a structure or hypothesis that stores the desired formula followed by an accessor proof;
- the catalog's untrusted verified label or the intake API probe as proof credit.

## Downstream freeze condition

The statement phase must approve an immutable source proposition, map every referenced definition
and assumption, audit corrections, obtain independent source review, choose an exact encoding, and
elaborate it under minimal pinned imports. Only then may it fill the null binders, hypotheses,
conclusion, expression hash, environment fingerprint, checked alternate encodings, and mutation
tests in the planned instance.
