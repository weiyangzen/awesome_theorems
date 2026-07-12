# THM-M-0032 anchor audit

Item: `S56-M-0032-ANCHOR_AUDIT`

Cutoff: 2026-07-13 07:19:19 +08:00

## Result

No placeholder-free Lean 4 proof of the frozen unrestricted target was located in the bounded
inventory. The accepted machine status therefore remains `M3`, not `M0` or `M1`.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the premise and
conclusion interfaces plus useful intermediate routes: regular-local definitions and transports,
Kaplansky's prime-ideal criterion, the prime-ideal-to-PID theorem, and PID-to-UFD. It does not
provide the missing implication from `IsRegularLocalRing R` to any of those sufficient UFD
hypotheses. The only theorem in `RegularLocalRing/Defs.lean` involving principal ideal rings points
the other way: local domain plus PID implies regular local. The checked audit probe also confirms
that `UniqueFactorizationMonoid R` is not synthesized from `[CommRing R]
[IsRegularLocalRing R]`.

The public search found a highly relevant but invalid external anchor. At immutable revision
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`, both
`PowerSeriesUFD.regularLocalRing_isUFD` and `auslander_buchsbaum_UFD` conclude
`UniqueFactorizationMonoid R`. Each adds `[IsDomain R]`, which pinned mathlib cannot derive from
the frozen premise, and each terminal body is literally `by sorry`. They are `M5_placeholder`
statement leads only. Their dependent power-series theorems do not furnish independent proof
bodies.

The topic-specific `JarodAlper/RegularLocalRings` project was inspected at immutable revision
`ea5a55ef4d5ce3618aea38376981c5a5eb33b7f0`. It proves a domain consequence and a
dimension-one DVR result under its own older regular-local class, Lean 4.23.0-rc2, and mathlib
revision `088f81e7d32006ca653ff4dd72226d1926ab0015`. Its complete three-file source scan contains no
`UniqueFactorizationMonoid`, UFD, or unrestricted principal-ideal conclusion. It is partial
infrastructure, not a root proof.

The external responses and immutable source hashes are recorded in `anchor-audit.json`. Public
discovery is deliberately bounded: authenticated GitHub code search returned HTTP 401 and
grep.app returned HTTP 503. These are access failures, not evidence of global absence.

## Candidate boundary

| Candidate | Exact role | Classification | Decision |
|---|---|---|---|
| pinned mathlib regular-local, Kaplansky, prime-ideal, and PID APIs | support, no terminal target | `M3_support_only / E3` | retain for later obligation design |
| Atlas `regularLocalRing_isUFD` | strengthened target with `[IsDomain R]`; body `by sorry` | `M5_placeholder / E3` | reject as proof anchor |
| Atlas `auslander_buchsbaum_UFD` | duplicate strengthened target; body `by sorry` | `M5_placeholder_duplicate / E3` | reject and deduplicate |
| `JarodAlper/RegularLocalRings` | domain and one-dimensional results under an incompatible earlier class | `M3_partial_support / E3` | no root integration |
| Formal Conjectures immutable tree | no matching path in 1204 entries | no candidate | nothing to integrate |

No candidate qualifies as `M1`: the audit found no independently reproducible upstream
placeholder-free proof. Consequently there is no repo-local integration debt to conceal. The
remaining debt is formalization debt for the exact theorem.

## Source boundary

The primary statement locator remains Auslander and Buchsbaum, *Unique Factorization in Regular
Local Rings*, PNAS 45(5), Theorem 5, page 734 (May 1959). Stacks tag `0AG0` is a modern
cross-check. This machine-anchor phase does not resolve the incorporated definitions, Nagata
reduction, complete assumptions/errata crosswalk, the catalog's 1958 date discrepancy, or
independent review. Human status remains `H1`; readability remains `R4`.

## Status boundary

The five-record frozen inventory is classified and locally self-tested pending master acceptance.
This is not `AUDIT-Z`: the obligation registry, full proof/provenance/trust graphs, proof body,
readable reconstruction, hermetic replay, independent validation, and release gates remain open.
No theorem completion or accepted state is claimed.
