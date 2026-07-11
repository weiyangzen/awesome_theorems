# Source-statement crosswalk

## Candidate sources

- A. V. Skorokhod, "Stochastic equations for diffusion processes in a bounded region," *Theory of
  Probability and Its Applications* 6 (1961), 264-274. This is the historical primary-paper
  candidate suggested by the repository year and reflected-diffusion gloss. The exact original or
  translated theorem, page, domain hypotheses, and corrections have not been inspected here.
- P.-L. Lions and A.-S. Sznitman, "Stochastic differential equations with reflecting boundary
  conditions," *Communications on Pure and Applied Mathematics* 37 (1984), 511-537. This is a
  modern primary research source candidate for reflected SDEs in domains; its exact theorem and
  assumptions remain to be inspected.
- J. M. Harrison and M. I. Reiman, "Reflected Brownian motion on an orthant," *The Annals of
  Probability* 9 (1981), 302-308. This is a candidate only if the intended scope is orthant
  reflection; it must not be generalized to arbitrary domains without source support.

These bibliographic records are discovery anchors, not `H0` evidence. An independent source audit
must verify an edition or scan, pinpoint theorem/page, definitions, hypotheses, errata, and the
relationship between the deterministic Skorokhod map and the stochastic theorem.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Skorokhod problem" | constrained path plus minimal regulator | path type, domain constraint, regulator, complementarity | family identified; exact variant open |
| "reflected stochastic differential equation" | SDE with boundary correction | stochastic integral equation, adaptedness, finite-variation process | literal gloss preserved; exact root open |
| existence | construct a reflected pair or stochastic solution | witnesses satisfying every equation and regularity condition | required; no machine evidence |
| uniqueness | uniqueness in the source-selected sense | equality of deterministic pairs, pathwise uniqueness, or uniqueness in law | notion open |
| boundary reflection | regulator acts only at the boundary | support/Stieltjes condition or normal-cone formulation | encoding open |
| 1961 / Skorokhod | historical locator | no formal component and no proof credit | candidate paper identified only |

## Source and machine boundary

The repository contains no theorem-specific legacy slot for this target, and a repository-wide
name search found no local Skorokhod declaration. That negative search is intake discovery only,
not the immutable mathlib/external anchor audit required by the later phase. No Lean module,
declaration, normalized expression, terminal proof body, or axiom profile has been accepted.

Before statement credit, a chosen source theorem must map row by row to ordered Lean binders,
hypotheses, conclusion, boundary cases, and checked transports. If the reflected-SDE theorem is
the root, a proof of only the deterministic half-line map is a dependency candidate, not a
substitute. If the deterministic problem is the root, stochastic consequences are outside that
root unless separately specified.
