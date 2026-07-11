# Source-statement crosswalk

Primary source: Hans Lindblad and Igor Rodnianski, *The global stability of Minkowski space-time in
harmonic gauge*, Annals of Mathematics (2) **171** (2010), no. 3, 1401-1477,
DOI `10.4007/annals.2010.171.1401`. The publication is the intended source anchor; a locally hashed
copy, theorem/page pinpoint, and errata review are still required before `H0`.

| Claim component | Source relationship | Lean target status | Intake assessment |
|---|---|---|---|
| Small asymptotically flat vacuum data | Hypothesis package of the paper's main global stability theorem | No declaration identified | Exact weighted Sobolev norms and asymptotic Schwarzschild/mass terms must be transcribed |
| Harmonic-coordinate evolution | Central reduction and construction in the paper | No declaration identified | Must distinguish reduced equations from constraint/gauge propagation |
| Global existence and decay toward Minkowski | Main analytic conclusion | No declaration identified | Exact decay and asymptotic clauses remain source-audit obligations |
| Future causal geodesic completeness | Geometric conclusion of the global stability result | No declaration identified | Cannot be weakened to global coordinate time |
| Vacuum Einstein solution | Follows only after propagation of gauge constraints is established | No declaration identified | Requires an explicit checked bridge in any formal proof |

The title and Stage0 gloss do not uniquely specify all binders or the smallness norm. Accordingly,
the intake freezes the theorem identity and semantic boundary, but deliberately leaves the exact
formal expression open rather than inventing constants or function spaces. Related
Einstein-scalar-field work and the Christodoulou-Klainerman theorem are excluded as substitutes.
