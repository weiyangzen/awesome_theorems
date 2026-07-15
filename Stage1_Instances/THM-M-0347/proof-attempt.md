# Superseded proof-phase attempt

This historical attempt predates the immutable ATLAS candidate now integrated
by `AtlasFourierSeries.lean` and `Proof.lean`. Its negative conclusion was
correct for the pinned mathlib and external candidates examined at that time,
but it is no longer the current proof verdict. See `proof-validation.md` and
`proof-receipt.json` for the exact root wrapper, provenance, validation, and
open acceptance/license boundaries.

## Outcome

`S56-M-0347-PROOF` remains blocked. The pinned mathlib API proves uniform convergence of the
bilateral Fourier series only under `Summable (fourierCoeff f)`. `Proof.lean` now supplies two
placeholder-free kernel-checked bodies: convergence of the symmetric partial sums under that
hypothesis, and convergence of the exact frozen Fejer means by Cesaro averaging. These are useful
bridge results, but the added summability premise is not available for an arbitrary continuous
function and therefore neither theorem is substituted for `FejerTheoremTarget`.

The first unresolved root cut is the frozen analytic chain `M0347-N-CONVOLUTION` through
`M0347-L-ESTIMATE`, especially the unrestricted Fejer-kernel concentration/approximate-identity
estimate. No exact proof body for that chain exists in the pinned dependency closure found by the
completed anchor audit. The proof task is not self-tested as complete, so no root
`.stage1-worker-selftest.json` is written and no theorem-completion claim is made.

## Validation

Base revision: `7780ee2963f599a6bf06f39a12c6fddb7eafc914`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-0347` | 0 | Rank 840; planned; theorem complete false. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0347/Proof.lean` | 0 | Both local bodies elaborated; each axiom profile is exactly `propext`, `Classical.choice`, `Quot.sound`; no `sorryAx`. |

Status boundary: partial proof progress only. The exact unrestricted root remains open, so this
artifact is blocker evidence rather than a proof-phase completion receipt.
