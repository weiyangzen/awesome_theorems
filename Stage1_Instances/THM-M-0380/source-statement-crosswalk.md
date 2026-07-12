# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `Sogge局部光滑性定理`, attributes it to Christopher
Sogge, gives the year 1991, and states only `波动方程解的局部光滑性` ("local smoothing of
solutions of the wave equation"). `Docs/Stage0_Blueprint.md` repeats that gloss and leaves exact
definitions, hypotheses, proof history, axioms, and formal artifacts open. The manifest preserves
`已验证` only as `source_status_untrusted`.

The repository also contains a distinct duplicate-name target, `THM-M-1211`, and nearby generic
local-smoothing and Strichartz targets. Their existence does not disambiguate this proposition.

## Candidate source boundary

A natural discovery candidate is Andreas Seeger, Christopher D. Sogge, and Elias M. Stein,
"Regularity properties of Fourier integral operators", *Annals of Mathematics* 134 (1991),
231-251, DOI `10.2307/2944346`. Christopher D. Sogge's *Fourier Integrals in Classical Analysis*
is a candidate locator for definitions and later formulations. These bibliographic leads have not
been accepted as the unique intended theorem, and no numbered theorem/page or errata record was
independently cross-checked in this intake. They are therefore discovery evidence, not `H0`.

## Crosswalk

| Repository phrase | Source component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "Sogge local smoothing theorem" | one numbered result at an immutable edition | one exact proposition | family scoped; exact anchor open |
| "wave equation" | wave propagator or source FIO, with phase/amplitude | concrete operator and all analytic assumptions | operator open |
| "local smoothing" | integrated-in-time gain over fixed-time regularity | measurable time family and a space-time norm inequality | included; gain open |
| dimension and exponent range | all restrictions on dimension and `p` | explicit binders and inequalities | absent from metadata |
| derivative gain/loss | exact Sobolev orders and epsilon convention | exact regularity spaces/norms | absent from metadata |
| localization | time interval, cutoffs, supports, frequency scale | explicit sets, measures, cutoffs, and quantified scale | absent from metadata |
| uniform estimate | dependencies of the bound's constant | quantified constant and dependency ordering | included; details open |
| `已验证` | untrusted inventory label | no proposition and no proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports Fourier-transform and Schwartz-space Fourier modules and checks representative
Fourier integral, Schwartz transform, derivative/Fourier interaction, and Plancherel APIs. These
are only ingredients. A scoped phrase search found no Sogge/local-smoothing/cinematic-curvature
declaration in pinned mathlib. This is not the later immutable formal-anchor audit.
