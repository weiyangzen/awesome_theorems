# THM-M-0041 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:314-319` names the Cayley-Hamilton theorem, attributes it to
William Hamilton and Arthur Cayley in 1858, and states `矩阵满足其特征多项式`: a matrix satisfies
its characteristic polynomial. All six catalog lines originated at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:1237-1265` repeats the gloss while explicitly leaving the exact definitions
and premises, proof route, equivalent statements, axiom use, formal status, and artifact links open.
The rev-5.6 manifest retains `已验证` only as untrusted source metadata and resets the target to
`L0 / rework_required`.

## Human-source lead

Crossref resolves DOI `10.1098/rstl.1858.0002` to Arthur Cayley, *II. A memoir on the theory of
matrices*, *Philosophical Transactions of the Royal Society of London* 148, pages 17-37,
published 1858-12-31. Its metadata exposes an abstract that calls an unqualified matrix square and
states that any matrix satisfies an algebraic equation of its own order, obtained from the
determinant of the matrix minus the matrix treated as a scalar quantity times the identity.

This is a strong primary-publication lead and a useful wording cross-check, but not an accepted `H0`
packet. Intake did not preserve and hash an immutable edition, establish the exact theorem/proof page
and surrounding definitions, map the coefficient system and every premise, inspect errata or later
corrections, reconcile Hamilton's contribution with the located Cayley-only publication, map proof
nodes, or obtain independent source review.

## Component mapping

| Catalog component | Intake-selected meaning | Pinned Lean candidate | Status |
|---|---|---|---|
| "matrix" | arbitrary finite square matrix | `A : Matrix n n R`, with `[Fintype n] [DecidableEq n]` | exact Lean carrier and binders frozen; historical source mapping open |
| "its characteristic polynomial" | `det(X I - A)` over the same coefficient ring | local `characteristicPolynomial A` | expanded definition frozen; `Matrix.charpoly` transport downstream |
| "satisfies" | evaluation at `A` gives the zero matrix | `Polynomial.aeval A (characteristicPolynomial A) = 0` | exact canonical conclusion elaborated and fingerprinted |
| coefficient domain | commutative ring, with no nontriviality premise | `[CommRing R]` | exact Lean domain frozen; historical scope review open |
| Hamilton/Cayley / 1858 | catalog attribution and date | no formal component | historical attribution audit open |
| `已验证` | catalog status label | no formal component | explicitly no H/M credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean:203-222` documents and declares:

```text
Matrix.aeval_self_charpoly (A : Matrix n n R) : aeval A A.charpoly = 0
```

in a context with `[CommRing R] [Fintype n] [DecidableEq n]`. The module says that this is the
Cayley-Hamilton theorem and that it holds over any commutative ring. The pinned package's
`docs/undergrad.yaml:55-57` also maps "Cayley-Hamilton theorem" directly to this declaration.

`Mathlib/LinearAlgebra/Charpoly/Basic.lean:84-94` provides:

```text
LinearMap.aeval_self_charpoly (f : M ->ₗ[R] M) : aeval f f.charpoly = 0
```

for a finite free module over a commutative ring. That theorem reduces through a chosen basis to the
matrix theorem. It is a related alternate encoding, not silently the canonical root.

`Statement.lean` deliberately imports two lower vocabulary modules and expands `det(X I - A)` rather
than importing `Charpoly.Basic`. Its exact root expression and environment are now fingerprinted,
and Lean confirms `Matrix.charpoly` and `Matrix.aeval_self_charpoly` are unavailable in that module.
The intake candidates remain discovery evidence only: source identity, the checked `Matrix.charpoly`
transport, terminal proof provenance, transitive dependencies, and `M0` classification remain open.

## Exactness risks held open

The statement phase has confirmed the finite square-matrix reading, coefficient domain, empty-index
and zero-ring boundaries, `det(X I - A)` convention, scalar-coefficient embedding, and exact
noncommutative matrix-algebra evaluation expression, pending master acceptance. The finite free-module theorem,
minimal-polynomial divisibility,
matrix-power reduction, and field-specialized textbook statements are related consequences or
encodings, not replacements without checked directional crosswalks.
