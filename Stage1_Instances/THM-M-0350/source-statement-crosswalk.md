# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Marcel Riesz, gives the year 1928, and supplies only the
gloss `Hilbert变换的L^p有界性` ("the Hilbert transform is bounded on `L^p`"). Stage0 repeats this
metadata. The rev-5.6 manifest deliberately carries `已验证` only as
`source_status_untrusted`. None of these records provides a formula, domain, exponent range,
normalization, theorem/page locator, assumptions, proof, errata, or formal declaration.

## Human-source candidate

Marcel Riesz, *Sur les fonctions conjuguées*, **Mathematische Zeitschrift** 27 (1928), 218-244,
is the historical primary-source candidate suggested by the repository attribution and date. At
intake this is a discovery locator, not an accepted pinpoint crosswalk: the exact theorem/page,
original periodic formulation, hypotheses, normalization, and any errata have not been independently
inspected. In particular, silently replacing an original conjugate-function result on the circle by
a real-line principal-value theorem would broaden the available source record.

## Crosswalk

| Repository phrase | Required mathematical component | Required Lean component | Intake assessment |
|---|---|---|---|
| "Hilbert transform" | real-line transform or periodic conjugate operator; kernel/sign/normalization | an exact operator definition and equality bridges between credited definitions | open |
| "`L^p`" | scalar field, measure space, a.e. quotient, and `1 < p < infinity` | `MeasureTheory.Lp` at a selected `ENNReal` exponent and measure | pinned carrier API probed; parameters open |
| "boundedness" | existence of `C_p` and a norm inequality, or a bounded linear extension | `ContinuousLinearMap` or an exact universally quantified inequality | shape open |
| principal value | truncation filters, convergence mode, and dense initial domain | a checked construction or a checked bridge to a Fourier multiplier | absent |
| Marcel Riesz / 1928 | historical source identity | node-specific source evidence, not a Lean hypothesis | candidate only |
| `已验证` | untrusted inventory status | no proposition and no proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`MeasureTheory.Lp`, `MeasureTheory.MemLp`, `ContinuousLinearMap`, and Fourier-multiplier definitions
for Schwartz functions and tempered distributions. A bounded repository search found no declaration
named for a Hilbert transform or Cauchy principal value. The available multiplier API is only an
encoding ingredient; it does not by itself supply the required `L^p` singular-integral operator or
M. Riesz estimate. This bounded observation is not the later immutable anchor audit.
