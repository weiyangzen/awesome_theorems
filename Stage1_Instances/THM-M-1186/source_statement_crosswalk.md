# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository label "McCann theorem" | R. J. McCann, *A convexity principle for interacting gases*, Advances in Mathematics 128 (1997), 153-179, DOI 10.1006/aima.1997.1634 | no exact declaration selected | Primary McCann paper identified, but its named convexity/displacement results are not automatically the repository's existence claim |
| Existence of an optimal coupling | C. Villani, *Topics in Optimal Transportation*, AMS GSM 58 (2003), Chapter 1 (secondary discovery anchor) | `StatementShapeCompactMetric` | Standard compactness/direct-method claim; exact theorem/page and primary genealogy still require audit |
| Couplings with fixed marginals | Same optimal-transport setup | `TransportPlan`, `ProbabilityCouplingSet` | Candidate object models only; equivalence and instance side conditions are unchecked in rev-5.6 |
| Compactness of feasible couplings | Prokhorov compactness/direct method | `probabilityCouplingSet_isCompact_of_compactMetric` | Historical local theorem is unaccepted discovery input |
| Lower-semicontinuous cost attains a minimum | extreme-value/direct-method step | `LowerSemicontinuousCostFunctionalTarget`, `exists_optimal_transportPlan_of_compactMetric_lscTarget` | Candidate bridge; the full l.s.c. integral premise is an open legacy leaf |

The target cannot yet truthfully be called an exact formalization of a particular McCann theorem.
The statement phase must first resolve whether the authoritative claim is (a) Kantorovich
existence, (b) McCann displacement interpolation/convexity, or (c) a specifically cited theorem
combining them. It must then freeze the source edition and pinpoint, serialize the elaborated Lean
type, verify transports, and mutation-test domains, hypotheses, binder scope, and infinite costs.

No `H0`, exact-statement, or machine-proof claim is made.
