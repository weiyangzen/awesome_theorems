# Scope map

## Included claim

- A continuous-time Markov transition family `P_t` on a state space fixed by the selected source,
  with an infinitesimal generator `A` and an explicit domain for `A`.
- The backward equation with the generator acting on the initial-state side. In a transition-density
  presentation this is conventionally `d/dt p(t,x,y) = A_x p(t,x,y)`; in an operator presentation
  it is the corresponding derivative identity for `P_t f`.
- The identity initial condition at time zero and the Markov/Chapman-Kolmogorov structure needed to
  make `P_t` a transition family.
- Every measurability, integrability, continuity, differentiability, conservativity, non-explosion,
  boundary, and generator-domain hypothesis used by the selected primary theorem.

## Decisions deferred to the statement phase

The exact source must decide finite, countable, Euclidean, or general state space; homogeneous or
two-parameter transition family; transition operator, kernel, matrix, or density presentation;
row/column and generator sign convention; strong, weak, or pointwise derivative; generator/core
domain; boundary behavior; reference measure; and whether the equation is asserted at `t = 0` or
only for positive time. Binder order, universes, and degenerate cases must follow those decisions.

## Explicit exclusions

- The Kolmogorov forward equation or Fokker-Planck equation as a substitute for the backward one.
- Discrete-time Chapman-Kolmogorov composition alone.
- A finite-state matrix special case substituted for a primary theorem with a broader state space.
- A structure, premise, or generator definition that contains the desired derivative identity as
  data.
- An arbitrary semigroup differentiation identity with no checked Markov-transition interpretation.

The later Lean statement must expose a concrete transition family, generator, generator domain, and
derivative notion. If the pinned libraries lack those interfaces, the statement phase must record
that exact API blocker rather than weaken or replace the claim.
