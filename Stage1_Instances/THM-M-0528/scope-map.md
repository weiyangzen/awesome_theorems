# Scope map

## Included subject

- A covering map `p : E -> X` between topological spaces.
- One or two continuous lifts into `E` whose composites with `p` are the same base map.
- An initial-value equality, or a specified point in the fiber, that determines the lift.
- The connectedness assumptions on the lift domain needed to propagate equality.

The repository's own statement gloss, `覆盖空间的提升唯一性` (uniqueness of lifting for covering
spaces), controls this scope. The title alone is not used to substitute the unrelated
uniformization theorem for Riemann surfaces.

## Statement selection

The statement phase selects equality of two continuous lifts from a `PreconnectedSpace` after
equality at one explicitly bound point. The projection is an `IsCoveringMap`; equality of
composites is the canonical encoding, with a checked transport to pointwise projection equality.
Path-lift uniqueness and the uniqueness clause of a lift-existence theorem remain related but
excluded variants.

## Explicit exclusions

- Analytic uniformization of simply connected Riemann surfaces.
- The covering-space lifting criterion or existence theorem in place of uniqueness alone.
- Homotopy lifting, unique path lifting, or monodromy endpoint invariance as an unmarked substitute
  for a more general selected root.
- A statement for arbitrary local homeomorphisms unless all separation hypotheses needed for
  uniqueness are retained.
- Any theorem that assumes the desired equality of lifts as input.
