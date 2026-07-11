# THM-M-1138 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the maximum principle for harmonic
functions. The source catalogue's `verified` label is discovery metadata only and supplies no
proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Weak maximum principle: a real-valued function continuous on the closure of a nonempty bounded domain, harmonic in the domain, is bounded above there by its boundary maximum | Precise Lean topology, boundary API, and elaborated expression belong to the statement phase |
| Domain | A nonempty bounded connected open subset of a finite-dimensional real Euclidean space | Whether connectedness is redundant for the weak form must be decided without weakening the source claim |
| Regularity | Continuity on the closure and harmonicity on the interior | No classical differentiability or mean-value encoding is yet selected |
| Boundary conclusion | `u x <= max_{y in frontier Omega} u y` for `x` in the closure (equivalently, the maximum on the closure occurs on the boundary) | Existence of the maximum needs compactness and nonempty-boundary side conditions |
| Related results | Minimum principle by applying the result to `-u`; strong maximum principle; mean-value property | These are transports or dependencies, not part of the root; THM-M-1140 separately owns the strong principle |
| Foundations | Lean 4 kernel and pinned mathlib | Toolchain, imports, classical/choice use, and environment fingerprint remain open |

The catalogue phrase alone is ambiguous between weak and strong forms. The separate adjacent target
THM-M-1140 (`strong maximum principle`) and the catalogue gloss `maximum principle for harmonic
functions` fix this intake's root to the weak boundary-maximum form. The statement phase must still
freeze a faithful Lean encoding and mutation-test boundedness, continuity, harmonicity, nonemptiness,
and boundary cases.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact-statement gate: no canonical Lean declaration, normalized expression hash, checked
transports, or environment fingerprint exists. This intake does not claim a Lean proof or theorem
completion.

Validation commands and their results are recorded in `validation.md`.
