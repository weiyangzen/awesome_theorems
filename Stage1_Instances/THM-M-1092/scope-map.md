# Scope map

## Included claim

- A time-homogeneous continuous-time Markov transition family `P_t` on a state space fixed by the
  selected source, with an infinitesimal generator `A` and an explicit domain for `A`.
- The backward equation, conventionally `d/dt (P_t f) = A (P_t f)`, with the generator acting at
  the initial-state side (equivalently `∂_s P_{s,t} = -A_s P_{s,t}`).
- The forward equation, conventionally `d/dt (P_t f) = P_t (A f)`, or its adjoint/kernel-density
  form, only when the source hypotheses make that expression meaningful.
- Initial condition `P_0 = id`, and all measurability, integrability, semigroup, conservativity,
  differentiability, boundary, and density hypotheses actually used by the chosen theorem.

## Decisions deferred to the statement phase

The exact source must decide finite/countable/general state space; transition matrix, Markov kernel,
semigroup, or density presentation; row/column convention; strong versus pointwise derivative;
generator/core domain; explosion and boundary conditions; reference measure and adjoint existence;
and whether the forward and backward results form one conjunction or two separately typed roots.
Binder order, universes, time domain, and degenerate `t = 0` behavior must follow those decisions.

## Explicit exclusions

- Discrete-time Chapman-Kolmogorov composition alone.
- A finite-state matrix identity substituted for a source theorem stated for transition densities,
  unless it is explicitly represented later as a scoped special-case child.
- The Fokker-Planck equation without a proved identification with the selected forward equation.
- A structure or hypothesis that contains both desired differential equations as fields.
- Mere differentiability of an arbitrary function or a formal rearrangement with no Markov model.

The exact Lean statement must expose a concrete transition family, generator and derivative notion;
otherwise the statement phase must record the missing mathlib API rather than weaken the claim.
