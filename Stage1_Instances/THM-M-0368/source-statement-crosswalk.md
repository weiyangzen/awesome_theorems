# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `极大函数定理`, attributes it to Hardy and Littlewood,
dates it to 1930, and glosses it as `Hardy-Littlewood极大函数的弱型估计` (the weak-type estimate
for the Hardy-Littlewood maximal function). `Docs/Stage0_Blueprint.md` repeats that record without
adding a formula or citation. The rev-5.6 manifest preserves `已验证` only as the explicitly
untrusted `source_status_untrusted` field.

The inventory gives no primary-source edition, theorem/page, assumptions, errata, proof boundary,
or formal artifact. It therefore locates a theorem family but does not support `H0` or an exact
formal target.

## Crosswalk

| Repository phrase | Mathematical component to freeze | Lean component | Intake status |
|---|---|---|---|
| Hardy-Littlewood maximal function | centeredness, averaging sets, radius range, normalization | a new canonical definition using `Metric.ball`/`closedBall`, measure, and integral APIs | absent |
| weak-type estimate | superlevel-set measure inequality and strictness convention | `Measure`, set comprehension, `ENNReal`/`Real` inequality | shape known; formula open |
| input function | codomain, representative, measurability, and finite `L1` norm | `AEMeasurable`, `Integrable`, `L1`, `lintegral`, `enorm` | open |
| Euclidean setting | dimension, norm, Borel structure, Lebesgue measure | finite-dimensional normed space or `EuclideanSpace` instances | open |
| estimate constant | exact constant and its dimension dependence | explicit term or existentially quantified finite constant | open |
| `已验证` | untrusted inventory label | no declaration and no proof credit | rejected as evidence |

## Source work still required

The statement phase must select and independently inspect an immutable authoritative source that
states the weak `(1,1)` theorem. The crosswalk must then record edition, theorem/page, exact
definition of the operator, every hypothesis, the constant, applicable dimensions, proof nodes,
errata search, and a line-by-line mapping to the Lean expression. A modern textbook may clarify the
standard formulation, but it cannot be cited vaguely and called primary-source fidelity.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe imports
`Mathlib.MeasureTheory.Covering.Besicovitch` and checks APIs for balls, Lebesgue measure, lower
integrals, Besicovitch covering, and Vitali differentiation infrastructure. A bounded source-tree
name search found no declaration defining the Hardy-Littlewood maximal operator or stating its weak
`(1,1)` estimate. This negative name search is discovery evidence only, not the later anchor audit.
Nearby covering and differentiation theorems are ingredients, not closure of this target.
