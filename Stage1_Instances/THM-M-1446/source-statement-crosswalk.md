# THM-M-1446 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10560-10565` supplies exactly the title `LU分解`, attribution Alan
Turing, year 1948, gloss `矩阵的三角分解` ("triangular decomposition of a matrix"), high importance,
and status `已验证`. Git blame attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, domain, quantifiers,
hypotheses, triangular or pivot convention, normalization, conclusion, proof, correction history,
or formal artifact.

`Docs/Stage0_Blueprint.md:39325-39350` repeats the gloss while leaving the exact premises, formal
system, proof path, dependencies, equivalent statements, axioms, machine status, and artifact links
open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

The repository also has `THM-M-0047` at `Docs/researches/math_theorems.md:356-361`, with the fuller
gloss "a matrix can be decomposed as the product of lower- and upper-triangular matrices." Its
dossier is a discovery lead, not an identity decision or a source/proof receipt for this target.

## Primary-publication lead

Crossref's DOI record for A. M. Turing, "Rounding-off Errors in Matrix Processes," *The Quarterly
Journal of Mechanics and Applied Mathematics* 1(1), 1948, pages 287-308, DOI
`10.1093/qjmam/1.1.287`, was inspected on 2026-07-13. It matches the catalog author and year.

The 25-page King's College, Cambridge Turing Digital Archive scan `AMT/B/18` was independently
downloaded and visually inspected for this target. Its observed SHA-256 was
`4762fc6d01628be3282d336e6fc080be6b34cc0d75d6e70542afa98b23e272d3`. Section 3, "Triangular
resolution of a matrix," journal page 289 (scan page 3), states that if the principal minors of
`A` are nonsingular, unique unit lower-triangular `L`, nonsingular diagonal `D`, and unit upper-
triangular `U` exist with `A = L D U`; it also states the reversed `A = U' D' L'` result. The proof
continues on journal page 290 and uses the product of the first diagonal entries to establish the
next one is nonzero. Page 288 places `A` in the context of a square matrix of order `n`.

Section 4 folds the diagonal factor into an upper factor through `L^-1 A = D U` and discusses row
and column interchanges. This explains the LU family, but does not authorize deletion of the
principal-minor hypothesis or selection of a pivot convention. The scan's scalar conventions,
exact meaning of "principal minors," LDU-to-LU transport, reverse clause, corrections, lawful
preservation, and independent source review remain open. The lead is therefore `H1`, not `H0`.

The archive offprint describes QJMAM volume I, part 3, September 1948, while Crossref reports issue
1. That metadata discrepancy and any correction history require reconciliation.

## Modern disambiguation lead

Van de Geijn and Myers, *Advanced Linear Algebra: Foundations to Frontiers*, online Section 5.2.3,
was inspected as a modern secondary lead. Definition 5.2.3.1 treats full-column-rank complex
`m x n` matrices with `m >= n`; Theorem 5.2.3.4 states unique LU exists exactly when all principal
leading submatrices are nonsingular. Section 5.3.3 separately uses `P A = L U` for partial pivoting.
These materially different valid variants demonstrate the missing catalog choice; they do not
select its root or establish `H0`.

## Clause crosswalk

| Catalog component | Candidate source/formal reading | Intake assessment |
|---|---|---|
| `矩阵` / matrix | finite square matrix, or modern rectangular variant | scalar, shape, indices, and hypotheses absent |
| triangular decomposition | lower, diagonal, and upper factors, or lower and upper factors | source and catalog do not state the same binder-complete clause |
| lower triangular | `Matrix.BlockTriangular OrderDual.toDual` | pinned predicate exists; unit normalization open |
| upper triangular | `Matrix.BlockTriangular id` | pinned predicate exists; unit normalization open |
| unpivoted product | `A = L * U` | unrestricted universal reading refuted by checked swap matrix |
| Turing Section 3 | unique `A = L * D * U` under nonsingular principal minors | inspected primary H1 lead; exact domain/transport/review open |
| Turing reverse clause | unique `A = U' * D' * L'` | source clause absent from catalog; inclusion open |
| possible pivot repair | `P * A = L * U`, `P * A * Q = L * U`, or another orientation | proposition-changing and absent from catalog |
| `已验证` | accepted source and kernel receipts would be required | untrusted metadata; no H or M credit |

## Checked falsity and formal boundary

`IntakeProbe.lean` proves over `Rat` that the swap matrix is not a lower-times-upper product under
the pinned triangular predicates. This refutes one unqualified universal reading; it neither
replaces the target nor proves a corrected LU theorem. A bounded search of repo-local Lean and
pinned mathlib found triangular and pivot infrastructure plus two specialized block LDU identities,
but no general exact LU/PLU/LUP/LDU terminal declaration. No formal candidate is credited.

## Source gate

The statement phase must preserve and independently review an immutable source edition, reconcile
the apparent duplicate, audit corrections, and decide whether the catalog is corrected, redirected,
merged, or rejected. It must map the scalar and matrix domains, ordered binders, every hypothesis,
principal-minor and pivot conventions, normalization, conclusion, reverse clause, uniqueness, and
boundary cases. Only then may it freeze an exact Lean expression, minimal imports, checked
transports, fingerprints, and statement mutations. Proof execution remains blocked until then.
