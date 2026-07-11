# Source-statement crosswalk

## Candidate sources

- R. M. Dudley, "The sizes of compact subsets of Hilbert space and continuity of Gaussian
  processes," *Journal of Functional Analysis* 1 (1967), 290-330. This is the historical primary
  paper candidate. Its exact numbered theorem, constants, separability hypotheses, notation, and
  corrections must be checked from the paper before it can provide `H0` evidence.
- R. M. Dudley, "Sample functions of the Gaussian process," *Annals of Probability* 1 (1973),
  66-103. This is a primary-author refinement candidate for the boundedness/continuity formulation;
  the precise relation of its statement to the expected-supremum inequality remains to be audited.
- M. Talagrand, *Upper and Lower Bounds for Stochastic Processes*, Springer, 2014, Chapter 1. This
  is a modern reconstruction candidate for chaining and entropy bounds, not a substitute for
  checking the historical source. Exact theorem/page, assumptions, and published errata remain open.

These bibliographic records are discovery anchors, not accepted source receipts. Intake does not
infer `H0` or an exact constant from the theorem name or a secondary summary.

## Crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| Dudley entropy bound | entropy-integral upper bound | one exact theorem declaration | included; expression open |
| Gaussian process | centered separable real Gaussian family | probability space, random variables, joint Gaussian predicate | included; API open |
| canonical metric | square root of increment variance | expectation, square, nonnegativity, pseudometric construction | included; quotient details open |
| metric entropy | logarithm of covering number | finite covers/balls and least cardinal encoding | included; convention open |
| entropy integral | integral of square-root log covering number | measurable extended-real/real integrand and endpoint convention | included; normalization open |
| upper bound | expected based supremum bounded by a universal constant times the integral | measurable supremum, integrability, inequality | included; constant open |
| separability | countable reduction controlling the supremum | separable modification or dense countable index bridge | required; encoding open |
| total boundedness | finite covers at every positive radius | pseudometric total-boundedness predicate | required |

## Assumption and boundary audit still required

The source audit must determine whether the selected theorem assumes a countable index set first,
sample separability, continuity, or merely a separable canonical pseudometric space; whether it
bounds a based supremum, an absolute increment supremum, or a diameter; and whether finiteness of
the entropy integral is an assumption or an extended-real conclusion. It must crosswalk the empty
and singleton index cases, zero diameter, zero-variance identifications, and infinite covering
numbers. Constants and integration endpoints must be compared under the same ball convention.

## Evidence boundary

No repo-local Lean declaration or external formal proof has been accepted or inspected in this
intake. The later anchor-audit phase must search the pinned mathlib revision and credible Lean 4
projects, recording exact modules, declaration types, immutable revisions, axioms, placeholders,
and terminal proof-body provenance. Before `H0`, an independent reviewer must verify the chosen
edition, theorem/page, assumptions, normalization, errata, and every row of the source-to-Lean map.
