# Source-statement crosswalk

| Claim component | Human source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Weak convergence is preserved by an everywhere-continuous map | Patrick Billingsley, *Convergence of Probability Measures*, 2nd ed., Wiley, 1999, Section 2, Theorem 2.7 (the mapping theorem; the everywhere-continuous case is its immediate specialization) | Weak convergence of `Measure.map f` | Named standard source located, but edition scan, exact page, premises, and errata have not received independent acceptance: `H1` |
| Probability-measure hypothesis | Same theorem and surrounding weak-convergence definitions | `IsProbabilityMeasure` instances or probability-measure subtype | Exact Lean representation is deferred |
| Pushforward/law formulation | Mapping theorem conclusion | `Measure.map f mu` | Candidate object model; imports and definition side conditions are not yet checked |
| Random-variable formulation | Standard corollary obtained by applying the mapping theorem to distributions | Laws of `f \u2218 X_n` and `f \u2218 X` | Equivalent only after a checked law/pushforward transport; no intake credit |
| Continuity almost everywhere | Billingsley's more general discontinuity-set premise | Possible `mu`-a.e. continuity encoding | Deliberately excluded from the exact root rather than silently broadening it |

The repository's source phrase, "continuous maps preserve weak convergence," fixes the
everywhere-continuous specialization. It does not determine Lean's topology, measurability,
probability-measure packaging, or weak-convergence predicate. The statement phase must inspect the
pinned mathlib API, elaborate the minimal faithful type, serialize its normalized expression, and
mutation-test probability, continuity, domains, binder scope, and boundary maps.

Discovery reference (not an immutable evidence receipt):

- Billingsley bibliographic record: <https://www.wiley.com/en-us/Convergence+of+Probability+Measures%2C+2nd+Edition-p-9780471197454>

No `H0` or machine-closure claim is made. Follow-up requires a hashed source copy or stable edition
record, pinpoint page verification, an errata/corrections search, premise-to-node mapping, and
independent review.
