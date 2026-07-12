# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `傅里叶变换反演公式`, attributes it to Joseph Fourier and
1822, and gives only `傅里叶变换的逆变换` ("the inverse transform of the Fourier transform"). Stage0
repeats that gloss and explicitly leaves precise definitions, assumptions, proof history, and
artifacts open. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted`.

This metadata is not a theorem-level source: it supplies no edition, theorem/page, transform
normalization, domain, hypotheses, conclusion, proof, errata, or assumption map. The historical
attribution also does not establish that a modern Lebesgue-integral formulation occurs verbatim in
Fourier's 1822 work. Consequently this intake assigns `H1`, not `H0`.

## Crosswalk

| Repository phrase | Mathematical choice still required | Pinned Lean candidate | Intake status |
|---|---|---|---|
| "Fourier transform" | domain, Haar/Lebesgue measure, sign and normalization | `FourierTransform.fourier` / notation `𝓕` | API checked; selection open |
| "inverse transform" | inverse convention and direction | `FourierTransformInv.fourierInv` / notation `𝓕⁻` | API checked; selection open |
| "inverse of the transform" | pointwise, function, a.e., or `L2` equality | `MeasureTheory.Integrable.fourierInv_fourier_eq` or `Continuous.fourierInv_fourier_eq` | candidate only |
| omitted assumptions | integrability, transform integrability, continuity/Lebesgue point | explicit hypotheses of candidate declarations | source crosswalk absent |
| `已验证` | untrusted inventory label | no proposition or proof credit | rejected as evidence |

## Lean candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Fourier.Inversion` provides a pointwise theorem on finite-dimensional real inner
product spaces: if `f` and `𝓕 f` are integrable and `f` is continuous at `v`, then
`𝓕⁻ (𝓕 f) v = f v`. It also provides the continuous-function equality corollary and reverse-order
variants. The bounded probe elaborates these declaration types and definitions only.

The statement phase must select an authoritative mathematical source with edition, theorem/page,
assumptions, convention, proof boundary, and errata, then determine whether one candidate is an
exact encoding. Until that crosswalk and independent review exist, the promising mathlib anchor is
not credited as closure of the repository's under-specified claim.
