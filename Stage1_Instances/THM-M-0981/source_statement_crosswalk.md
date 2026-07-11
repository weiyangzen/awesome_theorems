# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Events form a field/sigma-field on an elementary event space | A. N. Kolmogorov, *Foundations of the Theory of Probability*, 2nd English ed., Chelsea, 1956, Chapter I, section 1 | `[MeasurableSpace Omega]` and measurable sets | Primary edition and section located; line/page scan and independent review remain open |
| Probability is a nonnegative set function | Kolmogorov 1956, Chapter I, section 1, Axiom III | `Measure Omega` has codomain `ENNReal` | Codomain correspondence is plausible but not yet a checked/source-reviewed transport |
| Unit mass | Kolmogorov 1956, Chapter I, section 1, Axiom IV: `P(E) = 1` | `IsProbabilityMeasure P`, candidate consequence `P univ = 1` | Clause maps directly, subject to exact elaboration |
| Additivity for disjoint events | Kolmogorov 1956, Chapter I, section 1, Axiom V; section 2 adds the continuity axiom leading to the infinite-field formulation | `measure_iUnion` for pairwise disjoint measurable `A : Nat -> Set Omega` | The candidate uses sigma-additivity. The historical finite-additivity-plus-continuity versus modern countable-additivity relationship requires an explicit source audit |
| Empty event has probability zero | Kolmogorov 1956, Chapter I, section 2, Theorem 1 | candidate `P empty = 0` | Consequence is retained explicitly by the repository predicate, not misreported as a separate original axiom |

The source title describes an axiomatic system rather than a single theorem. The frozen target is the
modern sigma-additive probability-measure packaging of its core clauses, not the legacy module's
adjacent results about laws, independence, martingales, stopping times, or Kolmogorov processes.

Discovery source (not an immutable evidence receipt): Kolmogorov, translated by Nathan Morrison,
Chelsea Publishing Company, 1956. H0 requires a hash-pinned scan, exact page/assumption mapping,
translation/edition comparison, errata search, and independent review. No H0 claim is made.
