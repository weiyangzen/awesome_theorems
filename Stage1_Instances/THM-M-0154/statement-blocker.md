# Statement gate blocker

Item: `S56-M-0154-STATEMENT`  
Theorem: `THM-M-0154`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted intake freezes the generalized Stokes theorem rather than a Euclidean-box,
divergence, Green, or contour specialization. That exact claim cannot currently be represented by
the pinned Lean API. `Mathlib.Analysis.Calculus.DifferentialForm.Basic` defines `extDeriv` only for
forms on normed vector spaces. Its module TODO explicitly says bundled smooth forms on manifolds
are not defined yet. The manifold boundary module defines `ModelWithCorners.boundary` as a `Set M`;
its TODO explicitly says that making the boundary a submanifold still requires a submanifold
definition. Narrow source searches found no manifold-form integration or manifold-orientation API.

Thus the required objects cannot be connected in one type-correct proposition: a smooth compactly
supported `(n-1)`-form on `M`, its manifold exterior derivative, an outward-normal-first oriented
boundary manifold and smooth inclusion, the pullback along that inclusion, and integration of
top-degree forms over both oriented manifolds. Mathlib's Bochner integral and function-level
`HasCompactSupport` do not fill those semantic interfaces. Defining local opaque replacements or
passing the two integrals as arbitrary functions would be a proxy statement, not an elaboration of
generalized Stokes. Replacing the target with the available box divergence theorem would be a
strict specialization. Neither is credited.

Because no exact expression exists, there is no honest normalized expression hash, minimal target
import set, checked alternate transport, or removed-hypothesis, changed-domain, binder-scope, and
boundary-case mutation suite. The `n = 0` degree convention also remains unresolved. Machine state
stays `M4`; statement and theorem completion are false. No theorem, axiom, `sorry`, opaque proxy,
or proof body was introduced.

## Pinned Lean boundary

`StatementInfrastructure.lean` imports three minimal modules covering the independently available
surfaces and checks `extDeriv`, `ModelWithCorners.boundary`, `MeasureTheory.integral`, and
`HasCompactSupport`. It is feasibility evidence only and receives no statement or proof credit.
The canonical `.lake` artifacts were used read-only; no update, build, clone, fetch, or dependency
mutation was run.

- Base revision: `b66e26872f7b2eb2047782e029b32e32b0ead1d8`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0154` | 0 | rank 653, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | pinned Lean version and commit above |
| `cd Formalizations/Lean && lake --version` | 0 | pinned Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes recorded above and in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `rg` searches of pinned mathlib for Stokes, manifold differential forms, form integration, and manifold orientation | 0/1 | only a box-integral mention and incomplete substrate were found; no generalized manifold Stokes target or required joined API |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0154/StatementInfrastructure.lean` | 0 | all four available substrate types elaborated and printed |
| `python3 -m json.tool Stage1_Instances/THM-M-0154/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `rg -n '(^|[^[:alnum:]_])(sorry|admit)([^[:alnum:]_]|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0154 --glob '*.lean'` | 1 | no Lean proof escape or axiom declaration; exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-0154` | 0 | no scoped whitespace errors |

## Retry condition

Add pinned, kernel-checkable definitions for smooth manifold differential forms and their exterior
derivative, manifold orientation and outward-normal-first boundary orientation, the boundary as a
smooth oriented manifold with inclusion, pullback, and oriented manifold-form integration. The
next statement run can then settle `n = 0`, elaborate and fingerprint the exact target, minimize its
imports, check alternate transports, and execute all required mutations.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
