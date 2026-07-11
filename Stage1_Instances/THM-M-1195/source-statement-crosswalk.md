# Source-statement crosswalk

## Available source record

The repository inventory (`Docs/researches/math_theorems.md`) gives the title "Perelman entropy",
attribution to Grigori Perelman, year 2002, and the phrase "the entropy functional for Ricci flow".
Its `verified` status is untrusted metadata. No formula, theorem number, page, hypotheses, or Lean
declaration accompanies the entry.

The primary source family is Grigori Perelman, *The entropy formula for the Ricci flow and its
geometric applications*, arXiv:math/0211159 (submitted 11 November 2002). Sections 1-3 introduce
several related functionals and monotonicity formulae. This citation identifies the family only:
edition/page and errata checks and a precise result-level crosswalk remain downstream work.

## Crosswalk

| Source element | Information fixed | Information still open | Intake result |
|---|---|---|---|
| "Ricci flow" | evolving Riemannian metric | manifold class, interval, convention, regularity | unresolved |
| "entropy functional" | real-valued geometric/analytic functional | F or W, formula, normalization, auxiliary data | unresolved |
| Perelman / 2002 | author and primary paper family | exact section, displayed formula/result, errata | family identified |
| implicit theorem content | likely variation or monotonicity property | binders, hypotheses, conclusion, equality case | unresolved |
| `verified` | repository screening label | inspectable proof and kernel receipt | no credit |

## Lean boundary

No target-specific legacy artifact or canonical Lean declaration was found in the repository search
at intake. A future statement cannot receive credit from a merely analogous mathlib Ricci-flow or
measure-theory declaration. Before H0, a reviewer must verify the primary source at result level and
approve a row-by-row mapping from every source definition and assumption to the canonical Lean
expression. Before any M credit, that exact expression must elaborate under pinned imports.
