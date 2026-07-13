# THM-M-1467 scope map

## Preserved repository scope

The repository identifies the spectral element method, attributes it to Anthony Patera in 1984,
and glosses it as the combination of spectral methods and finite elements. This intake preserves
that hybrid numerical-analysis family. It does not infer a particular theorem from the untrusted
`已验证` label or from the historical metadata.

## Proposition-changing decisions

An approved source correction must freeze:

- the mathematical problem: approximation, elliptic or parabolic boundary-value problem,
  incompressible flow, eigenproblem, conservation law, or another specified equation;
- the spatial and time domains, dimension and geometry, scalar field, coefficients, data, boundary
  and initial conditions, exact solution convention, regularity, norms, and all typeclass context;
- the mesh or macro-element partition, reference element, physical-element maps, geometric
  regularity, conformity, continuity across interfaces, and treatment of curved boundaries;
- tensor-product or simplicial polynomial spaces, local and global degrees, nodal or modal basis,
  interpolation nodes, normalization, degrees of freedom, assembly, and boundary enforcement;
- Galerkin, Petrov-Galerkin, collocation, tau, discontinuous, or another residual formulation,
  including continuous and discrete trial/test spaces and the exact discrete solution relation;
- exact integration or a selected quadrature rule, its nodes and weights, degree of exactness,
  mass lumping, aliasing or dealiasing, and how quadrature modifies the variational form;
- every analytic premise: continuity, coercivity, ellipticity, inf-sup, consistency, stability,
  approximation, inverse and trace inequalities, mesh quality, regularity, and solvability;
- the exact conclusion: discrete existence or uniqueness, orthogonality, best approximation,
  stability, consistency, conservation, convergence, an error estimate and rate, conditioning,
  complexity, or an explicitly checked conjunction;
- quantifier order, constants and their dependencies, uniformity in mesh size and polynomial degree,
  asymptotic regime, and whether the claim covers an `h`, `p`, or `hp` family; and
- exact real or complex arithmetic versus floating point, linear/nonlinear solver semantics,
  stopping rule, rounding error, certificates, and implementation correctness.

These choices yield inequivalent propositions. They are a downstream resolution checklist, not a
canonical theorem statement.

## Candidate theorem families not credited

- Existence and uniqueness of one spectral-element discretization of one fixed PDE.
- Galerkin orthogonality, best approximation, or a Cea-type quasi-optimality estimate.
- Polynomial interpolation, projection, inverse, trace, or quadrature exactness on a reference
  element and its transport to a physical mesh.
- Algebraic, exponential, `h`, `p`, or `hp` convergence under a selected regularity regime.
- Stability, conservation, conditioning, complexity, or finite-precision correctness of an
  assembled solver.

No family in this list is selected or credited at intake.

## Degenerate and boundary scope

The statement phase must decide empty, singleton, or zero-dimensional domains; empty meshes and
zero-measure or inverted elements; polynomial degree zero and small degrees; singular or
non-bijective element maps; hanging nodes and nonmatching interfaces; discontinuous versus
conforming spaces; repeated interpolation or quadrature nodes; zero or negative weights;
underintegration; singular mass or stiffness operators; zero, nonsmooth, or incompatible data;
nonunique continuous or discrete solutions; straight versus curved geometry; real versus complex
coefficients; and exact versus rounded arithmetic. No case is silently excluded at intake.

## Explicit exclusions

- Patera's 1984 channel-expansion study presented as a general spectral-element theorem without a
  reviewed theorem/formula locator and exact source-to-target decision.
- Chebyshev orthogonality or quadrature, generic Hilbert-space projection, or Lax-Milgram
  well-posedness presented as the missing spectral-element root.
- A generic spectral-method (`THM-M-1460`), finite-element (`THM-M-1461`), Galerkin
  (`THM-M-1462`), Petrov-Galerkin (`THM-M-1463`), discontinuous-Galerkin (`THM-M-1464`), finite-
  difference (`THM-M-1465`), finite-volume (`THM-M-1466`), or `hp` finite-element
  (`THM-M-1468`) result substituted for this separately owned target.
- A structure or premise that assumes the desired discrete solvability, stability, convergence,
  error estimate, exactness, conservation, conditioning, or solver output.
- A convergence plot, benchmark, floating-point residual, theorem name, `#check`, or catalog status
  presented as proof.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks Lax-Milgram and orthogonal-projection APIs plus Chebyshev polynomial, orthogonality, and exact
quadrature interfaces. These can be ingredients of a later formalization, but they do not define a
mesh, element geometry, local-to-global assembly, discrete spectral-element problem, or the missing
root proposition. A bounded exact-topic search found no declaration named or documented as a
spectral-element or pseudospectral numerical method in pinned mathlib or repository-local Lean.
This is intake discovery only, not the downstream exhaustive anchor audit.

## Intake boundary

The scope map supports a provisional planned intake only. Exact source admission, statement work,
formal anchor audit, obligation-tree construction, proof, validation, and release remain separate
open phases.
