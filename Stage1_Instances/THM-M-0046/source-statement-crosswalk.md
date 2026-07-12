# THM-M-0046 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:349-354` names `QR分解定理`, attributes it to Alston Householder in
1958, and states `矩阵可分解为正交矩阵与上三角矩阵之积`: a matrix can be decomposed as the product
of an orthogonal matrix and an upper-triangular matrix. All six uncited lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:1375-1401` repeats the gloss while leaving the target system, exact
definitions and premises, proof route, dependencies, alternate statements, axiom use, machine
status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted metadata
and resets this target to `L0 / rework_required`.

The corpus separately lists `THM-M-1448` as `QR分解` with the gloss `矩阵的正交三角分解`. It has the
same attribution, year, importance, and untrusted status. This is a probable duplicate, but no
identity or scope-sharing decision is accepted; it grants no evidence to this target.

## Inspected modern source lead

Sheldon Axler, *Linear Algebra Done Right*, fourth edition, author-hosted PDF observed on 2026-07-13,
Section 7D, Theorem 7.58, printed page 264, states the following for scalar field `F = R` or `C`:
if `A` is square with linearly independent columns, then unique matrices `Q` and `R` exist such
that `Q` is unitary, `R` is upper triangular with positive diagonal entries, and `A = Q R`. The
proof applies the Gram-Schmidt procedure to the columns, makes `Q` from the resulting orthonormal
basis, defines `R` from inner products, checks triangularity and the product columnwise, and proves
positivity and uniqueness.

The observed PDF SHA-256 is
`45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`. It is an author-hosted,
mutable lead and was not added to the repository. The catalog does not cite it; the catalog's
unqualified word "matrix" does not record Axler's square and independent-column hypotheses; the
complex case says unitary rather than literally orthogonal; no correction audit, lawful immutable
preservation, historical-attribution review, or independent source review is recorded. Therefore
this is provisional `H1` evidence, not `H0`.

## Clause crosswalk

| Catalog component | Axler 7.58 component | Prospective Lean surface | Intake status |
|---|---|---|---|
| "matrix" | square matrix over `R` or `C` with linearly independent columns | `Matrix n n k` plus `LinearIndependent k` columns | field, index/order, shape, and whether rank is intended remain open |
| "orthogonal matrix" | unitary square `Q`; over `R` this is orthogonal | `Matrix.unitaryGroup n k`, `Matrix.mem_unitaryGroup_iff`, or an orthonormal-basis matrix | real/complex terminology and orientation open |
| "upper triangular matrix" | square `R`, zero below diagonal, positive diagonal | `Matrix.BlockTriangular id` plus diagonal predicate | ordered indices and positivity encoding open |
| "product" | exact equality `A = Q R` | matrix multiplication and equality | factor shapes and equality direction open outside square form |
| existence | unique normalized factors | nested existentials plus optional uniqueness | catalog does not say uniqueness or normalization |
| Householder / 1958 | catalog attribution only | no formal component | primary historical-source audit open |
| `已验证` | untrusted label | source and kernel receipts would be required | no H/M credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho` defines Gram-Schmidt orthogonalization and
normalization and proves orthogonality, span preservation, linear independence, basis construction,
and triangular coefficient results. The close matrix-facing declaration
`InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular` says that the input family's
coefficient matrix in the constructed orthonormal basis is block upper triangular.

`Mathlib.LinearAlgebra.UnitaryGroup` defines the unitary and orthogonal matrix groups and relevant
membership equations. `Matrix.BlockTriangular` provides the pinned upper-triangular predicate.
These are promising ingredients, not a source-crosswalked terminal statement with QR witnesses and
the exact matrix equality.

A bounded exact-topic search of repo-local Lean and pinned mathlib found no declaration named or
documented as QR decomposition or QR factorization. This is intake discovery only, not an exhaustive
anchor audit or a global absence proof. `IntakeProbe.lean` checks selected APIs and representative
axiom reports without defining a target.

## Source gate

Before source status can advance to `H0`, reviewers must preserve an immutable lawful edition,
select the exact source proposition, map every binder, hypothesis, conclusion and incorporated
definition, reconcile the catalog's field/shape/rank ambiguity, audit corrections and historical
attribution, and approve the mapping independently. Before machine status can advance, the
statement phase must elaborate that exact proposition and checked transports under pinned imports;
the later anchor and proof phases must then audit or implement actual terminal proof bodies.
