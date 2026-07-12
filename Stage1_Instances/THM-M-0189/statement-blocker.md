# Statement phase blocker

## Verdict

`S56-M-0189-STATEMENT` is blocked before canonical target elaboration. No statement-phase or
theorem completion is claimed.

The intake-selected root is the general Minkowski existence-and-translation-uniqueness theorem for
surface-area measures of full-dimensional convex bodies. Its defining codomain is not merely an
arbitrary map from convex bodies to measures: the surface-area measure must be constructed from
boundary area and outer normals, with a fixed normalization. The repository-pinned mathlib has
finite measures, sphere measures, Bochner integration, and a `ConvexBody` type, but it has no
surface-area-measure or outer-normal/Gauss-map interface capable of expressing the selected root.
Moreover, `ConvexBody` currently requires only a nonempty compact convex carrier; its source has an
explicit TODO for positive convex bodies with nonempty interior.

Introducing an uninterpreted parameter
`surfaceAreaMeasure : ConvexBody E -> Measure (sphere (0 : E) 1)` would elaborate a superficially
similar proposition, but it would erase the theorem's central geometric definition. It is therefore
an abstract substitution, not the exact target, and is rejected by the rev-5.6 statement gate.

## Pinned environment inspection

`StatementInfrastructure.lean` is infrastructure evidence only. It checks the available
`ConvexBody`, `Measure`, `Measure.toSphere`, `integral`, and metric-sphere vocabulary. It also uses
`#check_failure` for representative absent full-dimensionality, surface-area-measure, recognition,
and great-subsphere nonconcentration interfaces. The scoped source search found Hausdorff measure
and Haar-to-sphere constructions, but no outer-normal map, Gauss map for convex-body boundaries, or
surface-area measure.

The source gate is independently open: the intake records a modern general formulation, while the
1903 historical source may use a narrower formulation. The exact edition theorem/page,
normalization, dimension convention, and equivalence of nondegeneracy formulations have not been
frozen. Choosing one without that review would invent source fidelity.

## Failed gate and resumption condition

The first failed gate is the exact-target requirement in sections 2(3) and 5: the canonical claim
cannot be represented without replacing its central geometric object by uninterpreted data.
Consequently, there is no honest elaborated-expression fingerprint, checked alternate transport,
or mutation suite.

Resume after all of the following are available at immutable revisions:

1. a source pinpoint fixing the general Borel-measure theorem, conventions, and boundary cases;
2. a full-dimensional compact convex-body predicate;
3. an a.e. outer-normal/Gauss-map construction on nonsmooth convex-body boundaries;
4. its normalized pushforward surface-area measure on the unit sphere;
5. exact great-subsphere nonconcentration and translation-equivalence encodings.

No `.stage1-worker-selftest.json` is emitted because the assigned exact-target elaboration did not
pass.

