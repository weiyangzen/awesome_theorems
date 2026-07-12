# Statement phase blocker

Item: `S56-M-0155-STATEMENT`

Base revision: `44b9849ef3fd618f97e63d42e60134771f7302b9`

## Gate result

The exact-statement gate is blocked and no canonical Lean declaration is frozen. The intake fixes
the intended theorem family as the circulation form of Green's theorem for a suitably regular
planar region, including induced orientation and possible holes. It also explicitly rejects a
rectangle, disk, type-I region, flux theorem, or abstract equality-bearing structure as a
substitute. The intake dependency has not selected and inspected a primary-source formulation:
edition, theorem/page, exact region class, boundary multiplicity, regularity, and integral
conventions remain open. Choosing any of these here would invent mathematics rather than elaborate
the exact inherited claim.

The pinned mathlib revision has useful adjacent APIs but no discovered public API for the required
general region statement. `Mathlib.MeasureTheory.Integral.DivergenceTheorem` proves a Bochner
divergence formula for boxes and a planar rectangle specialization.
`Mathlib.MeasureTheory.Integral.CurveIntegral.Poincare` defines curve integrals and proves homotopy
invariance of closed one-forms; its proof applies the rectangular divergence theorem to a unit
square. Neither module supplies a type of regular planar regions together with an induced oriented
boundary operator and a boundary integral. Consequently these declarations cannot express the
intake root without narrowing it to a rectangle or replacing it by Poincare/Stokes data.

`statement_probe.lean` records the smallest import found that exposes both relevant surfaces and
elaborates against the pinned environment. It deliberately contains no theorem declaration: a
compiling adjacent or narrowed proposition is not the exact statement gate.

## Validation

The worker reused the existing `Formalizations/Lean/.lake` symlink and did not mutate or fetch Lake
dependencies.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard valid, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets and ordered ranks validated |
| `python3 scripts/stage1_target.py show THM-M-0155` | exit 0; rank 654, planned, theorem completion false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0155/statement_probe.lean` | exit 0; all four pinned declarations elaborated |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean `4.29.0` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-0155` | exit 0; no whitespace errors |

## First failed gate and unblock condition

The first failed gate is rev-5.6 section 5/5.1 exact target identification, before expression
elaboration, serialization, mutation tests, or proof inspection. Unblocking requires an accepted
source formulation with exact locators and a concrete Lean encoding of its region, induced
oriented boundary, and integral conventions. If the selected source uses general regular/Jordan
regions, the missing boundary-integration infrastructure must be implemented or pinned. If master
instead authorizes a rectangle-only theorem, that is a scope change and must be reconciled with the
intake exclusions before a statement receipt can be issued.

No expression hash, environment fingerprint for a canonical target, debt-vector improvement,
accepted receipt, audit completion, or theorem completion is claimed. The phase is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
