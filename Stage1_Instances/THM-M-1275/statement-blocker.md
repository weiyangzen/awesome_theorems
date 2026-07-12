# Statement gate blocker

Item: `S56-M-1275-STATEMENT`  
Theorem: `THM-M-1275`  
Base revision: `98065785d12e728c9b8ae0c44053eaa498c42ad6`

## Verdict

The exact Lean statement gate is blocked. The intake freezes the classical Yamabe existence claim:
for every smooth compact connected boundaryless manifold of dimension at least three and every
smooth Riemannian metric, some positive smooth conformal factor produces a metric of constant
scalar curvature. The pinned mathlib revision provides smooth Riemannian bundle and manifold
infrastructure, but it provides no definition of scalar curvature, the curvature tensors needed to
define it, or conformal rescaling of a Riemannian metric. A case-insensitive search of every pinned
mathlib source file for `scalar.?curvature`, `ricci`, `riemann.*curvature`, `curvature tensor`,
`conformal metric`, and `conformal.*riemann` returned no matches.

Consequently the root conclusion cannot be expressed with the intended mathematical semantics in
the pinned environment. Introducing an uninterpreted `ScalarCurvature` or `ConformalMetric`
parameter would merely replace the Yamabe theorem by an arbitrary-predicate proposition; defining
the missing differential-geometric theory is proof/infrastructure work beyond this statement node.
Neither is an exact target. There is therefore no truthful canonical declaration, elaborated
expression fingerprint, checked alternate transport, or mutation suite.

## Checked boundary

`StatementInfrastructure.lean` uses the single direct import
`Mathlib.Geometry.Manifold.Riemannian.Basic` and kernel-checks the available types
`Bundle.ContMDiffRiemannianMetric`, `Bundle.RiemannianBundle`,
`IsContMDiffRiemannianBundle`, and
`IsRiemannianManifold`. It declares no theorem, axiom, placeholder, substitute predicate, or proof.
This confirms only the nearest available substrate and receives no statement-completion credit.

## Environment fingerprint

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib Lake pin and checked revision:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from this worker clone on 2026-07-12. Lean ran from `Formalizations/Lean` against the
existing pinned `.lake` symlink; no update, fetch, clone, or build command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1275` | 0 | rank 448; planned; hard-mathlib-anchor lane; theorem incomplete |
| `rg -ni -e 'scalar.?curvature' -e ricci -e 'riemann.*curvature' -e 'curvature tensor' -e 'conformal metric' -e 'conformal.*riemann' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | no match in the complete pinned mathlib source tree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1275/StatementInfrastructure.lean` | 0 | all four Riemannian substrate declarations elaborated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact mathlib revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match the fingerprint above |
| `git diff --check -- Stage1_Instances/THM-M-1275` | 0 | no whitespace errors |

## Retry condition

Retry when an immutable, toolchain-compatible dependency supplies definitions for curvature,
scalar curvature, smooth conformal metric rescaling, and the required transformation interfaces,
or after those foundations are implemented and independently reviewed in the authoritative lane.
Then the statement phase must bind the exact dimension, compactness, connectedness, boundary,
regularity, positivity, exponent, and constancy conventions and run the required structural
mutations and boundary checks.

Until then the first failed gate is exact canonical target elaboration, machine debt remains `M4`,
and theorem completion is false. The assigned phase is not genuinely self-tested to completion, so
no `.stage1-worker-selftest.json` is emitted.
