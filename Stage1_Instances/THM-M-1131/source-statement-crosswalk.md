# Source-statement crosswalk

| Claim component | Source lead | Lean target surface | Intake assessment |
|---|---|---|---|
| Heat conduction model | J. Fourier, *Theorie analytique de la chaleur* (Paris: Firmin Didot, 1822) | Future flux and temperature fields | Primary historical work identified, but exact chapter/page, edition hash, translation, notation, and errata have not been audited; not H0 evidence |
| Fourier constitutive relation | Exact historical passage or a pinned modern primary treatment must supply the sign, isotropic/anisotropic conductivity, and units | `q = -K grad T` in a future selected field model | Schematic scope only; no exact transcription or checked encoding |
| Local energy balance | Must be separately sourced because it is not logically supplied merely by the flux relation | Future divergence/balance hypothesis | Required premise of the derivation, not a consequence to invent or suppress |
| Material relation | Source-selected dependence of internal energy on temperature, with density and heat capacity assumptions | Future coefficient hypotheses | Constant-coefficient and variable-coefficient variants cannot be conflated |
| Heat equation | Repository research note says only "热方程的推导" under Fourier (1822) | Future canonical implication from balance plus constitutive assumptions | Domain, regularity, source term, boundary conditions, and classical/weak equality remain unresolved |
| Historical metadata | `Docs/researches/math_theorems.md`, entry "Fourier热传导定律" | No Lean evidence | The labels `已验证` and "derivation" are untrusted discovery metadata and provide no proof credit |

The central source-to-statement issue is logical: Fourier's law alone is a constitutive equality for
flux, not the heat equation. A derivation also needs conservation of energy and a material
energy-temperature relation. The statement phase must freeze an exact conditional theorem with
ordered binders and hypotheses, then mutation-test removal of each premise and the signs and
coefficient regimes. Source audit must obtain an immutable edition, pinpoint every premise and
conclusion, check later corrections or translation differences, and receive independent review.
Human status therefore remains `H1`.
