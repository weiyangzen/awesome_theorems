# Scope map

## Included theorem family

- A `2n`-dimensional symplectic manifold and `n` smooth first integrals.
- Pairwise vanishing Poisson brackets and independence of differentials at a regular common level.
- A compact connected component of that regular common level set.
- The Liouville-Arnold conclusion: invariant torus structure and an action-angle normal form on an
  appropriate neighborhood, exactly as supported by the selected source theorem.

## Decisions deferred to statement phase

The exact source must decide differentiability, completeness of Hamiltonian vector fields,
connectedness and compactness, the meaning of independence, whether the conclusion is only that the
level component is diffeomorphic to a torus or includes a saturated neighborhood, and the precise
action-angle coordinate and Hamiltonian normal-form claims. It must also settle `n = 0`, empty or
singular levels, noncompact fibers, global monodromy, and boundary assumptions.

## Explicit exclusions

- Treating "integrable system" as a definition whose desired conclusion is stored as a field.
- Replacing Liouville integrability by solvability of a particular ODE or Lax equation.
- Claiming global action-angle coordinates without the hypotheses that remove monodromy and other
  global obstructions.
- Substituting the Arnold-Liouville theorem with KAM theory, algebraic complete integrability, or
  quantum integrability.
- Treating the Stage0 label `已验证` as source, Lean, or proof evidence.

The formal target must use concrete symplectic, differential, Poisson-bracket, regular-level, torus,
and local-coordinate interfaces, or state an exact missing-API blocker.
