# THM-M-1460 scope map

## Preserved repository scope

The repository identifies spectral methods as numerical methods based on orthogonal polynomials.
This intake preserves that numerical-analysis family. It does not infer a particular basis,
discretization, differential equation, approximation theorem, or convergence result from the
untrusted `已验证` label.

## Proposition-changing decisions

An approved source correction must freeze:

- the mathematical problem: polynomial or trigonometric approximation, interpolation,
  quadrature, an eigenvalue problem, or a specified ordinary or partial differential equation;
- the spatial and time domains, dimension, geometry, scalar field, coefficient and solution
  spaces, topology, norms, inner products, measures, universes, and typeclass context;
- boundary and initial conditions, operator domain, coefficient regularity, ellipticity or other
  analytic hypotheses, and whether the problem has a unique exact solution;
- Fourier, Chebyshev, Legendre, Jacobi, or another polynomial or function family, including weight,
  normalization, indexing, orthogonality, completeness, and tensor-product conventions;
- Galerkin, Petrov-Galerkin, tau, collocation, pseudospectral, interpolation, quadrature, or another
  discretization, with trial/test spaces, nodes, projection, residual, and discrete operator;
- truncation degree and index set, coefficient construction, interpolation or projection operator,
  aliasing/dealiasing rules, and representation of derivatives and boundary conditions;
- the exact conclusion: existence or uniqueness of the discrete solution, exactness, consistency,
  stability, convergence, a priori or a posteriori error, exponential or algebraic rate,
  conservation, conditioning, complexity, or a checked conjunction;
- the regularity or analyticity class, constants and their dependencies, norm and convergence mode,
  quantifier order, asymptotic regime, and uniformity of any estimate; and
- exact real/complex arithmetic versus floating point, quadrature error, rounding, solver and
  stopping policy, certification, and every boundary or degenerate case.

These choices yield inequivalent propositions. They are a downstream resolution checklist, not a
canonical theorem statement.

## Candidate families not credited

- Orthogonality, completeness, or coefficient identities for a selected polynomial or Fourier
  basis.
- Best approximation, interpolation, projection, or quadrature exactness for finite expansions.
- Spectral convergence for analytic functions, or algebraic convergence under Sobolev regularity.
- Stability and error of a Galerkin, tau, collocation, or pseudospectral discretization of a fixed
  boundary-value or initial-boundary-value problem.
- Conditioning, aliasing, time stepping, complexity, or finite-precision correctness of an
  implemented spectral solver.

No family in this list is selected or credited at intake.

## Degenerate and boundary scope

The statement phase must decide empty, singleton, and zero-dimensional domains; polynomial degree
zero and small truncations; zero weights and singular endpoints; repeated or coincident nodes;
zero or nonsmooth data; incompatible boundary conditions; nonunique continuous or discrete
solutions; a basis missing constants or boundary modes; zero denominators and singular mass or
stiffness matrices; quadrature orders below exactness; aliasing; complex coefficients; and exact
versus rounded arithmetic. No case is silently excluded at intake.

## Explicit exclusions

- Chebyshev orthogonality, Gaussian quadrature, Fourier `L2` expansion, or Weierstrass polynomial
  approximation presented as a full spectral numerical method.
- A theorem for one hand-picked equation, interval, basis, discretization, or regularity class
  presented as the unspecified catalog root.
- Galerkin (`THM-M-1462`), Petrov-Galerkin (`THM-M-1463`), discontinuous Galerkin
  (`THM-M-1464`), finite elements (`THM-M-1461`), or spectral elements (`THM-M-1467`) substituted
  without a reviewed scope and reduction decision.
- A structure or hypothesis that assumes the desired discrete solvability, stability, convergence,
  error estimate, exactness, or conditioning result.
- A sampled numerical run, convergence plot, benchmark, floating-point residual, theorem name,
  `#check`, or the untrusted catalog status presented as proof.

## Neighbor boundaries

`THM-M-1458` separately catalogs the fast Fourier transform, an algorithm for evaluating a discrete
transform rather than a spectral discretization theorem. `THM-M-1461` through `THM-M-1464`
separately catalog finite-element and Galerkin families. `THM-M-1467` separately catalogs spectral
elements. Those methods may later become dependencies or compared formulations, but no statement,
proof, or completion credit transfers between targets.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, Chebyshev APIs define
`T`, its polynomial sequence and weighted measure, prove orthogonality, and prove an exact
Chebyshev-Gauss quadrature formula. Fourier APIs provide an `L2` Hilbert basis and convergence of
the Fourier series, while the continuous-map Weierstrass API gives polynomial approximation on a
closed interval. `IntakeProbe.lean` checks representative declarations in the pinned toolchain.
These are substantive statement/interface substrate, hence provisional `M3`, but they do not
define a discretized operator or close any source-selected spectral-method result. No canonical
module, expression, fingerprint, alternate encoding, checked transport, or mutation suite exists.

## Intake boundary

This scope map supports a provisional planned intake only. Source selection, exact statement work,
formal anchor audit, obligation-tree construction, proof, validation, and release remain separate
open phases.
