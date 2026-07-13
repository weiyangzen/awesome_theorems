# Scope map

## Preserved catalog boundary

The repository fixes target `THM-M-0051`, the Chinese title `格拉斯曼恒等式`, Hermann Grassmann,
the year 1844, and only the gloss `关于外代数的恒等式` ("an identity about exterior algebra").
That is not a binder-complete mathematical statement. Intake preserves the named exterior-algebra
identity family but does not choose a particular formula.

A later statement phase may freeze a root only after an immutable source passage is admitted and
independently reviewed. Historical attribution, a modern exterior-algebra convention, or the
availability of a convenient mathlib declaration cannot fill the missing formula.

## Proposition-changing decisions

The exact-source statement phase must freeze all of the following:

1. The identity meant by the singular catalog title: generator square-zero, generator
   anticommutation, a multi-wedge permutation/sign identity, a Grassmann-Pluecker relation, a
   universal-property identity, or another explicitly sourced formula.
2. Whether `exterior algebra` means a quotient algebra, alternating algebra, graded algebra,
   exterior powers, decomposable multivectors, Grassmann coordinates, or an older historical
   calculus requiring a checked modern translation.
3. The coefficient domain and its hypotheses, including commutativity, characteristic two,
   nontriviality, fields versus semirings, and whether signs or division by two are used.
4. The module or vector-space domain, universe levels, finite-dimensional or free hypotheses,
   basis and orientation data, and any rank or degree restrictions.
5. Every ordered binder, hypothesis, conclusion, equality carrier, coercion, grading convention,
   wedge or multiplication notation, permutation action, and sign convention.
6. Whether the result concerns only degree-one generators or arbitrary homogeneous elements, and
   the exact parity exponents for a graded-commutativity formulation.
7. Whether Pluecker or Grassmann coordinate relations, if intended, include decomposability,
   nonzero, dimension, index-ordering, and projective-scaling conditions.
8. The foundation, classical-choice, quotient, computation, and trusted-computing-base profiles,
   plus checked transports for every credited alternate encoding.

These choices are not stylistic. They change the proposition, its domains, or its proof boundary.

## Boundary cases

- The zero module, zero vector, degree zero, degree one, empty alternating family, and repeated
  vectors.
- The zero ring, nontrivial rings, characteristic two, and rings in which `2` is or is not
  invertible.
- Equal generators, swapped generators, odd/even homogeneous degrees, and permutations with
  repeated inputs.
- Exterior powers above module rank and finite versus infinite-dimensional modules.
- Zero or decomposable multivectors, zero Pluecker coordinates, and index tuples with repetitions
  if a coordinate relation is eventually selected.

No boundary case is excluded at intake. The source-selected statement must resolve each one.

## Explicit non-substitutions

- `ExteriorAlgebra.ι_sq_zero`, `ExteriorAlgebra.ι_add_mul_swap`,
  `ExteriorAlgebra.ιMulti_mul_ιMulti`, or any other pinned declaration selected solely because its
  subject is exterior algebra.
- The definition or universal property of exterior algebra used as a theorem without evidence that
  the catalog intended it.
- A Grassmann-Pluecker relation, decomposability criterion, or determinant identity chosen without
  an exact source map.
- The subspace dimension formula, often called Grassmann's formula, or the three-dimensional vector
  triple-product identity, also called a Grassmann identity in some sources; neither is licensed by
  the catalog's exterior-algebra gloss.
- A special case over real or complex vector spaces, a fixed degree or dimension, a basis
  computation, or an assumption that already contains the requested equality.
- Geometric algebra, Clifford algebra with a nonzero quadratic form, Berezin/Grassmann-variable
  integration, or physics identities without a checked source relationship.
- A theorem name, keyword match, numerical example, `#check`, or the untrusted `verified` label as
  source or proof evidence.

## Statement-gate retry condition

Admit a lawful immutable copy or independently reviewed transcription of the exact historical or
approved authoritative formula, incorporated definitions, hypotheses, proof boundary, translation,
corrections, and errata. Then freeze the domain, binders, sign and grading conventions, and every
boundary case; elaborate the exact Lean target with minimal pinned imports; serialize expression
and environment fingerprints; check every claimed transport; and run the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.
