# THM-M-1522 frozen obligation architecture

Item: `S56-M-1522-OBLIGATION_TREE`. Registry version: 1. Freeze date: 2026-07-12.

The denominator contains 16 canonical obligations fixed from the elaborated statement and bounded
anchor audit before proof execution. Fourteen are machine-required, eleven require human-source
mapping, and all sixteen require a readable account. The root remains `M3`: the external pointwise
theorem is only an unchecked upstream anchor, and the ergodic constant-integral adapter is open.

## M1522-ROOT

The root is exactly `BirkhoffPointwiseErgodicTarget`, not an L1 or Hilbert mean-ergodic theorem.
For an integrable real observable on an ergodic probability system, its Birkhoff averages must
converge almost everywhere to `integral mu f`.

## Statement and normalization

<a id="m1522-s-definitions"></a> `M1522-S-DEFINITIONS` owns the orbit-average definitions.
<a id="m1522-s-domain"></a> `M1522-S-DOMAIN` owns the ordered measurable/probability/ergodic/L1
context. <a id="m1522-s-boundary"></a> `M1522-S-BOUNDARY` retains the almost-everywhere qualifier
and the harmless zero-index average. <a id="m1522-s-transport"></a> `M1522-S-TRANSPORT` is the
already checked finite-sum equivalence. <a id="m1522-s-foundation"></a> `M1522-S-FOUNDATION` keeps
the transitive axiom/TCB audit open. <a id="m1522-n-general"></a> `M1522-N-GENERAL` makes the central
reduction explicit: construct a general invariant pointwise limit, then identify it under ergodicity.

## Analytic core

<a id="m1522-c-limit-data"></a> `M1522-C-LIMIT-DATA` constructs an integrable invariant limit `g`
and preserves its integral. <a id="m1522-l-pointwise"></a> `M1522-L-POINTWISE` proves almost-everywhere
convergence to `g`; it is intentionally split-required because a single invocation of the external
project would hide the central theorem. <a id="m1522-x-upstream"></a> `M1522-X-UPSTREAM` separately
owns import, revision adaptation, body provenance, and trust audit for
`lua-vr/pointwise-birkhoff@fc06094ca0506d8d74eba8b45b34882ce5930bf4`.

<a id="m1522-b-ergodic"></a> `M1522-B-ERGODIC` derives almost-everywhere constancy of invariant `g`.
<a id="m1522-l-integral-id"></a> `M1522-L-INTEGRAL-ID` uses probability normalization and preserved
integral to identify that constant with `integral mu f`. <a id="m1522-t-identify"></a>
`M1522-T-IDENTIFY` packages those results as `ErgodicInvariantLimitIdentification`.

## Terminal composition

<a id="m1522-t-assemble"></a> `M1522-T-ASSEMBLE` is kernel-checked in `ObligationTree.lean`.
It consumes both `GeneralPointwiseLimitPackage` and `ErgodicInvariantLimitIdentification`, then
substitutes the a.e. limit equality into convergence. Both packages are explicit hypotheses, so
the checked declaration proves only the composition rule and gives no root closure by itself.

<a id="m1522-x-source"></a> `M1522-X-SOURCE` owns the still-open pinpoint source crosswalk.
<a id="m1522-x-provenance"></a> `M1522-X-PROVENANCE` owns wrapper/body provenance and cannot earn
independent proof credit.

## Closure boundary

The minimal root cut set is `M1522-L-POINTWISE` plus `M1522-T-IDENTIFY`. The registry, separate
proof/refinement/provenance/evidence/trust/documentation/workflow graphs, typed reciprocal edges,
and conditional composition are frozen and self-tested. No pointwise proof, H0 source status,
validation release, or theorem completion is claimed.
