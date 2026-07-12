# Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Gaussian curvature is intrinsic: a local isometry of regular surfaces preserves it pointwise | This is an invariance theorem, not a definition of curvature |
| Geometric objects | Smooth regular two-dimensional surfaces in Euclidean three-space, carrying induced metrics | Singular surfaces, arbitrary metric spaces, and higher-dimensional generalizations are excluded from the root |
| Map | A smooth local isometry, equivalently a local map preserving the first fundamental form | Mere homeomorphisms, conformal maps, and area-preserving maps do not suffice |
| Input data | First fundamental form, locally represented by `E dp^2 + 2F dp dq + G dq^2` | Orientation and a choice of unit normal must not affect the result |
| Output | Equality of Gaussian curvature at corresponding points | Mean and individual principal curvatures are extrinsic and are not claimed invariant |
| Coordinate route | Derive curvature from `E`, `F`, `G` and derivatives, then transfer across equal metric data | A raw coordinate identity alone is not the canonical theorem unless linked by checked transports |
| Intrinsic route | Identify extrinsic Gaussian curvature with intrinsic sectional curvature, then use isometry invariance | The stronger Gauss-equation bridge may support the proof but must not replace the root |
| Human source | Gauss 1827, Articles 11-12, with the 1902 Morehead-Hiltebeitel translation consulted | Pinpoint premise and terminology review exists, but independent source review and errata audit remain open |
| Lean surface | Lean 4 plus repository-pinned mathlib | No suitable declaration was identified by the bounded intake search; exact types and imports remain statement work |
| Foundations | Kernel-checked definitions and proof terms | Exact logical, trust, and dependency profiles remain later audit obligations |

## Boundary cases

- A plane and a cylinder are locally isometric and both have zero Gaussian curvature; this is an
  intended example, not a separate root.
- A sphere of positive curvature cannot be developed isometrically onto a plane; this is a
  consequence, not part of the canonical conclusion.
- Reversing orientation changes signed normal-dependent quantities but not Gaussian curvature.
- At a singular parametrization, `E G - F^2` can vanish and the regular-surface statement does not
  apply.

## Anticipated proof architecture

The expected high-level route is: regular surface and induced metric -> curvature definition ->
intrinsic formula or Gauss equation -> local-isometry transport -> pointwise equality. This is a
scope map only. It neither freezes the obligation denominator nor credits any node as proved.

