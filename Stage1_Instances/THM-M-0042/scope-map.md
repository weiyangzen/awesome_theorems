# Scope map

## Preserved theorem family

The intake preserves exactly the finite complex-matrix Jordan canonical-form family named by the
catalog: a square complex matrix admits a change of basis to a block diagonal matrix whose blocks
have one eigenvalue on the diagonal, ones immediately above the diagonal, and zeros elsewhere. This
sentence is a scope description, not the frozen canonical proposition.

Axler's inspected operator formulation says that every linear operator on a finite-dimensional
complex vector space has a Jordan basis. A future statement phase may select that formulation, a
square-matrix similarity formulation, or a checked equivalent encoding only after the source and
transport boundaries below are approved.

## Decisions required at statement freeze

An exact source-reviewed statement must decide all of the following:

1. Whether the root quantifies over `n x n` matrices indexed by `Fin n`, arbitrary finite index
   types, or operators on an arbitrary finite-dimensional complex vector space.
2. The definition of a Jordan block, including block size, scalar eigenvalue, the superdiagonal
   orientation, and the `1 x 1` convention.
3. The representation of a block family and block diagonal assembly, including whether blocks are
   ordered and whether zero blocks or an empty family are permitted.
4. The definition of Jordan normal form and whether it contains only the block-shape condition or
   also a canonical ordering of eigenvalues and block sizes.
5. The definition and orientation of similarity: `P⁻¹ A P = J`, `A = P J P⁻¹`, change-of-basis
   matrices, or equality of matrix representations under two bases.
6. How invertibility is expressed: a unit matrix, nonzero determinant, a linear equivalence, or a
   source-faithful equivalent predicate.
7. Whether existence alone is asserted or uniqueness of block data up to permutation is included.
8. The exact ordered binders, all typeclass and finiteness hypotheses, conclusion, universe levels,
   foundation profile, and every alternate encoding with a checked transport.

These choices alter the proposition or its proof boundary. The intake does not choose among them.

## Degenerate and boundary cases

Source review must explicitly address `n = 0`; `n = 1`; the zero matrix; scalar and diagonal
matrices; matrices with one eigenvalue; nilpotent matrices; repeated eigenvalues; defective
matrices; multiple blocks of equal size and eigenvalue; an empty block family; zero-sized blocks;
and permutations of otherwise identical block decompositions. The statement phase must also decide
whether a canonical ordering is mathematical data, an existential witness, or excluded from the
claim.

## Excluded substitutions

- Triangularizability or Schur triangularization is weaker than Jordan canonical form.
- A decomposition into generalized eigenspaces does not by itself construct Jordan chains or a
  Jordan-block basis.
- The Jordan-Chevalley-Dunford decomposition into commuting nilpotent and semisimple parts is a
  different theorem and cannot replace a Jordan normal-form statement.
- The spectral theorem, diagonalizability, rational canonical form, Frobenius normal form,
  characteristic-polynomial factorization, Cayley-Hamilton theorem, singular-value decomposition,
  and numerical eigendecomposition are distinct results.
- A result only for nilpotent, diagonalizable, normal, low-dimensional, or otherwise specialized
  matrices is not the requested universal complex-matrix theorem.
- A structure that stores the desired Jordan matrix, block decomposition, basis, or similarity
  equation as an input field supplies no proof.
- A numeric algorithm, floating-point example, theorem name, `#check`, or the catalog's untrusted
  `已验证` label supplies no H or M credit.

## Neighbor boundaries

`THM-M-0041` owns Cayley-Hamilton, `THM-M-0043` the spectral theorem, `THM-M-0044` singular-value
decomposition, and `THM-M-0045` Schur decomposition. Their future definitions, artifacts, and
proofs remain separate. They may become explicit dependencies only after exact statement and
obligation freezes; none grants status to this target by proximity.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks generalized-eigenspace,
matrix-unit, change-of-basis, matrix-representation, block-matrix, and Jordan-Chevalley interfaces.
The bounded exact-topic search found no Jordan block, basis, or canonical-form declaration. This is
scoped discovery evidence, not an exhaustive anchor audit or a proof of global absence.
