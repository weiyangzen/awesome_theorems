# Scope map

## Frozen repository boundary

The literal repository claim is "Hardy-space multipliers" under the label "Herz-Stein theorem".
The intake freezes that wording without treating it as a unique mathematical statement. It does
not silently replace the claim by the Fourier multiplier construction already present in mathlib.

## Parameters requiring source selection

| Surface | Must be fixed by the exact source | Current intake state |
|---|---|---|
| Ambient object | Euclidean space, torus, locally compact group, or another setting | open |
| Hardy space | real-variable, boundary/holomorphic, atomic, maximal-function, or distributional model | open |
| Exponent | exact range for `p`, including endpoints | open |
| Multiplier | Fourier transform convention and multiplier/operator definition | open |
| Hypotheses | smoothness, difference, integral, support, homogeneity, or size conditions | open |
| Conclusion | bounded endomorphism, mapping between spaces, norm estimate, or characterization | open |
| Constants | dependencies and normalization | open |
| Boundary cases | zero multiplier/function, dimension, endpoint exponents, distribution representatives | open |

## Provisional formalization surfaces

The pinned library exposes Schwartz functions, tempered distributions, Fourier transforms,
`SchwartzMap.fourierMultiplierCLM`, and generic `MeasureTheory.Lp`/`MemLp`. These are discovery
ingredients only. A scoped repository/mathlib search found no named Hardy-space definition or
Herz-Stein root theorem. The later statement phase must determine whether additional definitions
are required and must elaborate and mutation-test the exact proposition.

Out of scope for this intake are a proof, an obligation registry, an external-anchor conclusion,
and any claim that a Schwartz-space multiplier result transports to the unresolved Hardy space.

## Profiles

Lean 4 dependent type theory and pinned mathlib are the intended foundation. Classical logic,
choice, noncomputability, quotient/distribution representations, and analytic normalization are
not yet fixed. No numerical experiment, oracle, unchecked certificate, or source-label status is
credited.

