# Exact-statement gate: blocked

Item: `S56-M-0181-STATEMENT`  
Theorem: `THM-M-0181`  
Base revision: `bd4f335d8afb4d242d9df61f9d79a60034c17dfc`

## Decision

The exact Hamilton short-time Ricci-flow target cannot be truthfully frozen from the accepted
intake or elaborated in the pinned Lean environment. The repository gloss says only "short-time
existence and uniqueness." The intake correctly leaves unresolved the primary-source theorem and
pages, closed versus complete noncompact scope, dimension, boundary assumptions, regularity and
time interval, and literal versus gauge-mediated uniqueness. These choices change the ordered
binders, hypotheses, conclusion, and boundary cases. Selecting them here would invent missing
mathematics rather than elaborate an exact source claim.

There is also a formal object-model blocker. Pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides Riemannian metrics and smooth Riemannian
manifold infrastructure, but repository and pinned-source searches found no Ricci tensor or Ricci
flow declaration. Consequently the equation `partial_t g = -2 Ric(g)` and its geometric
uniqueness conclusion cannot currently be expressed using the pinned library's concrete APIs.

The legacy `AwesomeTheorems.Stage1.S1_M_129.StatementShape` is not an exact target. Its own source
models the initial metric, Ricci tensor, PDE, initial condition, and uniqueness merely as `Prop`
fields. Quantifying over that record asks those fields as assumptions/data and does not state
Hamilton's theorem. Reusing it would substitute an abstract proposition boundary for Ricci flow,
which rev-5.6 forbids.

## Checked Lean boundary

`StatementProbe.lean` has the single import
`Mathlib.Geometry.Manifold.Riemannian.Basic`. It checks the available `RiemannianMetric`,
`ContMDiffRiemannianMetric`, `IsManifold`, and `CompactSpace` interfaces and elaborates a
time-indexed family of Riemannian metrics. This is substrate evidence only. It deliberately adds
no Ricci surrogate, axiom, proof placeholder, or canonical theorem.

Environment fingerprint:

- validation date: 2026-07-12;
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
- mathlib pin and checked revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`;
- existing canonical `.lake` artifacts were reused without update, fetch, clone, or build.

## Validation record

Commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0181/StatementProbe.lean` | 0 | pinned Riemannian substrate and time-indexed metric family elaborated |
| `lake env lean AwesomeTheorems/Stage1/S1_M_129.lean` | 0 | legacy discovery module elaborated; no exact-statement credit assigned |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | exact pinned mathlib revision shown above |
| `rg` for `Ricci`, `RicciFlow`, and `ricci_flow` in pinned mathlib Lean sources | 1 | no matching concrete Ricci API; exit 1 denotes no matches |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0181` | 0 | rank 129, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0181` | 0 | no whitespace errors |

## Gate result and retry condition

First failed gate: section 5 canonical human claim and exact Lean target. Machine status remains
`M4`; no expression fingerprint, checked alternate transport, or meaningful removed-hypothesis,
domain, binder-scope, and boundary mutations can be issued before the target exists.

Retry after an authoritative primary-source edition and pinpoint theorem freeze all assumptions and
the uniqueness notion, and after compatible pinned Lean APIs (or an approved pinned external
dependency) provide concrete smooth metric, Ricci tensor, time derivative, and Ricci-flow objects.

The assigned phase is blocked, not self-tested complete, so no `.stage1-worker-selftest.json` is
emitted. This artifact advances no anchor-audit, obligation-tree, proof, validation, release, or
theorem-completion state.
