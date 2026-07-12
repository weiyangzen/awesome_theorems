# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the Chinese title `卡尔松定理`, attributes it to Lennart
Carleson, dates it to 1966, and says `L^2函数傅里叶级数几乎处处收敛` ("the Fourier series of an
L^2 function converges almost everywhere"). Stage0 repeats this wording. Neither record supplies
definitions, a theorem number, a page, complete assumptions, a proof boundary, or a formal artifact.
The rev-5.6 manifest therefore retains `已验证` only as untrusted source metadata.

## Primary-source candidate

Lennart Carleson, *On convergence and growth of partial sums of Fourier series*, Acta Mathematica
116 (1966), 135-157, is the primary-source candidate identified by title and bibliographic metadata.
The paper's exact theorem wording, page anchor, conventions, proof premises, and any errata have not
been independently inspected in this intake. This citation is a discovery anchor, not `H0` evidence.

## Crosswalk

| Repository/source phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| `L^2` function | square-integrable periodic function modulo null equality | `Lp ℂ 2 haarAddCircle` plus representative bridge | included; normalization open |
| Fourier series | coefficients against integer circle characters | `fourierCoeff`, `fourier`/`fourierLp` | pinned API exists |
| partial sums | symmetric sums over frequencies from `-N` through `N` | explicit finite integer interval and evaluated finite sum | exact encoding open |
| almost everywhere | outside a Haar-null set | measure-a.e. eventual pointwise `Tendsto` | exact expression open |
| converges | full sequence, not only a subsequence or Cesaro means | `Tendsto` along `N -> infinity` | topology and representative open |
| target value | the original function at almost every point | representative-independent a.e. equality | bridge obligation open |
| Carleson / 1966 | attribution and historical locator | no Lean proof credit | candidate paper identified |

## Source and machine boundary

The pinned mathlib module `Mathlib.Analysis.Fourier.AddCircle` provides Fourier coefficients,
characters, the `L^2` Fourier basis, Parseval identities, and `L^2`-topology summation. The intake
name/content search found no declaration identified as Carleson's almost-everywhere convergence
theorem. This is a narrow local observation, not the later immutable anchor audit and not proof of
absence from all Lean projects.

Before source status can improve, an independent reviewer must inspect the selected paper edition,
pinpoint the theorem and all definitions and assumptions, check errata, and approve each crosswalk
row. Before statement credit, those approved components must map to one elaborated Lean expression,
including the `Lp`-representative and symmetric-sum choices.

