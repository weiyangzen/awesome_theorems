# Source-statement crosswalk

## Candidate primary sources

- M. F. Atiyah and I. M. Singer, "The Index of Elliptic Operators: I", *Annals of Mathematics*
  **87** (1968), 484-530, DOI `10.2307/1970715`. This is a primary source for the general index
  theorem, but not by itself a uniquely identified heat-kernel formulation.
- H. P. McKean, Jr. and I. M. Singer, "Curvature and the Eigenvalues of the Laplacian", *Journal of
  Differential Geometry* **1** (1967), 43-69. This is a primary candidate for the heat-equation
  method and heat-trace index identity; exact theorem/page wording still requires inspection.
- M. F. Atiyah, R. Bott, and V. K. Patodi, "On the Heat Equation and the Index Theorem",
  *Inventiones Mathematicae* **19** (1973), 279-330, DOI `10.1007/BF01425417`. This is a primary
  candidate for the named proof method; its exact operator assumptions and formula must be checked.

These are discovery anchors, not immutable evidence receipts and not an `H0` claim.

## Crosswalk

| Metadata component | Candidate source meaning | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "index theorem" | likely Atiyah-Singer, but variant unspecified | operator, symbol class, and topological index must be explicit | unresolved |
| "heat-kernel proof" | heat supertrace and local asymptotics are proof architecture, not necessarily the root statement | analytic semigroup, kernel, trace-class, and asymptotic infrastructure required | included method boundary only |
| topology/algebraic topology category | records the topological output | differential-geometric and functional-analytic domains cannot be omitted | insufficient to select a theorem |
| `已验证` | untrusted source metadata | supplies no source or kernel credit | rejected as evidence |

Before `H0`, a reviewer must inspect a stable edition, record exact theorem labels/pages and all
incorporated definitions, check corrections or errata, crosswalk every hypothesis and conclusion,
and independently approve the mapping. Before a Lean statement, the reviewer must also decide
whether the root is the index equality or a specifically named heat-kernel lemma; neither may be
silently substituted for the other.
