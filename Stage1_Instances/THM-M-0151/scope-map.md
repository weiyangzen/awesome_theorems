# Scope map

## Included claim family

- Smooth projective varieties `X` of fixed positive dimension `n` and of general type.
- A dimension-only bound for a pluricanonical linear system.
- Birationality of the rational map defined by a multiple of the canonical divisor.
- The precise base field, admissible `r`, and quantifier shape must be copied from the selected
  primary theorem rather than inferred from this intake gloss.

## Decisions required before statement freeze

The statement phase must disambiguate the repository label against an inspected primary source. It
must fix characteristic (expected zero), geometric integrality/normality and smoothness, the meaning
of projective variety and general type, canonical divisor versus canonical sheaf, and whether the
result says `r = r_n`, all `r >= r_n`, or only sufficiently divisible `r`. It must also specify the
linear system's base locus and the exact predicate saying its rational map is birational onto its
image. Dimensions zero and empty/degenerate linear systems require explicit treatment.

## Explicit exclusions

- Finite generation of the canonical ring (the adjacent Hacon-McKernan theorem family).
- Effective numerical bounds in a fixed low dimension unless the source theorem is exactly that.
- Generic finiteness, separation of points, or nonconstancy in place of birationality.
- Assuming the desired birational map or pluricanonical theorem as structure data.
- A theorem about one fixed variety when the source claim is uniform in dimension.

The current mathlib availability of the required birational-geometry interfaces is not asserted at
intake. Missing infrastructure must be recorded at statement/anchor audit, not hidden by weakening
the claim.

