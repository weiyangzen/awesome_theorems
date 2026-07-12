# Scope map

## Included claim

- A parameter space `B` and a smooth fibration `p : X -> B` with compact fibers, under the exact
  compactness, boundary, and base hypotheses of the selected primary statement.
- Vector bundles over `X` and a continuously/smoothly parameterized family of elliptic operators
  acting fiberwise between their sections.
- The family symbol class and its topological pushforward/index in K-theory of `B`.
- The analytic family index class, formed from the fiberwise Fredholm family rather than a list of
  unrelated numerical indices.
- Equality of the analytic and topological K-theory index classes.

## Decisions deferred to the statement phase

The source inspection must fix whether the theorem uses compact Hausdorff or smooth base spaces,
closed fibers or allows boundary conditions, real or complex bundles and K-theory, graded versus
ungraded operators, pseudodifferential versus differential operators, and the exact symbol and
pushforward models. It must also fix universes, binder order, regularity, orientations, and the
behavior for empty base/fiber, disconnected fibers, a point base, and invertible families.

The cohomological formula involving the Chern character and fiber integration is a consequence or
alternate formulation only if the chosen source explicitly supplies it and a checked bridge to the
K-theoretic equality is constructed.

## Explicit exclusions

- The ordinary Atiyah-Singer theorem for one elliptic operator as a substitute for a family.
- The equivariant `G`-index theorem, local heat-kernel index theorem, or a Dirac-only specialization
  unless selected as the exact sourced root rather than silently substituted.
- A pointwise equality of integer indices with no K-theory class over the parameter space.
- Assuming the desired analytic/topological equality, index class, or pushforward as structure data.
- Treating nearby topology, bundle, Fredholm, or K-theory APIs as proof of the terminal theorem.

The formal statement must expose concrete family, ellipticity, symbol, analytic-index, and
topological-index interfaces, or record the first precise missing API rather than broaden the claim.
