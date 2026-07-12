# Statement phase blocker

## Verdict

`S56-M-0569-STATEMENT` remains blocked. No canonical Lean expression was created, and this phase
does not claim a statement receipt, an accepted alternate encoding, proof closure, audit closure,
or theorem completion. The prerequisite intake is also only provisional (`[_]`) in the generated
blueprint and has not received master acceptance.

## Exact claim that must be represented

The intake freezes the classical closed even-dimensional Chern-Gauss-Bonnet equality: for a compact
oriented boundaryless Riemannian manifold, the integral of the convention-normalized Pfaffian of
the Levi-Civita curvature equals its topological Euler characteristic. The statement phase may not
replace this with the surface case, an abstract equality between caller-supplied values, an Euler
class pairing without a checked Chern-Weil bridge, or a proposition that assumes the desired
equality.

## Pinned API audit

The dependency lock pins mathlib to `8a178386ffc0f5fef0b77738bb5449d50efeea95` and Lean to
`v4.29.0`. The narrow source audit found the Riemannian-manifold binder API in
`Mathlib.Geometry.Manifold.Riemannian.Basic`, including `IsRiemannianManifold` and smooth
Riemannian tangent bundles. `StatementInfrastructureProbe.lean` elaborates that available context
using this single import.

The same pinned-tree searches found no declaration or module for a Pfaffian, Chern-Gauss-Bonnet,
Gauss-Bonnet, a Levi-Civita connection/curvature form, or an Euler form. More decisively,
`Mathlib.Geometry.Manifold.PartitionOfUnity` records integration of a differential form over a
manifold as a TODO. The only `eulerChar` declarations found are for incidence algebras and
homological complexes; neither defines the topological Euler characteristic of this manifold.
Thus the two sides of the required equality do not have concrete terms in the pinned environment.

Introducing local uninterpreted `curvature`, `eulerForm`, `integral`, or `eulerCharacteristic`
parameters would elaborate only an abstract substitute and is prohibited by the exact-statement
gate. There is consequently no truthful expression fingerprint, alternate-form transport, or
statement mutation suite to record.

## Validation evidence

Run from repository root on 2026-07-12 (Asia/Shanghai):

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0569` | exit 0; rank 617, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0569/StatementInfrastructureProbe.lean` | exit 0; all three declarations printed by `#check` |
| `git diff --check -- Stage1_Instances/THM-M-0569` | exit 0; no output |

Environment inputs: `Formalizations/Lean/lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; `lake-manifest.json`
SHA-256 `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
The clone's `.lake` is the prescribed symlink to canonical pinned artifacts; it was not modified.

## Retry condition

Retry only after (1) master acceptance of the intake prerequisite, (2) a source-reviewed exact
formula and convention crosswalk, and (3) pinned Lean definitions for the Levi-Civita curvature,
normalized Pfaffian Euler form, oriented top-form integration, and manifold Euler characteristic,
or an immutable compatible external dependency providing those definitions. Then elaborate the
exact proposition and run the required removed-hypothesis, changed-domain, binder-scope, and
boundary-case mutations. Until then the root vector remains `[H1, M4, R4]` and no worker self-test
manifest is warranted.
