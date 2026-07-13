# THM-M-1477 scope map

## Preserved repository scope

The literal repository boundary is the label `A-稳定性`, glossed only as `数值方法的稳定性` and
attributed to Germund Dahlquist in 1963. This identifies a numerical-stability subject family. It
does not select one mathematical proposition.

A common one-step formulation calls a method A-stable when its absolute-stability region contains
the closed left half-plane, often expressed through a stability function `R` by
`Re z <= 0 -> |R z| <= 1`. A linear multistep formulation instead uses the roots of a
parameterized characteristic polynomial `rho(zeta) - z * sigma(zeta)`, including multiplicity
conditions on roots of unit modulus. A theorem about the maximum order of an A-stable multistep
method is different again. None of these candidates is selected at intake.

## Decisions required at statement freeze

1. Select an immutable source proposition and decide whether the root is a definition/property,
   characterization, example, impossibility or order-barrier theorem, or another exact result.
2. Fix the method class: one-step, Runge-Kutta, general linear, or linear multistep; for a concrete
   method, fix every tableau, coefficient, step, stage, and recurrence convention.
3. Fix the scalar test equation, complex parameter, step scaling, and sign convention, and state
   how this model relates to the intended method and any broader ODE problem.
4. Fix the stability representation: stability function, rational function, polynomial pair,
   characteristic equation, amplification operator, or source-identical alternative.
5. Fix the stability region and logical direction: open or closed left half-plane, inclusion versus
   equality, denominator poles, root locations, unit-circle multiplicities, and boundary behavior.
6. Fix all consistency, zero-stability, irreducibility, order, real/complex coefficient, positivity,
   nondegeneracy, and regularity assumptions, including their quantifier order.
7. Fix the exact conclusion. An A-stability predicate, a proof that one method is A-stable, a
   characterization, and the Dahlquist order barrier are proposition-changing alternatives.
8. Fix exact versus floating-point arithmetic, universes, foundation/TCB/computation profiles,
   minimal imports, expression fingerprints, checked transports, and all statement mutations.

## Boundary and degenerate cases

The statement phase must decide zero and negative step sizes; the test parameter `z = 0`; equality
on the imaginary axis and unit circle; poles of a rational stability function; identically zero or
constant numerator/denominator polynomials; common polynomial factors; repeated roots; roots at
zero and infinity; empty or degenerate tableaux; real versus complex coefficients; explicit versus
implicit methods; order zero, one, and two; finite versus asymptotic parameter behavior; and exact
versus floating-point evaluation.

No case is excluded at intake. Assuming the desired half-plane inclusion, root condition, or order
bound as a structure field would be circular if the selected root is meant to establish it.

## Candidate statements not credited

- The definition that a source-selected one-step method is A-stable exactly when its stability
  region contains the closed left half-plane.
- A stability-function condition `forall z, Re z <= 0 -> norm (R z) <= 1`, with source-selected
  domain, pole, and sign conventions.
- A root-condition definition or characterization for a selected linear multistep polynomial pair.
- A theorem that implicit Euler, the trapezoidal rule, or another concrete method is A-stable.
- The second Dahlquist barrier: an A-stable linear multistep method has order at most two, under its
  complete source assumptions.
- A Runge-Kutta algebraic stability criterion or another sufficient condition implying A-stability.

These are inequivalent or differently scoped statements. Intake admits none without an accountable
source decision and independent review.

## Neighbor and substitution exclusions

- `THM-M-1475` separately owns Runge-Kutta stability regions and cannot silently select this root.
- `THM-M-1476` separately owns stiff stability; A-stability may be relevant but is not identical.
- `THM-M-1478` separately owns L-stability, which normally adds a strong-decay condition and cannot
  be substituted for A-stability.
- `THM-M-1472`, `THM-M-1473`, and `THM-M-1474` separately own Lax equivalence, CFL, and von Neumann
  finite-difference stability analysis.
- A stable scalar recurrence, an implicit-Euler worked example, a plotted stability region, sampled
  complex points, or successful floating-point experiment does not establish an unidentified
  general target.
- Generic polynomial evaluation, complex norm, root, spectrum, or metric-region infrastructure is
  substrate only. The untrusted `已验证` label and theorem-name matches supply no H or M credit.

## Formal and execution boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Polynomial.eval` and
`Polynomial.eval₂` evaluate polynomials, `Complex.normSq` exposes squared complex norm, and
`Metric.mem_closedBall` characterizes metric balls. They do not define a numerical method,
stability function, multistep polynomial pair, A-stability predicate, or order-barrier theorem.

A bounded exact-topic search found no source-selected numerical A-stability declaration in pinned
mathlib or repo-local Lean. This is intake discovery, not an exhaustive anchor audit or a global
absence proof. Later phases own exact statement selection, candidate provenance, obligation
freezing, typed graphs, proof bodies, composition, trust, readable reconstruction, and release
evidence.
