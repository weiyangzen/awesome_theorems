# Scope map

## Preserved catalog boundary

The intake preserves the repository wording as a broad semisimple-Lie-theory family: classification
of semisimple Lie algebras together with a representation-theoretic result. This is not yet a
binder-complete theorem. In particular, intake does not replace the conjunction-like phrase by the
more convenient classification theorem or complete-reducibility theorem alone.

## Candidate readings without credit

1. **Algebra classification:** finite-dimensional complex semisimple Lie algebras are classified,
   up to isomorphism, by finite-type root systems or Dynkin diagrams; simple factors have classical
   types `A`, `B`, `C`, `D` or exceptional types `E6`, `E7`, `E8`, `F4`, `G2`.
2. **Weyl complete reducibility:** every finite-dimensional representation of a finite-dimensional
   semisimple Lie algebra over a characteristic-zero field is a direct sum of irreducibles.
3. **Highest-weight classification:** finite-dimensional irreducible representations of a complex
   semisimple Lie algebra are classified by dominant integral weights.
4. **Combined Cartan-Weyl program:** root decomposition and Dynkin classification of the algebra,
   followed by highest-weight classification of representations.

These readings differ in objects, binders, hypotheses, conclusions, and proof architecture. The
catalog does not choose among them or specify whether both classification and representation
clauses must be delivered by one root.

## Decisions required at statement freeze

1. Fix the exact named source, edition, theorem or section locator, incorporated definitions,
   correction history, proof boundary, and independent source review.
2. Decide whether the root concerns Lie algebras, connected Lie groups, compact groups, or a checked
   bridge between them.
3. Fix the scalar field and assumptions such as algebraic closure and characteristic zero, plus
   finite dimensionality and universe/typeclass conventions.
4. Define semisimplicity: direct sum of simple ideals, trivial radical, nondegenerate Killing form,
   or a source-selected equivalent form, with every transport direction checked.
5. Decide whether classification is of simple or semisimple algebras and whether it asserts
   existence, uniqueness, an equivalence of isomorphism classes, explicit classical/exceptional
   realizations, or only production of a root system.
6. Define the root datum or Dynkin-diagram carrier, crystallographic/reduced/finite conditions,
   connected components, type labels, and diagram isomorphism.
7. Fix the representation object, its dimension, morphisms and equivalence relation, and whether
   the conclusion is complete reducibility, irreducible highest-weight classification, character
   data, or another representation theorem.
8. Freeze ordered binders, all hypotheses, the exact conclusion, alternate encodings, foundation
   and TCB profiles, and the required logical relation between the classification and
   representation clauses.

## Degenerate and boundary cases

Source review must explicitly settle the zero Lie algebra; zero-dimensional representations; the
trivial representation; zero or positive rank; simple versus a product of simple ideals; repeated
simple factors; empty or disconnected Dynkin diagrams; real, complex, non-algebraically-closed, and
positive-characteristic fields; infinite-dimensional algebras or modules; reducible and
non-faithful representations; and whether isomorphic data with relabeled nodes count as equal.

## Excluded substitutions

- Root-space decomposition, Cartan-subalgebra existence, or construction of a root system alone.
- Merely defining the classical Lie algebras or the Cartan matrices `A` through `G2`.
- Trivial-radical equivalences or decomposition into simple ideals without the requested
  classification and representation conclusion.
- Lie's theorem for solvable Lie algebras, Engel's theorem, Ado's theorem, or the Peter-Weyl
  theorem for compact groups.
- Weyl complete reducibility alone unless an approved source shows that it is exactly the intended
  entire catalog claim.
- Highest-weight classification alone; that neighboring family is separately cataloged as
  `THM-M-0093`.
- Character and dimension formulas; those are separately cataloged as `THM-M-0090` and
  `THM-M-0091`.
- A fixed rank, one Dynkin type, one representation, or one special example.
- A structure, typeclass, hypothesis, axiom, or oracle that stores the desired classification or
  decomposition as input.
- The catalog's untrusted verified label or an API `#check` treated as source or proof credit.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks adjacent semisimple,
Cartan, root-system, classical-algebra, Cartan-matrix, and irreducibility APIs. This bounded probe is
not an exhaustive anchor audit and establishes neither classification nor representation closure.
