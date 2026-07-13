# THM-M-0995 obligation registry and typed graphs

Registry version 2 preserves the exact statement and the full version-1 denominator history. It
corrects one proof-architecture defect discovered during execution: version 1 required
`OptimizeExponentPackage`, but that interface is false at `v = 0`, `b = 1`, `t = 1`. The local
kernel theorem `Proof.not_optimizeExponentPackage` supplies the counterexample. The append-only
delta retires that ID, replaces the terminal assembly ID, and adds the missing positive-variance,
zero-variance, scalar-series, and finite-prefix semantic nodes. No theorem target was weakened.

## root
The exact bounded independent-summand upper-tail Bernstein target is provisionally machine-closed
by `Proof.bernsteinInequality_via_registry_v2`.

## s-exact
The checked statement preserves every binder, hypothesis, non-strict event, constant, and
totalized division boundary.

## l-exp-remainder
Expand `exp x - 1 - x` as its power-series tail, bound `2 * 3^n` by `(n+2)!`, dominate by the
geometric series with ratio `abs x / 3`, and weaken `abs x <= c` in the positive denominator.

## l-ind-mgf
Apply the scalar remainder pointwise to `s * X_i`, integrate the bound, cancel the centered linear
term, identify the second moment with the variance, and use `1 + y <= exp y`.

## t-ind-mgf
`individualMGF_compose` checks the exact scalar-to-individual-MGF child composition.

## l-prefix-mgf
Truncate the process outside `range n`, preserve independence and a.e. measurability, and apply
mathlib's whole-family finite-set MGF product theorem.

## l-sum-mgf
Bound every product factor, turn the product of exponentials into an exponential of a sum, and
apply the frozen variance budget through the positive tilt denominator.

## t-sum-mgf
`sumMGF_compose` checks the exact individual/prefix-to-sum-MGF child composition.

## l-chernoff
Bound the partial sum almost surely to obtain exponential integrability, then specialize mathlib's
exponential Markov inequality to the exact event.

## l-optimize-pos
For positive variance, the denominator is positive, the chosen tilt is nonnegative and strictly
inside `s*b < 3`, and field normalization proves the exact exponent comparison.

## l-var-zero-ae
If the variance budget is zero, nonnegativity forces every summand variance to zero. The zero-mean
variance characterization makes every prefix summand zero almost everywhere, hence so is the sum.

## b-zero-denom
When the displayed denominator is zero, totalized division makes the right side one and the
probability-measure bound closes the branch.

## b-var-zero
At threshold zero use the probability bound. At positive threshold the almost-everywhere zero sum
makes the tail event null.

## t-var-zero
`zeroVariance_compose` checks the zero-denominator and almost-everywhere-zero branch composition.

## b-empty
The empty prefix is retained inside the statement boundary and has sum zero.

## t-assemble-v2
Split exhaustively on `varianceBudget = 0`. The zero branch consumes `B-VAR-ZERO`; the positive
branch consumes the sum MGF, Chernoff, and positive-variance optimizer packages.
`root_compose_v2` checks the exact child-to-root composition.

## x-mathlib
Mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies supporting exponential
series, variance, independence, MGF, and Chernoff declarations. It is not counted as an exact
Bernstein terminal body.

## x-external
HighDimProb revision `8d4eec8bc06d80e8436ab3505000fca999b46546` remains a mismatched anchor and
supplies no proof credit.

## x-source
Primary-source pinpointing, errata review, H0 reconstruction, and independent review remain open.

## x-tcb
Release-grade transitive dependency, executable, platform, SBOM/license, cold-build, and
independent-verification work remains open.

## x-v1-refutation
`Proof.not_optimizeExponentPackage` is the kernel-checked counterexample that triggered the
registry-v2 correction; it supplies audit evidence but no positive root proof credit.

## Closure boundary

All sixteen machine-required registry-v2 obligations have local or checked imported proof bodies,
and the exact root is provisionally `M0-L`. This proof-phase result is not theorem completion:
human-source, readable reconstruction, full trust/provenance, hermetic validation, independent
replay, release, and master-acceptance gates remain open. Registry-v1's denominator and failed
optimizer ID remain reportable in `obligation-registry.json`.
