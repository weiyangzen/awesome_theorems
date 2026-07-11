# Source-statement crosswalk

## Candidate primary sources

- Peter Freyd, *Abelian Categories: An Introduction to the Theory of Functors*, Harper & Row
  (1964). This is a primary monograph candidate for the embedding and generator terminology; the
  exact theorem/page, hypotheses, and edition scan have not yet been inspected.
- Barry Mitchell, *Theory of Categories*, Pure and Applied Mathematics 17, Academic Press (1965).
  This is a historical source candidate for the embedding theorem now called Freyd-Mitchell; its
  exact statement and relation to Freyd's formulation remain to be checked.

These are discovery anchors, not `H0` evidence. No theorem number is asserted at intake.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "embedding theorem" | full faithful exact representation of a small abelian category | category, abelian structure, ring, module-category functor, fullness, faithfulness, exactness | included; conventions open |
| "generator existence" | injective cogenerator from a generator and auxiliary hypotheses | limits, enough injectives, separator, injective coseparator | separate branch; source identity open |
| dual existence | projective generator from dual hypotheses | colimits, enough projectives, coseparator, projective separator | included as legacy dual branch |
| "exact" | preservation of short exact sequences / finite (co)limits | source-equivalent exactness predicate or checked transport | encoding open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_134.lean` imports
`Mathlib.CategoryTheory.Abelian.FreydMitchell` and
`Mathlib.CategoryTheory.Generator.Abelian`. It records wrappers around
`CategoryTheory.Abelian.freyd_mitchell`, `has_injective_coseparator`, and
`has_projective_separator`. Those declarations are valuable candidates, but the legacy file's
revision string and local checks are not accepted rev-5.6 receipts. The statement and anchor-audit
phases must independently inspect their exact types, dependency revision, axioms, and source match.

Before `H0`, a reviewer must verify stable source scans, exact theorem/page, every hypothesis and
definition, any errata, and the row-by-row source-to-Lean correspondence, especially whether the
three branches form one justified target.
