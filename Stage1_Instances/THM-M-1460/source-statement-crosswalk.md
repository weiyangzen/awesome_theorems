# THM-M-1460 source-statement crosswalk

## Repository record

The source inventory at `Docs/researches/math_theorems.md:10658-10663` contains exactly:

- title: `谱方法` (spectral methods);
- proposer: `众多数学家` (many mathematicians);
- time: `20世纪` (20th century);
- statement gloss: `基于正交多项式的数值方法` (numerical methods based on orthogonal
  polynomials);
- importance: high; and
- formalization status: `已验证` (verified).

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, formula, problem,
domain, hypotheses, numerical scheme, conclusion, proof, formal declaration, or validation link.
The Stage0 projection at `Docs/Stage0_Blueprint.md:39703-39728` repeats the gloss and explicitly
leaves exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. Under rev-5.6, the verified label is untrusted metadata.

## Literal crosswalk

| Repository phrase | Material ambiguity | Required exact statement component | Intake status |
|---|---|---|---|
| `谱方法` | approximation, Galerkin, tau, collocation, pseudospectral, eigenvalue, or time-dependent method | problem, discretization, discrete operator, output | open |
| `基于正交多项式` | Fourier is not polynomial; polynomial families differ by domain, weight, and normalization | basis, weight, orthogonality, completeness, indexing | open |
| `数值方法` | exactness, solvability, stability, convergence, error, conditioning, or complexity | one truth-valued conclusion and arithmetic model | open |
| `众多数学家` / `20世纪` | no accountable author, work, edition, theorem, or page | versioned source identity and historical review | open |
| `已验证` | catalog inventory label only | no human or machine proof component | explicitly untrusted |

The rows do not determine ordered binders, hypotheses, or one conclusion. The canonical human
statement and Lean expression therefore remain null rather than silently selecting a textbook
theorem.

## Source-family leads, not admitted sources

Standard modern references that can guide a later source audit include D. Gottlieb and S. A.
Orszag, *Numerical Analysis of Spectral Methods: Theory and Applications* (SIAM, 1977), C. Canuto
et al., *Spectral Methods in Fluid Dynamics* (Springer, 1988), L. N. Trefethen, *Spectral Methods
in MATLAB* (SIAM, 2000), and J. P. Boyd, *Chebyshev and Fourier Spectral Methods*, second edition
(Dover, 2001). The repository cites none of them, and this intake did not pin or inspect a theorem,
page, assumptions, proof boundary, or errata from them. They distinguish several inequivalent
method and theorem families; listing them supplies discovery direction only, not H0 or a repair to
the catalog wording.

## Candidate source-to-statement rows

| Candidate family | Mathematical components that a source must fix | Lean obligations if selected | Current boundary |
|---|---|---|---|
| orthogonal projection | weighted function space, orthogonal basis, truncation, coefficient map | basis/measure definitions, projection, norm estimate | catalog selects none |
| interpolation or collocation | nodes, interpolant, differentiation matrix, residual equations | node distinctness, evaluation map, solvability, error transport | catalog selects none |
| Galerkin or tau discretization | equation/operator, trial/test spaces, boundary enforcement | discrete variational problem, stability, composition to error theorem | overlaps neighbors; no ownership decision |
| smooth-function convergence | regularity scale, norm, constants, algebraic exponent | approximation operator and quantified estimate | no source or exact rate |
| analytic-function convergence | complex extension region, coefficient decay, exponential rate | analytic domain encoding and uniform error bound | no source or boundary convention |
| finite-precision solver | representation, transform, linear solve, rounding and stopping | executable semantics, certificate, stability and error composition | catalog gives no computation contract |

These are resolution rows for a later statement phase, not inherited clauses or a proof crosswalk.

## Pinned formal substrate, not a root anchor

The bounded intake search used pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Relevant declarations include:

- `Polynomial.Chebyshev.integral_eval_T_real_mul_eval_T_real_measureT_of_ne` in
  `Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.Orthogonality`, establishing weighted
  orthogonality of distinct real Chebyshev polynomials;
- `Polynomial.Chebyshev.integral_eq_sumZeroes` in
  `Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.ChebyshevGauss`, an exact quadrature
  result for polynomials below the stated degree bound;
- `fourierBasis` and `hasSum_fourier_series_L2` in `Mathlib.Analysis.Fourier.AddCircle`, providing
  the Fourier Hilbert basis and its `L2` expansion; and
- `exists_polynomial_near_continuousMap` in `Mathlib.Topology.ContinuousMap.Weierstrass`, providing
  generic uniform polynomial approximation on a closed interval.

`IntakeProbe.lean` elaborates these definitions and theorem interfaces. A bounded exact-topic
search found no declaration named or documented as a numerical spectral, collocation, or
pseudospectral method in pinned mathlib or repository-local Lean. The checked interfaces justify
only `M3` statement/interface evidence. Orthogonality, quadrature, Fourier expansion, and generic
approximation do not select or prove a full numerical method, its discrete equations, stability,
or error theorem. This scoped search is not the downstream exhaustive anchor audit.

## Gate result

Human status is provisionally `H5`: the catalog target is a method-family gloss rather than one
stable proposition. Machine status is `M3`: substantive pinned definitions and theorem interfaces
elaborate, but no canonical expression or source-identical root exists. Readability status is
`R4`: this boundary explanation is not a readable proof of an exact theorem. Retry requires an
accountable immutable source selection and independent review fixing every proposition-changing
row before exact statement elaboration.
