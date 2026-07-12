# Exact-statement gate: blocked

Item: `S56-M-1068-STATEMENT`  
Theorem: `THM-M-1068`  
Base revision: `4344dc4263d0bcc8c386ec0ae1ad4e508c910b1e`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
entire mathematical claim supplied by `Docs/researches/math_theorems.md` and
`Docs/Stage0_Blueprint.md` is the name "Tanaka's formula" and the gloss "the Ito formula for
reflected Brownian motion". Neither record gives a formula, definitions, hypotheses, bibliography,
theorem/page locator, or normalization. The intake accordingly leaves the canonical variant open.

The gloss does not uniquely determine a proposition. At minimum it leaves unresolved:

- the positive-part, negative-part, or absolute-value identity, versus a reflected-Brownian or
  Skorokhod consequence;
- Brownian motion versus a general real continuous semimartingale;
- local time at zero versus an arbitrary level, and right, left, or symmetric normalization;
- the sign value at zero and strict versus non-strict indicator in the stochastic integrand;
- initial-value and initial-local-time terms;
- fixed-time almost-sure equality versus one null set supporting an identity for all times; and
- the filtration, adaptation, continuity, measurability, and stochastic-integrability assumptions.

These choices change domains, ordered binders, hypotheses, coefficients, and conclusions. The
historical 1963 paper and Revuz--Yor references listed by the intake are explicitly uninspected
discovery candidates. Selecting one formula from general mathematical knowledge would invent the
missing source decision; encoding an abstract stochastic-integral/local-time interface with the
desired equality as a field would assume the conclusion. Neither is exact-statement evidence.

The pinned mathlib source also contains no `Tanaka`, local-time, semimartingale, stochastic-integral,
or quadratic-variation API match. That API gap is not itself a license to substitute a weaker
deterministic formula or an uninterpreted proposition. Because the canonical human claim fails
first, minimal imports, expression serialization, checked alternate transports, and meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations cannot be produced.

No Lean declaration, axiom, placeholder, `sorry`, broadened theorem, or special-case substitute was
added. Machine state remains `M4`; statement acceptance, audit completion, and theorem completion
are false.

## Pinned environment and validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` directory is
linked into the clone and was read only; no update, build, clone, or fetch command was run.

- Lean toolchain file: `leanprover/lean4:v4.29.0`.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1068` | 0 | Rank 510, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| repository `rg` search for `THM-M-1068` and Tanaka's formula | 0 | Found only the underspecified source metadata and this intake dossier; no frozen formula or Lean target |
| `cd Formalizations/Lean && rg -n -i 'Tanaka\|local[ _-]?time\|semimartingale\|stochastic[ _-]?integral\|quadratic[ _-]?(variation\|covariation)' .lake/packages/mathlib/Mathlib` | 1 | No matching pinned-mathlib source (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check: the exact expression required to create
that file is the missing artifact. Elaborating a fabricated interface would conceal rather than
validate the blocker.

## Retry condition

An accountable source review must pin an immutable primary-source edition and exact theorem/page,
transcribe the displayed formula and all assumptions, dispose of errata, and freeze every variant,
normalization, indicator/sign, initial-term, filtration, and almost-sure quantifier choice listed
above. It must also explain whether the repository's reflection wording selects the root theorem or
a checked consequence. A later statement run can then encode that exact proposition, identify or
construct its concrete stochastic-calculus API, minimize imports, serialize the elaborated
expression and environment, compile alternate-form transports, and run the four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
