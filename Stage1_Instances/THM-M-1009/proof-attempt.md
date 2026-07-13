# THM-M-1009 proof-phase implementation

Item: `S56-M-1009-PROOF`

Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

Attempt date: 2026-07-13

## Implemented route

This attempt supersedes the earlier blocked attempt. `Proof.lean` now imports
the exact definitions and target from `Statement.lean` and proves the frozen
`ErdosRenyiLowerBoundTarget` without an added premise.

The local proof builds the finite indicator count and checks its first and
second moments. A finite Cauchy-Schwarz estimate bounds the squared first
moment by the measure of its support times the second moment. Applying this to
initial segments gives the finite ratio bound, including the zero-denominator
case fixed by ordinary real division.

For a fixed index `m`, the same estimate is applied to the window `[m,n)`. The
window square is bounded by the full initial-segment square, yielding

```text
eventMassRatio n <= measure(eventTail m) + 2 * partialEventMass m / partialEventMass n.
```

The divergence hypothesis sends the error to zero. The ratio is globally
nonnegative and at most one, so its filter limsup is bounded by every tail
measure. Finally, continuity from above and the checked identity between the
intersection of the tails and `limsup A atTop` give the exact root inequality.

## Status boundary

The exact frozen root has a repo-local, placeholder-free proof body that
elaborates in the pinned Lean environment. This supports only a provisional
worker proposal for `M0-L` and item state `[_]`. The frozen architecture files
truthfully retain their pre-proof open state. Master acceptance, H0/R0,
transitive provenance and trust review, hermetic replay, independent
verification, validation, release, and theorem completion remain open.

Exact commands and results are recorded in `proof-validation.md`; the
node-specific provisional receipt is `proof-receipt.json`.
