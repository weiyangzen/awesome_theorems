# Scope map

## Included claim

- A real normed space `E`, with its norm topology and weak topology `sigma(E, E*)`.
- A convex functional `F : E -> (-infinity, +infinity]` (or the source-equivalent extended-real
  encoding selected later).
- Norm lower semicontinuity implies weak lower semicontinuity. The converse follows because the
  norm topology is finer, so the intended terminal statement may be an equivalence.
- The substantive route is that lower level sets of `F` are convex and norm closed, hence weakly
  closed by a separation theorem.

## Decisions reserved for the statement phase

The inspected source must decide whether `E` is Banach or merely normed, whether `F` is proper,
whether `-infinity` is excluded, and whether lower semicontinuity is expressed through closed
sublevel sets, filters/topologies, or sequences. Weak topological lower semicontinuity must not be
silently replaced by weak sequential lower semicontinuity; their equivalence can require extra
hypotheses. Boundary cases for the identically `+infinity` functional and empty sublevel sets must
be retained if allowed by the source.

## Explicit exclusions

- Lower semicontinuity for an arbitrary nonconvex functional.
- Weak sequential lower semicontinuity as a substitute for weak topological lower semicontinuity.
- A theorem about weak continuity, coercivity, existence of minimizers, or the direct method.
- Assuming weak lower semicontinuity and returning it, or packaging it as structure data.
- A finite-dimensional-only statement unless the selected source itself has that scope.
