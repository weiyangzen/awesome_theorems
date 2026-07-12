# THM-M-0047 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:356-361` supplies exactly the title `LU分解定理`, attribution to
Alan Turing, year 1948, gloss `矩阵可分解为下三角与上三角矩阵之积` ("a matrix can be decomposed as
the product of a lower-triangular and an upper-triangular matrix"), high importance, and status
`已验证`. Git blame attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no bibliography, theorem locator,
domain, quantifiers, hypotheses, pivot convention, normalization, proof, correction history, or
formal artifact.

`Docs/Stage0_Blueprint.md:1402-1427` repeats the gloss while explicitly leaving the exact definitions
and premises, formal system and foundations, proof route, dependency graph, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 target manifest retains `已验证` only
as untrusted metadata and resets the target to `L0 / rework_required`.

The repository also has `THM-M-1446` at `Docs/researches/math_theorems.md:10560-10565`, attributed
to Turing in 1948 with the shorter gloss `矩阵的三角分解`. It is a separate Stage1 target. Duplicate
proximity supplies no statement identity or shared proof credit.

## Primary-publication lead

On 2026-07-13, Crossref's DOI record was inspected for A. M. Turing, "Rounding-off Errors in
Matrix Processes," *The Quarterly Journal of Mechanics and Applied Mathematics*, volume 1, issue
1, 1948, pages 287-308, DOI `10.1093/qjmam/1.1.287`. This matches the catalog's author and year and
is a credible primary-source lead.

The publisher endpoint returned HTML, but a 25-page scanned offprint was then inspected through the
King's College, Cambridge Turing Digital Archive record `AMT/B/18`. The observed PDF SHA-256 was
`4762fc6d01628be3282d336e6fc080be6b34cc0d75d6e70542afa98b23e272d3`.

Section 3, "Triangular resolution of a matrix," journal page 289 (scan page 3), defines lower and
upper triangular matrices and their unit variants. It states: if the principal minors of `A` are
nonsingular, there are unique unit lower-triangular `L`, nonsingular diagonal `D`, and unit upper-
triangular `U` such that `A = L D U`; it also gives the reversed `A = U' D' L'` form. The proof by
recursive coefficient equations/induction continues through page 290. Section 4 obtains
`L^-1 A = D U`, so `A = L (D U)` with `D U` upper triangular, and separately discusses row/column
permutations and pivoting on pages 290-291.

This is a strong primary proof lead and explains the catalog's lower-times-upper wording after
folding `D` into `U`. It does not justify deleting the principal-minor hypothesis. Exact source
terminology (including whether "principal" means successive leading minors), scalar/domain
conventions, LDU-to-LU transport, correction/errata audit, and independent review remain open. The
source status is therefore `H1`, not `H0`.

The archive landing describes the offprint as QJMAM volume I, part 3, September 1948, whereas
Crossref reports issue 1; that metadata conflict remains to be reconciled. The archive and DOI
records cited no errata, but no independent correction search was completed. The source theorem's
reverse `U' D' L'` clause and the zero-dimensional convention also need explicit inclusion or
exclusion decisions.

## Inspected modern source lead

Robert van de Geijn and Margaret Myers, *Advanced Linear Algebra: Foundations to Frontiers*, online
Section 5.2.3, was inspected on 2026-07-13. Definition 5.2.3.1 defines, for
`A in C^(m x n)` with `m >= n`, a factorization `A = L U` where `L` is unit lower trapezoidal and
`U` is square upper triangular with nonzero diagonal. Definition 5.2.3.2 defines principal leading
submatrices. Theorem 5.2.3.4 states and proves that a matrix with linearly independent columns has a
unique LU factorization exactly when all principal leading submatrices are nonsingular. Section
5.3.3 separately defines partial pivoting through `P(p) A = L U`.

The inspected Section 5.2.3 HTML had observed SHA-256
`15fc81a54356635a5311a50c0373d1c3e9ad5b384b7d2770906aba2f52bff9b3`. It is a current mutable web
source and the repository does not cite it. It demonstrates two materially different correct
statement families, but it neither identifies the catalog's intended correction nor supplies H0.

## Clause crosswalk

| Catalog component | Candidate mathematical reading | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "matrix" | finite square matrix, possibly with field and pivot hypotheses | `Matrix (Fin n) (Fin n) K` or ordered finite indices | scalar, shape, index, and hypotheses absent |
| "lower triangular" | entries above the diagonal vanish | `Matrix.BlockTriangular OrderDual.toDual` | pinned predicate exists; normalization open |
| "upper triangular" | entries below the diagonal vanish | `Matrix.BlockTriangular id` | pinned predicate exists; normalization open |
| "product" | literal `A = L * U` | matrix multiplication | universal reading refuted by the checked swap matrix |
| possible repair | a permutation and triangular factors | `P * A = L * U`, `A = P * L * U`, or another equation | proposition-changing and absent from catalog |
| possible restriction | unpivoted LU under nonzero-pivot/leading-minor conditions | determinant/minor hypotheses plus existential factors | proposition-changing and absent from catalog |
| modern unpivoted lead | ALAFF Theorem 5.2.3.4 with full column rank and nonsingular principal leading submatrices | unit lower trapezoidal and upper-triangular factor witnesses | inspected H1 lead; not catalog-selected |
| Turing / 1948 | DOI and archive identify the inspected paper | no Lean component | issue/part metadata conflict and correction audit open |
| Turing Section 3 | `A = L D U` under nonsingular principal-minor hypotheses | lower predicate, diagonal, upper predicate, and checked reassociation | primary proof inspected; exact assumptions/transport and review open |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H or M credit |

## Checked falsity boundary

`IntakeProbe.lean` proves that the rational swap matrix `[[0,1],[1,0]]` is not the product of a
lower-triangular and upper-triangular matrix under the pinned mathlib predicates. This is evidence
against the unqualified universal reading, not a replacement theorem and not proof of any corrected
LU statement. Consequently the catalog wording is not itself a stable true proposition, while the
provisional source debt is `H1`: Turing's complete qualified proof is located, but exact correction,
assumption mapping, transport, errata audit, and independent review remain open.

## Pinned Lean boundary

Pinned mathlib contains the triangular predicates, their multiplication and determinant lemmas,
explicit `2 x 2` matrix multiplication, and pivot/transvection reduction. The pivot theorem
`Matrix.Pivot.exists_list_transvec_mul_diagonal_mul_list_transvec` is a related Gaussian-reduction
factorization, not an LU/PLU root. A bounded `rg` search of repo-local Lean and pinned mathlib found
no obvious LU, PLU, or LUP terminal declaration. No corrected canonical target is frozen or
credited at intake.

## Source gate

The statement phase must preserve and independently review an immutable source edition, locate the
exact theorem and proof, audit corrections, decide whether the catalog is corrected, redirected,
or rejected, and map every domain, binder, hypothesis, pivot/permutation convention,
normalization, conclusion, and boundary case. Only then may it freeze a minimal-import Lean target,
checked transports, expression/environment fingerprints, and statement mutations. Until that
gate passes, ordinary proof execution is blocked.
