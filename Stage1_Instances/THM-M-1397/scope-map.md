# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1397`, the label `Adams方法` (Adams method), the gloss
`多步数值方法` (multistep numerical methods), an attribution to John Couch Adams, the year 1883,
and an untrusted `已验证` status. Intake preserves this numerical-ODE method-family boundary. It
does not turn the label into a proposition or select a familiar recurrence or theorem without
source authority.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- whether the root defines a numerical scheme, derives its coefficients, or proves order, local
  truncation error, consistency, convergence, zero-stability, absolute stability, iteration
  convergence, or a predictor-corrector result;
- explicit Adams-Bashforth, implicit Adams-Moulton, or a paired predictor-corrector procedure;
- the step/order parameter and indexing convention, coefficient normalization, number of stored
  history values, constant versus variable step sizes, and sign and nonzero conditions on the step;
- scalar field, state space, norm and completeness structure, ODE domain, autonomous versus
  nonautonomous vector field, exact solution model, and all universe and typeclass data;
- initial time and state, finite or infinite grid, starting history and how it is obtained, target
  interval, endpoint convention, and whether the claimed bound is local or global;
- continuity, differentiability, Lipschitz, bounded-derivative, uniqueness, stiffness, root, or
  spectral hypotheses and the exact norms and uniformity quantifiers;
- for implicit steps, existence and uniqueness of the nonlinear solve and whether an exact solve or
  a finite/fixed-point correction iteration is used; and
- one exact truth-valued conclusion, ordered binders, constants and their dependencies, asymptotic
  convention, exceptional cases, and a complete source and proof boundary.

These choices define inequivalent propositions. They are a resolution ledger, not a canonical
claim. The literal gloss has no quantifier or conclusion: it describes a class of numerical
methods. Intake cannot silently rewrite it as a universal convergence theorem, a recurrence
identity, a coefficient table, or an algorithm specification.

## Candidate families not credited

- The constant-step explicit Adams-Bashforth recurrence obtained by integrating an extrapolating
  polynomial through past derivative values.
- The constant-step implicit Adams-Moulton recurrence obtained from an interpolant that includes
  the new derivative value.
- A predictor-corrector algorithm using an Adams-Bashforth prediction and one or more
  Adams-Moulton corrections, with a separate contraction condition.
- Exact coefficient, degree/order, and local truncation-error formulas for one selected step count.
- A consistency plus zero-stability implies convergence theorem for a selected linear multistep
  encoding, or a direct global error estimate under source-specific regularity assumptions.
- An absolute-stability or root-condition result for the scalar test equation.
- A variable-step, adaptive-order, or stiffness-oriented Adams implementation theorem.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor boundaries and exclusions

- `THM-M-1395` finite-difference methods and `THM-M-1396` Runge-Kutta methods are broader or
  different discretization families; their statements and evidence cannot close this target.
- `THM-M-1398` stiff equations is a problem class, not an Adams theorem. `THM-M-1399` backward
  differentiation formulas are a distinct implicit multistep family.
- Euler and trapezoidal special cases do not by themselves establish a general Adams family result.
- Generic Lagrange interpolation, interval integration, ODE, sequence, polynomial, or finite-sum
  APIs are possible substrate only and receive no target statement or proof credit.
- A recurrence placed in a structure field, a numerical experiment, convergence plot, floating-
  point trajectory, or empirical order estimate is not a proof of a source-selected conclusion.
- Assuming the desired error estimate, stability condition, or solvability in an interface would
  be circular rather than a proof.
- The catalog label `已验证` supplies neither a human proof nor a machine artifact.

## Boundary cases

The statement phase must decide zero steps and zero-order methods; empty or insufficient starting
history; `h = 0` and negative steps; repeated or non-injective grid nodes; final times off the grid;
scalar versus vector states; incomplete spaces; nonsmooth or non-Lipschitz right-hand sides;
solutions leaving the ODE domain; implicit equations with no or multiple solutions; correction
iterations outside their contraction range; exact versus approximate starting values; accumulated
roundoff; variable steps and step-ratio bounds; characteristic roots on the unit circle or with
multiplicity; stiff test equations; uniformity of big-O constants; and finite versus unbounded
integration intervals.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks generic Lagrange interpolation,
interval integral, integral-curve, and finite-sum interfaces. A bounded local topic search found no
numerical Adams-Bashforth, Adams-Moulton, or multistep declaration in pinned mathlib or repo-local
Lean sources; the visible `Adams` occurrences concern unrelated namesakes. This is an intake
discovery observation, not an exhaustive anchor audit or a global absence claim.
