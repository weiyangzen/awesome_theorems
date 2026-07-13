# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-1475`, the title `龙格-库塔法的稳定性`, the gloss
`RK方法的稳定性区域`, the attribution "many mathematicians," the twentieth century, importance
"high," and the untrusted status `已验证`. This identifies the topic of stability regions for
Runge-Kutta methods. It does not identify one theorem.

## Proposition-changing decisions

Before an exact source statement can be frozen, an approved statement run must fix:

- the exact result: a definition, amplification recurrence, general stability-function formula,
  region characterization, equality or inclusion for one method, boundary theorem, or another
  source-named claim;
- the Runge-Kutta scheme: stage count, coefficient matrix, weights and nodes, explicit or implicit
  convention, named tableau if any, and stage/update equations;
- the problem class: the scalar complex test equation, a diagonalizable or arbitrary linear
  system, a nonlinear ODE, or another source-defined class;
- the stability notion: absolute stability, A-, L-, A(alpha)-, B-, algebraic, contractive,
  monotonicity, internal, or another definition, including its relation to neighboring targets;
- the scalar and parameter conventions: real or complex lambda, step h, z = h * lambda, positive,
  zero, negative, fixed, or variable steps, and exact versus floating-point arithmetic;
- for an implicit tableau, the domain of the amplification function, invertibility of `I - z A`,
  poles, singular cases, and whether the function is polynomial, rational, or partially defined;
- the stability predicate: modulus, norm, spectral radius, power boundedness, asymptotic decay, or
  another source criterion, with strict or non-strict boundary and finite- or infinite-time scope;
- the exact quantifier order, typeclass assumptions, directions of implications/equivalences,
  constants and dependencies, and every exceptional case.

These choices yield materially different propositions. The list is a resolution ledger, not a
canonical statement.

## Candidate branches not credited

An eventual reviewed source may select one of these roots, but none is asserted here:

- derive the amplification recurrence for a source-selected RK tableau on `y' = lambda y`;
- derive the general-tableau stability function on the domain where the stage system is solvable;
- identify the absolute-stability region as the source-defined sublevel set of that function;
- compute or characterize the region of explicit Euler, implicit Euler, midpoint, Heun, RK4,
  Gauss, Radau, or another named scheme;
- prove a stability-region inclusion, boundary parametrization, boundedness, or polynomial/rational
  property; or
- relate scalar absolute stability to a sourced linear-system or nonlinear stability theorem.

## Neighbor ownership and explicit exclusions

- `THM-M-1396` owns the broader Runge-Kutta method/numerical-integration family and explicitly
  leaves stability regions to this target. Its statement or evidence is not inherited.
- `THM-M-1474` owns von Neumann stability analysis. `THM-M-1476`, `THM-M-1477`, and
  `THM-M-1478` separately own stiff, A-, and L-stability. None may silently replace this root.
- A general amplification-function formula, stability-region definition, or named-method region
  chosen from memory cannot replace an accepted source proposition.
- A structure or hypothesis that stores the desired stability conclusion cannot be projected as a
  proof. A region plot, sampled grid, numerical trajectory, floating-point experiment, or unchecked
  symbolic inverse cannot serve as theorem evidence.
- Generic ODE existence, Picard iteration, Gronwall estimates, finite-matrix operations, complex
  norms, and rational-function evaluation are substrate, not an RK stability theorem.
- The catalog label `已验证`, a bibliography or URL, the API probe, and a bounded no-match search
  grant no source-fidelity or machine-proof credit.

## Boundary cases

The statement phase must explicitly decide zero stages, empty finite index types, degenerate or
inconsistent tableaux, zero or negative steps, `lambda = 0`, `z = 0`, zero initial value, singular
stage systems and poles, boundary points with modulus exactly one, repeated or defective matrix
eigenvalues, unbounded powers despite spectral information, fixed versus variable steps, finite
versus infinite horizons, and exact versus floating-point evaluation.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib has finite matrices and matrix-vector
products, complex scalars and norms, rational-function evaluation, and analytic ODE predicates.
Those interfaces can support a future definition after source selection; they do not select the
tableau, stability notion, source claim, or proof. The statement phase must admit and review one
immutable source proposition, implement every incorporated definition, minimize imports,
elaborate and fingerprint the exact target, add checked transports, and mutation-test removed
hypotheses, domains, binder scope, and boundary cases.
