# Scope map

## Preserved method family

The intake preserves the exact-arithmetic Gaussian-elimination family named by the catalog: select
a pivot, apply elementary equation or row operations to eliminate variables recursively, and use
substitution or a parametric readout to interpret the resulting system. This is a scope description,
not a frozen theorem.

Grcar Section 1.2 describes the canonical schoolbook method as rearranging equations or variables,
using a leading equation to eliminate the leading variable below it, recursing, and finally
back-substituting. It separately describes the technical literature's triangular-factorization
view. An accepted statement must choose one exact correctness boundary rather than merging them.

## Proposition-changing decisions

An independently reviewed source correction must decide all of the following:

1. The coefficient domain: rationals, reals, a commutative field, a division ring, or another exact
   algebraic structure; finite-precision arithmetic is a separate target.
2. Square or rectangular matrices, ordered `Fin` indices or arbitrary finite types, and whether the
   system is homogeneous or has a right-hand side.
3. The elementary operations and their encoding: row swaps, nonzero scaling, row addition,
   augmented matrices, transvections, or an explicit algorithmic state.
4. The pivot-selection rule, treatment of zero pivots, column swaps, rank revelation, and whether
   partial or complete pivoting is part of the claim.
5. The output: upper triangular, row-echelon, reduced row-echelon, diagonal, LU/PLU factors, a
   tableau, a solution, an inconsistency certificate, or a parametrization of all solutions.
6. The conclusion: stepwise solution-set preservation, existence of a normal form, termination,
   executable solver correctness, uniqueness, operation count, numerical stability, or a specified
   conjunction.
7. The ordered binders, universes, hypotheses, exact equality orientation, checked alternate
   encodings, foundation/TCB profiles, and all boundary cases.

## Boundary cases

The statement phase must resolve empty, zero-row, zero-column, and `1 x 1` matrices; zero and
identity matrices; singular and invertible square systems; overdetermined, underdetermined,
consistent, and inconsistent systems; zero pivots; free variables; nonunique solutions; row or
column permutations; homogeneous systems; and exact versus floating-point arithmetic.

## Excluded substitutions

- Merely asserting that an invertible matrix has a unique solution does not say Gaussian
  elimination computes it.
- LU, PLU, LUP, QR, Cholesky, or transvection-diagonal-transvection factorization cannot silently
  replace the method target. `THM-M-1446` separately owns LU decomposition.
- Cramer's rule, matrix inversion, rank-nullity, or determinant nonvanishing is not Gaussian
  elimination.
- A homogeneous rational tableau implementation is not a general affine solver correctness
  theorem, and meta/oracle execution is not kernel proof evidence by itself.
- A structure or premise storing the desired normal form, solution, correctness certificate, or
  termination result supplies no proof.
- Numeric examples, residual experiments, benchmark results, theorem names, API checks, and the
  untrusted `已验证` label supply no source or proof credit.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, transvections have
checked row-addition semantics and finite square matrices over a field admit a two-sided reduction
to diagonal form. Pinned mathlib also has matrix-vector/invertible-system APIs and a meta Gaussian
tableau implementation for a homogeneous system. None is an end-to-end, source-selected theorem
about the catalog's unspecified direct method. The probe is bounded intake discovery, not the
downstream exhaustive anchor audit.
