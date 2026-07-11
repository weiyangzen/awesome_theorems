# Source-statement crosswalk

| Claim component | Repository metadata | Primary-source discovery anchor | Intake assessment |
|---|---|---|---|
| Theorem family | "Harnack inequality (divergence form)"; attributed to John Nash/Jurgen Moser; year 1958 | J. Moser, *On Harnack's theorem for elliptic differential equations*, Communications on Pure and Applied Mathematics 14 (1961), 577-591, DOI `10.1002/cpa.3160140329` | Plausible primary theorem-family anchor, but the repository's 1958 date does not identify a theorem or edition |
| Divergence-form equation | Only the Chinese gloss `散度型椭圆方程的Harnack不等式` | Moser 1961 title and paper must be inspected at theorem/premise level | Exact operator, coefficient regularity, symmetry, and homogeneous/inhomogeneous scope are unresolved |
| Weak-solution and sign conditions | Not stated | Moser 1961, exact definition/theorem pinpoint still required | Sobolev domain, weak formulation, and nonnegative/positive convention cannot yet be frozen |
| Ellipticity | Not stated | Moser 1961, exact assumptions and notation still required | Lower/upper bounds and constant dependencies remain open |
| Geometric region | Not stated | Moser 1961, theorem-local domains/balls still required | Interior versus boundary claim and region nesting remain open |
| Inequality | Not stated beyond the family name | Moser 1961, displayed conclusion and quantifiers still required | `sup`/`inf` versus essential extrema and the controlling constant remain open |
| Lean target | Target system selected as Lean 4 by rev-5.6 | No repo-local declaration has been accepted | Later statement phase must search pinned mathlib, define missing analytic structures if necessary, elaborate the exact target, and mutation-test every assumption |

The Nash/Moser attribution is useful genealogy, not a precise citation. Nash's regularity work and
Moser's iteration are related, but neither a regularity theorem nor a harmonic-only Harnack theorem
may replace the requested divergence-form inequality. Before statement work proceeds, an auditor
must obtain an immutable copy of the selected primary source, record theorem/page and errata, and
map every coefficient, solution, domain, and constant premise to the formal target.

Discovery link (not an evidence receipt): <https://doi.org/10.1002/cpa.3160140329>.

No `H0` or machine-closure claim is made.

