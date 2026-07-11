# Source-statement crosswalk

| Claim component | Source anchor | Formal candidate | Intake assessment |
|---|---|---|---|
| Large deviations for sums of independent variables | H. Cramer, "Sur un nouveau theoreme-limite de la theorie des probabilites", *Actualites Scientifiques et Industrielles* 736 (1938), pp. 5-23 | `CR-ROOT`, `CR-TAIL` | Primary historical source identified, but exact scan, theorem pinpoint, assumptions, and errata are not yet audited |
| Modern real-valued LDP formulation | A. Dembo and O. Zeitouni, *Large Deviations Techniques and Applications*, 2nd ed., Springer (1998), Theorem 2.2.3 | `CR-UPPER`, `CR-LOWER`, `CR-RATE` | Secondary normalization anchor only; edition text and premise-by-premise mapping remain open |
| Log-mgf and Legendre transform | Same modern reference, Section 2.2 | `CR-LMGF`, `CR-RATE` | Candidate definitions; no Lean encoding selected |
| Repository wording | `Docs/researches/math_theorems.md`, THM-M-1059: "large deviations of sums of independent random variables" | none | Too underspecified to freeze a unique formal target |

The likely modern root says that empirical means of i.i.d. real random variables satisfy upper and
lower exponential bounds with rate function given by the Legendre-Fenchel transform of the log-mgf.
This is a discovery paraphrase, not the frozen statement. In particular, the original theorem's
tail formulation must not be treated as definitionally identical to the later topological LDP.

No source is accepted at `H0`. The statement/source phases must acquire immutable source artifacts,
record exact theorem/page and edition identifiers, audit corrections, map every hypothesis and
conclusion to a scope node, and obtain independent review.

