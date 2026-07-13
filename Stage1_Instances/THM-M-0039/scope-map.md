# Scope map

## Received claim

The repository record provides the title `卡普兰斯基定理`, attribution Irving Kaplansky, year
1958, and gloss `关于PI环的结构` ("the structure of PI rings"). It supplies no citation, exact
proposition, definition chain, assumptions, quantifier order, boundary cases, or formal
declaration. The `已验证` field is explicitly untrusted under rev-5.6.

## Primary candidate not yet selected

The strongest inspected match is Theorem 1 of Kaplansky's 1948 paper *Rings with a polynomial
identity*:

> A primitive algebra satisfying a polynomial identity is finite-dimensional over its center.

The paper defines a polynomial identity for an algebra `A` over a field `F` as a nonzero element
of the free associative `F`-algebra in finitely many indeterminates that evaluates to zero for
every substitution from `A`. It states Theorem 1 first for primitive algebras and notes a ring
extension in section 4(c) under coefficient hypotheses.

This candidate is not frozen as the target. The catalogue's 1958 date conflicts with the 1948
publication, the gloss is broader than the theorem, and the same paper contains materially
different results. Source and scope reviewers must approve any correction and selection.

## Proposition-changing decisions

The statement phase must freeze all of the following from an immutable, reviewed source passage:

- Theorem 1 for algebras, the section 4(c) ring extension, or another precisely identified result.
- Associative and unital conventions, base field `F`, algebra structure, and the exact meaning of
  primitive: faithful simple left module, faithful simple right module, or an equivalent ideal
  formulation with a checked transport.
- The center as `Subring.center A`, its induced field structure, and the scalar action used by
  `Module.Finite (Subring.center A) A` or another exact finite-dimensionality conclusion.
- A finite variable type and a nonzero element of `FreeAlgebra F X`, its evaluation through
  `FreeAlgebra.lift`, and universal vanishing over substitutions `X -> A`; whether coefficients
  must lie in `F`, in the center, or be operator coefficients in the ring formulation.
- Whether the existence of one identity or a chosen identity is quantified first, and whether a
  constant/nonzero-scalar "identity" must be ruled out separately.
- Universes, all explicit and implicit typeclasses, ordered binders, characteristic assumptions,
  classical choice, and the exact conclusion carrier.

## Candidate result families not credited

Kaplansky's paper also proves or discusses:

1. a division algebra satisfying any polynomial identity is finite-dimensional over its center;
2. the free algebra has a complete set of finite-dimensional representations;
3. an algebraic algebra of bounded degree satisfies a polynomial identity;
4. a primitive algebraic algebra of bounded degree is finite-dimensional over its center; and
5. a nil algebra satisfying a polynomial identity is locally finite.

None can be substituted for Theorem 1 or aggregated into a vague "structure of PI rings" root.
The neighboring Amitsur-Levitzki target `THM-M-0040` concerns a specific matrix polynomial identity
and contributes no statement or proof credit here. Artin-Wedderburn (`THM-M-0036`) and Jacobson
density (`THM-M-0035`) are potential ingredients, not replacements for the PI implication.

## Boundary cases to resolve

- zero or subsingleton algebra, zero module, absence of a faithful simple module, and left/right
  primitive conventions;
- empty variable type, zero polynomial, constant polynomial, zero coefficient field, and a
  polynomial with variables not actually occurring;
- zero-dimensional algebra, commutative/field/division-ring special cases, and whether the center
  scalar structure is definitionally or only propositionally the selected base;
- finite-dimensional over the original coefficient field versus over the algebra's center;
- algebra identity versus the operator-coefficient ring extension and the injectivity condition on
  coefficients; and
- the exact role of choice used to select a maximal subfield in the primary proof.

## Pinned Lean boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides useful
interfaces in `Mathlib.Algebra.FreeAlgebra` and
`Mathlib.RingTheory.SimpleModule.WedderburnArtin`: `FreeAlgebra`, `FreeAlgebra.lift`,
`IsSimpleModule`, `FaithfulSMul`, `jacobson_density`, `IsSimpleRing.isField_center`,
`Module.Finite`, and `IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite`.

These are discovery-only ingredients. The bounded repository/mathlib search found no named
Kaplansky PI theorem, no general polynomial-identity predicate for noncommutative algebras, and no
bridge proving the candidate conclusion. The next phase must first settle the exact source
statement; only then may it define and mutation-test a canonical Lean target.
