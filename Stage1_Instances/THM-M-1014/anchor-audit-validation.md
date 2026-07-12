# Anchor-audit validation record

Item: `S56-M-1014-ANCHOR_AUDIT`  
Base revision: `21b5f8a135c40b3fc4f9987beee433d2ebd8bd43`  
Audit cutoff: 2026-07-12

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains an exact terminal
candidate:
`MeasureTheory.ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous` in
`Mathlib.MeasureTheory.Measure.ProbabilityMeasure`. Its binders and conclusion match the frozen
probability-measure target. `AnchorAudit.lean` restates that target independently and checks the
one-step application. The terminal body is explicit: it passes through mathlib's weak-topology
integral characterization and the pushforward integral identity. The local axiom report contains
only `propext`, `Classical.choice`, and `Quot.sound`, with no custom axiom or `sorryAx`.

`ProbabilityMeasure.continuous_map` is an equivalent topological anchor backed by the same terminal
body. `TendstoInDistribution.continuous_comp` is the checked random-variable/law corollary, not a
replacement for the frozen measure-level root. The historical `S1_M_293` wrapper also delegates to
the same declaration, but rev-5.6 treats it only as discovery input.

The external search found an immutable use in
`mostlyharmfuleconometrics/lean-hansen-econometrics@b05e2b8e582f628155b69e441299716a7d1f3a7a`.
Its `score_sampleCrossMoment_tendstoInDistribution_multivariateGaussian` applies the mathlib
random-variable corollary to a continuous coordinate map. It is a credible client example, not an
independent terminal proof, and adding it as a dependency would provide no new closure. Its source
was inspected at the immutable commit; metadata retrieval timed out, so its toolchain and complete
trust closure are deliberately not claimed.

The candidate is therefore ready for the obligation-tree and proof phases as a unique pinned
terminal body. The anchor audit itself assigns no accepted proof credit and makes no theorem
completion claim.

## Commands and exact results

All Lean checks reused existing pinned Lake artifacts. No update, build, clone, fetch, dependency
installation, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard passed: 15 groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1014` | 0 | rank 293, planned, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg` over repo-local and pinned dependency Lean sources for the exact declaration and continuous-mapping names | 0 | exact terminal body found in pinned mathlib; local legacy wrappers delegate to it; no distinct pinned external body found |
| Sourcegraph search for `TendstoInDistribution.continuous_comp` | 0 | 7 matches; mathlib and three Hansen files; response SHA-256 `abc3bd7b8982fbcb05d3521f380a92a37f6842763c1a82d9ff2e7c9fd457c981` |
| GitHub REST repository search for the quoted theorem name plus Lean 4 | 0 | `total_count=0`, `incomplete_results=false`; response SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| immutable raw inspection of Hansen `Chapter7Asymptotics/Normality.lean` | 0 | continuous-composition client located at lines 237-252; source SHA-256 `ae043208a2b57e1f76160cd4e60f00aee5fe799d9c98862e58d32b0a6b861ba3` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1014/AnchorAudit.lean` | 0 | independently restated exact target and four pinned declarations elaborated; axiom report was exactly `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1014/Statement.lean` | 0 | frozen target and three statement mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-1014/check_anchor_audit.py` | 0 | pin, source hash, frozen-target clauses, five candidate classes, and status boundary agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-1014/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1014 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

## Boundary

This bounded audit is self-tested pending master acceptance. Public search coverage is not claimed
exhaustive. Human-source `H0`, the frozen obligation registry, accepted proof and composition
receipts, hermetic replay, readability review, independent verification, `AUDIT-Z`, and `THEOREM-Z`
all remain downstream.
