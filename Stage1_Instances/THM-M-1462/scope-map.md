# Scope map

## Preserved theorem family

The intake preserves Galerkin projection methods for variational approximation as the named family.
A common candidate framework would use a Hilbert or energy space `V`, a trial subspace `V_h`, a
bilinear or sesquilinear form `a`, a functional `f`, an exact solution `u`, and a discrete solution
`u_h` tested against `V_h`. This framework is explanatory only. The repository does not specify it,
and no component below is credited as the canonical theorem.

## Candidate result families not credited

- Galerkin orthogonality: `a (u - u_h) v_h = 0` for every `v_h` in the trial/test subspace.
- In a symmetric inner-product setting, identification of `u_h` with an orthogonal projection and
  a best-approximation property.
- Existence and uniqueness of the continuous or discrete variational solution under boundedness and
  coercivity assumptions.
- Cea quasi-optimality, with its exact continuity and coercivity constants and error norm.
- Convergence for a dense or nested family of spaces, possibly with an approximation rate.
- Correctness of a spectral, finite-element, or other application-specific Galerkin scheme.

These are inequivalent propositions. Selecting one from the phrase "projection method" would add
mathematics absent from the source record.

## Decisions required at statement freeze

1. The immutable source edition, pinpoint result and incorporated definitions, proof boundary,
   correction history, and independent review.
2. Whether the root is orthogonality, best approximation, solvability, quasi-optimality,
   convergence, an application theorem, or an explicitly checked conjunction.
3. Real or complex scalars; vector, Hilbert, Sobolev, or energy spaces; universes and typeclass
   assumptions; and bilinear versus sesquilinear argument orientation.
4. The continuous trial space, discrete trial and test spaces, inclusion or nonconformity,
   finite-dimensionality or closedness, and the approximation-family index.
5. The operator or form, continuity and coercivity constants, symmetry assumptions, right-hand-side
   functional, and whether exact/discrete solution existence is assumed or proved.
6. The exact discrete equation, residual/orthogonality convention, error norm, infimum or attained
   best approximation, constants, convergence mode, and any approximation rate.
7. Ordered binders, hypotheses, conclusion, alternate encodings and checked transports, foundation
   profile, and exact-arithmetic versus numerical-computation boundary.

## Boundary and degenerate cases

Source review must dispose of the zero space and zero-dimensional trial space; the full-space trial
case; zero and nonzero functionals; zero, degenerate, nonsymmetric, noncoercive, or merely inf-sup
stable forms; vanishing or nonpositive coercivity constants; empty approximation families; exact
solutions already in the discrete subspace; nonclosed or nonconforming spaces; nonunique solutions;
complex conjugation orientation; and whether an infimum is attained. Any mesh, basis, quadrature,
rounding, conditioning, or implementation claim requires separate hypotheses and evidence.

## Substitution exclusions

- Lax-Milgram alone is not a Galerkin approximation theorem.
- A generic orthogonal projection theorem alone does not supply the source's missing variational
  problem, discretization, or selected conclusion.
- Assuming a discrete solution already satisfies Galerkin orthogonality cannot replace proving its
  construction or correctness when that is part of the selected result.
- Cea's lemma cannot be stated without exact boundedness/coercivity premises and constants.
- Petrov-Galerkin (`THM-M-1463`), discontinuous Galerkin (`THM-M-1464`), and the finite-element
  method (`THM-M-1461`) remain separate targets and share no statement or proof credit.
- Ritz methods, collocation, least squares, spectral methods, finite differences, and finite volumes
  are not interchangeable merely because they can involve projection or residual conditions.
- A numerical experiment, sampled residual, convergence plot, tolerance result, or executable
  solver is not an exact theorem proof.
- The repository label `已验证` is not human-source or Lean kernel evidence.

No canonical Lean target, expression fingerprint, checked alternate encoding, discovery protocol,
obligation registry, or proof state is frozen at intake.
