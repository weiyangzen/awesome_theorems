# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` attributes the result to Christer Borell and to
Tsirelson-Ibragimov-Sudakov, dates it to 1976, and supplies only the phrase "concentration of
Gaussian processes" plus the untrusted label `已验证`. `Docs/Stage0_Blueprint.md` repeats that phrase
while leaving the definitions, hypotheses, equivalent forms, axioms, proof route, and machine
artifacts open. These records identify the named theorem family but not one exact proposition.

## Candidate sources

- Christer Borell, "The Brunn-Minkowski inequality in Gauss space," *Inventiones Mathematicae* 30
  (1975), 207-216. This is a historical primary-paper candidate for the Gaussian isoperimetric
  route underlying the inequality. Its exact statement-to-process corollary, assumptions, pages,
  and correction history require direct inspection.
- B. S. Tsirelson, I. A. Ibragimov, and V. N. Sudakov, "Norms of Gaussian sample functions,"
  *Proceedings of the Third Japan-USSR Symposium on Probability Theory*, Lecture Notes in
  Mathematics 550, Springer (1976), 20-41. This is the historical TIS source candidate; the exact
  numbered result, translated wording, conventions, and errata require inspection.
- Robert J. Adler and Jonathan E. Taylor, *Random Fields and Geometry*, Springer (2007), Theorem
  2.1.1. This is a modern statement candidate for the Borell-TIS inequality. Edition wording,
  surrounding definitions, page locator, hypotheses, and published errata must still be checked.

These citations are discovery anchors only, not `H0` evidence. Intake does not infer an exact
statement or proof genealogy from their titles.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| Borell-TIS inequality | concentration theorem for a Gaussian-process supremum | one exact canonical declaration | claim family included; expression open |
| Gaussian process | jointly Gaussian real random variables | probability space, measurable random variables, finite-dimensional Gaussian predicate | included; encoding open |
| centered | `E[X_t] = 0` for each index | integrability and expectation equality | included |
| supremum | `S = sup_t X_t` with an a.s. finite measurable representative | separability/countable reduction, supremum and integrability | included; conventions open |
| variance proxy | `sigma^2 = sup_t Var(X_t)` | variance, bounded supremum, nonnegativity | included; zero case open |
| concentration | exponential bound for deviations of `S` from `E[S]` | event measurability, probability inequality, exponential arithmetic | included; tail sidedness open |
| `已验证` | repository screening label | accepted source review or kernel receipt | no credit |

## Required source audit

Before `H0`, an independent reviewer must select and inspect a stable edition, record the exact
theorem/page, verify every hypothesis and definition, check errata, and map the one-sided/two-sided
form, strict versus non-strict event, constant, variance convention, and all boundary cases to the
canonical Lean expression. The relationship between the Borell isoperimetric source and the TIS
process formulation must be recorded rather than conflated.

No repo-local Lean declaration or external formal candidate is accepted at intake. Anchor audit
must search the pinned mathlib revision and credible Lean 4 projects and record exact modules,
declaration types, immutable revisions, axioms, placeholders, and terminal proof-body provenance.
