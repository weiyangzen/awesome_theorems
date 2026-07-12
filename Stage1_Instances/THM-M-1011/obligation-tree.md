# THM-M-1011 frozen obligation architecture

Item: `S56-M-1011-OBLIGATION_TREE`

The denominator is frozen from the exact `CanonicalStatement` and the bounded
anchor audit before proof-closure metrics are observed.  All nodes are root
relevant.  The checked Lean composition is conditional on an explicit
`T2Space X`; the frozen pseudo-metric context does not synthesize that child.

## M1011-ROOT

For every family of Borel probability measures in the frozen complete,
second-countable pseudo-metric context, uniform tightness is equivalent to
compactness of its closure in the weak topology.  This exact root remains M5.

## M1011-S-DEFINITIONS

Freeze probability measures, their underlying measures, uniform tightness,
weak topology, closure, and compactness.  The Lean aliases and their unfolding
are checked, but definitions alone carry no theorem credit.

## M1011-S-DOMAIN

Preserve all ordered binders.  In particular, do not silently replace
`PseudoMetricSpace X` by `MetricSpace X` or add `T2Space X`.  The anchor audit
checks that instance synthesis for the latter fails in the frozen context.

## M1011-S-BOUNDARY

The family is arbitrary and includes empty, singleton, and finite families.
No nonempty-family premise may appear in a child proof.  Exact boundary lemmas
remain open proof work.

## M1011-S-TRANSPORT

The local tightness alias unfolds to `IsTightMeasureSet` on the image under the
probability-measure coercion.  Relative compactness is frozen as compactness of
closure.  Other conventions require separately checked directional transport.

## M1011-S-FOUNDATION

The current wrapper reports `propext`, `Classical.choice`, and `Quot.sound`.
A transitive declaration, unsafe/oracle, kernel, and dependency audit remains
required before any release claim.

## M1011-N-SEPARATION

Resolve the separation mismatch without strengthening or substituting the
target: either prove an exact `T2Space X` bridge from the frozen hypotheses, or
return to the statement gate and re-freeze a corrected claim.  This is the
immediate root cut set and remains M5.

## M1011-B-TIGHT-COMPACT

Uniform tightness must imply compact closure in the exact context.  The checked
wrapper `tight_to_compact_of_t2` is conditional on M1011-N-SEPARATION and does
not close this branch.

## M1011-B-COMPACT-TIGHT

Compact closure implies uniform tightness through the pinned mathlib theorem
`isTightMeasureSet_of_isCompact_closure`.  The exact local wrapper elaborates;
this is direction-only M0-W evidence, not root closure.

## M1011-L-PROKHOROV

The forward imported engine is
`isCompact_closure_of_isTightMeasureSet`.  Its exact signature requires
`T2Space X`, so a short invocation cannot hide the open separation obligation.

## M1011-L-COMPACT-TIGHT

The reverse imported engine is
`isTightMeasureSet_of_isCompact_closure`.  It shares one terminal mathlib proof
body with its wrapper and is counted once in unique proof-body coverage.

## M1011-T-ASSEMBLE

`canonical_of_t2` explicitly consumes the separation child and both directional
children and yields the exact canonical proposition.  It is a checked
child-to-parent interface only because the separation child is open.

## M1011-X-SOURCE

Pinpoint primary-source theorem, edition, page, assumptions, conventions, and
errata coverage remains H1.  The source overlay is not a proof premise.

## M1011-X-PROVENANCE

The anchor audit records pinned mathlib bodies, revision, license, axioms, and
the rejected placeholder-bearing external candidate.  This informational
overlay cannot duplicate semantic or proof-body credit.

## Closure boundary

Every prospective leaf ledger is at most 100 substantive steps, while the
central imported theorem remains its own bridge obligation.  The seven graph
families are separate in `typed-graphs.json`.  The root is open at M5; H0, R0,
audit completion, theorem completion, release, and master acceptance are not
claimed.
