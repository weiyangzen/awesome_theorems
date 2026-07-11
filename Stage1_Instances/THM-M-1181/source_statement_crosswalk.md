# Source-statement crosswalk

## Repository source

The upstream metadata record in `Docs/researches/math_theorems.md` names Luis Caffarelli, dates the
result to 1990, and gives only `凸解的内部正则性`. That phrase is not an exact mathematical
statement. In particular it does not distinguish the conclusion `C^{1,alpha}`, `W^{2,p}`, or
`C^{2,alpha}`, nor the corresponding assumptions on the Monge-Ampere density.

## Candidate primary-source map

| Candidate branch | Primary source discovery anchor | Candidate assumptions/conclusion | Intake assessment |
|---|---|---|---|
| Strict convexity and interior `C^{1,alpha}` | L. A. Caffarelli, "A localization property of viscosity solutions to the Monge-Ampere equation and their strict convexity," *Annals of Mathematics* 131 (1990), 129-134, DOI `10.2307/1971519` | Convex generalized/viscosity solution, controlled Monge-Ampere measure; localization yields strict convexity and feeds interior regularity | Plausible match to the year and generic wording, but exact theorem number, hypotheses, and conclusion need inspection |
| Interior `W^{2,p}` | L. A. Caffarelli, "Interior W2,p estimates for solutions of the Monge-Ampere equation," *Annals of Mathematics* 131 (1990), 135-150, DOI `10.2307/1971520` | Interior second-derivative integrability for convex solutions under quantitative density assumptions | Plausible intended "interior regularity" theorem; `p`, density assumptions, normalization, and local domain must be transcribed from the paper |
| Interior `C^{2,alpha}` | L. A. Caffarelli, "Interior a priori estimates for solutions of fully nonlinear equations," *Annals of Mathematics* 130 (1989), 189-213, DOI `10.2307/1971480` | Stronger interior regularity for fully nonlinear elliptic equations under additional structure/regularity | Related source family, but the repository's 1990 date weighs against silently selecting it |

DOIs are discovery locators, not immutable evidence receipts. No edition/file hash, theorem/page
pinpoint, errata audit, or independent source review has been accepted, so no `H0` claim is made.

## Statement component crosswalk

| Component requiring a freeze | Repository wording | Candidate formal representation | Required decision |
|---|---|---|---|
| Ambient space | absent | finite-dimensional real Euclidean space, likely `Fin n -> Real` | fix dimension restrictions and coordinate invariance |
| Domain | absent | open convex `Omega`, with compactly contained subdomains for interior estimates | fix boundedness, normalization, and boundary distance |
| Solution notion | "convex solution" | convex Aleksandrov or viscosity solution | select the source's notion and prove any bridge used |
| Equation/data | absent | Monge-Ampere measure `Mu_u = f dx` or `det(D2 u) = f` | fix weak/classical formulation and density measurability |
| Ellipticity bounds | absent | constants `0 < lambda <= f <= Lambda` | transcribe exact quantifier and almost-everywhere/measure meaning |
| Conclusion | "interior regularity" | one of strict convexity, `C^{1,alpha}_loc`, `W^{2,p}_loc`, or `C^{2,alpha}_loc` | choose exactly one cited theorem; do not merge strengths |

## Lean crosswalk boundary

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_149.lean` defines an abstract input
and output package and explicitly says it does not prove the terminal theorem. It may guide API
discovery, but its implication-from-an-assumed-package is not an exact Caffarelli theorem and earns
no rev-5.6 proof credit. The statement phase must first resolve the primary source, then elaborate a
non-circular proposition and mutation-test its domain, density bounds, convexity, solution notion,
and interior boundary.

First actionable gate: inspect the two 1990 Annals papers in full, record theorem/page and all
assumptions, reconcile the repository's singular label with one result, and obtain independent
review before assigning a canonical Lean target.
