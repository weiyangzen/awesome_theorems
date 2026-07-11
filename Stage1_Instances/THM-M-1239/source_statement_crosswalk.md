# Source-statement crosswalk

| Repository component | Exact available wording | Intake consequence | Assessment |
|---|---|---|---|
| Name | `Poincare不等式` | Selects the Poincare-inequality family | Not an exact proposition |
| Category | `微分方程 / 偏微分方程` | Selects the PDE rather than probability branch | Domain and boundary model remain unknown |
| Content gloss | `Sobolev函数的L^p估计` | Requires a Sobolev and `L^p` formulation | Neither side of the estimate nor its assumptions are stated |
| Attribution/date | Henri Poincare; 1890 | Historical metadata | No work, edition, page, theorem number, or original text is given |
| Source status | `已验证` | Discovery metadata only | Explicitly untrusted under rev-5.6; gives no H0 or machine credit |

The inspected repository sources are `Docs/researches/math_theorems.md`,
`Docs/Stage0_Blueprint.md`, `Docs/Stage1_Blueprint_Applicable_Theorems.md`, and
`Docs/Stage1_Targets_rev-5.6.json`. Their wording agrees, but none supplies a theorem-level citation
or the missing mathematical parameters. In particular, the year and attribution do not identify
which modern Sobolev-domain formulation is intended.

Human debt is therefore `H4`: the claim family is recognizable, but exact source fidelity cannot
be audited. Retry requires an authoritative theorem statement fixing the domain, exponent,
function space, normalization/boundary condition, norms, gradient, and constant dependence, with
an immutable edition or file hash, pinpoint locator, assumptions, and errata review.
