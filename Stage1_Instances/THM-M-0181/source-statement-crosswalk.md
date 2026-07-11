# Source-statement crosswalk

## Candidate primary source

Richard S. Hamilton, "Three-manifolds with positive Ricci curvature," *Journal of Differential
Geometry* **17** (1982), 255-306, DOI `10.4310/jdg/1214436922`. This is the foundational primary
paper associated with Hamilton's Ricci flow and contains the short-time PDE construction used by
the later convergence argument. The exact theorem/section, printed pages, ordered assumptions, and
any relevant corrections must be inspected from a stable copy before the claim is frozen.

This bibliographic record is a discovery anchor, not an immutable evidence receipt and not `H0`.

## Crosswalk

| Repository metadata | Source-side question | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Hamilton Ricci flow theorem" | could name the foundational short-time result or the paper's three-dimensional convergence result | materially different conclusions and dependencies | metadata gloss selects short-time branch; primary wording still required |
| "short-time existence" | determine closedness, regularity, interval convention, and dependence of `T` | fixes manifold/metric/time binders and conclusion witness | unresolved |
| "uniqueness" | determine literal geometric uniqueness and the role of diffeomorphism gauge | fixes equality relation and DeTurck transport obligations | unresolved |
| no dimension in the gloss | determine whether the local theorem is stated for arbitrary dimension despite the paper title | fixes dimension assumptions and avoids accidental restriction | unresolved |

## Existing formalization boundary

The legacy blueprint points only to broad mathlib manifold, smooth-map, tensor, topology, and
analysis APIs. Those APIs do not themselves establish an exact Ricci-flow theorem. No repo-local or
external Lean declaration is credited during intake; candidate discovery belongs to the later
anchor-audit node.

Before `H0`, a reviewer must record the exact source edition, theorem/section and pages, transcribe
all hypotheses and the conclusion, check errata, crosswalk every component to the canonical claim,
and independently approve the mapping.
