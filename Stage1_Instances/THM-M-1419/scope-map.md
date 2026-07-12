# Scope map

## Included theorem family

- A probability space with a measurable, measure-preserving base transformation, with ergodicity
  included only if required by the selected source form.
- A measurable cocycle of finite-dimensional real linear maps or matrices, formed by ordered
  products along the base dynamics.
- Logarithmic integrability hypotheses on the one-step norm and, for a two-sided splitting form,
  on the inverse norm.
- Almost-everywhere existence of finitely many Lyapunov growth rates, together with the invariant
  filtration or direct-sum splitting needed to say which nonzero vectors realize each rate.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary theorem. It must freeze: probability
versus finite measure; invertible versus one-sided base dynamics; `GL(d, R)` versus possibly
singular endomorphisms; real versus complex scalars; fixed versus measurable fiber dimension;
strong measurability; the exact `log+` moment assumptions for the cocycle and inverse; forward or
two-sided product convention; filtration versus splitting; deterministic exponents under
ergodicity versus invariant exponent functions; multiplicities; exceptional null sets; and whether
the limit is stated for vector norms, singular values, exterior powers, or all of these.

Quantifier order must cover all relevant nonzero vectors without silently choosing a separate null
set for each vector. Boundary behavior for zero vectors, zero or repeated exponents, singular
matrices, zero-dimensional fibers, nonergodic bases, and nonintegrable cocycles must be explicit.

## Explicit exclusions

- Kingman's subadditive ergodic theorem alone, the scalar Birkhoff theorem, or existence of only the
  top exponent as a substitute for the selected multiplicative theorem.
- A constant-matrix spectral-radius result, deterministic matrix-product estimate, or numerical
  approximation of Lyapunov exponents.
- A theorem assuming the Oseledets filtration, splitting, exponents, or desired limits as fields of
  an input structure.
- The separately scheduled `THM-M-1056` statement boundary or its checked support lemmas as proof
  of this target.
- The metadata word `已验证` as human-source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose the cocycle,
measurability, integrability, almost-everywhere limit, invariant subspaces, and multiplicities rather
than package the desired conclusion as an assumption.
