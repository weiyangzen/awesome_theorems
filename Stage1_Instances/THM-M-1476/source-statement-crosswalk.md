# THM-M-1476 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10770-10775` supplies exactly the title `刚性稳定性`, attribution
`众多数学家`, the period `20世纪`, the gloss `刚性问题的数值稳定性`, importance "high," and
status `已验证`. Git provenance places all six uncited lines in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, equation,
definition of stiffness or stability, numerical method, binder, hypothesis, conclusion, proof,
theorem locator, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:40135-40160` repeats the gloss while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. Its generic closed-result and leaf-audit wording
is planning metadata, not evidence. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| stiff problem | separated modes, spectral/Jacobian scale, singular perturbation, or method-dependent step restriction | problem class plus a source-defined stiffness predicate | no definition supplied |
| numerical method | one-step, RK, multistep, multiderivative, BDF, or another scheme | coefficients, stages/history, grid, recurrence, and solve relation | no method supplied |
| stability | stiff, absolute, A-, L-, B-, algebraic, contractive, decay, or error stability | exact predicate, norm, horizon, constants, and directions | no notion selected |
| problems, plural | a uniform theorem over a class or a catalog topic | quantified admissible family | class and quantifier order absent |
| many mathematicians / twentieth century | broad genealogy | immutable source edition and pinpoint proposition | no locator supplied |
| `已验证` | untrusted screening label | accepted human-source or kernel receipt would be required | no H or M credit |

The gloss cannot populate a canonical domain, ordered binders, hypotheses, conclusion, alternate
encodings, excluded cases, or Lean expression fingerprint.

## Source-family leads, not admitted sources

Crossref metadata was inspected on 2026-07-13 for three related publications:

- Rolf Jeltsch, "Stiff Stability and Its Relation to A_0- and A(0)-Stability," *SIAM Journal on
  Numerical Analysis* 13(1), March 1976, pages 8-17, DOI `10.1137/0713002`.
- R. Jeltsch, "Stiff Stability of Multistep Multiderivative Methods," *SIAM Journal on Numerical
  Analysis* 14(4), September 1977, pages 760-772, DOI `10.1137/0714052`.
- Rolf Jeltsch, "Corrigendum: Stiff Stability of Multistep Multiderivative Methods," *SIAM Journal
  on Numerical Analysis* 16(2), April 1979, pages 339-345, DOI `10.1137/0716026`.

The titles themselves distinguish method-specific stiff stability and multiple related stability
notions, while the corrigendum makes correction auditing material. The catalog cites none of
these publications. Only deterministic Crossref metadata projections were inspected; no complete
paper, exact definition or theorem passage, incorporated assumptions, proof boundary, correction
impact, or independent source review was admitted. These leads are `E5` discovery evidence and do
not select the target or establish `H0`.

## Neighbor boundary

The catalog separately schedules Runge-Kutta stability regions (`THM-M-1475`), A-stability
(`THM-M-1477`), and L-stability (`THM-M-1478`) immediately around this target. It also separately
schedules stiff equations (`THM-M-1398`) and BDF methods (`THM-M-1399`). Those entries confirm
that the generic gloss must not be silently narrowed to any neighboring family, and no neighbor's
evidence is inherited.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.ODE.Basic`, `Gronwall`, and `PicardLindelof` provide continuous integral-curve,
trajectory-comparison, error-bound, uniqueness, and existence interfaces.
`Mathlib.Analysis.Complex.Trigonometric` provides the complex exponential norm identity used in
scalar decay analysis. `IntakeProbe.lean` checks representative declarations in the pinned
environment.

These declarations do not define stiffness, a numerical scheme, stiff stability, or a relation to
A- or L-stability. A bounded exact-topic search over repo-local Lean and pinned mathlib analysis
sources found no source-selected stiff-stability terminal declaration. This is intake discovery,
not an exhaustive external anchor audit, a global absence claim, or target proof evidence.

## Source exit gate

Before leaving `H5`, accountable reviewers must redirect the topic label to one corrected,
truth-valued proposition; preserve an immutable primary or authoritative edition; select exact
definition/theorem/section/page and proof boundary; map every incorporated definition, ordered
binder, hypothesis, constant, conclusion, and boundary case; reconcile neighboring targets; audit
the source and all corrections; and obtain independent numerical-analysis and source review.

Only then may the statement phase freeze minimal imports, elaborate and preserve the identical
Lean expression and environment fingerprint, compile checked transports, and mutation-test a
removed hypothesis, changed domain, changed binder scope, and boundary case. Until then no exact
statement, H0, M0, R0, proof, audit completion, or theorem completion is claimed.
