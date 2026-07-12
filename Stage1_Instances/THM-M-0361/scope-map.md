# Scope map

## Included topic boundary

- A source-specified real-variable characterization of a specified Hardy space `H^p`.
- The exact ambient Euclidean or other domain, dimension, measure, scalar field, and distribution or
  function realization.
- The source's precise radial, nontangential, grand maximal, area, or square functional, including
  kernels, test-function normalization, apertures, and dilation convention.
- The exact exponent range and a membership equivalence or quantitative quasinorm comparison with
  constants and dependency conditions.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these materially different targets:

1. **Radial maximal characterization:** membership in `H^p` characterized by the `L^p` behavior of
   a radial maximal convolution.
2. **Nontangential/grand maximal characterization:** an equivalence using a cone supremum or a
   supremum over a normalized class of Schwartz test functions.
3. **Area or square-function characterization:** an equivalence involving a Lusin area integral,
   Littlewood-Paley function, or another derivative/extension functional.
4. **Local versus global Hardy space:** an inhomogeneous/local theorem has different large-scale
   conditions from the global Euclidean space.
5. **Qualitative versus quantitative result:** equality of membership sets is weaker data than a
   two-sided quasinorm inequality with controlled constants.

The statement phase must inspect an immutable source and freeze the distribution model, all
ordered binders, `p` range, kernel cancellation and normalization, maximal or square functional,
measure, constants, and both implication directions. It must decide endpoints and zero/boundary
cases rather than silently importing modern conventions.

## Explicit exclusions

- The Fefferman-Stein sharp maximal function inequality or vector-valued maximal inequality as a
  substitute; these are separate theorems despite the shared names.
- A characterization of classical holomorphic Hardy spaces, BMO, Sobolev, Besov, or
  Triebel-Lizorkin spaces unless the selected source explicitly transports it to this target.
- Defining `H^p` to be the chosen maximal-function `L^p` class and then proving a tautology.
- Plain `L^p` Fourier, convolution, or maximal estimates without the selected Hardy-space
  equivalence and checked definitions.
- The separate adjacent targets for atomic decomposition, BMO duality, vector-valued inequalities,
  or maximal functions as substitutes or sources of duplicated proof credit.
- The inventory label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify one.
