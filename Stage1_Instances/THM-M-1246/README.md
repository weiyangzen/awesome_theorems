# THM-M-1246 rev-5.6 intake

This is a `planned` dossier for the Euclidean differential `L2` Hardy inequality. The Stage0 phrase
"singular-weight integral inequality," its PDE category, and its 1920 attribution do not uniquely
identify a Hardy inequality. This intake therefore makes the selected variant explicit rather than
silently treating the discrete or one-dimensional integral variants as interchangeable.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Sharp `L2` inequality on `R^n`, `n >= 3`, for real smooth compactly supported `u` | A mathematical scope freeze, not an elaborated Lean expression |
| Singular term | `|u(x)|^2 / |x|^2`, interpreted almost everywhere | The value at zero and integrability encoding remain statement obligations |
| Energy term | Integral of the squared Euclidean gradient norm | Fréchet derivative/gradient transport is not yet chosen |
| Constant | Sharp constant `4/(n-2)^2` | Natural-to-real coercions and division side conditions remain open |
| Function space | Smooth compact support | No extension to Sobolev completion or boundary domains is included |
| Exclusions | Discrete sequence, averaging-operator, one-dimensional, fractional, boundary, and Rellich inequalities | Any such result is only a possible lemma or analogue, never root proof credit |
| Foundations | Lean 4 kernel and a pinned mathlib environment | Exact imports, toolchain fingerprint, and trust inventory remain open |

## Intake verdict

The lifecycle is `planned` and the provisional root vector is `[H2, M4, R3]`. The source family is
identified, but the repository supplied no primary pinpoint for this exact variant and no immutable
source receipt was created. The first failed gate is the exact Lean statement gate: there is no
module, declaration, normalized expression hash, environment fingerprint, or mutation evidence.
The theorem is not complete.

Validation evidence and exact command outcomes are recorded in `validation.md`.
