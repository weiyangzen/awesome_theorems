# Scope map

## Included topic boundary

- A positive measure on a source-specified analytic domain with a specified boundary measure.
- A source-specified Carleson condition, including its test regions and uniform constant.
- The exact equivalent analytic condition named by the selected theorem.
- All hypotheses on the domain, exponent, function space, measurability, and measure finiteness.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these non-identical choices:

1. Unit disk versus upper half-plane, or a more general domain.
2. Carleson tents/squares over boundary arcs or intervals, including open/closed conventions and
   the height/length normalization.
3. Bounded `H^p -> L^p(mu)` embedding, a reproducing-kernel test, a Poisson-extension estimate, or
   another characterization.
4. One fixed `p`, every `p`, endpoint cases, and whether constants are asserted to be comparable.
5. Finite, locally finite, regular Borel, or other positive measures and boundary mass conventions.

The statement phase must inspect an immutable source and freeze the ordered binders, definitions,
normalizations, constants, degenerate cases, and exact biconditional or implication.

## Explicit exclusions

- The Carleson-Hunt theorem on almost-everywhere Fourier convergence.
- The Corona theorem, Carleson interpolation theorem, or Carleson's convergence theorem.
- Vanishing Carleson measures or compact embeddings unless explicitly selected by the source.
- Vector-valued, weighted, several-complex-variable, PDE, or geometric variants as substitutes.
- A tautology obtained by defining `IsCarleson` to mean the desired conclusion.
- The inventory label `已验证` as proof or source-fidelity evidence.

No canonical Lean target is frozen at intake because the repository record does not identify one.
