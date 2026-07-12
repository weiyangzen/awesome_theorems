# Statement gate blocker

Item: `S56-M-0178-STATEMENT`

Base revision: `c5e497a7dda44b669ff85eaf30ad2ec5da8085c3`

## Verdict

The exact Lean statement cannot truthfully be frozen from the available source record. The
repository name, "Bochner technique," denotes a method rather than a proposition, while the only
repository gloss, "the relation between harmonic forms and curvature," leaves the form degree,
curvature operator, identity or consequence, and global hypotheses unspecified. The intake names
two primary-source candidates but records no inspected theorem/page/display that selects between
them. Choosing a familiar vanishing theorem would therefore broaden or substitute the target.

This is the first failed rev-5.6 statement gate: canonical human claim selection. The retry
condition is an inspected, stable primary-source copy with one identified theorem/display and a
crosswalk fixing its ordered assumptions, definitions, curvature and Laplacian signs, boundary
conditions, and exact conclusion.

## Pinned Lean boundary

The worker reused Lean `v4.29.0` and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; it did not update or mutate `.lake`. A scoped source
search found no occurrence of a Bochner/Weitzenbock formula, Hodge Laplacian, harmonic differential
form, Ricci-curvature tensor, rough Laplacian, or connection Laplacian in pinned mathlib. The nearby
module `Mathlib.Geometry.Manifold.Riemannian.Basic` supplies only Riemannian-manifold and bundle
substrate. `StatementInfrastructure.lean` checks that narrow import without representing it as the
target.

Consequently no canonical Lean expression, expression hash, alternate-encoding transport, or
required removed-hypothesis/domain/binder/boundary mutation suite exists. The machine status stays
`M4`; no proof, audit, or theorem-completion credit is claimed. No worker self-test manifest is
emitted because the assigned statement phase is blocked rather than self-tested.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0178` | exit 0; rank 669, planned, theorem complete false |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i --glob '*.lean' 'Bochner formula\|Bochner identity\|Weitzenb.ck\|HodgeLaplacian\|Hodge Laplacian\|harmonic (one-)?form\|harmonic differential\|RicciCurvature\|Ricci curvature\|ricciTensor\|ricci tensor\|rough Laplacian\|connection Laplacian' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1, the expected ripgrep no-match result |
| first `lake env lean ../../Stage1_Instances/THM-M-0178/StatementInfrastructure.lean` attempt | exit 1; `RiemannianBundle` needed its actual `Bundle.RiemannianBundle` namespace; corrected without changing the mathematical boundary |
| `lake env lean ../../Stage1_Instances/THM-M-0178/StatementInfrastructure.lean` (from `Formalizations/Lean`) | exit 0; the three adjacent pinned declarations elaborate |
| `git diff --check -- Stage1_Instances/THM-M-0178` | exit 0; no output |
