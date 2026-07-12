# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `哈代不确定性原理`, attributes it to
Godfrey Hardy, gives the year 1933, and states only `函数与傅里叶变换衰减性的限制` ("a limit on
the decay of a function and its Fourier transform"). Stage0 repeats this metadata while marking
exact definitions and assumptions as open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`. No formula, transform convention, hypotheses, conclusion, edition,
theorem/page, proof source, or formal artifact is supplied.

## Candidate source work

The theorem name strongly locates a classical result, but is not enough for `H0`. The source audit
must inspect an immutable edition of Hardy's original paper or an authoritative modern statement,
record theorem/page, its Fourier normalization, assumptions, strict and critical cases, proof
boundary and errata, and obtain independent review. A modern reformulation must be crosswalked to
the original rather than silently replacing it.

## Crosswalk

| Repository phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "function" | domain, codomain, measurability/function class | a concrete function type plus analytic hypotheses | open |
| "Fourier transform" | sign, character, Haar/Lebesgue measure, normalization | `Fourier.fourierIntegral` or notation `𝓕` with explicit convention | pinned API probed; selection open |
| "decay" | pointwise, almost-everywhere, big-O, or weighted-integral bounds | norm inequalities involving real/complex exponential | open |
| "limit" | parameter threshold and its normalization-dependent constant | exact strict/critical comparison | absent from source record |
| theorem conclusion | zero above threshold and/or Gaussian at equality | extensional or almost-everywhere equality | absent from source record |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports the Fourier transform of the Gaussian and checks the general Fourier integral,
mathlib's real Fourier notation, the complex exponential, and `fourier_gaussian_pi`. The final
declaration proves that a Gaussian transforms to a Gaussian under mathlib's normalization. It does
not prove the converse rigidity or supercritical vanishing theorem, so it is only an encoding and
future dependency candidate. The bounded search found no declaration named as Hardy's uncertainty
principle; that observation is not a substitute for the later immutable anchor audit.
