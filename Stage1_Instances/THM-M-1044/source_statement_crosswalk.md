# Source-statement crosswalk

| Claim component | Source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Repository claim | `Docs/Stage0_Blueprint.md`, THM-M-1044: "测度变换与鞅" | none | Names the topic but omits domains, binders, assumptions, and conclusion; insufficient to freeze an exact proposition |
| Brownian finite-horizon form | I. V. Girsanov, "On transforming a certain class of stochastic processes by absolutely continuous substitution of measures", *Theory of Probability and its Applications* 5 (1960), 285-301 | candidate only | Primary historical source family; edition/page-level assumptions and translation must be audited before adoption |
| Continuous-martingale form | D. Revuz and M. Yor, *Continuous Martingales and Brownian Motion*, 3rd ed., Springer, 1999, Chapter VIII, section 1 | candidate only | Modern source family; exact theorem number, hypotheses, corrections, and node crosswalk remain open |
| Semimartingale form | J. Jacod and A. N. Shiryaev, *Limit Theorems for Stochastic Processes*, 2nd ed., Springer, 2003, Chapter III, section 3 | candidate only | Strictly more general formulation; cannot be substituted for the source record without a scope decision |
| Density integrability | True-martingale status of a stochastic exponential is commonly assumed or established by a separate criterion | none | Novikov and Kazamaki are distinct manifest records; this intake does not conflate them with Girsanov |

## Crosswalk gap

The following choices change the proposition and must be resolved before the statement gate:

1. absolute continuity versus equivalence and which measure is defined from which;
2. finite versus infinite horizon and the time/index type;
3. Brownian, continuous local-martingale, or semimartingale setting;
4. density terminal variable versus density process and its normalization/positivity;
5. whether stochastic-exponential integrability is assumed or proved;
6. the sign convention for drift/covariation correction;
7. local martingale, true martingale, or Brownian-motion conclusion;
8. filtration usual conditions and completion under the changed measure.

No `H0` claim is made. The citations are discovery anchors, not immutable evidence receipts. A later
source audit must pin editions or file hashes, locate exact theorem/page statements, map every
assumption, check errata, and obtain independent review. A later Lean audit must separately inspect
mathlib and external candidates; no external theorem is claimed here.
