# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `Elekes-Szabó定理`, attributes it to Gyorgy Elekes and
Endre Szabo, gives the year 2012, and supplies only `多项式在格点上的取值` ("values of a polynomial
on grid points"). `Docs/Stage0_Blueprint.md` repeats that gloss and marks the exact definitions,
assumptions, proof route, axioms, and formal artifact as open. The manifest preserves `已验证` only
as `source_status_untrusted`.

Thus the repository record contains no exact statement, theorem/page citation, ordered hypotheses,
conclusion, proof source, edition, or errata record.

## Primary-source candidate

Gyorgy Elekes and Endre Szabo, *How to find groups? (And how to use them in Erdős geometry?)*,
Combinatorica 32 (2012), is a bibliographic candidate suggested by the title, authors, and year.
It is only a discovery locator here: no stable copy, exact theorem number/page, definitions,
assumptions, proof boundary, or errata was independently inspected during this intake. It supplies
no `H0` credit. Later incidence-bound papers must be treated as separate candidates rather than as
silent restatements of the 2012 result.

## Crosswalk

| Repository/source phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "polynomial" | a three-variable polynomial defining a surface | `MvPolynomial` plus a fixed three-variable index type | API probed; coefficient field and hypotheses open |
| "grid points" | a finite Cartesian product `A x B x C` | `Finset.product`/finite-set cardinality and evaluation | API probed; exact cardinality regime open |
| "values" | usually a zero-set incidence count, not merely an image set | evaluation equation and filtered/product cardinality | repository wording ambiguous |
| "Elekes-Szabo theorem" | structural many-points-implies-group alternative | exceptional locus, local charts, and group relation | theorem/version and exact conclusion open |
| quantitative form | an upper bound outside the group-like case | exact exponent, constants, degree dependence | possible later/refined reading only |
| `已验证` | untrusted inventory label | no proposition or proof term | explicitly rejected as evidence |

## Lean and review boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
elaborates basic polynomial-evaluation and finite-product APIs. These are encoding ingredients only.
The bounded repository and pinned-mathlib name search found no Elekes-Szabo declaration; that is not
a substitute for the later immutable anchor audit.

Before statement credit, an independent reviewer must inspect one immutable source edition and map
its statement, every definition and hypothesis, exceptional cases, and conclusion row by row to an
elaborated Lean expression. Before `H0`, the proof passage and errata status also require review.

