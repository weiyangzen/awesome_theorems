# Intake validation

Base revision: `396f523f7db5499e43d86728d9cfe073ac081dfa`.

This validation covers manifest membership, dossier structure, JSON integrity, a bounded source
and pinned-mathlib name search, and a narrow pinned Lean API probe. Because the repository record
does not identify a unique proposition, no canonical target, expression hash, mutation result,
proof, or formal-anchor closure is claimed. The canonical `.lake` symlink was used read-only; no
update, build, clone, or fetch command was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0359` | exit 0; rank 852, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -i 'mihlin\|mikhlin\|mihlin乘子\|奇异乘子的L\\^p'` over repository sources with generated execution files, instance dossiers, and `.lake` excluded | exit 0; only `Docs/researches/math_theorems.md` contains the target name/gloss |
| `rg -n -i 'mihlin\|mikhlin\|fourier multiplier' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 0; Fourier-multiplier infrastructure found; no Mihlin/Mikhlin name occurrence |
| `python3 -m json.tool Stage1_Instances/THM-M-0359/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0359/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0359/IntakeProbe.lean)` | exit 0; all eight pinned multiplier and `L^p` API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0359 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are intentionally open: pinpoint source selection, attribution review and
independent approval, canonical statement elaboration and mutation tests, discovery and obligation
freezes, exhaustive anchor audit, `L^p` multiplier construction and proof, hermetic replay, and
release acceptance. They prevent theorem completion but do not invalidate a truthful `planned`
intake.
