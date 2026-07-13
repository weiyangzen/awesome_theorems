# THM-M-1448 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10574-10579` names `QR分解`, attributes it to Alston Householder
in 1958, and states `矩阵的正交三角分解`: an orthogonal-triangular factorization of a matrix. All
six uncited lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They provide no
bibliography, formula, dimensions, scalar field, definitions, hypotheses, proof, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:39379-39404` repeats the gloss while explicitly leaving the target
system, exact definitions and premises, proof route, dependencies, alternate statements, axiom
use, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets this target to `L0 / rework_required`.

The corpus separately lists `THM-M-0046` as `QR分解定理` with the more explicit gloss `矩阵可分解为
正交矩阵与上三角矩阵之积`. It has the same attribution, year, importance, and untrusted status.
This is a probable duplicate, not accepted identity: its dossier and any future status grant no
source or proof credit to `THM-M-1448`.

## Inspected modern source lead

Sheldon Axler, *Linear Algebra Done Right*, fourth edition, Section 7D, Theorem 7.58, printed page
264, author-hosted PDF observed on 2026-07-13, states the following for scalar field `F = R` or `C`:
if `A` is square with linearly independent columns, then unique matrices `Q` and `R` exist such that
`Q` is unitary, `R` is upper triangular with positive diagonal entries, and `A = Q R`. The proof
applies Gram-Schmidt to the columns, makes `Q` from the resulting orthonormal basis, defines `R`
from inner products, checks triangularity and the product columnwise, and proves positivity and
uniqueness.

The observed PDF SHA-256 is
`45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`. It is an author-hosted,
mutable lead and was not added to the repository. The catalog does not cite it; the word "matrix"
does not record Axler's square and independent-column hypotheses; the complex case says unitary
rather than literally orthogonal; and no correction audit, lawful immutable preservation,
historical-attribution review, or independent review is recorded. It supports provisional `H1`,
not `H0`.

A. S. Householder, "Unitary Triangularization of a Nonsymmetric Matrix," *Journal of the ACM* 5(4)
(1958), pages 339-342, DOI `10.1145/320941.320947`, is recorded only as a historical locator. Its
text, exact theorem, assumptions, proof, corrections, and relationship to modern QR terminology
were not inspected and receive no source credit.

## Clause crosswalk

| Catalog component | Axler 7.58 component | Prospective Lean surface | Intake status |
|---|---|---|---|
| "matrix" | square matrix over `R` or `C` with linearly independent columns | `Matrix (Fin n) (Fin n) k` plus linear independence of columns | field, shape, order, and rank scope not source-ratified |
| "orthogonal" | unitary square `Q`; over `R` this is orthogonal | `Matrix.unitaryGroup`, `Matrix.mem_unitaryGroup_iff`, or an orthonormal-basis matrix | real/complex terminology and orientation open |
| "triangular" | square `R`, zero below the diagonal, positive diagonal | `Matrix.BlockTriangular R id` plus a diagonal predicate | order, orientation, and normalization open |
| "decomposition" | exact equality `A = Q R` | matrix multiplication and equality | factor shapes open outside the square reading |
| existence | unique normalized factors | nested existentials plus optional uniqueness | catalog does not say uniqueness or normalization |
| Householder / 1958 | catalog attribution and uninspected historical locator | no formal component | primary historical-source audit open |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H/M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho` defines Gram-Schmidt orthogonalization and
normalization and proves orthogonality, span preservation, linear independence, basis construction,
and triangular coefficient results. The close matrix-facing declaration
`InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular` says the input family's
coefficient matrix in the constructed orthonormal basis is block upper triangular.

`Mathlib.LinearAlgebra.UnitaryGroup` defines unitary and orthogonal matrix groups and membership
equations. `Matrix.BlockTriangular` supplies the pinned upper-triangular predicate. These are
promising ingredients, not a source-crosswalked terminal statement with QR witnesses and the exact
matrix equality.

A bounded exact-topic search of repo-local Lean and pinned mathlib found no declaration named or
documented as QR decomposition or QR factorization. This is intake discovery only, not an exhaustive
anchor audit or a global absence proof. `IntakeProbe.lean` checks selected APIs and representative
axiom reports without defining a target.

## First source gate

Before source status can advance to `H0`, reviewers must preserve an immutable lawful edition,
select the exact proposition, map every binder, hypothesis, conclusion, incorporated definition,
and proof node, reconcile the catalog's field/shape/rank ambiguity and the `THM-M-0046` duplicate,
audit corrections and historical attribution, and approve the mapping independently. Before
machine status can advance, the statement phase must elaborate that exact proposition and checked
transports under pinned imports; later phases must audit or implement terminal proof bodies.
