# Source-statement crosswalk

## Candidate sources

- A. N. Kolmogorov, *Grundbegriffe der Wahrscheinlichkeitsrechnung*, Ergebnisse der Mathematik
  und ihrer Grenzgebiete 2(3), Springer, 1933. This is the historical primary-book candidate named
  by the repository metadata. The exact section, page, original hypotheses, and correction history
  require direct edition inspection.
- K. L. Chung, *A Course in Probability Theory*, third edition, Academic Press, 2001, the chapter
  treatment of continuity of stochastic processes. This is a modern comparison source candidate;
  an exact theorem/page and convention audit is still required.

These are discovery anchors only. Neither candidate is an `H0` record, and the intake does not
attribute modern Holder-language or the exact compact-interval normalization to the 1933 edition
without inspection.

## Crosswalk

| Repository component | Frozen mathematical meaning | Required Lean component | Intake status |
|---|---|---|---|
| stochastic process | family `X_t` of real random variables on one probability space, `t in [0,T]` | measurable-space and measure parameters plus a time-indexed function | included; encoding open |
| increment condition | `E[|X_t-X_s|^alpha] <= C |t-s|^(1+beta)` uniformly in `s,t` | measurability/integrability, integral or expectation, real powers | included; normalization open |
| modification | `X_t = Y_t` almost surely for every fixed `t` | pointwise-in-time almost-everywhere equality under `P` | included; quantifier encoding open |
| regularity | for every `0 < gamma < beta/alpha`, almost every `Y` path is gamma-Holder on `[0,T]` | a pathwise Holder predicate and an almost-everywhere quantifier | included; exact API open |
| continuity theorem | continuity follows from positive Holder regularity | checked implication from the selected Holder predicate to continuity | required downstream transport |
| compact time domain | one-dimensional interval `[0,T]`, `T > 0` | interval subtype or `Set.Icc` restriction | frozen human scope; Lean choice open |

## Lean discovery boundary

A repository search found `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_221.lean`, which defines
a `KolmogorovChentsovContinuityConclusion` and explicitly describes its terminal continuity theorem
as missing. That file belongs to a different historical target and is only a discovery signal; it
is neither owned here nor evidence of closure for `THM-M-1083`. No exact mathlib declaration has
been selected or inspected in this intake.

Before `H0`, a source reviewer must pin an edition, locate the precise result, map every premise and
conclusion, check terminology and exponent conventions, search corrections, record immutable
identifiers or content hashes, and approve this crosswalk. Before machine credit, later phases must
audit exact modules, declarations, revisions, theorem bodies, logical dependencies, and integration
feasibility.
