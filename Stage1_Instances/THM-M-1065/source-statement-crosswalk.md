# Source-statement crosswalk

## Candidate primary sources

- J. Komlos, P. Major, and G. Tusnady, "An approximation of partial sums of independent RV's and
  the sample DF. I," *Zeitschrift fur Wahrscheinlichkeitstheorie und Verwandte Gebiete* 32 (1975),
  111-131, DOI `10.1007/BF00533093`.
- J. Komlos, P. Major, and G. Tusnady, "An approximation of partial sums of independent RV's and
  the sample DF. II," *Zeitschrift fur Wahrscheinlichkeitstheorie und Verwandte Gebiete* 34 (1976),
  33-58, DOI `10.1007/BF00532688`.

These bibliographic records are discovery anchors. Direct inspection must identify which numbered
theorem proves the included normalized partial-sum claim, transcribe its hypotheses and constants,
record dependencies between Parts I and II, and check publisher or author errata. Until that work
and independent review occur, these citations are not `H0` evidence.

## Crosswalk

| Intended claim component | Human-source evidence required | Required Lean component | Intake status |
|---|---|---|---|
| centered variance-one input law | exact integrability, centering, variance, and nondegeneracy premises | probability measure on `Real`, moments, normalization | included; exact source premises open |
| moment generating function near zero | exact interval and finiteness convention | exponential integrability predicate | included; encoding open |
| common-space coupling | source quantifiers and construction output | probability space plus two sequences with law and independence fields | included; construction not credited |
| matching Gaussian walk | exact normal/Brownian convention | i.i.d. standard normal increments or Brownian integer samples | included; representation choice open |
| uniform running maximum | source index range and partial-sum convention | finite sums and maximum over `1 <= k <= n` | included; boundary convention open |
| logarithmic threshold | exact constants, log convention, and additive terms | existential positive real constants and normalized inequality | included; constants open |
| exponential tail | exact probability inequality and range of deviation parameter | measurable discrepancy event and measure bound | included; exact relation open |
| almost-sure `O(log n)` consequence | source corollary or derivation from summable tails | eventual almost-sure asymptotic bound | downstream child; not root proof credit |

## Evidence boundary

The Stage0 description supplies only the Chinese phrase "strong approximation theorem" and the
manifest supplies only the theorem name and untrusted `已验证` label. Neither fixes a formal
proposition. No repo-local or external Lean declaration has been inspected or accepted in this
intake. The statement and anchor-audit phases must record exact modules, declarations, immutable
revisions, types, toolchains, axioms, placeholders, dependency feasibility, and terminal proof-body
provenance.

Before `H0`, an independent probability-source reviewer must approve a pinpoint
edition/theorem/page crosswalk for every row, including assumption translations, normalization,
dependent results, and errata status. Before any `M0` claim, the exact Lean target and all credited
transports must elaborate and the accepted proof closure must pass the rev-5.6 kernel and trust
gates.
