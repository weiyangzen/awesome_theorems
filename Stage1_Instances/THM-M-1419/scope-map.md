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

## Statement-freeze decisions

The selected formal target freezes: probability measure; invertible ergodic base; almost-everywhere
invertible real `d x d` matrices for positive fixed `d`; a.e. strong measurability of the matrix and
inverse; `log+` integrability of both operator norms; forward products; a direct-sum splitting;
constant strictly decreasing exponents; multiplicity as subspace finrank; and actual vector-norm
growth limits on one common conull set. Subspace-field measurability is expressed through distance
to each fiber.

The quantifier order covers all relevant nonzero vectors without choosing a separate null set per
vector. Zero vectors are excluded from the logarithmic limit, repeated exponents are consolidated
into a single higher-rank subspace, and singular matrices, zero-dimensional fibers, nonergodic
bases, and nonintegrable cocycles are outside this selected variant.

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
