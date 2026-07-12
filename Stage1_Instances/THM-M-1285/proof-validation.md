# Proof-phase validation record

Item: `S56-M-1285-PROOF`  
Base revision: `4d5664421bb1948968c9c993cd7de255dfcc33fc`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

`Proof.lean` contains real, placeholder-free proof bodies for the radiality,
radial-antitonicity, and conditional measurability leaves of the frozen
profile construction. They are proved directly from equality/order of norms
and composition with `measurable_norm`; no new axiom declaration is added.

The assigned proof phase is **blocked**, not self-tested as complete. The
minimal open root cut remains `M1285-T-PACKAGE`: pinned mathlib has no
Schwarz-rearrangement construction, and this execution did not construct the
generalized-inverse radial profile or prove its measurability and exact
strict-superlevel equimeasurability. Consequently no root theorem, proof-phase
completion receipt, or `.stage1-worker-selftest.json` is emitted.

## Commands and exact results

The two-step `-o` recipe is necessary because dossier modules live outside the
Lake package. It writes only temporary `.olean` files under `/tmp`; pinned
`.lake` artifacts are reused and not mutated.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-1285 -o /tmp/thm-m-1285/Statement.olean ../../Stage1_Instances/THM-M-1285/Statement.lean` | 0 | exact frozen statement elaborated and temporary module emitted |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-1285 lake env lean -R ../../Stage1_Instances/THM-M-1285 ../../Stage1_Instances/THM-M-1285/Proof.lean` | 0 | all three proof bodies elaborated; each reports only mathlib's foundation axioms `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n '\\b(sorry|admit|axiom)\\b' Stage1_Instances/THM-M-1285/Proof.lean` | 1 | no placeholder or axiom declarations found |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1285` | 0 | rank 456; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1285` | 0 | no whitespace errors |

## Reopen condition

Continue from a concrete Lean definition of the distribution function and
generalized inverse. Acceptance needs proof that the induced radial profile is
measurable and that every positive strict superlevel has exactly the original
volume; the two lemmas here then close the radial shape properties without
additional premises.
