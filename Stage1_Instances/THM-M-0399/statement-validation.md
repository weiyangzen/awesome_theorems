# Statement validation record

Item `S56-M-0399-STATEMENT` elaborates the exact constant-one, exponent-`2 + epsilon` target in
`RothStatement.lean`. The three imports are individually necessary for real `rpow`, algebraicity,
and irrationality. The target uses rational values directly, so duplicate numerator-denominator
representations are absent, and `Rat.den` supplies the positive reduced denominator.

Base revision: `9642a08b78caa26afc9022d7c54b838d1baefdd9`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0399` | exit 0; rank 12, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0399/RothStatement.lean` | exit 0; exact `Prop` elaborated and printed |
| `python3 Stage1_Instances/THM-M-0399/check_statement.py` | exit 0; expression SHA-256 `d63a5863b947f4e03f21847e040b9f4980722607ae953749fa2cb7851a492389`; all four mutations killed |
| `python3 -m json.tool Stage1_Instances/THM-M-0399/statement.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0399` | exit 0; no output |

The worker clone reused the scheduler checkout's already materialized `.lake` dependency cache via
a temporary symlink; the command still ran this clone's pinned Lake project and lock file. The
symlink was removed after validation and is not evidence input. No theorem proof, audit completion,
or theorem completion is claimed. Master acceptance remains outstanding.
