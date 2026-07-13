# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-1478`, the title `L-稳定性`, the gloss `数值方法的稳定性`,
the attribution "many mathematicians," the twentieth century, importance "high," and the
untrusted status `已验证`. This identifies an L-stability topic in numerical analysis. It does not
identify one theorem.

The neighboring catalog record for A-stability has the identical gloss. The distinct titles are
therefore important non-substitution evidence, but they do not themselves define either property
or a relationship between them.

## Proposition-changing decisions

Before an exact source statement can be frozen, an approved statement run must fix:

- the target kind: a definition, equivalence or implication, named-method calculation, existence
  or nonexistence result, order/barrier theorem, parameter characterization, or another exact
  source-named claim;
- the numerical-method class: one-step, Runge-Kutta, general linear, multistep, multiderivative,
  Rosenbrock, extrapolation, or one exact named scheme, including all coefficient data;
- the problem semantics: the scalar complex test equation, a linear system, nonlinear stiff ODE,
  DAE, PDE semidiscretization, or another source-defined class;
- the stability object: amplification factor, polynomial or rational stability function, matrix
  transfer function, recurrence roots, or another source-defined object;
- for Runge-Kutta methods, the stage index, tableau matrix and weights, consistency normalization,
  stage equations, and invertibility domain; for multistep methods, the characteristic polynomials
  and root condition rather than an unjustified scalar one-step stability function;
- the function domain: total versus partial evaluation, finite poles, removable singularities,
  behavior at infinity, eventual pole-free behavior, and how singular stage systems are represented;
- the A-stability component, if any: the selected left half-plane and boundary convention, the
  exact modulus/norm or power-bounded predicate, and whether A-stability is a premise, conjunct,
  derived fact, or separately owned result;
- the decay component, if any: function value versus modulus, target zero, complex-plane
  cocompact filter versus negative-real or left-half-plane paths, uniform versus pointwise decay,
  and the exact quantifier order;
- the logical direction, constants and dependencies, universes, scalar carriers, exact versus
  floating-point arithmetic, and every exceptional case.
- whether stiff accuracy, algebraic stability, B-stability, A(alpha)-stability, or another related
  predicate is excluded, assumed, implied, equivalent, or separately owned rather than conflated
  with L-stability.

These choices yield materially different propositions. This list is a resolution ledger, not a
canonical definition or statement.

## Candidate branches not credited

An eventual reviewed source may select one of these roots, but none is asserted here:

- define L-stability for a source-selected class of scalar stability functions;
- prove that one exact rational stability function is A-stable and has the required decay;
- characterize L-stability of a source-selected Runge-Kutta, SDIRK, Rosenbrock, multistep, or
  multiderivative family by coefficient constraints;
- show a relationship among stiff decay, stiff accuracy, A-stability, and L-stability under exact
  hypotheses; or
- prove an existence, order, or impossibility theorem for a specified method class.

## Neighbor ownership and explicit exclusions

- `THM-M-1396` owns the broader Runge-Kutta method family, and `THM-M-1475` separately owns
  Runge-Kutta stability regions. Their statements and evidence are not inherited.
- `THM-M-1398` owns the broader stiff-equation numerical-solution topic, while `THM-M-1476` owns
  stiff stability. Neither can select this root.
- `THM-M-1477` separately owns A-stability. Even if an admitted definition later incorporates
  A-stability, its statement and proof credit cannot be copied without an exact checked bridge and
  an ownership decision.
- `THM-M-1399` owns backward differentiation formulas. A BDF root-condition or stiff-stability
  result cannot be recast as a scalar one-step L-stability predicate without source authority.
  Backward Euler, Radau, SDIRK, Rosenbrock, or any other convenient method likewise cannot replace
  the unspecified target.
- A predicate or structure that stores L-stability, A-stability, or the requested decay as data
  cannot be projected as a proof of the intended mathematical root.
- A stability-region plot, sampled grid, numerical trajectory, symbolic limit returned without a
  certificate, floating-point experiment, or benchmark cannot serve as theorem evidence.
- Generic complex limits, rational functions, matrices, norms, and ODE APIs are substrate, not an
  L-stability theorem. The untrusted catalog label, bibliography, API probe, and bounded no-match
  search grant no source-fidelity or machine-proof credit.

## Boundary cases

The statement phase must explicitly decide zero-stage or empty-index methods, degenerate or
inconsistent coefficient data, zero and negative steps, zero initial data, `lambda = 0` and
`z = 0`, reduced rational-function poles versus singular stage systems and removable singularities,
zero versus nonzero reduced rational functions, numerator/denominator degrees and leading
coefficients, consistency normalization such as `R(0) = 1`,
the imaginary-axis boundary, strict versus non-strict modulus inequalities, radial versus
arbitrary complex escape, negative-real versus full left-half-plane paths, repeated or defective
matrix eigenvalues, transient growth, finite versus infinite horizons, variable steps, and exact
versus floating-point evaluation.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib has complex numbers and norms,
`Filter.Tendsto`, the cocompact/cobounded filter, rational-function evaluation, finite matrices,
and exact ODE trajectory predicates. Those interfaces can support future definitions after source
selection; they do not select a method, stability function, A-stability predicate, limiting
semantics, claim kind, or proof. In particular, `RatFunc.eval` totalizes a reduced denominator zero
to the field value zero; the source must decide whether the formal object is a reduced rational
continuation, a partial function on its pole-free domain, or an actually solvable implicit stage
system. The statement phase must admit and review one immutable source
proposition, implement every incorporated definition, minimize imports, elaborate and fingerprint
the exact target, add checked transports, and mutation-test removed hypotheses, domains, binder
scope, and boundary cases.
