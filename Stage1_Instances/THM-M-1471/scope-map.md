# THM-M-1471 scope map

## Preserved repository scope

- Target identity: `THM-M-1471`, named `先验误差估计` (a priori error estimate).
- Catalog attribution and date: many mathematicians, twentieth century.
- Literal gloss: `数值解的收敛阶` (the convergence order of a numerical solution).
- Subject boundary: convergence-order or error estimates established before observing a computed
  solution, within numerical analysis.

This is all the mathematical scope fixed by the repository. It does not determine a proposition.

## Candidate theorem families not credited

1. Cea quasi-optimality for a source-selected coercive Galerkin problem.
2. An interpolation-derived `h`, `p`, or `hp` finite-element error estimate.
3. A consistency, stability, or global convergence-order theorem for one finite-difference or
   finite-volume scheme.
4. A local or global truncation-error estimate for one ODE or time-stepping method.
5. An algebraic, exponential, or spectral convergence estimate for a selected spectral method.
6. A contraction-iteration a priori estimate or generic asymptotic-order lemma.

These are separate possible roots, not an accepted conjunction or interchangeable special cases.

## Decisions required before statement freeze

An approved target correction must select one immutable source proposition and freeze:

1. The continuous problem or equation, exact solution, domain, initial and boundary data, and the
   scalar, function, normed, or inner-product spaces involved.
2. The numerical method: discrete spaces, mesh, grid, stencil, quadrature, basis, flux, projection,
   time integrator, recurrence, or algebraic solve, and the exact discrete-solution predicate.
3. The approximation or refinement parameter, its admissible values and limiting filter, and
   whether space, time, polynomial degree, or multiple parameters vary.
4. Every regularity, approximation, consistency, stability, coercivity, continuity, mesh-quality,
   and well-posedness hypothesis, including constants and their dependencies.
5. The error functional and norm and the exact conclusion: an explicit inequality, big-O bound,
   limit, quasi-optimality statement, or named order, with the rate exponent and quantifier order.
6. Whether constants are existential or explicit and uniform over solutions, data, meshes, and
   parameters, plus exact versus floating-point arithmetic and computational boundaries.
7. Ordered binders, universes, minimal Lean imports, foundation/TCB/computation profiles, alternate
   encodings, checked transports, statement mutations, and excluded degenerate cases.

Each choice changes truth conditions and proof obligations. This list is a resolution checklist,
not a canonical claim.

## Boundary and degenerate cases

Source review must decide zero error, an exact discrete solution, zero or negative step size,
empty or singleton discrete spaces, zero-dimensional or degenerate domains, singular or
inconsistent discrete problems, nonsmooth exact solutions, nonconforming or anisotropic meshes,
unstable regimes, multiple refinement parameters, zero or nonintegral claimed order, constants
that depend on the refinement parameter, finite refinement sequences, and roundoff or solver error.

No case is excluded at intake because no proposition has been selected.

## Neighbor and substitution exclusions

- `THM-M-1461` finite elements, `THM-M-1465` finite differences, and `THM-M-1466` finite volumes
  are method-family targets and grant no statement or proof credit here.
- `THM-M-1468` hp finite elements and `THM-M-1469` adaptive finite elements are separately owned;
  their rates cannot silently become this root.
- `THM-M-1470` a posteriori estimates use computed-solution information and are not interchangeable
  with this target.
- `THM-M-1472` Lax equivalence is a separately cataloged consistency-stability-convergence result;
  it cannot silently become this root.
- Generic big-O notation, Lax-Milgram solvability, orthogonal projection minimality, a Taylor
  remainder, or a contracting-map estimate alone cannot substitute for an unfrozen numerical
  error theorem.
- Assuming the desired error estimate as data or showing a finite convergence plot supplies no
  theorem closure. The catalog's `已验证` label and the discovery probe supply no H or M credit.

## Formal boundary and handoff

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` exposes generic big-O
semantics, real coercive variational solvability, and Hilbert-space best approximation. A bounded
search found no declaration selecting the catalog's numerical problem, method, error, or rate in
pinned mathlib or tracked repo-local Lean. This is intake discovery only, not an exhaustive anchor
audit or a global absence proof.

The statement phase must first replace the catalog result-family gloss with an independently
reviewed, source-selected truth-valued proposition. Only later phases may freeze a formal target,
obligations, typed graphs, proof bodies, composition, trust closure, or completion state.
