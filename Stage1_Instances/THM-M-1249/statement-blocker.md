# Exact-statement gate: blocked

Item: `S56-M-1249-STATEMENT`

Theorem: `THM-M-1249`

Base revision: `c370639c4481be6bdcec40b9aa3553046d6f7572`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the title `分布理论` ("distribution theory") and the gloss
`广义函数的理论` ("the theory of generalized functions"). This names a mathematical subject, not
a proposition. The record supplies no primary-source theorem, page, literal statement, ordered
binders, hypotheses, or conclusion.

Turning the label into a theorem would require choices that the source record does not make:

- whether the target is the definition of a distribution, differentiation by transposition, the
  embedding of locally integrable functions, a support result, or another theorem in the theory;
- the open domain and its finite-dimensional ambient real vector space;
- the test-function differentiability order and topology;
- real- or complex-valued test functions and the codomain/scalar structure;
- any local integrability, differentiability, support, or boundary hypotheses;
- the exact conclusion and its quantifier order.

These choices produce inequivalent claims. In particular, mathlib's `Distribution` type is an
abbreviation for continuous linear maps from smooth compactly supported test functions, but merely
checking that type would formalize a definition rather than elaborate a theorem stated by this
metadata. Selecting a derivative theorem or a regular-distribution embedding would instead
substitute one convenient result from a much larger theory. Both moves violate the rev-5.6 exact
statement rule.

Consequently the canonical human claim fails before minimal theorem imports, an elaborated target
fingerprint, checked transports, or meaningful hypothesis/domain/scope/boundary mutations can be
established. No declaration, weakened special case, broadened conjunction, or assumed interface
was introduced. Machine state remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and narrow check

Validation date: 2026-07-12 (Asia/Shanghai). Commands ran inside this worker clone. The existing
canonical `.lake` artifacts were used without update, build, clone, or fetch operations.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

`StatementProbe.lean` uses the single direct import
`Mathlib.Analysis.Distribution.Distribution` and checks the nearest pinned substrate types,
`Distribution` and `TestFunction`. This is deliberately not presented as a canonical target.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1249` | 0 | rank 429, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1249/StatementProbe.lean` | 0 | the pinned `Distribution` and `TestFunction` substrate types elaborated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository search for the Chinese title/gloss and their English translations | 0 | found only the same subject-level metadata and this dossier; no source-frozen proposition |
| pinned-mathlib file/symbol search for distributions and test functions | 0 | located the general distribution API, but cannot select a theorem absent a source proposition |

There is no applicable exact-target Lean check: the target expression does not exist. The probe is
only honest negative-boundary evidence that the pinned environment contains relevant definitions;
it cannot resolve source-statement identity.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, including assumptions and any errata, and explain why that proposition represents
this target rather than the separately scheduled Schwartz-space, support, convolution, or
fundamental-solution targets. It must freeze all domain, topology, scalar, differentiability,
binder, hypothesis, conclusion, and degenerate-case choices listed above. A later statement run can
then encode the exact expression, minimize its imports, fingerprint elaboration, add checked
transports, and execute structural mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
