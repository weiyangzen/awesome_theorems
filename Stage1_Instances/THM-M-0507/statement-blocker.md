# Exact-statement gate: blocked

Item: `S56-M-0507-STATEMENT`

Theorem: `THM-M-0507`

Base revision: `aa55669bb59986e08ea8a0d1d77a1e40343d8142`

## Decision

The exact Lean 4 target cannot be truthfully selected from the authoritative repository material.
The only source wording is `堆垒数论的基本方法` ("a fundamental method of additive number
theory"). This names a proof method, not a proposition with ordered binders, hypotheses, and a
conclusion. The accepted intake dependency consequently keeps the canonical claim and formal target
null and records the ambiguity explicitly.

The missing choices are mathematically constitutive. A statement would have to select a Waring,
Goldbach, partition, or other representation problem; define its counting function and domains;
fix the number of summands, weights, limiting regime, local conditions, main-term normalization,
uniformity, and error term; and specify all boundary cases. These choices lead to inequivalent
theorems. Choosing a familiar application would broaden or substitute the repository target.
Likewise, packaging desired major/minor-arc estimates as assumptions and projecting the result
would hide the missing theorem in hypotheses.

The first failed gate is therefore exact source-statement identity. Without it, this phase cannot
freeze a canonical declaration or elaborated-expression hash, prove minimality of imports, check
alternate-encoding transports, or run meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutations. Machine debt remains `M4`; no statement or proof credit is claimed.

## Pinned Lean boundary

The existing pinned environment provides `AddCircle`, its normalized Haar measure, Fourier
characters, Fourier coefficients, and an interval-integral formula through
`Mathlib.Analysis.Fourier.AddCircle`. The intake's `IntakeProbe.lean` elaborates these APIs. They are
possible infrastructure for some circle-method statements, but they neither choose nor express the
missing source theorem. The probe is therefore substrate evidence only, and its import cannot be
certified as the minimal import for an unresolved target.

The environment is Lean 4.29.0 (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`), Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and `lake-manifest.json`
SHA-256 values are `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The canonical `.lake`
artifacts were used read-only; no update, build, clone, or fetch was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0507` | 0 | rank 881; planned; legacy artifacts unaccepted; theorem incomplete |
| `rg -n -C 10 'THM-M-0507\|哈代-李特尔伍德圆法\|堆垒数论的基本方法' Docs Stage1_Instances Formalizations` (with generated authorities and this dossier excluded) | 0 | only method-level metadata and explicitly open Stage0 fields found; no proposition found |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 and the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0507/IntakeProbe.lean` | 0 | all six circle/Fourier substrate API checks elaborated and printed their types |
| `python3 -m json.tool Stage1_Instances/THM-M-0507/statement-blocker.json` | 0 | structured blocker is valid JSON |
| scoped forbidden-declaration scan of Lean artifacts | 1 | expected no-match result; no proof-gap declaration or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0507` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must pin and approve an immutable edition and exact theorem/page,
including assumptions and errata. The statement phase can then freeze the representation problem,
all conventions and boundary cases, elaborate the source-faithful target with minimized imports,
serialize its expression, check any transports, and perform the required mutations.

Because the assigned statement phase is not genuinely self-tested to completion, no
`.stage1-worker-selftest.json` is emitted.
