# Statement-phase blocker

Item: `S56-M-0006-STATEMENT`  
Theorem: `THM-M-0006`  
Base revision: `093814ff79615377ad01b5275537212b6a345688`

## Verdict

The exact-statement gate is blocked. The only repository claim is "existence of left/right derived
functors" in `Docs/researches/math_theorems.md`. It supplies no primary edition, theorem/page,
domains, variance, additivity or exactness hypotheses, resolution hypotheses, or choice between
degreewise resolution-derived functors and total Kan-extension-derived functors. Selecting any of
those data as canonical would broaden or substitute the source rather than elaborate its exact
target. This is the hard-stop condition in Phase 1 of `skills/execute-stage1-rev56/SKILL.md`.

`StatementCandidate.lean` records the narrowest already-discovered degreewise interpretation with
explicit universes and binders. It has only the two imports required for mathlib's left- and
right-derived abelian APIs. Its successful elaboration proves that this candidate is well typed;
it does not make the candidate source-authorized or canonical. The total-derived interpretation is
not silently substituted.

## Exact blocker and resolution condition

To unblock this node, an authoritative source must identify an edition, theorem/page, assumptions,
and intended construction. The integration lane can then select the corresponding formal target,
check transports from alternate encodings, and run hypothesis/domain/binder and boundary
mutations. Until that happens, the intake classifications `H4` and `M4` remain accurate and no
statement receipt or theorem credit is warranted.

## Validation record

Commands ran in this worker clone. Lean ran from `Formalizations/Lean` using the existing pinned
`.lake` link; no dependency operation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 15 groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0006` | 0 | rank 95, planned, L0/rework-required, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0006/StatementCandidate.lean` | 0 | candidate elaborated; explicit candidate expression printed |
| `lake env lean AwesomeTheorems/Stage1/S1_M_095.lean` | 0 | legacy discovery module elaborated under the pinned environment |

This node was not genuinely completed, so `.stage1-worker-selftest.json` is intentionally absent.
