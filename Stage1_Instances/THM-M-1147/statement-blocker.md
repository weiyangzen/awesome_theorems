# Exact-statement gate: blocked

Item: `S56-M-1147-STATEMENT`  
Theorem: `THM-M-1147`  
Base revision: `3727de2a4ceed9cd590d437f2e2e51c1a2e7c172`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository source record. The entire
mathematical wording is `调和函数的反演` ("inversion of harmonic functions") under the title
"Kelvin transform". The record supplies no primary source, edition, theorem/page, exact formula,
or assumptions. The metadata value `已验证` is not source or kernel evidence.

The wording does not determine the data needed to identify one proposition:

- the dimension, scalar codomain, Euclidean space or other ambient domain, and harmonicity notion;
- the inversion center and radius, the original domain, and exclusion of the inversion center;
- whether the result is preservation of harmonicity or an exact Laplacian covariance identity;
- the transform's norm power and radius normalization, including the dimension-two convention;
- the differentiability and domain hypotheses and the conclusion's image/inverted domain;
- treatment of zero, empty or disconnected domains, and any removable-singularity or infinity case.

These choices give inequivalent statements. For example, the familiar unit-centered formula
`x |-> |x|^(2-n) * u (x / |x|^2)` in dimension at least three is not the same statement as the
unweighted two-dimensional transform, a radius-`R` transform, a transform about a nonzero center,
or a Laplacian covariance formula. Selecting any one merely because it is standard would broaden
the source phrase by inventing missing mathematics. Meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations likewise cannot be defined before those choices are frozen.

The intake dependency records this ambiguity and explicitly declines to adopt its candidate shape.
A repository and pinned-mathlib name search found no target-specific Lean declaration that could
supply missing source identity; in any event, a library declaration could not select among the
unresolved human claims without a checked source crosswalk.

Consequently rev-5.6 section 5 fails at canonical human-claim identity, before minimal imports,
elaboration, expression serialization, checked transports, or mutation tests. No canonical
declaration, `sorry`, axiom, placeholder, weakened special case, or substitute theorem was added.
Machine debt remains `M4`; statement acceptance, audit completion, and theorem completion are
false.

## Narrow validation evidence

Commands ran on 2026-07-12 (Asia/Shanghai) inside this worker clone. The canonical `.lake` directory
was used read-only; no update, build, clone, fetch, or dependency mutation was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1147` | 0 | Rank 352, planned, no accepted legacy artifact, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision above |
| repository search for the target ID, Chinese/English title, and source gloss | 0 | Found only the underspecified metadata, generated scheduling records, and intake dossier |
| pinned-mathlib search for `Kelvin transform` naming variants | 1 | No named candidate; negative name search only, not an exhaustive anchor audit |

## Retry condition

An accountable source reviewer must identify an immutable primary-source edition and exact
theorem/page, check relevant errata, and freeze the dimension, codomain, harmonicity predicate,
inversion center/radius, domain mapping, weight, regularity, conclusion, and boundary conventions.
A later statement run can then transcribe that exact claim, minimize its pinned imports, serialize
the elaborated expression and environment fingerprint, and execute all four required mutation
classes.

The first failed gate is exact source-statement identity. The assigned phase is not genuinely
self-tested to its completion gate, so no `.stage1-worker-selftest.json` is emitted.
