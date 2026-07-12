# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `泊松求和公式`, attributes it to
Simeon Poisson, gives the year 1823, and supplies only `傅里叶级数与傅里叶变换的关系` ("the
relationship between Fourier series and the Fourier transform"). Stage0 repeats the gloss. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

This metadata has no displayed equality, domain, hypotheses, transform convention, edition,
theorem/page locator, proof, or errata record. It therefore cannot support H0 or choose one formal
variant. The source audit must obtain a pinpoint authoritative mathematical source and independent
review before the exact-statement gate can close.

## Crosswalk

| Repository phrase | Mathematical choice still needed | Pinned Lean candidate | Intake status |
|---|---|---|---|
| "Fourier transform" | normalization, sign, measure, complex codomain | mathlib notation `𝓕` on `ℝ → ℂ` | API available; choice open |
| "Fourier series" | periodicization, coefficient normalization, evaluation point | `Real.fourierCoeff_tsum_comp_add` | bridge candidate only |
| "relationship" | exact equality and phase factor | `Real.tsum_eq_tsum_fourier` | strongest direct candidate |
| summation formula | convergence/local uniform convergence hypotheses | hypotheses of `Real.tsum_eq_tsum_fourier` | not present in repository source |
| common sufficient version | polynomial decay of function and transform | `Real.tsum_eq_tsum_fourier_of_rpow_decay` | alternate candidate |
| smooth rapid-decay version | Schwartz function | `SchwartzMap.tsum_eq_tsum_fourier` | alternate candidate |
| `已验证` | untrusted inventory label | no proposition or proof evidence | explicitly rejected |

## Pinned formal source boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Fourier.PoissonSummation` documents and implements these candidates. The module
states that its general form assumes a continuous `ℝ → ℂ` function, summability of Fourier samples,
and local uniform summability of integer translates; it also provides decay and Schwartz
specializations. This immutable formal source is directly relevant, but it is not a replacement for
the missing human-source pinpoint and is not credited as canonical closure during intake.

`IntakeProbe.lean` checks the four declaration types only. Terminal bodies, axioms, transitive
dependencies, exact-source correspondence, and alternate-form transports remain for later phases.
