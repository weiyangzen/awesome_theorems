# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` names Craig Tracy and Harold Widom, gives 1994, and describes the
claim only as "the distribution of the largest eigenvalue of a random matrix." The generated
Stage0 record repeats that phrase and labels it verified. This is metadata-level discovery input,
not a precise theorem, primary-source proof, formal-system claim, or `H0` evidence.

## Candidate primary source

Craig A. Tracy and Harold Widom, "Level-Spacing Distributions and the Airy Kernel," *Communications
in Mathematical Physics* 159 (1994), 151-174, DOI `10.1007/BF02100489`, is the primary candidate
for the beta-2 Airy-kernel distribution. The intake records bibliographic identity only. The exact
theorem/equation/page locators, matrix normalization, hypotheses, proof dependencies, and published
corrections have not yet been inspected and must not be treated as `H0`.

A source auditor must also identify the primary finite-`N` GUE edge-asymptotic result needed to
justify the convergence wording if the cited paper presents the limiting Fredholm determinant
through correlation/gap probabilities rather than as the exact normalized-largest-eigenvalue
theorem frozen here. A secondary exposition cannot silently supply that missing source edge.

## Crosswalk

| Repository or intake phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "random matrix" | normalized `N x N` GUE Hermitian random matrix | matrix-valued random variable and its law | narrowed to GUE; exact density open |
| "largest eigenvalue" | top real eigenvalue `lambda_max(H_N)` | Hermitian spectrum, ordering, measurability | included; API open |
| "distribution" | asymptotic edge distribution under centering/scaling | pushforward laws or distribution functions and weak convergence | included; encoding open |
| spectral edge `2` | normalization-dependent semicircle edge | exact entry variance and normalization transport | constant audit open |
| `N^(2/3)` scaling | soft-edge fluctuation scale | real coercions/powers and scaled random variable | constant factor open |
| `F_2` | beta-2 Tracy-Widom distribution function | concrete real function/probability law | included; construction open |
| Airy-kernel formula | `F_2(s) = det(I-K_Ai)` on `L2(s,infinity)` | Airy function, integral operator, trace class, determinant | included; formal API open |
| convergence for every real `s` | limiting CDF statement | quantified limit/evaluation theorem | included; continuity bridge open |

## Review and status boundary

Before `H0`, an independent source reviewer must pin an accessible edition, enter theorem/equation
and page locators, map every normalization and analytic premise, inspect errata, and approve the
source-to-node crosswalk. Before any machine status stronger than `M4`, anchor audit must locate and
check an exact Lean declaration or record the absence and missing infrastructure. No source review,
Lean declaration, or proof closure is claimed by this intake.
