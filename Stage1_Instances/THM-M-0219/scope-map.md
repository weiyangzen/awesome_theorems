# Scope map

## Preserved catalog boundary

The repository fixes target `THM-M-0219`, the name `庞加莱半平面模型`, Henri Poincare, the year
1882, and the gloss `双曲几何的另一种模型`. Importance "high" and status `已验证` are catalog
metadata, not source or kernel evidence. Intake preserves the upper-half-plane hyperbolic-model
subject without turning that object description into a theorem.

## Proposition-changing decisions

An approved source correction must select one truth-valued root and freeze:

- the carrier: the complex upper half-plane, a real coordinate half-plane, a projective
  presentation, or another source-defined object, including treatment of its real boundary and
  ideal points;
- whether the primitive geometry is a distance formula, path metric, Riemannian line element,
  conformal structure, incidence/congruence structure, or a checked bundle of these;
- the scale convention, including whether the Riemannian curvature is normalized to `-1`;
- which result makes it a model: metric laws, completeness and simple connectedness, constant
  curvature, geodesic classification, conformality, satisfaction of a named axiom system, or a
  combination with exact dependencies;
- whether the symmetry group is `PSL(2,R)`, `SL(2,R)`, the positive-determinant subgroup of
  `GL(2,R)`, or an orientation-reversing extension, and which fractional-linear action is meant;
- whether equivalence with the Poincare disk is part of the root, a downstream transport, or
  excluded, together with the Cayley map, base point, radius, and normalization; and
- every universe, ordered binder, hypothesis, definition, conclusion clause, boundary convention,
  and degenerate case.

These choices produce different propositions. They form a resolution ledger, not a canonical
statement.

## Candidate families not credited

- Construction of the complex upper half-plane with the Poincare distance
  `2 * arsinh (|z-w| / (2 * sqrt(Im(z) * Im(w))))`.
- Construction from the Riemannian line element `(dx^2 + dy^2) / y^2` and proof that its induced
  distance has the displayed formula.
- Completeness, simple connectedness, or constant curvature `-1` of that Riemannian surface.
- Classification of geodesics as vertical lines and circles orthogonal to the real boundary.
- Satisfaction of a source-selected axiomatization of hyperbolic geometry.
- Isometric real fractional-linear action and an explicit conformal isometry to the disk model.

No item in this list is selected, asserted, or credited at intake.

## Neighbor target boundaries

`THM-M-0217` separately owns the Klein/projective model, and `THM-M-0218` separately owns the
Poincare disk model. A Cayley equivalence may eventually connect the disk and half-plane dossiers,
but neither dossier can inherit the other's statement, source evidence, or proof credit without a
checked source-faithful transport. `THM-M-0220` separately owns the hyperbolic triangle-area
formula and is not the model theorem itself.

## Explicit exclusions

Mere nonemptiness of the upper half-plane, its Euclidean subtype topology, complex-manifold
charts, one metric identity, one ball formula, or a modular-form application is not the complete
model theorem. Euclidean distance on the underlying subset is not the Poincare metric. Nor may a
generic structure store the desired metric, curvature, geodesic, or isometry property as a field
and then project it as a purported proof. The catalog word `已验证` and adjacent API elaboration
supply no H0 or M0 evidence.

## Formal boundary

No canonical Lean expression is frozen. At the pinned mathlib revision, `UpperHalfPlane` is a
complex upper-half-plane type; `UpperHalfPlane.dist_eq` exposes a Poincare distance formula; the
library constructs `MetricSpace` and `ProperSpace` instances; and the real special linear group
acts isometrically through the fractional-linear action. `Complex.UnitDisc` is also available, but
the bounded intake search found no checked Cayley isometry between these model structures. These
are genuine substrate and bounded discovery facts, not an exhaustive anchor audit, exact target
match, or proof of the unidentified catalog root.
