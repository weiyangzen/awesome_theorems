# Formal anchor audit

Item: `S56-M-1070-ANCHOR_AUDIT`  
Audit cutoff: `2026-07-12`  
Repository base: `25cf50267d347d2c52825407423be2c479090f93`

## Frozen search

The audit followed the required order: repo-local Lean, pinned mathlib, public Lean 4 projects,
then historical repositories. Queries covered `IsLevyProcess`, `LevyProcess`, both accented and
ASCII spellings, independent/stationary increments, stochastic continuity, and cadlag. The
machine-readable inventory and immutable identifiers are in `anchor-audit.json`.

The repository has no proof body for this target. `Statement.lean` defines the exact predicate and
checks its expansion; that is statement evidence, not a theorem anchor. At mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, source search finds no `IsLevyProcess` or
`LevyProcess` declaration. It does find exact component APIs:

| Candidate | Exact scope | Audit result |
|---|---|---|
| `ProbabilityTheory.HasIndepIncrements` | joint finite-family increment independence | exact clause; locally checked |
| `ProbabilityTheory.hasIndepIncrements_iff_nat` | sequence form of the same clause | useful alternate API; not root closure |
| `HasIndepIncrements.indepFun_sub_sub` | pairwise consequence | checked consequence only; converse not credited |
| `ProbabilityTheory.IdentDistrib` | equal image laws with AE measurability | exact stationary-law vocabulary |
| `MeasureTheory.TendstoInMeasure` | convergence in measure | exact stochastic-continuity vocabulary |

`AnchorAudit.lean` checks these names, proves by `rfl` that the finite-family clause is exactly the
one frozen in `Statement.lean`, and checks the pairwise consequence. `#print axioms` reports the
standard mathlib foundation set `propext`, `Classical.choice`, and `Quot.sound` for both audit
theorems; it reports no target-specific axiom.

## External candidate

The strongest public Lean 4 candidate found is `slink/LeanLevy` at immutable commit
`93b635fba23398bfb1f0db8d220f88172f6900b6`, tree
`5fdad55a9f84ebb7fe2de35eea05480dbbae6d0a`. Its
`LeanLevy/Processes/LevyProcess.lean` source hash is
`fa99538f9865983909718d0d40d389f631de05d242ea27b88bf21d711bff65d0` and defines
`ProbabilityTheory.IsLevyProcess`. The exact-revision upstream CI run `28901735390` succeeded.
The project uses MIT licensing, Lean `v4.29.0-rc3`, and mathlib
`8e096f85f9401f2c359b6708199c0402a980d921`. A regex defense scan found no `sorry`, `admit`,
bodyless `axiom`, `unsafe`, or `implemented_by` in the four audited process files.

This is not an exact target match. LeanLevy requires pointwise `X 0 = 0` and almost-everywhere
cadlag paths, while the frozen target requires almost-everywhere zero and stochastic continuity.
Its structure also does not carry the target's probability-measure or marginal-AE-measurability
clauses. Conversely, it offers substantive results such as `charFun_eq_exp_mul`, but those prove a
different convention. No equivalence wrapper is present or credited.

LeanLevy is not in the pinned Lake closure, so this audit did not clone, fetch, build, or mutate
`.lake`. Its exact upstream CI is `E2` evidence for its own declarations, while the mapping to this
target remains an `E3` non-identical anchor. Integration would require an explicit convention
bridge, a compatible pin, and local checking in a later proof phase.

GitHub repository search also returned the historical `catskillsresearch/grundbegriffe` project.
It is not treated as a viable current Lean 4 candidate: its last push was in 2021, and the attempted
immutable inventory request returned HTTP 403. That access failure is retained rather than turned
into a false negative claim.

## Classification boundary

The anchor-audit inventory is classified and self-tested, but the theorem audit and theorem root
remain open. The vector stays `[H1, M3, R4]`: exact mathlib components exist and a substantial
external near-match exists, but neither closes the canonical predicate as a substantive theorem.
Primary-source convention review, an obligation registry, an exact theorem deliverable, proof,
integration, provenance closure, and independent validation remain downstream work.

## Validation record

No dependency update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1070/AnchorAudit.lean` | 0 | names and exact component wrappers elaborate; axioms are `propext`, `Classical.choice`, `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1070/Statement.lean` | 0 | frozen canonical predicate still elaborates |
| `python3 -m json.tool Stage1_Instances/THM-M-1070/anchor-audit.json` | 0 | inventory JSON valid |
| placeholder regex scan of four immutable LeanLevy process sources | 0 | no matches |
| pinned-mathlib git grep for full Levy-process names | 0 | no matches; negative result scoped to the pinned revision |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1,546-target coverage valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1070` | 0 | rank 512, L0/rework-required, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1070 .stage1-worker-selftest.json` | 0 | no whitespace errors |
