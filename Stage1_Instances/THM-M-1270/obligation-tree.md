# THM-M-1270 frozen obligation tree

Registry version 1 freezes the architecture below before proof-phase closure credit. Every node is
open. The detailed schema, debts, ledgers, validation recipes, and typed reciprocal edges are in
`obligation-registry.json`, `typed-graphs.json`, and `validation-specs.json`.

## Root

`M1270-ROOT` is the exact declaration `EkelandVariationalPrincipleTarget`. It requires the checked
terminal composition `M1270-T-ASSEMBLE`; that composition assumes rather than constructs the hard
Ekeland witness package.

## S-exact

`M1270-S-EXACT` retains the ordered complete-metric, lower-semicontinuity, boundedness, positivity,
and pointwise approximate-minimizer boundary.

## S-boundary

`M1270-S-BOUNDARY` keeps both parameters strictly positive, so the penalty slope is meaningful, and
restricts the strict inequality to points distinct from the witness.

## S-transport

`M1270-S-TRANSPORT` is the already checked equivalence with the infimum-premise formulation. It is
an interface obligation and supplies no witness construction.

## S-foundation

`M1270-S-FOUNDATION` records the real-infimum, classical-choice, completeness, kernel, and pinned
dependency boundary. Transitive trust review remains open.

## N-slope

`M1270-N-SLOPE` normalizes the positive coefficient `epsilon / lambda`; later distance estimates
must use the same coefficient and parameter convention.

## C-sequence

`M1270-C-SEQUENCE` must construct a started quantitative descent sequence by selecting approximate
infima of successive descent sets. Choice and nonemptiness may not be hidden in a library slogan.

## C-invariants

`M1270-C-INVARIANTS` must prove nesting, value monotonicity, and penalized-distance drop estimates
for the sequence. These invariants are the shared inputs to Cauchy and maximality arguments.

## L-cauchy

`M1270-L-CAUCHY` must telescope value drops against the positive slope and use boundedness below to
prove `CauchySeq c`.

## L-limit

`M1270-L-LIMIT` must invoke completeness to obtain `v` and use lower semicontinuity to pass the
descent inequalities to the limit. Completeness and lower semicontinuity are separate boundaries.

## L-localize

`M1270-L-LOCALIZE` must derive both `f v <= f x0` and `dist v x0 <= lambda` from the construction,
the approximate-minimizer premise, and the normalized slope.

## L-maximal

`M1270-L-MAXIMAL` must show that a distinct point satisfying the non-strict descent relation would
contradict the terminal approximate-infimum property, yielding the strict inequality.

## T-witness

`M1270-T-WITNESS` packages one common point with value improvement, localization, and strict
penalized minimality. The conjuncts may not be proved using different witnesses.

## T-assemble

`M1270-T-ASSEMBLE` is checked by `ObligationTree.root_compose`. It maps the exact witness-package
premise to the exact root but does not instantiate that premise.

## X-anchors

`M1270-X-ANCHORS` records partial pinned mathlib infrastructure and the legacy conditional wrapper.
Neither is a terminal proof body for the root.

## X-source

`M1270-X-SOURCE` requires a pinpoint primary-source proof crosswalk and independent review; current
source debt remains `H1`/open.

## X-tcb

`M1270-X-TCB` requires transitive axiom, dependency, executable, and replay review before release.

## Status boundary

The frozen minimal open hard-core cut set is `C-SEQUENCE`, `C-INVARIANTS`, `L-CAUCHY`, `L-LIMIT`,
`L-LOCALIZE`, and `L-MAXIMAL`. Registry freeze and conditional composition do not close any member
of that set, the root remains `M3`, and neither `AUDIT-Z` nor `THEOREM-Z` is claimed.
