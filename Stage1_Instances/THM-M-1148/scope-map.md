# Scope map

## Included claim

- A disk in the complex plane with center `c` and radius `R > 0`, its boundary circle, and its
  closed disk.
- Continuous real-valued boundary data `g` on that circle.
- The extension obtained by integrating `g` against the disk's Poisson kernel with normalized
  angular/circle measure.
- Harmonicity in the open disk, continuity on the closed disk, and equality to `g` on the circle.
- The corresponding interior value formula; uniqueness may be included only if the selected source
  states it as part of the same theorem.

## Decisions deferred to statement phase

The inspected primary source must fix the unit-disk versus arbitrary-disk presentation, angular
versus circle-average normalization, real versus complex boundary values, the precise regularity
assumption, and whether boundary agreement is pointwise equality of a continuous extension or a
radial/nontangential limit. Binder order, universes, and treatment of `R <= 0` must then be explicit.
An arbitrary-radius statement should either use the source formula directly or provide a checked
transport from the unit disk.

## Explicit exclusions

- The Poisson summation formula, Poisson point process, Poisson equation, or half-plane formula.
- Merely reproducing harmonic functions already assumed harmonic, without constructing the
  Dirichlet extension from boundary data.
- A mean-value theorem or formula for an existing harmonic function as a substitute for existence,
  continuity to the boundary, and boundary trace.
- The `THM-M-1154` statement-shape package or its checked adjacent anchors as proof of this target.
- Measurable or `L^p` boundary data variants unless separately transported to the continuous-data
  theorem with all boundary conclusions preserved.

The exact Lean target must use concrete mathlib harmonicity, circle integration, Poisson kernel,
continuity, ball, closed-ball, and sphere APIs, or record a precise missing-API blocker.
