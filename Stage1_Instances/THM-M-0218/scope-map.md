# Scope map

## Included subject boundary

- A source-selected presentation of the Poincare disk model whose underlying point set is normally
  the open unit disk in the complex plane.
- The exact hyperbolic structure selected by the source: metric, distance, Riemannian line element,
  incidence/geodesic structure, or an explicitly related package.
- The exact meaning of "model of hyperbolic geometry": satisfaction of a chosen axiom system,
  isometry with a separately constructed hyperbolic plane, or another source-defined relation.
- The exact meaning of "conformal": the hyperbolic Riemannian metric is a positive scalar multiple
  of the Euclidean metric, local angle preservation, a complex-analytic formulation, or a checked
  equivalence among these notions.
- Every source-stated conclusion about curvature, completeness, geodesics, automorphisms,
  orientation, topology, or boundary behavior, but only when it is actually part of the selected
  theorem.

These bullets delimit the recognizable subject. They are not an accepted canonical statement.

## Decisions required at statement freeze

1. Select and independently inspect an immutable primary or authoritative source with exact
   definition/theorem/page locators, assumptions, proof boundary, corrections, and errata.
2. Decide whether the point set is `Complex.UnitDisc`, `Metric.ball (0 : Complex) 1`, a real
   two-dimensional disk, or an abstract manifold with a chart; prove any representation transport.
3. Freeze the hyperbolic structure and normalization. Common line elements differing by a constant
   factor change curvature and distance, so the coefficient cannot be filled in by convention.
4. Fix whether the target is a definition package, a metric-space theorem, a Riemannian theorem,
   an axiom-model theorem, an isometry theorem, or a conjunction of independently stated facts.
5. State the model relation and the comparison object. "Hyperbolic geometry" may mean a synthetic
   axiom system, a constant-curvature surface, the upper half-plane model, or an abstract hyperbolic
   plane; these are not definitionally interchangeable.
6. Freeze the conformality predicate, orientation policy, differentiability order, and whether
   conformality is a hypothesis, a conclusion, or built into the metric definition. Mathlib's
   generic `ConformalAt` includes antiholomorphic maps.
7. Decide whether geodesics being Euclidean diameters or boundary-orthogonal circular arcs is part
   of the root, and formalize lines, circles, orthogonality, endpoints at infinity, and uniqueness.
8. Decide whether completeness, simple connectedness, constant curvature, Mobius invariance,
   homogeneity, distance formulas, or metric-ball formulas are root conjuncts or downstream
   consequences.
9. Resolve coincident points, the center, boundary points (which are not disk points), limiting
   ideal points, zero tangent vectors, degenerate geodesics, orientation reversal, and every
   convention-dependent exceptional case.
10. Freeze ordered binders, universes, topology/metric/manifold instances, coercions to `Complex`,
    all hypotheses, the exact conclusion, and credited alternate encodings before proof search.

## Explicit exclusions

- Treating the definition of the open disk, a metric, or a line element alone as the requested
  theorem when no truth-valued property has been source-selected.
- Substituting only conformality, only curvature `-1`, only completeness, only a distance formula,
  only the geodesic description, or only Mobius invariance for an unspecified model theorem.
- Importing the Poincare upper-half-plane metric as if it were already a disk metric or a checked
  equivalence between the two models.
- Replacing this target with the separately cataloged `THM-M-0219` upper-half-plane model or
  `THM-M-0217` Klein model without a checked theorem-specific bridge.
- Using Euclidean distance inherited by `Complex.UnitDisc` as the hyperbolic distance.
- Assuming the desired metric, curvature, completeness, model axioms, conformality, or isometry as
  fields and then merely projecting those fields.
- Crediting a theorem name, the mathlib file title "Poincare disc", adjacent API elaboration, or
  the catalog label `已验证` as statement identity or proof evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.Analysis.Complex.UnitDisc.Basic` defines
`Complex.UnitDisc` as the Euclidean open ball and provides basic operations. A bounded search found
no disk hyperbolic metric, constant-curvature declaration, geodesic package, or Poincare-disk model
theorem. `Mathlib.Analysis.Complex.Conformal` supplies generic local conformality, and
`Mathlib.Analysis.Complex.UpperHalfPlane.Metric` supplies a Poincare metric on a different type.
These are feasibility surfaces only, not an anchor audit, global absence claim, target statement,
transport, or proof.
