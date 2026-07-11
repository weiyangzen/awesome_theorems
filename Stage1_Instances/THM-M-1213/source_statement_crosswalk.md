# Source-statement crosswalk

| Claim component | Source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Attribution and date | Repository research record: Jean Ginibre / Giorgio Velo, 1979 | none | Metadata only; not H0 evidence |
| Subject | Repository wording: “NLS local well-posedness” | none | Too broad to determine one proposition |
| Likely primary-source candidate | J. Ginibre and G. Velo, *On a class of nonlinear Schrödinger equations. I. The Cauchy problem, general case*, Journal of Functional Analysis 32 (1979), 1–32 | none | Bibliographic candidate, not yet verified against a scanned edition or theorem number |
| Local existence | Expected component of well-posedness | unresolved | Equation, hypotheses, space, and lifespan must be extracted verbatim |
| Uniqueness | Expected component of well-posedness | unresolved | Uniqueness class must not be silently strengthened |
| Continuous dependence | Expected component of well-posedness | unresolved | Topologies and quantitative/uniform form must be frozen |

The repo-local source is `Docs/researches/math_theorems.md` at the “Ginibre-Velo theorem” entry.
It supplies no formula or parameter range. Consequently, no canonical Lean proposition can yet be
truthfully written. The similar but distinct `THM-M-1222` (“Ginibre-Velo NLW theorem”) must not be
used as a substitute.

Retry condition: obtain and hash the primary source, identify the exact theorem/page meant by the
catalog entry, record its equation, scalar field, dimension, nonlinearity assumptions, data and
solution spaces, time interval, existence/uniqueness/dependence clauses, endpoints, and errata, and
have an independent reviewer confirm that selection. Until then the human debt is `H3`, machine
debt is `M4`, and no anchor or wrapper receives proof credit.
