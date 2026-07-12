# THM-M-0995 obligation registry and typed graphs

Registry version 1 freezes thirteen obligations before proof closure is observed. Proof,
refinement, provenance, evidence, trust, documentation, and workflow edges are separate; every
proof-requires edge has a reciprocal composition edge.

## root
The exact bounded independent-summand upper-tail Bernstein target remains open at `M3`.

## s-exact
Preserve the frozen package, hypotheses, non-strict event, constants, and totalized division.

## l-ind-mgf
Derive the variance-sensitive individual MGF inequality for `0 <= s` and `s*b < 3`. This is the
critical missing mathematical bridge; mathlib's Hoeffding MGF result has a different exponent.

## l-sum-mgf
Use independence to factor the MGF, combine individual bounds, and apply the variance budget.

## l-chernoff
Apply exponential Markov to the exact partial sum and upper-tail event. Mathlib provides a relevant
anchor, but its specialization to this interface is deferred to the proof phase.

## l-optimize
For a positive denominator, choose `s = t/(v+b*t/3)`, prove admissibility, and check the exact
exponent inequality.

## b-zero-denom
Handle `v+b*t/3 = 0` separately. Lean's real division is totalized, so the right side is one; the
ordinary positive-denominator tilt argument is not silently applied here.

## b-empty
Keep `n = 0` and the zero partial sum inside the theorem boundary.

## t-assemble
Split on the denominator and compose the five substantive packages into the exact root.

## x-mathlib
Pin the Chernoff, independent-sum, variance, and Hoeffding-support bodies at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. They are supporting anchors, not an exact proof.

## x-external
Record HighDimProb revision `8d4eec8bc06d80e8436ab3505000fca999b46546` as a materially mismatched
anchor. It supplies no completion credit without a checked exact transport and local integration.

## x-source
A primary theorem/page, assumption crosswalk, proof reconstruction, errata review, and independent
human-source review remain open.

## x-tcb
The release-grade transitive dependency, axiom, executable, computation, and platform audit remains
open.

## Closure boundary

`ObligationTree.root_compose` checks exact conditional parent composition. It does not discharge its
premises. No obligation is recorded closed. The root cut set is `L-IND-MGF`, `L-SUM-MGF`,
`L-CHERNOFF`, `L-OPTIMIZE`, and `B-ZERO-DENOM`; every current semantic unit has a budget of at most
100 steps, but those budgets are plans rather than closure evidence.
