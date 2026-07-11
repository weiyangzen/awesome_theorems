# Source-statement crosswalk

## Candidate primary sources

- M. F. Atiyah, R. Bott, and V. K. Patodi, "On the Heat Equation and the Index Theorem",
  *Inventiones Mathematicae* **19** (1973), 279-330, DOI `10.1007/BF01425417`. Candidate for local
  heat-equation index formulas; exact theorem/page and conventions remain to be inspected.
- J.-M. Bismut, "The Atiyah-Singer Index Theorem for Families of Dirac Operators: Two Heat Equation
  Proofs", *Inventiones Mathematicae* **83** (1986), 91-151. Candidate only if the intended theorem
  is the families/Dirac local formula; it must not be silently broadened into the target.
- H. P. McKean, Jr. and I. M. Singer, "Curvature and the Eigenvalues of the Laplacian", *Journal of
  Differential Geometry* **1** (1967), 43-69. Candidate for the heat-kernel route and local
  Gauss-Bonnet specialization; exact theorem/page wording remains to be inspected.

These bibliographic records are discovery anchors, not immutable source evidence or an `H0` claim.

## Crosswalk

| Metadata component | Candidate source meaning | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "local index theorem" | a family of local Atiyah-Singer formulas | operator and geometric variant must be explicit | unresolved |
| "local formula for the index density" | pointwise or differential-form heat-kernel asymptotics | density, supertrace, convergence/equality, and normalization required | included boundary, not frozen claim |
| topology/algebraic topology category | describes the global invariant | analytic and differential-geometric domains cannot be omitted | insufficient to select theorem |
| `已验证` | untrusted source metadata | grants no source or kernel credit | rejected as evidence |

Before `H0`, a reviewer must inspect a stable source edition, record the exact theorem label/pages
and incorporated definitions, check corrections or errata, and crosswalk every hypothesis and
conclusion. Before Lean elaboration, the statement owner must decide whether the root is a local
Dirac density, a de Rham/Gauss-Bonnet specialization, a families result, or another explicitly
sourced variant. The global integrated index formula is not an interchangeable replacement.
