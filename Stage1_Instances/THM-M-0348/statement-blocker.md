# Exact-statement gate: blocked

Item: `S56-M-0348-STATEMENT`  
Theorem: `THM-M-0348`  
Base revision: `c9694802ae049af37973e49a65f11b833135333f`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record gives only the Chinese title `里斯-费耶尔定理`, the gloss `傅里叶级数的收敛性`
("convergence of Fourier series"), the names Marcel Riesz and Lipot Fejer, and the year 1923. It
does not give a primary-source edition, theorem/page, exact wording, definitions, or hypotheses.

Those fields do not decide among ordinary Fourier partial-sum convergence, Cesaro/Fejer
summability, Riesz summability, pointwise, uniform, almost-everywhere, weak, or norm convergence.
They do not fix the periodic domain, coefficient normalization, scalar field, function class,
summation operator, topology, exponent range, exceptional set, or boundary cases. The paired name
is also close to the distinct Fejer-Riesz factorization theorem for nonnegative trigonometric
polynomials. These readings are not interchangeable.

Selecting any convenient member of these families would broaden, weaken, or substitute the
repository theorem. Consequently the exact-human-claim gate fails before minimal imports, an
elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutations can be produced. No theorem declaration,
placeholder, axiom, assumed convergence interface, or substituted special case was introduced.
Machine state remains `M4`; statement acceptance and theorem completion remain false.

## Pinned environment and validation

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. Existing `.lake` artifacts were used read-only; no update,
build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0348` | 0 | Rank 841, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese/English title and exact gloss | 0 | Found only the underspecified metadata and this intake dossier; no source-frozen proposition |
| pinned-mathlib `rg` search for Riesz/Fejer named means, summability, or factorization | 1 | No match; exit 1 means no matching text |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0348/IntakeProbe.lean` | 0 | Existing bounded probe elaborated representative Fourier, Cesaro, and Laurent APIs; it is not a canonical target |

There is no applicable `lake env lean <canonical-statement>.lean` check: the source record does not
identify an exact expression. Elaborating one of the candidate readings would be fake statement
evidence rather than the assigned deliverable.

## Retry condition

An accountable review must preserve an immutable primary or authoritative source edition, select
and transcribe its exact theorem and incorporated definitions, audit errata and attribution, and
independently approve the mapping. It must explicitly resolve the convergence/summability versus
factorization boundary and freeze every domain, binder, hypothesis, convention, topology, and
degenerate case listed above. A later statement run can then minimize imports, fingerprint the
elaborated expression, check alternate transports, and run all required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
