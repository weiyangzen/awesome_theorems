# Scope map

## Preserved repository scope

The repository identifies Newton iteration as a quadratically convergent equation root-finding
method. This intake preserves that Newton root-convergence family and the distinction from
optimization, secant, bisection, and generic fixed-point methods. Local convergence is one
conservative future scope candidate, not a source-derived clause. No exact proposition is inferred
from the slogan.

## Proposition-changing decisions

An approved source correction must freeze:

- the scalar real, scalar complex, finite-dimensional, or Banach-space carrier, the root equation,
  domain and codomain, norm/topology, universes, and typeclass data;
- the regularity class of `f`, the derivative notion, a specified root `a`, root simplicity or
  derivative invertibility, and the exact neighborhood on which derivative and remainder bounds
  hold;
- the Newton update convention, including division or inverse orientation, behavior outside its
  domain, initial point, iterate indexing, and proof that every iterate is well-defined and remains
  in the approved neighborhood;
- the exact conclusion: root existence or a given root, local convergence, uniqueness in a
  neighborhood, a one-step quadratic error estimate, Q-order two, an asymptotic ratio, big-O, an
  iteration-complexity result, or an exact conjunction;
- the constants, their positivity and uniformity, quantifier order, convergence mode, whether the
  estimate holds for all or sufficiently large indices, and whether convergence is a conclusion
  or a premise; and
- exact versus finite-precision arithmetic, stopping rules, alternate encodings and checked
  transport directions, logical profiles, and every boundary case.

These decisions yield inequivalent propositions. They are a resolution checklist, not a canonical
statement.

## Candidate families not credited

- Local scalar convergence near a simple root under a continuous or Lipschitz derivative.
- A stronger `C^2` theorem yielding a uniform one-step error constant.
- A Newton-Kantorovich theorem in Banach spaces with an invertible Fréchet derivative.
- A polynomial-only theorem using mathlib's ring-theoretic `Polynomial.newtonMap`.
- A finite-precision solver theorem with residual, rounding, stopping, or complexity bounds.

No family in this list is selected or credited at intake.

## Explicit exclusions

- A global or every-start convergence theorem silently selected without source authorization.
- An ordinary multiple-root case silently assigned a quadratic rate without an additional
  modified-Newton construction.
- Damped Newton, line search, trust-region Newton, quasi-Newton, or secant variants.
- Hessian-based optimization Newton, separately cataloged as `THM-M-1500`.
- Secant, bisection, fixed-point iteration, or Banach fixed-point results (`THM-M-1441` through
  `THM-M-1444`).
- A theorem that assumes the desired convergence, quadratic estimate, invariant neighborhood, or
  denominator well-definedness as an unexplained structure field.
- A numerical experiment, finite trajectory, plot, theorem name, `#check`, or untrusted `已验证`
  label presented as a general convergence proof.

## Degenerate and boundary scope

The statement phase must decide constant and linear functions; zero and identically zero
functions; simple versus multiple roots; derivative zero at the root or an iterate; an initial
point equal to the root; starting points inside, on, or outside the convergence neighborhood;
iterates leaving the domain; multiple nearby roots; complex versus real norms; a zero quadratic
constant; eventual versus all-index estimates; convergence without exact Q-order two; exact versus
rounded arithmetic; and the junk-value convention used by mathlib when a polynomial derivative
value is not a unit. No case is silently excluded at intake.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.Dynamics.Newton` exposes the polynomial
Newton map and root/fixed-point and nilpotent results checked by `IntakeProbe.lean`. The bounded
search located no source-identical analytic quadratic-convergence declaration. These observations
are discovery inputs only, not a statement gate, anchor audit, or proof.
