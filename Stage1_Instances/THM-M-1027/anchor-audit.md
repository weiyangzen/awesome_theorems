# Immutable Lean anchor audit

The frozen target is
`Stage1Instances.THM_M_1027.WienerExistenceTarget`. This audit was performed on
2026-07-12 and is limited to candidate discovery, immutable identification,
statement comparison, and the narrow checks available in the existing pinned
workspace. It supplies no theorem-completion credit.

## Candidate ledger

| Candidate | Immutable identity | Exact surface | Result |
|---|---|---|---|
| Repo-local legacy file | repository base `937d8467b6060fe4128f6ddd0b930b16ba7bd6e6` | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_218.lean`, `StatementShape` | `M3`: statement/interface discovery only; the shape adds Gaussian-process and adaptedness fields and has no existence proof |
| Pinned mathlib | `8a178386ffc0f5fef0b77738bb5449d50efeea95` | Gaussian laws/processes, `HasIndepIncrements`, and Kolmogorov-process APIs listed in `anchor-audit.json` | `M3`: useful infrastructure, but no Brownian/Wiener construction or exact terminal theorem was found |
| `RemyDegenne/brownian-motion` | tag `v4.29.0`, peeled commit `fdcef67f41b51b7635b3c2d08eb61768604f8f74`, source blob `4ebeae388f3ed11876b0307ed4b74e99516cd81d` | `BrownianMotion.Gaussian.BrownianMotion`; `brownian`, `IsBrownian_brownian`, measurability, continuity, Gaussian-law, independent-increment, and Wiener-measure declarations | `E3 / M3`: credible exact construction candidate, but not a local dependency and not independently replayed or transitively trust-audited |

The external `v4.29.0` tag matches the local Lean `v4.29.0` and mathlib
`8a178386...` pins. Its manifest additionally pins
`kolmogorov_extension4@e8d02e83550f893bbf48f0b651f782eccf6760e8`.
The inspected construction declarations have explicit bodies and no placeholder
token, but that narrow source inspection is not a transitive placeholder,
axiom, provenance, or TCB audit. Under rev-5.6, exact source identification is
only `E3`; it cannot be promoted to `M1` without an independently reproducible
upstream kernel check.

## Statement comparison

The external process is indexed by `NNReal`, is coordinate-measurable and
everywhere continuous, has law `gaussianReal 0 t` at time `t`, has symmetric
increment law with variance `max (s-t) (t-s)`, and has independent increments.
For ordered `s <= t`, its subtraction law with arguments reversed has the
frozen target's variance `t-s`. The zero-time Gaussian evaluation must be
transported to an almost-sure zero start. `AnchorAudit.lean` checks the exact
component-to-root composition contract without pretending that the unavailable
external declarations were imported.

## Integration blocker

`BrownianMotion.Gaussian.BrownianMotion` is absent from this repository's Lake
closure, so the literal import probe fails with `unknown module prefix
'BrownianMotion'`. This worker cannot edit shared Lake configuration or fetch a
dependency. A later integration phase must pin the peeled external commit and
its `kolmogorov_extension4` dependency, instantiate the checked bridge, inspect
the terminal/transitive bodies and axioms, and run the exact wrapper through the
kernel. Until then the root remains `M3`, not `M1` or `M0-P`.

Exact validation commands and results are in `anchor-validation.md`.
