# THM-M-1248 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Caffarelli-Kohn-Nirenberg
weighted interpolation inequalities. The manifest's historical `已验证` label is untrusted metadata
and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Root family | The weighted interpolation estimate of Caffarelli, Kohn, and Nirenberg for compactly supported smooth functions on `R^n` | The precise admissible parameter region must be transcribed and elaborated in the statement phase |
| Analytic data | dimension, exponents `p q r`, weights `alpha beta gamma`, interpolation coefficient `a`, and a test function | Endpoint conventions and integrability/measurability side conditions remain open |
| Scaling | the dimensional homogeneity relation among weights and reciprocal exponents | Candidate formula only; no checked arithmetic encoding exists |
| Estimate | weighted `L^r` norm bounded by a constant times a weighted gradient `L^p` norm and weighted `L^q` norm | Choice of extended/nonnegative-real norms and exponentiation API is not frozen |
| Constant | existence of a finite constant depending only on the admitted parameters | No optimal-constant or extremizer claim is included |
| Formal surface | Lean 4 plus pinned mathlib analysis APIs | No exact declaration, expression hash, import closure, or kernel proof is claimed |

Excluded from this target are the CKN Navier-Stokes partial-regularity theorem, later symmetry
breaking/classification results, best-constant computations, and a weaker unweighted interpolation
inequality substituted for the weighted theorem.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The primary paper and theorem
family are identified, but the source's complete parameter cases and conventions have not yet been
transcribed into an exact Lean proposition. The first failed theorem gate is therefore the exact
statement gate. No theorem completion or machine closure is claimed.

## Validation

The exact intake checks and results are recorded in `validation.md`. They establish target
membership, repository structural consistency, JSON syntax, and dossier hygiene only.
