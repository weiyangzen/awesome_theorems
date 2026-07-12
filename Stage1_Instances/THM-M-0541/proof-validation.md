# THM-M-0541 proof-phase validation

Item: `S56-M-0541-PROOF`  
Base revision: `be98a856ad5cbf322fb2fda71f1506bd05f1d355`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

`Proof.lean` gives a direct proof of the frozen ordered, unreduced integral simplicial-boundary
statement. It constructs the additive boundary on `Finsupp` chains, proves the ordered deletion
identity, pairs the two finite double sums by `(i,j) -> (j,i+1)`, extends square-zero from basis
chains to every chain, and assembles `StatementShape`. There is no imported theorem standing in for
the target and no placeholder or newly declared axiom.

The source repeats the six frozen definitions from `Statement.lean` because the dossier is outside
the Lake module tree; the terminal `#check` checks the proof against that exact in-file target. The
definition bodies and universe/domain/coefficient choices are unchanged from the frozen statement.

## Commands

Commands ran in the worker clone using the existing pinned Lake environment and did not mutate
`.lake`.

| command | exit | outcome |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0541/Proof.lean` | 0 | exact root typechecked; axiom report was `[propext, Classical.choice, Quot.sound]`, with no `sorryAx` |
| `python3 Stage1_Instances/THM-M-0541/check_proof.py` | 0 | exact-root marker, six proof bodies, and forbidden-construct scans passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0541` | 0 | rank 598, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0541` | 0 | no whitespace errors |

This receipt is proof-phase evidence pending master acceptance. It does not claim the later
hermetic validation, independent verification, release, H0/R0, `THEOREM-Z`, or theorem completion.
