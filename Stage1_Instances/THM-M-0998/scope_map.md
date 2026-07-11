# Scope map

| Surface | Intake scope | Boundary |
|---|---|---|
| Source identity | `THM-M-0998`, Poincare inequality, probability foundations, "upper bound on variance" | The label is not an exact theorem statement |
| Left side | Variance of a real-valued observable | Measure, integrability, and variance convention are open |
| Right side | An energy/gradient quantity multiplied by a Poincare constant | Energy form, derivative notion, normalization, and constant are open |
| Admissible functions | A domain supporting variance and energy | Smooth, Sobolev, Lipschitz, discrete, and mean-zero variants are not interchangeable |
| Geometry | Probability/measure-space formulation | Euclidean domains, Riemannian manifolds, graphs, Markov chains, and PDE boundary forms are candidates, not frozen scope |
| Lean surface | Lean 4 + mathlib | No declaration or expression is credited before exact source selection |
| Foundations | Kernel-checked measure/analysis definitions under a versioned profile | Toolchain, imports, classical choice, and TCB closure remain open |

## Required statement-phase decisions

1. Pin a theorem-level human source and identify its exact numbered statement or page.
2. Fix the carrier, measure normalization, scalar/codomain, admissible function class, and finiteness assumptions.
3. Define variance, the energy/gradient term, the inequality direction, and the constant convention.
4. Fix centering and boundary conditions and cover constant or zero-energy edge cases.
5. Only then select a Lean expression, elaborate it, fingerprint it, and mutation-test it.

## Explicit exclusions

No spectral-gap theorem, Wirtinger inequality, domain-specific PDE inequality, discrete-chain
inequality, Gaussian-only inequality, or tautological definition of "has a Poincare inequality" may
replace the root merely because it also bounds variance. Such forms may become alternate encodings
only after a checked relationship to the source-selected canonical claim exists.
