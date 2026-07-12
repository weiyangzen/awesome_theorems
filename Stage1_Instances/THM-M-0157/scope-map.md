# Scope map

## Included theorem family

- A regular surface, or a source-equivalent two-dimensional immersed manifold, in oriented
  Euclidean three-space.
- A chosen orientation/unit normal field and the associated Gauss map into the unit sphere.
- The differential of the Gauss map at a point, with tangent spaces identified as the source
  requires.
- One exact source-selected property: the differential/shape-operator identity, its
  determinant/Gaussian-curvature consequence, or another explicitly located result.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary theorem. It must freeze: local
parametrized patch versus abstract immersed surface; embedded versus immersed hypotheses;
regularity class; orientability and whether the normal is local or global; ambient orientation and
inner product; the sign convention for the shape operator; tangent-space identifications; Gaussian
curvature convention; determinant/Jacobian orientation and absolute-value conventions; and the
pointwise quantifier domain. It must also settle boundary points, nonorientable surfaces, singular
parametrizations, parabolic points, orientation reversal, and whether any global compactness or
degree hypothesis belongs to the selected claim.

These choices change Lean binders, hypotheses, or the conclusion. In particular, `dN = -S`,
`det(dN) = K`, the pullback area formula, and a degree/total-curvature theorem are related but are
not interchangeable statements.

## Explicit exclusions

- Gauss's Theorema Egregium, the Gauss-Bonnet theorem, or the Gauss-Codazzi equations as a
  substitute for the selected Gauss-map proposition.
- A global degree or total-curvature claim substituted for a local differential/Jacobian claim, or
  conversely.
- A hypersurface theorem in arbitrary codimension unless a checked specialization is provided and
  the selected source claim is preserved.
- A structure that assumes the differential/shape-operator or curvature identity as a field.
- A coordinate computation for one particular surface such as a sphere or graph.
- The repository metadata value `已验证` as human-source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose the immersion,
regularity, orientation, normal/Gauss map, derivative, tangent-space maps, and curvature convention
rather than encode the desired identity as an assumption.
