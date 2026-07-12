# Statement phase blocker

## Verdict

`S56-M-0153-STATEMENT` is blocked. No canonical Lean expression, expression fingerprint,
alternate-form transport, or mutation suite can truthfully be produced in the pinned environment.
The intake prerequisite is also only provisional (`[_]`) and has not received master acceptance.
This result claims neither statement completion nor proof, audit, or theorem completion.

## Required exact target

The frozen claim is the closed even-dimensional Chern-Gauss-Bonnet formula: for a compact,
oriented, boundaryless Riemannian manifold, the integral of the convention-normalized Pfaffian of
the Levi-Civita curvature equals the manifold's topological Euler characteristic. A surface-only
Gauss-Bonnet theorem, an Euler-class pairing without a checked Chern-Weil bridge, an equality of
uninterpreted caller-supplied quantities, or a proposition assuming the desired equality would be
a prohibited substitution.

## Pinned API result

The lock pins Lean `v4.29.0` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The minimal import
`Mathlib.Geometry.Manifold.Riemannian.Basic` supplies `IsRiemannianManifold`, smooth Riemannian
tangent-bundle structure, compactness, and a finite-dimensional even-rank predicate.
`StatementInfrastructureProbe.lean` checks that fragment with the pinned kernel.

A scoped case-insensitive search of every pinned mathlib Lean source for Gauss-Bonnet,
Chern-Gauss-Bonnet, Pfaffian, Levi-Civita, Euler form, and Euler characteristic found only
`Algebra/Homology/EulerCharacteristic.lean` and
`Combinatorics/Enumerative/IncidenceAlgebra.lean`. Those APIs describe homological complexes and
finite bounded orders, not the topological Euler characteristic of the Riemannian manifold.
There was no source hit for the other required constructions. Moreover,
`Mathlib.Geometry.Manifold.PartitionOfUnity` explicitly lists defining the integral of a
differential form over a manifold as a TODO. Thus neither side of the required equality can be
formed from concrete pinned definitions.

Adding local uninterpreted definitions for the missing curvature, Pfaffian, integral, or Euler
characteristic would only make a broadened abstract surrogate elaborate. It would not pass the
exact-statement gate. Since no canonical proposition can be formed, the required removed-
hypothesis, changed-domain, binder-scope, and boundary-case mutations have no legitimate subject.

## Validation evidence

Run from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0153` | 0 | rank 652; planned; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned commit `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0153/StatementInfrastructureProbe.lean` | 0 | the three probe declarations elaborate and print |
| scoped pinned-mathlib API search described above | 0 | only the two unrelated Euler-characteristic modules found |
| `git diff --check -- Stage1_Instances/THM-M-0153` | 0 | no whitespace errors |

Environment inputs: `Formalizations/Lean/lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`;
`Formalizations/Lean/lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Base revision is
`b6840b8306a1983491c1963271bd791635c42c3f`. The pre-existing `.lake` symlink reuses canonical
pinned artifacts; no update, fetch, build, or dependency mutation was performed.

## Retry condition

Retry after master acceptance of the intake, an inspected source formula with frozen conventions,
and pinned compatible Lean definitions for the Levi-Civita curvature, normalized Pfaffian Euler
form, oriented integration, and manifold Euler characteristic. Then elaborate the exact target and
run all four required statement mutations. Until that point the root vector remains
`[H1, M4, R4]`, and no worker self-test manifest is warranted.
