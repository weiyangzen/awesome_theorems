# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` attributes "Tanaka's formula" to Hiroshi Tanaka (1963) and gives
only the phrase "the Ito formula for reflected Brownian motion" plus `已验证`. `Docs/Stage0_Blueprint.md`
repeats that phrase but supplies no definitions, formula, bibliography, theorem locator, or machine
artifact. The status label is explicitly untrusted under rev-5.6.

## Candidate human sources

- H. Tanaka, "Note on continuous additive functionals of the 1-dimensional Brownian path,"
  *Zeitschrift fuer Wahrscheinlichkeitstheorie und Verwandte Gebiete* 1 (1963), 251-257. This is
  the historical primary-paper candidate. The exact theorem/page, formula convention, hypotheses,
  stable copy hash, and corrections have not been inspected in this intake.
- D. Revuz and M. Yor, *Continuous Martingales and Brownian Motion*, third edition, Springer, 1999,
  Chapter VI (local times and Tanaka's formula). This is a modern source candidate for interpreting
  conventions and variants; exact theorem/page and errata remain to be pinned.

These entries are discovery anchors, not `H0` evidence. `H1` records that a published proof is
known while exact statement, assumptions, errata, and node mapping remain unaudited.

## Crosswalk

| Repository/source phrase | Mathematical component | Required Lean surface | Intake result |
|---|---|---|---|
| "Tanaka's formula" | one exact nonsmooth stochastic-calculus identity | canonical proposition with fixed binders | family identified; variant open |
| "reflected Brownian motion" | reflection/local-time relation for a Brownian path | Brownian process plus reflection or Skorokhod decomposition | included scope signal; root-versus-corollary open |
| "Ito formula" | stochastic integral term plus correction for a nonsmooth function | stochastic integral and process equality API | included; no accepted API anchor |
| positive part / absolute value | convex nonsmooth test function | real positive part/absolute value applied pointwise | source choice open |
| local time | local time at a level with a fixed normalization | constructed local-time process, not an assumed conclusion | normalization and construction open |
| equality in time | pathwise/process identity | a.s. fixed-time or simultaneous/process equality | quantifier and null-set scope open |
| `已验证` | historical repository metadata | inspectable proof/source receipt | no credit |

## Required acceptance work

Before statement acceptance, a source reviewer must pin an immutable primary source, locate the
exact result and displayed formulas, transcribe every hypothesis and normalization, check errata,
and decide how the repository's reflection wording maps to that result. Every crosswalk row must
then point to the canonical Lean binder or definition and any alternate form must have a checked
relationship witness.

No repo-local or external Lean declaration was accepted or credited here. The anchor-audit phase
must search the pinned mathlib revision and credible Lean 4 projects and record exact module,
declaration type, revision, toolchain, proof-body provenance, dependencies, axioms, placeholders,
and compatibility with the source-selected identity.
