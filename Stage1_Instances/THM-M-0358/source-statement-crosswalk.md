# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `傅里叶乘子定理`, attributes it to Lars
Hormander, dates it to 1960, and states only `傅里叶乘子的L^p有界性` ("L^p boundedness of Fourier
multipliers"). `Docs/Stage0_Blueprint.md` repeats this metadata. The rev-5.6 manifest preserves
`已验证` only in the explicitly untrusted source-status field. None supplies the multiplier
definition, symbol hypothesis, exponent range, conclusion, proof reference, edition, page, errata,
or formal artifact.

The immediately following inventory target is a separately named Mihlin multiplier theorem. That
adjacency is evidence that silently selecting a familiar Hormander-Mihlin formulation could merge
two distinct repository targets, so it is not permitted at intake.

## Candidate source work

Hormander's original multiplier work and authoritative harmonic-analysis texts are candidate
locators, but no paper title, stable edition, theorem number, or page has been accepted here. The
source-audit phase must identify the intended result and record exact bibliographic identity,
notation, all symbol and dimension hypotheses, exponent restrictions, constant dependence, proof
boundary, corrections, and independent review. A plausible textbook theorem is not yet a source
crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Fourier multiplier" | `T_m f = F^{-1}(m F f)` on an initial dense class | fixed Fourier transform plus multiplication and inverse transform | pinned Schwartz/distribution API probed; exact operator open |
| `L^p` | Lebesgue-space exponent, normally with source-specific restrictions | `MemLp`, `Lp`, `eLpNorm`, measure and exponent | pinned API probed; range open |
| "boundedness" | extension to a bounded operator with a quantitative norm estimate | continuous linear map on `Lp` or equivalent exact bound | conclusion family known; exact constant open |
| symbol criterion | derivative, localized Sobolev, integral, or variation hypothesis | concrete predicates with all orders/scales quantified | absent from source record |
| Lars Hormander / 1960 | historical locator | no formal proposition and no proof credit | bibliography unresolved |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports Fourier multipliers for Schwartz functions and tempered distributions, the `L^2`
Fourier transform, and basic `L^p` infrastructure. It checks both multiplier continuous-linear-map
constructors, the bounded-symbol temperate-growth interface, the `L^2` Fourier isometry/norm result,
and `MemLp`/`eLpNorm`. These are encoding ingredients only. They do not establish an `L^p`
extension under a Hormander-type symbol condition. The bounded local name search is discovery
evidence, not the later immutable anchor audit.

Before `H0`, an independent reviewer must approve an exact source theorem/page, definitions, every
hypothesis and endpoint convention, proof boundary, and errata. Before statement credit, that
approved wording must map row by row to one elaborated Lean proposition.

