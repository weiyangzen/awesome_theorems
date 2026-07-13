# Scope map

## Preserved repository and source scope

The repository names the discontinuous Galerkin method family and points historically to Reed and
Hill (1973). The inspected Reed-Hill source is narrower than the modern family: it treats the
one-velocity neutron transport equation in two spatial dimensions, replaces angular dependence by
standard discrete ordinates, uses an explicit characteristic-directed sweep on a regular triangular
mesh, and approximates the angular flux independently on each triangle by a total-degree polynomial.

For polynomial degree `N`, the source uses `K = (N + 1)(N + 2) / 2` Lagrange degrees of freedom.
The discontinuous variant imposes no continuity across triangle interfaces. Its boundary value is
the trace approached in the streaming direction, with the jump on the other side. Substitution into
the transport equation gives an interior residual plus an incoming-face Dirac term; testing against
the `K`-dimensional polynomial space yields a local `K` by `K` linear system.

That is a method specification, not yet a theorem. The source phrases nonsingularity conditionally
on proper choices and supports stability and accuracy through experiments. It does not supply one
general, proved proposition matching the catalog gloss.

## Decisions required at statement freeze

1. Select an exact source proposition and decide whether it is construction, well-posedness,
   consistency, conservation, stability, convergence, an error estimate, or a benchmark theorem.
2. Fix the continuous model: transport, elliptic, hyperbolic, conservation-law, or another PDE;
   dimension, coefficient domain, state space, coefficients, sources, initial/boundary conditions,
   and solution notion.
3. Fix the spatial and angular discretization, including domain, mesh family, cell geometry,
   conformity/shape regularity, orientation, discrete ordinates or velocity space, and refinement
   parameter.
4. Fix the broken trial and test spaces, scalar field, polynomial degree, basis and interpolation
   points, local/global degrees of freedom, quadrature, mass terms, and exact integration policy.
5. Fix traces and jumps, face orientation, incoming/outgoing classification, numerical flux or
   penalty, boundary flux, and every sign convention.
6. For the Reed-Hill variant, fix the characteristic sweep, regular triangular-mesh restriction,
   local source generation, one- versus two-incoming-face cases, chosen polynomial weights, and
   the precise local matrix.
7. Fix the conclusion and norm. A local-system unisolvence theorem, global solvability theorem,
   stability bound, pointwise error, integral-observable error, convergence rate, or iteration count
   requires different hypotheses and cannot be inferred from a table.
8. Fix exact versus floating-point arithmetic, solvers and stopping rules, acceleration, fixups,
   cost claims, and the boundary between proof and experiment.
9. Freeze ordered binders, hypotheses, degenerate cases, foundation/TCB/computation profiles,
   minimal imports, expression/environment fingerprints, checked transports, and statement
   mutations.

## Boundary cases

The statement phase must decide empty meshes; zero-area, collinear, overlapping, hanging, or
inconsistently oriented cells; zero or one polynomial degree; malformed interpolation points;
singular local matrices; zero streaming direction; tangent characteristics; one or two incoming
faces; vacuum, inflow, reflective, and periodic boundaries; vanishing or discontinuous
coefficients; pure absorption versus scattering/fission; zero source and flux; negative flux;
optically thick regions; non-polynomial tests; exact versus numerical quadrature; and mesh
refinement outside the regular triangular family.

No case is excluded at intake. Assuming nonsingularity, stability, consistency, or the desired
error bound as a field would be circular if the selected root is meant to establish it.

## Neighbor and substitution exclusions

- `THM-M-1461` finite element method, `THM-M-1462` Galerkin method, and `THM-M-1463`
  Petrov-Galerkin method are separate catalog targets and provide no inherited statement or proof.
- `THM-M-1465` finite differences and `THM-M-1466` finite volumes are distinct discretization
  families; observed conservation or convergence there cannot be transferred.
- Generic Lax-Milgram solvability does not construct a mesh, broken space, trace, numerical flux,
  penalty, transport sweep, or DG error estimate.
- An affine triangle, a piecewise integral identity, polynomial dimension count, local matrix
  inverse, or assumed coercivity is substrate, not the source-selected root.
- A modern symmetric interior-penalty, local DG, Runge-Kutta DG, or conservation-law theorem cannot
  silently replace the Reed-Hill transport scheme, and conversely.
- A numerical table, residual, plot, solver run, API check, theorem-name match, or the catalog's
  `已验证` label supplies no H or M credit.

## Formal and execution boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, affine simplices and
opposite faces are defined; Bochner integrals support a checked piecewise-set decomposition; and
Lax-Milgram supplies a continuous equivalence for a coercive bounded bilinear form on a complete
real inner-product space. A bounded exact-topic search found no Reed-Hill, discontinuous Galerkin,
finite-element, numerical-flux, or broken-polynomial terminal theorem in pinned mathlib or the
repo-local Lean sources. This is intake discovery, not the required exhaustive anchor audit or a
global absence proof.

The statement phase must first replace the catalog method label with an independently reviewed,
source-selected proposition. Later phases own candidate audit, obligation freezing, typed graphs,
proof bodies, composition, trust closure, readable reconstruction, and release evidence.
