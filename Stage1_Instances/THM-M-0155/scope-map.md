# Scope map

## Provisional included claim

- A compact region `D` in the real plane with an oriented boundary that supports a boundary
  integral and the applicable planar change-of-variables/integration theory.
- A real-valued 1-form `P dx + Q dy`, with `P` and `Q` continuously differentiable on an open
  neighborhood of `D` (subject to the exact selected source).
- Counterclockwise orientation on outer boundary components and the induced opposite orientation
  on holes.
- Equality between the boundary circulation and the area integral of
  `partial_x Q - partial_y P` over `D`.

## Decisions required at statement freeze

The statement phase must select one exact source theorem and freeze whether `D` is a simple region,
Jordan domain, regular region, finite union of elementary regions, or a chain; whether its boundary
is piecewise `C1`, piecewise smooth, rectifiable, or Lipschitz; whether holes and disconnected
components are admitted; and whether self-intersection or multiplicity is represented by chains.
It must also freeze openness and regularity assumptions on `P,Q`, compact support if any, the
ambient scalar field, orientation conventions, and the precise line and area integral APIs.

Boundary cases requiring explicit treatment include the empty region, zero-area or degenerate
regions, empty boundary, corners, holes, reversed orientation, and functions defined only on `D`
rather than a neighborhood. Binder order must make the regularity assumptions depend on the chosen
region and neighborhood without hiding those data in an opaque terminal predicate.

## Explicit exclusions

- The divergence/flux form without a checked rotation equivalence to the selected circulation form.
- Green's identities involving the Laplacian, the divergence theorem in arbitrary dimension, or
  the full Stokes theorem as a substituted target.
- Rectangles, disks, or type-I regions alone as a substitute for the selected general region class.
- An abstract hypothesis asserting the desired integral equality or a structure carrying it as a
  field.
- The repository label `已验证`, a source citation, or an adjacent integration API as proof credit.

No Lean target is frozen in this intake. The statement phase must expose concrete region, boundary,
orientation, derivative, and integral objects, or report the precise missing API instead of
weakening the theorem.
