# Scope map

## Included subject

- A covering map `p : E -> X` between topological spaces.
- One or two continuous lifts into `E` whose composites with `p` are the same base map.
- An initial-value equality, or a specified point in the fiber, that determines the lift.
- The connectedness assumptions on the lift domain needed to propagate equality.

The repository's own statement gloss, `覆盖空间的提升唯一性` (uniqueness of lifting for covering
spaces), controls this scope. The title alone is not used to substitute the unrelated
uniformization theorem for Riemann surfaces.

## Decisions required before statement closure

The statement phase must select and cite an exact source variant. In particular, it must decide
whether the root is uniqueness of a lifted path after fixing its starting point, equality of two
lifts from a connected or path-connected space after equality at one point, or the uniqueness
clause of a lift-existence theorem. It must preserve the source's separation, local triviality,
continuity, nonemptiness, connectedness, endpoint, and basepoint conditions and all universe/binder
scope. These variants are related but are not interchangeable exact statements.

## Explicit exclusions

- Analytic uniformization of simply connected Riemann surfaces.
- The covering-space lifting criterion or existence theorem in place of uniqueness alone.
- Homotopy lifting, unique path lifting, or monodromy endpoint invariance as an unmarked substitute
  for a more general selected root.
- A statement for arbitrary local homeomorphisms unless all separation hypotheses needed for
  uniqueness are retained.
- Any theorem that assumes the desired equality of lifts as input.
