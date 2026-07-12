# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` has two near-duplicate records. They name Markus Keel and Terence
Tao, give 1998, and state only `端点Strichartz估计` ("endpoint Strichartz estimate"). Stage0 adds no
definition, hypotheses, conclusion, source pinpoint, proof path, or formal artifact. The rev-5.6
manifest retains `已验证` solely as `source_status_untrusted`.

This identifies a well-known result family, but it is not a source-exact proposition.

## Primary-source locator, not accepted H0 evidence

The aligned primary locator is Markus Keel and Terence Tao, *Endpoint Strichartz Estimates*,
American Journal of Mathematics 120 (1998), no. 5, 955-980. The abstract operator theorem commonly
cited as Theorem 1.2 is the leading statement-phase candidate. During intake, no immutable source
copy and pinpoint passage was archived and independently reviewed. Consequently the bibliographic
match does not establish exact wording, page-level assumptions, errata status, or `H0`.

The statement/source-audit phases must digest an immutable copy, transcribe the selected theorem and
definitions verbatim enough to preserve all quantifiers, record page/theorem numbers and errata,
and obtain independent review before accepting a canonical human claim.

## Provisional clause crosswalk

These rows are a scope guide for transcription, not a frozen statement.

| Repository/source-family phrase | Mathematical component to verify in source | Lean representation candidate | Intake status |
|---|---|---|---|
| operator family `U(t)` | maps energy data to spatial functions | time-indexed continuous linear maps or explicitly bounded maps | binder and codomain open |
| energy estimate | uniform `L^2` control of `U(t)f` | `eLpNorm`, `MemLp`, norm inequality | candidate API probed |
| dispersive estimate | time-decaying `L^1 -> L^infinity` bound for `U(s) U(t)^*` | adjoint/composition plus extended-real `L^p` bounds | hypotheses and zero separation open |
| admissible pair | relation among `q`, `r`, and decay parameter `sigma` | predicate over real/extended-real exponents | equality and exclusions open |
| endpoint | boundary pair retained beyond nonendpoint interpolation | exact source-side endpoint predicate | not stated by repository |
| homogeneous estimate | spacetime norm of `U(t)f` | iterated `eLpNorm` over time and space | inclusion in root open |
| dual estimate | integral of `U(s)^* F(s)` | Bochner integral and adjoint family | inclusion in root open |
| retarded estimate | time-ordered integral over `s < t` | restricted product measure or interval integral | inclusion in root open |
| `已验证` | untrusted inventory label | no Lean term or proof credit | explicitly rejected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.MeasureTheory.Function.LpSeminorm.Basic` and
`Mathlib.Analysis.Normed.Operator.ContinuousLinearMap`. It checks `eLpNorm`, `MemLp`, Bochner
integration, continuous linear maps and composition, and interval measures. These are only encoding
ingredients. No declaration is credited as Keel-Tao, no source theorem is claimed to elaborate, and
formal-anchor discovery remains a later phase.
