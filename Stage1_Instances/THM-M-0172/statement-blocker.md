# Statement phase blocker

## Verdict

`S56-M-0172-STATEMENT` is blocked before canonical target elaboration. No
statement-phase completion or theorem completion is claimed.

The frozen human claim requires a compact oriented boundaryless Riemannian
manifold of even dimension, the Levi-Civita curvature, its convention-normalized
Pfaffian Euler form, integration of that top-degree form, and a topological or
homological Euler characteristic of the manifold. At the repository-pinned
mathlib revision, the manifold Riemannian surface is present, but the remaining
interfaces required to state that equality are not.

Using an arbitrary real-valued `eulerFormIntegral` and integer-valued
`eulerCharacteristic` as parameters would elaborate, but would merely assume
the two mathematical sides and erase the theorem's defining content. That is
an abstract substitution, so it is explicitly rejected by the rev-5.6 exact
statement gate.

## Pinned environment inspection

The scoped source search found:

- `Mathlib.Geometry.Manifold.Riemannian.Basic`, including
  `IsRiemannianManifold`, `Bundle.RiemannianBundle`, and `TangentSpace`;
- homological-complex and finite-poset notions named Euler characteristic,
  neither of which defines the topological Euler characteristic of a manifold;
- no Chern-Gauss-Bonnet or Gauss-Bonnet declaration, Pfaffian-curvature
  construction, Euler differential form, Levi-Civita curvature interface, or
  manifold top-form integration interface suitable for this target.

`StatementInfrastructure.lean` checks the available Riemannian vocabulary and
uses `#check_failure` for four representative missing identifiers. It is
infrastructure evidence only and is not the canonical target.

## Failed gate and resumption condition

The first failed gate is section 5.1(2): the exact target cannot be expressed
and elaborated in the pinned environment. Consequently there is no honest
elaborated-expression hash, checked alternate transport, or mutation suite.

Resume only after the dependency-legal implementation or immutable pinned
integration of all of the following:

1. Levi-Civita connection and curvature for the selected Riemannian-manifold API;
2. Pfaffian and normalized Euler form with frozen sign and scalar conventions;
3. oriented integration of top-degree differential forms on compact manifolds;
4. a manifold Euler characteristic and the required homology/topology bridge;
5. an exact primary-source formula review fixing normalization, dimension-zero
   behavior, assumptions, and errata.

No `.stage1-worker-selftest.json` is emitted because the assigned exact-target
elaboration did not pass.
