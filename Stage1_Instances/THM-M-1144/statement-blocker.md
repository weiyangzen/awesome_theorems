# Exact-statement gate: blocked

Item: `S56-M-1144-STATEMENT`  
Theorem: `THM-M-1144`  
Base revision: `c37f5c9477ecee2c5ecf444e75e52be738eff1a8`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository's source record. The only
mathematical wording is the title "gradient estimate for harmonic functions" and the gloss "a
bound on derivatives of harmonic functions." The record names no primary source, theorem, page,
or precise estimate. The untrusted `已验证` metadata is not source evidence.

The wording does not determine any of the choices needed to identify one proposition:

- Euclidean space, a Riemannian manifold, or another domain, and its dimension;
- real-, complex-, or vector-valued functions and the definition of harmonicity;
- first derivative versus derivatives of arbitrary order;
- a pointwise gradient norm, a supremum norm, or an integral estimate;
- a ball, a general domain, an interior subdomain, or boundary-distance conditions;
- whether the right side uses an `L∞`, `Lᵖ`, oscillation, or positive-function bound;
- the radius power, dimensional constant, normalization, and boundary assumptions.

Standard estimates making different choices above are not definitionally or mathematically
equivalent. In particular, selecting a ball estimate of the form
`‖fderiv ℝ u x‖ ≤ C / r * sup ...`, a positive-harmonic-function estimate involving `u x`, or a
higher-derivative estimate would invent a theorem not fixed by the source. Degenerate cases such
as zero radius, dimension zero, an empty domain, and constant functions likewise cannot be
mutation-tested until a formulation has been selected.

The legacy-priority number `142` is not a target-specific artifact: the file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_142.lean` identifies itself as
`THM-M-1314`, the Penrose inequality. The rev-5.6 manifest assigns `THM-M-1144` no legacy slot.
It therefore supplies no statement candidate or credit.

Consequently section 5 fails before minimal target imports, canonical elaboration, expression
serialization, checked alternate encodings, or the required removed-hypothesis, changed-domain,
binder-scope, and boundary mutations can exist. No canonical declaration, `sorry`, axiom,
placeholder, abstract theorem interface, weakened special case, or broadened substitute was
introduced. Machine debt remains `M4`; statement acceptance, audit completion, and theorem
completion are false.

## Pinned environment and narrow evidence

Validation ran on 2026-07-12 (Asia/Shanghai) inside this worker clone, using the existing canonical
`.lake` artifacts read-only. No update, build, clone, or fetch command was used.

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
| `python3 scripts/stage1_target.py show THM-M-1144` | 0 | Rank 349, planned, no accepted legacy artifact, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision above |
| repository search for the Chinese/English title, gloss, target ID, and gradient/harmonic terms | 0 | Found only underspecified metadata/intake records and unrelated harmonic-function infrastructure; no source-frozen proposition |
| pinned-mathlib search for harmonic gradient/derivative estimates | 0 | Found harmonicity and derivative infrastructure but no result that identifies the unspecified source claim |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1144/StatementInfrastructureProbe.lean` | 0 | Elaborated `InnerProductSpace.HarmonicAt`, `HarmonicOnNhd`, `HarmonicOnNhd.contDiffOn`, `fderiv`, and `Metric.ball`; substrate only |

The probe deliberately imports only
`Mathlib.Analysis.InnerProductSpace.Harmonic.Basic`. It is substrate evidence, not a canonical
statement and not evidence that this import would be minimal for the unidentified target.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, check relevant errata, and freeze every domain, codomain, harmonicity, derivative,
norm, region, radius, constant, and boundary convention listed above. A later statement run can
then transcribe that claim exactly, minimize pinned imports, serialize its elaborated expression
and environment, and execute all four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
