# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `不确定性原理`, attributes it to Werner Heisenberg, dates
it to 1927, and gives only `函数与其傅里叶变换不能同时集中` ("a function and its Fourier
transform cannot both be concentrated"). Stage0 repeats the gloss and leaves exact definitions,
hypotheses, equivalent statements, axioms, and artifacts open. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted`.

This metadata provides neither a bibliographic edition/page nor a mathematical definition of
"concentrated". It also does not distinguish the harmonic-analysis theorem family from the
separate quantum-mechanical entries elsewhere in the repository.

## Candidate source work

An authoritative primary or standard reference must be selected during source audit. The accepted
record must identify edition, theorem/section and page, all assumptions, Fourier normalization,
proof boundary, equality cases, and errata, followed by independent review. Merely attaching a
standard Heisenberg inequality to the historical attribution would not establish that it is the
repository's intended exact statement.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "function" | `L2`, integrable, Sobolev, or Schwartz function on `ℝ`/`ℝ^n` | `MeasureTheory.Lp`, `MemLp`, or `SchwartzMap` | pinned APIs probed; exact domain open |
| "Fourier transform" | integral, `L1`, `L2`, or Schwartz transform | `Real.fourierIntegral`, `Lp.fourierTransformₗᵢ`, or Schwartz Fourier API | pinned APIs probed; convention open |
| "concentrated" | variance, support size, mass outside sets, or entropy | source-specific moments, support/measure, integrals, or entropy | absent from source record |
| "cannot both" | positive lower bound, quantitative tradeoff, or zero-function rigidity | exact inequality or implication | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Analysis.Fourier.LpSpace` and checks the ordinary Fourier integral, Fourier
kernel, `L2` Fourier linear isometry, norm preservation, and Schwartz Fourier transform. These are
encoding ingredients only. A bounded name search did not identify a declaration explicitly named
as an uncertainty principle; this is not the later immutable anchor audit.
