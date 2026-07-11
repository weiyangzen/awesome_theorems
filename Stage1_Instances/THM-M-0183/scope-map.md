# Scope map

## Frozen human claim

For every compact Kahler manifold `X` with vanishing real first Chern class, and every Kahler
cohomology class `kappa` on `X`, there exists a Kahler metric `g` whose Kahler form represents
`kappa` and whose Ricci curvature is zero.

## Included boundary

- `X` is a compact, finite-dimensional complex Kahler manifold without boundary.
- Vanishing means the image of `c1(X)` in real degree-two cohomology is zero.
- `kappa` is an arbitrary prescribed Kahler class, not merely some class.
- The conclusion is existence of a metric compatible with the fixed complex structure, in that
  class, with zero Ricci tensor (equivalently zero Ricci form once the comparison is established).
- Complex dimension zero and disconnected compact manifolds are not silently excluded; the
  statement phase must verify whether the chosen definitions cover them componentwise.

## Exclusions and adjacent results

- Do not replace the root by existence of an unspecified Ricci-flat Riemannian metric.
- Do not assume the desired metric or Ricci-flatness as a hypothesis or hide it in a predicate.
- The full Calabi-Yau theorem prescribing a Ricci form representing `2*pi*c1(X)` is stronger
  context, not a substitute root. Its uniqueness clause likewise receives no root credit here.
- Holonomy `SU(n)`, existence of a nowhere-vanishing holomorphic volume form, Hodge-number
  consequences, singular/noncompact variants, and algebraic Calabi-Yau varieties are excluded.

## Statement-phase obligations

Freeze universes and regularity, native representations of the complex/Kahler structure, compactness,
de Rham cohomology and `c1`, positivity/Kahler classes, metric-to-form association, and Ricci tensor
versus Ricci form. Record minimal pinned imports, an environment fingerprint, exact declaration type,
checked transports, and mutations removing compactness, `c1 = 0`, or prescribed-class membership.

