# Statement gate blocker

Item: `S56-M-0164-STATEMENT`  
Theorem: `THM-M-0164`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted intake freezes the mathematical root as the forward Jacobi-field theorem: the
variation field of a smooth variation through geodesics satisfies the Jacobi equation
`D_t (D_t J) + R(J, gamma') gamma' = 0`, with a convention still to be fixed. The pinned mathlib
revision cannot express that claim using its native differential-geometric interfaces. Repository
and pinned-source searches found smooth Riemannian metrics and general covariant derivatives with a
torsion tensor, but no definition of the Levi-Civita connection, curvature of a covariant
derivative, geodesic/autoparallel curves, covariant differentiation of a dependent vector field
along a curve, geodesic variations, or Jacobi fields.

Those missing notions are semantic parts of the exact target, not proof-only conveniences. Making
them arbitrary parameters or replacing them by opaque `Prop` fields would broaden the theorem to
an abstract implication and would not encode the claim that the operators arise from the given
Riemannian metric and variation. Defining the entire missing differential-geometric stack during a
statement node would likewise require unreviewed mathematical choices about pullback connections,
regularity, parameter domains, and curvature sign. Therefore no exact expression hash, checked
transport, or mutation suite can truthfully be produced in this phase.

`StatementInfrastructure.lean` checks only the nearest native pinned API. It deliberately declares
no theorem, unsupported constant, proof, placeholder, or substitute statement.

## Negative search boundary

The scoped search covered the pinned mathlib `Mathlib/Geometry/Manifold` tree and the repository's
Lean sources for `Jacobi field`, `geodesic variation`, `geodesic`, `LeviCivita`, `curvature`, and
covariant-derivative terminology. The manifold tree contains only these directly relevant files:

- `Mathlib/Geometry/Manifold/Riemannian/Basic.lean` and `PathELength.lean` for metrics and path length;
- `Mathlib/Geometry/Manifold/VectorBundle/CovariantDerivative/Basic.lean` for a general connection;
- `Mathlib/Geometry/Manifold/VectorBundle/CovariantDerivative/Torsion.lean` for torsion.

This is statement-feasibility evidence, not the later immutable external-anchor audit.

## Environment fingerprint

- Repository base revision: `d7b1a45d1590cdafe55436182144e1f35e6b4194`.
- Validation date: 2026-07-12.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib Lake pin and checked revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Infrastructure probe SHA-256:
  `69f24730a2a86457787b04a22351b42c5a75b7a1a18ab94d9515e11ac143ece6`.

## Validation evidence

Lean commands ran from `Formalizations/Lean` with the existing pinned `.lake` artifacts. No update,
fetch, clone, dependency build, or other `.lake` mutation command was used.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0164/StatementInfrastructure.lean` | 0 | the five native metric/connection/torsion/tangent API checks elaborated |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | checked revision equals the manifest pin |
| `sha256sum lean-toolchain lake-manifest.json ../../Stage1_Instances/THM-M-0164/StatementInfrastructure.lean` | 0 | hashes match the environment fingerprint |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0164` | 0 | rank 663, planned, L0/rework-required, theorem incomplete |

## Status boundary

The statement phase is not self-tested to completion. Machine status remains `M4`; exact-statement
acceptance and theorem completion are false. No `.stage1-worker-selftest.json` is emitted.

## Retry condition

Provide a pinned Lean 4 dependency with a compatible, source-audited Levi-Civita/curvature/geodesic
variation API, or first implement and independently review that API in an authorized shared
infrastructure target. Then freeze the curvature convention and parameter domains, elaborate the
native proposition, and run removed-hypothesis, changed-domain, binder-scope, and sign mutations.
