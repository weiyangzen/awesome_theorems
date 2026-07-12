# Statement validation

Base revision: `f53f980e1606a9b2eb406153ede39662661a45c2`.

Validation covers target/manifest consistency, the exact canonical proposition and two explicit
statement mutations, the direct dependency list, structured artifacts, and whitespace. Existing
`.lake` artifacts were used read-only; no update, build, clone, or fetch was run. Successful
elaboration is statement evidence only, not a proof of the target proposition.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1419` | exit 0; rank 688, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1419/OseledetsStatement.lean)` | exit 0; canonical target and both mutations elaborated and printed; no errors or warnings |
| `(cd Formalizations/Lean && lake env lean --deps ../../Stage1_Instances/THM-M-1419/OseledetsStatement.lean)` | exit 0; resolved `Init.olean` and the five pinned direct mathlib module oleans |
| `python3 -m json.tool Stage1_Instances/THM-M-1419/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1419/task-dag.json` | exit 0 |
| scoped Python statement assertions | exit 0; `statement invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1419 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact numbered primary-source selection and independent review,
formal-anchor audit, obligation registry, proof, hermetic replay, and release validation. They
prevent theorem completion but do not invalidate the exact elaborated statement phase.

## Anchor-audit validation

Base revision: `28be4ce7383f582503e6b54f645e2ca0e955d9de`.

The pinned mathlib infrastructure check and immutable external-source audit are detailed in
`anchor-audit.md` and structured in `anchor-audit.json`. The external candidate was not fetched,
built, or added to `.lake`: it requires a different Lean/mathlib closure, and no exact checked
transport is present. Anchor audit is therefore self-tested candidate evidence only, not M0.
