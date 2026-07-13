# THM-M-1476 scope map

## Preserved catalog scope

- Target identity: `THM-M-1476`, named `刚性稳定性`.
- Literal gloss: `刚性问题的数值稳定性` (numerical stability of stiff problems).
- Catalog attribution and period: many mathematicians, twentieth century.
- Recognizable boundary: stability of numerical treatment in a stiff-problem regime.

This is a topic family, not one proposition. Intake preserves that ambiguity rather than silently
adopting a familiar definition.

## Proposition-changing decisions

An accountable source correction must select one immutable proposition and freeze:

1. The meaning of stiffness: separated decay scales, a spectral or Jacobian condition, a
   stability-versus-accuracy step restriction, singular perturbation, or another source definition.
2. The problem class: scalar or system, real or complex, autonomous or nonautonomous, ODE, DAE,
   PDE, initial or boundary value, linear or nonlinear, and the exact solution concept.
3. The numerical-method family: one-step, Runge-Kutta, general linear, multistep,
   multiderivative, BDF, extrapolation, or one named scheme, with all coefficients and recurrences.
4. The stability notion: stiff stability, absolute stability, A-, A(0)-, A(alpha)-, L-, B-,
   algebraic, contractive, decay, power-boundedness, order reduction, or another defined property.
5. The analytic setting: state space, scalar field, norm, interval, initial data, regularity,
   dissipativity, spectral/Jacobian assumptions, solvability, and uniqueness.
6. The discrete parameters: fixed or variable steps, stage/order conventions, starting values,
   admissible parameter region, singular systems and poles, and finite or infinite time horizon.
7. The conclusion and logical direction: a bound, implication, equivalence, region inclusion,
   asymptotic decay, convergence statement, barrier theorem, or conjunction, with every constant
   and dependency.
8. The arithmetic and solver boundary: exact arithmetic, floating point, implicit-solve relation,
   iteration tolerance, oracle or certificate policy, and failure semantics.
9. Ordered binders, quantifier scope, strict versus non-strict inequalities, alternate encodings,
   degenerate cases, foundation, TCB, computation, and freshness profiles.

Each choice changes the target's truth conditions and proof obligations. This list is a resolution
ledger, not a candidate statement.

## Candidate families not credited

- A source-defined stiff-stability property for a multistep or multiderivative method.
- A relation between stiff stability and a source-defined A-stability variant.
- Stability of a selected implicit one-step or Runge-Kutta scheme on a stiff test family.
- Stability or decay of a selected BDF method under exact coefficient and step assumptions.
- A stiffness-uniform error, contractivity, or order-reduction theorem for a selected problem and
  method.

No candidate is selected, combined, or credited at intake.

## Neighbor ownership and exclusions

- `THM-M-1398` owns the broader stiff-equation numerical-solution topic.
- `THM-M-1399` owns backward differentiation formulas.
- `THM-M-1474` owns von Neumann stability analysis.
- `THM-M-1475` owns Runge-Kutta stability regions.
- `THM-M-1477` and `THM-M-1478` separately own A-stability and L-stability.

None of these targets contributes a statement, source, or proof receipt to this one. In particular,
implicit Euler, the Dahlquist scalar test equation, a generic amplification-function definition,
A-stability, L-stability, or one BDF/RK theorem cannot be substituted because it is convenient.
Generic ODE existence, Gronwall, trajectory comparison, complex exponential, matrix, or spectral
infrastructure is substrate only. Definitions, stability diagrams, sampled regions, numerical
experiments, floating-point runs, and structures that assume the desired result supply no theorem
credit. The catalog's `已验证` label supplies no H or M evidence.

## Boundary cases

Source review must decide zero or negative step size, empty or reversed intervals, zero-dimensional
state, zero initial value, zero or purely imaginary modes, repeated or defective eigenvalues,
singular Jacobians or stage systems, nonunique exact or implicit solutions, poles, boundary points
with amplification norm exactly one, transient growth, fixed versus variable steps, initialization,
finite versus infinite horizons, and exact versus inexact arithmetic. Intake silently excludes none
of them.

No canonical Lean target, checked transport, expression fingerprint, discovery protocol,
obligation registry, or proof state is frozen in this phase.
