# Scope map

## Included claim

Let `alpha : I -> R^3` be a sufficiently differentiable unit-speed curve on an open interval, and
work at points where the curvature `kappa = ||alpha''||` is positive. Fix the ambient orientation
and define

```text
T = alpha'
N = T' / kappa
B = T x N
tau = -<B', N>.
```

The included claim is the three frame equations

```text
T' = kappa N
N' = -kappa T + tau B
B' = -tau N.
```

Together these say that the derivative of the column frame `(T, N, B)` is obtained from it by the
skew-symmetric Frenet-Serret coefficient matrix under the displayed sign and column conventions.
The component equations are the root; a matrix equation is an alternate encoding requiring a
checked transport.

## Domains and binders to freeze at statement phase

- The exact differentiability class and whether the theorem is pointwise or quantified on a
  subinterval on which curvature never vanishes.
- A concrete open-interval or one-dimensional manifold encoding, including endpoint behavior.
- Unit-speed as a hypothesis, or an explicit transport from a regular non-unit-speed parameter to
  arc length; the latter must not be silently assumed.
- The Euclidean inner product, norm, ambient orientation, cross product, and derivative encoding.
- Positivity of curvature, which makes the principal normal well-defined, and the exact treatment
  of isolated zero-curvature points.
- The torsion sign, row/column matrix convention, ordered binders, universes, and typeclass inputs.

## Boundary cases

The canonical Frenet frame is not asserted where `kappa = 0`, for a merely regular straight line,
or at interval endpoints without a chosen derivative convention. Reversing ambient orientation or
using `tau = <N', B>` must be transported explicitly. A planar curve is included where the frame
is defined; its torsion is then zero as a consequence, not an additional premise.

## Explicit exclusions

- Only the planar pair of Frenet equations, a constant-curvature special curve, or a numerical
  moving-frame calculation.
- The fundamental theorem of space curves, which reconstructs a curve from curvature and torsion.
- A non-unit-speed formula with omitted speed factors presented as the unit-speed theorem.
- A structure that stores the three desired derivative equations as fields.
- An arbitrary orthonormal frame with an arbitrary skew-symmetric connection matrix detached from
  derivatives of a curve.
